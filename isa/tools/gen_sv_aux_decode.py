#!/usr/bin/env python3
"""Generate SystemVerilog prefix and effective-address decode snippets."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any

sys.dont_write_bytecode = True

from isa_spec import load_spec  # noqa: E402
from spec_model.encoding import ea_segment_named_values
from template_utils import render_tool_template  # noqa: E402


ACTIVE_SPEC: dict[str, Any] | None = None


def set_active_spec(spec: dict[str, Any]) -> None:
    global ACTIVE_SPEC
    ACTIVE_SPEC = spec


def active_spec() -> dict[str, Any]:
    if ACTIVE_SPEC is None:
        raise RuntimeError("active ISA spec is not set")
    return ACTIVE_SPEC


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


def parse_bit_pattern(pattern: str) -> tuple[int, int, int]:
    bits = "".join(ch if ch in "01" else "?" for ch in pattern if ch.isalnum() or ch == "?")
    if not bits:
        raise ValueError(f"empty bit pattern: {pattern!r}")
    mask = 0
    value = 0
    for ch in bits:
        mask <<= 1
        value <<= 1
        if ch in "01":
            mask |= 1
            value |= int(ch)
    return len(bits), mask, value


def hex_lit(width: int, value: int) -> str:
    digits = (width + 3) // 4
    return f"{width}'h{value:0{digits}x}"


def bin_pattern(width: int, mask: int, value: int) -> str:
    chars: list[str] = []
    for bit in range(width - 1, -1, -1):
        if (mask >> bit) & 1:
            chars.append("1" if (value >> bit) & 1 else "0")
        else:
            chars.append("?")
    grouped = "_".join("".join(chars[index : index + 4]) for index in range(0, len(chars), 4))
    return f"{width}'b{grouped}"


def enum_lines(type_name: str, width: int, entries: list[tuple[str, str]]) -> list[str]:
    lines = [f"  typedef enum logic [{width - 1}:0] {{"]
    for index, (name, comment) in enumerate(entries):
        comma = "," if index != len(entries) - 1 else ""
        suffix = f" // {comment}" if comment else ""
        lines.append(f"    {name} = {width}'d{index}{comma}{suffix}")
    lines.append(f"  }} {type_name};")
    return lines


def enum_width(entries: list[tuple[str, str]]) -> int:
    return max(1, (len(entries) - 1).bit_length())


def prefix_entries(spec: dict[str, Any]) -> list[dict[str, Any]]:
    entries = list((spec.get("prefixes") or {}).get("prefixes") or [])
    return sorted(entries, key=lambda item: int(item.get("value", 256)) if "value" in item else 256)


def prefix_enum_name(name: str) -> str:
    return "BR_PREFIX_" + re.sub(r"[^A-Za-z0-9]+", "_", name.upper()).strip("_")


def update_enum_name(name: str) -> str:
    return "BR_UPDATE_" + re.sub(r"[^A-Za-z0-9]+", "_", name.upper()).strip("_")


def access_enum_name(name: str) -> str:
    return "BR_ACCESS_" + re.sub(r"[^A-Za-z0-9]+", "_", name.upper()).strip("_")


def repeat_enum_name(name: str) -> str:
    return "BR_REPEAT_" + re.sub(r"[^A-Za-z0-9]+", "_", name.upper()).strip("_")


def prefix_byte_width(spec: dict[str, Any]) -> int:
    prefix_word = (spec.get("prefixes") or {}).get("prefix_word") or {}
    word_bits = int(prefix_word.get("bytes_per_instruction", 1)) * 8
    slot_count = len(prefix_word.get("fill_order") or prefix_word.get("decode_order") or [None])
    return max(1, word_bits // max(1, slot_count))


def prefix_case_literal(prefix: dict[str, Any], width: int) -> str:
    if "value" in prefix:
        return hex_lit(width, int(prefix["value"]))
    pattern = str(prefix.get("pattern", ""))
    pattern_width, mask, value = parse_bit_pattern(pattern)
    if pattern_width != width:
        name = prefix.get("name")
        raise ValueError(
            f"prefix pattern width mismatch for {name}: "
            f"pattern has {pattern_width} bits, prefix byte has {width} bits"
        )
    return bin_pattern(pattern_width, mask, value)


def pattern_field_positions(pattern: str) -> dict[str, list[int]]:
    bits = [ch for ch in pattern if ch.isalnum() or ch in "?-"]
    width = len(bits)
    positions: dict[str, list[int]] = {}
    for index, ch in enumerate(bits):
        if ch.isalpha() and ch not in {"x", "X", "z", "Z"}:
            positions.setdefault(ch, []).append(width - 1 - index)
    return positions


def field_slice_expr(source: str, pattern: str, field: str) -> str:
    positions = pattern_field_positions(pattern).get(field, [])
    if not positions:
        raise ValueError(f"field {field!r} is not present in prefix pattern {pattern!r}")
    ordered = sorted(positions, reverse=True)
    if ordered == list(range(ordered[0], ordered[-1] - 1, -1)):
        if ordered[0] == ordered[-1]:
            return f"{source}[{ordered[0]}]"
        return f"{source}[{ordered[0]}:{ordered[-1]}]"
    return "{" + ", ".join(f"{source}[{bit}]" for bit in ordered) + "}"


def prefix_decode_assignments(prefix: dict[str, Any]) -> list[str]:
    assignments: list[str] = ["r.valid = 1'b1", f"r.kind = {prefix_enum_name(str(prefix.get('name')))}"]
    pattern = str(prefix.get("pattern", ""))
    condition_field = ((prefix.get("condition") or {}) if isinstance(prefix.get("condition"), dict) else {}).get("field")
    if condition_field and pattern:
        assignments.append(f"r.condition = {field_slice_expr('prefix_byte', pattern, str(condition_field))}")
    operand = (prefix.get("operand") or {}) if isinstance(prefix.get("operand"), dict) else {}
    if operand.get("role") == "counter" and operand.get("field") and pattern:
        assignments.append(f"r.counter = {field_slice_expr('prefix_byte', pattern, str(operand.get('field')))}")
    return assignments


def sv_statement_block(assignments: list[str]) -> str:
    return " ".join(f"{assignment};" for assignment in assignments)


def prefix_update_entries(prefixes: list[dict[str, Any]]) -> list[tuple[str, str]]:
    return [("BR_UPDATE_NONE", "")] + [
        (update_enum_name(str(prefix.get("name"))), "")
        for prefix in prefixes
        if prefix.get("group") == "ea_update"
    ]


def prefix_access_entries(prefixes: list[dict[str, Any]]) -> list[tuple[str, str]]:
    return [("BR_ACCESS_C", "")] + [
        (access_enum_name(str(prefix.get("name"))), "")
        for prefix in prefixes
        if prefix.get("group") == "access_domain"
    ]


def prefix_repeat_entries(prefixes: list[dict[str, Any]]) -> list[tuple[str, str]]:
    return [("BR_REPEAT_NONE", "")] + [
        (repeat_enum_name(str(prefix.get("name"))), "")
        for prefix in prefixes
        if prefix.get("group") == "repeat"
    ]


def prefix_apply_lines(prefixes: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for prefix in prefixes:
        name = str(prefix.get("name"))
        group = str(prefix.get("group", ""))
        kind = prefix_enum_name(name)
        if group == "neutral":
            lines.append(f"      {kind}: begin end")
        elif name == "NOSPEC":
            lines.append(f"      {kind}: r.nospec = 1'b1;")
        elif name == "SATURATE":
            lines.append(f"      {kind}: r.saturate = 1'b1;")
        elif name == "NONTEMPORAL":
            lines.append(f"      {kind}: r.nontemporal = 1'b1;")
        elif group == "ea_update":
            lines.append(f"      {kind}: r.update_mode = {update_enum_name(name)};")
        elif group == "access_domain":
            lines.append(f"      {kind}: r.access_mode = {access_enum_name(name)};")
        elif group == "repeat":
            lines.append(f"      {kind}: begin r.repeat_kind = {repeat_enum_name(name)}; r.repeat_condition = prefix.condition; r.repeat_counter = prefix.counter; end")
        elif group == "repeat_boundary":
            lines.append(f"      {kind}: r.end_group = 1'b1;")
        else:
            lines.append(f"      {kind}: begin end")
    return lines


def prefix_synth_apply_lines(
    prefixes: list[dict[str, Any]],
    prefix_width: int,
    update_indexes: dict[str, int],
    access_indexes: dict[str, int],
    repeat_indexes: dict[str, int],
) -> list[str]:
    lines: list[str] = []
    for prefix in prefixes:
        name = str(prefix.get("name"))
        group = str(prefix.get("group", ""))
        literal = prefix_case_literal(prefix, prefix_width)
        pattern = str(prefix.get("pattern", ""))
        if group == "neutral":
            lines.append(f"        {literal}: begin end")
        elif name == "NOSPEC":
            lines.append(f"        {literal}: nospec_o = 1'b1;")
        elif name == "SATURATE":
            lines.append(f"        {literal}: saturate_o = 1'b1;")
        elif name == "NONTEMPORAL":
            lines.append(f"        {literal}: nontemporal_o = 1'b1;")
        elif group == "ea_update":
            lines.append(f"        {literal}: update_mode_o = 3'd{update_indexes[update_enum_name(name)]};")
        elif group == "access_domain":
            lines.append(f"        {literal}: access_mode_o = 2'd{access_indexes[access_enum_name(name)]};")
        elif group == "repeat":
            operand = (prefix.get("operand") or {}) if isinstance(prefix.get("operand"), dict) else {}
            counter = field_slice_expr("p", pattern, str(operand.get("field"))) if operand.get("field") else "3'd0"
            condition_field = ((prefix.get("condition") or {}) if isinstance(prefix.get("condition"), dict) else {}).get("field")
            condition = field_slice_expr("p", pattern, str(condition_field)) if condition_field else "4'd0"
            lines.append(
                f"        {literal}: begin repeat_kind_o = 2'd{repeat_indexes[repeat_enum_name(name)]}; "
                f"repeat_condition_o = {condition}; repeat_counter_o = {counter}; end"
            )
        elif group == "repeat_boundary":
            lines.append(f"        {literal}: end_group_o = 1'b1;")
    return lines


def compact_ea_forms(spec: dict[str, Any]) -> list[dict[str, Any]]:
    return list((spec.get("ea", {}).get("ea_forms", {}) or {}).get("compact", []) or [])


def extended_ea_forms(spec: dict[str, Any]) -> list[dict[str, Any]]:
    return list(spec.get("ea", {}).get("extended_ea_forms", []) or [])


def extended_ea_forms_by_mode(spec: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for form in extended_ea_forms(spec):
        grouped.setdefault(int(form.get("value")), []).append(form)
    for forms in grouped.values():
        forms.sort(key=lambda form: 1 if form.get("escape") == "S32_INDEXED_EXTENDED" else 0)
    return dict(sorted(grouped.items()))


def ea_form_names(spec: dict[str, Any]) -> dict[str, str]:
    used = {"BR_EA_INVALID"}
    names: dict[str, str] = {}
    for form in compact_ea_forms(spec) + extended_ea_forms(spec):
        name = str(form.get("name", ""))
        names[name] = sv_ident("BR_EA", name, used)
    return names


def extra_words(form: dict[str, Any]) -> int:
    if "extra_words" in form:
        return int(form.get("extra_words") or 0)
    displacement = str(form.get("displacement", ""))
    absolute = str(form.get("absolute", ""))
    width_source = displacement or absolute
    if width_source.endswith("16"):
        return 1
    if width_source.endswith("32"):
        return 2
    if width_source.endswith("64"):
        return 4
    operands = form.get("operands") or []
    if isinstance(operands, list):
        for operand in operands:
            if isinstance(operand, dict) and operand.get("type") == "DISP":
                return int(operand.get("words") or max(1, int(operand.get("width", 0)) // 16))
    return 0


def base_kind(form: dict[str, Any]) -> str:
    if form.get("absolute"):
        return "ABS"
    base = str(form.get("base", ""))
    register_class = str(form.get("register_class", ""))
    if base:
        return base
    if register_class:
        return register_class
    if str(form.get("class", "")) == "immediate":
        return "IMM"
    return "NONE"


def segment_kind(form: dict[str, Any]) -> str:
    if form.get("fixed_segment"):
        return str(form["fixed_segment"])
    if form.get("default_segment"):
        return str(form["default_segment"])
    base = str(form.get("base", ""))
    if base == "PC":
        return "CS"
    if base == "SP":
        return "SS"
    return "DS"


def is_register_form(form: dict[str, Any]) -> bool:
    return str(form.get("class", "")) == "register"


def is_memory_form(form: dict[str, Any]) -> bool:
    return bool(form.get("memory")) or str(form.get("class", "")) == "memory"


def is_immediate_form(form: dict[str, Any]) -> bool:
    return str(form.get("class", "")) == "immediate"


def has_base_reg(form: dict[str, Any]) -> bool:
    return base_kind(form) in {"D", "A"}


def has_index_reg(form: dict[str, Any]) -> bool:
    return bool(form.get("index"))


def displacement_words(form: dict[str, Any]) -> int:
    if has_displacement_payload(form) or form.get("absolute") or is_immediate_form(form):
        return extra_words(form)
    return 0


def has_displacement_payload(form: dict[str, Any]) -> bool:
    displacement = form.get("displacement")
    return bool(displacement) and str(displacement) != "none"


def sv_lines(lines: list[str]) -> str:
    return "\n".join(lines)


def emit_prefix_package(spec: dict[str, Any]) -> str:
    prefixes = prefix_entries(spec)
    prefix_width = prefix_byte_width(spec)
    kind_entries = [("BR_PREFIX_INVALID", "")] + [
        (prefix_enum_name(str(prefix.get("name"))), str(prefix.get("name")))
        for prefix in prefixes
    ]
    update_entries = prefix_update_entries(prefixes)
    access_entries = prefix_access_entries(prefixes)
    repeat_entries = prefix_repeat_entries(prefixes)
    decode_cases = [
        f"      {prefix_case_literal(prefix, prefix_width)}: begin {sv_statement_block(prefix_decode_assignments(prefix))} end"
        for prefix in prefixes
    ]
    return render_tool_template(
        "bedrock_prefix_decode_pkg.sv",
        {
            "KIND_ENUM": sv_lines(enum_lines("bedrock_prefix_kind_e", enum_width(kind_entries), kind_entries)),
            "UPDATE_ENUM": sv_lines(enum_lines("bedrock_update_mode_e", enum_width(update_entries), update_entries)),
            "ACCESS_ENUM": sv_lines(enum_lines("bedrock_access_mode_e", enum_width(access_entries), access_entries)),
            "REPEAT_ENUM": sv_lines(enum_lines("bedrock_repeat_kind_e", enum_width(repeat_entries), repeat_entries)),
            "PREFIX_DECODE_CASES": sv_lines(decode_cases),
            "PREFIX_APPLY_CASES": sv_lines(prefix_apply_lines(prefixes)),
        },
    )


def emit_prefix_module() -> str:
    return render_tool_template("bedrock_prefix_decode.sv", {})


def emit_ea_package(spec: dict[str, Any]) -> str:
    set_active_spec(spec)
    form_names = ea_form_names(spec)
    entries = [("BR_EA_INVALID", "")]
    entries += [(form_names[str(form.get("name", ""))], str(form.get("name", ""))) for form in compact_ea_forms(spec) + extended_ea_forms(spec)]
    width = 6
    compact_case_lines: list[str] = []
    for form in compact_ea_forms(spec):
        name = str(form.get("name", ""))
        width_bits, mask, value = parse_bit_pattern(str(form.get("pattern", "")))
        if width_bits != 6:
            raise ValueError(f"compact EA pattern for {name} is {width_bits} bits, expected 6")
        compact_case_lines.append(f"      {bin_pattern(6, mask, value)}: begin // {name}")
        compact_case_lines += ea_assignment_lines(form, form_names[name], compact=True, indent="        ")
        compact_case_lines.append("      end")

    reserved_case_lines: list[str] = []
    for reserved in spec.get("ea", {}).get("reserved_forms", []) or []:
        width_bits, mask, value = parse_bit_pattern(str(reserved.get("pattern", "")))
        if width_bits == 6:
            reserved_case_lines.extend(
                [
                    f"      {bin_pattern(6, mask, value)}: begin // {reserved.get('name', '')}",
                    "        r.reserved = 1'b1;",
                    "      end",
                ]
            )

    extended_case_lines: list[str] = []
    for mode_value, mode_forms in extended_ea_forms_by_mode(spec).items():
        extended_case_lines.append(f"      5'h{mode_value:02x}: begin")
        for index, form in enumerate(mode_forms):
            name = str(form.get("name", ""))
            condition = "signed32_index_escape" if form.get("escape") == "S32_INDEXED_EXTENDED" else "!signed32_index_escape"
            keyword = "if" if index == 0 else "else if"
            extended_case_lines.append(f"        {keyword} ({condition}) begin // {name}")
            extended_case_lines += ea_assignment_lines(form, form_names[name], compact=False, indent="          ")
            if form.get("segment_field") == "reserved_zero":
                extended_case_lines.append("          r.segment_valid = (segment == 3'd0);")
                fixed = str(form.get("fixed_segment", "DS"))
                extended_case_lines.append(f"          r.segment = {segment_enum(fixed)};")
            elif form.get("segment_selectable"):
                extended_case_lines.append("          r.segment = bedrock_ea_segment_decode(segment);")
                extended_case_lines.append("          r.segment_valid = 1'b1;")
            extended_case_lines.append("        end")
        extended_case_lines += [
            "        else begin",
            "          r.reserved = 1'b1;",
            "        end",
            "      end",
        ]

    return render_tool_template(
        "bedrock_ea_decode_pkg.sv",
        {
            "EA_FORM_ENUM": sv_lines(enum_lines("bedrock_ea_form_e", width, entries)),
            "EA_BASE_ENUM": sv_lines(
                enum_lines(
                    "bedrock_ea_base_e",
                    enum_width(ea_base_entries(spec)),
                    ea_base_entries(spec),
                )
            ),
            "EA_SEGMENT_ENUM": sv_lines(
                enum_lines(
                    "bedrock_ea_segment_e",
                    enum_width(ea_segment_entries(spec)),
                    ea_segment_entries(spec),
                )
            ),
            "EA_SEGMENT_DECODE_CASES": sv_lines(ea_segment_decode_cases(spec)),
            "COMPACT_EA_CASES": sv_lines(compact_case_lines),
            "RESERVED_COMPACT_EA_CASES": sv_lines(reserved_case_lines),
            "EXTENDED_EA_CASES": sv_lines(extended_case_lines),
        },
    )


def ea_segment_entries(spec: dict[str, Any]) -> list[tuple[str, str]]:
    return [(f"BR_EA_SEG_{name.upper()}", "") for name, _value in ea_segment_named_values(spec)]


def ea_segment_decode_cases(spec: dict[str, Any]) -> list[str]:
    values = ea_segment_named_values(spec)
    if not values:
        raise ValueError("ea.extended_ea_descriptor.segment_values is required")
    lines = []
    for name, value in values:
        lines.append(f"      3'd{value}: bedrock_ea_segment_decode = {segment_enum(name)};")
    lines.append(f"      default: bedrock_ea_segment_decode = {segment_enum(values[-1][0])};")
    return lines


def ea_base_entries(spec: dict[str, Any]) -> list[tuple[str, str]]:
    names = ["NONE"]
    for form in compact_ea_forms(spec) + extended_ea_forms(spec):
        base = base_kind(form).upper()
        if base and base not in names:
            names.append(base)
    return [(f"BR_EA_BASE_{name}", "") for name in names]


def ea_base_names(spec: dict[str, Any]) -> list[str]:
    return [entry[0].removeprefix("BR_EA_BASE_") for entry in ea_base_entries(spec)]


def segment_enum(name: str) -> str:
    valid = {segment_name.upper() for segment_name, _value in ea_segment_named_values(active_spec())}
    upper = name.upper()
    if upper not in valid:
        raise ValueError(f"unknown EA segment {name}")
    return f"BR_EA_SEG_{upper}"


def base_enum(name: str) -> str:
    upper = name.upper()
    if upper not in ea_base_names(active_spec()):
        raise ValueError(f"unknown EA base {name}")
    return f"BR_EA_BASE_{upper}"


def ea_assignment_lines(form: dict[str, Any], form_enum: str, compact: bool, indent: str) -> list[str]:
    base = base_kind(form)
    disp_words = displacement_words(form)
    payload_words = extra_words(form) + (0 if compact else 1)
    name = str(form.get("name", ""))
    lines = [
        f"{indent}r.valid = 1'b1;",
        f"{indent}r.form = {form_enum};",
        f"{indent}r.is_register = 1'b{1 if is_register_form(form) else 0};",
        f"{indent}r.is_memory = 1'b{1 if is_memory_form(form) else 0};",
        f"{indent}r.is_immediate = 1'b{1 if is_immediate_form(form) else 0};",
        f"{indent}r.update_eligible = 1'b{1 if form.get('update_eligible') else 0};",
        f"{indent}r.segment_selectable = 1'b{1 if form.get('segment_selectable') else 0};",
        f"{indent}r.segment = {segment_enum(segment_kind(form))};",
        f"{indent}r.base = {base_enum(base)};",
        f"{indent}r.has_base_reg = 1'b{1 if has_base_reg(form) else 0};",
        f"{indent}r.has_index_reg = 1'b{1 if has_index_reg(form) else 0};",
        f"{indent}r.has_displacement = 1'b{1 if has_displacement_payload(form) else 0};",
        f"{indent}r.has_absolute = 1'b{1 if form.get('absolute') else 0};",
        f"{indent}r.displacement_words = 3'd{disp_words};",
        f"{indent}r.payload_words = 3'd{payload_words};",
    ]
    if compact:
        if name == "EXTENDED":
            lines += [f"{indent}r.needs_descriptor = 1'b1;", f"{indent}r.payload_words = 3'd1;"]
        elif name == "S32_INDEXED_EXTENDED":
            lines += [
                f"{indent}r.needs_descriptor = 1'b1;",
                f"{indent}r.signed32_index_escape = 1'b1;",
                f"{indent}r.payload_words = 3'd1;",
            ]
        elif base in {"D", "A"}:
            lines.append(f"{indent}r.base_reg = ea[2:0];")
    else:
        if base == "A":
            lines.append(f"{indent}r.base_reg = extra[7:5];")
        if form.get("index"):
            lines.append(f"{indent}r.index_reg = extra[4:2];")
            lines.append(f"{indent}r.scale_log2 = extra[1:0];")
        if form.get("index_extension") == "signed32_to_64":
            lines.append(f"{indent}r.signed32_index_escape = 1'b1;")
    return lines


def emit_ea_module() -> str:
    return render_tool_template("bedrock_ea_decode.sv", {})


def emit_prefix_synth(spec: dict[str, Any]) -> str:
    prefixes = prefix_entries(spec)
    prefix_width = prefix_byte_width(spec)
    update_entries = prefix_update_entries(prefixes)
    access_entries = prefix_access_entries(prefixes)
    repeat_entries = prefix_repeat_entries(prefixes)
    update_indexes = {name: index for index, (name, _) in enumerate(update_entries)}
    access_indexes = {name: index for index, (name, _) in enumerate(access_entries)}
    repeat_indexes = {name: index for index, (name, _) in enumerate(repeat_entries)}
    return render_tool_template(
        "bedrock_prefix_decode_synth.sv",
        {
            "PREFIX_SYNTH_APPLY_CASES": sv_lines(
                prefix_synth_apply_lines(prefixes, prefix_width, update_indexes, access_indexes, repeat_indexes)
            ),
        },
    )


def emit_ea_synth(spec: dict[str, Any]) -> str:
    set_active_spec(spec)
    form_names = ea_form_names(spec)
    form_localparam_lines: list[str] = []
    for index, form in enumerate(compact_ea_forms(spec) + extended_ea_forms(spec), start=1):
        form_localparam_lines.append(f"  localparam [5:0] {form_names[str(form.get('name', ''))]} = 6'd{index}; // {form.get('name', '')}")

    compact_case_lines: list[str] = []
    for form in compact_ea_forms(spec):
        name = str(form.get("name", ""))
        width_bits, mask, value = parse_bit_pattern(str(form.get("pattern", "")))
        if width_bits == 6:
            compact_case_lines.append(f"      {bin_pattern(6, mask, value)}: begin // {name}")
            compact_case_lines += ea_synth_assignment_lines(form, form_names[name], compact=True, indent="        ")
            compact_case_lines.append("      end")

    reserved_case_lines: list[str] = []
    for reserved in spec.get("ea", {}).get("reserved_forms", []) or []:
        width_bits, mask, value = parse_bit_pattern(str(reserved.get("pattern", "")))
        if width_bits == 6:
            reserved_case_lines.append(f"      {bin_pattern(6, mask, value)}: begin reserved_o = 1'b1; end")

    extended_case_lines: list[str] = []
    for mode_value, mode_forms in extended_ea_forms_by_mode(spec).items():
        extended_case_lines.append(f"        5'h{mode_value:02x}: begin")
        for index, form in enumerate(mode_forms):
            name = str(form.get("name", ""))
            expected_s32 = bool(form.get("escape") == "S32_INDEXED_EXTENDED")
            keyword = "if" if index == 0 else "else if"
            extended_case_lines.append(f"          {keyword} (signed32_escape == 1'b{1 if expected_s32 else 0}) begin // {name}")
            extended_case_lines += ea_synth_assignment_lines(form, form_names[name], compact=False, indent="            ")
            if form.get("segment_field") == "reserved_zero":
                extended_case_lines.append("            valid_o = valid_o && (seg == 3'd0);")
                extended_case_lines.append("            segment_valid_o = (seg == 3'd0);")
                extended_case_lines.append(f"            segment_o = {segment_synth_value(str(form.get('fixed_segment', 'DS')))};")
            else:
                if form.get("segment_selectable"):
                    extended_case_lines.append("            segment_o = seg;")
                extended_case_lines.append("            segment_valid_o = 1'b1;")
            extended_case_lines.append("          end")
        extended_case_lines += ["          else begin reserved_o = 1'b1; end", "        end"]

    return render_tool_template(
        "bedrock_ea_decode_synth.sv",
        {
            "EA_FORM_LOCALPARAMS": sv_lines(form_localparam_lines),
            "COMPACT_EA_CASES": sv_lines(compact_case_lines),
            "RESERVED_COMPACT_EA_CASES": sv_lines(reserved_case_lines),
            "EXTENDED_EA_CASES": sv_lines(extended_case_lines),
        },
    )


def segment_synth_value(name: str) -> str:
    values = {segment_name.upper(): value for segment_name, value in ea_segment_named_values(active_spec())}
    upper = name.upper()
    if upper not in values:
        raise ValueError(f"unknown EA segment {name}")
    return f"3'd{values[upper]}"


def base_synth_value(name: str) -> str:
    names = ea_base_names(active_spec())
    upper = name.upper()
    if upper not in names:
        raise ValueError(f"unknown EA base {name}")
    return f"3'd{names.index(upper)}"


def ea_synth_assignment_lines(form: dict[str, Any], form_enum: str, compact: bool, indent: str) -> list[str]:
    base = base_kind(form)
    name = str(form.get("name", ""))
    payload_words = extra_words(form) + (0 if compact else 1)
    lines = [
        f"{indent}valid_o = 1'b1;",
        f"{indent}form_o = {form_enum};",
        f"{indent}is_register_o = 1'b{1 if is_register_form(form) else 0};",
        f"{indent}is_memory_o = 1'b{1 if is_memory_form(form) else 0};",
        f"{indent}is_immediate_o = 1'b{1 if is_immediate_form(form) else 0};",
        f"{indent}update_eligible_o = 1'b{1 if form.get('update_eligible') else 0};",
        f"{indent}segment_selectable_o = 1'b{1 if form.get('segment_selectable') else 0};",
        f"{indent}segment_o = {segment_synth_value(segment_kind(form))};",
        f"{indent}base_o = {base_synth_value(base)};",
        f"{indent}has_base_reg_o = 1'b{1 if has_base_reg(form) else 0};",
        f"{indent}has_index_reg_o = 1'b{1 if has_index_reg(form) else 0};",
        f"{indent}has_displacement_o = 1'b{1 if has_displacement_payload(form) else 0};",
        f"{indent}has_absolute_o = 1'b{1 if form.get('absolute') else 0};",
        f"{indent}displacement_words_o = 3'd{displacement_words(form)};",
        f"{indent}payload_words_o = 3'd{payload_words};",
    ]
    if compact:
        if name == "EXTENDED":
            lines += [f"{indent}needs_descriptor_o = 1'b1;", f"{indent}payload_words_o = 3'd1;"]
        elif name == "S32_INDEXED_EXTENDED":
            lines += [
                f"{indent}needs_descriptor_o = 1'b1;",
                f"{indent}signed32_escape = 1'b1;",
                f"{indent}signed32_index_escape_o = 1'b1;",
                f"{indent}payload_words_o = 3'd1;",
            ]
        elif base in {"D", "A"}:
            lines.append(f"{indent}base_reg_o = ea_i[2:0];")
    else:
        if base == "A":
            lines.append(f"{indent}base_reg_o = extra[7:5];")
        if form.get("index"):
            lines.append(f"{indent}index_reg_o = extra[4:2];")
            lines.append(f"{indent}scale_log2_o = extra[1:0];")
        if form.get("index_extension") == "signed32_to_64":
            lines.append(f"{indent}signed32_escape = 1'b1;")
            lines.append(f"{indent}signed32_index_escape_o = 1'b1;")
    return lines


def write(path: str, text: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("--prefix-package", default="build/generated/bedrock_prefix_decode_pkg.sv")
    parser.add_argument("--prefix-module", default="build/generated/bedrock_prefix_decode.sv")
    parser.add_argument("--prefix-synth-module", default="build/generated/bedrock_prefix_decode_synth.sv")
    parser.add_argument("--ea-package", default="build/generated/bedrock_ea_decode_pkg.sv")
    parser.add_argument("--ea-module", default="build/generated/bedrock_ea_decode.sv")
    parser.add_argument("--ea-synth-module", default="build/generated/bedrock_ea_decode_synth.sv")
    args = parser.parse_args(argv)

    spec = load_spec(args.spec_dir)
    write(args.prefix_package, emit_prefix_package(spec))
    write(args.prefix_module, emit_prefix_module())
    write(args.prefix_synth_module, emit_prefix_synth(spec))
    write(args.ea_package, emit_ea_package(spec))
    write(args.ea_module, emit_ea_module())
    write(args.ea_synth_module, emit_ea_synth(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
