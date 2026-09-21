"""GATIS models, bootstrapped by `gatis_schema.codegen` then hand-refined."""

from __future__ import annotations

from gatis_schema.models.edges import Edge, EdgeAdapter, EdgeBase, EdgeCollection
from gatis_schema.models.nodes import Node, NodeAdapter, NodeBase, NodeCollection
from gatis_schema.models.points import Point, PointAdapter, PointBase, PointCollection
from gatis_schema.models.zones import Zone, ZoneAdapter, ZoneBase, ZoneCollection

__all__ = [
    "Edge",
    "EdgeAdapter",
    "EdgeBase",
    "EdgeCollection",
    "Node",
    "NodeAdapter",
    "NodeBase",
    "NodeCollection",
    "Point",
    "PointAdapter",
    "PointBase",
    "PointCollection",
    "Zone",
    "ZoneAdapter",
    "ZoneBase",
    "ZoneCollection",
]
