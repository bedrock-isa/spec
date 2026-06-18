#!/usr/bin/env python3
"""Generate instruction, operand, and encoding summary tables from allocation output."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any
import sys

sys.dont_write_bytecode = True

from isa_spec import cleaned_pattern, load_and_validate, print_result
from spec_model.encoding import (
    bitmap_operand_ranges,
    compact_ea_forms,
    compact_ea_values_by_name,
    named_values as spec_named_values,
    named_value_width,
    register_class_count,
    size_codes as spec_size_codes,
    size_kind_field,
    size_kind_entries,
    size_kind_suffixes,
    size_kinds as spec_size_kinds,
    special_register_class,
    special_register_named_values,
)


ACTIVE_SPEC: dict[str, Any] | None = None
DEFAULT_MAX_WORDS = 8
SELECTOR_SOURCES = {"count", "bit_index", "offset", "width"}


def set_active_spec(spec: dict[str, Any]) -> None:
    global ACTIVE_SPEC
    ACTIVE_SPEC = spec


def active_spec() -> dict[str, Any]:
    if ACTIVE_SPEC is None:
        raise RuntimeError("active ISA spec is not set")
    return ACTIVE_SPEC


def fixed_size_kinds() -> set[str]:
    return set(spec_size_codes(active_spec()))


def size_kind_names() -> set[str]:
    return set(spec_size_kinds(active_spec()))


def is_size_kind_name(kind: str) -> bool:
    return kind.upper() in size_kind_names()


def md(text: Any) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def bits_to_words(bits: int) -> int:
    return 0 if bits <= 0 else math.ceil(bits / 16)


def pattern_word_count(raw: str) -> int:
    return bits_to_words(len(cleaned_pattern(raw)))


def entry_lengths(entries: list[Any]) -> dict[tuple[str, str], tuple[int, int]]:
    out: dict[tuple[str, str], tuple[int, int]] = {}
    for entry in entries:
        length = entry.source.get("length") or {}
        if isinstance(length, int):
            bounds = (length, length)
        elif isinstance(length, dict):
            min_words = int(length.get("min_words", length.get("words", entry.pattern.word_count)))
            max_words = int(length.get("max_words", length.get("words", DEFAULT_MAX_WORDS)))
            bounds = (min_words, max_words)
        else:
            bounds = (entry.pattern.word_count, DEFAULT_MAX_WORDS)
        out[(entry.mnemonic, str(entry.source.get("pattern", "")))] = bounds
    return out


def allocation_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    if item.get("kind") in {"compact", "compact_alias"}:
        return (int(str(item["start_payload"]), 16), 0, str(item["id"]))
    opcode = str(item.get("extended_opcode_start", item.get("extended_opcode", "0x0000"))).split("..", 1)[0]
    return (
        int(str(item.get("extension_root_payload", "0x000")).split("..", 1)[0], 16),
        int(opcode, 16),
        str(item["id"]),
    )


def split_operand(operand: str) -> tuple[str, str]:
    if ":" in operand:
        name, typ = operand.split(":", 1)
        return name, typ
    return operand, operand


def operand_tokens(text: str) -> set[str]:
    return {part for part in re.split(r"[^A-Za-z0-9]+", text.upper()) if part}


def names_ea_operand(text: str) -> bool:
    upper = text.upper()
    tokens = operand_tokens(text)
    return (
        upper == "EA"
        or upper.startswith("EA_")
        or upper.endswith("_EA")
        or "EA" in tokens
        or upper in {"LINEAR_OR_EA", "EA_OR_RANGE", "EA_OR_D"}
    )


def is_implicit_unencoded_operand(operand: str, field: dict[str, Any] | None) -> bool:
    if field is not None:
        return False
    name, _typ = split_operand(operand)
    upper = name.upper()
    return (
        upper == "OUTPUTS"
        or upper.startswith("OUTPUT")
        or "_IN_" in upper
        or upper.startswith("LEAF_IN_")
        or upper.startswith("SUBLEAF_IN_")
    )


def field_for_operand(fields: list[dict[str, Any]], operand: str) -> dict[str, Any] | None:
    name, typ = split_operand(operand)
    candidates = [name, typ, operand]
    for field in fields:
        source = str(field.get("source", ""))
        if source in candidates:
            return field
    upper = operand.upper()
    for field in fields:
        kind = str(field.get("kind", "")).upper()
        if names_ea_operand(upper) and kind == "EA":
            return field
        if (upper in {"DBANK", "DATA_BANK", "DATA_REGISTER_BANK"} or "BANK" in upper) and kind == "DBANK":
            return field
        if upper.startswith("D") and kind == "DREG":
            return field
        if upper.startswith("A") and kind == "AREG":
            return field
        if upper.startswith("S") and kind == "SREG":
            return field
        if (upper in {"ORDER", "MEMORY_ORDER"} or "MEMORY_ORDER" in upper) and kind == "MEMORY_ORDER":
            return field
        if "CONDITION" in upper and kind == "CONDITION":
            return field
    return None


def infer_operand_kind(operand: str, field: dict[str, Any] | None) -> str:
    if field is not None:
        return str(field.get("kind", ""))
    name, typ = split_operand(operand)
    upper = typ.upper()
    source = name.upper()
    if "BITMAP" in upper or "BITMAP" in source:
        return "BITMAP16"
    if upper in {"MEMORY_ORDER", "MEMORYORDER", "ORDER"} or source in {"ORDER", "MEMORY_ORDER"}:
        return "memory_order"
    if "CONDITION" in upper or upper == "CC" or source == "CONDITION":
        return "condition"
    if upper in {"SP", "SPREG", "STACK_POINTER", "STACK_REGISTER"} or source in {"SP", "STACK_POINTER", "STACK_REGISTER"}:
        return "SPREG"
    if upper in {"DBANK", "DATA_BANK", "DATA_REGISTER_BANK"} or source in {"BANK", "SRC_BANK", "DST_BANK", "BANK_A", "BANK_B", "DBANK"}:
        return "DBANK"
    if upper in {"DREG", "DLO", "DX", "DHI"} or upper.startswith("D") or source.startswith("D"):
        return "DREG"
    if upper in {"AREG"} or upper.startswith("A") or source.startswith("A"):
        return "AREG"
    if upper in {"SREG", "SEGREG", "SEGMENT_REGISTER"} or source.startswith("SREG") or source.startswith("SEG"):
        return "SREG"
    if upper.startswith("F") or source.startswith("F"):
        return "FREG"
    if upper in {"IMM_EA", "IMMEDIATE_EA", "IMMEA", "IMMEDIATE_OPERAND_EA"}:
        return "IMM_EA"
    if names_ea_operand(typ) or names_ea_operand(name) or "MEMORY" in upper or "MEMORY" in source:
        return "EA"
    if upper in {"CR", "CREG", "CONTROL_REGISTER"} or source in {"CR", "CONTROL_REGISTER"}:
        return "CR"
    if "IMM64" in upper or "IMM64" in source:
        return "imm64"
    if "IMM32" in upper or "IMM32" in source:
        return "imm32"
    if "IMM16" in upper or "IMM16" in source:
        return "imm16"
    if upper in {"SELECTOR_IMM6", "IMM6_SELECTOR"}:
        return "selector6"
    if "IMM" in upper or "IMM" in source or source in {"TARGET", "VALUE"}:
        return "imm"
    if (
        "COUNT" in upper
        or "OFFSET" in upper
        or "WIDTH" in upper
        or "BIT_INDEX" in upper
        or upper in {"SELECTOR", "DREG_OR_IMM", "REG_OR_IMM", "SMALL_SELECTOR"}
    ):
        return "small_selector"
    return typ


def operand_placeholder(kind: str, operand: str) -> str:
    lower = kind.lower()
    name, _typ = split_operand(operand)
    if kind == "DREG":
        return "Dn"
    if kind == "DBANK":
        return "DBn"
    if kind == "AREG":
        return "An"
    if kind == "SPREG":
        return "SP"
    if kind == "SREG":
        return "Sreg"
    if kind == "FREG":
        return "Fn"
    if kind == "EA":
        return "<ea>"
    if kind == "IMM_EA":
        return "imm"
    if kind == "condition":
        return "cc"
    if kind == "memory_order":
        return "order"
    if kind == "BITMAP16" or kind == "bitmap16":
        return "<bitmap16>"
    if lower == "cr":
        return "<cr>"
    if "imm64" in lower:
        return "<imm64>"
    if "imm32" in lower:
        return "<imm32>"
    if "imm16" in lower:
        return "<imm16>"
    if "imm" in lower:
        return "<imm>"
    if kind in {"small_selector", "selector6"}:
        if name.lower() in SELECTOR_SOURCES:
            suffix = "imm6" if kind == "selector6" else "Dn|imm"
            return f"<{name}:{suffix}>"
        return "<n>"
    return f"<{name}>"


def size_text(fields: list[dict[str, Any]], ident: str) -> str:
    for field in fields:
        if field.get("source") == "size" or is_size_kind_name(str(field.get("kind"))):
            kind = str(field.get("kind"))
            if is_size_kind_name(kind):
                return "/".join(
                    str(item.get("code"))
                    for item in size_kind_entries(active_spec(), kind)
                    if item.get("code") is not None
                )
            if kind.upper() in fixed_size_kinds():
                return kind.upper()
    parts = ident.split(".")
    for part in parts:
        if part.upper() in size_kind_names() or part.upper() in fixed_size_kinds():
            return size_text([{"kind": part, "source": "size"}], ident)
    return "-"


def syntax_text(item: dict[str, Any]) -> str:
    fields = item.get("fields", [])
    size = size_text(fields, str(item["id"]))
    suffix = "" if size == "-" else (f".{size}" if size in fixed_size_kinds() else f".<{size}>")
    suffix += memory_order_suffix(fields, symbolic=False)
    raw_mnemonic = str(item["mnemonic"])
    mnemonic = display_mnemonic(raw_mnemonic)
    operands = []
    for operand in item.get("operands", []):
        field = field_for_operand(fields, str(operand))
        if is_implicit_unencoded_operand(str(operand), field):
            continue
        kind = infer_operand_kind(str(operand), field)
        if kind == "condition" and is_condition_mnemonic(raw_mnemonic):
            continue
        if kind == "memory_order":
            continue
        operands.append(operand_placeholder(kind, str(operand)))
    tail = "" if not operands else " " + ", ".join(operands)
    return f"{mnemonic}{suffix}{tail}"


def line_syntax_text(item: dict[str, Any], fields: list[dict[str, Any]]) -> str:
    size = size_field_text(fields, str(item["id"]))
    suffix = "" if not size else (f".{size}" if size in fixed_size_kinds() else f".X({size})")
    suffix += memory_order_suffix(fields, symbolic=True)
    raw_mnemonic = str(item["mnemonic"])
    mnemonic = display_mnemonic(raw_mnemonic)
    operands = []
    for operand in item.get("operands", []):
        field = field_for_operand(fields, str(operand))
        if is_implicit_unencoded_operand(str(operand), field):
            continue
        kind = infer_operand_kind(str(operand), field)
        if kind == "condition" and is_condition_mnemonic(raw_mnemonic):
            continue
        if kind == "memory_order":
            continue
        operands.append(line_operand_placeholder(kind, str(operand), field))
    tail = "" if not operands else " " + ", ".join(operands)
    return f"{mnemonic}{suffix}{tail}"


def memory_order_field(fields: list[dict[str, Any]]) -> dict[str, Any] | None:
    return next((field for field in fields if str(field.get("kind", "")) == "memory_order"), None)


def memory_order_suffix(fields: list[dict[str, Any]], *, symbolic: bool) -> str:
    field = memory_order_field(fields)
    if field is None:
        return ""
    if symbolic:
        return f"/ORDER({field_symbol(field)})"
    return "/<ORDER>"


def is_condition_mnemonic(mnemonic: str) -> bool:
    return mnemonic.lower().endswith("cc")


def display_mnemonic(mnemonic: str) -> str:
    return mnemonic


def size_field_text(fields: list[dict[str, Any]], ident: str) -> str:
    for field in fields:
        if field.get("source") == "size" or is_size_kind_name(str(field.get("kind"))):
            kind = str(field.get("kind"))
            values = "/".join(suffix.lstrip(".") for suffix in size_kind_suffixes(active_spec(), kind))
            return f"{field_symbol(field)}:{values}"
    for part in ident.split("."):
        upper = part.upper()
        if upper in size_kind_names() or upper in fixed_size_kinds():
            if upper in fixed_size_kinds():
                return part
            values = size_text([{"kind": upper, "source": "size"}], ident)
            return f"X:{values}"
    return ""


def line_operand_placeholder(kind: str, operand: str, field: dict[str, Any] | None) -> str:
    symbol = field_symbol(field) if field else ""
    suffix = f"({symbol})" if symbol else ""
    name, _typ = split_operand(operand)
    if kind == "DREG":
        return f"Dn{suffix}"
    if kind == "DBANK":
        return f"DBn{suffix}"
    if kind == "AREG":
        return f"An{suffix}"
    if kind == "SPREG":
        return "SP"
    if kind == "SREG":
        return f"Sreg{suffix}"
    if kind == "FREG":
        return f"Fn{suffix}"
    if kind == "EA":
        return f"<ea{suffix}>"
    if kind == "IMM_EA":
        return f"<imm{suffix}>"
    if kind == "condition":
        return f"cc{suffix}"
    if kind == "memory_order":
        return f"order{suffix}"
    if kind in {"BITMAP16", "bitmap16"}:
        return "<bitmap>"
    if kind.lower() == "cr":
        return "<cr>"
    if "imm64" in kind.lower():
        return "imm64"
    if "imm32" in kind.lower():
        return "imm32"
    if "imm16" in kind.lower():
        return "imm16"
    if "imm" in kind.lower():
        return "imm"
    if kind in {"small_selector", "selector6"}:
        return f"<{name}{suffix}>"
    return f"<{name}{suffix}>"


def operand_types_text(item: dict[str, Any]) -> str:
    fields = item.get("fields", [])
    out = []
    for operand in item.get("operands", []):
        name, _typ = split_operand(str(operand))
        field = field_for_operand(fields, str(operand))
        if is_implicit_unencoded_operand(str(operand), field):
            continue
        kind = infer_operand_kind(str(operand), field)
        if kind == "memory_order":
            continue
        out.append(f"{name}:{kind}")
    return ", ".join(out) if out else "-"


def field_layout_text(item: dict[str, Any]) -> str:
    if item.get("kind") in {"compact", "compact_alias"}:
        return str(item.get("field_layout", ""))
    return str(item.get("descriptor_layout", ""))


def field_symbol(field: dict[str, Any] | None) -> str:
    if not field:
        return ""
    source = str(field.get("source", ""))
    kind = str(field.get("kind", ""))
    source_symbols = {
        "quotient": "q",
        "remainder": "r",
        "offset": "o",
        "width": "w",
        "bit_index": "b",
        "lo": "l",
        "hi": "h",
        "value": "x",
        "lhs": "l",
        "rhs": "r",
        "expected": "x",
        "desired": "y",
        "order": "o",
        "constant_id": "i",
    }
    if kind != "EA" and source in source_symbols:
        return source_symbols[source]
    if kind == "FREG" and source == "dst":
        return "d"
    name = str(field.get("name", ""))
    if name:
        if len(name) > 1 and name[-1].isdigit():
            return name[0].upper()
        return name[0]
    if kind == "EA":
        return "e"
    if kind == "DREG":
        return "d"
    if kind == "DBANK":
        return "k"
    if kind == "AREG":
        return "a"
    if kind == "SREG":
        return "g"
    if kind == "FREG":
        return "f"
    if kind == "condition":
        return "c"
    if kind in {"small_selector", "selector6"}:
        return "n"
    if is_size_kind_name(kind):
        return size_kind_field(active_spec(), kind)
    return "x"


def field_display_name(field: dict[str, Any]) -> str:
    symbol = field_symbol(field)
    if symbol:
        return symbol
    return str(field.get("name", "x"))[:1]


def parse_range(text: str) -> tuple[int, int]:
    if ".." not in text:
        value = int(text, 16)
        return value, value
    start, end = text.split("..", 1)
    return int(start, 16), int(end, 16)


def parse_descriptor_layout(item: dict[str, Any]) -> list[dict[str, Any]]:
    if item.get("kind") in {"compact", "compact_alias"}:
        return [dict(field, token=0) for field in item.get("fields", []) if "low_bit" in field]
    original = [dict(field) for field in item.get("fields", [])]
    occurrence: dict[tuple[str, str], int] = {}
    by_kind: dict[str, list[dict[str, Any]]] = {}
    for field in original:
        by_kind.setdefault(str(field.get("kind", "")), []).append(field)
    placed: list[dict[str, Any]] = []
    layout = str(item.get("descriptor_layout", ""))
    if layout == "none":
        return []

    payload_token = 2
    payload_bit = 0

    def source_for(name: str, kind: str) -> str:
        key = (name.rstrip("0123456789").lower(), kind)
        index = occurrence.get(key, 0)
        occurrence[key] = index + 1
        candidates = by_kind.get(kind, [])
        if index < len(candidates):
            return str(candidates[index].get("source", name))
        return name

    for part in [piece.strip() for piece in layout.split(",") if piece.strip()]:
        if "@root" in part or "=" in part:
            continue
        match = re.match(
            r"(?P<name>[A-Za-z][A-Za-z0-9_]*):(?P<kind>[A-Za-z0-9_]+)\[(?P<range>\d+(?::\d+)?)\]",
            part,
        )
        if match:
            kind = match.group("kind")
            bit_range = match.group("range")
            if ":" in bit_range:
                high_text, low_text = bit_range.split(":", 1)
                high = int(high_text)
                low = int(low_text)
            else:
                high = low = int(bit_range)
            name = match.group("name")
            placed.append(
                {
                    "name": name,
                    "kind": kind,
                    "source": source_for(name, kind),
                    "storage": "descriptor",
                    "token": 1,
                    "width": high - low + 1,
                    "low_bit": low,
                    "high_bit": high,
                }
            )
            continue

        match = re.match(
            r"(?P<name>[A-Za-z][A-Za-z0-9_]*):(?P<kind>[A-Za-z0-9_]+)/(?P<width>\d+)@(?P<where>payload|ext)",
            part,
        )
        if not match:
            continue
        name = match.group("name")
        kind = match.group("kind")
        width = int(match.group("width"))
        where = match.group("where")
        if where == "ext":
            low = payload_bit
            high = low + width - 1
            payload_bit = high + 1
            token = 1
        else:
            if payload_bit + width > 16:
                payload_token += 1
                payload_bit = 0
            low = payload_bit
            high = low + width - 1
            payload_bit = high + 1
            token = payload_token
        placed.append(
            {
                "name": name,
                "kind": kind,
                "source": source_for(name, kind),
                "storage": "descriptor",
                "token": token,
                "width": high - low + 1,
                "low_bit": low,
                "high_bit": high,
            }
        )
    return placed


def line_fields(item: dict[str, Any]) -> list[dict[str, Any]]:
    return parse_descriptor_layout(item)


def bit_pattern(
    total_bits: int,
    start: int,
    end: int,
    fields: list[dict[str, Any]],
    *,
    fill: str = "0",
    exact_values: list[int] | None = None,
) -> str:
    chars = [fill] * total_bits
    field_by_bit: dict[int, dict[str, Any]] = {}
    for field in fields:
        if "low_bit" not in field or "high_bit" not in field:
            continue
        for bit in range(int(field["low_bit"]), int(field["high_bit"]) + 1):
            field_by_bit[bit] = field
    for bit in range(total_bits):
        field = field_by_bit.get(bit)
        if field is not None:
            chars[total_bits - 1 - bit] = field_display_name(field)
            continue
        if exact_values:
            values = {(value >> bit) & 1 for value in exact_values}
            chars[total_bits - 1 - bit] = str(next(iter(values))) if len(values) == 1 else "t"
        else:
            low_bit = (start >> bit) & 1
            high_bit = (end >> bit) & 1
            chars[total_bits - 1 - bit] = str(low_bit) if low_bit == high_bit else "t"
    return group_bits("".join(chars))


def group_bits(bits: str) -> str:
    return " ".join(bits[index : index + 4] for index in range(0, len(bits), 4))


def root_fields_for_item(item: dict[str, Any], root_start: int, root_end: int) -> list[dict[str, Any]]:
    if root_end - root_start + 1 != 16:
        return []
    if not any(str(field.get("kind")) == "condition" for field in item.get("fields", [])):
        return []
    return [
        {
            "name": "c",
            "kind": "condition",
            "source": "cc",
            "storage": "root",
            "width": 4,
            "low_bit": 0,
            "high_bit": 3,
        }
    ]


def payload_tokens(item: dict[str, Any], fields: list[dict[str, Any]]) -> list[str]:
    tokens: list[str] = []
    encoded_sources = {str(field.get("source", "")) for field in fields}
    for operand in item.get("operands", []):
        name, typ = split_operand(str(operand))
        if name in encoded_sources or typ in encoded_sources:
            continue
        kind = infer_operand_kind(str(operand), None)
        token = payload_token_for_kind(kind)
        if token and token not in tokens:
            tokens.append(token)
    return tokens


def payload_token_for_kind(kind: str) -> str:
    lower = kind.lower()
    if "bitmap" in lower:
        return "<bitmap>"
    if lower == "cr":
        return "<cr>"
    if "imm64" in lower:
        return "<imm64>"
    if "imm32" in lower:
        return "<imm32>"
    if "imm16" in lower:
        return "<imm16>"
    if "imm" in lower or "relative" in lower:
        return "<imm>"
    return ""


def encoding_pattern_tokens(item: dict[str, Any], fields: list[dict[str, Any]]) -> list[str]:
    if item.get("kind") in {"compact", "compact_alias"}:
        alias_payloads = item.get("alias_payloads") if item.get("kind") == "compact_alias" else None
        exact_payloads = alias_payloads or item.get("primary_payloads")
        if exact_payloads:
            payload_values = [
                int(str(value), 16)
                for value in exact_payloads
            ]
            start, end = min(payload_values), max(payload_values)
        else:
            start, end = parse_range(str(item["start_payload"]) if item["start_payload"] == item["end_payload"] else f"{item['start_payload']}..{item['end_payload']}")
        primary_fields = [field for field in fields if int(field.get("token", 0)) == 0]
        return ["---- " + bit_pattern(12, start, end, primary_fields, exact_values=payload_values if exact_payloads else None)]
    root_start, root_end = parse_range(str(item["extension_root_payload"]))
    root_fields = root_fields_for_item(item, root_start, root_end)
    ext_start, ext_end = parse_range(str(item["extended_opcode"]))
    descriptor_fields = [field for field in fields if int(field.get("token", 1)) == 1]
    tokens = [
        "---- " + bit_pattern(12, root_start, root_end, root_fields),
        bit_pattern(16, ext_start, ext_end, descriptor_fields),
    ]
    payload_tokens_by_index: dict[int, list[dict[str, Any]]] = {}
    for field in fields:
        token = int(field.get("token", 1))
        if token > 1:
            payload_tokens_by_index.setdefault(token, []).append(field)
    for token in sorted(payload_tokens_by_index):
        tokens.append(bit_pattern(16, 0, 0, payload_tokens_by_index[token], fill="-"))
    return tokens


def compact_hex_ranges(values: list[Any]) -> str:
    ints = sorted({int(str(value), 16) for value in values})
    if not ints:
        return ""
    ranges: list[tuple[int, int]] = []
    start = previous = ints[0]
    for value in ints[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append((start, previous))
        start = previous = value
    ranges.append((start, previous))
    parts = []
    for start, end in ranges:
        if start == end:
            parts.append(f"0x{start:03x}")
        else:
            parts.append(f"0x{start:03x}..0x{end:03x}")
    return ", ".join(parts)


def encoding_line(item: dict[str, Any]) -> str:
    fields = line_fields(item)
    tokens = encoding_pattern_tokens(item, fields)
    tokens.extend(payload_tokens(item, fields))
    pattern = " ".join(f"`{token}`" for token in tokens if token)
    return f"{pattern}: `{line_syntax_text(item, fields)}`"


def encoding_text(item: dict[str, Any]) -> str:
    if item.get("kind") == "compact":
        start = str(item["start_payload"])
        end = str(item["end_payload"])
        payload = start if start == end else f"{start}..{end}"
        if item.get("reclaimed_payloads"):
            reclaimed = compact_hex_ranges(item.get("reclaimed_payloads", []))
            return f"primary {payload}; reclaimed {reclaimed}"
        return f"primary {payload}"
    if item.get("kind") == "compact_alias":
        payloads = ", ".join(str(payload) for payload in item.get("alias_payloads", []))
        return f"alias_of={item['alias_of']}; condition={item.get('alias_condition', 'T')}; primary={payloads}"
    if item.get("kind") == "extended_alias":
        payloads = ", ".join(str(payload) for payload in item.get("alias_payloads", []))
        return (
            f"alias_of={item['alias_of']}; condition={item.get('alias_condition', 'T')}; "
            f"root={item['extension_root']}@{payloads}; ext={item['extended_opcode']}"
        )
    return (
        f"{item['extension_root']} @ {item['extension_root_payload']}; "
        f"ext {item['extended_opcode']}"
    )


def default_words(item: dict[str, Any], lengths: dict[tuple[str, str], tuple[int, int]]) -> tuple[int, int, str]:
    if item.get("kind") in {"compact", "compact_alias"}:
        if "min_words" in item and "max_words" in item:
            note = "alias_of=" + str(item["alias_of"]) if item.get("kind") == "compact_alias" else ""
            if not note:
                note = "ea_payload=variable" if has_ea_field(item) else "overlong=padding"
            return int(item["min_words"]), int(item["max_words"]), note
        key = (str(item["mnemonic"]), str(item.get("shape_hint", "")))
        if key in lengths:
            min_words, max_words = lengths[key]
        elif item.get("shape_hint"):
            min_words = pattern_word_count(str(item["shape_hint"]))
            max_words = DEFAULT_MAX_WORDS
        else:
            min_words, max_words = 1, DEFAULT_MAX_WORDS
        note = "ea_payload=variable" if has_ea_field(item) else "overlong=padding"
        return min_words, max_words, note
    words = 2 + int(item.get("operand_descriptor_words", 0))
    if item.get("kind") == "extended_alias":
        note = "alias_of=" + str(item["alias_of"])
    else:
        note = "encoding=primary_root+extended_opcode"
    if int(item.get("operand_descriptor_words", 0)) and item.get("kind") != "extended_alias":
        note += "; descriptor=present"
    if has_ea_field(item):
        note += "; ea_payload=variable"
    return words, DEFAULT_MAX_WORDS, note


def has_ea_field(item: dict[str, Any]) -> bool:
    return any(str(field.get("kind")) == "EA" for field in item.get("fields", []))


def instruction_rows(plan: dict[str, Any], lengths: dict[tuple[str, str], tuple[int, int]]) -> list[dict[str, Any]]:
    rows = []
    allocations = [
        item for item in plan["solver"]["primary_allocations"] if item.get("kind") == "compact"
    ] + list(plan["solver"].get("primary_alias_allocations", [])) + list(plan["solver"]["extended_allocations"]) + list(plan["solver"].get("extended_alias_allocations", []))
    for item in sorted(allocations, key=allocation_sort_key):
        if item.get("kind") == "extension_root":
            continue
        min_words, max_words, note = default_words(item, lengths)
        rows.append(
            {
                "mnemonic": item["mnemonic"],
                "form": item["id"],
                "syntax": syntax_text(item),
                "operands": operand_types_text(item),
                "size": size_text(item.get("fields", []), str(item["id"])),
                "default_words": min_words,
                "max_words": max_words,
                "encoding": encoding_text(item),
                "fields": field_layout_text(item),
                "note": note,
            }
        )
    return rows


def sreg_names(spec: dict[str, Any]) -> list[str]:
    return [name for name, _value in special_register_named_values(spec, "S")]


def operand_type_rows(plan: dict[str, Any], spec: dict[str, Any]) -> list[dict[str, str]]:
    seen: dict[str, dict[str, str]] = {}
    allocations = (
        plan["solver"]["primary_allocations"]
        + plan["solver"].get("primary_alias_allocations", [])
        + plan["solver"]["extended_allocations"]
        + plan["solver"].get("extended_alias_allocations", [])
    )
    for item in allocations:
        if item.get("kind") == "extension_root":
            continue
        fields = item.get("fields", [])
        for operand in item.get("operands", []):
            field = field_for_operand(fields, str(operand))
            if is_implicit_unencoded_operand(str(operand), field):
                continue
            kind = infer_operand_kind(str(operand), field)
            if kind in seen:
                continue
            seen[kind] = {
                "type": kind,
                "syntax": operand_placeholder(kind, str(operand)),
                "encoding": operand_encoding_summary(kind, spec),
                "default_words": operand_default_words(kind),
                "notes": operand_notes(kind, spec),
            }
    return [seen[key] for key in sorted(seen)]


def operand_encoding_summary(kind: str, spec: dict[str, Any] | None = None) -> str:
    spec = spec or active_spec()
    compact_ea_width = max(compact_ea_values_by_name(spec).values()).bit_length()
    if kind == "DREG":
        return f"{max(1, (register_class_count(spec, 'D') - 1).bit_length())}-bit D register field"
    if kind == "AREG":
        return f"{max(1, (register_class_count(spec, 'A') - 1).bit_length())}-bit A register field"
    if kind == "SPREG":
        return "implicit SP register operand"
    if kind == "SREG":
        names = sreg_names(spec)
        bits = int(special_register_class(spec, "S").get("encoding_bits", 0))
        suffix = "" if len(names) >= (1 << bits) else "; remaining values reserved"
        return f"{bits}-bit S segment-register field ({'/'.join(names)}{suffix})"
    if kind == "FREG":
        return f"{max(1, (register_class_count(spec, 'F') - 1).bit_length())}-bit F register field"
    if kind == "EA":
        return f"{compact_ea_width}-bit compact EA selector; extended escapes to extended EA descriptor"
    if kind == "IMM_EA":
        return f"{compact_ea_width}-bit compact EA selector restricted to immediate forms"
    if kind == "condition":
        return "4-bit condition field"
    if kind == "memory_order":
        return f"{named_value_width(spec, 'memory_order')}-bit atomic memory-order field"
    if kind in {"BITMAP16", "bitmap16"}:
        width = int((spec.get("instructions", {}).get("operand_schema", {}).get("bitmap_operands", {}).get("bitmap16", {}) or {}).get("width", 0))
        return f"{width}-bit register bitmap payload"
    if kind == "selector6":
        return "6-bit immediate selector field carrying values 0..63"
    if kind == "small_selector":
        return "3- or 4-bit selector field; count/bit_index/offset/width may select D register or immediate"
    if "cr" in kind.lower():
        return "16-bit control-register selector"
    if "imm64" in kind.lower():
        return "64-bit immediate payload"
    if "imm32" in kind.lower():
        return "32-bit immediate payload"
    if "imm16" in kind.lower():
        return "16-bit immediate payload"
    if "imm" in kind.lower():
        return "immediate payload or EA IMM form"
    return "descriptor or payload field"


def operand_default_words(kind: str) -> str:
    if kind in {"DREG", "AREG", "SPREG", "SREG", "FREG", "condition", "small_selector", "selector6", "memory_order"}:
        return "+0 when packed in primary/descriptor"
    if kind == "EA":
        return "+0 for register/simple EA; varies by EA form"
    if kind == "IMM_EA":
        return "varies by selected immediate EA form"
    if kind in {"BITMAP16", "bitmap16"}:
        return "+1"
    if "imm64" in kind.lower():
        return "+4"
    if "imm32" in kind.lower():
        return "+2"
    if "imm16" in kind.lower():
        return "+1"
    if kind.lower() == "cr" or "imm" in kind.lower():
        return "+1 or instruction-defined"
    return "varies"


def operand_notes(kind: str, spec: dict[str, Any] | None = None) -> str:
    spec = spec or active_spec()
    if kind == "EA":
        return "see EA form table"
    if kind == "IMM_EA":
        return "/".join(
            str(form.get("name"))
            for form in compact_ea_forms(spec)
            if form.get("class") == "immediate"
        )
    if kind in {"BITMAP16", "bitmap16"}:
        ranges = []
        for item in bitmap_operand_ranges(spec, "bitmap16"):
            bits = item.get("bits", [])
            if isinstance(bits, list) and len(bits) == 2:
                ranges.append(f"bits {bits[0]}..{bits[1]}={item.get('register_class')}0..{item.get('register_class')}{bits[1] - bits[0]}")
        return ", ".join(ranges)
    if kind == "SREG":
        return ", ".join(sreg_names(spec))
    if kind == "memory_order":
        valid = ", ".join(name.lower() for name, _value in spec_named_values(spec, "memory_order"))
        reserved = ", ".join(str(value) for _name, value in spec_named_values(spec, "memory_order", include_reserved=True) if _name.startswith("RESERVED"))
        return f"{valid}; encodings {reserved} reserved" if reserved else valid
    if kind == "SPREG":
        return "SP"
    return "-"


def prefix_rows(spec: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        name = str(prefix.get("name", ""))
        rendered_syntax = prefix_syntax(prefix)
        aliases = prefix_aliases(prefix)
        encoding = str(prefix.get("pattern", f"0x{int(prefix.get('value', 0)):02x}"))
        operand = prefix_operand(prefix)
        semantics = str(prefix.get("semantics", "-"))
        raw_syntax = prefix.get("syntax", {})
        examples = raw_syntax.get("examples", []) if isinstance(raw_syntax, dict) else []
        rows.append(
            {
                "name": name,
                "syntax": rendered_syntax,
                "encoding": encoding,
                "operand": operand,
                "aliases": aliases,
                "semantics": semantics,
                "examples": ", ".join(str(example) for example in examples) if examples else "-",
            }
        )
    return rows


def prefix_syntax(prefix: dict[str, Any]) -> str:
    syntax = prefix.get("syntax")
    if isinstance(syntax, dict):
        if syntax.get("block"):
            return str(syntax.get("block_template", f"{prefix.get('name', '')} Dn {{ <instruction>; ... }}"))
        template = str(syntax.get("mnemonic_template", prefix.get("name", "")))
        operand = prefix_operand(prefix)
        text = template if operand == "-" else f"{template} {operand}"
        if syntax.get("applies_to_following_instruction") and str(syntax.get("separator", "")) == "comma":
            text = f"{text}, <instruction>"
        return text
    operand = prefix_operand(prefix)
    name = str(prefix.get("name", ""))
    return name if operand == "-" else f"{name} {operand}"


def prefix_aliases(prefix: dict[str, Any]) -> str:
    syntax = prefix.get("syntax")
    aliases = syntax.get("aliases") if isinstance(syntax, dict) else {}
    if not isinstance(aliases, dict) or not aliases:
        return "-"
    return ", ".join(f"{key}={value}" for key, value in sorted(aliases.items()))


def prefix_operand(prefix: dict[str, Any]) -> str:
    operand = prefix.get("operand")
    if not isinstance(operand, dict):
        return "-"
    typ = str(operand.get("type", ""))
    role = str(operand.get("role", ""))
    if typ == "DREG":
        text = "Dn"
    else:
        text = f"<{typ.lower()}>" if typ else "-"
    return text if not role else f"{text}:{role}"


def compact_ea_extra_words(form: dict[str, Any]) -> str:
    if form.get("name") == "EXTENDED":
        return "+1 descriptor plus extended-form extras"
    words = 0
    for operand in form.get("operands", []) or []:
        if not isinstance(operand, dict):
            continue
        if operand.get("source") in {"extension_word", "extension_words"}:
            words += int(operand.get("words", bits_to_words(int(operand.get("width", 0)))))
    if "displacement" in form and words == 0:
        disp = str(form.get("displacement"))
        if disp.endswith("16"):
            words = 1
        elif disp.endswith("32"):
            words = 2
        elif disp.endswith("64"):
            words = 4
    if "absolute" in form and words == 0:
        absolute = str(form.get("absolute"))
        if absolute.endswith("32"):
            words = 2
        elif absolute.endswith("64"):
            words = 4
    return f"+{words}"


def ea_rows(spec: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    ea_forms = spec["ea"].get("ea_forms", []) or []
    compact = ea_forms.get("compact", []) if isinstance(ea_forms, dict) else ea_forms
    for form in compact:
        rows.append(
            {
                "space": "compact EA",
                "name": str(form.get("name", "")),
                "syntax": str(form.get("syntax", form.get("name", ""))),
                "encoding": str(form.get("pattern", "")),
                "extra_words": compact_ea_extra_words(form),
                "class": str(form.get("class", "")),
                "update": "yes" if form.get("update_eligible") else "no",
            }
        )
    for form in spec["ea"].get("extended_ea_forms", []) or []:
        syntax = str(form.get("syntax", form.get("name", "")))
        default_syntax = form.get("default_segment_syntax")
        if default_syntax:
            syntax = f"{default_syntax} / {syntax}"
        rows.append(
            {
                "space": "extended EA",
                "name": str(form.get("name", "")),
                "syntax": syntax,
                "encoding": f"mode=0x{int(form.get('value', 0)):x}",
                "extra_words": f"+{int(form.get('extra_words', 0))}",
                "class": str(form.get("class", "")),
                "update": "yes" if form.get("update_eligible") else "no",
            }
        )
    return rows


def render(plan: dict[str, Any], spec: dict[str, Any], lengths: dict[tuple[str, str], tuple[int, int]]) -> str:
    set_active_spec(spec)
    lines = [
        "# Generated Instruction Encoding Tables",
        "",
        "Generated from `isa/spec/*.yaml` and `build/generated/allocation_plan.json`. Do not edit by hand.",
        "",
        "## Instruction Encodings",
        "",
    ]
    _ = lengths
    allocations = [
        item for item in plan["solver"]["primary_allocations"] if item.get("kind") == "compact"
    ] + list(plan["solver"].get("primary_alias_allocations", [])) + list(plan["solver"]["extended_allocations"]) + list(plan["solver"].get("extended_alias_allocations", []))
    previous_space = ""
    for item in sorted(allocations, key=allocation_sort_key):
        if item.get("kind") == "extension_root":
            continue
        space = "primary" if item.get("kind") in {"compact", "compact_alias"} else str(item.get("extension_root", "extended"))
        if previous_space and space != previous_space:
            lines.append("")
        previous_space = space
        lines.append(encoding_line(item))

    lines.extend(
        [
            "",
            "## Prefix Forms",
            "",
            "| Name | Syntax | Encoding | Operand | Alias | Semantics | Example |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in prefix_rows(spec):
        lines.append(
            f"| `{md(row['name'])}` | `{md(row['syntax'])}` | `{md(row['encoding'])}` | "
            f"{md(row['operand'])} | {md(row['aliases'])} | {md(row['semantics'])} | {md(row['examples'])} |"
        )

    lines.extend(
        [
            "",
            "## Operand Types",
            "",
            "| Type | Syntax | Encoding | Default Word Contribution | Notes |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in operand_type_rows(plan, spec):
        lines.append(
            f"| `{md(row['type'])}` | `{md(row['syntax'])}` | {md(row['encoding'])} | "
            f"{md(row['default_words'])} | {md(row['notes'])} |"
        )

    lines.extend(
        [
            "",
            "## EA Forms",
            "",
            "| Space | Name | Syntax | Encoding | Extra Words | Class | Update Eligible |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in ea_rows(spec):
        lines.append(
            f"| {md(row['space'])} | `{md(row['name'])}` | `{md(row['syntax'])}` | "
            f"`{md(row['encoding'])}` | {md(row['extra_words'])} | {md(row['class'])} | {row['update']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("--allocation", default="build/generated/allocation_plan.json")
    parser.add_argument("-o", "--output", default="build/generated/instruction_encoding_table.md")
    args = parser.parse_args(argv)

    spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1
    with Path(args.allocation).open("r", encoding="utf-8") as fp:
        plan = json.load(fp)
    text = render(plan, spec, entry_lengths(entries))
    if args.output == "-":
        sys.stdout.write(text)
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
