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
