"""GATIS point models.

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
from overture.schema.system.optionality import Omitable
from overture.schema.system.ref import Id, Identified
from pydantic import BaseModel, ConfigDict, Field, Tag, TypeAdapter

from gatis_schema.annotations import (
    Tier,
)
from gatis_schema.models.enums import (
    SurfaceIssue,
)
from gatis_schema.scalars import YesNo
from gatis_schema.shared import (
    ReferenceId,
)


class PointBase(Identified, Feature):
    """Common base for every GATIS point type."""

    model_config = ConfigDict(
        # Section 6.1 guarantees local extensibility: an unknown field warns,
        # it does not fail. Extras land in `model_extra` and Feature's
        # serializer routes them back through `properties`.
        extra="allow",
        populate_by_name=True,
        serialize_by_alias=True,
    )

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.POINT),
    ]
    # Redeclared from `Feature`, where it is `Omitable[Id]`, to make it
    # mandatory. Same narrowing, and the same silencing, as Overture's own
    # `OvertureFeature`.
    id: Annotated[Id, Tier("required")] = Field(  # type: ignore[assignment]
        alias="point_id",
        description="A unique identifier for the point. [NOTE: We will fill in "
        "instructions here on how to generate IDs, and we will also provide a data "
        "validator that may be capable of validating and helping to fill in these "
        "IDs.]",
    )


class ObjectPoint(PointBase):
    """A physical object that is likely to be of interest to travelers."""

    point_type: Annotated[Literal["object"], Tier("required")] = Field(
        description="Indicates the type of point."
    )

    object_type: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="Used to indicate objects that appear near the sidewalk or "
        "street space that, depending on the traveler, may be an amenity or an "
        "obstruction. Buffers around these points can be used to factor them into "
        "routing algorithms. If an object is on the pedestrian way, consider "
        "marking it with an issue node instead. Recommended values: bench; "
        "lighting; waste basket; accessible restroom; inaccessible restroom; water "
        "fountain; parklet / kiosk; pet station; transit stop."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum. Can add other attributes "
        "such as the beginning and ending milepost from a linear referencing "
        "system."
    )


class PointPoint(PointBase):
    """point"""

    point_type: Annotated[Literal["point"], Tier("required")] = Field(
        description="Indicates the type of point."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum. Can add other attributes "
        "such as the beginning and ending milepost from a linear referencing "
        "system."
    )

    sign_verbiage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Provides the text that appears on the sign. Include only the "
            "visible text, and do not wrap it in quotation marks or other punctuation."
        )
    )

    sign_auditory: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Indicates whether the sign_verbiage or another similar "
            "message is available in an auditory format at the sign location."
        )
    )

    sign_association: Annotated[Omitable[list[dict[str, object]]], Tier("optional")] = (
        Field(
            description="Indicates the GATIS ID of any infrastructure this sign refers "
            "to. For example, if a sign tells pedestrians that state law requires "
            "vehicles to yield to them in the crosswalk, this attribute can be used to "
            "indicate the GATIS ID of the specific crosswalk or crosswalks."
        )
    )

    sign_designation: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Indicates the type of sign as described within the MUTCD, "
        "within the 'Sign Designation' field (https://mutcd.fhwa.dot.gov/kno- "
        "shs_2024-release-status/index.htm)."
    )

    sign_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Indicates the type of sign as described within the MUTCD, "
        "within the 'Sign Name' field (https://mutcd.fhwa.dot.gov/kno- "
        "shs_2024-release-status/index.htm)."
    )

    surface_issue: Annotated[
        Omitable[list[SurfaceIssue]],
        Tier("optional", {3: "recommended", 4: "required"}),
    ] = Field(
        description="Identifies the type of damage or surface quality issue that "
        "may pose a challenge for travelers."
    )


Point = Annotated[
    Annotated[ObjectPoint, Tag("object")] | Annotated[PointPoint, Tag("point")],
    Field(
        discriminator=Feature.field_discriminator(
            "point_type",
            ObjectPoint,
            PointPoint,
        )
    ),
]
"""Any point, discriminated on `point_type`."""

PointAdapter: TypeAdapter[Point] = TypeAdapter(Point)
"""Validator for one point, including from raw GeoJSON."""


class PointCollection(BaseModel):
    """The contents of `points.geojson`."""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Point]
