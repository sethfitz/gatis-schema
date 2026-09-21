---
sidebar_position: 1
---

# PedestrianZone

Indicates a zone where pedestrians may travel freely in a range of paths they choose.

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `zone_id` | [`Id`](../../overture/schema/system/ref/id.md) | A unique identifier for the zone. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]<br/><br/>*`required at every tier`* |
| `bbox` | [`bbox`](../../system/geometric.md) (optional) | An optional bounding box for the feature |
| `geometry` | [`geometry`](../../system/geometric.md) | *Allowed geometry types: Polygon* |
| `zone_type` | `"pedestrian"` | Indicates the type of zone.<br/><br/>*`required at every tier`* |
| `surface_material` | `string` (optional) | Specifies the surface type. Select only one. Where the surface material changes, create a new zone.<br/><br/>*`optional from tier 1; recommended from tier 3`* |
| `facility_name` | `string` (optional) | Common or formal name for the zone. Can also include descriptions of a portion of a larger pedestrian zone if the zone is being segmented.<br/><br/>*`optional from tier 1; recommended from tier 3`* |
| `status` | [`Status`](types/status.md) (optional) | Most recent operating status of the zone. Whether the infrastructure is open and available for use. Default is 'open'<br/><br/>*`optional at every tier`* |
| `reference_ids[]` | `list<`[`ReferenceId`](../reference_id.md)`>` (optional) | Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.<br/><br/>*`optional at every tier`* |
| `reference_ids[].source` | `string` | Name of the dataset the id belongs to |
| `reference_ids[].id` | `string` | The identifier within that dataset |
