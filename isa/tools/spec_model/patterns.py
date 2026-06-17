from __future__ import annotations

from typing import Any, Iterable
import json
import re

from .core import Pattern, PatternEntry, SpecError

def cleaned_pattern(raw: str) -> str:
    ignored = set(" \t\r\n_|")
    return "".join(ch for ch in raw if ch not in ignored)


def parse_pattern(raw: str, declared_fields: Iterable[str] = ()) -> Pattern:
    text = cleaned_pattern(raw)
    if not text:
        raise SpecError("empty pattern")

    declared = sorted({str(name) for name in declared_fields if name}, key=len, reverse=True)
    width = 0
    mask = 0
    value = 0
    fields: dict[str, int] = {}
    i = 0

    while i < len(text):
        ch = text[i]
        if ch in "01":
            width += 1
            mask = (mask << 1) | 1
            value = (value << 1) | (1 if ch == "1" else 0)
            i += 1
            continue
        if ch in "-?.":
            width += 1
            mask <<= 1
            value <<= 1
            i += 1
            continue
        if ch.isalpha():
            name = None
            for candidate in declared:
                if text.startswith(candidate, i):
                    name = candidate
                    break
            if name is None:
                name = ch
            bit_width = len(name)
            width += bit_width
            mask <<= bit_width
            value <<= bit_width
            fields[name] = fields.get(name, 0) + bit_width
            i += bit_width
            continue
        raise SpecError(f"invalid pattern character {ch!r} in {raw!r}")

    return Pattern(raw=raw, width=width, mask=mask, value=value, fields=fields)


def patterns_overlap(left: Pattern, right: Pattern) -> bool:
    shared_width = min(left.width, right.width)
    if shared_width <= 0:
        return False
    left_shift = left.width - shared_width
    right_shift = right.width - shared_width
    left_mask = left.mask >> left_shift
    right_mask = right.mask >> right_shift
    left_value = left.value >> left_shift
    right_value = right.value >> right_shift
    return ((left_value ^ right_value) & left_mask & right_mask) == 0


def pattern_dict(pattern: Pattern) -> dict[str, Any]:
    return {
        "raw": pattern.raw,
        "width": pattern.width,
        "mask": pattern.mask_hex(),
        "value": pattern.value_hex(),
        "fields": dict(sorted(pattern.fields.items())),
    }


def entry_dict(entry: PatternEntry) -> dict[str, Any]:
    return {
        "id": entry.id,
        "kind": entry.kind,
        "mnemonic": entry.mnemonic,
        "pattern": pattern_dict(entry.pattern),
        "length": entry.source.get("length"),
        "operands": entry.source.get("operands", []),
        "prefixes": entry.source.get("prefixes", []),
        "class": entry.source.get("class"),
        "privilege": entry.source.get("privilege"),
        "canonical": entry.source.get("canonical"),
        "alias_of": entry.source.get("alias_of"),
    }


def json_dumps(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def field_names(entry: dict[str, Any]) -> list[str]:
    fields = entry.get("fields") or {}
    if isinstance(fields, dict):
        return [str(name) for name in fields]
    return []


def entry_id(entry: dict[str, Any], default_id: str) -> str:
    return str(entry.get("id") or entry.get("name") or entry.get("mnemonic") or default_id)


def aliases_for(entry: PatternEntry) -> set[str]:
    names = {entry.id, entry.mnemonic}
    form = entry.source.get("form")
    if form:
        names.add(f"{entry.mnemonic}_{form}")
    return names


def overlap_allowed(left: PatternEntry, right: PatternEntry) -> bool:
    left_names = aliases_for(left)
    right_names = aliases_for(right)
    left_overlaps = {str(item) for item in left.source.get("overlaps", [])}
    right_overlaps = {str(item) for item in right.source.get("overlaps", [])}
    if left_overlaps & right_names or right_overlaps & left_names:
        return True
    if str(left.source.get("alias_of", "")) in right_names:
        return True
    if str(right.source.get("alias_of", "")) in left_names:
        return True
    return False


def length_bounds(entry: dict[str, Any]) -> tuple[int, int]:
    length = entry.get("length", {})
    if isinstance(length, int):
        return length, length
    if isinstance(length, dict):
        min_words = int(length.get("min_words", length.get("words", 1)))
        max_words = int(length.get("max_words", length.get("words", min_words)))
        return min_words, max_words
    return 1, 1


def operand_field_refs(entry: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for operand in entry.get("operands", []) or []:
        if isinstance(operand, dict) and operand.get("field"):
            refs.append(str(operand["field"]))
    size = entry.get("size")
    if isinstance(size, dict) and size.get("field"):
        refs.append(str(size["field"]))
    return refs
