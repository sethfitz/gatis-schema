"""Dataset-level checks: the rules that need more than one file in hand."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gatis.dataset import Dataset

NODE_IDS = ("n1", "n2")


def _node(node_id: str, lon: float) -> dict[str, object]:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, 45.52]},
        "properties": {"node_id": node_id, "node_type": "generic"},
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


def test_an_explicit_null_property_reads_as_absent(tmp_path: Path) -> None:
    # Esri-derived GATIS exports write every unset field as an explicit null rather
    # than omitting it -- the two published sample datasets average 57% null slots
    # per feature -- and upstream's own JSON Schema permits null on most fields.
    directory = _write(
        tmp_path, edges=[_edge("e1", "n1", "n2", width_in=None, surface_material=None)]
    )
    edge = Dataset.load(directory).edges.features[0]  # type: ignore[union-attr]
    # Absent, not null: Overture's `Omitable` sentinel, and dropped on the way out.
    assert "width_in" not in edge.model_fields_set
    properties = json.loads(edge.model_dump_json())["properties"]
    assert "width_in" not in properties
    assert "surface_material" not in properties


def test_a_null_does_not_satisfy_a_required_field(tmp_path: Path) -> None:
    # Control for the above, in the other direction: dropping nulls must not turn a
    # required field into an optional one. `edge_type` is required from tier 1.
    directory = _write(tmp_path, edges=[_edge("e1", "n1", "n2")])
    raw = json.loads((directory / "edges.geojson").read_text())
    raw["features"][0]["properties"]["edge_type"] = None
    (directory / "edges.geojson").write_text(json.dumps(raw))
    with pytest.raises(Exception, match=r"edge_type|union_tag"):
        Dataset.load(directory)


def test_the_gatis_identifier_spelling_survives_a_round_trip(clean: Path) -> None:
    # `Feature` would hoist a bare `id` to the GeoJSON top level; GATIS spells it
    # `edge_id` inside `properties`, which is what serialize_by_alias preserves.
    edge = Dataset.load(clean).edges.features[0]  # type: ignore[union-attr]
    dumped = json.loads(edge.model_dump_json())
    assert dumped["properties"]["edge_id"] == "e1"
    assert "id" not in dumped


def test_every_published_reference_ids_encoding_validates() -> None:
    # The four shapes the two GATIS sample datasets actually use, across 348,223
    # features. None uses a key called `id`, which the spec's prose asks for and
    # its schema does not enforce -- so requiring it would reject all of them.
    from gatis.shared import ReferenceId

    for raw in (
        {"source": "austin", "sidewalks_id": "94639273"},
        {"source": "austin", "source_url": "", "CURB_RAMPS_ID": 15866993},
        {"source": "austin", "asmp_street_network_id": "330428"},
        {"source": "newark", "edge_id": 1070387},
    ):
        assert ReferenceId.model_validate(raw).model_dump(exclude_unset=True) == raw

    # And the prose's own shape still types its two keys when they are present.
    documented = ReferenceId.model_validate({"source": "osm", "id": "w123"})
    assert documented.model_dump() == {"source": "osm", "id": "w123"}
