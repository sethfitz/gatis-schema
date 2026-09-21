# Id

A unique identifier.

Underlying type: `string`

## Constraints

- Minimum length: 1
- Allows only strings that contain no whitespace characters. (`NoWhitespaceConstraint`, pattern: `^\S+$`) (from [`NoWhitespaceString`](../no_whitespace_string.md))

## Used By

- [`Edge`](../../../../gatis_schema/models/edge.md)
- [`Node`](../../../../gatis_schema/models/node.md)
- [`PedestrianZone`](../../../../gatis_schema/models/pedestrian_zone.md)
- [`Point`](../../../../gatis_schema/models/point.md)
