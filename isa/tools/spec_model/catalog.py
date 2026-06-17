from __future__ import annotations

from typing import Any

from .core import SpecError

FAMILY_SECTION_TARGETS = {
    "compact_primary": ("compact_primary_instructions",),
    "integer": ("integer_instructions",),
    "system": ("atomic_system_cache_instructions",),
    "fpu": ("fpu", "instructions"),
}


FAMILY_SECTION_METADATA = {"description", "notes", "category", "registers"}


def instruction_catalog(spec: dict[str, Any]) -> dict[str, Any]:
    """Return the normalized declarative instruction catalog."""
    catalog = spec.get("instructions") or {}
    if isinstance(catalog, dict) and isinstance(catalog.get("families"), dict):
        return normalized_family_catalog(catalog)
    raise SpecError("instructions.yaml must define the current families-based instruction catalog")


def normalized_family_catalog(catalog: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {
        "compact_primary_instructions": {},
        "integer_instructions": {},
        "atomic_system_cache_instructions": {},
        "fpu": {},
    }
    for key in ("operand_schema", "canonical_aliases", "allocation"):
        if key in catalog:
            normalized[key] = catalog[key]

    for family_name, family in (catalog.get("families") or {}).items():
        if not isinstance(family, dict):
            continue
        family_category = str(family.get("category", ""))
        if "registers" in family:
            normalized.setdefault("fpu", {})["registers"] = family["registers"]
        for section_name, target_path in FAMILY_SECTION_TARGETS.items():
            entries = family_section_entries(
                family.get(section_name),
                family_name=str(family_name),
                family_category=family_category,
            )
            if not entries:
                continue
            target = normalized
            for part in target_path[:-1]:
                target = target.setdefault(part, {})
            target.setdefault(target_path[-1], {}).update(entries)

    normalized.setdefault("fpu", {}).setdefault("instructions", {})
    return normalized


def family_section_entries(
    section: Any, *, family_name: str = "", family_category: str = ""
) -> dict[str, Any]:
    if not isinstance(section, dict):
        return {}
    entries = section.get("entries")
    if isinstance(entries, dict):
        raw_entries = entries
    else:
        raw_entries = {
            str(key): value
            for key, value in section.items()
            if key not in FAMILY_SECTION_METADATA
        }
    out: dict[str, Any] = {}
    for key, value in raw_entries.items():
        if not isinstance(value, dict):
            out[str(key)] = value
            continue
        item = dict(value)
        if family_name:
            item.setdefault("semantic_family", family_name)
        if family_category:
            item.setdefault("semantic_category", family_category)
        out[str(key)] = item
    return out
