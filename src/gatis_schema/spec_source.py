"""Read the vendored GATIS spec snapshot into typed records.

This is the input layer for model generation. It reads `spec/specification/*.json`
-- a pinned copy of dotbts/BPA's published v1.0 spec, see `spec/README.md` -- and
does no interpretation beyond resolving presence arrays. Normalising enum values,
resolving units and emitting Pydantic feature models all happen downstream of here.
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Sequence
from functools import cached_property
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from gatis_schema.presence import PresenceRule

SPEC_DIR = Path(__file__).resolve().parents[2] / "spec"

# Feature class -> the published file it is defined in. The four core files of
# section 2.1, singular here because a model is one feature.
FEATURE_CLASSES: dict[str, str] = {
    "node": "nodes.json",
    "edge": "edges.json",
    "point": "points.json",
    "zone": "zones.json",
}


class SpecDefect(BaseModel):
    """An upstream entry the reader could not interpret.

    Collected rather than raised: the spec is a live document, and a snapshot has
    to load so the defect can be reported. Generation refuses on a non-empty
    defect list.
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
    # v1.0 type-level facts. `allowed_on_road` says the type may be expressed as a
    # left/right modifier on a road edge rather than as its own feature, and
    # `forbidden_on_road` lists the fields that representation may not carry.
    allowed_on_road: bool = False
    forbidden_on_road: list[str] = Field(default_factory=list)
    allowed_uses: list[str] = Field(default_factory=list)
    prohibited_uses: list[str] = Field(default_factory=list)


class FieldSpec(BaseModel):
    """One published attribute: a field and its presence per feature type."""

    name: str
    description: str = ""
    type: str = ""
    listed_values: list[str] = Field(default_factory=list)
    example: str = ""
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
        """Field names appearing more than once. Empty in v1.0; pinned by a test."""
        seen: dict[str, int] = {}
        for name in self.field_names:
            seen[name] = seen.get(name, 0) + 1
        return sorted(name for name, count in seen.items() if count > 1)

    @cached_property
    def presence_columns(self) -> list[str]:
        """Feature types some field carries a presence entry for."""
        columns: dict[str, None] = {}
        for field in self.fields:
            for type_name in field.presence:
                columns.setdefault(type_name, None)
        return list(columns)

    @property
    def types_without_fields(self) -> list[str]:
        """Declared types with no presence entry anywhere, so no fields at all."""
        return sorted(set(self.type_names) - set(self.presence_columns))

    @property
    def fields_without_types(self) -> list[str]:
        """Presence entries naming something the file does not declare as a type.

        Upstream drift: `edges.json` still carries a `virtual_link` column for a
        type v1.0 removed.
        """
        return sorted(set(self.presence_columns) - set(self.type_names))

    @property
    def dangling_forbidden_on_road(self) -> dict[str, list[str]]:
        """Type -> fields it forbids on-road that are not attributes at all.

        Upstream drift: sidewalk, bikeway and multi_use_path all list
        `road_associated`, which v1.0 removed.
        """
        known = set(self.field_names)
        return {
            t.name: missing
            for t in self.types
            if (missing := [f for f in t.forbidden_on_road if f not in known])
        }


class MetadataField(BaseModel):
    """One key of `metadata.json`, whose presence varies by tier only."""

    name: str
    description: str = ""
    type: str = ""
    listed_values: list[str] = Field(default_factory=list)
    example: str = ""
    presence: PresenceRule | None = None


class Repair(BaseModel):
    """One deliberate correction applied to a snapshot value on read.

    v1.0 publishes `listed_values` by splitting a spreadsheet cell on newlines, and
    six edge cells do not survive it: hard-wrapped definitions fragment, blank lines
    become empty values, and run-together lines stay fused. Recorded here rather
    than guessed inline, so every departure from the verbatim snapshot is visible.
    """

    feature_class: str
    field: str
    values: list[str]
    reason: str


class RepairSet(BaseModel):
    """`spec/repairs.json`: every departure from the verbatim snapshot."""

    listed_values: list[Repair] = Field(default_factory=list)

    def values_for(self, feature_class: str, field: str) -> Repair | None:
        return next(
            (
                repair
                for repair in self.listed_values
                if repair.feature_class == feature_class and repair.field == field
            ),
            None,
        )


class SourcePin(BaseModel):
    """The upstream commit this snapshot was taken at."""

    repo: str
    url: str
    commit: str
    commit_date: str
    commit_subject: str = ""


class Manifest(BaseModel):
    """`spec/MANIFEST.json`: what was fetched, from where, and at which commit."""

    fetched_at: str
    source: SourcePin
    files: list[dict[str, object]] = Field(default_factory=list)


class SpecSnapshot(BaseModel):
    """The whole vendored snapshot, parsed."""

    manifest: Manifest
    feature_classes: dict[str, FeatureClassSpec]
    metadata_fields: list[MetadataField]
    repairs_applied: list[Repair] = Field(default_factory=list)

    @property
    def defects(self) -> list[SpecDefect]:
        """Every entry the reader could not interpret, across all feature classes."""
        return [
            defect for spec in self.feature_classes.values() for defect in spec.defects
        ]

    @property
    def spec_version(self) -> str:
        """The upstream commit this snapshot was taken from."""
        return self.manifest.source.commit


class SpecReader:
    """Loads `SpecSnapshot` from a spec directory."""

    def __init__(self, spec_dir: Path | str = SPEC_DIR) -> None:
        self.spec_dir = Path(spec_dir)

    def load(self) -> SpecSnapshot:
        self._applied: list[Repair] = []
        feature_classes = {
            name: self._feature_class(name, filename)
            for name, filename in FEATURE_CLASSES.items()
        }
        return SpecSnapshot(
            manifest=self.manifest,
            feature_classes=feature_classes,
            metadata_fields=list(self._metadata_fields()),
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

    def _document(self, filename: str) -> dict[str, Any]:
        with (self.spec_dir / "specification" / filename).open() as handle:
            document: dict[str, Any] = json.load(handle)
        return document

    def _feature_class(self, name: str, filename: str) -> FeatureClassSpec:
        document = self._document(filename)
        defects: list[SpecDefect] = []
        return FeatureClassSpec(
            name=name,
            types=list(_types(document["types"])),
            fields=list(self._fields(document["attributes"], name, defects)),
            defects=defects,
        )

    def _fields(
        self,
        attributes: Sequence[dict[str, Any]],
        feature_class: str,
        defects: list[SpecDefect],
    ) -> Iterator[FieldSpec]:
        for attribute in attributes:
            name = _text(attribute.get("name"))
            if not name:
                continue
            repair = self.repairs.values_for(feature_class, name)
            if repair is not None and repair not in self._applied:
                self._applied.append(repair)
            yield FieldSpec(
                name=name,
                description=_text(attribute.get("description")),
                type=_text(attribute.get("type")),
                listed_values=(
                    list(repair.values)
                    if repair is not None
                    else _values(attribute.get("listed_values"))
                ),
                example=_text(attribute.get("example")),
                presence=_presence(
                    attribute.get("presence") or {}, feature_class, name, defects
                ),
            )

    def _metadata_fields(self) -> Iterator[MetadataField]:
        for name, entry in self._document("metadata.json").items():
            yield MetadataField(
                name=name,
                description=_text(entry.get("description")),
                type=_text(entry.get("type")),
                listed_values=_values(entry.get("listed_values")),
                example=_text(entry.get("example")),
                presence=PresenceRule.parse(entry["presence"]),
            )


def _types(types: dict[str, Any]) -> Iterator[FeatureType]:
    for name, entry in types.items():
        yield FeatureType(
            name=name,
            description=_text(entry.get("description")),
            tier=entry.get("tier"),
            allowed_on_road=bool(entry.get("allowed_on_road", False)),
            forbidden_on_road=_values(entry.get("forbidden_field_if_allowed_on_road")),
            allowed_uses=_values(entry.get("allowed_uses")),
            prohibited_uses=_values(entry.get("prohibited_uses")),
        )


def _presence(
    presence: dict[str, Any],
    feature_class: str,
    field_name: str,
    defects: list[SpecDefect],
) -> dict[str, PresenceRule]:
    rules = {}
    for type_name, slots in presence.items():
        try:
            rules[type_name] = PresenceRule.parse(slots)
        except ValueError as error:
            defects.append(
                SpecDefect(
                    feature_class=feature_class,
                    field=field_name,
                    column=type_name,
                    value=json.dumps(slots),
                    problem=str(error),
                )
            )
    return rules


def _text(value: Any) -> str:
    """A cell as text. `null` and numeric examples both arrive here."""
    if value is None:
        return ""
    return str(value).strip()


def _values(value: Any) -> list[str]:
    """A `listed_values` array, stripped. `null` means the field is not enumerated."""
    if not value:
        return []
    return [str(v).strip() for v in value]
