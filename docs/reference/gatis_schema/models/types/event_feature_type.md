# EventFeatureType

`type` in the events table, and a different list from `LrsFeatureType`.

Same sentence introduces it and the vocabulary disagrees: this one adds
`virtual_node` and `open_movement` -- draft-2 names v1.0 renamed to `generic`
and `open` -- keeps `virtual_link`, and drops `generic`, `open` and
`traffic_calming`. Eleven v1.0 types are unreachable from an events row.

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
- `virtual_node` - Not a v1.0 feature type: the draft-2 name for what v1.0 calls `generic`, which this list does not offer.
- `curb_ramp`
- `object`
- `sign`
- `transit_stop`
- `issue`
- `counter`
- `bike_parking`
- `open_movement` - Not a v1.0 feature type: the draft-2 name for what v1.0 calls the `open` zone, which this list does not offer.

## Used By

- [`Event`](../event.md)
