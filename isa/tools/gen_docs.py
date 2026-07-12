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
from latex_to_markdown import render_markdown_from_latex  # noqa: E402
from validate_isa import allocation_mnemonic  # noqa: E402
from latex_builder.common import (  # noqa: E402
    LatexHiddenTopSection,
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
DEFAULT_OUTPUT = ROOT / "build" / "isa_reference.tex"
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


def display_text(value: Any) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    return compact_text(value).replace("_", " ")


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


def data_format_template_values(model: IsaModel) -> dict[str, Any]:
    schema = operand_schema(model)
    size_codes = schema.get("size_codes") or {}
    values: dict[str, Any] = {}
    for code in ("B", "W", "L", "Q", "S", "D"):
        body = size_codes.get(code)
        if not isinstance(body, dict):
            continue
        byte_count = int(body.get("bytes", 0) or 0)
        values[f"{code}_SUFFIX"] = body.get("suffix", f".{code}")
        values[f"{code}_BITS"] = byte_count * 8
        values[f"{code}_BYTES"] = byte_count
    for name, spec in (schema.get("immediate_operands") or {}).items():
        if not isinstance(spec, dict):
            continue
        key = str(name).upper()
        values[f"{key}_WIDTH"] = spec.get("width", "")
        rng = spec.get("range", "-")
        if isinstance(rng, list) and len(rng) == 2:
            rng = f"{rng[0]}..{rng[1]}"
        values[f"{key}_RANGE"] = rng
    return values


def instruction_family_rows(instructions: list[InstructionDef]) -> list[list[Any]]:
    counts: Counter[tuple[str, str]] = Counter()
    for inst in instructions:
        counts[(instruction_class(inst), instruction_family(inst))] += 1
    return [[cls, family, count] for (cls, family), count in sorted(counts.items())]


def encoding_class_template_values(model: IsaModel) -> dict[str, Any]:
    return {
        f"{cls.cls.upper()}_PAYLOAD_BITS": cls.payload_bits
        for cls in model.allocation_classes
    }


def form_allows_memory_memory(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("memory_memory") is True or value.get("constraint"):
            return True
        return any(form_allows_memory_memory(child) for child in value.values())
    if isinstance(value, list):
        return any(form_allows_memory_memory(child) for child in value)
    return False


def memory_memory_instruction_names(model: IsaModel) -> list[str]:
    return [inst.mnemonic for inst in model.instructions if form_allows_memory_memory(inst.forms)]


def repeat_syntax_rows(model: IsaModel) -> list[list[Any]]:
    rows: list[list[Any]] = []
    repcc = instruction_by_mnemonic(model, "REPcc")
    if repcc is not None:
        syntax = compact_text(repcc.forms.get("syntax", ""))
        rows.append(["REPcc", syntax, "-", "-"])
        rows.append(["REP", syntax.replace("REPcc", "REP", 1), "-", "-"])

    repg = instruction_by_mnemonic(model, "REPG")
    if repg is None:
        return rows
    rows.append(["REPG", repg.forms.get("syntax", ""), "-", "-"])
    aliases = repg.forms.get("assembler_checked_aliases") or {}
    for name, data in aliases.items():
        if not isinstance(data, dict):
            continue
        requirements: list[str] = []
        body_candidate = data.get("body_candidate_required")
        if body_candidate:
            requirements.append(f"body_candidate={display_text(body_candidate)}")
        body_constraints = data.get("body_constraints") or []
        if isinstance(body_constraints, list):
            requirements.extend(compact_text(item) for item in body_constraints)
        elif body_constraints:
            requirements.append(compact_text(body_constraints))
        rows.append(
            [
                name,
                compact_text(data.get("syntax", "")),
                compact_text(data.get("emits", "")),
                "; ".join(requirements) or "-",
            ]
        )
    return rows


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
            r"\begin{tabularx}{\linewidth}{@{}p{0.88in}>{\raggedright\arraybackslash}X@{}}",
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


def field_bit_range(entry: AllocationEntry, symbol: str) -> str:
    positions = [entry.payload_bits - 1 - index for index, char in enumerate(entry.bits) if char == symbol]
    if not positions:
        return "-"
    high = max(positions)
    low = min(positions)
    return str(high) if high == low else f"{high}:{low}"


def field_size_choices(form: str, symbol: str) -> str:
    match = re.search(rf"{re.escape(symbol)}:([A-Za-z0-9_/]+)", form)
    if not match:
        return ""
    return match.group(1)


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


def latex_field_explanation_block(entry: AllocationEntry, form: str) -> str:
    body_rows: list[str] = []
    operand_count = len(split_form_operands(form))
    for symbol, spec in ordered_entry_fields(entry):
        operand = field_operand(form, symbol)
        role = operand_role(operand[0], operand_count) if operand else "-"
        values = field_size_choices(form, symbol) if spec.get("kind") == "size" else "-"
        body_rows.append(
            " & ".join(
                [
                    tex_code(symbol),
                    latex_escape(display_text(spec.get("kind", "-"))),
                    latex_escape(role),
                    latex_escape(spec.get("width", "-")),
                    tex_code(field_bit_range(entry, symbol)),
                    latex_escape(values or "-"),
                ]
            )
            + r"\\"
        )
    if not body_rows:
        return ""
    return render_latex_template(
        "instruction_field_table.tex",
        {"FIELD_ROWS": "\n".join(body_rows)},
    )


def latex_allocated_instruction_form_block(inst: InstructionDef, entry: AllocationEntry) -> str:
    form = allocation_form_text(entry.text)
    notes = allocation_note_text(entry)
    rows = [
        ("Form", latex_escape(instruction_form_operands(form))),
        ("Encoding class", latex_escape(entry.cls)),
        ("Bytes", latex_escape(instruction_bytes_text(entry, form))),
        ("Privilege", latex_escape(privilege_text(inst.attributes.get("privilege", "unprivileged")))),
    ]
    if notes and notes != "-":
        rows.append(("Notes", latex_escape(notes)))
    rendered_rows = [rf"\textbf{{{latex_escape(key)}}} & {value}\\" for key, value in rows if value]
    return "\n".join(
        [
            r"\begin{manualformblock}{2.9in}",
            rf"\textbf{{{tex_code(form)}}}\par",
            r"\vspace{2pt}",
            r"\begin{tabularx}{\linewidth}{@{}p{0.88in}>{\raggedright\arraybackslash}X@{}}",
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
    return render_latex_template(
        "document.tex",
        {
            "REGISTER_SECTION": latex_register_section(model),
            "CPUID_SECTION": latex_cpuid_feature_discovery_section(model),
            "SAVE_RESTORE_SECTION": latex_save_restore_section(model),
            "DATA_FORMATS_SECTION": latex_data_formats_section(model),
            "CONDITION_CODES_SECTION": latex_condition_section(model),
            "EFFECTIVE_ADDRESS_SECTION": latex_ea_section(model),
            "PRIVILEGED_PROGRAMMING_SECTION": latex_privileged_programming_model_section(model),
            "EXCEPTION_PROCESSING_SECTION": latex_exception_processing_section(model),
            "INSTRUCTION_WORD_FORMATS_SECTION": latex_instruction_word_formats_section(model),
            "EXECUTION_MODEL_SECTION": latex_execution_model_section(model),
            "STREAMING_EXECUTION_SECTION": latex_streaming_model_section(model),
            "INSTRUCTION_SUMMARY_SECTION": latex_instruction_summary_section(model, instructions),
            "INSTRUCTION_REFERENCE_SECTION": latex_instruction_reference_section(model, instructions),
        },
    ) + "\n"


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


def latex_cpuid_feature_discovery_section(model: IsaModel) -> str:
    return render_latex_template(
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
        },
    )


def latex_save_restore_section(model: IsaModel) -> str:
    save = instruction_by_mnemonic(model, "SAVE")
    restore = instruction_by_mnemonic(model, "RESTORE")
    instruction_rows = []
    for inst in (save, restore):
        if inst is not None:
            instruction_rows.append([inst.mnemonic, inst.doc.get("summary", inst.mnemonic)])
    return render_latex_template(
        "save_restore_area.tex",
        {
            "SAVE_RESTORE_INSTRUCTION_TABLE": latex_code_table(
                ["Instruction", "Summary"],
                instruction_rows,
                ["0.85in", "4.55in"],
                "SAVE/RESTORE Instructions",
                {0},
                listed=False,
            ),
        },
    )


def latex_data_formats_section(model: IsaModel) -> str:
    return render_latex_template("data_formats.tex", data_format_template_values(model))


def latex_instruction_word_formats_section(model: IsaModel) -> str:
    return render_latex_template(
        "instruction_word_formats.tex",
        encoding_class_template_values(model),
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
    return render_latex_template(
        "register_model.tex",
        {
            "GENERAL_REGISTER_TABLE": latex_code_table(
                ["Register", "Encoding", "Width"],
                reg_rows,
                ["1.15in", "1.10in", "0.75in"],
                "General Register Encoding",
                {0, 1},
            ),
            "SEGMENT_REGISTER_TABLE": latex_code_table(
                ["Segment", "Selector", "Width"],
                segment_rows,
                ["0.85in", "1.10in", "0.75in"],
                "Segment Registers",
                {0},
            ),
            "SPECIAL_REGISTER_TABLE": latex_code_table(
                ["Special", "Width", "Fixed Segment", "EA Encoding"],
                special_rows,
                ["0.85in", "0.75in", "1.15in", "1.25in"],
                "Special Registers",
                {0, 2, 3},
            ),
        },
    )


def latex_condition_section(model: IsaModel) -> str:
    data = model.metadata.get("conditions") or {}
    rows = []
    for cond in data.get("conditions", []) or []:
        aliases = ", ".join(str(item) for item in cond.get("aliases", []) or [])
        rows.append([bits_text(cond.get("value", ""), 4), cond.get("name", ""), aliases or "-", cond.get("expression", "")])
    return render_latex_template(
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
    auto_update_section = render_latex_template("ea_auto_update_semantics.tex", {})
    return render_latex_template(
        "effective_address_modes.tex",
        {
            "COMPACT_EA_TABLE": latex_code_table(
                ["Bits", "Syntax", "Class", "Memory"],
                compact_rows,
                ["1.10in", "2.30in", "1.0in", "0.6in"],
                "Compact EA Encoding",
                {0, 1},
            ),
            "EXT0_SECTION": ext0_section,
            "AUTO_UPDATE_SECTION": auto_update_section,
        },
    )


def latex_execution_model_section(model: IsaModel) -> str:
    memory_exceptions = compact_text(memory_memory_instruction_names(model))
    return render_latex_template(
        "execution_model.tex",
        {"MEMORY_MEMORY_EXCEPTIONS": latex_escape(memory_exceptions)},
    )


def latex_streaming_model_section(model: IsaModel) -> str:
    repeat_syntax_table = latex_table(
        ["Form", "Syntax", "Emits", "Requirements"],
        repeat_syntax_rows(model),
        ["0.65in", "1.75in", "1.20in", "1.80in"],
        "Repeat Instruction Syntax",
    )
    return render_latex_template(
        "streaming_execution_model.tex",
        {"REPEAT_SYNTAX_TABLE": repeat_syntax_table},
    )


def latex_privileged_programming_model_section(model: IsaModel) -> str:
    supervisor_control_flow_table = latex_code_table(
        ["Instruction", "Summary"],
        instruction_brief_rows(model, ["SYSCALL", "SYSRET", "LRET", "IRET"]),
        ["0.85in", "4.55in"],
        "Supervisor Control-Flow Instructions",
        {0},
        listed=False,
    )
    return render_latex_template(
        "privileged_programming_model.tex",
        {"SUPERVISOR_CONTROL_FLOW_TABLE": supervisor_control_flow_table},
    )


def latex_exception_processing_section(model: IsaModel) -> str:
    exception_instruction_table = latex_code_table(
        ["Instruction", "Summary"],
        instruction_brief_rows(model, ["BKPT", "IRET", "RESET"]),
        ["0.85in", "4.55in"],
        "Exception Processing Instructions",
        {0},
        listed=False,
    )
    return render_latex_template(
        "interrupt_model.tex",
        {"EXCEPTION_INSTRUCTION_TABLE": exception_instruction_table},
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
            "INSTRUCTION_SUMMARY_TABLE": latex_longtable(
                ["Mnemonic", "Summary", "Forms"],
                rows,
                ["0.82in", "4.18in", "0.42in"],
                "Instruction Set Summary",
                listed=False,
            ),
        },
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


def infer_format(output: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    return "markdown" if output.suffix.lower() in {".md", ".markdown"} else "latex"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defs", type=Path, default=DEF_ROOT)
    parser.add_argument("--alloc", type=Path, default=ALLOC_ROOT)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--format", choices=["latex", "markdown"], default=None)
    parser.add_argument("--pandoc", help="Pandoc executable for derived Markdown output")
    parser.add_argument("--only-allocated", action="store_true")
    args = parser.parse_args()

    model = load_model(args.defs, args.alloc)
    latex = render_latex(model, only_allocated=args.only_allocated)
    fmt = infer_format(args.output, args.format)
    text = render_markdown_from_latex(latex, args.pandoc) if fmt == "markdown" else latex

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
