"""Scalar types GATIS uses that need a conversion or a shape check.

Built on `overture-schema-system` so the generated models share Overture's
primitives, JSON Schema behaviour and codegen portability.
"""

from __future__ import annotations

from typing import Annotated, Any

from overture.schema.system.field_constraint import PatternConstraint
from pydantic import BeforeValidator, PlainSerializer

# GATIS booleans are OSM-style strings on the wire (document section 3.4, citing
# the OpenStreetMap boolean format). Parsed to `bool` in Python and written back as
# "yes"/"no", so a round-trip preserves the spec's encoding.
_TRUE = {"yes", "true", "1"}
_FALSE = {"no", "false", "0"}


def _parse_yes_no(value: Any) -> Any:
    if isinstance(value, str):
        token = value.strip().lower()
        if token in _TRUE:
            return True
        if token in _FALSE:
            return False
    return value


YesNo = Annotated[
    bool,
    BeforeValidator(_parse_yes_no),
    PlainSerializer(lambda v: "yes" if v else "no", return_type=str),
]
"""An OSM-format boolean: `"yes"` or `"no"` on the wire, `bool` in Python."""


# GATIS dates are RFC 3339, but deliberately truncatable: "Where possible, a date
# should contain the year, month, and day, but month and year can be used if day is
# not available." A `datetime.date` cannot hold that, so the partial forms are kept
# as validated strings.
GatisDate = Annotated[
    str,
    PatternConstraint(
        pattern=r"^\d{4}(-\d{2}(-\d{2})?)?$",
        error_message=(
            "invalid GATIS date: {value}. Must be YYYY, YYYY-MM or YYYY-MM-DD "
            "(RFC 3339, truncated on the right)."
        ),
    ),
]
"""An RFC 3339 date, optionally truncated to year or year-month."""

GatisDatetime = Annotated[
    str,
    PatternConstraint(
        pattern=r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$",
        error_message="invalid GATIS datetime: {value}. Must be RFC 3339.",
    ),
]
"""An RFC 3339 datetime."""
