"""Field-level metadata the generated models carry.

Neither `Unit` nor `Tier` participates in validation. They are declarations read by
consumers -- documentation, a tier-conformance check, an adapter converting GATIS to
another schema -- via `typing.get_type_hints(..., include_extras=True)`.

`Unit` follows the mechanism sketched on Overture bead bd-uzbn: annotate the numeric
primitive rather than newtyping it, so the declared type is unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, get_args, get_origin, get_type_hints

from overture.schema.system.numeric import float64, int32
from pydantic import BaseModel

from gatis_schema.presence import Presence, PresenceRule


@dataclass(frozen=True, slots=True)
class Unit:
    """A unit fixed by the schema for every value in this field.

    GATIS states all of these in prose only, and does not use one unit throughout:
    widths are inches, buffers and lengths are feet, slopes are percent.
    """

    symbol: str
    name: str = ""

    def __str__(self) -> str:
        return self.symbol


@dataclass(frozen=True, slots=True)
class Tier:
    """How this field's presence changes across the four GATIS tiers.

    Holds the workbook's presence cell for the one feature type this field's model
    represents; the `(field x feature type)` pair is already resolved by the class.
    Written as the base presence plus the tiers that upgrade it::

        Tier("optional", {3: "recommended", 4: "required"})
    """

    base: Presence
    upgrades: tuple[tuple[int, Presence], ...] = ()

    def __init__(
        self, base: str | Presence, upgrades: dict[int, str | Presence] | None = None
    ) -> None:
        object.__setattr__(self, "base", Presence(base))
        object.__setattr__(
            self,
            "upgrades",
            tuple(sorted((t, Presence(p)) for t, p in (upgrades or {}).items())),
        )

    def __str__(self) -> str:
        """A one-line rendering, used by the Overture markdown generator."""
        if not self.upgrades:
            return f"{self.base.value} at every tier"
        parts = [f"{self.base.value} from tier 1"]
        parts += [f"{p.value} from tier {t}" for t, p in self.upgrades]
        return "; ".join(parts)

    @property
    def rule(self) -> PresenceRule:
        return PresenceRule(base=self.base, upgrades=dict(self.upgrades))

    def at(self, tier: int) -> Presence:
        return self.rule.at(tier)

    @property
    def required_from(self) -> int | None:
        """Lowest tier at which this field is required, if ever."""
        return next(
            (t for t in (1, 2, 3, 4) if self.rule.at(t) is Presence.REQUIRED), None
        )


# Scalar aliases over the Overture numeric primitives. The unit is metadata, so
# `Inches` is still an `int32` to every consumer that does not ask for extras.
Inches = Annotated[int32, Unit("in", "inches")]
InchesFloat = Annotated[float64, Unit("in", "inches")]
Feet = Annotated[float64, Unit("ft", "feet")]
Percent = Annotated[float64, Unit("%", "percent")]
Mph = Annotated[int32, Unit("mph", "miles per hour")]
Aadt = Annotated[int32, Unit("AADT", "annual average daily traffic")]


def field_units(model: type[BaseModel]) -> dict[str, Unit]:
    """Every field on `model` that declares a unit."""
    return _annotations_of(model, Unit)


def field_tiers(model: type[BaseModel]) -> dict[str, Tier]:
    """Every field on `model` that declares tier presence."""
    return _annotations_of(model, Tier)


def _annotations_of(model: type[BaseModel], kind: type[Any]) -> dict[str, Any]:
    found = {}
    hints = get_type_hints(model, include_extras=True)
    for name in model.model_fields:
        for metadata in _unwrap(hints.get(name)):
            if isinstance(metadata, kind):
                found[name] = metadata
                break
    return found


def _unwrap(hint: Any) -> list[Any]:
    """Annotated metadata, looking through Optional and list."""
    if hint is None:
        return []
    if get_origin(hint) is Annotated:
        args = get_args(hint)
        return [*args[1:], *_unwrap(args[0])]
    return [item for arg in get_args(hint) for item in _unwrap(arg)]
