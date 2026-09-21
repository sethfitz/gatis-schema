"""The bootstrap's own invariants -- the ones a wrong model would not announce."""

from __future__ import annotations

from collections.abc import Mapping

import pydantic
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
    # repo's own lint.
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
    # Undeclared, these values round-trip through `model_extra`: a conforming
    # bikeway on a roadway centerline is then indistinguishable from a local
    # extension nobody has heard of, and its enum never validates.
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
    # a wrong value fails rather than landing in `model_extra` unread.
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


def test_the_forbidden_on_road_set_holds_names_not_characters() -> None:
    # `frozenset("a", "b")` is a TypeError, but `frozenset("abc")` is
    # {'a','b','c'} -- silently. The generator emits a set literal, so a
    # one-element list cannot splat into characters; this fails if it ever goes
    # back to passing the names as arguments, which would import cleanly, pass
    # every other test, and reject nothing.
    from gatis_schema.models.edges import ROADEDGE_FORBIDDEN

    assert len(ROADEDGE_FORBIDDEN) == 36
    assert all(len(alias) > 1 and alias.count(":") == 2 for alias in ROADEDGE_FORBIDDEN)
    assert "bikeway:left:edge_id" in ROADEDGE_FORBIDDEN


def test_a_forbidden_on_road_attribute_is_rejected() -> None:
    # v1.0 forbids these in the modifier form because they describe the road, not
    # the facility beside it. Leaving them out of the model is not the same as
    # rejecting them: under `extra="allow"` they validate silently.
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory

    import pytest

    from gatis_schema.dataset import Dataset
    from gatis_schema.models.edges import RoadEdge

    def load(extra: dict[str, object]) -> RoadEdge:
        properties: dict[str, object] = {
            "edge_id": "r1",
            "edge_type": "road",
            "street_name": "Delaware Ave",
            "directionality": "both",
            **extra,
        }
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[-97.7, 30.3], [-97.6, 30.3]],
            },
            "properties": properties,
        }
        with TemporaryDirectory() as directory:
            Path(directory, "edges.geojson").write_text(
                json.dumps({"type": "FeatureCollection", "features": [feature]})
            )
            loaded = Dataset.load(directory).edges.features[0]  # type: ignore[union-attr]
        assert isinstance(loaded, RoadEdge)
        return loaded

    # The fixture validates bare. Without this the negative cases below would fail
    # for the wrong reason and still look like a pass.
    assert load({}) is not None

    for alias in ("bikeway:left:edge_id", "sidewalk:right:street_name"):
        with pytest.raises(Exception, match="forbidden in the on-road modifier form"):
            load({alias: "x"})

    # Controls: a legal modifier still validates, and an unknown key -- including
    # one shaped like a modifier -- is still an extra rather than a rejection.
    assert load({"bikeway:left:width_in": 72}).model_extra == {}
    assert load({"city_asset_tag": "A-1723"}).model_extra == {
        "city_asset_tag": "A-1723"
    }
    assert load({"bikeway:left:not_a_field": "x"}).model_extra == {
        "bikeway:left:not_a_field": "x"
    }


def test_the_on_road_prohibition_reaches_the_json_schema() -> None:
    # The reason this is a ModelConstraint rather than a @model_validator. A
    # validator enforces the rule only for callers who import this package; the
    # constraint's JSON Schema hook carries it to anyone who reads the schema.
    # Asserted on the emitted schema's behaviour, not on its text: a `not` clause
    # can be present and mean nothing.
    import json
    import subprocess

    jsonschema = pytest.importorskip("jsonschema")

    emitted = json.loads(
        subprocess.run(
            ["overture-schema", "json-schema", "--type", "gatis_edge"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout
    )
    road = dict(emitted["$defs"]["RoadEdge"]["properties"]["properties"])
    road["$defs"] = emitted.get("$defs", {})

    base = {
        "edge_id": "r1",
        "edge_type": "road",
        "street_name": "Delaware Ave",
        "directionality": "both",
    }

    def accepts(properties: Mapping[str, object]) -> bool:
        try:
            jsonschema.validate(properties, road)
        except jsonschema.ValidationError:
            return False
        return True

    # The positive control first: if the bare document did not validate, every
    # assertion below would pass for the wrong reason.
    assert accepts(base)
    assert accepts({**base, "bikeway:left:width_in": 72})
    assert accepts({**base, "city_asset_tag": "A-1723"})

    assert not accepts({**base, "bikeway:left:edge_id": "x"})
    assert not accepts({**base, "sidewalk:right:street_name": "x"})


def test_an_open_vocabulary_is_declared_but_not_enforced() -> None:
    # v1.0 publishes a vocabulary for `visual_markings` and types the field
    # `Text`, so the set is open on purpose. Austin ships "continental" on 6,717
    # crossings -- the US term for what GATIS calls "ladder". The models must
    # keep accepting it; the point of declaring the vocabulary is that a
    # transformation can ask, not that validation starts refusing.
    import json

    from gatis_schema.models import EdgeAdapter
    from gatis_schema.models.edges import CrossingEdge

    feature = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
        "properties": {
            "edge_id": "c1",
            "edge_type": "crossing",
            "visual_markings": "continental",
        },
    }
    edge = EdgeAdapter.validate_json(json.dumps(feature))
    assert isinstance(edge, CrossingEdge)
    # Through model_dump, as above: mypy cannot narrow the Omitable union past
    # the MISSING sentinel.
    assert edge.model_dump(exclude_unset=True)["visual_markings"] == "continental"


def test_a_closed_vocabulary_is_still_enforced() -> None:
    # The control for the test above. "Accepts anything" is the expected result
    # for an open vocabulary, so it proves nothing unless a closed one still
    # refuses -- otherwise a change that disabled enum validation outright would
    # read as a pass.
    import json

    import pydantic

    from gatis_schema.models import EdgeAdapter

    feature = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
        "properties": {
            "edge_id": "c1",
            "edge_type": "crossing",
            "surface_material": "continental",
        },
    }
    with pytest.raises(pydantic.ValidationError):
        EdgeAdapter.validate_json(json.dumps(feature))


def test_an_open_vocabulary_is_introspectable(snapshot: SpecSnapshot) -> None:
    # The half that serves a transformation author: reachable as data from the
    # model, without reading the spec snapshot or parsing a description string.
    from gatis_schema.annotations import field_vocabularies
    from gatis_schema.models.edges import CrossingEdge

    vocabularies = field_vocabularies(CrossingEdge)
    published = next(
        field
        for field in snapshot.feature_classes["edge"].fields
        if field.name == "visual_markings"
    )
    assert vocabularies["visual_markings"].values == tuple(published.listed_values)
    assert "ladder" in vocabularies["visual_markings"].values


def test_a_closed_vocabulary_is_not_declared_twice() -> None:
    # An `Enum` field's values are already in the enum class. Annotating those
    # too would put the same list in two places and leave neither canonical.
    from gatis_schema.annotations import field_vocabularies
    from gatis_schema.models.edges import CrossingEdge

    assert "surface_material" not in field_vocabularies(CrossingEdge)


def test_every_open_vocabulary_in_the_spec_reaches_a_model(
    snapshot: SpecSnapshot,
) -> None:
    # The count that catches a codegen path firing for some fields and not
    # others. Twelve edge fields publish a vocabulary on an open type; a partial
    # rollout would still pass every single-field assertion above.
    from gatis_schema.annotations import field_vocabularies
    from gatis_schema.models import edges as edge_models

    # `Text` specifically: a Boolean's values are carried by `YesNo`, and the
    # one Float with `listed_values` has a stray Word comment in the cell.
    expected = {
        field.name
        for field in snapshot.feature_classes["edge"].fields
        if field.listed_values and "Text" in (field.type or "Text")
    }
    assert len(expected) == 12

    declared: set[str] = set()
    for obj in vars(edge_models).values():
        if isinstance(obj, type) and issubclass(obj, pydantic.BaseModel):
            declared |= {
                # An on-road modifier carries the base field's vocabulary.
                name.rsplit(":", 1)[-1]
                for name in field_vocabularies(obj)
            }
    assert expected <= declared, expected - declared


def test_an_open_vocabulary_reaches_the_json_schema() -> None:
    # The reason this is a FieldConstraint and not a lookup table in this
    # package: most consumers of GATIS will read the JSON Schema and never
    # import Python. Asserted through the real generator, because
    # `model_json_schema()` does not exercise the system's field classifier.
    import json
    import subprocess

    emitted = json.loads(
        subprocess.run(
            ["overture-schema", "json-schema", "--type", "gatis_edge"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout
    )
    crossing = emitted["$defs"]["CrossingEdge"]["properties"]["properties"]

    assert crossing["properties"]["visual_markings"]["examples"] == [
        "marked - type unknown",
        "unmarked",
        "transverse",
        "longitudinal bar",
        "ladder",
        "bar pair",
        "high visibility",
        "other",
    ]
    # A field with a closed vocabulary gets an enum, not examples.
    assert "examples" not in crossing["properties"]["surface_material"]


def test_a_boolean_field_declares_the_string_encoding_it_actually_uses() -> None:
    # GATIS booleans are OSM-style strings on the wire, so a schema saying
    # `{"type": "boolean"}` rejects every published value -- Newark carries
    # "no" 3,855 times and "yes" 17 -- while Python accepts them anyway,
    # because the coercion runs first. That asymmetry is invisible from inside
    # the package, which is why the encoding is declared rather than left to a
    # validator.
    import json
    import subprocess

    emitted = json.loads(
        subprocess.run(
            ["overture-schema", "json-schema", "--type", "gatis_edge"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout
    )
    bridge = emitted["$defs"]["RoadEdge"]["properties"]["properties"]["properties"][
        "bridge"
    ]
    assert bridge["type"] == "string"
    assert bridge["enum"] == ["yes", "no"]


def test_the_boolean_encoding_matches_upstreams_own_schema() -> None:
    # The one place upstream's JSON Schema is worth citing. Its enums are
    # unreliable for `Array<Enum>` fields (a generator loop-variable bug), but
    # a scalar `Boolean` is outside that fault, and this is the only
    # machine-readable statement upstream makes about the wire encoding.
    import json
    import subprocess
    from pathlib import Path

    spec = Path(__file__).resolve().parent.parent / "spec" / "json-schemas"
    theirs = json.loads((spec / "edges_schema.json").read_text())
    their_bridge = theirs["properties"]["features"]["items"]["properties"][
        "properties"
    ]["properties"]["bridge"]
    their_values = next(
        arm["enum"] for arm in their_bridge["oneOf"] if arm.get("type") == "string"
    )

    emitted = json.loads(
        subprocess.run(
            ["overture-schema", "json-schema", "--type", "gatis_edge"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout
    )
    ours = emitted["$defs"]["RoadEdge"]["properties"]["properties"]["properties"][
        "bridge"
    ]
    assert ours["enum"] == their_values


def test_a_boolean_still_round_trips_through_python_as_bool() -> None:
    # The reason this is a constraint rather than `Literal["yes", "no"]`:
    # callers keep a real bool. Asserted in both directions, because a
    # constraint that only parsed would serialise back as `true`.
    import json

    from gatis_schema.models import EdgeAdapter
    from gatis_schema.models.edges import RoadEdge

    feature = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
        "properties": {
            "edge_id": "r1",
            "edge_type": "road",
            "street_name": "Delaware Ave",
            "directionality": "both",
            "bridge": "yes",
        },
    }
    edge = EdgeAdapter.validate_json(json.dumps(feature))
    assert isinstance(edge, RoadEdge)
    assert edge.model_dump(exclude_unset=True)["bridge"] is True
    assert json.loads(edge.model_dump_json())["properties"]["bridge"] == "yes"
