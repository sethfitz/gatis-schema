# Upstream spec snapshot

A pinned copy of the published GATIS v1.0 specification, taken from
[`dotbts/BPA`](https://github.com/dotbts/BPA). Refresh with `scripts/snapshot-spec`;
`MANIFEST.json` records the commit and a SHA-256 of every file.

`playbook.md` comes from Google Docs rather than the repository, so it has its own
script and its own manifest -- `scripts/snapshot-playbook` and
`PLAYBOOK-MANIFEST.json`, pinned by Drive `modifiedTime` and version rather than by
commit. The export escapes underscores, so `width\_in` is how a field name appears;
grep it through `sed 's/\\_/_/g'` or the hit count is 0. The two illustrations are
dropped on the way in -- Docs inlines them as ~290 KB of base64 that churns on every
re-export -- and the `![][imageN]` references are left in place to say where a figure
belongs. Both artifacts are CC0 1.0.

| Path | Source |
| --- | --- |
| `specification/*.json` | `draft_gatis_specification/specification_jsons/` -- types, attributes and the full presence matrix. The generation source. |
| `json-schemas/*.json` | `draft_gatis_specification/json_schemas/` -- upstream's own validator. Not read by the reader; compared against ours by `scripts/compare-json-schema`. |
| `explorer/**` | `gatis_explorer/data/` -- the same content as CSV, rendered at [the GATIS Explorer](https://dotbts.github.io/BPA/). A cross-check, not a source. |
| `introduction.html` | `gatis_explorer/pages/specification_introduction.html` -- the narrative sections the attribute tables assume. |
| `extensions.pdf` | `documents/drafts/GATIS Extensions and Tables.pdf` -- the only definition of the `lrs.json`, `events.json` and `relations.json` files section 2.1 declares. `extensions.txt` beside it is a `pdftotext -layout` extraction, derived rather than upstream, so the field tables can be grepped and diffed. |
| `extensions.json` | **Not upstream.** A hand transcription of those three tables into the shape `specification_jsons` would have used, so `models/extensions.py` has a source to be checked against. One field, `multiple`, is a judgement rather than a transcription -- it marks a column the PDF types as a scalar and then tells the publisher may hold several, and its value is the licensing sentence quoted from that column's own description. `scripts/snapshot-spec` does not write this file and `MANIFEST.json` does not list it. Delete it the day upstream publishes the tables as JSON. |
| `playbook.md` | The [GATIS Playbook](https://docs.google.com/document/d/1_3Zz1hudUCunHNpgFDY74ybvNgjttcTdQ9c9LTYm3uE/edit), which `introduction.html` links as one of the three published artifacts. Not in the repository, so it has its own pin. |

## Why a repository and not a Google Sheet

A Drive export cannot tell you the sheet it reads has been superseded. Upstream's
README calls `Draft_GATIS_Specification` **Draft #2**; draft #3 moved to a
different sheet and v1.0 was voted through on 2026-02-27, and through all of it
that first sheet still exists with the same revision history. A commit in
`dotbts/BPA` makes the version a property of the snapshot rather than an
assumption about a link.

## The presence matrix

`specification/*.json` carries `(feature type x field x tier)` as structured JSON:

```json
"width_in": { "type": "Integer", "presence": {
    "sidewalk": ["optional", "required", null, null] } }
```

Four slots, one per tier, `null` meaning unchanged from the tier before. That is
the whole matrix in machine-readable form, and it is why `spec_source` reads these
files and nothing else.

## What v1.0 gets wrong

Each is pinned by a test in `tests/`, so an upstream fix shows up as a failure
rather than going unnoticed.

- **`json_schemas/*_schema.json` is wrong for every `Array<Enum>` field.** Its
  generator reuses the last such field's vocabulary: `edges` gives
  `allowed_uses`, `prohibited_uses` and `cross_vehicle_traffic_control` the
  pedestrian-signal-timing list belonging to `ped_protection`; `nodes` gives
  `impediment` and `rail_crossing_control` the `surface_issue` list; `points`
  gives it to `accessibility_features`. `specification_jsons` is the artifact to
  trust. `scripts/compare-json-schema`
  reports the difference.
- **Upstream's JSON Schema declares no required fields at all**, on any of the
  four files, so it cannot check presence -- which is most of what the spec says.
- **`edges.json` carries a `virtual_link` presence column for a type it does not
  declare**, on every attribute. Generating from the presence columns would put a
  type into the union that `types` does not list, so generation reads `types`
  instead and `fields_without_types` reports the orphan.
- **Three edge types forbid a field that does not exist.** `sidewalk`, `bikeway`
  and `multi_use_path` list `road_associated` in
  `forbidden_field_if_allowed_on_road`; no file declares an attribute by that name.
- **A field name can mean something different depending on the file.** Of the
  names appearing in more than one of the four, these disagree in vocabulary, in
  declared type, or in both: `status`, `presence`, `impediment`, `surface_issue`,
  `other_issue`, `allowed_uses`, `prohibited_uses`, `surface_material`,
  `ada_compliant_with` and `width_in`. `status` has three vocabularies (`edges`
  adds the two `proposed` values, `nodes` `planned`, `zones` `other`);
  `surface_issue` is `Text` on edges and `Array<Enum>` on nodes and points;
  `width_in` is `Integer` on edges and `Float` on nodes.
- **`listed_values` arrays do not survive publication intact.** v1.0 exports each
  vocabulary from a spreadsheet cell. Splitting on newlines
  fragments a hard-wrapped definition (`separation_permeable_car` becomes six
  entries including `"curbs)"` and two empty strings) and turns a blank line into
  an empty value (`markings`); a run-together line stays fused
  (`separation_elements`'s `"trees  unknown"`, `allowed_uses`'s `"motor_vehicle
  ebike class 2 ebike class 3 other"`); a pipe is never treated as a separator at
  all (`presence` on nodes); `traffic_calming` interleaves section headings with
  values; and `incline`, a Float with no vocabulary to publish, carries a leaked
  Google Docs comment anchor as its only entry. Corrected in
  [`repairs.json`](repairs.json), which records every departure from the verbatim
  snapshot and why. The repairs are not the whole defect: `edge_type`, `node_type`
  and `street_parking` are mangled too and go unrepaired, because codegen routes
  around them rather than reading their `listed_values`.
- **Null-versus-omitted is unstated.** Nothing in `specification_jsons` says
  whether an unset property should be omitted or written as `null`, and the two
  published sample datasets choose differently -- Austin omits, Newark writes
  nulls for 57% of its slots. Upstream's JSON Schema permits `null` on 159 of 370
  edge properties, so these models accept it and treat it as absent; see
  `drop_null_properties`.
