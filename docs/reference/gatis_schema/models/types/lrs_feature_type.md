# LrsFeatureType

`Type` in the LRS table: "any edge, node, point or zone types within GATIS".

It is not. Two of the 22 values are not v1.0 feature types -- `virtual_link`,
which v1.0 removed, and `traffic island`, which v1.0 spells `traffic_island`
(two rows below `traffic_calming`, spelled with an underscore in this same
list). Eight v1.0 types are missing, including `road`, `pushbutton`,
`detector` and all three members of the curb-ramp system, so an LRS row cannot
name a road.

Kept verbatim anyway. Correcting it here would fork the spec and hide the
defect; `docs/spec-review.md` reports it and
`test_extension_type_vocabularies_still_predate_v1_0` pins it.

## Values

- `sidewalk`
- `footway`
- `crossing`
- `ramp`
- `traffic island` - Not a v1.0 feature type: v1.0 spells it `traffic_island`. This list spells `traffic_calming` with an underscore.
- `steps`
- `elevator`
- `escalator`
- `bikeway`
- `multi_use_path`
- `trail`
- `virtual_link` - Not a v1.0 feature type: removed from the edge types, though its presence column survives on all 78 edge attributes.
- `generic`
- `curb_ramp`
- `object`
- `sign`
- `transit_stop`
- `issue`
- `counter`
- `bike_parking`
- `open`
- `traffic_calming`

## Used By

- [`LrsCrosswalk`](../lrs_crosswalk.md)
