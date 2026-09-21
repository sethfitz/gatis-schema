"""The bootstrap's own invariants -- the ones a wrong model would not announce."""

from __future__ import annotations

import pytest

from gatis_schema.codegen import enum_names, parse_listed_values
from gatis_schema.models import enums
from gatis_schema.spec_source import SpecReader, SpecSnapshot


@pytest.fixture(scope="module")
def snapshot() -> SpecSnapshot:
    return SpecReader().load()


def test_a_field_with_one_vocabulary_keeps_the_short_name(
    snapshot: SpecSnapshot,
) -> None:
    names = enum_names(snapshot)
    assert names[("edge", "directionality")] == "Directionality"
    assert names[("node", "other_issue")] == names[("point", "other_issue")]


def test_a_field_with_differing_vocabularies_is_qualified(
    snapshot: SpecSnapshot,
) -> None:
    # Nine field names carry a different vocabulary depending on which file they
    # appear in. Without qualification one class's values overwrite another's --
    # silently, because both sides are valid Python and the enum still validates.
    names = enum_names(snapshot)
    assert names[("edge", "status")] == "EdgeStatus"
    assert names[("node", "status")] == "NodeStatus"
    assert names[("zone", "status")] == "ZoneStatus"
    assert names[("edge", "ada_compliant_with")] == "EdgeAdaCompliantWith"
    assert names[("node", "ada_compliant_with")] == "NodeAdaCompliantWith"


def test_the_qualified_enums_carry_the_vocabulary_of_their_own_class(
    snapshot: SpecSnapshot,
) -> None:
    # The assertion that actually catches the bug: names being distinct proves
    # nothing if both hold the same list.
    per_class = {
        name: [v.value for v in parse_listed_values(field.listed_values)]
        for name, spec in snapshot.feature_classes.items()
        for field in spec.fields
        if field.name == "status"
    }
    assert [e.value for e in enums.EdgeStatus] == per_class["edge"]
    assert [e.value for e in enums.NodeStatus] == per_class["node"]
    assert [e.value for e in enums.ZoneStatus] == per_class["zone"]
    assert per_class["edge"] != per_class["node"] != per_class["zone"]


def test_every_generated_enum_name_is_reachable(snapshot: SpecSnapshot) -> None:
    names = set(enum_names(snapshot).values())
    for name in names:
        assert hasattr(enums, name), name
    # And nothing generated is unreachable from the map, so a rename cannot leave
    # an orphan behind.
    generated = {
        k for k in dir(enums) if k[0].isupper() and not k.startswith("Documented")
    }
    assert generated == names


def test_units_are_annotated_from_the_field_name() -> None:
    from gatis_schema.annotations import field_units
    from gatis_schema.models.edges import RoadEdge, SidewalkEdge

    units = field_units(SidewalkEdge)
    assert str(units["width_in"]) == "in"
    assert str(units["buffer_width_ft"]) == "ft"
    assert str(field_units(RoadEdge)["posted_speed_limit_mph"]) == "mph"


def test_tier_presence_survives_into_the_models() -> None:
    from gatis_schema.annotations import field_tiers
    from gatis_schema.models.edges import SidewalkEdge

    tiers = field_tiers(SidewalkEdge)
    assert tiers["width_in"].at(1).value == "optional"
    assert tiers["width_in"].at(2).value == "required"
    assert tiers["width_in"].required_from == 2


def test_generated_source_fits_the_line_budget() -> None:
    # `ruff format` does not reflow docstrings or split a string literal, so every
    # break has to come from the generator. A single overflowing line fails the
    # repo's own lint, which is how this was found.
    from pathlib import Path

    models = Path(__file__).resolve().parents[1] / "src" / "gatis_schema" / "models"
    long_lines = [
        f"{path.name}:{number}"
        for path in sorted(models.glob("*.py"))
        for number, line in enumerate(path.read_text().splitlines(), 1)
        if len(line) > 88
    ]
    assert long_lines == []


def test_the_on_road_modifier_fields_match_upstreams_schema_exactly() -> None:
    # The set is derived here -- every non-forbidden field of each
    # `allowed_on_road` type, on each side, minus that type's
    # `forbidden_field_if_allowed_on_road` list -- and enumerated there. What the
    # match establishes is coverage: the models carry the same names upstream's
    # schema does. It is NOT independent confirmation that the derivation rule is
    # right, because both sides read `forbidden_field_if_allowed_on_road` the same
    # way; a wrong reading would be wrong in both and still agree.
    import json
    from pathlib import Path

    from gatis_schema.models.edges import RoadEdge
    from gatis_schema.spec_source import SPEC_DIR

    ours = {
        field.alias
        for field in RoadEdge.model_fields.values()
        if field.alias and ":" in field.alias
    }
    schema = json.loads(
        (Path(SPEC_DIR) / "json-schemas" / "edges_schema.json").read_text()
    )
    bag = schema["properties"]["features"]["items"]["properties"]["properties"]
    theirs = {name for name in bag["properties"] if ":" in name}

    assert len(ours) == 292
    assert ours == theirs


def test_an_on_road_modifier_is_typed_rather_than_an_extra() -> None:
    # The bug this replaced: the values round-tripped through `model_extra`, so a
    # conforming bikeway on a roadway centerline was indistinguishable from a local
    # extension nobody has heard of, and its enum never validated.
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory

    from gatis_schema.annotations import field_units
    from gatis_schema.dataset import Dataset
    from gatis_schema.models.edges import RoadEdge
    from gatis_schema.models.enums import Directionality

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[-97.7, 30.3], [-97.6, 30.3]],
        },
        "properties": {
            "edge_id": "r1",
            "edge_type": "road",
            "street_name": "Delaware Ave",
            "directionality": "both",
            "bikeway:left:bikeway_type": "Buffered Bike Lane",
            "bikeway:left:directionality": "both",
            "bikeway:left:width_in": 72,
            "bikeway:right:presence": "yes",
        },
    }
    with TemporaryDirectory() as directory:
        path = Path(directory) / "edges.geojson"
        path.write_text(
            json.dumps({"type": "FeatureCollection", "features": [feature]})
        )
        loaded = Dataset.load(directory).edges.features[0]  # type: ignore[union-attr]

    assert isinstance(loaded, RoadEdge)
    edge = loaded
    assert edge.model_extra == {}
    # Typed, not just present: the enum validates and the unit annotation rides.
    # Compared through model_dump so mypy sees values rather than the Omitable
    # union, which it cannot narrow past the MISSING sentinel.
    dumped = edge.model_dump(exclude_unset=True)
    assert dumped["bikeway:left:directionality"] is Directionality.BOTH
    assert dumped["bikeway:left:width_in"] == 72
    assert str(field_units(RoadEdge)["bikeway_left_width_in"]) == "in"

    # And the GATIS spelling survives the round trip.
    properties = json.loads(edge.model_dump_json())["properties"]
    assert properties["bikeway:left:bikeway_type"] == "Buffered Bike Lane"
    assert "bikeway_left_bikeway_type" not in properties


def test_an_unknown_field_is_still_an_extra() -> None:
    # Control: modelling 292 new names must not turn `extra="allow"` off, or a real
    # local extension would start failing instead of warning (section 6.1).
    from gatis_schema.models.edges import RoadEdge

    assert RoadEdge.model_config["extra"] == "allow"


def test_an_on_road_modifier_rejects_a_bad_value() -> None:
    # The other half of the control. Typing these fields is only worth anything if
    # a wrong value now fails where it previously landed in `model_extra` unread.
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory

    import pytest

    from gatis_schema.dataset import Dataset

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[-97.7, 30.3], [-97.6, 30.3]],
        },
        "properties": {
            "edge_id": "r1",
            "edge_type": "road",
            "street_name": "Delaware Ave",
            "directionality": "both",
            "bikeway:left:directionality": "sideways",
        },
    }
    with TemporaryDirectory() as directory:
        path = Path(directory) / "edges.geojson"
        path.write_text(
            json.dumps({"type": "FeatureCollection", "features": [feature]})
        )
        with pytest.raises(Exception, match=r"bikeway:left:directionality|sideways"):
            Dataset.load(directory)
