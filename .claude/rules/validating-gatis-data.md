# Validating GATIS data against these models

`scripts/validate-sample <file.geojson>` does all of this already. Read on when
writing new validation code or reading raw Pydantic output.

## Validate from JSON text, never from a parsed dict

`overture.schema.system.feature.Feature` unwraps the GeoJSON envelope in a
`model_validator(mode="wrap")` guarded by `if info.mode == "json"`. Pydantic
sets that mode from the *method*, not the data, so a dict never takes the
branch:

```python
NodeAdapter.validate_json(json.dumps(feature))  # envelope unwrapped
NodeAdapter.validate_python(feature)  # every field reads missing
```

`validate_python` fails in a way that looks like a data problem -- `node_id
Field required`, `node_type Field required`, on a feature that has both -- so
the symptom points away from the cause. The discriminator still works, because
`Feature.field_discriminator` sniffs for `{type, geometry, properties}` and
reaches into `properties` itself; only field validation is affected.

Validating one feature at a time therefore costs a re-serialise
(`json.dumps`). That is cheap: 334,007 features validate in about 10 seconds.
Do it per feature anyway. `Collection.model_validate_json` over the whole file
does not stop early -- it reports every error across every feature, which is
the problem: Newark's 4,283 edges yield a single `ValidationError` carrying
93,137 of them. Per-feature validation also gives you the count of features
that passed and each failure's `edge_type`, neither of which the collection
error hands you.

## Reading the errors

Two artifacts of how the models are built make raw output roughly three times
longer than the defect count, and both are noise:

- **Every optional-field failure arrives twice.** `Omitable[T]` is a union of
  `T` and a MISSING sentinel, so you get the real error plus
  `missing_sentinel_error: Input should be the 'MISSING' sentinel`. Drop any
  error whose `loc` contains `missing-sentinel`.
- **Paths repeat the discriminator tag**, as `road.road.width`, and end in a
  union-arm descriptor, as `width.constrained-float`. Strip a leading element
  equal to the tag and a trailing element containing `[` or `-`.

Bucket by `(feature type, field, cause)` rather than listing errors. One cause
routinely accounts for six figures of them.

**A class total from the report is not a count of the thing you would name it
after.** `wrong JSON scalar type` is a defect class; it holds every non-string
identifier *and* a fractional `traffic_volume`, so quoting its total as "the
identifier failures" overstates by 26. The per-field lines are safe because
they name a field; the class subtotals are not, and neither is any figure you
reach by adding them up. Before a count goes in a document or upstream, count
it from the data:

```python
sum(
    1
    for f in features
    for k in ("edge_id", "from_node", "to_node")
    if not isinstance(f["properties"].get(k, ""), str)
)
```

Validator output is exhaust -- derived, lossy about the distinction you care
about, and well-formed either way. Re-deriving a count from the source also
catches what the error path cannot show you: `reference_ids` looked like
348,223 failures until counting the data showed `newark_nodes` carries the
field zero times.

## Probing the models: assert the fixture validates first

A hand-built feature for a one-off probe is harder to get right than it looks,
because required fields vary by feature type and the discriminator hides which
ones. A fixture missing one fails with `missing`, identically, for every case
you then run against it -- so a battery of positive and negative cases all come
back rejected and read as a finding about the models.

Make the bare fixture a control and assert it before reading anything:

```python
m = EdgeAdapter.validate_json(json.dumps(base))  # must pass, or stop here
print(f"apparatus ok: {type(m).__name__}, extras={m.model_extra}")
```

A minimal `road` needs `edge_id`, `edge_type`, `directionality` and
`street_name`; other types differ, so derive the set from the `missing` errors
on an empty-properties feature rather than guessing. Then assert in both
directions -- a case that must validate and a case that must fail -- because a
fixture broken a second way makes everything fail and everything look
conclusive.

## Explicit `null` is rejected, and real data is full of it

`Omitable[T]` accepts the field being absent; it does not accept the field being
present with value `null`. Publishers split on this -- Austin omits, Newark
nulls 34 of 60 property slots on every feature -- and GATIS states no preference
either way. Upstream's own JSON Schema permits null on 159 of 370 edge fields.

So a run against a rectangular export reports thousands of failures that are one
unstated spec question. Classify an error whose input is `None` separately from
everything else before drawing any conclusion about the data; `scripts/validate-sample`
calls that class `explicit null for an absent field`.

## Schema-valid is not meaningful

The models check shape. They cannot see that 8,815 of Austin's 9,979
`last_inspection_date` values are `1970-01-01` -- Unix epoch zero, an Esri
export writing null as a date -- which matches `GatisDate` perfectly. When a
column validates, check its value distribution before reporting it clean:

```sh
jq -r '[.features[].properties.some_field] | group_by(.) | map({v:.[0], n:length})
       | sort_by(-.n) | .[:5][] | "\(.n)\t\(.v)"' file.geojson
```

Epoch zero, `1900-01-01`, `-9999`, `0` and empty string are the usual sentinels.

The same blind spot has a structural form, and `extra="allow"` is what creates
it: anything the models do not declare becomes `model_extra` and reports clean.
So a mechanism the spec defines and the models miss looks exactly like a local
extension.

**The check is to count extras on features that validate**, and it only works
once something does -- which is why it found nothing here until Austin's edges
started passing. Treat a cluster of similarly-shaped unknown keys as a missing
feature rather than as publisher invention. That is how the on-road modifier
form was found: 1.0 marks `sidewalk`, `bikeway` and `multi_use_path`
`allowed_on_road`, Austin sent `bikeway:left:bikeway_type` on 4,003 roads, and
all 292 modifier fields were landing in `model_extra`. `RoadEdge` declares them
now.

The other half of that mechanism is enforced too: each `allowed_on_road` type's
`forbidden_field_if_allowed_on_road` names are rejected rather than merely left
undeclared, so `bikeway:left:edge_id` fails instead of passing as an extra.
Verified in both directions on `f62df13` -- forbidden names fail, a legal
modifier and a genuinely unknown key both still behave.

## Before calling a mismatch a data defect

A failing enum value may be data written against an older draft rather than
data that is wrong -- no GATIS file declares its version. Which spec the models
track is pinned in `spec/MANIFEST.json`, which is the one place that cannot go
stale; do not trust a version named in prose, here or elsewhere. Check the
value against the pinned spec's `listed_values` -- see
[`upstream-gatis-sources.md`](upstream-gatis-sources.md) -- and check the
field's `presence` for that feature type at the dataset's tier before calling a
required field missing.

Some 1.0 `listed_values` are themselves mangled, in more than one way, so a
value that fails against them has not necessarily failed against the spec:

- **Split on newline, where the workbook cell is hard-wrapped mid-sentence.**
  `separation_permeable_car` reads as six entries including `curbs)` and `""`;
  `separation_elements` ends with `trees  unknown`. The defect is in the source
  cell, not the exporter, so fixing the exporter will not fix it. Local
  corrections are in `spec/repairs.json`.
- **Not split at all, where the separator is a pipe.** `presence` on *nodes*
  lists `["yes", "no | missing", "unknown"]`; the same field on *edges*
  correctly lists four members. A dataset sending `no` on a node fails against
  a vocabulary that never got parsed.

Treat a mangled list as the semantic values its prose describes. Where a field
exists on more than one feature class, check that class's file -- 1.0 gives the
same field name different vocabularies, sometimes deliberately (`status`) and
sometimes by defect (`presence`).
