"""Object shapes GATIS describes in prose but does not define as a schema."""

from __future__ import annotations

from overture.schema.system.optionality import Omitable
from pydantic import BaseModel, ConfigDict, Field


class ReferenceId(BaseModel):
    """An identifier for this feature in some other dataset.

    Nothing here is required, deliberately. The spec describes the shape only in
    prose -- "an array of JSONs with the source name and ID pair. Each JSON should
    contain an ID field and source field at minimum" -- and constrains nothing:
    the declared type is `Array<Object>` with no listed values, and upstream's own
    JSON Schema resolves it to `{"type": "object", "properties": {}}`, so any
    object validates.

    Requiring `id` and `source` is a reasonable reading of that sentence and it
    rejects 100% of published GATIS data. Across the two sample datasets, 348,223
    features carry a `reference_ids` entry and not one uses a key called `id`:
    Austin writes `sidewalks_id`, `CURB_RAMPS_ID` and `asmp_street_network_id`,
    Newark writes `edge_id`. All four conform. Enforcing the prose here would make
    these models stricter than the specification on the specification's own
    samples, which is a wish about the field rather than a model of it -- so the
    two named keys are typed when present, everything else is kept, and the
    underspecification is reported in `docs/spec-review.md` instead.

    This is the only join key GATIS offers to OSM, Overture, ARNOLD, TIGER or an
    LRS, which is what makes leaving it unconstrained upstream the costliest gap
    in the schema.
    """

    model_config = ConfigDict(extra="allow")

    source: Omitable[str] = Field(description="Name of the dataset the id belongs to")
    id: Omitable[str] = Field(description="The identifier within that dataset")


class GtfsReference(BaseModel):
    """A GTFS `agency_id` / `stop_id` pair for a transit stop."""

    agency_id: str = Field(description="GTFS agency_id")
    stop_id: str = Field(description="GTFS stop_id")


class SeasonalCondition(BaseModel):
    """A recurring seasonal issue affecting an edge."""

    season: Omitable[str] = Field(description="spring, summer, fall or winter")
    issue: Omitable[str] = Field(
        description="flooding, ice, snow, heavy rain, heat, low visibility, fog, wind"
    )
