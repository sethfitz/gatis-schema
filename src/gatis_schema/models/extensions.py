"""GATIS extension tables: LRS crosswalk, events and relations.

HAND-WRITTEN, not bootstrapped. Section 2.1 declares `lrs.json`, `events.json`
and `relations.json` alongside the five core files, and upstream publishes no
structured JSON, no JSON Schema and no Explorer table for any of them -- their
field tables exist only in `documents/drafts/GATIS Extensions and Tables.pdf`,
which the Explorer links from the same row of buttons as the core tables. So
`gatis_schema.codegen` has nothing to read and these models are written out.

The source of truth for them is [`spec/extensions.json`](../../../spec/extensions.json),
a hand transcription of that PDF kept beside it and verified against it.
`tests/test_extensions.py` asserts that every model here matches that file field
for field, so a re-transcription or an upstream publication shows up as a failing
test rather than as silent drift.

## Four ways these differ from the core models

**They are not features.** Section 2.1 gives the core five as GeoJSON and these
three as plain JSON, so a row is a `BaseModel` rather than an Overture `Feature`,
and there is no geometry, no `properties` envelope and no `drop_null_properties`.
Only `Event.event_location` carries geometry, as an ordinary field.

**They are outside the tier model**, so no field carries a `Tier` annotation. The
Playbook says so outright of the LRS extension -- "It is not associated with
GATIS' tier structure" -- and the PDF gives one Required/Optional flag per field
rather than the four-slot presence rule a core field gets. `Tier` would be a
fabrication.

**The envelope is unspecified.** Nothing says whether `events.json` is a bare
array, or an object keyed by table name, or something else; the Playbook only
says "Each row in the Events Extension represents a single event." The adapters
below validate a bare list, which is the only shape anyone has described, and
`Dataset.load` accepts either that or a single-key object wrapping it. Reported
in `docs/spec-review.md`.

**Some fields are typed against their own descriptions**, and the descriptions
win, on the `shared.ReferenceId` precedent: a model that rejects what the
specification tells a publisher to write is a wish rather than a model. See
`Event.event_location`, and `TextOrList` / `IdOrList` for the seven columns
declared as one value and documented as possibly several.

All three are registered under `overture.models` in `pyproject.toml` and tagged
`gatis:extension` by `gatis_schema.tag_providers`, so `scripts/generate-reference`
renders them alongside the four core classes.
"""

from __future__ import annotations

from typing import Annotated, Literal

from overture.schema.system.doc import DocumentedEnum
from overture.schema.system.geometric import Geometry
from overture.schema.system.numeric import float64, int32
from overture.schema.system.optionality import Omitable
from overture.schema.system.ref import Id
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from gatis_schema.constraints import (
    ScalarOrListConstraint,
    SuggestedValues,
    drop_null_properties,
)
from gatis_schema.scalars import GatisDatetime

# Seven columns are declared as one value and documented as possibly several.
# *Which* seven is data: `multiple` in `spec/extensions.json` marks them and
# quotes the sentence in each column's own description that licenses it, and
# `test_multi_valued_columns_come_from_the_transcription` asserts this set and
# that one agree. These aliases are only the mechanism -- see
# `ScalarOrListConstraint` for why a constraint rather than a `str | list[str]`
# union, which the codegen cannot render.
TextOrList = Annotated[list[str], ScalarOrListConstraint()]
"""A `Text` column that may carry several values."""

IdOrList = Annotated[list[Id], ScalarOrListConstraint()]
"""An `ID` column that may carry several identifiers."""

# --------------------------------------------------------------------------
# Vocabularies
# --------------------------------------------------------------------------


class GatisGeometryType(str, DocumentedEnum):
    """Which core file a row's `gatis_id` points into.

    The one vocabulary the LRS and events tables agree on exactly.
    """

    EDGE = "edge"
    NODE = "node"
    POINT = "point"
    ZONE = "zone"


class LrsFeatureType(str, DocumentedEnum):
    """`Type` in the LRS table: "any edge, node, point or zone types within GATIS".

    It is not. Two of the 22 values are not v1.0 feature types -- `virtual_link`,
    which v1.0 removed, and `traffic island`, which v1.0 spells `traffic_island`
    (two rows below `traffic_calming`, spelled with an underscore in this same
    list). Eight v1.0 types are missing, including `road`, `pushbutton`,
    `detector` and all three members of the curb-ramp system, so an LRS row cannot
    name a road.

    Kept verbatim anyway. Correcting it here would fork the spec and hide the
    defect; `docs/spec-review.md` reports it, each bad value carries its own
    note through `DocumentedEnum` so a reader meets it at the value rather than
    here, and `test_exactly_the_unrecognised_members_carry_a_note` derives which
    members those are rather than trusting this list.
    """

    SIDEWALK = "sidewalk"
    FOOTWAY = "footway"
    CROSSING = "crossing"
    RAMP = "ramp"
    TRAFFIC_ISLAND = (
        "traffic island",
        "Not a v1.0 feature type: v1.0 spells it `traffic_island`. This list "
        "spells `traffic_calming` with an underscore.",
    )
    STEPS = "steps"
    ELEVATOR = "elevator"
    ESCALATOR = "escalator"
    BIKEWAY = "bikeway"
    MULTI_USE_PATH = "multi_use_path"
    TRAIL = "trail"
    VIRTUAL_LINK = (
        "virtual_link",
        "Not a v1.0 feature type: removed from the edge types, though its "
        "presence column survives on all 78 edge attributes.",
    )
    GENERIC = "generic"
    CURB_RAMP = "curb_ramp"
    OBJECT = "object"
    SIGN = "sign"
    TRANSIT_STOP = "transit_stop"
    ISSUE = "issue"
    COUNTER = "counter"
    BIKE_PARKING = "bike_parking"
    OPEN = "open"
    TRAFFIC_CALMING = "traffic_calming"


class EventFeatureType(str, DocumentedEnum):
    """`type` in the events table, and a different list from `LrsFeatureType`.

    Same sentence introduces it and the vocabulary disagrees: this one adds
    `virtual_node` and `open_movement` -- draft-2 names v1.0 renamed to `generic`
    and `open` -- keeps `virtual_link`, and drops `generic`, `open` and
    `traffic_calming`. Eleven v1.0 types are unreachable from an events row.
    """

    SIDEWALK = "sidewalk"
    FOOTWAY = "footway"
    CROSSING = "crossing"
    RAMP = "ramp"
    TRAFFIC_ISLAND = (
        "traffic island",
        "Not a v1.0 feature type: v1.0 spells it `traffic_island`. This list "
        "spells `traffic_calming` with an underscore.",
    )
    STEPS = "steps"
    ELEVATOR = "elevator"
    ESCALATOR = "escalator"
    BIKEWAY = "bikeway"
    MULTI_USE_PATH = "multi_use_path"
    TRAIL = "trail"
    VIRTUAL_LINK = (
        "virtual_link",
        "Not a v1.0 feature type: removed from the edge types, though its "
        "presence column survives on all 78 edge attributes.",
    )
    VIRTUAL_NODE = (
        "virtual_node",
        "Not a v1.0 feature type: the draft-2 name for what v1.0 calls "
        "`generic`, which this list does not offer.",
    )
    CURB_RAMP = "curb_ramp"
    OBJECT = "object"
    SIGN = "sign"
    TRANSIT_STOP = "transit_stop"
    ISSUE = "issue"
    COUNTER = "counter"
    BIKE_PARKING = "bike_parking"
    OPEN_MOVEMENT = (
        "open_movement",
        "Not a v1.0 feature type: the draft-2 name for what v1.0 calls the "
        "`open` zone, which this list does not offer.",
    )


class LrsSide(str, DocumentedEnum):
    """Which side of the LRS segment the infrastructure is on.

    The only place in GATIS where `both` is a legal side. The on-road modifier
    fields in `edges_schema.json` enumerate `left` and `right` only, across all
    292 of them, though the Playbook's section on them is titled "Left, Right and
    Both Tags".
    """

    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


# --------------------------------------------------------------------------
# Rows
# --------------------------------------------------------------------------


class ExtensionRow(BaseModel):
    """Common configuration for a row in one of the three extension tables."""

    model_config = ConfigDict(
        # Section 6.1: an unknown field warns, it does not fail. The Playbook says
        # the same of the events table -- "New event_types can be freely added" --
        # and of extensions generally.
        extra="allow",
        populate_by_name=True,
        serialize_by_alias=True,
    )

    # An explicit `null` reads as absent, as it does on a core feature. Same
    # reasoning, same helper: Esri-derived exports write every unset field as a
    # null, and nothing in GATIS distinguishes "known empty" from "not
    # collected". Without this an extension row would be stricter than an edge
    # about the same publisher's output. The `properties` branch of the helper
    # is a no-op here -- a row is flat, with no GeoJSON envelope.
    _drop_nulls = model_validator(mode="before")(staticmethod(drop_null_properties))


class LrsCrosswalk(ExtensionRow):
    """One row of `lrs.json`: a GATIS feature located on an external LRS segment.

    This is the only shape in GATIS that carries an *extent*.
    `lrs_starting_milepoint` and `lrs_ending_milepoint` with `lrs_side` can say
    that a thing runs from here to there along one side of a segment, which no
    core field can -- `buffer_width_ft`, `street_parking`,
    `street_parking_buffer_ft`, `separation_elements`, `shoulder_width_in` and
    `curb_height_in` are all scalars on a road edge, so a buffer has a width and
    nowhere to start or stop. The extent is reachable only against an external
    linear referencing system, so a publisher without one cannot express it at
    all. `docs/spec-review.md` recommendation 5.
    """

    gatis_id: str = Field(
        description="The identification number within GATIS for this piece of "
        "infrastructure."
    )

    geometry_type: Omitable[GatisGeometryType] = Field(
        description="The type of geospatial feature within GATIS of the infrastructure."
    )

    # `Type`, capitalised, is the name as printed. The events table spells the
    # same concept `type`. Exposed under one Python name so a caller can write
    # `row.feature_type` against either table.
    feature_type: Omitable[LrsFeatureType] = Field(
        alias="Type",
        description="The type of infrastructure. Valid values are any edge, node, "
        "point or zone types within GATIS.",
    )

    # Declared `Text` here, and `Array<Object>` on every core feature: the third
    # meaning this field name carries. Its own description asks for "all IDs
    # within a properly formatted list", so a list is accepted alongside the
    # declared scalar rather than rejected.
    reference_ids: Omitable[TextOrList] = Field(
        description="The identification number or other identifier of the related "
        "road segment within the linear referencing system. Can be the "
        "identification number within a government, commercial or third-party "
        "LRS. If multiple LRS segments align with a piece of infrastructure "
        "mapped in GATIS, provide all IDs within a properly formatted list."
    )

    lrs_source_url: Omitable[AnyUrl] = Field(
        description="The URL where the linear referencing system referenced in "
        "reference_ids can be found."
    )

    # Text, per the table. The events table types the same quantity as `Decimal`
    # (`lrs_milepoint`). Neither is coerced to the other; see
    # `test_milepoint_types_disagree_between_the_two_tables`.
    lrs_starting_milepoint: Omitable[str] = Field(
        description="The milepoint on the LRS segment at which this specific "
        "infrastructure begins."
    )

    lrs_ending_milepoint: Omitable[str] = Field(
        description="The milepoint on the LRS segment at which this specific "
        "infrastructure ends."
    )

    lrs_side: Omitable[LrsSide] = Field(
        description="The side of the LRS segment where this infrastructure "
        "appears. This tagging should align with the direction of the LRS "
        "segment, with the segment start point appearing at milepoint 0. It may "
        "contradict the directionality of the GATIS segment, which is assigned "
        "based on the order in which the geometry of the GATIS segment was drawn."
    )


class Event(ExtensionRow):
    """One row of `events.json`: something that happened to a piece of infrastructure.

    Construction, inspection, an ADA assessment, a repair, a removal. The table is
    designed to absorb what an agency's asset management system already holds --
    `work_order_id`, `costs`, `downtime`, `owner`, `maintainer` -- rather than to
    ask for new collection.
    """

    event_id: str = Field(
        description="The unique identifier for the event. If the event already "
        "has an ID assigned within another dataset, such as an agency asset "
        "management dataset, use that ID here as well."
    )

    # Declared `Datetime` and described as a date: "The date on which the event
    # occurred. Include time if available; if not, fill in time with zeroes." The
    # instruction to zero-fill makes the datetime form always satisfiable, so the
    # declared type stands.
    event_datetime: Omitable[GatisDatetime] = Field(
        description="The date on which the event occurred. Include time if "
        "available; if not, fill in time with zeroes."
    )

    event_type: Omitable[
        Annotated[
            str,
            SuggestedValues(
                "maintenance inspection",
                "ADA assessment",
                "other assessment",
                "data update",
                "complaint",
                "repair",
                "other maintenance work",
                "construction",
                "redesign",
                "removal",
                "other",
            ),
        ]
    ] = Field(
        description="The type of event that occurred. If multiple events occurred "
        "on the same day, break each out into a separate row. Recommended values: "
        "maintenance inspection; ADA assessment; other assessment; data update; "
        "complaint; repair; other maintenance work; construction; redesign; "
        "removal; other."
    )

    gatis_id: Omitable[str] = Field(
        description="The GATIS identification number for the piece of "
        "infrastructure, used in the edge, node, point or zone tables."
    )

    feature_type: Omitable[EventFeatureType] = Field(
        alias="type",
        description="The type of infrastructure. Valid values are any edge, node, "
        "point or zone types wtihin GATIS.",
    )

    geometry_type: Omitable[GatisGeometryType] = Field(
        description="The type of geospatial feature within GATIS of the infrastructure."
    )

    # Declared `Geometry (Point)` and described as accepting a line: "If
    # inspection of a sidewalk, include the full sidewalk edge coordinates."
    # A `GeometryTypeConstraint(POINT)` would reject what the specification
    # instructs, so the constraint is omitted and the contradiction reported.
    event_location: Omitable[Geometry] = Field(
        description="Geospatial point or edge location where the event occurred. "
        "If inspection of a sidewalk, include the full sidewalk edge coordinates. "
        "If repair, include the point location where the repair was carried out."
    )

    location_description: Omitable[str] = Field(
        description="Text description of the location where the event occurred."
    )

    lrs_segment_id: Omitable[str] = Field(
        description="If the event occurred along a segment represented in the "
        "infrastructure owner's linear referencing system, the identification "
        "number or other identifier of the LRS segment."
    )

    lrs_milepoint: Omitable[float64] = Field(
        description="If the event occurred along a segment represented in the "
        "infrastructure owner's linear referencing system, the milepoint at which "
        "the event occurred."
    )

    work_order_id: Omitable[str] = Field(
        description="The identification number of the work order or other "
        "identifier within the managing jurisdiction's data systems."
    )

    owner: Omitable[str] = Field(
        description="The entity that owns this piece of infrastructure. If a "
        "department, office or subagency is responsible for the infrastructure, "
        "list that department, office or subagency."
    )

    maintainer: Omitable[str] = Field(
        description="The entity that is responsible for maintaining this piece of "
        "infrastructure. It may or may not be the same as owner. If a department, "
        "office or subagency is responsible for the infrastructure, list that "
        "department, office or subagency."
    )

    # "If multiple, list all in list format" against a declared `Text`.
    executor_of_work: Omitable[TextOrList] = Field(
        description="The entity that carried out any work associated with this "
        "event. If multiple, list all in list format. The executor may be a "
        "contractor, or it may be the entity listed as owner or maintainer for "
        "the infrastructure."
    )

    inspector: Omitable[TextOrList] = Field(
        description="If an inspection, the name or names of the party or parties "
        "carrying out the inspection. This may be the name of an individual, a "
        "contractor or some other party. If multiple, list all in list format."
    )

    inspection_method: Omitable[
        Annotated[
            str,
            SuggestedValues(
                "visual inspection",
                "survey/audit",
                "satellite",
                "lidar",
                "other imagery",
                "other",
            ),
        ]
    ] = Field(
        description="The method used for inspecting the infrastructure. "
        "Recommended values: visual inspection; survey/audit; satellite; lidar; "
        "other imagery; other."
    )

    description: Omitable[str] = Field(
        description="A description of the event, to convey further detail of what "
        "was done. This may include listing construction or repair work "
        "activities and describing materials used, providing the specific ADA "
        "standard under which an assessment was carried out and conveying results "
        "or planned next steps, or providing information on redesign- or "
        "planning-related activities."
    )

    comments: Omitable[str] = Field(
        description="Any additional remarks or notes provided within the "
        "infrastructure owner's asset management dataset related to the event."
    )

    costs: Omitable[int32] = Field(
        description="The total amount spent on carrying out any work or "
        "inspections that were part of the event, rounded to the nearest whole "
        "number."
    )

    # No currency anywhere in the table or the Playbook, so a bare integer is all
    # a consumer gets. Reported in `docs/spec-review.md`.
    downtime: Omitable[str] = Field(
        description="The total amount of time related to the event during which "
        "the infrastructure was closed or inaccessible in whole or in part. "
        'Provide a value plus units - ex. "2 weeks", "3.5 days", "12 hours".'
    )

    related_issue: Omitable[Id] = Field(
        description="The GATIS ID for an issue point related to this event."
    )

    funding_source: Omitable[str] = Field(
        description="The source of funds for the construction, repair or other "
        "action taken as a part of the event."
    )


class Relation(ExtensionRow):
    """One row of `relations.json`: a link between two pieces of infrastructure.

    Two uses were designed for: tying a pushbutton or detector to the crossings it
    controls (`signal_id`, `crossing_id`), and describing a turning movement
    (`from_id`, `to_id`, `turning_treatment`). The Playbook says the table "may be
    used for any other purpose of relating two pieces of infrastructure."

    It has no extent and no side. That is the gap that keeps a GATIS publisher
    without an external LRS from saying where along an edge something applies --
    `LrsCrosswalk` has the milepoints, and it can only anchor them to a foreign
    segment.
    """

    relation_id: Id = Field(
        description="The identification number for the relation described in this row."
    )

    from_id: Omitable[IdOrList] = Field(
        description="For a relation that is a movement, the GATIS ID for the "
        "piece of infrastructure at which the movement begins."
    )

    to_id: Omitable[IdOrList] = Field(
        description="For a relation that is a movement, the GATIS ID for the "
        "piece of infrastructure at which the movement completes."
    )

    signal_id: Omitable[IdOrList] = Field(
        description="For a signal relation, the GATIS ID for the signal point. If "
        "multiple (ex. at the west and east ends of a crossing), provide all IDs "
        "in a list."
    )

    crossing_id: Omitable[IdOrList] = Field(
        description="For a signal relation, the GATIS ID for the crossing edge "
        "that is affected when the signal point under signal_id is interacted "
        "with by a traveler. If multiple, provide all IDs in a list."
    )

    turning_treatment: Omitable[
        Annotated[
            str,
            SuggestedValues(
                "bike box",
                "two-stage turn box",
                "protected intersection",
                "bike signal",
                "bike leading interval",
                "mixing zone",
                "scramble",
            ),
        ]
    ] = Field(
        description="For a relation that is a turning movement, any treatments at "
        "the intersection that are meant to facilitate the turn for travelers. "
        "Recommended values: bike box; two-stage turn box; protected "
        "intersection; bike signal; bike leading interval; mixing zone; scramble."
    )


# --------------------------------------------------------------------------
# Files
# --------------------------------------------------------------------------

LrsCrosswalkAdapter: TypeAdapter[list[LrsCrosswalk]] = TypeAdapter(list[LrsCrosswalk])
"""Validator for the rows of `lrs.json`."""

EventAdapter: TypeAdapter[list[Event]] = TypeAdapter(list[Event])
"""Validator for the rows of `events.json`."""

RelationAdapter: TypeAdapter[list[Relation]] = TypeAdapter(list[Relation])
"""Validator for the rows of `relations.json`."""


class LrsTable(BaseModel):
    """The contents of `lrs.json`.

    The envelope is a guess and is documented as one: section 2.1 gives the
    filename and the word JSON, nothing publishes a schema, and no sample exists.
    A bare array is what the Playbook's "each row" language implies, so
    `Dataset.load` reads either that or this single-key object.
    """

    lrs: list[LrsCrosswalk] = Field(default_factory=list)


class EventTable(BaseModel):
    """The contents of `events.json`. Envelope unspecified; see `LrsTable`."""

    events: list[Event] = Field(default_factory=list)


class RelationTable(BaseModel):
    """The contents of `relations.json`. Envelope unspecified; see `LrsTable`."""

    relations: list[Relation] = Field(default_factory=list)


EXTENSION_FILES: dict[str, str] = {
    "lrs": "lrs.json",
    "events": "events.json",
    "relations": "relations.json",
}
"""The three extension filenames section 2.1 declares."""


ExtensionName = Literal["lrs", "events", "relations"]
