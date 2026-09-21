"""The vendored snapshot parses, and the invariants generation will rely on hold."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gatis_schema import FEATURE_CLASSES, TIERS, Presence, PresenceRule, SpecReader
from gatis_schema.spec_source import SpecSnapshot


@pytest.fixture(scope="module")
def snapshot() -> SpecSnapshot:
    return SpecReader().load()


def test_snapshot_is_pinned_to_a_drive_revision(snapshot: SpecSnapshot) -> None:
    assert snapshot.workbook_version.isdigit()


def test_all_four_feature_classes_load(snapshot: SpecSnapshot) -> None:
    assert set(snapshot.feature_classes) == set(FEATURE_CLASSES)


def test_edge_types_match_the_specification(snapshot: SpecSnapshot) -> None:
    edges = snapshot.feature_classes["edge"]
    assert edges.type_names == [
        "road",
        "sidewalk",
        "footpath",
        "crossing",
        "ramp",
        "traffic_island",
        "steps",
        "elevator",
        "escalator",
        "bikeway",
        "multi_use_path",
        "trail",
        "virtual_link",
    ]


def test_every_feature_class_has_an_id_and_a_type_field(
    snapshot: SpecSnapshot,
) -> None:
    for name, spec in snapshot.feature_classes.items():
        assert f"{name}_id" in spec.field_names
        assert f"{name}_type" in spec.field_names


def test_id_and_type_are_required_from_tier_1(snapshot: SpecSnapshot) -> None:
    for name, spec in snapshot.feature_classes.items():
        by_name = {field.name: field for field in spec.fields}
        for field_name in (f"{name}_id", f"{name}_type"):
            for type_name in spec.presence_columns:
                rule = by_name[field_name].presence.get(type_name)
                assert rule is not None, f"{name}.{field_name}/{type_name}"
                assert rule.at(1) is Presence.REQUIRED


def test_known_types_vs_fields_tab_drift_is_reported(snapshot: SpecSnapshot) -> None:
    # The `*_Types` and `*_Fields` tabs are maintained by hand and disagree.
    # `elevator` is an allowed edge type with no presence column, so the workbook
    # defines no fields for it at all. Points is worse: three of its four declared
    # types have no column, and the tab carries a `point` column that is not a type.
    drift = {
        name: (spec.types_without_fields, spec.fields_without_types)
        for name, spec in snapshot.feature_classes.items()
    }
    assert drift == {
        "node": ([], []),
        "edge": (["elevator"], []),
        "point": (["issue", "sign", "transit_stop"], ["point"]),
        "zone": ([], []),
    }


def test_forbidden_never_varies_by_tier(snapshot: SpecSnapshot) -> None:
    # Load-bearing for modelling each feature type as its own class: the set of
    # fields a type may carry is fixed, and only presence strength moves with tier.
    for spec in snapshot.feature_classes.values():
        for field in spec.fields:
            for type_name, rule in field.presence.items():
                values = {rule.at(tier) for tier in TIERS}
                assert not (
                    Presence.FORBIDDEN in values and len(values) > 1
                ), f"{field.name}/{type_name}"


def test_conditionally_required_is_only_the_ada_pair(snapshot: SpecSnapshot) -> None:
    conditional = {
        f"{name}.{field.name}"
        for name, spec in snapshot.feature_classes.items()
        for field in spec.fields
        if any(
            Presence.CONDITIONALLY_REQUIRED in {rule.at(tier) for tier in TIERS}
            for rule in field.presence.values()
        )
    }
    assert conditional == {
        "edge.ada_compliance_date",
        "edge.ada_compliant_with",
        "node.ada_compliance_date",
        "node.ada_compliant_with",
    }


def test_field_names_carry_no_stray_whitespace(snapshot: SpecSnapshot) -> None:
    # Three Edges_Fields names are stored with a trailing space upstream.
    for spec in snapshot.feature_classes.values():
        for field_name in spec.field_names:
            assert field_name == field_name.strip()


def test_known_upstream_duplicate_field_rows_are_reported(
    snapshot: SpecSnapshot,
) -> None:
    points = snapshot.feature_classes["point"]
    assert points.duplicate_field_names == ["impediment", "surface_issue"]
    for spec in ("node", "edge", "zone"):
        assert snapshot.feature_classes[spec].duplicate_field_names == []


def test_the_snapshot_reads_clean_once_repairs_are_applied(
    snapshot: SpecSnapshot,
) -> None:
    # One Points_Fields `impediment` row has its name and description pasted into
    # the two presence columns. `spec/repairs.json` blanks them; anything NOT
    # covered by a repair surfaces here instead of being silently absorbed.
    assert snapshot.defects == []
    assert [(r.feature_class, r.field, r.columns) for r in snapshot.repairs_applied] == [
        ("point", "impediment", ["object", "point"])
    ]


def test_an_unrepaired_bad_cell_is_collected_not_raised(tmp_path: Path) -> None:
    # Control: the defect path still fires when no repair covers the cell.
    spec = SpecReader().spec_dir
    shutil.copytree(spec, tmp_path / "spec")
    (tmp_path / "spec" / "repairs.json").unlink()
    snapshot = SpecReader(tmp_path / "spec").load()
    assert [(d.feature_class, d.field, d.column) for d in snapshot.defects] == [
        ("point", "impediment", "object"),
        ("point", "impediment", "point"),
    ]
    assert snapshot.repairs_applied == []


def test_metadata_fields_cover_the_required_basics(snapshot: SpecSnapshot) -> None:
    names = {field.name for field in snapshot.metadata_fields}
    assert {"title", "schema_version", "publisher", "license"} <= names


def test_presence_never_decreases_across_tiers(snapshot: SpecSnapshot) -> None:
    rank = {
        Presence.FORBIDDEN: 0,
        Presence.OPTIONAL: 1,
        Presence.CONDITIONALLY_REQUIRED: 2,
        Presence.RECOMMENDED: 2,
        Presence.REQUIRED: 3,
    }
    for spec in snapshot.feature_classes.values():
        for field in spec.fields:
            for type_name, rule in field.presence.items():
                ranks = [rank[rule.at(tier)] for tier in TIERS]
                assert ranks == sorted(ranks), f"{field.name}/{type_name}: {rule}"


class TestPresenceRule:
    def test_blank_cell_is_unspecified(self) -> None:
        assert PresenceRule.parse("") is None
        assert PresenceRule.parse("   \n  ") is None

    def test_uniform_cell_holds_at_every_tier(self) -> None:
        rule = PresenceRule.parse("forbidden")
        assert rule is not None
        assert rule.is_uniform
        assert [rule.at(tier) for tier in TIERS] == [Presence.FORBIDDEN] * 4

    def test_upgrade_applies_from_its_tier_upward(self) -> None:
        rule = PresenceRule.parse("optional\nT3:recommended\nT4:required")
        assert rule is not None
        assert not rule.is_uniform
        assert [rule.at(tier) for tier in TIERS] == [
            Presence.OPTIONAL,
            Presence.OPTIONAL,
            Presence.RECOMMENDED,
            Presence.REQUIRED,
        ]

    def test_unknown_presence_token_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            PresenceRule.parse("mandatory")

    def test_malformed_upgrade_line_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="unparseable presence upgrade"):
            PresenceRule.parse("optional\ntier 3: required")

    def test_tier_out_of_range_is_rejected(self) -> None:
        rule = PresenceRule.parse("optional")
        assert rule is not None
        with pytest.raises(ValueError, match="tier must be one of"):
            rule.at(5)
