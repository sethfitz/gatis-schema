"""Pydantic models for GATIS, generated from a pinned export of the upstream spec.

The specification's normative field tables live in a Google Sheet, not in the
specification document; see `spec/README.md`. `gatis_schema.spec_source` reads the
vendored snapshot of that sheet.
"""

__version__ = "0.1.0"

from gatis_schema.presence import TIERS, Presence, PresenceRule
from gatis_schema.spec_source import (
    FEATURE_CLASSES,
    SPEC_DIR,
    FeatureClassSpec,
    FeatureType,
    FieldSpec,
    Manifest,
    MetadataField,
    SourcePin,
    SpecDefect,
    SpecReader,
    SpecSnapshot,
)

__all__ = [
    "FEATURE_CLASSES",
    "SPEC_DIR",
    "TIERS",
    "FeatureClassSpec",
    "FeatureType",
    "FieldSpec",
    "Manifest",
    "MetadataField",
    "Presence",
    "PresenceRule",
    "SourcePin",
    "SpecDefect",
    "SpecReader",
    "SpecSnapshot",
    "__version__",
]
