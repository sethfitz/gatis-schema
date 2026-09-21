"""Presence: whether a field may, must, or must not appear -- and at which tier.

GATIS presence is four-dimensional: (feature class x feature type x field x tier).
v1.0 publishes the tier axis as a four-element array, one slot per tier, where
``null`` means "unchanged from the tier before"::

    "sidewalk": ["optional", "required", null, null]

meaning optional at tier 1 and required at tiers 2-4. ``PresenceRule.at(tier)``
resolves it.
"""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum

from pydantic import BaseModel, Field

TIERS: tuple[int, ...] = (1, 2, 3, 4)


class Presence(str, Enum):
    """The presence descriptors GATIS v1.0 uses.

    Draft 2 also carried ``conditionally_required``; 1.0 dropped it in favour of
    ``recommended`` (upstream commit "update tables to drop conditionals",
    2026-01-30). Nothing in the v1.0 spec is conditionally required.
    """

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"
    FORBIDDEN = "forbidden"


class PresenceRule(BaseModel):
    """A field's presence for one feature type, across all four tiers."""

    base: Presence
    upgrades: dict[int, Presence] = Field(default_factory=dict)

    def at(self, tier: int) -> Presence:
        """Presence at `tier`: the last change at or below it, else the base."""
        if tier not in TIERS:
            raise ValueError(f"tier must be one of {TIERS}, got {tier!r}")
        applicable = [t for t in sorted(self.upgrades) if t <= tier]
        return self.upgrades[applicable[-1]] if applicable else self.base

    @property
    def is_uniform(self) -> bool:
        """True when the field's presence does not change across tiers."""
        return not self.upgrades

    @classmethod
    def parse(cls, slots: Sequence[str | None]) -> PresenceRule:
        """Parse one v1.0 presence array: four slots, `null` meaning carry-forward."""
        if len(slots) != len(TIERS):
            raise ValueError(f"presence needs {len(TIERS)} slots, got {slots!r}")
        if slots[0] is None:
            raise ValueError(f"presence has no tier-1 value: {slots!r}")

        base = Presence(_normalize(slots[0]))
        upgrades: dict[int, Presence] = {}
        for tier, slot in zip(TIERS[1:], slots[1:], strict=True):
            if slot is not None:
                upgrades[tier] = Presence(_normalize(slot))
        return cls(base=base, upgrades=upgrades)


def _normalize(token: str) -> str:
    return token.strip().lower().replace(" ", "_").replace("-", "_")
