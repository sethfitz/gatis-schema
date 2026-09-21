"""A GATIS dataset: the five files together, and the checks that need all of them.

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

from pydantic import BaseModel

from gatis_schema.models import (
    EdgeCollection,
    NodeCollection,
    PointCollection,
    ZoneCollection,
)

FILES = {
    "nodes": "nodes.geojson",
    "edges": "edges.geojson",
    "points": "points.geojson",
    "zones": "zones.geojson",
    "metadata": "metadata.json",
}


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
    """The five files of a GATIS dataset, parsed.

    Every file is optional: the spec's tier model lets a publisher ship edges with
    no zones, and a dataset that omits `nodes.geojson` simply cannot be checked for
    dangling endpoints.
    """

    nodes: NodeCollection | None = None
    edges: EdgeCollection | None = None
    points: PointCollection | None = None
    zones: ZoneCollection | None = None
    metadata: dict[str, object] | None = None

    @classmethod
    def load(cls, directory: Path | str) -> Dataset:
        """Read whichever of the five files are present in `directory`."""
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
        return [*self._duplicate_ids(), *self._dangling_endpoints()]

    @property
    def unchecked(self) -> list[str]:
        """Checks that could not run, so a clean result is not mistaken for a pass."""
        missing = []
        if self.edges and not self.nodes:
            missing.append(
                "edge endpoints: edges.geojson is present and nodes.geojson is not, "
                "so from_node and to_node cannot be resolved"
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

    def _collections(
        self,
    ) -> Iterator[
        tuple[str, NodeCollection | EdgeCollection | PointCollection | ZoneCollection]
    ]:
        for name in ("nodes", "edges", "points", "zones"):
            collection = getattr(self, name)
            if collection is not None:
                yield name, collection
