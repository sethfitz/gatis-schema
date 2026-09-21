# GATIS

Pydantic models for GATIS, built on `overture-schema-system`. Read
[`README.md`](README.md) first for what the package is and why the models are
generated rather than hand-written.

## Data may target an older draft than the models

**`spec/MANIFEST.json` is the only authoritative statement of which spec the
models track** -- it pins the upstream commit. Prose anywhere, including below,
is a restatement that can go stale; read the manifest before relying on a
version claim, and when the pin moves, grep for the claim rather than editing
the file you happen to be thinking about.

No GATIS file declares which spec version *it* targets, so field vocabulary is
the only way to tell, and data predating the pinned spec stays in circulation
-- both published sample datasets do.

Treat an unrecognised field name as a **rename** before treating it as a local
extension: 1.0 renamed rather than dropped, mostly by suffixing the unit
(`width` to `width_in`, `posted_speed_limit` to `posted_speed_limit_mph`). The
map is in [`docs/sample-data-validation.md`](docs/sample-data-validation.md).
Enum members were renamed too, and `status` now differs by feature class, so
check the vocabulary in the file for the class you care about.

<!-- Established 2026-09-21 by validating both published sample datasets. This
section replaced one saying the models were Draft #2 and should be distrusted,
which the gatis-1.0 merge (f39758d) made false. -->

## Validating data

One gotcha costs an hour if you meet it cold: **validate from JSON text, never
from a parsed dict.** The Overture `Feature` wrap-validator only unwraps the
GeoJSON envelope when Pydantic is in JSON mode, so `validate_python(feature)`
validates the envelope as if it were the model and reports every field missing.

```python
NodeAdapter.validate_json(json.dumps(feature))  # correct
NodeAdapter.validate_python(feature)  # every field reads missing
```

The rest -- why optional-field errors arrive twice, why paths read
`road.road.width`, how explicit `null` behaves -- is in
[`.claude/rules/validating-gatis-data.md`](.claude/rules/validating-gatis-data.md).

`scripts/validate-sample <file.geojson>` runs a classified report over a whole
file. [`docs/sample-data-validation.md`](docs/sample-data-validation.md) is what
it found on the two published sample datasets, with data defects separated from
spec gaps.

## The Playbook is a second source, and descriptions are not ours to write

`spec/playbook.md` is the specification's companion prose, linked from
`introduction.html` as one of its three published artifacts and pinned by
`spec/PLAYBOOK-MANIFEST.json`. Read it when a field's meaning is underdetermined:
it carries the measurement conventions, the ID scheme and the left/right grammar
that the field descriptions only gesture at.

**Do not move Playbook text into a model's description.** Every one of the 149
attributes and 29 feature types already has a description, generated from
upstream's own structured JSON, so there is no gap to fill -- and where the
Playbook says more, it frequently says something the specification *contradicts*.
Writing our resolution into a description forks the spec quietly, and the
eventual upstream answer may go the other way. File the disagreement instead:
`docs/spec-review.md` records it and Appendix B stages it for
[`dotbts/BPA`](https://github.com/dotbts/BPA).

The one thing that does belong here is a vocabulary the spec publishes but leaves
open -- `SuggestedValues`, per the section below. The Playbook adds no new values
to any of them; its `bikeway_type` names are all already in `listed_values`.

## The extension tables are hand-written, and transcribed

`lrs.json`, `events.json` and `relations.json` are declared in section 2.1 and
published only as field tables in a PDF, so `codegen` has nothing to read and
`models/extensions.py` is written out by hand from `spec/extensions.json`, a
transcription of that PDF.

Two rules follow. **Change the transcription, not the model, when the PDF moves**
-- `tests/test_extensions.py` asserts the models match it field for field and in
order, and asserts the transcription matches the PDF's own text, so a drift on
either link fails. **A per-column decision belongs in the transcription too**,
not spread across annotations: the vocabularies are checked against
`listed_values`, and which columns may hold a list is `multiple`, which carries
the sentence from that column's description that licenses it. A class like
`ScalarOrListConstraint` is the mechanism; the set it applies to is data, and a
test joins them. **Do not add a `Tier` annotation to any of them**: the
extensions sit outside the tier model, which the Playbook says outright of the
LRS one, and the PDF gives one Required/Optional flag per field rather than the
four-slot presence rule a core field gets.

They are not Overture `Feature`s -- the three files are plain JSON, not GeoJSON
-- so the system's own tag provider does not tag them `feature` and a
`--tag feature` run drops them. `gatis.tag_providers` supplies `gatis:extension`
and `gatis:table=<name>` instead, the three rows are registered under
`overture.models` in `pyproject.toml`, and `scripts/generate-reference` asks for
both tags. **Registering a new model means editing three places**: the entry
point, the tag provider if it needs a tag the system will not infer, and the
script's tag list.

One constraint exists because of that pipeline. A field typed `str | list[str]`
raises `UnsupportedUnionError` in the codegen -- a multi-arm union renders only
when every arm is a `BaseModel` -- and the whole model then gets no page, so the
seven scalar-or-list columns use `ScalarOrListConstraint` instead. Reach for a
constraint rather than a bare `BeforeValidator`/`PlainSerializer` pair here for a
second reason as well as the usual one: the markdown renderer prints unknown
annotation metadata as its `repr`, so a bare validator stamps a memory address
into `docs/reference/` and the generated output differs on every run.

## Express a rule as a declaration, not as a validator

**Reaching for `@model_validator` or `@field_validator` is the reflex to
interrupt here.** It is the right tool in an ordinary Pydantic codebase and the
wrong one in this package, because a validator runs only for a caller who
imports `gatis`. Most consumers of this work will never import it -- they will
read the JSON Schema. A rule written as a Python function is invisible to all of
them, and nothing about the code says so.

The alternative is an Overture `ModelConstraint` (see
[`src/gatis/constraints.py`](src/gatis/constraints.py)). Subclass it, implement
`validate_instance` for the Python side and `edit_config` for the schema side,
and the same rule reaches both. `AllOrNoneConstraint` and
`ForbiddenOnRoadConstraint` are the two worked examples; the field-level
equivalent is `PatternConstraint` and friends from
`overture.schema.system.field_constraint`, which is why `GatisDate` is an
annotated `str` rather than a validator that parses dates.

**A wire encoding is a declaration too.** `YesNoConstraint` owns GATIS's
`"yes"`/`"no"` booleans -- the parse, the serialisation and the emitted
`{"type": "string", "enum": ["yes", "no"]}` -- where a `BeforeValidator` plus
`PlainSerializer` would coerce for importers and tell the schema nothing.

**A declaration need not be a rule.** Where the spec names values but leaves
the type open -- `listed_values` on a `Text` field -- use `SuggestedValues`,
not a sentence in the description. It rejects nothing (`FieldConstraint.validate`
defaults to a no-op) and still reaches both sides: `field_vocabularies()` from
Python, `examples` from the JSON Schema. A vocabulary in prose is one no
transformation can act on.

**The measurement that settles it**, and the reason this section exists:
`forbidden_on_road` was first written as a `@model_validator(mode="before")`
that raised. It worked, it had tests, it passed review. Generating the JSON
Schema showed the rule absent from it entirely, while `all_or_none` -- ten lines
above in the same file -- was present, because that one implements
`edit_config`. The bug was invisible from inside Python and one command away
from outside it.

Upstream's own encoding is a further step in the same direction and worth
imitating where the container allows: `edges_schema.json` expresses "these
attributes are forbidden on a road edge" by *enumerating the permitted ones and
closing the set*, with no code anywhere. Constraints as data beat constraints as
functions; we cannot close the set here only because section 6.1 requires an
unknown field to warn rather than fail.

**Two limits, so nobody discovers them the hard way.** The JSON Schema hook works
for a third-party constraint; the PySpark codegen target does not -- it
dispatches over a closed set of the system's own constraint types and raises
`TypeError` on ours, with no registry to opt into (Overture `bd-ic2h`). That
target is unusable for these models regardless: it raises on `Tier` before
reaching any constraint, so do not read a PySpark failure as a verdict on
whichever constraint you just added. And
`ModelConstraint`'s docstring advertises portability across codegen targets,
which is true of constraints defined in the system package and not of ours. The
schema hook is the portability actually on offer today.

When a rule genuinely cannot be declared -- `drop_null_properties` is the
standing example, since coercing input is parsing rather than constraining -- a
validator is correct. Say in a comment why it could not be a constraint, so the
next reader can tell a considered choice from a reflex.

## Layout

| Path | What it is |
| --- | --- |
| `spec/specification/` | The generation source: 1.0's own structured JSON, pinned by upstream commit in `MANIFEST.json` |
| `spec/repairs.json` | Local corrections to upstream's mangled `listed_values`, with reasoning per entry |
| `spec/json-schemas/` | Upstream's own validator. **Rejects every real GATIS feature** -- see below. Never cite it as evidence about the spec |
| `spec/playbook.md` | The GATIS Playbook, the spec's companion prose, pinned separately because it lives in Google Docs. Underscores arrive escaped |
| `spec/extensions.pdf` | Upstream's field tables for `lrs.json`, `events.json` and `relations.json`, plus a `pdftotext` extraction. The only place they are published |
| `spec/extensions.json` | **A local transcription** of that PDF, not upstream. The source `models/extensions.py` is tested against |
| `src/gatis/models/extensions.py` | The three extension tables. Hand-written, not bootstrapped -- codegen has no structured source to read |
| `src/gatis/spec_source.py` | Reads the snapshot into `FieldSpec`, `FeatureType`, `PresenceRule` |
| `src/gatis/codegen.py` | Generates the models; `scripts/bootstrap-models` drives it |
| `src/gatis/models/` | Bootstrapped once, **hand-owned after** -- the bootstrap refuses to overwrite without `--force` |
| `src/gatis/dataset.py` | The five files together; checks needing more than one of them |
| `docs/reference/` | **Generated, never hand-edited.** `scripts/generate-reference` wipes and rewrites it; run that instead of editing |
| `docs/spec-review.md` | Defects found in the spec while modelling it |

<!--
The "never hand-edited" is load-bearing because a sed sweep looks equivalent and
is not: some of docs/reference/ is derived from the package name rather than
written anywhere. `_category_.json`'s `label` is the package name title-cased, so
the 2026-09-21 `gatis_schema` -> `gatis` rename left `"Gatis Schema"` behind and
no grep for the old name could find it. Overture's markdown generator exposes no
override for that label.
-->

## Commands

```
uv sync --dev
uv run pytest
uv run mypy .
uv run ruff check . && uv run ruff format --check .
./scripts/snapshot-spec        # refresh spec/ from upstream
./scripts/snapshot-playbook    # refresh spec/playbook.md from Google Docs
./scripts/bootstrap-models     # regenerate models (refuses to clobber)
./scripts/generate-reference   # rebuild docs/reference/ from the models
./scripts/compare-json-schema  # ours vs upstream's JSON Schema
./scripts/validate-sample FILE # validate a GATIS GeoJSON file
```

`scripts/` holds executables with no extension. Python ones use
`#!/usr/bin/env -S uv run python`; keep both `ruff` and `mypy --strict` clean,
which means annotating them as if they were library code.

## Asking about the Overture schema system

`overture-schema-system` conventions -- `Omitable`, `Feature`,
`GeometryTypeConstraint`, the codegen, JSON Schema behaviour -- are documented in
the Overture schema workspace, not here. Reading a file over there needs nothing
special; do it inline. For judgment questions, spawn a delegate rooted in
`/Users/seth/src/overturemaps/schema-workspace/worktrees/main`, because CLAUDE.md
discovery is keyed to a session's project root and `--add-dir` does not load it.
Procedure: `~/src/sethfitz/tarn/runbooks/delegating-foreign-repo-work.md`.
