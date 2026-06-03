"""Instruction-reference and instruction-summary LaTeX renderers."""

from __future__ import annotations

from typing import Any
import re

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
    hidden_top_section,
    top_section,
)
from .diagrams import bit_diagram


def instruction_label(mnemonic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", mnemonic.lower()).strip("-")
    return f"instr:{slug or 'unknown'}"


def instruction_link(mnemonic: str) -> str:
    return rf"\hyperref[{instruction_label(mnemonic)}]{{{tex_code(mnemonic)}}}"


def instruction_link_list(mnemonics: list[str]) -> str:
    if not mnemonics:
        return tex_escape("-")
    return ", ".join(instruction_link(mnemonic) for mnemonic in mnemonics)


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
                instruction_link_list(listed_members),
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
                instruction_link(mnemonic),
                tex_code(instruction_privilege_summary(items, recs, ops)),
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
        [tex_escape("Priv"), tex_code("P"), tex_escape("at least one listed form is policy-controlled or configurable")],
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
    if "U" in short and ("S" in short or "P" in short or "state" in short):
        return "mixed"
    return "/".join(sorted(short))


def privilege_code(value: str) -> str:
    normalized = readable_text(value).lower()
    if normalized in {"unprivileged", "user allowed", "any"}:
        return "U"
    if normalized in {"supervisor", "privileged"}:
        return "S"
    if "policy" in normalized or "configurable" in normalized:
        return "P"
    if "segment register" in normalized:
        return "P"
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
        return tex_code("Y")
    if mark == "0":
        return tex_code("0")
    return tex_code("U")


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
            return tex_code("-")
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
    return tex_code("Y" if enabled else "-")


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


def runtime_instruction_examples_section() -> str:
    return render_latex_template("runtime_instruction_examples.tex")


def primary_payload_overview_text(
    plan: dict[str, Any],
    compact_primary: list[dict[str, Any]],
    extension_roots: list[dict[str, Any]],
    *,
    escaped: bool = True,
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
    return tex_escape(summary) if escaped else summary


def ragged_paragraph(text: str) -> str:
    return r"\begingroup\raggedright " + tex_escape(text) + r"\par\endgroup"


def prefix_byte_matrix(spec: dict[str, Any]) -> str:
    prefixes = (spec.get("prefixes") or {}).get("prefixes") or []
    cells: dict[int, tuple[str, str]] = {}
    for prefix in prefixes:
        if not isinstance(prefix, dict):
            continue
        label = prefix_grid_label(prefix)
        color = prefix_grid_color(str(prefix.get("group", "")))
        for value in prefix_values(prefix):
            cells[value] = (label, color)
    return "\n".join(
        [
            matrix_legend(prefix_grid_legend_rows()),
            opcode_grid_picture(
                "Prefix byte values",
                cells,
                "prefix[7:4]",
                "prefix[3:0]",
                cell_size="0.48cm",
                min_label_area=4,
                label_singletons=True,
                label_as_code=True,
            ),
        ]
    )


def primary_payload_matrices(compact_primary: list[dict[str, Any]], extension_roots: list[dict[str, Any]]) -> str:
    cells: dict[int, tuple[str, str]] = {}
    for item in sorted(compact_primary + extension_roots, key=payload_sort_key):
        label = primary_grid_label(item)
        color = primary_grid_color(item)
        for value in primary_payload_values(item):
            if 0 <= value <= 0xFFF:
                cells[value] = (label, color)
    solid_pages: dict[int, tuple[str, str]] = {}
    boards: list[str] = []
    for high in range(0x10):
        board_cells = {
            value & 0xFF: cell
            for value, cell in cells.items()
            if (value >> 8) == high
        }
        if len(board_cells) == 256 and len(set(board_cells.values())) == 1:
            solid_pages[high] = next(iter(board_cells.values()))
            continue
        boards.append(primary_payload_board(high, board_cells))
    return two_column_boards(
        "\n".join(
            [
                matrix_legend(primary_grid_legend_rows()),
                r"\par\smallskip",
                primary_page_strip(solid_pages),
            ]
        ),
        boards,
    )


def two_column_boards(legend: str, boards: list[str]) -> str:
    lines = [legend, r"\par\smallskip"]
    for index in range(0, len(boards), 2):
        left = boards[index]
        right = boards[index + 1] if index + 1 < len(boards) else ""
        lines.append(r"\Needspace{3.0in}")
        lines.append(r"\noindent\begin{minipage}[t]{0.49\linewidth}")
        lines.append(left)
        lines.append(r"\end{minipage}")
        if right:
            lines.append(r"\hfill\begin{minipage}[t]{0.49\linewidth}")
            lines.append(right)
            lines.append(r"\end{minipage}")
        lines.append(r"\par\smallskip")
    return "\n".join(lines)


def primary_payload_board(high_nibble: int, cells: dict[int, tuple[str, str]]) -> str:
    title = f"Primary payload 0x{high_nibble:x}00..0x{high_nibble:x}ff"
    return opcode_grid_picture(
        title,
        cells,
        "bits 7..4",
        "bits 3..0",
        cell_size="0.34cm",
        min_label_area=8,
        label_singletons=False,
        label_as_code=True,
    )


def primary_page_strip(solid_pages: dict[int, tuple[str, str]]) -> str:
    if not solid_pages:
        return ""
    rects = matrix_rectangles({page: cell for page, cell in solid_pages.items()})
    lines = [
        r"\begingroup\scriptsize",
        r"\centerline{\textbf{Solid 0xH00 primary pages}}",
        r"\vspace{2pt}",
        r"\begin{center}",
        r"\begin{tikzpicture}[x=0.60cm,y=0.42cm]",
    ]
    for page in range(16):
        lines.append(rf"\node[font=\tiny] at ({page + 0.5:.2f},0.22) {{{page:X}}};")
    lines.append(r"\draw[black!18,line width=0.10pt] (0,0) grid (16,-1);")
    for _row0, _row1, col0, col1, label, color in rects:
        lines.append(
            rf"\filldraw[fill={color},draw=black,line width=0.28pt] "
            rf"({col0},0) rectangle ({col1 + 1},-1);"
        )
        lines.append(
            rf"\node[font=\tiny,align=center,inner sep=0.5pt] at "
            rf"({(col0 + col1 + 1) / 2:.2f},-0.5) {{{matrix_label_code(label)}}};"
        )
    lines.extend(
        [
            r"\draw[black,line width=0.35pt] (0,0) rectangle (16,-1);",
            r"\end{tikzpicture}",
            r"\end{center}",
            r"\endgroup",
        ]
    )
    return "\n".join(lines)


def extended_payload_overview_text(
    plan: dict[str, Any],
    extended_items: list[dict[str, Any]],
    *,
    escaped: bool = True,
) -> str:
    space = plan.get("extended_space", {}) or {}
    bits = space.get("bits", 16)
    opcode_range = space.get("opcode_range", "0x0000..0xffff")
    root_count = len({str(item.get("extension_root", "")) for item in extended_items if item.get("extension_root")})
    used_slots = sum(int(item.get("extended_opcode_slots", 0) or 0) for item in extended_items)
    form_count = len([item for item in extended_items if item.get("kind") != "extended_alias"])
    alias_count = len([item for item in extended_items if item.get("kind") == "extended_alias"])
    summary = (
        f"The extended opcode payload is {bits} bits wide and spans {opcode_range} inside each primary extension root. "
        f"The current generated map contains {form_count} extended forms, {alias_count} extended aliases, "
        f"and {root_count} root-local payload spaces. Across all roots, allocated forms occupy {used_slots} payload slots."
    )
    return tex_escape(summary) if escaped else summary


def extended_payload_matrices(extended_items: list[dict[str, Any]]) -> str:
    if not extended_items:
        return tex_escape("No extended opcode payload allocations are present.")

    by_root: dict[str, list[dict[str, Any]]] = {}
    for item in extended_items:
        root = str(item.get("extension_root", "") or "EXT.unknown")
        by_root.setdefault(root, []).append(item)

    parts = [matrix_legend(extended_grid_legend_rows())]
    for root, items in sorted(by_root.items(), key=lambda pair: extended_root_sort_key(pair[1], pair[0])):
        rendered = extended_root_payload_matrices(root, items)
        if rendered:
            parts.append(rendered)
    return "\n".join(parts)


def extended_root_sort_key(items: list[dict[str, Any]], root: str) -> tuple[int, str]:
    payloads = [parse_hex_int(item.get("extension_root_payload")) for item in items if item.get("extension_root_payload")]
    return (min(payloads) if payloads else 0xFFFF, root)


def extended_root_payload_matrices(root: str, items: list[dict[str, Any]]) -> str:
    cells: dict[int, tuple[str, str]] = {}
    for item in sorted(items, key=extended_payload_sort_key):
        label = extended_grid_label(item)
        color = extended_grid_color(item)
        start, end = extended_opcode_range(item)
        for value in range(max(0, start), min(0xFFFF, end) + 1):
            cells[value] = (label, color)

    if not cells:
        return ""

    solid_pages: dict[int, tuple[str, str]] = {}
    mixed_pages: dict[int, dict[int, tuple[str, str]]] = {}
    for high_byte in range(0x100):
        board_cells = {
            value & 0xFF: cell
            for value, cell in cells.items()
            if (value >> 8) == high_byte
        }
        if not board_cells:
            continue
        if len(board_cells) == 256 and len(set(board_cells.values())) == 1:
            solid_pages[high_byte] = next(iter(board_cells.values()))
        else:
            mixed_pages[high_byte] = board_cells

    page_cells = dict(solid_pages)
    for high_byte in mixed_pages:
        page_cells[high_byte] = ("mixed", "gray!16")

    boards = [
        extended_payload_board(high_byte, board_cells)
        for high_byte, board_cells in sorted(mixed_pages.items())
    ]
    parts = [
        r"\Needspace{4.4in}",
        rf"\noindent\textbf{{{tex_code(root)}}}\par",
        r"\vspace{2pt}",
        extended_payload_page_overview(root, page_cells),
    ]
    if boards:
        parts.append(two_column_boards("", boards))
    return "\n".join(parts)


def extended_payload_page_overview(root: str, cells: dict[int, tuple[str, str]]) -> str:
    return opcode_grid_picture(
        f"{root} extended payload pages",
        cells,
        "bits 15..12",
        "bits 11..8",
        cell_size="0.32cm",
        min_label_area=8,
        label_singletons=False,
        label_as_code=True,
    )


def extended_payload_board(high_byte: int, cells: dict[int, tuple[str, str]]) -> str:
    title = f"extended payload 0x{high_byte:02x}00..0x{high_byte:02x}ff"
    return opcode_grid_picture(
        title,
        cells,
        "bits 7..4",
        "bits 3..0",
        cell_size="0.34cm",
        min_label_area=8,
        label_singletons=False,
        label_as_code=True,
    )


def opcode_grid_picture(
    title: str,
    cells: dict[int, tuple[str, str]],
    row_label: str,
    col_label: str,
    *,
    cell_size: str = "0.36cm",
    min_label_area: int = 4,
    label_singletons: bool = True,
    label_as_code: bool = False,
) -> str:
    rects = matrix_rectangles(cells)
    code_by_label: dict[str, str] = {}
    code_entries: list[tuple[str, str]] = []
    lines = [
        r"\begingroup\scriptsize",
        rf"\centerline{{\textbf{{{tex_escape(title)}}}}}",
        r"\vspace{2pt}",
        r"\begin{center}",
        rf"\begin{{tikzpicture}}[x={cell_size},y={cell_size}]",
        r"\node[anchor=east,font=\tiny] at (0.75,-8.8) {" + tex_escape(row_label) + r"};",
        r"\node[anchor=south,font=\tiny] at (9,0.72) {" + tex_escape(col_label) + r"};",
    ]
    for col in range(16):
        lines.append(rf"\node[font=\tiny] at ({1.5 + col:.2f},0.22) {{{col:X}}};")
    for row in range(16):
        lines.append(rf"\node[font=\tiny] at (0.55,{-1.5 - row:.2f}) {{{row:X}}};")
    lines.append(r"\draw[black!14,line width=0.08pt] (1,-1) grid (17,-17);")
    for guide in range(0, 17, 4):
        lines.append(rf"\draw[black!35,line width=0.18pt] ({1 + guide},-1) -- ({1 + guide},-17);")
        lines.append(rf"\draw[black!35,line width=0.18pt] (1,{-1 - guide}) -- (17,{-1 - guide});")
    for row0, row1, col0, col1, label, color in rects:
        x0 = 1 + col0
        x1 = 1 + col1 + 1
        y0 = -1 - row0
        y1 = -1 - row1 - 1
        lines.append(
            rf"\filldraw[fill={color},draw=black,line width=0.28pt] "
            rf"({x0},{y0}) rectangle ({x1},{y1});"
        )
        area = (row1 - row0 + 1) * (col1 - col0 + 1)
        width = col1 - col0 + 1
        height = row1 - row0 + 1
        if label and should_label_grid_rect(area, width, height, min_label_area, label_singletons):
            font = r"\tiny"
            if area >= 24:
                font = r"\scriptsize"
            label_text = matrix_label_code(label) if label_as_code else tex_escape(label)
            lines.append(
                rf"\node[font={font},align=center,inner sep=0.4pt] at "
                rf"({(x0 + x1) / 2:.2f},{(y0 + y1) / 2:.2f}) {{{label_text}}};"
            )
        elif label:
            code = code_by_label.get(label)
            if code is None:
                code = matrix_code(len(code_by_label))
                code_by_label[label] = code
                code_entries.append((code, label))
            lines.append(
                rf"\node[font=\tiny,align=center,inner sep=0.1pt] at "
                rf"({(x0 + x1) / 2:.2f},{(y0 + y1) / 2:.2f}) {{{matrix_label_code(code)}}};"
            )
    lines.extend(
        [
            r"\draw[black,line width=0.35pt] (1,-1) rectangle (17,-17);",
            r"\end{tikzpicture}",
            r"\end{center}",
            matrix_code_legend(code_entries),
            r"\endgroup",
        ]
    )
    return "\n".join(lines)


def should_label_grid_rect(area: int, width: int, height: int, min_label_area: int, label_singletons: bool) -> bool:
    if label_singletons and area == 1:
        return True
    if area < min_label_area:
        return False
    if height == 1:
        return width >= 6
    if width == 1:
        return height >= 6
    return width >= 3 and height >= 2


def matrix_code(index: int) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if index < len(alphabet):
        return alphabet[index]
    index -= len(alphabet)
    return alphabet[index // len(alphabet)] + alphabet[index % len(alphabet)]


def matrix_code_legend(entries: list[tuple[str, str]]) -> str:
    if not entries:
        return ""
    rows: list[str] = []
    for index in range(0, len(entries), 2):
        left_code, left_label = entries[index]
        if index + 1 < len(entries):
            right_code, right_label = entries[index + 1]
            rows.append(
                rf"\textbf{{{matrix_label_code(left_code)}}} & {matrix_label_code(left_label)} & "
                rf"\textbf{{{matrix_label_code(right_code)}}} & {matrix_label_code(right_label)}\\"
            )
        else:
            rows.append(
                rf"\textbf{{{matrix_label_code(left_code)}}} & {matrix_label_code(left_label)} & "
                r"\multicolumn{2}{@{}l@{}}{}\\"
            )
    return "\n".join(
        [
            r"\vspace{-2pt}",
            r"\begin{center}",
            r"\begingroup\tiny",
            r"\begin{tabularx}{0.92\linewidth}{@{}r@{ = }X r@{ = }X@{}}",
            *rows,
            r"\end{tabularx}",
            r"\endgroup",
            r"\end{center}",
        ]
    )


def matrix_label_code(label: str) -> str:
    escaped = tex_escape(label).replace("-", r"\symbol{45}")
    return rf"\texttt{{{escaped}}}"


def matrix_rectangles(cells: dict[int, tuple[str, str]]) -> list[tuple[int, int, int, int, str, str]]:
    grouped: dict[tuple[str, str], dict[int, list[int]]] = {}
    for value, (label, color) in cells.items():
        row = (value >> 4) & 0xF
        col = value & 0xF
        grouped.setdefault((label, color), {}).setdefault(row, []).append(col)

    rects: list[tuple[int, int, int, int, str, str]] = []
    for (label, color), rows in grouped.items():
        row_intervals = {row: contiguous_intervals(cols) for row, cols in rows.items()}
        active: dict[tuple[int, int], int] = {}
        for row in range(17):
            intervals = set(row_intervals.get(row, [])) if row < 16 else set()
            for interval, start_row in list(active.items()):
                if interval not in intervals:
                    col0, col1 = interval
                    rects.append((start_row, row - 1, col0, col1, label, color))
                    del active[interval]
            for interval in sorted(intervals):
                if interval not in active:
                    active[interval] = row
    return sorted(rects, key=lambda item: (item[0], item[2], item[1], item[3], item[4]))


def contiguous_intervals(values: list[int]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for value in sorted(set(values)):
        if not out or value != out[-1][1] + 1:
            out.append((value, value))
        else:
            out[-1] = (out[-1][0], value)
    return out


def matrix_legend(rows: list[tuple[str, str]]) -> str:
    cells = []
    for label, color in rows:
        cells.append(
            rf"\tikz[baseline=-0.5ex]\draw[fill={color},draw=black,line width=0.2pt] "
            rf"(0,0) rectangle (0.25,0.11); {tex_escape(label)}"
        )
    line1 = cells[:4]
    line2 = cells[4:]
    lines = [
        r"\begingroup\footnotesize",
        r"\begin{tabularx}{\linewidth}{@{}XXXX@{}}",
        " & ".join(line1) + r"\\",
    ]
    if line2:
        lines.append(" & ".join(line2 + [""] * (4 - len(line2))) + r"\\")
    lines.extend([r"\end{tabularx}", r"\endgroup"])
    return "\n".join(lines)


def primary_grid_legend_rows() -> list[tuple[str, str]]:
    return [
        ("integer/arithmetic", primary_category_color("integer")),
        ("data movement", primary_category_color("data_movement")),
        ("control flow", primary_category_color("control_flow")),
        ("sentinel/control", primary_category_color("sentinel")),
        ("extension root", primary_category_color("extended")),
        ("atomic/system/cache", primary_category_color("system")),
        ("unallocated", "white"),
    ]


def extended_grid_legend_rows() -> list[tuple[str, str]]:
    return [
        ("integer/arithmetic", primary_category_color("integer")),
        ("data movement", primary_category_color("data_movement")),
        ("control flow", primary_category_color("control_flow")),
        ("atomic/system/cache", primary_category_color("system")),
        ("floating-point", extended_category_color("fpu")),
        ("mixed page", "gray!16"),
        ("unallocated", "white"),
    ]


def prefix_grid_legend_rows() -> list[tuple[str, str]]:
    return [
        ("neutral", prefix_grid_color("neutral")),
        ("speculation", prefix_grid_color("speculation")),
        ("arithmetic mode", prefix_grid_color("arithmetic_mode")),
        ("memory hint", prefix_grid_color("memory_hint")),
        ("EA update", prefix_grid_color("ea_update")),
        ("repeat", prefix_grid_color("repeat")),
        ("repeat boundary", prefix_grid_color("repeat_boundary")),
        ("unallocated", "white"),
    ]


def primary_grid_color(item: dict[str, Any]) -> str:
    if item.get("kind") == "extension_root":
        return primary_category_color("extended")
    category = str(item.get("category", item.get("group", "")))
    group = str(item.get("group", ""))
    if category in {"atomic", "system", "cache", "tlb"} or any(key in group for key in ("atomic", "system", "cache", "tlb")):
        return primary_category_color("system")
    return primary_category_color(category)


def extended_grid_color(item: dict[str, Any]) -> str:
    category = str(item.get("category", item.get("group", ""))).lower()
    root = str(item.get("extension_root", "")).lower()
    if category.startswith("fpu") or ".fpu_" in root or root.startswith("ext.fpu"):
        return extended_category_color("fpu")
    return primary_grid_color(item)


def primary_category_color(category: str) -> str:
    normalized = category.lower()
    if normalized in {"integer", "arithmetic"}:
        return "green!22"
    if normalized in {"data_movement", "data movement"}:
        return "red!18"
    if normalized in {"control_flow", "control flow"}:
        return "violet!20"
    if normalized in {"sentinel", "control"}:
        return "gray!28"
    if normalized == "extended":
        return "gray!18"
    if normalized == "system":
        return "cyan!18"
    return "yellow!18"


def extended_category_color(category: str) -> str:
    if category.lower() == "fpu":
        return "blue!14"
    return primary_category_color(category)


def prefix_grid_color(group: str) -> str:
    return {
        "neutral": "gray!25",
        "speculation": "violet!18",
        "arithmetic_mode": "green!22",
        "memory_hint": "yellow!22",
        "ea_update": "cyan!20",
        "repeat": "orange!24",
        "repeat_boundary": "gray!35",
    }.get(group, "white")


def primary_grid_label(item: dict[str, Any]) -> str:
    if item.get("kind") == "extension_root":
        return extension_root_grid_label(str(item.get("group", item.get("id", ""))))
    return compact_primary_grid_label(item)


def extended_grid_label(item: dict[str, Any]) -> str:
    mnemonic = str(item.get("mnemonic", item.get("id", "")))
    item_id = str(item.get("id", mnemonic))
    form = item_id
    if mnemonic and item_id.startswith(mnemonic + "."):
        form = item_id[len(mnemonic) + 1 :]
    form = re.sub(r"\.(BWLQ|BWL|BW|LQ|WL|SD|S/D|Q|L|W|B)$", "", form)
    form = form.replace("_TO_", "->")
    form = form.replace("_OR_", "/")
    form = form.replace("_AND_", "&")
    form = form.replace("_", " ")
    return f"{mnemonic} {form}".strip() if form and form != item_id else mnemonic


def compact_primary_grid_label(item: dict[str, Any]) -> str:
    mnemonic = str(item.get("mnemonic", item.get("id", "")))
    item_id = str(item.get("id", mnemonic))
    if "D_TO_EA" in item_id:
        return f"{mnemonic} D->EA"
    if "EA_TO_D" in item_id:
        return f"{mnemonic} EA->D"
    if "D_TO_D" in item_id:
        return f"{mnemonic} D,D"
    if "IMM_TO_D" in item_id:
        return f"{mnemonic} imm,D"
    if "IMM_TO_A" in item_id:
        return f"{mnemonic} imm,A"
    if item_id.endswith(".D"):
        return f"{mnemonic} D"
    if item_id.endswith(".A"):
        return f"{mnemonic} A"
    if ".IMM" in item_id:
        suffix = item_id.split(".IMM", 1)[1]
        return f"{mnemonic} imm{suffix}".strip()
    if ".BITMAP" in item_id:
        return f"{mnemonic} map"
    return mnemonic[:10]


def extension_root_grid_label(group: str) -> str:
    labels = {
        "integer_alu": "EXT ALU",
        "integer_bounds_signed": "EXT BND.S",
        "integer_bounds_unsigned": "EXT BND.U",
        "integer_mul_div": "EXT MUL",
        "integer_mac": "EXT MAC",
        "integer_bitfield": "EXT BIT",
        "integer_bitfield_bit_imm": "EXT BIT.I",
        "integer_bitfield_rotate_imm": "EXT ROT.I",
        "integer_bitfield_shift_imm": "EXT SHF.I",
        "data_movement": "EXT MOV",
        "data_register_banking": "EXT BANK",
        "ea_utility": "EXT EA",
        "control_flow": "EXT CTRL",
        "conditional_control": "EXT COND",
        "atomic_memory": "EXT ATOM",
        "cache_hint": "EXT PREF",
        "tlb_cache": "EXT TLB",
        "system_core": "EXT SYS",
        "virtualization_acceleration": "EXT VIRT",
        "fpu_move_compare": "EXT F.MOV",
        "fpu_arithmetic": "EXT F.ALU",
        "fpu_transcendental": "EXT F.TR",
    }
    return labels.get(group, "EXT")


def prefix_grid_label(prefix: dict[str, Any]) -> str:
    name = str(prefix.get("name", ""))
    labels = {
        "NOSPEC": "NS",
        "SATURATE": "SAT",
        "NONTEMPORAL": "NT",
        "POSTINC": "A++",
        "PREINC": "++A",
        "POSTDEC": "A--",
        "PREDEC": "--A",
    }
    if name in labels:
        return labels[name]
    if name == "SATURATE":
        return "SAT"
    return name[:8]


def primary_payload_values(item: dict[str, Any]) -> list[int]:
    payloads = item.get("primary_payloads")
    if isinstance(payloads, list) and payloads:
        return [parse_hex_int(value) for value in payloads]
    start = parse_hex_int(item.get("start_payload", "0x0"))
    end = parse_hex_int(item.get("end_payload", item.get("start_payload", "0x0")))
    reclaimed = {
        parse_hex_int(value)
        for value in item.get("reclaimed_payloads", []) or []
    }
    return [value for value in range(start, end + 1) if value not in reclaimed]


def prefix_values(prefix: dict[str, Any]) -> list[int]:
    if "value" in prefix:
        return [parse_hex_int(prefix.get("value")) & 0xFF]
    pattern = prefix.get("pattern")
    if isinstance(pattern, str):
        return pattern_values(pattern, 8)
    return []


def pattern_values(pattern: str, width: int) -> list[int]:
    bits = "".join(ch for ch in pattern if not ch.isspace())
    if len(bits) != width:
        return []
    values = []
    for value in range(1 << width):
        ok = True
        for index, bit in enumerate(bits):
            if bit not in "01":
                continue
            actual = (value >> (width - index - 1)) & 1
            if actual != int(bit):
                ok = False
                break
        if ok:
            values.append(value)
    return values


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


def field_catalog_diagrams(items: list[dict[str, Any]]) -> str:
    entries = field_catalog_entries(items)
    if not entries:
        return tex_escape("No operand fields are present.")
    return "\n".join(field_catalog_diagram(entry) for entry in entries)


def field_catalog_entries(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    catalog: dict[tuple[str, int], dict[str, Any]] = {}
    for item in items:
        for field in item.get("fields", []) or []:
            kind = str(field.get("kind", field.get("name", "")))
            width = field_width(field)
            key = (kind, width)
            entry = catalog.setdefault(
                key,
                {
                    "kind": kind,
                    "width": width,
                    "storage": set(),
                    "roles": set(),
                    "symbols": set(),
                },
            )
            entry["storage"].add(field_storage_text(field))
            entry["roles"].add(role_name(str(field.get("source", field.get("name", "")))))
            entry["symbols"].add(field_symbol(field))
    return [
        catalog[key]
        for key in sorted(catalog, key=lambda pair: (field_catalog_sort_group(pair[0]), pair[0], pair[1]))
    ]


def field_catalog_sort_group(kind: str) -> int:
    normalized = kind.lower()
    if normalized in {"ea", "imm_ea"}:
        return 0
    if normalized.endswith("reg") or normalized in {"sreg", "cr", "dbank"}:
        return 1
    if normalized in {"condition"}:
        return 2
    if normalized in {"bw", "bwl", "bwlq", "lq", "s_d", "wl"}:
        return 3
    if "group" in normalized or "selector" in normalized or normalized == "memory_order":
        return 4
    return 5


def field_catalog_diagram(entry: dict[str, Any]) -> str:
    kind = str(entry["kind"])
    width = int(entry["width"])
    symbol = field_catalog_symbol(kind, entry["symbols"])
    token = symbol * max(width, 1)
    caption = f"{kind_description(kind)} ({kind}, {width} bit{'s' if width != 1 else ''})"
    labels = [f"{kind}[{width - 1}:0]" if width > 1 else f"{kind}[0]"]
    storage = sorted(entry["storage"])
    roles = sorted(entry["roles"])
    symbols = sorted(str(value) for value in entry["symbols"] if value)
    return "\n".join(
        [
            r"\Needspace{2.05in}",
            rf"\noindent\textbf{{{tex_code(kind)}}} "
            rf"\hfill {tex_escape(str(width))} {tex_escape('bits' if width != 1 else 'bit')}\par",
            bit_diagram([token], caption, labels),
            field_catalog_note_line("Symbols", ", ".join(tex_code(value) for value in symbols) or tex_escape("-")),
            field_catalog_note_line("Common storage", ", ".join(tex_code(value) for value in storage) or tex_escape("-")),
            field_catalog_note_line("Typical roles", tex_escape(", ".join(roles) or "-")),
            r"\par\medskip",
        ]
    )


def field_catalog_symbol(kind: str, symbols: set[str]) -> str:
    preferred = {
        "AREG": "a",
        "DREG": "d",
        "EA": "e",
        "FREG": "f",
        "SREG": "g",
        "DBANK": "k",
        "condition": "c",
        "bitmap16": "b",
        "selector6": "n",
        "memory_order": "o",
        "bit_group": "o",
        "rotate_group": "o",
        "shift_group": "o",
    }
    if kind in preferred:
        return preferred[kind]
    for candidate in ("s", "z", "i", "o", "n", "d", "a", "e", "c", "b", "g", "k", "f"):
        if candidate in symbols:
            return candidate
    for symbol in sorted(symbols):
        if len(symbol) == 1 and symbol.isalpha():
            return symbol
    return "x"


def field_catalog_note_line(label: str, value: str) -> str:
    return (
        r"\begingroup\footnotesize\noindent"
        rf"\textbf{{{tex_escape(label)}:}} {value}\par\endgroup"
    )


def payload_sort_key(item: dict[str, Any]) -> tuple[int, str]:
    return (parse_hex_int(item.get("start_payload", "0x0")), str(item.get("id", "")))


def extended_payload_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    start, end = extended_opcode_range(item)
    return (start, end, str(item.get("id", "")))


def extended_opcode_range(item: dict[str, Any]) -> tuple[int, int]:
    if item.get("extended_opcode_start") is not None:
        start = parse_hex_int(item.get("extended_opcode_start"))
        end = parse_hex_int(item.get("extended_opcode_end", item.get("extended_opcode_start")))
        return start, end
    text = str(item.get("extended_opcode", "0x0000") or "0x0000")
    if ".." in text:
        start_text, end_text = text.split("..", 1)
        return parse_hex_int(start_text), parse_hex_int(end_text)
    value = parse_hex_int(text)
    return value, value


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
    if isinstance(value, int):
        return value
    text = str(value or "0")
    try:
        return int(text, 16) if text.lower().startswith("0x") else int(text, 10)
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
        hidden_top_section(f"{title} Descriptions"),
    ]
    if title.startswith("General"):
        parts.append(instruction_description_intro_section())
        parts.append(r"\clearpage")
    for index, mnemonic in enumerate(mnemonics):
        if index:
            parts.append(r"\clearpage")
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
                instruction_link(mnemonic),
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
    lines = [rf"\instrhead{{{tex_escape(mnemonic)}}}{{{tex_escape(title)}}}{{\label{{{instruction_label(mnemonic)}}}}}"]
    lines.append(rf"\manualfield{{Summary:}}{{{tex_escape(doc_summary(mnemonic, docs, records, operations, items))}}}")
    lines.append(rf"\manualfield{{Operation:}}{{{operation_latex(operations)}}}")
    lines.append(rf"\manualfield{{Assembler Syntax:}}{{{syntax_block(items)}}}")
    lines.append(rf"\manualfield{{Attributes:}}{{{attribute_text(items, records, operations, lengths)}}}")
    lines.append(rf"\manualfield{{Description:}}{{{doc_description(mnemonic, docs, records, operations, aliases)}}}")
    lines.append(save_area_format_section(mnemonic, docs))
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


def save_area_format_section(mnemonic: str, docs: dict[str, dict[str, Any]]) -> str:
    entry = docs.get(mnemonic, {})
    layout = entry.get("save_area_format")
    if not isinstance(layout, dict):
        return ""

    def offset_text(value: Any) -> str:
        if isinstance(value, int):
            return f"0x{value:03x}"
        return str(value)

    def map_row(label: str, offset: str) -> str:
        return rf"\multicolumn{{8}}{{|c|}}{{{tex_escape(label)}}} & \textbf{{{tex_escape(offset)}}}\\"

    def slot_row(slot: dict[str, Any]) -> str:
        offset = offset_text(slot.get("offset", "-"))
        cells = slot.get("cells")
        if not isinstance(cells, list) or not cells:
            return map_row(str(slot.get("field", "-")), offset)
        pieces: list[str] = []
        consumed = 0
        for cell in cells:
            if not isinstance(cell, dict):
                continue
            span = int(cell.get("span", 1))
            if span < 1:
                continue
            consumed += span
            left_rule = "|" if not pieces else ""
            pieces.append(rf"\multicolumn{{{span}}}{{{left_rule}c|}}{{{tex_escape(str(cell.get('field', '-')))}}}")
        if consumed != 8:
            return map_row(str(slot.get("field", "-")), offset)
        return " & ".join(pieces) + rf" & \textbf{{{tex_escape(offset)}}}\\"

    def component_offset_text(value: Any) -> str:
        if isinstance(value, int):
            return f"+0x{value:03x}"
        return str(value)

    def component_id_text(value: Any) -> str:
        if isinstance(value, int):
            return f"0x{value:04x}"
        return str(value)

    def repeat_rows(spec: dict[str, Any]) -> list[tuple[str, str, str]]:
        count = int(spec.get("count", 0))
        start = spec.get("offset_start", 0)
        stride = spec.get("offset_stride", 0)
        n_start = int(spec.get("n_start", 0))
        field_template = str(spec.get("field_template", "entry {n}"))
        meaning_template = str(spec.get("meaning_template", ""))
        rows: list[tuple[str, str, str]] = []
        if not isinstance(start, int) or not isinstance(stride, int):
            return rows
        for index in range(count):
            n = n_start + index
            rows.append(
                (
                    component_offset_text(start + index * stride),
                    field_template.format(n=n),
                    meaning_template.format(n=n),
                )
            )
        return rows

    def component_slot_rows(component: dict[str, Any]) -> list[tuple[str, str, str]]:
        rows: list[tuple[str, str, str]] = []
        for slot in component.get("slots", []) or []:
            if not isinstance(slot, dict):
                continue
            repeat = slot.get("repeat")
            if isinstance(repeat, dict):
                rows.extend(repeat_rows(repeat))
                continue
            rows.append(
                (
                    component_offset_text(slot.get("offset", "-")),
                    str(slot.get("field", "-")),
                    str(slot.get("meaning", "")),
                )
            )
        return rows

    def component_format_section(component: dict[str, Any]) -> str:
        title = str(component.get("title", component.get("name", "Extension Component")))
        name = str(component.get("name", title))
        description = compact_text(component.get("description", ""))
        validity = compact_text(component.get("validity", ""))
        size = component.get("size", "-")
        rows = component_slot_rows(component)
        if not rows:
            return ""
        bitmap_bits = component.get("component_bitmap_bits", []) or []
        bitmap_description = ""
        bitmap_reserved = ""
        bitmap_items: list[Any] = []
        if isinstance(bitmap_bits, dict):
            bitmap_description = compact_text(bitmap_bits.get("description", ""))
            bitmap_reserved = compact_text(bitmap_bits.get("reserved_bits", ""))
            bitmap_items = bitmap_bits.get("mappings", []) or []
        elif isinstance(bitmap_bits, list):
            bitmap_items = bitmap_bits
        component_bitmap_rows = [
            (
                str(item.get("bits", "-")),
                str(item.get("slot", item.get("field", "-"))),
                str(item.get("meaning", "")),
            )
            for item in bitmap_items
            if isinstance(item, dict)
        ]
        lines = [
            r"\par\smallskip\Needspace{2.4in}",
            rf"\noindent\textbf{{Extension Component: {tex_escape(title)}}}\par\smallskip",
            r"\begingroup\footnotesize",
            r"\begin{tabularx}{0.985\linewidth}{@{}p{1.35in}X@{}}",
            rf"\textbf{{Component ID}} & {tex_escape(component_id_text(component.get('component_id', '-')))}\\",
            rf"\textbf{{Component Name}} & {tex_code(name)}\\",
            rf"\textbf{{Component Size}} & {tex_escape(component_id_text(size) if isinstance(size, int) else str(size))}\\",
            r"\end{tabularx}\endgroup\par\smallskip",
        ]
        if description:
            lines.append(rf"\noindent {tex_escape(description)}\par\smallskip")
        if validity:
            lines.append(rf"\noindent {tex_escape(validity)}\par\smallskip")
        if component_bitmap_rows:
            lines.append(r"\noindent\textbf{Component-Local Valid Bitmap:}\par\smallskip\noindent")
            if bitmap_description:
                lines.append(rf"{tex_escape(bitmap_description)}\par\smallskip\noindent")
            lines.extend(
                [
                    r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.08}",
                    r"\begin{tabularx}{0.985\linewidth}{|p{0.62in}|p{1.85in}|X|}",
                    r"\hline",
                    r"\textbf{Set Bit} & \textbf{Component Slot} & \textbf{Meaning}\\",
                    r"\hline",
                ]
            )
            for bits, slot, meaning in component_bitmap_rows:
                lines.append(rf"{tex_escape(bits)} & {tex_escape(slot)} & {tex_escape(meaning)}\\")
                lines.append(r"\hline")
            lines.append(r"\end{tabularx}\endgroup\par\smallskip")
            if bitmap_reserved:
                lines.append(rf"\noindent {tex_escape(bitmap_reserved)}\par\smallskip")
        table_rows = [
            [tex_escape(offset), tex_escape(field), tex_escape(meaning)]
            for offset, field, meaning in rows
        ]
        if len(table_rows) > 14:
            lines.append(
                latex_longtable(
                    ["Offset", "Saved State", "Meaning"],
                    table_rows,
                    ["0.72in", "1.85in", "3.0in"],
                )
            )
            lines.append(r"\smallskip")
        else:
            lines.extend(
                [
                    r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.08}",
                    r"\begin{tabularx}{0.985\linewidth}{|p{0.72in}|p{1.85in}|X|}",
                    r"\hline",
                    r"\textbf{Offset} & \textbf{Saved State} & \textbf{Meaning}\\",
                    r"\hline",
                ]
            )
            for offset, field, meaning in table_rows:
                lines.append(rf"{offset} & {field} & {meaning}\\")
                lines.append(r"\hline")
            lines.append(r"\end{tabularx}\endgroup\par\smallskip")
        return "\n".join(lines)

    rows = [slot for slot in layout.get("fixed_slots", []) or [] if isinstance(slot, dict)]
    if not rows:
        return ""
    bitmap_bits = layout.get("base_bitmap_bits", []) or []
    bitmap_description = ""
    bitmap_reserved = ""
    bitmap_items: list[Any] = []
    if isinstance(bitmap_bits, dict):
        bitmap_description = compact_text(bitmap_bits.get("description", ""))
        bitmap_reserved = compact_text(bitmap_bits.get("reserved_bits", ""))
        bitmap_items = bitmap_bits.get("mappings", []) or []
    elif isinstance(bitmap_bits, list):
        bitmap_items = bitmap_bits
    bitmap_rows = [
        (
            str(item.get("bits", "-")),
            str(item.get("slot", item.get("field", "-"))),
            str(item.get("meaning", "")),
        )
        for item in bitmap_items
        if isinstance(item, dict)
    ]
    behavior = compact_text(layout.get("behavior", ""))
    extension_text = compact_text(layout.get("extension_components", ""))
    extension_order_text = compact_text(layout.get("extension_component_order", ""))

    lines = [
        r"\par\smallskip\Needspace{6.6in}\noindent\textbf{Save Area Format:}\par\smallskip\noindent",
        r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.08}",
        r"\begin{tabularx}{0.985\linewidth}{|*{8}{>{\centering\arraybackslash}X|}p{0.56in}|}",
        r"\hline",
        r"\multicolumn{8}{|c|}{\textbf{Save-area bytes}} & \textbf{Offset}\\",
        r"\hline",
        r"\textbf{63..56} & \textbf{55..48} & \textbf{47..40} & \textbf{39..32} & \textbf{31..24} & \textbf{23..16} & \textbf{15..8} & \textbf{7..0} & \\",
        r"\hline",
    ]
    for slot in rows:
        lines.append(slot_row(slot))
        lines.append(r"\hline")
    lines.extend(
        [
            r"\end{tabularx}\endgroup\par\smallskip",
        ]
    )
    if bitmap_rows:
        lines.extend(
            [
                r"\noindent\textbf{Base Save-Slot Valid Bitmap:}\par\smallskip\noindent",
            ]
        )
        if bitmap_description:
            lines.append(rf"{tex_escape(bitmap_description)}\par\smallskip\noindent")
        lines.extend(
            [
                r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.08}",
                r"\begin{tabularx}{0.985\linewidth}{|p{0.62in}|p{1.55in}|X|}",
                r"\hline",
                r"\textbf{Set Bit} & \textbf{Base Save Slot} & \textbf{Meaning}\\",
                r"\hline",
            ]
        )
        for bits, slot, meaning in bitmap_rows:
            lines.append(rf"{tex_escape(bits)} & {tex_escape(slot)} & {tex_escape(meaning)}\\")
            lines.append(r"\hline")
        lines.append(r"\end{tabularx}\endgroup\par\smallskip")
        if bitmap_reserved:
            lines.append(rf"\noindent {tex_escape(bitmap_reserved)}\par\smallskip")
    if behavior:
        lines.append(rf"\noindent {tex_escape(behavior)}\par")
    if extension_text:
        lines.append(rf"\noindent {tex_escape(extension_text)}\par")
    if extension_order_text:
        lines.append(rf"\noindent {tex_escape(extension_order_text)}\par")
    extension_formats = [
        component
        for component in layout.get("extension_component_formats", []) or []
        if isinstance(component, dict)
    ]
    if extension_formats:
        lines.append(r"\par\smallskip\noindent\textbf{Extension Component Formats:}\par")
        for component in extension_formats:
            rendered = component_format_section(component)
            if rendered:
                lines.append(rendered)
    lines.append(r"\smallskip")
    return "\n".join(lines)


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
        "save_modified_processor_state": "Save modified base and extension state",
        "restore_processor_state": "Restore base and extension state",
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
        if any(operand.startswith("seg:SREG") for operand in operands):
            return "depends_on_segment_register"
        return "policy_controlled"
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
            "segment_register_forms",
            "segment_registers",
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
            "segment_register_access",
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
        "SREG": "segment register selector",
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
