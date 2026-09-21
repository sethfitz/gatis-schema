# gatis-schema

Pydantic models for the [General Active Transportation Infrastructure
Specification](https://github.com/dotbts/BPA) (GATIS) v2 draft, generated from a
pinned snapshot of the upstream spec workbook.

GATIS describes the infrastructure people use to walk, roll, cycle and use
micromobility devices: sidewalks, crossings, curb ramps, bikeways, paths and the
roads they interact with. It is a US national effort convened by the Bureau of
Transportation Statistics, published as five GeoJSON/JSON files -- `nodes`, `edges`,
`points`, `zones` and `metadata`.

## Status

Early. The spec snapshot and the reader that parses it are in place; model
generation is not.

- `spec/` -- pinned snapshot of the upstream workbook and document, refreshed by
  `scripts/snapshot-spec`. See [`spec/README.md`](spec/README.md) for provenance and
  the upstream defects it records.
- `gatis_schema.spec_source` -- reads that snapshot into typed records
  (`FieldSpec`, `FeatureType`, `PresenceRule`).
- `gatis_schema.presence` -- the tier-varying presence grammar.

## Why generate rather than hand-write

Sixty-five edge fields across twelve edge types across four tiers is 3,120 presence
decisions, and the upstream workbook is a live drafting document that moved twice in
the week this package was started. Hand-transcription would be stale on arrival, and
its drift would be invisible. The workbook is snapshotted with its Drive revision,
and the models are a function of that snapshot.

## Design notes

**Presence is four-dimensional.** `(feature class x feature type x field x tier)`
maps to one of `required`, `recommended`, `optional`, `conditionally_required`,
`forbidden`. The workbook packs the tier axis into one cell:

```
optional
T3:recommended
T4:required
```

`PresenceRule.at(tier)` resolves it.

**`forbidden` never varies by tier** (asserted by a test). The set of fields a
feature type may carry is fixed; only presence strength moves. That is what makes
one generated model per feature type the right shape, rather than one wide model
with a runtime matrix.

**Units are fixed by the schema and stated only in prose.** Eighteen fields carry a
dimension -- inches, feet, miles per hour, percent -- and none of it is
machine-readable upstream. Unlike Overture, GATIS never carries a unit as a per-row
value, so every one of them is the fixed-unit case, and they are not uniform: widths
are inches, buffers are feet. Anything converting GATIS to another schema needs the
unit programmatically.

**Booleans are OSM-style `"yes"`/`"no"` strings**, not JSON booleans.

**Unknown fields warn, they do not fail.** Section 6.1 makes local extension a
guarantee, so generated models cannot use `extra="forbid"`. A field that is
`forbidden` for its type is a different diagnostic from a field nobody has heard of.

## Development

```
uv sync --dev
uv run pytest
uv run mypy .
./scripts/snapshot-spec   # refresh spec/ from upstream; requires gws
```
