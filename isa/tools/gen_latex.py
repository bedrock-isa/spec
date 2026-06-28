#!/usr/bin/env python3
"""Generate a LaTeX ISA reference manual from the declarative ISA spec."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import argparse
import re
import sys

sys.dont_write_bytecode = True

from gen_instruction_specs import (
    allocation_items,
    mnemonic_aliases,
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
    set_active_spec as set_instruction_table_spec,
    syntax_text,
)
from isa_spec import load_and_validate, print_result
from spec_model.encoding import (
    named_value_set,
    special_register_encoding,
    special_register_layout,
)
from latex_builder.diagrams import (
    bit_diagram,
    bit_field_figure,
    bit_index_labels,
    paging_mode_figure,
    register_model_figure,
    stack_frame_figure,
    supervisor_stack_frame,
)


from latex_builder.common import (
    ARCH_NAME,
    LatexComponent,
    LatexDocumentEnd,
    LatexDocumentPreamble,
    LatexHiddenTopSection,
    LatexSequence,
    LatexTitlePage,
    LatexTopSection,
    MANUAL_TITLE,
    compact_text,
    instruction_docs,
    latex_longtable,
    latex_tabular,
    load_allocation,
    memory_rule_text,
    mdash_join,
    normalize_text,
    pretty_key,
    readable_text,
    render_latex_template,
    tex_code,
    tex_escape,
    tex_multiline,
    tex_multiline_latex,
    tex_table_value,
    top_section,
)
from latex_builder.effective_address import ea_table
from latex_builder.instruction_reference import (
    c_library_instruction_examples_section,
    condition_code_computation_section,
    form_label,
    fpu_mnemonics,
    instruction_description_intro_section,
    instruction_reference_sections,
    instruction_set_summary_by_class_section,
    instruction_summary,
    render_instruction,
    runtime_instruction_examples_section,
    save_area_format_reference_sections,
)

SEPARATE_INSTRUCTION_GROUPS = [
    ("Virtualization Acceleration Instructions", {"virtualization_acceleration"}),
    ("Floating-Point Transcendental Instructions", {"fpu_transcendental"}),
]


@dataclass(frozen=True)
class ManualRenderContext:
    plan: dict[str, Any]
    spec: dict[str, Any]
    lengths: dict[tuple[str, str], tuple[int, int]]
    items: list[dict[str, Any]]
    mnemonic_items: dict[str, list[dict[str, Any]]]
    records: dict[str, list[dict[str, Any]]]
    operations: dict[str, list[dict[str, Any]]]
    aliases: dict[str, list[str]]
    docs: dict[str, dict[str, Any]]
    mnemonics: list[str]
    reference_groups: list[tuple[str, list[str]]]

    @classmethod
    def build(
        cls,
        plan: dict[str, Any],
        spec: dict[str, Any],
        lengths: dict[tuple[str, str], tuple[int, int]],
    ) -> ManualRenderContext:
        set_instruction_table_spec(spec)
        items = allocation_items(plan)
        mnemonic_items: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            mnemonic_items.setdefault(str(item.get("mnemonic", item.get("id", ""))), []).append(item)

        records = semantic_records(spec)
        operations = operation_records(spec)
        aliases = mnemonic_aliases(spec, items)
        docs = instruction_docs(spec)
        mnemonics = sorted(set(records) | set(operations) | set(mnemonic_items) | set(aliases))
        reference_groups = instruction_reference_groups(spec, mnemonics, records, operations, mnemonic_items)
        return cls(
            plan=plan,
            spec=spec,
            lengths=lengths,
            items=items,
            mnemonic_items=mnemonic_items,
            records=records,
            operations=operations,
            aliases=aliases,
            docs=docs,
            mnemonics=mnemonics,
            reference_groups=reference_groups,
        )


@dataclass(frozen=True)
class ManualPreviewSection:
    slug: str
    title: str
    body: str

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.slug, self.title, self.body)


@dataclass(frozen=True)
class PreviewHeader(LatexComponent):
    title: str

    def render(self) -> str:
        return "\n".join(
            [
                r"\thispagestyle{empty}",
                r"\begin{center}",
                rf"{{\Large\bfseries {tex_escape(MANUAL_TITLE)}}}\\[4pt]",
                rf"{{\large {tex_escape(self.title)} Preview}}",
                r"\end{center}",
                r"\vspace{0.25in}",
            ]
        )


@dataclass(frozen=True)
class ManualDocument(LatexComponent):
    context: ManualRenderContext

    def render(self) -> str:
        context = self.context
        parts: list[Any] = [
            LatexDocumentPreamble(),
            LatexTitlePage(context.plan, len(context.mnemonics), len(context.items)),
            overview_sections(context.spec, context.plan, len(context.mnemonics), len(context.items)),
            LatexTopSection("Instruction Set Summary"),
            instruction_set_summary_by_class_section(
                context.spec,
                context.mnemonics,
                context.records,
                context.operations,
                context.mnemonic_items,
            ),
            LatexTopSection("Condition Code Computation"),
            condition_code_computation_section(),
        ]
        for title, group_mnemonics in context.reference_groups:
            parts.extend(
                instruction_reference_sections(
                    context.spec,
                    title,
                    group_mnemonics,
                    context.records,
                    context.operations,
                    context.mnemonic_items,
                    context.aliases,
                    context.lengths,
                    context.docs,
                )
            )
        parts.extend(
            [
                LatexTopSection("C Library Instruction Examples"),
                c_library_instruction_examples_section(),
                LatexTopSection("Runtime Instruction Examples"),
                runtime_instruction_examples_section(),
                LatexDocumentEnd(),
            ]
        )
        return LatexSequence(parts).render()


@dataclass(frozen=True)
class ManualPreviewIndex:
    context: ManualRenderContext

    def sections(self) -> list[ManualPreviewSection]:
        context = self.context
        entries: list[ManualPreviewSection] = []

        def add(title: str, body: str) -> None:
            entries.append(ManualPreviewSection(slugify(title), title, body))

        add("Overview", architecture_overview_section(context.spec, context.plan, len(context.mnemonics), len(context.items)))
        add("Terminology", LatexSequence([LatexTopSection("Terminology"), terminology_section(context.spec)]).render())
        add("Reserved and Compatibility Rules", compatibility_rules_section(context.spec))
        add("Programming Model", LatexSequence([LatexTopSection("Programming Model"), register_tables(context.spec)]).render())
        add(
            "CPUID Feature Discovery",
            LatexSequence([LatexTopSection("CPUID Feature Discovery"), cpuid_feature_discovery_section(context.spec)]).render(),
        )
        save_area_section = save_area_reference_section(context.spec)
        if save_area_section:
            add("SAVE/RESTORE Processor-State Save Area", save_area_section)
        add("Data Formats", LatexSequence([LatexTopSection("Data Formats"), data_format_section()]).render())
        add("Condition Codes", LatexSequence([LatexTopSection("Condition Codes"), condition_table(context.spec)]).render())
        add("Prefixes", LatexSequence([LatexTopSection("Prefixes"), prefix_table(context.spec)]).render())
        add("Effective Addressing Modes", LatexSequence([LatexTopSection("Effective Addressing Modes"), ea_table(context.spec)]).render())
        add(
            "Memory Address Translation",
            LatexSequence([LatexTopSection("Memory Address Translation"), memory_address_translation_section(context.spec)]).render(),
        )
        add("Memory Model", LatexSequence([LatexTopSection("Memory Model"), memory_model_section(context.spec)]).render())
        add(
            "Supervisor / Privileged Programming Model",
            LatexSequence(
                [
                    LatexTopSection("Supervisor / Privileged Programming Model"),
                    privileged_programming_model_section(context.spec),
                ]
            ).render(),
        )
        add(
            "Exception Processing Reference",
            LatexSequence([LatexTopSection("Exception Processing Reference"), interrupt_model_section(context.spec)]).render(),
        )
        add("Instruction Word Formats", LatexSequence([LatexTopSection("Instruction Word Formats"), encoding_overview_section(context.plan)]).render())
        add("Instruction Execution Model", LatexSequence([LatexTopSection("Instruction Execution Model"), execution_model_section(context.spec)]).render())
        add("Streaming Execution Model", LatexSequence([LatexTopSection("Streaming Execution Model"), streaming_execution_model_section()]).render())
        add(
            "Instruction Set Summary",
            LatexSequence(
                [
                    LatexTopSection("Instruction Set Summary"),
                    instruction_set_summary_by_class_section(
                        context.spec,
                        context.mnemonics,
                        context.records,
                        context.operations,
                        context.mnemonic_items,
                    ),
                ]
            ).render(),
        )
        add(
            "Condition Code Computation",
            LatexSequence([LatexTopSection("Condition Code Computation"), condition_code_computation_section()]).render(),
        )
        for title, group_mnemonics in context.reference_groups:
            add(
                f"{title} Summary",
                LatexSequence(
                    [
                        LatexTopSection(f"{title} Summary"),
                        instruction_summary(
                            group_mnemonics,
                            context.records,
                            context.operations,
                            context.mnemonic_items,
                            context.docs,
                            f"{title} Summary",
                        ),
                    ]
                ).render(),
            )
            description_intro = [instruction_description_intro_section()] if title.startswith("General") else []
            instruction_pages: list[str] = []
            if description_intro:
                instruction_pages.append(r"\clearpage")
            for index, mnemonic in enumerate(group_mnemonics):
                if index:
                    instruction_pages.append(r"\clearpage")
                instruction_pages.append(
                    render_instruction(
                        mnemonic,
                        context.records.get(mnemonic, []),
                        context.operations.get(mnemonic, []),
                        context.mnemonic_items.get(mnemonic, []),
                        context.aliases.get(mnemonic, []),
                        context.lengths,
                        context.docs,
                    )
                )
            add(
                f"{title} Descriptions",
                LatexSequence(
                    [LatexHiddenTopSection(f"{title} Descriptions")]
                    + description_intro
                    + instruction_pages
                ).render(),
            )
        add(
            "C Library Instruction Examples",
            LatexSequence([LatexTopSection("C Library Instruction Examples"), c_library_instruction_examples_section()]).render(),
        )
        add(
            "Runtime Instruction Examples",
            LatexSequence([LatexTopSection("Runtime Instruction Examples"), runtime_instruction_examples_section()]).render(),
        )
        return entries


@dataclass(frozen=True)
class ManualPreviewDocument(LatexComponent):
    context: ManualRenderContext
    requested: str

    def render(self) -> str:
        sections = ManualPreviewIndex(self.context).sections()
        selected = select_preview_section([section.as_tuple() for section in sections], self.requested)
        index = [section.as_tuple() for section in sections].index(selected)
        _slug, title, body = selected
        body = f"\\setcounter{{section}}{{{index}}}\n" + body
        return LatexSequence([LatexDocumentPreamble(), PreviewHeader(title), body, LatexDocumentEnd()]).render()



def data_format_section() -> str:
    return render_latex_template("data_formats.tex")


def memory_order_rows(spec: dict[str, Any]) -> list[list[str]]:
    body = named_value_set(spec, "memory_order")
    rows: list[list[str]] = []
    for key, selector in (("values", tex_code), ("reserved_values", tex_escape)):
        for item in body.get(key, []) or []:
            if not isinstance(item, dict):
                continue
            rows.append(
                [
                    selector(item.get("name", "")),
                    tex_code(item.get("value", "")),
                    tex_escape(item.get("description", "")),
                ]
            )
    return rows


def memory_model_section(spec: dict[str, Any]) -> str:
    return render_latex_template(
        "memory_model.tex",
        {
            "MEMORY_ORDER_TABLE": latex_longtable(
                ["Selector", "Code", "Architectural Ordering Effect"],
                memory_order_rows(spec),
                ["0.9in", "0.75in", "3.8in"],
                "Atomic Memory-Order Selectors",
            )
        },
    )


def streaming_execution_model_section() -> str:
    return render_latex_template("streaming_execution_model.tex")


def prefix_model_table(spec: dict[str, Any]) -> str:
    prefix_word = (spec.get("prefixes") or {}).get("prefix_word") or {}
    rows = (
        ("Prefix bytes", prefix_word.get("bytes_per_instruction", "-")),
        ("Fill order", prefix_word.get("fill_order", "-")),
        ("Decode order", prefix_word.get("decode_order", "-")),
        ("Unused slot encoding", prefix_word.get("unused_slot_encoding", "-")),
        ("Conflict resolution", prefix_word.get("conflict_resolution", "-")),
        ("Conflict note", prefix_word.get("conflict_note", "-")),
    )
    return latex_longtable(
        ["Property", "Spec Value"],
        [[tex_escape(label), tex_table_value(value)] for label, value in rows],
        ["1.55in", "3.95in"],
        "Prefix Word Rules",
    )


def bit_field_width(field: dict[str, Any]) -> int:
    if "bit" in field:
        return 1
    bits = field.get("bits")
    if isinstance(bits, list) and len(bits) == 2:
        return abs(int(bits[0]) - int(bits[1])) + 1
    return 0


def word0_field_rows(spec: dict[str, Any]) -> list[list[str]]:
    word0 = ((spec.get("opcodes") or {}).get("word0") or {})
    rows: list[list[str]] = []
    for key in ("prefix_present", "length_minus_one", "payload"):
        field = word0.get(key)
        if not isinstance(field, dict):
            continue
        name = str(field.get("name") or key)
        name_cell = tex_code(name) if re.fullmatch(r"[A-Za-z0-9_]+", name) else tex_escape(name)
        rows.append(
            [
                name_cell,
                tex_escape(field_bits_text(field)),
                tex_escape(field.get("description", "")),
            ]
        )
    return rows


def word0_field_table(spec: dict[str, Any]) -> str:
    return latex_longtable(
        ["Field", "Bits", "Meaning"],
        word0_field_rows(spec),
        ["1.20in", "0.65in", "3.65in"],
        "Word 0 Fields",
    )


def instruction_length_rows(spec: dict[str, Any]) -> list[list[str]]:
    opcodes = spec.get("opcodes") or {}
    length_field = ((opcodes.get("word0") or {}).get("length_minus_one") or {})
    width = bit_field_width(length_field)
    word_size = int(opcodes.get("word_size", 16))
    byte_count_exact = word_size % 8 == 0
    rows: list[list[str]] = []
    for encoded in range(1 << width):
        words = encoded + 1
        byte_text = str(words * word_size // 8) if byte_count_exact else f"{words * word_size} bits"
        rows.append([tex_code(f"{encoded:0{width}b}"), tex_escape(words), tex_escape(byte_text)])
    return rows


def instruction_length_table(spec: dict[str, Any]) -> str:
    return latex_longtable(
        ["L Field", "Total Words", "Total Bytes"],
        instruction_length_rows(spec),
        ["1.20in", "1.35in", "1.35in"],
        "Instruction Length Encoding",
    )


def architecture_overview_section(spec: dict[str, Any], plan: dict[str, Any], mnemonic_count: int, form_count: int) -> str:
    return render_latex_template(
        "architecture_overview.tex",
        {
            "ARCH_NAME": ARCH_NAME,
            "WORD0_FIELD_TABLE": word0_field_table(spec),
            "INSTRUCTION_LENGTH_TABLE": instruction_length_table(spec),
            "PREFIX_MODEL_TABLE": prefix_model_table(spec),
        },
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
        class_value = item.get("class")
        range_value = item.get("range")
        namespace = hex_text(class_value) if class_value is not None else cpuid_range_text(range_value)
        rows.append(
            [
                tex_escape(item.get("name", readable_text(key))),
                tex_code(namespace) if class_value is not None or range_value is not None else tex_escape("-"),
                tex_escape(compact_text(item.get("description", ""))),
            ]
        )
    return rows


def cpuid_class_rows(spec: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for item in cpuid_model(spec).get("classes", []) or []:
        if not isinstance(item, dict):
            continue
        rows.append(
            [
                tex_code(hex_text(item.get("class", "-"))),
                tex_escape(readable_text(item.get("name", ""))),
                tex_escape(compact_text(item.get("description", ""))),
            ]
        )
    if rows:
        return rows
    return rows


def cpuid_selector_rows(spec: dict[str, Any]) -> list[list[str]]:
    calling = cpuid_model(spec).get("calling_convention") or {}
    selector = calling.get("query_selector") if isinstance(calling, dict) else {}
    bits = selector.get("bits", []) if isinstance(selector, dict) else []
    rows: list[list[str]] = []
    for item in bits or []:
        if not isinstance(item, dict):
            continue
        if "bit" in item:
            location = str(item.get("bit"))
        else:
            bit_range = item.get("range")
            location = f"{bit_range[0]}..{bit_range[1]}" if isinstance(bit_range, list) and len(bit_range) == 2 else "-"
        rows.append(
            [
                tex_code(location),
                tex_code(str(item.get("name", ""))),
                tex_escape(compact_text(item.get("description", ""))),
            ]
        )
    return rows


def cpuid_result_entries(leaf: dict[str, Any]) -> list[dict[str, Any]]:
    results = leaf.get("results")
    if isinstance(results, list):
        return [item for item in results if isinstance(item, dict)]
    return []


def cpuid_index_sort_key(value: Any) -> tuple[int, int, str]:
    try:
        return (0, int(value), "")
    except (TypeError, ValueError):
        return (1, 0, str(value))


def cpuid_identifier_cell(value: Any, limit: int = 18) -> str:
    text = str(value)
    if len(text) <= limit:
        return tex_code(text)
    parts = text.split("_")
    if len(parts) <= 1:
        return tex_code(text)
    lines: list[str] = []
    current = parts[0]
    for part in parts[1:]:
        candidate = f"{current}_{part}"
        if len(candidate) <= limit:
            current = candidate
            continue
        lines.append(current + "_")
        current = part
    lines.append(current)
    return tex_multiline_latex([tex_code(line) for line in lines])


def latex_itemize_lines(lines: list[str]) -> str:
    if not lines:
        return ""
    body = "\n".join(r"\item " + tex_escape(line) for line in lines)
    return "\n".join([r"\begin{itemize}[leftmargin=1.4em,itemsep=1pt,topsep=2pt]\raggedright", body, r"\end{itemize}"])


def latex_itemize_latex_lines(lines: list[str]) -> str:
    if not lines:
        return ""
    body = "\n".join(r"\item " + line for line in lines)
    return "\n".join([r"\begin{itemize}[leftmargin=1.4em,itemsep=1pt,topsep=2pt]\raggedright", body, r"\end{itemize}"])


def cpuid_leaf_iter(spec: dict[str, Any]) -> list[tuple[Any, dict[str, Any], dict[str, Any]]]:
    classes = cpuid_model(spec).get("classes")
    if isinstance(classes, list) and classes:
        out: list[tuple[Any, dict[str, Any], dict[str, Any]]] = []
        for class_entry in classes:
            if not isinstance(class_entry, dict):
                continue
            class_value = class_entry.get("class", "-")
            for leaf in class_entry.get("leaves", []) or []:
                if isinstance(leaf, dict):
                    out.append((class_value, class_entry, leaf))
        return out
    return []


def cpuid_bit_location(bit: dict[str, Any]) -> str:
    if "bit" in bit:
        return str(bit.get("bit"))
    bit_range = bit.get("range")
    if isinstance(bit_range, list) and len(bit_range) == 2:
        return f"{bit_range[0]}..{bit_range[1]}"
    return "-"


CPUID_PAYLOAD_LABELS = {
    "reserved": "0",
    "MAX_STANDARD_LEAF": "MAX_LEAF",
    "ARCH_REVISION": "ARCH_REV",
    "BASE_PROFILE_ID": "PROFILE",
    "MAX_INSTRUCTION_WORDS": "INST_WORDS",
    "WORD_BITS": "WORD_BITS",
    "MAX_PREFIX_WORDS": "PFX_WORDS",
    "MAX_PREFIX_BYTES": "PFX_BYTES",
    "VENDOR_BYTES": "BYTE[7:0]",
    "MAX_EXTENSION_LEAF": "MAX_LEAF",
    "FP": "F",
    "FPTRANS": "T",
    "VIRTACCEL": "V",
    "MAX_IMPLEMENTATION_LEAF": "MAX_LEAF",
    "OUT_OF_ORDER": "O",
    "DBANK_COUNT": "BANK",
    "DBANK_SELECTOR_BITS": "SEL",
    "DBANK_TIER": "T",
    "MAX_TOPOLOGY_INDEX": "MAX_IDX",
    "TOPOLOGY_ID_BITS": "TOPO_BITS",
    "PROCESSOR_ID_BITS": "PROC_BITS",
    "HARDWARE_THREAD_COUNT": "THREADS",
    "CURRENT_PROCESSOR_ID": "PROC_ID",
    "CURRENT_TOPOLOGY_ID": "TOPO_ID",
    "LEVEL_TYPE": "TYPE",
    "LEVEL_SHIFT": "SHIFT",
    "LEVEL_WIDTH": "WIDTH",
    "UNITS_IN_PARENT": "UNITS",
    "THREADS_IN_UNIT": "THREADS",
    "SAVE_AREA_SIZE": "SAVE_SIZE",
    "SAVE_HEADER_SIZE": "HEADER",
    "SAVE_COMPONENT_COUNT": "COMPONENTS",
    "SAVE_BITMAP_WORDS": "BITMAPS",
    "COMPONENT_ID": "ID",
    "COMPONENT_FLAGS": "FLAGS",
    "COMPONENT_OFFSET": "OFFSET",
}


def cpuid_bit_bounds(bit: dict[str, Any]) -> tuple[int, int] | None:
    if "bit" in bit:
        try:
            value = int(bit.get("bit"))
        except (TypeError, ValueError):
            return None
        return (value, value)
    bit_range = bit.get("range")
    if isinstance(bit_range, list) and len(bit_range) == 2:
        try:
            low = int(bit_range[0])
            high = int(bit_range[1])
        except (TypeError, ValueError):
            return None
        return (min(low, high), max(low, high))
    return None


def cpuid_payload_label(name: Any, width: int) -> str:
    text = str(name)
    label = CPUID_PAYLOAD_LABELS.get(text, text)
    if width <= 1:
        return label[:1]
    if width <= 3 and len(label) > 2:
        return label[:2]
    if width <= 8 and len(label) > 9:
        return "".join(part[:1] for part in label.split("_") if part)[:4] or label[:4]
    return label


def cpuid_payload_fields(bits: list[Any]) -> list[tuple[str, int]]:
    ranges: list[tuple[int, int, str]] = []
    for bit in bits:
        if not isinstance(bit, dict):
            continue
        bounds = cpuid_bit_bounds(bit)
        if bounds is None:
            continue
        low, high = bounds
        if low < 0 or high > 63:
            continue
        width = high - low + 1
        ranges.append((high, low, cpuid_payload_label(bit.get("name", ""), width)))
    if not ranges:
        return []

    fields: list[tuple[str, int]] = []
    cursor = 63
    for high, low, label in sorted(ranges, key=lambda item: (-item[0], -item[1])):
        if high > cursor:
            continue
        if high < cursor:
            fields.append(("0", cursor - high))
        fields.append((label, high - low + 1))
        cursor = low - 1
    if cursor >= 0:
        fields.append(("0", cursor + 1))
    return [(label, width) for label, width in fields if width > 0]


def is_single_full_width_cpuid_payload(fields: list[tuple[str, int]], total_bits: int = 64) -> bool:
    return len(fields) == 1 and fields[0][1] == total_bits


def cpuid_leaf_rows(spec: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for class_value, _class_entry, leaf in cpuid_leaf_iter(spec):
        class_text = tex_code(hex_text(class_value))
        leaf_value = tex_code(hex_text(leaf.get("leaf", "-"), width=4))
        results = cpuid_result_entries(leaf)
        indexes = ", ".join(str(result_entry.get("index", "-")) for result_entry in sorted(results, key=lambda item: cpuid_index_sort_key(item.get("index", "")))) if results else "-"
        summary = leaf.get("summary") or leaf.get("description") or "-"
        rows.append([class_text, leaf_value, cpuid_identifier_cell(leaf.get("name", "")), tex_code(indexes), tex_escape(compact_text(summary))])
    return rows


def cpuid_leaf_detail_blocks(spec: dict[str, Any]) -> str:
    blocks: list[str] = []
    for class_value, _class_entry, leaf in cpuid_leaf_iter(spec):
        name = str(leaf.get("name", ""))
        selector_text = f"class {hex_text(class_value)}, leaf {hex_text(leaf.get('leaf', '-'), width=4)}"
        parts = [
            r"\Needspace{1.35in}",
            rf"\noindent{{\bfseries {tex_code(name)} ({tex_escape(selector_text)})}}\par",
        ]
        summary = leaf.get("summary")
        if summary:
            parts.append(tex_escape(compact_text(summary)) + r"\par")
        description = leaf.get("description")
        if description:
            description_text = compact_text(description)
            if not summary or description_text != compact_text(summary):
                parts.append(tex_escape(description_text) + r"\par")
        result_lines: list[str] = []
        for result_entry in sorted(cpuid_result_entries(leaf), key=lambda item: cpuid_index_sort_key(item.get("index", ""))):
            index = result_entry.get("index", "-")
            description_value = result_entry.get("description", result_entry.get("value", ""))
            description_text = readable_text(description_value)
            result_lines.append(f"index {index}: {description_text}")
            extraction = result_entry.get("extraction")
            if extraction:
                result_lines.append(f"index {index} extraction: {compact_text(extraction)}")
        if result_lines:
            parts.append(r"\noindent\textbf{Result Indexes:}\par")
            parts.append(latex_itemize_lines(result_lines))
        topology_level_types = leaf.get("topology_level_types")
        if isinstance(topology_level_types, dict) and topology_level_types:
            type_lines: list[str] = []
            for key, value in topology_level_types.items():
                type_lines.append(f"{key}: {readable_text(value)}")
            parts.append(r"\noindent\textbf{Topology Level Types:}\par")
            parts.append(latex_itemize_lines(type_lines))
        blocks.append("\n".join(parts))
    if not blocks:
        return ""
    return "\n".join([r"\subsection*{CPUID Leaf Details}", *blocks])


def cpuid_bit_field_leaf_blocks(spec: dict[str, Any]) -> str:
    blocks: list[str] = []
    for class_value, _class_entry, leaf in cpuid_leaf_iter(spec):
        result_blocks: list[str] = []
        leaf_name = str(leaf.get("name", ""))
        for result_entry in sorted(cpuid_result_entries(leaf), key=lambda item: cpuid_index_sort_key(item.get("index", ""))):
            bits = result_entry.get("bits")
            if not isinstance(bits, list) or not bits:
                continue
            index = str(result_entry.get("index", "-"))
            fields = cpuid_payload_fields(bits)
            rows: list[str] = []
            for bit in bits:
                if not isinstance(bit, dict):
                    continue
                location = cpuid_bit_location(bit)
                name = str(bit.get("name", ""))
                description = compact_text(bit.get("description", ""))
                if description:
                    rows.append(
                        rf"{tex_code(location)} & {cpuid_identifier_cell(name, limit=22)} & {tex_escape(description)}\\"
                    )
                    rows.append(r"\hline")
            if not rows:
                continue
            block_parts = [
                r"\Needspace{2.35in}",
                rf"\noindent\textbf{{Result index {tex_escape(index)}}}\par",
            ]
            if fields and not is_single_full_width_cpuid_payload(fields):
                block_parts.append(
                    bit_field_figure(
                        fields,
                        f"CPUID Payload: {leaf_name} index {index}",
                        "result[63:0]",
                        64,
                        top_labels=bit_index_labels(64, [63, 48, 32, 16, 0]),
                    )
                )
            block_parts.extend(
                [
                    r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.08}",
                    r"\begin{tabularx}{0.985\linewidth}{|p{0.72in}|p{1.80in}|X|}",
                    r"\hline",
                    r"\textbf{Bits} & \textbf{Field} & \textbf{Meaning}\\",
                    r"\hline",
                    *rows,
                    r"\end{tabularx}\endgroup\par\smallskip",
                ]
            )
            result_blocks.append("\n".join(block_parts))
        if not result_blocks:
            continue
        selector_text = f"class {hex_text(class_value)}, leaf {hex_text(leaf.get('leaf', '-'), width=4)}"
        parts = [
            r"\Needspace{2.35in}",
            rf"\noindent{{\bfseries {tex_code(leaf_name)} ({tex_escape(selector_text)})}}\par",
            *result_blocks,
        ]
        blocks.append("\n".join(parts))
    if not blocks:
        return ""
    return "\n".join([r"\subsection*{CPUID Bit Field Layouts}", *blocks])


def cpuid_feature_discovery_section(spec: dict[str, Any]) -> str:
    model = cpuid_model(spec)
    calling = model.get("calling_convention") or {}
    syntax = calling.get("syntax", "CPUID Dn") if isinstance(calling, dict) else "CPUID Dn"
    calling_rows = []
    if isinstance(calling, dict):
        for key in (
            "input",
            "output",
            "unsupported_class",
            "unsupported_leaf",
            "unsupported_index",
            "privilege",
            "serialization",
            "reserved_result_bits",
            "runtime_mutability",
        ):
            if key in calling:
                calling_rows.append([tex_escape(readable_text(key)), tex_escape(compact_text(calling[key]))])
    calling_table = latex_longtable(
        ["Property", "Spec Value"],
        calling_rows,
        ["1.60in", "3.85in"],
        "CPUID Calling Convention",
    ) if calling_rows else ""

    selector_rows = cpuid_selector_rows(spec)
    selector_table = ""
    if selector_rows:
        selector_table = latex_longtable(["Bits", "Field", "Meaning"], selector_rows, ["0.70in", "1.20in", "3.60in"], "CPUID Query Selector")

    policy_rows = cpuid_policy_rows(spec)
    policy_table = ""
    if policy_rows:
        policy_table = latex_longtable(["Policy", "Class", "Meaning"], policy_rows, ["1.25in", "1.15in", "3.10in"], "CPUID Discovery Policy")
    class_rows = cpuid_class_rows(spec)
    class_table = ""
    if class_rows:
        class_table = latex_longtable(["Class", "Name", "Meaning"], class_rows, ["1.15in", "1.45in", "2.90in"], "CPUID Classes")
    leaf_rows = cpuid_leaf_rows(spec)
    leaf_table = ""
    if leaf_rows:
        leaf_table = latex_longtable(["Class", "Leaf", "Name", "Indexes", "Summary"], leaf_rows, ["0.85in", "0.60in", "1.35in", "0.72in", "1.98in"], "CPUID Leaves")
    leaf_details = cpuid_leaf_detail_blocks(spec)
    bit_field_blocks = cpuid_bit_field_leaf_blocks(spec)
    return render_latex_template(
        "cpuid_feature_discovery.tex",
        {
            "SYNTAX": tex_code(syntax),
            "CALLING_CONVENTION_TABLE": calling_table,
            "SELECTOR_TABLE": selector_table,
            "POLICY_TABLE": policy_table,
            "CLASS_TABLE": class_table,
            "LEAF_TABLE": leaf_table,
            "LEAF_DETAILS": leaf_details,
            "BIT_FIELD_BLOCKS": bit_field_blocks,
        },
    )


def compatibility_rule_value(rules: dict[str, Any], path: list[str], default: Any) -> Any:
    value: Any = rules
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def compatibility_policy_rows(rules: dict[str, Any]) -> list[list[str]]:
    rows = [
        ("Reserved opcode exception", ["instruction_encoding_faults", "reserved_opcode", "exception"], "ILLEGAL_INSTRUCTION"),
        ("Reserved extension opcode exception", ["instruction_encoding_faults", "reserved_extension_opcode", "exception"], "ILLEGAL_INSTRUCTION"),
        ("Reserved EA form exception", ["instruction_encoding_faults", "reserved_effective_address_form", "exception"], "ILLEGAL_INSTRUCTION"),
        ("Unsupported optional group exception", ["instruction_encoding_faults", "unsupported_optional_instruction_group", "exception"], "ILLEGAL_INSTRUCTION"),
        ("Extension unavailable exception defined", ["instruction_encoding_faults", "extension_unavailable_exception", "defined"], False),
        ("Unassigned prefix exception", ["prefix_values", "unassigned", "exception"], "none"),
        ("Unassigned prefix behavior", ["prefix_values", "unassigned", "behavior"], "no_architectural_effect"),
        ("Unknown CPUID class result", ["cpuid", "unknown_class", "result"], "zero"),
        ("Unknown CPUID leaf result", ["cpuid", "unknown_leaf", "result"], "zero"),
        ("Unknown CPUID index result", ["cpuid", "unknown_index", "result"], "zero"),
        ("Reserved CPUID result bit software action", ["cpuid", "reserved_result_bits", "software_action"], "ignore"),
        ("CPUID privilege", ["cpuid", "privilege"], "unprivileged"),
        ("CPUID serialization", ["cpuid", "serialization"], "none"),
        ("CPUID stable after reset", ["cpuid", "runtime_mutability", "stable_after_reset"], True),
    ]
    return [
        [tex_escape(label), tex_code(compatibility_rule_value(rules, path, default))]
        for label, path, default in rows
    ]


def compatibility_rules_section(spec: dict[str, Any]) -> str:
    rules = (spec.get("semantics") or {}).get("compatibility_rules") or {}
    return render_latex_template(
        "compatibility_rules.tex",
        {
            "COMPATIBILITY_POLICY_TABLE": latex_longtable(
                ["Rule", "Spec Value"],
                compatibility_policy_rows(rules),
                ["2.35in", "2.95in"],
                "Compatibility Policy Values",
            ),
        },
    )


def overview_sections(spec: dict[str, Any], plan: dict[str, Any], mnemonic_count: int, form_count: int) -> str:
    lines = [
        architecture_overview_section(spec, plan, mnemonic_count, form_count),
        top_section("Terminology"),
        terminology_section(spec),
        compatibility_rules_section(spec),
        top_section("Programming Model"),
        register_tables(spec),
        top_section("CPUID Feature Discovery"),
        cpuid_feature_discovery_section(spec),
        save_area_reference_section(spec),
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
        memory_model_section(spec),
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


def save_area_reference_section(spec: dict[str, Any]) -> str:
    save_area_formats = ((spec.get("instructions") or {}).get("save_area_formats") or {})
    if not isinstance(save_area_formats, dict) or not save_area_formats:
        return ""
    applies_to = sorted(
        {
            str(mnemonic)
            for layout in save_area_formats.values()
            if isinstance(layout, dict)
            for mnemonic in (layout.get("applies_to", []) or [])
        }
    )
    sections = save_area_format_reference_sections(
        save_area_formats,
        applies_to or ["SAVE", "RESTORE"],
        include_titles=False,
    )
    if not sections:
        return ""
    first_layout = next((layout for layout in save_area_formats.values() if isinstance(layout, dict)), {})
    title = str(first_layout.get("title") or "SAVE/RESTORE Processor-State Save Area")
    return "\n".join([top_section(title)] + sections)


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
    for name, body in (registers.get("special_register_classes") or {}).items():
        rows.append(
            [
                tex_code(name),
                tex_table_value(len(body.get("registers", []) or [])),
                tex_table_value(body.get("width", "-")),
                tex_table_value(body.get("role", "-")),
                tex_table_value(False),
            ]
        )
    for name, body in (registers.get("control_register_classes") or {}).items():
        rows.append(
            [
                tex_code(name),
                tex_table_value(len(body.get("registers", []) or [])),
                tex_table_value(body.get("width", "-")),
                tex_table_value(body.get("role", "-")),
                tex_table_value(False),
            ]
        )
    segment_register_operand_class = ""
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
        segment_register_operand_class = render_latex_template(
            "segment_register_operand_class.tex",
            {
                "SEGMENT_REGISTER_CLASS_TABLE": latex_longtable(
                    ["Class", "Width", "Bits", "Role", "Registers"],
                    srows,
                    ["0.55in", "0.55in", "0.45in", "1.05in", "2.8in"],
                    "Table 2-2. Segment Register Operand Class",
                ),
                "SEGMENT_REGISTER_SELECTOR_TABLE": latex_longtable(
                    ["Bits", "Register", "Reserved Access"],
                    sreg_selector_rows(spec),
                    ["0.55in", "1.0in", "3.90in"],
                    "RDSEG/WRSEG Segment Register Selector Encoding",
                ),
            },
        )

    special = []
    for reg in registers.get("special_registers", []) or []:
        if not isinstance(reg, dict):
            continue
        if is_control_register(reg):
            continue
        if str(reg.get("class", "")).upper() == "S" or str(reg.get("role", "")).lower() == "segment":
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
    return render_latex_template(
        "register_model.tex",
        {
            "REGISTER_MODEL_FIGURE": register_model_figure(spec),
            "REGISTER_CLASS_TABLE": latex_tabular(
                ["Class", "Count", "Width", "Role", "Allocatable"],
                rows,
                ["0.7in", "0.65in", "0.65in", "1.45in", "1.2in"],
                "Table 2-1. Register Classes",
            ),
            "DATA_REGISTER_BANKING": data_register_banking_section(spec),
            "STATE_REGISTER_FORMATS": state_register_format_section(spec),
            "FLOATING_POINT_REGISTER_MODEL": floating_point_register_section(spec),
            "SEGMENT_REGISTER_FORMATS": segment_register_section(spec),
            "SEGMENT_REGISTER_OPERAND_CLASS": segment_register_operand_class,
            "SPECIAL_REGISTER_TABLE": latex_longtable(
                ["Name", "Width", "Class", "Role", "Privilege", "Implicit"],
                special,
                ["0.7in", "0.5in", "0.5in", "0.8in", "0.9in", "0.65in"],
                "Table 2-3. Special Registers",
            ),
            "TRANSLATION_CONTROL": translation_control_section(spec),
        },
    )


def cpuid_discovery_text(value: Any) -> str:
    if isinstance(value, dict):
        class_name = value.get("cpuid_class")
        leaf_name = value.get("cpuid_leaf")
        if class_name and leaf_name:
            return f"CPUID {class_name}.{leaf_name}"
        if leaf_name:
            return f"CPUID {leaf_name}"
    return compact_text(value)


def data_register_banking_section(spec: dict[str, Any]) -> str:
    banking = spec.get("registers", {}).get("data_register_banking") or {}
    if not isinstance(banking, dict) or not banking:
        return ""
    selector = banking.get("selector") or {}
    model = banking.get("model") or {}
    tiers = banking.get("tiers") or []
    selector_rows = [
        [tex_escape("Selector"), tex_code(selector.get("name", "-"))],
        [tex_escape("Selector width"), tex_escape(bit_count_text(selector.get("width")))],
        [tex_escape("Architectural namespace"), tex_escape(bank_count_text(selector.get("architectural_namespace")))],
        [tex_escape("Base required count"), tex_escape(selector.get("required_base_count", "-"))],
        [tex_escape("Discovery"), tex_escape(cpuid_discovery_text(selector.get("discovery", "-")))],
        [tex_escape("Object attribute"), tex_code(str(banking.get("object_attribute", "-")))],
    ]
    model_rows = [
        [tex_escape("Visible D register"), tex_code(model.get("visible_register_rule", "-"))],
        [tex_escape("Ordinary D operands"), tex_escape(model.get("ordinary_instruction_rule", "-"))],
        [tex_escape("Bank 0"), tex_escape(model.get("bank_zero_role", "-"))],
        [tex_escape("Public ABI boundary"), tex_escape(model.get("public_boundary_rule", "-"))],
        [tex_escape("Handler entry"), tex_escape(model.get("handler_entry_rule", "-"))],
        [tex_escape("Saved state"), tex_escape(model.get("saved_state_rule", "-"))],
    ]
    tier_rows = []
    for tier in tiers:
        if not isinstance(tier, dict):
            continue
        tier_rows.append(
            [
                tex_code(tier.get("name", "")),
                tex_escape(tier.get("required_banks", "-")),
                tex_escape(compact_text(tier.get("description", ""))),
            ]
        )
    tier_table = ""
    if tier_rows:
        tier_table = latex_longtable(["Tier", "Banks", "Meaning"], tier_rows, ["0.85in", "0.65in", "4.00in"], "Data Register Bank Availability Tiers")
    return render_latex_template(
        "data_register_banks.tex",
        {
            "SELECTOR_TABLE": latex_longtable(["Property", "Value"], selector_rows, ["1.55in", "3.95in"], "Data Register Bank Selector"),
            "MODEL_TABLE": latex_longtable(["Rule", "Meaning"], model_rows, ["1.55in", "3.95in"], "Data Register Bank Rules"),
            "TIER_TABLE": tier_table,
        },
    )


def bit_count_text(value: Any) -> str:
    return "-" if value is None else f"{value} bits"


def bank_count_text(value: Any) -> str:
    return "-" if value is None else f"{value} banks"


def is_control_register(reg: dict[str, Any]) -> bool:
    return str(reg.get("role", "")).lower() == "control" or str(reg.get("class", "")).upper() in {"C", "CR"}


def control_register_rows(spec: dict[str, Any]) -> list[list[str]]:
    registers = spec.get("registers", {})
    by_name = {
        str(reg.get("name", "")): reg
        for reg in registers.get("special_registers", []) or []
        if isinstance(reg, dict) and is_control_register(reg)
    }
    cr_class = ((registers.get("control_register_classes") or {}).get("CR") or {})
    groups = cr_class.get("selector_groups") if isinstance(cr_class, dict) else []
    grouped: set[str] = set()
    rows: list[list[str]] = []
    for group in groups or []:
        if not isinstance(group, dict):
            continue
        selectors = [item for item in group.get("selectors", []) or [] if isinstance(item, dict)]
        names = [str(item.get("register", "-")) for item in selectors]
        grouped.update(name for name in names if name != "-")
        roles = []
        for name in names:
            reg = by_name.get(name)
            roles.append(compact_text(reg.get("description", reg.get("role", "-"))) if reg else "-")
        rows.append(
            [
                tex_escape(readable_text(group.get("name", "-"))),
                tex_multiline_latex([tex_code(name) for name in names]),
                tex_escape("64"),
                tex_escape("supervisor"),
                tex_multiline(roles),
            ]
        )
    for name in sorted(name for name in by_name if name not in grouped):
        reg = by_name[name]
        rows.append(
            [
                tex_escape("unclassified"),
                tex_code(name),
                tex_escape(reg.get("width", "-")),
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
    rows: list[list[str]] = []
    for item in special_register_encoding(spec, "S"):
        bits = item.get("bits")
        if bits is None and isinstance(item.get("value"), int):
            bits = f"{int(item['value']):03b}"
        fault = item.get("access_fault")
        if not fault and str(item.get("register", "")).lower() == "reserved":
            fault = "ILLEGAL_INSTRUCTION"
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
    if not isinstance(groups, list):
        return []
    rows: list[list[str]] = []
    reserved_fault = cr_class.get("reserved_selector_fault", "INVALID_CONTROL_STATE") if isinstance(cr_class, dict) else "INVALID_CONTROL_STATE"
    for group in groups:
        if not isinstance(group, dict):
            continue
        group_name = readable_text(group.get("name", ""))
        selectors = group.get("selectors") or []
        entries = []
        for selector in selectors:
            if isinstance(selector, dict):
                entries.append(
                    f"{tex_code(numeric_selector_text(selector.get('value', '-'), width=4))} "
                    f"{tex_code(str(selector.get('register', '-')))}"
                )
        if entries:
            rows.append([tex_escape(group_name), tex_multiline_latex(entries)])
    rows.append(
        [
            tex_escape("unassigned"),
            tex_multiline_latex([tex_escape("all other selectors"), tex_code(str(reserved_fault))]),
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
    flags_rows = []
    for name, body in (flags.get("layout") or {}).items():
        if isinstance(body, dict):
            bit = body.get("bit", "-")
            meaning = body.get("description", "")
        else:
            bit = body
            meaning = ""
        flags_rows.append([tex_code(name), tex_escape(bit), tex_escape(meaning)])
    status_rows = []
    for name, body in (status.get("layout") or {}).items():
        if isinstance(body, dict):
            status_rows.append([tex_code(name), tex_escape(body.get("bit", "-")), tex_escape(body.get("description", "-"))])
        else:
            status_rows.append([tex_code(name), tex_escape(body), tex_escape("-")])
    return render_latex_template(
        "state_register_formats.tex",
        {
            "STATUS_MEANINGFUL_BITS": tex_escape(status.get("nonzero_bits", 0)),
            "FLAGS_TABLE": latex_longtable(["Bit", "Position", "Meaning"], flags_rows, ["0.55in", "0.65in", "4.05in"], "Table 2-4. FLAGS Bits"),
            "STATUS_TABLE": latex_longtable(["Bit", "Position", "Meaning"], status_rows, ["0.55in", "0.65in", "4.05in"], "Table 2-5. STATUS Bits"),
        },
    )


def floating_point_register_section(spec: dict[str, Any]) -> str:
    fpu = spec.get("registers", {}).get("floating_point_register_model") or {}
    if not isinstance(fpu, dict) or not fpu:
        return ""
    regs = fpu.get("registers") or {}
    fflags = fpu.get("fflags") or {}
    fstatus = fpu.get("fstatus") or {}
    register_rows = [
        [tex_escape("Registers"), tex_code(str(regs["names"]))],
        [tex_escape("Count"), tex_escape(regs["count"])],
        [tex_escape("Architectural width"), tex_escape(f"{regs['width']} bits")],
        [tex_escape("Scalar formats"), tex_table_value(regs["scalar_formats"])],
        [tex_escape("FFLAGS width"), tex_escape(f"{fflags['width']} bits")],
        [tex_escape("FSTATUS width"), tex_escape(f"{fstatus['width']} bits")],
        [tex_escape("FFLAGS reset"), tex_code(str(fflags["reset"]))],
        [tex_escape("FSTATUS reset"), tex_code(str(fstatus["reset"]))],
        [tex_escape("Unsupported extension instruction"), tex_code(str(fpu["unsupported_instruction_exception"]))],
    ]
    flag_rows = []
    for name, body in (fflags.get("bits") or {}).items():
        if not isinstance(body, dict):
            continue
        flag_rows.append([tex_code(name), tex_escape(body.get("bit", "-")), tex_escape(body.get("description", "-"))])
    fstatus_rows = []
    for name, body in (fstatus.get("fields") or {}).items():
        if not isinstance(body, dict):
            continue
        if "bit" in body:
            position = str(body.get("bit"))
        else:
            bits = body.get("bits", "-")
            position = f"{bits[0]}:{bits[1]}" if isinstance(bits, list) and len(bits) == 2 else str(bits)
        fstatus_rows.append([tex_code(name), tex_escape(position), tex_escape(body.get("description", "-"))])
    rounding_rows = []
    for value, meaning in (fstatus.get("rounding_modes") or {}).items():
        rounding_rows.append([tex_code(str(value)), tex_escape(meaning)])
    exception_rule = fstatus.get("exception_rule") or {}
    ieee_default = fstatus.get("ieee_754_default") or {}
    write_policy = fstatus.get("write_policy") or {}
    register_summary = (
        "The floating-point extension defines "
        f"{regs['count']} Q-sized floating-point registers, {regs['names']}."
    )
    fstatus_notes = [
        exception_rule.get("trap_disabled", "") if isinstance(exception_rule, dict) else "",
        exception_rule.get("trap_enabled", "") if isinstance(exception_rule, dict) else "",
        write_policy.get("description", "") if isinstance(write_policy, dict) else "",
        ieee_default.get("rule", "") if isinstance(ieee_default, dict) else "",
    ]
    fstatus_notes = [part for part in fstatus_notes if part]
    return render_latex_template(
        "floating_point_register_model.tex",
        {
            "REGISTER_MODEL_SUMMARY": tex_escape(register_summary),
            "REGISTER_TABLE": latex_tabular(["Property", "Value"], register_rows, ["1.55in", "3.95in"], "Floating-Point Register File"),
            "FFLAGS_TABLE": latex_tabular(["Bit", "Position", "Meaning"], flag_rows, ["0.55in", "0.65in", "4.05in"], "FFLAGS Bits"),
            "FSTATUS_TABLE": latex_tabular(["Field", "Position", "Meaning"], fstatus_rows, ["0.85in", "0.75in", "3.90in"], "FSTATUS Fields") if fstatus_rows else "",
            "ROUNDING_TABLE": latex_tabular(["Value", "Rounding Mode"], rounding_rows, ["0.65in", "4.85in"], "FSTATUS Rounding Modes") if rounding_rows else "",
            "FSTATUS_NOTES": latex_itemize_lines(fstatus_notes),
        },
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
    field_rows = []
    for name, field in (segments.get("layout") or {}).items():
        if not isinstance(field, dict):
            continue
        bits = field.get("bits", "-")
        if isinstance(bits, list) and len(bits) == 2:
            bit_text = str(bits[0]) if bits[0] == bits[1] else f"{bits[0]}:{bits[1]}"
        else:
            bit_text = str(bits)
        field_rows.append(
            [
                tex_code(field.get("field_name") or name),
                tex_escape(bit_text),
                tex_escape(field.get("description", "")),
            ]
        )
    return render_latex_template(
        "segment_registers.tex",
        {
            "REGISTER_TABLE": latex_longtable(
                ["Register", "Selector", "Width"],
                rows,
                ["0.75in", "1.1in", "0.65in"],
                "Table 2-6. Segment Registers",
            ),
            "FIELD_TABLE": latex_longtable(
                ["Field", "Bits", "Meaning"],
                field_rows,
                ["0.85in", "0.65in", "3.75in"],
                "Table 2-7. Segment Register Fields",
            ),
        },
    )


def translation_control_section(spec: dict[str, Any]) -> str:
    registers = spec.get("registers", {})
    control = registers.get("translation_control") or {}
    if not isinstance(control, dict):
        control = {}
    return render_latex_template(
        "translation_control.tex",
        {
            "CONTROL_REGISTER_TABLE": latex_tabular(
                ["Group", "Register(s)", "Width", "Privilege", "Role"],
                control_register_rows(spec),
                ["1.05in", "1.0in", "0.55in", "0.85in", "2.10in"],
                "Table 2-8. Control Registers",
            ),
            "CONTROL_REGISTER_SELECTOR_TABLE": latex_tabular(
                ["Group", "Selector / Register"],
                control_register_selector_rows(spec),
                ["1.35in", "4.15in"],
                "Control Register Selector Encoding",
            ),
            "PTCR_FIELD_TABLE": latex_longtable(["Field", "Bits", "Meaning"], ptcr_field_rows(spec), ["0.95in", "0.65in", "3.85in"], "Table 2-9. PTCR Fields"),
            "PABITS_SELECTOR_TABLE": latex_longtable(["Selector", "PABITS", "Reserved Access"], pabits_selector_rows(spec), ["0.80in", "0.85in", "3.85in"], "PTCR PABITS Selector Encoding"),
            "ASCR_FIELD_TABLE": latex_longtable(["Field", "Bits", "Meaning"], ascr_field_rows(spec), ["0.95in", "0.65in", "3.85in"], "Table 2-10. ASCR Fields"),
            "ICR_FIELD_TABLE": latex_longtable(["Field", "Bits", "Meaning"], icr_field_rows(spec), ["0.95in", "0.65in", "3.85in"], "Table 2-11. ICR Fields"),
        },
    )


def control_model(spec: dict[str, Any]) -> dict[str, Any]:
    model = spec.get("interrupts") or {}
    return model if isinstance(model, dict) else {}


def privileged_programming_model(spec: dict[str, Any]) -> dict[str, Any]:
    control = control_model(spec)
    model = control.get("privileged_programming_model") or {}
    return model if isinstance(model, dict) else {}


def exception_processing_model(spec: dict[str, Any]) -> dict[str, Any]:
    control = control_model(spec)
    model = control.get("exception_processing") or {}
    return model if isinstance(model, dict) else {}


def privilege_state_rows(model: dict[str, Any]) -> list[list[str]]:
    state = model.get("privilege_state") if isinstance(model, dict) else {}
    rows: list[list[str]] = []
    for field in ("PM", "access_domain"):
        values = (state or {}).get(field) if isinstance(state, dict) else {}
        if not isinstance(values, dict):
            continue
        for value, meaning in values.items():
            field_name = f"STATUS.{field}" if field == "PM" else "access domain"
            rows.append([tex_code(field_name), tex_code(value), tex_escape(meaning)])
    return rows


def privileged_model_rule_rows(model: dict[str, Any]) -> list[list[str]]:
    rules = model.get("normative_rules") if isinstance(model, dict) else None
    if not isinstance(rules, list):
        rules = []
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
    entry_registers = syscall.get("entry_registers") or []
    saved_state = syscall.get("saved_state") or []
    return [
        [tex_escape("Entry vector"), tex_escape(syscall.get("vector", "-"))],
        [tex_escape("Entry target"), tex_table_value(entry_registers)],
        [tex_escape("Frame style"), tex_escape(syscall.get("frame_style", "-"))],
        [tex_escape("Saved state"), tex_table_value(saved_state)],
        [tex_escape("Entry table size"), tex_escape(f"{syscall.get('entry_table_size_bytes', '-')} bytes")],
        [tex_escape("Entry address alignment"), tex_escape(f"{syscall.get('entry_address_alignment_bytes', '-')} bytes")],
        [tex_escape("Entry STATUS change"), tex_escape(syscall.get("status_change", "-"))],
        [tex_escape("Entry DBANK change"), tex_escape(syscall.get("dbank_change", "-"))],
        [tex_escape("Return instruction"), tex_code(syscall.get("return_instruction", "-"))],
        [tex_escape("Return policy"), tex_escape(syscall.get("return_policy", "-"))],
    ]


def privileged_rule_rows(model: dict[str, Any]) -> list[list[str]]:
    entry = model.get("entry_status_policy") if isinstance(model, dict) else {}
    irq = model.get("interrupt_exception_entry") if isinstance(model, dict) else {}
    returns = model.get("return_rules") if isinstance(model, dict) else {}
    nesting = model.get("interrupt_nesting") if isinstance(model, dict) else {}
    access = model.get("control_register_access") if isinstance(model, dict) else {}
    entry_changes = entry.get("entry_status_changes", []) if isinstance(entry, dict) else []
    return [
        [tex_escape("Entry STATUS update"), tex_table_value(entry_changes)],
        [tex_escape("Entry DBANK update"), tex_escape(entry.get("entry_dbank_change", "-") if isinstance(entry, dict) else "-")],
        [tex_escape("Saved STATUS return"), tex_escape(entry.get("saved_status_return", "-") if isinstance(entry, dict) else "-")],
        [tex_escape("Entry interrupt masking"), tex_escape("no automatic masking" if not (entry.get("interrupt_masking_on_entry", False) if isinstance(entry, dict) else False) else "mask on entry")],
        [tex_escape("Interrupt stack selection"), tex_escape(irq.get("stack_selection", "-") if isinstance(irq, dict) else "-")],
        [tex_escape("NMI stack selection"), tex_escape(irq.get("nmi_stack_selection", "-") if isinstance(irq, dict) else "-")],
        [tex_escape("Double-fault stack selection"), tex_escape(irq.get("double_fault_stack_selection", "-") if isinstance(irq, dict) else "-")],
        [tex_escape("Interrupt frame save"), tex_escape(irq.get("frame_save", "-") if isinstance(irq, dict) else "-")],
        [tex_code("SYSRET"), tex_escape(returns.get("SYSRET", "-") if isinstance(returns, dict) else "-")],
        [tex_code("IRET"), tex_escape(returns.get("IRET", "-") if isinstance(returns, dict) else "-")],
        [tex_escape("Malformed return frame"), tex_escape(returns.get("malformed_frame", "-") if isinstance(returns, dict) else "-")],
        [tex_code("ICR.MAX_IDEPTH"), tex_escape(nesting.get("max_idepth_rule", "-") if isinstance(nesting, dict) else "-")],
        [tex_code("RDCR/WRCR"), tex_escape(f"RDCR = {access.get('RDCR', '-')}; WRCR = {access.get('WRCR', '-')}" if isinstance(access, dict) else "-")],
        [tex_escape("User-visible control state"), tex_escape(access.get("user_access_policy", "-") if isinstance(access, dict) else "-")],
    ]


def privileged_programming_model_section(spec: dict[str, Any]) -> str:
    model = privileged_programming_model(spec)
    return render_latex_template(
        "privileged_programming_model.tex",
        {
            "PRIVILEGED_RULE_TABLE": latex_longtable(["No.", "Subject", "Rule"], privileged_model_rule_rows(model), ["0.35in", "1.45in", "3.65in"], "Table 8-1. Privileged Model Rules"),
            "PRIVILEGE_STATE_TABLE": latex_longtable(["Field", "Value", "Meaning"], privilege_state_rows(model), ["1.15in", "0.55in", "3.75in"], "Table 8-2. Privilege State and Access Domains"),
            "SYSCALL_TABLE": latex_longtable(["Property", "Rule"], syscall_model_rows(model), ["1.55in", "3.90in"], "Table 8-3. SYSCALL/SYSRET Rules"),
            "PRIVILEGED_EXECUTION_TABLE": latex_longtable(["Rule", "Meaning"], privileged_rule_rows(model), ["1.65in", "3.80in"], "Table 8-4. Privileged Execution Rules"),
        },
    )


def field_bits_text(field: dict[str, Any]) -> str:
    if "bit" in field:
        return str(field.get("bit"))
    bits = field.get("bits")
    if isinstance(bits, list) and len(bits) == 2:
        return str(bits[0]) if bits[0] == bits[1] else f"{bits[0]}:{bits[1]}"
    return "-"


def layout_field_rows(layout: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for name, field in sorted(
        layout.items(),
        key=lambda item: max(item[1].get("bits", [item[1].get("bit", 0)]) if isinstance(item[1], dict) else [0]),
        reverse=True,
    ):
        if not isinstance(field, dict):
            continue
        rows.append(
            [
                tex_code(name),
                tex_escape(field_bits_text(field)),
                tex_escape(field.get("description", "")),
            ]
        )
    return rows


def ptcr_field_rows(spec: dict[str, Any]) -> list[list[str]]:
    return layout_field_rows(special_register_layout(spec, "PTCR"))


def pabits_selector_rows(spec: dict[str, Any]) -> list[list[str]]:
    control = spec.get("registers", {}).get("translation_control") or {}
    ptcr = control.get("PTCR") if isinstance(control, dict) else {}
    entries = (ptcr or {}).get("PABITS_SEL") if isinstance(ptcr, dict) else None
    if not isinstance(entries, list):
        entries = []
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


def ascr_field_rows(spec: dict[str, Any]) -> list[list[str]]:
    return layout_field_rows(special_register_layout(spec, "ASCR"))


def pte_field_rows(spec: dict[str, Any]) -> list[list[str]]:
    control = spec.get("registers", {}).get("translation_control") or {}
    pte = (control.get("page_table_entry") or {}) if isinstance(control, dict) else {}
    fields = pte.get("low_attribute_bits") if isinstance(pte, dict) else None
    return layout_field_rows(fields if isinstance(fields, dict) else {})


def field_bit_range(field: dict[str, Any]) -> tuple[int, int]:
    if "bit" in field:
        bit = int(field["bit"])
        return bit, bit
    bits = field.get("bits")
    if isinstance(bits, list) and len(bits) == 2:
        high = int(bits[0])
        low = int(bits[1])
        return high, low
    raise ValueError(f"field does not declare bit or bits: {field!r}")


def pte_low_attribute_fields(spec: dict[str, Any]) -> list[tuple[str, int]]:
    pte = page_table_entry_spec(spec)
    fields = pte.get("low_attribute_bits")
    if not isinstance(fields, dict):
        return []
    ranges = []
    for name, field in fields.items():
        if not isinstance(field, dict):
            continue
        high, low = field_bit_range(field)
        ranges.append((str(name), high, low))
    ranges.sort(key=lambda item: item[1], reverse=True)
    if not ranges:
        return []
    expected_high = ranges[0][1]
    low_bit = ranges[-1][2]
    if low_bit != 0:
        raise ValueError("PTE low attribute diagram expects fields to end at bit 0")
    out: list[tuple[str, int]] = []
    for name, high, low in ranges:
        if high != expected_high:
            raise ValueError("PTE low attribute fields must be contiguous")
        out.append((name, high - low + 1))
        expected_high = low - 1
    return out


def pte_low_attribute_figure(spec: dict[str, Any]) -> str:
    fields = pte_low_attribute_fields(spec)
    if not fields:
        return ""
    total_bits = sum(width for _name, width in fields)
    top_labels = [total_bits - 1, 7, 0] if total_bits > 7 else [total_bits - 1, 0]
    return bit_field_figure(fields, "PTE Low Attribute Bits", "PTE[11:0]", total_bits, top_labels, listed=True)


def page_table_entry_spec(spec: dict[str, Any]) -> dict[str, Any]:
    control = spec.get("registers", {}).get("translation_control") or {}
    pte = (control.get("page_table_entry") or {}) if isinstance(control, dict) else {}
    return pte if isinstance(pte, dict) else {}


def pte_walk_rule_rows(spec: dict[str, Any]) -> list[list[str]]:
    rules = page_table_entry_spec(spec).get("walk_level_rules")
    if not isinstance(rules, dict):
        return []
    return [[tex_escape(readable_text(key)), tex_escape(value)] for key, value in rules.items()]


def pte_attribute_rule_rows(spec: dict[str, Any]) -> list[list[str]]:
    pte = page_table_entry_spec(spec)
    rows: list[list[str]] = []
    section_labels = {
        "non_leaf_attributes": "non-leaf",
        "leaf_attributes": "leaf",
    }
    for section_name in ("non_leaf_attributes", "leaf_attributes"):
        attributes = pte.get(section_name)
        if not isinstance(attributes, dict):
            continue
        for field, rule in attributes.items():
            rows.append([tex_multiline_latex([tex_escape(section_labels[section_name]), tex_code(field)]), tex_escape(rule)])
    return rows


def pte_permission_rule_rows(spec: dict[str, Any]) -> list[list[str]]:
    control = spec.get("registers", {}).get("translation_control") or {}
    pte = (control.get("page_table_entry") or {}) if isinstance(control, dict) else {}
    rules = pte.get("permission_rules") if isinstance(pte, dict) else None
    if not isinstance(rules, list):
        return []
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


def icr_field_rows(spec: dict[str, Any]) -> list[list[str]]:
    return layout_field_rows(special_register_layout(spec, "ICR"))


def byte_range_text(value: Any) -> str:
    if isinstance(value, list) and len(value) == 2:
        return f"bytes {value[0]}..{value[1]}"
    return f"byte {value}"


def ivt_entry_rows(spec: dict[str, Any]) -> list[list[str]]:
    table = spec.get("interrupts", {}).get("interrupt_vector_table") or {}
    layout = table.get("entry_layout") if isinstance(table, dict) else {}
    if not isinstance(layout, dict):
        return []
    rows: list[list[str]] = []
    handler = layout.get("handler_address")
    if isinstance(handler, dict):
        rows.append(
            [
                tex_code("handler_address"),
                tex_escape(byte_range_text(handler.get("bytes"))),
                tex_escape(handler.get("description", "")),
            ]
        )
    control = layout.get("control_byte")
    if isinstance(control, dict):
        byte = control.get("byte", "-")
        fields = control.get("fields") or {}
        if not isinstance(fields, dict):
            fields = {}
        for name, field in fields.items():
            if not isinstance(field, dict):
                continue
            description = str(field.get("description", ""))
            values = field.get("values")
            if isinstance(values, dict):
                description = tex_multiline([description, *[f"{key} = {value}" for key, value in values.items()]])
            else:
                description = tex_escape(description)
            rows.append(
                [
                    tex_code(name),
                    tex_escape(f"byte {byte} bit {field_bits_text(field)}"),
                    description,
                ]
            )
    reserved = layout.get("reserved")
    if isinstance(reserved, dict):
        rows.append(
            [
                tex_code("reserved"),
                tex_escape(byte_range_text(reserved.get("bytes"))),
                tex_escape(reserved.get("description", "")),
            ]
        )
    return rows



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
        payload_blocks = frame_type.get("payload_blocks", 0)
        rows.append(
            [
                tex_code(code_text),
                tex_code(str(frame_type.get("name", ""))),
                tex_escape(str(payload_blocks)),
                tex_table_value(payload or "none"),
                tex_table_value(frame_type.get("description", "")),
            ]
        )
    return rows


def payload_slot_rows(control: dict[str, Any]) -> list[list[str]]:
    frame = supervisor_stack_frame(control)
    payload_slots = frame.get("payload_slots") if isinstance(frame, dict) else {}
    if not isinstance(payload_slots, dict):
        payload_slots = {}
    rows = []
    for name, slot in payload_slots.items():
        if not isinstance(slot, dict):
            continue
        offset = int(slot.get("offset", 0))
        rows.append(
            [
                tex_code(f"+0x{offset:02X}"),
                tex_code(str(name)),
                tex_escape(slot.get("description", "")),
            ]
        )
    return rows


def frame_control_rows(control: dict[str, Any]) -> list[list[str]]:
    frame_control = (supervisor_stack_frame(control).get("frame_control") or {}) if isinstance(control, dict) else {}
    if not isinstance(frame_control, dict):
        frame_control = {}
    rows = []
    for name, field in frame_control.items():
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
        aux = {}
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
    return {}


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
        collapsed_text = "-"
    return [
        [tex_escape("CPU exception model"), tex_escape(model.get("cpu_exception_model", "-"))],
        [tex_escape("Restart policy"), tex_escape(model.get("restart_policy", "-"))],
        [tex_escape("Interrupt frame save"), tex_escape(model.get("interrupt_frame_save", "-"))],
        [tex_escape("Entry STATUS update"), tex_escape(model.get("status_on_entry", "-"))],
        [tex_escape("Return STATUS update"), tex_escape(model.get("status_on_return", "-"))],
        [tex_escape("Entry DBANK update"), tex_escape(model.get("dbank_on_entry", "-"))],
        [tex_escape("Return DBANK update"), tex_escape(model.get("dbank_on_return", "-"))],
        [tex_code("SYSRET"), tex_escape(returns.get("SYSRET", "-") if isinstance(returns, dict) else "-")],
        [tex_code("IRET"), tex_escape(returns.get("IRET", "-") if isinstance(returns, dict) else "-")],
        [tex_escape("IRET frame-type check"), tex_escape(model.get("iret_frame_type_check", "-"))],
        [tex_escape("Malformed return frame"), tex_escape(model.get("malformed_return_frame", "-"))],
        [tex_escape("Absent IVT handler"), tex_escape(model.get("handler_absent_behavior", "-"))],
        [tex_escape("Reserved CPU vector"), tex_escape(model.get("reserved_cpu_vector_behavior", "-"))],
        [tex_escape("Fault priority"), tex_table_value(priority or "-")],
        [tex_escape("Collapsed fault classes"), tex_escape(collapsed_text)],
        [tex_escape("Address fault vector"), tex_escape(model.get("address_fault_vector", "-"))],
    ]


def interrupt_model_section(spec: dict[str, Any]) -> str:
    control = control_model(spec)
    frame = supervisor_stack_frame(control)
    assignment = interrupt_vector_assignment(control)
    unit = int(frame.get("frame_size_unit_bytes", 8))
    base_size = int(frame.get("base_size_bytes", 96))
    payload_block_size = int(frame.get("payload_block_size_bytes", base_size))
    fixed_slots = len(frame.get("layout") or [])
    return render_latex_template(
        "interrupt_model.tex",
        {
            "IVT_ENTRY_TABLE": latex_longtable(["Field", "Location", "Meaning"], ivt_entry_rows(spec), ["0.95in", "0.85in", "3.65in"], "Table 4-1. Interrupt Vector Table Entry Fields"),
            "VECTOR_ASSIGNMENT_POLICY": tex_escape(assignment.get("policy", "")),
            "SYSCALL_ENTRY_PATH": tex_code(str(assignment.get("syscall_entry", "-"))),
            "VECTOR_RANGE_TABLE": latex_longtable(["Range", "Owner", "Meaning"], interrupt_vector_range_rows(control), ["0.85in", "1.35in", "3.30in"], "Table 4-2. Interrupt Vector Ranges"),
            "CPU_VECTOR_TABLE": latex_longtable(["Vector", "Name", "Source", "Frame"], interrupt_vector_rows(control), ["0.55in", "1.65in", "2.20in", "1.00in"], "Table 4-3. CPU-Owned Interrupt Vectors"),
            "EXCEPTION_ENTRY_TABLE": latex_longtable(["Rule", "Meaning"], exception_processing_rows(control), ["1.55in", "3.90in"], "Table 4-4. Exception Entry and Return Rules"),
            "BASE_FRAME_SIZE": tex_escape(base_size),
            "FIXED_SLOT_COUNT": tex_escape(fixed_slots),
            "FRAME_SIZE_UNIT_BYTES": tex_escape(unit),
            "BASE_FRAME_UNITS": tex_escape(base_size // unit),
            "PAYLOAD_BLOCK_SIZE": tex_escape(payload_block_size),
            "STACK_FRAME_FIGURE": stack_frame_figure(control),
            "STACK_FRAME_TABLE": latex_longtable(["Offset", "Slot", "Meaning"], stack_frame_rows(control), ["0.70in", "1.20in", "3.60in"], "Table 4-5. Supervisor Entry Stack Frame"),
            "FRAME_TYPE_TABLE": latex_longtable(["Code", "Type", "Payload Blocks", "Payload", "Meaning"], frame_type_rows(control), ["0.45in", "0.95in", "0.65in", "1.35in", "2.10in"], "Table 4-6. Supervisor Stack Frame Types"),
            "PAYLOAD_SLOT_TABLE": latex_longtable(["Offset", "Slot", "Meaning"], payload_slot_rows(control), ["0.70in", "1.20in", "3.60in"], "Table 4-7. Supervisor Payload Block Slots"),
            "FRAME_CONTROL_TABLE": latex_longtable(["Field", "Bits", "Meaning"], frame_control_rows(control), ["1.35in", "0.60in", "3.55in"], "Table 4-8. FRAME_CONTROL Fields"),
            "REPEAT_FAULT_AUX_TABLE": latex_longtable(["Field", "Bits", "Meaning"], repeat_fault_aux_rows(control), ["1.55in", "0.60in", "3.35in"], "Table 4-9. Repeat Fault Auxiliary Fields"),
            "RESET_STATE_TABLE": latex_longtable(["State", "Reset Value"], reset_state_rows(control), ["2.1in", "2.4in"], "Table 4-10. Interrupt and Translation Reset State"),
        },
    )


def reset_state_rows(control: dict[str, Any]) -> list[list[str]]:
    reset = (control.get("reset_state") or {}) if isinstance(control, dict) else {}
    return [[tex_code(key), tex_table_value(value)] for key, value in reset.items()]


def memory_address_translation_section(spec: dict[str, Any]) -> str:
    return render_latex_template(
        "memory_address_translation.tex",
        {
            "LA48_PAGE_WALK": paging_mode_figure(
                "LA48",
                [("sign", 16), ("L4 idx", 9), ("L3 idx", 9), ("L2 idx", 9), ("L1 idx", 9), ("offset", 12)],
                ["L4", "L3", "L2", "L1"],
                "LA48 Four-Level Page Walk",
            ),
            "LA57_PAGE_WALK": paging_mode_figure(
                "LA57",
                [("sign", 7), ("L5 idx", 9), ("L4 idx", 9), ("L3 idx", 9), ("L2 idx", 9), ("L1 idx", 9), ("offset", 12)],
                ["L5", "L4", "L3", "L2", "L1"],
                "LA57 Five-Level Page Walk",
            ),
            "PTE_LOW_ATTRIBUTE_FIGURE": pte_low_attribute_figure(spec),
            "PTE_FIELD_TABLE": latex_longtable(["Field", "Bits", "Meaning"], pte_field_rows(spec), ["0.55in", "0.65in", "4.25in"], "Table 3-2. Page-Table Entry Low Attribute Bits"),
            "PTE_WALK_RULE_TABLE": latex_longtable(["Level", "Rule"], pte_walk_rule_rows(spec), ["1.15in", "4.35in"], "Table 3-3. Page-Walk Level Rules"),
            "PTE_ATTRIBUTE_RULE_TABLE": latex_longtable(["Field", "Rule"], pte_attribute_rule_rows(spec), ["0.95in", "4.55in"], "Table 3-4. PTE Attribute Semantics"),
            "PTE_PERMISSION_RULE_TABLE": latex_longtable(["Mode", "Condition", "Result"], pte_permission_rule_rows(spec), ["0.85in", "2.35in", "2.30in"], "PTE User-Permission Rules"),
        },
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
    return render_latex_template(
        "condition_codes.tex",
        {
            "CONDITION_TABLE": latex_longtable(["Code", "Value", "Aliases", "Expression"], rows, ["0.65in", "0.65in", "1.05in", "2.95in"], "Table 4-1. Condition Codes"),
        },
    )


def prefix_semantics_block(prefix: dict[str, Any]) -> str:
    detail = tex_escape(prefix.get("description") or readable_text(prefix.get("semantics", "-")))
    applies_to = prefix.get("applies_to") or []
    if applies_to:
        detail += r"\newline " + tex_escape("Applies to: " + ", ".join(str(item) for item in applies_to))
    requires = prefix.get("requires")
    if isinstance(requires, dict):
        require_text = ", ".join(f"{key}={prefix_requirement_text(value)}" for key, value in requires.items())
        detail += r"\newline " + tex_escape("Requires: " + require_text)
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


def prefix_requirement_text(value: Any) -> str:
    if isinstance(value, list):
        return "/".join(str(item) for item in value)
    return str(value)


def prefix_semantics_section(spec: dict[str, Any]) -> str:
    lines = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        if prefix.get("name") in {"REPcc", "REPG"}:
            continue
        if prefix.get("group") in {"ea_update", "repeat_boundary"}:
            continue
        lines.append(rf"\Needspace{{0.75in}}\manualfield{{{tex_code(prefix.get('name', ''))}:}}{{{prefix_semantics_block(prefix)}}}")
    return render_latex_template("prefix_semantics.tex", {"PREFIX_FIELD_BLOCKS": "\n".join(lines)})


def prefix_is_address_update(prefix: dict[str, Any]) -> bool:
    return prefix.get("group") == "ea_update"


def prefix_is_access_domain(prefix: dict[str, Any]) -> bool:
    return prefix.get("group") == "access_domain"


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
        if syntax.get("operand_annotation"):
            return str(syntax.get("operand_annotation"))
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
        "POSTINC": "[An++]",
        "PREINC": "[++An]",
        "POSTDEC": "[An--]",
        "PREDEC": "[--An]",
    }.get(name, name)


def address_update_operand_table(spec: dict[str, Any]) -> str:
    rows = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict) or not prefix_is_address_update(prefix):
            continue
        name = str(prefix.get("name", ""))
        description = compact_text(prefix.get("description", ""))
        rows.append(
            [
                tex_code(address_update_operand_syntax(name)),
                tex_code(prefix_encoding_text(prefix)),
                tex_escape(description),
            ]
        )
    if not rows:
        return ""
    return render_latex_template(
        "address_update_operands.tex",
        {
            "ADDRESS_UPDATE_TABLE": latex_longtable(
                ["Operand Syntax", "Byte", "Update"],
                rows,
                ["1.25in", "0.75in", "3.1in"],
                "Address-Update Encodings",
            ),
        },
    )


def access_domain_operand_table(spec: dict[str, Any]) -> str:
    rows = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict) or not prefix_is_access_domain(prefix):
            continue
        syntax = prefix.get("syntax") if isinstance(prefix.get("syntax"), dict) else {}
        rows.append(
            [
                tex_code(str(syntax.get("operand_annotation", prefix.get("name", "")))),
                tex_code(prefix_encoding_text(prefix)),
                tex_escape(compact_text(prefix.get("semantics", ""))),
            ]
        )
    if not rows:
        return ""
    return render_latex_template(
        "access_domain_operands.tex",
        {
            "ACCESS_DOMAIN_TABLE": latex_longtable(
                ["Operand Domains", "Byte", "Encoded Meaning"],
                rows,
                ["1.65in", "0.75in", "3.0in"],
                "User-Access Operand Encodings",
            ),
        },
    )


def prefix_table(spec: dict[str, Any]) -> str:
    rows = []
    for prefix in spec.get("prefixes", {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        if prefix_is_address_update(prefix):
            continue
        if prefix_is_access_domain(prefix):
            continue
        rows.append(
            [
                tex_code(prefix_syntax_text(prefix)),
                tex_code(prefix_encoding_text(prefix)),
                tex_table_value(prefix.get("semantics", "-")),
            ]
        )
    return render_latex_template(
        "prefixes.tex",
        {
            "PREFIX_TABLE": latex_longtable(
                ["Syntax", "Byte/Pattern", "Meaning"],
                rows,
                ["1.45in", "0.95in", "3.0in"],
                "Prefix Encodings",
            ),
            "ADDRESS_UPDATE_OPERANDS": address_update_operand_table(spec),
            "ACCESS_DOMAIN_OPERANDS": access_domain_operand_table(spec),
            "PREFIX_SEMANTICS": prefix_semantics_section(spec),
            "REPCC_SECTION": repcc_prefix_section(spec),
            "REPG_SECTION": repg_prefix_section(spec),
        },
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

    fpu_conditional = repeat.get(
        "fpu_conditional_mnemonics",
        prefix.get("fpu_conditional_mnemonics", []),
    ) or []
    syntax = repeat.get("syntax")
    if not syntax:
        syntax_info = prefix.get("syntax") or {}
        syntax = syntax_info.get("mnemonic_template", "REPcc") + " Dn, <instruction>" if isinstance(syntax_info, dict) else "REPcc Dn, <instruction>"

    rep_rows = [
        [tex_escape("Syntax"), tex_code(syntax)],
        [tex_escape("Alias"), tex_table_value(repeat.get("alias", "REP = REPT"))],
        [tex_escape("FPU conditional subset"), tex_table_value(fpu_conditional or "-")],
        [tex_escape("FPU status predicates"), tex_table_value(repeat.get("fpu_fflags_condition_repeat", "not supported"))],
        [tex_escape("Counter"), tex_escape(f"{repeat.get('counter', 'DREG')}, {readable_text(repeat.get('counter_direction', 'signed_toward_zero'))}")],
        *repeat_counter_encoding_rows(repeat or prefix),
        [tex_escape("Commit rule"), tex_table_value(repeat.get("commit_rule", "-"))],
        [tex_escape("Condition source"), tex_table_value(repeat.get("condition_source", "-"))],
        [tex_escape("Architectural flags"), tex_table_value(repeat.get("architectural_flags", "-"))],
        [tex_escape("FFLAGS"), tex_table_value(repeat.get("fflags_accumulation", "-"))],
    ]
    observed_rows = rep_observed_rows(repeat, prefix)
    observed_table = ""
    if observed_rows:
        observed_table = latex_longtable(["Mnemonic", "Observed Value", "REPFLAGS Rule"], observed_rows, ["0.85in", "1.95in", "2.65in"], "REPcc Observed Values")
    return render_latex_template(
        "repcc_prefix.tex",
        {
            "REP_RULE_TABLE": latex_longtable(
                ["Item", "Value"],
                rep_rows,
                ["1.35in", "4.1in"],
                "REPcc Prefix Rules",
            ),
            "REP_EXECUTION_SEQUENCE": rep_execution_sequence(repeat, prefix),
            "OBSERVED_VALUE_TABLE": observed_table,
        },
    )


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

    sample_parts = []
    if samples:
        sample_parts.append(r"\subsection{Representative Encodings}")
        for name, tokens, syntax in samples:
            sample_parts.append(rf"\Needspace{{1.6in}}\noindent\textbf{{{tex_escape(name)}}}: {tex_code(syntax)}")
            sample_parts.append(bit_diagram(tokens, f"Encoding layout for {syntax}", [f"word {index}" for index in range(len(tokens))], listed=True))
    return render_latex_template(
        "encoding_overview.tex",
        {
            "REPRESENTATIVE_ENCODINGS": "\n".join(sample_parts),
        },
    )


def execution_model_section(spec: dict[str, Any]) -> str:
    instructions = spec.get("instructions") or {}
    semantics = instructions.get("operation_semantics") or {}
    labels = terminology_display_labels(spec)
    defaults = semantics.get("defaults") or {}
    notation = semantics.get("notation") or {}
    syntax_policy = semantics.get("syntax_policy") or {}
    groups = semantics.get("groups") or {}
    default_rows = execution_default_rows(defaults, labels)
    default_rule_table = ""
    if default_rows:
        default_rule_table = latex_longtable(["Topic", "Spec Value"], default_rows, ["1.45in", "4.0in"], "Execution Defaults")
    suffix_rows = condition_suffix_rows(syntax_policy, labels)
    suffix_rule_table = ""
    if suffix_rows:
        suffix_rule_table = latex_longtable(["Rule", "Value"], suffix_rows, ["1.55in", "3.9in"], "Conditional Mnemonic Suffix Rules")
    notation_table = ""
    if notation:
        notation_table = latex_longtable(
            ["Term", "Meaning"],
            [[tex_escape(semantic_label(str(key), labels)), semantic_cell(value, labels)] for key, value in notation.items()],
            ["1.45in", "4.0in"],
            "Semantic Notation",
        )
    shared_block = shared_execution_block(groups, labels)
    return render_latex_template(
        "execution_model.tex",
        {
            "DEFAULT_RULE_TABLE": default_rule_table,
            "SUFFIX_RULE_TABLE": suffix_rule_table,
            "NOTATION_TABLE": notation_table,
            "SHARED_SIDE_EFFECT_BLOCK": shared_block,
        },
    )


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
    return readable_text(value)


def execution_default_rows(defaults: dict[str, Any], labels: dict[str, str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for key, value in defaults.items():
        value_text = memory_rule_text(value) if key == "memory_memory" else readable_text(value)
        rows.append([tex_escape(semantic_label(str(key), labels)), tex_escape(value_text)])
    return rows


def condition_suffix_rows(policy: dict[str, Any], labels: dict[str, str]) -> list[list[str]]:
    condition = policy.get("condition_code") if isinstance(policy, dict) else None
    if not isinstance(condition, dict):
        return []
    rows: list[list[str]] = []
    for key in ("placement",):
        if key in condition:
            rows.append([tex_escape(semantic_label(key, labels)), tex_escape(readable_text(condition[key]))])
    applies = condition.get("applies_to")
    if applies:
        rows.append([tex_escape(semantic_label("applies_to", labels)), tex_table_value(applies)])
    return rows


def semantic_cell(value: Any, labels: dict[str, str]) -> str:
    if isinstance(value, dict):
        lines = [f"{semantic_label(str(key), labels)}: {readable_text(item)}" for key, item in value.items()]
        return tex_multiline(lines)
    if isinstance(value, list):
        return tex_multiline([readable_text(item) for item in value])
    return tex_escape(readable_text(value))


def terminology_display_labels(spec: dict[str, Any]) -> dict[str, str]:
    labels = (spec.get("terminology") or {}).get("display_labels") or {}
    if not isinstance(labels, dict):
        return {}
    return {str(key): str(value) for key, value in labels.items()}


def semantic_label(key: str, labels: dict[str, str]) -> str:
    if key in labels:
        return labels[key]
    normalized = key.replace("-", "_").replace(".", "_")
    if normalized in labels:
        return labels[normalized]
    words: list[str] = []
    for raw in normalized.split("_"):
        if not raw:
            continue
        upper = raw.upper()
        if raw in labels:
            words.append(labels[raw])
        elif upper in labels:
            words.append(labels[upper])
        else:
            raise ValueError(f"terminology.display_labels is missing label for {raw!r} from {key!r}")
    return " ".join(words)


def shared_execution_block(groups: dict[str, Any], labels: dict[str, str]) -> str:
    entries = shared_execution_entries(groups, labels)
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


def shared_execution_entries(groups: dict[str, Any], labels: dict[str, str]) -> list[tuple[str, list[str]]]:
    if not isinstance(groups, dict):
        return []
    specs = [
        ("integer_alu", "Integer ALU", ("memory", "flags")),
        ("integer_compare", "Compare/Test", ("memory",)),
        ("integer_extend", "Extension", ("memory", "source_sizes_by_destination", "flags")),
        ("data_movement", "Data Movement", ("memory", "flags")),
        ("data_register_banking", "Data Register Banking", ("flags",)),
        ("control_flow", "Control Transfer", ("long_transfer_operands", "atomic_cs_pc_commit", "flags")),
        ("atomics", "Atomics", ("atomic", "memory")),
        ("system_registers", "Control Registers", ("privilege", "flags")),
        ("virtualization_acceleration", "Virtualization Acceleration", ("cpuid_feature", "memory", "privilege", "flags")),
        ("tlb_context", "TLB and Context", ("privilege",)),
        ("cache", "Cache", ("privilege", "flags")),
        ("fpu_move_compare", "Floating-Point Move/Compare", ("fp_flags",)),
        ("fpu_arithmetic", "Floating-Point Arithmetic", ("fp_flags",)),
        ("fpu_transcendental", "Floating-Point Transcendental", ("cpuid_feature", "implementation", "fp_flags")),
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
            if isinstance(value, dict):
                lines.extend(shared_dict_lines(key, value, labels))
            elif key == "atomic":
                lines.append(f"{shared_rule_label(key, labels)}: {readable_text(value)}")
            elif key == "atomic_cs_pc_commit":
                lines.append(f"CS/PC commit is atomic for: {readable_text(value)}")
            elif key == "memory":
                lines.append(f"{shared_rule_label(key, labels)}: {memory_rule_text(value)}")
            else:
                lines.append(f"{shared_rule_label(key, labels)}: {readable_text(value)}")
        if lines:
            entries.append((label, lines))
    return entries


def shared_rule_label(key: str, labels: dict[str, str]) -> str:
    return semantic_label(key, labels)


def shared_dict_lines(key: str, value: dict[str, Any], labels: dict[str, str]) -> list[str]:
    if key == "source_sizes_by_destination":
        return [f"Source sizes for {subkey} destination: {readable_text(subvalue)}" for subkey, subvalue in value.items()]
    if key == "segment_register_forms":
        return [f"{subkey} segment-register form: {readable_text(subvalue)}" for subkey, subvalue in value.items()]
    if key == "segment_registers":
        return [f"{subkey} segment-register operands: {readable_text(subvalue)}" for subkey, subvalue in value.items()]
    if len(value) > 4:
        return [f"{shared_rule_label(key, labels)}: listed per mnemonic"]
    return [f"{shared_rule_label(key, labels)} {subkey}: {readable_text(subvalue)}" for subkey, subvalue in value.items()]


def rep_execution_sequence(repeat: dict[str, Any], prefix: dict[str, Any]) -> str:
    indexed = repeat.get("indexed_ea_counter_use") or {}
    if not isinstance(indexed, dict):
        indexed = {}
    example = indexed.get("example") if isinstance(indexed, dict) else None
    out: list[str] = []
    description = compact_text(repeat.get("description") or prefix.get("description", ""))
    if description:
        out.append(tex_escape(description))
    indexed_note = compact_text(indexed.get("note", ""))
    if indexed_note:
        out.append(tex_escape(indexed_note))
    if example:
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


def rep_observed_rows(repeat: dict[str, Any], prefix: dict[str, Any]) -> list[list[str]]:
    observed = repeat.get("observed_values") or {}
    repflags = repeat.get("repflag_rules") or {}
    observed_descriptions = prefix.get("observed_value_descriptions") or repeat.get("observed_value_descriptions") or {}
    repflags_descriptions = prefix.get("repflags_descriptions") or repeat.get("repflags_descriptions") or {}
    if not isinstance(observed, dict):
        observed = {}
    if not isinstance(repflags, dict):
        repflags = {}
    if not isinstance(observed_descriptions, dict):
        observed_descriptions = {}
    if not isinstance(repflags_descriptions, dict):
        repflags_descriptions = {}
    rows: list[list[str]] = []
    for mnemonic in sorted(set(observed) | set(repflags)):
        rows.append(
            [
                tex_code(mnemonic),
                tex_escape(rep_observed_value_text(observed.get(mnemonic, "-"), observed_descriptions)),
                tex_escape(repflags_rule_text(repflags.get(mnemonic, "-"), repflags_descriptions)),
            ]
        )
    return rows


def rep_observed_value_text(value: Any, descriptions: dict[str, Any]) -> str:
    text = str(value)
    names = {
        "src_value": "source value",
        "rhs_minus_lhs": "right operand minus left operand",
        "lhs_bitwise_and_rhs": "left operand bitwise-and right operand",
        "result_value": "result value",
    }
    return compact_text(descriptions.get(text, names.get(text, readable_text(text))))


def repflags_rule_text(value: Any, descriptions: dict[str, Any]) -> str:
    text = str(value)
    names = {
        "flags_logic_observed_value": "set Z/N from observed value and clear C/V",
        "flags_sub_rhs_lhs": "compute subtract flags from right operand minus left operand",
        "fpu_compare_flags": "floating-point compare flag rules",
        "fpu_interval_v_flag": "set V from interval check",
    }
    return compact_text(descriptions.get(text, names.get(text, readable_text(text))))


def reference_group_mnemonics(
    all_mnemonics: list[str],
    operations: dict[str, list[dict[str, Any]]],
    group_names: set[str],
) -> list[str]:
    selected: set[str] = set()
    for mnemonic, entries in operations.items():
        if any(str(entry.get("group", "")) in group_names for entry in entries):
            selected.add(mnemonic)
    return [mnemonic for mnemonic in all_mnemonics if mnemonic in selected]


def instruction_reference_groups(
    spec: dict[str, Any],
    mnemonics: list[str],
    records: dict[str, list[dict[str, Any]]],
    operations: dict[str, list[dict[str, Any]]],
    mnemonic_items: dict[str, list[dict[str, Any]]],
) -> list[tuple[str, list[str]]]:
    special_groups: list[tuple[str, list[str]]] = []
    claimed: set[str] = set()
    for title, group_names in SEPARATE_INSTRUCTION_GROUPS:
        selected = reference_group_mnemonics(mnemonics, operations, group_names)
        if selected:
            special_groups.append((title, selected))
            claimed.update(selected)

    fpu_set = fpu_mnemonics(spec, records, operations, mnemonic_items)
    general_mnemonics = [mnemonic for mnemonic in mnemonics if mnemonic not in claimed and mnemonic not in fpu_set]
    base_fpu_mnemonics = [mnemonic for mnemonic in mnemonics if mnemonic not in claimed and mnemonic in fpu_set]

    groups: list[tuple[str, list[str]]] = []
    if general_mnemonics:
        groups.append(("General Instructions", general_mnemonics))
    for title, selected in special_groups:
        if not title.startswith("Floating-Point"):
            groups.append((title, selected))
    if base_fpu_mnemonics:
        groups.append(("Floating-Point Instructions", base_fpu_mnemonics))
    for title, selected in special_groups:
        if title.startswith("Floating-Point"):
            groups.append((title, selected))
    return groups



def render_manual(plan: dict[str, Any], spec: dict[str, Any], lengths: dict[tuple[str, str], tuple[int, int]]) -> str:
    return ManualDocument(ManualRenderContext.build(plan, spec, lengths)).render()


def slugify(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return text.strip("-")


def preview_header(title: str) -> str:
    return PreviewHeader(title).render()


def preview_document(title: str, body: str) -> str:
    return LatexSequence([LatexDocumentPreamble(), PreviewHeader(title), body, LatexDocumentEnd()]).render()


def manual_preview_sections(
    plan: dict[str, Any],
    spec: dict[str, Any],
    lengths: dict[tuple[str, str], tuple[int, int]],
) -> list[tuple[str, str, str]]:
    context = ManualRenderContext.build(plan, spec, lengths)
    return [section.as_tuple() for section in ManualPreviewIndex(context).sections()]


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
    return ManualPreviewDocument(ManualRenderContext.build(plan, spec, lengths), requested).render()



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
