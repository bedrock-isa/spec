"""Instruction-reference and instruction-summary LaTeX renderers."""

from __future__ import annotations

from typing import Any, Callable
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
from spec_model.encoding import (
    fflag_meanings as spec_fflag_meanings,
    fflag_names as spec_fflag_names,
    flag_names as spec_flag_names,
    size_codes,
    size_code_label,
    size_kind_entries,
    size_kind_suffixes,
    size_kinds as spec_size_kinds,
)
from .common import (
    compact_text,
    latex_longtable,
    memory_rule_text,
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


ACTIVE_SPEC: dict[str, Any] | None = None


def set_active_spec(spec: dict[str, Any]) -> None:
    global ACTIVE_SPEC
    ACTIVE_SPEC = spec


def active_spec() -> dict[str, Any]:
    if ACTIVE_SPEC is None:
        raise RuntimeError("active ISA spec is not set")
    return ACTIVE_SPEC


def flag_order() -> list[str]:
    return spec_flag_names(active_spec())


def fflag_order() -> list[str]:
    return spec_fflag_names(active_spec())


def fflag_meanings() -> dict[str, str]:
    return spec_fflag_meanings(active_spec())


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
    mnemonic_items: dict[str, list[dict[str, Any]]] | None = None,
) -> str:
    set_active_spec(spec)
    records = records or {}
    operations = operations or {}
    mnemonic_items = mnemonic_items or {}
    return render_latex_template(
        "instruction_set_summary.tex",
        {
            "CLASS_SUMMARY_TABLE": instruction_class_summary_table(spec, mnemonics),
            "ATTRIBUTE_MATRIX_TABLE": instruction_attribute_matrix_table(
                spec,
                mnemonics,
                records,
                operations,
                mnemonic_items,
            ),
        },
    )


def instruction_class_summary_table(spec: dict[str, Any], mnemonics: list[str]) -> str:
    semantics = ((spec.get("instructions") or {}).get("operation_semantics") or {})
    groups = semantics.get("groups") or {}
    if not isinstance(groups, dict):
        return "No instruction class metadata is available.\\par\n"
    group_order = [str(name) for name in semantics.get("group_order", []) or []]
    ordered_names = [name for name in group_order if name in groups]
    ordered_names.extend(name for name in groups if name not in set(ordered_names))
    known = set(mnemonics)
    rows: list[list[str]] = []
    for name in ordered_names:
        body = groups.get(name)
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
    for key in ("memory", "atomic", "privilege", "flags", "implementation", "traps"):
        if key in body:
            if key == "flags":
                value = integer_flags_text(body[key])
            elif key == "memory":
                value = memory_rule_text(body[key])
            else:
                value = readable_text(body[key])
            notes.append(f"{pretty_key(key)}: {value}")
    return "; ".join(notes)


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
    mnemonic_items: dict[str, list[dict[str, Any]]],
) -> str:
    rows: list[list[str]] = []
    for mnemonic in mnemonics:
        recs = records.get(mnemonic, [])
        ops = operations.get(mnemonic, [])
        items = mnemonic_items.get(mnemonic, [])
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
    legend = render_latex_template("instruction_attribute_matrix_intro.tex")
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
        ],
        "Instruction Attribute Matrix",
        style="dense",
    )
    return legend + instruction_attribute_matrix_legend() + table


def instruction_attribute_matrix_legend() -> str:
    rows = [
        [tex_escape("Priv"), tex_code("U"), tex_escape("all listed forms are unprivileged")],
        [tex_escape("Priv"), tex_code("U*"), tex_escape("all listed forms are user-accessible under a listed architectural condition")],
        [tex_escape("Priv"), tex_code("S"), tex_escape("all listed forms require supervisor privilege")],
        [tex_escape("Priv"), tex_code("P"), tex_escape("at least one listed form is policy-controlled or configurable")],
        [tex_escape("Priv"), tex_code("mixed"), tex_escape("the mnemonic has both unprivileged and privileged forms")],
        [tex_escape("Flag"), tex_code("Y"), tex_escape("update permission for this FLAGS or FFLAGS bit")],
        [tex_escape("Flag"), tex_code("0"), tex_escape("the instruction writes this flag as cleared")],
        [tex_escape("Flag"), tex_code("U"), tex_escape("the flag is unchanged")],
        [tex_escape("Prefix"), tex_code("Y"), tex_escape("at least one form of the mnemonic supports the prefix")],
        [tex_escape("Prefix"), tex_code("-"), tex_escape("the prefix is not applicable to this mnemonic")],
        [tex_code("SAT"), tex_code("Y/-"), tex_escape("SATURATE prefix is applicable or not applicable")],
        [tex_code("NT"), tex_code("Y/-"), tex_escape("NONTEMPORAL hint is applicable or not applicable to memory forms")],
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
    if ("U" in short or "U*" in short) and ("S" in short or "P" in short or "state" in short):
        return "mixed"
    return "/".join(sorted(short))


def privilege_code(value: str) -> str:
    normalized = readable_text(value).lower()
    if normalized.startswith("user allowed when"):
        return "U*"
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
    names = [name for name in fflag_order() if f"FFLAGS.{name}" in text]
    if names:
        return ",".join(names)
    return abbreviate_text(readable_text(text), 28)


def instruction_flag_cells(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> list[str]:
    text = flags_text(records, operations)
    if "FFLAGS" in text:
        integer_marks = {flag: "-" for flag in flag_order()}
        floating_marks = fflag_marks(text)
    else:
        integer_marks = flag_marks(text or "unchanged")
        floating_marks = {flag: "-" for flag in fflag_order()}
    return [flag_matrix_cell(integer_marks[flag]) for flag in flag_order()] + [
        flag_matrix_cell(floating_marks[flag]) for flag in fflag_order()
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
    codes: list[str] = []
    for name, rule in rules.items():
        if not isinstance(rule, dict):
            continue
        if rule.get("scope") == "all_instructions":
            continue
        if prefix_rule_applies(rule, mnemonic, records, operations, items):
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

    def rule_cell(name: str) -> str:
        rule = rules.get(name) if isinstance(rules, dict) else None
        if not isinstance(rule, dict):
            return tex_code("-")
        return availability_cell(prefix_rule_applies(rule, mnemonic, records, operations, items))

    return [
        rule_cell("SATURATE"),
        rule_cell("NONTEMPORAL"),
    ]


def availability_cell(enabled: bool) -> str:
    return tex_code("Y" if enabled else "-")


def prefix_rule_applies(
    rule: dict[str, Any],
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> bool:
    if rule.get("scope") == "all_instructions":
        return True
    explicit = {str(value) for value in rule.get("mnemonics", []) or []}
    if mnemonic in explicit:
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
        pcode = spec.get("pcode") or []
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
        ("system/control", primary_category_color("system")),
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
    if normalized == "control":
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
    suffixes = sorted(
        {
            str(kind).replace("_", "")
            for kind in spec_size_kinds(active_spec())
        }
        | {
            str(kind).replace("_", "/")
            for kind in spec_size_kinds(active_spec())
        }
        | set(size_codes(active_spec()).keys()),
        key=len,
        reverse=True,
    )
    if suffixes:
        suffix_pattern = "|".join(re.escape(suffix) for suffix in suffixes)
        form = re.sub(rf"\.({suffix_pattern})$", "", form)
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
        "POSTINC": "An++",
        "PREINC": "++An",
        "POSTDEC": "An--",
        "PREDEC": "--An",
        "U2C": "U>C",
        "C2U": "C>U",
        "U2U": "U>U",
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
    if normalized == "ea":
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
        "fbitmap16": "b",
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
    spec: dict[str, Any],
    title: str,
    mnemonics: list[str],
    records: dict[str, list[dict[str, Any]]],
    operations: dict[str, list[dict[str, Any]]],
    mnemonic_items: dict[str, list[dict[str, Any]]],
    aliases: dict[str, list[str]],
    lengths: dict[tuple[str, str], tuple[int, int]],
    docs: dict[str, dict[str, Any]],
) -> list[str]:
    set_active_spec(spec)
    if not mnemonics:
        return []
    summary_caption = f"Table {'10-1' if title.startswith('Floating-Point') else '9-1'}. {title} Summary"
    parts = [
        top_section(f"{title} Summary"),
        instruction_summary(mnemonics, records, operations, mnemonic_items, docs, summary_caption),
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
                mnemonic_items.get(mnemonic, []),
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
    mnemonic_items: dict[str, list[dict[str, Any]]],
) -> set[str]:
    out: set[str] = set()
    for mnemonic, items in mnemonic_items.items():
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
    mnemonic_items: dict[str, list[dict[str, Any]]],
    docs: dict[str, dict[str, Any]],
    caption: str | None = None,
) -> str:
    rows = []
    for mnemonic in mnemonics:
        rows.append(
            [
                instruction_link(mnemonic),
                tex_escape(doc_title(mnemonic, docs, records.get(mnemonic, []), operations.get(mnemonic, []))),
                tex_escape(len(mnemonic_items.get(mnemonic, []))),
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
    lines = [
        rf"\begin{{manualinstruction}}{{{tex_escape(mnemonic)}}}{{{tex_escape(title)}}}{{{instruction_label(mnemonic)}}}"
    ]
    lines.append(rf"\manualinstructionfield{{Summary}}{{{tex_escape(doc_summary(mnemonic, docs, records, operations, items))}}}")
    lines.append(rf"\manualinstructionfield{{Operation}}{{{operation_latex(operations)}}}")
    lines.append(rf"\manualinstructionfield{{Assembler Syntax}}{{{syntax_block(items)}}}")
    lines.append(rf"\manualinstructionfield{{Attributes}}{{{attribute_text(items, records, operations, lengths)}}}")
    description = doc_description(mnemonic, docs, records, operations, aliases)
    if description:
        lines.append(rf"\manualinstructionfield{{Description}}{{{description}}}")
    lines.extend(instruction_body_extra_fields(mnemonic))
    lines.append(condition_code_section(records, operations))
    lines.append(instruction_forms_section(items, lengths, records, operations))
    lines.append(r"\end{manualinstruction}")
    return "\n".join(lines)


def instruction_body_extra_fields(mnemonic: str) -> list[str]:
    if mnemonic == "FCLASS":
        return [rf"\manualinstructionfield{{Result Bitmap}}{{{render_latex_template('fclass_result_bitmap.tex')}}}"]
    return []


def doc_title(
    mnemonic: str,
    docs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    entry = docs.get(mnemonic, {})
    return compact_text(entry.get("title", ""))


def doc_summary(
    mnemonic: str,
    docs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> str:
    _ = records
    _ = operations
    _ = items
    entry = docs.get(mnemonic, {})
    return compact_text(entry.get("summary", ""))


def doc_description(
    mnemonic: str,
    docs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    aliases: list[str],
) -> str:
    _ = records
    _ = operations
    _ = aliases
    entry = docs.get(mnemonic, {})
    return tex_escape(compact_text(entry.get("description", "")))


def save_area_format_reference_sections(
    save_area_formats: dict[str, Any],
    mnemonics: list[str],
    *,
    include_titles: bool = True,
) -> list[str]:
    if not isinstance(save_area_formats, dict):
        return []
    group_mnemonics = {str(mnemonic) for mnemonic in mnemonics}
    sections: list[str] = []
    for layout in save_area_formats.values():
        if not isinstance(layout, dict):
            continue
        applies_to = {str(mnemonic) for mnemonic in layout.get("applies_to", []) or []}
        if applies_to and not (applies_to & group_mnemonics):
            continue
        rendered = save_area_format_section(layout, include_title=include_titles)
        if rendered:
            sections.append(rendered)
    return sections


def save_area_format_section(layout: dict[str, Any], *, include_title: bool = True) -> str:
    if not isinstance(layout, dict):
        return ""

    def offset_text(value: Any) -> str:
        if isinstance(value, int):
            return f"0x{value:03x}"
        return str(value)

    def component_offset_text(value: Any) -> str:
        if isinstance(value, int):
            return f"+0x{value:03x}"
        return str(value)

    def component_id_text(value: Any) -> str:
        if isinstance(value, int):
            return f"0x{value:04x}"
        return str(value)

    def component_offset_value(value: str) -> int | None:
        text = str(value)
        try:
            if text.startswith("+0x"):
                return int(text[1:], 16)
            if text.startswith("0x"):
                return int(text, 16)
            return int(text, 10)
        except ValueError:
            return None

    def bit_range_value(value: Any) -> tuple[int, int] | None:
        if isinstance(value, int):
            return value, value
        text = str(value).strip()
        if re.fullmatch(r"\d+", text):
            bit = int(text)
            return bit, bit
        match = re.fullmatch(r"(\d+)\s*\.\.\s*(\d+)", text)
        if not match:
            return None
        first = int(match.group(1))
        second = int(match.group(2))
        return min(first, second), max(first, second)

    def header_format_rows(owner: dict[str, Any], offset_formatter: Callable[[Any], str]) -> list[tuple[str, list[tuple[str, int]]]]:
        grouped: dict[Any, list[tuple[int, int, str]]] = {}
        for field in owner.get("header_fields", []) or []:
            if not isinstance(field, dict):
                continue
            bit_range = bit_range_value(field.get("bits"))
            if bit_range is None:
                continue
            low, high = bit_range
            if low < 0 or high > 63:
                continue
            grouped.setdefault(field.get("offset", "-"), []).append((low, high, str(field.get("field", "-"))))

        def offset_sort_key(offset: Any) -> tuple[int, int, str]:
            offset_label = offset_formatter(offset)
            offset_value = component_offset_value(offset_label)
            return (0 if offset_value is not None else 1, offset_value or 0, str(offset_label))

        rows: list[tuple[str, list[tuple[str, int]]]] = []
        for offset in sorted(grouped, key=offset_sort_key):
            fields = sorted(grouped[offset], key=lambda item: item[1], reverse=True)
            expected_high = 63
            pieces: list[tuple[str, int]] = []
            for low, high, name in fields:
                if high > expected_high:
                    raise ValueError(f"overlapping save-area header field at {offset_formatter(offset)}")
                if high < expected_high:
                    pieces.append(("reserved", expected_high - high))
                pieces.append((name, high - low + 1))
                expected_high = low - 1
            if expected_high >= 0:
                pieces.append(("reserved", expected_high + 1))
            rows.append((offset_formatter(offset), pieces))
        return rows

    def field_display_label(name: str, width: int) -> str:
        if name == "reserved" and width <= 2:
            return ""
        if name == "reserved" and width <= 6:
            return "rsv"
        return name

    def field_node_option(width: int) -> str:
        if width < 4:
            return "[scale=0.56]"
        if width < 6:
            return "[scale=0.64]"
        if width < 10:
            return "[scale=0.76]"
        return ""

    def byte_cells(fields: list[str]) -> list[tuple[str, int]]:
        cells: list[tuple[str, int]] = []
        index = 0
        while index < len(fields):
            label = fields[index] or "reserved"
            span = 1
            while index + span < len(fields) and (fields[index + span] or "reserved") == label:
                span += 1
            cells.append((label, span * 8))
            index += span
        return cells

    def slot_layout_row(slot: dict[str, Any]) -> tuple[str, str | list[tuple[str, int]], str]:
        offset = offset_text(slot.get("offset", "-"))
        cells = slot.get("cells")
        if isinstance(cells, list) and cells:
            pieces: list[tuple[str, int]] = []
            consumed = 0
            for cell in cells:
                if not isinstance(cell, dict):
                    continue
                span = int(cell.get("span", 1))
                if span < 1:
                    continue
                consumed += span
                pieces.append((str(cell.get("field", "-")), span * 8))
            if consumed == 8:
                return offset, pieces, str(slot.get("meaning", ""))
        return offset, str(slot.get("field", "-")), str(slot.get("meaning", ""))

    def normalize_layout_rows(
        rows: list[tuple[str, str | list[tuple[str, int]], str]],
        offset_formatter: Callable[[Any], str],
    ) -> list[tuple[str, list[tuple[str, int]]]]:
        if not rows:
            return []
        parsed = [(component_offset_value(offset), offset, field) for offset, field, _meaning in rows]
        normalized: list[tuple[str, list[tuple[str, int]]]] = []
        if all(offset_value is not None for offset_value, _offset, _field in parsed):
            parsed = sorted(parsed, key=lambda item: (int(item[0] or 0), str(item[1])))
            numeric_offsets = [int(offset_value) for offset_value, _offset, _field in parsed if offset_value is not None]
            entries: list[tuple[int, int, int, str | list[tuple[str, int]]]] = []
            for index, (offset_value, _offset, field) in enumerate(parsed):
                assert offset_value is not None
                row_start = offset_value - (offset_value % 8)
                row_end = row_start + 8
                later_offsets = [candidate for candidate in numeric_offsets[index + 1 :] if candidate > offset_value]
                next_offset = later_offsets[0] if later_offsets else row_end
                size = max(1, min(row_end, next_offset) - offset_value)
                entries.append((row_start, offset_value - row_start, size, field))
            for row_start in sorted({entry[0] for entry in entries}):
                row_entries = [entry for entry in entries if entry[0] == row_start]
                if len(row_entries) == 1 and isinstance(row_entries[0][3], list):
                    normalized.append((offset_formatter(row_start), row_entries[0][3]))
                    continue
                fields = ["reserved"] * 8
                for _row_start, byte_offset, size, field in row_entries:
                    if isinstance(field, list):
                        continue
                    for byte in range(byte_offset, min(byte_offset + size, 8)):
                        fields[7 - byte] = field
                normalized.append((offset_formatter(row_start), byte_cells(fields)))
        else:
            for _offset_value, offset, field in parsed:
                if isinstance(field, list):
                    normalized.append((offset, field))
                else:
                    normalized.append((offset, [(field, 64)]))
        return normalized

    def layout_grid_table(
        title: str,
        rows: list[tuple[str, str | list[tuple[str, int]], str]],
        offset_formatter: Callable[[Any], str],
    ) -> str:
        layout_rows = normalize_layout_rows(rows, offset_formatter)
        if not layout_rows:
            return ""
        needspace = min(6.7, 0.48 + 0.20 * (len(layout_rows) + 2))
        lines = [
            rf"\Needspace{{{needspace:.2f}in}}",
            r"\noindent\begin{tikzpicture}[x=0.01368\linewidth,y=0.19in,every node/.style={font=\footnotesize,inner sep=1pt,align=center}]",
            r"\draw[line width=0.35pt] (0,0) rectangle (64,-1);",
            r"\node[font=\bfseries\footnotesize] at (32,-0.5) {" + tex_escape(title) + r"};",
            r"\draw[line width=0.35pt] (64,0) rectangle (72,-1);",
            r"\node[font=\bfseries\footnotesize] at (68,-0.5) {Offset};",
        ]
        bit_labels = ["63..56", "55..48", "47..40", "39..32", "31..24", "23..16", "15..8", "7..0"]
        for index, label in enumerate(bit_labels):
            x0 = index * 8
            x1 = x0 + 8
            lines.append(rf"\draw[line width=0.35pt] ({x0},-1) rectangle ({x1},-2);")
            lines.append(rf"\node[font=\bfseries\footnotesize] at ({x0 + 4},-1.5) {{{tex_escape(label)}}};")
        lines.extend(
            [
                r"\draw[line width=0.35pt] (64,-1) rectangle (72,-2);",
            ]
        )
        for row_index, (offset, fields) in enumerate(layout_rows, start=2):
            y_top = -row_index
            y_bottom = -(row_index + 1)
            x = 0
            for label, width in fields:
                if width <= 0:
                    continue
                x_end = x + width
                display = field_display_label(label or "reserved", width)
                lines.append(rf"\draw[line width=0.35pt] ({x},{y_top}) rectangle ({x_end},{y_bottom});")
                if display:
                    node_option = field_node_option(width)
                    lines.append(
                        rf"\node{node_option} at ({x + width / 2:.2f},{y_top - 0.5:.2f}) {{{tex_escape(display)}}};"
                    )
                x = x_end
            if x < 64:
                lines.append(rf"\draw[line width=0.35pt] ({x},{y_top}) rectangle (64,{y_bottom});")
            lines.append(rf"\draw[line width=0.35pt] (64,{y_top}) rectangle (72,{y_bottom});")
            lines.append(rf"\node[font=\bfseries\footnotesize] at (68,{y_top - 0.5:.2f}) {{{tex_escape(offset)}}};")
        lines.append(r"\end{tikzpicture}\par\smallskip")
        return "\n".join(lines)

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

    def component_slot_rows(component: dict[str, Any]) -> list[tuple[str, str | list[tuple[str, int]], str]]:
        rows: list[tuple[str, str | list[tuple[str, int]], str]] = [
            (offset, fields, "")
            for offset, fields in header_format_rows(component, component_offset_text)
        ]
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

    def header_field_rows(owner: dict[str, Any], offset_formatter: Callable[[Any], str]) -> list[tuple[str, str, str, str]]:
        rows: list[tuple[str, str, str, str]] = []
        for field in owner.get("header_fields", []) or []:
            if not isinstance(field, dict):
                continue
            rows.append(
                (
                    offset_formatter(field.get("offset", "-")),
                    str(field.get("bits", "-")),
                    str(field.get("field", "-")),
                    str(field.get("meaning", "")),
                )
            )
        return rows

    def header_field_table(rows: list[tuple[str, str, str, str]], title: str) -> str:
        if not rows:
            return ""
        needspace = min(2.4, 0.55 + 0.24 * len(rows))
        lines = [
            rf"\Needspace{{{needspace:.2f}in}}",
            rf"\noindent\textbf{{{tex_escape(title)}:}}\par\smallskip\noindent",
            r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.08}",
            r"\begin{tabularx}{0.985\linewidth}{|p{0.56in}|p{0.62in}|p{1.35in}|X|}",
            r"\hline",
            r"\textbf{Offset} & \textbf{Bits} & \textbf{Field} & \textbf{Meaning}\\",
            r"\hline",
        ]
        for offset, bits, field, meaning in rows:
            lines.append(
                rf"{tex_escape(offset)} & {tex_escape(bits)} & {tex_escape(field)} & {tex_escape(meaning)}\\"
            )
            lines.append(r"\hline")
        lines.append(r"\end{tabularx}\endgroup\par\smallskip")
        return "\n".join(lines)

    def component_format_section(component: dict[str, Any]) -> str:
        title = str(component.get("title", component.get("name", "Extension Component")))
        name = str(component.get("name", title))
        extension_requirement = compact_text(component.get("extension_requirement", ""))
        size = component.get("size", "-")
        slot_rows = component_slot_rows(component)
        component_header_rows = header_field_rows(component, component_offset_text)
        if not (slot_rows or component_header_rows):
            return ""
        lines = [
            r"\par\smallskip\Needspace{2.4in}",
            rf"\noindent\textbf{{Extension Component: {tex_escape(title)}}}\par\smallskip",
            r"\begingroup\footnotesize",
            r"\begin{tabularx}{0.985\linewidth}{@{}p{1.35in}X@{}}",
            rf"\textbf{{Component ID}} & {tex_escape(component_id_text(component.get('component_id', '-')))}\\",
            rf"\textbf{{Component Name}} & {tex_code(name)}\\",
            *(
                [rf"\textbf{{Extension Requirement}} & {tex_code(extension_requirement)}\\"]
                if extension_requirement
                else []
            ),
            rf"\textbf{{Component Size}} & {tex_escape(component_id_text(size) if isinstance(size, int) else str(size))}\\",
            r"\end{tabularx}\endgroup\par\smallskip",
        ]
        slot_table = layout_grid_table("Component-relative bytes", slot_rows, component_offset_text)
        if slot_table:
            lines.append(slot_table)
        header_table = header_field_table(component_header_rows, "Component Header Fields")
        if header_table:
            lines.append(header_table)
        return "\n".join(lines)

    rows = [slot for slot in layout.get("fixed_slots", []) or [] if isinstance(slot, dict)]
    if not rows:
        return ""
    base_header_rows = header_field_rows(layout, offset_text)
    base_header_format_rows = header_format_rows(layout, offset_text)
    base_header_offsets = {offset for offset, _fields in base_header_format_rows}

    lines = [
        r"\par\smallskip",
    ]
    if include_title:
        lines.append(rf"\noindent\textbf{{{tex_escape(str(layout.get('title', 'Save Area Format')))}:}}\par\smallskip")
    base_layout_rows: list[tuple[str, str | list[tuple[str, int]], str]] = [
        (offset, fields, "")
        for offset, fields in base_header_format_rows
    ]
    for slot in rows:
        if offset_text(slot.get("offset", "-")) in base_header_offsets:
            continue
        base_layout_rows.append(slot_layout_row(slot))
    base_layout_table = layout_grid_table("Save-area bytes", base_layout_rows, offset_text)
    if base_layout_table:
        lines.append(base_layout_table)
    base_header_table = header_field_table(base_header_rows, "Base Header Fields")
    if base_header_table:
        lines.append(base_header_table)
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
    return "; ".join(dict.fromkeys(texts))


def operation_texts(operations: list[dict[str, Any]]) -> list[str]:
    explicit = explicit_operation_texts(operations)
    if explicit:
        return explicit
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


def explicit_operation_texts(operations: list[dict[str, Any]]) -> list[str]:
    texts: list[str] = []
    for record in operations:
        spec = record.get("spec", {})
        if "operation_text" in spec:
            text = compact_text(spec["operation_text"])
            if text:
                texts.append(text)
    return list(dict.fromkeys(texts))


def pcode_operation_texts(operations: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for record in operations:
        spec = record.get("spec", {})
        if "pcode" not in spec:
            continue
        for statement in pcode_statements(spec["pcode"]):
            text = str(statement).strip()
            if text:
                lines.append(text)
    return lines


def pcode_statements(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [part.strip() for part in value.splitlines() if part.strip()]
    if isinstance(value, dict):
        return [value]
    return []


def rep_observed_value_text(value: Any) -> str:
    text = str(value)
    names = {
        "src_value": "source value",
        "rhs_minus_lhs": "right operand minus left operand",
        "lhs_bitwise_and_rhs": "left operand bitwise-and right operand",
        "result_value": "result value",
    }
    return names.get(text, readable_text(text))


def repeat_observed_metadata_text(value: Any) -> str:
    if isinstance(value, dict):
        return "; ".join(f"{key}: {rep_observed_value_text(item)}" for key, item in value.items())
    return rep_observed_value_text(value)


def operation_latex(operations: list[dict[str, Any]]) -> str:
    explicit = explicit_operation_texts(operations)
    if explicit:
        return wrapped_operation_block([tex_escape(text) for text in explicit])
    pcode = pcode_operation_texts(operations)
    if pcode:
        return wrapped_operation_block([tex_escape(row) for row in pcode])
    texts = operation_texts(operations)
    if not texts:
        return ""
    rows = []
    for text in texts:
        for piece in [part.strip() for part in text.split(";") if part.strip()]:
            rows.append(operation_piece_latex(piece))
    return wrapped_operation_block(rows)


def wrapped_operation_block(rows: list[str]) -> str:
    if not rows:
        return ""
    body = r"\par ".join(r"\noindent " + row for row in rows)
    return r"\begin{manualraggedblock}" + body + r"\end{manualraggedblock}"


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


def wrapped_line_block(lines: list[str]) -> str:
    body = "".join(
        r"\noindent " + tex_escape(line) + r"\par "
        for line in lines
    )
    return r"\begin{manualraggedblock}" + body + r"\end{manualraggedblock}"


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
    return wrapped_line_block(attrs)


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
    upper = size.upper()
    if upper in spec_size_kinds(active_spec()):
        labels = [
            size_code_label(active_spec(), str(item.get("code")))
            for item in size_kind_entries(active_spec(), upper)
            if item.get("code") is not None
        ]
        return ", ".join(labels)
    if upper in size_codes(active_spec()):
        return size_code_label(active_spec(), upper)
    return size


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


def word_name(token: int, storage: str = "") -> str:
    if token == 0:
        return "primary word"
    if token == 1:
        return "extended opcode word"
    _ = storage
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
    immediate = immediate_operand_metadata(kind)
    if immediate:
        signed_text = "signed" if immediate.get("signed") else "unsigned"
        return f"{signed_text} {immediate.get('width')}-bit immediate literal"
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
        "imm16": "16-bit immediate literal",
        "BITMAP16": "16-bit register bitmap",
        "bitmap16": "16-bit register bitmap",
        "fbitmap16": "16-bit floating-point register bitmap",
    }
    upper = kind.upper()
    if upper in spec_size_kinds(active_spec()):
        return "size selector"
    if upper in size_codes(active_spec()):
        return f"fixed {size_code_label(active_spec(), upper)} size"
    return mapping.get(kind, kind.replace("_", " ").lower())


def immediate_operand_metadata(kind: str) -> dict[str, Any]:
    operand_schema = ((active_spec().get("instructions") or {}).get("operand_schema") or {})
    immediate_operands = operand_schema.get("immediate_operands") or {}
    if not isinstance(immediate_operands, dict):
        return {}
    body = immediate_operands.get(kind) or immediate_operands.get(kind.lower())
    return body if isinstance(body, dict) else {}


def immediate_operation_size_note(kind: str) -> str:
    immediate = immediate_operand_metadata(kind)
    if not immediate:
        return ""
    extension = str(immediate.get("operation_size_extension") or "")
    applies_when = str(immediate.get("applies_when") or "operation-size forms")
    if extension == "zero_extend":
        return f" The encoded value is zero-extended before use for {applies_when}."
    if extension == "sign_extend":
        return f" The encoded value is sign-extended before use for {applies_when}."
    return ""


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
        storage = str(field.get("storage", ""))
        line = (
            f"{symbol}: {kind_description(kind)} for the {role_name(source)} "
            f"({word_name(token, storage)} bits {bit_text})."
        )
        if kind == "EA":
            line += " EA field selects register, memory, immediate, and extended EA forms."
        line += immediate_operation_size_note(kind)
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
    return note


def flags_text(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> str:
    for record in records:
        spec = record.get("spec", {})
        if "flags" in spec:
            return integer_flags_text(spec["flags"])
        if "fp_flags" in spec:
            return fp_flags_text(spec["fp_flags"])
    ordered_operations = sorted(
        operations,
        key=lambda record: 0 if record.get("group") == "instruction_override" else 1,
    )
    for record in ordered_operations:
        spec = record.get("spec", {})
        if "flags" in spec:
            return integer_flags_text(spec["flags"])
        if "fp_flags" in spec:
            return fp_flags_text(spec["fp_flags"])
    return ""


def integer_flags_text(value: Any) -> str:
    if isinstance(value, dict):
        if "description" in value:
            return compact_text(value["description"])
        flag_keys = [key for key in flag_order() if key in value]
        if flag_keys:
            return "; ".join(f"{key}: {readable_text(value[key])}" for key in flag_keys)
        return readable_text(value)
    return normalize_text(value)


def fp_flags_text(value: Any) -> str:
    if isinstance(value, dict):
        if "description" in value:
            return compact_text(value["description"])
        if "update" in value:
            return "update: " + fflags_list_text(value["update"])
        if "update_when_required" in value:
            return "update when required: " + fflags_list_text(value["update_when_required"])
        if value.get("unchanged") is True:
            return "FFLAGS unchanged"
        return readable_text(value)
    text = str(value)
    if text == "unchanged":
        return "FFLAGS unchanged"
    if text == "update_FFLAGS":
        return "update: " + fflags_list_text(fflag_order())
    if text == "update_when_conversion_or_compare_requires":
        return "update when required: " + fflags_list_text(fflag_order())
    if text.startswith("update_FFLAGS_"):
        suffix = text.removeprefix("update_FFLAGS_")
        meanings = fflag_meanings()
        names = [part for part in suffix.split("_") if part in meanings]
        if names:
            return "update: " + fflags_list_text(names)
    return readable_text(text)


def fflags_list_text(flags: Any) -> str:
    if isinstance(flags, str):
        names = [flags]
    else:
        names = [str(flag) for flag in flags]
    meanings = fflag_meanings()
    expanded = [f"FFLAGS.{name} ({meanings.get(name, name)})" for name in names]
    return ", ".join(expanded)


def condition_code_section(records: list[dict[str, Any]], operations: list[dict[str, Any]]) -> str:
    text = flags_text(records, operations) or "unchanged"
    if "FFLAGS" in text:
        flags = fflag_marks(text)
        rows = [
            " & ".join(r"\textbf{" + flag + "}" for flag in fflag_order()) + r"\\",
            " & ".join(tex_escape(flags[flag]) for flag in fflag_order()) + r"\\",
        ]
        table = r"\begin{tabular}[t]{@{}ccccc@{}}" + "\n" + "\n".join(rows) + "\n" + r"\end{tabular}"
        return rf"\manualinstructionstatus{{Floating-Point Status}}{{{status_detail_block(table, text)}}}"
    flags = flag_marks(text)
    rows = [
        " & ".join(r"\textbf{" + flag + "}" for flag in flag_order()) + r"\\",
        " & ".join(tex_escape(flags[flag]) for flag in flag_order()) + r"\\",
    ]
    table = r"\begin{tabular}[t]{@{}cccc@{}}" + "\n" + "\n".join(rows) + "\n" + r"\end{tabular}"
    return rf"\manualinstructionstatus{{Condition Codes}}{{{status_detail_block(table, readable_text(text))}}}"


def status_detail_block(table: str, text: str) -> str:
    return (
        r"\begin{manualraggedblock}"
        + table
        + r"\par\smallskip "
        + tex_escape(text)
        + r"\end{manualraggedblock}"
    )


def fflag_marks(text: str) -> dict[str, str]:
    if "unchanged" in text.lower():
        return {flag: "-" for flag in fflag_order()}
    return {flag: "*" if f"FFLAGS.{flag}" in text else "-" for flag in fflag_order()}


def flag_marks(text: str) -> dict[str, str]:
    lower = text.lower()
    normalized = lower.replace("-", "_").replace("/", "_").replace(" ", "_")
    marks = {flag: "-" for flag in flag_order()}
    if "unchanged" in lower:
        return marks
    if "clear_cv" in normalized or "clear_c_v" in normalized:
        marks.update({"Z": "*", "N": "*", "C": "0", "V": "0"})
        return marks
    if "zncv" in lower or "z_n_c_v" in normalized or "subtract" in lower or "compare" in lower:
        return {flag: "*" for flag in flag_order()}
    if "update z/n" in lower or "z_n" in normalized or "zn" in lower:
        marks.update({"Z": "*", "N": "*"})
    if "set z" in lower or "z:" in lower or "z=" in lower:
        marks["Z"] = "*"
    if "v:" in lower or "v =" in lower or "v_" in lower:
        marks["V"] = "*"
    return marks


def instruction_format_section(items: list[dict[str, Any]]) -> str:
    if not items:
        return r"\manualinstructionfield{Instruction Format}{No allocated instruction format.}"
    blocks = [r"\begin{manualinstructionformat}"]
    for item in items:
        fields = line_fields(item)
        syntax = line_syntax_text(item, fields)
        tokens = encoding_pattern_tokens(item, fields)
        labels = [f"word {index}" for index in range(len(tokens))]
        blocks.append(r"\begin{manualformblock}{1.8in}")
        blocks.append(rf"\textbf{{Form:}} {tex_escape(form_label(item, fields))}\par")
        blocks.append(rf"\textbf{{Syntax:}} {tex_code(syntax)}\par")
        blocks.append(bit_diagram(tokens, f"Instruction format for {syntax}", labels))
        blocks.append(field_explanation_block(item, fields))
        blocks.append(r"\end{manualformblock}")
    blocks.append(r"\end{manualinstructionformat}")
    return "\n".join(blocks)


def instruction_forms_section(
    items: list[dict[str, Any]],
    lengths: dict[tuple[str, str], tuple[int, int]],
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
) -> str:
    if not items:
        return r"\manualinstructionfield{Instruction Forms}{No allocated instruction forms.}"
    blocks = [r"\begin{manualinstructionforms}"]
    for item in items:
        min_words, max_words, note = default_words(item, lengths)
        fields = line_fields(item)
        syntax = line_syntax_text(item, fields)
        tokens = encoding_pattern_tokens(item, fields)
        labels = [f"word {index}" for index in range(len(tokens))]
        blocks.append(r"\begin{manualformblock}{2.9in}")
        blocks.append(rf"\textbf{{{tex_code(syntax)}}}\par")
        blocks.append(r"\vspace{2pt}")
        blocks.append(r"\begin{tabularx}{\linewidth}{@{}p{0.88in}X@{}}")
        blocks.append(rf"\textbf{{Form}} & {tex_escape(form_label(item, fields))}\\")
        blocks.append(rf"\textbf{{Encoding}} & {tex_escape(user_encoding_text(item))}\\")
        blocks.append(rf"\textbf{{Words}} & {tex_escape(f'{min_words}-{max_words}')}\\")
        blocks.append(rf"\textbf{{Privilege}} & {tex_escape(privilege_text(item_privilege(item, records, operations)))}\\")
        blocks.append(rf"\textbf{{Operands}} & {tex_escape(readable_operands_text(item))}\\")
        if note:
            blocks.append(rf"\textbf{{Notes}} & {tex_escape(readable_note_text(note))}\\")
        blocks.append(r"\end{tabularx}\par")
        blocks.append(bit_diagram(tokens, f"Instruction format for {syntax}", labels))
        blocks.append(field_explanation_block(item, fields))
        blocks.append(r"\end{manualformblock}")
    blocks.append(r"\end{manualinstructionforms}")
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
        if note:
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
        word = word_name(token, str(field.get("storage", "")))
        high = int(field.get("high_bit", 0))
        low = int(field.get("low_bit", 0))
        bit_text = str(low) if high == low else f"{high}:{low}"
        pieces.append(
            f"{field_symbol(field)}={field.get('source', field.get('name', ''))}:"
            f"{field.get('kind', '')}[{bit_text}] in {word}"
        )
    return "; ".join(pieces)
