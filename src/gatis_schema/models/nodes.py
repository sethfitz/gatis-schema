"""GATIS node models.

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

from gatis_schema.annotations import (
    InchesFloat,
    Percent,
    Tier,
)
from gatis_schema.constraints import (
    all_or_none,
    drop_null_properties,
)
from gatis_schema.models.enums import (
    CurbType,
    DetectableWarning,
    FeaturePresence,
    Impediment,
    NodeAdaCompliantWith,
    NodeStatus,
    NodeSurfaceIssue,
    OtherIssue,
    RailCrossingControl,
)
from gatis_schema.scalars import GatisDate
from gatis_schema.shared import (
    ReferenceId,
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
    # An explicit `null` property means absent. See `drop_null_properties`;
    # real GATIS data is overwhelmingly null-valued rather than sparse.
    _drop_nulls = model_validator(mode="before")(staticmethod(drop_null_properties))

    # Redeclared from `Feature`, where it is `Omitable[Id]`, to make it
    # mandatory. Same narrowing, and the same silencing, as Overture's own
    # `OvertureFeature`.
    id: Annotated[Id, Tier("required")] = Field(  # type: ignore[assignment]
        alias="node_id",
        description="A unique identifier for the node. [NOTE: We will fill in "
        "instructions here on how to generate IDs, and we will also provide a data "
        "validator that may be capable of validating and helping to fill in these "
        "IDs.]",
    )


class GenericNode(NodeBase):
    """Used to create nodes for routing in places where specific physical
    infrastructure doesn’t exist, but where edges are split because attributes are
    different, or where other nodes don’t suit the purpose.
    """

    node_type: Annotated[Literal["generic"], Tier("required")] = Field(
        description="Indicates the type of node."
    )

    curb_ramp_system_id: Annotated[Omitable[str], Tier("optional")] = Field(
        description="An identifier to link any nodes and/or edges that are "
        "involved in the same 'curb ramp system', which we define as the network "
        "of elements that sidewalk users use to transition from a sidewalk to a "
        "crossing or other pedestrian edge. For clarity, use the same "
        "curb_ramp_system_id for all elements of the same ramp system. The ID can "
        "be any unique number to the system. Curb ramp systems may include "
        "sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and crosswalk "
        "edges; as well as sidewalk_to_ramp_transition, ramp_to_street_transition "
        "or generic nodes."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
    )

    curb_type: Annotated[Omitable[CurbType], Tier("optional", {3: "recommended"})] = (
        Field(
            description="The type of curb that is present, if there is not a curb ramp."
        )
    )

    rail_crossing_control: Annotated[
        Omitable[list[RailCrossingControl]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Describes the pedestrian traffic warnings and controls in the "
        "approach to the rail crossing. The nodes mark the location of the "
        "controls on each side of the tracks. Mark the crossing itself as a "
        "crossing edge with attribute rail_crossing=yes."
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class CurbRampNode(NodeBase):
    """In Tiers 1-2, a node that indicates the location of curb ramps."""

    node_type: Annotated[Literal["curb_ramp"], Tier("required")] = Field(
        description="Indicates the type of node."
    )

    presence: Annotated[Omitable[FeaturePresence], Tier("optional")] = Field(
        description="Indicates whether the piece of infrastructure exists or is "
        "present. When other attributes are provided, the existence of the "
        "infrastructure can be assumed. This attribute is useful for identifying "
        "where a curb ramp or other infrastructure might be missing or where its "
        "presence is unknown. Conditionally required if no other identifying "
        "attributes provided."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
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

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {2: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[NodeAdaCompliantWith], Tier("optional", {2: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    incline: Annotated[Omitable[Percent], Tier("optional", {3: "recommended"})] = Field(
        description="Indicates the incline or running slope of the ramp, following "
        "the possible directions of travel. Reported as a decimal number "
        "describing the percentage of the slope, with two points of precision."
    )

    cross_slope: Annotated[
        Omitable[Percent], Field(ge=0), Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the cross slope of the ramp, which runs "
        "perpendicular to the incline / directions of travel. Reported as a "
        "decimal number describing the percentage of the slope, with two points of "
        "precision. Cannot be negative."
    )

    width_in: Annotated[Omitable[InchesFloat], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Indicates the minimum width of the ramp, measured between the "
            "handrails if handrails are provided. Reported as a whole number rounded "
            "to the nearest inch. Note that it is assumed that 80' of height clearance "
            "is available for the full width given in this field."
        )
    )

    ramp_type: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Indicates the orientation of the ramp in relation to the "
        "pedestrian direction of travel at the location. Where a double curb ramp "
        "exists, map each ramp as a separate curb_ramp node. Recommended values: "
        "diagonal; directional; parallel; perpendicular; built-up; combination; "
        "transition; cut-through (median/island ramp); unknown."
    )

    detectable_warning: Annotated[
        Omitable[DetectableWarning], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Describes whether tactile paving is present, and whether or "
        "not it has a constrasting color (which should meet ADA guidelines for the "
        "amount of contrast)."
    )

    impediment: Annotated[
        Omitable[list[Impediment]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Identifies the presence of an object that may pose a "
        "challenge for travelers passing through this node. Mark a node with this "
        "attribute only if the impediment is close enough to the pedestrian way or "
        "bike path to potentially pose a challenge. If left blank, the assumed "
        "value for this attribute is “unknown.”"
    )

    surface_issue: Annotated[
        Omitable[list[NodeSurfaceIssue]], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Description of surface quality issues that may pose a "
        "challenge for travelers passing through this node."
    )

    status: Annotated[Omitable[NodeStatus], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Most recent operating status of the node. Whether the "
            "infrastructure is open and available for use. If left blank, status is "
            "assumed 'open'"
        )
    )

    other_issue: Annotated[
        Omitable[OtherIssue], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Identifies whether this node has another type of issue that "
        "may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
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

    planned_work: Annotated[Omitable[str], Tier("optional", {3: "recommended"})] = (
        Field(
            description="Description of any planned work ahead for the infrastructure. "
            "This may include plans for construction or remodeling, upcoming work "
            "orders or other types of planned improvements."
        )
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


@all_or_none("ada_compliance_date", "ada_compliant_with")
class SidewalkToRampTransitionNode(NodeBase):
    """A node that, in pedestrian infrastructure, connects a curb ramp edge
    (type=curb_ramp_runslope) to a turning area (or top landing;
    type=curb_ramp_toplanding) edge.
    """

    node_type: Annotated[Literal["sidewalk_to_ramp_transition"], Tier("required")] = (
        Field(description="Indicates the type of node.")
    )

    curb_ramp_system_id: Annotated[str, Tier("required")] = Field(
        description="An identifier to link any nodes and/or edges that are "
        "involved in the same 'curb ramp system', which we define as the network "
        "of elements that sidewalk users use to transition from a sidewalk to a "
        "crossing or other pedestrian edge. For clarity, use the same "
        "curb_ramp_system_id for all elements of the same ramp system. The ID can "
        "be any unique number to the system. Curb ramp systems may include "
        "sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and crosswalk "
        "edges; as well as sidewalk_to_ramp_transition, ramp_to_street_transition "
        "or generic nodes."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
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

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[NodeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class RampToStreetTransitionNode(NodeBase):
    """A node that, in pedestrian infrastructure, connects a crossing to a ramp
    edge (type=curb_ramp_runslope).
    """

    node_type: Annotated[Literal["ramp_to_street_transition"], Tier("required")] = (
        Field(description="Indicates the type of node.")
    )

    curb_ramp_system_id: Annotated[str, Tier("required")] = Field(
        description="An identifier to link any nodes and/or edges that are "
        "involved in the same 'curb ramp system', which we define as the network "
        "of elements that sidewalk users use to transition from a sidewalk to a "
        "crossing or other pedestrian edge. For clarity, use the same "
        "curb_ramp_system_id for all elements of the same ramp system. The ID can "
        "be any unique number to the system. Curb ramp systems may include "
        "sidewalk edges, curb_ramp_toplanding, curb_ramp_runslope, and crosswalk "
        "edges; as well as sidewalk_to_ramp_transition, ramp_to_street_transition "
        "or generic nodes."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum."
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

    ada_compliance_date: Annotated[
        Omitable[GatisDate], Tier("optional", {3: "recommended"})
    ] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[
        Omitable[NodeAdaCompliantWith], Tier("optional", {3: "recommended"})
    ] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )


Node = Annotated[
    Annotated[GenericNode, Tag("generic")]
    | Annotated[CurbRampNode, Tag("curb_ramp")]
    | Annotated[SidewalkToRampTransitionNode, Tag("sidewalk_to_ramp_transition")]
    | Annotated[RampToStreetTransitionNode, Tag("ramp_to_street_transition")],
    Field(
        discriminator=Feature.field_discriminator(
            "node_type",
            GenericNode,
            CurbRampNode,
            SidewalkToRampTransitionNode,
            RampToStreetTransitionNode,
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
