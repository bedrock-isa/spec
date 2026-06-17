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
from spec_model.encoding import mnemonic_policy
from template_utils import render_tool_template  # noqa: E402


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

    allocation_policy = mnemonic_policy(spec)
    def policy_set(key: str) -> set[str]:
        value = allocation_policy.get(key, []) or []
        return {str(item).upper() for item in value} if isinstance(value, list) else set()

    return {
        "repeatable": collect(repeatable, "integer", "fpu"),
        "repg_general_extra": collect(repeatable, "state_query_general_only"),
        "streaming": collect(streaming, "integer", "fpu"),
        "fence": policy_set("fence_mnemonics"),
        "cache": policy_set("cache_management_mnemonics"),
        "tlb": policy_set("tlb_management_mnemonics"),
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
    group = str(item.get("group", "")).upper()
    return group in {"PUSH_POP", "PUSHM_POPM"}


def is_fence_form(item: dict[str, Any], policy: dict[str, set[str]]) -> bool:
    return str(item.get("mnemonic", "")).upper() in policy["fence"]


def is_tlb_cache_form(item: dict[str, Any], policy: dict[str, set[str]]) -> bool:
    group = str(item.get("group", "")).upper()
    mnemonic = str(item.get("mnemonic", "")).upper()
    return (
        "TLB" in group
        or "CACHE" in group
        or mnemonic in policy["tlb"]
        or mnemonic in policy["cache"]
    )


def is_atomic_form(item: dict[str, Any]) -> bool:
    group = str(item.get("group", "")).upper()
    category = str(item.get("category", "")).lower()
    return category == "atomic" or group in {"CMPXCHG", "FETCH_OPS"}


def form_repeat_attributes(item: dict[str, Any], policy: dict[str, set[str]]) -> dict[str, bool]:
    mnemonic = str(item.get("mnemonic", "")).upper()
    category = str(item.get("category", "")).lower()
    repeatable = mnemonic in policy["repeatable"]
    repg_general_extra = mnemonic in policy["repg_general_extra"]
    base_excluded = (
        category == "control_flow"
        or is_atomic_form(item)
        or is_stack_form(item)
        or is_tlb_cache_form(item, policy)
        or is_fence_form(item, policy)
    )
    repcc_allowed = repeatable and category not in {"control_flow", "system"} and not is_atomic_form(item)
    repg_allowed = (repeatable or repg_general_extra) and not base_excluded
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


def sv_lines(lines: list[str]) -> str:
    return "\n".join(lines)


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

    form_enum_lines: list[str] = []
    for index, item in enumerate(forms, start=1):
        comma = "," if index != len(forms) else ""
        form_enum_lines.append(f"    {form_names[str(item.get('id', ''))]} = {form_bits}'d{index}{comma} // {item.get('id', '')}")

    ext_root_enum_lines: list[str] = []
    for index, root in enumerate(sorted(root_names), start=1):
        comma = "," if index != len(root_names) else ""
        ext_root_enum_lines.append(f"    {root_names[root]} = {root_bits}'d{index}{comma} // {root}")

    field_kind_enum_lines: list[str] = []
    kind_items = [("NONE", "BR_FIELD_NONE")] + sorted(
        [(kind, name) for kind, name in kind_names.items() if kind != "NONE"],
        key=lambda item: item[1],
    )
    for index, (kind, name) in enumerate(kind_items):
        comma = "," if index != len(kind_items) - 1 else ""
        comment = "" if kind == "NONE" else f" // {kind}"
        field_kind_enum_lines.append(f"    {name} = {kind_bits}'d{index}{comma}{comment}")

    field_source_enum_lines: list[str] = []
    source_items = [("NONE", "BR_SOURCE_NONE")] + sorted(
        [(source, name) for source, name in source_names.items() if source != "NONE"],
        key=lambda item: item[1],
    )
    for index, (source, name) in enumerate(source_items):
        comma = "," if index != len(source_items) - 1 else ""
        comment = "" if source == "NONE" else f" // {source}"
        field_source_enum_lines.append(f"    {name} = {source_bits}'d{index}{comma}{comment}")

    primary_decode_lines: list[str] = []
    emitted_primary_patterns: set[str] = set()
    for item in sorted(compact_items(forms), key=decode_case_priority):
        p_start, p_end = primary_range(item)
        for pattern in unique_decode_patterns(item, 12, p_start, p_end, emitted_primary_patterns):
            primary_decode_lines.append(f"      {pattern}: begin // {item.get('id', '')}")
            emit_form_assignment(primary_decode_lines, item, form_names, "        ")
            primary_decode_lines.append("      end")

    for root in sorted(root_names):
        for start, end in root_ranges[root]:
            for pattern in range_patterns(12, start, end):
                primary_decode_lines.extend(
                    [
                        f"      {pattern}: begin // {root}",
                        "        r.valid = 1'b1;",
                        "        r.needs_extension = 1'b1;",
                        f"        r.ext_root = {root_names[root]};",
                        "      end",
                    ]
                )

    extended_by_root: dict[str, list[dict[str, Any]]] = {}
    for item in sorted(extended_items(forms), key=decode_priority):
        extended_by_root.setdefault(str(item.get("extension_root", "")), []).append(item)

    extended_decode_lines: list[str] = []
    for root in sorted(extended_by_root):
        root_items = extended_by_root[root]
        root_has_priority_overlap = ranges_overlap([extended_range(item) for item in root_items])
        extended_decode_lines.append(f"      {root_names[root]}: begin // {root}")
        if root_has_priority_overlap:
            first = True
            for item in root_items:
                e_start, e_end = extended_range(item)
                keyword = "if" if first else "else if"
                first = False
                extended_decode_lines.append(f"        {keyword} {range_condition('extension_word', 16, e_start, e_end)} begin // {item.get('id', '')}")
                emit_form_assignment(extended_decode_lines, item, form_names, "          ")
                extended_decode_lines.append("        end")
        else:
            extended_decode_lines.append("        unique casez (extension_word)")
            for item in root_items:
                e_start, e_end = extended_range(item)
                for pattern in range_patterns(16, e_start, e_end):
                    extended_decode_lines.append(f"          {pattern}: begin // {item.get('id', '')}")
                    emit_form_assignment(extended_decode_lines, item, form_names, "            ")
                    extended_decode_lines.append("          end")
            extended_decode_lines.extend(
                [
                    "          default: begin",
                    "          end",
                    "        endcase",
                ]
            )
        extended_decode_lines.append("      end")

    required_word_lines: list[str] = []
    for item in forms:
        fields = all_fields(item)
        required = form_required_words(item, fields)
        if required <= 1:
            continue
        required_word_lines.append(f"      {form_names[str(item.get('id', ''))]}: r = 4'd{required}; // {item.get('id', '')}")

    field_token_word_lines: list[str] = []
    for item in forms:
        fields = all_fields(item)
        token_words = form_field_token_words(item, fields)
        if token_words <= 1:
            continue
        field_token_word_lines.append(f"      {form_names[str(item.get('id', ''))]}: r = 4'd{token_words}; // {item.get('id', '')}")

    form_field_lines: list[str] = []
    for item in forms:
        fields = all_fields(item)
        if not fields:
            continue
        form_field_lines.append(f"      {form_names[str(item.get('id', ''))]}: begin // {item.get('id', '')}")
        form_field_lines.append("        unique case (field_index)")
        for index, field in enumerate(fields):
            kind = str(field.get("kind", "")) or "NONE"
            source = str(field.get("source", "")) or "NONE"
            token = int(field.get("token", 0))
            low = int(field.get("low_bit", 0))
            width = int(field.get("width", 0))
            form_field_lines.extend(
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
        form_field_lines.extend(
            [
                "          default: begin",
                "          end",
                "        endcase",
                "      end",
            ]
        )

    form_attribute_lines: list[str] = []
    for item in forms:
        attrs = form_repeat_attributes(item, repeat_policy)
        if not any(attrs.values()):
            continue
        form_attribute_lines.append(f"      {form_names[str(item.get('id', ''))]}: begin // {item.get('id', '')}")
        if attrs["repcc_allowed"]:
            form_attribute_lines.append("        r.repcc_allowed = 1'b1;")
        if attrs["repg_allowed"]:
            form_attribute_lines.append("        r.repg_allowed = 1'b1;")
        if attrs["repg_fast_candidate"]:
            form_attribute_lines.append("        r.repg_fast_candidate = 1'b1;")
        form_attribute_lines.append("      end")

    return render_tool_template(
        "bedrock_decode_pkg.sv",
        {
            "FORM_COUNT": len(forms),
            "FORM_BITS": form_bits,
            "EXT_ROOT_COUNT": len(root_names),
            "EXT_ROOT_BITS": root_bits,
            "FIELD_SLOTS": max_fields,
            "FIELD_KIND_BITS": kind_bits,
            "FIELD_SOURCE_BITS": source_bits,
            "FORM_ENUM_ENTRIES": sv_lines(form_enum_lines),
            "EXT_ROOT_ENUM_ENTRIES": sv_lines(ext_root_enum_lines),
            "FIELD_KIND_ENUM_ENTRIES": sv_lines(field_kind_enum_lines),
            "FIELD_SOURCE_ENUM_ENTRIES": sv_lines(field_source_enum_lines),
            "PRIMARY_DECODE_CASES": sv_lines(primary_decode_lines),
            "EXTENDED_DECODE_CASES": sv_lines(extended_decode_lines),
            "REQUIRED_WORD_CASES": sv_lines(required_word_lines),
            "FIELD_TOKEN_WORD_CASES": sv_lines(field_token_word_lines),
            "FORM_FIELD_CASES": sv_lines(form_field_lines),
            "FORM_ATTRIBUTE_CASES": sv_lines(form_attribute_lines),
        },
    )


def emit_module() -> str:
    return render_tool_template("bedrock_decode.sv", {})


def emit_synth_module(plan: dict[str, Any], repeat_policy: dict[str, set[str]]) -> str:
    items = allocation_items(plan)
    forms = sorted(items, key=decode_priority)
    form_names = assign_form_ids(forms)
    root_ranges = root_payload_ranges(forms)
    root_names = assign_root_ids(list(root_ranges))

    form_bits = bits_for_count(len(forms) + 1)
    root_bits = bits_for_count(len(root_names) + 1)

    form_localparam_lines: list[str] = []

    for index, item in enumerate(forms, start=1):
        form_localparam_lines.append(f"  localparam [{form_bits - 1}:0] {form_names[str(item.get('id', ''))]} = {form_bits}'d{index}; // {item.get('id', '')}")

    ext_root_localparam_lines: list[str] = []
    for index, root in enumerate(sorted(root_names), start=1):
        ext_root_localparam_lines.append(f"  localparam [{root_bits - 1}:0] {root_names[root]} = {root_bits}'d{index}; // {root}")

    primary_decode_lines: list[str] = []
    emitted_primary_patterns = set()
    for item in sorted(compact_items(forms), key=decode_case_priority):
        p_start, p_end = primary_range(item)
        for pattern in unique_decode_patterns(item, 12, p_start, p_end, emitted_primary_patterns):
            primary_decode_lines.extend(
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
                primary_decode_lines.extend(
                    [
                        f"      {pattern}: begin // {root}",
                        "        valid_o = 1'b1;",
                        "        needs_extension_o = 1'b1;",
                        f"        ext_root_o = {root_names[root]};",
                        "      end",
                    ]
                )

    extended_by_root: dict[str, list[dict[str, Any]]] = {}
    for item in sorted(extended_items(forms), key=decode_priority):
        extended_by_root.setdefault(str(item.get("extension_root", "")), []).append(item)

    extended_decode_lines: list[str] = []
    for root in sorted(extended_by_root):
        root_items = extended_by_root[root]
        root_has_priority_overlap = ranges_overlap([extended_range(item) for item in root_items])
        extended_decode_lines.append(f"        {root_names[root]}: begin // {root}")
        if root_has_priority_overlap:
            first = True
            for item in root_items:
                e_start, e_end = extended_range(item)
                keyword = "if" if first else "else if"
                first = False
                extended_decode_lines.extend(
                    [
                        f"          {keyword} {range_condition('extension_word_i', 16, e_start, e_end)} begin // {item.get('id', '')}",
                        "            valid_o = 1'b1;",
                        f"            alias_o = 1'b{1 if str(item.get('kind')).endswith('_alias') else 0};",
                        f"            form_id_o = {form_names[str(item.get('id', ''))]};",
                        "          end",
                    ]
                )
        else:
            extended_decode_lines.append("          casez (extension_word_i)")
            for item in root_items:
                e_start, e_end = extended_range(item)
                for pattern in range_patterns(16, e_start, e_end):
                    extended_decode_lines.extend(
                        [
                            f"            {pattern}: begin // {item.get('id', '')}",
                            "              valid_o = 1'b1;",
                            f"              alias_o = 1'b{1 if str(item.get('kind')).endswith('_alias') else 0};",
                            f"              form_id_o = {form_names[str(item.get('id', ''))]};",
                            "            end",
                        ]
                    )
            extended_decode_lines.extend(
                [
                    "            default: begin",
                    "            end",
                    "          endcase",
                ]
            )
        extended_decode_lines.append("        end")

    attribute_lines: list[str] = []
    for item in forms:
        attrs = form_repeat_attributes(item, repeat_policy)
        if not any(attrs.values()):
            continue
        attribute_lines.append(f"        {form_names[str(item.get('id', ''))]}: begin // {item.get('id', '')}")
        if attrs["repcc_allowed"]:
            attribute_lines.append("          repcc_allowed_o = 1'b1;")
        if attrs["repg_allowed"]:
            attribute_lines.append("          repg_allowed_o = 1'b1;")
        if attrs["repg_fast_candidate"]:
            attribute_lines.append("          repg_fast_candidate_o = 1'b1;")
        attribute_lines.append("        end")

    return render_tool_template(
        "bedrock_decode_synth.sv",
        {
            "FORM_ID_MSB": form_bits - 1,
            "EXT_ROOT_MSB": root_bits - 1,
            "FORM_BITS": form_bits,
            "EXT_ROOT_BITS": root_bits,
            "FORM_LOCALPARAMS": sv_lines(form_localparam_lines),
            "EXT_ROOT_LOCALPARAMS": sv_lines(ext_root_localparam_lines),
            "PRIMARY_DECODE_CASES": sv_lines(primary_decode_lines),
            "EXTENDED_DECODE_CASES": sv_lines(extended_decode_lines),
            "ATTRIBUTE_CASES": sv_lines(attribute_lines),
        },
    )


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
