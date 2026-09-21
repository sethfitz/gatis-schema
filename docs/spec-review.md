# Review of GATIS v1.0

Findings from modelling the spec in Pydantic, against the snapshot in
[`spec/`](../spec/) — `dotbts/BPA` at commit `ecc45ff8`, whose specification files
last changed 2026-02-03. GATIS v1.0 was voted through unanimously on 2026-02-27.

Three sections: defects, which are wrong as written and fixable in a pass;
modelling critiques, drawn from what Overture has learned building a schema over
the same subject matter; and GeoJSON artifacts, where a container's limits have
been written down as though they were design decisions.

Counts are measured against the snapshot, not estimated. Every defect below is
pinned by a test or a repair entry in this repo, so an upstream fix shows up here
as a failure rather than going unnoticed.

## What v1.0 fixed

This package reviewed draft 2 before the vote. Roughly half of that review's
defects are gone, and two of its structural critiques were answered:

- Every declared type now has fields. `elevator` was an allowed edge type with
  nothing defined for it, not even `edge_id`; `Points_Types` and `Points_Fields`
  disagreed about what a point was. Both files now declare and populate the same
  set.
- The duplicated `Points_Fields` rows, the column-shifted `impediment` row, the
  three field names carrying trailing whitespace, and the `mutli_use_path` /
  `raisedtraffic_island` misspellings are all gone.
- **Units are machine-readable**, which was recommendation 7. Fifteen fields carry
  the unit as a name suffix — `width_in`, `buffer_width_ft`,
  `posted_speed_limit_mph`, `crossing_time_sec` — where draft 2 stated all
  eighteen in prose only.
- **The document no longer contends with the field tables**, which was
  recommendation 4. Draft 2's specification document pasted stale copies of the
  workbook's pivots and named eleven fields the workbook did not define. v1.0
  publishes the tables as JSON and the prose as a short introduction that does not
  restate them. Nothing is now hand-copied between the two.
- `conditionally_required` is gone from the presence vocabulary, and with it the
  "Conditionally Forbidden" descriptor the document defined and never used.
- `transit_stop` and `issue` are no longer both a node type and a point type.
  Nodes are now four routing-participation types and everything else is a point,
  which is the distinction draft 2's internal notes were arguing about.
- Per-feature provenance exists where it did not: `owner`, `maintainer`,
  `lifecycle_stage`, `planned_work`, `last_inspection_date`, `last_inspection_type`
  and `maintenance_schedule`.
- `gtfs_id` no longer contradicts itself. It is two fields, `gtfs_stop_id` and
  `gtfs_agency_id`, both `Text`.

What did not move: identifiers, `reference_ids`, enum tokenisation, the tier model,
and the segmentation mandate. Those are recommendations 1, 2, 6 and 8, and they are
the ones everything else compounds on.

## Defects

**The presence vocabulary has four values and the specification defines three.**
Section 2.3 defines Optional, Recommended and Required. `forbidden` appears 2,860
times across the four files — 45% of all 6,408 presence decisions — and no
published prose says what it means. It is the descriptor that carries the most
information, because it is the one that makes a field *illegal* for a type rather
than merely absent, and it is the one a reader cannot look up.

**The two machine-readable artifacts disagree, and one of them is generated
wrong.** `json_schemas/*_schema.json` gives every `Array<Enum>` field the *last*
such field's vocabulary. In `edges_schema.json`, `allowed_uses`,
`prohibited_uses` and `cross_vehicle_traffic_control` all carry `ped_protection`'s
list, so `prohibited_uses` offers "leading pedestrian interval" and does not offer
"bike". In `nodes_schema.json`, `impediment` and `rail_crossing_control` carry
`surface_issue`'s list; in `points_schema.json`, `accessibility_features` does.
Seven fields, three files, one loop-variable bug. A publisher validating against
the shipped JSON Schema is validating against the wrong vocabulary and will be
told so by neither artifact.

**Upstream's JSON Schema declares no required fields at all.** Not `edge_id`, not
`edge_type`. Every property is optional in all four schemas, so the published
validator cannot check presence — which is what the tier model is made of, and
most of what the specification says.

**Six `listed_values` arrays do not survive publication.** v1.0 splits a
spreadsheet cell on newlines, and six edge cells were hard-wrapped, blank-lined or
run together. `separation_permeable_car` publishes as six entries including
`"curbs)"`, `"k-rail)"` and two empty strings; `separation_elements` ends in
`"trees  unknown"`; `allowed_uses` and `prohibited_uses` both end in
`"motor_vehicle ebike class 2 ebike class 3 other"`; `markings` carries an empty
value; `traffic_calming` interleaves the section headings `"for road edge type:"`
and `"for crossing edge type:"` with its values. Corrected in
[`spec/repairs.json`](../spec/repairs.json).

**Nine field names mean different things in different files.** `status` has three
vocabularies — edges add "proposed and funded" and "proposed - not yet funded",
nodes add "planned", zones add "other" — and two different stated defaults: a blank
`status` is assumed `unknown` on an edge and `open` on a node or zone. `impediment`,
`surface_issue`, `other_issue`, `presence`, `allowed_uses`, `prohibited_uses`,
`surface_material` and `ada_compliant_with` all differ too. Five of them change
*declared type* as well: `surface_issue` is `Text` on edges and `Array<Enum>` on
nodes and points; `impediment` is `Array<Text>` on edges and points and
`Array<Enum>` on nodes; `surface_material` is `Enum` on edges and `Text` on zones.
A consumer reading two GATIS files cannot treat a shared field name as a shared
field. This package emits `EdgeStatus`, `NodeStatus` and `ZoneStatus` rather than
one `Status`, because generating the short name let one file's vocabulary silently
overwrite another's.

**`edges.json` carries a presence column for a type it does not declare.**
`virtual_link` was removed from the edge types and left in the presence map of all
78 attributes. Generating from the presence columns — the obvious reading — puts
the type back into the data model.

**Three edge types forbid a field that no longer exists.** `sidewalk`, `bikeway`
and `multi_use_path` each list `road_associated` in
`forbidden_field_if_allowed_on_road`. v1.0 removed the attribute, so the rule
constrains nothing, and the one field that recorded an edge's relationship to a
road is gone with no replacement.

**Null-versus-omitted is unstated, and publishers have already diverged.** Section
2.1.2 mentions it once, for booleans — "Boolean fields may be left blank. Most
software will interpret blank values as 'null'" — and nowhere generally. The two
sample datasets GATIS itself publishes choose differently: Austin omits unset
fields entirely, Newark writes explicit nulls for 57% of every feature's slots.
Upstream's JSON Schema permits null on 159 of 370 edge properties and says nothing
about the rest. Both datasets conform; neither can be read by a consumer who
assumed the other convention.

**Section 3.0, Governance and Process for Changes, is four unfilled
placeholders.** "This specification is managed by [ORGANIZATION] through community
consultation. Please visit [LINK]." This is in the version that was voted through.

**Two Listed Values cells still hold an editorial comment instead of values.**
`edge.incline` carries `[JG1]Grabbed from NACTO Bike design guide`; `point_type`
carries `[Same as Point Types]`.

**The introduction's section numbering collides.** 2.1.2 (Attribute Types) appears
after 2.2 (Geospatial Features) and before 2.3, so the only third-level heading in
the document sorts into the wrong parent.

## Modelling critiques

Not defects: places where the schema will cost its users something, judged against
what Overture has already paid for.

**Identifiers are still unspecified, and everything depends on them.** Every
`*_id` description still ends `[NOTE: We will fill in instructions here on how to
generate IDs…]` — unchanged through two drafts and a ratification vote.
Downstream that is change detection between releases, conflation to OSM or a system
of record, per-feature provenance, and the `from_node`/`to_node` graph itself.
Overture spent years arriving at GERS for this. ID stability is a schema-level
commitment a validator cannot supply later, and v1.0 shipping without it means
every early adopter has already chosen differently. The sample datasets show it
happening: Newark ships `edge_id` as an integer and `from_node` as a float
(`2000002.0`) against a type the JSON Schema resolves to `string`.

**`reference_ids` is the only join to the rest of the world and it is
unspecified.** Its definition is still *"an array of JSONs with the source name and
ID pair. Each JSON should contain an ID field and source field at minimum."* The
field names are not given and the source vocabulary is not given; the JSON Schema
types it `{"type": "object", "properties": {}}`, so any object validates. The two
published sample datasets use four different encodings across 348,223 features and
none of them uses a key called `id`: `{"source": "austin", "sidewalks_id": "…"}`,
`{"source": "austin", "CURB_RAMPS_ID": …}`, `{"source": "austin",
"asmp_street_network_id": "…"}`, `{"source": "newark", "edge_id": …}`. All four
conform. This is the field the interoperability claim to OSM, Overture, ARNOLD,
HPMS and TIGER rests on.

**Enumerated values are display text, not tokens.** Values carry spaces, capitals
and punctuation — `under construction`, `Gates and flashing lights`, `proposed -
not yet funded`, `uneven / displacement` — and several mash the token together with
its definition, so `separation_permeable_car`'s first value is the sentence `hard
separator: the separator cannot be easily bypassed by motor vehicles (jersey
barriers, curbs)`. Display text as a wire value cannot be renamed, localised or
matched without string normalisation, and every consumer invents its own. Overture
uses `lower_snake_case` throughout and carries the human-readable form as
documentation. v1.0 shows the cost arriving: the six mangled `listed_values` cells
above are all cells where the definition and the token share a field, and the
newline that separated them was load-bearing. This package keeps the literal
strings, because changing them would fork the spec.

**`other` without a companion free-text field destroys the enum.** Twenty-eight
fields across the four classes offer an `other`-ish value and not one has a
companion field to say what it was. A consumer learns only that something unlisted
happened.

**Nine fields fuse a boolean with a taxonomy.** `impediment`, `surface_issue` and
`other_issue` are enumerations whose first two members are `yes` and `no`, followed
by specific conditions. `["yes"]` and `["potholes/holes"]` are both valid and
overlap in meaning, and `["yes", "no"]` is legal. Presence and classification are
separate facts and want separate fields.

**The tier model is conformance, and it has been folded into the schema.** Tiers
are a maturity roadmap — a claim about a *dataset's* completeness — but they are
expressed by varying each field's presence, which makes presence four-dimensional
(feature class × feature type × field × tier) and yields 4,368 decisions for edges
alone, 6,408 across the spec. Overture keeps schema and conformance apart for this
reason: the schema says what a valid feature looks like, and a separate profile
says what a publisher has committed to. Folding them together means a Tier 1
publisher and a Tier 4 publisher validate against different schemas that share a
name — and, since v1.0's published JSON Schema declares nothing required at all,
against no tier in particular.

**`recommended` is not a validation state, and it now carries more weight.** It
sits between `optional` and `required`, and a validator can do nothing with it that
it cannot do with `optional`. v1.0 retired `conditionally_required` in its favour
("recommended over 'conditionally'", upstream, 2026-01-30), so 613 presence
decisions now rest on a descriptor that is documentation. Where draft 2 could at
least say *this field is required when that one is present*, v1.0 can only suggest.

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

**The type vocabulary is named and not defined anywhere machine-readable.**
Section 2.1.2 describes `Date`, `ID`, `Boolean`, `Enum`, `Array<Type>` in prose and
gives an example each; nothing else pins them. What that permits is visible in the
sample data: 8,815 of Austin's 9,979 curb-ramp nodes carry
`last_inspection_date: "1970-01-01"` — Unix epoch zero, an Esri export rendering
null as a date — and all 73,482 of its `date_built` values are full RFC 3339
datetimes against a field typed `Date`, every one at midnight `-06:00`, across 42
distinct values. Both pass any date check the spec implies. A `Date` that forbids a
time component, and an `ID` with a stated format, would catch both.

## Artifacts of assuming GeoJSON

GeoJSON is the delivery format, and in several places its limits have been written
down as though they were decisions. Two of the entries below turn out not to be
limits at all: CurbLR ships curb regulations as GeoJSON and avoids both, which
makes those GATIS choices rather than constraints.

**The four files do the type system's work.** Nodes and points are both `Point`
geometry, distinguished only by which file they are in. v1.0 settled draft 2's
argument — `transit_stop` and `issue` were both, with near-identical descriptions
and internal notes reading *"This is a point, not a node"* against *"a lot of folks
in the accessibility working group wanted them to be nodes, for routing
convenience"* — by making nodes purely about graph participation: `generic`,
`curb_ramp`, and the two curb-ramp transition types. That is the right cut, and it
is being carried by file placement rather than stated, because a GeoJSON file holds
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

**Everything offset from a centerline is flattened onto it — but v1.0 opened a
door.** `buffer_width_ft`, `street_parking`, `street_parking_buffer_ft`,
`separation_elements`, `shoulder_width_in` and `curb_height_in` all describe
something beside the roadway, and all are scalars on the road edge. So a buffer has
a width and no extent: it cannot start, stop, or change partway along.

v1.0 adds `lrs_references`, *"a JSON list capturing the attributes that appear in
the GATIS LRS extension … Either this attribute or the extension may be used."*
That is the linear-referencing hook draft 2 had no equivalent of, and it is
optional, which is the right shape — guiding principle 3 promises that "a text
editor and common web-based tools that can produce a GeoJSON" are enough at Tier 1,
and a reference that only resolved through a linear-referencing toolchain would
break that promise for exactly the city GIS staff the specification names as its
audience. What is missing is the extension itself: the field points at a document
that is not in the repository, and the field's own shape is undefined, so it is
`reference_ids` again — a named join with no schema.

Meanwhile the field that recorded an edge's relationship to a road at all,
`road_associated`, was removed. `street_name` is free text and `reference_ids`
points at external datasets rather than at another GATIS edge, so nothing now
records *which* road a sidewalk runs beside.

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

**Left/right is encoded in field names, and the names exist in only one published
artifact.** Draft 2 endorsed roadway-centerline representation and defined none of
the fields it needs, which this review called its costliest omission for Tier 1
publishers. v1.0 has defined them — `edges_schema.json` enumerates 292
colon-namespaced properties, `sidewalk:left:width_in` through
`multi_use_path:right:width_tolerance_in`, and they are internally consistent:
exactly `{sidewalk, bikeway, multi_use_path} × {left, right} ×` that type's own
non-forbidden fields, minus the six each type lists in
`forbidden_field_if_allowed_on_road`.

They appear nowhere else. `specification_jsons` has zero colon-namespaced
attributes; so does the attribute table on the GATIS Explorer, which is what a
publisher actually reads. The mechanism is referenced from
`forbidden_field_if_allowed_on_road` without the field names being given. So the
representation is now specified for a validator and undocumented for a human, which
is a narrower gap than draft 2's and a stranger one.

The encoding itself still costs what it cost. Field names become a grammar a
validator must parse rather than a set it can check, where CurbLR makes
`sideOfStreet` an ordinary enum and spends its prose on the part that is actually
subtle: left and right are relative to the direction of digitization, so a two-way
street carries two references. GATIS says nothing about which direction defines
left.

**Per-feature provenance arrived; per-feature versioning did not.** v1.0 added
`owner`, `maintainer`, `lifecycle_stage`, `last_inspection_date`,
`last_inspection_type`, `maintenance_schedule` and `planned_work`, which is most of
what draft 2 could only say once per dataset in `metadata.json`. What is still
missing is change detection: there is no per-feature `version`, `update_time` or
`sources[]`, so comparing two releases is a geometry diff. Overture carries all
three on every feature, with per-property attribution, which is what lets a blended
dataset — LiDAR-derived widths over a 2019 field survey of surface condition — be
read correctly.

**Booleans are strings.** `yes`/`no`, in the OpenStreetMap format (section 2.1.2).
JSON has booleans and GeoJSON permits them; this is inherited vocabulary rather than
a constraint, but it survives because the properties bag makes the type invisible
until someone writes a parser. Every consumer now special-cases ten fields.

**Objects are described in prose because nesting is free.** `reference_ids`,
`sign_association`, `seasonal` and `lrs_references` are all typed `Array<Object>`
with their shape given in a sentence or not at all. Nothing in the container forces
a declaration, and a validator can check none of them.

## What would move the most

Ordered by what it unblocks, not by effort. Items 1, 2 and 5 carried over from the
draft 2 review unchanged, which is itself the finding.

1. **Specify identifiers.** Everything else compounds on it, and v1.0 shipped
   without it. The `[NOTE: We will fill in instructions here…]` has now survived a
   ratification vote.
2. **Specify `reference_ids`**, and `lrs_references` with it. Between them they are
   the entire interoperability story and currently two sentences.
3. **Fix the JSON Schema generator.** Seven fields carry the wrong vocabulary, and
   the schema is what a publisher validates against. Then give it the required
   fields — a schema that requires nothing cannot express a tier.
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
6. **Tokenise enum values** before more datasets ship. The six mangled
   `listed_values` cells are the first bill for storing tokens as display text.
7. **Settle null versus omitted**, in one sentence. Two of the spec's own sample
   datasets already disagree.
8. **Separate the tier model from the field tables.** Presence becomes
   two-dimensional and the schema starts meaning one thing.
