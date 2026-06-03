#!/usr/bin/env python3
"""Generate SystemVerilog decode snippets from the allocated Bedrock opcode map."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

sys.dont_write_bytecode = True

from gen_asm_disasm_c import (  # noqa: E402
    allocation_items,
    all_fields,
    exact_primary_values,
    extended_range,
    primary_range,
    required_word_count,
)
from isa_spec import load_spec  # noqa: E402


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_repeat_policy(spec_path: Path) -> dict[str, set[str]]:
    spec = load_spec(spec_path)
    attributes = (
        spec.get("instructions", {})
        .get("operation_semantics", {})
        .get("operation_attributes", {})
    )
    repeatable = attributes.get("repeatable_operation", {}) or {}
    streaming = attributes.get("streaming_candidate", {}) or {}

    def collect(mapping: dict[str, Any], *keys: str) -> set[str]:
        out: set[str] = set()
        for key in keys:
            value = mapping.get(key, []) or []
            if isinstance(value, list):
                out.update(str(item).upper() for item in value)
        return out

    return {
        "repeatable": collect(repeatable, "integer", "fpu"),
        "repg_general_extra": collect(repeatable, "state_query_general_only"),
        "streaming": collect(streaming, "integer", "fpu"),
    }


def bits_for_count(count: int) -> int:
    return max(1, math.ceil(math.log2(max(2, count))))


def sv_ident(prefix: str, text: str, used: set[str]) -> str:
    body = re.sub(r"[^A-Za-z0-9]+", "_", text.upper()).strip("_")
    if not body:
        body = "UNNAMED"
    if body[0].isdigit():
        body = "_" + body
    ident = f"{prefix}_{body}"
    candidate = ident
    suffix = 2
    while candidate in used:
        candidate = f"{ident}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def sv_str(text: Any) -> str:
    return json.dumps("" if text is None else str(text), ensure_ascii=True)


def hex_lit(width: int, value: int) -> str:
    digits = (width + 3) // 4
    return f"{width}'h{value:0{digits}x}"


def range_condition(signal: str, width: int, start: int, end: int) -> str:
    max_value = (1 << width) - 1
    lo = hex_lit(width, start)
    hi = hex_lit(width, end)
    if start == 0 and end == max_value:
        return "1'b1"
    if start == end:
        return f"({signal} == {lo})"
    if start == 0:
        return f"({signal} <= {hi})"
    if end == max_value:
        return f"({signal} >= {lo})"
    return f"(({signal} >= {lo}) && ({signal} <= {hi}))"


def exact_or_range_condition(signal: str, width: int, values: list[int], start: int, end: int) -> str:
    if values:
        return "(" + " || ".join(f"({signal} == {hex_lit(width, value)})" for value in values) + ")"
    return range_condition(signal, width, start, end)


def and_conditions(*conditions: str) -> str:
    active = [condition for condition in conditions if condition != "1'b1"]
    if not active:
        return "1'b1"
    return " && ".join(active)


def range_blocks(width: int, start: int, end: int) -> list[tuple[int, int]]:
    """Return aligned power-of-two blocks as (base, size)."""
    max_size = 1 << width
    out: list[tuple[int, int]] = []
    current = start
    while current <= end:
        remaining = end - current + 1
        size = 1 << (remaining.bit_length() - 1)
        alignment = (current & -current) if current else max_size
        while size > alignment:
            size >>= 1
        out.append((current, size))
        current += size
    return out


def casez_pattern(width: int, base: int, size: int) -> str:
    wildcard_bits = int(math.log2(size))
    chars: list[str] = []
    for bit in range(width - 1, -1, -1):
        if bit < wildcard_bits:
            chars.append("?")
        else:
            chars.append("1" if (base >> bit) & 1 else "0")
    grouped = "_".join("".join(chars[index : index + 4]) for index in range(0, len(chars), 4))
    return f"{width}'b{grouped}"


def range_patterns(width: int, start: int, end: int) -> list[str]:
    return [casez_pattern(width, base, size) for base, size in range_blocks(width, start, end)]


def exact_or_range_patterns(width: int, values: list[int], start: int, end: int) -> list[str]:
    if values:
        return [casez_pattern(width, value, 1) for value in values]
    return range_patterns(width, start, end)


def ranges_overlap(ranges: list[tuple[int, int]]) -> bool:
    high_water = -1
    for start, end in sorted(ranges):
        if start <= high_water:
            return True
        high_water = max(high_water, end)
    return False


def is_stack_form(item: dict[str, Any]) -> bool:
    mnemonic = str(item.get("mnemonic", "")).upper()
    group = str(item.get("group", "")).upper()
    return mnemonic in {"PUSH", "POP", "PUSHM", "POPM"} or group in {"PUSH_POP", "PUSHM_POPM"}


def is_fence_form(item: dict[str, Any]) -> bool:
    return str(item.get("mnemonic", "")).upper() in {"RFENCE", "WFENCE", "AFENCE"}


def is_tlb_cache_form(item: dict[str, Any]) -> bool:
    group = str(item.get("group", "")).upper()
    mnemonic = str(item.get("mnemonic", "")).upper()
    return (
        "TLB" in group
        or "CACHE" in group
        or mnemonic in {"INVTLB", "INVPAGE", "INVASID", "INVDCACHE", "INVICACHE", "FLSHDCACHE", "WRBKDCACHE", "SYNCCACHE", "PREFETCH"}
    )


def is_atomic_form(item: dict[str, Any]) -> bool:
    group = str(item.get("group", "")).upper()
    mnemonic = str(item.get("mnemonic", "")).upper()
    return group == "CMPXCHG" or group == "FETCH_OPS" or mnemonic.startswith("FETCH") or mnemonic == "CMPXCHG"


def form_repeat_attributes(item: dict[str, Any], policy: dict[str, set[str]]) -> dict[str, bool]:
    mnemonic = str(item.get("mnemonic", "")).upper()
    category = str(item.get("category", "")).lower()
    repeatable = mnemonic in policy["repeatable"]
    repg_general_extra = mnemonic in policy["repg_general_extra"]
    base_forbidden = (
        category == "control_flow"
        or is_atomic_form(item)
        or is_stack_form(item)
        or is_tlb_cache_form(item)
        or is_fence_form(item)
    )
    repcc_allowed = repeatable and category not in {"control_flow", "system"} and not is_atomic_form(item)
    repg_allowed = (repeatable or repg_general_extra) and not base_forbidden
    return {
        "repcc_allowed": repcc_allowed,
        "repg_allowed": repg_allowed,
        "repg_fast_candidate": repg_allowed and mnemonic in policy["streaming"],
    }


def compact_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if str(item.get("kind")) in {"compact", "compact_alias"}]


def extended_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if str(item.get("kind")) in {"extended", "extended_alias"}]


def decode_case_priority(item: dict[str, Any]) -> tuple[int, int, int, int, str]:
    p_start, p_end = primary_range(item)
    e_start, _ = extended_range(item)
    alias_priority = 0 if str(item.get("kind")).endswith("_alias") else 1
    span = p_end - p_start
    return p_start, e_start, alias_priority, span, str(item.get("id", ""))


def unique_decode_patterns(
    item: dict[str, Any],
    width: int,
    start: int,
    end: int,
    emitted: set[str],
) -> list[str]:
    patterns = exact_or_range_patterns(width, exact_primary_values(item), start, end)
    out: list[str] = []
    for pattern in patterns:
        if pattern in emitted:
            continue
        emitted.add(pattern)
        out.append(pattern)
    return out


def decode_priority(item: dict[str, Any]) -> tuple[int, int, int, int, str]:
    p_start, _ = primary_range(item)
    e_start, _ = extended_range(item)
    alias_priority = 0 if str(item.get("kind")).endswith("_alias") else 1
    span = primary_range(item)[1] - p_start
    return p_start, e_start, alias_priority, span, str(item.get("id", ""))


def root_payload_ranges(items: list[dict[str, Any]]) -> dict[str, list[tuple[int, int]]]:
    roots: dict[str, list[tuple[int, int]]] = {}
    for item in extended_items(items):
        root = str(item.get("extension_root", ""))
        start, end = primary_range(item)
        roots.setdefault(root, []).append((start, end))
    merged: dict[str, list[tuple[int, int]]] = {}
    for root, ranges in roots.items():
        ranges = sorted(set(ranges))
        out: list[tuple[int, int]] = []
        for start, end in ranges:
            if out and start <= out[-1][1] + 1:
                out[-1] = (out[-1][0], max(out[-1][1], end))
            else:
                out.append((start, end))
        merged[root] = out
    return merged


def assign_form_ids(items: list[dict[str, Any]]) -> dict[str, str]:
    used: set[str] = set()
    names: dict[str, str] = {}
    for item in sorted(items, key=decode_priority):
        names[str(item.get("id", ""))] = sv_ident("BR_FORM", str(item.get("id", "")), used)
    return names


def assign_root_ids(roots: list[str]) -> dict[str, str]:
    used = {"BR_EXT_ROOT_NONE"}
    return {root: sv_ident("BR_EXT_ROOT", root.removeprefix("EXT."), used) for root in sorted(roots)}


FIELD_KIND_ALIASES = {
    "condition": "COND",
    "cr": "CR",
    "memory_order": "MEMORY_ORDER",
    "small_selector": "SMALL_SELECTOR",
    "selector6": "SELECTOR6",
}


def field_enum_name(prefix: str, text: str, used: set[str] | None = None) -> str:
    normalized = FIELD_KIND_ALIASES.get(str(text), str(text))
    if used is None:
        used = set()
    return sv_ident(prefix, normalized, used)


def field_kind_names(forms: list[dict[str, Any]]) -> dict[str, str]:
    kinds = {"NONE"}
    for item in forms:
        for field in all_fields(item):
            kinds.add(str(field.get("kind", "")) or "NONE")
    used = {"BR_FIELD_NONE"}
    out = {"NONE": "BR_FIELD_NONE"}
    for kind in sorted(k for k in kinds if k != "NONE"):
        out[kind] = field_enum_name("BR_FIELD", kind, used)
    return out


def field_source_names(forms: list[dict[str, Any]]) -> dict[str, str]:
    sources = {"NONE"}
    for item in forms:
        for field in all_fields(item):
            sources.add(str(field.get("source", "")) or "NONE")
    used = {"BR_SOURCE_NONE"}
    out = {"NONE": "BR_SOURCE_NONE"}
    for source in sorted(s for s in sources if s != "NONE"):
        out[source] = field_enum_name("BR_SOURCE", source, used)
    return out


def form_required_words(item: dict[str, Any], fields: list[dict[str, Any]]) -> int:
    return max(required_word_count(item, fields), max(1, min(8, int(item.get("min_words", 1)))))


def form_field_token_words(item: dict[str, Any], fields: list[dict[str, Any]]) -> int:
    base_words = 2 if item.get("kind") in {"extended", "extended_alias"} else 1
    if not fields:
        return base_words
    return max(base_words, max(int(field.get("token", 0)) for field in fields) + 1)


def emit_form_assignment(lines: list[str], item: dict[str, Any], form_names: dict[str, str], indent: str) -> None:
    lines.extend(
        [
            f"{indent}r.valid = 1'b1;",
            f"{indent}r.is_alias = 1'b{1 if str(item.get('kind')).endswith('_alias') else 0};",
            f"{indent}r.form_id = {form_names[str(item.get('id', ''))]};",
        ]
    )


def emit_package(plan: dict[str, Any], repeat_policy: dict[str, set[str]]) -> str:
    items = allocation_items(plan)
    forms = sorted(items, key=decode_priority)
    form_names = assign_form_ids(forms)
    root_ranges = root_payload_ranges(forms)
    root_names = assign_root_ids(list(root_ranges))
    kind_names = field_kind_names(forms)
    source_names = field_source_names(forms)
    max_fields = max([len(all_fields(item)) for item in forms] + [0])

    form_bits = bits_for_count(len(forms) + 1)
    root_bits = bits_for_count(len(root_names) + 1)
    kind_bits = bits_for_count(len(kind_names))
    source_bits = bits_for_count(len(source_names))

    lines: list[str] = [
        "`timescale 1ns/1ps",
        "`default_nettype none",
        "",
        "// Generated from build/generated/allocation_plan.json.",
        "// Do not edit by hand.",
        "",
        "package bedrock_decode_pkg;",
        "  import bedrock_pkg::*;",
        "",
        f"  localparam int BEDROCK_DECODE_FORM_COUNT = {len(forms)};",
        f"  localparam int BEDROCK_DECODE_FORM_ID_BITS = {form_bits};",
        f"  localparam int BEDROCK_DECODE_EXT_ROOT_COUNT = {len(root_names)};",
        f"  localparam int BEDROCK_DECODE_EXT_ROOT_BITS = {root_bits};",
        f"  localparam int BEDROCK_DECODE_FIELD_SLOTS = {max_fields};",
        f"  localparam int BEDROCK_DECODE_FIELD_KIND_BITS = {kind_bits};",
        f"  localparam int BEDROCK_DECODE_FIELD_SOURCE_BITS = {source_bits};",
        "",
        f"  typedef enum logic [BEDROCK_DECODE_FORM_ID_BITS-1:0] {{",
        f"    BR_FORM_INVALID = {form_bits}'d0,",
    ]
    for index, item in enumerate(forms, start=1):
        comma = "," if index != len(forms) else ""
        lines.append(f"    {form_names[str(item.get('id', ''))]} = {form_bits}'d{index}{comma} // {item.get('id', '')}")
    lines.extend(
        [
            "  } bedrock_form_id_e;",
            "",
            f"  typedef enum logic [BEDROCK_DECODE_EXT_ROOT_BITS-1:0] {{",
            f"    BR_EXT_ROOT_NONE = {root_bits}'d0,",
        ]
    )
    for index, root in enumerate(sorted(root_names), start=1):
        comma = "," if index != len(root_names) else ""
        lines.append(f"    {root_names[root]} = {root_bits}'d{index}{comma} // {root}")
    lines.extend(
        [
            "  } bedrock_ext_root_e;",
            "",
            f"  typedef enum logic [BEDROCK_DECODE_FIELD_KIND_BITS-1:0] {{",
        ]
    )
    kind_items = [("NONE", "BR_FIELD_NONE")] + sorted(
        [(kind, name) for kind, name in kind_names.items() if kind != "NONE"],
        key=lambda item: item[1],
    )
    for index, (kind, name) in enumerate(kind_items):
        comma = "," if index != len(kind_items) - 1 else ""
        comment = "" if kind == "NONE" else f" // {kind}"
        lines.append(f"    {name} = {kind_bits}'d{index}{comma}{comment}")
    lines.extend(
        [
            "  } bedrock_decode_field_kind_e;",
            "",
            f"  typedef enum logic [BEDROCK_DECODE_FIELD_SOURCE_BITS-1:0] {{",
        ]
    )
    source_items = [("NONE", "BR_SOURCE_NONE")] + sorted(
        [(source, name) for source, name in source_names.items() if source != "NONE"],
        key=lambda item: item[1],
    )
    for index, (source, name) in enumerate(source_items):
        comma = "," if index != len(source_items) - 1 else ""
        comment = "" if source == "NONE" else f" // {source}"
        lines.append(f"    {name} = {source_bits}'d{index}{comma}{comment}")
    lines.extend(
        [
            "  } bedrock_decode_field_source_e;",
            "",
            "  typedef struct packed {",
            "    logic valid;",
            "    bedrock_decode_field_kind_e kind;",
            "    bedrock_decode_field_source_e source;",
            "    logic [1:0] token;",
            "    logic [3:0] low_bit;",
            "    logic [4:0] width;",
            "  } bedrock_decode_field_meta_t;",
            "",
            "  typedef struct packed {",
            "    logic valid;",
            "    logic needs_extension;",
            "    logic is_alias;",
            "    bedrock_form_id_e form_id;",
            "    bedrock_ext_root_e ext_root;",
            "  } bedrock_primary_decode_t;",
            "",
            "  typedef struct packed {",
            "    logic valid;",
            "    logic is_alias;",
            "    bedrock_form_id_e form_id;",
            "  } bedrock_extended_decode_t;",
            "",
            "  typedef struct packed {",
            "    logic repcc_allowed;",
            "    logic repg_allowed;",
            "    logic repg_fast_candidate;",
            "  } bedrock_form_attributes_t;",
            "",
            "  function automatic bedrock_primary_decode_t bedrock_decode_primary_payload(input primary_payload_t payload);",
            "    bedrock_primary_decode_t r;",
            "    r = '0;",
            "    r.form_id = BR_FORM_INVALID;",
            "    r.ext_root = BR_EXT_ROOT_NONE;",
            "",
        ]
    )

    lines.extend(["    priority casez (payload)"])

    emitted_primary_patterns: set[str] = set()
    for item in sorted(compact_items(forms), key=decode_case_priority):
        p_start, p_end = primary_range(item)
        for pattern in unique_decode_patterns(item, 12, p_start, p_end, emitted_primary_patterns):
            lines.append(f"      {pattern}: begin // {item.get('id', '')}")
            emit_form_assignment(lines, item, form_names, "        ")
            lines.append("      end")

    for root in sorted(root_names):
        for start, end in root_ranges[root]:
            for pattern in range_patterns(12, start, end):
                lines.extend(
                    [
                        f"      {pattern}: begin // {root}",
                        "        r.valid = 1'b1;",
                        "        r.needs_extension = 1'b1;",
                        f"        r.ext_root = {root_names[root]};",
                        "      end",
                    ]
                )

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
        ]
    )

    lines.extend(
        [
            "",
            "    return r;",
            "  endfunction",
            "",
            "  function automatic bedrock_extended_decode_t bedrock_decode_extended_opcode(",
            "    input bedrock_ext_root_e ext_root,",
            "    input logic [15:0] extension_word",
            "  );",
            "    bedrock_extended_decode_t r;",
            "    r = '0;",
            "    r.form_id = BR_FORM_INVALID;",
            "",
        ]
    )

    extended_by_root: dict[str, list[dict[str, Any]]] = {}
    for item in sorted(extended_items(forms), key=decode_priority):
        extended_by_root.setdefault(str(item.get("extension_root", "")), []).append(item)

    lines.extend(["    unique case (ext_root)"])
    for root in sorted(extended_by_root):
        root_items = extended_by_root[root]
        root_has_priority_overlap = ranges_overlap([extended_range(item) for item in root_items])
        lines.append(f"      {root_names[root]}: begin // {root}")
        if root_has_priority_overlap:
            first = True
            for item in root_items:
                e_start, e_end = extended_range(item)
                keyword = "if" if first else "else if"
                first = False
                lines.append(f"        {keyword} {range_condition('extension_word', 16, e_start, e_end)} begin // {item.get('id', '')}")
                emit_form_assignment(lines, item, form_names, "          ")
                lines.append("        end")
        else:
            lines.append("        unique casez (extension_word)")
            for item in root_items:
                e_start, e_end = extended_range(item)
                for pattern in range_patterns(16, e_start, e_end):
                    lines.append(f"          {pattern}: begin // {item.get('id', '')}")
                    emit_form_assignment(lines, item, form_names, "            ")
                    lines.append("          end")
            lines.extend(
                [
                    "          default: begin",
                    "          end",
                    "        endcase",
                ]
            )
        lines.append("      end")

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
        ]
    )

    lines.extend(
        [
            "",
            "    return r;",
            "  endfunction",
            "",
            "  function automatic logic [3:0] bedrock_decode_form_required_words(input bedrock_form_id_e form_id);",
            "    logic [3:0] r;",
            "    r = 4'd1;",
            "    unique case (form_id)",
        ]
    )

    for item in forms:
        fields = all_fields(item)
        required = form_required_words(item, fields)
        if required <= 1:
            continue
        lines.append(f"      {form_names[str(item.get('id', ''))]}: r = 4'd{required}; // {item.get('id', '')}")

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
            "    return r;",
            "  endfunction",
            "",
            "  function automatic logic [3:0] bedrock_decode_form_field_token_words(input bedrock_form_id_e form_id);",
            "    logic [3:0] r;",
            "    r = 4'd1;",
            "    unique case (form_id)",
        ]
    )

    for item in forms:
        fields = all_fields(item)
        token_words = form_field_token_words(item, fields)
        if token_words <= 1:
            continue
        lines.append(f"      {form_names[str(item.get('id', ''))]}: r = 4'd{token_words}; // {item.get('id', '')}")

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
            "    return r;",
            "  endfunction",
            "",
            "  function automatic bedrock_decode_field_meta_t bedrock_decode_form_field(",
            "    input bedrock_form_id_e form_id,",
            "    input logic [2:0] field_index",
            "  );",
            "    bedrock_decode_field_meta_t r;",
            "    r = '0;",
            "    r.kind = BR_FIELD_NONE;",
            "    r.source = BR_SOURCE_NONE;",
            "    unique case (form_id)",
        ]
    )

    for item in forms:
        fields = all_fields(item)
        if not fields:
            continue
        lines.append(f"      {form_names[str(item.get('id', ''))]}: begin // {item.get('id', '')}")
        lines.append("        unique case (field_index)")
        for index, field in enumerate(fields):
            kind = str(field.get("kind", "")) or "NONE"
            source = str(field.get("source", "")) or "NONE"
            token = int(field.get("token", 0))
            low = int(field.get("low_bit", 0))
            width = int(field.get("width", 0))
            lines.extend(
                [
                    f"          3'd{index}: begin",
                    "            r.valid = 1'b1;",
                    f"            r.kind = {kind_names[kind]};",
                    f"            r.source = {source_names[source]};",
                    f"            r.token = 2'd{token};",
                    f"            r.low_bit = 4'd{low};",
                    f"            r.width = 5'd{width};",
                    "          end",
                ]
            )
        lines.extend(
            [
                "          default: begin",
                "          end",
                "        endcase",
                "      end",
            ]
        )

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
            "    return r;",
            "  endfunction",
            "",
            "  function automatic bedrock_form_attributes_t bedrock_decode_form_attributes(input bedrock_form_id_e form_id);",
            "    bedrock_form_attributes_t r;",
            "    r = '0;",
            "    unique case (form_id)",
        ]
    )

    for item in forms:
        attrs = form_repeat_attributes(item, repeat_policy)
        if not any(attrs.values()):
            continue
        lines.append(f"      {form_names[str(item.get('id', ''))]}: begin // {item.get('id', '')}")
        if attrs["repcc_allowed"]:
            lines.append("        r.repcc_allowed = 1'b1;")
        if attrs["repg_allowed"]:
            lines.append("        r.repg_allowed = 1'b1;")
        if attrs["repg_fast_candidate"]:
            lines.append("        r.repg_fast_candidate = 1'b1;")
        lines.append("      end")

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
            "    return r;",
            "  endfunction",
            "",
            "endpackage",
            "",
            "`default_nettype wire",
            "",
        ]
    )
    return "\n".join(lines)


def emit_module() -> str:
    return "\n".join(
        [
            "`timescale 1ns/1ps",
            "`default_nettype none",
            "",
            "// Generated decode wrapper. The input extension_word_i is the first",
            "// opcode/descriptor word after word 0 and after any prefix word.",
            "",
            "module bedrock_decode",
            "  import bedrock_pkg::*;",
            "  import bedrock_decode_pkg::*;",
            "(",
            "  input  primary_payload_t  primary_payload_i,",
            "  input  logic [15:0]       extension_word_i,",
            "  output logic              valid_o,",
            "  output logic              needs_extension_o,",
            "  output logic              alias_o,",
            "  output bedrock_form_id_e  form_id_o,",
            "  output bedrock_ext_root_e ext_root_o,",
            "  output logic              repcc_allowed_o,",
            "  output logic              repg_allowed_o,",
            "  output logic              repg_fast_candidate_o",
            ");",
            "",
            "  bedrock_primary_decode_t primary_decode;",
            "  bedrock_extended_decode_t extended_decode;",
            "  bedrock_form_attributes_t attributes;",
            "",
            "  always_comb begin",
            "    primary_decode = bedrock_decode_primary_payload(primary_payload_i);",
            "    extended_decode = '0;",
            "    extended_decode.form_id = BR_FORM_INVALID;",
            "    attributes = '0;",
            "",
            "    valid_o = primary_decode.valid;",
            "    needs_extension_o = primary_decode.needs_extension;",
            "    alias_o = primary_decode.is_alias;",
            "    form_id_o = primary_decode.form_id;",
            "    ext_root_o = primary_decode.ext_root;",
            "",
            "    if (primary_decode.needs_extension) begin",
            "      extended_decode = bedrock_decode_extended_opcode(primary_decode.ext_root, extension_word_i);",
            "      valid_o = extended_decode.valid;",
            "      alias_o = extended_decode.is_alias;",
            "      form_id_o = extended_decode.form_id;",
            "    end",
            "",
            "    attributes = bedrock_decode_form_attributes(form_id_o);",
            "    repcc_allowed_o = valid_o && attributes.repcc_allowed;",
            "    repg_allowed_o = valid_o && attributes.repg_allowed;",
            "    repg_fast_candidate_o = valid_o && attributes.repg_fast_candidate;",
            "  end",
            "endmodule",
            "",
            "`default_nettype wire",
            "",
        ]
    )


def emit_synth_module(plan: dict[str, Any], repeat_policy: dict[str, set[str]]) -> str:
    items = allocation_items(plan)
    forms = sorted(items, key=decode_priority)
    form_names = assign_form_ids(forms)
    root_ranges = root_payload_ranges(forms)
    root_names = assign_root_ids(list(root_ranges))

    form_bits = bits_for_count(len(forms) + 1)
    root_bits = bits_for_count(len(root_names) + 1)

    lines: list[str] = [
        "`timescale 1ns/1ps",
        "`default_nettype none",
        "",
        "// Package-free generated decoder for synthesis/statistics tools.",
        "// The typed integration wrapper is build/generated/bedrock_decode.sv.",
        "",
        "module bedrock_decode_synth(",
        "  input  [11:0] primary_payload_i,",
        "  input  [15:0] extension_word_i,",
        "  output reg        valid_o,",
        "  output reg        needs_extension_o,",
        "  output reg        alias_o,",
        f"  output reg [{form_bits - 1}:0] form_id_o,",
        f"  output reg [{root_bits - 1}:0] ext_root_o,",
        "  output reg        repcc_allowed_o,",
        "  output reg        repg_allowed_o,",
        "  output reg        repg_fast_candidate_o",
        ");",
        "",
        f"  localparam [{form_bits - 1}:0] BR_FORM_INVALID = {form_bits}'d0;",
    ]

    for index, item in enumerate(forms, start=1):
        lines.append(f"  localparam [{form_bits - 1}:0] {form_names[str(item.get('id', ''))]} = {form_bits}'d{index}; // {item.get('id', '')}")

    lines.extend(
        [
            "",
            f"  localparam [{root_bits - 1}:0] BR_EXT_ROOT_NONE = {root_bits}'d0;",
        ]
    )
    for index, root in enumerate(sorted(root_names), start=1):
        lines.append(f"  localparam [{root_bits - 1}:0] {root_names[root]} = {root_bits}'d{index}; // {root}")

    lines.extend(
        [
            "",
            "  always @* begin",
            "    valid_o = 1'b0;",
            "    needs_extension_o = 1'b0;",
            "    alias_o = 1'b0;",
            "    form_id_o = BR_FORM_INVALID;",
            "    ext_root_o = BR_EXT_ROOT_NONE;",
            "    repcc_allowed_o = 1'b0;",
            "    repg_allowed_o = 1'b0;",
            "    repg_fast_candidate_o = 1'b0;",
            "",
            "    casez (primary_payload_i)",
        ]
    )

    emitted_primary_patterns = set()
    for item in sorted(compact_items(forms), key=decode_case_priority):
        p_start, p_end = primary_range(item)
        for pattern in unique_decode_patterns(item, 12, p_start, p_end, emitted_primary_patterns):
            lines.extend(
                [
                    f"      {pattern}: begin // {item.get('id', '')}",
                    "        valid_o = 1'b1;",
                    f"        alias_o = 1'b{1 if str(item.get('kind')).endswith('_alias') else 0};",
                    f"        form_id_o = {form_names[str(item.get('id', ''))]};",
                    "      end",
                ]
            )

    for root in sorted(root_names):
        for start, end in root_ranges[root]:
            for pattern in range_patterns(12, start, end):
                lines.extend(
                    [
                        f"      {pattern}: begin // {root}",
                        "        valid_o = 1'b1;",
                        "        needs_extension_o = 1'b1;",
                        f"        ext_root_o = {root_names[root]};",
                        "      end",
                    ]
                )

    lines.extend(
        [
            "      default: begin",
            "      end",
            "    endcase",
            "",
            "    if (needs_extension_o) begin",
            "      valid_o = 1'b0;",
            "      alias_o = 1'b0;",
            "      form_id_o = BR_FORM_INVALID;",
            "",
            "      case (ext_root_o)",
        ]
    )

    extended_by_root: dict[str, list[dict[str, Any]]] = {}
    for item in sorted(extended_items(forms), key=decode_priority):
        extended_by_root.setdefault(str(item.get("extension_root", "")), []).append(item)

    for root in sorted(extended_by_root):
        root_items = extended_by_root[root]
        root_has_priority_overlap = ranges_overlap([extended_range(item) for item in root_items])
        lines.append(f"        {root_names[root]}: begin // {root}")
        if root_has_priority_overlap:
            first = True
            for item in root_items:
                e_start, e_end = extended_range(item)
                keyword = "if" if first else "else if"
                first = False
                lines.extend(
                    [
                        f"          {keyword} {range_condition('extension_word_i', 16, e_start, e_end)} begin // {item.get('id', '')}",
                        "            valid_o = 1'b1;",
                        f"            alias_o = 1'b{1 if str(item.get('kind')).endswith('_alias') else 0};",
                        f"            form_id_o = {form_names[str(item.get('id', ''))]};",
                        "          end",
                    ]
                )
        else:
            lines.append("          casez (extension_word_i)")
            for item in root_items:
                e_start, e_end = extended_range(item)
                for pattern in range_patterns(16, e_start, e_end):
                    lines.extend(
                        [
                            f"            {pattern}: begin // {item.get('id', '')}",
                            "              valid_o = 1'b1;",
                            f"              alias_o = 1'b{1 if str(item.get('kind')).endswith('_alias') else 0};",
                            f"              form_id_o = {form_names[str(item.get('id', ''))]};",
                            "            end",
                        ]
                    )
            lines.extend(
                [
                    "            default: begin",
                    "            end",
                    "          endcase",
                ]
            )
        lines.append("        end")

    lines.extend(
        [
            "        default: begin",
            "        end",
            "      endcase",
            "    end",
            "",
            "    if (valid_o) begin",
            "      case (form_id_o)",
        ]
    )

    for item in forms:
        attrs = form_repeat_attributes(item, repeat_policy)
        if not any(attrs.values()):
            continue
        lines.append(f"        {form_names[str(item.get('id', ''))]}: begin // {item.get('id', '')}")
        if attrs["repcc_allowed"]:
            lines.append("          repcc_allowed_o = 1'b1;")
        if attrs["repg_allowed"]:
            lines.append("          repg_allowed_o = 1'b1;")
        if attrs["repg_fast_candidate"]:
            lines.append("          repg_fast_candidate_o = 1'b1;")
        lines.append("        end")

    lines.extend(
        [
            "        default: begin",
            "        end",
            "      endcase",
            "    end",
            "  end",
            "endmodule",
            "",
            "`default_nettype wire",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allocation", default="build/generated/allocation_plan.json")
    parser.add_argument("--package", default="build/generated/bedrock_decode_pkg.sv")
    parser.add_argument("--module", default="build/generated/bedrock_decode.sv")
    parser.add_argument("--synth-module", default="build/generated/bedrock_decode_synth.sv")
    parser.add_argument("--spec", default="isa/spec")
    args = parser.parse_args(argv)

    plan = load_plan(Path(args.allocation))
    repeat_policy = load_repeat_policy(Path(args.spec))
    package_path = Path(args.package)
    module_path = Path(args.module)
    synth_module_path = Path(args.synth_module)
    package_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.parent.mkdir(parents=True, exist_ok=True)
    synth_module_path.parent.mkdir(parents=True, exist_ok=True)
    package_path.write_text(emit_package(plan, repeat_policy), encoding="utf-8")
    module_path.write_text(emit_module(), encoding="utf-8")
    synth_module_path.write_text(emit_synth_module(plan, repeat_policy), encoding="utf-8")
    print(f"wrote {package_path}")
    print(f"wrote {module_path}")
    print(f"wrote {synth_module_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
