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
    return "DEFAULT"


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


def emit_prefix_package(spec: dict[str, Any]) -> str:
    lines: list[str] = [
        "`timescale 1ns/1ps",
        "`default_nettype none",
        "",
        "// Generated from isa/spec/prefixes.yaml.",
        "// Do not edit by hand.",
        "",
        "package bedrock_prefix_decode_pkg;",
        "",
    ]
    lines += enum_lines(
        "bedrock_prefix_kind_e",
        4,
        [
            ("BR_PREFIX_INVALID", ""),
            ("BR_PREFIX_NPX", "NPX"),
            ("BR_PREFIX_NOSPEC", "NOSPEC"),
            ("BR_PREFIX_SATURATE", "SATURATE"),
            ("BR_PREFIX_NONTEMPORAL", "NONTEMPORAL"),
            ("BR_PREFIX_POSTINC", "POSTINC"),
            ("BR_PREFIX_PREINC", "PREINC"),
            ("BR_PREFIX_POSTDEC", "POSTDEC"),
            ("BR_PREFIX_PREDEC", "PREDEC"),
            ("BR_PREFIX_REPCC", "REPcc"),
            ("BR_PREFIX_REPG", "REPG"),
            ("BR_PREFIX_ENDG", "ENDG"),
        ],
    )
    lines += [
        "",
        *enum_lines(
            "bedrock_update_mode_e",
            3,
            [
                ("BR_UPDATE_NONE", ""),
                ("BR_UPDATE_POSTINC", ""),
                ("BR_UPDATE_PREINC", ""),
                ("BR_UPDATE_POSTDEC", ""),
                ("BR_UPDATE_PREDEC", ""),
            ],
        ),
        "",
        *enum_lines(
            "bedrock_repeat_kind_e",
            2,
            [
                ("BR_REPEAT_NONE", ""),
                ("BR_REPEAT_REPCC", ""),
                ("BR_REPEAT_REPG", ""),
            ],
        ),
        "",
        "  typedef struct packed {",
        "    logic valid;",
        "    bedrock_prefix_kind_e kind;",
        "    logic [3:0] condition;",
        "    logic [2:0] counter;",
        "  } bedrock_prefix_byte_decode_t;",
        "",
        "  typedef struct packed {",
        "    logic valid;",
        "    bedrock_prefix_byte_decode_t low;",
        "    bedrock_prefix_byte_decode_t high;",
        "    logic nospec;",
        "    logic saturate;",
        "    logic nontemporal;",
        "    bedrock_update_mode_e update_mode;",
        "    bedrock_repeat_kind_e repeat_kind;",
        "    logic [3:0] repeat_condition;",
        "    logic [2:0] repeat_counter;",
        "    logic end_group;",
        "  } bedrock_prefix_word_decode_t;",
        "",
        "  function automatic bedrock_prefix_byte_decode_t bedrock_decode_prefix_byte(input logic [7:0] prefix_byte);",
        "    bedrock_prefix_byte_decode_t r;",
        "    r = '0;",
        "    unique casez (prefix_byte)",
        "      8'h00: begin r.valid = 1'b1; r.kind = BR_PREFIX_NPX; end",
        "      8'h01: begin r.valid = 1'b1; r.kind = BR_PREFIX_NOSPEC; end",
        "      8'h02: begin r.valid = 1'b1; r.kind = BR_PREFIX_SATURATE; end",
        "      8'h0b: begin r.valid = 1'b1; r.kind = BR_PREFIX_NONTEMPORAL; end",
        "      8'h04: begin r.valid = 1'b1; r.kind = BR_PREFIX_POSTINC; end",
        "      8'h05: begin r.valid = 1'b1; r.kind = BR_PREFIX_PREINC; end",
        "      8'h06: begin r.valid = 1'b1; r.kind = BR_PREFIX_POSTDEC; end",
        "      8'h07: begin r.valid = 1'b1; r.kind = BR_PREFIX_PREDEC; end",
        "      8'b0110_0???: begin r.valid = 1'b1; r.kind = BR_PREFIX_REPG; r.counter = prefix_byte[2:0]; end",
        "      8'h68: begin r.valid = 1'b1; r.kind = BR_PREFIX_ENDG; end",
        "      8'b1???_????: begin r.valid = 1'b1; r.kind = BR_PREFIX_REPCC; r.condition = prefix_byte[6:3]; r.counter = prefix_byte[2:0]; end",
        "      default: begin r.kind = BR_PREFIX_INVALID; end",
        "    endcase",
        "    return r;",
        "  endfunction",
        "",
        "  function automatic bedrock_prefix_word_decode_t bedrock_apply_prefix_byte(",
        "    input bedrock_prefix_word_decode_t state,",
        "    input bedrock_prefix_byte_decode_t prefix",
        "  );",
        "    bedrock_prefix_word_decode_t r;",
        "    r = state;",
        "    r.valid = r.valid && prefix.valid;",
        "    unique case (prefix.kind)",
        "      BR_PREFIX_NOSPEC: r.nospec = 1'b1;",
        "      BR_PREFIX_SATURATE: r.saturate = 1'b1;",
        "      BR_PREFIX_NONTEMPORAL: r.nontemporal = 1'b1;",
        "      BR_PREFIX_POSTINC: r.update_mode = BR_UPDATE_POSTINC;",
        "      BR_PREFIX_PREINC: r.update_mode = BR_UPDATE_PREINC;",
        "      BR_PREFIX_POSTDEC: r.update_mode = BR_UPDATE_POSTDEC;",
        "      BR_PREFIX_PREDEC: r.update_mode = BR_UPDATE_PREDEC;",
        "      BR_PREFIX_REPCC: begin r.repeat_kind = BR_REPEAT_REPCC; r.repeat_condition = prefix.condition; r.repeat_counter = prefix.counter; end",
        "      BR_PREFIX_REPG: begin r.repeat_kind = BR_REPEAT_REPG; r.repeat_counter = prefix.counter; end",
        "      BR_PREFIX_ENDG: r.end_group = 1'b1;",
        "      default: begin",
        "      end",
        "    endcase",
        "    return r;",
        "  endfunction",
        "",
        "  function automatic bedrock_prefix_word_decode_t bedrock_decode_prefix_word(input logic [15:0] prefix_word);",
        "    bedrock_prefix_word_decode_t r;",
        "    r = '0;",
        "    r.valid = 1'b1;",
        "    r.low = bedrock_decode_prefix_byte(prefix_word[7:0]);",
        "    r.high = bedrock_decode_prefix_byte(prefix_word[15:8]);",
        "    r = bedrock_apply_prefix_byte(r, r.low);",
        "    r = bedrock_apply_prefix_byte(r, r.high);",
        "    return r;",
        "  endfunction",
        "",
        "endpackage",
        "",
        "`default_nettype wire",
        "",
    ]
    return "\n".join(lines)


def emit_prefix_module() -> str:
    return "\n".join(
        [
            "`timescale 1ns/1ps",
            "`default_nettype none",
            "",
            "module bedrock_prefix_decode",
            "  import bedrock_prefix_decode_pkg::*;",
            "(",
            "  input  logic [15:0] prefix_word_i,",
            "  output logic        valid_o,",
            "  output logic        nospec_o,",
            "  output logic        saturate_o,",
            "  output logic        nontemporal_o,",
            "  output bedrock_update_mode_e update_mode_o,",
            "  output bedrock_repeat_kind_e repeat_kind_o,",
            "  output logic [3:0] repeat_condition_o,",
            "  output logic [2:0] repeat_counter_o,",
            "  output logic        end_group_o",
            ");",
            "  bedrock_prefix_word_decode_t decode;",
            "  always_comb begin",
            "    decode = bedrock_decode_prefix_word(prefix_word_i);",
            "    valid_o = decode.valid;",
            "    nospec_o = decode.nospec;",
            "    saturate_o = decode.saturate;",
            "    nontemporal_o = decode.nontemporal;",
            "    update_mode_o = decode.update_mode;",
            "    repeat_kind_o = decode.repeat_kind;",
            "    repeat_condition_o = decode.repeat_condition;",
            "    repeat_counter_o = decode.repeat_counter;",
            "    end_group_o = decode.end_group;",
            "  end",
            "endmodule",
            "",
            "`default_nettype wire",
            "",
        ]
    )


def emit_ea_package(spec: dict[str, Any]) -> str:
    form_names = ea_form_names(spec)
    entries = [("BR_EA_INVALID", "")]
    entries += [(form_names[str(form.get("name", ""))], str(form.get("name", ""))) for form in compact_ea_forms(spec) + extended_ea_forms(spec)]
    width = 6
    lines: list[str] = [
        "`timescale 1ns/1ps",
        "`default_nettype none",
        "",
        "// Generated from isa/spec/ea.yaml.",
        "// Do not edit by hand.",
        "",
        "package bedrock_ea_decode_pkg;",
        "",
        *enum_lines("bedrock_ea_form_e", width, entries),
        "",
        *enum_lines(
            "bedrock_ea_base_e",
            3,
            [
                ("BR_EA_BASE_NONE", ""),
                ("BR_EA_BASE_D", ""),
                ("BR_EA_BASE_A", ""),
                ("BR_EA_BASE_SP", ""),
                ("BR_EA_BASE_PC", ""),
                ("BR_EA_BASE_ABS", ""),
                ("BR_EA_BASE_IMM", ""),
            ],
        ),
        "",
        *enum_lines(
            "bedrock_ea_segment_e",
            3,
            [
                ("BR_EA_SEG_DEFAULT", ""),
                ("BR_EA_SEG_CS", ""),
                ("BR_EA_SEG_DS", ""),
                ("BR_EA_SEG_SS", ""),
                ("BR_EA_SEG_GS0", ""),
                ("BR_EA_SEG_GS1", ""),
                ("BR_EA_SEG_RESERVED", ""),
            ],
        ),
        "",
        "  typedef struct packed {",
        "    logic valid;",
        "    logic reserved;",
        "    logic needs_descriptor;",
        "    logic signed32_index_escape;",
        "    bedrock_ea_form_e form;",
        "    logic is_register;",
        "    logic is_memory;",
        "    logic is_immediate;",
        "    logic update_eligible;",
        "    logic segment_selectable;",
        "    logic segment_valid;",
        "    bedrock_ea_segment_e segment;",
        "    bedrock_ea_base_e base;",
        "    logic has_base_reg;",
        "    logic has_index_reg;",
        "    logic [2:0] base_reg;",
        "    logic [2:0] index_reg;",
        "    logic [1:0] scale_log2;",
        "    logic has_displacement;",
        "    logic has_absolute;",
        "    logic [2:0] displacement_words;",
        "    logic [2:0] payload_words;",
        "  } bedrock_ea_decode_t;",
        "",
        "  function automatic bedrock_ea_segment_e bedrock_ea_segment_decode(input logic [2:0] segment);",
        "    unique case (segment)",
        "      3'd0: bedrock_ea_segment_decode = BR_EA_SEG_DEFAULT;",
        "      3'd1: bedrock_ea_segment_decode = BR_EA_SEG_CS;",
        "      3'd2: bedrock_ea_segment_decode = BR_EA_SEG_DS;",
        "      3'd3: bedrock_ea_segment_decode = BR_EA_SEG_SS;",
        "      3'd4: bedrock_ea_segment_decode = BR_EA_SEG_GS0;",
        "      3'd5: bedrock_ea_segment_decode = BR_EA_SEG_GS1;",
        "      default: bedrock_ea_segment_decode = BR_EA_SEG_RESERVED;",
        "    endcase",
        "  endfunction",
        "",
        "  function automatic bedrock_ea_decode_t bedrock_decode_compact_ea(input logic [5:0] ea);",
        "    bedrock_ea_decode_t r;",
        "    r = '0;",
        "    r.segment_valid = 1'b1;",
        "    unique casez (ea)",
    ]
    for form in compact_ea_forms(spec):
        name = str(form.get("name", ""))
        width_bits, mask, value = parse_bit_pattern(str(form.get("pattern", "")))
        if width_bits != 6:
            raise ValueError(f"compact EA pattern for {name} is {width_bits} bits, expected 6")
        lines.append(f"      {bin_pattern(6, mask, value)}: begin // {name}")
        lines += ea_assignment_lines(form, form_names[name], compact=True, indent="        ")
        lines.append("      end")
    for reserved in spec.get("ea", {}).get("reserved_forms", []) or []:
        width_bits, mask, value = parse_bit_pattern(str(reserved.get("pattern", "")))
        if width_bits == 6:
            lines.extend(
                [
                    f"      {bin_pattern(6, mask, value)}: begin // {reserved.get('name', '')}",
                    "        r.reserved = 1'b1;",
                    "      end",
                ]
            )
    lines += [
        "      default: begin",
        "        r.reserved = 1'b1;",
        "      end",
        "    endcase",
        "    return r;",
        "  endfunction",
        "",
        "  function automatic bedrock_ea_decode_t bedrock_decode_extended_ea(",
        "    input logic signed32_index_escape,",
        "    input logic [15:0] descriptor",
        "  );",
        "    bedrock_ea_decode_t r;",
        "    logic [4:0] mode;",
        "    logic [2:0] segment;",
        "    logic [7:0] extra;",
        "    r = '0;",
        "    r.signed32_index_escape = signed32_index_escape;",
        "    mode = descriptor[15:11];",
        "    segment = descriptor[10:8];",
        "    extra = descriptor[7:0];",
        "    r.segment = bedrock_ea_segment_decode(segment);",
        "    r.segment_valid = (segment <= 3'd5);",
        "    unique case (mode)",
    ]
    for mode_value, mode_forms in extended_ea_forms_by_mode(spec).items():
        lines.append(f"      5'h{mode_value:02x}: begin")
        for index, form in enumerate(mode_forms):
            name = str(form.get("name", ""))
            condition = "signed32_index_escape" if form.get("escape") == "S32_INDEXED_EXTENDED" else "!signed32_index_escape"
            keyword = "if" if index == 0 else "else if"
            lines.append(f"        {keyword} ({condition}) begin // {name}")
            lines += ea_assignment_lines(form, form_names[name], compact=False, indent="          ")
            if form.get("segment_field") == "reserved_zero":
                lines.append("          r.segment_valid = (segment == 3'd0);")
                fixed = str(form.get("fixed_segment", "DEFAULT"))
                lines.append(f"          r.segment = {segment_enum(fixed)};")
            elif form.get("segment_selectable"):
                lines.append("          r.segment = bedrock_ea_segment_decode(segment);")
                lines.append("          r.segment_valid = (segment <= 3'd5);")
            lines.append("        end")
        lines += [
            "        else begin",
            "          r.reserved = 1'b1;",
            "        end",
            "      end",
        ]
    lines += [
        "      default: begin",
        "        r.reserved = 1'b1;",
        "      end",
        "    endcase",
        "    r.valid = r.valid && r.segment_valid;",
        "    return r;",
        "  endfunction",
        "",
        "  function automatic bedrock_ea_decode_t bedrock_decode_ea(input logic [5:0] ea, input logic [15:0] descriptor);",
        "    bedrock_ea_decode_t compact;",
        "    compact = bedrock_decode_compact_ea(ea);",
        "    if (compact.needs_descriptor) begin",
        "      return bedrock_decode_extended_ea(compact.signed32_index_escape, descriptor);",
        "    end",
        "    return compact;",
        "  endfunction",
        "",
        "endpackage",
        "",
        "`default_nettype wire",
        "",
    ]
    return "\n".join(lines)


def segment_enum(name: str) -> str:
    mapping = {
        "DEFAULT": "BR_EA_SEG_DEFAULT",
        "CS": "BR_EA_SEG_CS",
        "DS": "BR_EA_SEG_DS",
        "SS": "BR_EA_SEG_SS",
        "GS0": "BR_EA_SEG_GS0",
        "GS1": "BR_EA_SEG_GS1",
    }
    return mapping.get(name.upper(), "BR_EA_SEG_DEFAULT")


def base_enum(name: str) -> str:
    mapping = {
        "NONE": "BR_EA_BASE_NONE",
        "D": "BR_EA_BASE_D",
        "A": "BR_EA_BASE_A",
        "SP": "BR_EA_BASE_SP",
        "PC": "BR_EA_BASE_PC",
        "ABS": "BR_EA_BASE_ABS",
        "IMM": "BR_EA_BASE_IMM",
    }
    return mapping.get(name.upper(), "BR_EA_BASE_NONE")


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
    return "\n".join(
        [
            "`timescale 1ns/1ps",
            "`default_nettype none",
            "",
            "module bedrock_ea_decode",
            "  import bedrock_ea_decode_pkg::*;",
            "(",
            "  input  logic [5:0]  ea_i,",
            "  input  logic [15:0] descriptor_i,",
            "  output logic        valid_o,",
            "  output logic        reserved_o,",
            "  output logic        needs_descriptor_o,",
            "  output bedrock_ea_form_e form_o,",
            "  output logic        is_register_o,",
            "  output logic        is_memory_o,",
            "  output logic        is_immediate_o,",
            "  output logic        update_eligible_o,",
            "  output logic        signed32_index_escape_o,",
            "  output logic        segment_selectable_o,",
            "  output logic        segment_valid_o,",
            "  output logic        has_base_reg_o,",
            "  output logic        has_index_reg_o,",
            "  output logic        has_displacement_o,",
            "  output logic        has_absolute_o,",
            "  output bedrock_ea_segment_e segment_o,",
            "  output bedrock_ea_base_e base_o,",
            "  output logic [2:0]  base_reg_o,",
            "  output logic [2:0]  index_reg_o,",
            "  output logic [1:0]  scale_log2_o,",
            "  output logic [2:0]  displacement_words_o,",
            "  output logic [2:0]  payload_words_o",
            ");",
            "  bedrock_ea_decode_t decode;",
            "  always_comb begin",
            "    decode = bedrock_decode_ea(ea_i, descriptor_i);",
            "    valid_o = decode.valid;",
            "    reserved_o = decode.reserved;",
            "    needs_descriptor_o = decode.needs_descriptor;",
            "    form_o = decode.form;",
            "    is_register_o = decode.is_register;",
            "    is_memory_o = decode.is_memory;",
            "    is_immediate_o = decode.is_immediate;",
            "    update_eligible_o = decode.update_eligible;",
            "    signed32_index_escape_o = decode.signed32_index_escape;",
            "    segment_selectable_o = decode.segment_selectable;",
            "    segment_valid_o = decode.segment_valid;",
            "    has_base_reg_o = decode.has_base_reg;",
            "    has_index_reg_o = decode.has_index_reg;",
            "    has_displacement_o = decode.has_displacement;",
            "    has_absolute_o = decode.has_absolute;",
            "    segment_o = decode.segment;",
            "    base_o = decode.base;",
            "    base_reg_o = decode.base_reg;",
            "    index_reg_o = decode.index_reg;",
            "    scale_log2_o = decode.scale_log2;",
            "    displacement_words_o = decode.displacement_words;",
            "    payload_words_o = decode.payload_words;",
            "  end",
            "endmodule",
            "",
            "`default_nettype wire",
            "",
        ]
    )


def emit_prefix_synth() -> str:
    return "\n".join(
        [
            "`timescale 1ns/1ps",
            "`default_nettype none",
            "",
            "module bedrock_prefix_decode_synth(",
            "  input  [15:0] prefix_word_i,",
            "  output reg        valid_o,",
            "  output reg        nospec_o,",
            "  output reg        saturate_o,",
            "  output reg        nontemporal_o,",
            "  output reg [2:0]  update_mode_o,",
            "  output reg [1:0]  repeat_kind_o,",
            "  output reg [3:0]  repeat_condition_o,",
            "  output reg [2:0]  repeat_counter_o,",
            "  output reg        end_group_o",
            ");",
            "  task automatic apply_prefix(input [7:0] p);",
            "    begin",
            "      casez (p)",
            "        8'h00: begin end",
            "        8'h01: nospec_o = 1'b1;",
            "        8'h02: saturate_o = 1'b1;",
            "        8'h0b: nontemporal_o = 1'b1;",
            "        8'h04: update_mode_o = 3'd1;",
            "        8'h05: update_mode_o = 3'd2;",
            "        8'h06: update_mode_o = 3'd3;",
            "        8'h07: update_mode_o = 3'd4;",
            "        8'b0110_0???: begin repeat_kind_o = 2'd2; repeat_counter_o = p[2:0]; end",
            "        8'h68: end_group_o = 1'b1;",
            "        8'b1???_????: begin repeat_kind_o = 2'd1; repeat_condition_o = p[6:3]; repeat_counter_o = p[2:0]; end",
            "        default: valid_o = 1'b0;",
            "      endcase",
            "    end",
            "  endtask",
            "  always @* begin",
            "    valid_o = 1'b1;",
            "    nospec_o = 1'b0;",
            "    saturate_o = 1'b0;",
            "    nontemporal_o = 1'b0;",
            "    update_mode_o = 3'd0;",
            "    repeat_kind_o = 2'd0;",
            "    repeat_condition_o = 4'd0;",
            "    repeat_counter_o = 3'd0;",
            "    end_group_o = 1'b0;",
            "    apply_prefix(prefix_word_i[7:0]);",
            "    apply_prefix(prefix_word_i[15:8]);",
            "  end",
            "endmodule",
            "",
            "`default_nettype wire",
            "",
        ]
    )


def emit_ea_synth(spec: dict[str, Any]) -> str:
    form_names = ea_form_names(spec)
    lines = [
        "`timescale 1ns/1ps",
        "`default_nettype none",
        "",
        "module bedrock_ea_decode_synth(",
        "  input  [5:0]  ea_i,",
        "  input  [15:0] descriptor_i,",
        "  output reg        valid_o,",
        "  output reg        reserved_o,",
        "  output reg        needs_descriptor_o,",
        "  output reg [5:0]  form_o,",
        "  output reg        is_register_o,",
        "  output reg        is_memory_o,",
        "  output reg        is_immediate_o,",
        "  output reg        update_eligible_o,",
        "  output reg        signed32_index_escape_o,",
        "  output reg        segment_selectable_o,",
        "  output reg        segment_valid_o,",
        "  output reg        has_base_reg_o,",
        "  output reg        has_index_reg_o,",
        "  output reg        has_displacement_o,",
        "  output reg        has_absolute_o,",
        "  output reg [2:0]  segment_o,",
        "  output reg [2:0]  base_o,",
        "  output reg [2:0]  base_reg_o,",
        "  output reg [2:0]  index_reg_o,",
        "  output reg [1:0]  scale_log2_o,",
        "  output reg [2:0]  displacement_words_o,",
        "  output reg [2:0]  payload_words_o",
        ");",
    ]
    for index, form in enumerate(compact_ea_forms(spec) + extended_ea_forms(spec), start=1):
        lines.append(f"  localparam [5:0] {form_names[str(form.get('name', ''))]} = 6'd{index}; // {form.get('name', '')}")
    lines += [
        "  wire [4:0] mode = descriptor_i[15:11];",
        "  wire [2:0] seg = descriptor_i[10:8];",
        "  wire [7:0] extra = descriptor_i[7:0];",
        "  reg signed32_escape;",
        "  always @* begin",
        "    valid_o = 1'b0;",
        "    reserved_o = 1'b0;",
        "    needs_descriptor_o = 1'b0;",
        "    form_o = 6'd0;",
        "    is_register_o = 1'b0;",
        "    is_memory_o = 1'b0;",
        "    is_immediate_o = 1'b0;",
        "    update_eligible_o = 1'b0;",
        "    signed32_index_escape_o = 1'b0;",
        "    segment_selectable_o = 1'b0;",
        "    segment_valid_o = 1'b1;",
        "    has_base_reg_o = 1'b0;",
        "    has_index_reg_o = 1'b0;",
        "    has_displacement_o = 1'b0;",
        "    has_absolute_o = 1'b0;",
        "    segment_o = 3'd0;",
        "    base_o = 3'd0;",
        "    base_reg_o = 3'd0;",
        "    index_reg_o = 3'd0;",
        "    scale_log2_o = 2'd0;",
        "    displacement_words_o = 3'd0;",
        "    payload_words_o = 3'd0;",
        "    signed32_escape = 1'b0;",
        "    casez (ea_i)",
    ]
    for form in compact_ea_forms(spec):
        name = str(form.get("name", ""))
        width_bits, mask, value = parse_bit_pattern(str(form.get("pattern", "")))
        if width_bits == 6:
            lines.append(f"      {bin_pattern(6, mask, value)}: begin // {name}")
            lines += ea_synth_assignment_lines(form, form_names[name], compact=True, indent="        ")
            lines.append("      end")
    for reserved in spec.get("ea", {}).get("reserved_forms", []) or []:
        width_bits, mask, value = parse_bit_pattern(str(reserved.get("pattern", "")))
        if width_bits == 6:
            lines += [f"      {bin_pattern(6, mask, value)}: begin reserved_o = 1'b1; end"]
    lines += [
        "      default: begin reserved_o = 1'b1; end",
        "    endcase",
        "    if (needs_descriptor_o) begin",
        "      valid_o = 1'b0;",
        "      reserved_o = 1'b0;",
        "      form_o = 6'd0;",
        "      is_register_o = 1'b0;",
        "      is_memory_o = 1'b0;",
        "      is_immediate_o = 1'b0;",
        "      update_eligible_o = 1'b0;",
        "      signed32_index_escape_o = signed32_escape;",
        "      segment_selectable_o = 1'b0;",
        "      segment_valid_o = 1'b1;",
        "      has_base_reg_o = 1'b0;",
        "      has_index_reg_o = 1'b0;",
        "      has_displacement_o = 1'b0;",
        "      has_absolute_o = 1'b0;",
        "      segment_o = seg;",
        "      base_o = 3'd0;",
        "      base_reg_o = 3'd0;",
        "      index_reg_o = 3'd0;",
        "      scale_log2_o = 2'd0;",
        "      displacement_words_o = 3'd0;",
        "      payload_words_o = 3'd0;",
        "      case (mode)",
    ]
    for mode_value, mode_forms in extended_ea_forms_by_mode(spec).items():
        lines.append(f"        5'h{mode_value:02x}: begin")
        for index, form in enumerate(mode_forms):
            name = str(form.get("name", ""))
            expected_s32 = bool(form.get("escape") == "S32_INDEXED_EXTENDED")
            keyword = "if" if index == 0 else "else if"
            lines.append(f"          {keyword} (signed32_escape == 1'b{1 if expected_s32 else 0}) begin // {name}")
            lines += ea_synth_assignment_lines(form, form_names[name], compact=False, indent="            ")
            if form.get("segment_field") == "reserved_zero":
                lines.append("            valid_o = valid_o && (seg == 3'd0);")
                lines.append("            segment_valid_o = (seg == 3'd0);")
                lines.append(f"            segment_o = {segment_synth_value(str(form.get('fixed_segment', 'DEFAULT')))};")
            else:
                if form.get("segment_selectable"):
                    lines.append("            segment_o = seg;")
                lines.append("            valid_o = valid_o && (seg <= 3'd5);")
                lines.append("            segment_valid_o = (seg <= 3'd5);")
            lines.append("          end")
        lines += ["          else begin reserved_o = 1'b1; end", "        end"]
    lines += [
        "        default: begin reserved_o = 1'b1; end",
        "      endcase",
        "    end",
        "  end",
        "endmodule",
        "",
        "`default_nettype wire",
        "",
    ]
    return "\n".join(lines)


def segment_synth_value(name: str) -> str:
    return {
        "DEFAULT": "3'd0",
        "CS": "3'd1",
        "DS": "3'd2",
        "SS": "3'd3",
        "GS0": "3'd4",
        "GS1": "3'd5",
    }.get(name.upper(), "3'd0")


def base_synth_value(name: str) -> str:
    return {
        "NONE": "3'd0",
        "D": "3'd1",
        "A": "3'd2",
        "SP": "3'd3",
        "PC": "3'd4",
        "ABS": "3'd5",
        "IMM": "3'd6",
    }.get(name.upper(), "3'd0")


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
    write(args.prefix_synth_module, emit_prefix_synth())
    write(args.ea_package, emit_ea_package(spec))
    write(args.ea_module, emit_ea_module())
    write(args.ea_synth_module, emit_ea_synth(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
