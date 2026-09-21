# Which upstream GATIS artifact to trust

Upstream is [`dotbts/BPA`](https://github.com/dotbts/BPA). It publishes the same
specification five ways, they disagree, and one of them is corrupt. Establish
which artifact a claim came from before acting on it.

## The order of authority

**`draft_gatis_specification/specification_jsons/{edges,nodes,points,zones,metadata}.json`
is the source to generate from and to settle arguments with.** This is GATIS
1.0, voted through 2026-02-27. Each file carries `types` and an `attributes`
array; each attribute has `name`, `description`, `type`, `listed_values`,
`example`, and a `presence` map of `{feature_type: [tier1, tier2, tier3,
tier4]}` where `null` means unchanged from the previous tier. That is the whole
(type x field x tier) matrix as structured JSON.

```sh
jq -r '.attributes[] | select(.name=="status") | .type, (.listed_values|tojson)' edges.json
```

**`gatis_explorer/data/**`** mirrors those files as CSV, same names and order.
Useful as a cross-check, not as a second opinion -- it is a rendering of the
same data. <https://dotbts.github.io/BPA/> renders it for humans.

**`draft_gatis_specification/json_schemas/*_schema.json` is upstream's own
validator and is broken for every `Array<Enum>` field.** Its generator has a
loop-variable bug: each `Array<Enum>` field gets the *last* `Array<Enum>`
field's enum. In `edges_schema.json`, `prohibited_uses`, `allowed_uses`,
`cross_vehicle_traffic_control` and `ped_protection` all carry the identical
12-value pedestrian-signal-timing list, so `prohibited_uses` offers "leading
pedestrian interval". In `nodes_schema.json`, `impediment`,
`rail_crossing_control` and `surface_issue` all carry the surface-issue list;
in `points_schema.json`, `accessibility_features` carries it too. Verified
2026-09-21 in the three files that have an `Array<Enum>` field at all; `zones`
has none, so it cannot show the bug either way.

**It also rejects every real GATIS feature, as shipped.** The discriminator's
enum is a spreadsheet cross-reference that was exported literally:
`edge_type` permits exactly `"(Same as Edge Types)"` and `node_type` exactly
`"(Same as Node Types)"`. So `edge_type: "road"` fails and the cross-reference
string passes. Measured against both published sample datasets: 0 of 351,693
features validate.

Two more faults matter if you ever repair it enough to run:

- **It requires nothing.** The `properties` object carries no `required` list
  at all, so every `required` presence rule in 1.0 is absent from it. It cannot
  catch Austin's 9,929 roads missing `directionality`.
- **`oneOf` plus an unasserted `format` inverts the date fields.** 21 edge
  fields are `oneOf [{"type":"string","format":"date"}, <YYYY-MM pattern>,
  <YYYY pattern>, null]`. `format` is annotation-only by default, so the first
  branch matches *any* string: `"banana"` validates, and `"2007-01"` and
  `"2007"` are **rejected** because they match two branches and `oneOf` demands
  exactly one. The spec's own permitted truncations fail while junk passes.
  Turning format assertion on fixes both, and it is off by default in every
  major implementation.

So: never take an enum, a required rule, or a date verdict from the JSON
Schema, and never cite it as evidence about what the spec permits. Its scalar
`type` keywords and its `null` branches are the sound part, and the null
branches remain the only machine-readable statement upstream makes about
whether an absent field may be written as `null`.

`specification_jsons` is the artifact to trust, not an artifact that is correct.
Its `listed_values` are mangled for at least eight fields, by two separate
mechanisms -- a newline split against hard-wrapped workbook cells, and a pipe
that was never treated as a separator at all. See
[`validating-gatis-data.md`](validating-gatis-data.md) for the cases, and
`spec/repairs.json` for the local corrections. Check the file for the feature
class you care about: 1.0 gives one field name different vocabularies across
edges, nodes and zones, sometimes on purpose.

**The Google Sheet `1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ` is Draft #2**,
which upstream's README labels as such. Draft #3 used a different sheet. Both
are superseded and neither is pinned here any more. Do not read either to
answer a question about current GATIS.

## Reading it without Drive access

Everything above is in the public git repository, so `gh` reaches it and nothing
needs a Google login.

```sh
gh api 'repos/dotbts/BPA/git/trees/main?recursive=1' --jq '.tree[].path'
curl -sL https://raw.githubusercontent.com/dotbts/BPA/main/draft_gatis_specification/specification_jsons/edges.json
```

Pin a commit rather than tracking `main`; upstream force-pushes (there is a
`Revert "incorporate feedback"` in the history).

## The sample datasets

The [sample datasets
page](https://dotbts.github.io/BPA/gatis_explorer/pages/sample_datasets.html)
contains no data. It is a shell that fetches
`draft_gatis_specification/sample_data/maps/maps.json` and iframes ~30 MB Folium
maps. The datasets themselves:

- **Newark, DE (Tier 3)** -- in the repo, at
  `draft_gatis_specification/sample_data/newark_de/newarkDE_sample_{edges,nodes}.geojson`.
- **Austin, TX (Tier 2)** -- not in the repo. ArcGIS item ids are in the
  `description` field of `maps.json`; download with
  `https://usdot.maps.arcgis.com/sharing/rest/content/items/<id>/data`. The
  edges file is 280 MB and is the full dataset, not the clipped sample the map
  shows.

Neither file declares a spec version, and both predate the commit `spec/`
pins, so they can carry vocabulary 1.0 has since renamed. Check
`spec/MANIFEST.json` for what is actually pinned rather than assuming either
direction.

An `osm/` conversion notebook exists with no committed output, and
`seattle/` has a notebook and no data.
