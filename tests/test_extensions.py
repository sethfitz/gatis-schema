"""The three extension tables: the models, their source, and the defects in it.

`models/extensions.py` is hand-written because upstream publishes no structured
JSON for `lrs.json`, `events.json` or `relations.json` -- only the field tables in
`documents/drafts/GATIS Extensions and Tables.pdf`. Two links have to hold for
that to be trustworthy, and both are asserted here: the models agree with
`spec/extensions.json`, and `spec/extensions.json` agrees with the PDF.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from gatis_schema.dataset import Dataset
from gatis_schema.models.extensions import (
    Event,
    EventAdapter,
    EventFeatureType,
    LrsCrosswalk,
    LrsFeatureType,
    LrsSide,
    Relation,
)
from gatis_schema.spec_source import SPEC_DIR

TABLES: dict[str, type[BaseModel]] = {
    "lrs": LrsCrosswalk,
    "events": Event,
    "relations": Relation,
}


@pytest.fixture(scope="module")
def transcription() -> dict[str, Any]:
    payload: dict[str, Any] = json.loads((SPEC_DIR / "extensions.json").read_text())
    return payload["tables"]


def _wire_names(model: type[BaseModel]) -> list[str]:
    return [field.alias or name for name, field in model.model_fields.items()]


# --------------------------------------------------------------------------
# The models against their source
# --------------------------------------------------------------------------


@pytest.mark.parametrize("table", sorted(TABLES))
def test_model_fields_match_the_transcription(
    table: str, transcription: dict[str, Any]
) -> None:
    """Same wire names, same order, so a re-transcription cannot drift silently."""
    expected = [field["name"] for field in transcription[table]["fields"]]
    assert _wire_names(TABLES[table]) == expected


@pytest.mark.parametrize("table", sorted(TABLES))
def test_required_fields_match_the_transcription(
    table: str, transcription: dict[str, Any]
) -> None:
    model = TABLES[table]
    expected = {
        field["name"] for field in transcription[table]["fields"] if field["required"]
    }
    actual = {
        field.alias or name
        for name, field in model.model_fields.items()
        if field.is_required()
    }
    assert actual == expected


@pytest.mark.parametrize("table", sorted(TABLES))
def test_every_field_carries_its_published_description(
    table: str, transcription: dict[str, Any]
) -> None:
    """A description may add to the published one; it may not replace it.

    Several say more than the PDF -- `Recommended values: ...` appended from the
    listed-values column, the way the core models do it -- so the test is
    containment rather than equality, on the leading sentence.
    """
    model = TABLES[table]
    by_wire_name = {
        field.alias or name: field for name, field in model.model_fields.items()
    }
    for published in transcription[table]["fields"]:
        described = by_wire_name[published["name"]].description or ""
        head = published["description"].split(". Recommended values")[0]
        assert head[:60] in described, published["name"]


def test_transcription_matches_the_pdf(transcription: dict[str, Any]) -> None:
    """The control on the transcription itself, read from the PDF's own text.

    `spec/extensions.txt` is `pdftotext -layout` over `spec/extensions.pdf`, both
    written by `scripts/snapshot-spec`. The regex has to allow a single space
    between a name and its description, because five of the longest names run
    into the description column -- with two, `lrs_starting_milepoint`,
    `location_description`, `inspection_method` and `turning_treatment` all
    vanish and the extraction silently undercounts by five.
    """
    text = (
        (SPEC_DIR / "extensions.txt").read_text().replace("ﬁ", "fi").replace("ﬃ", "ffi")
    )
    headings = {
        "LRS Extension": "lrs",
        "Events Table": "events",
        "Relations Table": "relations",
    }
    found: dict[str, list[str]] = {name: [] for name in headings.values()}
    current: str | None = None
    for line in text.splitlines():
        if line.strip() in headings:
            current = headings[line.strip()]
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9_]*) +[A-Z“\"]", line)
        if not (match and current) or match.group(1) == "Name":
            continue
        if match.group(1) not in found[current]:
            found[current].append(match.group(1))

    for table in TABLES:
        expected = [field["name"] for field in transcription[table]["fields"]]
        assert found[table] == expected, table
    # The did-happen half: the extraction found something in every table, so an
    # empty `found` cannot pass as agreement with an empty transcription.
    assert all(found.values())
    assert sum(len(names) for names in found.values()) == 36


# --------------------------------------------------------------------------
# Defects, pinned so an upstream fix shows up as a failure
# --------------------------------------------------------------------------


def test_extension_type_vocabularies_still_predate_v1_0() -> None:
    """Both `type` enums name types v1.0 removed and omit types it added."""
    lrs = {member.value for member in LrsFeatureType}
    events = {member.value for member in EventFeatureType}

    assert "virtual_link" in lrs
    assert {"virtual_link", "virtual_node", "open_movement"} <= events
    # Neither can name a road, which is the type the LRS crosswalk exists for.
    assert "road" not in lrs
    assert "road" not in events
    # The same list spells one type with a space and the next with an underscore.
    assert "traffic island" in lrs
    assert "traffic_calming" in lrs
    assert "traffic_island" not in lrs


def test_the_two_tables_disagree_about_the_infrastructure_type_vocabulary() -> None:
    """One sentence introduces both and the vocabularies differ by six values."""
    lrs = {member.value for member in LrsFeatureType}
    events = {member.value for member in EventFeatureType}
    assert lrs != events
    assert lrs - events == {"generic", "open", "traffic_calming"}
    assert events - lrs == {"virtual_node", "open_movement"}


def test_milepoint_types_disagree_between_the_two_tables() -> None:
    """The LRS table types a milepoint as text; the events table as a decimal."""
    # Through model_dump, per test_codegen: mypy cannot narrow the Omitable union.
    row = LrsCrosswalk.model_validate({"gatis_id": "1", "lrs_starting_milepoint": "4"})
    assert row.model_dump()["lrs_starting_milepoint"] == "4"

    event = Event.model_validate({"event_id": "e1", "lrs_milepoint": 4})
    milepoint = event.model_dump()["lrs_milepoint"]
    assert milepoint == 4.0
    assert isinstance(milepoint, float)


def test_both_is_a_legal_side_here_and_nowhere_in_the_core_schema() -> None:
    """`lrs_side` admits it; the 292 on-road modifier fields do not."""
    assert LrsSide("both")
    schema = json.loads((SPEC_DIR / "json-schemas" / "edges_schema.json").read_text())
    names: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "properties" and isinstance(value, dict):
                    names.extend(value)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(schema)
    colon = [name for name in names if ":" in name]
    assert len(colon) == 292
    assert {name.split(":")[1] for name in colon} == {"left", "right"}


def test_event_location_accepts_the_line_its_description_asks_for() -> None:
    """Declared `Geometry (Point)`, described as holding a whole sidewalk edge.

    Constraining it to POINT would reject what the specification instructs, so
    the constraint is omitted. `shared.ReferenceId` makes the same trade.
    """
    event = Event.model_validate(
        {
            "event_id": "e1",
            "event_location": {
                "type": "LineString",
                "coordinates": [[-122.68, 45.52], [-122.67, 45.52]],
            },
        }
    )
    assert event.event_location is not None


# --------------------------------------------------------------------------
# Wire behaviour
# --------------------------------------------------------------------------


def test_the_capital_type_spelling_survives_a_round_trip() -> None:
    """The LRS column is printed `Type`; the events one is `type`."""
    row = LrsCrosswalk.model_validate({"gatis_id": "1", "Type": "sidewalk"})
    assert row.model_dump(by_alias=False)["feature_type"] is LrsFeatureType.SIDEWALK
    assert row.model_dump(mode="json", exclude_none=True)["Type"] == "sidewalk"

    event = Event.model_validate({"event_id": "e1", "type": "sidewalk"})
    assert event.model_dump(by_alias=False)["feature_type"] is EventFeatureType.SIDEWALK
    assert event.model_dump(mode="json", exclude_none=True)["type"] == "sidewalk"


def test_an_identifier_column_takes_the_list_its_description_asks_for() -> None:
    """ "If multiple (ex. at the west and east ends of a crossing), provide all IDs
    in a list" -- against a declared type of `ID`.
    """
    relation = Relation.model_validate(
        {"relation_id": "r1", "signal_id": ["s1", "s2"], "crossing_id": "c1"}
    )
    dumped = relation.model_dump(mode="json", exclude_none=True)
    assert dumped["signal_id"] == ["s1", "s2"]
    assert dumped["crossing_id"] == "c1"


def test_an_unknown_column_is_kept_rather_than_rejected() -> None:
    """Section 6.1, and the Playbook: new event types and columns may be added."""
    event = Event.model_validate({"event_id": "e1", "contractor_phone": "555-0100"})
    assert (event.model_extra or {})["contractor_phone"] == "555-0100"


def test_a_row_without_its_required_identifier_is_refused() -> None:
    with pytest.raises(ValidationError):
        EventAdapter.validate_python([{"event_type": "repair"}])


# --------------------------------------------------------------------------
# Dataset wiring
# --------------------------------------------------------------------------


def _core(directory: Path) -> Path:
    (directory / "nodes.geojson").write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [-122.68, 45.52]},
                        "properties": {"node_id": "n1", "node_type": "generic"},
                    }
                ],
            }
        )
    )
    return directory


def test_an_extension_row_pointing_at_no_feature_is_reported(tmp_path: Path) -> None:
    _core(tmp_path)
    (tmp_path / "lrs.json").write_text(json.dumps([{"gatis_id": "nope"}]))
    (tmp_path / "relations.json").write_text(
        json.dumps([{"relation_id": "r1", "signal_id": ["n1", "ghost"]}])
    )

    errors = Dataset.load(tmp_path).check_integrity()
    problems = {(error.file, error.field, error.feature_id) for error in errors}
    assert ("lrs.json", "gatis_id", "0") in problems
    assert ("relations.json", "signal_id", "r1") in problems
    # The control: `n1` resolves, so only the ghost is reported.
    assert len(errors) == 2


def test_a_resolvable_extension_row_reports_nothing(tmp_path: Path) -> None:
    _core(tmp_path)
    (tmp_path / "events.json").write_text(
        json.dumps([{"event_id": "e1", "gatis_id": "n1", "event_type": "repair"}])
    )
    dataset = Dataset.load(tmp_path)
    assert dataset.events is not None
    assert dataset.check_integrity() == []


def test_extensions_without_a_core_file_are_unchecked_not_clean(
    tmp_path: Path,
) -> None:
    (tmp_path / "events.json").write_text(
        json.dumps([{"event_id": "e1", "gatis_id": "nope"}])
    )
    dataset = Dataset.load(tmp_path)
    assert dataset.check_integrity() == []
    assert any("events.json references" in note for note in dataset.unchecked)


@pytest.mark.parametrize(
    "payload",
    [
        [{"event_id": "e1"}],
        {"events": [{"event_id": "e1"}]},
        {"rows": [{"event_id": "e1"}]},
    ],
    ids=["bare-array", "named-key", "single-other-key"],
)
def test_both_plausible_envelopes_are_accepted(payload: object, tmp_path: Path) -> None:
    """Section 2.1 gives a filename and a format and never says which."""
    (tmp_path / "events.json").write_text(json.dumps(payload))
    dataset = Dataset.load(tmp_path)
    assert dataset.events is not None
    assert [event.event_id for event in dataset.events] == ["e1"]


def test_an_unrecognisable_envelope_is_refused_rather_than_guessed(
    tmp_path: Path,
) -> None:
    (tmp_path / "events.json").write_text(json.dumps({"a": [], "b": []}))
    with pytest.raises(ValueError, match="expected a list of events rows"):
        Dataset.load(tmp_path)


def test_an_absent_extension_is_none_and_an_empty_one_is_a_list(
    tmp_path: Path,
) -> None:
    """`None` means the publisher said nothing; `[]` means they said there are none."""
    _core(tmp_path)
    (tmp_path / "relations.json").write_text("[]")
    dataset = Dataset.load(tmp_path)
    assert dataset.relations == []
    assert dataset.events is None
    assert dataset.lrs is None


# --------------------------------------------------------------------------
# Discovery and reference generation
# --------------------------------------------------------------------------


def test_every_extension_row_is_registered_and_tagged() -> None:
    """Registration is silent when it breaks.

    A typo in `pyproject.toml`, a rename, or a tree installed without
    `uv sync` all leave discovery returning fewer models and
    `scripts/generate-reference` quietly emitting fewer pages.
    """
    from overture.schema.system.discovery import discover_models

    from gatis_schema.tag_providers import EXTENSION_TAG

    discovered = {key.name: key.tags for key in discover_models()}
    expected = {
        "gatis_lrs_crosswalk": "lrs",
        "gatis_event": "events",
        "gatis_relation": "relations",
    }
    for name, table in expected.items():
        assert name in discovered, name
        assert EXTENSION_TAG in discovered[name]
        assert f"gatis:table={table}" in discovered[name]

    # The did-differ half: the four core classes are discovered too, and they
    # carry `feature` and not ours, so the provider is selecting rather than
    # tagging everything it is handed.
    for name in ("gatis_edge", "gatis_node", "gatis_point", "gatis_zone"):
        assert discovered[name] == frozenset({"feature"}), name


def test_the_reference_generator_renders_all_seven_models(tmp_path: Path) -> None:
    """The regression that wiped `docs/reference/`.

    One field typed `str | list[str]` raises `UnsupportedUnionError` in the
    codegen's union handling and the run dies after `generate-reference` has
    already removed the output directory, so the failure presents as a missing
    reference rather than as a bad annotation. Running the real generator over
    the real models is the only check that catches it.
    """
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from overture.schema.codegen.cli import main; main()",
            "generate",
            "--format",
            "markdown",
            "--tag",
            "feature",
            "--tag",
            "gatis:extension",
            "--exclude",
            "overture",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

    models = tmp_path / "gatis_schema" / "models"
    rendered = {path.stem for path in models.glob("*.md")}
    assert {"lrs_crosswalk", "event", "relation"} <= rendered
    assert {"edge", "node", "point", "zone"} <= rendered


def test_the_generated_reference_is_byte_identical_across_runs(
    tmp_path: Path,
) -> None:
    """A bare `BeforeValidator` renders as a `repr` carrying a memory address.

    That makes `docs/reference/` differ on every run, which shows up as noise in
    every diff rather than as an error. `ScalarOrListConstraint` exists partly
    to avoid it; this asserts the property rather than the workaround.
    """
    import subprocess
    import sys

    def render(target: Path) -> dict[str, str]:
        subprocess.run(
            [
                sys.executable,
                "-c",
                "from overture.schema.codegen.cli import main; main()",
                "generate",
                "--format",
                "markdown",
                "--tag",
                "gatis:extension",
                "--output-dir",
                str(target),
            ],
            capture_output=True,
            check=True,
        )
        return {
            str(path.relative_to(target)): path.read_text()
            for path in sorted(target.rglob("*.md"))
        }

    first = render(tmp_path / "one")
    second = render(tmp_path / "two")
    assert first == second
    assert first, "no pages rendered, so identity is vacuous"


def test_a_scalar_or_list_column_round_trips_both_forms() -> None:
    relation = Relation.model_validate({"relation_id": "r1", "signal_id": "s1"})
    assert relation.model_dump()["signal_id"] == ["s1"]
    assert relation.model_dump(mode="json")["signal_id"] == "s1"

    several = Relation.model_validate({"relation_id": "r1", "signal_id": ["s1", "s2"]})
    assert several.model_dump(mode="json")["signal_id"] == ["s1", "s2"]


def test_a_one_item_list_comes_back_as_a_scalar() -> None:
    """The documented lossy case, asserted so it is a decision and not a bug."""
    relation = Relation.model_validate({"relation_id": "r1", "signal_id": ["only"]})
    assert relation.model_dump(mode="json")["signal_id"] == "only"


def test_both_wire_forms_reach_the_json_schema() -> None:
    """The reason this is a constraint: the rule has to leave Python."""
    emitted = Relation.model_json_schema()["properties"]["signal_id"]
    branches = emitted["oneOf"]
    assert [branch.get("type") for branch in branches] == ["string", "array"]
    assert branches[1]["items"]["type"] == "string"
