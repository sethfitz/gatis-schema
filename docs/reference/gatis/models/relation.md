---
sidebar_position: 1
---

# Relation

One row of `relations.json`: a link between two pieces of infrastructure.

Two uses were designed for: tying a pushbutton or detector to the crossings it
controls (`signal_id`, `crossing_id`), and describing a turning movement
(`from_id`, `to_id`, `turning_treatment`). The Playbook says the table "may be
used for any other purpose of relating two pieces of infrastructure."

It has no extent and no side. That is the gap that keeps a GATIS publisher
without an external LRS from saying where along an edge something applies --
`LrsCrosswalk` has the milepoints, and it can only anchor them to a foreign
segment.

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `relation_id` | [`Id`](../../overture/schema/system/ref/id.md) | The identification number for the relation described in this row. |
| `from_id` | `list<`[`Id`](../../overture/schema/system/ref/id.md)`>` (optional) | For a relation that is a movement, the GATIS ID for the piece of infrastructure at which the movement begins.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `to_id` | `list<`[`Id`](../../overture/schema/system/ref/id.md)`>` (optional) | For a relation that is a movement, the GATIS ID for the piece of infrastructure at which the movement completes.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `signal_id` | `list<`[`Id`](../../overture/schema/system/ref/id.md)`>` (optional) | For a signal relation, the GATIS ID for the signal point. If multiple (ex. at the west and east ends of a crossing), provide all IDs in a list.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `crossing_id` | `list<`[`Id`](../../overture/schema/system/ref/id.md)`>` (optional) | For a signal relation, the GATIS ID for the crossing edge that is affected when the signal point under signal_id is interacted with by a traveler. If multiple, provide all IDs in a list.<br/><br/>*A column declared as one value and documented as possibly several. (`ScalarOrListConstraint`)* |
| `turning_treatment` | `string` (optional) | For a relation that is a turning movement, any treatments at the intersection that are meant to facilitate the turn for travelers. Recommended values: bike box; two-stage turn box; protected intersection; bike signal; bike leading interval; mixing zone; scramble.<br/><br/>*A vocabulary v1.0 publishes for a field whose type it leaves open. (`SuggestedValues`)* |
