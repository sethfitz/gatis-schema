"""GATIS edge models.

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
from gatis_schema.constraints import all_or_none
from gatis_schema.scalars import GatisDate, GatisDatetime, YesNo
from gatis_schema.shared import (
    GtfsReference,
    ReferenceId,
    SeasonalCondition,
)
from gatis_schema.models.enums import (
    AdaCompliantWith,
    AllowedUses,
    BikewayGradeSeparation,
    CrossVehicleTrafficControl,
    Directionality,
    FeaturePresence,
    PedProtection,
    PedTrafficControl,
    ProhibitedUses,
    SeparationPermeableCar,
    Status,
    StreetParking,
    SurfaceMaterial,
    TactileMarking,
    VehicleTrafficControl,
)


class RoadEdge(Feature):
    """A public road primarily intended for automobile travel."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[str, Tier("required")] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    edge_type: Annotated[Literal["road"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Directionality, Tier("required")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional")] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    curb_height: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="Indicates typical height of the curb along this segment of the road; can be used in deciding whether to route specific pedestrians off the sidewalk when there are obstructions or discontinuities. Measured and rounded to the nearest inch. Cannot be negative.")
    """Indicates typical height of the curb along this segment of the road; can be used in deciding whether to route specific pedestrians off the sidewalk when there are obstructions or discontinuities."""

    measured_length: Annotated[Omitable[Feet], Tier("optional")] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    traffic_volume: Annotated[Omitable[Aadt], Field(ge=0), Tier("optional", {4: "recommended"})] = Field(description="Measures the motor vehicle annual average daily traffic (AADT) for the edge. Reported with no more than two significant figures. Cannot be negative.")
    """Measures the motor vehicle annual average daily traffic (AADT) for the edge."""

    posted_speed_limit: Annotated[Omitable[Mph], Field(ge=0), Tier("optional", {4: "recommended"})] = Field(description="Used to indicate the posted speed limit. Measured in miles per hour. Cannot be negative. If used on bikeway, multi-use path, or trail, it's assumed that is the speed limit for non-motorized users.")
    """Used to indicate the posted speed limit."""

    mv_freeflow_speed: Annotated[Omitable[Mph], Field(ge=0), Tier("optional", {4: "recommended"})] = Field(description="Used to indicate the free-flow motor vehicle speed. Suggest using the 85th percentile. Measured in miles per hour. Cannot be negative.")
    """Used to indicate the free-flow motor vehicle speed."""

    thru_lanes: Annotated[Omitable[int32], Field(ge=0), Tier("optional", {4: "recommended"})] = Field(description="Describes the number of vehicle thru lanes on an edge. Does not include turn lanes or shoulders. Cannot be negative.")
    """Describes the number of vehicle thru lanes on an edge."""

    aux_lanes: Annotated[Omitable[int32], Field(ge=0), Tier("optional", {4: "recommended"})] = Field(description="Describes the number of temporary vehicle lanes like turn lanes. Cannot be negative.")
    """Describes the number of temporary vehicle lanes like turn lanes."""

    shoulder_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional", {4: "recommended"})] = Field(description="Width of the paved shoulder that can be used by pedestrians or cyclists. Measured in feet with one decimal point of precision. Cannot be negative.")
    """Width of the paved shoulder that can be used by pedestrians or cyclists."""

    roadway_centerline: Annotated[Omitable[YesNo], Tier("optional", {4: "recommended"})] = Field(description="Indicates if there is a painted road centerline. Might be a useful attribute to track for finding low-stress streets.")
    """Indicates if there is a painted road centerline."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    traffic_calming: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = Field(description="Used to identify traffic calming features along a road, shared-use path or crossing. Implies that feature is present alongside the entirety of the edge. The fields that the traffic calming element(s) affect should be modified (i.e., a road narrowing should reduce the road's width field from its typical value). Recommended values are from https://www.ite.org/pub/?id=2a60c136-b1c0-b231-0522-ccbd075cac84 and https://wiki.openstreetmap.org/wiki/Key:traffic_calming")
    """Used to identify traffic calming features along a road, shared-use path or crossing."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional")] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional")] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional")] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class SidewalkEdge(Feature):
    """A designated pedestrian path along the side of a roadway."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional", {2: "required"})] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["sidewalk"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional", {2: "recommended"})] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {2: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    pedestrian_lane: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="Indicates whether the stretch of sidewalk is a pedestrian lane, in which a section of the roadway surface is divided out for pedestrian use.")
    """Indicates whether the stretch of sidewalk is a pedestrian lane, in which a section of the roadway surface is divided out for pedestrian use."""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class FootpathEdge(Feature):
    """A dedicated pedestrian path that does not fall into another category."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["footpath"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional", {3: "recommended"})] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {3: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class CrossingEdge(Feature):
    """A location where infrastructure or a designation exists to help pedestrians and/or cyclists cross traffic lanes or other areas designated for traffic."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional", {2: "required"})] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["crossing"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional", {2: "recommended"})] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    vehicle_traffic_control: Annotated[Omitable[VehicleTrafficControl], Tier("optional", {3: "recommended"})] = Field(description="Describes how motor vehicle traffic that passes through the crossing space is controlled.")
    """Describes how motor vehicle traffic that passes through the crossing space is controlled."""

    cross_vehicle_traffic_control: Annotated[Omitable[list[CrossVehicleTrafficControl]], Tier("optional", {3: "recommended"})] = Field(description="Describes how motor vehicle traffic coming from cross streets is controlled. This traffic may or may not turn into the crossing space. For intersections with more than one cross street, list all of the control types present.")
    """Describes how motor vehicle traffic coming from cross streets is controlled."""

    ped_traffic_control: Annotated[Omitable[PedTrafficControl], Tier("optional", {3: "required"})] = Field(description="Describes the type of signal that controls the timing of pedestrian use of the crossing.")
    """Describes the type of signal that controls the timing of pedestrian use of the crossing."""

    ped_protection: Annotated[Omitable[list[PedProtection]], Tier("optional", {3: "recommended"})] = Field(description="Lists any features of traffic control that are intended to improve the protection of pedestrians while crossing.")
    """Lists any features of traffic control that are intended to improve the protection of pedestrians while crossing."""

    traffic_calming: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = Field(description="Used to identify traffic calming features along a road, shared-use path or crossing. Implies that feature is present alongside the entirety of the edge. The fields that the traffic calming element(s) affect should be modified (i.e., a road narrowing should reduce the road's width field from its typical value). Recommended values are from https://www.ite.org/pub/?id=2a60c136-b1c0-b231-0522-ccbd075cac84 and https://wiki.openstreetmap.org/wiki/Key:traffic_calming")
    """Used to identify traffic calming features along a road, shared-use path or crossing."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {2: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    rail_crossing: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(description="Used to indicate if a pedestrian or bicycle crossing is a railroad crossing. Use generic nodes to connect a rail crossing to the rest of the network. Note that there is also a value of 'rail tracks' for the other_issue attribute for edges. Use rail_crossing for track crossings that people walking, rolling or biking will need to cross, and that have active rail traffic. The 'rail tracks' value for other_issue can be used on other edge types or to identify remaining or unused tracks no longer traveled by trains.")
    """Used to indicate if a pedestrian or bicycle crossing is a railroad crossing."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class TrafficIslandEdge(Feature):
    """A median or other raised or protected area between traffic lanes on the road surface meant to provide a safe space for pedestrians to stop."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["traffic_island"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional", {3: "recommended"})] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {3: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class StepsEdge(Feature):
    """Fixed steps or stairs that appear along a pedestrian way."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["steps"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional")] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    wheel_channel: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Whether there is a wheel channel to allow for pushing a bicycle up the stairs.")
    """Whether there is a wheel channel to allow for pushing a bicycle up the stairs."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {3: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    step_count: Annotated[Omitable[int32], Field(gt=0), Tier("optional", {3: "recommended", 4: "required"})] = Field(description="The number of steps that make up this set of stairs. Must be greater than zero.")
    """The number of steps that make up this set of stairs."""

    handrail: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Whether a handrail is available on this set of stairs.")
    """Whether a handrail is available on this set of stairs."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class EscalatorEdge(Feature):
    """Escalators or any other construction of moving stairs meant to carry a pedestrian from one level of physical infrastructure to another."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["escalator"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {3: "recommended"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Directionality, Tier("required")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional")] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional")] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


class BikewayEdge(Feature):
    """A designated cycling lane or path that can be on, next to or away from a road."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[YesNo, Tier("required")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["bikeway"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Directionality, Tier("required")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional")] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    bikeway_type: Annotated[Literal["bikeway"], Tier("required")] = Field(description="Common name used for the bicycle facility type. Should align with the National Bikeway Network, NACTO, or AASHTO facility types.")
    """Common name used for the bicycle facility type."""

    bikeway_grade_separation: Annotated[Omitable[BikewayGradeSeparation], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="The vertical level of the bikeway with respect to the road. Not meant for bikeways that are not road associated.")
    """The vertical level of the bikeway with respect to the road."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional", {1: "recommended", 2: "required"})] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional", {1: "recommended", 2: "required"})] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional", {3: "recommended"})] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional", {2: "recommended"})] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    posted_speed_limit: Annotated[Omitable[Mph], Field(ge=0), Tier("optional")] = Field(description="Used to indicate the posted speed limit. Measured in miles per hour. Cannot be negative. If used on bikeway, multi-use path, or trail, it's assumed that is the speed limit for non-motorized users.")
    """Used to indicate the posted speed limit."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {2: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional")] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional")] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class MultiUsePathEdge(Feature):
    """A generic link that allows both bike and pedestrian travel."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[YesNo, Tier("required")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["multi_use_path"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional", {3: "recommended"})] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    posted_speed_limit: Annotated[Omitable[Mph], Field(ge=0), Tier("optional")] = Field(description="Used to indicate the posted speed limit. Measured in miles per hour. Cannot be negative. If used on bikeway, multi-use path, or trail, it's assumed that is the speed limit for non-motorized users.")
    """Used to indicate the posted speed limit."""

    mup_modal_delineation: Annotated[Omitable[YesNo], Tier("optional", {2: "recommended"})] = Field(description="Designates whether bikes and pedestrians have designated spaces on a multi-use/shared-use path, or whether all travelers use the same space.")
    """Designates whether bikes and pedestrians have designated spaces on a multi-use/shared-use path, or whether all travelers use the same space."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {2: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {2: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class TrailEdge(Feature):
    """Any kind of path or trail that allows bicycle or pedestrian travel that wouldn't fall into the multi_use_path designation."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    street_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs. In many cases, routing engines can fill in the closest street name for travelers to see. Use this field to specify the associated street explicitly or to correct an error within routing engines.")
    """Specifies the name of a road or the road associated with the edge, such as the street along which a sidewalk or cycleway runs."""

    facility_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(description="The common name for this edge, by which travelers might recognize it.")
    """The common name for this edge, by which travelers might recognize it."""

    edge_type: Annotated[Literal["trail"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(description="Indicates if the edge is or is on a bridge. Can be used for any bridge type, including road bridges and pedestrian bridges. Reccomend marking roads with bike lanes that are bridges.")
    """Indicates if the edge is or is on a bridge."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    official: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = Field(description="Indicates whether a trail has been officially designated by a government body or other recognized organization, with a string of the name of the recognizing body and/or a URL to the source/reference to the recognition for users to validate/verify/see additional information.")
    """Indicates whether a trail has been officially designated by a government body or other recognized organization, with a string of the name of the recognizing body and/or a URL to the source/reference to the recognition for users to validate/verify/see additional information."""

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a sidewalk or a crossing might be missing or where its presence is unknown. Conditionally required if no other identfiying fields supplied.")
    """Indicates whether the piece of infrastructure exists or is present."""

    measured_length: Annotated[Omitable[Feet], Tier("optional", {3: "recommended"})] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(description="The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer.")
    """The materials used to separate the cycleway or footpath from motor vehicle traffic -- for example, as part of a buffer."""

    separation_permeable_car: Annotated[Omitable[SeparationPermeableCar], Tier("optional")] = Field(description="Can a vehicle easily access this edge? Primarily intended for bikeways but could be used for pedestrian facilities.")
    """Can a vehicle easily access this edge?"""

    buffer_width: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """Distance between the edge of the motor vehicle travel lane and the bike lane or sidewalk."""

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(description="Field intended to indicate orientation of street parking in relation to a bike facility. Floating street parking is also referred to as parking protected.")
    """Field intended to indicate orientation of street parking in relation to a bike facility."""

    street_parking_buffer: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(description="The space between a bicycle facility and the street parking. Measured in feet and rounded to the nearest half foot. Cannot be negative.")
    """The space between a bicycle facility and the street parking."""

    posted_speed_limit: Annotated[Omitable[Mph], Field(ge=0), Tier("optional")] = Field(description="Used to indicate the posted speed limit. Measured in miles per hour. Cannot be negative. If used on bikeway, multi-use path, or trail, it's assumed that is the speed limit for non-motorized users.")
    """Used to indicate the posted speed limit."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {2: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional")] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional")] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    visual_markings: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="The way the crossing is marked within the roadway space. “Standard” means two solid parallel lines that indicate the outline, “dashed lines” means two dashed parallel lines that indicate the outline, “zebra” means regularly spaced diagonal bars along its length, “continental” means regularly spaced horizontal bars along its length, and “ladder” means standard plus either zebra or continental.")
    """The way the crossing is marked within the roadway space."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


@all_or_none("ada_compliance_date", "ada_compliant_with")
class RampEdge(Feature):
    """Indicates any type of ramp, where the footpath is built to deliberately slope up or down to improve access."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    edge_type: Annotated[Literal["ramp"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="Generalized width of the edge that best characterizes the width across its length. Measured in inches and rounded to the nearest inch. Cannot be negative. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")
    """Generalized width of the edge that best characterizes the width across its length."""

    width_min_passable: Annotated[Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The passable width of the edge at the point where it is narrowest. Measured in inches and rounded to the nearest inch. Cannot be negative.")
    """The passable width of the edge at the point where it is narrowest."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the segment. Whether the infrastructure is open and available for use. Default is 'open'")
    """Most recent operating status of the segment."""

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="Indicates when the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """Indicates when the facility was officially opened for use."""

    check_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")
    """The date that this infrastructure was last inspected."""

    measured_length: Annotated[Omitable[Feet], Tier("optional")] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(description="Indicates whether the segment is commonly affected by seasonal issues. Use this field for recurring (ex. yearly flooding) and not one-time (ex. single flood) events. Include both the seasonal concern and the season when it occurs as a JSON String.")
    """Indicates whether the segment is commonly affected by seasonal issues."""

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional", {2: "required"})] = Field(description="Specifies the material used for the surface of the segment as of the inspection in 'check_date'")
    """Specifies the material used for the surface of the segment as of the inspection in 'check_date'"""

    surface_issue: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other")
    """yes, no, cracking, scaling, spalling, uneven, frequent water pooling, heaving, missing bricks/stones, potholes/holes, slickness, detectable warning surface damage, longitudinal cracks and seams, other"""

    incline: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="The running slope of the full segment. Assume the given incline is in the forward direction of the edge, regardless of edge directionality. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The running slope of the full segment."""

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at most points along its path. Cross slope is never reported in negative numbers. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at most points along its path."""

    cross_slope_max: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})] = Field(description="The cross slope of the edge at the point along its path where there is the greatest slope. Report as percentage of the slope, with two decimal points of precision. Cannot be negative.")
    """The cross slope of the edge at the point along its path where there is the greatest slope."""

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.. This field is conditionally required if 'ada_compliant_with' is filled out.")
    """Indicates the date when ADA compliance was assessed."""

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")
    """If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment."""

    impediment: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing along this edge. Mark an edge with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")
    """Identifies the presence of an object that may pose a challenge for travelers passing along this edge."""

    handrail: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Whether a handrail is available on this set of stairs.")
    """Whether a handrail is available on this set of stairs."""

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(description="Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes. It is recommended to segment the edge so that this field is only equal to “yes” for the segment where the detectable warning appears. Do not use this field for tactile markings on curb ramps; instead, use the detectable_warning field for curb ramps.")
    """Indicates when tactile guidestrips or other markings are present to help identify the edge of a crosswalk or traffic island, the beginning or end of steps, or the presence of other infrastructure nearby, such as bike lanes."""


class VirtualLinkEdge(Feature):
    """Links added for topology, connectivity, or crossing reasons by the analyst."""

    geometry: Annotated[
        Geometry,
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]

    edge_id: Annotated[Id, Tier("required")] = Field(description="A unique identifier for the edge. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]")
    """A unique identifier for the edge."""

    road_associated: Annotated[YesNo, Tier("required")] = Field(description="Specifies if the edge is adjacent or associated to a road.")
    """Specifies if the edge is adjacent or associated to a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")
    """Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.)."""

    edge_type: Annotated[Literal["virtual_link"], Tier("required")] = Field(description="Identifies the edge type. Also used for assigning attributes that need to be filled in.")
    """Identifies the edge type."""

    from_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge begins. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge begins."""

    to_node: Annotated[Omitable[Id], Tier("optional", {2: "required"})] = Field(description="This field is used to identify the node where an edge ends. This information is needed for routing. Value needs to be from the nodes table in the node ID field.")
    """This field is used to identify the node where an edge ends."""

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(description="Specifies the directionality of the edge. If the edge is bidirectional, choose “both.” Used to help identify when bicycle infrastructure allows traffic in both directions. If left blank, then assumes 'both'.")
    """Specifies the directionality of the edge."""

    width_tolerance: Annotated[Omitable[Inches], Tier("optional")] = Field(description="Used to specify the tolerance of the width measurement in inches. Everything along the edge should be within +/- of this width.")
    """Used to specify the tolerance of the width measurement in inches."""

    measured_length: Annotated[Omitable[Feet], Tier("optional")] = Field(description="The measured length of the edge in feet. Note that geospatial data also contains a length attribute by default that may be useful in some cases. Measuring the traversable length of the segment is preferable.")
    """The measured length of the edge in feet."""

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = Field(description="Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex. “E-bikes prohibited on this trail”). Can provide one or multiple in list form.")
    """Specifies which types of users are legally prohibited from using the facility, based on the laws, policy, or signage on a facility (ex."""

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(description="Specifies exceptions to the usually prohibited users. Intended for designating whether bikes are allowed to use sidewalks, footpaths, and crossings for routing purposes.")
    """Specifies exceptions to the usually prohibited users."""


Edge = Annotated[
    Annotated[RoadEdge, Tag("road")]
    | Annotated[SidewalkEdge, Tag("sidewalk")]
    | Annotated[FootpathEdge, Tag("footpath")]
    | Annotated[CrossingEdge, Tag("crossing")]
    | Annotated[TrafficIslandEdge, Tag("traffic_island")]
    | Annotated[StepsEdge, Tag("steps")]
    | Annotated[EscalatorEdge, Tag("escalator")]
    | Annotated[BikewayEdge, Tag("bikeway")]
    | Annotated[MultiUsePathEdge, Tag("multi_use_path")]
    | Annotated[TrailEdge, Tag("trail")]
    | Annotated[RampEdge, Tag("ramp")]
    | Annotated[VirtualLinkEdge, Tag("virtual_link")],
    Field(
        discriminator=Feature.field_discriminator(
            "edge_type",
            RoadEdge,
            SidewalkEdge,
            FootpathEdge,
            CrossingEdge,
            TrafficIslandEdge,
            StepsEdge,
            EscalatorEdge,
            BikewayEdge,
            MultiUsePathEdge,
            TrailEdge,
            RampEdge,
            VirtualLinkEdge,
        )
    ),
]
"""Any edge, discriminated on `edge_type`."""

EdgeAdapter: TypeAdapter[Edge] = TypeAdapter(Edge)
"""Validator for one edge, including from raw GeoJSON."""


class EdgeCollection(BaseModel):
    """The contents of `edges.geojson`."""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Edge]
