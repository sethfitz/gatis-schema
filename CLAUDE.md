# gatis-schema

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
NodeAdapter.validate_json(json.dumps(feature))   # correct
NodeAdapter.validate_python(feature)             # every field reads missing
```

The rest -- why optional-field errors arrive twice, why paths read
`road.road.width`, how explicit `null` behaves -- is in
[`.claude/rules/validating-gatis-data.md`](.claude/rules/validating-gatis-data.md).

`scripts/validate-sample <file.geojson>` runs a classified report over a whole
file. [`docs/sample-data-validation.md`](docs/sample-data-validation.md) is what
it found on the two published sample datasets, with data defects separated from
spec gaps.

**Quote per-field counts from that report, never a defect-class subtotal.** A
class holds several unrelated causes, so its total is not a count of whatever
you would name it after. Count anything narrower from the data.

## Layout

| Path | What it is |
| --- | --- |
| `spec/specification/` | The generation source: 1.0's own structured JSON, pinned by upstream commit in `MANIFEST.json` |
| `spec/repairs.json` | Local corrections to upstream's mangled `listed_values`, with reasoning per entry |
| `spec/json-schemas/` | Upstream's own validator. Sound on types, **broken on every `Array<Enum>`** |
| `src/gatis_schema/spec_source.py` | Reads the snapshot into `FieldSpec`, `FeatureType`, `PresenceRule` |
| `src/gatis_schema/codegen.py` | Generates the models; `scripts/bootstrap-models` drives it |
| `src/gatis_schema/models/` | Bootstrapped once, **hand-owned after** -- the bootstrap refuses to overwrite without `--force` |
| `src/gatis_schema/dataset.py` | The five files together; checks needing more than one of them |
| `docs/spec-review.md` | Defects found in the spec while modelling it |

## Commands

```
uv sync --dev
uv run pytest
uv run mypy .
uv run ruff check . && uv run ruff format --check .
./scripts/snapshot-spec        # refresh spec/ from upstream
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
