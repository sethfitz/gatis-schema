# Upstream spec snapshot

A pinned copy of the two upstream GATIS sources. Refresh with `scripts/snapshot-spec`;
`MANIFEST.json` records the Drive revision and a SHA-256 of every file.

| Path | Source |
| --- | --- |
| `workbook/*.csv` | [`Draft_GATIS_Specification`](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit), one CSV per tab (all 25, hidden ones included) |
| `document.md` | [GATIS v2 DRAFT](https://docs.google.com/document/d/13sJdh-GmfxNb_tfUXKkpZgofuBU60ag6HpqbGVUlsZE/edit), exported as Markdown |

The only transform applied is to `document.md`: Docs emits each figure as a
base64 `data:` URI, which is 97% of the export's bytes and re-encodes on every
render. Those definition lines are replaced with `<data:image stripped>`.

## The workbook is normative, not the document

Section 3.0 of the document is a stub. Every field and type table in 3.2-3.4 reads
*"Moved here"* and links to a workbook tab. The `** README **` tab states the
direction of travel: *"The 'final' tabs are imported into the Google Doc for the
spec."*

That import is manual and has not kept up. As snapshotted, the workbook was modified
**2026-01-30** and the document **2025-11-12**, and the tables pasted into the
document are two and a half months stale.

The derivation chain, and which link to trust:

```
*_Fields, *_Types   authoritative -- hand-maintained, the actual spec
      |
      v
*_Presence, Presence Tables   derived pivots, stale
      |
      v
document sections 3.3.1 / 3.4.1   pasted from the pivots, stale
```

Generate from `*_Fields` and `*_Types`. Anything taken from the document's presence
tables will name fields the workbook does not define -- `road_speed`, `width_min`,
`surface_quality`, `car_freeflow_speed`, `ada_compliance`, `rail`, and a
`detectable_warning` that exists only on nodes.

The document remains the only source for the metadata file (section 3.1), the
presence descriptors (3.3), the attribute types (3.4) and all of the narrative that
the field tables assume: tiers (2.1), routability (2.2.1), directionality and the
left/right modifiers (2.2.1), segmentation (2.2.2), and representation conventions
(2.3).

## Known upstream defects

The reader surfaces these rather than crashing or silently picking a side. Each is
pinned by a test in `tests/test_spec_source.py`.

- **Three edge field names carry a trailing space** (`ped_traffic_control `,
  `vehicle_traffic_control `, `cross_vehicle_traffic_control `). Stripped on read;
  unstripped they would generate unreachable fields.
- **`Points_Fields` lists `impediment` and `surface_issue` twice**, with value sets
  that disagree with each other and with the node equivalents.
- **One `Points_Fields` `impediment` row is column-shifted**: its name and
  description are pasted into the two presence columns. Reported as a `SpecDefect`.
- **`*_Types` and `*_Fields` disagree on which types exist.** `elevator` is a
  declared edge type with no presence column, so the workbook gives it no fields at
  all -- not even `edge_id`. `Points_Types` declares `object`, `sign`,
  `transit_stop` and `issue`; `Points_Fields` has columns for `object` and `point`,
  and `point` is not a declared type.
- **`Presence Tables` and the document still spell `multi_use_path` as
  `mutli_use_path`** and `traffic_island` as `raisedtraffic_island`. `Edges_Types`
  and `Edges_Fields` have the correct spellings.
- **`node.width` is `Float` while `edge.width` is `Integer`**, though both
  descriptions say inches rounded to the nearest inch.
- **Two cells hold an editorial comment where values belong**: `edge.incline` and
  `node.traffic_calming_type` both have `[JG1]Grabbed from NACTO Bike design guide`
  in Listed Values.
