"""GATIS models, bootstrapped by `gatis_schema.codegen` then hand-refined.

`extensions` is the exception: section 2.1's three extension tables have no
machine-readable source upstream, so those models are hand-written from
`spec/extensions.json`. See that module's docstring.
"""

from __future__ import annotations

from gatis_schema.models.edges import Edge, EdgeAdapter, EdgeBase, EdgeCollection
from gatis_schema.models.extensions import (
    EXTENSION_FILES,
    Event,
    EventAdapter,
    EventFeatureType,
    EventTable,
    ExtensionRow,
    GatisGeometryType,
    LrsCrosswalk,
    LrsCrosswalkAdapter,
    LrsFeatureType,
    LrsSide,
    LrsTable,
    Relation,
    RelationAdapter,
    RelationTable,
)
from gatis_schema.models.nodes import Node, NodeAdapter, NodeBase, NodeCollection
from gatis_schema.models.points import Point, PointAdapter, PointBase, PointCollection
from gatis_schema.models.zones import Zone, ZoneAdapter, ZoneBase, ZoneCollection

__all__ = [
    "EXTENSION_FILES",
    "Edge",
    "EdgeAdapter",
    "EdgeBase",
    "EdgeCollection",
    "Event",
    "EventAdapter",
    "EventFeatureType",
    "EventTable",
    "ExtensionRow",
    "GatisGeometryType",
    "LrsCrosswalk",
    "LrsCrosswalkAdapter",
    "LrsFeatureType",
    "LrsSide",
    "LrsTable",
    "Node",
    "NodeAdapter",
    "NodeBase",
    "NodeCollection",
    "Point",
    "PointAdapter",
    "PointBase",
    "PointCollection",
    "Relation",
    "RelationAdapter",
    "RelationTable",
    "Zone",
    "ZoneAdapter",
    "ZoneBase",
    "ZoneCollection",
]
