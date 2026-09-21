"""Bootstrap the Pydantic models from the vendored spec snapshot.

The output is a STARTING POINT, not a build artifact. `scripts/bootstrap-models`
writes it once; from then on the models under `gatis/models/` are hand-owned
source, refined in ways the workbook cannot express -- real descriptions,
tighter constraints, the relationships the spec only implies. Re-running the
bootstrap refuses to overwrite without `--force`; `--into` writes elsewhere so a
fresh snapshot can be diffed against the hand-edited models instead of
clobbering them.

Shape of the output, and why. Presence is `(feature class x feature type x field x
tier)`, and `forbidden` never varies by tier -- the field *partition* is fixed and
only presence strength moves. That licenses one `Feature` subclass per feature type,
joined by a discriminated union, which makes `forbidden` structural: a field
forbidden for a type is simply absent from that type's class. The tier axis is what
is left, and it rides along as a `Tier` annotation on each field.
"""

from __future__ import annotations

import datetime as dt
import keyword
import re
import subprocess
import textwrap
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from gatis.presence import Presence, PresenceRule
from gatis.spec_source import (
    FeatureClassSpec,
    FieldSpec,
    SpecReader,
    SpecSnapshot,
)

MODELS_DIR = Path(__file__).resolve().parent / "models"

GEOMETRY_TYPE = {
    "node": "POINT",
    "edge": "LINE_STRING",
    "point": "POINT",
    "zone": "POLYGON",
}

# v1.0 carries the unit in the field NAME -- `width_in`, `buffer_width_ft`,
# `posted_speed_limit_mph`, `crossing_time_sec`. That is a suffix match rather than
# a prose match, so it is read first and cannot drift with an edited description.
UNIT_SUFFIXES: dict[str, str] = {
    "in": "Inches",
    "ft": "Feet",
    "mph": "Mph",
    "sec": "Seconds",
}

# Dimensioned fields v1.0 left un-suffixed. Slopes and traffic volume carry their
# unit in prose only, so these still have to be read out of English.
UNIT_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"percentage of the slope|percent grade|expressed as a percent", "Percent"),
    (r"annual average daily traffic", "Aadt"),
)

# Array<Object> fields whose element shape the spec describes only in prose.
OBJECT_ELEMENTS = {
    "reference_ids": "ReferenceId",
    "gtfs_id": "GtfsReference",
    "seasonal": "SeasonalCondition",
}

# Cross-file foreign keys. `Reference` is declarative -- Overture does not enforce
# referential integrity either, since a segment and its connectors ship in separate
# partitions, exactly as GATIS edges and nodes do. The declaration is what makes the
# relationship machine-readable; `validate_dataset` does the enforcing.
REFERENCES: dict[tuple[str, str], tuple[str, str]] = {
    ("edge", "from_node"): ("NodeBase", "starts_at"),
    ("edge", "to_node"): ("NodeBase", "ends_at"),
}

# GATIS's only conditionally-required rule: each is required exactly when the other
# is set. Emitted as an `@all_or_none` decorator on any class carrying both.
CO_PRESENT = ("ada_compliance_date", "ada_compliant_with")

# The edge type that carries another facility as prefixed attributes. v1.0 marks
# sidewalk, bikeway and multi_use_path `allowed_on_road: true` and lists what each
# may not carry in that form, but it never names the type doing the carrying. It is
# the road: the mechanism exists so a roadway centerline can describe the sidewalk
# or bike lane beside it, and that is how the published sample data uses it.
ON_ROAD_CARRIER = "road"

# Generated enum names that would collide with a package symbol. `presence` is a
# GATIS field (does this infrastructure exist?) and is unrelated to the presence
# descriptors of document section 3.3.
ENUM_RENAMES = {"Presence": "FeaturePresence"}


@dataclass(frozen=True, slots=True)
class EnumValue:
    """One allowed value: the literal wire string, and how to name it in Python."""

    value: str
    description: str = ""

    @property
    def member(self) -> str:
        name = re.sub(r"[^a-z0-9]+", "_", self.value.lower()).strip("_").upper()
        name = re.sub(r"_+", "_", name)
        if not name or name[0].isdigit():
            name = f"V_{name}"
        return f"{name}_" if keyword.iskeyword(name.lower()) else name


def parse_listed_values(listed: Sequence[str]) -> list[EnumValue]:
    """The allowed values of an enumerated field.

    v1.0 publishes `listed_values` as an array, so there is nothing to split. What
    remains is that several entries carry a definition after a colon, and that
    upstream has no canonical token spelling -- values are display text ("under
    construction", "Buffered Bike Lane"). The literal string is kept: normalising
    here would fork the spec, since the display text is what published data uses.
    """
    values: list[EnumValue] = []
    seen: set[str] = set()
    for entry in listed:
        value, _, description = entry.strip().partition(":")
        value = " ".join(value.split())
        if not value or value.lower() in seen:
            continue
        seen.add(value.lower())
        values.append(EnumValue(value=value, description=" ".join(description.split())))
    return values if len(values) > 1 else []


def unit_alias(field: FieldSpec) -> str | None:
    """The unit annotation for a dimensioned field, or None.

    Name suffix wins: v1.0 made it machine-readable and prose did not keep up.
    """
    _, _, suffix = field.name.rpartition("_")
    alias = UNIT_SUFFIXES.get(suffix)
    if alias is None:
        for pattern, candidate in UNIT_PATTERNS:
            if re.search(pattern, field.description, re.I):
                alias = candidate
                break
    if alias is None:
        return None
    # A Float-typed inch field keeps the fractional width (upstream mixes both).
    if alias == "Inches" and field.type == "Float":
        return "InchesFloat"
    return alias


def enum_names(snapshot: SpecSnapshot) -> dict[tuple[str, str], str]:
    """Pick a Python class name for every enumerated field, avoiding collisions.

    Nine field names carry a DIFFERENT vocabulary on different feature classes --
    `status` has three (edges add "proposed and funded", nodes "planned", zones
    "other"), and `impediment`, `surface_issue`, `other_issue`, `presence`,
    `allowed_uses`, `prohibited_uses`, `surface_material` and `ada_compliant_with`
    all disagree too. Naming an enum after its field alone would let one class's
    values silently overwrite another's, so a field whose vocabularies differ is
    qualified by feature class (`EdgeStatus`, `NodeStatus`, `ZoneStatus`) and one
    that agrees everywhere keeps the short shared name.

    This is an upstream defect surfaced rather than absorbed: the same field name
    means different things depending on which file it appears in.
    """
    seen: dict[str, dict[str, tuple[str, ...]]] = {}
    for class_name, spec in snapshot.feature_classes.items():
        for field in spec.fields:
            # The discriminator becomes a `Literal`, never an enum class.
            if field.name == f"{class_name}_type":
                continue
            values = parse_listed_values(field.listed_values)
            if values and _is_enum(field):
                base = _class_name(field.name)
                seen.setdefault(base, {})[class_name] = tuple(v.value for v in values)

    names: dict[tuple[str, str], str] = {}
    for base, per_class in seen.items():
        collides = len(set(per_class.values())) > 1
        for class_name in per_class:
            chosen = _class_name(class_name) + base if collides else base
            names[(class_name, _field_from(base))] = ENUM_RENAMES.get(chosen, chosen)
    return names


def _field_from(class_name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()


class ClassWriter:
    """Renders one feature class into a module."""

    def __init__(
        self,
        spec: FeatureClassSpec,
        snapshot: SpecSnapshot,
        enum_names: dict[tuple[str, str], str] | None = None,
    ) -> None:
        self.spec = spec
        self.snapshot = snapshot
        self.name = spec.name
        self.enum_names = enum_names if enum_names is not None else {}
        self.enums: dict[str, list[EnumValue]] = {}
        self.uses_all_or_none = False
        self.uses_forbidden_on_road = False
        self.uses_suggested_values = False

    # -- fields ---------------------------------------------------------------

    def _fields_for(self, feature_type: str) -> list[tuple[FieldSpec, PresenceRule]]:
        chosen = []
        for field in self.spec.fields:
            rule = field.presence.get(feature_type)
            if rule is None or rule.base is Presence.FORBIDDEN:
                continue
            chosen.append((field, rule))
        return chosen

    def _base_type(self, field: FieldSpec, feature_type: str) -> tuple[str, list[str]]:
        extra: list[str] = []
        declared = field.type or "Text"
        is_array = declared.startswith(("Array<", "List<"))
        inner = declared[declared.index("<") + 1 : -1] if is_array else declared

        if field.name == f"{self.name}_type":
            base = f'Literal["{feature_type}"]'
        elif inner == "Enum":
            values = parse_listed_values(field.listed_values)
            if values:
                base = self.enum_names.get((self.name, field.name)) or ENUM_RENAMES.get(
                    _class_name(field.name), _class_name(field.name)
                )
                self.enums[base] = values
            else:
                base = "str"
        elif inner == "Object":
            base = OBJECT_ELEMENTS.get(field.name, "dict[str, object]")
        elif inner == "Boolean":
            base = "YesNo"
        elif inner == "Date":
            base = "GatisDate"
        elif inner == "Datetime":
            base = "GatisDatetime"
        elif inner == "ID":
            base = "Id"
        elif inner == "URL":
            base = "AnyUrl"
        elif inner in {"Float", "Integer"}:
            base = unit_alias(field) or ("float64" if inner == "Float" else "int32")
            if re.search(r"cannot be negative", field.description, re.I):
                extra.append("Field(ge=0)")
            elif re.search(r"greater than zero", field.description, re.I):
                extra.append("Field(gt=0)")
        else:
            base = "str"
            # A `Text` field with listed values: v1.0 publishes the vocabulary
            # and leaves the type open. Declaring it lets a transformation read
            # the values; the description keeps them for people.
            suggested = _open_vocabulary(field)
            if suggested:
                self.uses_suggested_values = True
                rendered = ", ".join(_literal(value.value) for value in suggested)
                base = f"Annotated[str, SuggestedValues({rendered})]"

        reference = REFERENCES.get((self.name, field.name))
        if reference is not None:
            target, role = reference
            extra.append(
                f'Reference(Relationship.ASSOCIATION, {target}, role="{role}")'
            )

        return (f"list[{base}]" if is_array else base), extra

    def _render_field(
        self, field: FieldSpec, rule: PresenceRule, feature_type: str
    ) -> list[str]:
        base, extra = self._base_type(field, feature_type)
        discriminator = field.name == f"{self.name}_type"
        required = discriminator or rule.at(1) is Presence.REQUIRED

        inner = base if required else f"Omitable[{base}]"
        metadata = [*extra, _tier_src(rule)]
        annotation = f"Annotated[{inner}, {', '.join(metadata)}]"

        description = " ".join(field.description.split())
        # Also in prose: `examples` serves machines, and the markdown target
        # renders only a constraint's class docstring, so without this the
        # reference docs would say a vocabulary exists without naming it. Both
        # copies are generated from `listed_values` in this pass, so neither
        # can drift from the other.
        suggested = _open_vocabulary(field)
        if suggested:
            values = "; ".join(value.value for value in suggested)
            description = (
                f"{description} Recommended values: {values}."
                if description
                else f"Recommended values: {values}."
            )
        assignment = (
            f" = Field(description={_literal(description)})" if description else ""
        )
        if discriminator and not description:
            assignment = ""

        # No field docstring: `Field(description=...)` already carries the text,
        # and a docstring beside it is the same sentence truncated.
        return [f"    {field.name}: {annotation}{assignment}", ""]

    def _render_on_road(self) -> list[str]:
        """The colon-namespaced attributes a road edge may carry for a parallel way.

        `sidewalk:left:width_in` and its 291 siblings: every non-forbidden field of
        each `allowed_on_road` type, on each side, minus that type's
        `forbidden_field_if_allowed_on_road` list. Always optional -- the spec
        assigns the modifier form no presence of its own.

        Modelled rather than left to `extra="allow"` because the two are not the
        same diagnostic. As extras these arrive untyped and indistinguishable from
        a local extension nobody has heard of, so a consumer reading Austin's
        roadway centerlines silently loses the bikeway on 4,003 of them while the
        validator calls the features clean.
        """
        lines: list[str] = []
        self.forbidden_on_road: list[str] = []
        for feature_type in self.spec.type_names:
            declaration = next(
                (t for t in self.spec.types if t.name == feature_type), None
            )
            if declaration is None or not declaration.allowed_on_road:
                continue
            forbidden = set(declaration.forbidden_on_road)
            known = set(self.spec.field_names)
            for side in ("left", "right"):
                self.forbidden_on_road.extend(
                    f"{feature_type}:{side}:{name}"
                    for name in declaration.forbidden_on_road
                    if name in known
                )
                for field, _ in self._fields_for(feature_type):
                    if field.name in forbidden:
                        continue
                    base, extra = self._base_type(field, feature_type)
                    metadata = [*extra, 'Tier("optional")']
                    alias = f"{feature_type}:{side}:{field.name}"
                    doc = _ON_ROAD_DOC % (feature_type, side, field.name)
                    lines.extend(
                        [
                            f"    {feature_type}_{side}_{field.name}: Annotated[",
                            f"        Omitable[{base}], {', '.join(metadata)}",
                            "    ] = Field(",
                            f'        alias="{alias}",',
                            f"        description={_literal(doc)},",
                            "    )",
                            "",
                        ]
                    )
        if lines:
            lines = [
                "",
                "    # The on-road modifier form: this road's parallel facilities,"
                " carried as",
                "    # prefixed attributes rather than as their own features. See"
                " section 2.2.",
                "",
                *lines,
            ]
        return lines

    # -- module ---------------------------------------------------------------

    def render(self) -> str:
        classes: list[str] = []
        members: list[tuple[str, str]] = []

        base_name = _class_name(self.name) + "Base"
        classes.append(self._render_base(base_name))

        # Declared types, not presence columns: v1.0 removed `virtual_link` from
        # `edges.json`'s `types` but left its presence column on all 78 attributes.
        # Generating from the columns would put a type back into the discriminated
        # union that the spec no longer allows. `fields_without_types` reports the
        # orphan instead.
        for feature_type in self.spec.type_names:
            class_name = _class_name(feature_type) + _class_name(self.name)
            members.append((feature_type, class_name))
            fields = [
                (field, rule)
                for field, rule in self._fields_for(feature_type)
                if field.name != f"{self.name}_id"
            ]
            names = {field.name for field, _ in fields}

            decorators = []
            if set(CO_PRESENT) <= names:
                self.uses_all_or_none = True
                decorators.append(f'@all_or_none("{CO_PRESENT[0]}", "{CO_PRESENT[1]}")')
            if self.name == "edge" and feature_type == ON_ROAD_CARRIER:
                self.uses_forbidden_on_road = True
                decorators.append(
                    f"@forbidden_on_road(*{class_name.upper()}_FORBIDDEN)"
                )

            description = next(
                (t.description for t in self.spec.types if t.name == feature_type), ""
            )
            body: list[str] = [
                *decorators,
                f"class {class_name}({base_name}):",
                *_docstring(_summarise(description) or feature_type),
                "",
            ]
            for field, rule in fields:
                body.extend(self._render_field(field, rule, feature_type))
            if self.name == "edge" and feature_type == ON_ROAD_CARRIER:
                on_road = self._render_on_road()
                if on_road:
                    classes.append(
                        f"{class_name.upper()}_FORBIDDEN = frozenset({{\n"
                        + "".join(
                            f'    "{alias}",\n'
                            for alias in sorted(self.forbidden_on_road)
                        )
                        + "})\n"
                    )
                    # The constant has to precede the class that references it.
                    classes.insert(-1, classes.pop())
                body.extend(on_road)
            body.append("")
            classes.append("\n".join(body))

        title = _class_name(self.name)
        if len(members) == 1:
            # A discriminated union needs two members; GATIS declares one zone type.
            union = [f"{title} = {members[0][1]}"]
        else:
            tagged = [f'Annotated[{cls}, Tag("{tag}")]' for tag, cls in members]
            union = [
                f"{title} = Annotated[",
                "    " + "\n    | ".join(tagged) + ",",
                "    Field(",
                "        discriminator=Feature.field_discriminator(",
                f'            "{self.name}_type",',
                *[f"            {cls}," for _, cls in members],
                "        )",
                "    ),",
                "]",
            ]
        union += [
            f'"""Any {self.name}, discriminated on `{self.name}_type`."""',
            "",
            f"{title}Adapter: TypeAdapter[{title}] = TypeAdapter({title})",
            f'"""Validator for one {self.name}, including from raw GeoJSON."""',
            "",
            "",
            f"class {title}Collection(BaseModel):",
            f'    """The contents of `{self.name}s.geojson`."""',
            "",
            '    type: Literal["FeatureCollection"] = "FeatureCollection"',
            f"    features: list[{title}]",
            "",
        ]

        return "\n".join(
            [
                _header(self.name, self.snapshot),
                self._imports(),
                "",
                "",
                *classes,
                *union,
            ]
        )

    def _render_base(self, base_name: str) -> str:
        """The shared base: a required, aliased identifier and the geometry type.

        `Identified` before `Feature` is load-bearing -- it is what makes `id`
        required rather than inheriting `Feature`'s `Omitable[Id]`. GATIS spells
        the identifier `<class>_id` inside `properties`, so it is aliased rather
        than carried twice; `serialize_by_alias` keeps the GATIS spelling on the
        way out, where the GeoJSON-canonical default would hoist a bare `id` to
        the top level.
        """
        id_field = next(
            (f for f in self.spec.fields if f.name == f"{self.name}_id"), None
        )
        description = " ".join(id_field.description.split()) if id_field else ""
        return "\n".join(
            [
                f"class {base_name}(Identified, Feature):",
                f'    """Common base for every GATIS {self.name} type."""',
                "",
                "    model_config = ConfigDict(",
                "        # Section 6.1 guarantees local extensibility: an unknown"
                " field warns,",
                "        # it does not fail. Extras land in `model_extra` and"
                " Feature's",
                "        # serializer routes them back through `properties`.",
                '        extra="allow",',
                "        populate_by_name=True,",
                "        serialize_by_alias=True,",
                "    )",
                "",
                "    geometry: Annotated[",
                "        Geometry,",
                f"        GeometryTypeConstraint("
                f"GeometryType.{GEOMETRY_TYPE[self.name]}),",
                "    ]",
                "    # An explicit `null` property means absent. See"
                " `drop_null_properties`;",
                "    # real GATIS data is overwhelmingly null-valued rather than"
                " sparse.",
                '    _drop_nulls = model_validator(mode="before")(',
                "        staticmethod(drop_null_properties)",
                "    )",
                "",
                "    # Redeclared from `Feature`, where it is `Omitable[Id]`, to"
                " make it",
                "    # mandatory. Same narrowing, and the same silencing, as"
                " Overture's own",
                "    # `OvertureFeature`.",
                '    id: Annotated[Id, Tier("required")] = Field(  '
                "# type: ignore[assignment]",
                f'        alias="{self.name}_id",',
                f"        description={_literal(description)},",
                "    )",
                "",
                "",
            ]
        )

    def _imports(self) -> str:
        lines = [
            "from __future__ import annotations",
            "",
            "from typing import Annotated, Literal",
            "",
            "from overture.schema.system.feature import Feature",
            "from overture.schema.system.geometric import (",
            "    Geometry,",
            "    GeometryType,",
            "    GeometryTypeConstraint,",
            ")",
            "from overture.schema.system.numeric import float64, int32",
            "from overture.schema.system.optionality import Omitable",
            "from overture.schema.system.ref import Id, Identified",
            "from pydantic import (",
            "    AnyUrl,",
            "    BaseModel,",
            "    ConfigDict,",
            "    Field,",
            "    Tag,",
            "    TypeAdapter,",
            "    model_validator,",
            ")",
            "",
            "from gatis.annotations import (",
            "    Aadt,",
            "    Feet,",
            "    Inches,",
            "    InchesFloat,",
            "    Mph,",
            "    Percent,",
            "    Seconds,",
            "    Tier,",
            ")",
        ]
        if any(key[0] == self.name for key in REFERENCES):
            lines[
                lines.index("from overture.schema.system.ref import Id, Identified")
            ] = (
                "from overture.schema.system.ref import (\n"
                "    Id,\n"
                "    Identified,\n"
                "    Reference,\n"
                "    Relationship,\n"
                ")"
            )
        helpers = ["drop_null_properties"]
        if self.uses_all_or_none:
            helpers.append("all_or_none")
        if self.uses_forbidden_on_road:
            helpers.append("forbidden_on_road")
        if self.uses_suggested_values:
            helpers.append("SuggestedValues")
        lines.append(
            "from gatis.constraints import (\n"
            + "".join(f"    {helper},\n" for helper in sorted(helpers))
            + ")"
        )
        lines.extend(
            [
                "from gatis.scalars import GatisDate, GatisDatetime, YesNo",
                "from gatis.shared import (",
                "    GtfsReference,",
                "    ReferenceId,",
                "    SeasonalCondition,",
                ")",
            ]
        )
        targets = sorted(
            {target for (cls, _), (target, _) in REFERENCES.items() if cls == self.name}
        )
        if targets:
            module = {"NodeBase": "nodes"}
            for target in targets:
                lines.append(f"from gatis.models.{module[target]} import {target}")
        if self.enums:
            lines.append("from gatis.models.enums import (")
            lines.extend(f"    {name}," for name in sorted(self.enums))
            lines.append(")")
        return "\n".join(lines)


_ON_ROAD_DOC = "The %s on the %s side of this road: see the %s field on that type."


def _open_vocabulary(field: FieldSpec) -> list[EnumValue]:
    """The values a `Text` field publishes without closing the set.

    Empty for an `Enum` (its class carries them), for a `Boolean` (`YesNo`
    does), and for the one `Float` whose cell holds a stray Word comment
    rather than a vocabulary.
    """
    declared = field.type or "Text"
    inner = declared[declared.index("<") + 1 : -1] if "<" in declared else declared
    if inner != "Text":
        return []
    return parse_listed_values(field.listed_values)


def _is_enum(field: FieldSpec) -> bool:
    declared = field.type or "Text"
    inner = declared[declared.index("<") + 1 : -1] if "<" in declared else declared
    return inner == "Enum"


def _tier_src(rule: PresenceRule) -> str:
    """Render a presence rule as the `Tier(...)` call that reproduces it."""
    base = f'"{rule.base.value}"'
    if not rule.upgrades:
        return f"Tier({base})"
    upgrades = ", ".join(
        f'{tier}: "{presence.value}"'
        for tier, presence in sorted(rule.upgrades.items())
    )
    return f"Tier({base}, {{{upgrades}}})"


# `ruff format` puts the first chunk of an implicit concatenation on the same line
# as the keyword that precedes it and the rest on their own lines, and how deep
# that sits depends on whether the field's `Annotated[...]` also had to split.
# Budget for the deeper case (12 spaces) so neither layout overflows 88 columns.
_INDENT = 12
_FIRST_CHUNK = 88 - _INDENT - len("description=") - 3
_NEXT_CHUNK = 88 - _INDENT - 3


def _literal(text: str) -> str:
    """A string literal, wrapped as implicit concatenation when it is long.

    `ruff format` lays implicit concatenation out across lines but never splits a
    single literal, so the break points have to come from here.
    """
    escaped = _escape(" ".join(text.split()))
    if len(escaped) <= _FIRST_CHUNK:
        return f'"{escaped}"'
    chunks = textwrap.wrap(
        escaped,
        width=_NEXT_CHUNK,
        initial_indent=" " * (_NEXT_CHUNK - _FIRST_CHUNK),
        break_long_words=False,
    )
    chunks[0] = chunks[0].lstrip()
    return " ".join(f'"{chunk} "' for chunk in chunks[:-1]) + f' "{chunks[-1]}"'


def _docstring(text: str, indent: str = "    ") -> list[str]:
    """A docstring, wrapped. `ruff format` does not reflow these either."""
    flat = _escape(" ".join(text.split()))
    if not flat:
        return []
    # The one-line form spends six columns on the two triple quotes.
    body = 88 - len(indent) - 6
    if len(flat) <= body:
        return [f'{indent}"""{flat}"""']
    # Wrapping to that same width guarantees at least two content lines. It has to:
    # `ruff format` pulls a lone closing `"""` back up onto a single content line,
    # which would reinstate the overflow this branch exists to avoid.
    lines = textwrap.wrap(
        flat, width=body, initial_indent="   ", break_long_words=False
    )
    lines[0] = lines[0].lstrip()
    return [
        f'{indent}"""{lines[0]}',
        *(f"{indent}{line}" for line in lines[1:]),
        f'{indent}"""',
    ]


def _class_name(token: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in token.split("_"))


def _escape(text: str) -> str:
    return text.replace("\\", "").replace('"', "'")


def _summarise(text: str) -> str:
    flat = " ".join(text.split())
    if not flat:
        return ""
    sentence = re.split(r"(?<=[.?!])\s", flat)[0].strip()
    return _escape(sentence)


def _header(name: str, snapshot: SpecSnapshot) -> str:
    return (
        f'"""GATIS {name} models.\n\n'
        "BOOTSTRAPPED by `gatis.codegen` from the pinned spec snapshot\n"
        f"(dotbts/BPA@{snapshot.spec_version[:8]}) on "
        f"{dt.date.today().isoformat()}.\n\n"
        "Hand-edits are expected and are not overwritten: the bootstrap refuses to\n"
        "rewrite an existing file without `--force`. Refine freely -- the published\n"
        "spec cannot express half of what these models should say.\n"
        '"""\n'
    )


def generate(
    snapshot: SpecSnapshot | None = None,
    out_dir: Path = MODELS_DIR,
    force: bool = False,
) -> tuple[list[Path], list[Path]]:
    """Write the bootstrap. Returns (written, skipped-because-present)."""
    snapshot = snapshot or SpecReader().load()
    if snapshot.defects:
        details = "\n".join(
            f"  {d.feature_class}.{d.field} [{d.column}]: {d.problem}"
            for d in snapshot.defects
        )
        raise ValueError(f"snapshot has unresolved defects:\n{details}")

    out_dir.mkdir(parents=True, exist_ok=True)
    names = enum_names(snapshot)
    writers = {
        name: ClassWriter(spec, snapshot, names)
        for name, spec in snapshot.feature_classes.items()
    }
    sources = {f"{name}s.py": writer.render() for name, writer in writers.items()}

    enums: dict[str, list[EnumValue]] = {}
    for writer in writers.values():
        enums.update(writer.enums)
    sources["enums.py"] = _render_enums(enums, snapshot)
    sources["__init__.py"] = _render_package(list(writers))

    written, skipped = [], []
    for filename, source in sources.items():
        path = out_dir / filename
        if path.exists() and not force:
            skipped.append(path)
            continue
        path.write_text(source if source.endswith("\n") else source + "\n")
        written.append(path)

    if written:
        _format(written)
    return written, skipped


def _format(paths: list[Path]) -> None:
    """Hand the output to ruff. Generated line breaks are a starting point only."""
    for command in (
        ["ruff", "check", "--fix-only", "--quiet", *map(str, paths)],
        ["ruff", "format", "--quiet", *map(str, paths)],
    ):
        subprocess.run(command, check=False)


def _render_enums(enums: dict[str, list[EnumValue]], snapshot: SpecSnapshot) -> str:
    parts = [
        '"""Enumerated values.\n\n'
        "BOOTSTRAPPED by `gatis.codegen` from the pinned spec snapshot\n"
        f"(dotbts/BPA@{snapshot.spec_version[:8]}).\n\n"
        "Each member's value is the literal display string the spec lists. GATIS\n"
        "defines no canonical token spelling, so normalising here would fork the "
        "spec.\n"
        '"""\n',
        "from __future__ import annotations",
        "",
        "from overture.schema.system.doc import DocumentedEnum",
        "",
        "",
    ]
    for name in sorted(enums):
        parts.append(f"class {name}(str, DocumentedEnum):")
        parts.append(f'    """Allowed values for `{_field_of(name)}`."""')
        parts.append("")
        for entry in enums[name]:
            value = _escape(entry.value)
            if entry.description:
                # DocumentedEnum takes (value, doc); several GATIS cells carry the
                # definition after a colon, which is exactly what belongs there.
                parts.append(
                    f"    {entry.member} = "
                    f"({_literal(value)}, {_literal(entry.description)})"
                )
            else:
                parts.append(f'    {entry.member} = "{value}"')
        parts.extend(["", ""])
    return "\n".join(parts).rstrip() + "\n"


def _field_of(enum_name: str) -> str:
    """The GATIS field an enum was generated for, from its class name."""
    field = re.sub(r"(?<!^)(?=[A-Z])", "_", enum_name).lower()
    if field == "feature_presence":
        return "presence"
    for prefix in ("edge_", "node_", "point_", "zone_"):
        if field.startswith(prefix) and field != f"{prefix.rstrip('_')}_type":
            return f"{field[len(prefix) :]} (on {prefix.rstrip('_')}s)"
    return field


def _render_package(names: list[str]) -> str:
    lines = [
        '"""GATIS models, bootstrapped by `gatis.codegen` then hand-refined."""\n',
        "from __future__ import annotations",
        "",
    ]
    exports: list[str] = []
    for name in names:
        title = _class_name(name)
        symbols = [title, f"{title}Adapter", f"{title}Base", f"{title}Collection"]
        lines.append(f"from gatis.models.{name}s import " + ", ".join(symbols))
        exports.extend(symbols)
    lines.extend(["", "__all__ = ["])
    lines.extend(f'    "{symbol}",' for symbol in sorted(exports))
    lines.append("]")
    return "\n".join(lines)
