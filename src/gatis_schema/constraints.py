"""Model-level constraints GATIS needs that the Overture system does not yet have."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from overture.schema.system._json_schema import (
    get_static_json_schema_extra,
    put_if,
    put_not,
    required_non_null,
)
from overture.schema.system.model_constraint import (
    ModelConstraint,
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


def drop_null_properties(data: Any) -> Any:
    """Treat an explicit JSON `null` as an absent property.

    GATIS says nothing about null-vs-omitted: `properties` is GeoJSON's untyped bag
    and the spec never distinguishes "known empty" from "not collected". Real data
    settles it in one direction -- Esri-derived exports write every unset field as
    an explicit null, and the two published sample datasets average 57% null slots
    per feature. Upstream's own JSON Schema permits null on 159 of 370 edge fields
    via `oneOf [..., {"type": "null"}]`, so rejecting it here would make these
    models stricter than the spec's own validator on the spec's own sample data.

    Nothing is lost by collapsing them, because GATIS assigns no meaning to the
    difference: `status` says a blank is assumed `open` (or `unknown`, depending on
    the feature class) whether it arrived as null or never arrived at all.
    """
    if not isinstance(data, dict):
        return data
    properties = data.get("properties")
    if isinstance(properties, dict):
        data = {
            **data,
            "properties": {k: v for k, v in properties.items() if v is not None},
        }
    return {
        k: v
        for k, v in data.items()
        if v is not None or k in {"geometry", "properties"}
    }


class ForbiddenOnRoadConstraint(ModelConstraint):
    """Refuse the colon-namespaced attributes a type may not carry in on-road form.

    v1.0 gives each `allowed_on_road` type a `forbidden_field_if_allowed_on_road`
    list -- `edge_id`, `edge_type`, `street_name`, `from_node`, `to_node`, `bridge`
    -- because those describe the road itself, not the facility beside it.

    Omitting them from the model is not the same as rejecting them. `extra="allow"`
    is mandatory here (section 6.1 makes local extension a guarantee), so an
    undeclared `bikeway:left:edge_id` lands in `model_extra` and validates
    silently: a publisher doing the one thing the spec explicitly forbids gets no
    signal. Section 6.1 is about fields nobody has heard of; this is a field the
    spec has heard of and ruled out, and the two want different diagnostics.

    Upstream expresses the same rule as *data* -- `edges_schema.json` enumerates
    the 292 permitted modifier properties and sets `additionalProperties: false`,
    so the prohibition is the absence from an enumerated set, with no code
    anywhere. That encoding is unavailable to us, because closing the property set
    would turn every local extension into a failure. A `ModelConstraint` is the
    nearest equivalent: unlike a `@model_validator` it carries a JSON Schema hook,
    so the rule reaches a consumer who reads the schema rather than importing this
    package -- which is the half that matters, since the schema is what a
    downstream validator consumes.

    What it does NOT buy, contrary to what `ModelConstraint`'s own docstring
    suggests: portability to the other codegen targets. That holds for constraints
    defined in the system package and not for a third-party subclass --
    `codegen/pyspark/constraint_dispatch.py` matches a closed set of vendor types
    and raises `TypeError` on ours, with no registry to opt into.
    `AllOrNoneConstraint` above has the same limitation. Upstream `bd-ic2h`.

    The names are aliases rather than field names -- they are deliberately not
    declared on the model -- so this subclasses `ModelConstraint` directly rather
    than `FieldGroupConstraint`, whose members must resolve to real fields.
    """

    def __init__(self, *aliases: str) -> None:
        if not aliases:
            raise ValueError("a forbidden-on-road constraint needs at least one alias")
        super().__init__(f"@forbidden_on_road/{len(set(aliases))}")
        self.__aliases = frozenset(aliases)

    @property
    def aliases(self) -> frozenset[str]:
        return self.__aliases

    def validate_instance(self, model_instance: BaseModel) -> None:
        super().validate_instance(model_instance)
        present = sorted(self.__aliases & set(model_instance.model_extra or {}))
        if present:
            raise ValueError(
                "forbidden in the on-road modifier form, because it describes the "
                f"road rather than the facility beside it: {', '.join(present)} "
                f"(`{self.name}`)"
            )

    def edit_config(self, model_class: type[BaseModel], config: ConfigDict) -> None:
        """Mirror the rule into JSON Schema: none of these names may be present."""
        super().edit_config(model_class, config)
        put_not(
            get_static_json_schema_extra(config),
            {"anyOf": [{"required": [alias]} for alias in sorted(self.__aliases)]},
        )


def forbidden_on_road(
    *aliases: str,
) -> Callable[[type[BaseModel]], type[BaseModel]]:
    """Decorate a model so the named on-road modifier attributes are refused."""
    return ForbiddenOnRoadConstraint(*aliases).decorate
