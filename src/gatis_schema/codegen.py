"""Bootstrap the Pydantic models from the vendored spec snapshot.

The output is a STARTING POINT, not a build artifact. `scripts/bootstrap-models`
writes it once; from then on the models under `gatis_schema/models/` are hand-owned
source, refined in ways the workbook cannot express -- real descriptions, tighter
constraints, the relationships the spec only implies. Re-running the bootstrap
refuses to overwrite without `--force`; `--into` writes elsewhere so a fresh
snapshot can be diffed against the hand-edited models instead of clobbering them.

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
from dataclasses import dataclass
from pathlib import Path

from gatis_schema.presence import Presence, PresenceRule
from gatis_schema.spec_source import (
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

# Units are stated only in field descriptions upstream. Read them once, here, so no
# consumer has to parse English. Mechanism follows Overture bead bd-uzbn option (b):
# annotate the primitive, leave the declared type alone.
UNIT_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"nearest inch|in inches|measured in inches", "Inches"),
    (r"in feet|nearest half foot", "Feet"),
    (r"percentage of the slope", "Percent"),
    (r"miles per hour", "Mph"),
    (r"annual average daily traffic", "Aadt"),
)

# Array<Object> fields whose element shape the spec describes only in prose.
OBJECT_ELEMENTS = {
    "reference_ids": "ReferenceId",
    "gtfs_id": "GtfsReference",
    "seasonal": "SeasonalCondition",
}

# GATIS's only conditionally-required rule: each is required exactly when the other
# is set. Emitted as an `@all_or_none` decorator on any class carrying both.
CO_PRESENT = ("ada_compliance_date", "ada_compliant_with")

# Generated enum names that would collide with a package symbol. `presence` is a
# GATIS field (does this infrastructure exist?) and is unrelated to the presence
# descriptors of document section 3.3.
ENUM_RENAMES = {"Presence": "FeaturePresence"}

# A Listed Values cell holding a cross-reference or an editorial note, not values.
_NOT_VALUES = re.compile(r"^\s*[\[(]")


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


def parse_listed_values(cell: str) -> list[EnumValue]:
    """Parse a Listed Values cell into its allowed values.

    Upstream has no canonical token spelling -- values are display text ("under
    construction", "Buffered Bike Lane") and sometimes carry a definition after a
    colon. The literal string is kept: normalising here would fork the spec, since
    the display text is what appears in published data.
    """
    if not cell.strip() or _NOT_VALUES.match(cell):
        return []

    # Newlines and pipes are the outer separator. Fall back to commas only when
    # neither appears, so a definition containing commas survives intact.
    chunks = [c for c in re.split(r"[\n|]", cell) if c.strip()]
    if len(chunks) == 1:
        chunks = cell.split(",")

    values: list[EnumValue] = []
    seen: set[str] = set()
    for chunk in chunks:
        value, _, description = chunk.strip().partition(":")
        value = " ".join(value.split())
        if not value or value.lower() in seen:
            continue
        seen.add(value.lower())
        values.append(EnumValue(value=value, description=" ".join(description.split())))
    return values if len(values) > 1 else []


def unit_alias(field: FieldSpec) -> str | None:
    for pattern, alias in UNIT_PATTERNS:
        if re.search(pattern, field.description, re.I):
            # Float-typed inch fields exist upstream (node.width); keep the width.
            if alias == "Inches" and field.type == "Float":
                return "InchesFloat"
            return alias
    return None


class ClassWriter:
    """Renders one feature class into a module."""

    def __init__(self, spec: FeatureClassSpec, snapshot: SpecSnapshot) -> None:
        self.spec = spec
        self.snapshot = snapshot
        self.name = spec.name
        self.enums: dict[str, list[EnumValue]] = {}
        self.uses_all_or_none = False

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
        elif inner == "Enum" or (inner == "Text" and field.valid == "Valid"):
            values = parse_listed_values(field.listed_values)
            if values:
                base = _class_name(field.name)
                base = ENUM_RENAMES.get(base, base)
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
        elif inner in {"Float", "Integer"}:
            base = unit_alias(field) or ("float64" if inner == "Float" else "int32")
            if re.search(r"cannot be negative", field.description, re.I):
                extra.append("Field(ge=0)")
            elif re.search(r"greater than zero", field.description, re.I):
                extra.append("Field(gt=0)")
        else:
            base = "str"

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

        description = _escape(" ".join(field.description.split()))
        if field.valid == "Recommended":
            suggested = parse_listed_values(field.listed_values)
            if suggested:
                values = _escape("; ".join(v.value for v in suggested))
                description = (
                    f"{description} Recommended values: {values}." if description
                    else f"Recommended values: {values}."
                )
        assignment = f' = Field(description="{description}")' if description else ""
        if discriminator and not description:
            assignment = ""

        # No field docstring: `Field(description=...)` already carries the text,
        # and a docstring beside it is the same sentence truncated.
        return [f"    {field.name}: {annotation}{assignment}", ""]

    # -- module ---------------------------------------------------------------

    def render(self) -> str:
        classes: list[str] = []
        members: list[tuple[str, str]] = []

        for feature_type in self.spec.presence_columns:
            class_name = _class_name(feature_type) + _class_name(self.name)
            members.append((feature_type, class_name))
            fields = self._fields_for(feature_type)
            names = {field.name for field, _ in fields}

            decorators = []
            if set(CO_PRESENT) <= names:
                self.uses_all_or_none = True
                decorators.append(f'@all_or_none("{CO_PRESENT[0]}", "{CO_PRESENT[1]}")')

            description = next(
                (t.description for t in self.spec.types if t.name == feature_type), ""
            )
            body: list[str] = [
                *decorators,
                f"class {class_name}(Feature):",
                f'    """{_summarise(description) or feature_type}"""',
                "",
                "    geometry: Annotated[",
                "        Geometry,",
                f"        GeometryTypeConstraint("
                f"GeometryType.{GEOMETRY_TYPE[self.name]}),",
                "    ]",
                "",
            ]
            for field, rule in fields:
                body.extend(self._render_field(field, rule, feature_type))
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
            "from overture.schema.system.ref import Id",
            "from pydantic import BaseModel, Field, Tag, TypeAdapter",
            "",
            "from gatis_schema.annotations import (",
            "    Aadt,",
            "    Feet,",
            "    Inches,",
            "    InchesFloat,",
            "    Mph,",
            "    Percent,",
            "    Tier,",
            ")",
        ]
        if self.uses_all_or_none:
            lines.append("from gatis_schema.constraints import all_or_none")
        lines.extend(
            [
                "from gatis_schema.scalars import GatisDate, GatisDatetime, YesNo",
                "from gatis_schema.shared import (",
                "    GtfsReference,",
                "    ReferenceId,",
                "    SeasonalCondition,",
                ")",
            ]
        )
        if self.enums:
            lines.append("from gatis_schema.models.enums import (")
            lines.extend(f"    {name}," for name in sorted(self.enums))
            lines.append(")")
        return "\n".join(lines)


def _tier_src(rule: PresenceRule) -> str:
    """Render a presence rule as the `Tier(...)` call that reproduces it."""
    base = f'"{rule.base.value}"'
    if not rule.upgrades:
        return f"Tier({base})"
    upgrades = ", ".join(
        f'{tier}: "{presence.value}"' for tier, presence in sorted(rule.upgrades.items())
    )
    return f"Tier({base}, {{{upgrades}}})"


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
        "BOOTSTRAPPED by `gatis_schema.codegen` from the pinned spec snapshot\n"
        f"(workbook Drive revision {snapshot.workbook_version}) on "
        f"{dt.date.today().isoformat()}.\n\n"
        "Hand-edits are expected and are not overwritten: the bootstrap refuses to\n"
        "rewrite an existing file without `--force`. Refine freely -- the workbook\n"
        "cannot express half of what these models should say.\n"
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
    writers = {
        name: ClassWriter(spec, snapshot)
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
    return written, skipped


def _render_enums(enums: dict[str, list[EnumValue]], snapshot: SpecSnapshot) -> str:
    parts = [
        '"""Enumerated values.\n\n'
        "BOOTSTRAPPED by `gatis_schema.codegen` from the pinned spec snapshot\n"
        f"(workbook Drive revision {snapshot.workbook_version}).\n\n"
        "Each member's value is the literal display string the workbook lists. GATIS\n"
        "defines no canonical token spelling, so normalising here would fork the spec.\n"
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
                    f'    {entry.member} = ("{value}", "{_escape(entry.description)}")'
                )
            else:
                parts.append(f'    {entry.member} = "{value}"')
        parts.extend(["", ""])
    return "\n".join(parts).rstrip() + "\n"


def _field_of(enum_name: str) -> str:
    """The GATIS field an enum was generated for, from its class name."""
    field = re.sub(r"(?<!^)(?=[A-Z])", "_", enum_name).lower()
    return "presence" if field == "feature_presence" else field


def _render_package(names: list[str]) -> str:
    lines = [
        '"""GATIS models, bootstrapped by `gatis_schema.codegen` then hand-refined."""\n',
        "from __future__ import annotations",
        "",
    ]
    exports: list[str] = []
    for name in names:
        title = _class_name(name)
        symbols = [title, f"{title}Adapter", f"{title}Collection"]
        lines.append(
            f"from gatis_schema.models.{name}s import "
            + ", ".join(symbols)  # noqa: FLY002
        )
        exports.extend(symbols)
    lines.extend(["", "__all__ = ["])
    lines.extend(f'    "{symbol}",' for symbol in sorted(exports))
    lines.append("]")
    return "\n".join(lines)
