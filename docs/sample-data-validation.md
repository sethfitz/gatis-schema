# Validating the published GATIS sample datasets

Austin's published GATIS data is substantially conformant and Newark's cannot be
read at all. Neither fact was visible at first: against the models as they stood
in September 2026, all 351,693 features in both datasets failed, and that number
measured our models rather than the data.

The datasets are the two linked from the [GATIS
Explorer](https://dotbts.github.io/BPA/gatis_explorer/pages/sample_datasets.html):
Austin, TX (Tier 2, city data) and Newark, DE (Tier 3, city data). Reproduce with
[`scripts/validate-sample`](../scripts/validate-sample). Measured against
`f62df13`.

| File | Features | Valid | What stops the rest |
| --- | --- | --- | --- |
| `austin_nodes` | 9,979 | **9,979 (100%)** | -- |
| `austin_edges` | 334,007 | **247,710 (74%)** | `date_built` 73,482, `directionality` 9,929, `cross_vehicle_traffic_control` 2,886 |
| `newark_edges` | 4,283 | 0 | numeric identifiers on every feature; 3,746 validate once coerced |
| `newark_nodes` | 3,424 | 0 | every node is `virtual`, a type 1.0 removed |

Newark's zero is two structural facts, not 4,283 bad records. Both are one
find-and-replace away from most of the file reading cleanly.

Getting here took four rounds, and the sequence is the point: each fix made the
next defect visible. Rejecting explicit `null` hid 474 missing `street_name`
values; requiring an `id` inside `reference_ids` hid 247,710 valid Austin edges;
and not modelling the on-road modifier form hid 292 fields on 4,003 roads. None
of those announced itself, because each looked like the data being wrong.

The findings below are grouped by who has to act: the specification, the
publishers, or nobody, because a shape check cannot see the problem at all.

## The two publishers disagree about how to say "absent"

Austin omits a field it has no value for: 6.95 property keys per edge, zero
nulls in 334,007 features. Newark writes every field on every feature and nulls
the ones it lacks: 60 keys per edge, 34.25 of them null, 146,710 nulls in 4,283
features. One dataset is sparse, the other rectangular, and neither is wrong,
because GATIS never says.

This is the single largest source of failures and it is a specification gap, not
a data defect. The 1.0 `specification_jsons` carry a type and a presence matrix
per attribute and say nothing about null. Upstream's own JSON Schema permits
null on 159 of 370 edge fields through `oneOf [..., {"type": "null"}]`, so the
spec's own validator accepts what our models reject -- on data the spec's own
authors published.

The asymmetry decided it. Accepting null costs a distinction GATIS never drew:
`status` says outright that a blank is assumed `open` or `unknown` depending on
feature class, so there is no "known empty" versus "unknown" semantics being
discarded. Rejecting null costs the ability to read either published dataset.
The models now drop null-valued properties before validation, so a null means
absent. The specification gap is untouched by that and is still worth reporting
upstream.

## `reference_ids` is the most-violated field and constrains nothing

It accounts for every Austin failure and 4,237 Newark ones, and no publisher is
at fault. GATIS 1.0 types it `Array<Object>` with `listed_values: null`, and the
description is still the draft's prose -- *"an array of JSONs with the source
name and ID pair. Each JSON should contain an ID field and source field at
minimum."* Upstream's JSON Schema renders that as `{"type": "object",
"properties": {}}`: any object validates.

So the four encodings in the wild are equally conformant, because there is
nothing to conform to:

```
{"source": "austin",  "sidewalks_id": "94639273"}
{"source": "austin",  "source_url": "", "CURB_RAMPS_ID": 15866993}
{"source": "austin",  "asmp_street_network_id": "330428"}
{"source": "newark",  "edge_id": 1070387}
```

Every one puts the identifier under a source-specific key; none uses `id`. Our
`ReferenceId` requires `source` and `id`, which is a reasonable reading of the
prose and stricter than anything upstream enforces. This is the only join key
GATIS offers to OSM, Overture, ARNOLD, TIGER or an LRS, and it is unusable as
one: a consumer cannot find the identifier without per-source knowledge. Report
it upstream as the costliest gap in the schema; do not report it as a data
defect.

## Defects that are real

Four, and they stay defects against 1.0.

**Identifiers are not strings.** 1.0 types `edge_id`, `node_id`, `from_node` and
`to_node` as `ID`, which its JSON Schema resolves to `{"type": "string"}`.
Newark ships all of them as numbers, and its endpoint references as floats:
`from_node: 2000000.0`. All 3,424 Newark nodes, and 12,757 identifier values
across its 4,283 edges. Floats are the worse half -- `2000002.0` and `2000002`
are the same node, and nothing in the format says so.

**`directionality` is missing from every Austin road.** 1.0 makes it `required`
for `road` from Tier 1, so it is a violation at any tier. 9,929 features.

**`cross_vehicle_traffic_control` is sent as a bare string.** 1.0 types it
`Array<Enum>`. Austin sends `"traffic signal"`, Newark `"standard signal"`.
2,895 features.

**`separation_elements` is sent as a bare string.** 1.0 types it `Array<Text>`.
Newark only, 22 features, values like `"mountable concrete barrier"` and
`6"concrete curb`.

Four values fall outside their 1.0 vocabulary, but only one of them is a
publisher error. The other three name real devices GATIS cannot express, so
they belong upstream as vocabulary gaps; the case for each is under [The four
out-of-vocabulary values](#the-four-out-of-vocabulary-values-are-three-gaps-and-one-synonym).

## Defects no schema will catch

The Austin dates pass every structural check and are meaningless.

8,815 of 9,979 curb-ramp nodes carry `last_inspection_date: "1970-01-01"`. That
is Unix epoch zero -- an Esri export rendering a null date field -- and it
matches `GatisDate`'s `YYYY-MM-DD` pattern exactly. 88% of the column is
schema-valid garbage, and a validator that checks shape reports it clean.

Separately, all 73,482 non-null Austin `date_built` values are full RFC 3339
datetimes, `2007-01-01T00:00:00-06:00`, where 1.0 types the field `Date`. Every
one is midnight at the same offset and there are 42 distinct values across
73,482 features, so the column carries a year and eleven characters of export
padding. This one our models do catch, because `GatisDate` anchors its pattern.

Both are the same shape: the container accepts a value the semantics do not.
1.0 names a type vocabulary -- `ID`, `Date`, `Boolean`, `Array<Enum>` -- and
defines it in no machine-readable place, so each consumer re-invents what `Date`
admits. A profile check catches these; a JSON Schema does not.

## Version drift, which was never a finding about the data

The models were generated from Draft #2 (workbook Drive revision 3542,
2026-01-30) when this run started. GATIS 1.0 was voted through 2026-02-27, and
the sample datasets were refreshed 2026-04-17 and 2026-06-01 -- both after that
snapshot. Three classes of failure were our models being out of date, and all
three are gone now that the models track the spec pinned in
`spec/MANIFEST.json`. They are recorded because the same trap is still live for
anyone reading GATIS data: it is what a stale model looks like from the inside,
and it is indistinguishable from bad data until you check.

- `vehicle_traffic_control` and `ped_traffic_control` were renamed. 1.0 has
  `traffic signal` and `pedestrian signal`; Draft #2 had `standard signal`.
  Austin matches 1.0. 5,772 features.
- `status` was widened to include `unknown`, and now differs by feature class:
  edges take `proposed and funded` and `proposed - not yet funded`, nodes take
  `planned`, zones take `other`. Three vocabularies and two blank-defaults for
  one field name. 2,564 features.
- `road_associated` is required by our `multi_use_path` model and is not an
  attribute in 1.0 at all. 2,564 features.

Newark carries 19 edge property keys 1.0 does not define, and they are not local
extensions -- they are Draft #2 names that 1.0 renamed by suffixing the unit:
`width` to `width_in`, `curb_height` to `curb_height_in`, `buffer_width` to
`buffer_width_ft`, `posted_speed_limit` to `posted_speed_limit_mph`,
`car_freeflow_speed` to `mv_freeflow_speed_mph`. That retires the README's
observation that GATIS units are machine-unreadable: for 1.0 they are in the
field name. It also means a consumer cannot tell a Draft #2 dataset from a 1.0
one except by field vocabulary, since neither file declares a spec version.

## What the model fixes changed

Three changes account for the whole difference between "nothing validates" and
the table at the top. Null-valued properties are dropped before validation, so
Newark's 31,865 null failures go to zero. `ReferenceId` was relaxed to what 1.0
constrains -- `Array<Object>`, any object conforms. And the models moved from
Draft #2 to 1.0, retiring the drift below.

| | before | after |
| --- | --- | --- |
| `austin_nodes` | 0 / 9,979 | **9,979 / 9,979 (100%)** |
| `austin_edges` | 0 / 334,007 | **247,710 / 334,007 (74%)** |
| `newark_edges` | 0 / 4,283 | 0 / 4,283 |
| `newark_nodes` | 0 / 3,424 | 0 / 3,424 |

Austin was a substantially conformant dataset the whole time. Requiring `id`
inside `reference_ids` -- a field 1.0 declines to constrain -- was the
difference between reading none of it and reading three quarters.

Austin's 86,297 remaining failures are three causes that do not overlap:
`date_built` 73,482, `directionality` 9,929, `cross_vehicle_traffic_control`
2,886.

Newark still reads as zero, for two reasons that are not about field values.
Every node carries a retired type name, and every edge carries a numeric
identifier; 12,783 identifier values across 10 fields. Normalise the
identifiers and 3,746 of 4,283 edges validate. What remains after that is
`street_name` 474, `directionality` 6 -- both required, both null, and both
masked by the null flood until 1.0 started dropping nulls -- `traffic_volume`
26 as the float `490.00000000000006`, and the vocabulary cases below.

348,223 features carried a `reference_ids` entry with no `id` key: every Austin
feature and 4,237 Newark edges. Counted directly, not inferred from the error
output.

### Three defects the 1.0 run exposed

**`virtual` is no longer a node type, and it is Newark's only one.** 1.0
declares `curb_ramp`, `generic`, `ramp_to_street_transition` and
`sidewalk_to_ramp_transition`. All 3,424 Newark nodes are `virtual`, which
Draft #2 defined and 1.0 removed; `generic` appears to be its replacement. The
whole file is unreadable against 1.0 for this one reason.

**`presence` has a different, and broken, vocabulary on nodes than on edges.**
Edges list `yes`, `no`, `missing`, `unknown`. Nodes list `yes`, `no | missing`,
`unknown` -- three members, the middle one a pipe-joined pair that was never
split. Austin sends `no`, valid on an edge and invalid on a node, on 426 curb
ramps. This is a different failure from the newline-split mangling in
`spec/repairs.json`: the separator here is a pipe the exporter never treated as
one.

**The models did not implement the on-road modifier form, and Austin uses it.**
1.0 marks `sidewalk`, `bikeway` and `multi_use_path` as `allowed_on_road`,
which lets a road edge carry them as prefixed attributes,
`bikeway:left:bikeway_type`, with seven fields forbidden in that form. Austin
uses it on 4,003 road edges. Those values were landing in `model_extra` and
reading as unrecognised local extensions -- nothing failed, so a consumer would
have lost the bikeway data on 4,003 roads against a clean validation report.

Fixed in `f39758d`: `RoadEdge` declares all 292 modifier fields, typed and
aliased. Re-deriving the set independently from `spec/specification/edges.json`
-- each `allowed_on_road` type's attributes with a non-forbidden tier-1
presence, minus its `forbidden_field_if_allowed_on_road`, times two sides --
gives exactly the 292 declared. That confirms the generator against the spec
source; it does not confirm the reading of
`forbidden_field_if_allowed_on_road`, since both derivations share it.

One half remains unenforced. `forbidden_field_if_allowed_on_road` excludes
names from the model but does not reject them, so `bikeway:left:edge_id`
validates as an extra rather than failing. Same silent-degradation shape, one
scale smaller.

### The four out-of-vocabulary values are three gaps and one synonym

All 23 features carrying them are bikeways and crossings on a single street,
Delaware Avenue in Newark. That is one facility coded by one publisher, not a
pattern across publishers, so the case for each rests on the device being real
and unrepresentable, not on how often it appears.

- **`separation_permeable_car: "mountable"` (14) is a genuine gap.** The
  vocabulary is a binary -- hard means a separator motor vehicles cannot bypass,
  soft means one they can. A mountable concrete barrier is neither: crossing it
  requires mounting it. The publisher used `hard separator` for a 6-inch
  concrete curb and `mountable` for a mountable one, so they drew the
  distinction deliberately and consistently.
- **`bikeway_grade_separation: "intermediate"` (2) is a genuine gap.** A bike
  lane raised above the roadway but below the sidewalk is standard separated
  bike lane practice, and `at_grade | raised | sidewalk_level` cannot say it.
  Both features also carry `mountable`, which is the same facility described
  twice.
- **`vehicle_traffic_control: "bicycle traffic signal"` (7) is a genuine gap,
  and a structural one.** A bicycle signal face is a distinct MUTCD device.
  GATIS has `vehicle_traffic_control` and `ped_traffic_control` and no bicycle
  equivalent, so a bikeway crossing controlled by a bicycle signal cannot be
  described in an active transportation specification.
- **`vehicle_traffic_control: "none"` (2) is a synonym, not a gap.** 1.0 offers
  `no vehicle control`, which means exactly this. A data defect.

### Newark's bikeway layer is topologically disconnected

All 33 Newark `bikeway`, `crossing` and `traffic_island` edges carry null
`from_node` and `to_node`, so the bikeway and crossing layer cannot be routed
and `Dataset.check_integrity` has nothing to resolve for it. Ten `road` and
three `multi_use_path` edges lack endpoints too -- 46 in all -- and for those
five types 1.0 makes both fields `required` from Tier 2, so 34 of the 46 are
presence violations at Newark's Tier 3 rather than an absent optional. While explicit nulls
were rejected this was 21 more rows in the null pile; dropping nulls is what
makes it visible as a structural property of the dataset.

## What the run could not check

Both datasets ship only `edges` and `nodes`. Nothing exercises `points`,
`zones`, or `metadata.json`, and `Dataset.check_integrity` was not run, so
`from_node`/`to_node` resolution across the two files is unmeasured -- Newark's
floats would need normalising first, and its bikeway layer has no endpoints to
resolve. Austin ships curb-ramp nodes and sidewalk edges that do not reference
them, so the two files may not describe one graph at all.

`scripts/validate-sample` counts unknown fields only on features that
validate, so Newark's contribute nothing: its 19 unrecognised keys were found
by set-differencing against the 1.0 attribute list, and they are older-draft
renames rather than extensions. Austin can be counted, and across its 247,710
valid edges and 9,979 valid nodes there are no local extensions at all.
