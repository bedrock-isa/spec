"""Instruction-reference and instruction-summary LaTeX renderers."""

from __future__ import annotations

from typing import Any
import re

from gen_instruction_specs import allocation_items
from gen_instruction_tables import (
    default_words,
    encoding_pattern_tokens,
    field_layout_text,
    field_symbol,
    line_fields,
    line_syntax_text,
    operand_types_text,
    syntax_text,
)
from .common import (
    FFLAG_MEANINGS,
    FFLAG_ORDER,
    FLAG_ORDER,
    SIZE_NAMES,
    compact_text,
    latex_longtable,
    mdash_join,
    normalize_text,
    pretty_key,
    readable_text,
    render_latex_template,
    tex_code,
    tex_escape,
    tex_table_value,
    top_section,
)
from .diagrams import bit_diagram

def instruction_set_summary_by_class_section(
    spec: dict[str, Any],
    mnemonics: list[str],
    records: dict[str, list[dict[str, Any]]] | None = None,
    operations: dict[str, list[dict[str, Any]]] | None = None,
    items_by_mnemonic: dict[str, list[dict[str, Any]]] | None = None,
) -> str:
    records = records or {}
    operations = operations or {}
    items_by_mnemonic = items_by_mnemonic or {}
    return render_latex_template(
        "instruction_set_summary.tex",
        {
            "CLASS_SUMMARY_TABLE": instruction_class_summary_table(spec, mnemonics),
            "ATTRIBUTE_MATRIX_TABLE": instruction_attribute_matrix_table(
                spec,
                mnemonics,
                records,
                operations,
                items_by_mnemonic,
            ),
        },
    )


def instruction_class_summary_table(spec: dict[str, Any], mnemonics: list[str]) -> str:
    groups = (((spec.get("instructions") or {}).get("operation_semantics") or {}).get("groups") or {})
    if not isinstance(groups, dict):
        return "No instruction class metadata is available.\\par\n"
    known = set(mnemonics)
    rows: list[list[str]] = []
    for name, body in groups.items():
        if not isinstance(body, dict):
            continue
        members = [str(member) for member in body.get("members", []) or []]
        listed_members = [member for member in members if not known or member in known]
        if not listed_members:
            listed_members = members
        rows.append(
            [
                tex_escape(instruction_class_title(str(name))),
                tex_table_value(listed_members),
                tex_escape(instruction_class_note(body)),
            ]
        )
    return latex_longtable(
        ["Class", "Mnemonics", "Notes"],
        rows,
        ["1.25in", "2.25in", "2.0in"],
        "Instruction Classes",
    )


def instruction_class_note(body: dict[str, Any]) -> str:
    notes: list[str] = []
    for key in ("memory", "atomic", "privilege", "flags", "implementation", "traps", "long_transfer_operands"):
        if key in body:
            value = integer_flags_text(body[key]) if key == "flags" else readable_text(body[key])
            notes.append(f"{pretty_key(key)}: {value}")
    for key in ("privilege_by_mnemonic", "flags_by_mnemonic", "fp_flags_by_mnemonic"):
        if key in body:
            notes.append(f"{pretty_key(key)}: varies by mnemonic")
    if "operation_by_mnemonic" in body and not notes:
        operations = body.get("operation_by_mnemonic") or {}
        if isinstance(operations, dict):
            examples = []
            for mnemonic, operation in list(operations.items())[:3]:
                examples.append(f"{mnemonic}: {readable_text(operation)}")
            if examples:
                notes.append("; ".join(examples))
    return "; ".join(notes) if notes else "See individual instruction descriptions."


def instruction_class_title(name: str) -> str:
    replacements = {
        "ea": "EA",
        "tlb": "TLB",
        "fpu": "FPU",
        "alu": "ALU",
    }
    parts = []
    for part in name.replace("-", "_").split("_"):
        lower = part.lower()
        parts.append(replacements.get(lower, part.title()))
    return " ".join(parts)


def instruction_attribute_matrix_table(
    spec: dict[str, Any],
    mnemonics: list[str],
    records: dict[str, list[dict[str, Any]]],
    operations: dict[str, list[dict[str, Any]]],
    items_by_mnemonic: dict[str, list[dict[str, Any]]],
) -> str:
    rows: list[list[str]] = []
    for mnemonic in mnemonics:
        recs = records.get(mnemonic, [])
        ops = operations.get(mnemonic, [])
        items = items_by_mnemonic.get(mnemonic, [])
        if not (recs or ops or items):
            continue
        flag_cells = instruction_flag_cells(recs, ops)
        prefix_cells = instruction_prefix_cells(spec, mnemonic, recs, ops, items)
        rows.append(
            [
                tex_code(mnemonic),
                tex_escape(instruction_privilege_summary(items, recs, ops)),
                *flag_cells,
                *prefix_cells,
            ]
        )
    legend = (
        r"\subsection{Instruction Attribute Matrix}"
        "\n"
        "The following table is a compact availability index. "
        "NOSPEC is a common prefix and is omitted from the per-instruction prefix list. "
        "Address-update forms are operand spellings described in the Effective Addressing and Prefix Model sections, "
        "not a separate per-mnemonic prefix column.\\par\n"
    )
    table = latex_longtable(
        [
            "Instr.",
            "Priv",
            "Z",
            "N",
            "C",
            "V",
            "NV",
            "DZ",
            "OF",
            "UF",
            "NX",
            "SAT",
            "NT",
            "REP",
            "REPcc",
            "REPG",
            "REPGF",
        ],
        rows,
        [
            "0.62in",
            "0.28in",
            "0.13in",
            "0.13in",
            "0.13in",
            "0.13in",
            "0.18in",
            "0.18in",
            "0.18in",
            "0.18in",
            "0.18in",
            "0.22in",
            "0.18in",
            "0.22in",
            "0.32in",
            "0.30in",
            "0.34in",
        ],
        "Instruction Attribute Matrix",
    )
    table = table.replace(
        r"\begingroup\footnotesize",
        r"\begingroup\scriptsize\setlength{\tabcolsep}{2pt}",
        1,
    )
    return legend + instruction_attribute_matrix_legend() + table


def instruction_attribute_matrix_legend() -> str:
    rows = [
        [tex_escape("Priv"), tex_code("U"), tex_escape("all listed forms are unprivileged")],
        [tex_escape("Priv"), tex_code("S"), tex_escape("all listed forms require supervisor privilege")],
        [tex_escape("Priv"), tex_code("mixed"), tex_escape("the mnemonic has both unprivileged and privileged forms")],
        [tex_escape("Flag"), tex_code("Y"), tex_escape("the instruction may update this FLAGS or FFLAGS bit")],
        [tex_escape("Flag"), tex_code("0"), tex_escape("the instruction writes this flag as cleared")],
        [tex_escape("Flag"), tex_code("U"), tex_escape("the flag is unchanged")],
        [tex_escape("Prefix"), tex_code("Y"), tex_escape("at least one form of the mnemonic supports the prefix")],
        [tex_escape("Prefix"), tex_code("-"), tex_escape("the prefix is not applicable to this mnemonic")],
        [tex_code("SAT"), tex_code("Y/-"), tex_escape("SATURATE prefix is applicable or not applicable")],
        [tex_code("NT"), tex_code("Y/-"), tex_escape("NONTEMPORAL hint is applicable or not applicable to memory forms")],
        [tex_code("REP"), tex_code("Y/-"), tex_escape("unconditional repeat form is legal or not legal")],
        [tex_code("REPcc"), tex_code("Y/-"), tex_escape("conditional repeat form is legal or not legal")],
        [tex_code("REPG"), tex_code("Y/-"), tex_escape("grouped repeat form is legal or not legal")],
        [tex_code("REPGF"), tex_code("Y/-"), tex_escape("fast grouped-repeat contract form is legal or not legal")],
    ]
    return latex_longtable(
        ["Column", "Cell", "Meaning"],
        rows,
        ["0.75in", "0.45in", "4.0in"],
        "Instruction Attribute Matrix Legend",
    )


def instruction_privilege_summary(
    items: list[dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    values = {privilege_text(item_privilege(item, records, operations)) for item in items}
    if not values:
        for record in operations + records:
            value = (record.get("spec") or {}).get("privilege")
            if value:
                values.add(privilege_text(str(value)))
    if not values:
        values.add("unprivileged")
    short = {privilege_code(value) for value in values}
    if len(short) == 1:
        return next(iter(short))
    if "U" in short and ("S" in short or "policy" in short or "state" in short):
        return "mixed"
    return "/".join(sorted(short))


def privilege_code(value: str) -> str:
    normalized = readable_text(value).lower()
    if normalized in {"unprivileged", "user allowed", "any"}:
        return "U"
    if normalized in {"supervisor", "privileged"}:
        return "S"
    if "policy" in normalized or "configurable" in normalized:
        return "policy"
    if "state register" in normalized:
        return "state"
    if "spr" in normalized or "control register" in normalized:
        return "S"
    return readable_text(value)


def instruction_flags_summary(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> str:
    text = flags_text(records, operations)
    if not text:
        return "unchanged"
    if "FFLAGS" in text:
        return "unchanged"
    return short_flag_effect_text(text)


def short_flag_effect_text(text: str) -> str:
    readable = readable_text(text)
    normalized = readable.lower().replace("-", "_").replace("/", "_").replace(" ", "_")
    if normalized in {"unchanged", "flags_unchanged"}:
        return "unchanged"
    if "address_flags" in normalized:
        return "addr optional"
    if "status_result_optional" in normalized:
        return "status optional"
    if "update_optional" in normalized:
        return "optional"
    if "update_zncv" in normalized or "zncv" in normalized:
        return "ZNCV"
    if "update_zn_clear_cv" in normalized or ("zn" in normalized and "clear_cv" in normalized):
        return "ZN; C/V=0"
    if "z_from_not_old_bit" in normalized:
        return "Z=!old; N/C/V unchanged"
    if "zn_optional" in normalized or ("zn" in normalized and "optional" in normalized):
        return "ZN optional"
    if "compare_result" in normalized or "compare" in normalized:
        return "compare"
    if "old_bit" in normalized:
        return "old bit"
    if "v:" in readable.lower() or normalized.startswith("v_") or " v " in f" {readable.lower()} ":
        return "V"
    if "unchanged_or_update_zn" in normalized:
        return "unchanged/ZN"
    return abbreviate_text(readable, 28)


def instruction_fflags_summary(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> str:
    text = flags_text(records, operations)
    is_fpu = any(record_is_fpu(record) for record in records + operations) or any(item_is_fpu(item) for item in items)
    if "FFLAGS" not in text:
        return "unchanged" if is_fpu else "-"
    if "unchanged" in text.lower():
        return "unchanged"
    names = [name for name in FFLAG_ORDER if f"FFLAGS.{name}" in text]
    if names:
        return ",".join(names)
    return abbreviate_text(readable_text(text), 28)


def instruction_flag_cells(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> list[str]:
    text = flags_text(records, operations)
    if "FFLAGS" in text:
        integer_marks = {flag: "-" for flag in FLAG_ORDER}
        floating_marks = fflag_marks(text)
    else:
        integer_marks = flag_marks(text or "unchanged")
        floating_marks = {flag: "-" for flag in FFLAG_ORDER}
    return [flag_matrix_cell(integer_marks[flag]) for flag in FLAG_ORDER] + [
        flag_matrix_cell(floating_marks[flag]) for flag in FFLAG_ORDER
    ]


def flag_matrix_cell(mark: str) -> str:
    if mark == "*":
        return "Y"
    if mark == "0":
        return "0"
    return "U"


def instruction_prefix_summary(
    spec: dict[str, Any],
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> str:
    semantics = ((spec.get("instructions") or {}).get("operation_semantics") or {})
    rules = semantics.get("prefix_availability") or {}
    if not isinstance(rules, dict):
        return "-"
    attrs = semantics.get("operation_attributes") or {}
    codes: list[str] = []
    for name, rule in rules.items():
        if not isinstance(rule, dict):
            continue
        if rule.get("scope") == "all_instructions":
            continue
        if prefix_rule_applies(rule, mnemonic, attrs, records, operations, items):
            codes.append(str(rule.get("table_code") or name))
    return ", ".join(codes) if codes else "-"


def instruction_prefix_cells(
    spec: dict[str, Any],
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> list[str]:
    semantics = ((spec.get("instructions") or {}).get("operation_semantics") or {})
    rules = semantics.get("prefix_availability") or {}
    attrs = semantics.get("operation_attributes") or {}
    repeatable = mnemonic in operation_attribute_members(attrs, "repeatable_operation")
    streaming = mnemonic in operation_attribute_members(attrs, "streaming_candidate")

    def rule_cell(name: str) -> str:
        rule = rules.get(name) if isinstance(rules, dict) else None
        if not isinstance(rule, dict):
            return "-"
        return availability_cell(prefix_rule_applies(rule, mnemonic, attrs, records, operations, items))

    return [
        rule_cell("SATURATE"),
        rule_cell("NONTEMPORAL"),
        availability_cell(repeatable),
        availability_cell(repeatable),
        availability_cell(repeatable),
        availability_cell(streaming),
    ]


def availability_cell(enabled: bool) -> str:
    return "Y" if enabled else "-"


def prefix_rule_applies(
    rule: dict[str, Any],
    mnemonic: str,
    attributes: dict[str, Any],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> bool:
    if rule.get("scope") == "all_instructions":
        return True
    explicit = {str(value) for value in rule.get("mnemonics", []) or []}
    if mnemonic in explicit:
        return True
    attr_name = rule.get("operation_attribute")
    if attr_name and mnemonic in operation_attribute_members(attributes, str(attr_name)):
        return True
    general_only = {str(value) for value in rule.get("general_only_mnemonics", []) or []}
    if mnemonic in general_only:
        return True
    derived = rule.get("derived_from")
    if derived == "memory_operand":
        return instruction_has_memory_prefix_candidate(mnemonic, records, operations, items)
    if derived in {"update_eligible_ea", "update-eligible EA"}:
        return instruction_has_update_prefix_candidate(mnemonic, records, operations, items)
    return False


def operation_attribute_members(attributes: dict[str, Any], name: str) -> set[str]:
    return collect_attribute_mnemonics(
        attributes.get(name),
        skip_keys={"excluded_categories", "state_query_general_only"},
    )


def collect_attribute_mnemonics(value: Any, skip_keys: set[str]) -> set[str]:
    if isinstance(value, list):
        return {str(item) for item in value if isinstance(item, str) and item[:1].isupper()}
    if isinstance(value, dict):
        out: set[str] = set()
        for key, child in value.items():
            if str(key) in skip_keys:
                continue
            out.update(collect_attribute_mnemonics(child, skip_keys))
        return out
    return set()


def instruction_has_memory_prefix_candidate(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> bool:
    if mnemonic in {"JMP", "Jcc", "CALL", "LCALL", "LJMP", "DJcc"}:
        return False
    if instruction_is_no_memory_access(records, operations):
        return False
    return instruction_has_ea_operand(items)


def instruction_has_update_prefix_candidate(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> bool:
    return instruction_has_memory_prefix_candidate(mnemonic, records, operations, items)


def instruction_is_no_memory_access(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> bool:
    for record in operations + records:
        spec = record.get("spec") or {}
        if spec.get("no_memory_access") is True:
            return True
        if spec.get("canonical_address_check_only") is True:
            return True
        pcode = spec.get("pcode") or spec.get("pcode_by_mnemonic") or []
        if isinstance(pcode, list) and pcode and all("read_memory" not in str(line) and "write_memory" not in str(line) for line in pcode):
            if any("effective_address" in str(line) or "segment_translate" in str(line) for line in pcode):
                return True
    return False


def instruction_has_ea_operand(items: list[dict[str, Any]]) -> bool:
    for item in items:
        if any(":EA" in str(operand) or str(operand).endswith("EA") for operand in item.get("operands", []) or []):
            return True
        if any(str(field.get("kind")) == "EA" for field in item.get("fields", []) or []):
            return True
    return False


def abbreviate_text(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def condition_code_computation_section() -> str:
    return render_latex_template("condition_code_computation.tex")


def instruction_description_intro_section() -> str:
    return render_latex_template("instruction_description_intro.tex")


def c_library_instruction_examples_section() -> str:
    return render_latex_template("c_library_instruction_examples.tex")


def opcode_instruction_format_summary_section(plan: dict[str, Any]) -> str:
    items = allocation_items(plan)
    primary_allocations = list(plan.get("primary_allocations", []) or [])
    primary_aliases = list(plan.get("primary_alias_allocations", []) or [])
    extension_roots = [item for item in primary_allocations if item.get("kind") == "extension_root"]
    compact_primary = [item for item in primary_allocations if item.get("kind") != "extension_root"] + primary_aliases
    parts = [
        "This appendix summarizes the generated opcode and field structure. It is a reading guide for the "
        "instruction format diagrams and generated encoding tables; the declarative specification remains the source of truth.",
        r"\subsection{Instruction Word Stack}",
        "Every instruction starts with word 0. Word 0 supplies the prefix-present bit, the total instruction length, "
        "and the twelve-bit primary payload. Compact forms decode directly from that payload. Extended forms use a "
        "primary root and a following 16-bit extended opcode or descriptor word.",
        latex_longtable(
            ["Word", "Purpose"],
            [
                [tex_escape("word 0"), tex_escape("prefix-present bit, encoded instruction length, and primary payload")],
                [tex_escape("word 1, when P=1"), tex_escape("two prefix bytes, decoded from low byte to high byte")],
                [tex_escape("extended opcode word"), tex_escape("family-local subopcode and generated operand descriptor fields")],
                [tex_escape("payload words"), tex_escape("immediates, displacements, absolute addresses, bitmaps, or extended-EA descriptors")],
            ],
            ["1.35in", "4.05in"],
            "Instruction Word Roles",
        ),
        r"\subsection{Primary Payload Map}",
        primary_payload_overview_text(plan, compact_primary, extension_roots),
        latex_longtable(
            ["Payload", "Use", "Form", "Fields"],
            primary_payload_rows(compact_primary, extension_roots),
            ["0.75in", "1.35in", "2.25in", "1.10in"],
            "Primary Payload Summary",
        ),
        r"\subsection{Extension Root Summary}",
        "Extension roots are primary payload entries that open a family-local 16-bit extended opcode space. "
        "The allocator keeps related roots together so that primary instruction classification can group families before "
        "examining the extended word.",
        latex_longtable(
            ["Root Payload", "Family", "Members", "Root Fields"],
            extension_root_rows(extension_roots),
            ["0.78in", "1.65in", "0.62in", "2.35in"],
            "Extension Roots",
        ),
        r"\subsection{Generated Field Catalog}",
        "The allocator places conceptual fields in reusable bit positions when doing so improves decode regularity. "
        "The table below lists the field kinds that appear in allocated forms and the storage locations observed in the generated layouts.",
        latex_longtable(
            ["Field Kind", "Width", "Common Storage", "Typical Roles"],
            field_catalog_rows(items),
            ["1.05in", "0.55in", "2.15in", "1.75in"],
            "Generated Operand Field Catalog",
        ),
    ]
    return "\n".join(parts)


def primary_payload_overview_text(
    plan: dict[str, Any],
    compact_primary: list[dict[str, Any]],
    extension_roots: list[dict[str, Any]],
) -> str:
    target = plan.get("target_space", {}) or {}
    solver = plan.get("solver", {}) or {}
    payload_range = target.get("payload_range", "0x000..0xfff")
    bits = target.get("bits", 12)
    compact_count = len([item for item in compact_primary if item.get("kind") != "compact_alias"])
    alias_count = len([item for item in compact_primary if item.get("kind") == "compact_alias"])
    root_count = len(extension_roots)
    used = solver.get("primary_used_slot_count")
    free = solver.get("primary_free_slot_count")
    summary = (
        f"The primary payload is {bits} bits wide and spans {payload_range}. "
        f"The current generated map contains {compact_count} compact primary forms, {alias_count} primary aliases, "
        f"and {root_count} extension roots."
    )
    if used is not None and free is not None:
        summary += f" It uses {used} primary payload slots and leaves {free} unallocated slots."
    return tex_escape(summary)


def primary_payload_rows(compact_primary: list[dict[str, Any]], extension_roots: list[dict[str, Any]]) -> list[list[str]]:
    rows = []
    for item in sorted(compact_primary + extension_roots, key=payload_sort_key):
        kind = str(item.get("kind", ""))
        if kind == "extension_root":
            use = "extension root"
            form = instruction_class_title(str(item.get("group", item.get("id", ""))))
        elif kind == "compact_alias":
            use = "canonical alias"
            form = f"{item.get('mnemonic', item.get('id', ''))} alias of {item.get('alias_of', '-')}"
        else:
            use = instruction_class_title(str(item.get("category", item.get("group", "compact"))))
            form = payload_form_text(item)
        rows.append(
            [
                tex_code(payload_range_text(item)),
                tex_escape(use),
                tex_escape(form),
                tex_escape(primary_field_summary(item)),
            ]
        )
    return rows


def extension_root_rows(extension_roots: list[dict[str, Any]]) -> list[list[str]]:
    rows = []
    for item in sorted(extension_roots, key=payload_sort_key):
        rows.append(
            [
                tex_code(payload_range_text(item)),
                tex_escape(instruction_class_title(str(item.get("group", item.get("id", ""))))),
                tex_escape(item.get("member_count", "-")),
                tex_escape(readable_text(item.get("field_layout", "subop/operands in following word"))),
            ]
        )
    return rows


def field_catalog_rows(items: list[dict[str, Any]]) -> list[list[str]]:
    catalog: dict[tuple[str, str], dict[str, set[str]]] = {}
    for item in items:
        for field in item.get("fields", []) or []:
            kind = str(field.get("kind", field.get("name", "")))
            width = str(field_width(field))
            key = (kind, width)
            entry = catalog.setdefault(key, {"storage": set(), "roles": set()})
            entry["storage"].add(field_storage_text(field))
            source = str(field.get("source", field.get("name", "")))
            entry["roles"].add(role_name(source))
    rows = []
    for (kind, width), entry in sorted(catalog.items(), key=lambda pair: (pair[0][0], pair[0][1])):
        rows.append(
            [
                tex_escape(kind_description(kind)),
                tex_escape(width),
                tex_table_value(entry["storage"]),
                tex_table_value(entry["roles"]),
            ]
        )
    return rows


def payload_sort_key(item: dict[str, Any]) -> tuple[int, str]:
    return (parse_hex_int(item.get("start_payload", "0x0")), str(item.get("id", "")))


def payload_range_text(item: dict[str, Any]) -> str:
    start = str(item.get("start_payload", "") or "")
    end = str(item.get("end_payload", "") or start)
    return start if not end or start == end else f"{start}..{end}"


def payload_form_text(item: dict[str, Any]) -> str:
    try:
        return line_syntax_text(item, line_fields(item))
    except Exception:
        return str(item.get("id", item.get("mnemonic", "-")))


def primary_field_summary(item: dict[str, Any]) -> str:
    if item.get("kind") == "extension_root":
        return readable_text(item.get("field_layout", "subop/operands in following word"))
    fields = [field for field in item.get("fields", []) or [] if field.get("storage", "primary") == "primary"]
    if not fields:
        return readable_text(item.get("field_layout", "no primary operand fields"))
    return "; ".join(field_position_summary(field) for field in fields)


def field_position_summary(field: dict[str, Any]) -> str:
    symbol = field_symbol(field)
    kind = field.get("kind", "")
    if "high_bit" in field and "low_bit" in field:
        high = int(field.get("high_bit", 0))
        low = int(field.get("low_bit", 0))
        bit_text = str(low) if high == low else f"{high}:{low}"
        return f"{symbol}:{kind}[{bit_text}]"
    return f"{symbol}:{kind}/{field_width(field)}"


def field_width(field: dict[str, Any]) -> int:
    if "width" in field:
        return int(field.get("width", 0))
    if "high_bit" in field and "low_bit" in field:
        return int(field.get("high_bit", 0)) - int(field.get("low_bit", 0)) + 1
    return 0


def field_storage_text(field: dict[str, Any]) -> str:
    storage = str(field.get("storage", "primary"))
    if "high_bit" in field and "low_bit" in field:
        high = int(field.get("high_bit", 0))
        low = int(field.get("low_bit", 0))
        bit_text = str(low) if high == low else f"{high}:{low}"
        return f"{storage}[{bit_text}]"
    return storage


def parse_hex_int(value: Any) -> int:
    text = str(value or "0")
    try:
        return int(text, 16)
    except ValueError:
        return 0

def instruction_reference_sections(
    title: str,
    mnemonics: list[str],
    records: dict[str, list[dict[str, Any]]],
    operations: dict[str, list[dict[str, Any]]],
    items_by_mnemonic: dict[str, list[dict[str, Any]]],
    aliases: dict[str, list[str]],
    lengths: dict[tuple[str, str], tuple[int, int]],
    docs: dict[str, dict[str, Any]],
) -> list[str]:
    if not mnemonics:
        return []
    summary_caption = f"Table {'10-1' if title.startswith('Floating-Point') else '9-1'}. {title} Summary"
    parts = [
        top_section(f"{title} Summary"),
        instruction_summary(mnemonics, records, operations, items_by_mnemonic, docs, summary_caption),
        top_section(f"{title} Descriptions"),
    ]
    if title.startswith("General"):
        parts.append(instruction_description_intro_section())
    for mnemonic in mnemonics:
        parts.append(
            render_instruction(
                mnemonic,
                records.get(mnemonic, []),
                operations.get(mnemonic, []),
                items_by_mnemonic.get(mnemonic, []),
                aliases.get(mnemonic, []),
                lengths,
                docs,
            )
        )
    return parts


def fpu_mnemonics(
    spec: dict[str, Any],
    records: dict[str, list[dict[str, Any]]],
    operations: dict[str, list[dict[str, Any]]],
    items_by_mnemonic: dict[str, list[dict[str, Any]]],
) -> set[str]:
    out: set[str] = set()
    families = spec.get("instructions", {}).get("instruction_families", {}) or {}
    if isinstance(families, dict):
        for family_name, body in families.items():
            if "fpu" not in str(family_name).lower():
                continue
            members = body.get("members", []) if isinstance(body, dict) else body
            if isinstance(members, list):
                out.update(str(member) for member in members)
    for mnemonic, items in items_by_mnemonic.items():
        if any(item_is_fpu(item) for item in items):
            out.add(mnemonic)
    for mnemonic, entries in records.items():
        if any(record_is_fpu(entry) for entry in entries):
            out.add(mnemonic)
    for mnemonic, entries in operations.items():
        if any(record_is_fpu(entry) for entry in entries):
            out.add(mnemonic)
    return out


def item_is_fpu(item: dict[str, Any]) -> bool:
    for key in ("category", "family", "extension_family", "extension_root", "group", "root"):
        value = str(item.get(key, "")).lower()
        if value == "fpu" or value.startswith("fpu_") or ".fpu_" in value:
            return True
    return False


def record_is_fpu(record: dict[str, Any]) -> bool:
    for key in ("category", "family", "group", "unit"):
        value = str(record.get(key, "")).lower()
        if value == "fpu" or value.startswith("fpu_"):
            return True
    spec = record.get("spec", {})
    if isinstance(spec, dict):
        for key in ("category", "family", "group", "unit"):
            value = str(spec.get(key, "")).lower()
            if value == "fpu" or value.startswith("fpu_"):
                return True
    return False


def instruction_summary(
    mnemonics: list[str],
    records: dict[str, list[dict[str, Any]]],
    operations: dict[str, list[dict[str, Any]]],
    items_by_mnemonic: dict[str, list[dict[str, Any]]],
    docs: dict[str, dict[str, Any]],
    caption: str | None = None,
) -> str:
    rows = []
    for mnemonic in mnemonics:
        rows.append(
            [
                tex_code(mnemonic),
                tex_escape(doc_title(mnemonic, docs, records.get(mnemonic, []), operations.get(mnemonic, []))),
                tex_escape(len(items_by_mnemonic.get(mnemonic, []))),
            ]
        )
    return latex_longtable(
        ["Mnemonic", "Summary", "Forms"],
        rows,
        ["0.82in", "4.18in", "0.42in"],
        caption,
    )


def render_instruction(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
    aliases: list[str],
    lengths: dict[tuple[str, str], tuple[int, int]],
    docs: dict[str, dict[str, Any]],
) -> str:
    title = doc_title(mnemonic, docs, records, operations)
    lines = [rf"\instrhead{{{tex_escape(mnemonic)}}}{{{tex_escape(title)}}}{{}}"]
    lines.append(rf"\manualfield{{Summary:}}{{{tex_escape(doc_summary(mnemonic, docs, records, operations, items))}}}")
    lines.append(rf"\manualfield{{Operation:}}{{{operation_latex(operations)}}}")
    lines.append(rf"\manualfield{{Assembler Syntax:}}{{{syntax_block(items)}}}")
    lines.append(rf"\manualfield{{Attributes:}}{{{attribute_text(items, records, operations, lengths)}}}")
    lines.append(rf"\manualfield{{Description:}}{{{doc_description(mnemonic, docs, records, operations, aliases)}}}")
    lines.append(condition_code_section(records, operations))
    lines.append(instruction_forms_section(items, lengths, records, operations))
    return "\n".join(lines)


def doc_title(
    mnemonic: str,
    docs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    entry = docs.get(mnemonic, {})
    if entry.get("title"):
        return compact_text(entry["title"])
    return fallback_instruction_title(mnemonic, records, operations)


def doc_summary(
    mnemonic: str,
    docs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> str:
    entry = docs.get(mnemonic, {})
    if entry.get("summary"):
        return compact_text(entry["summary"])
    return short_description_text(mnemonic, records, operations, items)


def doc_description(
    mnemonic: str,
    docs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    aliases: list[str],
) -> str:
    entry = docs.get(mnemonic, {})
    if entry.get("description"):
        text = compact_text(entry["description"])
        if aliases:
            text += " " + alias_description(aliases)
        return tex_escape(text)
    return description_text(records, operations, aliases)


def alias_description(aliases: list[str]) -> str:
    return "Aliases: " + "; ".join(sorted(set(readable_text(alias) for alias in aliases))) + "."


def fallback_instruction_title(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    name = mnemonic.replace("cc", " Condition")
    if name.startswith("F") and len(name) > 1:
        return "Floating " + pretty_key(name[1:])
    if name.startswith("BND"):
        return "Bounds Check"
    if mnemonic:
        return pretty_key(name)
    return instruction_title(records, operations)


def instruction_title(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> str:
    for record in records:
        family = str(record.get("family", ""))
        if family:
            return pretty_key(family)
    for record in operations:
        group = str(record.get("group", ""))
        if group:
            return pretty_key(group)
    return "Instruction"


def instruction_family(records: list[dict[str, Any]]) -> str:
    categories = sorted({str(record.get("category", "")) for record in records if record.get("category")})
    families = sorted({str(record.get("family", "")) for record in records if record.get("family")})
    return mdash_join(categories + families)


def operation_text(operations: list[dict[str, Any]]) -> str:
    texts = operation_texts(operations)
    return "; ".join(dict.fromkeys(texts)) if texts else "Operation is specified by the instruction semantic catalog."


def operation_texts(operations: list[dict[str, Any]]) -> list[str]:
    pcode = pcode_operation_texts(operations)
    if pcode:
        return pcode
    texts = []
    for record in operations:
        spec = record.get("spec", {})
        for key in ("operation", "effect", "effects", "performs", "computes", "result"):
            if key in spec:
                texts.append(compact_text(spec[key]))
                break
    return list(dict.fromkeys(texts))


def pcode_operation_texts(operations: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for record in operations:
        spec = record.get("spec", {})
        if "pcode" not in spec:
            continue
        for statement in pcode_statements(spec["pcode"]):
            text = pcode_statement_text(statement)
            if text:
                lines.append(text)
    return list(dict.fromkeys(lines))


def pcode_statements(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [part.strip() for part in value.splitlines() if part.strip()]
    if isinstance(value, dict):
        return [value]
    return []


def pcode_statement_text(statement: Any) -> str:
    if isinstance(statement, dict):
        return pcode_dict_statement_text(statement)
    text = str(statement).strip()
    if not text:
        return ""

    match = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*read_operand\((.*)\)$", text)
    if match:
        target, args = match.groups()
        arg_list = pcode_args(args)
        source = arg_list[0] if arg_list else "operand"
        return f"Read {pcode_operand_text(source)} into {pcode_name_text(target)}."

    match = re.match(r"^write_operand\((.*)\)$", text)
    if match:
        args = pcode_args(match.group(1))
        destination = pcode_operand_text(args[0]) if args else "destination"
        value = pcode_expr_text(args[1]) if len(args) > 1 else "the computed value"
        return f"Write {value} to {destination}."

    match = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*read_memory\((.*)\)$", text)
    if match:
        target, args = match.groups()
        location = pcode_memory_location(args)
        return f"Read memory at {location} into {pcode_name_text(target)}."

    match = re.match(r"^write_memory\((.*)\)$", text)
    if match:
        args = pcode_args(match.group(1))
        location = pcode_memory_location(", ".join(args[:2])) if len(args) >= 2 else "the selected address"
        value = pcode_expr_text(args[2]) if len(args) > 2 else "the computed value"
        return f"Write {value} to memory at {location}."

    match = re.match(r"^FLAGS\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", text)
    if match:
        primitive, args = match.groups()
        return f"Update FLAGS using {pcode_primitive_text(primitive)} for {pcode_expr_text(args)}."

    match = re.match(r"^raise_?exception\((.*)\)$", text)
    if match:
        return f"Raise {readable_text(match.group(1))} exception."

    match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", text)
    if match:
        primitive, args = match.groups()
        if primitive in {"atomic_begin", "atomic_end"}:
            arg_list = pcode_args(args)
            location = pcode_operand_text(arg_list[0]) if arg_list else "the memory operand"
            order = pcode_name_text(arg_list[1]) if len(arg_list) > 1 else "the selected memory-order value"
            action = pcode_primitive_text(primitive)
            return f"{action} for {location} with {order}."
        if primitive == "write_cr":
            arg_list = pcode_args(args)
            selector = pcode_operand_text(arg_list[0]) if arg_list else "the selected control register"
            value = pcode_expr_text(arg_list[1]) if len(arg_list) > 1 else "the value"
            return f"Write {value} to {selector}."
        arg_text = pcode_expr_text(args) if args.strip() else ""
        action = pcode_primitive_text(primitive)
        return f"{action}." if not arg_text else f"{action} for {arg_text}."

    match = re.match(r"^if\s+(.+?)\s+then\s+write_operand\((.*)\)\s+else\s+(.+)$", text)
    if match:
        condition, args, otherwise = match.groups()
        arg_list = pcode_args(args)
        destination = pcode_operand_text(arg_list[0]) if arg_list else "destination"
        value = pcode_expr_text(arg_list[1]) if len(arg_list) > 1 else "the computed value"
        return (
            f"If {pcode_expr_text(condition)}, write {value} to {destination}; "
            f"otherwise {readable_text(otherwise)}."
        )

    match = re.match(r"^if\s+(.+?)\s+then\s+raise_?exception\((.*)\)\s+else\s+(.+)$", text)
    if match:
        condition, exception, otherwise = match.groups()
        return (
            f"If {pcode_expr_text(condition)}, raise {readable_text(exception)} exception; "
            f"otherwise {readable_text(otherwise)}."
        )

    match = re.match(r"^if\s+(.+?)\s+then\s+(.+?)\s+else\s+(.+)$", text)
    if match:
        condition, then_text, otherwise = match.groups()
        then_rendered = pcode_statement_text(then_text).rstrip(".")
        return (
            f"If {pcode_expr_text(condition)}, {then_rendered[0].lower() + then_rendered[1:]}; "
            f"otherwise {readable_text(otherwise)}."
        )

    match = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*(.+)$", text)
    if match:
        target, expr = match.groups()
        return f"Set {pcode_name_text(target)} to {pcode_expr_text(expr)}."

    match = re.match(r"^(.+?)\s*=\s*(.+)$", text)
    if match:
        target, expr = match.groups()
        return f"Set {pcode_name_text(target)} to {pcode_expr_text(expr)}."

    if text.startswith("for_each_"):
        return readable_text(text) + "."
    return readable_text(text) + ("." if not text.endswith(".") else "")


def pcode_dict_statement_text(statement: dict[str, Any]) -> str:
    if "read" in statement:
        return f"Read {pcode_operand_text(statement.get('from', 'operand'))} into {pcode_name_text(statement['read'])}."
    if "write" in statement:
        value = pcode_expr_text(statement.get("value", "the computed value"))
        return f"Write {value} to {pcode_operand_text(statement['write'])}."
    if "set" in statement:
        return f"Set {pcode_name_text(statement['set'])} to {pcode_expr_text(statement.get('expr', 'value'))}."
    if "flags" in statement:
        source = statement.get("from", "the result")
        return f"Update FLAGS using {readable_text(statement['flags'])} from {pcode_expr_text(source)}."
    if "trap" in statement:
        prefix = f"If {pcode_expr_text(statement['when'])}, " if statement.get("when") else ""
        return prefix + f"raise {readable_text(statement['trap'])} exception."
    if "note" in statement:
        return readable_text(statement["note"]) + "."
    return readable_text(statement) + "."


def pcode_args(text: Any) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in str(text):
        if ch == "," and depth == 0:
            part = "".join(current).strip()
            if part:
                args.append(part)
            current = []
            continue
        current.append(ch)
        if ch in "([{":
            depth += 1
        elif ch in ")]}" and depth:
            depth -= 1
    part = "".join(current).strip()
    if part:
        args.append(part)
    return args


def pcode_memory_location(args_text: Any) -> str:
    args = pcode_args(args_text)
    if len(args) >= 2:
        return f"{pcode_expr_text(args[0])}:{pcode_expr_text(args[1])}"
    if args:
        return pcode_expr_text(args[0])
    return "the selected address"


def pcode_operand_text(value: Any) -> str:
    text = str(value)
    names = {
        "src": "the source operand",
        "dst": "the destination operand",
        "lhs": "the left operand",
        "rhs": "the right operand",
        "target": "the target operand",
        "new_cs": "the new CS operand",
        "counter": "the counter operand",
        "count": "the count operand",
        "bit_index": "the bit-index operand",
        "lo": "the low-bound operand",
        "hi": "the high-bound operand",
        "value": "the value operand",
        "expected": "the expected operand",
        "desired": "the desired operand",
        "memory": "the memory operand",
        "order": "the memory-order qualifier",
        "quotient": "the quotient/dividend register",
        "remainder": "the remainder register",
        "page": "the page operand",
        "outputs": "the output operand",
        "cr": "the control-register selector",
        "asid": "the ASID operand",
        "src_or_dst": "the tested operand",
    }
    return names.get(text, pcode_expr_text(text))


def pcode_name_text(value: Any) -> str:
    text = str(value)
    names = {
        "src_v": "the source value",
        "dst_v": "the destination value",
        "result, carry": "the result and carry-out",
        "lhs_v": "the left operand value",
        "rhs_v": "the right operand value",
        "result": "the result",
        "carry": "the carry input",
        "borrow": "the borrow input",
        "old": "the old value",
        "old_bit": "the old bit value",
        "not old_bit": "not the old bit value",
        "target": "the target address",
        "dividend": "the dividend",
        "quotient_v": "the quotient",
        "remainder_v": "the remainder",
        "count_v": "the count value",
        "bit_index_v": "the bit index",
        "lo_v": "the low bound",
        "hi_v": "the high bound",
        "value_v": "the checked value",
        "expected_v": "the expected value",
        "desired_v": "the desired value",
        "order_v": "the memory-order value",
        "new_cs_v": "the new CS value",
        "target_v": "the target address",
        "return_pc": "the return PC",
        "return_cs": "the return CS",
        "counter_v": "the counter value",
        "counter_next": "the decremented counter",
        "address": "the effective address",
        "walk_result": "the page-walk result",
    }
    return names.get(text, pcode_expr_text(text))


def pcode_primitive_text(value: Any) -> str:
    names = {
        "flags_add": "addition flag rules",
        "flags_sub": "subtraction flag rules",
        "flags_logic": "logical-result flag rules",
        "flags_add_with_carry": "add-with-carry flag rules",
        "flags_sub_with_borrow": "subtract-with-borrow flag rules",
        "flags_abs": "absolute-value flag rules",
        "flags_shift_left": "shift-left flag rules",
        "flags_shift_right": "logical-shift-right flag rules",
        "flags_shift_arithmetic_right": "arithmetic-shift-right flag rules",
        "flags_rotate_left": "rotate-left flag rules",
        "flags_rotate_right": "rotate-right flag rules",
        "flags_rotate_through_carry_left": "rotate-through-carry-left flag rules",
        "flags_rotate_through_carry_right": "rotate-through-carry-right flag rules",
        "floating_compare_flags": "floating-point compare flag rules",
        "no_state_change": "Make no architectural state change",
        "enter_halt_state_until_event": "Enter the halted state until an enabled event resumes execution",
        "perform_warm_reset_preserving_boot_state": "Perform a warm reset while preserving BOOTPC and BOOTCFG",
        "restore_syscall_frame": "Restore the syscall return frame",
        "restore_interrupt_frame": "Restore the interrupt return frame",
        "save_syscall_frame_and_enter_supervisor": "Save the syscall frame and enter the supervisor entry state",
        "wait_for_event_or_interrupt": "Wait for an event or interrupt according to privilege policy",
        "yield_hint": "Provide an implementation scheduling hint",
        "order_reads_before_later_reads": "Order prior reads before later reads",
        "order_writes_before_later_writes": "Order prior writes before later writes",
        "order_memory_before_later_memory": "Order prior memory operations before later memory operations",
        "emit_trace_marker_if_enabled": "Emit a trace marker when tracing is enabled",
        "atomic_begin": "Begin the atomic read-modify-write sequence",
        "atomic_end": "Complete the atomic read-modify-write sequence",
        "write_cr": "Write the selected control register",
        "serializing_boundary": "Execute a serializing boundary",
        "update_tlb_context": "Update the active TLB context",
        "invalidate_tlb_all": "Invalidate all TLB entries",
        "invalidate_tlb_page": "Invalidate the selected TLB page entry",
        "invalidate_tlb_asid": "Invalidate TLB entries for the selected ASID",
        "perform_page_walk": "Perform a page-table walk",
        "store_core_context": "Store the core context",
        "load_core_context": "Load the core context",
        "store_extended_context": "Store the dirty extended context",
        "load_extended_context": "Load the dirty extended context",
        "prefetch_memory": "Issue a prefetch hint",
        "invalidate_data_cache": "Invalidate data cache state",
        "invalidate_instruction_cache": "Invalidate instruction cache state",
        "flush_data_cache": "Flush data cache state",
        "writeback_data_cache": "Write back data cache state",
        "synchronize_instruction_data_caches": "Synchronize instruction and data cache visibility",
    }
    return names.get(str(value), readable_text(value))


def pcode_expr_text(value: Any) -> str:
    text = str(value).strip()
    exact = {
        "result": "the result",
        "value": "the value",
        "selected_register": "the selected register",
    }
    if text in exact:
        return exact[text]
    replacements = {
        "src_v": "source value",
        "dst_v": "destination value",
        "lhs_v": "left operand value",
        "rhs_v": "right operand value",
        "count_v": "count value",
        "bit_index_v": "bit index",
        "lo_v": "low bound",
        "hi_v": "high bound",
        "value_v": "checked value",
        "expected_v": "expected value",
        "desired_v": "desired value",
        "new_cs_v": "new CS value",
        "target_v": "target address",
        "dividend": "dividend",
        "quotient_v": "quotient",
        "remainder_v": "remainder",
        "return_pc": "return PC",
        "return_cs": "return CS",
        "counter_v": "counter value",
        "counter_next": "decremented counter",
        "FLAGS.C": "FLAGS.C",
    }
    for old, new in replacements.items():
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    text = text.replace(" & ", " bitwise AND ")
    text = text.replace(" | ", " bitwise OR ")
    text = text.replace(" ^ ", " bitwise XOR ")
    return readable_text(text)


def operation_latex(operations: list[dict[str, Any]]) -> str:
    pcode = pcode_operation_texts(operations)
    if pcode:
        return wrapped_operation_block([tex_escape(row) for row in pcode])
    texts = operation_texts(operations)
    if not texts:
        return tex_escape("Operation is specified by the instruction semantic catalog.")
    rows = []
    for text in texts:
        for piece in [part.strip() for part in text.split(";") if part.strip()]:
            rows.append(operation_piece_latex(piece))
    return wrapped_operation_block(rows)


def wrapped_operation_block(rows: list[str]) -> str:
    if not rows:
        return ""
    body = r"\par ".join(r"\noindent " + row for row in rows)
    return r"\begin{minipage}[t]{\hsize}\raggedright " + body + r"\end{minipage}"


def operation_piece_latex(text: str) -> str:
    if re.search(r"\braise\b", text, re.IGNORECASE):
        return tex_escape(readable_text(text))
    if expression_like(text):
        return r"\ensuremath{" + math_expression(text) + "}"
    return tex_escape(readable_text(text))


def expression_like(text: str) -> bool:
    stripped = text.strip()
    if re.match(r"(?i)^if\b.+\bthen\b", stripped):
        return True
    if re.search(r"(?<![-<>=!])=(?![=>])|[&|^%]|\[[A-Za-z_]", stripped):
        return True
    return bool(re.search(r"\b(min|max|extend|read|write|class|sqrt|sin|cos|tan|log)\w*\(", stripped))


def math_expression(text: str) -> str:
    protected = (
        text.replace("fall through", "fall_through")
        .replace("do not store tmp", "do_not_store_tmp")
    )
    tokens = re.findall(
        r"0x[0-9A-Fa-f]+|[A-Za-z_][A-Za-z0-9_.]*|==|!=|<=|>=|<<|>>|->|<-|[+\-*/&|^%=(),\[\]]|\S",
        protected,
    )
    out: list[str] = []
    for index, token in enumerate(tokens):
        lower = token.lower()
        next_token = tokens[index + 1] if index + 1 < len(tokens) else ""
        if lower in {"if", "then", "else"}:
            out.append(r"\operatorname{" + lower + "}")
        elif token in {"=", "<-"}:
            out.append(r"\leftarrow")
        elif token == "->":
            out.append(r"\rightarrow")
        elif token == "<=":
            out.append(r"\le")
        elif token == ">=":
            out.append(r"\ge")
        elif token == "!=":
            out.append(r"\ne")
        elif token == "==":
            out.append(r"=")
        elif token == "&":
            out.append(r"\mathbin{\&}")
        elif token == "|":
            out.append(r"\mathbin{|}")
        elif token == "^":
            out.append(r"\mathbin{\oplus}")
        elif token == "%":
            out.append(r"\bmod")
        elif re.match(r"^[A-Za-z_][A-Za-z0-9_.]*$", token):
            name = token.replace("_", r"\_")
            if lower == "not_in":
                out.append(r"\notin")
            elif lower in {"and", "or", "not"}:
                out.append(r"\operatorname{" + lower + "}")
            elif next_token == "(" or lower in {"unsigned_min", "signed_min", "unsigned_max", "signed_max"}:
                out.append(r"\operatorname{" + name + "}")
            elif token in {"C", "V", "Z", "N"}:
                out.append(token)
            else:
                out.append(r"\mathit{" + name + "}")
        else:
            out.append(tex_math_symbol(token))
    return " ".join(out)


def tex_math_symbol(token: str) -> str:
    mapping = {"{": r"\{", "}": r"\}", "#": r"\#", "$": r"\$"}
    return mapping.get(token, tex_escape(token))


def short_description_text(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> str:
    operation = operation_text(operations)
    if operation and "semantic catalog" not in operation:
        sentence = readable_text(operation)
        if not sentence.endswith("."):
            sentence += "."
    else:
        title = instruction_title(records, operations).lower()
        sentence = f"{mnemonic} is a {title} instruction."

    forms = []
    seen = set()
    for item in items:
        fields = line_fields(item)
        label = form_label(item, fields)
        if label in seen:
            continue
        seen.add(label)
        forms.append(label)
        if len(forms) == 4:
            break
    if forms:
        sentence += " Forms: " + "; ".join(forms) + "."
    return sentence


def syntax_block(items: list[dict[str, Any]]) -> str:
    syntaxes = []
    seen = set()
    for item in items:
        text = syntax_text(item)
        if text in seen:
            continue
        seen.add(text)
        syntaxes.append(tex_code(text))
    if not syntaxes:
        return "No allocated syntax."
    return r"\begin{tabular}[t]{@{}l@{}}" + r"\\".join(syntaxes) + r"\end{tabular}"


def attribute_text(
    items: list[dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    lengths: dict[tuple[str, str], tuple[int, int]],
) -> str:
    sizes = sorted({str(item.get("size", "")) for item in instruction_rows_for_attrs(items) if str(item.get("size", "")) not in {"", "-"}})
    words = sorted({f"{default_words(item, lengths)[0]}-{default_words(item, lengths)[1]}" for item in items})
    flags = flags_text(records, operations)
    attrs = []
    if sizes:
        attrs.append("Size = (" + ", ".join(size_label(size) for size in sizes) + ")")
    if words:
        attrs.append("Words = (" + ", ".join(words) + ")")
    privileges = sorted({privilege_text(item_privilege(item, records, operations)) for item in items})
    if privileges:
        if len(privileges) == 1:
            attrs.append("Privilege = " + privileges[0])
        else:
            attrs.append("Privilege = mixed by form")
    if flags:
        if "FFLAGS" in flags:
            attrs.append("FFLAGS = see Floating-Point Status")
        else:
            attrs.append("Flags = " + readable_text(flags))
    if not attrs:
        return tex_escape("No explicit attributes.")
    return r"\begin{tabular}[t]{@{}l@{}}" + r"\\".join(tex_escape(attr) for attr in attrs) + r"\end{tabular}"


def privilege_text(value: str) -> str:
    if isinstance(value, dict):
        base = value.get("level") or value.get("default") or value.get("mode") or ""
        if value.get("policy_controlled"):
            normalized = f"{base}_or_policy_controlled" if base else "policy_controlled"
        else:
            normalized = str(base)
    else:
        normalized = str(value or "").strip()
    if normalized in {"", "any", "user_allowed", "unprivileged"}:
        return "unprivileged"
    return readable_text(normalized)


def item_privilege(
    item: dict[str, Any],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    raw_value = item.get("privilege")
    if isinstance(raw_value, dict):
        value = privilege_text(raw_value)
    else:
        value = str(raw_value or "").strip()
    if value:
        return value
    operands = [str(operand) for operand in item.get("operands", []) or []]
    if any(operand.endswith(":SREG") or ":SREG" in operand for operand in operands):
        if any(operand.startswith("dst:SREG") for operand in operands):
            return "policy_controlled"
        return "depends_on_state_register"
    for record in operations + records:
        spec = record.get("spec", {})
        value = spec.get("privilege")
        if isinstance(value, dict):
            return privilege_text(value)
        if value:
            return str(value)
    return "unprivileged"


def instruction_rows_for_attrs(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for item in items:
        row = dict(item)
        fields = item.get("fields", [])
        row["size"] = next((str(field.get("kind")) for field in fields if field.get("source") == "size"), item.get("fixed_size_suffix", ""))
        out.append(row)
    return out


def size_label(size: str) -> str:
    if "/" in size:
        return size
    if size in {"BWLQ", "BWLX"}:
        return "Byte, Word, Long, Quad"
    if size == "BWL":
        return "Byte, Word, Long"
    if size == "BW":
        return "Byte, Word"
    if size == "LQ":
        return "Long, Quad"
    if size == "WL":
        return "Word, Long"
    return SIZE_NAMES.get(size, size)


def description_text(records: list[dict[str, Any]], operations: list[dict[str, Any]], aliases: list[str]) -> str:
    bits = []
    for record in operations:
        spec = record.get("spec", {})
        for key in (
            "inputs",
            "output",
            "source_size_suffix",
            "destination_size",
            "destination_size_by_mnemonic",
            "source_sizes_by_destination",
            "memory",
            "state_register_forms",
            "state_registers",
            "implementation",
            "privilege",
            "traps",
            "updates",
            "reads",
            "writes",
            "repeat_observed_value",
            "repeat_observed_value_by_mnemonic",
            "zero_input",
            "signedness",
            "bounds_mode",
            "nan_policy",
            "commit_rule",
        ):
            if key in spec:
                bits.append(f"{pretty_key(key)}: {readable_text(spec[key])}")
    for record in records:
        spec = record.get("spec", {})
        for key in (
            "notes",
            "description",
            "privilege",
            "traps",
            "atomic",
            "memory_memory",
            "access_width",
            "constraint",
            "stack_segment",
            "stack_register",
            "bitmap",
            "valid_bits",
            "state_register_access",
            "prefixes",
            "source_size",
            "destination_size",
            "source_sizes",
            "destination_sizes",
            "source_sizes_by_destination",
            "destination_size_by_mnemonic",
        ):
            if key in spec:
                bits.append(f"{pretty_key(key)}: {readable_text(spec[key])}")
    if aliases:
        bits.append("Aliases: " + "; ".join(sorted(set(aliases))))
    return tex_escape(" ".join(bits) if bits else "See operation, syntax, and instruction field descriptions.")


def user_encoding_text(item: dict[str, Any]) -> str:
    if item.get("kind") in {"compact", "compact_alias"}:
        start = str(item.get("start_payload", "") or "")
        end = str(item.get("end_payload", "") or "")
        if item.get("kind") == "compact_alias":
            return "canonical alias in primary opcode space"
        if start and end and start != end:
            return f"primary opcode range {start} to {end}"
        if start:
            return f"primary opcode {start}"
        return "primary opcode space"
    if item.get("kind") == "extended_alias":
        return "canonical alias in extended opcode space"
    return "extended opcode form"


def form_label(item: dict[str, Any], fields: list[dict[str, Any]] | None = None) -> str:
    fields = fields if fields is not None else line_fields(item)
    syntax = line_syntax_text(item, fields)
    if " " not in syntax:
        return syntax
    return syntax.split(" ", 1)[1]


def word_name(token: int) -> str:
    if token == 0:
        return "primary word"
    if token == 1:
        return "descriptor word"
    return f"payload word {token - 1}"


def role_name(source: str) -> str:
    names = {
        "src": "source operand",
        "dst": "destination operand",
        "lhs": "left operand",
        "rhs": "right operand",
        "target": "branch target",
        "counter": "counter register",
        "memory": "memory operand",
        "expected": "expected value",
        "desired": "desired value",
        "size": "operand size",
        "cc": "condition code",
        "condition": "condition code",
        "regs": "register bitmap",
        "reg": "register operand",
        "lo": "lower bound operand",
        "hi": "upper bound operand",
        "quotient": "quotient/dividend register",
        "remainder": "remainder register",
        "new_cs": "new code-segment value",
        "new_ptcr": "new page-table-control value",
        "asid": "address-space identifier",
        "cr": "control-register selector",
        "order": "ordering mode",
    }
    return names.get(source, source.replace("_", " "))


def kind_description(kind: str) -> str:
    mapping = {
        "EA": "compact effective-address field",
        "DREG": "data register number",
        "AREG": "address register number",
        "SPREG": "stack pointer register",
        "SREG": "state register number",
        "CR": "control-register selector",
        "memory_order": "atomic memory-order value",
        "cr": "control-register selector",
        "FREG": "floating-point register number",
        "condition": "condition-code selector",
        "imm16": "16-bit immediate selector",
        "BITMAP16": "16-bit register bitmap",
        "bitmap16": "16-bit register bitmap",
        "LQ": "size selector",
        "WL": "size selector",
        "BW": "size selector",
        "BWL": "size selector",
        "BWLQ": "size selector",
        "S_D": "floating-point size selector",
    }
    if kind in SIZE_NAMES:
        return f"fixed {SIZE_NAMES[kind]} size"
    return mapping.get(kind, kind.replace("_", " ").lower())


def field_explanation_lines(item: dict[str, Any], fields: list[dict[str, Any]]) -> list[str]:
    if not fields:
        return ["No explicit operand fields are encoded in this form."]
    lines = []
    for field in fields:
        token = int(field.get("token", 0))
        high = int(field.get("high_bit", 0))
        low = int(field.get("low_bit", 0))
        bit_text = str(low) if high == low else f"{high}:{low}"
        symbol = field_symbol(field)
        source = str(field.get("source", field.get("name", "")))
        kind = str(field.get("kind", ""))
        line = (
            f"{symbol}: {kind_description(kind)} for the {role_name(source)} "
            f"({word_name(token)} bits {bit_text})."
        )
        if kind == "EA":
            line += " Register, memory, immediate, and extended EA forms are selected by this field."
        lines.append(line)
    if any(str(field.get("kind")) == "EA" for field in fields):
        lines.append("EA selections may append displacement, absolute-address, immediate, or extended-EA payload words.")
    return lines


def field_explanation_block(item: dict[str, Any], fields: list[dict[str, Any]]) -> str:
    rows = [r"\par\noindent\begin{tabularx}{\linewidth}{@{}p{0.28in}X@{}}"]
    for line in field_explanation_lines(item, fields):
        if ":" in line:
            symbol, rest = line.split(":", 1)
            rows.append(rf"{tex_code(symbol)} & {tex_escape(rest.strip())}\\")
        else:
            rows.append(rf" & {tex_escape(line)}\\")
    rows.append(r"\end{tabularx}\par")
    return "\n".join(rows)


def readable_operands_text(item: dict[str, Any]) -> str:
    operands = []
    for operand in item.get("operands", []) or []:
        text = str(operand)
        if ":" in text:
            name, kind = text.split(":", 1)
            if kind == "memory_order":
                continue
            operands.append(f"{role_name(name)} is {kind_description(kind)}")
        else:
            operands.append(readable_text(text))
    return "; ".join(operands) if operands else "no explicit operands"


def readable_note_text(note: str) -> str:
    replacements = {
        "primary root + extended opcode + descriptor": "uses an extended opcode word and an operand descriptor",
        "primary root + extended opcode": "uses an extended opcode word",
        "EA forms may add displacement/extended-EA words": "EA forms may add displacement or extended-EA payload words",
        "EA forms may add words": "EA forms may add extra payload words",
        "overlong padding allowed": "instruction length may be longer than the minimum; extra words are padding",
    }
    text = note
    for old, new in replacements.items():
        text = text.replace(old, new)
    return readable_text(text)


def flags_text(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> str:
    for record in operations:
        spec = record.get("spec", {})
        if "flags" in spec:
            return integer_flags_text(spec["flags"])
        if "fp_flags" in spec:
            return fp_flags_text(spec["fp_flags"])
    for record in records:
        spec = record.get("spec", {})
        if "flags" in spec:
            return integer_flags_text(spec["flags"])
        if "fp_flags" in spec:
            return fp_flags_text(spec["fp_flags"])
    return ""


def integer_flags_text(value: Any) -> str:
    if isinstance(value, dict):
        if value.get("mode") == "per_shift":
            return "update ZNCV by shift/rotate count rules"
        if "status_result" in value:
            return "operation-defined status result"
        flag_keys = [key for key in FLAG_ORDER if key in value]
        if flag_keys:
            return "; ".join(f"{key}: {readable_text(value[key])}" for key in flag_keys)
        return readable_text(value)
    return normalize_text(value)


def fp_flags_text(value: Any) -> str:
    if isinstance(value, dict):
        if "update" in value:
            return "may update " + fflags_list_text(value["update"])
        if "update_when_required" in value:
            return "may update " + fflags_list_text(value["update_when_required"]) + " when the operation signals a floating-point exception"
        if value.get("unchanged") is True:
            return "FFLAGS unchanged"
        return readable_text(value)
    text = str(value)
    if text == "unchanged":
        return "FFLAGS unchanged"
    if text == "update_FFLAGS":
        return "may update " + fflags_list_text(FFLAG_ORDER)
    if text == "update_when_conversion_or_compare_requires":
        return "may update " + fflags_list_text(FFLAG_ORDER) + " when the conversion or comparison signals a floating-point exception"
    if text.startswith("update_FFLAGS_"):
        suffix = text.removeprefix("update_FFLAGS_")
        names = [part for part in suffix.split("_") if part in FFLAG_MEANINGS]
        if names:
            return "may update " + fflags_list_text(names)
    return readable_text(text)


def fflags_list_text(flags: Any) -> str:
    if isinstance(flags, str):
        names = [flags]
    else:
        names = [str(flag) for flag in flags]
    expanded = [f"FFLAGS.{name} ({FFLAG_MEANINGS.get(name, name)})" for name in names]
    return ", ".join(expanded)


def condition_code_section(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> str:
    text = flags_text(records, operations) or "unchanged"
    if "FFLAGS" in text:
        flags = fflag_marks(text)
        rows = [
            " & ".join(r"\textbf{" + flag + "}" for flag in FFLAG_ORDER) + r"\\",
            " & ".join(tex_escape(flags[flag]) for flag in FFLAG_ORDER) + r"\\",
        ]
        table = r"\begin{tabular}[t]{@{}ccccc@{}}" + "\n" + "\n".join(rows) + "\n" + r"\end{tabular}"
        return rf"\manualfield{{Floating-Point Status:}}{{{status_detail_block(table, text)}}}"
    flags = flag_marks(text)
    rows = [
        " & ".join(r"\textbf{" + flag + "}" for flag in FLAG_ORDER) + r"\\",
        " & ".join(tex_escape(flags[flag]) for flag in FLAG_ORDER) + r"\\",
    ]
    table = r"\begin{tabular}[t]{@{}cccc@{}}" + "\n" + "\n".join(rows) + "\n" + r"\end{tabular}"
    return rf"\manualfield{{Condition Codes:}}{{{status_detail_block(table, readable_text(text))}}}"


def status_detail_block(table: str, text: str) -> str:
    return (
        r"\begin{minipage}[t]{\hsize}"
        + table
        + r"\par\smallskip "
        + tex_escape(text)
        + r"\end{minipage}"
    )


def fflag_marks(text: str) -> dict[str, str]:
    if "unchanged" in text.lower():
        return {flag: "-" for flag in FFLAG_ORDER}
    return {flag: "*" if f"FFLAGS.{flag}" in text else "-" for flag in FFLAG_ORDER}


def flag_marks(text: str) -> dict[str, str]:
    lower = text.lower()
    normalized = lower.replace("-", "_").replace("/", "_").replace(" ", "_")
    marks = {flag: "-" for flag in FLAG_ORDER}
    if "unchanged" in lower:
        return marks
    if "clear_cv" in normalized or "clear_c_v" in normalized:
        marks.update({"Z": "*", "N": "*", "C": "0", "V": "0"})
        return marks
    if "zncv" in lower or "z_n_c_v" in normalized or "subtract" in lower or "compare" in lower:
        return {flag: "*" for flag in FLAG_ORDER}
    if "update z/n" in lower or "may update z/n" in lower or "z_n" in normalized or "zn" in lower:
        marks.update({"Z": "*", "N": "*"})
    if "set z" in lower or "z:" in lower or "z=" in lower:
        marks["Z"] = "*"
    if "v:" in lower or "v =" in lower or "v_" in lower:
        marks["V"] = "*"
    return marks


def instruction_format_section(items: list[dict[str, Any]]) -> str:
    if not items:
        return r"\manualfield{Instruction Format:}{No allocated instruction format.}"
    blocks = [r"\par\noindent\textbf{Instruction Format:}\par"]
    for item in items:
        fields = line_fields(item)
        syntax = line_syntax_text(item, fields)
        tokens = encoding_pattern_tokens(item, fields)
        labels = [f"word {index}" for index in range(len(tokens))]
        blocks.append(r"\Needspace{1.8in}")
        blocks.append(r"\par\vspace{7pt}\noindent\begin{minipage}{\linewidth}\footnotesize")
        blocks.append(rf"\textbf{{Form:}} {tex_escape(form_label(item, fields))}\par")
        blocks.append(rf"\textbf{{Syntax:}} {tex_code(syntax)}\par")
        blocks.append(bit_diagram(tokens, f"Instruction format for {syntax}", labels))
        blocks.append(field_explanation_block(item, fields))
        blocks.append(r"\end{minipage}\par")
    return "\n".join(blocks)


def instruction_forms_section(
    items: list[dict[str, Any]],
    lengths: dict[tuple[str, str], tuple[int, int]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    if not items:
        return r"\manualfield{Instruction Forms:}{No allocated instruction forms.}"
    blocks = [r"\par\vspace{6pt}\noindent\textbf{Instruction Forms:}\par"]
    for item in items:
        min_words, max_words, note = default_words(item, lengths)
        fields = line_fields(item)
        syntax = line_syntax_text(item, fields)
        tokens = encoding_pattern_tokens(item, fields)
        labels = [f"word {index}" for index in range(len(tokens))]
        blocks.append(r"\Needspace{2.9in}")
        blocks.append(r"\par\vspace{7pt}\noindent\begin{minipage}{\linewidth}\footnotesize")
        blocks.append(rf"\textbf{{{tex_code(syntax)}}}\par")
        blocks.append(r"\vspace{2pt}")
        blocks.append(r"\begin{tabularx}{\linewidth}{@{}p{0.88in}X@{}}")
        blocks.append(rf"\textbf{{Form}} & {tex_escape(form_label(item, fields))}\\")
        blocks.append(rf"\textbf{{Encoding}} & {tex_escape(user_encoding_text(item))}\\")
        blocks.append(rf"\textbf{{Words}} & {tex_escape(f'{min_words}-{max_words}')}\\")
        blocks.append(rf"\textbf{{Privilege}} & {tex_escape(privilege_text(item_privilege(item, records, operations)))}\\")
        blocks.append(rf"\textbf{{Operands}} & {tex_escape(readable_operands_text(item))}\\")
        blocks.append(rf"\textbf{{Notes}} & {tex_escape(readable_note_text(note))}\\")
        blocks.append(r"\end{tabularx}\par")
        blocks.append(bit_diagram(tokens, f"Instruction format for {syntax}", labels))
        blocks.append(field_explanation_block(item, fields))
        blocks.append(r"\end{minipage}\par")
    return "\n".join(blocks)


def instruction_fields_section(
    items: list[dict[str, Any]],
    lengths: dict[tuple[str, str], tuple[int, int]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    if not items:
        return r"\manualfield{Encoding Notes:}{No allocated encoding notes.}"
    blocks = [r"\par\vspace{6pt}\noindent\textbf{Encoding Notes:}\par"]
    for item in items:
        min_words, max_words, note = default_words(item, lengths)
        fields = line_fields(item)
        blocks.append(r"\Needspace{0.65in}")
        blocks.append(r"\par\smallskip\noindent\begin{tabularx}{\linewidth}{@{}p{0.95in}X@{}}")
        blocks.append(rf"\textbf{{Form}} & {tex_escape(form_label(item, fields))}\\")
        blocks.append(rf"\textbf{{Encoding}} & {tex_escape(user_encoding_text(item))}\\")
        blocks.append(rf"\textbf{{Words}} & {tex_escape(f'{min_words}-{max_words}')}\\")
        blocks.append(rf"\textbf{{Privilege}} & {tex_escape(privilege_text(item_privilege(item, records, operations)))}\\")
        blocks.append(rf"\textbf{{Operands}} & {tex_escape(readable_operands_text(item))}\\")
        blocks.append(rf"\textbf{{Notes}} & {tex_escape(readable_note_text(note))}\\")
        blocks.append(r"\end{tabularx}\par")
    return "\n".join(blocks)


def field_summary_text(item: dict[str, Any]) -> str:
    fields = line_fields(item)
    if not fields:
        raw = field_layout_text(item)
        return raw if raw else "no explicit operand fields"
    pieces = []
    for field in fields:
        token = int(field.get("token", 0))
        word = "word0" if token == 0 else ("descriptor" if token == 1 else f"payload{token - 1}")
        high = int(field.get("high_bit", 0))
        low = int(field.get("low_bit", 0))
        bit_text = str(low) if high == low else f"{high}:{low}"
        pieces.append(
            f"{field_symbol(field)}={field.get('source', field.get('name', ''))}:"
            f"{field.get('kind', '')}[{bit_text}] in {word}"
        )
    return "; ".join(pieces)
