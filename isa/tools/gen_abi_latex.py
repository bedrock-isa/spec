#!/usr/bin/env python3
"""Generate a LaTeX ABI document from a Bedrock ABI YAML file."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import re
import sys

import yaml

sys.dont_write_bytecode = True

TEMPLATE_DIR = Path(__file__).parent / "latex_builder" / "templates"
TABLE_INLINE_LIST_MAX_CHARS = 32
TABLE_INLINE_ITEM_MAX_CHARS = 20
REGISTER_LIST_RE = re.compile(r"(?:R|F)\d{1,2}|SP|PC|CS|DS|SS|GS\d")

ABI_HIERARCHY_LABELS = {
    "standard_library_abi": ["Standard Library ABI"],
    "language_abi": ["Language ABI"],
    "os_abi": ["OS ABI"],
    "language_neutral_object_format": ["ELF ABI"],
}

ABI_LAYER_ALIASES = {
    "elf abi": "language_neutral_object_format",
    "elf": "language_neutral_object_format",
    "object format abi": "language_neutral_object_format",
    "language-neutral object format": "language_neutral_object_format",
    "language_neutral_object_format": "language_neutral_object_format",
    "language abi": "language_abi",
    "language_abi": "language_abi",
    "os abi": "os_abi",
    "os_abi": "os_abi",
    "standard library abi": "standard_library_abi",
    "standard_library_abi": "standard_library_abi",
}


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def abi_layer_id(value: Any) -> str:
    key = str(value or "elf abi").strip().lower().replace("_", " ")
    return ABI_LAYER_ALIASES.get(key, str(value or "language_neutral_object_format"))

class AbiRootSchema:
    name = "ABI root"
    keys = {
        "document",
        "scope",
        "abi_hierarchy",
        "terminology",
    }

    def matches(self, path: Path, abi: dict[str, Any]) -> bool:
        return False

    def validate(self, path: Path, abi: Any) -> None:
        if not isinstance(abi, dict):
            raise ValueError(f"{path}: ABI document must be a mapping")
        unknown = sorted(str(key) for key in abi if str(key) not in self.keys)
        if unknown:
            raise ValueError(f"{path}: unknown ABI root keys: {', '.join(unknown)}")


class LanguageNeutralAbiSchema(AbiRootSchema):
    name = "ELF ABI root"
    keys = AbiRootSchema.keys | {
        "object_format",
        "register_banking",
        "sections",
        "symbols",
        "program_loading",
        "dynamic_linking",
        "tls",
        "code_models",
        "relocations",
        "assembler_contract",
    }

    def matches(self, path: Path, abi: dict[str, Any]) -> bool:
        return not CAbiSchema().matches(path, abi)


class CAbiSchema(AbiRootSchema):
    name = "C ABI root"
    keys = AbiRootSchema.keys | {
        "data_model",
        "register_convention",
        "calling_convention",
        "examples",
        "freestanding_c",
        "memory_model",
        "system_interface",
    }

    def matches(self, path: Path, abi: dict[str, Any]) -> bool:
        current_layer = str((abi.get("abi_hierarchy") or {}).get("current_layer", "")).lower()
        return "language abi" in current_layer or path.name.lower().startswith("c_")


class AbiSchema:
    def __init__(self) -> None:
        self.candidates: tuple[AbiRootSchema, ...] = (CAbiSchema(), LanguageNeutralAbiSchema())

    def for_document(self, path: Path, abi: Any) -> AbiRootSchema:
        if not isinstance(abi, dict):
            return LanguageNeutralAbiSchema()
        for candidate in self.candidates:
            if candidate.matches(path, abi):
                return candidate
        return LanguageNeutralAbiSchema()

    def validate(self, path: Path, abi: Any) -> None:
        self.for_document(path, abi).validate(path, abi)


def tex_escape(value: Any) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "|": r"\textbar{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    escaped = "".join(replacements.get(ch, ch) for ch in text)
    return escaped.replace(r"-\textgreater{}", r"\ensuremath{\rightarrow{}}")


def tex_code(value: Any) -> str:
    text = tex_escape(value).replace(r"\_", r"\_\allowbreak{}")
    return r"\texttt{" + text + "}"


def tex_cell_lines(lines: list[str]) -> str:
    body = r"\\".join(lines)
    return r"\begin{tabular}[t]{@{}l@{}}" + body + r"\end{tabular}"


def is_register_name_list(items: list[Any], text_fn: Any = str) -> bool:
    texts = [" ".join(str(text_fn(item)).split()) for item in items]
    return bool(texts) and all(REGISTER_LIST_RE.fullmatch(text) for text in texts)


def table_list_should_stack(items: list[Any], text_fn: Any = str) -> bool:
    if is_register_name_list(items, text_fn):
        return False
    texts = [" ".join(str(text_fn(item)).split()) for item in items]
    joined = ", ".join(texts)
    return (
        len(joined) > TABLE_INLINE_LIST_MAX_CHARS
        or any(len(text) > TABLE_INLINE_ITEM_MAX_CHARS for text in texts)
    )


def tex_code_value(value: Any) -> str:
    if isinstance(value, list):
        if not value:
            return tex_escape("-")
        if table_list_should_stack(value):
            return tex_cell_lines([tex_code(item) for item in value])
        return ", ".join(tex_code(item) for item in value)
    return tex_code(value)


def tex_table_value(value: Any) -> str:
    if isinstance(value, list):
        if not value:
            return tex_escape("-")
        if table_list_should_stack(value, readable):
            return tex_cell_lines([tex_escape(readable(item)) for item in value])
        return ", ".join(tex_escape(readable(item)) for item in value)
    return tex_escape(readable(value))


def compact_text(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return yaml.safe_dump(value, sort_keys=False, allow_unicode=False).strip()
    return " ".join(str(value).split())


def readable(value: Any) -> str:
    return compact_text(value).replace("_", " ")


def template(name: str, values: dict[str, Any] | None = None) -> str:
    text = (TEMPLATE_DIR / name).read_text(encoding="utf-8")
    for key, value in (values or {}).items():
        text = text.replace(f"@{key}@", str(value))
    unresolved = sorted(set(re.findall(r"@[A-Z0-9_]+@", text)))
    if unresolved:
        raise ValueError(f"unresolved template placeholders in {name}: {', '.join(unresolved)}")
    return text


def section(title: str) -> str:
    return "\n".join([r"\clearpage", rf"\section{{{tex_escape(title)}}}"])


def subsection(title: str) -> str:
    return rf"\subsection{{{tex_escape(title)}}}"


def table(headers: list[str], rows: list[list[str]], widths: list[str], caption: str | None = None) -> str:
    if not rows:
        return "No entries.\\par\n"
    spec = "@{}" + "".join(f"p{{{width}}}" for width in widths) + "@{}"
    out: list[str] = []
    if caption:
        out.append(rf"\manualtablecaption{{{tex_escape(caption)}}}")
    out.extend([r"\begingroup\footnotesize", r"\setlength{\tabcolsep}{2pt}", rf"\begin{{longtable}}{{{spec}}}", r"\toprule"])
    out.append(" & ".join(r"\textbf{" + tex_escape(header) + "}" for header in headers) + r"\\")
    out.extend([r"\midrule", r"\endhead"])
    for row in rows:
        out.append(" & ".join(row) + r"\\")
    out.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup"])
    return "\n".join(out)


def bullet_list(items: list[Any]) -> str:
    if not items:
        return ""
    out = [r"\begin{itemize}"]
    out.extend(rf"\item {tex_escape(readable(item))}" for item in items)
    out.append(r"\end{itemize}")
    return "\n".join(out)


def code_block(text: str) -> str:
    out = [r"\begingroup\small\ttfamily", r"\begin{tabularx}{\linewidth}{@{}X@{}}"]
    for line in str(text).rstrip().splitlines() or [""]:
        out.append(tex_escape(line) + r"\tabularnewline")
    out.extend([r"\end{tabularx}", r"\endgroup"])
    return "\n".join(out)


def field(name: str, value: Any) -> str:
    return rf"\manualfield{{{tex_escape(name)}:}}{{{tex_escape(readable(value))}}}"


def mapping_rows(
    mapping: dict[str, Any],
    code_keys: set[str] | None = None,
    code_label_keys: set[str] | None = None,
) -> list[list[str]]:
    code_keys = code_keys or set()
    code_label_keys = code_label_keys or set()
    rows: list[list[str]] = []
    for key, value in mapping.items():
        label = tex_code(key) if key in code_label_keys else tex_escape(readable(key))
        cell = tex_code_value(value) if key in code_keys else tex_table_value(value)
        rows.append([label, cell])
    return rows


def tex_node_label(lines: list[str], current: bool = False) -> str:
    rendered = [tex_escape(line) for line in lines]
    if current:
        rendered.append(r"{\footnotesize Current document}")
    return r"\\".join(rendered)


def abi_layer_style(current_layer: str, layer_id: str) -> str:
    return "currentAbiLayerBox" if current_layer == layer_id else "abiLayerBox"


def render_abi_hierarchy_diagram(current_layer: str) -> str:
    current_layer = abi_layer_id(current_layer)
    style = {
        layer_id: abi_layer_style(current_layer, layer_id)
        for layer_id in ABI_HIERARCHY_LABELS
    }
    label = {
        layer_id: tex_node_label(lines, current=(current_layer == layer_id))
        for layer_id, lines in ABI_HIERARCHY_LABELS.items()
    }
    return "\n".join(
        [
            r"\Needspace{2.7in}",
            r"\begin{center}",
            r"\begin{tikzpicture}[",
            r"  abiLayerBox/.style={draw=RuleGray, fill=white, line width=0.75pt, minimum height=0.72cm, align=center, font=\small\bfseries},",
            r"  currentAbiLayerBox/.style={abiLayerBox, fill=black!12, line width=1.15pt},",
            r"  abiAxis/.style={-{Latex[length=2.2mm,width=1.7mm]}, draw=RuleGray, line width=0.65pt}",
            r"]",
            rf"\node[{style['standard_library_abi']}, minimum width=11.0cm, text width=10.4cm] (standard) at (0,2.10) {{{label['standard_library_abi']}}};",
            rf"\node[{style['language_abi']}, minimum width=5.35cm, text width=4.8cm] (language) at (-2.825,1.05) {{{label['language_abi']}}};",
            rf"\node[{style['os_abi']}, minimum width=5.35cm, text width=4.8cm] (os) at (2.825,1.05) {{{label['os_abi']}}};",
            rf"\node[{style['language_neutral_object_format']}, minimum width=11.0cm, text width=10.4cm] (object) at (0,0.00) {{{label['language_neutral_object_format']}}};",
            r"\draw[abiAxis] (-5.85,-0.34) -- (-5.85,2.43);",
            r"\node[font=\footnotesize, rotate=90, anchor=south] at (-6.13,1.05) {higher-level contracts};",
            r"\end{tikzpicture}",
            r"\end{center}",
        ]
    )


def render_abi_hierarchy(abi: dict[str, Any]) -> str:
    hierarchy = abi.get("abi_hierarchy", {})
    if not hierarchy:
        return ""

    current_layer = abi_layer_id(hierarchy.get("current_layer", "elf abi"))
    parts = [
        subsection("ABI Hierarchy"),
        tex_escape(readable(hierarchy.get("summary", ""))),
        render_abi_hierarchy_diagram(current_layer),
    ]
    current_scope = hierarchy.get("current_document_scope", "")
    if current_scope:
        parts.append(r"\noindent\textbf{Current document.} " + tex_escape(readable(current_scope)))
    return "\n".join(part for part in parts if part)


def render_scope(abi: dict[str, Any]) -> str:
    scope = abi.get("scope", {})
    rows = [
        [tex_code(profile.get("name", "")), tex_escape(readable(profile.get("description", "")))]
        for profile in scope.get("profiles", [])
    ]
    parts = [
        section("Scope and Profiles"),
        tex_escape(readable(scope.get("summary", ""))),
        render_abi_hierarchy(abi),
        subsection("ABI Profiles"),
        table(["Profile", "Meaning"], rows, ["1.35in", "4.15in"], "Reference ABI Profiles"),
    ]
    return "\n".join(part for part in parts if part)


def description_list(terms: list[dict[str, Any]]) -> str:
    rows = [
        r"\begin{description}[style=nextline,leftmargin=1.45in,labelwidth=1.35in,itemsep=3pt,topsep=3pt]"
    ]
    for item in terms:
        term = item.get("term", "")
        definition = item.get("definition", "")
        if term and definition:
            rows.append(rf"\item[{tex_escape(term)}] {tex_escape(compact_text(definition))}")
    rows.append(r"\end{description}")
    return "\n".join(rows)


def render_terminology(abi: dict[str, Any]) -> str:
    terminology = abi.get("terminology", {})
    if not terminology:
        return ""
    parts = [section("Terminology")]
    summary = terminology.get("summary", "")
    if summary:
        parts.append(tex_escape(compact_text(summary)))
    terms = terminology.get("terms") or []
    if terms:
        parts.append(description_list([item for item in terms if isinstance(item, dict)]))
    for group in terminology.get("groups") or []:
        if not isinstance(group, dict):
            continue
        name = group.get("name", "")
        group_terms = group.get("terms") or []
        if name:
            parts.append(subsection(name))
        parts.append(description_list([item for item in group_terms if isinstance(item, dict)]))
    return "\n".join(part for part in parts if part)


def render_data_model(abi: dict[str, Any]) -> str:
    model = abi.get("data_model", {})
    if not model:
        return ""
    scalar_rows = [
        [
            tex_code(item.get("name", "")),
            tex_escape(item.get("bits", "")),
            tex_escape(item.get("alignment", "")),
        ]
        for item in model.get("scalar_types", [])
    ]
    header_size = model.get("instruction_header_bits", "")
    parts = [
        section("Data Model"),
        field("Model", model.get("name", "")),
        field("Byte Order", model.get("byte_order", "")),
        field("Instruction Header", f"{header_size} bits" if header_size != "" else ""),
        field("Stack Alignment", f"{model.get('stack_alignment_bytes', '')} bytes"),
        field("Aggregate Maximum Alignment", f"{model.get('aggregate_alignment_max_bytes', '')} bytes"),
        subsection("Scalar Types"),
        table(["Type", "Bits", "Align"], scalar_rows, ["2.1in", "1.0in", "1.0in"], "Reference C Data Model"),
        subsection("Layout Rules"),
        bullet_list(model.get("layout_rules", [])),
    ]
    return "\n".join(part for part in parts if part)


def render_object_format(abi: dict[str, Any]) -> str:
    obj = abi.get("object_format", {})
    if not obj:
        return ""
    machine = obj.get("machine", {})
    flags = obj.get("flags", {})
    reloc = obj.get("relocations", {})
    sections = obj.get("sections", {})
    ident = obj.get("elf_ident", {})
    header_sizes = obj.get("header_sizes", {})
    entry_point = obj.get("entry_point", {})
    program_header = obj.get("program_header", {})
    section_header = obj.get("section_header", {})
    symbol_values = obj.get("symbol_values", {})
    extension_attributes = obj.get("extension_attributes", {})
    rows = [
        [tex_escape("Format"), tex_code_value(obj.get("format", ""))],
        [tex_escape("ELF Class"), tex_code_value(obj.get("elf_class", ""))],
        [tex_escape("Data Encoding"), tex_code_value(obj.get("data_encoding", ""))],
        [tex_escape("File Types"), tex_code_value(obj.get("file_type_model", ""))],
        [tex_escape("Machine"), tex_code_value(f"{machine.get('name', '')} ({machine.get('value', '')})")],
        [tex_escape("e_flags"), tex_escape(readable(flags.get("e_flags", "")))],
        [tex_escape("Unknown nonzero e_flags"), tex_escape(readable(flags.get("unknown_nonzero_e_flags", "")))],
        [tex_escape("Extension metadata"), tex_code(flags.get("extension_metadata", ""))],
        [tex_escape("Relocation Encoding"), tex_code_value(reloc.get("encoding", ""))],
        [tex_escape("Relocation Addend"), tex_escape(readable(reloc.get("addend_storage", "")))],
        [tex_escape("String Table"), tex_code(sections.get("string_table", ""))],
        [tex_escape("Symbol Table"), tex_code(sections.get("symbol_table", ""))],
        [tex_escape("Relocation Prefix"), tex_code(sections.get("relocation_prefix", ""))],
    ]
    parts = [
        section("ELF Object Format"),
        table(["Field", "Value"], rows, ["1.8in", "3.7in"], "ELF Identification"),
    ]
    if ident:
        parts.extend(
            [
                subsection("ELF Identification Bytes"),
                table(
                    ["e_ident Field", "Value"],
                    mapping_rows(ident, set(ident), set(ident)),
                    ["1.55in", "3.95in"],
                    "ELF e_ident Values",
                ),
            ]
        )
    if header_sizes:
        parts.extend(
            [
                subsection("ELF Header Sizes"),
                table(
                    ["Header Field", "Bytes"],
                    mapping_rows(header_sizes, code_label_keys=set(header_sizes)),
                    ["1.55in", "3.95in"],
                    "ELF Header Size Values",
                ),
            ]
        )
    if entry_point:
        parts.extend(
            [
                subsection("Entry Point Semantics"),
                table(
                    ["File Type", "e_entry Meaning"],
                    mapping_rows(entry_point, code_label_keys=set(entry_point)),
                    ["1.75in", "3.75in"],
                    "ELF Entry Point Rules",
                ),
            ]
        )
    if program_header:
        ph_rows = []
        if program_header.get("supported_types"):
            ph_rows.append([tex_escape("Supported p_type"), tex_code_value(program_header["supported_types"])])
        for key, value in (program_header.get("p_flags") or {}).items():
            ph_rows.append([tex_code(key), tex_table_value(value)])
        for key, value in (program_header.get("p_align") or {}).items():
            ph_rows.append([tex_code(f"p_align {key}"), tex_table_value(value)])
        parts.extend(
            [
                subsection("Program Header Policy"),
                table(["Field", "Rule"], ph_rows, ["1.75in", "3.75in"], "ELF Program Header Rules"),
            ]
        )
    if section_header or symbol_values:
        rows2 = []
        for key, value in section_header.items():
            rows2.append([tex_escape(readable(key)), tex_code_value(value) if isinstance(value, list) else tex_table_value(value)])
        for key, value in symbol_values.items():
            rows2.append([tex_code(key), tex_table_value(value)])
        parts.extend(
            [
                subsection("Section and Symbol Policy"),
                table(["Field", "Rule"], rows2, ["1.75in", "3.75in"], "ELF Section and Symbol Rules"),
            ]
        )
    if extension_attributes:
        attr_rows = []
        for name, body in extension_attributes.items():
            if not isinstance(body, dict):
                continue
            attr_rows.append(
                [
                    tex_code(name),
                    tex_escape(readable(body.get("encoding", ""))),
                    tex_escape(readable(body.get("default", ""))),
                    tex_escape(readable(body.get("meaning", ""))),
                ]
            )
        parts.extend(
            [
                subsection("Bedrock Object Attributes"),
                table(["Attribute", "Encoding", "Default", "Meaning"], attr_rows, ["1.65in", "1.0in", "0.65in", "2.20in"], "Bedrock ELF Attribute Notes"),
            ]
        )
    return "\n".join(parts)


def render_register_banking(abi: dict[str, Any]) -> str:
    banking = abi.get("register_banking", {})
    if not banking:
        return ""
    arch = banking.get("architectural_model", {})
    attributes = banking.get("object_attribute_rules", {})
    parts = [
        section(banking.get("title", "Register Banking")),
        tex_escape(readable(banking.get("summary", ""))),
    ]
    if arch:
        parts.extend(
            [
                subsection("Architectural ABI Model"),
                table(
                    ["Item", "Rule"],
                    mapping_rows(arch, {"selector"}),
                    ["1.9in", "3.6in"],
                    banking.get("model_caption", "Register Banking Model"),
                ),
            ]
        )
    if banking.get("boundary_rules"):
        parts.extend(
            [
                subsection(banking.get("boundary_title", "ABI Boundaries")),
                bullet_list(banking.get("boundary_rules", [])),
            ]
        )
    if attributes:
        parts.extend(
            [
                subsection("Object Attribute Rules"),
                table(
                    ["Rule", "Value"],
                    mapping_rows(attributes, {"required_attribute"}),
                    ["2.05in", "3.45in"],
                    banking.get("attribute_caption", "Register Banking Object Attribute Rules"),
                ),
            ]
        )
    if banking.get("recommended_use"):
        parts.extend(
            [
                subsection("Recommended Uses"),
                bullet_list(banking.get("recommended_use", [])),
            ]
        )
    return "\n".join(part for part in parts if part)


def render_program_loading(abi: dict[str, Any]) -> str:
    loading = abi.get("program_loading", {})
    if not loading:
        return ""
    permission_rows = [
        [
            tex_code(item.get("p_flags", "")),
            tex_table_value(item.get("pte_flags", [])),
            tex_table_value(item.get("meaning", "")),
        ]
        for item in loading.get("page_permission_mapping", [])
    ]
    initial_rows = [
        [tex_code(key), tex_code(value) if key in {"CS", "DS", "SS"} else tex_table_value(value)]
        for key, value in (loading.get("initial_state") or {}).items()
    ]
    environment_rows = mapping_rows(loading.get("execution_environment", {}))
    parts = [
        section("Program Loading"),
        tex_escape(readable(loading.get("summary", ""))),
        subsection("Loading Rules"),
        table(
            ["Rule", "Value"],
            mapping_rows(
                loading.get("rules", {}),
                {"executable_file_types"},
                {"PT_INTERP"},
            ),
            ["2.0in", "3.5in"],
            "ELF Loading Rules",
        ),
        subsection("Page Permissions"),
        table(["ELF Flags", "PTE Flags", "Meaning"], permission_rows, ["1.2in", "1.45in", "2.85in"], "ELF Segment Permission Mapping"),
    ]
    if environment_rows:
        parts.extend(
            [
                subsection("Execution Environment"),
                table(["Requirement", "Rule"], environment_rows, ["1.7in", "3.8in"], "Loader Execution Environment"),
            ]
        )
    if initial_rows:
        parts.extend(
            [
                subsection("Initial Non-Segment State"),
                table(["Register", "Initial Value"], initial_rows, ["1.2in", "4.3in"], "Loader Initial Non-Segment State"),
            ]
        )
    return "\n".join(part for part in parts if part)


def register_rows(registers: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for group_name, group in registers.items():
        if group_name == "data_register_banking":
            continue
        if isinstance(group, dict):
            for key, value in group.items():
                rows.append([tex_table_value(group_name), tex_table_value(key), tex_table_value(value)])
        else:
            rows.append([tex_table_value(group_name), tex_escape("-"), tex_table_value(group)])
    return rows


def render_data_register_banking_convention(registers: dict[str, Any]) -> str:
    banking = registers.get("data_register_banking", {})
    if not banking:
        return ""
    rows = [
        [tex_table_value(key), tex_table_value(value)]
        for key, value in banking.items()
        if key not in {"summary", "recommended_compiler_policy"}
    ]
    parts = [
        subsection(banking.get("title", "Register Banking")),
        tex_escape(readable(banking.get("summary", ""))),
        table(
            ["Rule", "Value"],
            rows,
            ["2.0in", "3.5in"],
            banking.get("caption", "C ABI Register Banking Rules"),
        ),
    ]
    if banking.get("recommended_compiler_policy"):
        parts.extend(
            [
                r"\noindent\textbf{Recommended compiler policy.}",
                bullet_list(banking.get("recommended_compiler_policy", [])),
            ]
        )
    return "\n".join(part for part in parts if part)


def render_register_convention(abi: dict[str, Any]) -> str:
    registers = abi.get("register_convention", {})
    if not registers:
        return ""
    return "\n".join(
        [
            section("Register Convention"),
            table(["Group", "Rule", "Registers / Meaning"], register_rows(registers), ["1.35in", "1.55in", "2.6in"], "Register Preservation and Assignment"),
            render_data_register_banking_convention(registers),
        ]
    )


def bytes_value(value: Any) -> str:
    return tex_escape(str(value))


def rule_value(mapping: dict[str, Any], key: str, default: Any = "") -> Any:
    return mapping.get(key, default)


def render_calling_convention_template(call: dict[str, Any]) -> str:
    stack = call.get("stack", {})
    return_address = call.get("return_address", {})
    arguments = call.get("argument_passing", {})
    returns = (call.get("return_values", {}) or {}).get("c_binding", {})
    aggregate_rules = (call.get("aggregate_passing", {}) or {}).get("rules", {})
    varargs_rules = (call.get("varargs", {}) or {}).get("rules", {})
    frame_pointer = call.get("frame_pointer", {})
    i128_pair = arguments.get("scalar_128_bit_integer_register_pair", {})
    if not isinstance(i128_pair, dict):
        i128_pair = {"registers": i128_pair, "low_register": "", "high_register": ""}
    small_aggregate = aggregate_rules.get("small_aggregate_register_return", {})
    if not isinstance(small_aggregate, dict):
        small_aggregate = {"max_size_bytes": 16, "registers": small_aggregate}
    general_argument_registers = rule_value(arguments, "general_registers", [])
    general_return = rule_value(returns, "general_scalar")

    return template(
        "c_abi_calling_convention.tex",
        {
            "STACK_DIRECTION": tex_escape(readable(rule_value(stack, "grows"))),
            "RETURN_ADDRESS_SIZE": bytes_value(rule_value(return_address, "size_bytes")),
            "RETURN_ADDRESS_LOCATION": tex_code(rule_value(return_address, "location_at_entry")),
            "STACK_ENTRY_ALIGNMENT": bytes_value(rule_value(stack, "entry_alignment")),
            "FRAME_POINTER_DEFAULT": tex_escape(readable(rule_value(frame_pointer, "default"))),
            "FRAME_POINTER_REGISTER": tex_code(rule_value(frame_pointer, "conventional_register")),
            "FRAME_POINTER_NOTE": tex_escape(readable(rule_value(frame_pointer, "note"))),
            "GENERAL_ARGUMENT_REGISTERS": tex_code_value(general_argument_registers),
            "FP_ARGUMENT_REGISTERS": tex_code_value(rule_value(arguments, "floating_point_registers", [])),
            "STACK_ARGUMENT_ORDER": tex_escape(readable(rule_value(arguments, "stack_arguments"))),
            "STACK_ARGUMENT_SLOT_SIZE": bytes_value(rule_value(arguments, "stack_argument_slot_size")),
            "STACK_ARGUMENT_ALIGNMENT": bytes_value(rule_value(arguments, "stack_argument_alignment")),
            "I128_REGISTERS": tex_code(rule_value(i128_pair, "registers")),
            "I128_LOW_REGISTER": tex_code(rule_value(i128_pair, "low_register")),
            "I128_HIGH_REGISTER": tex_code(rule_value(i128_pair, "high_register")),
            "I128_STACK_ALIGNMENT": bytes_value(rule_value(arguments, "scalar_128_bit_stack_slot_alignment")),
            "STACK_VALUE_PLACEMENT": tex_escape(readable(rule_value(arguments, "stack_argument_value_placement"))),
            "GENERAL_RETURN": tex_code(general_return),
            "FP_RETURN": tex_code(rule_value(returns, "floating_point_scalar")),
            "LONG_DOUBLE_RETURN": tex_code(rule_value(returns, "long_double_scalar")),
            "I128_RETURN": tex_code(rule_value(returns, "scalar_128_bit")),
            "SMALL_AGG_RETURN": tex_code(rule_value(returns, "small_aggregate_up_to_16_bytes")),
            "SRET_REGISTER": tex_code(rule_value(aggregate_rules, "conditional_sret_buffer_argument_register")),
            "SRET_RETURN_REGISTER": tex_code(rule_value(aggregate_rules, "return_register_result")),
            "AGG_COPY_ALIGNMENT": bytes_value(rule_value(aggregate_rules, "argument_copy_alignment")),
            "AGG_COPY_REGISTERS": tex_code_value(rule_value(aggregate_rules, "argument_copy_registers", [])),
            "AGG_REGISTER_ARGUMENTS": tex_escape(readable(rule_value(aggregate_rules, "aggregate_register_arguments"))),
            "SMALL_AGGREGATE_MAX_SIZE": bytes_value(rule_value(small_aggregate, "max_size_bytes")),
            "SMALL_AGGREGATE_REGISTERS": tex_code(rule_value(small_aggregate, "registers")),
            "SMALL_AGGREGATE_LAYOUT": tex_escape(readable(rule_value(aggregate_rules, "small_aggregate_layout"))),
            "RETURN_BUFFER_ALIGNMENT": bytes_value(rule_value(aggregate_rules, "return_buffer_alignment")),
            "VARARG_REGISTER_SAVE_AREA": tex_escape(readable(rule_value(varargs_rules, "register_save_area"))),
            "VARARG_SLOT_SIZE": bytes_value(rule_value(varargs_rules, "variadic_stack_slot_size")),
            "VARARG_SLOT_ALIGNMENT": bytes_value(rule_value(varargs_rules, "variadic_stack_slot_alignment")),
            "VA_ARG_ALIGNMENT": bytes_value(rule_value(varargs_rules, "va_arg_alignment")),
            "VA_LIST": tex_escape(readable(rule_value(varargs_rules, "va_list"))),
        },
    )


def render_calling_convention(abi: dict[str, Any]) -> str:
    call = abi.get("calling_convention", {})
    if not call:
        return ""
    parts = [
        section("Calling Convention"),
        render_calling_convention_template(call),
    ]
    return "\n".join(part for part in parts if part)


def render_sections_symbols(abi: dict[str, Any]) -> str:
    sections = abi.get("sections", {})
    symbols = abi.get("symbols", {})
    if not sections and not symbols:
        return ""
    section_rows = [
        [tex_code(item.get("name", "")), tex_table_value(item.get("attributes", []))]
        for item in sections.get("standard", [])
    ]
    symbol_rows = [
        [tex_escape("Bindings"), tex_table_value(symbols.get("binding", []))],
        [tex_escape("Visibility"), tex_table_value(symbols.get("visibility", []))],
        [tex_escape("Types"), tex_table_value(symbols.get("types", []))],
    ]
    return "\n".join(
        [
            section("Sections and Symbols"),
            tex_escape(readable(sections.get("summary", ""))),
            subsection("Standard Sections"),
            table(["Section", "Attributes"], section_rows, ["1.45in", "4.05in"], "Standard Section Names"),
            subsection("Symbol Model"),
            table(["Item", "Values"], symbol_rows, ["1.25in", "4.25in"], "Symbol Classes"),
            bullet_list(symbols.get("rules", [])),
        ]
    )


def render_relocations(abi: dict[str, Any]) -> str:
    reloc = abi.get("relocations", {})
    if not reloc:
        return ""
    expr = reloc.get("expression_model", {})
    expr_code_keys = {"canonical_form"}
    expr_rows = [
        [
            tex_escape(readable(key)),
            tex_code(value) if key in expr_code_keys else tex_escape(readable(value)),
        ]
        for key, value in expr.items()
    ]
    term_rows = [
        [tex_code(item.get("name", "")), tex_escape(readable(item.get("meaning", "")))]
        for item in reloc.get("expression_terms", [])
    ]
    reloc_rows = []
    reloc_use_items = []
    for item in reloc.get("core_set", []):
        reloc_rows.append(
            [
                tex_escape(item.get("type_id", "")),
                tex_code(item.get("name", "")),
                tex_escape(relocation_size_text(item)),
                tex_code(item.get("calculation", "")),
            ]
        )
        reloc_use_items.append(
            rf"\item {tex_code(item.get('name', ''))}: {tex_escape(readable(item.get('use', '')))}"
        )
    parts = [
        section("Relocation Set"),
        "Bedrock ELF objects use RELA relocation entries with explicit addends. "
        "The Bedrock ABI defines how each relocation type patches instruction or data fields.",
        subsection("Expression Model"),
        table(["Rule", "Value"], expr_rows, ["1.75in", "3.75in"], "Relocation Expression Model"),
        subsection("Expression Terms"),
        table(["Term", "Meaning"], term_rows, ["1.0in", "4.5in"], "Relocation Expression Terms"),
        subsection("GOT and PLT Model"),
        bullet_list(reloc.get("got_plt_model", [])),
        subsection("Relocations"),
        table(["Type", "Name", "Size", "Calculation"], reloc_rows, ["0.45in", "2.15in", "0.85in", "2.05in"], "Bedrock ELF Relocation Types"),
        subsection("Relocation Uses"),
        "\n".join([r"\begin{itemize}"] + reloc_use_items + [r"\end{itemize}"]) if reloc_use_items else "",
    ]
    return "\n".join(part for part in parts if part)


def relocation_size_text(item: dict[str, Any]) -> str:
    width = item.get("width_bits", "")
    unit = readable(item.get("unit", ""))
    signed = item.get("signed", "")

    if width in {0, "0"} or unit == "none":
        return "0"

    parts: list[str] = []
    if str(width) == "variable":
        parts.append("variable-size")
    else:
        parts.append(f"{width}-bit")

    if unit and unit not in {"byte", "none"}:
        parts.append(unit.replace("16-bit word", "word-scaled"))

    if signed is True:
        parts.append("signed")
    elif signed is False:
        parts.append("unsigned")

    return " ".join(parts)


def render_dynamic_linking(abi: dict[str, Any]) -> str:
    dynamic = abi.get("dynamic_linking", {})
    if not dynamic:
        return ""
    got_rows = [
        [
            tex_escape(item.get("index", "")),
            tex_code(item.get("name", "")),
            tex_escape(readable(item.get("meaning", ""))),
        ]
        for item in dynamic.get("got_reserved_entries", [])
    ]
    plt_rows = [
        [tex_code(item.get("entry", "")), tex_escape(readable(item.get("effect", "")))]
        for item in dynamic.get("plt_layout", [])
    ]
    parts = [
        section("Dynamic Linking"),
        tex_escape(readable(dynamic.get("summary", ""))),
        subsection("Dynamic Linking Rules"),
        table(["Rule", "Value"], mapping_rows(dynamic.get("rules", {}), {"global_offset_table_symbol"}), ["2.0in", "3.5in"], "Dynamic Linking Rules"),
        subsection("GOT Reserved Entries"),
        table(["Index", "Name", "Meaning"], got_rows, ["0.55in", "1.55in", "3.4in"], "Global Offset Table Reserved Entries"),
        subsection("PLT Layout"),
        table(["Entry", "Effect"], plt_rows, ["1.35in", "4.15in"], "Procedure Linkage Table Layout"),
    ]
    return "\n".join(part for part in parts if part)


def render_tls(abi: dict[str, Any]) -> str:
    tls = abi.get("tls", {})
    if not tls:
        return ""
    entry_rows = [
        [
            tex_code(item.get("offset", "")),
            tex_code(item.get("field", "")),
            tex_code(item.get("type", "")),
            tex_escape(readable(item.get("meaning", ""))),
        ]
        for item in tls.get("tlsdesc_entry", [])
    ]
    parts = [
        section("Thread-Local Storage"),
        tex_escape(readable(tls.get("summary", ""))),
        subsection("TLS Base Model"),
        table(
            ["Rule", "Value"],
            mapping_rows(
                tls.get("rules", {}),
                {
                    "tls_base_register",
                    "program_internal_model",
                    "dynamic_tls_model",
                    "local_exec_relocations",
                    "dynamic_tls_relocations",
                },
            ),
            ["2.0in", "3.5in"],
            "TLS Base Model",
        ),
        subsection("Model Selection"),
        bullet_list(tls.get("model_selection", [])),
        subsection("TLSDESC Entry"),
        table(["Offset", "Field", "Type", "Meaning"], entry_rows, ["0.8in", "1.7in", "0.65in", "2.35in"], "TLSDESC Entry Layout"),
        subsection("TLSDESC Call ABI"),
        table(["Rule", "Value"], mapping_rows(tls.get("tlsdesc_call", {})), ["1.2in", "4.3in"], "TLSDESC Resolver Call ABI"),
        subsection("TLSDESC Relocation and Relaxation"),
        bullet_list(tls.get("relaxation", [])),
    ]
    return "\n".join(part for part in parts if part)


def render_code_models(abi: dict[str, Any]) -> str:
    code_models = abi.get("code_models", {})
    if not code_models:
        return ""
    rows = []
    detail_blocks = []
    for item in code_models.get("models", []):
        rows.append(
            [
                tex_code(item.get("name", "")),
                tex_table_value(item.get("placement", "")),
                tex_table_value(item.get("direct_range", "")),
                tex_table_value(item.get("rule", "")),
            ]
        )
        details = {
            "code references": item.get("code_references", ""),
            "data references": item.get("data_references", ""),
            "GOT/PLT": item.get("got_plt", ""),
            "default relocations": item.get("default_relocations", []),
            "relaxation": item.get("relaxation", ""),
        }
        detail_blocks.extend(
            [
                subsection(f"{item.get('name', 'model')} Model Details"),
                table(["Aspect", "Rule"], mapping_rows(details, {"default relocations"}), ["1.45in", "4.05in"], f"{item.get('name', 'model')} Code Model Details"),
            ]
        )
    parts = [
        section("Code Models"),
        tex_escape(readable(code_models.get("summary", ""))),
        table(["Model", "Placement", "Direct Range", "Rule"], rows, ["0.7in", "1.25in", "1.3in", "2.25in"], "Bedrock Code Models"),
        *detail_blocks,
    ]
    return "\n".join(part for part in parts if part)


def render_assembler_contract(abi: dict[str, Any]) -> str:
    contract = abi.get("assembler_contract", {})
    if not contract:
        return ""
    return "\n".join(
        [
            section("Assembler Contract"),
            field("Default ABI", contract.get("default_abi", "")),
            subsection("Strict Mode"),
            bullet_list(contract.get("strict_mode", [])),
            subsection("Relaxation"),
            bullet_list(contract.get("relaxation", [])),
        ]
    )


def render_freestanding_c_template(freestanding: dict[str, Any]) -> str:
    rules = freestanding.get("rules", {})
    helpers = freestanding.get("runtime_helpers", {})
    i128_helpers = helpers.get("integer_128", {})
    call_reloc = rules.get("c_call_relocation_default", {})
    if not isinstance(call_reloc, dict):
        call_reloc = {"direct": call_reloc, "external_plt": ""}
    return template(
        "c_abi_freestanding.tex",
        {
            "I128_RETURN": tex_code(helpers.get("int128_return_rule", "")),
            "I128_HELPER_MULTIPLY": tex_code(i128_helpers.get("multiply", "")),
            "I128_HELPER_SIGNED_DIVIDE": tex_code(i128_helpers.get("signed_divide", "")),
            "I128_HELPER_UNSIGNED_DIVIDE": tex_code(i128_helpers.get("unsigned_divide", "")),
            "I128_HELPER_SIGNED_REMAINDER": tex_code(i128_helpers.get("signed_remainder", "")),
            "I128_HELPER_UNSIGNED_REMAINDER": tex_code(i128_helpers.get("unsigned_remainder", "")),
            "I128_HELPER_SHIFT_LEFT": tex_code(i128_helpers.get("shift_left", "")),
            "I128_HELPER_ARITH_SHIFT_RIGHT": tex_code(i128_helpers.get("arithmetic_shift_right", "")),
            "I128_HELPER_LOGICAL_SHIFT_RIGHT": tex_code(i128_helpers.get("logical_shift_right", "")),
            "DIRECT_CALL_RELOCATION": tex_code(call_reloc.get("direct", "")),
        },
    )


def render_freestanding_c(abi: dict[str, Any]) -> str:
    freestanding = abi.get("freestanding_c", {})
    if not freestanding:
        return ""
    return "\n".join(
        [
            section("Freestanding C Binding"),
            render_freestanding_c_template(freestanding),
        ]
    )


def render_memory_model_template(model: dict[str, Any]) -> str:
    atomics = model.get("c_atomics", {})
    order = atomics.get("memory_order_mapping", {})
    return template(
        "c_abi_memory_model.tex",
        {
            "LOCK_FREE_WIDTHS": tex_escape(", ".join(str(item) for item in atomics.get("lock_free_widths_bytes", []))),
            "ORDER_RELAXED": tex_code(order.get("relaxed", "")),
            "ORDER_CONSUME": tex_code(order.get("consume", "")),
            "ORDER_ACQUIRE": tex_code(order.get("acquire", "")),
            "ORDER_RELEASE": tex_code(order.get("release", "")),
            "ORDER_ACQ_REL": tex_code(order.get("acq_rel", "")),
            "ORDER_SEQ_CST": tex_code(order.get("seq_cst", "")),
            "FETCH_ADD": tex_escape(atomics.get("fetch_add_lowering", "")),
            "FETCH_SUB": tex_escape(atomics.get("fetch_sub_lowering", "")),
            "FETCH_AND": tex_escape(atomics.get("fetch_and_lowering", "")),
            "FETCH_OR": tex_escape(atomics.get("fetch_or_lowering", "")),
            "FETCH_XOR": tex_escape(atomics.get("fetch_xor_lowering", "")),
            "CMPXCHG": tex_escape(atomics.get("compare_exchange_lowering", "")),
        },
    )


def render_memory_model(abi: dict[str, Any]) -> str:
    model = abi.get("memory_model", {})
    if not model:
        return ""
    parts = [section("C Memory Model"), render_memory_model_template(model)]
    return "\n".join(part for part in parts if part)


def render_example_case(case: dict[str, Any]) -> str:
    parts = [
        r"\Needspace{1.45in}",
        rf"\noindent\textbf{{{tex_escape(case.get('title', 'Example'))}}}\par",
        code_block(case.get("source", "")),
        bullet_list(case.get("result", [])),
    ]
    return "\n".join(part for part in parts if part)


def render_return_examples(abi: dict[str, Any]) -> str:
    examples = abi.get("examples", {})
    if not examples:
        return ""
    c_examples = examples.get("c_return_values", {})
    parts = [section("Return Value Examples")]
    if c_examples:
        parts.append(subsection("C Binding Examples"))
        parts.append(tex_escape(readable(c_examples.get("introduction", ""))))
        parts.extend(render_example_case(case) for case in c_examples.get("cases", []))
    return "\n".join(part for part in parts if part)


def render_system_interface(abi: dict[str, Any]) -> str:
    system = abi.get("system_interface", {})
    if not system:
        return ""
    syscall = system.get("syscall", {})
    return "\n".join(
        [
            section("System Interface Boundary"),
            tex_escape(readable(system.get("summary", ""))),
            subsection("SYSCALL Boundary"),
            field("Instruction", syscall.get("instruction", "")),
            tex_escape(readable(syscall.get("note", ""))),
        ]
    )


def render(abi: dict[str, Any]) -> str:
    document = abi.get("document", {})
    arch = document.get("architecture", "Bedrock")
    parts = [
        template(
            "abi_document_preamble.tex",
            {
                "ABI_TITLE": tex_escape(document.get("title", "Bedrock ELF ABI")),
                "ARCH_NAME": tex_escape(arch),
            },
        ),
        template(
            "abi_title_page.tex",
            {
                "ARCH_NAME_UPPER": tex_escape(str(arch).upper()),
                "ABI_TITLE": tex_escape(document.get("title", "Bedrock ELF ABI")),
                "ABI_SUBTITLE": tex_escape(document.get("subtitle", "ELF Application Binary Interface")),
                "ABI_VERSION": tex_escape(document.get("version", "0.1")),
            },
        ),
        render_scope(abi),
        render_terminology(abi),
        render_object_format(abi),
        render_register_banking(abi),
        render_program_loading(abi),
        render_data_model(abi),
        render_register_convention(abi),
        render_calling_convention(abi),
        render_sections_symbols(abi),
        render_relocations(abi),
        render_dynamic_linking(abi),
        render_tls(abi),
        render_code_models(abi),
        render_assembler_contract(abi),
        render_freestanding_c(abi),
        render_memory_model(abi),
        render_return_examples(abi),
        render_system_interface(abi),
        r"\end{document}",
    ]
    return "\n\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("abi_spec", nargs="?", default="isa/abi/elf.yaml")
    parser.add_argument("-o", "--output", default="build/latex/elf_abi/elf_abi.tex")
    args = parser.parse_args()

    abi_path = Path(args.abi_spec)
    abi = load_yaml(abi_path)
    AbiSchema().validate(abi_path, abi)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(render(abi), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
