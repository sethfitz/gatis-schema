"""The vendored snapshot parses, and the invariants generation will rely on hold."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from gatis_schema import FEATURE_CLASSES, TIERS, Presence, PresenceRule, SpecReader
from gatis_schema.spec_source import SpecSnapshot


@pytest.fixture(scope="module")
def snapshot() -> SpecSnapshot:
    return SpecReader().load()


def test_snapshot_is_pinned_to_an_upstream_commit(snapshot: SpecSnapshot) -> None:
    source = snapshot.manifest.source
    assert source.repo == "dotbts/BPA"
    assert len(source.commit) == 40
    assert snapshot.spec_version == source.commit


def test_all_four_feature_classes_load(snapshot: SpecSnapshot) -> None:
    assert set(snapshot.feature_classes) == set(FEATURE_CLASSES)


def test_edge_types_match_the_specification(snapshot: SpecSnapshot) -> None:
    edges = snapshot.feature_classes["edge"]
    assert edges.type_names == [
        "road",
        "sidewalk",
        "curb_ramp_toplanding",
        "curb_ramp_runslope",
        "footway",
        "crossing",
        "ramp",
        "traffic_island",
        "steps",
        "elevator",
        "escalator",
        "bikeway",
        "multi_use_path",
        "trail",
    ]


def test_node_types_match_the_specification(snapshot: SpecSnapshot) -> None:
    assert snapshot.feature_classes["node"].type_names == [
        "generic",
        "curb_ramp",
        "sidewalk_to_ramp_transition",
        "ramp_to_street_transition",
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
            for type_name in spec.type_names:
                rule = by_name[field_name].presence.get(type_name)
                assert rule is not None, f"{name}.{field_name}/{type_name}"
                assert rule.at(1) is Presence.REQUIRED


def test_every_declared_type_has_fields(snapshot: SpecSnapshot) -> None:
    # Draft 2 declared `elevator` as an edge type with no presence column, so the
    # spec gave it no fields at all -- not even `edge_id`. v1.0 fixed that; this
    # fails if it regresses.
    for name, spec in snapshot.feature_classes.items():
        assert spec.types_without_fields == [], name


def test_known_orphan_presence_columns_are_reported(snapshot: SpecSnapshot) -> None:
    # v1.0 removed `virtual_link` from `edges.json`'s `types` but left its presence
    # column on all 78 attributes. Reported rather than silently generated: it
    # would otherwise put a type back into the discriminated union that the spec
    # no longer allows.
    drift = {
        name: spec.fields_without_types
        for name, spec in snapshot.feature_classes.items()
    }
    assert drift == {"node": [], "edge": ["virtual_link"], "point": [], "zone": []}


def test_known_dangling_on_road_field_references_are_reported(
    snapshot: SpecSnapshot,
) -> None:
    # The same drift in the other direction: three edge types forbid
    # `road_associated` in their on-road representation, and v1.0 removed the
    # field. There is nothing for a validator to check.
    assert snapshot.feature_classes["edge"].dangling_forbidden_on_road == {
        "sidewalk": ["road_associated"],
        "bikeway": ["road_associated"],
        "multi_use_path": ["road_associated"],
    }
    for name in ("node", "point", "zone"):
        assert snapshot.feature_classes[name].dangling_forbidden_on_road == {}


def test_forbidden_never_varies_by_tier(snapshot: SpecSnapshot) -> None:
    # Load-bearing for modelling each feature type as its own class: the set of
    # fields a type may carry is fixed, and only presence strength moves with tier.
    for spec in snapshot.feature_classes.values():
        for field in spec.fields:
            for type_name, rule in field.presence.items():
                values = {rule.at(tier) for tier in TIERS}
                assert not (Presence.FORBIDDEN in values and len(values) > 1), (
                    f"{field.name}/{type_name}"
                )


def test_conditionally_required_is_gone(snapshot: SpecSnapshot) -> None:
    # Draft 2 used `conditionally_required` for the ADA pair. v1.0 dropped the
    # descriptor entirely (upstream "update tables to drop conditionals"), so the
    # vocabulary is four values and `Presence` has no member for it.
    assert not hasattr(Presence, "CONDITIONALLY_REQUIRED")
    seen = {
        rule.at(tier).value
        for spec in snapshot.feature_classes.values()
        for field in spec.fields
        for rule in field.presence.values()
        for tier in TIERS
    }
    assert seen == {"required", "recommended", "optional", "forbidden"}


def test_field_names_carry_no_stray_whitespace(snapshot: SpecSnapshot) -> None:
    # Draft 2 stored three Edges_Fields names with a trailing space.
    for spec in snapshot.feature_classes.values():
        for field_name in spec.field_names:
            assert field_name == field_name.strip()


def test_no_duplicate_field_rows(snapshot: SpecSnapshot) -> None:
    # Draft 2's Points_Fields listed `impediment` and `surface_issue` twice, with
    # value sets that disagreed. v1.0 publishes each attribute once.
    for name, spec in snapshot.feature_classes.items():
        assert spec.duplicate_field_names == [], name


def test_the_snapshot_reads_clean_once_repairs_are_applied(
    snapshot: SpecSnapshot,
) -> None:
    assert snapshot.defects == []
    assert sorted((r.feature_class, r.field) for r in snapshot.repairs_applied) == [
        ("edge", "allowed_uses"),
        ("edge", "markings"),
        ("edge", "prohibited_uses"),
        ("edge", "separation_elements"),
        ("edge", "separation_permeable_car"),
        ("edge", "traffic_calming"),
        ("node", "presence"),
    ]


def test_repairs_are_what_the_upstream_values_are_not(tmp_path: Path) -> None:
    # Control, in both directions. Without repairs the seven cells load verbatim
    # and are visibly broken -- empty strings and fragments; with them they are
    # clean. A repair whose values already matched upstream would pass the
    # assertion above while changing nothing, so assert the difference, not just
    # the application -- and assert it for EVERY repair, driven off repairs.json
    # rather than a hand-kept list, so a new entry cannot land uncovered. Three
    # of the seven were spot-checked here once; the other four were applied and
    # never proven to do anything.
    spec = SpecReader().spec_dir
    shutil.copytree(spec, tmp_path / "spec")
    (tmp_path / "spec" / "repairs.json").unlink()
    raw = SpecReader(tmp_path / "spec").load()
    assert raw.repairs_applied == []

    verbatim = {f.name: f.listed_values for f in raw.feature_classes["edge"].fields}
    assert "" in verbatim["separation_permeable_car"]
    assert "curbs)" in verbatim["separation_permeable_car"]
    assert "trees  unknown" in verbatim["separation_elements"]
    # A third mechanism: a pipe the exporter never treated as a separator. Only
    # `nodes.json` has it -- `edges.json` lists the same field correctly.
    node_verbatim = {
        f.name: f.listed_values for f in raw.feature_classes["node"].fields
    }
    assert "no | missing" in node_verbatim["presence"]

    entries = json.loads((spec / "repairs.json").read_text())["listed_values"]
    assert entries, "no repairs to control for"
    repaired_snapshot = SpecReader().load()
    for entry in entries:
        feature_class, field = entry["feature_class"], entry["field"]
        before = next(
            f.listed_values
            for f in raw.feature_classes[feature_class].fields
            if f.name == field
        )
        after = next(
            f.listed_values
            for f in repaired_snapshot.feature_classes[feature_class].fields
            if f.name == field
        )
        assert after != before, f"{feature_class}.{field} repair changes nothing"
        assert all(value.strip() for value in after), f"{feature_class}.{field}"


def test_the_two_presence_vocabularies_agree_once_repaired(
    snapshot: SpecSnapshot,
) -> None:
    # `presence` is published as four values on edges and three on nodes, the
    # middle one being the unsplit pair "no | missing". Repaired, they match --
    # which is what lets the generator emit one shared enum rather than two.
    listed = {
        name: next(
            f.listed_values
            for f in snapshot.feature_classes[name].fields
            if f.name == "presence"
        )
        for name in ("edge", "node")
    }
    assert listed["edge"] == listed["node"] == ["yes", "no", "missing", "unknown"]


def test_every_repair_names_a_field_that_exists(snapshot: SpecSnapshot) -> None:
    # A repair for a renamed or removed field would silently stop applying.
    for repair in json.loads((SpecReader().spec_dir / "repairs.json").read_text())[
        "listed_values"
    ]:
        spec = snapshot.feature_classes[repair["feature_class"]]
        assert repair["field"] in spec.field_names, repair["field"]


def test_metadata_fields_cover_the_required_basics(snapshot: SpecSnapshot) -> None:
    names = {field.name for field in snapshot.metadata_fields}
    assert {"title", "schema_version", "publisher", "license"} <= names


def test_presence_never_decreases_across_tiers(snapshot: SpecSnapshot) -> None:
    rank = {
        Presence.FORBIDDEN: 0,
        Presence.OPTIONAL: 1,
        Presence.RECOMMENDED: 2,
        Presence.REQUIRED: 3,
    }
    for spec in snapshot.feature_classes.values():
        for field in spec.fields:
            for type_name, rule in field.presence.items():
                ranks = [rank[rule.at(tier)] for tier in TIERS]
                assert ranks == sorted(ranks), f"{field.name}/{type_name}: {rule}"


def test_units_are_readable_from_field_names(snapshot: SpecSnapshot) -> None:
    # v1.0's headline modelling change: the unit moved into the field name, so a
    # consumer no longer has to parse English to know whether 60 is inches or feet.
    edges = {f.name for f in snapshot.feature_classes["edge"].fields}
    assert {"width_in", "buffer_width_ft", "posted_speed_limit_mph"} <= edges
    assert not {"width", "buffer_width", "posted_speed_limit"} & edges


class TestPresenceRule:
    def test_uniform_array_holds_at_every_tier(self) -> None:
        rule = PresenceRule.parse(["forbidden", None, None, None])
        assert rule.is_uniform
        assert [rule.at(tier) for tier in TIERS] == [Presence.FORBIDDEN] * 4

    def test_a_change_applies_from_its_tier_upward(self) -> None:
        rule = PresenceRule.parse(["optional", None, "recommended", "required"])
        assert not rule.is_uniform
        assert [rule.at(tier) for tier in TIERS] == [
            Presence.OPTIONAL,
            Presence.OPTIONAL,
            Presence.RECOMMENDED,
            Presence.REQUIRED,
        ]

    def test_unknown_presence_token_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            PresenceRule.parse(["mandatory", None, None, None])

    def test_conditionally_required_no_longer_parses(self) -> None:
        with pytest.raises(ValueError):
            PresenceRule.parse(["conditionally_required", None, None, None])

    def test_a_short_array_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="presence needs 4 slots"):
            PresenceRule.parse(["optional", None])

    def test_a_missing_tier_1_value_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="no tier-1 value"):
            PresenceRule.parse([None, "required", None, None])

    def test_tier_out_of_range_is_rejected(self) -> None:
        rule = PresenceRule.parse(["optional", None, None, None])
        with pytest.raises(ValueError, match="tier must be one of"):
            rule.at(5)


def test_seasonal_condition_still_matches_the_mangled_cell() -> None:
    # `SeasonalCondition` hand-splits one cell into two vocabularies, because
    # `seasonal`'s `listed_values` carries its own section labels inside values
    # ("season: spring", ..., "seasonal issues: flooding", ...). No exporter fix
    # recovers that, so the split is a judgement this package makes and nothing
    # else re-checks. Pin it: if upstream repairs or re-mangles the cell, this
    # fails rather than leaving the hand-written values quietly wrong.
    from gatis_schema.annotations import field_vocabularies
    from gatis_schema.shared import SeasonalCondition

    published = next(
        field
        for field in SpecReader().load().feature_classes["edge"].fields
        if field.name == "seasonal"
    )
    assert published.listed_values == [
        "season: spring",
        "summer",
        "fall",
        "winter",
        "seasonal issues: flooding",
        "ice",
        "snow",
        "heavy rain",
        "heat / lack of shade",
        "low visibility",
        "fog",
        "wind",
    ]

    declared = field_vocabularies(SeasonalCondition)
    # Every published value reaches one of the two fields, with the section
    # label stripped from the two that carry one.
    stripped = {value.split(": ")[-1] for value in published.listed_values}
    assert stripped == set(declared["season"].values) | set(declared["issue"].values)
