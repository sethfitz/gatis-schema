# LrsSide

Which side of the LRS segment the infrastructure is on.

The only place in GATIS where `both` is a legal side. The on-road modifier
fields in `edges_schema.json` enumerate `left` and `right` only, across all
292 of them, though the Playbook's section on them is titled "Left, Right and
Both Tags".

## Values

- `left`
- `right`
- `both`

## Used By

- [`LrsCrosswalk`](../lrs_crosswalk.md)
