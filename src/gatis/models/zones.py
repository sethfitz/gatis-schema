"""GATIS zone models.

BOOTSTRAPPED by `gatis.codegen` from the pinned spec snapshot
(dotbts/BPA@ecc45ff8) on 2026-09-21.

Hand-edits are expected and are not overwritten: the bootstrap refuses to
rewrite an existing file without `--force`. Refine freely -- the published
spec cannot express half of what these models should say.
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
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    Tag,
    TypeAdapter,
    model_validator,
)

from gatis.annotations import (
    Tier,
)
from gatis.constraints import (
    SuggestedValues,
    drop_null_properties,
)
from gatis.models.enums import (
    TrafficCalmingType,
    ZoneStatus,
)
from gatis.scalars import GatisDate
from gatis.shared import (
    ReferenceId,
)


class ZoneBase(Identified, Feature):
    """Common base for every GATIS zone type."""

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
        GeometryTypeConstraint(GeometryType.POLYGON),
    ]
    # An explicit `null` property means absent. See `drop_null_properties`;
    # real GATIS data is overwhelmingly null-valued rather than sparse.
    _drop_nulls = model_validator(mode="before")(staticmethod(drop_null_properties))

    # Redeclared from `Feature`, where it is `Omitable[Id]`, to make it
    # mandatory. Same narrowing, and the same silencing, as Overture's own
    # `OvertureFeature`.
    id: Annotated[Id, Tier("required")] = Field(  # type: ignore[assignment]
        alias="zone_id",
        description="A unique identifier for the zone. [NOTE: We will fill in "
        "instructions here on how to generate IDs, and we will also provide a data "
        "validator that may be capable of validating and helping to fill in these "
        "IDs.]",
    )


class OpenZone(ZoneBase):
    """Indicates a zone where travelers may travel freely in a range of paths they
    choose.
    """

    zone_type: Annotated[Literal["open"], Tier("required")] = Field(
        description="Indicates the type of zone."
    )

    surface_material: Annotated[
        Omitable[
            Annotated[
                str,
                SuggestedValues(
                    "asphalt",
                    "concrete",
                    "gravel",
                    "grass",
                    "dirt",
                    "paved",
                    "unpaved",
                    "grass paver",
                    "paving stones",
                    "other",
                ),
            ]
        ],
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="Specifies the surface type. Select only one. Where the "
        "surface material changes, create a new zone. Recommended values: asphalt; "
        "concrete; gravel; grass; dirt; paved; unpaved; grass paver; paving "
        "stones; other."
    )

    facility_name: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Common or formal name for the zone. Can also include "
            "descriptions of a portion of a larger open zone (like a park or a plaza) "
            "if the zone is being segmented."
        )
    )

    status: Annotated[Omitable[ZoneStatus], Tier("optional")] = Field(
        description="Most recent operating status of the zone. Whether the "
        "infrastructure is open and available for use. If blank, the assumed value "
        "is 'open.'"
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should be "
        "an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum. Can add other attributes "
        "such as the beginning and ending milepost from a linear referencing "
        "system."
    )

    prohibited_uses: Annotated[
        Omitable[
            list[
                Annotated[
                    str,
                    SuggestedValues(
                        "walk",
                        "bike",
                        "ebike class 1",
                        "ebike class 2",
                        "ebike class 3",
                        "scooter",
                        "NEV",
                        "motor_vehicle",
                        "other",
                    ),
                ]
            ]
        ],
        Tier("optional"),
    ] = Field(
        description="Specifies which types of users are legally prohibited from "
        "using the facility, based on the laws, policy, or signage on a facility "
        "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
        "list form. Recommended values: walk; bike; ebike class 1; ebike class 2; "
        "ebike class 3; scooter; NEV; motor_vehicle; other."
    )

    allowed_uses: Annotated[
        Omitable[
            list[
                Annotated[
                    str,
                    SuggestedValues(
                        "walk",
                        "bike",
                        "ebike class 1",
                        "ebike class 2",
                        "ebike class 3",
                        "scooter",
                        "NEV",
                        "motor_vehicle",
                        "other",
                    ),
                ]
            ]
        ],
        Tier("optional"),
    ] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes. Recommended values: walk; "
        "bike; ebike class 1; ebike class 2; ebike class 3; scooter; NEV; "
        "motor_vehicle; other."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="Indicates when the facility was officially opened for use. If "
        "the facility has had a major remodeling where the structure, shape or "
        "another fundamental aspect was changed, the date of remodeling can be "
        "placed here. Report in RFC 3339 format containing day, month and year, or "
        "just month and year or year if day or month is not available."
    )


class TrafficCalmingZone(ZoneBase):
    """Used to identify where traffic calming features are located where these
    features are an area (versus a point).
    """

    zone_type: Annotated[Literal["traffic_calming"], Tier("required")] = Field(
        description="Indicates the type of zone."
    )

    surface_material: Annotated[
        Omitable[
            Annotated[
                str,
                SuggestedValues(
                    "asphalt",
                    "concrete",
                    "gravel",
                    "grass",
                    "dirt",
                    "paved",
                    "unpaved",
                    "grass paver",
                    "paving stones",
                    "other",
                ),
            ]
        ],
        Tier("optional"),
    ] = Field(
        description="Specifies the surface type. Select only one. Where the "
        "surface material changes, create a new zone. Recommended values: asphalt; "
        "concrete; gravel; grass; dirt; paved; unpaved; grass paver; paving "
        "stones; other."
    )

    status: Annotated[Omitable[ZoneStatus], Tier("optional")] = Field(
        description="Most recent operating status of the zone. Whether the "
        "infrastructure is open and available for use. If blank, the assumed value "
        "is 'open.'"
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should be "
        "an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum. Can add other attributes "
        "such as the beginning and ending milepost from a linear referencing "
        "system."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    date_built: Annotated[Omitable[GatisDate], Tier("recommended")] = Field(
        description="Indicates when the facility was officially opened for use. If "
        "the facility has had a major remodeling where the structure, shape or "
        "another fundamental aspect was changed, the date of remodeling can be "
        "placed here. Report in RFC 3339 format containing day, month and year, or "
        "just month and year or year if day or month is not available."
    )

    traffic_calming_type: Annotated[TrafficCalmingType, Tier("required")] = Field(
        description="The type of traffic calming measure that is present in a "
        "traffic_calming zone. Recommended values are from "
        "https://www.ite.org/technical-resources/traffic-calming/traffic-calming- "
        "measures/ and https://wiki.openstreetmap.org/wiki/Key:traffic_calming."
    )


Zone = Annotated[
    Annotated[OpenZone, Tag("open")]
    | Annotated[TrafficCalmingZone, Tag("traffic_calming")],
    Field(
        discriminator=Feature.field_discriminator(
            "zone_type",
            OpenZone,
            TrafficCalmingZone,
        )
    ),
]
"""Any zone, discriminated on `zone_type`."""

ZoneAdapter: TypeAdapter[Zone] = TypeAdapter(Zone)
"""Validator for one zone, including from raw GeoJSON."""


class ZoneCollection(BaseModel):
    """The contents of `zones.geojson`."""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Zone]
