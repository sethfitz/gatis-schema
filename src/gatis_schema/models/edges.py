"""GATIS edge models.

BOOTSTRAPPED by `gatis_schema.codegen` from the pinned spec snapshot
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
from overture.schema.system.numeric import float64, int32
from overture.schema.system.optionality import Omitable
from overture.schema.system.ref import (
    Id,
    Identified,
    Reference,
    Relationship,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    Tag,
    TypeAdapter,
    model_validator,
)

from gatis_schema.annotations import (
    Aadt,
    Feet,
    Inches,
    InchesFloat,
    Mph,
    Tier,
)
from gatis_schema.constraints import all_or_none, drop_null_properties
from gatis_schema.models.enums import (
    AllowedUses,
    BikewayGradeSeparation,
    CrossVehicleTrafficControl,
    DetectableWarning,
    Directionality,
    EdgeAdaCompliantWith,
    EdgePresence,
    EdgeStatus,
    PedProtection,
    PedTrafficControl,
    ProhibitedUses,
    SeparationPermeableCar,
    StreetParking,
    SurfaceMaterial,
    TactileMarking,
    VehicleTrafficControl,
)
from gatis_schema.models.nodes import NodeBase
from gatis_schema.scalars import GatisDate, YesNo
from gatis_schema.shared import (
    ReferenceId,
    SeasonalCondition,
)


class EdgeBase(Identified, Feature):
    """Common base for every GATIS edge type."""

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
        GeometryTypeConstraint(GeometryType.LINE_STRING),
    ]
    # An explicit `null` property means absent. See `drop_null_properties`;
    # real GATIS data is overwhelmingly null-valued rather than sparse.
    _drop_nulls = model_validator(mode="before")(staticmethod(drop_null_properties))

    # Redeclared from `Feature`, where it is `Omitable[Id]`, to make it
    # mandatory. Same narrowing, and the same silencing, as Overture's own
    # `OvertureFeature`.
    id: Annotated[Id, Tier("required")] = Field(  # type: ignore[assignment]
        alias="edge_id",
        description="A unique identifier for the edge. [NOTE: We will fill in "
        "instructions here on how to generate IDs, and we will also provide a data "
        "validator that may be capable of validating and helping to fill in these "
        "IDs.]",
    )


class RoadEdge(EdgeBase):
    """A public road primarily intended for automobile travel."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[str, Tier("required")] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    edge_type: Annotated[Literal["road"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Directionality, Tier("required")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[
        Omitable[YesNo], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[Omitable[EdgeStatus], Tier("optional")] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="When the facility was officially opened for use. date_built "
        "represents the original opening date. Use the Events extension to record "
        "details about construction history, remodeling, removal and other "
        "physical changes. Report in RFC 3339 format containing day, month and "
        "year, or just month and year or year if day or month is not available."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    curb_height_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates typical height of the curb along this segment of "
        "the road; can be used in deciding whether to route specific pedestrians "
        "off the sidewalk when there are obstructions or discontinuities. Measured "
        "and rounded to the nearest inch. Cannot be negative."
    )

    measured_length_ft: Annotated[Omitable[Feet], Tier("optional")] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    bikeway_type: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Common name used for the bicycle facility type. Should align "
        "with the National Bikeway Network, NACTO, or AASHTO facility types. "
        "Recommended values: Bike Lane; Buffered Bike Lane; Separated Bike Lane; "
        "Counter-Flow Bike Lane; Bicycle Boulevard; Paved Shoulder; Shared Lane."
    )

    traffic_volume: Annotated[
        Omitable[Aadt], Field(ge=0), Tier("optional", {4: "recommended"})
    ] = Field(
        description="Measures the motor vehicle annual average daily traffic "
        "(AADT) for the edge. Ideally rounded to the nearest hundred for low- "
        "volume roads and the nearest thousand for high-volume roads. Cannot be "
        "negative."
    )

    posted_speed_limit_mph: Annotated[
        Omitable[Mph], Field(ge=0), Tier("optional", {4: "recommended"})
    ] = Field(
        description="Used to indicate the posted speed limit. Measured in miles "
        "per hour. Cannot be negative. If used on bikeway, multi-use path, or "
        "trail, it's assumed that is the speed limit for non-motorized users."
    )

    mv_freeflow_speed_mph: Annotated[
        Omitable[Mph], Field(ge=0), Tier("optional", {4: "recommended"})
    ] = Field(
        description="Used to indicate the free-flow motor vehicle speed. Suggest "
        "using the 85th percentile. Measured in miles per hour. Cannot be "
        "negative."
    )

    thru_lanes: Annotated[
        Omitable[int32], Field(ge=0), Tier("optional", {4: "recommended"})
    ] = Field(
        description="Describes the number of vehicle thru lanes on an edge. Does "
        "not include turn lanes or shoulders. Cannot be negative."
    )

    aux_lanes: Annotated[
        Omitable[int32], Field(ge=0), Tier("optional", {4: "recommended"})
    ] = Field(
        description="Describes the number of temporary vehicle lanes like turn "
        "lanes. Cannot be negative."
    )

    shoulder_width_in: Annotated[
        Omitable[InchesFloat], Field(ge=0), Tier("optional", {4: "recommended"})
    ] = Field(
        description="Width of the paved shoulder or shoulders along the edge that "
        "can be used by pedestrians or cyclists. Measured in inches. Cannot be "
        "negative. Left/right/both tags may be used, and the directionality is "
        "determined based on how the edge geometry was drawn. See Directionality "
        "and Left/Right/Both Tags in the GATIS Playbook for further explanation."
    )

    markings: Annotated[Omitable[list[str]], Tier("optional", {4: "recommended"})] = (
        Field(
            description="Markings that delineate or mark the area of the road or other "
            "edge for bicyclists or pedestrians, or for motor vehicle driver awareness "
            "of bike and pedestrian infrastructure or space. Left/right/both tagging "
            "may be used. See the Playbook for more information on this tagging. "
            "Recommended values: green_paint; sharrows; edge_lines; centerline; "
            "ped_lane; bike_lane."
        )
    )

    roadway_centerline: Annotated[
        Omitable[YesNo], Tier("optional", {4: "recommended"})
    ] = Field(
        description="Indicates if there is a painted road centerline. This "
        "attribute is sometimes used to help identify low-stress streets. "
        "Recommended values: yes; no."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    traffic_calming: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Used to identify features along a road or crossing meant to "
        "slow the speed of motor vehicle traffic when that feature is present "
        "alongside the entirety or majority of the edge. Most traffic calming "
        "features are better mapped as zones or points, due to their shape and "
        "placement. Please see the traffic_calming zone and point types to map "
        "other types of traffic calming. The attributes that the traffic calming "
        "element(s) affect should be modified -- for example, a road narrowing "
        "should reduce the road's width attribute to match the narrowed width. "
        "Recommended values are from https://www.ite.org/technical- "
        "resources/traffic-calming/traffic-calming-measures/ and "
        "https://wiki.openstreetmap.org/wiki/Key:traffic_calming. Recommended "
        "values: narrowed road; closure; lateral shift; raised crossing."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional")] = Field(
        description="Specifies the material used for the surface of the segment."
    )

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {2: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[Omitable[float64], Field(ge=0), Tier("optional")] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[Omitable[float64], Field(ge=0), Tier("optional")] = (
        Field(
            description="The cross slope of the edge at the point along its path where "
            "there is the greatest cross slope. Report as a percentage with two "
            "decimal points of precision. Cannot be negative."
        )
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The lifecycle stage of this piece of infrastructure, as of "
        "the last_inspection_date. Recommended values: new; operational; nearing "
        "replacement; replacement planned or in planning."
    )

    maintenance_schedule: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class SidewalkEdge(EdgeBase):
    """A designated pedestrian path along the side of a roadway."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional", {2: "required"})] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["sidewalk"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {2: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    markings: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Markings that delineate or mark the area of the road or other "
        "edge for bicyclists or pedestrians, or for motor vehicle driver awareness "
        "of bike and pedestrian infrastructure or space. Left/right/both tagging "
        "may be used. See the Playbook for more information on this tagging. "
        "Recommended values: green_paint; sharrows; edge_lines; centerline; "
        "ped_lane; bike_lane."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {2: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    pedestrian_lane: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = (
        Field(
            description="Indicates whether the stretch of sidewalk is a pedestrian "
            "lane, in which a section of the roadway surface is divided out for "
            "pedestrian use."
        )
    )

    incline: Annotated[Omitable[float64], Tier("optional", {2: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {2: "required"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at the point along its path where "
        "there is the greatest cross slope. Report as a percentage with two "
        "decimal points of precision. Cannot be negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {2: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {2: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[
        Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class CurbRampToplandingEdge(EdgeBase):
    """An edge that represents the transition area from sidewalk space to a curb
    ramp (curb_ramp_runslope).
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    curb_ramp_system_id: Annotated[str, Tier("required")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["curb_ramp_toplanding"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {4: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[
        Omitable[float64], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64],
        Field(ge=0),
        Tier("optional", {3: "recommended", 4: "required"}),
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    handrail: Annotated[
        Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Whether a handrail is available on this set of stairs. "
        "Recommended values: yes; no."
    )

    tactile_marking: Annotated[
        Omitable[TactileMarking], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    detectable_warning: Annotated[
        Omitable[DetectableWarning], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Describes whether tactile paving is present, and whether or "
        "not it has a constrasting color (which should meet ADA guidelines for the "
        "amount of contrast)."
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class CurbRampRunslopeEdge(EdgeBase):
    """An edge that represents the sloped surface (curb ramp) that aids a user in
    transitioning from the sidewalk space down to the street level for crossing,
    where a curb cut exists.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    curb_ramp_system_id: Annotated[str, Tier("required")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["curb_ramp_runslope"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {4: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[
        Omitable[float64], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64],
        Field(ge=0),
        Tier("optional", {3: "recommended", 4: "required"}),
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    handrail: Annotated[
        Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Whether a handrail is available on this set of stairs. "
        "Recommended values: yes; no."
    )

    tactile_marking: Annotated[
        Omitable[TactileMarking], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    detectable_warning: Annotated[
        Omitable[DetectableWarning], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Describes whether tactile paving is present, and whether or "
        "not it has a constrasting color (which should meet ADA guidelines for the "
        "amount of contrast)."
    )

    ramp_type: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="Indicates the orientation of the ramp in relation to the "
        "pedestrian direction of travel at the location. Where a double curb ramp "
        "exists, map each ramp as a separate curb_ramp_runslope. Recommended "
        "values: diagonal; directional; parallel; perpendicular; built-up; "
        "combination; transition; cut-through (median/island ramp); unknown."
    )

    ramp_length: Annotated[Omitable[float64], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Indicates the length of the incline portion of the curb ramp."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class FootwayEdge(EdgeBase):
    """A dedicated pedestrian path/route that does not fall into another category."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["footway"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    official: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Indicates whether a trail has been officially designated by a "
            "government body or other recognized organization, with a string of the "
            "name of the recognizing body and/or a URL to the source/reference to the "
            "recognition for users to verify and see additional information. If not an "
            "official trail, the value should be 'no.' If left blank, the trail is "
            "assumed official and managed by a local government agency."
        )
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    markings: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Markings that delineate or mark the area of the road or other "
        "edge for bicyclists or pedestrians, or for motor vehicle driver awareness "
        "of bike and pedestrian infrastructure or space. Left/right/both tagging "
        "may be used. See the Playbook for more information on this tagging. "
        "Recommended values: green_paint; sharrows; edge_lines; centerline; "
        "ped_lane; bike_lane."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {3: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {3: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "required"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at the point along its path where "
        "there is the greatest cross slope. Report as a percentage with two "
        "decimal points of precision. Cannot be negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {2: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {2: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[
        Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The lifecycle stage of this piece of infrastructure, as of "
        "the last_inspection_date. Recommended values: new; operational; nearing "
        "replacement; replacement planned or in planning."
    )

    maintenance_schedule: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class CrossingEdge(EdgeBase):
    """A location where infrastructure or a designation exists to help pedestrians
    and/or cyclists cross motor vehicle traffic lanes or other areas designated
    for traffic.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional", {2: "required"})] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["crossing"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {2: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    vehicle_traffic_control: Annotated[
        Omitable[VehicleTrafficControl], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Describes how motor vehicle traffic that passes through the "
        "crossing edge is controlled. In an intersection where two roads cross, "
        "the road that is perpendicular to the crossing edge would be described "
        "using this attribute. Use cross_vehicle_traffic_control to describe the "
        "road that is parallel to the crossing edge."
    )

    cross_vehicle_traffic_control: Annotated[
        Omitable[list[CrossVehicleTrafficControl]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Describes how motor vehicle traffic coming from cross streets "
        "is controlled. This traffic may or may not turn into the crossing space. "
        "In an intersection where two roads cross, the road that is parallel to "
        "the crossing edge would be described using this attribute. Use "
        "vehicle_traffic_control to describe the road that is perpendicular to the "
        "crossing edge. For intersections with more than one cross street, list "
        "all of the control types present for all of the cross streets in this "
        "attribute."
    )

    ped_traffic_control: Annotated[
        Omitable[PedTrafficControl], Tier("optional", {3: "required"})
    ] = Field(
        description="Describes the type of signal that controls pedestrian use of "
        "the crossing. If left blank, 'unknown' is assumed."
    )

    ped_protection: Annotated[
        Omitable[list[PedProtection]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Any features of traffic control that are intended to improve "
        "the protection of pedestrians while crossing. List all that are present. "
        "If left blank, 'unknown' is assumed."
    )

    traffic_calming: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Used to identify features along a road or crossing meant to "
        "slow the speed of motor vehicle traffic when that feature is present "
        "alongside the entirety or majority of the edge. Most traffic calming "
        "features are better mapped as zones or points, due to their shape and "
        "placement. Please see the traffic_calming zone and point types to map "
        "other types of traffic calming. The attributes that the traffic calming "
        "element(s) affect should be modified -- for example, a road narrowing "
        "should reduce the road's width attribute to match the narrowed width. "
        "Recommended values are from https://www.ite.org/technical- "
        "resources/traffic-calming/traffic-calming-measures/ and "
        "https://wiki.openstreetmap.org/wiki/Key:traffic_calming. Recommended "
        "values: narrowed road; closure; lateral shift; raised crossing."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {2: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {2: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {2: "required"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at the point along its path where "
        "there is the greatest cross slope. Report as a percentage with two "
        "decimal points of precision. Cannot be negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {2: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {2: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    rail_crossing: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Used to indicate if a pedestrian or bicycle crossing is a "
            "railroad crossing. Use generic nodes to connect a rail crossing to the "
            "rest of the network. Note that there is also a value of 'rail tracks' for "
            "the other_issue attribute for edges. Use this attribute for track "
            "crossings that people walking, rolling or biking will need to cross, and "
            "that have active rail traffic. The 'rail tracks' value for other_issue "
            "can be used on other edge types or to identify remaining or unused tracks "
            "no longer traveled by trains. Recommended values: yes; no."
        )
    )

    visual_markings: Annotated[
        Omitable[str], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="The way the crossing is marked within the roadway space. See "
        "the Manual of Uniform Traffic Control Devices "
        "(https://mutcd.fhwa.dot.gov/pdfs/11th_Edition/part3.pdf) Chapter 3C and "
        "Figure 3C-1 for more information. This attribute can accept a list of "
        "values. Include all that apply. Recommended values: marked - type "
        "unknown; unmarked; transverse; longitudinal bar; ladder; bar pair; high "
        "visibility; other."
    )

    tactile_marking: Annotated[
        Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class RampEdge(EdgeBase):
    """Indicates any type of ramp, other than a curb ramp, where the footway is
    built to deliberately slope up or down to improve access.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    edge_type: Annotated[Literal["ramp"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="When the facility was officially opened for use. date_built "
        "represents the original opening date. Use the Events extension to record "
        "details about construction history, remodeling, removal and other "
        "physical changes. Report in RFC 3339 format containing day, month and "
        "year, or just month and year or year if day or month is not available."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    measured_length_ft: Annotated[Omitable[Feet], Tier("optional")] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {2: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {3: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at the point along its path where "
        "there is the greatest cross slope. Report as a percentage with two "
        "decimal points of precision. Cannot be negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    handrail: Annotated[
        Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Whether a handrail is available on this set of stairs. "
        "Recommended values: yes; no."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class TrafficIslandEdge(EdgeBase):
    """A median or other raised or protected area between traffic lanes on the
    road surface, sometimes meant to provide a safe space for pedestrians to stop.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["traffic_island"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    markings: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Markings that delineate or mark the area of the road or other "
        "edge for bicyclists or pedestrians, or for motor vehicle driver awareness "
        "of bike and pedestrian infrastructure or space. Left/right/both tagging "
        "may be used. See the Playbook for more information on this tagging. "
        "Recommended values: green_paint; sharrows; edge_lines; centerline; "
        "ped_lane; bike_lane."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {3: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {3: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at the point along its path where "
        "there is the greatest cross slope. Report as a percentage with two "
        "decimal points of precision. Cannot be negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[
        Omitable[TactileMarking], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class StepsEdge(EdgeBase):
    """Fixed steps or stairs that appear along a pedestrian way."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    edge_type: Annotated[Literal["steps"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="When the facility was officially opened for use. date_built "
        "represents the original opening date. Use the Events extension to record "
        "details about construction history, remodeling, removal and other "
        "physical changes. Report in RFC 3339 format containing day, month and "
        "year, or just month and year or year if day or month is not available."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[Omitable[Feet], Tier("optional")] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    wheel_channel: Annotated[
        Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Whether there is a wheel channel to allow for pushing a "
        "bicycle up the stairs. Recommended values: yes; no."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {3: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    step_count: Annotated[
        Omitable[int32],
        Field(gt=0),
        Tier("optional", {3: "recommended", 4: "required"}),
    ] = Field(
        description="The number of steps that make up this set of stairs. Must be "
        "greater than zero."
    )

    handrail: Annotated[
        Omitable[YesNo], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Whether a handrail is available on this set of stairs. "
        "Recommended values: yes; no."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class ElevatorEdge(EdgeBase):
    """Elevators, funiculars, or other car- or enclosure-based constructions meant
    to vertically carry a pedestrian from one level of physical infrastructure to
    another.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    edge_type: Annotated[Literal["elevator"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Directionality, Tier("required")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="When the facility was officially opened for use. date_built "
        "represents the original opening date. Use the Events extension to record "
        "details about construction history, remodeling, removal and other "
        "physical changes. Report in RFC 3339 format containing day, month and "
        "year, or just month and year or year if day or month is not available."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[Omitable[Feet], Tier("optional")] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional")] = Field(
        description="Specifies the material used for the surface of the segment."
    )

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class EscalatorEdge(EdgeBase):
    """Escalators or any other construction of moving stairs meant to carry a
    pedestrian from one level of physical infrastructure to another.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The common or official name for this edge, by which travelers "
        "might recognize it. The same facility_name may be used for multiple "
        "edges, such as segments that make up a longer distance multi-use path "
        "with a name (ex. 'Atlanta BeltLine')."
    )

    edge_type: Annotated[Literal["escalator"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {3: "recommended"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Directionality, Tier("required")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[Omitable[Inches], Field(ge=0), Tier("optional")] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional")
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="When the facility was officially opened for use. date_built "
        "represents the original opening date. Use the Events extension to record "
        "details about construction history, remodeling, removal and other "
        "physical changes. Report in RFC 3339 format containing day, month and "
        "year, or just month and year or year if day or month is not available."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[Omitable[Feet], Tier("optional")] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[Omitable[SurfaceMaterial], Tier("optional")] = Field(
        description="Specifies the material used for the surface of the segment."
    )

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class BikewayEdge(EdgeBase):
    """A designated cycling lane or path that can be on, next to or away from a road."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = (
        Field(
            description="The common or official name for this edge, by which travelers "
            "might recognize it. The same facility_name may be used for multiple "
            "edges, such as segments that make up a longer distance multi-use path "
            "with a name (ex. 'Atlanta BeltLine')."
        )
    )

    edge_type: Annotated[Literal["bikeway"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Directionality, Tier("required")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[Omitable[Feet], Tier("optional")] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    bikeway_type: Annotated[str, Tier("required")] = Field(
        description="Common name used for the bicycle facility type. Should align "
        "with the National Bikeway Network, NACTO, or AASHTO facility types. "
        "Recommended values: Bike Lane; Buffered Bike Lane; Separated Bike Lane; "
        "Counter-Flow Bike Lane; Bicycle Boulevard; Paved Shoulder; Shared Lane."
    )

    bikeway_grade_separation: Annotated[
        Omitable[BikewayGradeSeparation],
        Tier("optional", {2: "recommended", 3: "required"}),
    ] = Field(
        description="The vertical level of the bikeway with respect to the road. "
        "Not meant for bikeways that are not road associated."
    )

    separation_elements: Annotated[
        Omitable[list[str]], Tier("recommended", {2: "required"})
    ] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("recommended", {2: "required"})
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[
        Omitable[StreetParking], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional", {2: "recommended"})
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    posted_speed_limit_mph: Annotated[Omitable[Mph], Field(ge=0), Tier("optional")] = (
        Field(
            description="Used to indicate the posted speed limit. Measured in miles "
            "per hour. Cannot be negative. If used on bikeway, multi-use path, or "
            "trail, it's assumed that is the speed limit for non-motorized users."
        )
    )

    markings: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Markings that delineate or mark the area of the road or other "
        "edge for bicyclists or pedestrians, or for motor vehicle driver awareness "
        "of bike and pedestrian infrastructure or space. Left/right/both tagging "
        "may be used. See the Playbook for more information on this tagging. "
        "Recommended values: green_paint; sharrows; edge_lines; centerline; "
        "ped_lane; bike_lane."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {2: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {2: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[Omitable[float64], Field(ge=0), Tier("optional")] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[Omitable[float64], Field(ge=0), Tier("optional")] = (
        Field(
            description="The cross slope of the edge at the point along its path where "
            "there is the greatest cross slope. Report as a percentage with two "
            "decimal points of precision. Cannot be negative."
        )
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class MultiUsePathEdge(EdgeBase):
    """A path that allows more than one use (i.e."""

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = (
        Field(
            description="The common or official name for this edge, by which travelers "
            "might recognize it. The same facility_name may be used for multiple "
            "edges, such as segments that make up a longer distance multi-use path "
            "with a name (ex. 'Atlanta BeltLine')."
        )
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["multi_use_path"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {2: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    posted_speed_limit_mph: Annotated[Omitable[Mph], Field(ge=0), Tier("optional")] = (
        Field(
            description="Used to indicate the posted speed limit. Measured in miles "
            "per hour. Cannot be negative. If used on bikeway, multi-use path, or "
            "trail, it's assumed that is the speed limit for non-motorized users."
        )
    )

    markings: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Markings that delineate or mark the area of the road or other "
        "edge for bicyclists or pedestrians, or for motor vehicle driver awareness "
        "of bike and pedestrian infrastructure or space. Left/right/both tagging "
        "may be used. See the Playbook for more information on this tagging. "
        "Recommended values: green_paint; sharrows; edge_lines; centerline; "
        "ped_lane; bike_lane."
    )

    mup_modal_delineation: Annotated[
        Omitable[YesNo], Tier("optional", {2: "recommended"})
    ] = Field(
        description="Designates whether bicyclists and pedestrians have separate "
        "designated spaces on a multi-use path, or whether all travelers use the "
        "same space. Recommended values: yes; no."
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {2: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional", {2: "required"})] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at the point along its path where "
        "there is the greatest cross slope. Report as a percentage with two "
        "decimal points of precision. Cannot be negative."
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class TrailEdge(EdgeBase):
    """Any kind of path or trail that allows bicycle and/or pedestrian travel that
    does not fall into the multi_use_path designation.
    """

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other data sources such "
        "as OSM, Overture, ARNOLD, HMPS, TIGER, Census road network, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    street_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = Field(
        description="Specifies the name of a road associated with the edge, such "
        "as the street along which a sidewalk or cycleway runs. In many cases, "
        "routing engines can fill in the closest street name for travelers to see. "
        "Use this attribute to specify the associated street explicitly or to "
        "correct an error within routing engines."
    )

    facility_name: Annotated[Omitable[str], Tier("optional", {2: "recommended"})] = (
        Field(
            description="The common or official name for this edge, by which travelers "
            "might recognize it. The same facility_name may be used for multiple "
            "edges, such as segments that make up a longer distance multi-use path "
            "with a name (ex. 'Atlanta BeltLine')."
        )
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and edges that are involved "
        "in the same 'curb ramp system,' which is the network of elements that "
        "sidewalk users use to transition from a sidewalk to a crossing. This may "
        "include sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and "
        "crosswalk edges, as well as sidewalk_to_ramp, bottom_of_ramp or generic "
        "nodes."
    )

    edge_type: Annotated[Literal["trail"], Tier("required")] = Field(
        description="Indicates the type of edge."
    )

    from_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="starts_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "begins, using the node_id attribute on the nodes table. This information "
        "is needed for routing via metadata but is optional for data designed to "
        "be routed via fully connected geospatial data."
    )

    to_node: Annotated[
        Omitable[Id],
        Reference(Relationship.ASSOCIATION, NodeBase, role="ends_at"),
        Tier("optional", {2: "required"}),
    ] = Field(
        description="This attribute is used to identify the node where an edge "
        "ends, using the node_id attribute on the nodes table. This information is "
        "needed for routing via metadata but is optional for data designed to be "
        "routed via fully connected geospatial data."
    )

    directionality: Annotated[Omitable[Directionality], Tier("optional")] = Field(
        description="Specifies the directionality of the edge. If the edge is "
        "bidirectional, choose “both.” Used to help identify when bicycle "
        "infrastructure allows traffic in both directions. If left blank, 'both' "
        "is assumed. See the Playbook for a fuller explanation of the "
        "directionality of geometric linework and how different GATIS attributes "
        "relate."
    )

    width_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "required"})
    ] = Field(
        description="Average or typical width of the edge. Measured in inches and "
        "rounded to the nearest inch. Cannot be negative. Use width_tolerance_in "
        "to describe the variance in the width along this edge. If the width "
        "changes substantially, the edge should be segmented into multiple edges "
        "with differing width_in values."
    )

    height_max_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable height of the edge at the point where it is the "
        "shortest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_min_passable_in: Annotated[
        Omitable[Inches], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The passable width of the edge at the point where it is "
        "narrowest. Measured in inches and rounded to the nearest inch. Cannot be "
        "negative."
    )

    width_tolerance_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="Used to specify the tolerance of the width measurement in "
        "inches. Everything along the edge should be within +/- of this width."
    )

    bridge: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates if the edge is or is on a bridge. Can be used for "
        "any bridge type, including road bridges (with or without bike lanes) and "
        "pedestrian and bike bridges. Recommended values: yes; no."
    )

    underpass_tunnel: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents an underground path, such "
        "as a tunnel or an underpass. Recommended values: yes; no."
    )

    overpass_skywalk: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Indicates that the edge represents a skywalk, pedestrian or "
        "bicycle overpass, or other elevated infrastructure that is not a bridge. "
        "Recommended values: yes; no."
    )

    above_below_grade_ft: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Height of the path above/below grade, measured in feet and "
        "rounded to the closest foot. If below grade, provide the value as a "
        "negative number. (Ex. if the path is 10 feet above grade, this attribute "
        "would equal '10'.) For uncertain heights, use an appropriate description "
        "from the list: 'above', 'below', 'at grade'"
    )

    building_level: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Level of the building or structure the path is on, as "
        "labelled for users inside the building. Intended to capture the fact that "
        "often floor 1 isn't the level at-grade and sometimes buildings skip "
        "floors or label below-grade floors 'B' or 'SB'."
    )

    status: Annotated[
        Omitable[EdgeStatus], Tier("optional", {2: "recommended", 3: "required"})
    ] = Field(
        description="Most recent operating status of the segment. Whether the "
        "infrastructure is open and available for use. If left blank, status is "
        "assumed 'unknown.'"
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = (
        Field(
            description="When the facility was officially opened for use. date_built "
            "represents the original opening date. Use the Events extension to record "
            "details about construction history, remodeling, removal and other "
            "physical changes. Report in RFC 3339 format containing day, month and "
            "year, or just month and year or year if day or month is not available."
        )
    )

    last_inspection_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The date that this infrastructure was last inspected. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available."
    )

    official: Annotated[Omitable[list[str]], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Indicates whether a trail has been officially designated by a "
            "government body or other recognized organization, with a string of the "
            "name of the recognizing body and/or a URL to the source/reference to the "
            "recognition for users to verify and see additional information. If not an "
            "official trail, the value should be 'no.' If left blank, the trail is "
            "assumed official and managed by a local government agency."
        )
    )

    presence: Annotated[Omitable[EdgePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a sidewalk or a crossing might be missing or where its presence is "
        "unknown. Conditionally required if no other identfiying fields supplied."
    )

    measured_length_ft: Annotated[
        Omitable[Feet], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The measured length of the edge in feet. Represent partial "
        "feet using decimals. Note that geospatial data also contains a length "
        "attribute by default that may be useful in some cases. Measuring the "
        "traversable length of the segment is preferable."
    )

    separation_elements: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="The materials used to separate the cycleway or footway from "
        "motor vehicle traffic -- for example, as part of a buffer. Recommended "
        "values: bollards; concrete barrier; parking; median; trees; unknown."
    )

    separation_permeable_car: Annotated[
        Omitable[SeparationPermeableCar], Tier("optional")
    ] = Field(
        description="Whether a motor vehicle can easily access this edge. "
        "Primarily intended for bikeways but can be used for pedestrian "
        "facilities."
    )

    buffer_width_ft: Annotated[Omitable[Feet], Field(ge=0), Tier("optional")] = Field(
        description="Distance between the edge of the motor vehicle travel lane "
        "and the bike lane or sidewalk. Measured in feet, with partial feet "
        "represented using decimals. Cannot be negative."
    )

    street_parking: Annotated[Omitable[StreetParking], Tier("optional")] = Field(
        description="Indicates the orientation of street parking in relation to a "
        "bike facility. The value 'floating' means the same as 'parking "
        "protected.'"
    )

    street_parking_buffer_ft: Annotated[
        Omitable[Feet], Field(ge=0), Tier("optional")
    ] = Field(
        description="The space between a bicycle facility and the street parking. "
        "Measured in feet, with partial feet represented as decimals. Cannot be "
        "negative."
    )

    posted_speed_limit_mph: Annotated[Omitable[Mph], Field(ge=0), Tier("optional")] = (
        Field(
            description="Used to indicate the posted speed limit. Measured in miles "
            "per hour. Cannot be negative. If used on bikeway, multi-use path, or "
            "trail, it's assumed that is the speed limit for non-motorized users."
        )
    )

    prohibited_uses: Annotated[Omitable[list[ProhibitedUses]], Tier("optional")] = (
        Field(
            description="Specifies which types of users are legally prohibited from "
            "using the facility, based on the laws, policy, or signage on a facility "
            "(ex. “E-bikes prohibited on this trail”). Can provide one or multiple in "
            "list form."
        )
    )

    allowed_uses: Annotated[Omitable[list[AllowedUses]], Tier("optional")] = Field(
        description="Specifies exceptions to the usually prohibited users. "
        "Intended for designating whether bikes are allowed to use sidewalks, "
        "footways, and crossings for routing purposes."
    )

    restricted_access: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Whether access to the edge is restricted based on membership, "
        "passes / permits or access codes. Meant to help travelers easily know if "
        "general access is not allowed. Recommended values: private; "
        "access_code_required; membership_required; permit_required."
    )

    seasonal: Annotated[Omitable[list[SeasonalCondition]], Tier("optional")] = Field(
        description="Indicates whether the segment is commonly affected by "
        "seasonal issues. Use this field for recurring (ex. yearly flooding) and "
        "not one-time (ex. single flood) events. Include both the seasonal concern "
        "and the season when it occurs as a JSON String. Recommended values: "
        "season; summer; fall; winter; seasonal issues; ice; snow; heavy rain; "
        "heat / lack of shade; low visibility; fog; wind."
    )

    surface_material: Annotated[
        Omitable[SurfaceMaterial], Tier("optional", {2: "required"})
    ] = Field(description="Specifies the material used for the surface of the segment.")

    surface_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing along this edge. Recommended values: yes; "
        "no; cracking; scaling; spalling; uneven; frequent water pooling; heaving; "
        "missing bricks/stones; potholes/holes; slickness; detectable warning "
        "surface damage; longitudinal cracks and seams; metal plates; other."
    )

    incline: Annotated[Omitable[float64], Tier("optional")] = Field(
        description="The running slope of the full edge. The incline should follow "
        "the direction in which the geospatial feature was drawn. If the incline "
        "increases between the from_node and the to_node, it should be positive. "
        "If the incline decreases between the from_node and the to_node, it should "
        "be negative. Report as a percentage with two decimal points of precision. "
        "See the Playbook for more information on directionality."
    )

    cross_slope: Annotated[
        Omitable[float64], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="The cross slope of the edge at most points along its path. "
        "Report as percentage with two decimal points of precision. Cannot be "
        "negative."
    )

    cross_slope_max: Annotated[Omitable[float64], Field(ge=0), Tier("optional")] = (
        Field(
            description="The cross slope of the edge at the point along its path where "
            "there is the greatest cross slope. Report as a percentage with two "
            "decimal points of precision. Cannot be negative."
        )
    )

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[EdgeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    impediment: Annotated[
        Omitable[list[str]], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing along this edge. Mark an edge with this "
        "attribute only if the impediment is close enough to the "
        "footway/pedestrian way or bike path to potentially pose a challenge. If "
        "left blank, the assumed value for this attribute is “unknown.” "
        "Recommended values: yes; no; low overgrowth (lower than 27'); high "
        "overgrowth (27' or higher); sign; low protrusion (lower than 27'); high "
        "protrusion (27' or higher); utility cover; stormwater grate; metal plate; "
        "metal decking (ex. on bridges); other surface impediment; other "
        "impediment."
    )

    tactile_marking: Annotated[Omitable[TactileMarking], Tier("optional")] = Field(
        description="Indicates when tactile guidestrips or other markings are "
        "present to help identify the edge of a crosswalk or traffic island, the "
        "beginning or end of steps, or the presence of other infrastructure "
        "nearby, such as bike lanes. It is recommended to segment the edge so that "
        "this field is only equal to “yes” for the segment where the detectable "
        "warning appears. Do not use this field for tactile markings on curb "
        "ramps; instead, use the detectable_warning attribute for curb_ramp nodes "
        "in Tiers 1 and 2, and the detectable_warning attribute for the "
        "curb_ramp_runslope and curb_ramp_toplanding edges in Tiers 3 and 4."
    )

    other_issue: Annotated[
        Omitable[str], Tier("optional", {3: "recommended", 4: "required"})
    ] = Field(
        description="Identifies whether this edge has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types. Note that "
        "there is also an attribute for rail_crossing, which indicates if a "
        "crossing edge is a rail crossing. Use rail_crossing for track crossings "
        "that people walking, rolling or biking will need to cross, and that have "
        "active rail traffic. The 'rail tracks' value here can be used on other "
        "edge types or to identify remaining or unused tracks no longer traveled "
        "by trains. Recommended values: yes; no; detectable warning not aligned "
        "with crossing; push button not working; markings worn; markings missing; "
        "rail tracks; broken / damaged signal; auditory signal not working; "
        "vibrotactile signal not working; poor volume for auditory signal; signal "
        "button height issue; no visual countdown for signal; signal distance from "
        "walk path; other."
    )

    lrs_references: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="A JSON list capturing the attributes that appear in the GATIS "
        "LRS extension. See the extension for full attribute descriptions. Either "
        "this attribute or the extension may be used based on which is more "
        "convenient for the data producer and likely users. This attribute should "
        "be placed on each separate piece of infrastructure that is being mapped "
        "to LRS, with its specific milepoints."
    )

    last_inspection_type: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="The type of inspection that was carried out on the piece of "
        "infrastructure, on the date listed under last_inspection_date. "
        "Recommended values: routine maintenance check; ADA; safety audit; "
        "construction inspection; post-crash audit; other."
    )

    lifecycle_stage: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The lifecycle stage of this piece of infrastructure, as of "
            "the last_inspection_date. Recommended values: new; operational; nearing "
            "replacement; replacement planned or in planning."
        )
    )

    maintenance_schedule: Annotated[
        Omitable[str], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of the maintenance schedule, frequency of "
        "inspection, replacement schedule or other information about when the "
        "piece of infrastructure is maintained."
    )

    planned_work: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Description of any planned work ahead for the infrastructure. "
        "This may include plans for construction or remodeling, upcoming work "
        "orders or other types of planned improvements."
    )

    owner: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    lighting: Annotated[Omitable[YesNo], Tier("optional", {3: "recommended"})] = Field(
        description="Whether or not this edge has lighting along its entirety or "
        "majority. For single points where lighting appears, use the object point "
        "type with object_type = lighting. For enhanced lighting of crosswalks, "
        "see the ped_protection attribute on the crossing edge."
    )

    bike_dismount_area: Annotated[Omitable[YesNo], Tier("optional")] = Field(
        description="Whether this edge contains an area where cyclists are asked "
        "to dismount from their cycles."
    )

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional")] = (
        Field(
            description="Describes whether tactile paving is present, and whether or "
            "not it has a constrasting color (which should meet ADA guidelines for the "
            "amount of contrast)."
        )
    )


Edge = Annotated[
    Annotated[RoadEdge, Tag("road")]
    | Annotated[SidewalkEdge, Tag("sidewalk")]
    | Annotated[CurbRampToplandingEdge, Tag("curb_ramp_toplanding")]
    | Annotated[CurbRampRunslopeEdge, Tag("curb_ramp_runslope")]
    | Annotated[FootwayEdge, Tag("footway")]
    | Annotated[CrossingEdge, Tag("crossing")]
    | Annotated[RampEdge, Tag("ramp")]
    | Annotated[TrafficIslandEdge, Tag("traffic_island")]
    | Annotated[StepsEdge, Tag("steps")]
    | Annotated[ElevatorEdge, Tag("elevator")]
    | Annotated[EscalatorEdge, Tag("escalator")]
    | Annotated[BikewayEdge, Tag("bikeway")]
    | Annotated[MultiUsePathEdge, Tag("multi_use_path")]
    | Annotated[TrailEdge, Tag("trail")],
    Field(
        discriminator=Feature.field_discriminator(
            "edge_type",
            RoadEdge,
            SidewalkEdge,
            CurbRampToplandingEdge,
            CurbRampRunslopeEdge,
            FootwayEdge,
            CrossingEdge,
            RampEdge,
            TrafficIslandEdge,
            StepsEdge,
            ElevatorEdge,
            EscalatorEdge,
            BikewayEdge,
            MultiUsePathEdge,
            TrailEdge,
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
