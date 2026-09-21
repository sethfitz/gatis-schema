"""Model-level constraints GATIS needs that the Overture system does not yet have."""

from __future__ import annotations

from collections.abc import Callable

from overture.schema.system._json_schema import (
    get_static_json_schema_extra,
    put_if,
    required_non_null,
)
from overture.schema.system.model_constraint import (
    OptionalFieldGroupConstraint,
    apply_alias,
)
from pydantic import BaseModel, ConfigDict


class AllOrNoneConstraint(OptionalFieldGroupConstraint):
    """Require that a group of optional fields is either wholly set or wholly absent.

    This is GATIS's entire use of `conditionally_required`: `ada_compliance_date`
    and `ada_compliant_with` are each required exactly when the other is present.

    `overture.schema.system.model_constraint` has no equivalent. Its conditions are
    *value* conditions (`FieldEqCondition`, `Not`), so `require_if` expresses "if X
    equals v then Y is required" but not "if X is set at all". Built on the
    Overture base class rather than a bare `@model_validator` so it still carries
    the JSON Schema hooks and cross-target codegen the system provides. A
    presence condition upstream would retire this.
    """

    def __init__(self, *field_names: str) -> None:
        # The field names go in the constraint's name deliberately. A constraint
        # registers its validator under its name, so two constraints sharing one
        # name shadow each other on the same class -- silently, and only on the
        # Python side, while the metadata and the JSON Schema keep both.
        super().__init__(f"@all_or_none{field_names}", tuple(field_names))

    def validate_instance(self, model_instance: BaseModel) -> None:
        present = [
            name
            for name in self.field_names
            if self._field_has_non_none_value(model_instance, name)
        ]
        if not present or len(present) == len(self.field_names):
            return
        missing = [name for name in self.field_names if name not in present]
        raise ValueError(
            "these fields must be set together, but "
            f"{', '.join(missing)} {'is' if len(missing) == 1 else 'are'} "
            f"missing: {', '.join(self.field_names)}"
        )

    def edit_config(self, model_class: type[BaseModel], config: ConfigDict) -> None:
        """Mirror the rule into JSON Schema: any one set requires all of them."""
        super().edit_config(model_class, config)
        schema = get_static_json_schema_extra(config)
        aliases = [apply_alias(model_class, name) for name in self.field_names]
        for alias in aliases:
            put_if(schema, {"required": [alias]}, required_non_null(aliases))


def all_or_none(
    *field_names: str,
) -> Callable[[type[BaseModel]], type[BaseModel]]:
    """Decorate a model so the named optional fields are all set or all absent."""
    return AllOrNoneConstraint(*field_names).decorate
