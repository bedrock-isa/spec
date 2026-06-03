#!/usr/bin/env python3
"""Generate a Ghidra SLEIGH decode skeleton from the allocated ISA spec."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import argparse
import json
import re
import sys

sys.dont_write_bytecode = True

from isa_spec import load_and_validate, print_result


PRIMARY_BITS = 12
WORD_BITS = 16
MAX_INSTRUCTION_WORDS = 8
SIZE_NAMES = {
    "BWLQ": [".B", ".W", ".L", ".Q"],
    "LQ": [".L", ".Q"],
    "WL": [".W", ".L"],
    "S_D": [".S", ".D"],
    "BW": [".B", ".W"],
    "BWL": [".B", ".W", ".L", ".invalid"],
    "BWLX": [".B", ".W", ".L", ".invalid"],
}
CONDITION_VALUES = {
    "T": 0,
    "F": 1,
    "EQ": 2,
    "NE": 3,
    "ULT": 4,
    "UGE": 5,
    "MI": 6,
    "PL": 7,
    "VS": 8,
    "VC": 9,
    "ULE": 10,
    "UGT": 11,
    "LT": 12,
    "GE": 13,
    "LE": 14,
    "GT": 15,
}
CONDITIONAL_MNEMONICS = {"Jcc", "DJcc", "SETcc", "MOVcc", "TRAPcc", "FMOVcc"}


def is_condition_mnemonic(mnemonic: str) -> bool:
    return mnemonic in CONDITIONAL_MNEMONICS or mnemonic.lower().endswith("cc")


@dataclass(frozen=True)
class SField:
    token: int
    name: str
    low: int
    high: int
    kind: str = ""
    source: str = ""
    width: int = 0

    @property
    def mask(self) -> int:
        return ((1 << (self.high - self.low + 1)) - 1) << self.low


def default_allocation_path(spec_dir: str) -> Path:
    return Path(spec_dir).resolve().parents[1] / "build" / "generated" / "allocation_plan.json"


def load_allocation(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def parse_hex(value: str | int) -> int:
    if isinstance(value, int):
        return value
    return int(str(value).split("..", 1)[0], 16)


def parse_range(start: str | int, end: str | int | None = None) -> tuple[int, int]:
    if end is not None:
        return parse_hex(start), parse_hex(end)
    text = str(start)
    if ".." in text:
        left, right = text.split("..", 1)
        return int(left, 16), int(right, 16)
    value = int(text, 16)
    return value, value


def split_operand(operand: str) -> tuple[str, str]:
    if ":" in operand:
        return tuple(operand.split(":", 1))  # type: ignore[return-value]
    return operand, operand


def operand_tokens(text: str) -> set[str]:
    return {part for part in re.split(r"[^A-Za-z0-9]+", text.upper()) if part}


def is_ea_operand(text: str) -> bool:
    upper = text.upper()
    tokens = operand_tokens(text)
    return (
        upper == "EA"
        or upper.startswith("EA_")
        or upper.endswith("_EA")
        or "EA" in tokens
        or upper in {"LINEAR_OR_EA", "EA_OR_RANGE", "EA_OR_D"}
    )


def infer_operand_kind(operand: str, field: dict[str, Any] | None = None) -> str:
    if field is not None:
        return str(field.get("kind", ""))
    name, typ = split_operand(operand)
    upper = typ.upper()
    source = name.upper()
    if "BITMAP" in upper or "BITMAP" in source:
        return "bitmap16"
    if upper in {"MEMORY_ORDER", "MEMORYORDER", "ORDER"} or source in {"ORDER", "MEMORY_ORDER"}:
        return "memory_order"
    if "CONDITION" in upper or upper == "CC" or source == "CONDITION" or source == "CC":
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
    if is_ea_operand(typ) or is_ea_operand(name) or "MEMORY" in upper or "MEMORY" in source:
        return "EA"
    if upper in {"CR", "CREG", "CONTROL_REGISTER"} or source in {"CR", "CONTROL_REGISTER"}:
        return "cr"
    if "ASID" in upper or "ASID" in source:
        return "asid"
    if "RELATIVE" in upper or source == "TARGET":
        return "relative_imm"
    if "IMM64" in upper or "IMM64" in source:
        return "imm64"
    if "IMM32" in upper or "IMM32" in source:
        return "imm32"
    if "IMM16" in upper or "IMM16" in source:
        return "imm16"
    if upper in {"SELECTOR_IMM6", "IMM6_SELECTOR"}:
        return "selector6"
    if "IMM" in upper or "IMM" in source or source == "VALUE":
        return "imm"
    if any(key in upper or key in source for key in ("COUNT", "BIT_INDEX")):
        return "selector6"
    if any(key in upper or key in source for key in ("OFFSET", "WIDTH", "SELECTOR")):
        return "small_selector"
    return typ


def is_implicit_operand(operand: str) -> bool:
    name, _typ = split_operand(operand)
    upper = name.upper()
    return (
        upper == "OUTPUTS"
        or upper.startswith("OUTPUT")
        or "_IN_" in upper
        or upper.startswith("LEAF_IN_")
        or upper.startswith("SUBLEAF_IN_")
    )


def payload_words_for_kind(kind: str, fallback: int = 1) -> int:
    lower = kind.lower()
    if "bitmap" in lower or "imm16" in lower or lower == "cr" or "asid" in lower:
        return 1
    if "imm32" in lower:
        return 2
    if "imm64" in lower:
        return 4
    if "relative" in lower or "imm" in lower:
        return fallback
    return 0


def sanitize(text: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9_]", "_", text)
    if not clean:
        clean = "x"
    if clean[0].isdigit():
        clean = "x_" + clean
    return clean


def token_prefix(token: int) -> str:
    return "p" if token == 0 else f"w{token}"


def token_field_name(token: int, low: int, high: int) -> str:
    prefix = token_prefix(token)
    if token == 0:
        return f"{prefix}{low}" if low == high else f"{prefix}{low}_{high}"
    return f"{prefix}_{low}" if low == high else f"{prefix}_{low}_{high}"


def field_prefix(kind: str, source: str = "") -> str:
    upper = kind.upper()
    if upper in SIZE_NAMES:
        return "z" if upper in {"LQ", "WL", "S_D"} else "s"
    if upper == "DREG":
        return "d"
    if upper == "DBANK":
        return "db"
    if upper == "AREG":
        return "a"
    if upper == "SPREG":
        return "sp"
    if upper == "SREG":
        return "g"
    if upper == "FREG":
        return "f"
    if upper in {"EA", "IMM_EA"}:
        return "ea"
    if upper == "CONDITION":
        return "c"
    if upper == "SMALL_SELECTOR":
        return "n"
    if upper == "MEMORY_ORDER":
        return "o"
    if "IMM" in upper or "RELATIVE" in upper:
        return "i"
    if "BITMAP" in upper:
        return "b"
    return sanitize(source or kind).lower()[:8]


def sleigh_field_name(field: dict[str, Any], token: int) -> str:
    low = int(field["low_bit"])
    high = int(field["high_bit"])
    kind = str(field.get("kind", ""))
    source = str(field.get("source", ""))
    prefix = field_prefix(kind, source)
    kind_tag = sanitize(kind).lower()
    return f"{prefix}_{kind_tag}_{token_field_name(token, low, high)}"


def size_values(kind: str) -> list[str]:
    return SIZE_NAMES.get(kind.upper(), [])


def condition_names(spec: dict[str, Any]) -> list[str]:
    out = ["T", "F", "EQ", "NE", "ULT", "UGE", "MI", "PL", "VS", "VC", "ULE", "UGT", "LT", "GE", "LE", "GT"]
    for item in spec.get("conditions", {}).get("conditions", []) or []:
        if not isinstance(item, dict):
            continue
        value = int(item.get("value", len(out)))
        while len(out) <= value:
            out.append(f"C{len(out)}")
        out[value] = str(item.get("name", out[value]))
    return out[:16]


def field_for_operand(fields: list[dict[str, Any]], operand: str) -> dict[str, Any] | None:
    name, typ = split_operand(operand)
    candidates = {name, typ, operand}
    for field in fields:
        source = str(field.get("source", ""))
        if source in candidates:
            return field
    kind = infer_operand_kind(operand)
    for field in fields:
        if str(field.get("kind")) == kind:
            return field
    return None


def parse_descriptor_layout(item: dict[str, Any]) -> list[dict[str, Any]]:
    raw_fields = [dict(field) for field in item.get("fields", []) or []]
    layout = str(item.get("_resolved_descriptor_layout", item.get("descriptor_layout", "")))
    occurrence: dict[tuple[str, str], int] = {}
    by_kind: dict[str, list[dict[str, Any]]] = {}
    for field in raw_fields:
        by_kind.setdefault(str(field.get("kind", "")), []).append(field)

    start_token = 2 if item.get("kind") in {"extended", "extended_alias"} else 1
    payload_token = start_token
    payload_bit = 0

    def source_for(name: str, kind: str) -> str:
        key = (name.rstrip("0123456789").lower(), kind)
        index = occurrence.get(key, 0)
        occurrence[key] = index + 1
        candidates = by_kind.get(kind, [])
        return str(candidates[index].get("source", name)) if index < len(candidates) else name

    out: list[dict[str, Any]] = []
    for part in [piece.strip() for piece in layout.split(",") if piece.strip()]:
        if "@root" in part or "=" in part:
            continue
        match = re.match(
            r"(?P<name>[A-Za-z][A-Za-z0-9_]*):(?P<kind>[A-Za-z0-9_]+)\[(?P<high>\d+)(?::(?P<low>\d+))?\]",
            part,
        )
        if match:
            name = match.group("name")
            kind = match.group("kind")
            high = int(match.group("high"))
            low = int(match.group("low") or match.group("high"))
            out.append(
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
            # Only used by aliases when a concrete alias target layout is not
            # available. Keep the fallback deterministic and low-bit packed.
            low = payload_bit
            high = low + width - 1
            payload_bit = high + 1
            token = 1
        else:
            if payload_bit + width > WORD_BITS:
                payload_token += 1
                payload_bit = 0
            low = payload_bit
            high = low + width - 1
            payload_bit = high + 1
            token = payload_token
        out.append(
            {
                "name": name,
                "kind": kind,
                "source": source_for(name, kind),
                "storage": "descriptor",
                "token": token,
                "width": width,
                "low_bit": low,
                "high_bit": high,
            }
        )
    return out


def item_fields(item: dict[str, Any]) -> list[dict[str, Any]]:
    if item.get("kind") in {"compact", "compact_alias"}:
        return [dict(field, token=0) for field in item.get("fields", []) or [] if "low_bit" in field]
    return parse_descriptor_layout(item)


def field_token(field: dict[str, Any], default: int) -> int:
    return int(field.get("token", default))


def root_condition_field(item: dict[str, Any]) -> dict[str, Any] | None:
    if item.get("kind") not in {"extended", "extended_alias"}:
        return None
    if not any(infer_operand_kind(str(operand)) == "condition" for operand in item.get("operands", []) or []):
        return None
    start, end = parse_range(str(item.get("extension_root_payload", "0x000")))
    variable = start ^ end
    if variable == 0:
        return None
    low = (variable & -variable).bit_length() - 1
    high = variable.bit_length() - 1
    width = high - low + 1
    if width != 4:
        return None
    return {
        "name": "c",
        "kind": "condition",
        "source": "cc",
        "storage": "primary",
        "width": width,
        "low_bit": low,
        "high_bit": high,
    }


def payload_word_count(item: dict[str, Any]) -> int:
    if item.get("kind") in {"compact", "compact_alias"}:
        return max(0, int(item.get("min_words", 1)) - 1)
    return max(0, int(item.get("operand_descriptor_words", 0) or 0))


def payload_symbol(kind: str, start_word: int, word_count: int) -> str:
    clean = sanitize(kind.lower())
    return f"{clean}_w{start_word}_{word_count}"


def payload_tokens(start_word: int, word_count: int) -> list[str]:
    return [f"word{index}" for index in range(start_word, start_word + word_count)]


def collect_allocations(plan: dict[str, Any]) -> list[dict[str, Any]]:
    solver = plan.get("solver", plan)
    out: list[dict[str, Any]] = []
    out.extend(dict(item) for item in solver.get("primary_allocations", []) if item.get("kind") == "compact")
    out.extend(dict(item) for item in solver.get("primary_alias_allocations", []))
    for item in solver.get("extended_allocations", []):
        copied = dict(item)
        copied.setdefault("kind", "extended")
        out.append(copied)
    out.extend(dict(item) for item in solver.get("extended_alias_allocations", []))
    by_id = {str(item.get("id", "")): item for item in out}
    for item in out:
        if item.get("kind") != "extended_alias":
            continue
        alias_target = by_id.get(str(item.get("alias_of", "")))
        if alias_target and alias_target.get("descriptor_layout"):
            item["_resolved_descriptor_layout"] = alias_target["descriptor_layout"]
    for item in out:
        if item.get("kind") != "compact_alias" or not item.get("alias_condition"):
            continue
        alias_target = by_id.get(str(item.get("alias_of", "")))
        if not alias_target:
            continue
        value = CONDITION_VALUES.get(str(item.get("alias_condition", "")).upper())
        if value is None:
            continue
        fixed_fields = []
        for field in alias_target.get("fields", []) or []:
            if str(field.get("kind")) == "condition" and "low_bit" in field:
                fixed_fields.append(dict(field, token=0, value=value))
        if fixed_fields:
            item["_fixed_condition_fields"] = fixed_fields
    return out


def collect_sleigh_fields(allocations: list[dict[str, Any]]) -> dict[str, SField]:
    fields: dict[str, SField] = {}

    def add(token: int, name: str, low: int, high: int, kind: str = "", source: str = "") -> None:
        fields.setdefault(name, SField(token=token, name=name, low=low, high=high, kind=kind, source=source, width=high - low + 1))

    for bit in range(PRIMARY_BITS):
        add(0, token_field_name(0, bit, bit), bit, bit)
    add(0, token_field_name(0, 0, PRIMARY_BITS - 1), 0, PRIMARY_BITS - 1)
    for token in range(1, MAX_INSTRUCTION_WORDS):
        add(token, f"word{token}", 0, WORD_BITS - 1)
        add(token, token_field_name(token, 0, WORD_BITS - 1), 0, WORD_BITS - 1)

    for item in allocations:
        for field in item_fields(item):
            token = field_token(field, 0 if item.get("kind") in {"compact", "compact_alias"} else 1)
            name = sleigh_field_name(field, token)
            add(
                token,
                name,
                int(field["low_bit"]),
                int(field["high_bit"]),
                str(field.get("kind", "")),
                str(field.get("source", "")),
            )
        root_field = root_condition_field(item)
        if root_field:
            add(
                0,
                sleigh_field_name(root_field, 0),
                int(root_field["low_bit"]),
                int(root_field["high_bit"]),
                "condition",
                "cc",
            )
        for field in item.get("_fixed_condition_fields", []) or []:
            token = field_token(field, 0)
            add(
                token,
                sleigh_field_name(field, token),
                int(field["low_bit"]),
                int(field["high_bit"]),
                "condition",
                str(field.get("source", "cc")),
            )
        start, end = item_primary_range(item)
        for low, high in fixed_constraint_ranges(start, end, primary_variable_mask(item)):
            add(0, token_field_name(0, low, high), low, high)
        if item.get("kind") in {"extended", "extended_alias"}:
            ext_start, ext_end = parse_range(str(item.get("extended_opcode", "0x0000")))
            for low, high in fixed_constraint_ranges(ext_start, ext_end, descriptor_variable_mask(item)):
                add(1, token_field_name(1, low, high), low, high)
    return fields


def item_primary_range(item: dict[str, Any]) -> tuple[int, int]:
    if item.get("kind") in {"extended", "extended_alias"}:
        return parse_range(str(item.get("extension_root_payload", "0x000")))
    if item.get("kind") == "compact_alias" and item.get("alias_payloads"):
        values = [parse_hex(value) for value in item.get("alias_payloads", [])]
        return min(values), max(values)
    return parse_range(str(item.get("start_payload", "0x000")), str(item.get("end_payload", "0x000")))


def field_mask(fields: list[dict[str, Any]]) -> int:
    mask = 0
    for field in fields:
        low = int(field["low_bit"])
        high = int(field["high_bit"])
        mask |= ((1 << (high - low + 1)) - 1) << low
    return mask


def primary_variable_mask(item: dict[str, Any]) -> int:
    fields = [field for field in item_fields(item) if field_token(field, 0) == 0] if item.get("kind") in {"compact", "compact_alias"} else []
    root = root_condition_field(item)
    if root:
        fields = fields + [root]
    return field_mask(fields)


def descriptor_variable_mask(item: dict[str, Any]) -> int:
    if item.get("kind") not in {"extended", "extended_alias"}:
        return 0
    return field_mask([field for field in item_fields(item) if field_token(field, 1) == 1])


def fixed_constraint_ranges(start: int, end: int, variable_mask: int, width: int = PRIMARY_BITS) -> list[tuple[int, int]]:
    if width == WORD_BITS:
        bit_limit = WORD_BITS
    else:
        bit_limit = PRIMARY_BITS
    fixed_mask = ((1 << bit_limit) - 1) ^ variable_mask
    if (start & fixed_mask) != (end & fixed_mask):
        return [(0, bit_limit - 1)]
    ranges: list[tuple[int, int]] = []
    bit = 0
    while bit < bit_limit:
        if not (fixed_mask & (1 << bit)):
            bit += 1
            continue
        low = bit
        while bit + 1 < bit_limit and fixed_mask & (1 << (bit + 1)):
            bit += 1
        ranges.append((low, bit))
        bit += 1
    return ranges


def fixed_constraints(start: int, end: int, variable_mask: int, token: int, width: int) -> list[str]:
    fixed_mask = ((1 << width) - 1) ^ variable_mask
    if (start & fixed_mask) != (end & fixed_mask):
        field = token_field_name(token, 0, width - 1)
        return [f"({field} >= 0x{start:x} & {field} <= 0x{end:x})"]
    constraints = []
    for low, high in fixed_constraint_ranges(start, end, variable_mask, width):
        field = token_field_name(token, low, high)
        value = (start >> low) & ((1 << (high - low + 1)) - 1)
        constraints.append(f"{field}=0x{value:x}")
    return constraints


def register_names(prefix: str, count: int) -> list[str]:
    return [f"{prefix}{index}" for index in range(count)]


def sreg_names(spec: dict[str, Any], *, padded: bool = False) -> list[str]:
    classes = spec.get("registers", {}).get("special_register_classes", {})
    sreg = classes.get("S", {}) if isinstance(classes, dict) else {}
    raw_names = sreg.get("registers", []) if isinstance(sreg, dict) else []
    names = [str(name) for name in raw_names if str(name)]
    if not names:
        names = [
            str(item.get("name", ""))
            for item in spec.get("segments", {}).get("segment_registers", []) or []
            if isinstance(item, dict) and item.get("name")
        ]
    if padded:
        target = 1 << max(1, (len(names) - 1).bit_length())
        names = names + [f"SRES{index}" for index in range(len(names), target)]
    return names


def render_registers(spec: dict[str, Any]) -> str:
    register_classes = spec.get("registers", {}).get("register_classes", {})
    d_count = int(register_classes.get("D", {}).get("count", 8) or 8)
    a_count = int(register_classes.get("A", {}).get("count", 8) or 8)
    names = (
        register_names("D", d_count)
        + register_names("A", a_count)
        + sreg_names(spec)
        + register_names("F", 32)
    )
    for item in spec.get("registers", {}).get("special_registers", []) or []:
        if isinstance(item, dict):
            name = str(item.get("name", ""))
        else:
            name = str(item)
        if name and name not in names:
            names.append(name)
    lines = ["define register offset=0 size=8 ["]
    for index in range(0, len(names), 8):
        lines.append("  " + " ".join(names[index : index + 8]))
    lines.append("];")
    return "\n".join(lines)


def render_token(name: str, fields: list[SField]) -> str:
    lines = [f"define token {name} (16)"]
    for field in sorted(fields, key=lambda item: (item.low, item.high, item.name)):
        lines.append(f"  {field.name}=({field.low},{field.high})")
    lines.append(";")
    return "\n".join(lines)


def render_tokens(fields: dict[str, SField]) -> str:
    grouped: dict[int, list[SField]] = {}
    for field in fields.values():
        grouped.setdefault(field.token, []).append(field)
    blocks = []
    for token in sorted(grouped):
        name = "instr0" if token == 0 else f"instr{token}"
        blocks.append(render_token(name, grouped[token]))
    return "\n\n".join(blocks)


def render_attaches(spec: dict[str, Any], fields: dict[str, SField]) -> str:
    by_kind: dict[str, list[str]] = {}
    for field in fields.values():
        if field.kind:
            by_kind.setdefault(field.kind, []).append(field.name)
    lines: list[str] = []
    d_fields = sorted(by_kind.get("DREG", []))
    db_fields = sorted(by_kind.get("DBANK", []))
    a_fields = sorted(by_kind.get("AREG", []))
    s_fields = sorted(by_kind.get("SREG", []))
    f_fields = sorted(by_kind.get("FREG", []))
    c_fields = sorted(by_kind.get("condition", []))
    order_fields = sorted(by_kind.get("memory_order", []))
    if d_fields:
        lines.append(f"attach variables [ {' '.join(d_fields)} ] [ {' '.join(register_names('D', 8))} ];")
    if db_fields:
        db_names = " ".join(f'"DB{i}"' for i in range(16))
        lines.append(f"attach names [ {' '.join(db_fields)} ] [ {db_names} ];")
    if a_fields:
        lines.append(f"attach variables [ {' '.join(a_fields)} ] [ {' '.join(register_names('A', 8))} ];")
    if s_fields:
        names = " ".join(f'"{name}"' for name in sreg_names(spec, padded=True))
        lines.append(f"attach names [ {' '.join(s_fields)} ] [ {names} ];")
    if f_fields:
        lines.append(f"attach variables [ {' '.join(f_fields)} ] [ {' '.join(register_names('F', 32))} ];")
    if c_fields:
        names = " ".join(f'"{name}"' for name in condition_names(spec))
        lines.append(f"attach names [ {' '.join(c_fields)} ] [ {names} ];")
    if order_fields:
        names = '"RELAXED" "ACQUIRE" "RELEASE" "ACQREL" "SEQCST" "RESERVED5" "RESERVED6" "RESERVED7"'
        lines.append(f"attach names [ {' '.join(order_fields)} ] [ {names} ];")
    for kind, values in sorted(SIZE_NAMES.items()):
        size_fields = sorted(by_kind.get(kind, []))
        if not size_fields:
            continue
        names = " ".join(f'"{value}"' for value in values)
        lines.append(f"attach names [ {' '.join(size_fields)} ] [ {names} ];")
    return "\n".join(lines)


def ea_table_name(field_name: str) -> str:
    return f"ea_{field_name}"


def payload_table_name(kind: str, start_word: int, word_count: int) -> str:
    return payload_symbol(kind, start_word, word_count)


def render_operand_tables(fields: dict[str, SField]) -> str:
    lines: list[str] = []
    ea_fields = sorted(
        (field for field in fields.values() if field.kind == "EA"),
        key=lambda field: (field.token, field.low, field.high, field.name),
    )
    for field in ea_fields:
        table = ea_table_name(field.name)
        lines.append(f'{table}: "<ea:"^{field.name}^">" is {field.name} {{ }}')
    lines.append("")
    payload_tables: set[tuple[str, int, int]] = set()
    for start in range(1, MAX_INSTRUCTION_WORDS):
        for kind, count in (
            ("imm16", 1),
            ("relative_imm", 1),
            ("bitmap16", 1),
            ("cr", 1),
            ("asid", 1),
            ("imm32", 2),
            ("imm64", 4),
            ("payload", 1),
        ):
            if start + count - 1 < MAX_INSTRUCTION_WORDS:
                payload_tables.add((kind, start, count))
    for kind, start, count in sorted(payload_tables, key=lambda item: (item[1], item[2], item[0])):
        table = payload_table_name(kind, start, count)
        tokens = " ; ".join(payload_tokens(start, count))
        if count == 1:
            display = f"word{start}"
        else:
            display = f'"<{kind}>"'
        lines.append(f"{table}: {display} is {tokens} {{ }}")
    return "\n".join(lines)


def display_name_for_field(field: dict[str, Any], token: int | None = None) -> str:
    effective_token = field_token(field, token if token is not None else 0)
    name = sleigh_field_name(field, effective_token)
    if str(field.get("kind")) in {"EA", "IMM_EA"}:
        return ea_table_name(name)
    return name


def payload_operand_display(kind: str, start_word: int, available_words: int) -> tuple[str, int]:
    count = payload_words_for_kind(kind, fallback=max(1, available_words))
    if count <= 0:
        count = 1
    count = min(count, max(1, available_words))
    return payload_table_name(kind, start_word, count), count


def constructor_display(item: dict[str, Any], fields: list[dict[str, Any]], token: int, payload_count: int) -> tuple[str, list[str]]:
    mnemonic = str(item.get("mnemonic", item.get("id", "")))
    size_field = next((field for field in fields if str(field.get("kind")) in SIZE_NAMES), None)
    fixed_size = str(item.get("fixed_size_suffix", ""))
    suffix = f"^{display_name_for_field(size_field, token)}" if size_field else (f".{fixed_size}" if fixed_size else "")
    condition_suffix = ""
    order_suffix = ""
    operands: list[str] = []
    payload_terms: list[str] = []
    payload_cursor = 1 if item.get("kind") in {"compact", "compact_alias"} else 2
    field_payload_tokens = {field_token(field, token) for field in fields if field_token(field, token) >= payload_cursor}
    consumed_payload_tokens = set(field_payload_tokens)

    root_field = root_condition_field(item)
    for operand in item.get("operands", []) or []:
        operand_text = str(operand)
        if is_implicit_operand(operand_text):
            continue
        kind = infer_operand_kind(operand_text)
        if kind == "condition":
            field = root_field or field_for_operand(fields, operand_text)
            if field is not None:
                condition_display = display_name_for_field(field, 0 if field is root_field else token)
                if is_condition_mnemonic(mnemonic):
                    condition_suffix = f"^{condition_display}"
                else:
                    operands.append(condition_display)
            continue
        field = field_for_operand(fields, operand_text)
        if field is not None:
            if kind == "memory_order":
                order_suffix = f'"/"^{display_name_for_field(field, token)}'
                continue
            operands.append(display_name_for_field(field, token))
            continue
        if kind == "SPREG":
            operands.append('"SP"')
            continue
        while payload_cursor in consumed_payload_tokens:
            payload_cursor += 1
        available_words = max(0, payload_count - (payload_cursor - (1 if item.get("kind") in {"compact", "compact_alias"} else 2)))
        if available_words > 0:
            symbol, used = payload_operand_display(kind, payload_cursor, available_words)
            operands.append(symbol)
            payload_terms.append(symbol)
            consumed_payload_tokens.update(range(payload_cursor, payload_cursor + used))
            payload_cursor += used
            continue
        name, _typ = split_operand(operand_text)
        operands.append(f'"<{sanitize(name).lower()}>"')

    end_payload_token = (1 if item.get("kind") in {"compact", "compact_alias"} else 2) + payload_count
    while payload_cursor < end_payload_token:
        if payload_cursor in consumed_payload_tokens:
            payload_cursor += 1
            continue
        symbol = payload_table_name("payload", payload_cursor, 1)
        payload_terms.append(symbol)
        consumed_payload_tokens.add(payload_cursor)
        payload_cursor += 1

    if condition_suffix:
        mnemonic = re.sub(r"cc$", condition_suffix, mnemonic, flags=re.IGNORECASE)
    operand_text = "" if not operands else " " + ",".join(operands)
    return f"{mnemonic}{suffix}{order_suffix}{operand_text}", payload_terms


def item_pattern(item: dict[str, Any], fields: list[dict[str, Any]], payload_terms: list[str]) -> str:
    fields_by_token: dict[int, list[dict[str, Any]]] = {}
    for field in fields:
        fields_by_token.setdefault(field_token(field, 0 if item.get("kind") in {"compact", "compact_alias"} else 1), []).append(field)
    fixed_condition_terms = [
        f"{display_name_for_field(field, field_token(field, 0))}=0x{int(field.get('value', 0)):x}"
        for field in item.get("_fixed_condition_fields", []) or []
    ]

    if item.get("kind") in {"compact", "compact_alias"}:
        start, end = item_primary_range(item)
        terms = fixed_constraints(start, end, primary_variable_mask(item), 0, PRIMARY_BITS)
        terms.extend(fixed_condition_terms)
        terms.extend(display_name_for_field(field, 0) for field in fields_by_token.get(0, []))
        pattern = " & ".join(terms) if terms else "epsilon"
        for token_index in sorted(token for token in fields_by_token if token > 0):
            token_terms = [display_name_for_field(field, token_index) for field in fields_by_token[token_index]]
            pattern += " ; " + " & ".join(token_terms)
        if payload_terms:
            pattern += " ; " + " ; ".join(payload_terms)
        return pattern

    primary_start, primary_end = item_primary_range(item)
    root = root_condition_field(item)
    root_terms = fixed_constraints(primary_start, primary_end, primary_variable_mask(item), 0, PRIMARY_BITS)
    if root:
        root_terms.append(display_name_for_field(root, 0))
    ext_start, ext_end = parse_range(str(item.get("extended_opcode", "0x0000")))
    ext_terms = fixed_constraints(ext_start, ext_end, descriptor_variable_mask(item), 1, WORD_BITS)
    ext_terms.extend(display_name_for_field(field, 1) for field in fields_by_token.get(1, []))
    primary = " & ".join(root_terms) if root_terms else "epsilon"
    ext = " & ".join(ext_terms) if ext_terms else "epsilon"
    pattern = primary + " ; " + ext
    for token_index in sorted(token for token in fields_by_token if token > 1):
        token_terms = [display_name_for_field(field, token_index) for field in fields_by_token[token_index]]
        pattern += " ; " + " & ".join(token_terms)
    if payload_terms:
        pattern += " ; " + " ; ".join(payload_terms)
    return pattern


def constructor_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    if item.get("kind") in {"compact", "compact_alias"}:
        start, _end = item_primary_range(item)
        return (start, -1, str(item.get("id", "")))
    root_start, _root_end = parse_range(str(item.get("extension_root_payload", "0x000")))
    ext_start, _ext_end = parse_range(str(item.get("extended_opcode", "0x0000")))
    return (root_start, ext_start, str(item.get("id", "")))


def render_constructors(allocations: list[dict[str, Any]]) -> str:
    lines = [
        "# Instruction constructors. Semantics are intentionally stubbed until",
        "# instruction p-code lowering is specified.",
    ]
    for item in sorted(allocations, key=constructor_sort_key):
        fields = item_fields(item)
        token = 0 if item.get("kind") in {"compact", "compact_alias"} else 1
        payload_count = payload_word_count(item)
        display, payload_terms = constructor_display(item, fields, token, payload_count)
        pattern = item_pattern(item, fields, payload_terms)
        lines.append(f":{display} is {pattern} {{ isa_unimplemented(); }}")
    return "\n".join(lines)


def render(spec_dir: str, spec: dict[str, Any], plan: dict[str, Any], allocation_path: Path) -> str:
    allocations = collect_allocations(plan)
    fields = collect_sleigh_fields(allocations)
    solver = plan.get("solver", {})
    header = f"""# Generated SLEIGH specification
# Source spec: {spec_dir}
# Source allocation: {allocation_path}
# Solver status: {solver.get("status", plan.get("solver", "unknown"))}
# Constructors: {len(allocations)}
#
# This is a decode/disassembly skeleton. It follows the allocated opcode map and
# leaves instruction p-code behind isa_unimplemented() while semantics stabilize.

define endian=little;
define alignment=2;

define space ram type=ram_space size=8 default;
define space register type=register_space size=8;

define pcodeop isa_unimplemented;
"""
    sections = [
        header.rstrip(),
        render_registers(spec),
        render_tokens(fields),
        render_attaches(spec, fields),
        render_operand_tables(fields),
        render_constructors(allocations),
        "",
    ]
    return "\n\n".join(section for section in sections if section.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("-o", "--output", default="build/generated/isa.slaspec")
    parser.add_argument("--allocation", help="allocation_plan.json to use")
    args = parser.parse_args(argv)

    spec, result, _entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1

    allocation_path = Path(args.allocation) if args.allocation else default_allocation_path(args.spec_dir)
    if not allocation_path.exists():
        raise SystemExit(f"allocation plan not found: {allocation_path}")

    text = render(args.spec_dir, spec, load_allocation(allocation_path), allocation_path)
    if args.output == "-":
        sys.stdout.write(text)
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
