"""Scalar types GATIS uses that need a conversion or a shape check.

Built on `overture-schema-system` so the generated models share Overture's
primitives, JSON Schema behaviour and codegen portability.
"""

from __future__ import annotations

from typing import Annotated

from overture.schema.system.field_constraint import PatternConstraint

from gatis_schema.constraints import YesNoConstraint

YesNo = Annotated[bool, YesNoConstraint()]
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
