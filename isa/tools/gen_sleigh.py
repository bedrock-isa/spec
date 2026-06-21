#!/usr/bin/env python3
"""Generate a Ghidra SLEIGH specification from the allocated ISA spec."""

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
from spec_model.encoding import (
    condition_named_values,
    condition_names_by_value as spec_condition_names_by_value,
    condition_sleigh_checks,
    flag_pseudo_registers,
    named_values as spec_named_values,
    register_names as spec_register_names,
    size_code_bytes,
    size_kind_byte_widths,
    size_kind_field,
    size_kind_suffixes,
    size_kind_width,
    size_kinds as spec_size_kinds,
    special_register_attach_names,
    special_register_named_values,
)


PRIMARY_BITS = 12
WORD_BITS = 16
MAX_INSTRUCTION_WORDS = 8
ACTIVE_SPEC: dict[str, Any] | None = None


def is_condition_mnemonic(mnemonic: str) -> bool:
    return mnemonic.lower().endswith("cc")


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


@dataclass(frozen=True)
class OperandBinding:
    role: str
    kind: str
    display: str
    ref: str


DIRECT_REGISTER_KINDS = {"DREG", "AREG", "SREG", "FREG", "SPREG"}
PCODE_SCRATCH_ROLES = {"size", "result", "tmp", "carry", "borrow"}
PCODE_ROLE_VAR_RE = re.compile(r"\b([a-z][a-z0-9_]*?)_old_v\b|\b([a-z][a-z0-9_]*)_v\b")
LOCAL_PCODE_VAR_RE = re.compile(r"^\s*local\s+([A-Za-z][A-Za-z0-9_]*)(?::\d+)?\b")


def active_spec() -> dict[str, Any]:
    if ACTIVE_SPEC is None:
        raise RuntimeError("active spec is not set")
    return ACTIVE_SPEC


def size_kind_names() -> set[str]:
    return set(spec_size_kinds(active_spec()))


def is_size_kind(kind: str) -> bool:
    return kind.upper() in size_kind_names()


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
    explicit_type = ":" in operand
    upper = typ.upper()
    source = name.upper()
    if "BITMAP" in upper or "BITMAP" in source:
        bitmaps = (
            active_spec()
            .get("instructions", {})
            .get("operand_schema", {})
            .get("bitmap_operands", {})
        )
        lower = typ.lower()
        if isinstance(bitmaps, dict) and lower in bitmaps:
            return lower
        return "bitmap16"
    if upper in {"MEMORY_ORDER", "MEMORYORDER", "ORDER"} or source in {"ORDER", "MEMORY_ORDER"}:
        return "memory_order"
    if "CONDITION" in upper or upper == "CC" or source == "CONDITION" or source == "CC":
        return "condition"
    if upper in {"SP", "SPREG", "STACK_POINTER", "STACK_REGISTER"} or source in {"SP", "STACK_POINTER", "STACK_REGISTER"}:
        return "SPREG"
    if upper in {"DBANK", "DATA_BANK", "DATA_REGISTER_BANK"} or source in {"BANK", "SRC_BANK", "DST_BANK", "BANK_A", "BANK_B", "DBANK"}:
        return "DBANK"
    if upper in {"DREG", "DLO", "DX", "DHI"} or upper.startswith("D") or (not explicit_type and source.startswith("D")):
        return "DREG"
    if upper in {"AREG"} or upper.startswith("A") or (not explicit_type and source.startswith("A")):
        return "AREG"
    if upper in {"SREG", "SEGREG", "SEGMENT_REGISTER"} or (not explicit_type and (source.startswith("SREG") or source.startswith("SEG"))):
        return "SREG"
    if upper.startswith("F") or (not explicit_type and source.startswith("F")):
        return "FREG"
    if upper in {"IMM_EA", "IMMEDIATE_EA", "IMMEA", "IMMEDIATE_OPERAND_EA"}:
        return "IMM_EA"
    if is_ea_operand(typ) or is_ea_operand(name) or "MEMORY" in upper or "MEMORY" in source:
        return "EA"
    if upper in {"CR", "CREG", "CONTROL_REGISTER"} or source in {"CR", "CONTROL_REGISTER"}:
        return "cr"
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


def payload_words_for_kind(kind: str, default_count: int = 1) -> int:
    lower = kind.lower()
    if "bitmap" in lower or "imm16" in lower or lower == "cr":
        return 1
    if "imm32" in lower:
        return 2
    if "imm64" in lower:
        return 4
    if "relative" in lower or "imm" in lower:
        return default_count
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
    if is_size_kind(upper):
        return size_kind_field(active_spec(), upper)
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
    return size_kind_suffixes(active_spec(), kind)


def condition_names(spec: dict[str, Any]) -> list[str]:
    return spec_condition_names_by_value(spec)


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
    if layout == "none":
        return []
    occurrence: dict[tuple[str, str], int] = {}
    by_kind: dict[str, list[dict[str, Any]]] = {}
    by_name_kind: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for field in raw_fields:
        by_kind.setdefault(str(field.get("kind", "")), []).append(field)
        by_name_kind.setdefault((str(field.get("name", "")), str(field.get("kind", ""))), []).append(field)

    start_token = 2 if item.get("kind") in {"extended", "extended_alias"} else 1
    payload_token = start_token
    payload_bit = 0

    def source_for(name: str, kind: str) -> str:
        candidates = by_name_kind.get((name, kind))
        key = (name, kind)
        if not candidates:
            key = (name.rstrip("0123456789").lower(), kind)
            candidates = by_kind.get(kind, [])
        index = occurrence.get(key, 0)
        occurrence[key] = index + 1
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
            # Alias-only synthetic layouts stay deterministic and low-bit packed.
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


def collect_allocations(spec: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
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
    condition_values = {name.upper(): value for name, value in condition_named_values(spec)}
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
        value = condition_values.get(str(item.get("alias_condition", "")).upper())
        if value is None:
            continue
        fixed_fields = []
        for field in alias_target.get("fields", []) or []:
            if str(field.get("kind")) == "condition" and "low_bit" in field:
                fixed_fields.append(dict(field, token=0, value=value))
        if fixed_fields:
            item["_fixed_condition_fields"] = fixed_fields
    return out


def pcode_statements(value: Any) -> list[str]:
    if isinstance(value, str):
        return [line.rstrip() for line in value.splitlines()]
    if isinstance(value, list):
        lines: list[str] = []
        for item in value:
            if isinstance(item, str):
                lines.extend(line.rstrip() for line in item.splitlines())
        return lines
    return []


def semantic_value_for_mnemonic(group: dict[str, Any], key: str, mnemonic: str) -> Any:
    by_mnemonic = group.get(f"{key}_by_mnemonic")
    if isinstance(by_mnemonic, dict) and mnemonic in by_mnemonic:
        return by_mnemonic[mnemonic]
    return group.get(key)


def operation_semantics_map(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    operation_semantics = (
        spec.get("instructions", {})
        .get("operation_semantics", {})
    )
    groups = operation_semantics.get("groups", {}) if isinstance(operation_semantics, dict) else {}
    out: dict[str, dict[str, Any]] = {}
    if isinstance(groups, dict):
        for group in groups.values():
            if not isinstance(group, dict):
                continue
            for member in [str(item) for item in group.get("members", []) or []]:
                entry = out.setdefault(member, {})
                for key in ("inputs", "input_output", "output"):
                    value = semantic_value_for_mnemonic(group, key, member)
                    if value is not None:
                        entry[key] = value
    instructions = operation_semantics.get("instructions", {}) if isinstance(operation_semantics, dict) else {}
    if isinstance(instructions, dict):
        for mnemonic, entry in instructions.items():
            if not isinstance(entry, dict):
                continue
            target = out.setdefault(str(mnemonic), {})
            for key in ("inputs", "input_output", "output"):
                if key in entry:
                    target[key] = entry[key]
            if "pcode" in entry:
                target["pcode"] = pcode_statements(entry["pcode"])
            if "pcode_by_form" in entry:
                target["pcode_by_form"] = [
                    {
                        **form,
                        "operation": pcode_statements(form.get("operation")),
                    }
                    for form in entry.get("pcode_by_form", []) or []
                    if isinstance(form, dict)
                ]
    return out


def role_names(value: Any, available: set[str]) -> list[str]:
    if value is None:
        return []
    if isinstance(value, dict):
        explicit = value.get("explicit")
        if isinstance(explicit, str) and explicit in available:
            return [explicit]
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item) in available]
    text = str(value).strip()
    if not text or text.lower() == "none":
        return []
    if text in available:
        return [text]
    out = []
    for role in sorted(available):
        if re.search(rf"\b{re.escape(role)}\b", text):
            out.append(role)
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
            for low, high in fixed_constraint_ranges(ext_start, ext_end, descriptor_variable_mask(item), WORD_BITS):
                add(1, token_field_name(1, low, high), low, high)
    return fields


def item_primary_range(item: dict[str, Any]) -> tuple[int, int]:
    if item.get("kind") in {"extended", "extended_alias"}:
        return parse_range(str(item.get("extension_root_payload", "0x000")))
    if item.get("kind") == "compact_alias" and item.get("alias_payloads"):
        values = [parse_hex(value) for value in item.get("alias_payloads", [])]
        return min(values), max(values)
    if item.get("primary_payloads"):
        values = [parse_hex(value) for value in item.get("primary_payloads", [])]
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


def render_registers(spec: dict[str, Any]) -> str:
    names = (
        spec_register_names(spec, "D")
        + spec_register_names(spec, "A")
        + [name for name, _value in special_register_named_values(spec, "S")]
        + spec_register_names(spec, "F")
    )
    dbank_name = str(
        spec.get("registers", {})
        .get("data_register_banking", {})
        .get("selector", {})
        .get("name", "")
    )
    if dbank_name and dbank_name not in names:
        names.append(dbank_name)
    for item in spec.get("registers", {}).get("special_registers", []) or []:
        if isinstance(item, dict):
            name = str(item.get("name", ""))
        else:
            name = str(item)
        if name == "FLAGS":
            continue
        if name and name not in names:
            names.append(name)
    lines = ["define register offset=0 size=8 ["]
    for index in range(0, len(names), 8):
        lines.append("  " + " ".join(names[index : index + 8]))
    lines.append("];")
    lines.append("")
    lines.append(f"define register offset=0x1000 size=1 [ {' '.join(flag_pseudo_registers(spec))} ];")
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
        lines.append(f"attach variables [ {' '.join(d_fields)} ] [ {' '.join(spec_register_names(spec, 'D'))} ];")
    if db_fields:
        namespace = int(
            spec.get("registers", {})
            .get("data_register_banking", {})
            .get("selector", {})
            .get("architectural_namespace", 0)
        )
        db_names = " ".join(f'"DB{i}"' for i in range(namespace))
        lines.append(f"attach names [ {' '.join(db_fields)} ] [ {db_names} ];")
    if a_fields:
        lines.append(f"attach variables [ {' '.join(a_fields)} ] [ {' '.join(spec_register_names(spec, 'A'))} ];")
    if s_fields:
        names = " ".join(special_register_attach_names(spec, "S"))
        lines.append(f"attach variables [ {' '.join(s_fields)} ] [ {names} ];")
    if f_fields:
        lines.append(f"attach variables [ {' '.join(f_fields)} ] [ {' '.join(spec_register_names(spec, 'F'))} ];")
    if c_fields:
        names = " ".join(f'"{name}"' for name in condition_names(spec))
        lines.append(f"attach names [ {' '.join(c_fields)} ] [ {names} ];")
    if order_fields:
        names = " ".join(f'"{name}"' for name, _value in spec_named_values(spec, "memory_order", include_reserved=True))
        lines.append(f"attach names [ {' '.join(order_fields)} ] [ {names} ];")
    for kind in sorted(spec_size_kinds(spec)):
        values = size_kind_suffixes(spec, kind)
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
        (field for field in fields.values() if field.kind in {"EA", "IMM_EA"}),
        key=lambda field: (field.token, field.low, field.high, field.name),
    )
    for field in ea_fields:
        table = ea_table_name(field.name)
        lines.extend(render_ea_table(table, field.name))
    lines.append("")
    payload_tables: set[tuple[str, int, int]] = set()
    bitmap_kinds = (
        active_spec()
        .get("instructions", {})
        .get("operand_schema", {})
        .get("bitmap_operands", {})
    )
    bitmap_kind_names = sorted(bitmap_kinds) if isinstance(bitmap_kinds, dict) else ["bitmap16"]
    for start in range(1, MAX_INSTRUCTION_WORDS):
        for kind in ("imm", "imm16", "relative_imm", "cr", "payload", *bitmap_kind_names):
            payload_tables.add((kind, start, 1))
        for kind, counts in (
            ("imm32", (2,)),
            ("imm64", (4,)),
            ("relative_imm", (2, 4)),
        ):
            for count in counts:
                if start + count - 1 < MAX_INSTRUCTION_WORDS:
                    payload_tables.add((kind, start, count))
    for kind, start, count in sorted(payload_tables, key=lambda item: (item[1], item[2], item[0])):
        table = payload_table_name(kind, start, count)
        tokens = " ; ".join(payload_tokens(start, count))
        display = f"word{start}" if count == 1 else f'"<{kind}>"'
        lines.append(f"{table}: {display} is {tokens} {{ {payload_export_statement(kind, start, count)} }}")
    return "\n".join(lines)


def render_ea_table(table: str, field_name: str) -> list[str]:
    lines: list[str] = []
    for index in range(8):
        lines.append(f'{table}: "D{index}" is {field_name}=0x{index:x} {{ export D{index}; }}')
    for index in range(8):
        value = 0x08 + index
        lines.append(f'{table}: "A{index}" is {field_name}=0x{value:x} {{ export A{index}; }}')
    for index in range(8):
        value = 0x10 + index
        lines.append(f'{table}: "[A{index}]" is {field_name}=0x{value:x} {{ export *:8 A{index}; }}')
    special = {
        0x2F: ('"SP"', "SP"),
    }
    for value, (display, export) in special.items():
        lines.append(f"{table}: {display} is {field_name}=0x{value:x} {{ export {export}; }}")
    used = set(range(0x00, 0x18)) | set(special)
    for value in range(64):
        if value in used:
            continue
        lines.append(
            f'{table}: "<ea:{value:02x}>" is {field_name}=0x{value:x} '
            f"{{ ea_tmp:8 = 0x{value:x}; export *[const]:8 ea_tmp; }}"
        )
    return lines


def payload_export_statement(kind: str, start: int, count: int) -> str:
    words = [f"word{index}" for index in range(start, start + count)]
    if count == 1:
        return f"export *[const]:8 {words[0]};"
    lines = [f"payload_word0:2 = {words[0]};", "payload_tmp:8 = zext(payload_word0);"]
    for offset, word in enumerate(words[1:], start=1):
        lines.append(f"payload_word{offset}:2 = {word};")
        lines.append(f"payload_part{offset}:8 = zext(payload_word{offset}) << {16 * offset};")
        lines.append(f"payload_tmp = payload_tmp | payload_part{offset};")
    lines.append("export *[const]:8 payload_tmp;")
    return " ".join(lines)


def display_name_for_field(field: dict[str, Any], token: int | None = None) -> str:
    effective_token = field_token(field, token if token is not None else 0)
    name = sleigh_field_name(field, effective_token)
    if str(field.get("kind")) in {"EA", "IMM_EA"}:
        return ea_table_name(name)
    return name


def payload_operand_display(kind: str, start_word: int, available_words: int) -> tuple[str, int]:
    count = payload_words_for_kind(kind, default_count=max(1, available_words))
    if count <= 0:
        count = 1
    count = min(count, max(1, available_words))
    return payload_table_name(kind, start_word, count), count


def raw_field_symbol(field: dict[str, Any], token: int | None = None) -> str:
    return sleigh_field_name(field, field_token(field, token if token is not None else 0))


def constructor_operands(
    item: dict[str, Any],
    fields: list[dict[str, Any]],
    token: int,
    payload_count: int,
) -> tuple[str, list[str], dict[str, OperandBinding]]:
    mnemonic = str(item.get("mnemonic", item.get("id", "")))
    size_field = next((field for field in fields if is_size_kind(str(field.get("kind")))), None)
    fixed_size = str(item.get("fixed_size_suffix", ""))
    suffix = f"^{display_name_for_field(size_field, token)}" if size_field else (f".{fixed_size}" if fixed_size else "")
    condition_suffix = ""
    order_suffix = ""
    operands: list[str] = []
    payload_terms: list[str] = []
    bindings: dict[str, OperandBinding] = {}
    payload_cursor = 1 if item.get("kind") in {"compact", "compact_alias"} else 2
    field_payload_tokens = {field_token(field, token) for field in fields if field_token(field, token) >= payload_cursor}
    consumed_payload_tokens = set(field_payload_tokens)

    root_field = root_condition_field(item)
    for operand in item.get("operands", []) or []:
        operand_text = str(operand)
        if is_implicit_operand(operand_text):
            continue
        role, _typ = split_operand(operand_text)
        field = field_for_operand(fields, operand_text)
        kind = infer_operand_kind(operand_text, field)
        if kind == "condition":
            field = root_field or field
            if field is not None:
                condition_display = display_name_for_field(field, 0 if field is root_field else token)
                condition_ref = raw_field_symbol(field, 0 if field is root_field else token)
                bindings[role] = OperandBinding(role, kind, condition_display, condition_ref)
                if is_condition_mnemonic(mnemonic):
                    condition_suffix = f"^{condition_display}"
                else:
                    operands.append(condition_display)
            continue
        if field is not None:
            display = display_name_for_field(field, token)
            ref = display if kind in {"EA", "IMM_EA"} else raw_field_symbol(field, token)
            bindings[role] = OperandBinding(role, kind, display, ref)
            if kind == "memory_order":
                order_suffix = f'"/"^{display}'
                continue
            operands.append(display)
            continue
        if kind == "SPREG":
            operands.append('"SP"')
            bindings[role] = OperandBinding(role, kind, "SP", "SP")
            continue
        while payload_cursor in consumed_payload_tokens:
            payload_cursor += 1
        available_words = max(0, payload_count - (payload_cursor - (1 if item.get("kind") in {"compact", "compact_alias"} else 2)))
        if available_words > 0:
            symbol, used = payload_operand_display(kind, payload_cursor, available_words)
            operands.append(symbol)
            payload_terms.append(symbol)
            bindings[role] = OperandBinding(role, kind, symbol, symbol)
            consumed_payload_tokens.update(range(payload_cursor, payload_cursor + used))
            payload_cursor += used
            continue
        operands.append(f'"<{sanitize(role).lower()}>"')
        bindings[role] = OperandBinding(role, kind, "0", "0")

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
    add_canonical_role_aliases(bindings)
    return f"{mnemonic}{suffix}{order_suffix}{operand_text}", payload_terms, bindings


def add_canonical_role_aliases(bindings: dict[str, OperandBinding]) -> None:
    aliases = (
        ("src", "imm"),
        ("src", "lhs"),
        ("dst", "rhs"),
        ("constant", "constant_id"),
        ("page", "src"),
    )
    for canonical, alias in aliases:
        if canonical not in bindings and alias in bindings:
            aliased = bindings[alias]
            bindings[canonical] = OperandBinding(
                role=canonical,
                kind=aliased.kind,
                display=aliased.display,
                ref=aliased.ref,
            )


def constructor_display(item: dict[str, Any], fields: list[dict[str, Any]], token: int, payload_count: int) -> tuple[str, list[str]]:
    display, payload_terms, _bindings = constructor_operands(item, fields, token, payload_count)
    return display, payload_terms


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


def size_expression(item: dict[str, Any], fields: list[dict[str, Any]], token: int) -> str:
    size_field = next((field for field in fields if is_size_kind(str(field.get("kind")))), None)
    if size_field is not None:
        return "8"
    fixed_size = str(item.get("fixed_size_suffix", "")).upper()
    return str(size_code_bytes(active_spec(), fixed_size) if fixed_size else 8)


def size_init_lines(item: dict[str, Any], fields: list[dict[str, Any]], token: int) -> list[str]:
    size_field = next((field for field in fields if is_size_kind(str(field.get("kind")))), None)
    if size_field is None:
        return [f"local size_v:8 = {size_expression(item, fields, token)};"]

    kind = str(size_field.get("kind", ""))
    values = size_values(kind)
    if not values:
        return ["local size_v:8 = 8;"]
    ref = raw_field_symbol(size_field, token)
    byte_widths = dict(size_kind_byte_widths(active_spec(), kind))
    lines = ["local size_v:8 = 8;", f"local size_code_v:{size_kind_width(active_spec(), kind)} = {ref};"]
    for value, byte_width in byte_widths.items():
        next_label = f"<size_next_{value}>"
        lines.append(f"if (size_code_v != 0x{value:x}) goto {next_label};")
        lines.append(f"size_v = {byte_width};")
        lines.append("goto <size_done>;")
        lines.append(next_label)
    lines.append("<size_done>")
    return lines


def render_condition_read(role: str, ref: str) -> list[str]:
    done_label = f"<{role}_condition_done>"
    checks = condition_sleigh_checks(active_spec())
    code_var = f"{role}_code_v"
    lines = [f"local {role}_v:8 = 0;", f"local {code_var}:1 = {ref};"]
    for value, expr in checks:
        next_label = f"<{role}_condition_next_{value}>"
        lines.append(f"if ({code_var} != 0x{value:x}) goto {next_label};")
        if expr == "1":
            lines.append(f"{role}_v = 1;")
        elif expr != "0":
            false_label = f"<{role}_condition_false_{value}>"
            lines.append(f"if (!({expr})) goto {false_label};")
            lines.append(f"{role}_v = 1;")
            lines.append(false_label)
        lines.append(f"goto {done_label};")
        lines.append(next_label)
    lines.append(done_label)
    return lines


def render_role_read(binding: OperandBinding) -> list[str]:
    role = sanitize(binding.role)
    kind = binding.kind
    if kind == "condition":
        return render_condition_read(role, binding.ref)
    if kind == "memory_order":
        return [f"local {role}_v:8 = {binding.ref};"]
    if kind in DIRECT_REGISTER_KINDS:
        return [f"local {role}_v:8 = {binding.ref};"]
    return [f"local {role}_v:8 = {binding.ref};"]


def render_role_init(binding: OperandBinding) -> list[str]:
    role = sanitize(binding.role)
    return [f"local {role}_v:8 = 0;"]


def render_role_write(binding: OperandBinding) -> list[str]:
    role = sanitize(binding.role)
    kind = binding.kind
    if kind in {"condition", "memory_order"}:
        return []
    if kind in DIRECT_REGISTER_KINDS:
        return [f"{binding.ref} = {role}_v;"]
    if kind in {"EA", "IMM_EA"}:
        return [f"{binding.ref} = {role}_v;"]
    return []


def operand_kind_profile(operands: list[Any]) -> list[str]:
    profile: list[str] = []
    for operand in operands:
        _role, kind = split_operand(str(operand))
        profile.append(infer_operand_kind(kind).upper())
    return profile


def form_pcode_matches(item: dict[str, Any], form: dict[str, Any]) -> bool:
    expected = [str(kind).upper() for kind in form.get("operands", []) or []]
    return expected == operand_kind_profile(item.get("operands", []) or [])


def select_pcode_body(mnemonic: str, item: dict[str, Any], semantics: dict[str, Any]) -> Any:
    for form in semantics.get("pcode_by_form", []) or []:
        if isinstance(form, dict) and form_pcode_matches(item, form):
            return form.get("operation")
    return semantics.get("pcode")


def pcode_role_references(lines: list[str]) -> set[str]:
    local_roles: set[str] = set()
    for line in lines:
        match = LOCAL_PCODE_VAR_RE.match(line)
        if match and match.group(1).endswith("_v"):
            local_roles.add(match.group(1)[:-2])

    out: set[str] = set()
    for line in lines:
        for match in PCODE_ROLE_VAR_RE.finditer(line):
            role = match.group(1) or match.group(2)
            if role not in PCODE_SCRATCH_ROLES and role not in local_roles:
                out.add(role)
    return out


def mentioned_roles(lines: list[str], bindings: dict[str, OperandBinding]) -> set[str]:
    return pcode_role_references(lines) & set(bindings)


def render_pcode_body(
    item: dict[str, Any],
    fields: list[dict[str, Any]],
    token: int,
    bindings: dict[str, OperandBinding],
    semantics_by_mnemonic: dict[str, dict[str, Any]],
) -> str:
    mnemonic = str(item.get("mnemonic", ""))
    semantics = semantics_by_mnemonic.get(mnemonic, {})
    body = select_pcode_body(mnemonic, item, semantics)
    if body is None:
        raise ValueError(f"missing SLEIGH pcode for {mnemonic}")
    lines = [line for line in body if line.strip()]
    if not lines:
        raise ValueError(f"empty SLEIGH pcode for {mnemonic}")
    available = set(bindings)
    input_output_roles = role_names(semantics.get("input_output"), available)
    read_roles = set(role_names(semantics.get("inputs"), available)) | set(input_output_roles)
    write_roles = set(role_names(semantics.get("output"), available)) | set(input_output_roles)
    referenced_roles = pcode_role_references(lines)
    missing_roles = sorted(referenced_roles - set(bindings))
    if missing_roles:
        raise ValueError(
            f"{mnemonic} SLEIGH pcode references unbound operand roles: "
            + ", ".join(missing_roles)
        )
    mentioned = mentioned_roles(lines, bindings)
    read_roles |= mentioned - write_roles
    declared_roles = read_roles | write_roles | mentioned

    rendered: list[str] = [
        *size_init_lines(item, fields, token),
        "local result_v:8 = 0;",
        "local tmp_v:8 = 0;",
        "local carry_v:8 = 0;",
        "local borrow_v:8 = 0;",
    ]
    for role in sorted(declared_roles):
        binding = bindings.get(role)
        if binding is None:
            raise ValueError(f"{mnemonic} SLEIGH pcode role {role} is not bound")
        if role in read_roles:
            rendered.extend(render_role_read(binding))
        else:
            rendered.extend(render_role_init(binding))
        rendered.append(f"local {sanitize(role)}_old_v:8 = {sanitize(role)}_v;")
    rendered.extend(lines)
    for role in sorted(write_roles):
        binding = bindings.get(role)
        if binding is not None:
            rendered.extend(render_role_write(binding))
    return "{\n" + "\n".join(f"  {line}" for line in rendered) + "\n}"


def render_constructors(allocations: list[dict[str, Any]], semantics_by_mnemonic: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Instruction constructors. Semantic bodies come directly from",
        "# operation_semantics pcode entries.",
    ]
    for item in sorted(allocations, key=constructor_sort_key):
        fields = item_fields(item)
        token = 0 if item.get("kind") in {"compact", "compact_alias"} else 1
        payload_count = payload_word_count(item)
        display, payload_terms, bindings = constructor_operands(item, fields, token, payload_count)
        pattern = item_pattern(item, fields, payload_terms)
        body = render_pcode_body(item, fields, token, bindings, semantics_by_mnemonic)
        lines.append(f":{display} is {pattern} {body}")
    return "\n".join(lines)


def render_tool_template(name: str, values: dict[str, Any]) -> str:
    text = (Path(__file__).parent / "templates" / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace(f"@{key}@", str(value))
    return text


def render(spec_dir: str, spec: dict[str, Any], plan: dict[str, Any], allocation_path: Path) -> str:
    global ACTIVE_SPEC
    ACTIVE_SPEC = spec
    allocations = collect_allocations(spec, plan)
    fields = collect_sleigh_fields(allocations)
    semantics_by_mnemonic = operation_semantics_map(spec)
    solver = plan.get("solver", {})
    header = render_tool_template(
        "sleigh_header.slaspec",
        {
            "SPEC_DIR": spec_dir,
            "ALLOCATION_PATH": allocation_path,
            "SOLVER_STATUS": solver.get("status", plan.get("solver", "unknown")),
            "CONSTRUCTOR_COUNT": len(allocations),
        },
    )
    sections = [
        header.rstrip(),
        render_registers(spec),
        render_tokens(fields),
        render_attaches(spec, fields),
        render_operand_tables(fields),
        render_constructors(allocations, semantics_by_mnemonic),
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
