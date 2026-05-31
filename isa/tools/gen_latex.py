#!/usr/bin/env python3
"""Generate a LaTeX ISA reference manual from the declarative ISA spec."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import re
import sys

sys.dont_write_bytecode = True

from gen_instruction_specs import (
    aliases_by_mnemonic,
    allocation_items,
    operation_records,
    semantic_records,
)
from gen_instruction_tables import (
    default_words,
    encoding_pattern_tokens,
    encoding_text,
    field_layout_text,
    field_symbol,
    line_fields,
    line_syntax_text,
    operand_types_text,
    syntax_text,
)
from isa_spec import load_and_validate, print_result
from latex_builder.diagrams import (
    abbreviated_bit_field_figure,
    bit_diagram,
    bit_field_figure,
    bit_index_labels,
    paging_mode_figure,
)


from latex_builder.common import (
    ARCH_NAME,
    FFLAG_MEANINGS,
    FFLAG_ORDER,
    FLAG_ORDER,
    MANUAL_TITLE,
    SIZE_NAMES,
    compact_text,
    document_end,
    document_preamble,
    instruction_docs,
    latex_longtable,
    load_allocation,
    listed_figure_caption,
    mdash_join,
    normalize_text,
    pretty_key,
    readable_text,
    render_latex_template,
    tex_code,
    tex_escape,
    tex_multiline,
    tex_table_value,
    title_page,
    top_section,
)
from latex_builder.effective_address import ea_table
from latex_builder.arch_diagrams import (
    ascr_register_figure,
    flags_register_figure,
    frame_info_figure,
    icr_register_figure,
    ivt_control_byte_figure,
    ivt_entry_figure,
    la48_paging_figure,
    la57_paging_figure,
    prefix_word_figure,
    primary_word_figure,
    ptcr_register_figure,
    pte_attribute_figure,
    register_model_figure,
    segment_register_figure,
    stack_frame_figure,
    supervisor_stack_frame,
    status_register_figure,
    translation_pipeline_figure,
    word0_overview_figure,
)
from latex_builder.instruction_reference import (
    c_library_instruction_examples_section,
    condition_code_computation_section,
    form_label,
    fpu_mnemonics,
    instruction_description_intro_section,
    instruction_reference_sections,
    instruction_set_summary_by_class_section,
    instruction_summary,
    opcode_instruction_format_summary_section,
    render_instruction,
)



def data_format_section() -> str:
    return render_latex_template("data_formats.tex")


def memory_model_section() -> str:
    return render_latex_template("memory_model.tex")


def segment_paging_interaction_section() -> str:
    return render_latex_template("segment_paging_interaction.tex")


def streaming_execution_model_section() -> str:
    return render_latex_template("streaming_execution_model.tex")


def prefix_model_paragraph(spec: dict[str, Any]) -> str:
    prefix_word = (spec.get("prefixes") or {}).get("prefix_word") or {}
    unused = str(prefix_word.get("unused_slot_encoding", "NPX"))
    conflict = readable_text(prefix_word.get("conflict_resolution", "last_prefix_wins"))
    note = compact_text(prefix_word.get("conflict_note", ""))
    details = (
        f"If P is set, word 1 is a prefix word containing two independent 8-bit prefix slots. "
        f"The low byte, bits 7..0, is {tex_code('prefix0')} and is filled and decoded first. "
        f"The high byte, bits 15..8, is {tex_code('prefix1')} and is filled and decoded second. "
        f"An unused slot is encoded as {tex_code(unused)}. Prefixes do not determine instruction length."
    )
    if note:
        details += " " + tex_escape(note)
    elif conflict:
        details += f" Prefix effects are applied in this byte order; conflicting effects use {tex_escape(conflict)}."
    return details


def length_encoding_table() -> str:
    rows = []
    for value in range(8):
        words = value + 1
        rows.append([tex_code(f"{value:03b}"), tex_escape(words), tex_escape(words * 2)])
    return latex_longtable(
        ["L Field", "Total Words", "Total Bytes"],
        rows,
        ["1.2in", "1.35in", "1.35in"],
        "Table 1-1. Instruction Length Encoding",
    )


def architecture_overview_section(spec: dict[str, Any], plan: dict[str, Any], mnemonic_count: int, form_count: int) -> str:
    return "\n".join(
        [
            top_section("Overview"),
            f"{ARCH_NAME} defines a bounded, 16-bit-word-oriented CISC instruction set architecture. "
            "It includes selected register-memory forms, compact register-register forms, explicit instruction lengths, "
            "and a fixed maximum instruction size.",
            f"The base architecture combines simplified effective addressing with page-granular segmented "
            "address pre-translation, optional page-table translation, and ordinary memory-mapped device access.",
            r"\subsection{Design Goals}",
            f"{ARCH_NAME} is intended for high-performance general-purpose systems rather than as a minimal "
            "embedded instruction set. The architecture keeps the visible programming model scalar and bounded, "
            "while giving implementations explicit repeated-operation structures that may be executed by "
            "microarchitectural streaming or internal SIMD machinery.",
            r"\begin{itemize}",
            r"\item preserve selected CISC code-density advantages without unbounded instruction forms",
            r"\item make instruction boundaries and maximum instruction size explicit",
            r"\item support register-memory operations and compact hot-path register-register operations",
            r"\item expose scalar architectural state while allowing wider internal execution resources",
            r"\item accelerate fast, regular loops through REP, REPcc, REPG, and update-eligible effective addresses",
            r"\item let common loop kernels scale with implementation width without adding programmer-visible vector state or width-specific opcode families",
            r"\item avoid making vector width or internal streaming resources part of the architectural ABI",
            r"\item leave specialized cryptographic, image, matrix, tensor, and accelerator workloads to extensions or devices",
            r"\end{itemize}",
            r"\subsection{Architectural Profile}",
            r"\begin{itemize}",
            r"\item 16-bit instruction words",
            r"\item explicit instruction length encoded in word 0",
            r"\item maximum instruction length of eight words",
            r"\item at most one prefix word containing two prefix bytes",
            r"\item register-register and register-memory instruction forms",
            r"\item bounded compact and extended effective-address forms",
            r"\item page-granular segment pre-translation before optional paging",
            r"\item memory-mapped device access through the normal memory map",
            r"\item no separate I/O port address space",
            r"\item no direct physical-memory load/store instructions",
            r"\end{itemize}",
            r"\subsection{Instruction Stream}",
            "The instruction stream is composed of 16-bit words. Instructions are aligned to 16-bit boundaries. "
            "The program counter addresses bytes, but instruction length is defined in units of 16-bit words.",
            r"\[",
            r"\mathit{next\_pc} = \mathit{pc} + 2 \times \mathit{instruction\_length\_in\_words}",
            r"\]",
            "The maximum instruction length is eight words, or 16 bytes. No instruction may exceed this bound.",
            r"\subsection{Word 0 Format}",
            "Every instruction begins with word 0. The instruction boundary is determined from word 0 alone.",
            word0_overview_figure(),
            r"\manualfield{P:}{Prefix-present bit. If set, word 1 is interpreted as the prefix word.}",
            r"\manualfield{L:}{Total instruction length encoded as length minus one.}",
            length_encoding_table(),
            r"\[",
            r"\mathit{length} = \mathit{word0.L} + 1 \qquad "
            r"\mathit{next\_pc} = \mathit{pc} + 2 \times \mathit{length}",
            r"\]",
            r"\subsection{Prefix Model}",
            prefix_model_paragraph(spec),
            prefix_word_figure(),
        ]
    )


def terminology_description_list(terms: list[dict[str, Any]]) -> str:
    if not terms:
        return ""
    lines = [
        r"\begin{description}[style=nextline,leftmargin=1.42in,labelwidth=1.32in,itemsep=3pt,topsep=3pt]"
    ]
    for item in terms:
        term = item.get("term", "")
        definition = item.get("definition", "")
        if term and definition:
            lines.append(rf"\item[{tex_escape(term)}] {tex_escape(compact_text(definition))}")
    lines.append(r"\end{description}")
    return "\n".join(lines)


def terminology_section(spec: dict[str, Any]) -> str:
    terminology = spec.get("terminology") or {}
    groups = terminology.get("groups") or []
    parts = [tex_escape(compact_text(terminology.get("summary", "")))]
    for group in groups:
        if not isinstance(group, dict):
            continue
        name = group.get("name")
        terms = group.get("terms") or []
        if name:
            parts.append(rf"\subsection{{{tex_escape(name)}}}")
            parts.append(terminology_description_list([term for term in terms if isinstance(term, dict)]))
    return "\n".join(part for part in parts if part)


def hex_text(value: Any, *, width: int = 8) -> str:
    if isinstance(value, int):
        return f"0x{value:0{width}x}"
    text = str(value)
    try:
        return f"0x{int(text, 0):0{width}x}"
    except ValueError:
        return text


def cpuid_model(spec: dict[str, Any]) -> dict[str, Any]:
    raw = spec.get("cpuid") or {}
    model = raw.get("cpuid") if isinstance(raw, dict) else {}
    return model if isinstance(model, dict) else {}


def cpuid_range_text(value: Any) -> str:
    if isinstance(value, list) and len(value) == 2:
        return f"{hex_text(value[0])}..{hex_text(value[1])}"
    return str(value)


def cpuid_policy_rows(spec: dict[str, Any]) -> list[list[str]]:
    policy = cpuid_model(spec).get("policy") or {}
    rows: list[list[str]] = []
    for key in ("base_profile", "optional_extensions", "implementation_properties"):
        item = policy.get(key) if isinstance(policy, dict) else {}
        if not isinstance(item, dict):
            continue
        range_value = item.get("range")
        rows.append(
            [
                tex_escape(item.get("name", readable_text(key))),
                tex_code(cpuid_range_text(range_value)) if range_value is not None else tex_escape("-"),
                tex_escape(compact_text(item.get("description", ""))),
            ]
        )
    return rows


def cpuid_leaf_range_rows(spec: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for item in cpuid_model(spec).get("leaf_ranges", []) or []:
        if not isinstance(item, dict):
            continue
        rows.append(
            [
                tex_code(cpuid_range_text(item.get("range", "-"))),
                tex_escape(readable_text(item.get("name", ""))),
                tex_escape(compact_text(item.get("description", ""))),
            ]
        )
    return rows


def cpuid_leaf_rows(spec: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for leaf in cpuid_model(spec).get("leaves", []) or []:
        if not isinstance(leaf, dict):
            continue
        leaf_value = tex_code(hex_text(leaf.get("leaf", "-")))
        name = tex_code(str(leaf.get("name", "")))
        outputs = leaf.get("outputs") or {}
        if not isinstance(outputs, dict):
            continue
        for reg in ("D0", "D1", "D2", "D3"):
            value = outputs.get(reg, "reserved, zero")
            if isinstance(value, dict):
                description = "bit fields listed in the next table"
            else:
                description = readable_text(value)
            rows.append([leaf_value, name, tex_code(reg), tex_escape(description)])
    return rows


def cpuid_bit_field_rows(spec: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for leaf in cpuid_model(spec).get("leaves", []) or []:
        if not isinstance(leaf, dict):
            continue
        outputs = leaf.get("outputs") or {}
        if not isinstance(outputs, dict):
            continue
        for reg, value in outputs.items():
            if not isinstance(value, dict):
                continue
            for bit in value.get("bits", []) or []:
                if not isinstance(bit, dict):
                    continue
                if "bit" in bit:
                    bit_text = str(bit.get("bit"))
                else:
                    bit_range = bit.get("range")
                    bit_text = f"{bit_range[0]}..{bit_range[1]}" if isinstance(bit_range, list) and len(bit_range) == 2 else "-"
                rows.append(
                    [
                        tex_code(hex_text(leaf.get("leaf", "-"))),
                        tex_code(str(reg)),
                        tex_code(bit_text),
                        tex_code(str(bit.get("name", ""))),
                        tex_escape(compact_text(bit.get("description", ""))),
                    ]
                )
    return rows


def cpuid_feature_discovery_section(spec: dict[str, Any]) -> str:
    model = cpuid_model(spec)
    calling = model.get("calling_convention") or {}
    inputs = calling.get("inputs", {}) if isinstance(calling, dict) else {}
    unsupported_leaf = calling.get("unsupported_leaf", "D0..D3 = 0") if isinstance(calling, dict) else "D0..D3 = 0"
    unsupported_subleaf = calling.get("unsupported_subleaf", "D0..D3 = 0") if isinstance(calling, dict) else "D0..D3 = 0"
    parts = [
        "CPUID is the architectural discovery instruction. It is intended to expose base-profile identity, "
        "optional architectural extensions, and program-visible tuning properties. It is not a dump of internal "
        "microarchitectural structures.",
        f"The input register {tex_code('D0')} contains the {tex_escape(inputs.get('D0', 'leaf'))}; "
        f"{tex_code('D1')} contains the {tex_escape(inputs.get('D1', 'subleaf'))}. "
        f"Results are returned in {tex_code('D0')} through {tex_code('D3')}. "
        f"Unsupported leaves and unsupported subleaves return {tex_code(unsupported_leaf)} and "
        f"{tex_code(unsupported_subleaf)}, respectively.",
        "All non-FPU instructions defined by this manual are part of the base Bedrock ISA profile. "
        "REP, REPcc, REPG, atomics, fences, cache and TLB management instructions, segmentation, paging, "
        "and control-register access are therefore not advertised as independently optional instruction fragments.",
        "Floating-point discovery is intentionally coarse. An implementation reports whether the base floating-point "
        "extension is available, and separately whether the transcendental floating-point group is available. "
        "Double precision, fused multiply-add/subtract, floating-point conditional move, conversion, classification, "
        "and ordinary floating-point memory/register forms are base features of the floating-point extension.",
        "Implementation-property leaves expose only information a program can reasonably use to select code paths or "
        "tune algorithms. Structures such as register renaming, reorder buffers, issue queues, and physical register "
        f"files are not architectural discovery bits. The initial execution-property leaf exposes only {tex_code('OUT_OF_ORDER')}.",
    ]
    policy_rows = cpuid_policy_rows(spec)
    if policy_rows:
        parts.append(latex_longtable(["Policy", "Range", "Meaning"], policy_rows, ["1.25in", "1.45in", "2.80in"], "CPUID Discovery Policy"))
    range_rows = cpuid_leaf_range_rows(spec)
    if range_rows:
        parts.append(latex_longtable(["Leaf Range", "Name", "Meaning"], range_rows, ["1.45in", "1.35in", "2.70in"], "CPUID Leaf Ranges"))
    leaf_rows = cpuid_leaf_rows(spec)
    if leaf_rows:
        parts.append(latex_longtable(["Leaf", "Name", "Reg", "Output"], leaf_rows, ["0.95in", "1.65in", "0.45in", "2.45in"], "CPUID Leaves"))
    bit_rows = cpuid_bit_field_rows(spec)
    if bit_rows:
        parts.append(latex_longtable(["Leaf", "Reg", "Bits", "Name", "Meaning"], bit_rows, ["0.95in", "0.45in", "0.55in", "1.85in", "1.70in"], "CPUID Bit Fields"))
    return "\n".join(parts)


def overview_sections(spec: dict[str, Any], plan: dict[str, Any], mnemonic_count: int, form_count: int) -> str:
    lines = [
        architecture_overview_section(spec, plan, mnemonic_count, form_count),
        top_section("Terminology"),
        terminology_section(spec),
        top_section("Programming Model"),
        register_tables(spec),
        top_section("CPUID Feature Discovery"),
        cpuid_feature_discovery_section(spec),
        top_section("Data Formats"),
        data_format_section(),
        top_section("Condition Codes"),
        condition_table(spec),
        top_section("Prefixes"),
        prefix_table(spec),
        top_section("Effective Addressing Modes"),
        ea_table(spec),
        top_section("Memory Address Translation"),
        memory_address_translation_section(spec),
        top_section("Memory Model"),
        memory_model_section(),
        top_section("Supervisor / Privileged Programming Model"),
        privileged_programming_model_section(spec),
        top_section("Exception Processing Reference"),
        interrupt_model_section(spec),
        top_section("Instruction Word Formats"),
        encoding_overview_section(plan),
        top_section("Instruction Execution Model"),
        execution_model_section(spec),
        top_section("Streaming Execution Model"),
        streaming_execution_model_section(),
    ]
    return "\n".join(lines)


def register_tables(spec: dict[str, Any]) -> str:
    registers = spec.get("registers", {})
    rows = []
    for name, body in (registers.get("register_classes") or {}).items():
        rows.append(
            [
                tex_code(name),
                tex_table_value(body.get("count", "-")),
                tex_table_value(body.get("width", "-")),
                tex_table_value(body.get("role", "-")),
                tex_table_value(body.get("allocatable", "-")),
            ]
        )
    parts = [
        r"\subsection{Register Model}",
        "The programming model exposes separate data, address, stack-pointer, program-counter, and floating-point register classes. "
        "SP is an independent stack register, not an alias of the A-register class.",
        register_model_figure(spec),
        latex_longtable(["Class", "Count", "Width", "Role", "Allocatable"], rows, ["0.7in", "0.65in", "0.65in", "1.45in", "1.2in"], "Table 2-1. Register Classes"),
        state_register_format_section(spec),
        floating_point_register_section(spec),
        segment_register_section(spec),
    ]

    srows = []
    for name, body in (registers.get("special_register_classes") or {}).items():
        srows.append(
            [
                tex_code(name),
                tex_table_value(body.get("width", "-")),
                tex_table_value(body.get("encoding_bits", "-")),
                tex_table_value(body.get("role", "-")),
                tex_table_value(body.get("registers", [])),
            ]
        )
    if srows:
        parts.extend(
            [
                r"\subsection{Special Register Classes}",
                "The S class is the Q-sized state/segment-register operand class used by MOV, AND, and OR state-register forms. "
                "It includes the SS segment register; SS is distinct from the SP stack-pointer register.",
                latex_longtable(["Class", "Width", "Bits", "Role", "Registers"], srows, ["0.55in", "0.55in", "0.45in", "1.05in", "2.8in"], "Table 2-2. Special Register Classes"),
                latex_longtable(["Bits", "Register", "Reserved Access"], sreg_selector_rows(spec), ["0.55in", "1.0in", "3.90in"], "S Register Selector Encoding"),
            ]
        )

    special = []
    for reg in registers.get("special_registers", []) or []:
        if not isinstance(reg, dict):
            continue
        if is_control_register(reg):
            continue
        special.append(
            [
                tex_code(reg.get("name", "")),
                tex_table_value(reg.get("width", "-")),
                tex_table_value(reg.get("class", "-")),
                tex_table_value(reg.get("role", "-")),
                tex_table_value(reg.get("privilege", "any")),
                tex_table_value(reg.get("implicit", False)),
            ]
        )
    parts.extend(
        [
            r"\subsection{Special Registers}",
            latex_longtable(["Name", "Width", "Class", "Role", "Privilege", "Implicit"], special, ["0.7in", "0.5in", "0.5in", "0.8in", "0.9in", "0.65in"], "Table 2-3. Special Registers"),
            translation_control_section(spec),
        ]
    )
    return "\n".join(parts)


def is_control_register(reg: dict[str, Any]) -> bool:
    return str(reg.get("role", "")).lower() == "control" or str(reg.get("class", "")).upper() in {"C", "CR"}


def control_register_rows(spec: dict[str, Any]) -> list[list[str]]:
    registers = spec.get("registers", {})
    class_order: list[str] = []
    for body in (registers.get("control_register_classes") or {}).values():
        if isinstance(body, dict):
            class_order.extend(str(item) for item in body.get("registers", []) or [])
    by_name = {
        str(reg.get("name", "")): reg
        for reg in registers.get("special_registers", []) or []
        if isinstance(reg, dict) and is_control_register(reg)
    }
    names = class_order + sorted(name for name in by_name if name not in class_order)
    rows: list[list[str]] = []
    for name in names:
        reg = by_name.get(name)
        if not reg:
            continue
        rows.append(
            [
                tex_code(name),
                tex_escape(reg.get("width", "-")),
                tex_escape(reg.get("class", "-")),
                tex_escape(reg.get("privilege", "any")),
                tex_escape(compact_text(reg.get("description", reg.get("role", "-")))),
            ]
        )
    return rows


def numeric_selector_text(value: Any, *, width: int = 4) -> str:
    if isinstance(value, int):
        return f"0x{value:0{width}x}"
    text = str(value)
    try:
        return f"0x{int(text, 0):0{width}x}"
    except ValueError:
        return text


def selector_range_text(value: Any, *, width: int = 4) -> str:
    if isinstance(value, list) and len(value) == 2:
        return f"{numeric_selector_text(value[0], width=width)}..{numeric_selector_text(value[1], width=width)}"
    return numeric_selector_text(value, width=width)


def sreg_selector_rows(spec: dict[str, Any]) -> list[list[str]]:
    sclass = ((spec.get("registers", {}).get("special_register_classes") or {}).get("S") or {})
    encoding = sclass.get("encoding") if isinstance(sclass, dict) else None
    if not isinstance(encoding, list) or not encoding:
        encoding = [
            {"value": 0, "bits": "000", "register": "CS"},
            {"value": 1, "bits": "001", "register": "DS"},
            {"value": 2, "bits": "010", "register": "SS"},
            {"value": 3, "bits": "011", "register": "GS0"},
            {"value": 4, "bits": "100", "register": "GS1"},
            {"value": 5, "bits": "101", "register": "FLAGS"},
            {"value": 6, "bits": "110", "register": "STATUS"},
            {"value": 7, "bits": "111", "register": "reserved", "access_fault": "INVALID_OPCODE"},
        ]
    rows: list[list[str]] = []
    for item in encoding:
        if not isinstance(item, dict):
            continue
        bits = item.get("bits")
        if bits is None and isinstance(item.get("value"), int):
            bits = f"{int(item['value']):03b}"
        fault = item.get("access_fault")
        if not fault and str(item.get("register", "")).lower() == "reserved":
            fault = "INVALID_OPCODE"
        rows.append(
            [
                tex_code(str(bits if bits is not None else "-")),
                tex_code(str(item.get("register", "-"))),
                tex_code(str(fault)) if fault else tex_escape("-"),
            ]
        )
    return rows


def control_register_selector_rows(spec: dict[str, Any]) -> list[list[str]]:
    cr_class = ((spec.get("registers", {}).get("control_register_classes") or {}).get("CR") or {})
    groups = cr_class.get("selector_groups") if isinstance(cr_class, dict) else None
    if not isinstance(groups, list) or not groups:
        groups = [
            {"name": "translation", "range": [0x0000, 0x00FF], "selectors": [{"value": 0x0000, "register": "PTCR"}, {"value": 0x0001, "register": "ASCR"}, {"value": 0x0002, "register": "ICR"}]},
            {"name": "supervisor_entry", "range": [0x0100, 0x01FF], "selectors": [{"value": 0x0100, "register": "SPC"}, {"value": 0x0101, "register": "SCS"}, {"value": 0x0102, "register": "SDS"}]},
            {"name": "interrupt stack banks", "range": [0x0200, 0x02FF], "selectors": []},
            {"name": "boot", "range": [0x1000, 0x10FF], "selectors": [{"value": 0x1000, "register": "BOOTPC"}, {"value": 0x1001, "register": "BOOTCFG"}]},
            {"name": "counters", "range": [0x1100, 0x11FF], "selectors": [{"value": 0x1100, "register": "PTC"}, {"value": 0x1101, "register": "PMC"}]},
        ]
    rows: list[list[str]] = []
    reserved_fault = cr_class.get("reserved_selector_fault", "INVALID_CONTROL_STATE") if isinstance(cr_class, dict) else "INVALID_CONTROL_STATE"
    for group in groups:
        if not isinstance(group, dict):
            continue
        group_name = readable_text(group.get("name", ""))
        group_range = selector_range_text(group.get("range", "-"), width=4)
        selectors = group.get("selectors") or []
        for selector in selectors:
            if not isinstance(selector, dict):
                continue
            rows.append(
                [
                    tex_escape(group_name),
                    tex_code(group_range),
                    tex_code(numeric_selector_text(selector.get("value", "-"), width=4)),
                    tex_code(str(selector.get("register", "-"))),
                ]
            )
    rows.append(
        [
            tex_escape("unassigned"),
            tex_code("all other selectors"),
            tex_escape("-"),
            tex_code(str(reserved_fault)),
        ]
    )
    return rows


def special_register_by_name(spec: dict[str, Any], name: str) -> dict[str, Any]:
    for reg in spec.get("registers", {}).get("special_registers", []) or []:
        if isinstance(reg, dict) and reg.get("name") == name:
            return reg
    return {}


def state_register_format_section(spec: dict[str, Any]) -> str:
    flags = special_register_by_name(spec, "FLAGS")
    status = special_register_by_name(spec, "STATUS")
    flag_meanings = {
        "Z": "zero",
        "N": "negative",
        "C": "carry or borrow",
        "V": "overflow",
    }
    flags_rows = []
    for name, body in (flags.get("layout") or {}).items():
        if isinstance(body, dict):
            bit = body.get("bit", "-")
            meaning = body.get("description", flag_meanings.get(str(name), "condition-code bit"))
        else:
            bit = body
            meaning = flag_meanings.get(str(name), "condition-code bit")
        flags_rows.append([tex_code(name), tex_escape(bit), tex_escape(meaning)])
    status_rows = []
    for name, body in (status.get("layout") or {}).items():
        if isinstance(body, dict):
            status_rows.append([tex_code(name), tex_escape(body.get("bit", "-")), tex_escape(body.get("description", "-"))])
        else:
            status_rows.append([tex_code(name), tex_escape(body), tex_escape("-")])
    access_text = (
        "FLAGS and STATUS are accessed through 64-bit Q-sized state-register operations, "
        "but the architectural registers are 16 bits wide. Reserved bits read as zero and must remain zero; "
        "FLAGS has four meaningful bits and STATUS has seven meaningful bits."
    )
    return "\n".join(
        [
            r"\subsection{FLAGS and STATUS Registers}",
            access_text,
            flags_register_figure(),
            latex_longtable(["Bit", "Position", "Meaning"], flags_rows, ["0.55in", "0.65in", "4.05in"], "Table 2-4. FLAGS Bits"),
            status_register_figure(),
            latex_longtable(["Bit", "Position", "Meaning"], status_rows, ["0.55in", "0.65in", "4.05in"], "Table 2-5. STATUS Bits"),
        ]
    )


def floating_point_register_section(spec: dict[str, Any]) -> str:
    fpu = spec.get("registers", {}).get("floating_point_register_model") or {}
    if not isinstance(fpu, dict) or not fpu:
        return ""
    regs = fpu.get("registers") or {}
    fflags = fpu.get("fflags") or {}
    if not isinstance(regs, dict):
        regs = {}
    if not isinstance(fflags, dict):
        fflags = {}
    register_rows = [
        [tex_escape("Registers"), tex_code(str(regs.get("names", "F0-F31")))],
        [tex_escape("Count"), tex_escape(regs.get("count", 32))],
        [tex_escape("Architectural width"), tex_escape(f"{regs.get('width', 64)} bits")],
        [tex_escape("Scalar formats"), tex_table_value(regs.get("scalar_formats", ["S", "D"]))],
        [tex_escape("Unavailable extension"), tex_code(str(fpu.get("unavailable_exception", "EXTENSION_UNAVAILABLE")))],
    ]
    flag_rows = []
    for name, body in (fflags.get("bits") or {}).items():
        if not isinstance(body, dict):
            continue
        flag_rows.append([tex_code(name), tex_escape(body.get("bit", "-")), tex_escape(body.get("description", "-"))])
    return "\n".join(
        [
            r"\subsection{Floating-Point Register Model}",
            "The floating-point extension defines 32 Q-sized floating-point registers, F0 through F31. "
            "Single-precision and double-precision operations use the same register file; floating-point exception status is recorded in FFLAGS.",
            latex_longtable(["Property", "Value"], register_rows, ["1.55in", "3.95in"], "Floating-Point Register File"),
            latex_longtable(["Bit", "Position", "Meaning"], flag_rows, ["0.55in", "0.65in", "4.05in"], "FFLAGS Bits"),
        ]
    )


def segment_register_section(spec: dict[str, Any]) -> str:
    segments = spec.get("segments") or {}
    rows = []
    for reg in segments.get("segment_registers", []) or []:
        if not isinstance(reg, dict):
            continue
        rows.append(
            [
                tex_code(reg.get("name", "")),
                tex_escape(reg.get("selector", "-")),
                tex_escape(reg.get("width", "-")),
            ]
        )
    field_rows = [
        [tex_code("base_page"), tex_escape("63:12"), tex_escape("page-unit segment base index")],
        [tex_code("e"), tex_escape("11:7"), tex_escape("segment size exponent")],
        [tex_code("m"), tex_escape("6:1"), tex_escape("segment size mantissa")],
        [tex_code("b"), tex_escape("0"), tex_escape("bounds-only mode; check bounds without adding the base address")],
    ]
    return "\n".join(
        [
            r"\Needspace{3.8in}",
            r"\subsection{Segment Registers}",
            "Segment registers define a currently addressable memory window plus a simple address translation step. "
            "They are not the memory-protection mechanism; paging supplies memory access permissions and final address translation. "
            "When the segment mantissa field is zero, the segment entry is disabled. When the mantissa is nonzero, "
            "an address passes through segmentation first and then through paging.",
            "The bounds-only bit enables a check-only mode for segment translation: the segment bounds are tested, "
            "but the segment base address is not added to the translated address.",
            latex_longtable(["Register", "Selector", "Width"], rows, ["0.75in", "1.1in", "0.65in"], "Table 2-6. Segment Registers"),
            segment_register_figure(),
            latex_longtable(["Field", "Bits", "Meaning"], field_rows, ["0.85in", "0.65in", "3.75in"], "Table 2-7. Segment Register Fields"),
            r"\begin{align*}",
            r"\text{base byte address} &= \mathit{base\_page} \times 4096\\",
            r"\text{segment size} &= m \times 2^e \times 4096\\",
            r"\text{limit byte address} &= (\mathit{base\_page} + m \times 2^e) \times 4096\\",
            r"b=0:\quad \text{segmented address} &= \text{base byte address} + \text{offset},\quad 0 \le \text{offset} < \text{segment size}\\",
            r"b=1:\quad \text{segmented address} &= \text{offset},\quad \text{base byte address} \le \text{offset} < \text{limit byte address}",
            r"\end{align*}",
            r"The base, segment size, and limit are computed in an unsigned domain wide enough to represent the full 64-bit linear-address space plus one. "
            r"If the limit exceeds \(2^{64}\), the segment register image is invalid and any access through it reports \texttt{PAGE\_FAULT}.",
            "If m is zero, segmentation is disabled for that segment selector and the effective address is already the linear address. "
            "If m is nonzero, the segment bounds are checked before paging. In normal mode (b = 0), the segment base is added to "
            "the offset after the bounds check. In bounds-only mode (b = 1), the base is not added; the segment only constrains "
            "which linear-address window may be accessed.",
        ]
    )


def translation_control_section(spec: dict[str, Any]) -> str:
    registers = spec.get("registers", {})
    control = registers.get("translation_control") or {}
    if not isinstance(control, dict):
        control = {}
    return "\n".join(
        [
            r"\subsection{Control Registers}",
            "Control registers are Q-sized privileged registers used for translation, interrupt, boot, counter, "
            "and privileged-entry state. PTCR and ASCR configure the memory-address translation pipeline described "
            "in the Memory Address Translation section; ICR configures interrupt-vector state; SPC, SCS, and SDS "
            "hold supervisor-entry control state.",
            latex_longtable(["Name", "Width", "Class", "Privilege", "Role"], control_register_rows(spec), ["0.75in", "0.55in", "0.55in", "1.0in", "2.45in"], "Table 2-8. Control Registers"),
            "RDCR and WRCR use 16-bit control-register selectors. Selectors are grouped by function, leaving space inside each group for related control state.",
            latex_longtable(["Group", "Group Range", "Selector", "Register / Fault"], control_register_selector_rows(spec), ["1.35in", "1.05in", "0.85in", "2.25in"], "Control Register Selector Encoding"),
            ptcr_register_figure(),
            latex_longtable(["Field", "Bits", "Meaning"], ptcr_field_rows(), ["0.95in", "0.65in", "3.85in"], "Table 2-9. PTCR Fields"),
            latex_longtable(["Selector", "PABITS", "Reserved Access"], pabits_selector_rows(spec), ["0.80in", "0.85in", "3.85in"], "PTCR PABITS Selector Encoding"),
            ascr_register_figure(),
            "ASCR holds the current address-space identifier. SWPT Dn performs an ASID-non-aware page-table swap: "
            "PTCR is updated and ASCR is cleared. SWPTA Dn, imm16 performs an ASID-aware page-table swap: "
            "PTCR is updated, ASCR.ASID is set from the immediate ASID selector, and ASCR.AE is set.",
            latex_longtable(["Field", "Bits", "Meaning"], ascr_field_rows(), ["0.95in", "0.65in", "3.85in"], "Table 2-10. ASCR Fields"),
            icr_register_figure(),
            latex_longtable(["Field", "Bits", "Meaning"], icr_field_rows(), ["0.95in", "0.65in", "3.85in"], "Table 2-11. ICR Fields"),
            "The detailed interrupt-vector and supervisor-entry frame layouts are described in the Exception Processing Reference section.",
        ]
    )


def privileged_programming_model(spec: dict[str, Any]) -> dict[str, Any]:
    registers = spec.get("registers", {})
    control = registers.get("translation_control") or {}
    if not isinstance(control, dict):
        return {}
    model = control.get("privileged_programming_model") or {}
    return model if isinstance(model, dict) else {}


def exception_processing_model(spec: dict[str, Any]) -> dict[str, Any]:
    registers = spec.get("registers", {})
    control = registers.get("translation_control") or {}
    if not isinstance(control, dict):
        return {}
    model = control.get("exception_processing") or {}
    return model if isinstance(model, dict) else {}


def privilege_state_rows(model: dict[str, Any]) -> list[list[str]]:
    state = model.get("privilege_state") if isinstance(model, dict) else {}
    rows: list[list[str]] = []
    for field in ("PM", "UA"):
        values = (state or {}).get(field) if isinstance(state, dict) else {}
        if not isinstance(values, dict):
            continue
        for value, meaning in values.items():
            rows.append([tex_code(f"STATUS.{field}"), tex_code(value), tex_escape(meaning)])
    if rows:
        return rows
    return [
        [tex_code("STATUS.PM"), tex_code("0"), tex_escape("user mode")],
        [tex_code("STATUS.PM"), tex_code("1"), tex_escape("supervisor mode")],
        [tex_code("STATUS.UA"), tex_code("0"), tex_escape("user-memory access disabled")],
        [tex_code("STATUS.UA"), tex_code("1"), tex_escape("user-memory access enabled")],
    ]


def privileged_model_rule_rows(model: dict[str, Any]) -> list[list[str]]:
    rules = model.get("normative_rules") if isinstance(model, dict) else None
    if not isinstance(rules, list) or not rules:
        rules = [
            {"topic": "privilege mode encoding", "rule": "STATUS.PM=0 is user mode; STATUS.PM=1 is supervisor mode"},
            {"topic": "user-memory access control", "rule": "STATUS.UA=0 disables supervisor access to user pages; STATUS.UA=1 enables it"},
            {"topic": "saved STATUS return", "rule": "STATUS is restored verbatim from the saved frame image; entry sets STATUS.PM=1 only and does not mask interrupts"},
            {"topic": "SYSCALL frame and entry", "rule": "SYSCALL saves SS:SP, CS:PC, DS, and FLAGS/STATUS, then uses a 32-byte entry table with 16-byte entry-address alignment"},
            {"topic": "return instruction split", "rule": "SYSRET is only for SYSCALL return; IRET is for interrupt, trap, and exception return"},
            {"topic": "IRET restore policy", "rule": "IRET restores all saved interrupt-frame state and does not validate FRAME_INFO.frame_type"},
            {"topic": "malformed return frames", "rule": "malformed frames are software errors and do not raise a separate architectural exception"},
            {"topic": "NMI and double-fault stacks", "rule": "NMI and DOUBLE_FAULT use the SN field of their IVT entries"},
            {"topic": "interrupt nesting limit", "rule": "when hidden_current_idepth equals ICR.MAX_IDEPTH, maskable interrupts are implicitly masked"},
            {"topic": "control-register access", "rule": "RDCR and WRCR are always privileged; user-visible control state uses dedicated gated instructions"},
            {"topic": "reserved CPU vectors", "rule": "reserved CPU vectors have no frame type; attempted delivery immediately becomes DOUBLE_FAULT"},
        ]
    rows = []
    for index, item in enumerate(rules, 1):
        if not isinstance(item, dict):
            continue
        rows.append(
            [
                tex_escape(str(index)),
                tex_escape(readable_text(item.get("topic", ""))),
                tex_escape(item.get("rule", "")),
            ]
        )
    return rows


def syscall_model_rows(model: dict[str, Any]) -> list[list[str]]:
    syscall = model.get("syscall") if isinstance(model, dict) else {}
    if not isinstance(syscall, dict):
        syscall = {}
    entry_registers = syscall.get("entry_registers") or ["SPC", "SCS", "SDS"]
    saved_state = syscall.get("saved_state") or ["SS:SP", "CS:PC", "DS", "FLAGS_STATUS"]
    return [
        [tex_escape("Entry vector"), tex_escape(syscall.get("vector", "none"))],
        [tex_escape("Entry target"), tex_table_value(entry_registers)],
        [tex_escape("Frame style"), tex_escape(syscall.get("frame_style", "expanded long-call frame"))],
        [tex_escape("Saved state"), tex_table_value(saved_state)],
        [tex_escape("Entry table size"), tex_escape(f"{syscall.get('entry_table_size_bytes', 32)} bytes")],
        [tex_escape("Entry address alignment"), tex_escape(f"{syscall.get('entry_address_alignment_bytes', 16)} bytes")],
        [tex_escape("Entry STATUS change"), tex_escape(syscall.get("status_change", "set STATUS.PM to 1 only"))],
        [tex_escape("Return instruction"), tex_code(syscall.get("return_instruction", "SYSRET"))],
        [tex_escape("Return policy"), tex_escape(syscall.get("return_policy", "read the syscall frame as written and return"))],
    ]


def privileged_rule_rows(model: dict[str, Any]) -> list[list[str]]:
    entry = model.get("entry_status_policy") if isinstance(model, dict) else {}
    irq = model.get("interrupt_exception_entry") if isinstance(model, dict) else {}
    returns = model.get("return_rules") if isinstance(model, dict) else {}
    nesting = model.get("interrupt_nesting") if isinstance(model, dict) else {}
    access = model.get("control_register_access") if isinstance(model, dict) else {}
    entry_changes = entry.get("entry_status_changes", ["set STATUS.PM to 1"]) if isinstance(entry, dict) else ["set STATUS.PM to 1"]
    return [
        [tex_escape("Entry STATUS update"), tex_table_value(entry_changes)],
        [tex_escape("Saved STATUS return"), tex_escape(entry.get("saved_status_return", "restored verbatim from the saved frame image") if isinstance(entry, dict) else "restored verbatim from the saved frame image")],
        [tex_escape("Entry interrupt masking"), tex_escape("no automatic masking" if not (entry.get("interrupt_masking_on_entry", False) if isinstance(entry, dict) else False) else "mask on entry")],
        [tex_escape("Interrupt stack selection"), tex_escape(irq.get("stack_selection", "IVT entry SN selects SSSn:SSPn") if isinstance(irq, dict) else "IVT entry SN selects SSSn:SSPn")],
        [tex_escape("NMI stack selection"), tex_escape(irq.get("nmi_stack_selection", "use the IVT entry SN field") if isinstance(irq, dict) else "use the IVT entry SN field")],
        [tex_escape("Double-fault stack selection"), tex_escape(irq.get("double_fault_stack_selection", "use the IVT entry SN field") if isinstance(irq, dict) else "use the IVT entry SN field")],
        [tex_escape("Interrupt frame save"), tex_escape(irq.get("frame_save", "atomic") if isinstance(irq, dict) else "atomic")],
        [tex_code("SYSRET"), tex_escape(returns.get("SYSRET", "syscall frame only") if isinstance(returns, dict) else "syscall frame only")],
        [tex_code("IRET"), tex_escape(returns.get("IRET", "restore all saved interrupt frame state; frame_type is not validated by hardware") if isinstance(returns, dict) else "restore all saved interrupt frame state; frame_type is not validated by hardware")],
        [tex_escape("Malformed return frame"), tex_escape(returns.get("malformed_frame", "software error; no architectural exception is raised") if isinstance(returns, dict) else "software error; no architectural exception is raised")],
        [tex_code("ICR.MAX_IDEPTH"), tex_escape(nesting.get("max_idepth_rule", "when hidden_current_idepth equals ICR.MAX_IDEPTH, maskable interrupts are implicitly masked") if isinstance(nesting, dict) else "when hidden_current_idepth equals ICR.MAX_IDEPTH, maskable interrupts are implicitly masked")],
        [tex_code("RDCR/WRCR"), tex_escape(f"RDCR = {access.get('RDCR', 'supervisor')}; WRCR = {access.get('WRCR', 'supervisor')}" if isinstance(access, dict) else "supervisor only")],
        [tex_escape("User-visible control state"), tex_escape(access.get("user_access_policy", "use dedicated instructions gated by control-register policy bits") if isinstance(access, dict) else "use dedicated instructions gated by control-register policy bits")],
    ]


def privileged_programming_model_section(spec: dict[str, Any]) -> str:
    model = privileged_programming_model(spec)
    return "\n".join(
        [
            "The privileged programming model defines how execution moves between user mode and supervisor mode, "
            "which saved state is used for return, and which control state is directly accessible.",
            r"\subsection{Privileged Model Rules}",
            "The following rules define the supervisor and exception-control behavior used by the rest of this manual.",
            latex_longtable(["No.", "Subject", "Rule"], privileged_model_rule_rows(model), ["0.35in", "1.45in", "3.65in"], "Table 8-1. Privileged Model Rules"),
            r"\subsection{Privilege State}",
            f"{tex_code('STATUS.PM')} selects the current privilege level. {tex_code('STATUS.UA')} controls supervisor access to user memory: "
            f"a clear {tex_code('UA')} bit disables supervisor access to user pages, while a set {tex_code('UA')} bit enables it.",
            latex_longtable(["Field", "Value", "Meaning"], privilege_state_rows(model), ["1.10in", "0.55in", "3.80in"], "Table 8-2. Privilege State Bits"),
            r"\subsection{SYSCALL and SYSRET}",
            f"{tex_code('SYSCALL')} is an explicit supervisor-entry path rather than an IVT-vector event. "
            "It behaves like an extended long call: it saves the user control state, uses a 32-byte supervisor-entry "
            "table with 16-byte entry-address alignment, loads the supervisor entry state from SPC/SCS/SDS, "
            "and sets STATUS.PM to supervisor mode. "
            f"{tex_code('SYSRET')} is the matching return instruction and is only for this syscall frame shape.",
            latex_longtable(["Property", "Rule"], syscall_model_rows(model), ["1.55in", "3.90in"], "Table 8-3. SYSCALL/SYSRET Rules"),
            r"\subsection{Interrupt and Control-State Rules}",
            "Trap, interrupt, and exception entry also set STATUS.PM to supervisor mode, but do not automatically mask interrupts. "
            "The saved STATUS image is restored verbatim by the matching return path. Malformed return frames are software errors; "
            "the architecture does not raise a second exception merely because the return frame is nonsensical.",
            latex_longtable(["Rule", "Meaning"], privileged_rule_rows(model), ["1.65in", "3.80in"], "Table 8-4. Privileged Execution Rules"),
        ]
    )


def ptcr_field_rows() -> list[list[str]]:
    return [
        [tex_code("root_page"), tex_escape("63:12"), tex_escape("page-table root physical frame number")],
        [tex_code("PABITS_SEL"), tex_escape("11:8"), tex_escape("physical address width selector; see the selector table below")],
        [tex_code("LA57"), tex_escape("7"), tex_escape("0 = 4-level paging with 48-bit canonical linear addresses; 1 = 5-level paging with 57-bit canonical linear addresses")],
        [tex_code("reserved"), tex_escape("6:1"), tex_escape("reserved, must be zero")],
        [tex_code("PE"), tex_escape("0"), tex_escape("page-table translation enable")],
    ]


def pabits_selector_rows(spec: dict[str, Any]) -> list[list[str]]:
    control = spec.get("registers", {}).get("translation_control") or {}
    ptcr = control.get("PTCR") if isinstance(control, dict) else {}
    entries = (ptcr or {}).get("PABITS_SEL") if isinstance(ptcr, dict) else None
    if not isinstance(entries, list) or not entries:
        entries = [
            {"selector": 0, "physical_address_bits": 48},
            {"selector": 1, "physical_address_bits": 56},
            {"selector": "2..15", "physical_address_bits": "reserved", "access_fault": "INVALID_CONTROL_STATE"},
        ]
    rows: list[list[str]] = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        selector = item.get("selector", "-")
        selector_text = str(selector) if isinstance(selector, str) else str(selector)
        fault = item.get("access_fault")
        rows.append(
            [
                tex_code(selector_text),
                tex_escape(item.get("physical_address_bits", "-")),
                tex_code(str(fault)) if fault else tex_escape("-"),
            ]
        )
    return rows


def ascr_field_rows() -> list[list[str]]:
    return [
        [tex_code("reserved"), tex_escape("63:32"), tex_escape("reserved, must be zero")],
        [tex_code("ASID"), tex_escape("31:16"), tex_escape("current address-space identifier")],
        [tex_code("reserved"), tex_escape("15:1"), tex_escape("reserved, must be zero")],
        [tex_code("AE"), tex_escape("0"), tex_escape("ASID enable")],
    ]


def pte_field_rows() -> list[list[str]]:
    return [
        [tex_code("P"), tex_escape("0"), tex_escape("Present")],
        [tex_code("W"), tex_escape("1"), tex_escape("Writable")],
        [tex_code("X"), tex_escape("2"), tex_escape("Executable")],
        [tex_code("U"), tex_escape("3"), tex_escape("User accessible")],
        [tex_code("G"), tex_escape("4"), tex_escape("Global TLB entry")],
        [tex_code("A"), tex_escape("5"), tex_escape("Accessed")],
        [tex_code("D"), tex_escape("6"), tex_escape("Dirty")],
        [tex_code("AT"), tex_escape("7"), tex_escape("0 = byte-addressed memory; 1 = externally acknowledged / bus-sized addressing")],
        [tex_code("CP"), tex_escape("9:8"), tex_escape("00 = cacheable; 01 = uncacheable; 10 = write-through; 11 = reserved")],
        [tex_code("SW0"), tex_escape("10"), tex_escape("software-defined")],
        [tex_code("T"), tex_escape("11"), tex_escape("0 = leaf PTE; 1 = next-level table entry")],
    ]


def pte_walk_rule_rows() -> list[list[str]]:
    return [
        [
            tex_escape("Non-leaf levels"),
            tex_escape("P must be 1 and T must be 1. The PFN names the next-level table frame. Large pages are not defined; T=0 above L1 reports PAGE_FAULT."),
        ],
        [
            tex_escape("L1 leaf level"),
            tex_escape("P must be 1 and T must be 0. The PFN names the mapped 4 KiB page frame. T=1 at L1 reports PAGE_FAULT."),
        ],
        [
            tex_escape("Not-present entries"),
            tex_escape("P=0 at any walk level reports PAGE_FAULT before the entry is used."),
        ],
    ]


def pte_attribute_rule_rows() -> list[list[str]]:
    return [
        [
            tex_code("W/X/U"),
            tex_escape("Permission bits are accumulated across the walk. A store, instruction fetch, or user access is allowed only if every traversed entry and the leaf permit it."),
        ],
        [
            tex_code("A"),
            tex_escape("Set on each non-leaf entry successfully traversed and on the leaf entry successfully used."),
        ],
        [
            tex_code("D"),
            tex_escape("Leaf-only dirty bit. Set on a successful store through the leaf mapping; must be zero in non-leaf entries."),
        ],
        [
            tex_code("G"),
            tex_escape("Leaf-only global-translation marker; must be zero in non-leaf entries."),
        ],
        [
            tex_code("CP"),
            tex_escape("For non-leaf entries, selects the cache policy for hardware table-walk accesses to the next-level table. For leaf entries, selects the cache policy for the mapped access."),
        ],
        [
            tex_code("AT"),
            tex_escape("Must be zero in non-leaf entries. In leaf entries it is an access attribute only: address formation remains PFN plus page offset."),
        ],
        [
            tex_code("SW0"),
            tex_escape("Software-defined and ignored by hardware at every level."),
        ],
    ]


def pte_permission_rule_rows(spec: dict[str, Any]) -> list[list[str]]:
    control = spec.get("registers", {}).get("translation_control") or {}
    pte = (control.get("page_table_entry") or {}) if isinstance(control, dict) else {}
    rules = pte.get("permission_rules") if isinstance(pte, dict) else None
    if not isinstance(rules, list) or not rules:
        rules = [
            {"mode": "user", "condition": "effective U permission is 0", "result": "PRIVILEGE_FAULT"},
            {"mode": "user", "condition": "effective U permission is 1", "result": "allowed subject to present, W/X, and access-type checks"},
            {"mode": "supervisor", "condition": "effective U permission is 0", "result": "allowed subject to present, W/X, and access-type checks"},
            {"mode": "supervisor", "condition": "effective U permission is 1 and STATUS.UA is 0", "result": "PAGE_FAULT"},
            {"mode": "supervisor", "condition": "effective U permission is 1 and STATUS.UA is 1", "result": "allowed subject to present, W/X, and access-type checks"},
        ]
    rows: list[list[str]] = []
    for item in rules:
        if not isinstance(item, dict):
            continue
        rows.append(
            [
                tex_escape(item.get("mode", "-")),
                tex_escape(item.get("condition", "-")),
                tex_escape(item.get("result", "-")),
            ]
        )
    return rows


def icr_field_rows() -> list[list[str]]:
    return [
        [tex_code("ivt_page"), tex_escape("63:12"), tex_escape("interrupt vector table frame number / page number")],
        [tex_code("MAX_IDEPTH"), tex_escape("11:8"), tex_escape("0 disables maskable interrupt nesting; n is the maximum hidden_current_idepth; equality implicitly masks maskable interrupts")],
        [tex_code("NMI_PENDING"), tex_escape("7"), tex_escape("hardware-managed NMI pending bit")],
        [tex_code("NMI_LATCH"), tex_escape("6"), tex_escape("latch NMI while STATUS.NI = 1")],
        [tex_code("DF_ENABLE"), tex_escape("5"), tex_escape("double-fault handling enable")],
        [tex_code("reserved"), tex_escape("4:1"), tex_escape("reserved, must be zero")],
        [tex_code("IVT_VALID"), tex_escape("0"), tex_escape("interrupt vector table valid")],
    ]


def ivt_entry_rows() -> list[list[str]]:
    return [
        [tex_code("handler"), tex_escape("bytes 0..7"), tex_escape("64-bit interrupt handler address")],
        [tex_code("HP"), tex_escape("byte 8 bit 0"), tex_escape("handler present; if clear, delivery becomes DOUBLE_FAULT")],
        [tex_code("reserved"), tex_escape("byte 8 bit 1"), tex_escape("reserved, must be zero")],
        [
            tex_code("SN"),
            tex_escape("byte 8 bits 3:2"),
            tex_multiline(
                [
                    "selects interrupt stack bank:",
                    "0 = SSS0:SSP0",
                    "1 = SSS1:SSP1",
                    "2 = SSS2:SSP2",
                    "3 = SSS3:SSP3",
                ]
            ),
        ],
        [tex_code("reserved"), tex_escape("byte 8 bits 7:4"), tex_escape("reserved, must be zero")],
        [tex_code("reserved"), tex_escape("bytes 9..15"), tex_escape("reserved, must be zero")],
    ]



def stack_frame_rows(control: dict[str, Any]) -> list[list[str]]:
    rows = []
    for slot in supervisor_stack_frame(control).get("layout", []) or []:
        offset = int(slot.get("offset", 0))
        rows.append(
            [
                tex_code(f"+0x{offset:02X}"),
                tex_code(str(slot.get("name", ""))),
                tex_escape(slot.get("description", "")),
            ]
        )
    return rows


def frame_type_rows(control: dict[str, Any]) -> list[list[str]]:
    frame = supervisor_stack_frame(control)
    frame_types = frame.get("frame_types") or []
    rows = []
    for frame_type in frame_types:
        if not isinstance(frame_type, dict):
            continue
        code = frame_type.get("code", "-")
        if isinstance(code, int):
            code_text = f"0x{code:x}"
        else:
            code_text = str(code)
        payload = frame_type.get("payload") or []
        rows.append(
            [
                tex_code(code_text),
                tex_code(str(frame_type.get("name", ""))),
                tex_table_value(payload or "none"),
                tex_table_value(frame_type.get("description", "")),
            ]
        )
    return rows


def frame_info_rows(control: dict[str, Any]) -> list[list[str]]:
    frame_info = (supervisor_stack_frame(control).get("frame_info") or {}) if isinstance(control, dict) else {}
    if not isinstance(frame_info, dict) or not frame_info:
        frame_info = {
            "vector": {"bits": [0, 7], "description": "interrupt, exception, or trap vector number"},
            "frame_size_units": {"bits": [8, 15], "description": "total frame size in 8-byte units"},
            "saved_idepth": {"bits": [16, 19], "description": "saved interrupt nesting depth"},
            "frame_type": {"bits": [20, 23], "description": "supervisor stack frame type code"},
            "from_user": {"bit": 24, "description": "entry was taken from user mode"},
            "nmi_frame": {"bit": 25, "description": "frame was created by NMI entry"},
            "rep_fault": {"bit": 26, "description": "fault occurred during REP, REPcc, or REPG repeated execution"},
            "reserved": {"bits": [27, 63], "description": "reserved, must be zero"},
        }
    rows = []
    for name, field in frame_info.items():
        if not isinstance(field, dict):
            continue
        if "bit" in field:
            location = str(field.get("bit"))
        else:
            bits = field.get("bits", [])
            location = f"{bits[0]}..{bits[1]}" if isinstance(bits, list) and len(bits) == 2 else "-"
        rows.append([tex_code(str(name)), tex_escape(location), tex_escape(field.get("description", ""))])
    return rows


def repeat_fault_aux_rows(control: dict[str, Any]) -> list[list[str]]:
    def split_long_table_line(line: str, limit: int = 52) -> list[str]:
        if len(line) <= limit:
            return [line]
        words = line.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if len(candidate) > limit and current:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines

    frame = supervisor_stack_frame(control)
    aux = frame.get("repeat_fault_aux") if isinstance(frame, dict) else None
    if not isinstance(aux, dict):
        aux = {
            "fields": {
                "counter_register": {"bits": [0, 2], "description": "D-register counter number, D0-D7"},
                "group_start_delta_words": {
                    "bits": [3, 7],
                    "description": "REPG-general/REPG-fast unsigned negative displacement in 16-bit words from fault_pc to group start",
                },
                "repeat_kind": {
                    "bits": [8, 9],
                    "description": "repeat context kind",
                    "values": {0: "REP_or_REPcc", 1: "REPG-general", 2: "REPG-fast", 3: "reserved"},
                },
                "reserved": {"bits": [10, 63], "description": "reserved, must be zero"},
            }
        }
    fields = aux.get("fields") or {}
    rows: list[list[str]] = []
    if not isinstance(fields, dict):
        return rows
    for name, field in fields.items():
        if not isinstance(field, dict):
            continue
        if "bit" in field:
            location = str(field.get("bit"))
        else:
            bits = field.get("bits", [])
            location = f"{bits[0]}..{bits[1]}" if isinstance(bits, list) and len(bits) == 2 else "-"
        description = str(field.get("description", ""))
        values = field.get("values")
        description_lines: list[str] = []
        for line in description.splitlines():
            parts = line.split("; ")
            if len(parts) > 1:
                for index, part in enumerate(parts):
                    suffix = ";" if index < len(parts) - 1 else ""
                    description_lines.extend(split_long_table_line(part + suffix))
            else:
                description_lines.extend(split_long_table_line(line))
        if isinstance(values, dict) and values:
            value_lines = [f"{key}: {readable_text(value)}" for key, value in values.items()]
            description_lines.extend(value_lines)
        rows.append([tex_code(str(name)), tex_escape(location), tex_multiline(description_lines)])
    return rows


def vector_hex(value: Any) -> str:
    if isinstance(value, int):
        return f"0x{value:02X}"
    text = str(value)
    try:
        return f"0x{int(text, 0):02X}"
    except ValueError:
        return text


def vector_range_text(value: Any) -> str:
    if isinstance(value, list) and len(value) == 2:
        low = vector_hex(value[0])
        high = vector_hex(value[1])
        return low if low == high else f"{low}..{high}"
    return str(value)


def interrupt_vector_assignment(control: dict[str, Any]) -> dict[str, Any]:
    assignment = (control.get("interrupt_vector_assignment") or {}) if isinstance(control, dict) else {}
    if isinstance(assignment, dict) and assignment:
        return assignment
    return {
            "policy": "Vectors 0x00..0x1F are CPU-owned. Assigned CPU vectors are grouped by supervisor stack frame type; reserved CPU vectors do not predefine a frame type. PRIVILEGE_FAULT precedes PAGE_FAULT. Length and segment faults have no separate CPU vectors; canonical-address faults report as PAGE_FAULT when paging is enabled. Vectors 0x20..0x3F are reserved for future architecture; 0x40..0xFF are OS/platform/device assignable.",
        "syscall_vector": "none",
        "syscall_entry": "SPC/SCS/SDS supervisor-entry path",
        "ranges": [
            {"range": [0x00, 0x05], "owner": "CPU", "meaning": "assigned BASIC-frame CPU exceptions and traps"},
            {"range": [0x06, 0x07], "owner": "CPU", "meaning": "reserved CPU vectors; frame type not predefined"},
            {"range": [0x08, 0x0E], "owner": "CPU", "meaning": "assigned ERROR/PAGE_FAULT-frame CPU exceptions"},
            {"range": [0x0F, 0x0F], "owner": "CPU", "meaning": "reserved CPU vector; frame type not predefined"},
            {"range": [0x10, 0x17], "owner": "CPU", "meaning": "reserved CPU vectors; frame type not predefined"},
            {"range": [0x18, 0x1A], "owner": "CPU", "meaning": "assigned AUX_FAULT-frame CPU exceptions"},
            {"range": [0x1B, 0x1F], "owner": "CPU", "meaning": "reserved CPU vectors; frame type not predefined"},
            {"range": [0x20, 0x3F], "owner": "CPU", "meaning": "reserved for future architectural vectors"},
            {"range": [0x40, 0xFF], "owner": "OS/platform/device", "meaning": "assignable interrupt and event vectors"},
        ],
        "vectors": [
            {"vector": 0x05, "name": "TRAP", "source": "TRAP instruction or true TRAPcc condition", "frame_type": "BASIC"},
            {"vector": 0x08, "name": "PRIVILEGE_FAULT", "source": "privileged instruction, CR access, or supervisor-only state violation", "frame_type": "ERROR"},
            {"vector": 0x09, "name": "PAGE_FAULT", "source": "segment, paging-enabled canonical-address, page-table, permission, presence, or stack-memory translation failure", "frame_type": "PAGE_FAULT"},
        ],
    }


def interrupt_vector_range_rows(control: dict[str, Any]) -> list[list[str]]:
    rows = []
    for item in interrupt_vector_assignment(control).get("ranges", []):
        if not isinstance(item, dict):
            continue
        rows.append(
            [
                tex_code(vector_range_text(item.get("range", ""))),
                tex_escape(item.get("owner", "")),
                tex_escape(item.get("meaning", "")),
            ]
        )
    return rows


def interrupt_vector_rows(control: dict[str, Any]) -> list[list[str]]:
    rows = []
    for item in interrupt_vector_assignment(control).get("vectors", []):
        if not isinstance(item, dict):
            continue
        frame_type = item.get("frame_type")
        frame_text = readable_text(frame_type) if frame_type else "-"
        rows.append(
            [
                tex_code(vector_hex(item.get("vector", ""))),
                tex_escape(readable_text(item.get("name", ""))),
                tex_escape(item.get("source", "")),
                tex_escape(frame_text),
            ]
        )
    return rows


def exception_processing_rows(control: dict[str, Any]) -> list[list[str]]:
    model = control.get("exception_processing") if isinstance(control, dict) else {}
    if not isinstance(model, dict):
        model = {}
    privileged = control.get("privileged_programming_model") if isinstance(control, dict) else {}
    returns = (privileged or {}).get("return_rules", {}) if isinstance(privileged, dict) else {}
    priority = model.get("fault_priority", [])
    collapsed = model.get("collapsed_fault_classes", {})
    if isinstance(collapsed, dict) and collapsed:
        collapsed_text = "; ".join(f"{key}: {value}" for key, value in collapsed.items())
    else:
        collapsed_text = "length fault has no separate vector; segment failures and paging-enabled canonical-address failures report as PAGE_FAULT"
    return [
        [tex_escape("CPU exception model"), tex_escape(model.get("cpu_exception_model", "synchronous, restartable"))],
        [tex_escape("Restart policy"), tex_escape(model.get("restart_policy", "the OS decides whether to retry, emulate, report, or terminate"))],
        [tex_escape("Interrupt frame save"), tex_escape(model.get("interrupt_frame_save", "atomic"))],
        [tex_escape("Entry STATUS update"), tex_escape(model.get("status_on_entry", "set STATUS.PM to 1 only; do not automatically mask interrupts"))],
        [tex_escape("Return STATUS update"), tex_escape(model.get("status_on_return", "restore saved STATUS image verbatim"))],
        [tex_code("SYSRET"), tex_escape(returns.get("SYSRET", "syscall frame only") if isinstance(returns, dict) else "syscall frame only")],
        [tex_code("IRET"), tex_escape(returns.get("IRET", "restore all saved interrupt frame state; frame_type is not validated by hardware") if isinstance(returns, dict) else "restore all saved interrupt frame state; frame_type is not validated by hardware")],
        [tex_escape("IRET frame-type check"), tex_escape(model.get("iret_frame_type_check", "none; IRET does not validate FRAME_INFO.frame_type"))],
        [tex_escape("Malformed return frame"), tex_escape(model.get("malformed_return_frame", "software error; no separate architectural exception"))],
        [tex_escape("Absent IVT handler"), tex_escape(model.get("handler_absent_behavior", "IVT HP=0 immediately becomes DOUBLE_FAULT"))],
        [tex_escape("Reserved CPU vector"), tex_escape(model.get("reserved_cpu_vector_behavior", "reserved CPU vectors have no frame type; attempted delivery immediately becomes DOUBLE_FAULT"))],
        [tex_escape("Fault priority"), tex_table_value(priority or "privilege fault, page fault")],
        [tex_escape("Collapsed fault classes"), tex_escape(collapsed_text)],
        [tex_escape("Address fault vector"), tex_escape(model.get("address_fault_vector", "PAGE_FAULT"))],
    ]


def interrupt_model_section(spec: dict[str, Any]) -> str:
    registers = spec.get("registers", {})
    control = registers.get("translation_control") or {}
    if not isinstance(control, dict):
        control = {}
    frame = supervisor_stack_frame(control)
    assignment = interrupt_vector_assignment(control)
    unit = int(frame.get("frame_size_unit_bytes", 8))
    base_size = int(frame.get("base_size_bytes", 96))
    fixed_slots = len(frame.get("layout") or [])
    return "\n".join(
        [
            "Exception processing covers synchronous restartable CPU exceptions, traps, NMIs, external interrupts, and the "
            "supervisor-entry state needed to return from them. The processor records a restartable context for CPU exceptions; "
            "the operating system decides whether that context is retried, emulated, reported, or terminated. ICR selects the "
            "interrupt vector table page and controls interrupt nesting; each IVT entry selects a handler and one of the "
            "supervisor stack banks.",
            r"\subsection{Interrupt Vector Table}",
            r"The interrupt vector table occupies one 4096-byte page selected by \texttt{ICR.ivt\_page}. It contains 256 fixed-size "
            r"entries, each 16 bytes. The vector number selects the entry at \texttt{ICR.ivt\_page} * 4096 + vector * 16.",
            ivt_entry_figure(),
            "Bytes 0 through 7 contain the 64-bit interrupt handler address. Byte 8 is the entry control byte. "
            f"HP is the handler-present bit; if it is clear, delivery immediately becomes {tex_code('DOUBLE_FAULT')}. SN selects one of "
            "four interrupt stack banks, SSS0:SSP0 through SSS3:SSP3. Byte 8 bit 1 and bits 7 through 4 are reserved, "
            "and bytes 9 through 15 are reserved.",
            ivt_control_byte_figure(),
            latex_longtable(["Field", "Location", "Meaning"], ivt_entry_rows(), ["0.95in", "0.85in", "3.65in"], "Table 4-1. Interrupt Vector Table Entry Fields"),
            r"\Needspace{3.4in}",
            r"\subsection{Vector Assignment}",
            tex_escape(assignment.get("policy", "")),
            f"{tex_code('SYSCALL')} does not allocate or consume an IVT vector. It enters supervisor mode through the "
            f"{tex_code(str(assignment.get('syscall_entry', 'SPC/SCS/SDS supervisor-entry path')))}.",
            latex_longtable(["Range", "Owner", "Meaning"], interrupt_vector_range_rows(control), ["0.85in", "1.35in", "3.30in"], "Table 4-2. Interrupt Vector Ranges"),
            latex_longtable(["Vector", "Name", "Source", "Frame"], interrupt_vector_rows(control), ["0.55in", "1.65in", "2.20in", "1.00in"], "Table 4-3. CPU-Owned Interrupt Vectors"),
            r"\subsection{Entry and Return Rules}",
            "The processor changes only the privilege bit on entry: STATUS.PM is set to supervisor mode. "
            "Interrupts are not automatically masked merely because an exception or interrupt was taken. "
            "The interrupt stack frame is saved atomically. When returning, the saved STATUS image is restored exactly "
            "as recorded in the frame.",
            latex_longtable(["Rule", "Meaning"], exception_processing_rows(control), ["1.55in", "3.90in"], "Table 4-4. Exception Entry and Return Rules"),
            r"\clearpage",
            r"\subsection{Supervisor Entry Stack Frame}",
            f"The fixed supervisor-entry frame is {base_size} bytes: {fixed_slots} 64-bit slots. "
            f"{tex_code('FRAME_INFO.frame_size_units')} records the total frame size in {unit}-byte units, so the base frame records "
            f"{base_size // unit} units before any optional payload. Offsets are measured from the saved stack pointer.",
            stack_frame_figure(control),
            latex_longtable(["Offset", "Slot", "Meaning"], stack_frame_rows(control), ["0.70in", "1.20in", "3.60in"], "Table 4-5. Supervisor Entry Stack Frame"),
            f"{tex_code('FRAME_INFO.frame_type')} documents the stack frame format, M68000-style. "
            "Payload slots, if any, are appended after the fixed frame in the order listed for the selected type. "
            f"{tex_code('FRAME_INFO.frame_size_units')} gives the total number of {unit}-byte slots, and the "
            "frame type code determines how software interprets the appended slots. IRET does not validate the frame type.",
            latex_longtable(["Code", "Type", "Payload", "Meaning"], frame_type_rows(control), ["0.45in", "1.10in", "1.65in", "2.30in"], "Table 4-6. Supervisor Stack Frame Types"),
            frame_info_figure(),
            latex_longtable(["Field", "Bits", "Meaning"], frame_info_rows(control), ["1.35in", "0.60in", "3.55in"], "Table 4-7. FRAME_INFO Fields"),
            r"\paragraph{Repeat Fault Continuation.}",
            f"When {tex_code('FRAME_INFO.rep_fault')} is set, the {tex_code('FAULT_AUX')} payload records the active repeat context. "
            f"{tex_code('FAULT_AUX.repeat_kind')} distinguishes {tex_code('REP')}/{tex_code('REPcc')}, "
            f"{tex_code('REPG-general')}, and {tex_code('REPG-fast')} continuations. "
            f"For {tex_code('REPG')}, the saved {tex_code('PC')} is the faulting grouped instruction, and the group start is reconstructed as "
            f"{tex_code('group_start_pc = fault_pc - 2 * group_start_delta_words')}. "
            "The delta is an unsigned negative displacement measured in 16-bit words, so five bits cover the full 64-byte grouping window. "
            "Returning with IRET preserves the continuation state: execution resumes at the saved faulting instruction under the active repeat context. "
            "Software that wants to abandon or emulate the repeated operation may edit the frame before returning.",
            latex_longtable(["Field", "Bits", "Meaning"], repeat_fault_aux_rows(control), ["1.55in", "0.60in", "3.35in"], "Table 4-8. Repeat Fault Auxiliary Fields"),
            r"\subsection{Interrupt Reset State}",
            latex_longtable(["State", "Reset Value"], reset_state_rows(control), ["2.1in", "2.4in"], "Table 4-9. Interrupt and Translation Reset State"),
        ]
    )


def reset_state_rows(control: dict[str, Any]) -> list[list[str]]:
    reset = (control.get("reset_state") or {}) if isinstance(control, dict) else {}
    rows = [[tex_code(key), tex_table_value(value)] for key, value in reset.items()]
    if rows:
        return rows
    return [
        [tex_code("ICR"), tex_escape("0")],
        [tex_code("ICR.IVT_VALID"), tex_escape("0")],
        [tex_code("STATUS.IE"), tex_escape("0")],
        [tex_code("STATUS.IN"), tex_escape("0")],
        [tex_code("STATUS.NI"), tex_escape("0")],
        [tex_code("hidden_current_idepth"), tex_escape("0")],
        [tex_code("hidden_nmi_pending"), tex_escape("0")],
        [tex_code("PTCR.PE"), tex_escape("0")],
        [tex_code("ASCR"), tex_escape("0")],
    ]


def memory_address_translation_section(spec: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Memory address translation is a separate pipeline after effective-address calculation. "
            "Effective-address evaluation produces an EA value or address expression; segmentation optionally turns that value into "
            "a linear address, and paging optionally turns the linear address into a memory-system address.",
            translation_pipeline_figure(),
            r"\subsection{Translation Pipeline}",
            latex_longtable(
                ["Stage", "Result"],
                [
                    [tex_escape("Effective address"), tex_escape("address generated by the selected EA form")],
                    [tex_escape("Segment pre-translation"), tex_escape("disabled segment passes the address through; enabled segment checks a byte-addressed window with page-granular base and span")],
                    [tex_escape("Linear address"), tex_escape("segment output, or the EA directly when segmentation is disabled")],
                    [tex_escape("Paging, PTCR.PE = 1"), tex_escape("walk page tables from PTCR.root_page and apply PTE attributes")],
                    [tex_escape("Paging, PTCR.PE = 0"), tex_escape("use the linear address directly")],
                ],
                ["1.65in", "3.85in"],
                "Table 3-1. Address Translation Stages",
            ),
            segment_paging_interaction_section(),
            r"\subsection{Segmentation Stage}",
            "Segmentation is a page-granular address-window and pre-translation mechanism, not the primary memory-protection mechanism. "
            "A segment with m = 0 is disabled and passes the effective-address result through unchanged. "
            "A translated segment checks an offset against the segment span and then adds the segment base. "
            "A bounds-only segment checks an already-linear address against the segment window without adding the base.",
            r"\begin{align*}",
            r"\mathit{base} &= \mathit{base\_page} \times 4096\\",
            r"\mathit{span} &= m \times 2^e \times 4096\\",
            r"\mathit{limit} &= \mathit{base} + \mathit{span}\\",
            r"m=0:\quad \mathit{linear} &= x\\",
            r"m\ne0,\ b=0:\quad 0 \le x < \mathit{span},\quad \mathit{linear} &= \mathit{base}+x\\",
            r"m\ne0,\ b=1:\quad \mathit{base} \le x < \mathit{limit},\quad \mathit{linear} &= x",
            r"\end{align*}",
            r"The base, span, and limit are computed in an unsigned domain wide enough to represent the full 64-bit linear-address space plus one. "
            r"If \(\mathit{limit} > 2^{64}\), the segment register image is invalid and any access through it reports \texttt{PAGE\_FAULT}.",
            r"\subsection{Paging Stage}",
            "Paging performs final address translation and supplies the protection attributes. LA57 selects either four-level paging "
            "with 48-bit canonical linear addresses or five-level paging with 57-bit canonical linear addresses. PTE[0..11] are "
            "architecturally assigned low attribute bits, PTE[12..PABITS-1] contains the physical frame number or next-table frame number, "
            "and PTE[PABITS..63] is software-defined. Bit 10 is reserved for software use.",
            r"\clearpage",
            r"\subsection{LA48 Four-Level Paging}",
            "When PTCR.LA57 is zero, paging uses a 48-bit canonical linear address. Bits 63..48 must be the canonical sign extension of bit 47. "
            "The remaining address bits select four nine-bit page-table indexes followed by a twelve-bit page offset.",
            la48_paging_figure(),
            r"\clearpage",
            r"\subsection{LA57 Five-Level Paging}",
            "When PTCR.LA57 is one, paging uses a 57-bit canonical linear address. Bits 63..57 must be the canonical sign extension of bit 56. "
            "The additional L5 index selects the top-level table before the same L4 through L1 walk used by LA48.",
            la57_paging_figure(),
            r"\clearpage",
            r"\subsection{Page-Table Entry Format}",
            pte_attribute_figure(),
            latex_longtable(["Field", "Bits", "Meaning"], pte_field_rows(), ["0.55in", "0.65in", "4.25in"], "Table 3-2. Page-Table Entry Low Attribute Bits"),
            latex_longtable(["Level", "Rule"], pte_walk_rule_rows(), ["1.15in", "4.35in"], "Table 3-3. Page-Walk Level Rules"),
            latex_longtable(["Field", "Rule"], pte_attribute_rule_rows(), ["0.75in", "4.75in"], "Table 3-4. PTE Attribute Semantics"),
            latex_longtable(["Mode", "Condition", "Result"], pte_permission_rule_rows(spec), ["0.85in", "2.35in", "2.30in"], "PTE User-Permission Rules"),
        ]
    )


def condition_table(spec: dict[str, Any]) -> str:
    rows = []
    for condition in spec.get("conditions", {}).get("conditions", []) or []:
        aliases = condition.get("aliases", []) or []
        rows.append(
            [
                tex_code(condition.get("name", "")),
                tex_code(hex(int(condition.get("value", 0)))),
                tex_table_value(aliases or "-"),
                tex_code(condition.get("expression", "")),
            ]
        )
    intro = (
        "Conditional instructions encode a four-bit condition code. The zero-valued condition is T, "
        "which is also used for canonical aliases such as JMP for Jcc.T and TRAP for TRAPcc.T. "
        "The condition-code bits are the low four meaningful bits of FLAGS, as shown in the Register Model section."
    )
    return "\n".join(
        [
            intro,
            latex_longtable(["Code", "Value", "Aliases", "Expression"], rows, ["0.65in", "0.65in", "1.05in", "2.95in"], "Table 4-1. Condition Codes"),
        ]
    )


def prefix_semantics_block(prefix: dict[str, Any]) -> str:
    detail = tex_escape(prefix.get("description") or readable_text(prefix.get("semantics", "-")))
    applies_to = prefix.get("applies_to") or []
    if applies_to:
        detail += r"\newline " + tex_escape("Applies to: " + ", ".join(str(item) for item in applies_to))
    requires = prefix.get("requires")
    if isinstance(requires, dict):
        require_text = ", ".join(f"{key}={value}" for key, value in requires.items())
        detail += r"\newline " + tex_escape("Requires: " + require_text)
    eligible = prefix.get("eligible_mnemonics") or []
    if eligible:
        detail += r"\newline " + tex_escape("Eligible instructions: " + ", ".join(str(item) for item in eligible))
    syntax = prefix.get("syntax")
    if isinstance(syntax, dict):
        aliases = syntax.get("aliases") or {}
        if aliases:
            alias_text = ", ".join(f"{key}={value}" for key, value in aliases.items())
            detail += r"\newline " + tex_escape("Aliases: " + alias_text)
        examples = syntax.get("examples") or []
        if examples:
            detail += r"\newline " + "Examples: " + ", ".join(tex_code(example) for example in examples)
    return detail


def prefix_semantics_section(spec: dict[str, Any]) -> str:
    lines = [
        r"\subsection{Prefix Semantics}",
        "Prefix bytes are interpreted as modifiers of the immediately following instruction only. "
        "Assemblers should avoid redundant or contradictory prefixes, but architectural prefix interpretation remains deterministic because later prefix slots override earlier conflicting effects.",
    ]
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        if prefix.get("name") in {"REPcc", "REPG"}:
            continue
        if prefix.get("group") in {"ea_update", "repeat_boundary"}:
            continue
        lines.append(rf"\Needspace{{0.75in}}\manualfield{{{tex_code(prefix.get('name', ''))}:}}{{{prefix_semantics_block(prefix)}}}")
    return "\n".join(lines)


def prefix_is_address_update(prefix: dict[str, Any]) -> bool:
    return prefix.get("group") == "ea_update"


def prefix_encoding_text(prefix: dict[str, Any]) -> str:
    pattern = prefix.get("pattern")
    if pattern:
        return str(pattern)
    return f"0x{int(prefix.get('value', 0)):02x}"


def prefix_syntax_text(prefix: dict[str, Any]) -> str:
    name = str(prefix.get("name", ""))
    syntax = prefix.get("syntax")
    if name == "REPcc":
        return "REP{cc} Dn, instr"
    if name == "REPG":
        return "REPG Dn, {...}"
    if name == "ENDG":
        return "ENDG"
    if isinstance(syntax, dict):
        if syntax.get("assembler_generated"):
            return "(generated)"
        if syntax.get("block"):
            return str(syntax.get("block_template", "REPG Dn, { ... }"))
        template = str(syntax.get("mnemonic_template", name))
        if syntax.get("applies_to_following_instruction"):
            return f"{template} Dn, instr"
        return template
    return {
        "SATURATE": "SAT",
        "NONTEMPORAL": "NT",
    }.get(name, name)


def address_update_operand_syntax(name: str) -> str:
    return {
        "POSTINC": "[A++]",
        "PREINC": "[++A]",
        "POSTDEC": "[A--]",
        "PREDEC": "[--A]",
    }.get(name, name)


def address_update_description(name: str) -> str:
    return {
        "POSTINC": "use EA, then increment",
        "PREINC": "increment, then use EA",
        "POSTDEC": "use EA, then decrement",
        "PREDEC": "decrement, then use EA",
    }.get(name, readable_text(name))


def address_update_operand_table(spec: dict[str, Any]) -> str:
    rows = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict) or not prefix_is_address_update(prefix):
            continue
        name = str(prefix.get("name", ""))
        rows.append(
            [
                tex_code(address_update_operand_syntax(name)),
                tex_code(prefix_encoding_text(prefix)),
                tex_escape(address_update_description(name)),
            ]
        )
    if not rows:
        return ""
    return "\n".join(
        [
            r"\subsection{Address-Update Operand Syntax}",
            "Address update is selected by the memory operand spelling, not by a standalone prefix mnemonic. "
            "The assembler emits the corresponding prefix byte only for update-eligible indirect EA forms. "
            "Because legality depends on the selected EA form, address update is not listed as a separate "
            "per-mnemonic column in the instruction attribute matrix.",
            latex_longtable(
                ["Operand Syntax", "Byte", "Update"],
                rows,
                ["1.25in", "0.75in", "3.1in"],
                "Address-Update Encodings",
            ),
        ]
    )


def prefix_table(spec: dict[str, Any]) -> str:
    rows = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        if prefix_is_address_update(prefix):
            continue
        rows.append(
            [
                tex_code(prefix_syntax_text(prefix)),
                tex_code(prefix_encoding_text(prefix)),
                tex_table_value(prefix.get("semantics", "-")),
            ]
        )
    text = (
        "Prefix words modify the following instruction. One prefix word contains two 8-bit slots; "
        "the low byte is filled and decoded first, and the high byte is filled and decoded second. "
        "The table below lists standalone prefix spellings and assembler-generated repeat-boundary bytes. "
        "Address-update forms are shown separately because they are selected by operand syntax."
    )
    return "\n".join(
        [
            text,
            latex_longtable(
                ["Syntax", "Byte/Pattern", "Meaning"],
                rows,
                ["1.45in", "0.95in", "3.0in"],
                "Prefix Encodings",
            ),
            address_update_operand_table(spec),
            prefix_semantics_section(spec),
            repcc_prefix_section(spec),
            repg_prefix_section(spec),
        ]
    )


def repcc_prefix_section(spec: dict[str, Any]) -> str:
    instructions = spec.get("instructions") or {}
    semantics = instructions.get("operation_semantics") or {}
    repeat = (semantics.get("repeat_prefixes") or {}).get("REPcc", {})
    prefix = next(
        (
            candidate
            for candidate in spec.get("prefixes", {}).get("prefixes", []) or []
            if isinstance(candidate, dict) and candidate.get("name") == "REPcc"
        ),
        {},
    )
    if not repeat and not prefix:
        return ""

    eligible = repeat.get("eligible_mnemonics", prefix.get("eligible_mnemonics", [])) or []
    eligible_text = eligible if eligible else repeat.get(
        "eligible_operation_attribute",
        prefix.get("eligible_operation_attribute", "-"),
    )
    fpu_conditional = repeat.get(
        "fpu_conditional_mnemonics",
        prefix.get("fpu_conditional_mnemonics", []),
    ) or []
    syntax = repeat.get("syntax")
    if not syntax:
        syntax_info = prefix.get("syntax") or {}
        syntax = syntax_info.get("mnemonic_template", "REP{condition}") + " Dn, <instruction>" if isinstance(syntax_info, dict) else "REP{condition} Dn, <instruction>"

    rep_rows = [
        [tex_escape("Syntax"), tex_code(syntax)],
        [tex_escape("Alias"), tex_table_value(repeat.get("alias", "REP = REPT"))],
        [tex_escape("Eligible instructions"), tex_table_value(eligible_text)],
        [tex_escape("FPU conditional subset"), tex_table_value(fpu_conditional or "-")],
        [tex_escape("FPU status predicates"), tex_table_value(repeat.get("fpu_fflags_condition_repeat", "not supported"))],
        [tex_escape("Counter"), tex_escape(f"{repeat.get('counter', 'DREG')}, {readable_text(repeat.get('counter_direction', 'signed_toward_zero'))}")],
        *repeat_counter_encoding_rows(repeat or prefix),
        [tex_escape("Commit rule"), tex_table_value(repeat.get("commit_rule", "-"))],
        [tex_escape("Condition source"), tex_table_value(repeat.get("condition_source", "-"))],
        [tex_escape("Architectural flags"), tex_table_value(repeat.get("architectural_flags", "-"))],
        [tex_escape("FFLAGS"), tex_table_value(repeat.get("fflags_accumulation", "-"))],
    ]
    parts = [
        r"\subsection{Conditional Repeat Prefix REPcc}",
        "REPcc is the conditional repeat prefix family. It combines a D-register repeat counter with a full condition-code selector, "
        "then applies that repeat contract to the following eligible instruction. "
        "REP is the canonical alias for REPT.",
        "The selected D register remains an ordinary signed two's-complement value. "
        "REP/REPcc tests that value for zero before each iteration. "
        "After the instruction body completes, REPFLAGS are computed from the observed value; the counter moves one step toward zero only when the selected REP condition remains true. "
        "A completed terminating iteration whose REP condition is false commits the instruction body's ordinary side effects but leaves the counter unchanged. "
        "If the same D register appears in an indexed effective address, EA evaluation uses the same architectural value before the iteration update.",
        latex_longtable(
            ["Item", "Value"],
            rep_rows,
            ["1.35in", "4.1in"],
            "REPcc Prefix Rules",
        ),
        rep_execution_sequence(repeat),
    ]
    observed_rows = rep_observed_rows(repeat)
    if observed_rows:
        parts.append(latex_longtable(["Mnemonic", "Observed Value", "REPFLAGS Rule"], observed_rows, ["0.85in", "1.95in", "2.65in"], "REPcc Observed Values"))
    parts.append(render_latex_template("repcc_behavior_examples.tex"))
    return "\n".join(parts)


def repg_prefix_section(spec: dict[str, Any]) -> str:
    prefix = next(
        (
            candidate
            for candidate in spec.get("prefixes", {}).get("prefixes", []) or []
            if isinstance(candidate, dict) and candidate.get("name") == "REPG"
        ),
        {},
    )
    if not prefix:
        return ""
    return render_latex_template("repg_prefix.tex")


def encoding_overview_section(plan: dict[str, Any]) -> str:
    solver = plan.get("solver", plan)
    items = allocation_items(plan)
    sample_ids = ("MOV.EA_TO_D", "MOV.D_TO_EA", "Jcc.IMM")
    samples = []
    for prefix in sample_ids:
        item = next((candidate for candidate in items if str(candidate.get("id", "")).startswith(prefix)), None)
        if item:
            fields = line_fields(item)
            samples.append((form_label(item, fields), encoding_pattern_tokens(item, fields), line_syntax_text(item, fields)))

    parts = [
        "The first instruction word contains a four-bit prefix/length area and a twelve-bit primary payload. "
        "Compact instructions place operand fields directly in this primary payload when the field set fits. "
        "Extended instructions use a primary root and a following descriptor/opcode word, with more payload words added only when needed.",
        primary_word_figure(),
    ]
    if samples:
        parts.append(r"\subsection{Representative Encodings}")
        for name, tokens, syntax in samples:
            parts.append(rf"\Needspace{{1.6in}}\noindent\textbf{{{tex_escape(name)}}}: {tex_code(syntax)}")
            parts.append(bit_diagram(tokens, f"Encoding layout for {syntax}", [f"word {index}" for index in range(len(tokens))], listed=True))
    return "\n".join(parts)


def execution_model_section(spec: dict[str, Any]) -> str:
    instructions = spec.get("instructions") or {}
    semantics = instructions.get("operation_semantics") or {}
    defaults = semantics.get("defaults") or {}
    notation = semantics.get("notation") or {}
    syntax_policy = semantics.get("syntax_policy") or {}
    groups = semantics.get("groups") or {}
    parts = [
        "This section defines the common execution contract used by the instruction descriptions. "
        "An individual instruction may add stricter rules, but it does not silently replace the rules below. "
        "The purpose of this section is to make operand evaluation, side effects, repetition, and status updates readable before the per-instruction pages.",
        r"\subsection{Instruction Boundary and Default Execution Rules}",
        "The instruction boundary is fixed by word 0 before operand evaluation begins. "
        "An implementation may reject an instruction before any architectural state is changed if the encoded length cannot contain the selected form.",
    ]
    default_rows = execution_default_rows(defaults)
    if default_rows:
        parts.append(latex_longtable(["Topic", "Architectural Rule"], default_rows, ["1.45in", "4.0in"], "Execution Defaults"))
    suffix_rows = condition_suffix_rows(syntax_policy)
    if suffix_rows:
        parts.extend(
            [
                r"\subsection{Mnemonic Suffix Rules}",
                "Conditional mnemonic forms use the condition names listed in the Condition Codes section.",
                latex_longtable(["Rule", "Value"], suffix_rows, ["1.55in", "3.9in"], "Conditional Mnemonic Suffix Rules"),
            ]
        )
    if notation:
        parts.extend(
            [
                r"\subsection{Operand and Status Notation}",
                "The generated operation fields use compact notation. "
                "The following terms define when an operand is only addressed, when it is read, and which status register is affected.",
                latex_longtable(
                    ["Term", "Meaning"],
                    [[tex_escape(semantic_label(str(key))), semantic_cell(value)] for key, value in notation.items()],
                    ["1.45in", "4.0in"],
                    "Semantic Notation",
                ),
            ]
        )
    shared_block = shared_execution_block(groups)
    if shared_block:
        parts.extend(
            [
                r"\subsection{Shared Side-Effect Rules}",
                "These rows summarize execution rules that apply to whole instruction families. "
                "The instruction descriptions list exact forms and operands; this block records the common side-effect model.",
                shared_block,
            ]
        )
    return "\n".join(parts)


def repeat_counter_encoding_rows(repeat: dict[str, Any]) -> list[list[str]]:
    encoding = repeat.get("counter_encoding") or {}
    if not isinstance(encoding, dict):
        return []
    interpretation = encoding.get("interpretation", "signed_twos_complement")
    value_bits = encoding.get("value_bits")
    if not value_bits:
        value_bits = encoding.get("counter_bits", "63..0")
    index_value = encoding.get("index_value") or {}
    if isinstance(index_value, dict):
        index_text = "; ".join(f"{readable_text(key)}: {readable_text(value)}" for key, value in index_value.items())
    else:
        index_text = readable_text(index_value)
    bits_text = str(value_bits)
    bits_text = f"bits {bits_text}"
    rows = [
        [
            tex_escape("Counter encoding"),
            tex_escape(f"{rep_rule_text(interpretation)}; {bits_text}"),
        ],
        [tex_escape("Zero test"), tex_escape(rep_rule_text(encoding.get("zero_rule", "signed_zero_means_no_iteration")))],
        [tex_escape("REP index value"), tex_escape(index_text)],
    ]
    update = (
        encoding.get("update_after_condition_true_iteration")
        or encoding.get("update_after_successful_iteration")
        or encoding.get("update_after_successful_group_iteration")
    )
    if update:
        rows.append([tex_escape("Condition-true update"), tex_escape(rep_rule_text(update))])
    false_rule = encoding.get("condition_false_iteration_counter_rule")
    if false_rule:
        rows.append([tex_escape("Condition-false update"), tex_escape(rep_rule_text(false_rule))])
    completion = encoding.get("completion_rule")
    if completion:
        rows.append([tex_escape("Completion"), tex_escape(rep_rule_text(completion))])
    restart = encoding.get("fault_restart_rule")
    if restart:
        rows.append([tex_escape("Fault restart state"), tex_escape(rep_rule_text(restart))])
    return rows


def rep_rule_text(value: Any) -> str:
    mappings = {
        "signed_twos_complement": "signed two's-complement",
        "signed_zero_means_no_iteration": "signed zero means no iteration",
        "toward_zero": "positive counters decrement; negative counters increment toward zero",
        "move_signed_counter_one_step_toward_zero": "positive counters decrement; negative counters increment toward zero",
        "counter_not_updated": "counter is not updated",
        "zero_or_condition_false": "counter is zero or the REP condition is false",
        "counter_zero_or_condition_false": "counter is zero or the REP condition is false",
        "preserve_remaining_signed_count": "preserve remaining signed count",
        "pre_update": "architectural counter value before iteration update",
        "architectural_counter_value_before_iteration_update": "architectural counter value before iteration update",
        "pre_update_signed": "architectural signed counter before iteration update",
        "architectural_signed_counter_before_iteration_update": "architectural signed counter before iteration update",
        "condition_false_commits_body": "condition-false terminating iteration commits the body and leaves the counter unchanged",
        "last_completed_body": "body instruction rules apply to the last completed iteration",
        "after_group_completion_only": "counter is updated only after the whole group iteration completes",
        "prior_group_instructions_commit": "completed iterations and completed prior group instructions commit",
        "completed_iterations_and_prior_group_instructions": "completed iterations and completed prior group instructions commit",
        "completed_group_prefix": "successful iterations and completed group instructions only commit",
        "last_completed_group_instruction": "grouped instruction rules apply to the last completed group instruction",
        "signed_toward_zero": "signed counter moves toward zero",
        "final_counter_zero": "final counter is written as zero",
    }
    text = str(value)
    return mappings.get(text, readable_text(text))


def execution_default_rows(defaults: dict[str, Any]) -> list[list[str]]:
    labels = {
        "overlong_encoding": "Overlong Encoding",
        "undersized_encoding": "Undersized Encoding",
        "memory_memory": "Memory-Memory Operands",
        "unmentioned_flags": "Unmentioned FLAGS/FFLAGS",
        "operand_evaluation_order": "Operand Evaluation Order",
    }
    rows: list[list[str]] = [
        [
            tex_escape("Instruction boundary"),
            tex_escape("word 0 length selects the instruction boundary; prefixes and extension words never extend it implicitly"),
        ],
        [
            tex_escape("Operand evaluation"),
            tex_escape("operands are decoded in instruction order; source reads complete before the final destination write unless an atomic form says otherwise"),
        ],
        [
            tex_escape("Effective address"),
            tex_escape("EA calculation may produce an address without reading memory; memory is read only when the operation needs the operand value"),
        ],
    ]
    meanings = {
        "overlong_encoding": "extra trailing words within the encoded length are padding payload",
        "undersized_encoding": "the encoded length must contain all required opcode, descriptor, immediate, displacement, and prefix words",
        "memory_memory": "memory-memory operands are rejected unless the operation explicitly allows them",
        "unmentioned_flags": "status bits not named by the instruction remain unchanged",
        "operand_evaluation_order": "the generated operand order is the architectural operand evaluation order",
    }
    for key, value in defaults.items():
        value_text = readable_text(value)
        meaning = meanings.get(str(key))
        if meaning:
            text = f"{value_text}; {meaning}"
        else:
            text = value_text
        rows.append([tex_escape(labels.get(str(key), semantic_label(str(key)))), tex_escape(text)])
    return rows


def condition_suffix_rows(policy: dict[str, Any]) -> list[list[str]]:
    condition = policy.get("condition_code") if isinstance(policy, dict) else None
    if not isinstance(condition, dict):
        return []
    rows: list[list[str]] = []
    for key in ("placement",):
        if key in condition:
            rows.append([tex_escape(semantic_label(key)), tex_escape(readable_text(condition[key]))])
    applies = condition.get("applies_to")
    if applies:
        rows.append([tex_escape("Applies To"), tex_table_value(applies)])
    return rows


def semantic_cell(value: Any) -> str:
    if isinstance(value, dict):
        lines = [f"{semantic_label(str(key))}: {readable_text(item)}" for key, item in value.items()]
        return tex_multiline(lines)
    if isinstance(value, list):
        return tex_multiline([readable_text(item) for item in value])
    return tex_escape(readable_text(value))


def semantic_label(key: str) -> str:
    replacements = {
        "EA": "EA",
        "ZNCV": "ZNCV",
        "NV": "NV",
        "DZ": "DZ",
        "OF": "OF",
        "UF": "UF",
        "NX": "NX",
        "FP": "FP",
        "FPU": "FPU",
        "FFLAGS": "FFLAGS",
        "FLAGS": "FLAGS",
        "TLB": "TLB",
        "CR": "CR",
        "CS": "CS",
        "PC": "PC",
        "REPFLAGS": "REPFLAGS",
    }
    words: list[str] = []
    for raw in key.replace("-", "_").replace(".", "_").split("_"):
        if not raw:
            continue
        upper = raw.upper()
        words.append(replacements.get(upper, raw.title()))
    return " ".join(words)


def shared_execution_block(groups: dict[str, Any]) -> str:
    entries = shared_execution_entries(groups)
    if not entries:
        return ""
    out: list[str] = []
    for label, lines in entries:
        out.append(r"\Needspace{0.55in}")
        out.append(rf"\noindent\textbf{{{tex_escape(label)}}}\par")
        out.append(r"\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=1pt]")
        out.extend(rf"\item {tex_escape(line)}" for line in lines)
        out.append(r"\end{itemize}")
    return "\n".join(out)


def shared_execution_entries(groups: dict[str, Any]) -> list[tuple[str, list[str]]]:
    if not isinstance(groups, dict):
        return []
    specs = [
        ("integer_alu", "Integer ALU", ("memory", "flags", "state_register_forms")),
        ("integer_compare", "Compare/Test", ("memory", "flags_by_mnemonic", "repeat_observed_value_by_mnemonic")),
        ("integer_extend", "Extension", ("memory", "source_sizes_by_destination", "flags")),
        ("data_movement", "Data Movement", ("memory_by_mnemonic", "state_registers", "flags")),
        ("control_flow", "Control Transfer", ("long_transfer_operands", "atomic_cs_pc_commit", "flags")),
        ("atomics", "Atomics", ("atomic", "memory")),
        ("system_registers", "Control Registers", ("privilege_by_mnemonic", "flags")),
        ("tlb_context", "TLB and Context", ("privilege",)),
        ("cache", "Cache", ("privilege_by_mnemonic", "flags")),
        ("fpu_move_compare", "Floating-Point Move/Compare", ("fp_flags_by_mnemonic",)),
        ("fpu_arithmetic", "Floating-Point Arithmetic", ("fp_flags_by_mnemonic",)),
        ("fpu_transcendental", "Floating-Point Transcendental", ("implementation", "fp_flags_by_mnemonic")),
    ]
    entries: list[tuple[str, list[str]]] = []
    for group_name, label, keys in specs:
        body = groups.get(group_name)
        if not isinstance(body, dict):
            continue
        lines: list[str] = []
        for key in keys:
            if key not in body:
                continue
            value = body[key]
            if key.endswith("_by_mnemonic") and isinstance(value, dict):
                lines.append(f"{shared_rule_label(key)}: varies by mnemonic")
            elif isinstance(value, dict):
                lines.extend(shared_dict_lines(key, value))
            elif key == "atomic" and value is True:
                lines.append("Atomic read-modify-write operation")
            elif key == "atomic_cs_pc_commit":
                lines.append(f"CS/PC commit is atomic for: {readable_text(value)}")
            else:
                lines.append(f"{shared_rule_label(key)}: {readable_text(value)}")
        if lines:
            entries.append((label, lines))
    return entries


def shared_rule_label(key: str) -> str:
    labels = {
        "flags": "FLAGS",
        "flags_by_mnemonic": "FLAGS",
        "fp_flags_by_mnemonic": "FFLAGS",
        "memory": "Memory operands",
        "memory_by_mnemonic": "Memory operands",
        "privilege": "Privilege",
        "privilege_by_mnemonic": "Privilege",
        "implementation": "Implementation",
        "long_transfer_operands": "Long transfer operands",
        "source_sizes_by_destination": "Source sizes",
        "state_register_forms": "State-register forms",
        "state_registers": "State-register operands",
        "repeat_observed_value_by_mnemonic": "REP observed value",
    }
    return labels.get(key, semantic_label(key))


def shared_dict_lines(key: str, value: dict[str, Any]) -> list[str]:
    if key.endswith("_by_mnemonic"):
        return [f"{shared_rule_label(key)}: varies by mnemonic"]
    if key == "source_sizes_by_destination":
        return [f"Source sizes for {subkey} destination: {readable_text(subvalue)}" for subkey, subvalue in value.items()]
    if key == "state_register_forms":
        return [f"{subkey} state-register form: {readable_text(subvalue)}" for subkey, subvalue in value.items()]
    if key == "state_registers":
        return [f"{subkey} state-register operands: {readable_text(subvalue)}" for subkey, subvalue in value.items()]
    if len(value) > 4:
        return [f"{shared_rule_label(key)}: listed per mnemonic"]
    return [f"{shared_rule_label(key)} {subkey}: {readable_text(subvalue)}" for subkey, subvalue in value.items()]


def rep_execution_sequence(repeat: dict[str, Any]) -> str:
    indexed = repeat.get("indexed_ea_counter_use") or {}
    example = indexed.get("example") if isinstance(indexed, dict) else None
    encoding = repeat.get("counter_encoding") or {}
    interpretation = encoding.get("interpretation") if isinstance(encoding, dict) else None
    value_bits = encoding.get("value_bits", "63..0") if isinstance(encoding, dict) else "63..0"
    counter_text = rep_rule_text(interpretation or "signed_twos_complement")
    lines = [
        f"Each iteration reads the selected D register as a {counter_text} counter using bits {value_bits}.",
        "If the counter is zero, the prefixed instruction performs no iteration.",
        "Indexed effective-address evaluation uses the ordinary architectural D-register value before the iteration update.",
        "The repeated instruction observes a temporary value selected by mnemonic; REPFLAGS are computed from that observed value.",
        "The REP condition is tested against REPFLAGS, not against the architectural FLAGS value from before the instruction.",
        "If the REP condition is true, a positive counter is decremented and a negative counter is incremented, so the counter moves one step toward zero and repetition may continue.",
        "If the REP condition is false, the terminating instruction body's ordinary side effects remain committed but the counter is not updated.",
        "If a fault occurs, earlier completed iterations remain committed and the remaining signed count is restartable by software policy.",
        "The body instruction defines the architectural FLAGS value after the last completed iteration.",
    ]
    if isinstance(indexed, dict) and indexed.get("allowed"):
        counter_value = indexed.get("counter_value", "before_iteration_decrement")
        lines.append(f"Indexed effective addresses may use the counter value as the {rep_rule_text(counter_value)}.")
    out = [r"\begin{itemize}"]
    out.extend(rf"\item {tex_escape(line)}" for line in lines)
    out.append(r"\end{itemize}")
    if example:
        out.append(r"\noindent Example:\par")
        out.append(r"\begingroup\small\ttfamily")
        out.append(r"\begin{tabularx}{\linewidth}{@{}X@{}}")
        for line in code_example_lines(str(example)):
            cell = tex_escape(line)
            if line.lstrip().startswith("["):
                cell = r"\relax " + cell
            out.append(cell + r"\tabularnewline")
        out.append(r"\end{tabularx}")
        out.append(r"\endgroup")
    return "\n".join(out)


def code_example_lines(example: str) -> list[str]:
    if "], [" in example:
        first, second = example.split("], [", 1)
        return [first + "],", "    [" + second]
    if len(example) <= 72:
        return [example]
    midpoint = len(example) // 2
    comma = example.find(", ", midpoint)
    if comma > 0:
        return [example[: comma + 1], "    " + example[comma + 2 :]]
    return [example]


def rep_observed_rows(repeat: dict[str, Any]) -> list[list[str]]:
    observed = repeat.get("observed_value_by_mnemonic") or {}
    repflags = repeat.get("repflags_by_mnemonic") or {}
    if not isinstance(observed, dict):
        return []
    rows: list[list[str]] = []
    for mnemonic in sorted(observed):
        rows.append(
            [
                tex_code(mnemonic),
                tex_escape(readable_text(observed.get(mnemonic, "-"))),
                tex_escape(repflags_rule_text(repflags.get(mnemonic, "-") if isinstance(repflags, dict) else "-")),
            ]
        )
    return rows


def repflags_rule_text(value: Any) -> str:
    mappings = {
        "flags_logic_observed_value": "set Z/N from observed value and clear C/V",
        "flags_sub_rhs_lhs": "compute subtract flags from rhs - lhs",
    }
    text = str(value)
    return mappings.get(text, readable_text(text))



def render_manual(plan: dict[str, Any], spec: dict[str, Any], lengths: dict[tuple[str, str], tuple[int, int]]) -> str:
    items = allocation_items(plan)
    items_by_mnemonic: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        items_by_mnemonic.setdefault(str(item.get("mnemonic", item.get("id", ""))), []).append(item)

    records = semantic_records(spec)
    operations = operation_records(spec)
    aliases = aliases_by_mnemonic(spec, items)
    docs = instruction_docs(spec)
    mnemonics = sorted(set(records) | set(operations) | set(items_by_mnemonic) | set(aliases))
    fpu_set = fpu_mnemonics(spec, records, operations, items_by_mnemonic)
    general_mnemonics = [mnemonic for mnemonic in mnemonics if mnemonic not in fpu_set]
    fpu_mnemonic_list = [mnemonic for mnemonic in mnemonics if mnemonic in fpu_set]

    parts = [
        document_preamble(),
        title_page(plan, len(mnemonics), len(items)),
        overview_sections(spec, plan, len(mnemonics), len(items)),
        top_section("Instruction Set Summary"),
        instruction_set_summary_by_class_section(spec, mnemonics, records, operations, items_by_mnemonic),
        top_section("Condition Code Computation"),
        condition_code_computation_section(),
    ]
    parts.extend(instruction_reference_sections("General Instructions", general_mnemonics, records, operations, items_by_mnemonic, aliases, lengths, docs))
    parts.extend(instruction_reference_sections("Floating-Point Instructions", fpu_mnemonic_list, records, operations, items_by_mnemonic, aliases, lengths, docs))
    parts.append(top_section("C Library Instruction Examples"))
    parts.append(c_library_instruction_examples_section())
    parts.append(top_section("Opcode / Instruction Format Summary Appendix"))
    parts.append(opcode_instruction_format_summary_section(plan))
    parts.append(document_end())
    return "\n".join(parts)


def slugify(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return text.strip("-")


def preview_header(title: str) -> str:
    return "\n".join(
        [
            r"\thispagestyle{empty}",
            r"\begin{center}",
            rf"{{\Large\bfseries {tex_escape(MANUAL_TITLE)}}}\\[4pt]",
            rf"{{\large {tex_escape(title)} Preview}}",
            r"\end{center}",
            r"\vspace{0.25in}",
        ]
    )


def preview_document(title: str, body: str) -> str:
    return "\n".join([document_preamble(), preview_header(title), body, document_end()])


def manual_preview_sections(
    plan: dict[str, Any],
    spec: dict[str, Any],
    lengths: dict[tuple[str, str], tuple[int, int]],
) -> list[tuple[str, str, str]]:
    items = allocation_items(plan)
    items_by_mnemonic: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        items_by_mnemonic.setdefault(str(item.get("mnemonic", item.get("id", ""))), []).append(item)

    records = semantic_records(spec)
    operations = operation_records(spec)
    aliases = aliases_by_mnemonic(spec, items)
    docs = instruction_docs(spec)
    mnemonics = sorted(set(records) | set(operations) | set(items_by_mnemonic) | set(aliases))
    fpu_set = fpu_mnemonics(spec, records, operations, items_by_mnemonic)
    general_mnemonics = [mnemonic for mnemonic in mnemonics if mnemonic not in fpu_set]
    fpu_mnemonic_list = [mnemonic for mnemonic in mnemonics if mnemonic in fpu_set]

    entries: list[tuple[str, str, str]] = []

    def add(title: str, body: str) -> None:
        entries.append((slugify(title), title, body))

    add("Overview", architecture_overview_section(spec, plan, len(mnemonics), len(items)))
    add("Terminology", "\n".join([top_section("Terminology"), terminology_section(spec)]))
    add("Programming Model", "\n".join([top_section("Programming Model"), register_tables(spec)]))
    add("CPUID Feature Discovery", "\n".join([top_section("CPUID Feature Discovery"), cpuid_feature_discovery_section(spec)]))
    add("Data Formats", "\n".join([top_section("Data Formats"), data_format_section()]))
    add("Condition Codes", "\n".join([top_section("Condition Codes"), condition_table(spec)]))
    add("Prefixes", "\n".join([top_section("Prefixes"), prefix_table(spec)]))
    add("Effective Addressing Modes", "\n".join([top_section("Effective Addressing Modes"), ea_table(spec)]))
    add("Memory Address Translation", "\n".join([top_section("Memory Address Translation"), memory_address_translation_section(spec)]))
    add("Memory Model", "\n".join([top_section("Memory Model"), memory_model_section()]))
    add(
        "Supervisor / Privileged Programming Model",
        "\n".join([top_section("Supervisor / Privileged Programming Model"), privileged_programming_model_section(spec)]),
    )
    add("Exception Processing Reference", "\n".join([top_section("Exception Processing Reference"), interrupt_model_section(spec)]))
    add("Instruction Word Formats", "\n".join([top_section("Instruction Word Formats"), encoding_overview_section(plan)]))
    add("Instruction Execution Model", "\n".join([top_section("Instruction Execution Model"), execution_model_section(spec)]))
    add("Streaming Execution Model", "\n".join([top_section("Streaming Execution Model"), streaming_execution_model_section()]))
    add(
        "Instruction Set Summary",
        "\n".join(
            [
                top_section("Instruction Set Summary"),
                instruction_set_summary_by_class_section(spec, mnemonics, records, operations, items_by_mnemonic),
            ]
        ),
    )
    add("Condition Code Computation", "\n".join([top_section("Condition Code Computation"), condition_code_computation_section()]))
    add(
        "General Instructions Summary",
        "\n".join(
            [
                top_section("General Instructions Summary"),
                instruction_summary(
                    general_mnemonics,
                    records,
                    operations,
                    items_by_mnemonic,
                    docs,
                    "Table 9-1. General Instructions Summary",
                ),
            ]
        ),
    )
    add(
        "General Instructions Descriptions",
        "\n".join(
            [
                top_section("General Instructions Descriptions"),
                instruction_description_intro_section(),
            ]
            + [
                render_instruction(
                    mnemonic,
                    records.get(mnemonic, []),
                    operations.get(mnemonic, []),
                    items_by_mnemonic.get(mnemonic, []),
                    aliases.get(mnemonic, []),
                    lengths,
                    docs,
                )
                for mnemonic in general_mnemonics
            ]
        ),
    )
    add(
        "Floating-Point Instructions Summary",
        "\n".join(
            [
                top_section("Floating-Point Instructions Summary"),
                instruction_summary(
                    fpu_mnemonic_list,
                    records,
                    operations,
                    items_by_mnemonic,
                    docs,
                    "Table 10-1. Floating-Point Instructions Summary",
                ),
            ]
        ),
    )
    add(
        "Floating-Point Instructions Descriptions",
        "\n".join(
            [top_section("Floating-Point Instructions Descriptions")]
            + [
                render_instruction(
                    mnemonic,
                    records.get(mnemonic, []),
                    operations.get(mnemonic, []),
                    items_by_mnemonic.get(mnemonic, []),
                    aliases.get(mnemonic, []),
                    lengths,
                    docs,
                )
                for mnemonic in fpu_mnemonic_list
            ]
        ),
    )
    add("C Library Instruction Examples", "\n".join([top_section("C Library Instruction Examples"), c_library_instruction_examples_section()]))
    add(
        "Opcode / Instruction Format Summary Appendix",
        "\n".join([top_section("Opcode / Instruction Format Summary Appendix"), opcode_instruction_format_summary_section(plan)]),
    )
    return entries


def select_preview_section(sections: list[tuple[str, str, str]], requested: str) -> tuple[str, str, str]:
    key = slugify(requested)
    exact = [section for section in sections if section[0] == key or section[1].lower() == requested.lower()]
    if len(exact) == 1:
        return exact[0]
    partial = [section for section in sections if key and (key in section[0] or requested.lower() in section[1].lower())]
    if len(partial) == 1:
        return partial[0]
    available = "\n".join(f"  {slug}: {title}" for slug, title, _ in sections)
    if not exact and not partial:
        raise ValueError(f"unknown preview section {requested!r}. Available sections:\n{available}")
    matches = "\n".join(f"  {slug}: {title}" for slug, title, _ in partial)
    raise ValueError(f"ambiguous preview section {requested!r}. Matching sections:\n{matches}\n\nAvailable sections:\n{available}")


def render_manual_preview(
    plan: dict[str, Any],
    spec: dict[str, Any],
    lengths: dict[tuple[str, str], tuple[int, int]],
    requested: str,
) -> str:
    sections = manual_preview_sections(plan, spec, lengths)
    selected = select_preview_section(sections, requested)
    index = sections.index(selected)
    _, title, body = selected
    body = f"\\setcounter{{section}}{{{index}}}\n" + body
    return preview_document(title, body)



def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("--allocation", default="build/generated/allocation_plan.json")
    parser.add_argument("--preview-section", help="render only one top-level manual section by title or slug")
    parser.add_argument("--list-preview-sections", action="store_true", help="list section slugs available for --preview-section")
    parser.add_argument("-o", "--output", default="build/generated/isa_reference.tex")
    args = parser.parse_args(argv)

    spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1

    plan = load_allocation(Path(args.allocation))
    from gen_instruction_tables import entry_lengths

    lengths = entry_lengths(entries)
    if args.list_preview_sections:
        for slug, title, _ in manual_preview_sections(plan, spec, lengths):
            print(f"{slug}\t{title}")
        return 0

    try:
        text = (
            render_manual_preview(plan, spec, lengths, args.preview_section)
            if args.preview_section
            else render_manual(plan, spec, lengths)
        )
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    if args.output == "-":
        sys.stdout.write(text)
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
