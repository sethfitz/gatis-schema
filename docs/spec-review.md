# Review of the GATIS v2 draft

Findings from modelling the spec in Pydantic, against the snapshot in
[`spec/`](../spec/) — workbook Drive revision 3542 (modified 2026-01-30),
document revision 5909 (2025-11-12).

Three sections: defects, which are wrong as written and fixable in a pass;
modelling critiques, drawn from what Overture has learned building a schema over
the same subject matter; and GeoJSON artifacts, where a container's limits have
been written down as though they were design decisions. The third is the most
consequential, because those are the ones that will not read as problems to
anyone working inside the format.

Counts are measured against the snapshot, not estimated. Every defect below is
pinned by a test or a repair entry in this repo, so an upstream fix shows up here
as a failure rather than going unnoticed.

## Defects

**The document and the workbook have diverged, and the document is stale.**
Section 3.0 is a stub: every field and type table reads *"Moved here"* and links
to a workbook tab. The workbook's own README states the direction of travel —
*"the 'final' tabs are imported into the Google Doc"* — but that import is manual
and the document is two and a half months behind. The presence tables still in
the document name eleven fields the workbook does not define: `road_speed`
(thirteen occurrences), `width_min`, `surface_quality`, `car_freeflow_speed`,
`ada_compliance`, `rail`, `issue`, `bike_runnelwheel_channel`, a
`detectable_warning` that exists only on nodes, and the misspellings below.
Twenty workbook fields are never mentioned in the document, four of which change
the data model: `presence`, `directionality`, `reference_ids`,
`restricted_access`. Anyone implementing from the published document builds the
wrong schema.

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

**`Points_Fields` lists `impediment` and `surface_issue` twice**, with value sets
that disagree with each other and with the node equivalents. Nothing says which
wins.

**The same field name means different things on different feature classes.**
`rail_crossing` is a `Boolean` (`yes`/`no`) on edges and an `Array<Enum>` of
warning devices (`Gates and flashing lights`, `flashing lights only`, `crossbucks
or stop sign only`, …) on nodes. `width` is `Integer` on edges and `Float` on
nodes, with both descriptions saying inches rounded to the nearest inch.

**Three field names carry trailing whitespace**: `ped_traffic_control `,
`vehicle_traffic_control `, `cross_vehicle_traffic_control `. A generator that
does not strip emits fields nothing can populate.

**Two Listed Values cells contain an editorial comment instead of values**:
`edge.incline` and `node.traffic_calming_type` both hold `[JG1]Grabbed from NACTO
Bike design guide`. `edge.pedestrian_lane` is typed `Enum` with an empty Listed
Values cell and is optional on all twelve edge types, so it has no allowed values
at all. `edge.surface_issue`'s Description column is a verbatim copy of its
Listed Values.

**`zone.prohibited_uses` and `zone.allowed_uses` have no Type cell.**

**The Valid column has six spellings for four states**: `Valid`, `Valild`, `NA`,
`N/A`, `Recommended`, and blank.

**Four fields state a default in prose and declare none.** `status` defaults to
`"open"` on nodes, edges and zones; `directionality` "assumes both" if left
blank. A default in a description is not a default: two implementations will
disagree about an absent value, and both will believe they conform.

**`presence` states its own conditional in prose**: *"Conditionally required if
no other identifying fields supplied."* The presence column says `optional`. The
spec has a `conditionally_required` descriptor and does not use it here.

**The document defines a presence descriptor the workbook never uses**:
"Conditionally Forbidden" (section 3.3). Nothing in the workbook is conditionally
forbidden.

**The derived tabs and the document still carry two misspellings the source tabs
have fixed**: `mutli_use_path` for `multi_use_path`, `raisedtraffic_island` for
`traffic_island`.

**The document's section numbering collides.** There are two 3.1s (Files,
Metadata), two 3.2s (Definitions, Nodes), two 3.4s (Attribute Types — and then
Points *and* Zones both numbered 3.4), and three 2.2.1s (Relation Tables,
Routing, Directionality). Section 3.1 also introduces `points.geojson` as a
fourth file after 2.2.0 has stated there are three core entity types.

## Modelling critiques

These are not defects. They are places where the schema will cost its users
something, judged against what Overture has already paid for.

**Identifiers are the unfinished foundation.** Every `*_id` description ends
`[NOTE: We will fill in instructions here on how to generate IDs…]`. Stable
identifiers are the hardest problem in this space and everything downstream
depends on them: change detection between releases, conflation to OSM or a system
of record, per-feature provenance, and the `from_node`/`to_node` graph itself.
Overture spent years arriving at GERS for exactly this, and the lesson worth
transferring is that ID stability is a schema-level commitment, not an
implementation detail a validator can supply later. Deciding it late means every
early adopter has already chosen differently.

**`reference_ids` is the only join to the rest of the world and it is
unspecified.** Its entire definition is *"an array of JSONs with the source name
and ID pair. Each JSON should contain an ID field and source field at minimum."*
The field names are not given, the source vocabulary is not given, and the
milepost extension is described but not typed. This is the field that makes GATIS
interoperable with OSM, Overture, ARNOLD, HPMS and TIGER — section 9.1's entire
interoperability claim rests on it — and it is the least specified thing in the
schema. Two publishers will produce incompatible arrays and both will validate.

**Enumerated values are display text, not tokens.** Twenty-one enums have values
with spaces or capitals: `under construction`, `Buffered Bike Lane`, `Gates and
flashing lights`, `detectable warning not aligned with crossing`. Some cells mash
the token and its definition together — `separation_permeable_car` lists `hard
separator: the separator cannot be easily bypassed by motor vehicles (jersey
barriers, curbs)`. Display text as a wire value means the value cannot be
renamed, localised or matched without string normalisation, and every consumer
invents its own. Overture uses `lower_snake_case` throughout and carries the
human-readable form as documentation. This package keeps the literal strings,
because changing them would fork the spec — but it is the cheapest fix available
and the window closes when the first dataset ships.

**`other` without a companion free-text field destroys the enum.** Nearly every
enum ends in `other`, and there is nowhere to say what the other was. The value
that most needs explaining is the one that carries none, and a data consumer
learns only that something unlisted happened.

**Three fields fuse a boolean with a taxonomy.** `impediment`, `surface_issue`
and `other_issue` are `Array<Enum>` whose first two members are `yes` and `no`,
followed by specific conditions (`potholes/holes`, `heaving`, `markings worn`).
`["yes"]` and `["potholes/holes"]` are both valid and overlap in meaning, and
`["yes", "no"]` is legal. Presence and classification are separate facts and want
separate fields.

**Units are fixed by the schema and stated only in prose.** Eighteen fields carry
a dimension and none of it is machine-readable: inches for `width`,
`width_min_passable`, `width_tolerance`, `height_max_passable` and `curb_height`;
feet for `buffer_width`, `shoulder_width`, `street_parking_buffer` and
`measured_length`; percent for the slopes; mph for the speeds; AADT for
`traffic_volume`. The mixture is the problem — a consumer converting GATIS to any
other schema must parse English to know whether 60 is inches or feet. The
`node.width` / `edge.width` type disagreement above is what prose-only units
produce. Overture is working the same gap from the other side (schema issue
bd-uzbn) and has the easier case, since its fixed units are uniformly metres.

**The tier model is conformance, and it has been folded into the schema.** Tiers
are a maturity roadmap — a claim about a *dataset's* completeness — but they are
expressed by varying each field's presence, which makes presence four-dimensional
(feature class × feature type × field × tier) and yields 3,120 decisions for
edges alone. Overture keeps schema and conformance apart for this reason: the
schema says what a valid feature looks like, and a separate profile says what a
publisher has committed to. Folding them together means a Tier 1 publisher and a
Tier 4 publisher are validating against different schemas that share a name, and
`required` no longer means required.

**`recommended` is not a validation state.** It sits in the presence vocabulary
between `optional` and `required`, and a validator can do nothing with it that it
cannot do with `optional`. It is documentation wearing a schema's clothes, and it
roughly doubles the size of the presence matrix.

**Referential integrity is nobody's job, and the spec should say so.**
`from_node` and `to_node` reference `nodes.node_id` across files, and the files
are validated separately -- nothing holds both an edge and its endpoints at
validation time. A dangling `from_node` is therefore a conforming dataset. This
is not a criticism of the split: Overture has the identical shape, with
`Segment.connectors[].connector_id` referencing a `Connector` that ships in its
own partition, and it declares the relationship in the schema while checking
nothing. The declaration is for downstream tooling; enforcement is a
dataset-level step. What GATIS is missing is the *declaration* -- there is no
machine-readable statement that `from_node` points at `nodes.node_id` at all,
only the sentence "Value needs to be from the nodes table in the node ID field."
This package declares it with an Overture `Reference` and implements the
integrity check at the dataset level.

**Relation tables are named and not defined.** *"At this time, the specification
does not explicitly define how to create or utilize relation tables. We expect to
address this more fully in the second draft."* They are the stated mechanism for
intersections, turn restrictions and two-stage left turns — which is to say, for
the parts of a network where routing actually gets hard. Overture's
segment/connector model with turn-restriction rules is a worked precedent for the
same problem and is worth reading before the second draft settles the shape.

## Artifacts of assuming GeoJSON

GeoJSON is the delivery format, and in several places its limits have been
written down as though they were decisions. Each of these reads as policy and is
really a container constraint.

**Open extensibility is not a governance choice.** Section 6.1 grants that
*"anyone can add any attribute they want to a dataset"* and that the validator
*"will warn, but not fail on, new or unknown fields."* GeoJSON's `properties` is
an untyped bag, so this is what the container already does; the spec has
described its container rather than decided anything. The cost is real: a field
that is `forbidden` for a feature type and a field nobody has heard of arrive
identically, and the validator cannot distinguish a spec violation from a
sanctioned local extension without the presence matrix in hand. A schema'd
container makes extension explicit — a declared namespace, a typed extension
column — and then a warning means something. This repo models it the same way for
compatibility, keeping the forbidden set as data purely to produce the right
diagnostic.

**The four files are the type system, and that is one axis too few.** Nodes and
points are both `Point` geometry, distinguished only by which file they are in.
`transit_stop` and `issue` appear as *both* a node type and a point type with
near-identical descriptions, and the internal notes are an unresolved argument
about which they should be — *"This is a point, not a node"* / *"a lot of folks in
the accessibility working group wanted them to be nodes, for routing
convenience."* That is not a disagreement about taxonomy; it is one about graph
participation, and it is being settled by file placement because a GeoJSON file
holds one FeatureCollection with no room for a second discriminator. Overture's
theme / type / subtype / class nesting lets a transit stop be one kind of thing
that is or is not part of the routing graph.

**Banning MultiLineString and MultiPolygon is aimed at the wrong target.**
Section 3.1 says features *"must be LINE type (MULTILINE type is not supported)"*.
The real requirement is one traversable path per edge, so the topology is
well-defined. The prohibition does not deliver that — a self-intersecting
LineString or two coincident edges both pass — and it rules out legitimate
multipart geometry for a zone with a hole. State the topological requirement and
let the geometry type follow.

**No linear referencing, so segmentation became a mandate.** Section 2.2.2
requires splitting an edge whenever any attribute changes, because *"edges can
only support one set of attributes along their entire length."* That is a
statement about a flat properties bag, not about sidewalks. Overture moved away
from exactly this rule to scoped properties with `between: [start, end]`
subranges, because splitting explodes feature counts, destroys identifier
stability across releases — the same identifiers the spec has not yet defined —
and forces every attribute change to be a topology change. A spec that already
requires segmentation at every intersection is asking publishers to re-split
their network each time a width measurement improves.

**Left/right/both is encoded in field names.** Section 2.2.1 shows
`sidewalk:left:presence=yes` — OSM colon-namespacing, adopted because a GeoJSON
properties object is a flat string-to-value map with no nested scope. Two
consequences. Field names become a grammar a validator must parse rather than a
set it can check. And none of these colon-namespaced fields appear anywhere in
section 3.0 or the workbook, which means **roadway-centerline representation —
blessed in section 2.3, and what every Tier 1 publisher will use — is
unspecified**. This package can only model parallel-feature representation, and
that is a property of the source, not a limitation of the modelling. It is the
largest gap in the draft.

**Provenance is dataset-wide because a feature has nowhere to put it.** GeoJSON
gives a feature no metadata slot, so everything provenance-related lives in
`metadata.json`: one `collection_method`, one `source_dataset`, one
`collection_period`. A real dataset blends LiDAR-derived widths with a 2019 field
survey of surface condition, and GATIS has no way to say so. `check_date` and
`date_built` are the only per-feature temporal facts, and there is no
per-feature `version` or `update_time` at all, so change detection between two
releases is a geometry diff. Overture carries `version`, `update_time` and a
`sources[]` array with per-property attribution on every feature, and the
per-property part is what makes a blended dataset honest.

**Booleans are strings.** `yes`/`no`, in the OpenStreetMap format (section 3.4).
JSON has booleans and GeoJSON permits them; this is inherited vocabulary rather
than a constraint, but it survives because the properties bag makes the type
invisible until someone writes a parser. Every consumer now special-cases nine
fields.

**Objects are described in prose because nesting is free.** `reference_ids`,
`gtfs_id` and `seasonal` are all typed `Array<Object>` with their shape given in
a sentence. `gtfs_id` contradicts itself — typed `Array<Object>`, described as
*"Represent as string with the format `{agency_id},{stop_id}`"*. Nothing in the
container forces a declaration, so none was made, and a validator can check none
of the three.

## What would move the most

Ordered by what it unblocks, not by effort.

1. **Specify identifiers.** Everything else compounds on it.
2. **Specify `reference_ids`.** It is the entire interoperability story and
   currently one sentence.
3. **Specify roadway-centerline representation**, or withdraw the endorsement in
   section 2.3. Tier 1 publishers have nothing to implement.
4. **Regenerate the document from the workbook, and stop hand-pasting.** The
   published artifact currently describes a schema that does not exist.
5. **Tokenise enum values** before the first dataset ships.
6. **Give the eighteen dimensioned fields a structural unit.**
7. **Separate the tier model from the field tables.** Presence becomes
   two-dimensional and the schema starts meaning one thing.
