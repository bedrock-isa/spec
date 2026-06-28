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
from template_utils import render_tool_template  # noqa: E402


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_repg_fast_policy(spec_path: Path) -> dict[str, set[str]]:
    spec = load_spec(spec_path)
    attributes = (
        spec.get("instructions", {})
        .get("operation_semantics", {})
        .get("operation_attributes", {})
    )
    streaming = attributes.get("streaming_candidate", {}) or {}

    def collect(mapping: dict[str, Any], *keys: str) -> set[str]:
        out: set[str] = set()
        for key in keys:
            value = mapping.get(key, []) or []
            if isinstance(value, list):
                out.update(str(item).upper() for item in value)
        return out

    return {
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


def contiguous_ranges(values: list[int]) -> list[tuple[int, int]]:
    if not values:
        return []
    out: list[tuple[int, int]] = []
    start = values[0]
    end = values[0]
    for value in values[1:]:
        if value == end + 1:
            end = value
            continue
        out.append((start, end))
        start = end = value
    out.append((start, end))
    return out


def value_set_patterns(width: int, values: list[int]) -> list[str]:
    patterns: list[str] = []
    for start, end in contiguous_ranges(sorted(set(values))):
        patterns.extend(range_patterns(width, start, end))
    return patterns


def ranges_overlap(ranges: list[tuple[int, int]]) -> bool:
    high_water = -1
    for start, end in sorted(ranges):
        if start <= high_water:
            return True
        high_water = max(high_water, end)
    return False


def form_repg_fast_attributes(item: dict[str, Any], policy: dict[str, set[str]]) -> dict[str, bool]:
    mnemonic = str(item.get("mnemonic", "")).upper()
    return {
        "repg_fast_candidate": mnemonic in policy["streaming"],
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
    emitted_patterns: set[str],
    emitted_values: set[int],
) -> list[str]:
    exact_values = exact_primary_values(item)
    values = exact_values if exact_values else list(range(start, end + 1))
    active_values = [value for value in sorted(set(values)) if value not in emitted_values]
    patterns = value_set_patterns(width, active_values)
    out: list[str] = []
    for pattern in patterns:
        if pattern in emitted_patterns:
            continue
        emitted_patterns.add(pattern)
        out.append(pattern)
    emitted_values.update(active_values)
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


FieldFormatField = tuple[str, int, int, int]
FieldFormatSignature = tuple[FieldFormatField, ...]


def opcode_key(item: dict[str, Any]) -> str:
    mnemonic = str(item.get("mnemonic", ""))
    return mnemonic if mnemonic else str(item.get("id", ""))


def assign_opcode_ids(items: list[dict[str, Any]]) -> dict[str, str]:
    used = {"BR_OPCODE_INVALID"}
    names: dict[str, str] = {}
    for item in sorted(items, key=decode_priority):
        key = opcode_key(item)
        if key in names:
            continue
        names[key] = sv_ident("BR_OPCODE", key, used)
    return names


def field_format_signature(item: dict[str, Any]) -> FieldFormatSignature:
    fields = all_fields(item)
    return tuple(sorted(
        {
            (
                str(field.get("kind", "")) or "NONE",
                int(field.get("token", 0)),
                int(field.get("low_bit", 0)),
                int(field.get("width", 0)),
            )
            for field in fields
        },
        key=lambda field: (field[1], field[2], field[0], field[3]),
    ))


def field_format_sort_key(signature: FieldFormatSignature) -> tuple[int, FieldFormatSignature]:
    return len(signature), signature


def field_format_label(signature: FieldFormatSignature) -> str:
    if not signature:
        return "NO_FIELDS"
    parts: list[str] = []
    for kind, token, low, width in signature:
        parts.append(f"{kind}{width}@{token}:{low}")
    return "_".join(parts)


def assign_field_format_ids(items: list[dict[str, Any]]) -> dict[FieldFormatSignature, str]:
    names: dict[FieldFormatSignature, str] = {(): "BR_FIELD_FORMAT_NONE"}
    signatures = sorted(
        {field_format_signature(item) for item in items if field_format_signature(item)},
        key=field_format_sort_key,
    )
    for index, signature in enumerate(signatures, start=1):
        names[signature] = f"BR_FIELD_FORMAT_F{index:03d}"
    return names


def field_format_fields(signature: FieldFormatSignature) -> list[dict[str, Any]]:
    return [
        {
            "kind": kind,
            "token": token,
            "low_bit": low,
            "width": width,
        }
        for kind, token, low, width in signature
    ]


def field_format_token_words(signature: FieldFormatSignature) -> int:
    if not signature:
        return 1
    return max(token for _kind, token, _low, _width in signature) + 1


def sv_packed_slice(slot: int, width: int) -> str:
    low = slot * width
    high = low + width - 1
    return f"[{high}:{low}]"


def token_word_name(token: int) -> str:
    if token < 0 or token > 7:
        raise RuntimeError(f"field token {token} is outside the full-decode extraction window")
    return f"token{token}_word"


def word_part_expr(token: int, low: int, width: int) -> str:
    word = token_word_name(token)
    if width == 1:
        return f"{word}[{low}]"
    return f"{word}[{low + width - 1}:{low}]"


def zero_extend_expr(expr: str, width: int, target_width: int) -> str:
    if width == target_width:
        return expr
    if width > target_width:
        return f"{expr}[{target_width - 1}:0]"
    return f"{{{target_width - width}'d0, {expr}}}"


def assign_root_ids(roots: list[str]) -> dict[str, str]:
    used = {"BR_EXT_ROOT_NONE"}
    return {root: sv_ident("BR_EXT_ROOT", root.removeprefix("EXT."), used) for root in sorted(roots)}


def form_required_words(item: dict[str, Any], fields: list[dict[str, Any]]) -> int:
    return max(required_word_count(item, fields), max(1, min(8, int(item.get("min_words", 1)))))


def default_required_words(item: dict[str, Any]) -> int:
    return 2 if item.get("kind") in {"extended", "extended_alias"} else 1


def append_required_words_override(lines: list[str], item: dict[str, Any], indent: str, target: str) -> None:
    required = form_required_words(item, all_fields(item))
    field_token_words = field_format_token_words(field_format_signature(item))
    decode_baseline = max(default_required_words(item), field_token_words)
    if required > decode_baseline:
        lines.append(f"{indent}{target} = 4'd{required};")


def append_repg_fast_assignments(
    lines: list[str],
    item: dict[str, Any],
    repg_fast_policy: dict[str, set[str]],
    indent: str,
    *,
    target_prefix: str = "r.",
    target_suffix: str = "",
) -> None:
    attrs = form_repg_fast_attributes(item, repg_fast_policy)
    if attrs["repg_fast_candidate"]:
        lines.append(f"{indent}{target_prefix}repg_fast_candidate{target_suffix} = 1'b1;")


def emit_decode_assignment(
    lines: list[str],
    item: dict[str, Any],
    opcode_names: dict[str, str],
    field_format_names: dict[FieldFormatSignature, str],
    repg_fast_policy: dict[str, set[str]],
    indent: str,
    *,
    target_prefix: str = "r.",
) -> None:
    lines.extend(
        [
            f"{indent}{target_prefix}valid = 1'b1;",
            f"{indent}{target_prefix}opcode_id = {opcode_names[opcode_key(item)]};",
            f"{indent}{target_prefix}field_format_id = {field_format_names[field_format_signature(item)]};",
        ]
    )
    append_required_words_override(lines, item, indent, f"{target_prefix}required_words")
    append_repg_fast_assignments(lines, item, repg_fast_policy, indent, target_prefix=target_prefix)


def sv_lines(lines: list[str]) -> str:
    return "\n".join(lines)


def emit_package(plan: dict[str, Any], repg_fast_policy: dict[str, set[str]]) -> str:
    items = allocation_items(plan)
    forms = sorted(items, key=decode_priority)
    opcode_names = assign_opcode_ids(forms)
    field_format_names = assign_field_format_ids(forms)
    root_ranges = root_payload_ranges(forms)
    root_names = assign_root_ids(list(root_ranges))
    field_format_items = sorted(
        (signature for signature in field_format_names if signature),
        key=field_format_sort_key,
    )

    opcode_bits = bits_for_count(len(opcode_names) + 1)
    field_format_bits = bits_for_count(len(field_format_names))
    root_bits = bits_for_count(len(root_names) + 1)

    opcode_enum_lines: list[str] = []
    opcode_items = sorted(opcode_names, key=lambda key: opcode_names[key])
    for index, key in enumerate(opcode_items, start=1):
        comma = "," if index != len(opcode_items) else ""
        opcode_enum_lines.append(f"    {opcode_names[key]} = {opcode_bits}'d{index}{comma} // {key}")

    field_format_enum_lines: list[str] = []
    for index, signature in enumerate(field_format_items, start=1):
        comma = "," if index != len(field_format_items) else ""
        field_format_enum_lines.append(
            f"    {field_format_names[signature]} = {field_format_bits}'d{index}{comma} // {field_format_label(signature)}"
        )

    ext_root_enum_lines: list[str] = []
    for index, root in enumerate(sorted(root_names), start=1):
        comma = "," if index != len(root_names) else ""
        ext_root_enum_lines.append(f"    {root_names[root]} = {root_bits}'d{index}{comma} // {root}")

    primary_decode_lines: list[str] = []
    emitted_primary_patterns: set[str] = set()
    emitted_primary_values: set[int] = set()
    for item in sorted(compact_items(forms), key=decode_case_priority):
        p_start, p_end = primary_range(item)
        for pattern in unique_decode_patterns(item, 12, p_start, p_end, emitted_primary_patterns, emitted_primary_values):
            primary_decode_lines.append(f"      {pattern}: begin // {item.get('id', '')}")
            emit_decode_assignment(primary_decode_lines, item, opcode_names, field_format_names, repg_fast_policy, "        ")
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
                emit_decode_assignment(extended_decode_lines, item, opcode_names, field_format_names, repg_fast_policy, "          ")
                extended_decode_lines.append("        end")
        else:
            extended_decode_lines.append("        unique casez (extension_word)")
            for item in root_items:
                e_start, e_end = extended_range(item)
                for pattern in range_patterns(16, e_start, e_end):
                    extended_decode_lines.append(f"          {pattern}: begin // {item.get('id', '')}")
                    emit_decode_assignment(extended_decode_lines, item, opcode_names, field_format_names, repg_fast_policy, "            ")
                    extended_decode_lines.append("          end")
            extended_decode_lines.extend(
                [
                    "          default: begin",
                    "          end",
                    "        endcase",
                ]
            )
        extended_decode_lines.append("      end")

    field_format_token_word_lines: list[str] = []
    for signature in field_format_items:
        token_words = field_format_token_words(signature)
        if token_words <= 1:
            continue
        field_format_token_word_lines.append(
            f"      {field_format_names[signature]}: r = 4'd{token_words}; // {field_format_label(signature)}"
        )

    field_format_extract_lines: list[str] = []
    field_format_ea1_descriptor_word_lines: list[str] = []
    for signature in field_format_items:
        fields = field_format_fields(signature)
        token_words = field_format_token_words(signature)
        field_format_extract_lines.append(f"      {field_format_names[signature]}: begin // {field_format_label(signature)}")
        field_format_extract_lines.append(f"        r.token_words = 4'd{token_words};")
        ea_index = 0
        for field in fields:
            kind = str(field.get("kind", "")) or "NONE"
            token = int(field.get("token", 0))
            low = int(field.get("low_bit", 0))
            width = int(field.get("width", 0))
            if kind in {"EA", "IMM_EA"} and ea_index < 2:
                ea_value = zero_extend_expr(word_part_expr(token, low, width), width, 6)
                field_format_extract_lines.extend(
                    [
                        f"        r.ea_present[{ea_index}] = 1'b1;",
                        f"        r.ea_value{sv_packed_slice(ea_index, 6)} = {ea_value};",
                    ]
                )
                if ea_index == 0:
                    field_format_extract_lines.append(
                        f"        r.ea0_descriptor_word = {token_word_name(token_words)};"
                    )
                ea_index += 1
        field_format_extract_lines.append("      end")

        if ea_index >= 2:
            field_format_ea1_descriptor_word_lines.append(
                f"      {field_format_names[signature]}: begin // {field_format_label(signature)}"
            )
            field_format_ea1_descriptor_word_lines.append("        unique case (ea0_payload_words)")
            for payload_words in range(0, 8 - token_words):
                field_format_ea1_descriptor_word_lines.append(
                    f"          3'd{payload_words}: r = {token_word_name(token_words + payload_words)};"
                )
            field_format_ea1_descriptor_word_lines.extend(
                [
                    "          default: begin",
                    "          end",
                    "        endcase",
                    "      end",
                ]
            )

    return render_tool_template(
        "bedrock_decode_pkg.sv",
        {
            "OPCODE_COUNT": len(opcode_names),
            "OPCODE_BITS": opcode_bits,
            "FIELD_FORMAT_COUNT": len(field_format_names),
            "FIELD_FORMAT_BITS": field_format_bits,
            "EXT_ROOT_COUNT": len(root_names),
            "EXT_ROOT_BITS": root_bits,
            "OPCODE_ENUM_ENTRIES": sv_lines(opcode_enum_lines),
            "FIELD_FORMAT_ENUM_ENTRIES": sv_lines(field_format_enum_lines),
            "EXT_ROOT_ENUM_ENTRIES": sv_lines(ext_root_enum_lines),
            "PRIMARY_DECODE_CASES": sv_lines(primary_decode_lines),
            "EXTENDED_DECODE_CASES": sv_lines(extended_decode_lines),
            "FIELD_FORMAT_TOKEN_WORD_CASES": sv_lines(field_format_token_word_lines),
            "FIELD_FORMAT_EXTRACT_CASES": sv_lines(field_format_extract_lines),
            "FIELD_FORMAT_EA1_DESCRIPTOR_WORD_CASES": sv_lines(field_format_ea1_descriptor_word_lines),
        },
    )


def emit_module() -> str:
    return render_tool_template("bedrock_decode.sv", {})


def emit_synth_module(plan: dict[str, Any], repg_fast_policy: dict[str, set[str]]) -> str:
    items = allocation_items(plan)
    forms = sorted(items, key=decode_priority)
    opcode_names = assign_opcode_ids(forms)
    field_format_names = assign_field_format_ids(forms)
    root_ranges = root_payload_ranges(forms)
    root_names = assign_root_ids(list(root_ranges))
    field_format_items = sorted(
        (signature for signature in field_format_names if signature),
        key=field_format_sort_key,
    )

    opcode_bits = bits_for_count(len(opcode_names) + 1)
    field_format_bits = bits_for_count(len(field_format_names))
    root_bits = bits_for_count(len(root_names) + 1)

    opcode_localparam_lines: list[str] = []
    for index, key in enumerate(sorted(opcode_names, key=lambda key: opcode_names[key]), start=1):
        opcode_localparam_lines.append(
            f"  localparam [{opcode_bits - 1}:0] {opcode_names[key]} = {opcode_bits}'d{index}; // {key}"
        )

    field_format_localparam_lines: list[str] = []
    for index, signature in enumerate(field_format_items, start=1):
        field_format_localparam_lines.append(
            f"  localparam [{field_format_bits - 1}:0] {field_format_names[signature]} = "
            f"{field_format_bits}'d{index}; // {field_format_label(signature)}"
        )

    ext_root_localparam_lines: list[str] = []
    for index, root in enumerate(sorted(root_names), start=1):
        ext_root_localparam_lines.append(f"  localparam [{root_bits - 1}:0] {root_names[root]} = {root_bits}'d{index}; // {root}")

    primary_decode_lines: list[str] = []
    emitted_primary_patterns: set[str] = set()
    emitted_primary_values: set[int] = set()
    for item in sorted(compact_items(forms), key=decode_case_priority):
        p_start, p_end = primary_range(item)
        for pattern in unique_decode_patterns(item, 12, p_start, p_end, emitted_primary_patterns, emitted_primary_values):
            primary_decode_lines.extend(
                [
                    f"      {pattern}: begin // {item.get('id', '')}",
                    "        valid_o = 1'b1;",
                    f"        opcode_id_o = {opcode_names[opcode_key(item)]};",
                    f"        field_format_id_o = {field_format_names[field_format_signature(item)]};",
                ]
            )
            append_required_words_override(primary_decode_lines, item, "        ", "required_words_o")
            append_repg_fast_assignments(
                primary_decode_lines,
                item,
                repg_fast_policy,
                "        ",
                target_prefix="",
                target_suffix="_o",
            )
            primary_decode_lines.append("      end")

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
                        f"            opcode_id_o = {opcode_names[opcode_key(item)]};",
                        f"            field_format_id_o = {field_format_names[field_format_signature(item)]};",
                    ]
                )
                append_required_words_override(extended_decode_lines, item, "            ", "required_words_o")
                append_repg_fast_assignments(
                    extended_decode_lines,
                    item,
                    repg_fast_policy,
                    "            ",
                    target_prefix="",
                    target_suffix="_o",
                )
                extended_decode_lines.append("          end")
        else:
            extended_decode_lines.append("          casez (extension_word_i)")
            for item in root_items:
                e_start, e_end = extended_range(item)
                for pattern in range_patterns(16, e_start, e_end):
                    extended_decode_lines.extend(
                        [
                            f"            {pattern}: begin // {item.get('id', '')}",
                            "              valid_o = 1'b1;",
                            f"              opcode_id_o = {opcode_names[opcode_key(item)]};",
                            f"              field_format_id_o = {field_format_names[field_format_signature(item)]};",
                        ]
                    )
                    append_required_words_override(extended_decode_lines, item, "              ", "required_words_o")
                    append_repg_fast_assignments(
                        extended_decode_lines,
                        item,
                        repg_fast_policy,
                        "              ",
                        target_prefix="",
                        target_suffix="_o",
                    )
                    extended_decode_lines.append("            end")
            extended_decode_lines.extend(
                [
                    "            default: begin",
                    "            end",
                    "          endcase",
                ]
            )
        extended_decode_lines.append("        end")

    field_format_token_word_lines: list[str] = []
    for signature in field_format_items:
        token_words = field_format_token_words(signature)
        if token_words <= 1:
            continue
        field_format_token_word_lines.append(
            f"        {field_format_names[signature]}: field_format_token_words = 4'd{token_words}; // {field_format_label(signature)}"
        )

    return render_tool_template(
        "bedrock_decode_synth.sv",
        {
            "OPCODE_ID_MSB": opcode_bits - 1,
            "FIELD_FORMAT_ID_MSB": field_format_bits - 1,
            "EXT_ROOT_MSB": root_bits - 1,
            "OPCODE_BITS": opcode_bits,
            "FIELD_FORMAT_BITS": field_format_bits,
            "EXT_ROOT_BITS": root_bits,
            "OPCODE_LOCALPARAMS": sv_lines(opcode_localparam_lines),
            "FIELD_FORMAT_LOCALPARAMS": sv_lines(field_format_localparam_lines),
            "EXT_ROOT_LOCALPARAMS": sv_lines(ext_root_localparam_lines),
            "PRIMARY_DECODE_CASES": sv_lines(primary_decode_lines),
            "EXTENDED_DECODE_CASES": sv_lines(extended_decode_lines),
            "FIELD_FORMAT_TOKEN_WORD_CASES": sv_lines(field_format_token_word_lines),
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
    repg_fast_policy = load_repg_fast_policy(Path(args.spec))
    package_path = Path(args.package)
    module_path = Path(args.module)
    synth_module_path = Path(args.synth_module)
    package_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.parent.mkdir(parents=True, exist_ok=True)
    synth_module_path.parent.mkdir(parents=True, exist_ok=True)
    package_path.write_text(emit_package(plan, repg_fast_policy), encoding="utf-8")
    module_path.write_text(emit_module(), encoding="utf-8")
    synth_module_path.write_text(emit_synth_module(plan, repg_fast_policy), encoding="utf-8")
    print(f"wrote {package_path}")
    print(f"wrote {module_path}")
    print(f"wrote {synth_module_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
