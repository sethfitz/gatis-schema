# Review of GATIS v1.0

Findings from modelling the spec in Pydantic, against the snapshot in
[`spec/`](../spec/) — `dotbts/BPA` at commit `ecc45ff8`, whose specification files
last changed 2026-02-03. GATIS v1.0 was voted through unanimously on 2026-02-27.

Four sections. **Bugs** are mechanical: each has an unambiguous fix and no design
question attached, and they are the ones worth reporting upstream. **Modelling
critiques** are drawn from what Overture has learned building a schema over the
same subject matter. **GeoJSON artifacts** are where a container's limits have
been written down as though they were design decisions. **What would move the
most** orders the rest by what it unblocks.

Counts are measured against the snapshot, not estimated. Sample-data counts come
from validating the two datasets GATIS itself publishes — Austin and Newark,
351,693 features — against the models in this repo. Every bug below is pinned by a
test or a repair entry, so an upstream fix shows up here as a failure rather than
going unnoticed.

## Bugs

Mechanical, and reportable as-is.

**`json_schemas/*_schema.json` gives every `Array<Enum>` field the wrong
vocabulary.** Each one carries the *last* such field's enum. In
`edges_schema.json`, `allowed_uses`, `prohibited_uses` and
`cross_vehicle_traffic_control` all carry `ped_protection`'s list, so
`prohibited_uses` offers "leading pedestrian interval" and does not offer "bike".
In `nodes_schema.json`, `impediment` and `rail_crossing_control` carry
`surface_issue`'s list; in `points_schema.json`, `accessibility_features` does.
Seven fields, three files, one loop-variable bug. `zones_schema.json` has no
`Array<Enum>` field and so cannot exhibit it. A publisher validating against the
shipped schema is validating against the wrong vocabulary and will be told so by
neither artifact.

**The shipped JSON Schemas declare no required fields at all.** Not `edge_id`, not
`edge_type`. Every property is optional in all four, so the published validator
cannot check presence — which is what the tier model is made of.

**The specification defines three presence descriptors and the data uses four.**
Section 2.3 defines Optional, Recommended and Required. `forbidden` appears 2,860
times across the four files — 45% of all 6,408 presence decisions — and no
published prose says what it means. It is the descriptor that carries the most
information, because it is the one that makes a field *illegal* for a type rather
than merely absent, and it is the one a reader cannot look up.

**The `listed_values` pipeline fails in three separate ways.** All three are
artifacts of publishing a spreadsheet cell as an array.

- *A pipe that was never treated as a separator.* `presence` is four values on
  edges — `yes`, `no`, `missing`, `unknown` — and three on nodes, the middle being
  the single entry `"no | missing"`. So `presence: "no"` is valid on an edge and
  invalid on a node, which is how 426 of Austin's curb-ramp nodes fail against a
  value the spec plainly intends to allow.
- *Newline-splitting a hard-wrapped cell.* `separation_permeable_car` publishes as
  six entries including `"curbs)"`, `"k-rail)"` and two empty strings, because two
  of its three definitions wrap mid-parenthetical. `markings` carries an empty
  value from a blank line.
- *A run-together line that stays fused.* `separation_elements` ends in
  `"trees  unknown"`; `allowed_uses` and `prohibited_uses` both end in
  `"motor_vehicle ebike class 2 ebike class 3 other"`, four values on one line.

`traffic_calming` additionally interleaves the section headings
`"for road edge type:"` and `"for crossing edge type:"` with its values. All seven
cells are corrected in [`spec/repairs.json`](../spec/repairs.json), which records
each departure from the verbatim snapshot and why.

**`edges.json` carries a presence column for a type it does not declare.**
`virtual_link` was removed from the edge types and left in the presence map of all
78 attributes. Generating from the presence columns — the obvious reading — puts
the type back into the data model.

**Three edge types forbid a field that no longer exists.** `sidewalk`, `bikeway`
and `multi_use_path` each list `road_associated` in
`forbidden_field_if_allowed_on_road`. v1.0 removed the attribute, so the rule
constrains nothing — and the one field that recorded an edge's relationship to a
road is gone with no replacement.

**The colon-namespaced on-road fields exist in exactly one artifact.**
`edges_schema.json` enumerates 292 of them, `sidewalk:left:width_in` through
`multi_use_path:right:width_tolerance_in`, and they are internally consistent:
exactly `{sidewalk, bikeway, multi_use_path} × {left, right} ×` that type's own
non-forbidden fields, minus the six each lists in
`forbidden_field_if_allowed_on_road`. Deriving the set from `specification_jsons`
reproduces those 292 names exactly, so the mechanism is well defined — it is just
not written down anywhere a reader will find it. They appear nowhere else.
`specification_jsons` has zero colon-namespaced attributes, and so does the
attribute table on the GATIS Explorer, which is what a publisher reads. The
mechanism is referenced from `forbidden_field_if_allowed_on_road` without the
names ever being given, and the specification never says which type does the
carrying. It is the road, but that has to be inferred from the field's name and
from how the sample data uses it: Austin ships `bikeway:left:bikeway_type` on
4,003 road edges.

**Two Listed Values cells hold an editorial comment instead of values.**
`edge.incline` carries `[JG1]Grabbed from NACTO Bike design guide`; `point_type`
carries `[Same as Point Types]`.

**The introduction's section numbering collides.** 2.1.2 (Attribute Types) appears
after 2.2 (Geospatial Features) and before 2.3, so the document's only
third-level heading sorts into the wrong parent.

**The published sample datasets do not conform.** They are the worked examples a
publisher copies, and all four files fail. `newark_nodes` is unreadable in its
entirety: all 3,424 nodes are `node_type: "virtual"`, a draft-2 type v1.0 replaced
with `generic`. Newark also ships `edge_id` as an integer and `from_node` as a
float (`2000002.0`) against a type the JSON Schema resolves to `string`, sends a
bare string where `cross_vehicle_traffic_control` and `separation_elements` are
arrays, and carries null `street_name` on 474 roads and null `directionality` on
six, both required. Austin omits `directionality` on all 9,929 of its road edges.

## Modelling critiques

Not bugs: places where the schema will cost its users something, judged against
what Overture has already paid for.

**Identifiers are unspecified, and everything depends on them.** Every `*_id`
description ends `[NOTE: We will fill in instructions here on how to generate
IDs…]` — unchanged through two drafts and a ratification vote. Downstream that is
change detection between releases, conflation to OSM or a system of record,
per-feature provenance, and the `from_node`/`to_node` graph itself. Overture spent
years arriving at GERS for this. ID stability is a schema-level commitment a
validator cannot supply later, and shipping without it means every early adopter
has already chosen differently — which the sample datasets show happening.

**`reference_ids` is the only join to the rest of the world and it is
unspecified.** Its definition is *"an array of JSONs with the source name and ID
pair. Each JSON should contain an ID field and source field at minimum."* The
field names are not given and the source vocabulary is not given; the JSON Schema
types it `{"type": "object", "properties": {}}`, so any object validates. Across
the two sample datasets, 348,223 features carry an entry and not one uses a key
called `id`: Austin writes `sidewalks_id`, `CURB_RAMPS_ID` and
`asmp_street_network_id`, Newark writes `edge_id`. All four conform.

This is the sharpest demonstration that the prose and the schema have come apart.
Modelling the sentence — requiring `id` and `source` — rejects every one of those
348,223 features; modelling the schema accepts any object at all. There is no
third reading, and a consumer cannot join on this field without knowing in advance
which publisher wrote it. This package models the schema and reports the sentence.
Section 9.1's interoperability claim, to OSM, Overture, ARNOLD, HPMS and TIGER,
rests entirely here.

**Enumerated values are display text, not tokens.** Values carry spaces, capitals
and punctuation — `under construction`, `Gates and flashing lights`, `proposed -
not yet funded`, `uneven / displacement` — and several mash the token together with
its definition, so `separation_permeable_car`'s first value is the sentence `hard
separator: the separator cannot be easily bypassed by motor vehicles (jersey
barriers, curbs)`. Display text as a wire value cannot be renamed, localised or
matched without string normalisation, and every consumer invents its own. Overture
uses `lower_snake_case` throughout and carries the human-readable form as
documentation.

The seven mangled cells in the bug list are the first bill for this: every one is
a cell where a token and its definition share a field, and the separator between
them was load-bearing. This package keeps the literal strings, because changing
them would fork the spec.

**Nine field names mean different things in different files.** `status` has three
vocabularies — edges add "proposed and funded" and "proposed - not yet funded",
nodes add "planned", zones add "other" — and two different stated defaults: a blank
`status` is assumed `unknown` on an edge and `open` on a node or zone.
`impediment`, `surface_issue`, `other_issue`, `presence`, `allowed_uses`,
`prohibited_uses`, `surface_material` and `ada_compliant_with` all differ too.
Five change *declared type* as well: `surface_issue` is `Text` on edges and
`Array<Enum>` on nodes and points; `impediment` is `Array<Text>` on edges and
points and `Array<Enum>` on nodes; `surface_material` is `Enum` on edges and
`Text` on zones.

A consumer reading two GATIS files cannot treat a shared field name as a shared
field. This package emits `EdgeStatus`, `NodeStatus` and `ZoneStatus` rather than
one `Status`, because generating the short name let one file's vocabulary silently
overwrite another's — both spellings are valid and the enum still validates, so
nothing announces it.

**There is vehicle traffic control and pedestrian traffic control and no bicycle
traffic control.** `vehicle_traffic_control`, `cross_vehicle_traffic_control` and
`ped_traffic_control` are the three control fields in the schema. A bicycle signal
face is a distinct MUTCD device with its own indications, and a bikeway crossing
governed by one cannot be described: the publisher must call it a vehicle signal,
which is wrong, or a pedestrian signal, which is also wrong. Newark's Delaware
Avenue separated bike lane does the first, on seven crossings, with the
out-of-vocabulary value `"bicycle traffic signal"`. This is a gap in the field set
rather than a missing enum member, and a conspicuous one in a specification whose
subject is active transportation.

Two more values on that corridor sit outside their vocabularies for the same
reason — the device exists and the schema has no word for it.
`separation_permeable_car` is a binary, hard (cannot be bypassed by a motor
vehicle) against soft (can be), and a mountable curb is neither; the same
publisher used `hard separator` for a six-inch concrete curb and `"mountable"` for
a mountable one on the same street, so the distinction was drawn deliberately in
both directions. `bikeway_grade_separation` offers `at_grade`, `raised` and
`sidewalk_level`, and a bike lane raised above the roadway but below the sidewalk
— standard separated-bike-lane practice — is none of them. All three come from one
facility, so this is a design case rather than a distribution.

**`other` without a companion free-text field destroys the enum.** Twenty-eight
fields across the four classes offer an `other`-ish value and not one has a
companion field to say what it was. A consumer learns only that something unlisted
happened.

**Eight fields fuse a boolean with a taxonomy.** `impediment`, `surface_issue` and
`other_issue`, on each of the classes that carries them, are enumerations whose
first two members are `yes` and `no`, followed by specific conditions. `["yes"]` and `["potholes/holes"]` are both valid and
overlap in meaning, and `["yes", "no"]` is legal. Presence and classification are
separate facts and want separate fields.

**Null versus omitted is unstated, and publishers have already diverged.** Section
2.1.2 mentions it once, for booleans — "Boolean fields may be left blank. Most
software will interpret blank values as 'null'" — and nowhere generally. The two
sample datasets choose oppositely: Austin omits unset fields entirely, Newark
writes explicit nulls for 57% of every feature's slots. The shipped JSON Schema
permits null on 159 of 370 edge properties and says nothing about the rest. Both
conform; neither can be read by a consumer who assumed the other convention.

This is one sentence of specification, and the cost of not writing it compounds:
the null flood also hides real defects, since a required field arriving as null and
a required field arriving absent are different errors that look identical until
somebody decides which one null is.

**The type vocabulary is named and not defined anywhere machine-readable.**
Section 2.1.2 describes `Date`, `ID`, `Boolean`, `Enum` and `Array<Type>` in prose
with one example each; nothing else pins them. What that permits is visible in the
sample data: 8,815 of Austin's 9,979 curb-ramp nodes carry
`last_inspection_date: "1970-01-01"` — Unix epoch zero, an Esri export rendering
null as a date — and all 73,482 of its `date_built` values are full RFC 3339
datetimes against a field typed `Date`, every one at midnight `-06:00`, across 42
distinct values. The column is a year plus eleven characters of export padding.
Both pass any date check the spec implies. A `Date` that forbids a time component,
and an `ID` with a stated format, would catch both.

**The tier model is conformance, and it has been folded into the schema.** Tiers
are a maturity roadmap — a claim about a *dataset's* completeness — but they are
expressed by varying each field's presence, which makes presence four-dimensional
(feature class × feature type × field × tier) and yields 4,368 decisions for edges
alone, 6,408 across the spec. Overture keeps schema and conformance apart for this
reason: the schema says what a valid feature looks like, and a separate profile
says what a publisher has committed to. Folding them together means a Tier 1
publisher and a Tier 4 publisher validate against different schemas that share a
name — and, since the published JSON Schema declares nothing required, against no
tier in particular.

**`recommended` is not a validation state, and it now carries more weight.** It
sits between `optional` and `required`, and a validator can do nothing with it that
it cannot do with `optional`. v1.0 retired `conditionally_required` in its favour
("recommended over 'conditionally'", upstream, 2026-01-30), so 613 presence
decisions now rest on a descriptor that is documentation. Where the previous draft
could at least say *this field is required when that one is present*, v1.0 can only
suggest.

**Referential integrity is nobody's job, and the spec should say so.** `from_node`
and `to_node` reference `nodes.node_id` across files, and the files are validated
separately — nothing holds both an edge and its endpoints at validation time. A
dangling `from_node` is therefore a conforming dataset. This is not a criticism of
the split: Overture has the identical shape, with
`Segment.connectors[].connector_id` referencing a `Connector` that ships in its own
partition, and it declares the relationship in the schema while checking nothing.
The declaration is for downstream tooling; enforcement is a dataset-level step.
What GATIS is missing is the *declaration* — nothing machine-readable says
`from_node` points at `nodes.node_id`, only the prose "using the node_id attribute
on the nodes table." This package declares it with an Overture `Reference` and
implements the check in `gatis_schema.dataset`.

The cost is already visible. All 33 of Newark's bikeway, crossing and
traffic-island edges carry a null `from_node` and a null `to_node`, so that layer
is topologically disconnected from the network it belongs to. Both fields are
optional for those types, so the file conforms, and nothing in the specification or
its validator would report it.

## Artifacts of assuming GeoJSON

GeoJSON is the delivery format, and in several places its limits have been written
down as though they were decisions. Two of the entries below turn out not to be
limits at all: CurbLR ships curb regulations as GeoJSON and avoids both, which
makes those GATIS choices rather than constraints.

**The four files do the type system's work.** Nodes and points are both `Point`
geometry, distinguished only by which file they are in. v1.0 made nodes purely
about graph participation — `generic`, `curb_ramp`, and the two curb-ramp
transition types — and moved everything else to points. That is the right cut, and
it is carried by file placement rather than stated, because a GeoJSON file holds
one FeatureCollection and has no room for a second discriminator. Overture's theme
/ type / subtype / class nesting lets a transit stop be one kind of thing that is
or is not part of the routing graph.

**Banning MultiLineString is aimed at the wrong target.** Section 2.1 says edge
features *"must be LINE type (MULTILINE type is not supported)"*. The real
requirement is one traversable path per edge, so the topology is well-defined. The
prohibition does not deliver that — a self-intersecting LineString or two
coincident edges both pass — and it rules out legitimate multipart geometry for a
zone with a hole. State the topological requirement and let the geometry type
follow.

**Segmentation is a mandate because geometry is identity.** An edge can carry one
set of attributes along its length, so expressing variation means making more
features. Splitting explodes feature counts, destroys identifier stability across
releases — the same identifiers the spec has not yet defined — and turns every
attribute change into a topology change. A spec that already requires segmentation
at every intersection is asking publishers to re-split their network each time a
width measurement improves.

GeoJSON is not what forces this, and CurbLR is the proof: it is a GeoJSON spec, it
describes things that vary along a street, and it does not split. A CurbLR feature
is one located span carrying an *array* of regulations, and the spec says why
plainly — it "prevents the need to repeat geometry and location data multiple times
for the same street segment." Where two rules overlap in time and space, a
`priorityCategory` on each and an ordered `priorityHierarchy` in the manifest
decide which wins. No geometry is cut. Overture arrived at the same place from the
other direction, with scoped properties and `between: [start, end]` subranges.

Both alternatives keep one feature and move the variation into its properties —
and, as the CDS entry below sets out, both cost something in return. GATIS does not
appear to have chosen between them: the segmentation rule is stated as a
consequence of how edges work, with no alternative considered.

**Everything offset from a centerline is flattened onto it — but there is now a
door.** `buffer_width_ft`, `street_parking`, `street_parking_buffer_ft`,
`separation_elements`, `shoulder_width_in` and `curb_height_in` all describe
something beside the roadway, and all are scalars on the road edge. So a buffer has
a width and no extent: it cannot start, stop, or change partway along.

`lrs_references` is *"a JSON list capturing the attributes that appear in the GATIS
LRS extension … Either this attribute or the extension may be used."* That is a
linear-referencing hook, and it is optional, which is the right shape — guiding
principle 3 promises that "a text editor and common web-based tools that can
produce a GeoJSON" are enough at Tier 1, and a reference that only resolved through
a linear-referencing toolchain would break that promise for exactly the city GIS
staff the specification names as its audience. What is missing is the extension
itself: the field points at a document that is not in the repository, and the
field's own shape is undefined, so it is `reference_ids` again — a named join with
no schema.

Meanwhile nothing records *which* road a sidewalk runs beside. `street_name` is
free text, `reference_ids` points at external datasets rather than at another GATIS
edge, and `road_associated` was deleted.

Section 9.1's interoperability list named the Curb Data Specification and not
CurbLR, and CDS is worth reading for what it changed. Its Policy object "borrows
heavily from the work of the CurbLR project", and it keeps the array:
`curb_policy_ids` holds several policies per zone, so variation in time, user class
and rate still costs no extra geometry. What it inverts is which representation is
authoritative. `geometry` is Required and a polygon is preferred;
`location_references` is Optional. So a CDS publisher maintains an independent
polygon per curb zone, and the linear reference — where present — annotates it
rather than defining it.

The inversion costs CDS both properties. Its first rule for a curb zone is GATIS's
segmentation mandate in different words: a zone must "always have a common
regulation along their entire extent", so half loading and half metered means two
zones and two polygons. And identity rides on geometry — "a new `curb_zone_id` is
required if this geometry changes", which its own criteria then soften to "SHOULD
remain consistent as long as the Curb Zone's geography remains substantially the
same". There is also a `length` field, in centimetres, "projected along the street
centerline" and explicitly "not the edge length of the geographic polygon": a field
added to recover what a linear reference answers for free.

CDS documents no reason for the change, so what follows is inference. The likeliest
one is that geometry-as-identity works in the tools its users already have, and a
linear reference does not. A polygon opens in ArcGIS or QGIS, renders, edits and
exports; `shstRefId` plus two offsets resolves to a place on a map only against a
basemap, through software written for the purpose. CurbLR's own documentation
describes that software as a prerequisite rather than a convenience: collect points,
tag each as the beginning, middle or end of a regulation, run the SharedStreets CLI
to snap and segment them, then run conversion scripts to emit the feed. Its
strongest tell is that a CurbLR feature ships a GeoJSON geometry anyway, which the
reference makes redundant for identity and which exists so the data can be seen.

The dependency has since gone quiet. `sharedstreets-js` was last pushed in January
2023, the reference system in February 2023, and the builder in December 2020. A
spec whose identifiers resolve only through a dormant toolchain is a different
proposition from one whose features are polygons.

Two CDS ideas are still worth taking. `location_references` is an *array*, each
entry carrying a `source` URL naming its referencing system — SharedStreets, OpenLR,
or a city's own — so one feature can be located in several basemaps at once. That is
what `reference_ids` gestures at and does not specify, and what `lrs_references`
could become. And a Curb Object carries `linear_distance` and
`perpendicular_distance`, offsets in centimetres along and away from the curb, the
perpendicular one signed positive towards the sidewalk. GATIS has no way to place an
object beside an edge at all.

**Left/right is encoded in field names, and the prose never says so.** The
specification's narrative does not mention sides at all — the word "left" appears
in it once, in "Boolean fields may be left blank." The mechanism exists only as
`allowed_on_road` and `forbidden_field_if_allowed_on_road` in the type
definitions, and as 292 colon-namespaced properties in the JSON Schema. OSM
colon-namespacing is what a GeoJSON properties object forces, being a flat
string-to-value map with no nested scope, and it costs what it costs elsewhere:
field names become a grammar a validator must parse rather than a set it can
check. CurbLR makes `sideOfStreet` an ordinary enum and spends its prose on the
part that is actually subtle — left and right are relative to the direction of
digitization, so a two-way street carries two references. GATIS says nothing about
which direction defines left, because it says nothing about left.

**Per-feature provenance exists; per-feature versioning does not.** `owner`,
`maintainer`, `lifecycle_stage`, `last_inspection_date`, `last_inspection_type`,
`maintenance_schedule` and `planned_work` are all per-feature. What is missing is
change detection: there is no per-feature `version`, `update_time` or `sources[]`,
so comparing two releases is a geometry diff. Overture carries all three on every
feature, with per-property attribution, which is what lets a blended dataset —
LiDAR-derived widths over a 2019 field survey of surface condition — be read
correctly.

**Booleans are strings.** `yes`/`no`, in the OpenStreetMap format (section 2.1.2).
JSON has booleans and GeoJSON permits them; this is inherited vocabulary rather than
a constraint, but it survives because the properties bag makes the type invisible
until someone writes a parser. Every consumer now special-cases ten fields.

**Objects are described in prose because nesting is free.** `reference_ids`,
`sign_association`, `seasonal` and `lrs_references` are all typed `Array<Object>`
with their shape given in a sentence or not at all. Nothing in the container forces
a declaration, and a validator can check none of them.

## What would move the most

Ordered by what it unblocks, not by effort. Items 1, 2, 5 and 8 were written
against the previous draft and are unchanged here because the spec is: nothing in
v1.0 touched them.

1. **Specify identifiers.** Everything else compounds on it, and v1.0 shipped
   without it. The `[NOTE: We will fill in instructions here…]` has now survived a
   ratification vote.
2. **Specify `reference_ids`**, and `lrs_references` with it. Between them they are
   the entire interoperability story and currently two sentences.
3. **Fix the JSON Schema generator, and give it the required fields.** Seven fields
   carry the wrong vocabulary, and the schema is what a publisher validates
   against. A schema that requires nothing cannot express a tier.
4. **Define `forbidden` in the prose**, and publish the colon-namespaced on-road
   fields where a publisher will see them. Both exist in the data and in neither
   document.
5. **Give an edge an optional reference to another edge, with an extent.**
   `lrs_references` is the beginning of this; it needs the extension it names.
   Optional, it costs Tier 1 publishers nothing and lets the rest replace the
   `road_associated` that v1.0 deleted, give buffers and parking an extent, and
   stop splitting an edge every time a measurement improves. CDS is the model to
   copy rather than CurbLR: geometry stays authoritative, and `location_references`
   is an array whose entries each name their own referencing system.
6. **Settle null versus omitted**, in one sentence. Two of the spec's own sample
   datasets already disagree, and the ambiguity hides real defects behind a legal
   encoding.
7. **Tokenise enum values** before more datasets ship. The seven mangled
   `listed_values` cells are the first bill for storing tokens as display text.
8. **Separate the tier model from the field tables.** Presence becomes
   two-dimensional and the schema starts meaning one thing.
