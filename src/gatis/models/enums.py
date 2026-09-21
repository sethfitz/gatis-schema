"""Enumerated values.

BOOTSTRAPPED by `gatis.codegen` from the pinned spec snapshot
(dotbts/BPA@ecc45ff8).

Each member's value is the literal display string the spec lists. GATIS
defines no canonical token spelling, so normalising here would fork the spec.
"""

from __future__ import annotations

from overture.schema.system.doc import DocumentedEnum


class AccessibilityFeatures(str, DocumentedEnum):
    """Allowed values for `accessibility_features`."""

    BRAILLE_MESSAGE = "braille_message"
    DETECTABLE_BASE = "detectable_base"
    AUDITORY_MESSAGE = "auditory_message"
    MULTILINGUAL = "multilingual"


class AllowedUses(str, DocumentedEnum):
    """Allowed values for `allowed_uses`."""

    WALK = "walk"
    BIKE = "bike"
    EBIKE_CLASS_1 = "ebike class 1"
    SCOOTER = "scooter"
    NEV = "NEV"
    MOTOR_VEHICLE = "motor_vehicle"
    EBIKE_CLASS_2 = "ebike class 2"
    EBIKE_CLASS_3 = "ebike class 3"
    OTHER = "other"


class BikewayGradeSeparation(str, DocumentedEnum):
    """Allowed values for `bikeway_grade_separation`."""

    AT_GRADE = "at_grade"
    RAISED = "raised"
    SIDEWALK_LEVEL = "sidewalk_level"


class Button(str, DocumentedEnum):
    """Allowed values for `button`."""

    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class CrossVehicleTrafficControl(str, DocumentedEnum):
    """Allowed values for `cross_vehicle_traffic_control`."""

    NO_VEHICLE_CONTROL = "no vehicle control"
    TRAFFIC_SIGNAL = "traffic signal"
    FLASHING_RED_LIGHT = "flashing red light"
    FLASHING_YELLOW_LIGHT = "flashing yellow light"
    YIELD_SIGN = "yield sign"
    STOP_SIGN = "stop sign"
    OTHER = "other"


class CurbType(str, DocumentedEnum):
    """Allowed values for `curb_type`."""

    RAISED = "raised"
    ROLLED = "rolled"
    FLUSH = "flush"
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


class EdgeAdaCompliantWith(str, DocumentedEnum):
    """Allowed values for `ada_compliant_with (on edges)`."""

    V_2010 = "2010"
    PROWAG = "PROWAG"


class EdgeStatus(str, DocumentedEnum):
    """Allowed values for `status (on edges)`."""

    OPEN = "open"
    CLOSED = "closed"
    UNDER_CONSTRUCTION = "under construction"
    PROPOSED_AND_FUNDED = "proposed and funded"
    PROPOSED_NOT_YET_FUNDED = "proposed - not yet funded"
    UNKNOWN = "unknown"


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
    LOW_OVERGROWTH_MORE_THAN_48_REMAINING = "low overgrowth (more than 48' remaining)"
    HIGH_OVERGROWTH_LESS_THAN_48_REMAINING = "high overgrowth (less than 48' remaining)"
    SIGN = "sign"
    LOW_PROTRUSION_MORE_THAN_48_REMAINING = "low protrusion (more than 48' remaining)"
    HIGH_PROTRUSION_LESS_THAN_48_REMAINING = "high protrusion (less than 48' remaining)"
    UTILITY_COVER = "utility cover"
    STORMWATER_GRATE = "stormwater grate"
    METAL_PLATE = "metal plate"
    METAL_DECKING_EX_ON_BRIDGES = "metal decking (ex. on bridges)"
    OTHER_SURFACE_IMPEDIMENT = "other surface impediment"
    OTHER_IMPEDIMENT = "other impediment"


class NodeAdaCompliantWith(str, DocumentedEnum):
    """Allowed values for `ada_compliant_with (on nodes)`."""

    V_2010 = "2010"
    PROWAG = "PROWAG"
    OTHER = "other"


class NodeStatus(str, DocumentedEnum):
    """Allowed values for `status (on nodes)`."""

    OPEN = "open"
    CLOSED = "closed"
    UNDER_CONSTRUCTION = "under construction"
    PLANNED = "planned"
    UNKNOWN = "unknown"


class NodeSurfaceIssue(str, DocumentedEnum):
    """Allowed values for `surface_issue (on nodes)`."""

    YES = "yes"
    NO = "no"
    CRACKING = "cracking"
    SCALING = "scaling"
    SPALLING = "spalling"
    UNEVEN_JOINTS = "uneven joints"
    DISPLACEMENT = "displacement"
    FREQUENT_WATER_POOLING = "frequent water pooling"
    HEAVING = "heaving"
    MISSING_BRICKS_STONES = "missing bricks/stones"
    POTHOLES_HOLES = "potholes/holes"
    SLICKNESS = "slickness"
    DETECTABLE_WARNING_SURFACE_DAMAGE = "detectable warning surface damage"
    LONGITUDINAL_CRACKS_AND_SEAMS = "longitudinal cracks and seams"
    METAL_PLATES = "metal plates"
    OTHER = "other"


class OtherIssue(str, DocumentedEnum):
    """Allowed values for `other_issue`."""

    YES = "yes"
    NO = "no"
    DETECTABLE_WARNING_NOT_ALIGNED_WITH_CROSSING = (
        "detectable warning not aligned with crossing"
    )
    PUSH_BUTTON_NOT_WORKING = "push button not working"
    MARKINGS_WORN = "markings worn"
    MARKINGS_MISSING = "markings missing"
    TURNING_SPACE_MISSING = "turning space missing"
    OTHER = "other"


class ParkingType(str, DocumentedEnum):
    """Allowed values for `parking_type`."""

    BICYCLE = "bicycle"
    SCOOTER = "scooter"
    EBIKE = "ebike"
    SHARED_SCOOTER = "shared scooter"
    SHARED_BICYCLE = "shared bicycle"
    SHARED_EBIKE = "shared ebike"
    OTHER = "other"
    OTHER_SHARED = "other shared"


class PedProtection(str, DocumentedEnum):
    """Allowed values for `ped_protection`."""

    SCRAMBLE_ALL_PEDESTRIAN_INTERVAL = "scramble / all pedestrian interval"
    LEADING_PEDESTRIAN_INTERVAL = "leading pedestrian interval"
    NO_RIGHT_ON_RED_FOR_MOTOR_VEHICLES = "no right on red for motor vehicles"
    AUTOMATIC_PEDESTRIAN_RECALL = "automatic pedestrian recall"
    HIGH_VISIBILITY_CROSSWALK_MARKINGS = "high visibility crosswalk markings"
    ENHANCED_CROSSWALK_LIGHTING = "enhanced crosswalk lighting"
    ADVANCE_STOP_YIELD_LINES = "advance stop / yield lines"
    ADDITIONAL_SIGNAGE = "additional signage"
    SUPPLEMENTAL_FLASHING_BEACON = "supplemental flashing beacon"
    OTHER = "other"
    NONE = "none"
    UNKNOWN = "unknown"


class PedTrafficControl(str, DocumentedEnum):
    """Allowed values for `ped_traffic_control`."""

    NO_PEDESTRIAN_CONTROL = "no pedestrian control"
    PEDESTRIAN_SIGNAL = "pedestrian signal"
    PEDESTRIAN_HYBRID_BEACON_HAWK = "pedestrian hybrid beacon / HAWK"
    RECTANGULAR_RAPID_FLASHING_BEACON = "rectangular rapid flashing beacon"
    UNKNOWN = "unknown"


class PointSurfaceIssue(str, DocumentedEnum):
    """Allowed values for `surface_issue (on points)`."""

    CRACKING = "cracking"
    SCALING = "scaling"
    SPALLING = "spalling"
    UNEVEN_DISPLACEMENT = "uneven / displacement"
    FREQUENT_WATER_POOLING = "frequent water pooling"
    HEAVING = "heaving"
    MISSING_BRICKS_STONES = "missing bricks / stones"
    GRATES_UTILITY_COVERS_OTHER_SURFACE_IMPEDIMENTS = (
        "grates / utility covers / other surface impediments"
    )
    POTHOLES_HOLES = "potholes / holes"
    SLICKNESS = "slickness"
    UNEVEN_JOINTS = "uneven joints"
    MARKINGS_WORN_MISSING = "markings worn / missing"
    DETECTABLE_WARNING_SURFACE_DAMAGE = "detectable warning surface damage"
    OTHER = "other"


class ProhibitedUses(str, DocumentedEnum):
    """Allowed values for `prohibited_uses`."""

    WALK = "walk"
    BIKE = "bike"
    EBIKE_CLASS_1 = "ebike class 1"
    SCOOTER = "scooter"
    NEV = "NEV"
    MOTOR_VEHICLE = "motor_vehicle"
    EBIKE_CLASS_2 = "ebike class 2"
    EBIKE_CLASS_3 = "ebike class 3"
    OTHER = "other"


class RailCrossingControl(str, DocumentedEnum):
    """Allowed values for `rail_crossing_control`."""

    GATES_AND_FLASHING_LIGHTS = "Gates and flashing lights"
    FLASHING_LIGHTS_ONLY = "flashing lights only"
    CROSSBUCKS_OR_STOP_SIGN_ONLY = "crossbucks or stop sign only"
    TACTILE_MARKINGS = "tactile markings"
    OTHER = "other"


class SeparationPermeableCar(str, DocumentedEnum):
    """Allowed values for `separation_permeable_car`."""

    HARD_SEPARATOR = "hard separator"
    SOFT_SEPARATOR = "soft separator"
    NONE = "none"


class StreetParking(str, DocumentedEnum):
    """Allowed values for `street_parking`."""

    PARALLEL = "parallel"
    ANGLED = "angled"
    FLOATING = (
        "floating",
        "Also known as parking protected. Put this value if present "
        "regardless if parking is parallel/angled parking.",
    )


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
    WOOD = "wood"
    OTHER = "other"


class TactileMarking(str, DocumentedEnum):
    """Allowed values for `tactile_marking`."""

    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class TrafficCalmingType(str, DocumentedEnum):
    """Allowed values for `traffic_calming_type`."""

    BULBOUT = "bulbout"
    CHOKER = "choker"
    CHICANE = "chicane"
    MINI_ROUNDABOUT = "mini roundabout"
    DIAGONAL_DIVERTER = "diagonal diverter"
    MEDIAN_BARRIER_FORCED_TURN_ISLAND = "median barrier/forced turn island"
    RAISED_INTERSECTION = "raised intersection"
    REALIGNED_INTERSECTION = "realigned intersection"
    SPEED_BUMP = "speed bump"
    SPEED_HUMP = "speed hump"
    SPEED_TABLE = "speed table"
    TRAFFIC_CIRCLE = "traffic circle"


class VehicleTrafficControl(str, DocumentedEnum):
    """Allowed values for `vehicle_traffic_control`."""

    NO_VEHICLE_CONTROL = "no vehicle control"
    TRAFFIC_SIGNAL = "traffic signal"
    FLASHING_RED_LIGHT = "flashing red light"
    FLASHING_YELLOW_LIGHT = "flashing yellow light"
    YIELD_SIGN = "yield sign"
    STOP_SIGN = "stop sign"
    OTHER = "other"


class ZoneStatus(str, DocumentedEnum):
    """Allowed values for `status (on zones)`."""

    OPEN = "open"
    CLOSED = "closed"
    UNDER_CONSTRUCTION = "under construction"
    OTHER = "other"
