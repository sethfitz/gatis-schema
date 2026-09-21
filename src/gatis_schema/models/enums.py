"""Enumerated values.

BOOTSTRAPPED by `gatis_schema.codegen` from the pinned spec snapshot
(workbook Drive revision 3542).

Each member's value is the literal display string the workbook lists. GATIS
defines no canonical token spelling, so normalising here would fork the spec.
"""

from __future__ import annotations

from overture.schema.system.doc import DocumentedEnum


class AdaCompliantWith(str, DocumentedEnum):
    """Allowed values for `ada_compliant_with`."""

    V_2010 = "2010"
    PROWAG = "PROWAG"


class AllowedUses(str, DocumentedEnum):
    """Allowed values for `allowed_uses`."""

    WALK = "walk"
    BIKE = "bike"
    EBIKE = "ebike"
    SCOOTER = "scooter"
    NEV = "NEV"
    MOTOR_VEHICLE = "motor_vehicle"


class BikewayGradeSeparation(str, DocumentedEnum):
    """Allowed values for `bikeway_grade_separation`."""

    AT_GRADE = "at_grade"
    RAISED = "raised"
    SIDEWALK_LEVEL = "sidewalk_level"


class CrossVehicleTrafficControl(str, DocumentedEnum):
    """Allowed values for `cross_vehicle_traffic_control`."""

    UNCONTROLLED = "uncontrolled"
    STANDARD_SIGNAL = "standard signal"
    FLASHING_RED_SIGNAL = "flashing red signal"
    FLASHING_YELLOW_SIGNAL = "flashing yellow signal"
    YIELD_SIGN = "yield sign"
    STOP_SIGN = "stop sign"


class CurbType(str, DocumentedEnum):
    """Allowed values for `curb_type`."""

    RAISED = "raised"
    ROLLED = "rolled"
    FLUSH = "flush"
    GENERIC = "generic"
    DRIVEWAY = "driveway"
    OTHER = "other"


class DetectableWarning(str, DocumentedEnum):
    """Allowed values for `detectable_warning`."""

    TACTILE_AND_CONTRASTED = "tactile and contrasted"
    TACTILE_AND_NOT_CONTRASTED = "tactile and not contrasted"
    NOT_TACTILE_AND_CONTRASTED = "not tactile and contrasted"
    NO = "no"


class Directionality(str, DocumentedEnum):
    """Allowed values for `directionality`."""

    FORWARD = "forward"
    BACKWARD = "backward"
    BOTH = "both"


class FeaturePresence(str, DocumentedEnum):
    """Allowed values for `presence`."""

    YES = "yes"
    NO = "no"
    MISSING = "missing"
    UNKNOWN = "unknown"


class Impediment(str, DocumentedEnum):
    """Allowed values for `impediment`."""

    YES = "yes"
    NO = "no"
    LOW_OVERGROWTH_LOWER_THAN_27 = "low overgrowth (lower than 27')"
    HIGH_OVERGROWTH_27_OR_HIGHER = "high overgrowth (27' or higher)"
    SIGN = "sign"
    LOW_PROTRUSION_LOWER_THAN_27 = "low protrusion (lower than 27')"
    HIGH_PROTRUSION_27_OR_HIGHER = "high protrusion (27' or higher)"
    UTILITY_COVER = "utility cover"
    STORMWATER_GRATE = "stormwater grate"
    METAL_PLATE = "metal plate"
    METAL_DECKING_EX_ON_BRIDGES = "metal decking (ex. on bridges)"
    OTHER_SURFACE_IMPEDIMENT = "other surface impediment"
    OTHER_IMPEDIMENT = "other impediment"


class PedProtection(str, DocumentedEnum):
    """Allowed values for `ped_protection`."""

    SCRAMBLE_ALL_PEDESTRIAN_INTERVAL = "scramble / all pedestrian interval"
    LEADING_PEDESTRIAN_INTERVAL = "leading pedestrian interval"
    NO_RIGHT_ON_RED = "no right on red"
    RAISED_SIDEWALK = "raised sidewalk"
    NONE = "none"
    UNKNOWN = "unknown"


class PedTrafficControl(str, DocumentedEnum):
    """Allowed values for `ped_traffic_control`."""

    UNCONTROLLED = "uncontrolled"
    STANDARD_SIGNAL = "standard signal"
    FLASHING_RED_SIGNAL = "flashing red signal"
    FLASHING_YELLOW_SIGNAL = "flashing yellow signal"
    PEDESTRIAN_HYBRID_BEACON_HAWK = "pedestrian hybrid beacon / HAWK"
    RECTANGULAR_RAPID_FLASHING_BEACON = "rectangular rapid flashing beacon"
    YIELD_SIGN = "yield sign"
    STOP_SIGN = "stop sign"


class ProhibitedUses(str, DocumentedEnum):
    """Allowed values for `prohibited_uses`."""

    WALK = "walk"
    BIKE = "bike"
    EBIKE = "ebike"
    SCOOTER = "scooter"
    NEV = "NEV"
    MOTOR_VEHICLE = "motor_vehicle"


class RailCrossing(str, DocumentedEnum):
    """Allowed values for `rail_crossing`."""

    GATES_AND_FLASHING_LIGHTS = "Gates and flashing lights"
    FLASHING_LIGHTS_ONLY = "flashing lights only"
    CROSSBUCKS_OR_STOP_SIGN_ONLY = "crossbucks or stop sign only"
    TACTILE_MARKINGS = "tactile markings"
    OTHER = "other"


class SeparationPermeableCar(str, DocumentedEnum):
    """Allowed values for `separation_permeable_car`."""

    HARD_SEPARATOR = ("hard separator", "the separator cannot be easily bypassed by motor vehicles (jersey barriers, curbs)")
    SOFT_SEPARATOR = ("soft separator", "the separator can be easily bypassed by motor vehicles (flex posts, k-rail)")
    NONE = ("none", "no separator is present (just paint separation)")


class Status(str, DocumentedEnum):
    """Allowed values for `status`."""

    OPEN = "open"
    CLOSED = "closed"
    UNDER_CONSTRUCTION = "under construction"
    OTHER = "other"


class StreetParking(str, DocumentedEnum):
    """Allowed values for `street_parking`."""

    PARALLEL = "parallel"
    ANGLED = "angled"
    FLOATING = ("floating", "Also known as parking protected. Put this value if present regardless if parking is parallel/angled parking.")


class SurfaceIssue(str, DocumentedEnum):
    """Allowed values for `surface_issue`."""

    CRACKING = "cracking"
    SCALING = "scaling"
    SPALLING = "spalling"
    UNEVEN_DISPLACEMENT = "uneven / displacement"
    FREQUENT_WATER_POOLING = "frequent water pooling"
    HEAVING = "heaving"
    MISSING_BRICKS_STONES = "missing bricks / stones"
    GRATES_UTILITY_COVERS_OTHER_SURFACE_IMPEDIMENTS = "grates / utility covers / other surface impediments"
    POTHOLES_HOLES = "potholes / holes"
    SLICKNESS = "slickness"
    UNEVEN_JOINTS = "uneven joints"
    MARKINGS_WORN_MISSING = "markings worn / missing"
    DETECTABLE_WARNING_SURFACE_DAMAGE = "detectable warning surface damage"
    OTHER = "other"


class SurfaceMaterial(str, DocumentedEnum):
    """Allowed values for `surface_material`."""

    ASPHALT = "asphalt"
    CONCRETE = "concrete"
    GRAVEL = "gravel"
    GRASS = "grass"
    DIRT = "dirt"
    PAVED = "paved"
    UNPAVED = "unpaved"
    GRASS_PAVER = "grass_paver"
    PAVING_STONES = "paving_stones"
    OTHER = "other"


class TactileMarking(str, DocumentedEnum):
    """Allowed values for `tactile_marking`."""

    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class VehicleTrafficControl(str, DocumentedEnum):
    """Allowed values for `vehicle_traffic_control`."""

    UNCONTROLLED = "uncontrolled"
    STANDARD_SIGNAL = "standard signal"
    FLASHING_RED_SIGNAL = "flashing red signal"
    FLASHING_YELLOW_SIGNAL = "flashing yellow signal"
    YIELD_SIGN = "yield sign"
    STOP_SIGN = "stop sign"
