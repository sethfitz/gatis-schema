# gatis-schema

Pydantic models for the [General Active Transportation Infrastructure
Specification](https://github.com/dotbts/BPA) (GATIS) v1.0, generated from a pinned
snapshot of the published spec.

GATIS describes the infrastructure people use to walk, roll, cycle and use
micromobility devices: sidewalks, crossings, curb ramps, bikeways, paths and the
roads they interact with. It is a US national effort convened by the Bureau of
Transportation Statistics, published as five GeoJSON/JSON files -- `nodes`, `edges`,
`points`, `zones` and `metadata`.

## Status

Early, and now tracking the version that was voted through rather than a draft.
GATIS v1.0 passed unanimously on 2026-02-27 and is published as JSON in
`dotbts/BPA`; this package regenerated against it on 2026-09-21, replacing a
snapshot pinned to what upstream calls Draft #2.

- `spec/` -- pinned snapshot of `dotbts/BPA`, refreshed by `scripts/snapshot-spec`.
  See [`spec/README.md`](spec/README.md) for provenance and the upstream defects it
  records.
- `gatis_schema.spec_source` -- reads that snapshot into typed records
  (`FieldSpec`, `FeatureType`, `PresenceRule`).
- `gatis_schema.presence` -- the tier-varying presence grammar.
- `gatis_schema.models` -- the models themselves, bootstrapped by
  `scripts/bootstrap-models` and hand-owned from there.
- `gatis_schema.dataset` -- the five files together, and the checks that need
  more than one of them: unique ids within a file, and `from_node`/`to_node`
  resolving into `nodes.geojson`.
- `scripts/compare-json-schema` -- our generated JSON Schema against the one
  upstream ships. Two renderings of one spec; where they disagree, one is wrong.
- [`docs/spec-review.md`](docs/spec-review.md) -- defects found in the spec while
  modelling it, plus critiques from Overture's experience and from what the
  GeoJSON container has quietly decided.

## Why generate rather than hand-write

Seventy-eight edge fields across fourteen edge types across four tiers is 4,368
presence decisions. Hand-transcription would be stale on arrival, and its drift
would be invisible -- which is exactly what happened to the previous snapshot,
which sat two drafts behind for seven months without anything noticing. The spec is
snapshotted at an upstream commit, and the models are a function of that snapshot.

## Design notes

**Presence is four-dimensional.** `(feature class x feature type x field x tier)`
maps to one of `required`, `recommended`, `optional`, `forbidden`. v1.0 publishes
the tier axis as a four-slot array, `null` meaning unchanged from the tier before:

```json
"sidewalk": ["optional", "required", null, null]
```

`PresenceRule.at(tier)` resolves it. Draft 2 also had `conditionally_required`;
v1.0 dropped the descriptor.

**`forbidden` never varies by tier** (asserted by a test). The set of fields a
feature type may carry is fixed; only presence strength moves. That is what makes
one generated model per feature type the right shape, rather than one wide model
with a runtime matrix.

**Units are in the field name.** v1.0's headline modelling change: `width_in`,
`buffer_width_ft`, `posted_speed_limit_mph`, `crossing_time_sec`. Fifteen fields
carry the unit as a suffix, which is what makes it machine-readable at all --
draft 2 stated every one of them in prose only. They are not uniform (widths are
inches, buffers are feet), so a consumer converting GATIS to another schema still
needs to read the suffix. `gatis_schema.annotations` lifts it into a `Unit`
annotation. The slopes and `traffic_volume` are still prose-only.

**Booleans are OSM-style `"yes"`/`"no"` strings**, not JSON booleans.

**Unknown fields warn, they do not fail.** Section 6.1 makes local extension a
guarantee, so generated models cannot use `extra="forbid"`. A field that is
`forbidden` for its type is a different diagnostic from a field nobody has heard of.

**An explicit `null` means absent.** GATIS never says whether an unset property
should be omitted or written as `null`, and the two published sample datasets
disagree -- Austin omits, Newark writes nulls for 57% of its slots. Rejecting null
would make these models stricter than upstream's own validator on upstream's own
sample data, and GATIS assigns no meaning to the difference, so
`drop_null_properties` collapses them.

**Rules are declared, not validated in Python.** A `@model_validator` runs only
for callers who import this package; an Overture `ModelConstraint` also carries a
JSON Schema hook, so the rule reaches whoever reads the schema instead. Both rules
here are constraints -- `all_or_none` for the ADA pair, `forbidden_on_road` for the
attributes a parallel facility may not carry. The PySpark codegen target renders
neither, since it dispatches over a closed set of the system's own constraint types
(Overture `bd-ic2h`), so the schema hook is the portability actually on offer.
`CLAUDE.md` has the reasoning.

**A road edge carries its parallel facilities as prefixed attributes.** v1.0 marks
sidewalk, bikeway and multi_use_path `allowed_on_road`, so a roadway centerline can
describe the sidewalk or bike lane beside it as `bikeway:left:width_in` rather than
as a separate feature. `RoadEdge` declares all 292, typed and aliased — the same
292 upstream's JSON Schema enumerates, derived here independently. Leaving them to
`extra="allow"` was the alternative and it is worse than it looks: the values
round-trip, so nothing fails, and a consumer silently reads conforming bikeway data
as an unrecognised local extension.

**Enums are named per feature class where the vocabularies differ.** Nine field
names mean different things in different files -- `status` alone has three
vocabularies -- so the generated enums are `EdgeStatus`, `NodeStatus`,
`ZoneStatus` rather than one `Status` whose values depend on which module was
written last.

## Development

```
uv sync --dev
uv run pytest
uv run mypy .
./scripts/snapshot-spec           # refresh spec/ from dotbts/BPA; requires gh
./scripts/bootstrap-models        # reseed the models from spec/
./scripts/compare-json-schema     # ours vs upstream's JSON Schema
```

## Licence

MIT, in [`LICENSE`](LICENSE).

That covers this repository's own work -- the models, the generator, the scripts
and the documentation. It does not cover what `spec/` vendors. Those files are a
pinned snapshot of [`dotbts/BPA`](https://github.com/dotbts/BPA), whose
`LICENSE.md` dedicates them to the public domain under CC0 1.0 as a work of the
United States Government under 17 USC 105. `spec/playbook.md` states the same
dedication in its own text. The commit each is pinned to is in
`spec/MANIFEST.json` and `spec/PLAYBOOK-MANIFEST.json`.
