"""GATIS node models.

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
from overture.schema.system.ref import Id, Identified
from pydantic import BaseModel, ConfigDict, Field, Tag, TypeAdapter

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
    CurbType,
    DetectableWarning,
    FeaturePresence,
    Impediment,
    RailCrossing,
    Status,
    SurfaceIssue,
)


class NodeBase(Identified, Feature):
    """Common base for every GATIS node type."""

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
        alias="node_id",
        description="A unique identifier for the node. [NOTE: We will fill in instructions here on how to generate IDs, and we will also provide a data validator that may be capable of validating and helping to fill in these IDs.]",
    )


class VirtualNode(NodeBase):
    """Used to create nodes for routing in places where specific physical infrastructure doesn’t exist, where edges are split because attributes are different between them, or where other nodes don’t suit the purpose."""

    node_type: Annotated[Literal["virtual"], Tier("required")] = Field(description="Indicates the type of node.")

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")

    curb_type: Annotated[Omitable[CurbType], Tier("optional", {3: "recommended"})] = Field(description="The type of curb that is present, if there is not a curb ramp.")

    rail_crossing: Annotated[Omitable[list[RailCrossing]], Tier("optional", {3: "recommended"})] = Field(description="Describes the pedestrian traffic warnings and controls in the approach to the rail crossing. The nodes mark the location of the controls on each side of the tracks. Mark the crossing itself as a virtual link (edge).")


@all_or_none("ada_compliance_date", "ada_compliant_with")
class CurbRampNode(NodeBase):
    """Indicates a location where a pedestrian must make a decision about which direction to travel, most commonly in locations where a curb ramp does or should exist."""

    node_type: Annotated[Literal["curb_ramp"], Tier("required")] = Field(description="Indicates the type of node.")

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a curb ramp or other infrastructure might be missing or where its presence is unknown. Conditionally required if no other identifying attributes provided.")

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {2: "recommended"})] = Field(description="When the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {2: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available. This field is conditionally required if 'ada_compliant_with' is filled out.")

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")

    incline: Annotated[Omitable[Percent], Tier("optional", {3: "required"})] = Field(description="Indicates the incline or running slope of the ramp, following the possible directions of travel. Reported as a decimal number describing the percentage of the slope, with two points of precision.")

    cross_slope: Annotated[Omitable[Percent], Field(ge=0), Tier("optional", {3: "required"})] = Field(description="Indicates the cross slope of the ramp, which runs perpendicular to the incline / directions of travel. Reported as a decimal number describing the percentage of the slope, with two points of precision. Cannot be negative.")

    width: Annotated[Omitable[InchesFloat], Tier("optional", {3: "required"})] = Field(description="Indicates the minimum width of the ramp, measured between the handrails if handrails are provided. Reported as a whole number rounded to the nearest inch. Note that it is assumed that 80' of height clearance is available for the full width given in this field.")

    ramp_type: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = Field(description="Indicates the orientation of the ramp in relation to the pedestrian direction of travel at the location. Where a double curb ramp exists, map each ramp as a separate curb_ramp node. Recommended values: diagonal; parallel; perpendicular; unknown.")

    detectable_warning: Annotated[Omitable[DetectableWarning], Tier("optional", {3: "required"})] = Field(description="Describes whether tactile paving is present, and whether or not it has a constrasting color (which should meet ADA guidelines for the amount of contrast).")

    impediment: Annotated[Omitable[list[Impediment]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing through this node. Mark a node with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")

    surface_issue: Annotated[Omitable[list[SurfaceIssue]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Description of surface quality issues that may pose a challenge for travelers passing through this node.")

    status: Annotated[Omitable[Status], Tier("optional", {2: "recommended", 3: "required"})] = Field(description="Most recent operating status of the node. Whether the infrastructure is open and available for use. Default is 'open'")


@all_or_none("ada_compliance_date", "ada_compliant_with")
class ElevatorNode(NodeBase):
    """Elevators, funiculars, or other car- or enclosure-based constructions meant to vertically carry a pedestrian from one level of physical infrastructure to another."""

    node_type: Annotated[Literal["elevator"], Tier("required")] = Field(description="Indicates the type of node.")

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a curb ramp or other infrastructure might be missing or where its presence is unknown. Conditionally required if no other identifying attributes provided.")

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="When the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("conditionally_required")] = Field(description="Indicates the date when ADA compliance was assessed. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available. This field is conditionally required if 'ada_compliant_with' is filled out.")

    ada_compliant_with: Annotated[Omitable[AdaCompliantWith], Tier("conditionally_required")] = Field(description="If this infrastructure has been assessed for ADA compliance, the specific ADA guidelines or standards used in the assessment. Also fill out 'ada_compliance_date.' If no ADA assessment is being reported, leave blank.")

    status: Annotated[Omitable[Status], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Most recent operating status of the node. Whether the infrastructure is open and available for use. Default is 'open'")


class TransitStopNode(NodeBase):
    """A node indicating the location of a transit stop of any kind."""

    node_type: Annotated[Literal["transit_stop"], Tier("required")] = Field(description="Indicates the type of node.")

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")

    gtfs_id: Annotated[Omitable[list[GtfsReference]], Tier("optional", {3: "recommended"})] = Field(description="An array of objects containing keys for GTFS agency_id and stop_id from an existing GTFS dataset for this transit stop. Represent as string with the format '{agency_id},{stop_id}'. These IDs can be crosswalked with GTFS and TIDES data to obtain additional stop attributes and connect to the broader transit network. See GTFS documentation for more information.")


class IssueNode(NodeBase):
    """A node indicating a particular point that has an issue relevant to routing for some travelers."""

    node_type: Annotated[Literal["issue"], Tier("required")] = Field(description="Indicates the type of node.")

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    impediment: Annotated[Omitable[list[Impediment]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Identifies the presence of an object that may pose a challenge for travelers passing through this node. Mark a node with this attribute only if the impediment is close enough to the footpath/pedestrian way or bike path to potentially pose a challenge. If left blank, the assumed value for this attribute is “unknown.”")

    surface_issue: Annotated[Omitable[list[SurfaceIssue]], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Description of surface quality issues that may pose a challenge for travelers passing through this node.")


class TrafficCalmingNode(NodeBase):
    """traffic_calming"""

    node_type: Annotated[Literal["traffic_calming"], Tier("required")] = Field(description="Indicates the type of node.")

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(description="Indicates whether the piece of infrastructure exists or is present. When other attributes are provided, the existence of the infrastructure can be assumed. This attribute is useful for identifying where a curb ramp or other infrastructure might be missing or where its presence is unknown. Conditionally required if no other identifying attributes provided.")

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(description="Can be used to add reference IDs to other datasources such as OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should be an array of JSONs with the source name and ID pair. Each JSON should contain an ID field and source field at minimum. Can add other attributes such as the beginning and ending milepost from a linear referencing system.")

    date_built: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="When the facility was officially opened for use. If the facility has had a major remodeling where the structure, shape or another fundamental aspect was changed, the date of remodeling can be placed here. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    check_date: Annotated[Omitable[GatisDate], Tier("optional", {3: "recommended"})] = Field(description="The date that this infrastructure was last inspected. Report in RFC 3339 format containing day, month and year, or just month and year or year if day or month is not available.")

    traffic_calming_type: Annotated[Omitable[str], Tier("optional", {3: "recommended", 4: "required"})] = Field(description="Used to identify traffic calming features on a road or crossing. Used when it makes more sense to model the traffic calming feature as a node instead of an edge. Recommended values are from https://www.ite.org/pub/?id=2a60c136-b1c0-b231-0522-ccbd075cac84 and https://wiki.openstreetmap.org/wiki/Key:traffic_calming")

    status: Annotated[Omitable[Status], Tier("optional")] = Field(description="Most recent operating status of the node. Whether the infrastructure is open and available for use. Default is 'open'")


Node = Annotated[
    Annotated[VirtualNode, Tag("virtual")]
    | Annotated[CurbRampNode, Tag("curb_ramp")]
    | Annotated[ElevatorNode, Tag("elevator")]
    | Annotated[TransitStopNode, Tag("transit_stop")]
    | Annotated[IssueNode, Tag("issue")]
    | Annotated[TrafficCalmingNode, Tag("traffic_calming")],
    Field(
        discriminator=Feature.field_discriminator(
            "node_type",
            VirtualNode,
            CurbRampNode,
            ElevatorNode,
            TransitStopNode,
            IssueNode,
            TrafficCalmingNode,
        )
    ),
]
"""Any node, discriminated on `node_type`."""

NodeAdapter: TypeAdapter[Node] = TypeAdapter(Node)
"""Validator for one node, including from raw GeoJSON."""


class NodeCollection(BaseModel):
    """The contents of `nodes.geojson`."""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Node]
