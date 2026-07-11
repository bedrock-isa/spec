#!/usr/bin/env python3
"""Generate draft ISA reference documents from rewrite YAML sources."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to generate ISA documents") from exc

TOOL_DIR = Path(__file__).resolve().parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from validate_alloc import (  # noqa: E402
    compact_bits,
    entry_claims,
    namespace_patterns,
    validate_file,
)
from alloc_notes import allocation_form_text, allocation_note_text  # noqa: E402
from validate_isa import allocation_mnemonic  # noqa: E402
from latex_builder.common import (  # noqa: E402
    LatexDocumentEnd,
    LatexDocumentPreamble,
    LatexHiddenTopSection,
    LatexTitlePage,
    LatexTopSection,
    latex_longtable,
    latex_tabular,
    render_latex_template,
    tex_code,
    tex_escape as latex_escape,
)


ROOT = Path(__file__).resolve().parents[2]
DEF_ROOT = ROOT / "isa" / "defs"
ALLOC_ROOT = ROOT / "isa" / "alloc"
DEFAULT_OUTPUT = ROOT / "build" / "isa_reference.md"
OLD_LATEX_REFERENCE = ROOT / "old" / "build" / "latex" / "isa_reference" / "isa_reference.tex"
LEGACY_REFERENCE_SECTION_ALLOWLIST = {
    "Memory Address Translation",
}
LEGACY_REFERENCE_REJECT_PATTERNS = [
    r"\bD[nN](?:\b|\()",
    r"\bA[nN]\(",
    r"\bD[0-7]\b",
    r"\bA[0-7]\b",
    r"\bDBANK\b",
    r"\bSELDB\b",
    r"\bGETDB\b",
    r"Data Register Bank",
    r"Address Register",
]
INSTRUCTION_SET_SECTION_ORDER = [
    "base",
    "virtualization_acceleration",
    "fpu",
    "fpu_transcendental",
]
INSTRUCTION_SET_SECTION_TITLES = {
    "base": "General Instructions Summary",
    "virtualization_acceleration": "Virtualization Acceleration Instructions Summary",
    "fpu": "Floating-Point Instructions Summary",
    "fpu_transcendental": "Floating-Point Transcendental Instructions Summary",
}


@dataclass(frozen=True)
class InstructionDef:
    path: Path
    instruction_set: str
    mnemonic: str
    data: dict[str, Any]

    @property
    def doc(self) -> dict[str, Any]:
        value = self.data.get("doc")
        return value if isinstance(value, dict) else {}

    @property
    def behavior(self) -> dict[str, Any]:
        value = self.data.get("behavior")
        return value if isinstance(value, dict) else {}

    @property
    def attributes(self) -> dict[str, Any]:
        value = self.data.get("attributes")
        return value if isinstance(value, dict) else {}

    @property
    def forms(self) -> dict[str, Any]:
        value = self.data.get("forms")
        return value if isinstance(value, dict) else {}


@dataclass(frozen=True)
class AllocationEntry:
    path: Path
    cls: str
    payload_bits: int
    entry_id: str
    bits: str
    text: str
    assigned: int
    skipped: int
    fields: dict[str, Any]
    constraints: list[dict[str, Any]]

    @property
    def mnemonic(self) -> str | None:
        return allocation_mnemonic(allocation_form_text(self.text))


@dataclass(frozen=True)
class AllocationClass:
    path: Path
    cls: str
    payload_bits: int
    summary: dict[str, int]
    skipped_by_reason: Counter[str]
    overlaps: list[str]
    entries: list[AllocationEntry]


@dataclass(frozen=True)
class IsaModel:
    defs_root: Path
    alloc_root: Path
    metadata: dict[str, Any]
    instructions: list[InstructionDef]
    allocation_classes: list[AllocationClass]
    allocated_by_mnemonic: dict[str, list[AllocationEntry]]


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def compact_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(compact_text(item) for item in value)
    if isinstance(value, dict):
        value = yaml.safe_dump(value, sort_keys=False, allow_unicode=False).strip()
    return " ".join(str(value).split())


def compact_clause_text(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(compact_text(item).rstrip(".") for item in value if compact_text(item)) + "."
    return compact_text(value)


def display_text(value: Any) -> str:
    """Render schema values as reference prose instead of raw YAML tokens."""
    if isinstance(value, bool):
        return "yes" if value else "no"
    text = compact_text(value)
    mapping = {
        "at_most_one_memory_operand": "at most one memory operand",
        "false for every context": "not repeatable unless explicitly marked",
        "repgf_candidate": "REPGF candidate",
        "repeat_observed_value": "repeat-observed value",
        "repeat_flags": "repeat flags",
        "policy_controlled": "policy-controlled",
        "policy controlled": "policy-controlled",
        "memory_memory": "memory-memory form",
        "src_current_memory_register_or_immediate_dst_user_memory": "source may be current-domain memory, register, or immediate; destination memory uses the user domain",
        "src_user_memory_dst_current_memory_or_register": "source memory uses the user domain; destination may be current-domain memory or register",
        "src_user_memory_dst_user_memory": "source and destination memory both use the user domain",
        "extra trailing payload bytes are padding payload": "extra trailing payload bytes are padding",
    }
    return mapping.get(text, text)


def privilege_text(value: Any, default: str = "unprivileged") -> str:
    """Render instruction privilege attributes in reader-facing form."""
    if isinstance(value, dict):
        base = compact_text(value.get("default", default)) or default
        qualifiers: list[str] = []
        if value.get("policy_controlled"):
            qualifiers.append("policy-controlled")
        for key, item in value.items():
            if key in {"default", "policy_controlled"}:
                continue
            item_text = display_text(item)
            if item_text:
                qualifiers.append(f"{display_text(key)}: {item_text}")
        if qualifiers:
            return f"{base}, " + ", ".join(qualifiers)
        return base
    return display_text(value) or default


def label_text(value: Any) -> str:
    text = display_text(value)
    return text.replace("_", " ")


def instruction_set_text(value: Any) -> str:
    names = {
        "base": "base",
        "virtualization_acceleration": "virtualization acceleration",
        "fpu": "floating-point",
        "fpu_transcendental": "floating-point transcendental",
    }
    text = compact_text(value)
    return names.get(text, label_text(text))


def bits_text(value: Any, width: int | None = None) -> str:
    if isinstance(value, int):
        if width is None:
            return str(value)
        return f"{value:0{width}b}"
    return str(value)


def manifest_instruction_paths(defs_root: Path) -> list[tuple[str, Path]]:
    manifest = load_yaml(defs_root / "manifest.yaml")
    if not isinstance(manifest, dict):
        raise ValueError(f"{defs_root / 'manifest.yaml'}: expected mapping")

    paths: list[tuple[str, Path]] = []
    for spec in manifest.get("instruction_sets", []):
        name = str(spec["name"])
        include = defs_root / spec["include"]
        data = load_yaml(include)
        if not isinstance(data, dict):
            raise ValueError(f"{include}: expected mapping")
        for item in data.get("include", []) or []:
            path = include.parent / item
            if not path.exists():
                raise FileNotFoundError(path)
            paths.append((name, path))
    return paths


def load_instructions(defs_root: Path) -> list[InstructionDef]:
    instructions: list[InstructionDef] = []
    for instruction_set, path in manifest_instruction_paths(defs_root):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue
        mnemonic = data.get("mnemonic")
        if not mnemonic:
            continue
        instructions.append(InstructionDef(path, instruction_set, str(mnemonic), data))
    return sorted(instructions, key=lambda item: (item.mnemonic.lower(), str(item.path)))


def load_allocation_class(path: Path) -> AllocationClass:
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    cls, summary, skipped, overlaps = validate_file(path)
    payload_bits = int(data["payload_bits"])
    namespaces = namespace_patterns(payload_bits, data)
    entries: list[AllocationEntry] = []
    for raw in data.get("entries", []) or []:
        if not isinstance(raw, dict):
            continue
        claims, entry_skipped = entry_claims(path, payload_bits, namespaces, raw)
        entries.append(
            AllocationEntry(
                path=path,
                cls=cls,
                payload_bits=payload_bits,
                entry_id=str(raw["id"]),
                bits=compact_bits(str(raw["bits"])),
                text=str(raw.get("text", "")),
                assigned=len(claims),
                skipped=sum(entry_skipped.values()),
                fields=raw.get("fields") or {},
                constraints=raw.get("constraints") or [],
            )
        )
    return AllocationClass(
        path=path,
        cls=cls,
        payload_bits=payload_bits,
        summary=summary,
        skipped_by_reason=skipped,
        overlaps=overlaps,
        entries=entries,
    )


def load_allocations(alloc_root: Path) -> list[AllocationClass]:
    order = {"extrashort": 0, "short": 1, "medium": 2, "long": 3, "extralong": 4}
    classes = [load_allocation_class(path) for path in sorted(alloc_root.glob("*.yaml"))]
    return sorted(classes, key=lambda item: (order.get(item.cls, 99), item.cls))


def load_metadata(defs_root: Path) -> dict[str, Any]:
    names = [
        "registers",
        "segments",
        "conditions",
        "ea",
        "operands",
        "semantics",
        "terminology",
        "manifest",
    ]
    out: dict[str, Any] = {}
    for name in names:
        path = defs_root / f"{name}.yaml"
        if path.exists():
            out[name] = load_yaml(path)
    return out


def load_model(defs_root: Path, alloc_root: Path) -> IsaModel:
    instructions = load_instructions(defs_root)
    allocation_classes = load_allocations(alloc_root)
    allocated_by_mnemonic: dict[str, list[AllocationEntry]] = defaultdict(list)
    for cls in allocation_classes:
        for entry in cls.entries:
            mnemonic = entry.mnemonic
            if mnemonic:
                allocated_by_mnemonic[mnemonic].append(entry)
    return IsaModel(
        defs_root=defs_root,
        alloc_root=alloc_root,
        metadata=load_metadata(defs_root),
        instructions=instructions,
        allocation_classes=allocation_classes,
        allocated_by_mnemonic=dict(sorted(allocated_by_mnemonic.items())),
    )


def latex_existing_section(title: str) -> str:
    """Return a rendered section from the previous manual when it is still reusable."""
    if not OLD_LATEX_REFERENCE.exists():
        return ""
    text = OLD_LATEX_REFERENCE.read_text(encoding="utf-8")
    marker = rf"\section{{{title}}}"
    start = text.find(marker)
    if start < 0:
        return ""
    end = text.find(r"\section{", start + len(marker))
    if end < 0:
        end = text.find(r"\end{document}", start)
    if end < 0:
        end = len(text)
    section = text[start:end].strip()
    section = re.sub(
        r"(\\manual(?:table|figure)caption\{)(?:Table|Figure) \d+-\d+\.\s+",
        r"\1",
        section,
    )
    return (r"\clearpage" + "\n" + section).rstrip()


def latex_legacy_reference_section(title: str) -> str:
    """Import only stable legacy prose/diagrams that are not sourced from rewrite YAML."""
    if title not in LEGACY_REFERENCE_SECTION_ALLOWLIST:
        return ""
    section = latex_existing_section(title)
    if not section:
        return ""
    for pattern in LEGACY_REFERENCE_REJECT_PATTERNS:
        if re.search(pattern, section):
            return ""
    return section


def md_escape(value: Any) -> str:
    return compact_text(value).replace("|", r"\|")


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_No entries._\n"
    out = [
        "| " + " | ".join(md_escape(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(out) + "\n"


def code_block(text: str, lang: str = "text") -> str:
    body = text.rstrip()
    return f"```{lang}\n{body}\n```\n" if body else ""


def md_paragraphs(title: str, paragraphs: list[str], *, level: int = 2) -> str:
    heading_marks = "#" * level
    body = "\n\n".join(paragraph.strip() for paragraph in paragraphs if paragraph.strip())
    return f"{heading_marks} {title}\n\n{body}\n" if body else f"{heading_marks} {title}\n"


def md_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) + "\n"


def latex_subsection(title: str) -> str:
    return rf"\subsection{{{latex_escape(title)}}}"


def latex_paragraphs(paragraphs: list[str]) -> str:
    return "\n\n".join(latex_escape(paragraph.strip()) for paragraph in paragraphs if paragraph.strip())


def latex_itemize(items: list[str]) -> str:
    if not items:
        return ""
    lines = [r"\begin{itemize}"]
    lines.extend(rf"\item {latex_escape(item)}" for item in items)
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def latex_description(rows: list[tuple[str, str]]) -> str:
    if not rows:
        return ""
    lines = [
        r"\begin{description}[style=nextline,leftmargin=1.42in,labelwidth=1.32in,itemsep=3pt,topsep=3pt]"
    ]
    for term, body in rows:
        lines.append(rf"\item[{latex_escape(term)}] {latex_escape(body)}")
    lines.append(r"\end{description}")
    return "\n".join(lines)


def operand_text(operand: Any) -> str:
    if not isinstance(operand, dict):
        return compact_text(operand)
    name = operand.get("name")
    typ = operand.get("type")
    if name and typ:
        return f"{name}:{typ}"
    if typ:
        return str(typ)
    return compact_text(operand)


def operand_list_text(value: Any) -> str:
    if value == []:
        return "-"
    if isinstance(value, list):
        return ", ".join(operand_text(item) for item in value) or "-"
    return compact_text(value) or "-"


def form_attribute_text(key: str, value: Any) -> str:
    if key == "compact":
        return "compact form" if value else "extended form only"
    if key == "flags":
        return "FLAGS " + display_text(value) if not isinstance(value, dict) else flag_summary(value)
    if key == "profile":
        return f"profile: {display_text(value)}"
    if key == "constraint":
        return f"constraint: {display_text(value)}"
    if key == "result":
        return f"result: {display_text(value)}"
    return f"{label_text(key)}: {display_text(value)}"


def form_size_text(value: Any) -> str:
    text = compact_text(value)
    if not text or text == "-":
        return "-"
    mapping = {
        "BWLQ": "B/W/L/Q",
        "BWL": "B/W/L",
        "BW": "B/W",
        "WLQ": "W/L/Q",
        "WL": "W/L",
        "LQ": "L/Q",
        "S_D": "S/D",
        "implicit_Q": "Q",
        "fixed: Q": "Q",
    }
    return mapping.get(text, text)


def form_rows(instruction: InstructionDef) -> list[list[str]]:
    forms = instruction.forms
    rows: list[list[str]] = []

    def add_form(kind: str, form: dict[str, Any]) -> None:
        operands = form.get("operands", forms.get("operands", []))
        attrs = []
        for key in ("profile", "constraint", "result", "flags", "compact"):
            if key in form:
                attrs.append(form_attribute_text(key, form[key]))
        rows.append(
            [
                kind,
                operand_list_text(operands),
                form_size_text(form.get("size", forms.get("size", "-"))),
                "; ".join(attrs) or "-",
            ]
        )

    for key, label in (("compact_forms", "compact"), ("extended_forms", "extended")):
        for form in forms.get(key, []) or []:
            if isinstance(form, dict):
                add_form(label, form)

    operands = forms.get("operands")
    if operands is not None:
        if isinstance(operands, list) and operands and all(isinstance(item, list) for item in operands):
            for item in operands:
                rows.append(["form", operand_list_text(item), form_size_text(forms.get("size", "-")), "-"])
        else:
            rows.append(["form", operand_list_text(operands), form_size_text(forms.get("size", "-")), "-"])

    return rows


def iter_instruction_forms(instruction: InstructionDef) -> list[tuple[str, dict[str, Any]]]:
    forms = instruction.forms
    out: list[tuple[str, dict[str, Any]]] = []
    for key, label in (("compact_forms", "compact"), ("extended_forms", "extended")):
        for form in forms.get(key, []) or []:
            if isinstance(form, dict):
                out.append((label, form))
    operands = forms.get("operands")
    if operands is not None:
        if isinstance(operands, list) and operands and all(isinstance(item, list) for item in operands):
            for item in operands:
                out.append(("form", {"operands": item, "size": forms.get("size", "-")}))
        else:
            out.append(("form", {"operands": operands, "size": forms.get("size", "-")}))
    return out


def instruction_form_count(instruction: InstructionDef, model: IsaModel) -> int:
    allocated_forms = {
        allocation_form_text(entry.text)
        for entry in model.allocated_by_mnemonic.get(instruction.mnemonic, [])
        if allocation_form_text(entry.text)
    }
    return max(len(allocated_forms), len(iter_instruction_forms(instruction)))


def instruction_family(instruction: InstructionDef) -> str:
    return label_text(instruction.doc.get("instruction_family", "-")) or "-"


def instruction_class(instruction: InstructionDef) -> str:
    return label_text(instruction.doc.get("instruction_class", "-")) or "-"


def allocation_status(instruction: InstructionDef, model: IsaModel) -> str:
    entries = model.allocated_by_mnemonic.get(instruction.mnemonic, [])
    if not entries:
        return "-"
    return ", ".join(sorted({entry.cls for entry in entries}))


def instruction_set_groups(instructions: list[InstructionDef]) -> list[tuple[str, list[InstructionDef]]]:
    by_set: dict[str, list[InstructionDef]] = defaultdict(list)
    for inst in instructions:
        by_set[inst.instruction_set].append(inst)

    ordered_sets = [name for name in INSTRUCTION_SET_SECTION_ORDER if name in by_set]
    ordered_sets.extend(sorted(name for name in by_set if name not in set(ordered_sets)))
    return [
        (INSTRUCTION_SET_SECTION_TITLES.get(name, f"{name.replace('_', ' ').title()} Instructions Summary"), by_set[name])
        for name in ordered_sets
    ]


def instruction_by_mnemonic(model: IsaModel, mnemonic: str) -> InstructionDef | None:
    target = mnemonic.upper()
    for inst in model.instructions:
        if inst.mnemonic.upper() == target:
            return inst
    return None


def instruction_brief_rows(model: IsaModel, mnemonics: list[str]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for mnemonic in mnemonics:
        inst = instruction_by_mnemonic(model, mnemonic)
        if inst is None:
            continue
        rows.append([inst.mnemonic, inst.doc.get("summary", inst.doc.get("title", inst.mnemonic))])
    return rows


def operand_schema(model: IsaModel) -> dict[str, Any]:
    data = model.metadata.get("operands") or {}
    schema = data.get("operand_schema")
    return schema if isinstance(schema, dict) else {}


def size_code_rows(model: IsaModel) -> list[list[Any]]:
    schema = operand_schema(model)
    size_codes = schema.get("size_codes") or {}
    order = ["B", "W", "L", "Q", "S", "D"]
    rows: list[list[Any]] = []
    for code in order:
        body = size_codes.get(code)
        if not isinstance(body, dict):
            continue
        byte_count = int(body.get("bytes", 0) or 0)
        rows.append([code, body.get("suffix", f".{code}"), byte_count * 8, byte_count, body.get("label", "")])
    return rows


def memory_order_rows(model: IsaModel) -> list[list[Any]]:
    schema = operand_schema(model)
    memory_order = ((schema.get("named_values") or {}).get("memory_order") or {})
    rows: list[list[Any]] = []
    for item in memory_order.get("values", []) or []:
        if isinstance(item, dict):
            rows.append([item.get("name", ""), item.get("value", ""), item.get("description", "")])
    for item in memory_order.get("reserved_values", []) or []:
        if isinstance(item, dict):
            rows.append([item.get("name", ""), item.get("value", ""), item.get("description", "")])
    return rows


def terminology_groups(model: IsaModel) -> list[dict[str, Any]]:
    data = model.metadata.get("terminology") or {}
    return [group for group in data.get("groups", []) or [] if isinstance(group, dict)]


def flatten_rule_rows(value: Any, path_key: str = "") -> list[list[str]]:
    rows: list[list[str]] = []
    if isinstance(value, dict):
        for key, body in value.items():
            name = f"{path_key}.{key}" if path_key else str(key)
            rows.extend(flatten_rule_rows(body, name))
    elif isinstance(value, list):
        rows.append([path_key, ", ".join(compact_text(item) for item in value)])
    else:
        rows.append([path_key, compact_text(value)])
    return rows


def compatibility_rows(model: IsaModel) -> list[list[str]]:
    data = ((model.metadata.get("semantics") or {}).get("compatibility_rules") or {})
    label_map = {
        "reserved_bits.architected_register_bits.read": "Reserved architectural bits, read",
        "reserved_bits.architected_register_bits.write": "Reserved architectural bits, write",
        "reserved_bits.control_register_bits.read": "Reserved control bits, read",
        "reserved_bits.control_register_bits.write": "Reserved control bits, write",
        "reserved_bits.control_register_bits.write_exception": "Reserved control bits, write fault",
        "reserved_bits.selector_values.exception": "Reserved selector values",
        "reserved_bits.page_table_bits.consumed_exception": "Consumed reserved PTE bits",
        "reserved_bits.interrupt_vector_table_bits.write": "Reserved IVT bits, write",
        "reserved_bits.supervisor_frame_bits.write": "Reserved supervisor-frame bits",
        "reserved_bits.software_defined_bits.hardware_use": "Software-defined bits, hardware",
        "reserved_bits.software_defined_bits.software_use": "Software-defined bits, software",
        "instruction_encoding_faults.reserved_opcode.exception": "Reserved opcode",
        "instruction_encoding_faults.reserved_extension_opcode.exception": "Reserved extension opcode",
        "instruction_encoding_faults.reserved_effective_address_form.exception": "Reserved EA form",
        "instruction_encoding_faults.unsupported_optional_instruction_group.exception": "Unavailable optional group",
        "instruction_encoding_faults.extension_unavailable_exception.defined": "Extension-unavailable fault",
        "canonical_encodings.assembler_default": "Assembler default",
        "canonical_encodings.disassembler_default": "Disassembler default",
        "canonical_encodings.noncanonical_default.exception": "Noncanonical default",
        "canonical_encodings.explicit_alias_or_priority.allowed": "Explicit alias or priority",
        "cpuid.unknown_class.result": "CPUID unknown class",
        "cpuid.unknown_leaf.result": "CPUID unknown leaf",
        "cpuid.unknown_index.result": "CPUID unknown index",
        "cpuid.reserved_result_bits.value": "CPUID reserved result bits",
    }
    rows = []
    for key, value in flatten_rule_rows(data):
        rows.append([label_map.get(key, key.replace("_", " ").replace(".", ", ")), policy_value_text(value)])
    return rows


def compatibility_rules(model: IsaModel) -> dict[str, Any]:
    data = ((model.metadata.get("semantics") or {}).get("compatibility_rules") or {})
    return data if isinstance(data, dict) else {}


def policy_value_text(value: Any) -> str:
    mapping = {
        "zero": "zero",
        "must_be_zero": "must be zero",
        "ignored": "ignored",
        "ignore": "ignore",
        "allowed": "allowed",
        "none": "none",
        "no_architectural_effect": "no architectural effect",
        "canonical": "canonical",
        "unprivileged": "unprivileged",
        "True": "yes",
        "False": "no",
    }
    if isinstance(value, bool):
        return "yes" if value else "no"
    return mapping.get(str(value), compact_text(value))


def compat_get(data: dict[str, Any], *keys: str, default: Any = "-") -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def size_decoding_rows() -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["0xxxxxxx", "-", 1],
        ["10xxxxxx", "xxxxxxxx", 2],
    ]
    for length in range(16):
        rows.append([f"11{length:04b}oo", "bbbbxxxx", 3 + length])
    return rows


def opcode_length_rows() -> list[list[Any]]:
    return [
        ["0xxxxx", "medium", 3, "any extended instruction length"],
        ["10xxxx", "medium", 3, "any extended instruction length"],
        ["110xxx", "medium", 3, "any extended instruction length"],
        ["1110xx", "medium", 3, "any extended instruction length"],
        ["11110x", "long", 4, "instruction length must be at least 4 bytes"],
        ["111110", "long", 4, "instruction length must be at least 4 bytes"],
        ["111111", "extralong", 5, "instruction length must be at least 5 bytes"],
    ]


def instruction_family_rows(instructions: list[InstructionDef]) -> list[list[Any]]:
    counts: Counter[tuple[str, str]] = Counter()
    for inst in instructions:
        counts[(instruction_class(inst), instruction_family(inst))] += 1
    return [[cls, family, count] for (cls, family), count in sorted(counts.items())]


def encoding_class_rows(model: IsaModel) -> list[list[Any]]:
    selectors = {
        "extrashort": "byte0[7]=0; payload is byte0[6:0]",
        "short": "byte0[7:6]=10; payload is byte0[5:0] followed by byte1[7:0]",
        "medium": "byte0[7:6]=11 and opcode selector is 0xxxxx, 10xxxx, 110xxx, or 1110xx",
        "long": "byte0[7:6]=11 and opcode selector is 11110x or 111110",
        "extralong": "byte0[7:6]=11 and opcode selector is 111111",
    }
    return [
        [
            cls.cls,
            cls.payload_bits,
            selectors.get(cls.cls, "-"),
        ]
        for cls in model.allocation_classes
    ]


def render_markdown(model: IsaModel, only_allocated: bool = False) -> str:
    instructions = [
        item
        for item in model.instructions
        if not only_allocated or item.mnemonic in model.allocated_by_mnemonic
    ]
    parts = [
        "# ISA Reference\n",
        render_architecture_overview_md(model, instructions),
        render_terminology_md(model),
        render_compatibility_md(model),
        render_data_formats_md(model),
        render_instruction_word_formats_md(model),
        render_registers_md(model),
        render_segments_md(model),
        render_conditions_md(model),
        render_condition_computation_md(model),
        render_ea_md(model),
        render_execution_model_md(model),
        render_streaming_model_md(model),
        render_memory_translation_md(model),
        render_memory_model_md(model),
        render_instruction_set_overview_md(model, instructions),
        render_instruction_summary_md(model, instructions),
        render_instruction_reference_md(model, instructions),
    ]
    return "\n".join(part.rstrip() for part in parts if part).rstrip() + "\n"


def render_source_summary(model: IsaModel, instructions: list[InstructionDef]) -> str:
    allocated = set(model.allocated_by_mnemonic)
    defined = {item.mnemonic for item in model.instructions}
    rows = [
        ["Definition root", str(model.defs_root)],
        ["Allocation root", str(model.alloc_root)],
        ["Instruction definitions", len(instructions)],
        ["Allocated mnemonics", len(allocated)],
        ["Allocated without definition", len(allocated - defined)],
        ["Definitions without allocation", len(defined - allocated)],
    ]
    return "## Source Summary\n\n" + md_table(["Item", "Value"], rows)


def render_architecture_overview_md(model: IsaModel, instructions: list[InstructionDef]) -> str:
    body = md_paragraphs(
        "Overview",
        [
            "Bedrock defines a bounded, byte-addressed CISC instruction set with explicit instruction lengths, compact hot-path register forms, and selected register-memory and memory-memory forms.",
            "Bedrock uses a unified 16-entry Rn integer register file. SP and PC are special architectural registers outside the Rn namespace, with SP-relative addressing tied to SS and PC-relative addressing tied to CS.",
            "The reference is organized around programmer-visible state, operand formation, execution semantics, and instruction behavior. Byte-level instruction framing is specified separately in the Instruction Header Formats chapter.",
        ],
    )
    body += "\n### Architectural Profile\n\n"
    body += md_bullets(
        [
            "The PC names a byte in the instruction stream; sequential execution advances it by the decoded instruction length.",
            "Instruction length is explicit and bounded; the base profile defines lengths from 1 to 18 bytes.",
            "Four integer operation sizes: B, W, L, and Q.",
            "The effective-address model covers register, memory, immediate, absolute, segment-qualified, indexed, and auto-update operands.",
            "Segment pre-translation precedes optional page-table translation.",
            "User and supervisor modes share the instruction set, with privileged instructions and checked user-access moves defining supervisor-only behavior.",
            "REP, REPcc, and REPG expose scalar repeated execution while leaving internal streaming width implementation-defined.",
        ]
    )
    return body


def render_terminology_md(model: IsaModel) -> str:
    parts = ["## Terminology\n"]
    for group in terminology_groups(model):
        rows = []
        for term in group.get("terms", []) or []:
            if isinstance(term, dict):
                rows.append([term.get("term", ""), term.get("definition", "")])
        if rows:
            parts.append(f"### {group.get('name', 'Terms')}\n")
            parts.append(md_table(["Term", "Definition"], rows))
    return "\n".join(parts)


def render_compatibility_md(model: IsaModel) -> str:
    paragraphs = [
        "Reserved and unallocated encodings are held for future architectural definition. Software must not depend on their value, decode result, or behavior.",
        "This manual treats reserved and unallocated encodings as one architectural category. Future architecture revisions may assign narrower meanings, but existing software must assume no operation is available there.",
        "Noncanonical encodings are invalid unless an instruction description explicitly defines an alias or priority rule. Assemblers should emit canonical encodings and disassemblers should prefer canonical spellings.",
    ]
    rows = compatibility_rows(model)
    return md_paragraphs("Reserved and Compatibility Rules", paragraphs) + "\n" + md_table(["Rule", "Value"], rows)


def render_data_formats_md(model: IsaModel) -> str:
    body = md_paragraphs(
        "Data Formats",
        [
            "Integer operands use size suffixes to select the low-order subfield of an Rn register and the number of bytes transferred by memory operands.",
            "An Rn destination write smaller than Q replaces only the selected low-order subfield and preserves bits above the operation size. Q-sized Rn writes replace all 64 bits. Memory destination writes transfer only the selected number of bytes.",
            "Instruction-specific full-register writes, zero-extension, sign-extension, or other upper-bit rules override the default subfield write rule.",
            "Integer data, immediates, displacements, and absolute address payloads are little-endian. Instruction headers are byte-coded in instruction-stream order rather than decoded as little-endian integers.",
        ],
    )
    body += "\n" + md_table(["Code", "Suffix", "Bits", "Bytes", "Name"], size_code_rows(model))
    schema = operand_schema(model)
    immediate_rows = []
    for name, spec in sorted((schema.get("immediate_operands") or {}).items()):
        if not isinstance(spec, dict):
            continue
        rng = spec.get("range", "-")
        if isinstance(rng, list) and len(rng) == 2:
            rng = f"{rng[0]}..{rng[1]}"
        immediate_rows.append(
            [
                name,
                spec.get("width", ""),
                "signed" if spec.get("signed") else "unsigned",
                rng,
                spec.get("operation_size_extension", ""),
                spec.get("applies_when", ""),
            ]
        )
    if immediate_rows:
        body += "\n### Immediate Operand Interpretation\n\n"
        body += md_table(["Operand", "Bits", "Value", "Range", "Extension", "Applies When"], immediate_rows)
    return body


def render_instruction_word_formats_md(model: IsaModel) -> str:
    rows = [
        ["byte 0 bit 7", "class", "0 selects a one-byte extrashort instruction with payload in byte0[6:0]."],
        ["byte 0 bits 7..6", "class", "10 selects a two-byte short instruction; 11 selects an extended instruction."],
        ["byte 0 bits 5..2", "L / payload", "For short, payload[13:10]. For extended, L encodes total instruction bytes as 3+L."],
        ["byte 0 bits 1..0", "opcode", "For short, payload[9:8]. For extended, opcode-stream bits[highest:highest-1]."],
        ["byte 1 bits 7..0", "opcode", "For short, payload[7:0]. For extended, the next eight opcode-stream bits."],
    ]
    body = md_paragraphs(
        "Instruction Header Formats",
        [
            "Instruction framing is byte-oriented. Byte 0 alone identifies extrashort and short instructions; extended instructions use byte 0 and byte 1 to determine both total instruction length and opcode class.",
            "Extended byte0[5:2] is L, and the total instruction length is 3+L bytes. The opcode stream begins at byte0[1:0], continues through byte1, and then consumes later bytes as required by the opcode class.",
            "An extended instruction is invalid if its encoded total length is shorter than the opcode class minimum: 3 bytes for medium, 4 bytes for long, and 5 bytes for extralong.",
        ],
    )
    body += "\n" + md_table(["Bits", "Field", "Meaning"], rows)
    body += "\n### Instruction Length Truth Table\n\n"
    body += md_table(["Byte 0 Pattern", "Byte 1 Pattern", "Instruction Bytes"], size_decoding_rows())
    body += "\n### Opcode Length Truth Table\n\n"
    body += md_table(["Opcode Selector", "Class", "Opcode Bytes", "Validity"], opcode_length_rows())
    body += "\n### Encoding Classes\n\n"
    body += md_table(["Class", "Payload Bits", "Selection"], encoding_class_rows(model))
    return body


def render_registers_md(model: IsaModel) -> str:
    data = model.metadata.get("registers") or {}
    rows = []
    for reg in data.get("general_registers", []) or []:
        rows.append([reg.get("name", ""), bits_text(reg.get("encoding", ""), 4), reg.get("width", "")])
    special_rows = []
    for reg in data.get("special_registers", []) or []:
        special_rows.append(
            [
                reg.get("name", ""),
                reg.get("width", ""),
                reg.get("fixed_segment", ""),
                bits_text(reg.get("ea_encoding", ""), 7),
            ]
        )
    body = md_paragraphs(
        "Register Model",
        [
            "The integer programming model exposes sixteen 64-bit Rn registers, R0 through R15. Bedrock uses one general-purpose register class for integer values, address values, counters, selectors, and temporary data.",
            "SP and PC are special architectural registers outside the four-bit Rn namespace. SP-relative memory forms use SS by default; PC-relative memory forms use CS by default.",
        ],
    )
    body += md_table(["Register", "Encoding", "Width"], rows)
    if special_rows:
        body += "\n" + md_table(["Special", "Width", "Fixed Segment", "EA Encoding"], special_rows)
    return body


def render_segments_md(model: IsaModel) -> str:
    data = model.metadata.get("segments") or {}
    rows = []
    for reg in data.get("segment_registers", []) or []:
        rows.append([reg.get("name", ""), reg.get("selector", ""), reg.get("width", "")])
    return "## Segment Registers\n\n" + md_table(["Register", "Selector", "Width"], rows)


def render_conditions_md(model: IsaModel) -> str:
    data = model.metadata.get("conditions") or {}
    rows = []
    for cond in data.get("conditions", []) or []:
        aliases = ", ".join(str(item) for item in cond.get("aliases", []) or [])
        rows.append([bits_text(cond.get("value", ""), 4), cond.get("name", ""), aliases or "-", cond.get("expression", "")])
    return "## Condition Codes\n\n" + md_table(["Bits", "Name", "Aliases", "Expression"], rows)


def render_condition_computation_md(model: IsaModel) -> str:
    body = md_paragraphs(
        "Condition Code Computation",
        [
            "Integer condition codes are held in FLAGS. Integer instructions leave FLAGS unchanged unless their instruction description explicitly defines a FLAGS write. Unmentioned FLAGS bits are preserved unless the instruction says otherwise.",
            "For an operand width of n bits, ordinary integer ALU results are evaluated modulo 2^n unless the instruction explicitly defines a wider intermediate.",
        ],
    )
    body += "\n" + md_table(
        ["Bit", "Name", "Meaning"],
        [
            ["Z", "zero", "Set when the result value is zero."],
            ["N", "negative", "Set from the most significant bit of the result at the operand size."],
            ["C", "carry/borrow", "Set on unsigned carry out for addition, or unsigned borrow for subtraction."],
            ["V", "overflow", "Set on signed overflow, or by instructions that explicitly report exceptional conditions through V."],
        ],
    )
    body += "\n" + md_table(
        ["Operation Class", "FLAGS Result"],
        [
            ["ADD, SUB, AND, OR, XOR", "Leave FLAGS unchanged."],
            ["ADC, SBB", "Read C as carry/borrow input and update Z, N, C, and V from the stored result."],
            ["CMP, TEST", "Update Z, N, C, and V from the temporary result and do not store that result."],
            ["CMPJcc, TESTJcc", "Compute temporary condition flags for the branch decision and leave architectural FLAGS unchanged."],
            ["INC, DEC", "Leave FLAGS unchanged."],
            ["INCF, DECF", "Update Z, N, C, and V from the stored increment/decrement result."],
            ["SETF, CLRF", "Set or clear selected FLAGS bits from the imm4 mask; unselected FLAGS bits are preserved."],
            ["NEG, ABS", "Leave FLAGS unchanged."],
            ["CLR", "Writes zero and leaves FLAGS unchanged."],
            ["Bounds checks", "Set V when the value is outside the selected interval; Z, N, and C are unchanged."],
        ],
    )
    body += "\n" + md_table(
        ["Operation", "Count Rule"],
        [
            ["SHL, SHR, SAR", "The count is not reduced modulo the operand width. Oversized counts have defined zero or sign-fill behavior."],
            ["ROL, ROR", "The effective count is count modulo the operand width. Effective count zero leaves the destination and FLAGS unchanged."],
        ],
    )
    body += "\n" + md_table(
        ["Operation", "FLAGS Result for Nonzero Effective Count"],
        [
            ["SHL", "Z and N come from the result. C is the last bit shifted out. V reports signed multiplication overflow."],
            ["SHR", "Z and N come from the result. C is the last bit shifted out. V is cleared."],
            ["SAR", "Z and N come from the result. C is the last bit shifted out, or the original sign bit for oversized counts. V is cleared."],
            ["ROL", "Z and N come from the result. C is the least significant result bit. V is cleared."],
            ["ROR", "Z and N come from the result. C is the most significant result bit. V is cleared."],
        ],
    )
    return body


def render_ea_md(model: IsaModel) -> str:
    data = model.metadata.get("ea") or {}
    rows = []
    for form in data.get("compact_ea", []) or []:
        memory = form.get("memory", "")
        rows.append([form.get("bits", ""), form.get("syntax", form.get("class", "")), form.get("class", ""), display_text(memory)])
    ext_rows = []
    for form in ((data.get("ext0") or {}).get("forms", []) or []):
        ext_rows.append([form.get("bits", ""), form.get("syntax", ""), form.get("base", ""), form.get("index", ""), form.get("segment", form.get("fixed_segment", ""))])
    body = md_paragraphs(
        "Effective Address Encoding",
        [
            "Most instructions that accept an effective-address operand share the seven-bit EA field. Compact EA encodings cover direct Rn operands, common Rn/SP/PC memory forms, absolute memory forms, immediates, and EXT0 escapes.",
            "EXT0 has no default segment. Segment-qualified forms carry an explicit segment field; SP-based and PC-based forms omit that field because SP and PC are tied to SS and CS respectively.",
            "Indexed scale is implicit in the consuming instruction. For ordinary memory operations, B/W/L/Q imply scales 1, 2, 4, and 8. LEA uses its suffix to select the scale.",
        ],
    )
    body += md_table(["Bits", "Syntax", "Class", "Memory"], rows)
    if ext_rows:
        body += "\n### EXT0\n\n" + md_table(["Bits", "Syntax", "Base", "Index", "Segment"], ext_rows)
    auto = data.get("auto_update_semantics") or {}
    if auto:
        body += "\n### Auto-Update Semantics\n\n"
        body += md_bullets([compact_text(item) for item in auto.get("evaluation_model", []) or []])
        examples = auto.get("same_register_examples") or []
        if examples:
            body += "\n" + md_table(
                ["Syntax", "Meaning"],
                [[item.get("syntax", ""), compact_clause_text(item.get("meaning", ""))] for item in examples if isinstance(item, dict)],
            )
    return body


def render_execution_model_md(model: IsaModel) -> str:
    rules = (model.metadata.get("semantics") or {}).get("encoding_rules") or {}
    body = md_paragraphs(
        "Instruction Execution Model",
        [
            "The instruction boundary is fixed by byte 0 for extrashort and short forms, and by the first two bytes for extended forms, before operand evaluation begins. An implementation may reject an instruction before any architectural state is changed if the encoded length cannot contain the selected form.",
            "Operands are decoded in instruction order. Source reads complete before the final destination write unless an atomic form says otherwise. Effective-address calculation may produce an address without reading memory.",
            "Auto-update EA forms update a temporary operand-evaluation image. The architectural register update becomes visible only when the instruction commits.",
        ],
    )
    rows = [
        ["Instruction boundary", "The instruction header length selects the full instruction record; later payloads never extend it implicitly."],
        ["Overlong encoding", display_text(((rules.get("instruction_length") or {}).get("overlong_encoding") or {}).get("payload", ""))],
        ["Undersized encoding", display_text(((rules.get("instruction_length") or {}).get("undersized_encoding") or {}).get("rule", ""))],
        ["Default memory operands", display_text((rules.get("memory_operands") or {}).get("default", ""))],
        ["Memory-memory exceptions", compact_text((rules.get("memory_operands") or {}).get("memory_memory_allowed_for", ""))],
        ["Repeat instructions", compact_text((rules.get("repeat_instructions") or {}).get("members", ""))],
    ]
    body += "\n" + md_table(["Rule", "Meaning"], rows)
    return body


def repeat_instruction_rules(model: IsaModel) -> dict[str, Any]:
    rules = (model.metadata.get("semantics") or {}).get("encoding_rules") or {}
    repeat = rules.get("repeat_instructions") or {}
    return repeat if isinstance(repeat, dict) else {}


def rule_label(key: Any) -> str:
    return str(key).replace("_", " ")


def repeat_syntax_rows(model: IsaModel) -> list[list[Any]]:
    syntax = repeat_instruction_rules(model).get("syntax") or {}
    rows = [[name, value] for name, value in syntax.items()]
    aliases = repeat_instruction_rules(model).get("assembler_checked_aliases") or {}
    for name, data in aliases.items():
        if not isinstance(data, dict):
            continue
        value = f"{compact_text(data.get('syntax', ''))}; emits {compact_text(data.get('emits', ''))}"
        requirements: list[str] = []
        body_candidate = data.get("body_candidate_required")
        if body_candidate:
            requirements.append(f"body candidate: {display_text(body_candidate)}")
        body_constraints = data.get("body_constraints") or []
        if isinstance(body_constraints, list):
            requirements.extend(compact_text(item) for item in body_constraints)
        elif body_constraints:
            requirements.append(compact_text(body_constraints))
        if requirements:
            value += "; requires " + "; ".join(requirements)
        rows.append([f"{name} assembler alias", value])
    return rows


def repeatable_class_rows(model: IsaModel) -> list[list[Any]]:
    contexts = repeat_instruction_rules(model).get("repeatable_contexts") or {}
    constraints = repeat_instruction_rules(model).get("repeatable_constraints") or {}
    annotations = repeat_instruction_rules(model).get("repeatable_annotations") or {}
    rows = [[name, display_text(value)] for name, value in contexts.items()]
    rows.extend([f"constraint: {rule_label(name)}", display_text(value)] for name, value in constraints.items())
    rows.extend([f"annotation: {rule_label(name)}", display_text(value)] for name, value in annotations.items())
    return rows


def repeat_body_entry_rows(model: IsaModel) -> list[list[Any]]:
    body = repeat_instruction_rules(model).get("body_entry") or {}
    return [[rule_label(key), display_text(value)] for key, value in body.items()]


def repeat_counter_rows(model: IsaModel) -> list[list[Any]]:
    counter = repeat_instruction_rules(model).get("counter") or {}
    condition = repeat_instruction_rules(model).get("condition") or {}
    rows = [[f"counter: {rule_label(key)}", display_text(value)] for key, value in counter.items()]
    rows.extend([f"condition: {rule_label(key)}", display_text(value)] for key, value in condition.items())
    return rows


def repeat_legality_rows(model: IsaModel) -> list[list[Any]]:
    legality = repeat_instruction_rules(model).get("legality") or {}
    pc = repeat_instruction_rules(model).get("pc_and_interrupts") or {}
    debug = repeat_instruction_rules(model).get("debugging") or {}
    rows = [[f"legality: {rule_label(key)}", display_text(value)] for key, value in legality.items()]
    rows.extend([f"pc: {rule_label(key)}", display_text(value)] for key, value in pc.items())
    rows.extend([f"debug: {rule_label(key)}", display_text(value)] for key, value in debug.items())
    return rows


def repeat_fault_aux_rows(model: IsaModel) -> list[list[Any]]:
    fault_aux = repeat_instruction_rules(model).get("fault_aux") or {}
    fields = fault_aux.get("fields") or []
    rows: list[list[Any]] = []
    for field in fields:
        if not isinstance(field, dict):
            continue
        rows.append([field.get("name", ""), field.get("bits", ""), field.get("meaning", "")])
    return rows


def render_streaming_model_md(model: IsaModel) -> str:
    body = md_paragraphs(
        "Streaming Execution Model",
        [
            "REP, REPcc, REPG, and any explicitly defined repeat instruction are architecturally scalar. Their visible behavior is the same as executing the repeated instruction or byte-counted instruction group in program order under the selected counter and termination rules.",
            "An implementation may recognize regular repeated operations and execute them with a micro-loop, loop buffer, streaming engine, or wider internal datapath. That internal width is not architectural state and is not part of the ABI.",
            "The repeated body is decoded when repeat state is entered and remains the body for that repeat context. Body decode and repeatability checks occur before zero-count annulment.",
            "Faults remain precise at the repeated-operation boundary. Completed iterations are committed; an incomplete faulting iteration is reported at the faulting instruction with restart state sufficient to continue or emulate the remaining work.",
        ],
    )
    body += "\n### Repeat Syntax\n\n" + md_table(["Form", "Syntax"], repeat_syntax_rows(model))
    body += "\n### Repeatability Contexts\n\n" + md_table(["Context", "Meaning"], repeatable_class_rows(model))
    body += "\n### Body Entry\n\n" + md_table(["Rule", "Meaning"], repeat_body_entry_rows(model))
    body += "\n### Counter and Condition\n\n" + md_table(["Rule", "Meaning"], repeat_counter_rows(model))
    body += "\n### Legality, PC, and Debug\n\n" + md_table(["Rule", "Meaning"], repeat_legality_rows(model))
    return body


def render_memory_translation_md(model: IsaModel) -> str:
    segment_rows = [
        ["disabled", "m = 0", "no segment-window check", "linear = EA"],
        ["translated window", "m != 0, b = 0", "0 <= EA < span", "linear = base + EA"],
        ["bounds-only window", "m != 0, b = 1", "base <= EA < limit", "linear = EA"],
    ]
    composition_rows = [
        ["Effective address", "address generated by the selected EA form"],
        ["Segment image", "base = base_page * 4096; span = (m << e) * 4096; limit = base + span, checked before 64-bit truncation"],
        ["Segment pre-translation", "disabled segments pass the address through; enabled segments check a byte-addressed window with page-granular base and span"],
        ["Linear address", "segment output, or the EA directly when segmentation is disabled"],
        ["Paging enabled", "walk page tables from PTCR.root_page and apply PTE attributes"],
        ["Paging disabled", "use the linear address directly as the memory-system address"],
        ["Faults", "invalid segment images raise INVALID_CONTROL_STATE on write; bounds and canonical-address failures raise PAGE_FAULT"],
    ]
    body = md_paragraphs(
        "Memory Address Translation",
        [
            "Memory address translation is a separate pipeline after effective-address calculation. Effective-address evaluation produces an address value or operand designator; segmentation optionally turns that value into a linear address, and paging optionally turns the linear address into a memory-system address.",
            "Instruction fetches use CS, stack accesses use SS, and ordinary data accesses use the operation default data segment unless an effective-address form explicitly selects another segment. SP and PC forms use their fixed segments.",
            "SEGLEA exposes the linear address produced by segment pre-translation when software explicitly needs it. The ISA does not prescribe a language pointer representation; the Bedrock C ABI uses canonical post-segment virtual addresses and restricts C-visible address contexts to disabled or bounds-only modes, with GS0-relative TLS as an explicit exception.",
        ],
    )
    body += "\n" + md_table(["Stage", "Result"], composition_rows)
    body += "\n" + md_table(["Mode", "Segment State", "Check", "Linear Address"], segment_rows)
    return body


def render_memory_model_md(model: IsaModel) -> str:
    body = md_paragraphs(
        "Memory Model",
        [
            "The memory model defines instruction fetches, loads, stores, atomic read-modify-write operations, cache maintenance, and translation-cache maintenance after EA calculation and address translation.",
            "Unaligned ordinary memory accesses are architecturally permitted, but may be implemented as multiple aligned memory beats and have no tear-free or atomicity guarantee.",
            "Atomic read-modify-write instructions require naturally aligned memory operands. A misaligned atomic operand is invalid for the atomic operation and must not complete as a non-atomic update.",
            "Stores to memory that is later executed as instructions are ordinary data stores until an explicit synchronization sequence makes the modified bytes visible to instruction fetch.",
        ],
    )
    body += "\n" + md_table(
        ["Suffix", "Bytes", "Natural Alignment", "Tear-Free Guarantee"],
        [
            ["B", 1, "any byte address", "aligned normal-memory load/store is tear-free"],
            ["W", 2, "address divisible by 2", "aligned normal-memory load/store is tear-free"],
            ["L", 4, "address divisible by 4", "aligned normal-memory load/store is tear-free"],
            ["Q", 8, "address divisible by 8", "aligned normal-memory load/store is tear-free"],
        ],
    )
    body += "\n### Atomic Memory-Order Selectors\n\n"
    body += md_table(["Selector", "Code", "Architectural Ordering Effect"], memory_order_rows(model))
    body += "\n### Fence Instructions\n\n"
    body += md_table(
        ["Instruction", "Ordering Effect"],
        [
            ["RFENCE", "Orders prior reads before later reads issued by the same hardware thread."],
            ["WFENCE", "Orders prior writes before later writes issued by the same hardware thread."],
            ["AFENCE", "Orders prior memory operations before later memory operations issued by the same hardware thread."],
        ],
    )
    return body


def render_instruction_set_overview_md(model: IsaModel, instructions: list[InstructionDef]) -> str:
    body = md_paragraphs(
        "Instruction Attribute Matrix",
        [
            "The instruction set is grouped semantically. Each instruction entry carries its own forms, operand rules, and encoding diagrams where those details are architecturally relevant.",
            "Extension instruction groups remain separate architectural definition sets: base, floating-point, transcendental floating-point, and virtualization acceleration.",
        ],
    )
    body += "\n" + md_table(["Class", "Family", "Definitions"], instruction_family_rows(instructions))
    return body


def render_instruction_summary_md(model: IsaModel, instructions: list[InstructionDef]) -> str:
    rows = []
    for inst in instructions:
        rows.append(
            [
                inst.mnemonic,
                instruction_set_text(inst.instruction_set),
                instruction_class(inst),
                instruction_family(inst),
                label_text(inst.behavior.get("group", "-")),
                privilege_text(inst.attributes.get("privilege", "-"), "-"),
                allocation_status(inst, model),
                inst.doc.get("summary", ""),
            ]
        )
    return "## Instruction Summary\n\n" + md_table(
        ["Mnemonic", "Set", "Class", "Family", "Group", "Privilege", "Encoding", "Summary"],
        rows,
    )


def render_instruction_reference_md(model: IsaModel, instructions: list[InstructionDef]) -> str:
    parts = ["## Instruction Reference\n"]
    for inst in instructions:
        parts.append(f"### {inst.mnemonic}\n")
        title = inst.doc.get("title")
        if title and title != inst.mnemonic:
            parts.append(f"**{md_escape(title)}**\n")
        summary = inst.doc.get("summary")
        if summary:
            parts.append(md_escape(summary) + "\n")
        description = inst.doc.get("description")
        if description:
            parts.append(md_escape(description) + "\n")
        rows = [
            ["Set", instruction_set_text(inst.instruction_set)],
            ["Class", instruction_class(inst)],
            ["Family", instruction_family(inst)],
            ["Behavior group", label_text(inst.behavior.get("group", "-"))],
            ["Privilege", privilege_text(inst.attributes.get("privilege", "-"), "-")],
            ["Encoding", allocation_status(inst, model)],
        ]
        parts.append(md_table(["Property", "Value"], rows))

        forms = form_rows(inst)
        if forms:
            parts.append(md_table(["Form Kind", "Operands", "Size", "Attributes"], forms))

        operations = inst.behavior.get("operation", []) or []
        if operations:
            parts.append(code_block("\n".join(str(item) for item in operations)))

        alloc_rows = []
        for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
            form = allocation_form_text(entry.text)
            notes = allocation_note_text(entry)
            alloc_rows.append([entry.cls, entry.bits, form, notes])
        if alloc_rows:
            parts.append(md_table(["Class", "Bits", "Form", "Notes"], alloc_rows))
    return "\n".join(parts)


def latex_cell(value: Any) -> str:
    return latex_escape(compact_text(value) or "-")


def latex_ragged_block(lines: list[str]) -> str:
    if not lines:
        return "-"
    body = "".join(rf"\noindent {line}\par " for line in lines)
    return rf"\begin{{manualraggedblock}}{body}\end{{manualraggedblock}}"


def latex_instruction_field(label: str, value_latex: str) -> str:
    if not value_latex:
        return ""
    return rf"\manualinstructionfield{{{latex_escape(label)}}}{{{value_latex}}}"


def latex_instruction_status(label: str, value_latex: str) -> str:
    if not value_latex:
        return ""
    return rf"\manualinstructionstatus{{{latex_escape(label)}}}{{{value_latex}}}"


def latex_code_line_stack(lines: list[str]) -> str:
    if not lines:
        return tex_code("-")
    rendered_lines = []
    for line in lines:
        rendered = tex_code(line).replace(", ", r",\allowbreak{} ")
        rendered_lines.append(rf"\noindent {rendered}\par ")
    return r"\begin{manualraggedblock}" + "".join(rendered_lines) + r"\end{manualraggedblock}"


def flag_summary(flags: Any) -> str:
    if isinstance(flags, dict):
        return "; ".join(f"{key}: {compact_text(value)}" for key, value in flags.items()) or "-"
    return compact_text(flags) or "-"


def latex_attributes_block(inst: InstructionDef, model: IsaModel) -> str:
    attrs = inst.attributes
    lines = [
        rf"{latex_escape('Class')} = {latex_escape(instruction_class(inst))}",
        rf"{latex_escape('Family')} = {latex_escape(instruction_family(inst))}",
        rf"{latex_escape('Privilege')} = {latex_escape(privilege_text(attrs.get('privilege', '-'), '-'))}",
    ]
    flags = attrs.get("flags")
    if flags:
        lines.append(rf"{latex_escape('Flags')} = {latex_escape(flag_summary(flags))}")
    return latex_ragged_block(lines)


def latex_operation_field(lines: list[Any]) -> str:
    if not lines:
        return ""
    escaped_lines = [latex_escape(line) for line in lines]
    return latex_instruction_field("Operation", latex_ragged_block(escaped_lines))


def latex_flag_status(inst: InstructionDef) -> str:
    flags = inst.attributes.get("flags")
    if not isinstance(flags, dict) or not flags:
        return ""
    names = [name for name in ("Z", "N", "C", "V") if name in flags]
    if names:
        header = " & ".join(rf"\textbf{{{latex_escape(name)}}}" for name in names)
        values = " & ".join("*" for _ in names)
        text = latex_escape(flag_summary(flags))
        return latex_instruction_status(
            "Condition Codes",
            rf"\begin{{manualraggedblock}}\begin{{tabular}}[t]{{@{{}}{'c' * len(names)}@{{}}}}"
            + "\n"
            + header
            + r"\\"
            + "\n"
            + values
            + r"\\"
            + "\n"
            + rf"\end{{tabular}}\par\smallskip {text}\end{{manualraggedblock}}",
        )
    return latex_instruction_status("Status", latex_ragged_block([latex_escape(flag_summary(flags))]))


def operand_syntax(operand: Any) -> str:
    if not isinstance(operand, dict):
        return compact_text(operand)
    typ = compact_text(operand.get("type", ""))
    mapping = {
        "EA": "<ea>",
        "Rn": "Rn",
        "imm": "<imm>",
        "imm3": "<imm3>",
        "imm6": "<imm6>",
        "imm8": "<imm8>",
        "imm16": "<imm16>",
        "imm32": "<imm32>",
        "SREG": "SREG",
    }
    return mapping.get(typ, typ or compact_text(operand.get("name", "-")))


def size_suffix(size: Any) -> str:
    text = compact_text(size)
    if not text or text == "-":
        return ""
    return ".<" + "/".join(text) + ">"


def fallback_form_syntax(inst: InstructionDef, form: dict[str, Any]) -> str:
    operands = form.get("operands", inst.forms.get("operands", []))
    suffix = size_suffix(form.get("size", inst.forms.get("size", "")))
    if operands == []:
        return inst.mnemonic
    return f"{inst.mnemonic}{suffix} {operand_list_text(operands).replace(':', ' ')}"


def assembler_syntax_lines(model: IsaModel, inst: InstructionDef) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
        form = allocation_form_text(entry.text)
        if form and form not in seen:
            lines.append(form)
            seen.add(form)
    if lines:
        return lines
    for _kind, form in iter_instruction_forms(inst):
        syntax = fallback_form_syntax(inst, form)
        if syntax not in seen:
            lines.append(syntax)
            seen.add(syntax)
    return lines


def latex_instruction_form_block(title: str, rows: list[tuple[str, str]], *, needspace: str = "1.45in") -> str:
    rendered_rows = []
    for key, value in rows:
        if not value:
            continue
        rendered_rows.append(rf"\textbf{{{latex_escape(key)}}} & {value}\\")
    if not rendered_rows:
        return ""
    return "\n".join(
        [
            rf"\begin{{manualformblock}}{{{needspace}}}",
            rf"\textbf{{{tex_code(title)}}}\par",
            r"\vspace{2pt}",
            r"\begin{tabularx}{\linewidth}{@{}p{0.88in}X@{}}",
            *rendered_rows,
            r"\end{tabularx}\par",
            r"\end{manualformblock}",
        ]
    )


def instruction_form_operands(form: str) -> str:
    parts = compact_text(form).split(maxsplit=1)
    return parts[1] if len(parts) > 1 else "-"


def split_form_operands(form: str) -> list[str]:
    operands = instruction_form_operands(form)
    if operands == "-":
        return []
    return [part.strip() for part in operands.split(",") if part.strip()]


def field_operand(form: str, symbol: str) -> tuple[int, str] | None:
    marker = f"({symbol})"
    for index, operand in enumerate(split_form_operands(form)):
        if marker in operand:
            return index, operand
    return None


def operand_role(index: int, operand_count: int) -> str:
    if operand_count == 1:
        return "operand"
    if index == 0:
        return "source operand"
    if index == 1:
        return "destination operand"
    return f"operand {index + 1}"


def operand_kind_description(operand: str) -> str:
    compact = operand.replace(" ", "")
    if compact.startswith("Rn("):
        return "general-purpose register operand"
    if compact.startswith("<ea>"):
        return "compact effective-address operand"
    if compact.startswith("<imm") or compact.startswith("imm"):
        return "immediate operand"
    if compact.startswith("SREG("):
        return "segment register operand"
    if compact == "SP":
        return "stack pointer operand"
    if compact == "PC":
        return "program-counter operand"
    return readable_operand_fragment(operand)


def readable_operand_fragment(operand: str) -> str:
    text = operand
    text = re.sub(r"\([a-zA-Z]\)", "", text)
    text = text.replace("<", "").replace(">", "")
    return compact_text(text).replace("_", " ") or "operand"


def readable_operands_from_form(form: str) -> str:
    operands = split_form_operands(form)
    if not operands:
        return "no explicit operands"
    if len(operands) == 1 and operands[0].startswith("<imm") and (
        form.startswith("J") or form.startswith("CALL")
    ):
        return "target is signed immediate displacement"
    pieces = []
    for index, operand in enumerate(operands):
        pieces.append(f"{operand_role(index, len(operands))} is {operand_kind_description(operand)}")
    return "; ".join(pieces)


def allocation_encoding_text(entry: AllocationEntry) -> str:
    return f"{entry.cls} opcode form"


CLASS_BASE_BYTES = {
    "extrashort": 1,
    "short": 2,
    "medium": 3,
    "long": 4,
    "extralong": 5,
}


def allocation_base_bytes(entry: AllocationEntry) -> int:
    if entry.cls in CLASS_BASE_BYTES:
        return CLASS_BASE_BYTES[entry.cls]
    return 2 + (max(0, entry.payload_bits - 10) + 7) // 8


def instruction_bytes_text(entry: AllocationEntry, form: str) -> str:
    base = allocation_base_bytes(entry)
    if any((field.get("kind") == "ea7") for field in entry.fields.values() if isinstance(field, dict)):
        return f"{base}-18"
    extra = 0
    if re.search(r"<imm16|imm16/bitmap", form):
        extra = max(extra, 2)
    if re.search(r"<imm32", form):
        extra = max(extra, 4)
    if re.search(r"<imm64", form):
        extra = max(extra, 8)
    return str(base + extra)


def allocation_size_bits(entry: AllocationEntry) -> str:
    if entry.cls == "extrashort":
        return "0"
    if entry.cls == "short":
        return "10"
    l_value = max(0, allocation_base_bytes(entry) - 3)
    return f"11{l_value:04b}"


def bit_label(text: str) -> str:
    if set(text) <= {"0", "1", "?"}:
        return text.replace("?", "-")
    if len(set(text)) == 1:
        return text[0]
    return text


def bit_segments(bits: str) -> list[tuple[str, int]]:
    if not bits:
        return []
    out: list[tuple[str, int]] = []
    start = 0

    def segment_class(ch: str) -> str:
        return "fixed" if ch in "01?" else ch

    current = segment_class(bits[0])
    for index, ch in enumerate(bits[1:], start=1):
        cls = segment_class(ch)
        if cls != current:
            chunk = bits[start:index]
            out.extend(split_bit_chunk(chunk))
            start = index
            current = cls
    chunk = bits[start:]
    out.extend(split_bit_chunk(chunk))
    return out


def split_bit_chunk(chunk: str) -> list[tuple[str, int]]:
    if set(chunk) <= {"0", "1", "?"} and len(chunk) > 4:
        return [(bit_label(chunk[index : index + 4]), len(chunk[index : index + 4])) for index in range(0, len(chunk), 4)]
    return [(bit_label(chunk), len(chunk))]


def bit_row_segments(label: str, segments: list[tuple[str, int]]) -> str:
    fields = [
        rf"\manualbitfieldcode{{{latex_escape(text)}}}{{{width}}}"
        for text, width in segments
        if width > 0
    ]
    return "\n".join([rf"\manualbitrow{{{latex_escape(label)}}}{{%", *fields, "}"])


def byte_pair_row_segments(label: str, byte0_segments: list[tuple[str, int]], byte1_segments: list[tuple[str, int]]) -> str:
    fields = [
        rf"\manualbitfieldcode{{{latex_escape(text)}}}{{{width}}}"
        for text, width in byte0_segments
        if width > 0
    ]
    fields.append(r"\manualbitgap{1}")
    fields.extend(
        rf"\manualbitfieldcode{{{latex_escape(text)}}}{{{width}}}"
        for text, width in byte1_segments
        if width > 0
    )
    return "\n".join(
        [
            rf"\manualbitfieldrow{{{latex_escape(label)}}}{{%",
            r"\manualbytepairlabels",
            r"}{%",
            *fields,
            "}",
        ]
    )


def split_segments_at_width(segments: list[tuple[str, int]], width: int) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    left: list[tuple[str, int]] = []
    right: list[tuple[str, int]] = []
    remaining = width
    for label, segment_width in segments:
        if remaining <= 0:
            right.append((label, segment_width))
        elif segment_width <= remaining:
            left.append((label, segment_width))
            remaining -= segment_width
        else:
            left.append((label, remaining))
            right.append((label, segment_width - remaining))
            remaining = 0
    return left, right


def entry_header_byte_segments(entry: AllocationEntry) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    if entry.cls == "extrashort":
        header_segments = [("0", 1), *bit_segments(entry.bits)]
        byte0, byte1 = split_segments_at_width(header_segments, 8)
        return byte0, byte1
    if entry.cls == "short":
        header_segments = [("10", 2), *bit_segments(entry.bits)]
        return split_segments_at_width(header_segments, 8)
    first_payload = entry.bits[:10]
    size_bits = allocation_size_bits(entry)
    header_segments = [(size_bits[:2], 2), (size_bits[2:], 4), *bit_segments(first_payload)]
    return split_segments_at_width(header_segments, 8)


def entry_payload_bit_rows(entry: AllocationEntry) -> list[tuple[str, list[tuple[str, int]]]]:
    if entry.cls in {"extrashort", "short"}:
        return []
    rows: list[tuple[str, list[tuple[str, int]]]] = []
    remaining = entry.bits[10:]
    byte_index = 2
    while remaining:
        chunk = remaining[:8]
        remaining = remaining[8:]
        rows.append((f"opcode byte {byte_index}", bit_segments(chunk)))
        byte_index += 1
    return rows


def latex_entry_bit_diagram(entry: AllocationEntry, form: str) -> str:
    byte0, byte1 = entry_header_byte_segments(entry)
    rows = [byte_pair_row_segments("header", byte0, byte1)]
    rows.extend(bit_row_segments(label, segments) for label, segments in entry_payload_bit_rows(entry))
    return "\n".join(
        [
            rf"\begin{{manualbitdiagram}}{{Instruction format for {latex_escape(form)}}}",
            *rows,
            r"\end{manualbitdiagram}",
        ]
    )


def field_bit_text(entry: AllocationEntry, symbol: str) -> str:
    positions = [entry.payload_bits - 1 - index for index, char in enumerate(entry.bits) if char == symbol]
    if not positions:
        return "opcode payload"
    high = max(positions)
    low = min(positions)
    bit_range = str(high) if high == low else f"{high}:{low}"
    if entry.cls == "extrashort":
        return f"extrashort opcode payload bits {bit_range}"
    if entry.cls == "short":
        return f"short opcode payload bits {bit_range}"
    return f"opcode payload bits {bit_range}"


def field_size_choices(form: str, symbol: str) -> str:
    match = re.search(rf"{re.escape(symbol)}:([A-Za-z0-9_/]+)", form)
    if not match:
        return ""
    return match.group(1)


def field_description(entry: AllocationEntry, form: str, symbol: str, spec: dict[str, Any]) -> str:
    kind = str(spec.get("kind", ""))
    operand = field_operand(form, symbol)
    operand_count = len(split_form_operands(form))
    role = operand_role(operand[0], operand_count) if operand else "operand"
    bit_text = field_bit_text(entry, symbol)
    if kind == "ea7":
        return (
            f"compact effective-address field for the {role} ({bit_text}). "
            "EA field selects register, memory, immediate, and EXT0 forms."
        )
    if kind == "rn":
        return f"general-purpose register number for the {role} ({bit_text})."
    if kind == "freg":
        return f"floating-point register number for the {role} ({bit_text})."
    if kind == "size":
        choices = field_size_choices(form, symbol)
        suffix = f" ({choices})" if choices else ""
        return f"size selector for the operand size{suffix} ({bit_text})."
    if kind == "condition":
        return f"condition-code selector ({bit_text})."
    if kind == "immediate":
        width = spec.get("width")
        width_text = f"{width}-bit " if width else ""
        return f"{width_text}immediate literal field for the {role} ({bit_text})."
    if kind == "bits":
        return f"encoded bit field for the {role} ({bit_text})."
    return f"encoded field for the {role} ({bit_text})."


def ordered_entry_fields(entry: AllocationEntry) -> list[tuple[str, dict[str, Any]]]:
    seen: set[str] = set()
    out: list[tuple[str, dict[str, Any]]] = []
    for symbol in entry.bits:
        if symbol in seen or symbol in "01?":
            continue
        field = entry.fields.get(symbol)
        if isinstance(field, dict):
            out.append((symbol, field))
            seen.add(symbol)
    for symbol, field in entry.fields.items():
        if symbol not in seen and isinstance(field, dict):
            out.append((symbol, field))
    return out


def constraint_texts(entry: AllocationEntry) -> list[str]:
    out: list[str] = []
    for constraint in entry.constraints:
        if not isinstance(constraint, dict):
            continue
        field = compact_text(constraint.get("field", ""))
        reason = compact_text(constraint.get("reason", ""))
        if field and constraint.get("exclude") in {"rn_direct", "reg_direct"}:
            out.append(f"{field} excludes register-direct EA encodings reserved for shorter canonical forms.")
        elif constraint.get("destination") and constraint.get("exclude") == "immediate":
            out.append("destination EA excludes immediate forms.")
        elif field and constraint.get("allow") and reason == "condition_true_false_reclaimed":
            out.append(f"{field} uses condition codes 0010..1111; T and F encodings are reserved.")
        elif field and constraint.get("allow") and reason == "condition_false_reclaimed":
            out.append(f"{field} uses condition codes 0000 and 0010..1111; F encoding is reserved.")
        elif field and constraint.get("allow"):
            out.append(f"{field} is restricted to {compact_text(constraint.get('allow'))}.")
        elif field and constraint.get("exclude"):
            out.append(f"{field} excludes {compact_text(constraint.get('exclude'))}.")
    return out


def latex_field_explanation_block(entry: AllocationEntry, form: str) -> str:
    rows = [r"\par\noindent\begin{tabularx}{\linewidth}{@{}p{0.28in}X@{}}"]
    body_rows: list[str] = []
    has_ea = False
    for symbol, spec in ordered_entry_fields(entry):
        if spec.get("kind") == "ea7":
            has_ea = True
        body_rows.append(rf"\texttt{{{latex_escape(symbol)}}} & {latex_escape(field_description(entry, form, symbol, spec))}\\")
    if has_ea:
        body_rows.append(
            r" & EA selections may append displacement, absolute-address, immediate, or EXT0 payload bytes.\\"
        )
    for text in constraint_texts(entry):
        body_rows.append(rf" & {latex_escape(text)}\\")
    if not body_rows:
        return ""
    rows.extend(body_rows)
    rows.append(r"\end{tabularx}\par")
    return "\n".join(rows)


def latex_allocated_instruction_form_block(inst: InstructionDef, entry: AllocationEntry) -> str:
    form = allocation_form_text(entry.text)
    notes = allocation_note_text(entry)
    rows = [
        ("Form", latex_escape(instruction_form_operands(form))),
        ("Encoding", latex_escape(allocation_encoding_text(entry))),
        ("Bytes", latex_escape(instruction_bytes_text(entry, form))),
        ("Privilege", latex_escape(privilege_text(inst.attributes.get("privilege", "unprivileged")))),
        ("Operands", latex_escape(readable_operands_from_form(form))),
    ]
    if notes and notes != "-":
        rows.append(("Notes", latex_escape(notes)))
    rendered_rows = [rf"\textbf{{{latex_escape(key)}}} & {value}\\" for key, value in rows if value]
    return "\n".join(
        [
            r"\begin{manualformblock}{2.9in}",
            rf"\textbf{{{tex_code(form)}}}\par",
            r"\vspace{2pt}",
            r"\begin{tabularx}{\linewidth}{@{}p{0.88in}X@{}}",
            *rendered_rows,
            r"\end{tabularx}\par",
            latex_entry_bit_diagram(entry, form),
            latex_field_explanation_block(entry, form),
            r"\end{manualformblock}",
        ]
    )


def latex_instruction_forms_block(model: IsaModel, inst: InstructionDef) -> str:
    blocks: list[str] = []
    for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
        blocks.append(latex_allocated_instruction_form_block(inst, entry))
    if not blocks:
        for kind, form in iter_instruction_forms(inst):
            attrs = []
            for key in ("profile", "constraint", "result", "flags", "compact"):
                if key in form:
                    attrs.append(form_attribute_text(key, form[key]))
            rows = [
                ("Form", latex_escape(operand_list_text(form.get("operands", inst.forms.get("operands", []))))),
                ("Kind", latex_escape(kind)),
                ("Size", latex_escape(form_size_text(form.get("size", inst.forms.get("size", "-"))))),
            ]
            if attrs:
                rows.append(("Attributes", latex_escape("; ".join(attrs))))
            blocks.append(latex_instruction_form_block(fallback_form_syntax(inst, form), rows, needspace="1.25in"))
    if not blocks:
        return ""
    return "\n".join([r"\begin{manualinstructionforms}", *blocks, r"\end{manualinstructionforms}"])


def render_latex(model: IsaModel, only_allocated: bool = False) -> str:
    instructions = [
        item
        for item in model.instructions
        if not only_allocated or item.mnemonic in model.allocated_by_mnemonic
    ]
    plan = {"solver": {"status": "manual allocation"}}
    allocated_form_count = sum(
        entry.assigned
        for cls in model.allocation_classes
        for entry in cls.entries
    )
    parts = [
        LatexDocumentPreamble(),
        LatexTitlePage(plan, len(instructions), allocated_form_count),
        latex_architecture_overview_section(model, instructions),
        latex_terminology_section(model),
        latex_compatibility_section(model),
        latex_register_section(model),
        latex_cpuid_feature_discovery_section(model),
        latex_save_restore_section(model),
        latex_data_formats_section(model),
        latex_condition_section(model),
        latex_ea_section(model),
        latex_legacy_reference_section("Memory Address Translation") or latex_memory_translation_section(model),
        latex_legacy_reference_section("Memory Model") or latex_memory_model_section(model),
        latex_privileged_programming_model_section(model),
        latex_exception_processing_section(model),
        latex_instruction_word_formats_section(model),
        latex_execution_model_section(model),
        latex_streaming_model_section(model),
        latex_instruction_summary_section(model, instructions),
        latex_condition_computation_section(model),
        latex_instruction_reference_section(model, instructions),
        latex_c_library_examples_section(),
        latex_runtime_examples_section(),
        LatexDocumentEnd(),
    ]
    return "\n".join(str(part) for part in parts if part) + "\n"


def latex_table(
    headers: list[str],
    rows: list[list[Any]],
    widths: list[str],
    caption: str,
    *,
    style: str = "default",
    listed: bool = True,
) -> str:
    return latex_longtable(
        headers,
        [[latex_cell(value) for value in row] for row in rows],
        widths,
        caption,
        style=style,
        listed=listed,
    )


def latex_fixed_table(
    headers: list[str],
    rows: list[list[Any]],
    widths: list[str],
    caption: str,
    *,
    listed: bool = True,
) -> str:
    return latex_tabular(
        headers,
        [[latex_cell(value) for value in row] for row in rows],
        widths,
        caption,
        listed=listed,
    )


def latex_code_table(
    headers: list[str],
    rows: list[list[Any]],
    widths: list[str],
    caption: str,
    code_columns: set[int],
    *,
    style: str = "default",
    listed: bool = True,
) -> str:
    rendered_rows: list[list[str]] = []
    for row in rows:
        rendered = []
        for index, value in enumerate(row):
            rendered.append(tex_code(value) if index in code_columns else latex_cell(value))
        rendered_rows.append(rendered)
    return latex_longtable(headers, rendered_rows, widths, caption, style=style, listed=listed)


def latex_block_field(label: str, value: Any) -> str:
    text = compact_text(value)
    if not text:
        return ""
    return rf"\manualblockfield{{{latex_escape(label)}:}}{{{latex_escape(text)}}}"


def latex_code_block(lines: list[Any]) -> str:
    if not lines:
        return ""
    body = "\n".join(latex_escape(line) + r"\\" for line in lines)
    return "\n".join(
        [
            r"\begin{manualformblock}{0.70in}",
            r"\begin{tabular}{@{}l@{}}",
            body,
            r"\end{tabular}",
            r"\end{manualformblock}",
        ]
    )


def latex_operation_block(lines: list[Any]) -> str:
    if not lines:
        return ""
    return "\n".join(
        [
            r"\par\Needspace{0.70in}",
            rf"\noindent\textbf{{{latex_escape('Operation')}:}}\par",
            latex_code_block(lines),
        ]
    )


def latex_rn_register_model_figure() -> str:
    return r"""
\begin{center}
\resizebox{0.98\linewidth}{!}{%
\begin{tikzpicture}[x=1in,y=1in,every node/.style={font=\scriptsize}]
\def\regw{1.70}
\def\rowh{0.18}
\foreach \i in {0,...,15} {
  \pgfmathsetmacro{\y}{-0.235*\i}
  \draw (0,\y) rectangle (\regw,\y-\rowh);
  \draw (0.85,\y) -- (0.85,\y-\rowh);
  \draw (1.275,\y) -- (1.275,\y-\rowh);
  \draw (1.488,\y) -- (1.488,\y-\rowh);
  \node[anchor=west] at (1.78,\y-\rowh/2) {R\i};
}
\node[anchor=south] at (0,0.02) {63};
\node[anchor=south] at (0.85,0.02) {31};
\node[anchor=south] at (1.275,0.02) {15};
\node[anchor=south] at (1.488,0.02) {7};
\node[anchor=south] at (1.70,0.02) {0};
\draw (2.28,0) -- (2.42,0) -- (2.42,-3.705) -- (2.28,-3.705);
\node[anchor=west] at (2.60,-1.85) {\shortstack[l]{GENERAL\\REGISTERS\\R0--R15}};

\draw (0,-4.05) rectangle (\regw,-4.23);
\node[anchor=west] at (1.78,-4.14) {SP};
\draw (0,-4.33) rectangle (\regw,-4.51);
\node[anchor=west] at (1.78,-4.42) {PC};
\draw (2.28,-4.05) -- (2.42,-4.05) -- (2.42,-4.51) -- (2.28,-4.51);
\node[anchor=west] at (2.60,-4.28) {\shortstack[l]{SPECIAL\\REGISTERS}};

\draw (1.275,-4.86) rectangle (1.70,-5.04);
\node[anchor=west] at (1.78,-4.95) {FLAGS};
\draw (1.275,-5.13) rectangle (1.70,-5.31);
\node[anchor=west] at (1.78,-5.22) {STATUS};
\draw (2.28,-4.86) -- (2.42,-4.86) -- (2.42,-5.31) -- (2.28,-5.31);
\node[anchor=west] at (2.60,-5.08) {\shortstack[l]{INTEGER\\STATE}};

\foreach \i in {0,1,2} {
  \pgfmathsetmacro{\y}{-0.235*\i}
  \draw (3.45,\y) rectangle (5.15,\y-\rowh);
  \draw (4.30,\y) -- (4.30,\y-\rowh);
  \node[anchor=west] at (5.23,\y-\rowh/2) {F\i};
}
\draw (3.45,-0.705) rectangle (5.15,-0.885);
\draw (4.30,-0.705) -- (4.30,-0.885);
\node[anchor=west] at (5.23,-0.795) {...};
\draw (3.45,-0.940) rectangle (5.15,-1.120);
\draw (4.30,-0.940) -- (4.30,-1.120);
\node[anchor=west] at (5.23,-1.030) {F15};
\node[anchor=south] at (3.45,0.02) {63};
\node[anchor=south] at (4.30,0.02) {31};
\node[anchor=south] at (5.15,0.02) {0};
\draw (5.73,0) -- (5.87,0) -- (5.87,-1.120) -- (5.73,-1.120);
\node[anchor=west] at (6.05,-0.56) {\shortstack[l]{FLOATING-POINT\\REGISTERS}};

\draw (4.725,-1.45) rectangle (5.15,-1.63);
\node[anchor=west] at (5.23,-1.54) {FFLAGS};
\draw (4.725,-1.72) rectangle (5.15,-1.90);
\node[anchor=west] at (5.23,-1.81) {FSTATUS};
\draw (5.73,-1.45) -- (5.87,-1.45) -- (5.87,-1.90) -- (5.73,-1.90);
\node[anchor=west] at (6.05,-1.675) {\shortstack[l]{FPU\\STATE}};

\foreach \name/\idx in {CS/0,DS/1,SS/2,GS0/3,GS1/4,GS2/5,GS3/6,GS4/7} {
  \pgfmathsetmacro{\y}{-2.25-0.235*\idx}
  \draw (3.45,\y) rectangle (5.15,\y-\rowh);
  \node[anchor=west] at (5.23,\y-\rowh/2) {\name};
}
\draw (5.73,-2.25) -- (5.87,-2.25) -- (5.87,-4.075) -- (5.73,-4.075);
\node[anchor=west] at (6.05,-3.16) {\shortstack[l]{SEGMENT\\REGISTERS}};

\foreach \name/\idx in {PTCR/0,ASCR/1,ICR/2,SPC/3,SCS/4,SDS/5,PMC/6} {
  \pgfmathsetmacro{\y}{-4.40-0.235*\idx}
  \draw (3.45,\y) rectangle (5.15,\y-\rowh);
  \node[anchor=west] at (5.23,\y-\rowh/2) {\name};
}
\draw (5.73,-4.40) -- (5.87,-4.40) -- (5.87,-5.990) -- (5.73,-5.990);
\node[anchor=west] at (6.05,-5.20) {\shortstack[l]{CONTROL\\REGISTERS}};
\end{tikzpicture}
}
\manualfigurecaption{User Programming Model}
\end{center}
""".strip()


def latex_state_register_format_diagrams() -> str:
    return r"""
\subsection{FLAGS and STATUS Registers}
FLAGS and STATUS are accessed through dedicated read/write instructions. Reserved bits read as zero and must remain zero.

\begin{manuallistedformatdiagram}{FLAGS Register Format}{3}
\manualformatrow{FLAGS[15:0]}{%
\manualformatfield{0}{12}
\manualformatfield{Z}{1}
\manualformatfield{N}{1}
\manualformatfield{C}{1}
\manualformatfield{V}{1}
}
\end{manuallistedformatdiagram}

\begin{manuallistedformatdiagram}{STATUS Register Format}{3}
\manualformatrow{STATUS[15:0]}{%
\manualformatfield{0}{10}
\manualformatfield{IE}{1}
\manualformatfield{PM}{1}
\manualformatfield{RF}{1}
\manualformatfield{TF}{1}
\manualformatfield{NI}{1}
\manualformatfield{IN}{1}
}
\end{manuallistedformatdiagram}
""".strip()


def latex_segment_register_format_diagram() -> str:
    return r"""
\begin{manuallistedformatdiagram}{Segment Register Format}{5}
\manualformatrow{segment[63:0]}{%
\manualformatfield{base\_page}{52}
\manualformatfield{e}{5}
\manualformatfield{m}{6}
\manualformatfield{b}{1}
}
\end{manuallistedformatdiagram}
""".strip()


def latex_integer_register_subfield_diagram() -> str:
    return r"""
\begin{manuallistedformatdiagram}{Integer Register Operand Subfields}{4}
\manualformatrow{Q}{%
\manualformatfield{Q operand bits 63..0}{64}
}
\manualformatrow{L}{%
\manualformatfield{unchanged / instruction-defined}{32}
\manualformatfield{L operand bits 31..0}{32}
}
\manualformatrow{W}{%
\manualformatfield{unchanged / instruction-defined}{48}
\manualformatfield{W bits 15..0}{16}
}
\manualformatrow{B}{%
\manualformatfield{unchanged / instruction-defined}{56}
\manualformatfield{B bits 7..0}{8}
}
\end{manuallistedformatdiagram}
""".strip()


def latex_save_area_diagram() -> str:
    rows = []
    offset = 0x010
    for index in range(16):
        rows.append([f"0x{offset:03x}", f"R{index}", "64-bit general-purpose register image"])
        offset += 8
    rows.extend(
        [
            ["0x090", "GS0", "optional segment image; present when the corresponding GS_VALID bit is set"],
            ["0x098", "GS1", "optional segment image; present when the corresponding GS_VALID bit is set"],
            ["0x0a0", "GS2", "optional segment image; present when the corresponding GS_VALID bit is set"],
            ["0x0a8", "GS3", "optional segment image; present when the corresponding GS_VALID bit is set"],
            ["0x0b0", "GS4", "optional segment image; present when the corresponding GS_VALID bit is set"],
            ["0x0b8", "reserved", "reserved fixed-base slot; written as zero"],
            ["0x0c0+", "extension state", "CPUID-defined 64-byte-aligned component slots"],
        ]
    )
    return "\n".join(
        [
            r"\begin{manuallistedformatdiagram}{SAVE/RESTORE Base Header}{4}",
            r"\manualformatrowrange{header[63:0]}{63}{0}{%",
            r"\manualformatfield{reserved}{12}",
            r"\manualformatfield{STATUS}{16}",
            r"\manualformatfield{FLAGS}{16}",
            r"\manualformatfield{reserved}{11}",
            r"\manualformatfield{GS\_VALID}{5}",
            r"\manualformatfield{FMT}{4}",
            r"}",
            r"\manualformatrowrange{bitmap[63:0]}{63}{0}{%",
            r"\manualformatfield{state block bitmap}{64}",
            r"}",
            r"\end{manuallistedformatdiagram}",
            latex_code_table(
                ["Offset", "Field", "Contents"],
                rows,
                ["0.55in", "0.90in", "3.95in"],
                "SAVE/RESTORE Fixed Base Block",
                {0, 1},
                style="dense",
                listed=False,
            ),
        ]
    )


def latex_ivt_entry_diagrams() -> str:
    return r"""
\begin{manuallistedformatdiagram}{Interrupt Vector Table Entry}{3}
\manualformatrowrange{entry bytes}{15}{0}{%
\manualformatfield{reserved}{7}
\manualformatfield{control}{1}
\manualformatfield{handler address}{8}
}
\end{manuallistedformatdiagram}

\begin{manuallistedformatdiagram}{IVT Entry Control Byte}{2}
\manualformatrowrange{byte 8}{7}{0}{%
\manualformatfield{reserved}{4}
\manualformatfield{SN}{2}
\manualformatfield{0}{1}
\manualformatfield{HP}{1}
}
\end{manuallistedformatdiagram}
""".strip()


@dataclass(frozen=True)
class StackFrameSlot:
    offset: int
    name: str
    is_payload: bool = False


def latex_stack_frame_figure(slots: list[StackFrameSlot], caption: str) -> str:
    if not slots:
        return ""
    rows = [rf"\begin{{manuallistedstackframediagram}}{{{latex_escape(caption)}}}"]
    for slot in slots:
        if slot.is_payload:
            command = "manualstackframepayload"
        elif slot.offset == 0:
            command = "manualstackframespslot"
        else:
            command = "manualstackframeslot"
        rows.append(
            rf"\{command}{{{latex_escape(f'+0x{slot.offset:02X}')}}}{{{latex_escape(slot.name)}}}"
        )
    rows.append(r"\end{manuallistedstackframediagram}")
    return "\n".join(rows)


def latex_supervisor_stack_frame_diagram() -> str:
    slots = [
        StackFrameSlot(0x40, "type-selected 64-byte payload blocks", is_payload=True),
        StackFrameSlot(0x38, "SAVED_SS"),
        StackFrameSlot(0x30, "SAVED_DS"),
        StackFrameSlot(0x28, "SAVED_CS"),
        StackFrameSlot(0x20, "SAVED_SP"),
        StackFrameSlot(0x18, "SAVED_PC"),
        StackFrameSlot(0x10, "FRAME_EXT1"),
        StackFrameSlot(0x08, "FRAME_EXT0"),
        StackFrameSlot(0x00, "FRAME_CONTROL"),
    ]
    return latex_stack_frame_figure(slots, "Supervisor Entry Stack Frame")


def latex_frame_control_diagram() -> str:
    return r"""
\begin{manuallistedformatdiagram}{FRAME\_CONTROL Format}{3}
\manualformatrowrange{FRAME\_CONTROL[63:32]}{63}{32}{%
\manualformatfield{STATUS}{16}
\manualformatfield{FLAGS}{16}
}
\manualformatrowrange{FRAME\_CONTROL[31:0]}{31}{0}{%
\manualformatfield{entry metadata}{8}
\manualformatfield{frame type}{4}
\manualformatfield{idepth}{4}
\manualformatfield{frame size}{8}
\manualformatfield{vector}{8}
}
\end{manuallistedformatdiagram}
""".strip()


def latex_repeat_fault_aux_diagram() -> str:
    return r"""
\begin{manuallistedformatdiagram}{FAULT\_AUX Repeat Continuation Format}{2}
\manualformatrowrange{FAULT\_AUX[63:32]}{63}{32}{%
\manualformatfield{reserved}{16}
\manualformatfield{body bytes}{16}
}
\manualformatrowrange{FAULT\_AUX[31:0]}{31}{0}{%
\manualformatfield{group start delta}{16}
\manualformatfield{reserved}{6}
\manualformatfield{kind}{2}
\manualformatfield{cc}{4}
\manualformatfield{reg}{4}
}
\end{manuallistedformatdiagram}
""".strip()


def latex_data_byte_order_diagrams() -> str:
    return r"""
\begin{manuallistedbyteorderdiagram}{Little-Endian Byte Order for a 64-Bit Value}{byte}{address}{increasing addresses}{least significant byte first}{most significant byte last}
\manualbytecell{$V[7..0]$}{A+0}
\manualbytecell{$V[15..8]$}{A+1}
\manualbytecell{$V[23..16]$}{A+2}
\manualbytecell{$V[31..24]$}{A+3}
\manualbytecell{$V[39..32]$}{A+4}
\manualbytecell{$V[47..40]$}{A+5}
\manualbytecell{$V[55..48]$}{A+6}
\manualbytecell{$V[63..56]$}{A+7}
\end{manuallistedbyteorderdiagram}

\begin{manuallistedbyteorderdiagram}{Instruction Start Bytes}{header byte}{}{instruction stream byte order}{}{}
\manualbytecell{\shortstack{class/length\\opcode high}}{PC+0}
\manualbytecell{\shortstack{opcode bits\\if present}}{PC+1}
\end{manuallistedbyteorderdiagram}
""".strip()


def latex_instruction_encoding_diagrams() -> str:
    return r"""
\begin{manuallistedbitdiagram}{Instruction Record Components}
\manualbitrow{extrashort byte}{%
\manualbitfieldcode{0}{1}
\manualbitfieldtext{payload[6:0]}{7}
}
\manualbitfieldrow{short header}{%
\manualbytepairlabels
}{%
\manualbitfieldcode{10}{2}
\manualbitfieldtext{payload[13:8]}{6}
\manualbitgap{1}
\manualbitfieldtext{payload[7:0]}{8}
}
\manualbitfieldrow{extended header}{%
\manualbytepairbitlabels
}{%
\manualbitfieldcode{11}{2}
\manualbitfieldtext{L}{4}
\manualbitfieldtext{opcode high}{2}
\manualbitgap{1}
\manualbitfieldtext{opcode next}{8}
}
\manualbitrow{extended continuation}{%
\manualbitfieldtext{remaining opcode bytes, EA descriptors, immediates, and displacements}{16}
}
\end{manuallistedbitdiagram}

\begin{manuallistedbitdiagram}{Opcode Payload Namespaces}
\manualbitrow{extrashort}{%
\manualbitfieldtext{payload[6:0]}{7}
}
\manualbitrow{short}{%
\manualbitfieldtext{payload[13:0]}{14}
}
\manualbitrow{medium}{%
\manualbitfieldtext{payload[17:0]}{18}
}
\manualbitrow{long group 0}{%
\manualbitfieldcode{11110x}{6}
\manualbitfieldtext{payload[19:0]}{20}
}
\manualbitrow{long group 1}{%
\manualbitfieldcode{111110}{6}
\manualbitfieldtext{payload[19:0]}{20}
}
\manualbitrow{extralong}{%
\manualbitfieldcode{111111}{6}
\manualbitfieldtext{payload[27:0]}{28}
}
\end{manuallistedbitdiagram}

\subsection{Representative Encodings}
\begin{manuallistedbitdiagram}{Short Encoding Layout for MOV.X(z:L/Q) Rn(s), Rn(d)}
\manualbitrow{payload[13:0]}{%
\manualbitfieldcode{00}{2}
\manualbitfieldcode{000}{3}
\manualbitfieldcode{z}{1}
\manualbitfieldcode{s}{4}
\manualbitfieldcode{d}{4}
}
\end{manuallistedbitdiagram}

\begin{manuallistedbitdiagram}{Medium Encoding Layout for MOV.X(z:B/W) Rn(s), \textless{}ea\textgreater{}(e)}
\manualbitrow{payload[17:0]}{%
\manualbitfieldcode{00}{2}
\manualbitfieldcode{0000}{4}
\manualbitfieldcode{z}{1}
\manualbitfieldcode{s}{4}
\manualbitfieldcode{e}{7}
}
\end{manuallistedbitdiagram}

\begin{manuallistedbitdiagram}{Long Encoding Layout for ADC.X(z:B/W/L/Q) Rn(s), \textless{}ea\textgreater{}(e)}
\manualbitrow{payload[25:0]}{%
\manualbitfieldcode{1111000000}{10}
\manualbitfieldcode{z}{2}
\manualbitfieldcode{000}{3}
\manualbitfieldcode{s}{4}
\manualbitfieldcode{e}{7}
}
\end{manuallistedbitdiagram}
""".strip()


def latex_ea_field_diagrams() -> str:
    return r"""
\begin{manuallistedbitdiagram}{Compact Effective-Address Field}
\manualbitfieldrow{EA[6:0]}{%
\manualbitlabel{6}
\manualbitlabel{4}
\manualbitlabel{3}
\manualbitlabel{0}
}{%
\manualbitfieldtext{mode}{3}
\manualbitfieldtext{register/form}{4}
}
\end{manuallistedbitdiagram}

\begin{manuallistedbitdiagram}{EXT0 One-Byte Descriptor Forms}
\manualbitrow{SEG + base}{%
\manualbitfieldcode{0}{1}
\manualbitfieldcode{s}{3}
\manualbitfieldcode{b}{4}
}
\manualbitrow{SEG + zero}{%
\manualbitfieldcode{1}{1}
\manualbitfieldcode{s}{3}
\manualbitfieldcode{0011}{4}
}
\manualbitrow{default base++}{%
\manualbitfieldcode{1}{1}
\manualbitfieldcode{b}{4}
\manualbitfieldcode{100}{3}
}
\manualbitrow{default --base}{%
\manualbitfieldcode{1}{1}
\manualbitfieldcode{b}{4}
\manualbitfieldcode{101}{3}
}
\end{manuallistedbitdiagram}

\begin{manuallistedbitdiagram}{EXT0 Two-Byte Indexed Descriptor Forms}
\manualbitrow{SEG + base + index}{%
\manualbitfieldcode{1}{1}
\manualbitfieldcode{s}{3}
\manualbitfieldcode{mode}{4}
\manualbitfieldcode{b}{4}
\manualbitfieldcode{i}{4}
}
\manualbitrow{SP/PC + index}{%
\manualbitfieldcode{1000101}{7}
\manualbitfieldcode{x}{1}
\manualbitfieldcode{mode}{4}
\manualbitfieldcode{i}{4}
}
\end{manuallistedbitdiagram}
""".strip()


def ea_payload_catalog_rows() -> list[list[Any]]:
    return [
        ["disp8s", 1, "signed", "displacement added to the selected base/index expression"],
        ["disp16s", 2, "signed", "displacement added to the selected base/index expression"],
        ["disp32s", 4, "signed", "displacement added to the selected base/index expression"],
        ["disp64", 8, "unsigned", "displacement added to the selected base/index expression"],
        ["abs32s", 4, "signed", "absolute address payload, sign-extended before use"],
        ["abs64", 8, "unsigned", "absolute address payload"],
        ["imm8s", 1, "signed", "immediate operand payload"],
        ["imm16s", 2, "signed", "immediate operand payload"],
        ["imm32s", 4, "signed", "immediate operand payload"],
        ["imm64", 8, "unsigned", "immediate operand payload"],
        ["EXT0 descriptor", "1 or 2", "encoded", "extended EA descriptor; present only for EXT0 escapes"],
    ]


def ea_reference_needspace(rows: list[tuple[str, str]], diagram: str) -> str:
    if not diagram:
        return "2.35in"
    if "manualeaindexedmemoryflow" in diagram:
        base = 5.95
    elif "manualeaadditivememoryflow" in diagram:
        base = 4.75
    elif "manualeasimplememoryflow" in diagram:
        base = 4.25
    elif "manualeadirectflow" in diagram or "manualeaimmediateflow" in diagram:
        base = 3.65
    else:
        base = 4.50
    # Long assembler-syntax/descriptor rows wrap and need to be reserved with the diagram.
    wrapped_row_margin = 0.16 * sum(1 for _key, value in rows if len(value) > 92)
    return f"{base + wrapped_row_margin:.2f}in"


def ea_reference_block(title: str, rows: list[tuple[str, str]], *, diagram: str = "", needspace: str | None = None) -> str:
    block_needspace = needspace or ea_reference_needspace(rows, diagram)
    rendered_rows = [rf"\textbf{{{latex_escape(key)}}} & {latex_escape(value)}\\" for key, value in rows if value]
    parts = [
        rf"\begin{{manualformblock}}{{{block_needspace}}}",
        rf"\textbf{{{tex_code(title)}}}\par",
        r"\vspace{2pt}",
        r"\begin{tabularx}{\linewidth}{@{}p{1.10in}X@{}}",
        *rendered_rows,
        r"\end{tabularx}\par",
    ]
    if diagram:
        parts.append(diagram)
    parts.append(r"\end{manualformblock}")
    return "\n".join(parts)


def compact_ea_reference_blocks() -> list[str]:
    return [
        ea_reference_block(
            "Register Direct",
            [
                ("Assembler syntax", "Rn(r), SP"),
                ("EA encoding", "000rrrr selects Rn(r); 1101000 selects SP."),
                ("EA type", "register operand, not a memory reference."),
                ("Generation", "The operand value is the selected register value. No effective memory address is generated."),
                ("Segment", "No segment is selected."),
                ("Payload", "No appended EA payload bytes."),
                ("Update", "No auto-update."),
            ],
            diagram=r"\manualeadirectflow{Direct register operand}{REGISTER}{Rn or SP contents}{REGISTER VALUE}",
        ),
        ea_reference_block(
            "Rn Memory",
            [
                ("Assembler syntax", "[Rn(r)], [Rn(r) + disp8s], [Rn(r) + disp16s], [Rn(r) + disp32s], [Rn(r) + disp64]"),
                ("EA encoding", "001rrrr has no displacement; 010rrrr, 011rrrr, 100rrrr, and 101rrrr select disp8s, disp16s, disp32s, and disp64."),
                ("EA type", "memory operand."),
                ("Generation", "offset = temporary Rn(r) + displacement. The no-displacement form uses displacement 0."),
                ("Segment", "Uses the operation default data segment unless the instruction defines a different default."),
                ("Payload", "Only displacement forms append payload bytes. Displacement payload is little-endian and has the size named by the EA form."),
                ("Update", "No auto-update in compact Rn memory forms."),
            ],
            diagram=r"\manualeaadditivememoryflow{Rn memory address generation}{BASE REGISTER}{Rn(r)}{optional displacement}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "SP Memory",
            [
                ("Assembler syntax", "[SP], [SP + disp8s], [SP + disp16s], [SP + disp32s], [SP + disp64]"),
                ("EA encoding", "1101001 has no displacement; 1100000, 1100001, 1100010, and 1100011 select disp8s, disp16s, disp32s, and disp64."),
                ("EA type", "memory operand."),
                ("Generation", "offset = temporary SP + displacement. The no-displacement form uses displacement 0."),
                ("Segment", "Fixed to SS; no segment field is encoded."),
                ("Payload", "Only displacement forms append payload bytes. Displacement payload is little-endian and has the size named by the EA form."),
                ("Update", "No auto-update in compact SP memory forms."),
            ],
            diagram=r"\manualeaadditivememoryflow{SP memory address generation}{STACK POINTER}{SP}{optional displacement}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "PC Memory",
            [
                ("Assembler syntax", "[PC + disp8s], [PC + disp16s], [PC + disp32s], [PC + disp64]"),
                ("EA encoding", "1100100, 1100101, 1100110, and 1100111 select disp8s, disp16s, disp32s, and disp64."),
                ("EA type", "memory operand."),
                ("Generation", "offset = temporary PC term + displacement. The PC term is the PC value supplied to operand evaluation by the execution model."),
                ("Segment", "Fixed to CS; no segment field is encoded."),
                ("Payload", "A displacement payload is always present. Payload is little-endian and has the size named by the EA form."),
                ("Update", "No auto-update for PC forms."),
            ],
            diagram=r"\manualeaadditivememoryflow{PC-relative address generation}{PROGRAM COUNTER}{PC term}{displacement}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "Absolute Memory",
            [
                ("Assembler syntax", "[abs32s], [abs64]"),
                ("EA encoding", "1101010 selects abs32s; 1101011 selects abs64."),
                ("EA type", "memory operand."),
                ("Generation", "offset = sign-extended abs32s or unsigned abs64."),
                ("Segment", "Uses the operation default data segment unless the instruction defines a different default."),
                ("Payload", "The absolute address payload is little-endian and has the size named by the EA form."),
                ("Update", "No auto-update."),
            ],
            diagram=r"\manualeasimplememoryflow{Absolute memory address generation}{ABSOLUTE ADDRESS}{address payload}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "Immediate",
            [
                ("Assembler syntax", "imm8s, imm16s, imm32s, imm64"),
                ("EA encoding", "1101100, 1101101, 1101110, and 1101111 select imm8s, imm16s, imm32s, and imm64."),
                ("EA type", "immediate operand, not a memory reference."),
                ("Generation", "The operand value is decoded from the immediate payload. Signed payloads are sign-extended according to the consuming instruction's operand rule."),
                ("Segment", "No segment is selected."),
                ("Payload", "The immediate payload is little-endian and has the size named by the EA form."),
                ("Update", "No auto-update. Immediate forms are not valid destinations unless an instruction explicitly defines such a form."),
            ],
            diagram=r"\manualeaimmediateflow{Immediate operand generation}{payload value}{IMMEDIATE VALUE}",
        ),
        ea_reference_block(
            "EXT0 Escape",
            [
                ("Assembler syntax", "EXT0, EXT0/disp8s, EXT0/disp16s, EXT0/disp32s, EXT0/disp64"),
                ("EA encoding", "1110100 selects no displacement; 1110000, 1110001, 1110010, and 1110011 select disp8s, disp16s, disp32s, and disp64."),
                ("EA type", "memory operand described by the appended EXT0 descriptor."),
                ("Generation", "The EXT0 descriptor selects segment, base, index, and auto-update behavior. The compact EA escape selects only the displacement size."),
                ("Segment", "EXT0 has no implicit segment. Segment-qualified forms encode SEG(s); SP and PC indexed forms use SS and CS; default base-update forms use the operation default data segment."),
                ("Payload", "Payload order is EXT0 descriptor byte or bytes first, then the optional displacement payload selected by the compact EA escape."),
                ("Update", "Only EXT0 forms with ++ or -- update the temporary operand-evaluation image."),
            ],
        ),
    ]


def ext0_reference_blocks() -> list[str]:
    return [
        ea_reference_block(
            "EXT0 Explicit Segment Base",
            [
                ("Assembler syntax", "[SEG(s):Rn(b) + displacement]"),
                ("Descriptor", "0sssbbbb, one byte."),
                ("Generation", "offset = temporary Rn(b) + displacement."),
                ("Segment", "SEG(s) selects CS, DS, SS, or GS0..GS4."),
                ("Payload", "One descriptor byte plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "No auto-update."),
            ],
            diagram=r"\manualeaadditivememoryflow{EXT0 explicit segment base}{BASE REGISTER}{Rn(b)}{optional displacement}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "EXT0 Explicit Segment Indexed",
            [
                ("Assembler syntax", "[SEG(s):Rn(b) + Rn(i) * scale + displacement], [SEG(s):Rn(b) + Rn(i)++ * scale + displacement], [SEG(s):Rn(b) + --Rn(i) * scale + displacement]"),
                ("Descriptor", "1sss0010 bbbbiiii for no update; 1sss0000 bbbbiiii for postincrement index; 1sss0001 bbbbiiii for predecrement index. Two bytes."),
                ("Generation", "offset = temporary Rn(b) + index_term * scale + displacement."),
                ("Segment", "SEG(s) selects CS, DS, SS, or GS0..GS4."),
                ("Scale", "Scale is implicit in the consuming instruction. B/W/L/Q normally imply 1/2/4/8."),
                ("Payload", "Two descriptor bytes plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "Index postincrement uses the current temporary Rn(i), then increments it by one element. Index predecrement decrements temporary Rn(i) by one element before use."),
            ],
            diagram=r"\manualeaindexedmemoryflow{EXT0 explicit segment indexed}{BASE REGISTER}{Rn(b)}{optional displacement}{Rn(i)}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "EXT0 Explicit Segment Zero Base",
            [
                ("Assembler syntax", "[SEG(s):0 + displacement]"),
                ("Descriptor", "1sss0011, one byte."),
                ("Generation", "offset = displacement. Without a displacement payload, offset is 0."),
                ("Segment", "SEG(s) selects CS, DS, SS, or GS0..GS4."),
                ("Payload", "One descriptor byte plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "No auto-update."),
            ],
            diagram=r"\manualeasimplememoryflow{EXT0 zero-base address generation}{ZERO BASE}{0 plus displacement}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "EXT0 Explicit Segment Base Auto-Update",
            [
                ("Assembler syntax", "[SEG(s):Rn(b)++ + displacement], [SEG(s):--Rn(b) + displacement]"),
                ("Descriptor", "1sss1000 bbbb0000 for base postincrement; 1sss1000 bbbb0001 for base predecrement. Two bytes."),
                ("Generation", "offset = base_term + displacement."),
                ("Segment", "SEG(s) selects CS, DS, SS, or GS0..GS4."),
                ("Payload", "Two descriptor bytes plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "Base postincrement uses the current temporary Rn(b), then increments it by the memory access size. Base predecrement decrements temporary Rn(b) by the memory access size before use."),
            ],
            diagram=r"\manualeaadditivememoryflow{EXT0 base auto-update}{BASE REGISTER}{Rn(b) temporary}{optional displacement}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "EXT0 Explicit Segment Zero-Base Indexed",
            [
                ("Assembler syntax", "[SEG(s):0 + Rn(i) * scale + displacement], [SEG(s):0 + Rn(i)++ * scale + displacement], [SEG(s):0 + --Rn(i) * scale + displacement]"),
                ("Descriptor", "1sss1001 0010iiii for no update; 1sss1001 0000iiii for postincrement index; 1sss1001 0001iiii for predecrement index. Two bytes."),
                ("Generation", "offset = index_term * scale + displacement."),
                ("Segment", "SEG(s) selects CS, DS, SS, or GS0..GS4."),
                ("Payload", "Two descriptor bytes plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "Index update follows the same one-element temporary-image rule as other indexed update forms."),
            ],
            diagram=r"\manualeaindexedmemoryflow{EXT0 zero-base indexed}{ZERO BASE}{0}{optional displacement}{Rn(i)}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "EXT0 SP/PC Indexed",
            [
                ("Assembler syntax", "[SP + Rn(i) * scale + displacement], [SP + Rn(i)++ * scale + displacement], [SP + --Rn(i) * scale + displacement], and the matching PC forms."),
                ("Descriptor", "10001010 0010iiii, 0000iiii, or 0001iiii for SP; 10001011 0010iiii, 0000iiii, or 0001iiii for PC. Two bytes."),
                ("Generation", "offset = temporary SP or PC term + index_term * scale + displacement."),
                ("Segment", "SP forms are fixed to SS. PC forms are fixed to CS."),
                ("Payload", "Two descriptor bytes plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "Only the Rn(i) index register may auto-update; SP and PC are not auto-updated by these forms."),
            ],
            diagram=r"\manualeaindexedmemoryflow{EXT0 SP/PC indexed}{SP OR PC}{SP or PC term}{optional displacement}{Rn(i)}{EFFECTIVE ADDRESS}",
        ),
        ea_reference_block(
            "EXT0 Default-Segment Base Auto-Update",
            [
                ("Assembler syntax", "[Rn(b)++ + displacement], [--Rn(b) + displacement]"),
                ("Descriptor", "1bbbb100 for base postincrement; 1bbbb101 for base predecrement. One byte."),
                ("Generation", "offset = base_term + displacement."),
                ("Segment", "Uses the operation default data segment."),
                ("Payload", "One descriptor byte plus the optional displacement selected by the compact EXT0 escape."),
                ("Update", "Postincrement uses the current temporary Rn(b), then increments it by the memory access size. Predecrement decrements temporary Rn(b) by the memory access size before use."),
            ],
            diagram=r"\manualeaadditivememoryflow{EXT0 default-segment base auto-update}{BASE REGISTER}{Rn(b) temporary}{optional displacement}{EFFECTIVE ADDRESS}",
        ),
    ]


def latex_address_translation_pipeline_figure() -> str:
    return r"""
\begin{center}\vspace{3pt}
\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={font=\scriptsize},>=stealth,line width=0.82pt]
\tikzset{box/.style={draw,align=center,minimum height=0.70cm,inner sep=2pt}, lab/.style={fill=white,inner sep=1pt}}
\node[box,minimum width=1.15cm] (ea) at (0.55,0) {EA\\address};
\node[box,minimum width=1.30cm] (sel) at (1.95,0) {select\\segment};
\node[box,minimum width=1.45cm] (check) at (3.65,0) {enabled\\window\\check};
\node[box,minimum width=2.45cm] (add) at (6.10,1.55) {$m\ne0$, $b=0$\\linear = base + EA};
\node[box,minimum width=2.45cm] (keep) at (6.10,0) {$m\ne0$, $b=1$\\linear = EA};
\node[box,minimum width=2.45cm] (disabled) at (6.10,-1.55) {$m=0$\\linear = EA};
\node[box,minimum width=1.45cm] (lin) at (8.45,0) {linear\\address};
\node[box,minimum width=2.00cm] (page) at (10.65,0.95) {PTCR.PE=1\\page-table\\translation};
\node[box,minimum width=2.00cm] (direct) at (10.65,-0.95) {PTCR.PE=0\\use linear\\directly};
\node[box,minimum width=1.75cm] (out) at (12.90,0) {memory-system\\address};
\draw[->] (ea.east) -- (sel.west);
\coordinate (modebranch) at (2.75,0);
\draw (sel.east) -- (modebranch);
\draw[->] (modebranch) -- (check.west);
\draw[->] (modebranch) |- node[lab,pos=0.20,right] {$m=0$} (disabled.west);
\coordinate (segbranch) at (4.55,0);
\draw[->] (check.east) -- (segbranch) |- (add.west);
\draw[->] (check.east) -- (keep.west);
\draw[->] (check.south) -- ++(0,-0.58) node[lab,below] {window fail: PAGE\_FAULT};
\coordinate (linmerge) at (7.45,0);
\draw (add.east) -- ++(0.34,0) |- (linmerge);
\draw (keep.east) -- (linmerge);
\draw (disabled.east) -- ++(0.34,0) |- (linmerge);
\draw[->] (linmerge) -- (lin.west);
\coordinate (pebranch) at (9.45,0);
\draw[->] (lin.east) -- (pebranch) |- (page.west);
\draw[->] (lin.east) -- (pebranch) |- (direct.west);
\draw[->] (page.east) -| (out.north);
\draw[->] (direct.east) -| (out.south);
\end{tikzpicture}
\manualfigurecaption{Address Translation Pipeline}
\end{center}
""".strip()


def latex_architecture_overview_section(model: IsaModel, instructions: list[InstructionDef]) -> str:
    return "\n".join(
        [
            str(LatexTopSection("Overview")),
            render_latex_template("architecture_overview.tex"),
        ]
    )


def latex_overview_section(model: IsaModel, instructions: list[InstructionDef]) -> str:
    allocated = set(model.allocated_by_mnemonic)
    defined = {item.mnemonic for item in model.instructions}
    rows = [
        ["Definition root", str(model.defs_root)],
        ["Allocation root", str(model.alloc_root)],
        ["Instruction definitions", len(instructions)],
        ["Allocated mnemonics", len(allocated)],
        ["Allocated without definition", len(allocated - defined)],
        ["Definitions without allocation", len(defined - allocated)],
    ]
    return "\n".join(
        [
            latex_subsection("Source Summary"),
            latex_table(["Item", "Value"], rows, ["1.75in", "3.65in"], "Reference Source Summary"),
        ]
    )


def latex_terminology_section(model: IsaModel) -> str:
    parts = [str(LatexTopSection("Terminology"))]
    for group in terminology_groups(model):
        rows = []
        for term in group.get("terms", []) or []:
            if isinstance(term, dict):
                rows.append([term.get("term", ""), term.get("definition", "")])
        if rows:
            title = str(group.get("name", "Terms"))
            parts.append(latex_subsection(title))
            parts.append(latex_table(["Term", "Definition"], rows, ["1.35in", "4.05in"], f"{title} Terms"))
    return "\n".join(parts)


def latex_compatibility_section(model: IsaModel) -> str:
    rules = compatibility_rules(model)
    reserved = compat_get(rules, "reserved_bits", default={})
    faults = compat_get(rules, "instruction_encoding_faults", default={})
    canonical = compat_get(rules, "canonical_encodings", default={})
    cpuid = compat_get(rules, "cpuid", default={})

    field_rows = [
        [
            "Architected register reserved bits",
            policy_value_text(compat_get(reserved, "architected_register_bits", "read")),
            policy_value_text(compat_get(reserved, "architected_register_bits", "write")),
            "-",
        ],
        [
            "Control-register reserved bits",
            policy_value_text(compat_get(reserved, "control_register_bits", "read")),
            policy_value_text(compat_get(reserved, "control_register_bits", "write")),
            compat_get(reserved, "control_register_bits", "write_exception"),
        ],
        [
            "Reserved selector values",
            "-",
            "invalid selector",
            compat_get(reserved, "selector_values", "exception"),
        ],
        [
            "Consumed reserved PTE bits",
            "-",
            "invalid translation input",
            compat_get(reserved, "page_table_bits", "consumed_exception"),
        ],
        [
            "Reserved IVT bits",
            "-",
            policy_value_text(compat_get(reserved, "interrupt_vector_table_bits", "write")),
            "-",
        ],
        [
            "Reserved supervisor-frame bits",
            "-",
            policy_value_text(compat_get(reserved, "supervisor_frame_bits", "write")),
            "-",
        ],
    ]
    software_rows = [
        ["Hardware use", policy_value_text(compat_get(reserved, "software_defined_bits", "hardware_use"))],
        ["Software use", policy_value_text(compat_get(reserved, "software_defined_bits", "software_use"))],
    ]
    encoding_rows = [
        ["Reserved instruction opcode", compat_get(faults, "reserved_opcode", "exception")],
        ["Reserved extension opcode", compat_get(faults, "reserved_extension_opcode", "exception")],
        ["Reserved effective-address form", compat_get(faults, "reserved_effective_address_form", "exception")],
        ["Unsupported optional instruction group", compat_get(faults, "unsupported_optional_instruction_group", "exception")],
    ]
    canonical_rows = [
        ["Assembler default", policy_value_text(compat_get(canonical, "assembler_default"))],
        ["Disassembler default", policy_value_text(compat_get(canonical, "disassembler_default"))],
        ["Noncanonical default", compat_get(canonical, "noncanonical_default", "exception")],
        ["Explicit alias or priority rule", "allowed" if compat_get(canonical, "explicit_alias_or_priority", "allowed") else "not allowed"],
    ]
    cpuid_rows = [
        ["Unknown CPUID class", policy_value_text(compat_get(cpuid, "unknown_class", "result"))],
        ["Unknown CPUID leaf", policy_value_text(compat_get(cpuid, "unknown_leaf", "result"))],
        ["Unknown CPUID index", policy_value_text(compat_get(cpuid, "unknown_index", "result"))],
        ["Reserved result bits", policy_value_text(compat_get(cpuid, "reserved_result_bits", "software_action"))],
        ["Privilege", policy_value_text(compat_get(cpuid, "privilege"))],
        ["Serialization", policy_value_text(compat_get(cpuid, "serialization"))],
        ["Runtime mutability", "stable after reset" if compat_get(cpuid, "runtime_mutability", "stable_after_reset") else "may change at runtime"],
    ]
    return "\n".join(
        [
            str(LatexTopSection("Reserved and Compatibility Rules")),
            render_latex_template(
                "compatibility_rules.tex",
                {
                    "TERMINOLOGY_TABLE": latex_table(
                        ["Term", "Meaning"],
                        [
                            ["reserved", "Held for a future architectural definition. Software must not depend on its current value or behavior."],
                            ["must be zero", "Software writes zero. A nonzero value is invalid unless a later architectural revision assigns the field."],
                            ["read as zero", "Reads of the field return zero; software still treats the field as reserved."],
                            ["ignored", "Hardware accepts the field but does not use it for the current operation."],
                            ["software-defined", "Hardware does not interpret the field and reserves it for software use."],
                            ["illegal", "Use of a disallowed opcode, EA form, selector, or operation raises the named exception."],
                        ],
                        ["1.25in", "4.15in"],
                        "Compatibility Terms",
                        listed=False,
                    ),
                    "RESERVED_FIELD_TABLE": latex_code_table(
                        ["Field Class", "Read Rule", "Write or Use Rule", "Fault"],
                        field_rows,
                        ["1.65in", "0.75in", "1.35in", "1.65in"],
                        "Reserved Field Defaults",
                        {3},
                        listed=False,
                    ),
                    "SOFTWARE_DEFINED_TABLE": latex_table(
                        ["Software-Defined Field Rule", "Value"],
                        software_rows,
                        ["1.75in", "3.65in"],
                        "Software-Defined Field Defaults",
                        listed=False,
                    ),
                    "RESERVED_ENCODING_TABLE": latex_code_table(
                        ["Encoding Class", "Fault"],
                        encoding_rows,
                        ["3.55in", "1.85in"],
                        "Reserved Encoding Faults",
                        {1},
                        listed=False,
                    ),
                    "CANONICAL_DEFAULTS_TABLE": latex_code_table(
                        ["Canonical Encoding Rule", "Value"],
                        canonical_rows,
                        ["2.15in", "3.25in"],
                        "Canonical Encoding Defaults",
                        {1},
                        listed=False,
                    ),
                    "CPUID_DEFAULTS_TABLE": latex_table(
                        ["CPUID Case", "Rule"],
                        cpuid_rows,
                        ["2.10in", "3.30in"],
                        "CPUID Compatibility Defaults",
                        listed=False,
                    ),
                },
            ),
        ]
    )


def latex_cpuid_feature_discovery_section(model: IsaModel) -> str:
    cpuid = compat_get(compatibility_rules(model), "cpuid", default={})
    selector_rows = [
        ["0..15", "index", "result index within the selected leaf"],
        ["16..31", "leaf", "information leaf within the selected class"],
        ["32..63", "class", "CPUID information class"],
    ]
    policy_rows = [
        ["Bedrock base ISA", "0x00000000", "base profile identity, instruction length limits, integer register model, condition-code model, and mandatory base instruction groups"],
        ["optional extensions", "0x00000001", "optional architectural groups such as floating-point, transcendental floating-point, and virtualization acceleration"],
        ["implementation properties", "0x00000002", "program-visible implementation limits, topology, and SAVE/RESTORE area layout"],
    ]
    leaf_rows = [
        ["0x00000000", "0x0000", "BASE_IDENTITY", "0..2", "base profile, architectural revision, vendor string, and maximum standard leaf"],
        ["0x00000000", "0x0001", "BASE_LIMITS", "0", "word size, maximum instruction bytes, opcode class model, and Rn register count"],
        ["0x00000001", "0x0000", "EXTENSION_DIRECTORY", "0", "availability bits for optional architectural extension groups"],
        ["0x00000002", "0x0000", "EXECUTION_PROPERTIES", "0", "program-visible execution properties such as out-of-order capability"],
        ["0x00000002", "0x0001", "TOPOLOGY", "indexed", "hardware-thread topology and current hardware-thread identity"],
        ["0x00000002", "0x0004", "SAVE_AREA_LAYOUT", "0..n", "SAVE/RESTORE maximum size, header size, component count, bitmap size, and component descriptors"],
    ]
    bit_rows = [
        ["Feature bit", "Meaning"],
        ["FP", "base floating-point instruction group is present"],
        ["FPTRANS", "transcendental floating-point instruction group is present"],
        ["VIRTACCEL", "virtualization acceleration instruction group is present"],
        ["SAVE_AREA_SIZE", "maximum bytes required for a CPUID-defined SAVE area"],
        ["COMPONENT_OFFSET", "64-byte-aligned offset of an extension state component"],
    ]
    return "\n".join(
        [
            str(LatexTopSection("CPUID Feature Discovery")),
            render_latex_template(
                "cpuid_feature_discovery.tex",
                {
                    "CPUID_INSTRUCTION_TABLE": latex_code_table(
                        ["Instruction", "Summary"],
                        instruction_brief_rows(model, ["CPUID"]),
                        ["0.85in", "4.55in"],
                        "CPUID Instruction",
                        {0},
                        listed=False,
                    ),
                    "SELECTOR_TABLE": latex_code_table(
                        ["Bits", "Field", "Meaning"],
                        selector_rows,
                        ["0.65in", "0.85in", "3.90in"],
                        "CPUID Query Selector",
                        {0, 1},
                        listed=False,
                    ),
                    "QUERY_DEFAULTS_TABLE": latex_table(
                        ["Query Case", "Result"],
                        [
                            ["Unknown class", policy_value_text(compat_get(cpuid, "unknown_class", "result"))],
                            ["Unknown leaf", policy_value_text(compat_get(cpuid, "unknown_leaf", "result"))],
                            ["Unknown index", policy_value_text(compat_get(cpuid, "unknown_index", "result"))],
                            ["Reserved result bits", policy_value_text(compat_get(cpuid, "reserved_result_bits", "software_action"))],
                        ],
                        ["1.35in", "4.05in"],
                        "CPUID Query Defaults",
                        listed=False,
                    ),
                    "POLICY_TABLE": latex_table(
                        ["Policy", "Class", "Meaning"],
                        policy_rows,
                        ["1.25in", "1.10in", "3.05in"],
                        "CPUID Discovery Policy",
                        listed=False,
                    ),
                    "LEAF_TABLE": latex_code_table(
                        ["Class", "Leaf", "Name", "Indexes", "Summary"],
                        leaf_rows,
                        ["0.82in", "0.62in", "1.35in", "0.70in", "1.90in"],
                        "CPUID Leaf Directory",
                        {0, 1, 2, 3},
                        style="dense",
                        listed=False,
                    ),
                    "BIT_FIELD_TABLE": latex_table(
                        ["Field", "Meaning"],
                        bit_rows[1:],
                        ["1.35in", "4.05in"],
                        "Representative CPUID Result Fields",
                        listed=False,
                    ),
                },
            ),
        ]
    )


def latex_save_restore_section(model: IsaModel) -> str:
    save = instruction_by_mnemonic(model, "SAVE")
    restore = instruction_by_mnemonic(model, "RESTORE")
    rows = [
        ["Header", "base save-area metadata and state-block bitmap"],
        ["General registers", "R0 through R15"],
        ["Segment validity", "GS validity bits and implemented segment state"],
        ["Integer status", "FLAGS and STATUS subject to privilege restore rules"],
        ["Extension state", "CPUID-defined 64-byte-aligned component slots"],
    ]
    instruction_rows = []
    for inst in (save, restore):
        if inst is not None:
            instruction_rows.append([inst.mnemonic, inst.doc.get("summary", inst.mnemonic)])
    return "\n".join(
        [
            str(LatexTopSection("SAVE/RESTORE Processor-State Save Area")),
            render_latex_template(
                "save_restore_area.tex",
                {
                    "SAVE_AREA_DIAGRAM": latex_save_area_diagram(),
                    "SAVE_RESTORE_INSTRUCTION_TABLE": latex_code_table(
                        ["Instruction", "Summary"],
                        instruction_rows,
                        ["0.85in", "4.55in"],
                        "SAVE/RESTORE Instructions",
                        {0},
                        listed=False,
                    ),
                    "SAVE_AREA_COMPONENT_TABLE": latex_table(
                        ["Area", "Contents"],
                        rows,
                        ["1.35in", "4.05in"],
                        "Processor-State Save Area Components",
                        listed=False,
                    ),
                    "SAVE_RESTORE_RULE_TABLE": latex_table(
                        ["Rule", "Value"],
                        [
                            ["Base alignment", "SAVE-area base address is 4 KiB aligned."],
                            ["Fixed base block", "Contains header, state-block bitmap, R0-R15, optional GS images, FLAGS, and STATUS."],
                            ["GS validity", "GS_VALID bits identify which GS0..GS4 segment images are valid in the fixed block."],
                            ["Extension slots", "Component offsets and maximum size are discovered through CPUID SAVE_AREA_LAYOUT leaves."],
                            ["Clean extension state", "SAVE may skip architecturally clean extension blocks and report them clear in the state-block bitmap."],
                            ["Restore privilege", "User-mode RESTORE ignores supervisor-only STATUS state; supervisor RESTORE applies STATUS write validation."],
                        ],
                        ["1.35in", "4.05in"],
                        "SAVE/RESTORE Image Rules",
                        listed=False,
                    ),
                },
            ),
        ]
    )


def latex_data_formats_section(model: IsaModel) -> str:
    schema = operand_schema(model)
    immediate_rows = []
    for name, spec in sorted((schema.get("immediate_operands") or {}).items()):
        if not isinstance(spec, dict):
            continue
        rng = spec.get("range", "-")
        if isinstance(rng, list) and len(rng) == 2:
            rng = f"{rng[0]}..{rng[1]}"
        immediate_rows.append(
            [
                name,
                spec.get("width", ""),
                "signed" if spec.get("signed") else "unsigned",
                rng,
                spec.get("operation_size_extension", ""),
                spec.get("applies_when", ""),
            ]
        )
    immediate_operand_table = ""
    if immediate_rows:
        immediate_operand_table = latex_code_table(
                ["Operand", "Bits", "Value", "Range", "Extension", "Applies When"],
                immediate_rows,
                ["0.65in", "0.38in", "0.62in", "0.62in", "0.90in", "2.00in"],
                "Immediate Operand Interpretation",
                {0},
                style="dense",
        )
    return "\n".join(
        [
            str(LatexTopSection("Data Formats")),
            render_latex_template(
                "data_formats.tex",
                {
                    "INTEGER_SIZE_TABLE": latex_code_table(
                        ["Code", "Suffix", "Bits", "Bytes", "Name"],
                        size_code_rows(model),
                        ["0.45in", "0.55in", "0.45in", "0.50in", "1.55in"],
                        "Scalar Data Sizes",
                        {0, 1},
                    ),
                    "INTEGER_REGISTER_SUBFIELD_DIAGRAM": latex_integer_register_subfield_diagram(),
                    "BYTE_ORDER_DIAGRAMS": latex_data_byte_order_diagrams(),
                    "PAYLOAD_ORDER_TABLE": latex_code_table(
                        ["Payload", "Bytes", "Memory Order"],
                        [
                            ["imm8", 1, "single byte"],
                            ["imm16", 2, "bits 7..0 at the lower byte, bits 15..8 at the next byte"],
                            ["imm32", 4, "least significant byte first"],
                            ["imm64", 8, "least significant byte first"],
                            ["disp8", 1, "single signed two's-complement byte"],
                            ["disp16", 2, "signed two's-complement value, little-endian"],
                            ["disp32", 4, "signed two's-complement value, least significant byte first"],
                            ["disp64", 8, "declared-width displacement payload, least significant byte first"],
                            ["abs32", 4, "absolute-address payload, least significant byte first"],
                            ["abs64", 8, "absolute-address payload, least significant byte first"],
                        ],
                        ["0.75in", "0.45in", "4.20in"],
                        "Immediate, Displacement, and Address Payload Order",
                        {0},
                        style="dense",
                    ),
                    "IMMEDIATE_OPERAND_TABLE": immediate_operand_table,
                },
            ),
        ]
    )


def latex_instruction_word_formats_section(model: IsaModel) -> str:
    bit_diagram = r"""
\begin{manuallistedbitdiagram}{Instruction Header Byte Formats}
\manualbitrow{extrashort byte}{%
\manualbitfieldcode{0}{1}
\manualbitfieldtext{payload[6:0]}{7}
}
\manualbitfieldrow{short bytes}{%
\manualbytepairlabels
}{%
\manualbitfieldcode{10}{2}
\manualbitfieldtext{payload[13:8]}{6}
\manualbitgap{1}
\manualbitfieldtext{payload[7:0]}{8}
}
\manualbitfieldrow{extended start bytes}{%
\manualbytepairlabels
}{%
\manualbitfieldcode{11}{2}
\manualbitfieldtext{L}{4}
\manualbitfieldtext{opcode high}{2}
\manualbitgap{1}
\manualbitfieldtext{opcode next}{8}
}
\end{manuallistedbitdiagram}
""".strip()
    field_rows = [
        ["byte 0 bit 7", "class", "0 selects a one-byte extrashort instruction with payload in byte0[6:0]."],
        ["byte 0 bits 7..6", "class", "10 selects a two-byte short instruction; 11 selects an extended instruction."],
        ["byte 0 bits 5..2", "L / payload", "For short, payload[13:10]. For extended, L encodes total instruction bytes as 3+L."],
        ["byte 0 bits 1..0", "opcode", "For short, payload[9:8]. For extended, the first two opcode-stream bits."],
        ["byte 1 bits 7..0", "opcode", "For short, payload[7:0]. For extended, the next eight opcode-stream bits."],
    ]
    return "\n".join(
        [
            str(LatexTopSection("Instruction Header Formats")),
            render_latex_template(
                "instruction_word_formats.tex",
                {
                    "WORD0_BIT_DIAGRAM": bit_diagram,
                    "WORD0_FIELD_TABLE": latex_table(["Bits", "Field", "Meaning"], field_rows, ["1.05in", "0.75in", "3.60in"], "Instruction Header Fields"),
                    "INSTRUCTION_ENCODING_DIAGRAMS": latex_instruction_encoding_diagrams(),
                    "SIZE_DECODING_TABLE": latex_code_table(
                        ["Byte 0 Pattern", "Byte 1 Pattern", "Bytes"],
                        size_decoding_rows(),
                        ["1.25in", "1.25in", "0.55in"],
                        "Instruction Length Truth Table",
                        {0, 1},
                        style="dense",
                    ),
                    "OPCODE_LENGTH_TABLE": latex_code_table(
                        ["Opcode Selector", "Class", "Opcode Bytes", "Validity"],
                        opcode_length_rows(),
                        ["0.95in", "0.80in", "0.75in", "2.90in"],
                        "Opcode Length Truth Table",
                        {0, 1},
                        style="dense",
                    ),
                    "ENCODING_CLASS_TABLE": latex_table(
                        ["Class", "Payload Bits", "Selection"],
                        encoding_class_rows(model),
                        ["0.72in", "0.75in", "3.20in"],
                        "Encoding Class Summary",
                        style="dense",
                    ),
                },
            ),
        ]
    )


def latex_register_section(model: IsaModel) -> str:
    data = model.metadata.get("registers") or {}
    reg_rows = [
        [reg.get("name", ""), bits_text(reg.get("encoding", ""), 4), reg.get("width", "")]
        for reg in data.get("general_registers", []) or []
    ]
    special_rows = [
        [reg.get("name", ""), reg.get("width", ""), reg.get("fixed_segment", ""), bits_text(reg.get("ea_encoding", ""), 7)]
        for reg in data.get("special_registers", []) or []
    ]
    segment_data = model.metadata.get("segments") or {}
    segment_rows = [
        [reg.get("name", ""), reg.get("selector", ""), reg.get("width", "")]
        for reg in segment_data.get("segment_registers", []) or []
    ]
    fpu_rows = [[f"F{index}", "64"] for index in range(16)]
    segment_operand_rows = [
        ["CS", "000", "code segment; default for instruction fetch and PC-relative forms"],
        ["DS", "001", "default data segment"],
        ["SS", "010", "stack segment; fixed for SP-relative forms"],
        ["GS0", "011", "TLS context in the ELF and C ABIs"],
        ["GS1", "100", "general segment 1"],
        ["GS2", "101", "general segment 2"],
        ["GS3", "110", "general segment 3"],
        ["GS4", "111", "volatile far-data window in bedrock-c-far; otherwise target-specific"],
    ]
    control_rows = [
        ["PTCR", "page-table control and root"],
        ["ASCR", "address-space control"],
        ["ICR", "interrupt control"],
        ["SPC", "saved program counter"],
        ["SCS", "saved code segment"],
        ["SDS", "saved data segment"],
        ["PMC", "performance-monitor control"],
    ]
    return "\n".join(
        [
            str(LatexTopSection("Programming Model")),
            render_latex_template(
                "register_model.tex",
                {
                    "RN_REGISTER_MODEL_FIGURE": latex_rn_register_model_figure(),
                    "GENERAL_REGISTER_TABLE": latex_code_table(
                        ["Register", "Encoding", "Width"],
                        reg_rows,
                        ["1.15in", "1.10in", "0.75in"],
                        "General Register Encoding",
                        {0, 1},
                    ),
                    "STATE_REGISTER_FORMAT_DIAGRAMS": latex_state_register_format_diagrams(),
                    "FLOATING_POINT_REGISTER_TABLE": latex_code_table(
                        ["Register", "Width"],
                        fpu_rows,
                        ["0.85in", "0.75in"],
                        "Floating-Point Registers",
                        {0},
                        style="dense",
                    ),
                    "SEGMENT_REGISTER_FORMAT_DIAGRAM": latex_segment_register_format_diagram(),
                    "SEGMENT_REGISTER_TABLE": latex_code_table(
                        ["Segment", "Selector", "Width"],
                        segment_rows,
                        ["0.85in", "1.10in", "0.75in"],
                        "Segment Registers",
                        {0},
                    ),
                    "SEGMENT_REGISTER_OPERAND_TABLE": latex_code_table(
                        ["SREG", "Bits", "Use"],
                        segment_operand_rows,
                        ["0.60in", "0.50in", "4.30in"],
                        "Segment Register Operand Encoding",
                        {0, 1},
                    ),
                    "SPECIAL_REGISTER_TABLE": latex_code_table(
                        ["Special", "Width", "Fixed Segment", "EA Encoding"],
                        special_rows,
                        ["0.85in", "0.75in", "1.15in", "1.25in"],
                        "Special Registers",
                        {0, 2, 3},
                    ),
                    "CONTROL_REGISTER_TABLE": latex_table(
                        ["Register", "Purpose"],
                        control_rows,
                        ["0.85in", "4.55in"],
                        "Control Register Namespace",
                    ),
                },
            ),
        ]
    )


def latex_condition_section(model: IsaModel) -> str:
    data = model.metadata.get("conditions") or {}
    rows = []
    for cond in data.get("conditions", []) or []:
        aliases = ", ".join(str(item) for item in cond.get("aliases", []) or [])
        rows.append([bits_text(cond.get("value", ""), 4), cond.get("name", ""), aliases or "-", cond.get("expression", "")])
    return "\n".join(
        [
            str(LatexTopSection("Condition Codes")),
            render_latex_template(
                "condition_codes.tex",
                {
                    "CONDITION_TABLE": latex_code_table(
                        ["Bits", "Name", "Aliases", "Expression"],
                        rows,
                        ["0.65in", "0.55in", "0.85in", "3.0in"],
                        "Condition Code Encoding",
                        {0, 1, 2},
                    ),
                },
            ),
        ]
    )


def latex_condition_computation_section(model: IsaModel) -> str:
    return "\n".join(
        [
            str(LatexTopSection("Condition Code Computation")),
            render_latex_template(
                "condition_code_computation.tex",
                {
                    "FLAG_MEANING_TABLE": latex_table(
                        ["Bit", "Name", "Meaning"],
                        [
                            ["Z", "zero", "Set when the result value is zero."],
                            ["N", "negative", "Set from the most significant bit of the result at the operand size."],
                            ["C", "carry/borrow", "Set on unsigned carry out for addition, or unsigned borrow for subtraction."],
                            ["V", "overflow", "Set on signed overflow, or by instructions that explicitly report exceptional conditions through V."],
                        ],
                        ["0.45in", "1.05in", "3.90in"],
                        "Integer Condition-Code Bits",
                    ),
                    "INTEGER_FLAG_RULE_TABLE": latex_table(
                        ["Operation Class", "FLAGS Result"],
                        [
                            ["ADD, SUB, AND, OR, XOR", "Leave FLAGS unchanged."],
                            ["ADC, SBB", "Read C as carry/borrow input and update Z, N, C, and V from the stored result."],
                            ["CMP, TEST", "Update Z, N, C, and V from the temporary result and do not store that result."],
                            ["CMPJcc, TESTJcc", "Compute temporary condition flags for the branch decision and leave architectural FLAGS unchanged."],
                            ["INC, DEC", "Leave FLAGS unchanged."],
                            ["INCF, DECF", "Update Z, N, C, and V from the stored increment/decrement result."],
                            ["SETF, CLRF", "Set or clear selected FLAGS bits from the imm4 mask; unselected FLAGS bits are preserved."],
                            ["NEG, ABS", "Leave FLAGS unchanged."],
                            ["CLR", "Writes zero and leaves FLAGS unchanged."],
                            ["Bounds checks", "Set V when the value is outside the selected interval; Z, N, and C are unchanged."],
                        ],
                        ["1.30in", "4.10in"],
                        "Common Integer Flag Computation",
                    ),
                    "SHIFT_COUNT_RULE_TABLE": latex_table(
                        ["Operation", "Count Rule"],
                        [
                            ["SHL, SHR, SAR", "The count is not reduced modulo the operand width. Oversized counts have defined zero or sign-fill behavior."],
                            ["ROL, ROR", "The effective count is count modulo the operand width. Effective count zero leaves the destination and FLAGS unchanged."],
                        ],
                        ["1.30in", "4.10in"],
                        "Shift and Rotate Count Rules",
                    ),
                    "SHIFT_FLAG_RULE_TABLE": latex_table(
                        ["Operation", "FLAGS Result for Nonzero Effective Count"],
                        [
                            ["SHL", "Z and N come from the result. C is the last bit shifted out. V reports signed multiplication overflow."],
                            ["SHR", "Z and N come from the result. C is the last bit shifted out. V is cleared."],
                            ["SAR", "Z and N come from the result. C is the last bit shifted out, or the original sign bit for oversized counts. V is cleared."],
                            ["ROL", "Z and N come from the result. C is the least significant result bit. V is cleared."],
                            ["ROR", "Z and N come from the result. C is the most significant result bit. V is cleared."],
                        ],
                        ["0.75in", "4.65in"],
                        "Shift and Rotate Flag Computation",
                    ),
                },
            ),
        ]
    )


def latex_ea_section(model: IsaModel) -> str:
    data = model.metadata.get("ea") or {}
    compact_rows = [
        [form.get("bits", ""), form.get("syntax", form.get("class", "")), form.get("class", ""), display_text(form.get("memory", ""))]
        for form in data.get("compact_ea", []) or []
    ]
    ext_rows = [
        [
            form.get("bits", ""),
            form.get("syntax", ""),
            form.get("base", ""),
            form.get("index", ""),
            form.get("segment", form.get("fixed_segment", "")),
        ]
        for form in ((data.get("ext0") or {}).get("forms", []) or [])
    ]
    ext0_section = ""
    if ext_rows:
        ext0_section = render_latex_template(
            "ext0_addressing_modes.tex",
            {
                "EXT0_REFERENCE_BLOCKS": "\n".join(ext0_reference_blocks()),
                "EXT0_TABLE": latex_code_table(
                    ["Bits", "Syntax", "Base", "Index", "Segment"],
                    ext_rows,
                    ["1.30in", "2.15in", "0.55in", "0.55in", "0.75in"],
                    "EXT0 Encoding",
                    {0, 1},
                    style="dense",
                ),
            },
        )
    auto = data.get("auto_update_semantics") or {}
    auto_update_section = ""
    if auto:
        examples = auto.get("same_register_examples") or []
        example_rows = [[item.get("syntax", ""), compact_clause_text(item.get("meaning", ""))] for item in examples if isinstance(item, dict)]
        example_table = ""
        if example_rows:
            example_table = latex_code_table(
                    ["Syntax", "Meaning"],
                    example_rows,
                    ["1.45in", "3.95in"],
                    "Auto-Update Same-Register Examples",
                    {0},
            )
        auto_update_section = render_latex_template(
            "ea_auto_update_semantics.tex",
            {
                "AUTO_UPDATE_ORDER_TABLE": latex_table(
                    ["Step", "Rule"],
                    [[index + 1, compact_text(item)] for index, item in enumerate(auto.get("evaluation_model", []) or [])],
                    ["0.35in", "5.05in"],
                    "EA Auto-Update Evaluation Order",
                ),
                "AUTO_UPDATE_DELTA_TABLE": latex_table(
                    ["Mode", "Meaning"],
                    [
                        ["postincrement", compact_text(((auto.get("modes") or {}).get("postincrement", "")))],
                        ["predecrement", compact_text(((auto.get("modes") or {}).get("predecrement", "")))],
                        ["base update delta", compact_text(((auto.get("deltas") or {}).get("base_update", "")))],
                        ["index update delta", compact_text(((auto.get("deltas") or {}).get("index_update", "")))],
                        ["REP interaction", compact_text(auto.get("rep_interaction", ""))],
                    ],
                    ["1.30in", "4.10in"],
                    "EA Auto-Update Delta Rules",
                ),
                "AUTO_UPDATE_EXAMPLE_TABLE": example_table,
            },
        )
    return "\n".join(
        [
            str(LatexTopSection("Effective Addressing Modes")),
            render_latex_template(
                "effective_address_modes.tex",
                {
                    "COMPACT_EA_REFERENCE_BLOCKS": "\n".join(compact_ea_reference_blocks()),
                    "COMPACT_EA_TABLE": latex_code_table(
                        ["Bits", "Syntax", "Class", "Memory"],
                        compact_rows,
                        ["1.10in", "2.30in", "1.0in", "0.6in"],
                        "Compact EA Encoding",
                        {0, 1},
                    ),
                    "EA_FIELD_DIAGRAMS": latex_ea_field_diagrams(),
                    "EA_PAYLOAD_CATALOG_TABLE": latex_table(
                        ["Payload", "Bytes", "Value", "Use"],
                        ea_payload_catalog_rows(),
                        ["0.95in", "0.45in", "0.70in", "3.30in"],
                        "EA Payload Names",
                        style="dense",
                    ),
                    "EA_PAYLOAD_SEQUENCE_TABLE": latex_table(
                        ["Case", "Payload Sequence"],
                        [
                            ["Compact displacement", "EA field, then displacement payload at the operand payload position."],
                            ["Compact absolute", "EA field, then absolute-address payload at the operand payload position."],
                            ["Compact immediate", "EA field, then immediate payload at the operand payload position."],
                            ["EXT0 without displacement", "EA field 1110100, then one or two EXT0 descriptor bytes."],
                            ["EXT0 with displacement", "EA field 1110000..1110011, then EXT0 descriptor byte or bytes, then the selected displacement payload."],
                            ["Multiple EA operands", "Repeat the appropriate payload sequence for each EA operand in instruction operand order."],
                        ],
                        ["1.35in", "4.05in"],
                        "EA Payload Sequence Rules",
                    ),
                    "EXT0_SECTION": ext0_section,
                    "AUTO_UPDATE_SECTION": auto_update_section,
                },
            ),
        ]
    )


def latex_execution_model_section(model: IsaModel) -> str:
    rules = (model.metadata.get("semantics") or {}).get("encoding_rules") or {}
    rows = [
        ["Instruction boundary", "The instruction header length selects the full instruction record; later payloads never extend it implicitly."],
        ["Overlong encoding", display_text(((rules.get("instruction_length") or {}).get("overlong_encoding") or {}).get("payload", ""))],
        ["Undersized encoding", display_text(((rules.get("instruction_length") or {}).get("undersized_encoding") or {}).get("rule", ""))],
        ["Default memory operands", display_text((rules.get("memory_operands") or {}).get("default", ""))],
        ["Memory-memory exceptions", compact_text((rules.get("memory_operands") or {}).get("memory_memory_allowed_for", ""))],
        ["Repeat instructions", compact_text((rules.get("repeat_instructions") or {}).get("members", ""))],
    ]
    execution_defaults_table = latex_table(
        ["Topic", "Spec Value"],
        [
            ["Overlong encoding", "allowed when the selected instruction form defines unused trailing payload bytes"],
            ["Undersized encoding", "length/decode fault before architectural state is changed"],
            ["Memory-memory operands", "operation opt-in only"],
            ["Unmentioned FLAGS/FFLAGS", "unchanged"],
            ["Operand evaluation order", "instruction operand order"],
            ["Instruction commit", "single commit point unless the instruction explicitly defines partial completion"],
        ],
        ["1.55in", "3.85in"],
        "Execution Defaults",
    )
    mnemonic_suffix_table = latex_table(
        ["Rule", "Value"],
        [
            ["Size suffix placement", "mnemonic suffix"],
            ["Integer suffixes", "B, W, L, Q"],
            ["Floating suffixes", "S, D where the floating-point group defines them"],
            ["Conditional suffix users", "CMPJcc, DJcc, IJcc, Jcc, MOVcc, SETcc, TESTJcc, FMOVcc"],
            ["Single-size mnemonics", "omit the suffix when the form has only one architectural size"],
        ],
        ["1.45in", "3.95in"],
        "Mnemonic Suffix Rules",
    )
    semantic_notation_table = latex_table(
        ["Term", "Meaning"],
        [
            ["Operand Read", "read operand value after applying its addressing mode and operation size"],
            ["Operand Write", "write the selected-size result to the destination; sub-Q Rn writes preserve upper bits unless the instruction defines another upper-bit rule"],
            ["EA Address", "compute an effective address without reading memory unless the operation needs the memory value"],
            ["Selector", "selector operands may name an Rn register, a segment register, or an encoded immediate selector"],
            ["Overlong", "extra trailing instruction payload bytes are ignored only when the form explicitly permits them"],
            ["FLAGS ZNCV", "integer flags Z, N, C, and V"],
            ["FFLAGS", "floating-point accrued exception/status bits"],
        ],
        ["1.35in", "4.05in"],
        "Semantic Notation",
    )
    shared_side_effect_table = latex_table(
        ["Family", "Common Rule"],
        [
            ["Integer ALU", "ordinary forms use at most one memory operand unless a memory-memory form is explicitly encoded"],
            ["Compare/Test", "may read two operands and update FLAGS without storing the temporary result"],
            ["Extension", "EXTS/EXTZ may be used as register, register-memory, memory-register, or encoded memory-memory conversion forms; FLAGS are unchanged unless a repeat rule observes a value"],
            ["Data Movement", "MOV, LEA, and segment-address forms preserve FLAGS unless the instruction definition states otherwise"],
            ["Control Transfer", "PC/CS changes occur at a single control-transfer commit point"],
            ["Atomics", "naturally aligned addressable memory operand is required; the read-modify-write has one architectural commit point"],
            ["TLB and Context", "translation-cache, page-table context, and privileged control instructions require supervisor privilege"],
            ["Cache", "cache maintenance instructions preserve FLAGS and define their own visibility requirements"],
            ["Floating-Point Transcendental", "available only when the corresponding CPUID feature bit reports support"],
        ],
        ["1.35in", "4.05in"],
        "Shared Side-Effect Families",
    )
    return "\n".join(
        [
            str(LatexTopSection("Instruction Execution Model")),
            render_latex_template(
                "execution_model.tex",
                {
                    "EXECUTION_DEFAULTS_TABLE": execution_defaults_table,
                    "INSTRUCTION_BOUNDARY_TABLE": latex_table(["Rule", "Meaning"], rows[:3], ["1.65in", "3.75in"], "Instruction Boundary Rules"),
                    "OPERAND_DEFAULTS_TABLE": latex_table(["Rule", "Meaning"], rows[3:], ["1.65in", "3.75in"], "Operand Evaluation Defaults"),
                    "MNEMONIC_SUFFIX_TABLE": mnemonic_suffix_table,
                    "SEMANTIC_NOTATION_TABLE": semantic_notation_table,
                    "SHARED_SIDE_EFFECT_TABLE": shared_side_effect_table,
                },
            ),
        ]
    )


def latex_streaming_model_section(model: IsaModel) -> str:
    repeat_syntax_table = latex_table(
        ["Form", "Syntax"],
        repeat_syntax_rows(model),
        ["1.05in", "4.35in"],
        "Repeat Instruction Syntax",
    )
    repeatable_class_table = latex_table(
        ["Context", "Meaning"],
        repeatable_class_rows(model),
        ["0.85in", "4.55in"],
        "Repeatability Contexts",
    )
    repeat_body_entry_table = latex_table(
        ["Rule", "Meaning"],
        repeat_body_entry_rows(model),
        ["1.65in", "3.75in"],
        "Repeat Body Entry Rules",
    )
    repeat_counter_table = latex_table(
        ["Rule", "Meaning"],
        repeat_counter_rows(model),
        ["1.65in", "3.75in"],
        "Repeat Counter and Condition Rules",
    )
    repeat_legality_table = latex_table(
        ["Rule", "Meaning"],
        repeat_legality_rows(model),
        ["1.65in", "3.75in"],
        "Repeat Legality, PC, and Debug Rules",
    )
    streaming_candidate_table = latex_table(
        ["Candidate", "Typical Shape"],
        [
            ["copy/fill", "REPG over MOV from one Rn-stepped stream to another; REPGF may be used as an assembler-checked spelling"],
            ["scan/compare", "REPG over TEST or CMP where the grouped body handles termination"],
            ["bulk extension", "REPG over EXTS/EXTZ with source and destination auto-update"],
            ["cache maintenance", "REPG over regular cache-line traversal where the instruction definition permits repetition"],
            ["fixed instruction group", "REPG group whose byte count ends on an instruction boundary and whose body is straight-line"],
        ],
        ["1.35in", "4.05in"],
        "Streaming Candidate Shapes",
    )
    repeat_restart_table = latex_table(
        ["Property", "single-instruction repeat", "REPG"],
        [
            ["Body decode", "body instruction decoded once when repeat state is entered", "group body decoded once when repeat state is entered"],
            ["Zero counter", "body checked, then annulled with no side effects", "group checked, then annulled with no side effects"],
            ["Body", "one following instruction", "encoded byte-counted instruction group"],
            ["Counter update", "after a completed condition-true iteration", "after the whole group iteration succeeds"],
            ["Terminating fault", "reported at the repeated scalar instruction", "reported at the faulting instruction inside the current group iteration"],
            ["Completed work", "completed iterations remain committed", "completed iterations and completed prior group instructions remain committed"],
        ],
        ["1.15in", "2.10in", "2.15in"],
        "Repeat Restart Properties",
    )
    return "\n".join(
        [
            str(LatexTopSection("Streaming Execution Model")),
            render_latex_template(
                "streaming_execution_model.tex",
                {
                    "REPEAT_SYNTAX_TABLE": repeat_syntax_table,
                    "REPEATABLE_CLASS_TABLE": repeatable_class_table,
                    "REPEAT_BODY_ENTRY_TABLE": repeat_body_entry_table,
                    "REPEAT_COUNTER_TABLE": repeat_counter_table,
                    "REPEAT_LEGALITY_TABLE": repeat_legality_table,
                    "STREAMING_CANDIDATE_TABLE": streaming_candidate_table,
                    "REPEAT_RESTART_TABLE": repeat_restart_table,
                },
            ),
        ]
    )


def latex_memory_translation_section(model: IsaModel) -> str:
    composition_rows = [
        ["Effective address", "address generated by the selected EA form"],
        ["Segment image", "base = base_page * 4096; span = (m << e) * 4096; limit = base + span, checked before 64-bit truncation"],
        ["Segment pre-translation", "disabled segments pass the address through; enabled segments check a byte-addressed window with page-granular base and span"],
        ["Linear address", "segment output, or the EA directly when segmentation is disabled"],
        ["Paging enabled", "walk page tables from PTCR.root_page and apply PTE attributes"],
        ["Paging disabled", "use the linear address directly as the memory-system address"],
        ["Faults", "invalid segment images raise INVALID_CONTROL_STATE on write; bounds and canonical-address failures raise PAGE_FAULT"],
    ]
    segment_rows = [
        ["disabled", "m = 0", "no segment-window check", "linear = EA"],
        ["translated window", "m != 0, b = 0", "0 <= EA < span", "linear = base + EA"],
        ["bounds-only window", "m != 0, b = 1", "base <= EA < limit", "linear = EA"],
    ]
    return "\n".join(
        [
            str(LatexTopSection("Memory Address Translation")),
            render_latex_template(
                "memory_address_translation.tex",
                {
                    "ADDRESS_TRANSLATION_PIPELINE_FIGURE": latex_address_translation_pipeline_figure(),
                    "ADDRESS_TRANSLATION_STAGE_TABLE": latex_table(["Stage", "Result"], composition_rows, ["1.55in", "3.85in"], "Address Translation Stages"),
                    "SEGMENT_PRETRANSLATION_TABLE": latex_table(
                        ["Mode", "Segment State", "Check", "Linear Address"],
                        segment_rows,
                        ["1.05in", "1.15in", "1.55in", "1.65in"],
                        "Segment Pre-Translation Modes",
                    ),
                },
            ),
        ]
    )


def latex_memory_model_section(model: IsaModel) -> str:
    return "\n".join(
        [
            str(LatexTopSection("Memory Model")),
            render_latex_template(
                "memory_model.tex",
                {
                    "SCALAR_ACCESS_TABLE": latex_table(
                        ["Suffix", "Bytes", "Natural Alignment", "Tear-Free Guarantee"],
                        [
                            ["B", 1, "any byte address", "aligned normal-memory load/store is tear-free"],
                            ["W", 2, "address divisible by 2", "aligned normal-memory load/store is tear-free"],
                            ["L", 4, "address divisible by 4", "aligned normal-memory load/store is tear-free"],
                            ["Q", 8, "address divisible by 8", "aligned normal-memory load/store is tear-free"],
                        ],
                        ["0.65in", "0.55in", "1.45in", "2.75in"],
                        "Scalar Access Sizes and Alignment",
                    ),
                    "MEMORY_ORDER_TABLE": latex_code_table(
                        ["Selector", "Code", "Architectural Ordering Effect"],
                        memory_order_rows(model),
                        ["0.95in", "0.45in", "4.00in"],
                        "Atomic Memory-Order Selectors",
                        {0, 1},
                    ),
                    "FENCE_INSTRUCTION_TABLE": latex_code_table(
                        ["Instruction", "Ordering Effect"],
                        [
                            ["RFENCE", "Orders prior reads before later reads issued by the same hardware thread."],
                            ["WFENCE", "Orders prior writes before later writes issued by the same hardware thread."],
                            ["AFENCE", "Orders prior memory operations before later memory operations issued by the same hardware thread."],
                        ],
                        ["0.85in", "4.55in"],
                        "Fence Instructions",
                        {0},
                    ),
                },
            ),
        ]
    )


def latex_privileged_programming_model_section(model: IsaModel) -> str:
    privileged_rule_table = latex_table(
        ["No.", "Subject", "Rule"],
        [
            [1, "privilege mode encoding", "STATUS.PM=0 is user mode; STATUS.PM=1 is supervisor mode."],
            [2, "access domain", "Ordinary supervisor memory operands use current-domain access. Checked user-domain memory access is expressed only by MOVUC, MOVCU, and MOVUU."],
            [3, "entry STATUS update", "SYSCALL, trap, interrupt, and exception entry set STATUS.PM to 1 and otherwise use the entry rule defined by the event class."],
            [4, "saved STATUS return", "SYSRET and IRET restore the saved STATUS image after validating that the return state is architecturally permitted."],
            [5, "SYSCALL frame and entry", "SYSCALL saves FRAME_CONTROL, SS:SP, CS:PC, and DS, then loads the supervisor entry target from SPC/SCS/SDS."],
            [6, "return instruction split", "SYSRET is only for SYSCALL return. IRET is for interrupt, trap, and exception return."],
            [7, "control-register access", "RDCR, WRCR, translation-state updates, interrupt-control updates, and page-table context switches are privileged unless an instruction definition states otherwise."],
            [8, "reserved CPU vectors", "Attempted delivery of a reserved CPU-owned vector is invalid delivery and escalates through the double-fault path."],
        ],
        ["0.35in", "1.35in", "3.70in"],
        "Privileged Model Rules",
        listed=False,
    )
    privilege_state_table = latex_table(
        ["Field", "Value", "Meaning"],
        [
            ["STATUS.PM", "0", "user mode"],
            ["STATUS.PM", "1", "supervisor mode"],
            ["STATUS.IE", "0/1", "maskable interrupt enable"],
            ["STATUS.TF", "0/1", "single-step trace control"],
            ["STATUS.RF", "0/1", "resume flag for exception restart"],
            ["STATUS.NI", "0/1", "nested-interrupt inhibit"],
            ["STATUS.IN", "0/1", "inside interrupt or supervisor entry"],
            ["current memory domain", "-", "default memory access domain for ordinary memory operands"],
            ["checked user access", "-", "MOVUC, MOVCU, and MOVUU select user-domain access for their architecturally defined memory operands"],
        ],
        ["1.05in", "0.45in", "3.90in"],
        "Privilege State and Access Domains",
        listed=False,
    )
    syscall_table = latex_table(
        ["Property", "Rule"],
        [
            ["Entry vector", "none; SYSCALL does not allocate or consume an IVT vector"],
            ["Entry target", "SPC, SCS, and SDS provide the supervisor PC, code segment, and data segment state"],
            ["Saved state", "FRAME_CONTROL, SS:SP, CS:PC, and DS"],
            ["Entry STATUS change", "set STATUS.PM to 1 at the supervisor-entry commit point"],
            ["Return instruction", "SYSRET"],
            ["Return policy", "read the syscall frame as written, validate saved state, and return to the saved PC and segment state"],
        ],
        ["1.45in", "3.95in"],
        "SYSCALL/SYSRET Rules",
        listed=False,
    )
    supervisor_control_flow_table = latex_code_table(
        ["Instruction", "Summary"],
        instruction_brief_rows(model, ["SYSCALL", "SYSRET", "LRET", "IRET"]),
        ["0.85in", "4.55in"],
        "Supervisor Control-Flow Instructions",
        {0},
        listed=False,
    )
    privileged_execution_table = latex_table(
        ["Rule", "Meaning"],
        [
            ["Interrupt stack selection", "IVT entry SN selects the supervisor stack set used for the entry frame."],
            ["NMI and double fault", "NMI and double-fault delivery use the SN field of their IVT entries."],
            ["Interrupt nesting limit", "When the hidden current interrupt depth equals ICR.MAX_IDEPTH, maskable interrupts are implicitly masked."],
            ["Reserved bits", "Reserved control and status bits must validate before commit; invalid writes raise INVALID_CONTROL_STATE."],
            ["User-visible control state", "User-readable state uses dedicated gated instructions rather than direct control-register access."],
        ],
        ["1.45in", "3.95in"],
        "Privileged Execution Rules",
        listed=False,
    )
    return "\n".join(
        [
            str(LatexTopSection("Supervisor / Privileged Programming Model")),
            render_latex_template(
                "privileged_programming_model.tex",
                {
                    "PRIVILEGED_RULE_TABLE": privileged_rule_table,
                    "PRIVILEGE_STATE_TABLE": privilege_state_table,
                    "SYSCALL_TABLE": syscall_table,
                    "SUPERVISOR_CONTROL_FLOW_TABLE": supervisor_control_flow_table,
                    "PRIVILEGED_EXECUTION_TABLE": privileged_execution_table,
                },
            ),
        ]
    )


def latex_exception_processing_section(model: IsaModel) -> str:
    ivt_entry_table = latex_table(
        ["Field", "Location", "Meaning"],
        [
            ["handler_address", "bytes 0..7", "interrupt handler address"],
            ["HP", "byte 8 bit 0", "handler present; if clear, delivery becomes DOUBLE_FAULT"],
            ["reserved_low", "byte 8 bit 1", "reserved, must be zero"],
            ["SN", "byte 8 bits 3..2", "selects supervisor stack set 0..3 for this delivery"],
            ["reserved_high", "byte 8 bits 7..4", "reserved, must be zero"],
            ["reserved", "bytes 9..15", "reserved, must be zero"],
        ],
        ["1.10in", "1.05in", "3.25in"],
        "Interrupt Vector Table Entry Fields",
        listed=False,
    )
    vector_range_table = latex_table(
        ["Range", "Owner", "Meaning"],
        [
            ["0x00..0x03", "CPU", "assigned BASIC-frame CPU exceptions"],
            ["0x04", "CPU", "reserved CPU vector; frame type not predefined"],
            ["0x05", "CPU", "assigned BASIC-frame CPU trap"],
            ["0x06..0x07", "CPU", "reserved CPU vectors; frame type not predefined"],
            ["0x08..0x0E", "CPU", "assigned ERROR/PAGE_FAULT-frame CPU exceptions"],
            ["0x0F..0x17", "CPU", "reserved CPU vectors; frame type not predefined"],
            ["0x18..0x1A", "CPU", "assigned AUX_FAULT-frame CPU exceptions"],
            ["0x1B..0x1F", "CPU", "reserved CPU vectors; frame type not predefined"],
            ["0x20..0x3F", "CPU", "reserved for future architectural vectors"],
            ["0x40..0xFF", "OS/platform/device", "assignable interrupt and event vectors"],
        ],
        ["0.85in", "1.35in", "3.20in"],
        "Interrupt Vector Ranges",
        listed=False,
    )
    cpu_vector_table = latex_table(
        ["Vector", "Name", "Source", "Frame"],
        [
            ["0x00", "DEBUG_TRACE", "debug, trace, watchpoint, or single-step entry", "BASIC"],
            ["0x01", "NMI", "non-maskable interrupt", "BASIC"],
            ["0x02", "BREAKPOINT", "BKPT instruction", "BASIC"],
            ["0x03", "ILLEGAL_INSTRUCTION", "illegal, undefined, reserved, noncanonical, or disabled extension encoding", "BASIC"],
            ["0x08", "PRIVILEGE_FAULT", "privileged instruction, control-register access, or supervisor-only state violation", "ERROR"],
            ["0x09", "PAGE_FAULT", "segment pre-translation, page-table translation, permission, presence, or stack-memory translation failure", "PAGE_FAULT"],
            ["0x0A", "DIVIDE_ERROR", "integer divide, modulo, or quotient overflow", "ERROR"],
            ["0x0B", "ARITHMETIC_TRAP", "reserved arithmetic trap class", "ERROR"],
            ["0x0C", "BOUNDS_FAULT", "bounds-check exception class", "ERROR"],
            ["0x0D", "INVALID_CONTROL_STATE", "invalid control-register, status, or return state", "ERROR"],
            ["0x0E", "FLOATING_POINT_FAULT", "floating-point exception trap", "ERROR"],
            ["0x18", "DOUBLE_FAULT", "fault during exception delivery, reserved CPU vector delivery, or IVT HP=0", "AUX_FAULT"],
            ["0x19", "MACHINE_CHECK", "machine-check or hardware integrity failure", "AUX_FAULT"],
            ["0x1A", "BUS_ERROR", "externally acknowledged or bus-sized access failure", "AUX_FAULT"],
        ],
        ["0.50in", "1.55in", "2.50in", "0.85in"],
        "CPU-Owned Interrupt Vectors",
        listed=False,
    )
    exception_entry_table = latex_table(
        ["Rule", "Meaning"],
        [
            ["CPU exception model", "synchronous and restartable"],
            ["Restart policy", "CPU exceptions identify the faulting instruction or operation at a restartable boundary; software chooses retry, emulation, signal, or termination policy."],
            ["Interrupt frame save", "atomic with respect to architectural visibility"],
            ["Entry STATUS update", "set STATUS.PM to 1 at the entry commit point"],
            ["Return STATUS update", "restore saved STATUS image after validation"],
            ["SYSRET", "syscall frame only"],
            ["IRET", "interrupt, trap, and exception frames"],
            ["Absent IVT handler", "IVT HP=0 immediately becomes DOUBLE_FAULT"],
            ["Reserved CPU vector", "attempted delivery immediately becomes DOUBLE_FAULT"],
            ["Collapsed fault classes", "invalid length is an invalid instruction encoding; segment and canonical-address failures are reported through PAGE_FAULT"],
        ],
        ["1.45in", "3.95in"],
        "Exception Entry and Return Rules",
        listed=False,
    )
    exception_instruction_table = latex_code_table(
        ["Instruction", "Summary"],
        instruction_brief_rows(model, ["BKPT", "IRET", "RESET"]),
        ["0.85in", "4.55in"],
        "Exception Processing Instructions",
        {0},
        listed=False,
    )
    stack_frame_table = latex_table(
        ["Offset", "Slot", "Meaning"],
        [
            ["+0x00", "FRAME_CONTROL", "frame metadata, entry flags, saved FLAGS, and saved STATUS"],
            ["+0x08", "FRAME_EXT0", "reserved for future architected base-frame state; must be zero"],
            ["+0x10", "FRAME_EXT1", "reserved for future architected base-frame state; must be zero"],
            ["+0x18", "SAVED_PC", "saved program counter"],
            ["+0x20", "SAVED_SP", "saved stack pointer"],
            ["+0x28", "SAVED_CS", "saved code segment selector or image"],
            ["+0x30", "SAVED_DS", "saved data segment selector or image"],
            ["+0x38", "SAVED_SS", "saved stack segment selector or image"],
        ],
        ["0.70in", "1.20in", "3.60in"],
        "Supervisor Entry Stack Frame Fields",
        listed=False,
    )
    frame_type_table = latex_table(
        ["Code", "Type", "Payload Blocks", "Payload", "Meaning"],
        [
            ["0x0", "BASIC", 0, "none", "fixed frame only"],
            ["0x1", "ERROR", 1, "ERROR_CODE", "fixed frame plus one 64-byte payload block containing the exception error code"],
            ["0x2", "PAGE_FAULT", 1, "ERROR_CODE, FAULT_EA, FAULT_LINEAR", "page-fault payload with effective-address context and linear address"],
            ["0x3", "AUX_FAULT", 1, "ERROR_CODE, FAULT_EA, FAULT_LINEAR, FAULT_AUX", "auxiliary fault payload for machine-check, bus, or repeat-continuation state"],
        ],
        ["0.40in", "0.82in", "0.62in", "1.55in", "2.00in"],
        "Supervisor Stack Frame Types",
        listed=False,
    )
    payload_slot_table = latex_table(
        ["Offset", "Slot", "Meaning"],
        [
            ["+0x00", "ERROR_CODE", "exception-specific error code"],
            ["+0x08", "FAULT_EA", "faulting effective-address operand information"],
            ["+0x10", "FAULT_LINEAR", "faulting linear address"],
            ["+0x18", "FAULT_AUX", "auxiliary fault information"],
        ],
        ["0.70in", "1.20in", "3.60in"],
        "Supervisor Payload Block Slots",
        listed=False,
    )
    frame_control_table = latex_table(
        ["Field", "Bits", "Meaning"],
        [
            ["vector", "0..7", "interrupt, exception, or trap vector number"],
            ["frame_size", "8..15", "total frame size in 8-byte units"],
            ["saved_idepth", "16..19", "saved interrupt nesting depth"],
            ["frame_type", "20..23", "supervisor stack frame type code"],
            ["from_user", "24", "entry was taken from user mode"],
            ["nmi_frame", "25", "frame was created by NMI entry"],
            ["rep_fault", "26", "repeat continuation state is saved in FAULT_AUX"],
            ["entry_flags", "27..31", "reserved entry flags for this base profile; must be zero unless defined"],
            ["flags", "32..47", "saved FLAGS image"],
            ["status", "48..63", "saved STATUS image"],
        ],
        ["1.10in", "0.65in", "3.65in"],
        "FRAME_CONTROL Fields",
        listed=False,
    )
    repeat_fault_aux_table = latex_fixed_table(
        ["Field", "Bits", "Meaning"],
        repeat_fault_aux_rows(model),
        ["1.55in", "0.60in", "3.35in"],
        "Repeat Fault Auxiliary Fields",
        listed=False,
    )
    reset_state_table = latex_table(
        ["State", "Reset Value"],
        [
            ["ICR", "0"],
            ["ICR.IVT_VALID", "0"],
            ["STATUS.IE", "0"],
            ["STATUS.IN", "0"],
            ["STATUS.NI", "0"],
            ["FSTATUS", "0"],
            ["FFLAGS", "0"],
            ["hidden_current_idepth", "0"],
            ["hidden_nmi_pending", "0"],
            ["PTCR.PE", "0"],
            ["ASCR", "0"],
        ],
        ["2.00in", "2.40in"],
        "Interrupt and Translation Reset State",
        listed=False,
    )
    return "\n".join(
        [
            str(LatexTopSection("Exception Processing Reference")),
            render_latex_template(
                "interrupt_model.tex",
                {
                    "IVT_ENTRY_DIAGRAMS": latex_ivt_entry_diagrams(),
                    "IVT_ENTRY_TABLE": ivt_entry_table,
                    "VECTOR_RANGE_TABLE": vector_range_table,
                    "CPU_VECTOR_TABLE": cpu_vector_table,
                    "EXCEPTION_ENTRY_TABLE": exception_entry_table,
                    "EXCEPTION_INSTRUCTION_TABLE": exception_instruction_table,
                    "STACK_FRAME_DIAGRAMS": latex_supervisor_stack_frame_diagram(),
                    "STACK_FRAME_TABLE": stack_frame_table,
                    "FRAME_TYPE_TABLE": frame_type_table,
                    "PAYLOAD_SLOT_TABLE": payload_slot_table,
                    "FRAME_CONTROL_DIAGRAM": latex_frame_control_diagram(),
                    "FRAME_CONTROL_TABLE": frame_control_table,
                    "REPEAT_FAULT_AUX_DIAGRAM": latex_repeat_fault_aux_diagram(),
                    "REPEAT_FAULT_AUX_TABLE": repeat_fault_aux_table,
                    "RESET_STATE_TABLE": reset_state_table,
                },
            ),
        ]
    )


def latex_c_library_examples_section() -> str:
    return "\n".join(
        [
            str(LatexTopSection("C Library Instruction Examples")),
            render_latex_template(
                "c_library_instruction_examples.tex",
                {
                    "MEMCPY_EXAMPLE": latex_code_block(
                        [
                            "; memcpy(dst, src, n), byte copy forward",
                            "; R0 = src, R1 = dst",
                            "; R2 = n",
                            "REP R2, (MOV.B [R0++], [R1++])",
                        ]
                    ),
                    "MEMMOVE_EXAMPLE": latex_code_block(
                        [
                            "; memmove(dst, src, n), non-overlapping or forward byte copy",
                            "; R0 = src, R1 = dst",
                            "; R2 = n",
                            "REP R2, (MOV.B [R0++], [R1++])",
                        ]
                    ),
                    "MEMSET_EXAMPLE": latex_code_block(
                        [
                            "; memset(dst, c, n), byte fill",
                            "; R1 = dst, R3 = byte c",
                            "; R2 = n",
                            "REP R2, (MOV.B R3, [R1++])",
                        ]
                    ),
                    "MEMCMP_EXAMPLE": latex_code_block(
                        [
                            "; memcmp(a, b, n), forward byte compare",
                            "; R0 = a, R1 = b",
                            "; R2 = n",
                            "REPEQ R2, (CMP.B [R0++], [R1++])",
                        ]
                    ),
                    "BULK_EXTENSION_EXAMPLE": latex_code_block(
                        [
                            "; widen n bytes to n 32-bit elements",
                            "; R0 = src, R1 = dst",
                            "; R2 = n",
                            "REP R2, (EXTZL.B [R0++], [R1++])",
                        ]
                    ),
                },
            ),
        ]
    )


def latex_runtime_examples_section() -> str:
    return "\n".join(
        [
            str(LatexTopSection("Runtime Instruction Examples")),
            render_latex_template("runtime_instruction_examples.tex"),
        ]
    )


def latex_instruction_set_overview_section(model: IsaModel, instructions: list[InstructionDef]) -> str:
    return render_latex_template(
        "instruction_set_summary.tex",
        {
            "INSTRUCTION_FAMILY_TABLE": latex_table(
                ["Class", "Family", "Definitions"],
                instruction_family_rows(instructions),
                ["1.25in", "2.90in", "0.75in"],
                "Instruction Families",
                style="dense",
            ),
            "INSTRUCTION_SUMMARY_TABLE": "",
        },
    )


def latex_instruction_summary_section(model: IsaModel, instructions: list[InstructionDef]) -> str:
    rows = [
        [
            rf"\hyperref[{instruction_label(inst.mnemonic)}]{{{tex_code(inst.mnemonic)}}}",
            latex_cell(inst.doc.get("summary", inst.doc.get("title", inst.mnemonic))),
            latex_cell(instruction_form_count(inst, model)),
        ]
        for inst in instructions
    ]
    return "\n".join(
        [
            str(LatexTopSection("Instruction Set Summary")),
            render_latex_template(
                "instruction_set_summary.tex",
                {
                    "INSTRUCTION_FAMILY_TABLE": latex_table(
                        ["Class", "Family", "Definitions"],
                        instruction_family_rows(instructions),
                        ["1.25in", "2.90in", "0.75in"],
                        "Instruction Families",
                        style="dense",
                    ),
                    "INSTRUCTION_SUMMARY_TABLE": latex_longtable(
                        ["Mnemonic", "Summary", "Forms"],
                        rows,
                        ["0.82in", "4.18in", "0.42in"],
                        "Instruction Set Summary",
                        listed=False,
                    ),
                },
            ),
        ]
    )


def instruction_label(mnemonic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", mnemonic.lower()).strip("-")
    return f"instr:{slug or 'unknown'}"


def latex_instruction_entry(model: IsaModel, inst: InstructionDef) -> str:
    parts: list[str] = [r"\clearpage"]
    title = compact_text(inst.doc.get("title", inst.mnemonic)) or inst.mnemonic
    parts.append(
        rf"\begin{{manualinstruction}}{{{latex_escape(inst.mnemonic)}}}{{{latex_escape(title)}}}{{{instruction_label(inst.mnemonic)}}}"
    )
    summary = compact_text(inst.doc.get("summary", ""))
    if summary:
        parts.append(latex_instruction_field("Summary", latex_escape(summary)))
    description = compact_text(inst.doc.get("description", ""))
    if description:
        parts.append(latex_instruction_field("Description", latex_escape(description)))
    parts.append(latex_operation_field(list(inst.behavior.get("operation", []) or [])))
    syntax_lines = assembler_syntax_lines(model, inst)
    if syntax_lines:
        parts.append(latex_instruction_field("Assembler Syntax", latex_code_line_stack(syntax_lines)))
    parts.append(latex_instruction_field("Attributes", latex_attributes_block(inst, model)))
    status = latex_flag_status(inst)
    if status:
        parts.append(status)
    forms_block = latex_instruction_forms_block(model, inst)
    if forms_block:
        parts.append(forms_block)
    parts.append(r"\end{manualinstruction}")
    return "\n".join(parts)


def latex_reading_instruction_description_section() -> str:
    return render_latex_template("instruction_description_intro.tex")


def latex_instruction_reference_section(model: IsaModel, instructions: list[InstructionDef]) -> str:
    parts: list[str] = []
    for title, group in instruction_set_groups(instructions):
        description_title = title.replace(" Summary", " Descriptions")
        rows = [
            [
                rf"\hyperref[{instruction_label(inst.mnemonic)}]{{{tex_code(inst.mnemonic)}}}",
                latex_cell(inst.doc.get("summary", inst.doc.get("title", inst.mnemonic))),
                latex_cell(instruction_form_count(inst, model)),
            ]
            for inst in group
        ]
        parts.extend(
            [
                str(LatexTopSection(title)),
                latex_longtable(
                    ["Mnemonic", "Summary", "Forms"],
                    rows,
                    ["0.82in", "4.18in", "0.42in"],
                    title,
                    listed=False,
                ),
                str(LatexHiddenTopSection(description_title)),
            ]
        )
        if title == "General Instructions Summary":
            parts.append(latex_reading_instruction_description_section())
        parts.extend(latex_instruction_entry(model, inst) for inst in group)
    return "\n".join(parts)


def infer_format(output: Path | None, explicit: str | None) -> str:
    if explicit:
        return explicit
    if output and output.suffix.lower() in {".tex", ".latex"}:
        return "latex"
    return "markdown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defs", type=Path, default=DEF_ROOT)
    parser.add_argument("--alloc", type=Path, default=ALLOC_ROOT)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--format", choices=["markdown", "latex"], default=None)
    parser.add_argument("--only-allocated", action="store_true")
    args = parser.parse_args()

    fmt = infer_format(args.output, args.format)
    model = load_model(args.defs, args.alloc)
    if fmt == "latex":
        text = render_latex(model, only_allocated=args.only_allocated)
    else:
        text = render_markdown(model, only_allocated=args.only_allocated)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
