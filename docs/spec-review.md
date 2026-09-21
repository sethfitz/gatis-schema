# Review of the GATIS v2 draft

Findings from modelling the spec in Pydantic, against the snapshot in
[`spec/`](../spec/) — workbook Drive revision 3542 (modified 2026-01-30),
document revision 5909 (2025-11-12).

Three sections: defects, which are wrong as written and fixable in a pass;
modelling critiques, drawn from what Overture has learned building a schema
over the same subject matter; and GeoJSON artifacts, where a container's limits
have been written down as though they were design decisions. The third is the
one least likely to be noticed from inside the format.

Counts are measured against the snapshot, not estimated. Every defect below is
pinned by a test or a repair entry in this repo, so an upstream fix shows up
here as a failure rather than going unnoticed.

## Defects

**The document and the workbook have diverged, and the document is stale.**
Section 3.0 is a stub: every field and type table reads *"Moved here"* and
links to a workbook tab. The workbook's own README states the direction of
travel — *"the 'final' tabs are imported into the Google Doc"* — but that
import is manual and the document is two and a half months behind. The presence
tables still in the document name eleven fields the workbook does not define:
`road_speed` (thirteen occurrences), `width_min`, `surface_quality`,
`car_freeflow_speed`, `ada_compliance`, `rail`, `issue`,
`bike_runnelwheel_channel`, a `detectable_warning` that exists only on nodes,
and the misspellings below. Twenty workbook fields are never mentioned in the
document, four of which change the data model: `presence`, `directionality`,
`reference_ids`, `restricted_access`. Anyone implementing from the published
document builds the wrong schema.

**Fourteen of 109 fields (13%) apply to no feature type.** They are defined —
name, type, description, allowed values — with every presence cell blank, so no
feature may carry them. They are unreachable rather than optional: `tunnel`,
`height_max_passable`, `above_below_grade`, `building_level`, `markings`,
`restricted_access` and `other_issue` on edges; `other_issue` on nodes;
`impediment`, `surface_issue` and `other_issue` on points; `prohibited_uses` and
`allowed_uses` on zones. Several are load-bearing — `tunnel` and
`height_max_passable` are the only clearance and grade-separation signals in the
schema, and `restricted_access` is the only way to say a path is private.

**`elevator` is an allowed edge type with no fields at all.** It appears in
`Edges_Types` but has no presence column in `Edges_Fields`, so the workbook
defines nothing for it — not even `edge_id`. It is also still listed as a node
type, where the internal note says *"Remove as node, move to edge"*; the move
happened in one tab and not the other.

**`Points_Types` and `Points_Fields` disagree about what a point is.**
`Points_Types` declares `object`, `sign`, `transit_stop` and `issue`.
`Points_Fields` has presence columns for `object` and `point` — so three of the
four declared types have no fields, and `point` is not a declared type. The
`sign_*` fields hang off the undeclared column.

**One `Points_Fields` row is column-shifted.** The `impediment` row has its own
name and description pasted into the two presence columns, so it carries no
presence value at all. Recorded in [`spec/repairs.json`](../spec/repairs.json)
rather than guessed.

**`Points_Fields` lists `impediment` and `surface_issue` twice**, with value
sets that disagree with each other and with the node equivalents. Nothing says
which wins.

**The same field name means different things on different feature classes.**
`rail_crossing` is a `Boolean` (`yes`/`no`) on edges and an `Array<Enum>` of
warning devices (`Gates and flashing lights`, `flashing lights only`,
`crossbucks or stop sign only`, …) on nodes. `width` is `Integer` on edges and
`Float` on nodes, with both descriptions saying inches rounded to the nearest
inch.

**Three field names carry trailing whitespace**: `ped_traffic_control `,
`vehicle_traffic_control `, `cross_vehicle_traffic_control `. A generator that
does not strip emits fields nothing can populate.

**Two Listed Values cells contain an editorial comment instead of values**:
`edge.incline` and `node.traffic_calming_type` both hold `[JG1]Grabbed from
NACTO Bike design guide`. `edge.pedestrian_lane` is typed `Enum` with an empty
Listed Values cell and is optional on all twelve edge types, so it has no
allowed values at all. `edge.surface_issue`'s Description column is a verbatim
copy of its Listed Values.

**`zone.prohibited_uses` and `zone.allowed_uses` have no Type cell.**

**The Valid column has six spellings for four states**: `Valid`, `Valild`, `NA`,
`N/A`, `Recommended`, and blank.

**Four fields state a default in prose and declare none.** `status` defaults to
`"open"` on nodes, edges and zones; `directionality` "assumes both" if left
blank. Two implementations will disagree about an absent value, and both will
believe they conform.

**`presence` states its own conditional in prose**: *"Conditionally required if
no other identifying fields supplied."* The presence column says `optional`. The
spec has a `conditionally_required` descriptor and does not use it here.

**The document defines a presence descriptor the workbook never uses**:
"Conditionally Forbidden" (section 3.3). Nothing in the workbook is
conditionally forbidden.

**The derived tabs and the document still carry two misspellings the source tabs
have fixed**: `mutli_use_path` for `multi_use_path`, `raisedtraffic_island` for
`traffic_island`.

**The document's section numbering collides.** There are two 3.1s (Files,
Metadata), two 3.2s (Definitions, Nodes), two 3.4s (Attribute Types — and then
Points *and* Zones both numbered 3.4), and three 2.2.1s (Relation Tables,
Routing, Directionality). Section 3.1 also introduces `points.geojson` as a
fourth file after 2.2.0 has stated there are three core entity types.

## Modelling critiques

Not defects: places where the schema will cost its users something, judged
against what Overture has already paid for.

**Identifiers are unspecified, and everything depends on them.** Every `*_id`
description ends `[NOTE: We will fill in instructions here on how to generate
IDs…]`. Downstream that is change detection between releases, conflation to OSM
or a system of record, per-feature provenance, and the `from_node`/`to_node`
graph itself. Overture spent years arriving at GERS for this. ID stability is a
schema-level commitment; a validator cannot supply it later. Deciding it late
means every early adopter has already chosen differently.

**`reference_ids` is the only join to the rest of the world and it is
unspecified.** Its entire definition is *"an array of JSONs with the source
name and ID pair. Each JSON should contain an ID field and source field at
minimum."* The field names are not given, the source vocabulary is not given,
and the milepost extension is described but not typed. Section 9.1's
interoperability claim — to OSM, Overture, ARNOLD, HPMS and TIGER — rests
entirely on this field. Two publishers will produce incompatible arrays and
both will validate.

**Enumerated values are display text, not tokens.** Twenty-one enums have
values with spaces or capitals: `under construction`, `Buffered Bike Lane`,
`Gates and flashing lights`, `detectable warning not aligned with crossing`.
Some cells mash the token and its definition together —
`separation_permeable_car` lists `hard separator: the separator cannot be
easily bypassed by motor vehicles (jersey barriers, curbs)`. Display text as a
wire value means the value cannot be renamed, localised or matched without
string normalisation, and every consumer invents its own. Overture uses
`lower_snake_case` throughout and carries the human-readable form as
documentation. This package keeps the literal strings, because changing them
would fork the spec. The fix is cheap now and expensive once the first dataset
ships.

**`other` without a companion free-text field destroys the enum.** Nearly every
enum ends in `other`, and there is nowhere to say what it was. A consumer
learns only that something unlisted happened.

**Three fields fuse a boolean with a taxonomy.** `impediment`, `surface_issue`
and `other_issue` are `Array<Enum>` whose first two members are `yes` and `no`,
followed by specific conditions (`potholes/holes`, `heaving`, `markings worn`).
`["yes"]` and `["potholes/holes"]` are both valid and overlap in meaning, and
`["yes", "no"]` is legal. Presence and classification are separate facts and
want separate fields.

**Units are fixed by the schema and stated only in prose.** Eighteen fields
carry a dimension and none of it is machine-readable: inches for `width`,
`width_min_passable`, `width_tolerance`, `height_max_passable` and
`curb_height`; feet for `buffer_width`, `shoulder_width`,
`street_parking_buffer` and `measured_length`; percent for the slopes; mph for
the speeds; AADT for `traffic_volume`. Because the units are mixed, a consumer
converting GATIS to any other schema must parse English to know whether 60 is
inches or feet. The `node.width` / `edge.width` type disagreement above is what
prose-only units produce. Overture is working the same gap from the other side
(schema issue bd-uzbn) and has the easier case, since its fixed units are
uniformly metres. CurbLR shows the cheap version: `unitHeightLength` and
`unitWeight` sit in the feed manifest, each required only when a rule using it
is present. Feed-level is coarser than per-field, and it is machine-readable,
which English is not.

**The tier model is conformance, and it has been folded into the schema.**
Tiers are a maturity roadmap — a claim about a *dataset's* completeness — but
they are expressed by varying each field's presence, which makes presence
four-dimensional (feature class × feature type × field × tier) and yields 3,120
decisions for edges alone. Overture keeps schema and conformance apart for this
reason: the schema says what a valid feature looks like, and a separate profile
says what a publisher has committed to. Folding them together means a Tier 1
publisher and a Tier 4 publisher validate against different schemas that share
a name.

**`recommended` is not a validation state.** It sits in the presence vocabulary
between `optional` and `required`, and a validator can do nothing with it that
it cannot do with `optional`. It is documentation, and it roughly doubles the
size of the presence matrix.

**Referential integrity is nobody's job, and the spec should say so.**
`from_node` and `to_node` reference `nodes.node_id` across files, and the files
are validated separately — nothing holds both an edge and its endpoints at
validation time. A dangling `from_node` is therefore a conforming dataset. This
is not a criticism of the split: Overture has the identical shape, with
`Segment.connectors[].connector_id` referencing a `Connector` that ships in its
own partition, and it declares the relationship in the schema while checking
nothing. The declaration is for downstream tooling; enforcement is a
dataset-level step. What GATIS is missing is the *declaration* — there is no
machine-readable statement that `from_node` points at `nodes.node_id` at all,
only the sentence "Value needs to be from the nodes table in the node ID field."
This package declares it with an Overture `Reference` and implements the
integrity check at the dataset level.

**Relation tables are named and not defined.** *"At this time, the
specification does not explicitly define how to create or utilize relation
tables. We expect to address this more fully in the second draft."* They are
the stated mechanism for intersections, turn restrictions and two-stage left
turns, which is where routing is hardest. Overture's segment/connector model
with turn-restriction rules is a worked precedent for the same problem and is
worth reading before the second draft settles the shape.

## Artifacts of assuming GeoJSON

GeoJSON is the delivery format, and in several places its limits have been
written down as though they were decisions. Two of the entries below turn out
not to be limits at all: CurbLR ships curb regulations as GeoJSON and avoids
both, which makes those GATIS choices rather than constraints.

**Open extensibility is what the container already does.** Section 6.1 grants
that *"anyone can add any attribute they want to a dataset"* and that the
validator *"will warn, but not fail on, new or unknown fields."* GeoJSON's
`properties` is an untyped bag, so the spec has described its container rather
than decided anything here. The cost is real: a field
that is `forbidden` for a feature type and a field nobody has heard of arrive
identically, and the validator cannot distinguish a spec violation from a
sanctioned local extension without the presence matrix in hand. A schema'd
container makes extension explicit — a declared namespace, a typed extension
column — so a warning says which kind it is. This repo models it the same way
for compatibility, keeping the forbidden set as data purely to produce the
right diagnostic.

**The four files do the type system's work, and one axis is missing.** Nodes
and points are both `Point` geometry, distinguished only by which file they are
in. `transit_stop` and `issue` appear as *both* a node type and a point type
with near-identical descriptions, and the internal notes are an unresolved
argument about which they should be — *"This is a point, not a node"* / *"a lot
of folks in the accessibility working group wanted them to be nodes, for
routing convenience."* The disagreement is about graph participation, and file
placement is settling it, because a GeoJSON file holds one FeatureCollection
and has no room for a second discriminator. Overture's theme / type / subtype /
class nesting lets a transit stop be one kind of thing that is or is not part
of the routing graph.

**Banning MultiLineString and MultiPolygon is aimed at the wrong target.**
Section 3.1 says features *"must be LINE type (MULTILINE type is not
supported)"*. The real requirement is one traversable path per edge, so the
topology is well-defined. The prohibition does not deliver that — a
self-intersecting LineString or two coincident edges both pass — and it rules
out legitimate multipart geometry for a zone with a hole. State the topological
requirement and let the geometry type follow.

**Segmentation is a mandate because geometry is identity.** Section 2.2.2
requires splitting an edge whenever any attribute changes, because *"edges can
only support one set of attributes along their entire length."* Splitting
explodes feature counts, destroys identifier stability across releases — the
same identifiers the spec has not yet defined — and turns every attribute
change into a topology change. A spec that already requires segmentation at
every intersection is asking publishers to re-split their network each time a
width measurement improves.

GeoJSON is not what forces this, and CurbLR is the proof: it is a GeoJSON spec,
it describes things that vary along a street, and it does not split. A CurbLR
feature is one located span carrying an *array* of regulations, and the spec
says why plainly — it "prevents the need to repeat geometry and location data
multiple times for the same street segment." Where two rules overlap in time
and space, a `priorityCategory` on each and an ordered `priorityHierarchy` in
the manifest decide which wins. No geometry is cut. Overture arrived at the
same place from the other direction, with scoped properties and `between:
[start, end]` subranges.

What GATIS has done is make geometry the identity of the attribute set. Once a
feature can carry only one set of values, the only way to express variation is
to make more features. Both alternatives keep one feature and move the
variation into its properties.

**Everything offset from a centerline is flattened onto it.** `buffer_width`,
`street_parking`, `street_parking_buffer`, `separation_elements`,
`shoulder_width` and `curb_height` all describe something beside the roadway,
and all are scalars on the road edge, because section 2.3 offers two places to
put a thing and neither fits: a separate geometry, which duplicates the
centerline and, by the spec's own admission, loses the relation to it; or an
attribute on the road, which discards the offset. So a buffer has a width and
no extent. It cannot start, stop, or change partway along.

CurbLR takes a third option. A CurbLR feature has its own record and its own
attributes but no independent geometry to maintain: it is located by
`shstRefId` plus `shstLocationStart` and `shstLocationEnd`, offsets in metres
along a referenced street, plus `sideOfStreet`. `derivedFrom` holds the ids of
the physical assets the span came from, so the signs and meters stay in the
source data and the feature points back at them rather than replacing them. The
distinction the spec leads with is the useful one: a parking sign is a physical
geometry, the rule it conveys is a *regulatory* geometry, and the two are not
the same shape.

GATIS has no equivalent, and the field that would be the hook is a boolean.
`road_associated` records *that* an edge runs alongside a road; nothing records
*which* road. `street_name` is free text, and `reference_ids` points at
external datasets rather than at another GATIS edge. Section 2.3.1 names the
loss — *"the relation to the parallel road segment is lost, unless the parallel
road segment ID is included as an attribute"* — and the schema does not define
that attribute.

Section 9.1 lists the Curb Data Specification and not CurbLR, and CDS is worth
reading for what it changed. Its Policy object "borrows heavily from the work
of the CurbLR project", and it keeps the array: `curb_policy_ids` holds several
policies per zone, so variation in time, user class and rate still costs no
extra geometry. What it inverts is which representation is authoritative.
`geometry` is Required and a polygon is preferred; `location_references` is
Optional. So a CDS publisher maintains an independent polygon per curb zone,
and the linear reference — where present — annotates it rather than defining
it.

The inversion costs CDS the two things worth having here. Its first rule for a
curb zone is GATIS's segmentation mandate in different words: a zone must
"always have a common regulation along their entire extent", so half loading
and half metered means two zones and two polygons. And identity rides on
geometry — "a new `curb_zone_id` is required if this geometry changes", which
its own criteria then soften to "SHOULD remain consistent as long as the Curb
Zone's geography remains substantially the same". There is also a `length`
field, in centimetres, "projected along the street centerline" and explicitly
"not the edge length of the geographic polygon": a field added to recover what
a linear reference answers for free.

Two CDS ideas are still worth taking. `location_references` is an *array*, each
entry carrying a `source` URL naming its referencing system — SharedStreets,
OpenLR, or a city's own — so one feature can be located in several basemaps at
once. That is what GATIS's `reference_ids` gestures at and does not specify.
And a Curb Object carries `linear_distance` and `perpendicular_distance`,
offsets in centimetres along and away from the curb, the perpendicular one
signed positive towards the sidewalk. GATIS has no way to place an object
beside an edge at all.

**Left/right/both is encoded in field names.** Section 2.2.1 shows
`sidewalk:left:presence=yes` — OSM colon-namespacing, adopted because a GeoJSON
properties object is a flat string-to-value map with no nested scope. Two
consequences. Field names become a grammar a validator must parse rather than a
set it can check, where CurbLR makes `sideOfStreet` an ordinary enum and spends
its prose on the part that is actually subtle: left and right are relative to
the direction of digitization, so a two-way street carries two references. And
none of these colon-namespaced fields appear anywhere in section 3.0 or the
workbook, which means **roadway-centerline representation — blessed in section
2.3, and what every Tier 1 publisher will use — is unspecified**. This package
can only model parallel-feature representation, because the source specifies
nothing else.

**Provenance is dataset-wide because a feature has nowhere to put it.** GeoJSON
gives a feature no metadata slot, so everything provenance-related lives in
`metadata.json`: one `collection_method`, one `source_dataset`, one
`collection_period`. A real dataset blends LiDAR-derived widths with a 2019
field survey of surface condition, and GATIS has no way to say so. `check_date`
and `date_built` are the only per-feature temporal facts, and there is no
per-feature `version` or `update_time` at all, so change detection between two
releases is a geometry diff. Overture carries `version`, `update_time` and a
`sources[]` array with per-property attribution on every feature, which is what
lets a blended dataset be read correctly.

**Booleans are strings.** `yes`/`no`, in the OpenStreetMap format (section 3.4).
JSON has booleans and GeoJSON permits them; this is inherited vocabulary rather
than a constraint, but it survives because the properties bag makes the type
invisible until someone writes a parser. Every consumer now special-cases nine
fields.

**Objects are described in prose because nesting is free.** `reference_ids`,
`gtfs_id` and `seasonal` are all typed `Array<Object>` with their shape given in
a sentence. `gtfs_id` contradicts itself — typed `Array<Object>`, described as
*"Represent as string with the format `{agency_id},{stop_id}`"*. Nothing in the
container forces a declaration, and a validator can check none of the three.

## What would move the most

Ordered by what it unblocks, not by effort.

1. **Specify identifiers.** Everything else compounds on it.
2. **Specify `reference_ids`.** It is the entire interoperability story and
   currently one sentence.
3. **Specify roadway-centerline representation**, or withdraw the endorsement in
   section 2.3. Tier 1 publishers have nothing to implement.
4. **Regenerate the document from the workbook, and stop hand-pasting.** The
   published artifact currently describes a schema that does not exist.
5. **Give an edge a way to reference another edge, with an extent.** A
   reference plus start and end offsets plus a side would retire
   `road_associated`, carry the buffers and parking that are currently scalars
   with no extent, and remove most of the reason to split an edge at all.
   CurbLR is the worked example, in GeoJSON; take CDS's array of references,
   each naming its own system, rather than CurbLR's single one.
6. **Tokenise enum values** before the first dataset ships.
7. **Give the eighteen dimensioned fields a structural unit.**
8. **Separate the tier model from the field tables.** Presence becomes
   two-dimensional and the schema starts meaning one thing.
