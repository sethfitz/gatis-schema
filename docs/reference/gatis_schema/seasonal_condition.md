# SeasonalCondition

A recurring seasonal issue affecting an edge.

The two vocabularies are hand-split from one mangled cell. `seasonal`'s
`listed_values` runs both together and marks the boundary with a label
carried inside a value -- `"season: spring", "summer", ..., "seasonal
issues: flooding", "ice", ...` -- so no exporter fix recovers them and
`spec/repairs.json` does not try: codegen routes this field to this class
instead. `test_seasonal_condition_still_matches_the_mangled_cell` pins them
to the snapshot.

Open on purpose, like every other `Text` vocabulary in v1.0.

## Fields

| Name | Type | Description |
| -----: | :----: | ------------- |
| `season` | `string` (optional) | Recommended values: spring; summer; fall; winter.<br/><br/>*A vocabulary v1.0 publishes for a field whose type it leaves open. (`SuggestedValues`)* |
| `issue` | `string` (optional) | Recommended values: flooding; ice; snow; heavy rain; heat / lack of shade; low visibility; fog; wind.<br/><br/>*A vocabulary v1.0 publishes for a field whose type it leaves open. (`SuggestedValues`)* |

## Used By

- [`Edge`](models/edge.md)
