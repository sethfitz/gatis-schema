"""Dataset-level checks: the rules that need more than one file in hand."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gatis_schema.dataset import Dataset

NODE_IDS = ("n1", "n2")


def _node(node_id: str, lon: float) -> dict[str, object]:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, 45.52]},
        "properties": {"node_id": node_id, "node_type": "virtual"},
    }


def _edge(
    edge_id: str, from_node: str, to_node: str, **extra: object
) -> dict[str, object]:
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[-122.68, 45.52], [-122.67, 45.52]],
        },
        "properties": {
            "edge_id": edge_id,
            "edge_type": "sidewalk",
            "road_associated": "yes",
            "from_node": from_node,
            "to_node": to_node,
            **extra,
        },
    }


def _write(directory: Path, **files: list[dict[str, object]]) -> Path:
    for name, features in files.items():
        (directory / f"{name}.geojson").write_text(
            json.dumps({"type": "FeatureCollection", "features": features})
        )
    return directory


@pytest.fixture
def clean(tmp_path: Path) -> Path:
    return _write(
        tmp_path,
        nodes=[_node("n1", -122.68), _node("n2", -122.67)],
        edges=[_edge("e1", "n1", "n2")],
    )


def test_a_consistent_dataset_reports_nothing(clean: Path) -> None:
    dataset = Dataset.load(clean)
    assert dataset.check_integrity() == []
    assert dataset.unchecked == []


def test_a_dangling_endpoint_is_reported(tmp_path: Path) -> None:
    directory = _write(
        tmp_path, nodes=[_node("n1", -122.68)], edges=[_edge("e1", "n1", "n404")]
    )
    errors = Dataset.load(directory).check_integrity()
    assert [(e.field, e.feature_id) for e in errors] == [("to_node", "e1")]
    assert "n404" in errors[0].problem


def test_duplicate_ids_within_a_file_are_reported(tmp_path: Path) -> None:
    directory = _write(tmp_path, nodes=[_node("n1", -122.68), _node("n1", -122.67)])
    errors = Dataset.load(directory).check_integrity()
    assert [(e.file, e.field) for e in errors] == [("nodes.geojson", "id")]


def test_a_missing_nodes_file_is_reported_as_unchecked_not_as_clean(
    tmp_path: Path,
) -> None:
    # The control that matters: with no nodes.geojson the endpoint check cannot
    # run, and an empty error list would otherwise read as a pass.
    directory = _write(tmp_path, edges=[_edge("e1", "n1", "n404")])
    dataset = Dataset.load(directory)
    assert dataset.check_integrity() == []
    assert len(dataset.unchecked) == 1
    assert "nodes.geojson" in dataset.unchecked[0]


def test_unknown_fields_are_kept_rather_than_dropped(tmp_path: Path) -> None:
    # Section 6.1 guarantees local extensibility: a validator warns on an unknown
    # field, it does not fail, and the value must survive a round-trip.
    directory = _write(
        tmp_path, edges=[_edge("e1", "n1", "n2", local_vendor_field="kept")]
    )
    edge = Dataset.load(directory).edges.features[0]  # type: ignore[union-attr]
    assert edge.model_extra == {"local_vendor_field": "kept"}
    assert "local_vendor_field" in json.loads(edge.model_dump_json())["properties"]


def test_the_gatis_identifier_spelling_survives_a_round_trip(clean: Path) -> None:
    # `Feature` would hoist a bare `id` to the GeoJSON top level; GATIS spells it
    # `edge_id` inside `properties`, which is what serialize_by_alias preserves.
    edge = Dataset.load(clean).edges.features[0]  # type: ignore[union-attr]
    dumped = json.loads(edge.model_dump_json())
    assert dumped["properties"]["edge_id"] == "e1"
    assert "id" not in dumped
