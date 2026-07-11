#!/usr/bin/env python3
"""Render allocation forms and constraint notes consistently."""

from __future__ import annotations

from typing import Any

from validate_alloc import parse_range


def allocation_form_text(text: str) -> str:
    """Return only the instruction form, without legacy semicolon notes."""
    return str(text).split(";", 1)[0].strip()


def allocation_note_text(entry: Any) -> str:
    notes = allocation_notes(entry)
    return "; ".join(notes) if notes else "-"


def allocation_notes(entry: Any) -> list[str]:
    fields = _entry_get(entry, "fields", {}) or {}
    constraints = _entry_get(entry, "constraints", []) or []
    raw_notes = _entry_get(entry, "notes", []) or []

    out: list[str] = []
    for note in _as_note_list(raw_notes):
        _append_unique(out, note)

    for constraint in constraints:
        if not isinstance(constraint, dict):
            continue
        note = constraint_note(constraint, fields)
        if note:
            _append_unique(out, note)
    return out


def constraint_note(constraint: dict[str, Any], fields: dict[str, Any]) -> str:
    field = str(constraint.get("field", "") or "")
    reason = str(constraint.get("reason", "") or "")

    if "allow" in constraint:
        if field and reason == "register_direct_reclaimed":
            return f"{field} excludes register-direct EA forms"
        if field and reason == "sp_direct_reclaimed":
            return f"{field} excludes SP-direct EA form"
        if field and reason == "register_direct_and_sp_direct_reclaimed":
            return f"{field} excludes register-direct and SP-direct EA forms"
        if field and reason == "condition_true_false_reclaimed":
            return f"{field} excludes T and F condition codes"
        if field and reason == "condition_false_reclaimed":
            return f"{field} excludes F condition code"
        if field and reason == "zero_immediate_reclaimed":
            return f"{field} excludes zero"
        if field:
            width = _field_width(fields, field)
            label = _field_label(field, width)
            ranges = _range_list_text(constraint.get("allow") or [], width)
            return f"allow {label}={ranges}"
        return ""

    if "exclude" in constraint:
        predicate = str(constraint.get("exclude", ""))
        if reason == "user_source_memory_required":
            return "source must be memory"
        if reason == "user_destination_memory_required":
            return "destination must be memory"
        if constraint.get("destination") and predicate == "immediate":
            return "destination excludes immediate forms"
        if field:
            return f"{field} excludes {_predicate_text(predicate)}"
    return ""


def _predicate_text(predicate: str) -> str:
    if predicate in {"rn_direct", "reg_direct"}:
        return "register-direct EA forms"
    if predicate == "sp_direct":
        return "SP-direct EA form"
    if predicate == "immediate":
        return "immediate forms"
    return predicate.replace("_", " ")


def _entry_get(entry: Any, key: str, default: Any) -> Any:
    if isinstance(entry, dict):
        return entry.get(key, default)
    return getattr(entry, key, default)


def _as_note_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _append_unique(out: list[str], value: str) -> None:
    if value and value not in out:
        out.append(value)


def _field_width(fields: dict[str, Any], field: str) -> int:
    spec = fields.get(field)
    if isinstance(spec, dict):
        try:
            return int(spec.get("width", 0))
        except (TypeError, ValueError):
            return 0
    return 0


def _field_label(field: str, width: int) -> str:
    if len(field) == 1 and width > 1:
        return field * width
    return field


def _range_list_text(items: list[Any], width: int) -> str:
    return ",".join(_range_text(item, width) for item in items)


def _range_text(item: Any, width: int) -> str:
    lo, hi = parse_range(item)
    if width > 0:
        lo_text = f"{lo:0{width}b}"
        hi_text = f"{hi:0{width}b}"
    else:
        lo_text = f"0x{lo:x}"
        hi_text = f"0x{hi:x}"
    return lo_text if lo == hi else f"{lo_text}..{hi_text}"
