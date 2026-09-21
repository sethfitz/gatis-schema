"""GATIS zone models.

BOOTSTRAPPED by `gatis_schema.codegen` from the pinned spec snapshot
(workbook Drive revision 3542) on 2026-09-20.

Hand-edits are expected and are not overwritten: the bootstrap refuses to
rewrite an existing file without `--force`. Refine freely -- the workbook
cannot express half of what these models should say.
"""

from __future__ import annotations

from typing import Annotated, Literal

from overture.schema.system.feature import Feature
from overture.schema.system.geometric import (
    Geometry,
    GeometryType,
    GeometryTypeConstraint,
)
from overture.schema.system.numeric import float64, int32
from overture.schema.system.optionality import Omitable
from overture.schema.system.ref import Id
from pydantic import BaseModel, Field, Tag, TypeAdapter

from gatis_schema.annotations import (
    Aadt,
    Feet,
    Inches,
    InchesFloat,
    Mph,
    Percent,
    Tier,
)
from gatis_schema.scalars import GatisDate, GatisDatetime, YesNo
from gatis_schema.shared import (
    GtfsReference,
    ReferenceId,
    SeasonalCondition,
)
from gatis_schema.models.enums import (
    Status,
)


class PedestrianZone(Feature):
    """Indicates a zone where pedestrians may travel freely in a range of paths they choose."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.POLYGON),
    ]

    zone_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the zone. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the zone."""

    zone_type: Annotated[Literal["pedestrian"], Tier("required")] = Field(description="Indicates the type of zone.")
    """Indicates the type of zone."""

    surface_material: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="Specifies the surface type. Select only one. Where the surface material changes, create a new zone.")
    """Specifies the surface type."""

    facility_name: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="Common or formal name for the zone. Can also include descriptions of a portion of a larger pedestrian zone if the zone is being segmented.")
    """Common or formal name for the zone."""

    status: Annotated[Omitable[Status], Tier("optional")] = Field(description="Most recent operating status of the zone. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the zone."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""


Zone = PedestrianZone
"""Any zone, discriminated on `zone_type`."""

ZoneAdapter: TypeAdapter[Zone] = TypeAdapter(Zone)
"""Validator for one zone, including from raw GeoJSON."""


class ZoneCollection(BaseModel):
    """The contents of `zones.geojson`."""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Zone]
