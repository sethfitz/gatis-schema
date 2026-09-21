"""Pydantic models for GATIS, generated from a pinned copy of the published spec.

GATIS v1.0 is published as JSON in `dotbts/BPA`, not as a document; see
`spec/README.md`. `gatis.spec_source` reads the vendored snapshot.

`Dataset` and `IntegrityError` are resolved lazily. They live in `dataset`, which
imports the generated models -- and `scripts/bootstrap-models` has to import
`gatis.codegen` at a moment when those models do not exist yet. Eager imports
here made the package unbootstrappable from a clean tree.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

__version__ = "0.1.0"

from gatis.presence import TIERS, Presence, PresenceRule
from gatis.spec_source import (
    FEATURE_CLASSES,
    SPEC_DIR,
    FeatureClassSpec,
    FeatureType,
    FieldSpec,
    Manifest,
    MetadataField,
    Repair,
    RepairSet,
    SourcePin,
    SpecDefect,
    SpecReader,
    SpecSnapshot,
)

if TYPE_CHECKING:
    from gatis.dataset import Dataset, IntegrityError

_LAZY = {"Dataset": "dataset", "IntegrityError": "dataset"}


def __getattr__(name: str) -> Any:
    module_name = _LAZY.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    return getattr(import_module(f"{__name__}.{module_name}"), name)


__all__ = [
    "FEATURE_CLASSES",
    "SPEC_DIR",
    "TIERS",
    "Dataset",
    "FeatureClassSpec",
    "FeatureType",
    "FieldSpec",
    "IntegrityError",
    "Manifest",
    "MetadataField",
    "Presence",
    "PresenceRule",
    "Repair",
    "RepairSet",
    "SourcePin",
    "SpecDefect",
    "SpecReader",
    "SpecSnapshot",
    "__version__",
]
