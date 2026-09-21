"""Presence: whether a field may, must, or must not appear -- and at which tier.

GATIS presence is four-dimensional: (feature class x feature type x field x tier).
The workbook encodes the tier axis inside a single cell as a base value followed by
zero or more upgrade lines::

    optional
    T3:recommended
    T4:required

meaning optional at tiers 1-2, recommended at tier 3, required at tier 4. A cell with
no upgrade lines holds at every tier.
"""

from __future__ import annotations

import re
from enum import Enum

from pydantic import BaseModel, Field

TIERS: tuple[int, ...] = (1, 2, 3, 4)

_UPGRADE = re.compile(r"^T(?P<tier>[1-4])\s*:\s*(?P<presence>.+)$")


class Presence(str, Enum):
    """The presence descriptors the workbook actually uses.

    Note the divergence from document section 3.3, which also defines
    "Conditionally Forbidden". No cell in the workbook uses it.
    """

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"
    CONDITIONALLY_REQUIRED = "conditionally_required"
    FORBIDDEN = "forbidden"


class PresenceRule(BaseModel):
    """A field's presence for one feature type, across all four tiers."""

    base: Presence
    upgrades: dict[int, Presence] = Field(default_factory=dict)

    def at(self, tier: int) -> Presence:
        """Presence at `tier`: the last upgrade at or below it, else the base."""
        if tier not in TIERS:
            raise ValueError(f"tier must be one of {TIERS}, got {tier!r}")
        applicable = [t for t in sorted(self.upgrades) if t <= tier]
        return self.upgrades[applicable[-1]] if applicable else self.base

    @property
    def is_uniform(self) -> bool:
        """True when the field's presence does not change across tiers."""
        return not self.upgrades

    @classmethod
    def parse(cls, cell: str) -> PresenceRule | None:
        """Parse one workbook cell. Returns None for a blank cell (unspecified)."""
        lines = [line.strip() for line in cell.splitlines() if line.strip()]
        if not lines:
            return None

        base = Presence(_normalize(lines[0]))
        upgrades: dict[int, Presence] = {}
        for line in lines[1:]:
            match = _UPGRADE.match(line)
            if match is None:
                raise ValueError(f"unparseable presence upgrade {line!r} in {cell!r}")
            upgrades[int(match["tier"])] = Presence(_normalize(match["presence"]))
        return cls(base=base, upgrades=upgrades)


def _normalize(token: str) -> str:
    return token.strip().lower().replace(" ", "_").replace("-", "_")
