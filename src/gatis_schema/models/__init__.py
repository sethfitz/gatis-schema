"""GATIS models, bootstrapped by `gatis_schema.codegen` then hand-refined."""

from __future__ import annotations

from gatis_schema.models.nodes import Node, NodeAdapter, NodeCollection
from gatis_schema.models.edges import Edge, EdgeAdapter, EdgeCollection
from gatis_schema.models.points import Point, PointAdapter, PointCollection
from gatis_schema.models.zones import Zone, ZoneAdapter, ZoneCollection

__all__ = [
    "Edge",
    "EdgeAdapter",
    "EdgeCollection",
    "Node",
    "NodeAdapter",
    "NodeCollection",
    "Point",
    "PointAdapter",
    "PointCollection",
    "Zone",
    "ZoneAdapter",
    "ZoneCollection",
]
