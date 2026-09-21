---
sidebar_position: 1
---

# Event

One row of `events.json`: something that happened to a piece of infrastructure.

Construction, inspection, an ADA assessment, a repair, a removal. The table is
designed to absorb what an agency's asset management system already holds --
`work_order_id`, `costs`, `downtime`, `owner`, `maintainer` -- rather than to
ask for new collection.

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `event_id` | `string` | The unique identifier for the event. If the event already has an ID assigned within another dataset, such as an agency asset management dataset, use that ID here as well. |
| `event_datetime` | `string` (optional) | The date on which the event occurred. Include time if available; if not, fill in time with zeroes.<br/><br/>*Generic pattern-based string constraint. (`PatternConstraint`, pattern: `^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$`)* |
| `event_type` | `string` (optional) | The type of event that occurred. If multiple events occurred on the same day, break each out into a separate row. Recommended values: maintenance inspection; ADA assessment; other assessment; data update; complaint; repair; other maintenance work; construction; redesign; removal; other.<br/><br/>*A vocabulary v1.0 publishes for a field whose type it leaves open. (`SuggestedValues`)* |
| `gatis_id` | `string` (optional) | The GATIS identification number for the piece of infrastructure, used in the edge, node, point or zone tables. |
| `type` | [`EventFeatureType`](types/event_feature_type.md) (optional) | The type of infrastructure. Valid values are any edge, node, point or zone types wtihin GATIS. |
| `geometry_type` | [`GatisGeometryType`](types/gatis_geometry_type.md) (optional) | The type of geospatial feature within GATIS of the infrastructure. |
| `event_location` | [`geometry`](../../system/geometric.md) (optional) | Geospatial point or edge location where the event occurred. If inspection of a sidewalk, include the full sidewalk edge coordinates. If repair, include the point location where the repair was carried out. |
| `location_description` | `string` (optional) | Text description of the location where the event occurred. |
| `lrs_segment_id` | `string` (optional) | If the event occurred along a segment represented in the infrastructure owner's linear referencing system, the identification number or other identifier of the LRS segment. |
| `lrs_milepoint` | [`float64`](../../system/numeric.md) (optional) | If the event occurred along a segment represented in the infrastructure owner's linear referencing system, the milepoint at which the event occurred. |
| `work_order_id` | `string` (optional) | The identification number of the work order or other identifier within the managing jurisdiction's data systems. |
| `owner` | `string` (optional) | The entity that owns this piece of infrastructure. If a department, office or subagency is responsible for the infrastructure, list that department, office or subagency. |
| `maintainer` | `string` (optional) | The entity that is responsible for maintaining this piece of infrastructure. It may or may not be the same as owner. If a department, office or subagency is responsible for the infrastructure, list that department, office or subagency. |
| `executor_of_work` | `list<string>` (optional) | The entity that carried out any work associated with this event. If multiple, list all in list format. The executor may be a contractor, or it may be the entity listed as owner or maintainer for the infrastructure.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `inspector` | `list<string>` (optional) | If an inspection, the name or names of the party or parties carrying out the inspection. This may be the name of an individual, a contractor or some other party. If multiple, list all in list format.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `inspection_method` | `string` (optional) | The method used for inspecting the infrastructure. Recommended values: visual inspection; survey/audit; satellite; lidar; other imagery; other.<br/><br/>*A vocabulary v1.0 publishes for a field whose type it leaves open. (`SuggestedValues`)* |
| `description` | `string` (optional) | A description of the event, to convey further detail of what was done. This may include listing construction or repair work activities and describing materials used, providing the specific ADA standard under which an assessment was carried out and conveying results or planned next steps, or providing information on redesign- or planning-related activities. |
| `comments` | `string` (optional) | Any additional remarks or notes provided within the infrastructure owner's asset management dataset related to the event. |
| `costs` | [`int32`](../../system/numeric.md) (optional) | The total amount spent on carrying out any work or inspections that were part of the event, rounded to the nearest whole number. |
| `downtime` | `string` (optional) | The total amount of time related to the event during which the infrastructure was closed or inaccessible in whole or in part. Provide a value plus units - ex. "2 weeks", "3.5 days", "12 hours". |
| `related_issue` | [`Id`](../../overture/schema/system/ref/id.md) (optional) | The GATIS ID for an issue point related to this event. |
| `funding_source` | `string` (optional) | The source of funds for the construction, repair or other action taken as a part of the event. |
