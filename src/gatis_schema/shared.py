"""Object shapes GATIS describes in prose but does not define as a schema."""

from __future__ import annotations

from overture.schema.system.optionality import Omitable
from pydantic import BaseModel, ConfigDict, Field


class ReferenceId(BaseModel):
    """An identifier for this feature in some other dataset.

    The spec defines this only in prose -- "an array of JSONs with the source name
    and ID pair. Each JSON should contain an ID field and source field at minimum"
    -- so the two named keys are modelled and anything else is kept. This is the
    only join key GATIS offers to OSM, Overture, ARNOLD, TIGER or an LRS, which
    makes leaving it unspecified upstream the costliest gap in the schema.
    """

    model_config = ConfigDict(extra="allow")

    source: str = Field(description="Name of the dataset the id belongs to")
    id: str = Field(description="The identifier within that dataset")


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
