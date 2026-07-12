#!/usr/bin/env python3
"""Render allocation forms and constraints as compact structural data."""

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
    parts: list[str] = []
    if field:
        parts.append(f"field={field}")
    if constraint.get("destination"):
        parts.append("destination=true")
    if "allow" in constraint:
        width = _field_width(fields, field)
        parts.append(f"allow={_range_list_text(constraint.get('allow') or [], width)}")
    if "exclude" in constraint:
        parts.append(f"exclude={constraint.get('exclude', '')}")
    reason = str(constraint.get("reason", "") or "")
    if reason:
        parts.append(f"reason={reason}")
    return ", ".join(parts)


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
