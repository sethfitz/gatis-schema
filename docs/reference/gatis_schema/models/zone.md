---
sidebar_position: 1
---

# Zone

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `zone_id` | [`Id`](../../overture/schema/system/ref/id.md) | A unique identifier for the zone. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]<br/><br/>*`required at every tier`* |
| `geometry` | [`geometry`](../../system/geometric.md) | *Allowed geometry types: Polygon* |
| `bbox` | [`bbox`](../../system/geometric.md) (optional) | An optional bounding box for the feature |
| `zone_type` *(Open)* | `"open"` | Indicates the type of zone.<br/><br/>*`required at every tier`* |
| `surface_material` *(Open)* | `string` (optional) | Specifies the surface type. Select only one. Where the surface material changes, create a new zone. Recommended values: asphalt; concrete; gravel; grass; dirt; paved; unpaved; grass paver; paving stones; other.<br/><br/>*`optional from tier 1; recommended from tier 3`* |
| `facility_name` *(Open)* | `string` (optional) | Common or formal name for the zone. Can also include descriptions of a portion of a larger open zone (like a park or a plaza) if the zone is being segmented.<br/><br/>*`optional from tier 1; recommended from tier 3`* |
| `status` *(Open, TrafficCalming)* | [`ZoneStatus`](types/zone_status.md) (optional) | Most recent operating status of the zone. Whether the infrastructure is open and available for use. If blank, the assumed value is 'open.'<br/><br/>*`optional at every tier`* |
| `reference_ids[]` *(Open, TrafficCalming)* | `list<`[`ReferenceId`](../reference_id.md)`>` (optional) | Can be used to add reference IDs to other datasources such as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.<br/><br/>*`optional at every tier`* |
| `reference_ids[].source` | `string` | Name of the dataset the id belongs to |
| `reference_ids[].id` | `string` | The identifier within that dataset |
| `prohibited_uses` *(Open)* | `list<string>` (optional) | Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form. Recommended values: walk; bike; ebike class 1; ebike class 2; ebike class 3; scooter; NEV; motor_vehicle; other.<br/><br/>*`optional at every tier`* |
| `allowed_uses` *(Open)* | `list<string>` (optional) | Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footways, and crossings for routing purposes. Recommended values: walk; bike; ebike class 1; ebike class 2; ebike class 3; scooter; NEV; motor_vehicle; other.<br/><br/>*`optional at every tier`* |
| `last_inspection_date` *(Open, TrafficCalming)* | `string` (optional) | The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.<br/><br/>*`optional at every tier`*<br/>*Generic pattern-based string constraint. (`PatternConstraint`, pattern: `^\d{4}(-\d{2}(-\d{2})?)?$`)* |
| `date_built` *(Open)* | `string` (optional) | Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.<br/><br/>*`optional at every tier`*<br/>*Generic pattern-based string constraint. (`PatternConstraint`, pattern: `^\d{4}(-\d{2}(-\d{2})?)?$`)* |
| `zone_type` *(TrafficCalming)* | `"traffic_calming"` | Indicates the type of zone.<br/><br/>*`required at every tier`* |
| `surface_material` *(TrafficCalming)* | `string` (optional) | Specifies the surface type. Select only one. Where the surface material changes, create a new zone. Recommended values: asphalt; concrete; gravel; grass; dirt; paved; unpaved; grass paver; paving stones; other.<br/><br/>*`optional at every tier`* |
| `date_built` *(TrafficCalming)* | `string` (optional) | Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.<br/><br/>*`recommended at every tier`*<br/>*Generic pattern-based string constraint. (`PatternConstraint`, pattern: `^\d{4}(-\d{2}(-\d{2})?)?$`)* |
| `traffic_calming_type` *(TrafficCalming)* | [`TrafficCalmingType`](types/traffic_calming_type.md) | The type of traffic calming measure that is present in a traffic_calming zone. Recommended values are from https://www.ite.org/technical-resources/traffic-calming/traffic-calming- measures/ and https://wiki.openstreetmap.org/wiki/Key:traffic_calming.<br/><br/>*`required at every tier`* |
