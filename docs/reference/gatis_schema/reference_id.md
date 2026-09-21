# ReferenceId

An identifier for this feature in some other dataset.

The spec defines this only in prose -- "an array of JSONs with the source name
and ID pair. Each JSON should contain an ID field and source field at minimum"
-- so the two named keys are modelled and anything else is kept. This is the
only join key GATIS offers to OSM, Overture, ARNOLD, TIGER or an LRS, which
makes leaving it unspecified upstream the costliest gap in the schema.

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `source` | `string` | Name of the dataset the id belongs to |
| `id` | `string` | The identifier within that dataset |

## Used By

- [`Edge`](models/edge.md)
- [`Node`](models/node.md)
- [`PedestrianZone`](models/pedestrian_zone.md)
- [`Point`](models/point.md)
