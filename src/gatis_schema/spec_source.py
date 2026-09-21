"""Read the vendored GATIS spec snapshot into typed records.

This is the input layer for model generation. It reads `spec/workbook/*.csv` --
a pinned export of the upstream Google Sheet, see `spec/README.md` -- and does no
interpretation beyond parsing presence cells. Normalising enum values, resolving
units and emitting Pydantic feature models all happen downstream of here.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Iterator, Sequence
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, Field

from gatis_schema.presence import PresenceRule

SPEC_DIR = Path(__file__).resolve().parents[2] / "spec"

# Feature class -> (types tab, fields tab). The four core files of section 3.1.
FEATURE_CLASSES: dict[str, tuple[str, str]] = {
    "node": ("nodes-types.csv", "nodes-fields.csv"),
    "edge": ("edges-types.csv", "edges-fields.csv"),
    "point": ("points-types.csv", "points-fields.csv"),
    "zone": ("zones-types.csv", "zones-fields.csv"),
}


class SpecDefect(BaseModel):
    """An upstream cell the reader could not interpret.

    Collected rather than raised: the workbook is a live drafting document, and a
    snapshot has to load so the defect can be reported. Generation refuses on a
    non-empty defect list.
    """

    feature_class: str
    field: str
    column: str
    value: str
    problem: str


class FeatureType(BaseModel):
    """One allowed value of `edge_type` / `node_type` / `point_type` / `zone_type`."""

    name: str
    description: str = ""
    tier: int | None = None
    notes: str = ""
    proposed_change: str = ""


class FieldSpec(BaseModel):
    """One row of a `*_Fields` tab: a field and its presence per feature type."""

    name: str
    description: str = ""
    type: str = ""
    valid: str = ""
    listed_values: str = ""
    example: str = ""
    provenance: str = ""
    osm_mapping: str = ""
    notes: str = ""
    presence: dict[str, PresenceRule] = Field(default_factory=dict)

    def applies_to(self, feature_type: str, tier: int) -> bool:
        rule = self.presence.get(feature_type)
        return rule is not None and rule.at(tier).value != "forbidden"


class FeatureClassSpec(BaseModel):
    """The types and fields for one of the four core files."""

    name: str
    types: list[FeatureType]
    fields: list[FieldSpec]
    defects: list[SpecDefect] = Field(default_factory=list)

    @property
    def type_names(self) -> list[str]:
        return [t.name for t in self.types]

    @property
    def field_names(self) -> list[str]:
        return [f.name for f in self.fields]

    @property
    def duplicate_field_names(self) -> list[str]:
        """Field names appearing on more than one row.

        An upstream defect rather than a parse failure: the Points_Fields tab lists
        `impediment`, `surface_issue` and `other_issue` twice, with value sets that
        disagree. Surfaced so generation can refuse rather than silently pick one.
        """
        seen: dict[str, int] = {}
        for name in self.field_names:
            seen[name] = seen.get(name, 0) + 1
        return sorted(name for name, count in seen.items() if count > 1)

    @cached_property
    def presence_columns(self) -> list[str]:
        """Feature types the `*_Fields` tab actually has a presence column for."""
        columns: dict[str, None] = {}
        for field in self.fields:
            for type_name in field.presence:
                columns.setdefault(type_name, None)
        return list(columns)

    @property
    def types_without_fields(self) -> list[str]:
        """Declared types with no presence column, so no fields at all -- not even an id.

        Upstream drift between the `*_Types` and `*_Fields` tabs.
        """
        return sorted(set(self.type_names) - set(self.presence_columns))

    @property
    def fields_without_types(self) -> list[str]:
        """Presence columns naming something the `*_Types` tab does not declare."""
        return sorted(set(self.presence_columns) - set(self.type_names))


class MetadataField(BaseModel):
    """One row of the Metadata tab: a `metadata.json` key."""

    name: str
    presence: str = ""
    description: str = ""
    type: str = ""
    valid: str = ""
    listed_values: str = ""
    example: str = ""


class SourcePin(BaseModel):
    """The Drive revision one snapshot source was taken at."""

    id: str
    name: str
    drive_version: str
    modified_time: str
    tab_count: int | None = None


class Repair(BaseModel):
    """One deliberate correction applied to a snapshot cell on read."""

    feature_class: str
    field: str
    columns: list[str]
    match_prefix: str = ""
    reason: str


class RepairSet(BaseModel):
    """`spec/repairs.json`: every departure from the verbatim snapshot."""

    blank_presence: list[Repair] = Field(default_factory=list)

    def blanks_for(self, feature_class: str, field: str) -> list[Repair]:
        return [
            repair
            for repair in self.blank_presence
            if repair.feature_class == feature_class and repair.field == field
        ]


class Manifest(BaseModel):
    """`spec/MANIFEST.json`: what was fetched, from where, and at which revision."""

    fetched_at: str
    sources: dict[str, SourcePin]
    files: list[dict[str, object]] = Field(default_factory=list)


class SpecSnapshot(BaseModel):
    """The whole vendored snapshot, parsed."""

    manifest: Manifest
    feature_classes: dict[str, FeatureClassSpec]
    metadata_fields: list[MetadataField]
    repairs_applied: list[Repair] = Field(default_factory=list)

    @property
    def defects(self) -> list[SpecDefect]:
        """Every cell the reader could not interpret, across all feature classes."""
        return [
            defect
            for spec in self.feature_classes.values()
            for defect in spec.defects
        ]

    @property
    def workbook_version(self) -> str:
        """The Drive revision of the workbook this snapshot was taken from."""
        return self.manifest.sources["workbook"].drive_version


class SpecReader:
    """Loads `SpecSnapshot` from a spec directory."""

    def __init__(self, spec_dir: Path | str = SPEC_DIR) -> None:
        self.spec_dir = Path(spec_dir)

    def load(self) -> SpecSnapshot:
        self._applied: list[Repair] = []
        feature_classes = {
            name: self._feature_class(name, types_csv, fields_csv)
            for name, (types_csv, fields_csv) in FEATURE_CLASSES.items()
        }
        return SpecSnapshot(
            manifest=self.manifest,
            feature_classes=feature_classes,
            metadata_fields=self._metadata_fields(),
            repairs_applied=self._applied,
        )

    @cached_property
    def repairs(self) -> RepairSet:
        path = self.spec_dir / "repairs.json"
        if not path.exists():
            return RepairSet()
        with path.open() as handle:
            return RepairSet.model_validate(json.load(handle))

    @cached_property
    def manifest(self) -> Manifest:
        with (self.spec_dir / "MANIFEST.json").open() as handle:
            return Manifest.model_validate(json.load(handle))

    def _rows(self, filename: str) -> list[list[str]]:
        with (self.spec_dir / "workbook" / filename).open(newline="") as handle:
            # Cells are stripped here: three field names in Edges_Fields carry
            # trailing whitespace upstream (`ped_traffic_control `), which would
            # otherwise produce unreachable fields.
            return [[cell.strip() for cell in row] for row in csv.reader(handle)]

    def _feature_class(
        self, name: str, types_csv: str, fields_csv: str
    ) -> FeatureClassSpec:
        defects: list[SpecDefect] = []
        return FeatureClassSpec(
            name=name,
            types=list(self._types(types_csv)),
            fields=list(self._fields(fields_csv, name, defects)),
            defects=defects,
        )

    def _types(self, filename: str) -> Iterator[FeatureType]:
        rows = self._rows(filename)
        header, body = rows[0], rows[1:]
        index = _column_index(header)
        for row in body:
            type_name = _cell(row, index.get("Name"))
            if not type_name:
                continue
            tier = _cell(row, index.get("Tier"))
            yield FeatureType(
                name=type_name,
                description=_cell(row, index.get("Description")),
                tier=int(tier) if tier.isdigit() else None,
                notes=_cell(row, index.get("Internal Notes")),
                proposed_change=_cell(row, index.get("Proposal For Change"))
                or _cell(row, index.get("Proposal for Change")),
            )

    def _fields(
        self, filename: str, feature_class: str, defects: list[SpecDefect]
    ) -> Iterator[FieldSpec]:
        rows = self._rows(filename)
        # Row 0 is a banner explaining the Valid/Listed Values columns; row 1 is the
        # real header, whose leading columns are the feature type names.
        header, body = rows[1], rows[2:]
        index = _column_index(header)
        first_attribute = index["Name"]
        # Keep each type's column position: a blank cell in the prefix would
        # otherwise shift every presence value one type to the left.
        type_columns = [
            (position, label)
            for position, label in enumerate(header[:first_attribute])
            if label
        ]

        for row in body:
            field_name = _cell(row, first_attribute)
            if not field_name:
                continue
            yield FieldSpec(
                name=field_name,
                description=_cell(row, index.get("Description")),
                type=_cell(row, index.get("Type")),
                valid=_cell(row, index.get("Valid")) or _cell(row, index.get("Valid Values")),
                listed_values=_cell(row, index.get("Listed Values")),
                example=_cell(row, index.get("Example")),
                provenance=_cell(row, index.get("Provenance")),
                osm_mapping=_cell(row, index.get("OSM Mapping")),
                notes=_cell(row, index.get("Notes")),
                presence=_presence(
                    row,
                    type_columns,
                    feature_class,
                    field_name,
                    defects,
                    self._blanked(feature_class, field_name, row, first_attribute),
                ),
            )

    def _metadata_fields(self) -> list[MetadataField]:
        rows = self._rows("metadata.csv")
        header, body = rows[1], rows[2:]
        index = _column_index(header)
        fields = []
        for row in body:
            name = _cell(row, index.get("Name"))
            if not name:
                continue
            fields.append(
                MetadataField(
                    name=name,
                    presence=_cell(row, index.get("presence")),
                    description=_cell(row, index.get("Description")),
                    type=_cell(row, index.get("Type")),
                    valid=_cell(row, index.get("Valid")),
                    listed_values=_cell(row, index.get("Listed Values")),
                    example=_cell(row, index.get("Example")),
                )
            )
        return fields


    def _blanked(
        self,
        feature_class: str,
        field_name: str,
        row: Sequence[str],
        first_attribute: int,
    ) -> set[str]:
        """Presence columns this row's repairs say to treat as empty."""
        blanked: set[str] = set()
        for repair in self.repairs.blanks_for(feature_class, field_name):
            cells = [c for c in row[:first_attribute] if c]
            if repair.match_prefix and not any(
                cell.startswith(repair.match_prefix) for cell in cells
            ):
                continue
            blanked.update(repair.columns)
            if repair not in self._applied:
                self._applied.append(repair)
        return blanked


def _column_index(header: Sequence[str]) -> dict[str, int]:
    """Map header label -> column. Later duplicates lose to the first."""
    index: dict[str, int] = {}
    for position, label in enumerate(header):
        if label and label not in index:
            index[label] = position
    return index


def _cell(row: Sequence[str], position: int | None) -> str:
    if position is None or position >= len(row):
        return ""
    return row[position]


def _presence(
    row: Sequence[str],
    type_columns: Sequence[tuple[int, str]],
    feature_class: str,
    field_name: str,
    defects: list[SpecDefect],
    blanked: set[str],
) -> dict[str, PresenceRule]:
    rules = {}
    for position, type_name in type_columns:
        if type_name in blanked:
            continue
        value = _cell(row, position)
        try:
            rule = PresenceRule.parse(value)
        except ValueError as error:
            defects.append(
                SpecDefect(
                    feature_class=feature_class,
                    field=field_name,
                    column=type_name,
                    value=value,
                    problem=str(error),
                )
            )
            continue
        if rule is not None:
            rules[type_name] = rule
    return rules
