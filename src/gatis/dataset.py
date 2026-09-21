"""A GATIS dataset: the eight files together, and the checks that need more than one.

The `Reference` annotations on `from_node` and `to_node` are declarative -- they say
what an identifier points at so downstream tooling can read it, and they enforce
nothing. Nor could they: GATIS ships nodes and edges as separate GeoJSON files, so
nothing holds both at validation time. Overture has the same split, with
`Segment.connectors[].connector_id` referencing a `Connector` in its own partition,
and resolves it the same way -- declare in the schema, enforce at the dataset level.
This module is that level.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, TypeAdapter

from gatis.models import (
    EdgeCollection,
    Event,
    EventAdapter,
    LrsCrosswalk,
    LrsCrosswalkAdapter,
    NodeCollection,
    PointCollection,
    Relation,
    RelationAdapter,
    ZoneCollection,
)

FILES = {
    "nodes": "nodes.geojson",
    "edges": "edges.geojson",
    "points": "points.geojson",
    "zones": "zones.geojson",
    "metadata": "metadata.json",
    "lrs": "lrs.json",
    "events": "events.json",
    "relations": "relations.json",
}

EXTENSIONS = ("lrs", "events", "relations")
"""The three optional tables from section 2.1. Rows, not GeoJSON features."""


@dataclass(frozen=True, slots=True)
class IntegrityError:
    """One violation of a rule that spans more than one feature."""

    file: str
    feature_id: str
    field: str
    problem: str

    def __str__(self) -> str:
        return f"{self.file}[{self.feature_id}].{self.field}: {self.problem}"


@dataclass(slots=True)
class Dataset:
    """The eight files of a GATIS dataset, parsed.

    Every file is optional: the spec's tier model lets a publisher ship edges with
    no zones, and a dataset that omits `nodes.geojson` simply cannot be checked for
    dangling endpoints. The three extension tables are optional in a stronger
    sense -- they sit outside the tier model entirely, so nothing about a dataset
    makes them expected.

    An extension that is present is `[]` rather than `None`, which is the
    distinction `check_integrity` needs: an empty `relations.json` is a publisher
    saying there are no relations, and an absent one says nothing at all.
    """

    nodes: NodeCollection | None = None
    edges: EdgeCollection | None = None
    points: PointCollection | None = None
    zones: ZoneCollection | None = None
    metadata: dict[str, object] | None = None
    lrs: list[LrsCrosswalk] | None = None
    events: list[Event] | None = None
    relations: list[Relation] | None = None

    @classmethod
    def load(cls, directory: Path | str) -> Dataset:
        """Read whichever of the eight files are present in `directory`."""
        root = Path(directory)
        collections: dict[str, type[BaseModel]] = {
            "nodes": NodeCollection,
            "edges": EdgeCollection,
            "points": PointCollection,
            "zones": ZoneCollection,
        }
        parsed: dict[str, object] = {}
        for name, model in collections.items():
            path = root / FILES[name]
            if path.exists():
                parsed[name] = model.model_validate_json(path.read_text())
        metadata_path = root / FILES["metadata"]
        if metadata_path.exists():
            with metadata_path.open() as handle:
                parsed["metadata"] = json.load(handle)

        adapters: dict[str, TypeAdapter[Any]] = {
            "lrs": LrsCrosswalkAdapter,
            "events": EventAdapter,
            "relations": RelationAdapter,
        }
        for name in EXTENSIONS:
            path = root / FILES[name]
            if path.exists():
                with path.open() as handle:
                    parsed[name] = adapters[name].validate_python(
                        _rows(json.load(handle), name, path)
                    )
        return cls(**parsed)  # type: ignore[arg-type]

    @property
    def node_ids(self) -> set[str]:
        return {node.id for node in self.nodes.features} if self.nodes else set()

    def check_integrity(self) -> list[IntegrityError]:
        """Every rule that needs more than one feature in hand.

        Returns the violations; an empty list means the dataset is consistent. The
        checks are silent when the data they need is absent, so an empty list from a
        dataset with no `nodes.geojson` says nothing about its endpoints -- see
        `unchecked`.
        """
        return [
            *self._duplicate_ids(),
            *self._dangling_endpoints(),
            *self._dangling_extension_refs(),
        ]

    @property
    def unchecked(self) -> list[str]:
        """Checks that could not run, so a clean result is not mistaken for a pass."""
        missing = []
        if self.edges and not self.nodes:
            missing.append(
                "edge endpoints: edges.geojson is present and nodes.geojson is not, "
                "so from_node and to_node cannot be resolved"
            )
        for name in EXTENSIONS:
            if getattr(self, name) and not self._feature_ids:
                missing.append(
                    f"{FILES[name]} references: no core file is present, so its "
                    "GATIS ids cannot be resolved"
                )
        return missing

    def _duplicate_ids(self) -> Iterator[IntegrityError]:
        """Section 3.4: an id is 'unique ID' when it must be unique within a file."""
        for name, collection in self._collections():
            counts = Counter(feature.id for feature in collection.features)
            for feature_id, count in sorted(counts.items()):
                if count > 1:
                    yield IntegrityError(
                        file=FILES[name],
                        feature_id=feature_id,
                        field="id",
                        problem=f"appears {count} times; ids are unique within a file",
                    )

    def _dangling_endpoints(self) -> Iterator[IntegrityError]:
        """`from_node` and `to_node` must name a node in `nodes.geojson`."""
        if not self.edges or not self.nodes:
            return
        known = self.node_ids
        for edge in self.edges.features:
            for field in ("from_node", "to_node"):
                target = getattr(edge, field, None)
                if isinstance(target, str) and target not in known:
                    yield IntegrityError(
                        file=FILES["edges"],
                        feature_id=edge.id,
                        field=field,
                        problem=f"references node {target!r}, which is not in "
                        f"{FILES['nodes']}",
                    )

    @property
    def _feature_ids(self) -> set[str]:
        """Every id in the core files, across all four."""
        return {
            feature.id
            for _, collection in self._collections()
            for feature in collection.features
        }

    def _dangling_extension_refs(self) -> Iterator[IntegrityError]:
        """An extension row's GATIS ids must name a feature in a core file.

        This is the whole point of the three tables -- they carry no geometry and
        exist only to say something about a feature that lives elsewhere -- and it
        is a check nothing upstream can perform, because no JSON Schema covers
        them and the published validator reads the core five.

        Silent when no core file is loaded; `unchecked` says so.
        """
        known = self._feature_ids
        if not known:
            return
        # `relation_id` and `event_id` name the row, not a feature, so neither is
        # resolved here.
        referencing = {
            "lrs": ("gatis_id",),
            "events": ("gatis_id",),
            "relations": ("from_id", "to_id", "signal_id", "crossing_id"),
        }
        for name, fields in referencing.items():
            for index, row in enumerate(getattr(self, name) or []):
                for field in fields:
                    yield from _missing(name, index, row, field, known)

    def _collections(
        self,
    ) -> Iterator[
        tuple[str, NodeCollection | EdgeCollection | PointCollection | ZoneCollection]
    ]:
        for name in ("nodes", "edges", "points", "zones"):
            collection = getattr(self, name)
            if collection is not None:
                yield name, collection


def _missing(
    name: str,
    index: int,
    row: object,
    field: str,
    known: set[str],
) -> Iterator[IntegrityError]:
    """Yield an error for each id in `row.field` that no core file declares."""
    value = getattr(row, field, None)
    if value is None:
        return
    targets = value if isinstance(value, list) else [value]
    row_id = str(
        getattr(row, "event_id", None) or getattr(row, "relation_id", None) or index
    )
    for target in targets:
        if isinstance(target, str) and target not in known:
            yield IntegrityError(
                file=FILES[name],
                feature_id=row_id,
                field=field,
                problem=f"references GATIS id {target!r}, which is in no core file",
            )


def _rows(payload: object, name: str, path: Path) -> list[object]:
    """The rows of an extension file, whichever envelope it arrived in.

    Section 2.1 names the file and its format and stops, so nothing says whether
    the payload is a bare array or an object wrapping one. Both are accepted, and
    anything else is refused rather than guessed at.
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        rows = payload.get(name)
        if isinstance(rows, list):
            return rows
        if len(payload) == 1:
            only = next(iter(payload.values()))
            if isinstance(only, list):
                return only
    raise ValueError(
        f"{path}: expected a list of {name} rows, or an object with one key "
        f"holding that list; got {type(payload).__name__}"
    )
