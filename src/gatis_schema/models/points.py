"""GATIS point models.

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
    AnyUrl,
    BaseModel,
    ConfigDict,
    Field,
    Tag,
    TypeAdapter,
    model_validator,
)

from gatis_schema.annotations import (
    Inches,
    Seconds,
    Tier,
)
from gatis_schema.constraints import (
    all_or_none,
    drop_null_properties,
)
from gatis_schema.models.enums import (
    AccessibilityFeatures,
    Button,
    OtherIssue,
    ParkingType,
    PointSurfaceIssue,
    TrafficCalmingType,
)
from gatis_schema.scalars import GatisDate
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
    # An explicit `null` property means absent. See `drop_null_properties`;
    # real GATIS data is overwhelmingly null-valued rather than sparse.
    _drop_nulls = model_validator(mode="before")(staticmethod(drop_null_properties))

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

    object_type: Annotated[str, Tier("required")] = Field(
        description="Used to indicate objects that appear near the sidewalk or "
        "street space that, depending on the traveler, may be an amenity or an "
        "obstruction. Buffers around these points can be used to factor them into "
        "routing algorithms. If an object is on the pedestrian way, consider "
        "marking it with an issue node instead. Recommended values: bench; "
        "lighting; wastebasket; restroom; water fountain; parklet / kiosk; pet "
        "station; transit stop bench; transit stop shelter; bicycle shop / repair; "
        "permanent bollards; removable bollards; gate; fencing."
    )

    reference_ids: Annotated[Omitable[list[ReferenceId]], Tier("optional")] = Field(
        description="Can be used to add reference IDs to other datasources such as "
        "OSM, OpenLR, ARNOLD, HMPS, TIGER, Census road network, OSM, etc.). Should "
        "be an array of JSONs with the source name and ID pair. Each JSON should "
        "contain an ID field and source field at minimum. Can add other attributes "
        "such as the beginning and ending milepost from a linear referencing "
        "system."
    )

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the type of object that may pose a challenge for "
        "travelers passing through the area. Mark an issue with a node only if it "
        "is close enough to the footway or pedestrian way to potentially pose a "
        "challenge. “Horizontal overgrowth” refers to temporary obstruction at "
        "ground level, such as bushes or plants. “Vertical overgrowth” refers to "
        "temporary obstruction between 25-80' high, such as a branch or limb. "
        "“Fixed vertical obstruction” refers to a permanent obstruction between "
        "25-80' high, such as a sign. “Solid fixed object” includes street "
        "furniture, planters and other objects that cannot be difficult to "
        "navigate around and are within the pedestrian way. “Flexible fixed "
        "object” refers to bollards and other objects that some travelers may be "
        "able to navigate around and that are within the pedestrian way. "
        "“Protrusion” refers to objects of any type that are primarily located out "
        "of the pedestrian way but have some portion of them that sticks out into "
        "the pedestrian space. Recommended values: yes; no; horizontal overgrowth; "
        "vertical overgrowth; fixed vertical obstruction; solid fixed object; "
        "flexible fixed object; protrusion; turning space missing or issue; "
        "detectable warning not aligned with crossing; push button not working; "
        "other."
    )


class SignPoint(PointBase):
    """A sign that conveys information about travel or infrastructure to
    bicyclists or pedestrians.
    """

    point_type: Annotated[Literal["sign"], Tier("required")] = Field(
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

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    sign_message: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Provides the text that appears on the sign. Include only the "
        "visible text, and do not wrap it in quotation marks or other punctuation. "
        "If this attribute is blank, ensure that the sign_name attribute is filled "
        "out, and vice versa."
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
        "shs_2024-release-status/index.htm). Use the MUTCD value provided under "
        "'Sign Designation' in the Regulatory Signs table."
    )

    sign_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Indicates the type of sign as described within the MUTCD, "
        "within the 'Sign Name' field (https://mutcd.fhwa.dot.gov/kno- "
        "shs_2024-release-status/index.htm). Match the text exactly to what "
        "appears in MUTCD, including punctuation and spaces. If this attribute is "
        "blank, ensure that the sign_verbiage attribute is filled out, and vice "
        "versa."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
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


class TransitStopPoint(PointBase):
    """A point indicating the location of a transit stop of any kind."""

    point_type: Annotated[Literal["transit_stop"], Tier("required")] = Field(
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

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    surface_issue: Annotated[Omitable[list[PointSurfaceIssue]], Tier("optional")] = (
        Field(
            description="Identifies the type of damage or surface quality issue that "
            "may pose a challenge for travelers."
        )
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the type of object that may pose a challenge for "
        "travelers passing through the area. Mark an issue with a node only if it "
        "is close enough to the footway or pedestrian way to potentially pose a "
        "challenge. “Horizontal overgrowth” refers to temporary obstruction at "
        "ground level, such as bushes or plants. “Vertical overgrowth” refers to "
        "temporary obstruction between 25-80' high, such as a branch or limb. "
        "“Fixed vertical obstruction” refers to a permanent obstruction between "
        "25-80' high, such as a sign. “Solid fixed object” includes street "
        "furniture, planters and other objects that cannot be difficult to "
        "navigate around and are within the pedestrian way. “Flexible fixed "
        "object” refers to bollards and other objects that some travelers may be "
        "able to navigate around and that are within the pedestrian way. "
        "“Protrusion” refers to objects of any type that are primarily located out "
        "of the pedestrian way but have some portion of them that sticks out into "
        "the pedestrian space. Recommended values: yes; no; horizontal overgrowth; "
        "vertical overgrowth; fixed vertical obstruction; solid fixed object; "
        "flexible fixed object; protrusion; turning space missing or issue; "
        "detectable warning not aligned with crossing; push button not working; "
        "other."
    )

    gtfs_agency_id: Annotated[str, Tier("required")] = Field(
        description="The agency_id from the General Transit Feed Specification for "
        "the agency that maintains data about this stop. Both agency_id and "
        "stop_id must be provided. These IDs can be crosswalked with GTFS and "
        "TIDES data to obtain additional stop attributes and connect to the "
        "broader transit network. See GTFS documentation for more information."
    )

    gtfs_stop_id: Annotated[str, Tier("required")] = Field(
        description="The stop_id from the General Transit Feed Specification for "
        "the agency that maintains data about this stop. Both agency_id and "
        "stop_id must be provided. These IDs can be crosswalked with GTFS and "
        "TIDES data to obtain additional stop attributes and connect to the "
        "broader transit network. See GTFS documentation for more information."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
    )


class IssuePoint(PointBase):
    """A point indicating a particular spot that has an issue relevant to routing
    for some travelers.
    """

    point_type: Annotated[Literal["issue"], Tier("required")] = Field(
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

    surface_issue: Annotated[Omitable[list[PointSurfaceIssue]], Tier("optional")] = (
        Field(
            description="Identifies the type of damage or surface quality issue that "
            "may pose a challenge for travelers."
        )
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the type of object that may pose a challenge for "
        "travelers passing through the area. Mark an issue with a node only if it "
        "is close enough to the footway or pedestrian way to potentially pose a "
        "challenge. “Horizontal overgrowth” refers to temporary obstruction at "
        "ground level, such as bushes or plants. “Vertical overgrowth” refers to "
        "temporary obstruction between 25-80' high, such as a branch or limb. "
        "“Fixed vertical obstruction” refers to a permanent obstruction between "
        "25-80' high, such as a sign. “Solid fixed object” includes street "
        "furniture, planters and other objects that cannot be difficult to "
        "navigate around and are within the pedestrian way. “Flexible fixed "
        "object” refers to bollards and other objects that some travelers may be "
        "able to navigate around and that are within the pedestrian way. "
        "“Protrusion” refers to objects of any type that are primarily located out "
        "of the pedestrian way but have some portion of them that sticks out into "
        "the pedestrian space. Recommended values: yes; no; horizontal overgrowth; "
        "vertical overgrowth; fixed vertical obstruction; solid fixed object; "
        "flexible fixed object; protrusion; turning space missing or issue; "
        "detectable warning not aligned with crossing; push button not working; "
        "other."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
    )


class CounterPoint(PointBase):
    """A point indicating the location of a camera, sensor, pneumatic tube,
    inductive loop, magnetometer or other mechanism for counting the number of
    bicyclists or pedestrians passing through a counting site.
    """

    point_type: Annotated[Literal["counter"], Tier("required")] = Field(
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

    counter_site_id: Annotated[str, Tier("required")] = Field(
        description="The identification number for this counter site within the "
        "source dataset."
    )

    counter_site_name: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The name for this counter site within the source dataset."
    )

    counter_data_source: Annotated[Omitable[str], Tier("optional")] = Field(
        description="The name of the specification or dataset from which data can "
        "be obtained about the counter and its results. For any point of type "
        "'counter', please ensure that either counter_data_source or "
        "counter_data_URL is filled out."
    )

    counter_data_URL: Annotated[Omitable[AnyUrl], Tier("optional")] = Field(
        description="The URL for the dataset from which data can be obtained about "
        "the counter and its results. For any point of type 'counter,' please "
        "ensure that either counter_data_source or counter_data_URL is filled out."
    )

    counter_comments: Annotated[Omitable[str], Tier("optional")] = Field(
        description="Any comments about the data or its source that are important "
        "for understanding how to access and crosswalk data about the counter "
        "site. For example, this field may be used to list multiple detector IDs "
        "located at the site."
    )


class BikeParkingPoint(PointBase):
    """A point indicating the location of a bicycle or micromobility parking
    facility.
    """

    point_type: Annotated[Literal["bike_parking"], Tier("required")] = Field(
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

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    surface_issue: Annotated[Omitable[list[PointSurfaceIssue]], Tier("optional")] = (
        Field(
            description="Identifies the type of damage or surface quality issue that "
            "may pose a challenge for travelers."
        )
    )

    impediment: Annotated[Omitable[list[str]], Tier("optional")] = Field(
        description="Identifies the type of object that may pose a challenge for "
        "travelers passing through the area. Mark an issue with a node only if it "
        "is close enough to the footway or pedestrian way to potentially pose a "
        "challenge. “Horizontal overgrowth” refers to temporary obstruction at "
        "ground level, such as bushes or plants. “Vertical overgrowth” refers to "
        "temporary obstruction between 25-80' high, such as a branch or limb. "
        "“Fixed vertical obstruction” refers to a permanent obstruction between "
        "25-80' high, such as a sign. “Solid fixed object” includes street "
        "furniture, planters and other objects that cannot be difficult to "
        "navigate around and are within the pedestrian way. “Flexible fixed "
        "object” refers to bollards and other objects that some travelers may be "
        "able to navigate around and that are within the pedestrian way. "
        "“Protrusion” refers to objects of any type that are primarily located out "
        "of the pedestrian way but have some portion of them that sticks out into "
        "the pedestrian space. Recommended values: yes; no; horizontal overgrowth; "
        "vertical overgrowth; fixed vertical obstruction; solid fixed object; "
        "flexible fixed object; protrusion; turning space missing or issue; "
        "detectable warning not aligned with crossing; push button not working; "
        "other."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
    )

    parking_type: Annotated[ParkingType, Tier("required")] = Field(
        description="The type of parking facility."
    )

    parking_id: Annotated[Omitable[str], Tier("recommended")] = Field(
        description="The identification number for this parking site within the "
        "source dataset."
    )

    parking_provider: Annotated[Omitable[str], Tier("recommended")] = Field(
        description="The name of the provider of the parking services at this "
        "parking site. This attribute is most useful for shared micromobility, to "
        "identify the provider of the micromobility service."
    )

    parking_data_URL: Annotated[Omitable[AnyUrl], Tier("recommended")] = Field(
        description="The URL for the dataset from which data can be obtained about "
        "this parking site."
    )

    date_built: Annotated[Omitable[GatisDate], Tier("optional")] = Field(
        description="Indicates when the facility was officially opened for use. If "
        "the facility has had a major remodeling where the structure, shape or "
        "another fundamental aspect was changed, the date of remodeling can be "
        "placed here. Report in RFC 3339 format containing day, month and year, or "
        "just month and year or year if day or month is not available."
    )


class TrafficCalmingPoint(PointBase):
    """Used to identify where traffic calming features are located."""

    point_type: Annotated[Literal["traffic_calming"], Tier("required")] = Field(
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

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
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


@all_or_none("ada_compliance_date", "ada_compliant_with")
class PushbuttonPoint(PointBase):
    """Identifies the location of a signal button, accessible pedestrian signal,
    or pedestrian or cyclist detector.
    """

    point_type: Annotated[Literal["pushbutton"], Tier("required")] = Field(
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

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("recommended")] = Field(
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

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("recommended")] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[Omitable[str], Tier("recommended")] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    button: Annotated[Omitable[Button], Tier("optional")] = Field(
        description="Whether or not a push button is present at the signal "
        "location. The button may or may not be functional; use the other_issue "
        "attribute to track if a button is not working."
    )

    button_vert_height_in: Annotated[Omitable[Inches], Tier("optional")] = Field(
        description="If a button is present, the vertical height in inches of the "
        "push button, measured from the ground to the bottom of the button."
    )

    tactile_message: Annotated[Omitable[str], Tier("optional")] = Field(
        description="What types of tactile information are available at the signal "
        "location to help pedestrians cross. Recommended values: arrow; vibration "
        "walk signal; minimap; other."
    )

    auditory_message: Annotated[Omitable[str], Tier("optional")] = Field(
        description="What auditory messages are available at the signal location. "
        "“Information message” means any message that names the street being "
        "crossed or provides other geographical details. Recommended values: "
        "auditory walk signal; information message; button locator tone; other."
    )

    actuation_type: Annotated[Omitable[str], Tier("recommended")] = Field(
        description="What type of mechanism, if any, helps to identify that a "
        "pedestrian is at the crossing and wishes to cross. “Pedestrian actuated” "
        "indicates that a push button can or must be pushed to call the signal. "
        "“Pedestrian auto-detected” includes any kind of device that identifies "
        "the presence of a pedestrian and triggers the signal. Recommended values: "
        "Pedestrian actuated; pedestrian auto-detected; bike actuated; bike auto- "
        "detected; recall (no actuation or detection); unknown."
    )

    crossing_time_sec: Annotated[Omitable[Seconds], Tier("recommended")] = Field(
        description="The time in whole seconds that the signal provides for "
        "pedestrians to cross the crossing. For signals that do not have a fixed "
        "crossing time, list the minimum time provided."
    )


@all_or_none("ada_compliance_date", "ada_compliant_with")
class DetectorPoint(PointBase):
    """Identifies the location of a pedestrian or cyclist detector."""

    point_type: Annotated[Literal["detector"], Tier("required")] = Field(
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

    accessibility_features: Annotated[
        Omitable[list[AccessibilityFeatures]], Tier("optional")
    ] = Field(
        description="Features available as part of this infrastructure for "
        "accessibility related to signage, digital signage, benches, kiosks, "
        "transit stops, etc."
    )

    other_issue: Annotated[Omitable[OtherIssue], Tier("optional")] = Field(
        description="Identifies whether this point marks another type of issue "
        "that may pose a challenge for travelers, besides impediments and surface "
        "damage. Includes design, construction and other issue types."
    )

    last_inspection_date: Annotated[Omitable[GatisDate], Tier("recommended")] = Field(
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

    ada_compliance_date: Annotated[Omitable[GatisDate], Tier("recommended")] = Field(
        description="Indicates the date when ADA compliance was assessed. Report "
        "in RFC 3339 format containing day, month and year, or just month and year "
        "or year if day or month is not available.. This field is conditionally "
        "required if 'ada_compliant_with' is filled out."
    )

    ada_compliant_with: Annotated[Omitable[str], Tier("recommended")] = Field(
        description="If this infrastructure has been assessed for ADA compliance, "
        "the specific ADA guidelines or standards used in the assessment. Also "
        "fill out 'ada_compliance_date.' If no ADA assessment is being reported, "
        "leave blank."
    )

    actuation_type: Annotated[Omitable[str], Tier("recommended")] = Field(
        description="What type of mechanism, if any, helps to identify that a "
        "pedestrian is at the crossing and wishes to cross. “Pedestrian actuated” "
        "indicates that a push button can or must be pushed to call the signal. "
        "“Pedestrian auto-detected” includes any kind of device that identifies "
        "the presence of a pedestrian and triggers the signal. Recommended values: "
        "Pedestrian actuated; pedestrian auto-detected; bike actuated; bike auto- "
        "detected; recall (no actuation or detection); unknown."
    )

    crossing_time_sec: Annotated[Omitable[Seconds], Tier("recommended")] = Field(
        description="The time in whole seconds that the signal provides for "
        "pedestrians to cross the crossing. For signals that do not have a fixed "
        "crossing time, list the minimum time provided."
    )


Point = Annotated[
    Annotated[ObjectPoint, Tag("object")]
    | Annotated[SignPoint, Tag("sign")]
    | Annotated[TransitStopPoint, Tag("transit_stop")]
    | Annotated[IssuePoint, Tag("issue")]
    | Annotated[CounterPoint, Tag("counter")]
    | Annotated[BikeParkingPoint, Tag("bike_parking")]
    | Annotated[TrafficCalmingPoint, Tag("traffic_calming")]
    | Annotated[PushbuttonPoint, Tag("pushbutton")]
    | Annotated[DetectorPoint, Tag("detector")],
    Field(
        discriminator=Feature.field_discriminator(
            "point_type",
            ObjectPoint,
            SignPoint,
            TransitStopPoint,
            IssuePoint,
            CounterPoint,
            BikeParkingPoint,
            TrafficCalmingPoint,
            PushbuttonPoint,
            DetectorPoint,
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
