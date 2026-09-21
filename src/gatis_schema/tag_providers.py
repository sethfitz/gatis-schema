"""Discovery tags for the models this package registers.

Overture's discovery system finds models through the `overture.models` entry
point group and labels them through `overture.tag_providers`. The system's own
provider adds `feature` to anything deriving from `Feature`, which covers the
four core classes and by design misses the three extension tables -- `lrs.json`,
`events.json` and `relations.json` are plain JSON rather than GeoJSON, so their
rows are `BaseModel`s. Untagged, they are discovered and then filtered out of
every `--tag feature` run, which is why `scripts/generate-reference` produced no
page for them.

This provider gives them one. `gatis:extension` marks a row of an extension
table, and `gatis:table=<name>` says which. The namespace is what makes them
ours: `:` signals ownership in Overture's tag grammar, and `overture` and
`system` are reserved to their own packages, so a third-party tag has to be
namespaced or it risks colliding with one the system may add later.
"""

from __future__ import annotations

from collections.abc import Iterable

from overture.schema.system.discovery import ModelKey
from pydantic import BaseModel

from gatis_schema.models.extensions import Event, ExtensionRow, LrsCrosswalk, Relation

EXTENSION_TAG = "gatis:extension"
"""Carried by every row model of an extension table."""

TABLE_TAG = "gatis:table"
"""Key of `gatis:table=<name>`, naming which of the three a model belongs to."""

_TABLES: dict[type[BaseModel], str] = {
    LrsCrosswalk: "lrs",
    Event: "events",
    Relation: "relations",
}


def gatis_provider(
    types: Iterable[type[BaseModel]],
    key: ModelKey,
    tags: set[str],
) -> set[str]:
    """Tag the extension-table rows among `types`.

    Parameters
    ----------
    types
        Concrete `BaseModel` subclasses behind one entry point. Overture walks a
        discriminated union to every arm before calling this, so a union of
        extension rows would tag correctly too.
    key
        Key identifying the model. Unused: the tag is decided by the class, not
        by what the entry point happened to be called.
    tags
        Tags added so far.

    Returns
    -------
    set[str]
        `tags`, plus `gatis:extension` and a `gatis:table=<name>` for each
        extension row found.
    """
    del key
    for model in types:
        if not (isinstance(model, type) and issubclass(model, ExtensionRow)):
            continue
        tags.add(EXTENSION_TAG)
        table = _TABLES.get(model)
        if table is not None:
            tags.add(f"{TABLE_TAG}={table}")
    return tags
