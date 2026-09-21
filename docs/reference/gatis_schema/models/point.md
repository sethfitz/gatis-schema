---
sidebar_position: 1
---

# Point

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `point_id` | [`Id`](../../overture/schema/system/ref/id.md) | A unique identifier for the point. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]<br/><br/>*`required at every tier`* |
| `geometry` | [`geometry`](../../system/geometric.md) | *Allowed geometry types: Point* |
| `bbox` | [`bbox`](../../system/geometric.md) (optional) | An optional bounding box for the feature |
| `point_type` *(Object)* | `"object"` | Indicates the type of point.<br/><br/>*`required at every tier`* |
| `object_type` *(Object)* | `string` (optional) | Used to indicate objects that appear near the sidewalk or street space that, depending on the traveler, may be an amenity or an obstruction. Buffers around these points can be used to factor them into routing algorithms. If an object is on the pedestrian way, consider marking it with an issue node instead. Recommended values: bench; lighting; waste basket; accessible restroom; inaccessible restroom; water fountain; parklet / kiosk; pet station; transit stop.<br/><br/>*`optional from tier 1; recommended from tier 3`* |
| `reference_ids[]` *(Object, Point)* | `list<`[`ReferenceId`](../reference_id.md)`>` (optional) | Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.<br/><br/>*`optional at every tier`* |
| `reference_ids[].source` | `string` | Name of the dataset the id belongs to |
| `reference_ids[].id` | `string` | The identifier within that dataset |
| `point_type` *(Point)* | `"point"` | Indicates the type of point.<br/><br/>*`required at every tier`* |
| `sign_verbiage` *(Point)* | `string` (optional) | Provides the text that appears on the sign. Include only the visible text, and do not wrap it in quotation marks or other punctuation.<br/><br/>*`optional from tier 1; recommended from tier 3`* |
| `sign_auditory` *(Point)* | `boolean` (optional) | Indicates whether the sign_verbiage or another similar message is available in an auditory format at the sign location.<br/><br/>*`optional from tier 1; recommended from tier 3`*<br/>*`BeforeValidator(func=<function _parse_yes_no at 0x103912c00>, json_schema_input_type=PydanticUndefined)`*<br/>*`PlainSerializer(func=<function <lambda> at 0x103912ca0>, return_type=<class 'str'>, when_used='always')`* |
| `sign_association` *(Point)* | `list<`map<string, object>`>` (optional) | Indicates the GATIS ID of any infrastructure this sign refers to. For example, if a sign tells pedestrians that state law requires vehicles to yield to them in the crosswalk, this attribute can be used to indicate the GATIS ID of the specific crosswalk or crosswalks.<br/><br/>*`optional at every tier`* |
| `sign_designation` *(Point)* | `string` (optional) | Indicates the type of sign as described within the MUTCD, within the 'Sign Designation' field (https://mutcd.fhwa.dot.gov/kno- shs_2024-release-status/index.htm).<br/><br/>*`optional at every tier`* |
| `sign_name` *(Point)* | `string` (optional) | Indicates the type of sign as described within the MUTCD, within the 'Sign Name' field (https://mutcd.fhwa.dot.gov/kno- shs_2024-release-status/index.htm).<br/><br/>*`optional at every tier`* |
| `surface_issue` *(Point)* | `list<`[`SurfaceIssue`](types/surface_issue.md)`>` (optional) | Identifies the type of damage or surface quality issue that may pose a challenge for travelers.<br/><br/>*`optional from tier 1; recommended from tier 3; required from tier 4`* |
