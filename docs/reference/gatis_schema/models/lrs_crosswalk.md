---
sidebar_position: 1
---

# LrsCrosswalk

One row of `lrs.json`: a GATIS feature located on an external LRS segment.

This is the only shape in GATIS that carries an *extent*.
`lrs_starting_milepoint` and `lrs_ending_milepoint` with `lrs_side` can say
that a thing runs from here to there along one side of a segment, which no
core field can -- `buffer_width_ft`, `street_parking`,
`street_parking_buffer_ft`, `separation_elements`, `shoulder_width_in` and
`curb_height_in` are all scalars on a road edge, so a buffer has a width and
nowhere to start or stop. The extent is reachable only against an external
linear referencing system, so a publisher without one cannot express it at
all. `docs/spec-review.md` recommendation 5.

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `gatis_id` | `string` | The identification number within GATIS for this piece of infrastructure. |
| `geometry_type` | [`GatisGeometryType`](types/gatis_geometry_type.md) (optional) | The type of geospatial feature within GATIS of the infrastructure. |
| `Type` | [`LrsFeatureType`](types/lrs_feature_type.md) (optional) | The type of infrastructure. Valid values are any edge, node, point or zone types within GATIS. |
| `reference_ids` | `list<string>` (optional) | The identification number or other identifier of the related road segment within the linear referencing system. Can be the identification number within a government, commercial or third-party LRS. If multiple LRS segments align with a piece of infrastructure mapped in GATIS, provide all IDs within a properly formatted list.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `lrs_source_url` | [`AnyUrl`](../../pydantic/networks/any_url.md) (optional) | The URL where the linear referencing system referenced in reference_ids can be found. |
| `lrs_starting_milepoint` | `string` (optional) | The milepoint on the LRS segment at which this specific infrastructure begins. |
| `lrs_ending_milepoint` | `string` (optional) | The milepoint on the LRS segment at which this specific infrastructure ends. |
| `lrs_side` | [`LrsSide`](types/lrs_side.md) (optional) | The side of the LRS segment where this infrastructure appears. This tagging should align with the direction of the LRS segment, with the segment start point appearing at milepoint 0. It may contradict the directionality of the GATIS segment, which is assigned based on the order in which the geometry of the GATIS segment was drawn. |
