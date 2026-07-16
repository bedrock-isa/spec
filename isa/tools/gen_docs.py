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
    PREDICATES,
    compact_bits,
    entry_claims,
    expand_pattern,
    namespace_patterns,
    parse_range,
    validate_file,
)
from alloc_notes import allocation_form_text  # noqa: E402
from latex_to_markdown import render_markdown_from_latex  # noqa: E402
from validate_isa import allocation_mnemonic  # noqa: E402
from latex_builder.common import (  # noqa: E402
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
    "fpu",
    "fpu_transcendental_approx",
]
INSTRUCTION_SET_SECTION_TITLES = {
    "base": "General Instructions",
    "fpu": "Floating-Point Instructions",
    "fpu_transcendental_approx": "Approximate Floating-Point Transcendental Instructions",
}
INSTRUCTION_SET_SECTION_INTRO_TEMPLATES = {
    "fpu_transcendental_approx": "approximate_floating_point_intro.tex",
}
INSTRUCTION_FILENAME = "instruction.yaml"
INSTRUCTION_DETAILS_FILENAME = "details.tex"


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
    def approximation(self) -> dict[str, Any]:
        value = self.behavior.get("approximation")
        return value if isinstance(value, dict) else {}

    @property
    def attributes(self) -> dict[str, Any]:
        value = self.data.get("attributes")
        return value if isinstance(value, dict) else {}

    @property
    def forms(self) -> dict[str, Any]:
        value = self.data.get("forms")
        return value if isinstance(value, dict) else {}

    @property
    def details_path(self) -> Path:
        return self.path.with_name(INSTRUCTION_DETAILS_FILENAME)


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
        common = data.get("common")
        if not isinstance(common, str) or not common.strip():
            raise ValueError(f"{include}: missing common metadata path")
        common_path = include.parent / common
        if not common_path.is_file():
            raise FileNotFoundError(f"common metadata not found: {common_path}")
        include_items = data.get("include")
        if not isinstance(include_items, list):
            raise ValueError(f"{include}: include must be a list of instruction directories")
        for item in include_items:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{include}: instruction include entries must be non-empty strings")
            directory = include.parent / item
            if not directory.is_dir():
                raise FileNotFoundError(f"instruction directory not found: {directory}")
            path = directory / INSTRUCTION_FILENAME
            if not path.is_file():
                raise FileNotFoundError(f"instruction definition not found: {path}")
            paths.append((name, path))
    return paths


def load_instructions(defs_root: Path) -> list[InstructionDef]:
    instructions: list[InstructionDef] = []
    for instruction_set, path in manifest_instruction_paths(defs_root):
        data = load_yaml(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected mapping")
        mnemonic = data.get("mnemonic")
        if not mnemonic:
            raise ValueError(f"{path}: missing mnemonic")
        if path.parent.name != str(mnemonic):
            raise ValueError(
                f"{path}: directory name {path.parent.name!r} does not match mnemonic {mnemonic!r}"
            )
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


def instruction_set_groups(instructions: list[InstructionDef]) -> list[tuple[str, str, list[InstructionDef]]]:
    by_set: dict[str, list[InstructionDef]] = defaultdict(list)
    for inst in instructions:
        by_set[inst.instruction_set].append(inst)

    ordered_sets = [name for name in INSTRUCTION_SET_SECTION_ORDER if name in by_set]
    ordered_sets.extend(sorted(name for name in by_set if name not in set(ordered_sets)))
    return [
        (
            name,
            INSTRUCTION_SET_SECTION_TITLES.get(name, f"{name.replace('_', ' ').title()} Instructions Summary"),
            by_set[name],
        )
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


def latex_instruction_links(model: IsaModel, mnemonics: list[str], lead: str) -> str:
    links = []
    for mnemonic in mnemonics:
        inst = instruction_by_mnemonic(model, mnemonic)
        if inst is not None:
            links.append(rf"\hyperref[{instruction_label(inst.mnemonic)}]{{\texttt{{{latex_escape(inst.mnemonic)}}}}}")
    if not links:
        return ""
    return f"{lead} " + ", ".join(links) + r".\par"


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
    return "\n".join(rf"\manualcodeline{{{latex_escape(line)}}}" for line in lines)


def flag_summary(flags: Any) -> str:
    if isinstance(flags, dict):
        return "; ".join(f"{key}: {compact_text(value)}" for key, value in flags.items()) or "-"
    return compact_text(flags) or "-"


def instruction_length_summary(inst: InstructionDef, model: IsaModel) -> str:
    lengths: set[int] = set()
    for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
        form = allocation_form_text(entry.text)
        lengths.update(instruction_length(entry, form, model.metadata.get("ea")).required_bytes)
    if not lengths:
        return "variable length"
    low, high = min(lengths), max(lengths)
    return f"{low} byte" if low == high == 1 else (f"{low} bytes" if low == high else f"{low}-{high} bytes")


def latex_instruction_metadata(inst: InstructionDef, model: IsaModel) -> str:
    return rf"\manualinstructionmetadata{{{latex_escape(instruction_class(inst))}}}" \
        rf"{{{latex_escape(instruction_family(inst))}}}" \
        rf"{{{latex_escape(privilege_text(inst.attributes.get('privilege', '-'), '-'))}}}" \
        rf"{{{latex_escape(instruction_length_summary(inst, model))}}}"


def latex_attributes_block(inst: InstructionDef, model: IsaModel) -> str:
    lines = [
        rf"{latex_escape('Class')} = {latex_escape(instruction_class(inst))}",
        rf"{latex_escape('Family')} = {latex_escape(instruction_family(inst))}",
        rf"{latex_escape('Privilege')} = "
        rf"{latex_escape(privilege_text(inst.attributes.get('privilege', '-'), '-'))}",
        rf"{latex_escape('Length')} = {latex_escape(instruction_length_summary(inst, model))}",
    ]
    return latex_ragged_block(lines)


def latex_approximation_field(inst: InstructionDef) -> str:
    approximation = inst.approximation
    if not approximation:
        return ""
    max_ulp = approximation.get("max_ulp") or {}
    if not isinstance(max_ulp, dict):
        max_ulp = {}
    lines = [
        f"Contract ID: {compact_text(approximation.get('contract_id'))}",
        f"Reference: {compact_text(approximation.get('reference_function'))}",
        f"Domain: {compact_text(approximation.get('domain'))}",
        f"ISA maximum error: S <= {compact_text(max_ulp.get('S'))} ULP; D <= {compact_text(max_ulp.get('D'))} ULP",
    ]
    anchors = approximation.get("exact_anchors") or []
    if anchors:
        lines.append("Exact anchors: " + "; ".join(compact_text(item) for item in anchors))
    properties = approximation.get("properties") or []
    if properties:
        lines.append("Properties: " + "; ".join(compact_text(item) for item in properties))
    return latex_instruction_field(
        "Approximation Contract",
        latex_ragged_block([latex_escape(line) for line in lines]),
    )


def latex_flag_status(inst: InstructionDef) -> str:
    flags = inst.attributes.get("flags")
    if not isinstance(flags, dict) or not flags:
        return ""
    names = [name for name in ("Z", "N", "C", "V") if name in flags]
    if names:
        items = "".join(rf"\manualstatusitem{{{latex_escape(name)}}}{{*}}" for name in names)
        return "\n".join(
            [r"\begin{manualstatusstrip}", items, rf"\par\textcolor{{ManualMuted}}{{{latex_escape(flag_summary(flags))}}}", r"\end{manualstatusstrip}"]
        )
    return rf"\begin{{manualstatusstrip}}\textbf{{Status}}\enspace {latex_escape(flag_summary(flags))}\end{{manualstatusstrip}}"


def latex_instruction_constant_ids(inst: InstructionDef) -> str:
    constants = inst.forms.get("constant_ids")
    if constants is None:
        return ""
    if not isinstance(constants, list) or not constants:
        raise ValueError(f"{inst.path}: forms.constant_ids must be a non-empty list")

    rows: list[list[str]] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(constants):
        if not isinstance(item, dict):
            raise ValueError(f"{inst.path}: forms.constant_ids[{index}] must be a mapping")
        constant_id = compact_text(item.get("id"))
        name = compact_text(item.get("name"))
        value_bits = compact_text(item.get("value_bits"))
        if not constant_id or not name or not value_bits:
            raise ValueError(
                f"{inst.path}: forms.constant_ids[{index}] requires id, name, and value_bits"
            )
        if constant_id in seen_ids:
            raise ValueError(f"{inst.path}: duplicate constant ID {constant_id}")
        seen_ids.add(constant_id)
        rows.append(
            [
                tex_code(constant_id),
                latex_escape(display_text(name)),
                tex_code(value_bits),
            ]
        )

    result_format = compact_text(inst.forms.get("result_format", ""))
    title = f"{inst.mnemonic} Constant IDs"
    if result_format:
        title += f" ({result_format})"
    return latex_longtable(
        ["ID", "Constant", "Result bits"],
        rows,
        ["0.75in", "2.35in", "2.30in"],
        title,
    )


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


def latex_instruction_form_block(
    title: str,
    rows: list[tuple[str, str]],
    *,
    needspace: str = "1.45in",
    include_forms_heading: bool = False,
) -> str:
    values = {key: value for key, value in rows if value and key != "Form"}
    if not values:
        return ""
    kind = values.pop("Kind", "form")
    size = values.pop("Size", "variable length")
    attributes = values.pop("Attributes", "unprivileged")
    return "\n".join(
        [
            rf"\begin{{manualformblock}}{{{needspace}}}",
            *([r"\manualinstructionformsheading"] if include_forms_heading else []),
            rf"\textbf{{{tex_code(title)}}}\par",
            rf"\manualformmetadata{{{kind}}}{{{size}}}{{{attributes}}}",
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
    if operand_count == 2:
        return "source operand" if index == 0 else "destination operand"
    return f"operand {index + 1}"


CLASS_OPCODE_BYTES = {
    "extrashort": 1,
    "short": 2,
    "medium": 3,
    "long": 4,
    "extralong": 5,
}


def allocation_opcode_bytes(entry: AllocationEntry) -> int:
    if entry.cls in CLASS_OPCODE_BYTES:
        return CLASS_OPCODE_BYTES[entry.cls]
    return 2 + (max(0, entry.payload_bits - 10) + 7) // 8


@dataclass(frozen=True)
class InstructionLength:
    opcode_bytes: int
    required_bytes: tuple[int, ...]

    @property
    def minimum_required_bytes(self) -> int:
        return min(self.required_bytes)

    @property
    def maximum_required_bytes(self) -> int:
        return max(self.required_bytes)


def named_payload_bytes(name: Any, sizes: dict[str, int]) -> int:
    text = compact_text(name)
    if not text or text == "none":
        return 0
    if text in sizes:
        return sizes[text]
    match = re.search(r"(8|16|32|64)", text)
    if match:
        return int(match.group(1)) // 8
    raise ValueError(f"unknown instruction payload size: {text!r}")


def ea_payload_byte_lengths(ea_data: Any) -> tuple[int, ...]:
    if not isinstance(ea_data, dict):
        raise ValueError("missing EA metadata for instruction length calculation")
    displacements = ea_data.get("displacements") or {}
    sizes = {
        str(name): int(spec["bytes"])
        for name, spec in displacements.items()
        if isinstance(spec, dict) and "bytes" in spec
    }
    ext0 = ea_data.get("ext0") or {}
    descriptor_sizes = {
        (len(re.sub(r"[\s_]", "", str(form.get("bits", "")))) + 7) // 8
        for form in (ext0.get("forms") or [])
        if isinstance(form, dict) and form.get("bits")
    }
    if not descriptor_sizes:
        descriptor_sizes = {1}

    lengths: set[int] = set()
    for form in ea_data.get("compact_ea", []) or []:
        if not isinstance(form, dict):
            continue
        if form.get("class") == "ext0_escape":
            displacement_bytes = named_payload_bytes(form.get("displacement"), sizes)
            lengths.update(size + displacement_bytes for size in descriptor_sizes)
            continue
        payload_bytes = 0
        for key in ("displacement", "absolute", "immediate"):
            if key in form:
                payload_bytes += named_payload_bytes(form.get(key), sizes)
        lengths.add(payload_bytes)
    if not lengths:
        raise ValueError("EA metadata defines no compact EA payload lengths")
    return tuple(sorted(lengths))


def fixed_form_payload_bytes(form: str) -> int:
    total = 0
    for marker in re.findall(r"<([^>]+)>", form):
        if marker == "ea":
            continue
        total += named_payload_bytes(marker, {})
    return total


def instruction_length(entry: AllocationEntry, form: str, ea_data: Any) -> InstructionLength:
    opcode_bytes = allocation_opcode_bytes(entry)
    required = {opcode_bytes + fixed_form_payload_bytes(form)}
    ea_count = sum(
        1
        for field in entry.fields.values()
        if isinstance(field, dict) and field.get("kind") == "ea7"
    )
    if ea_count:
        ea_lengths = ea_payload_byte_lengths(ea_data)
        for _ in range(ea_count):
            required = {
                current + payload
                for current in required
                for payload in ea_lengths
                if current + payload <= 18
            }
    if not required:
        raise ValueError(f"{entry.path}: {form} has no encoding that fits the 18-byte instruction limit")
    if entry.cls in {"extrashort", "short"} and required != {opcode_bytes}:
        raise ValueError(f"{entry.path}: {form} appends payload to a fixed-length {entry.cls} encoding")
    return InstructionLength(opcode_bytes, tuple(sorted(required)))


def required_bytes_text(length: InstructionLength) -> str:
    low = length.minimum_required_bytes
    high = length.maximum_required_bytes
    return str(low) if low == high else f"{low}-{high}"


def required_bytes_label(length: InstructionLength) -> str:
    value = required_bytes_text(length)
    return f"{value} byte" if value == "1" else f"{value} bytes"


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


def normalize_byte_segments(segments: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Keep contiguous fixed bits aligned to four-bit groups within a byte."""
    normalized: list[tuple[str, int]] = []
    fixed_bits = ""

    def flush_fixed_bits() -> None:
        nonlocal fixed_bits
        for index in range(0, len(fixed_bits), 4):
            chunk = fixed_bits[index : index + 4]
            normalized.append((chunk, len(chunk)))
        fixed_bits = ""

    for label, width in segments:
        if len(label) == width and set(label) <= {"0", "1", "-"}:
            fixed_bits += label
            continue
        flush_fixed_bits()
        normalized.append((label, width))
    flush_fixed_bits()
    return normalized


def instruction_byte_row_segments(
    byte_index: int,
    left_segments: list[tuple[str, int]],
    right_segments: list[tuple[str, int]] | None = None,
) -> str:
    def field(text: str, width: int) -> str:
        if set(text) <= {"0", "1"}:
            macro = "manualbitfixed"
        elif set(text) <= {"-"}:
            macro = "manualbitreserved"
        else:
            macro = "manualbitvariable"
        return rf"\{macro}{{{latex_escape(text)}}}{{{width}}}"

    fields = [
        field(text, width)
        for text, width in left_segments
        if width > 0
    ]
    if right_segments is None:
        labels = rf"\manualsinglebytelabels{{{byte_index}}}"
        fields.append(r"\manualbitgap{9}")
    else:
        labels = rf"\manualbytepairlabelsfor{{{byte_index}}}{{{byte_index + 1}}}"
        fields.append(r"\manualbitgap{1}")
        fields.extend(
            field(text, width)
            for text, width in right_segments
            if width > 0
        )
    return "\n".join(
        [
            r"\manualbitfieldrow{}{%",
            labels,
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
            left_label = label
            right_label = label
            if len(label) == segment_width and set(label) <= {"0", "1", "-"}:
                left_label = label[:remaining]
                right_label = label[remaining:]
            left.append((left_label, remaining))
            right.append((right_label, segment_width - remaining))
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
    header_segments = [("11", 2), ("L", 4), *bit_segments(first_payload)]
    return split_segments_at_width(header_segments, 8)


def entry_byte_segments(entry: AllocationEntry) -> list[list[tuple[str, int]]]:
    byte0, byte1 = entry_header_byte_segments(entry)
    byte_segments = [byte0]
    if byte1:
        byte_segments.append(byte1)
    if entry.cls not in {"extrashort", "short"}:
        remaining = entry.bits[10:]
        while remaining:
            chunk = remaining[:8]
            remaining = remaining[8:]
            byte_segments.append(bit_segments(chunk))
    byte_segments = [normalize_byte_segments(segments) for segments in byte_segments]
    for byte_index, segments in enumerate(byte_segments):
        width = sum(segment_width for _label, segment_width in segments)
        if width != 8:
            raise ValueError(f"{entry.path}: {entry.entry_id} byte {byte_index} has {width} bits, expected 8")
    return byte_segments


def latex_entry_bit_diagram(entry: AllocationEntry, form: str) -> str:
    byte_segments = entry_byte_segments(entry)
    rows = [
        instruction_byte_row_segments(
            index,
            byte_segments[index],
            byte_segments[index + 1] if index + 1 < len(byte_segments) else None,
        )
        for index in range(0, len(byte_segments), 2)
    ]
    return "\n".join(
        [
            rf"\begin{{manualbitdiagram}}{{Format \textemdash{{}} Instruction format for {latex_escape(form)}}}",
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


def constraint_allowed_values(constraint: dict[str, Any]) -> set[int]:
    allowed: set[int] = set()
    for item in constraint.get("allow") or []:
        low, high = parse_range(item)
        allowed.update(range(low, high + 1))
    return allowed


def decimal_value_ranges(values: set[int]) -> str:
    if not values:
        return "-"
    runs: list[tuple[int, int]] = []
    start = previous = min(values)
    for value in sorted(values)[1:]:
        if value == previous + 1:
            previous = value
            continue
        runs.append((start, previous))
        start = previous = value
    runs.append((start, previous))
    return ", ".join(str(low) if low == high else f"{low}-{high}" for low, high in runs)


def field_constraint_values(
    model: IsaModel,
    inst: InstructionDef,
    entry: AllocationEntry,
    symbol: str,
    spec: dict[str, Any],
) -> str:
    constraints = [
        constraint
        for constraint in entry.constraints
        if constraint.get("field") == symbol and "allow" in constraint
    ]
    if not constraints:
        return ""
    width = int(spec.get("width", 0))
    allowed = set(range(1 << width)) if width > 0 else set()
    for constraint in constraints:
        allowed &= constraint_allowed_values(constraint)

    if spec.get("kind") == "condition":
        names = {
            int(condition["value"]): str(condition["name"])
            for condition in (model.metadata.get("conditions") or {}).get("conditions", [])
            if isinstance(condition, dict) and "value" in condition and "name" in condition
        }
        if allowed <= names.keys():
            return ", ".join(names[value] for value in sorted(allowed))

    memory_order = inst.attributes.get("memory_ordering") or {}
    if symbol == "o" and isinstance(memory_order, dict):
        encodings = memory_order.get("encodings") or {}
        names = {
            int(value): display_text(name)
            for name, value in encodings.items()
        }
        if allowed <= names.keys():
            return ", ".join(names[value] for value in sorted(allowed))

    return decimal_value_ranges(allowed)


@dataclass(frozen=True)
class CompactEaDisplayRow:
    syntax: str
    mode_bits: str
    form_bits: str
    values: frozenset[int]


@dataclass(frozen=True)
class EAAvailabilityCategory:
    name: str
    members: tuple[str, ...]
    allowed: tuple[str, ...]
    mode: str
    exceptions: tuple[str, ...] = ()


@dataclass(frozen=True)
class EAAvailabilitySummary:
    """Lossless, presentation-ready summary of one form's compact-EA availability."""

    categories: tuple[EAAvailabilityCategory, ...]
    allowed_syntax: frozenset[str]

    def reconstructed_allowed_syntax(self) -> frozenset[str]:
        reconstructed: set[str] = set()
        for category in self.categories:
            members = set(category.members)
            if category.mode == "all":
                reconstructed.update(members)
            elif category.mode == "except":
                reconstructed.update(members - set(category.exceptions))
            elif category.mode == "only":
                reconstructed.update(category.exceptions)
            elif category.mode != "none":
                raise ValueError(f"unknown EA availability mode: {category.mode}")
        return frozenset(reconstructed)


def compact_ea_display_rows(ea_data: Any) -> list[CompactEaDisplayRow]:
    if not isinstance(ea_data, dict):
        raise ValueError("missing EA metadata for addressing-mode table")
    rows: list[CompactEaDisplayRow] = []
    for item in ea_data.get("compact_ea", []) or []:
        if not isinstance(item, dict) or item.get("class") == "reserved":
            continue
        bits = compact_bits(str(item.get("bits", "")))
        syntax = compact_text(item.get("syntax"))
        if len(bits) != 7 or ".." in bits or not syntax:
            raise ValueError(f"invalid compact EA display form: bits={bits!r}, syntax={syntax!r}")
        rows.append(
            CompactEaDisplayRow(
                syntax=syntax,
                mode_bits=bits[:3],
                form_bits=bits[3:],
                values=frozenset(expand_pattern(bits)),
            )
        )
    if not rows:
        raise ValueError("EA metadata defines no displayable compact EA forms")
    return rows


def compact_ea_category(syntax: str) -> str:
    if syntax in {"Rn(r)", "SP"}:
        return "Register"
    if syntax.startswith("["):
        return "Memory"
    if syntax.startswith("imm"):
        return "Immediate"
    if syntax.startswith("EXT0"):
        return "EXT0"
    raise ValueError(f"uncategorized compact EA syntax: {syntax!r}")


def ea_availability_summary(model: IsaModel, entry: AllocationEntry, symbol: str) -> EAAvailabilitySummary:
    constraints = ea_constraints_for_field(entry, symbol)
    rows = compact_ea_display_rows(model.metadata.get("ea"))
    allowed: set[str] = set()
    for row in rows:
        allowed_values = {value for value in row.values if ea_value_allowed(value, constraints)}
        if allowed_values and allowed_values != row.values:
            raise ValueError(
                f"{entry.path}: {entry.entry_id} partially allows EA form {row.syntax!r} for field {symbol}"
            )
        if allowed_values:
            allowed.add(row.syntax)
    categories: list[EAAvailabilityCategory] = []
    for name in ("Register", "Memory", "Immediate", "EXT0"):
        members = tuple(row.syntax for row in rows if compact_ea_category(row.syntax) == name)
        category_allowed = tuple(item for item in members if item in allowed)
        excluded = tuple(item for item in members if item not in allowed)
        if not category_allowed:
            mode, exceptions = "none", ()
        elif len(category_allowed) == len(members):
            mode, exceptions = "all", ()
        elif len(excluded) <= len(category_allowed):
            mode, exceptions = "except", excluded
        else:
            mode, exceptions = "only", category_allowed
        categories.append(EAAvailabilityCategory(name, members, category_allowed, mode, exceptions))
    summary = EAAvailabilitySummary(tuple(categories), frozenset(allowed))
    if summary.reconstructed_allowed_syntax() != summary.allowed_syntax:
        raise ValueError(f"{entry.path}: lossy EA summary for {entry.entry_id} field {symbol}")
    return summary


def latex_ea_syntax_list(items: tuple[str, ...]) -> str:
    return ", ".join(tex_code(item) for item in items)


def latex_ea_availability_summary(summary: EAAvailabilitySummary) -> str:
    allowed_terms: list[str] = []
    unavailable: list[str] = []
    for category in summary.categories:
        if category.mode == "all":
            allowed_terms.append(category.name)
        elif category.mode == "except":
            allowed_terms.append(f"{category.name} except {latex_ea_syntax_list(category.exceptions)}")
        elif category.mode == "only":
            allowed_terms.append(f"{category.name} only {latex_ea_syntax_list(category.exceptions)}")
        else:
            unavailable.append(category.name)
    return rf"\manualeasummary{{{'; '.join(allowed_terms) or 'none'}}}{{{', '.join(unavailable)}}}"


def destination_ea_field(entry: AllocationEntry) -> str | None:
    for symbol in ("d", "e"):
        spec = entry.fields.get(symbol)
        if isinstance(spec, dict) and spec.get("kind") == "ea7":
            return symbol
    return None


def ea_constraints_for_field(entry: AllocationEntry, symbol: str) -> list[dict[str, Any]]:
    destination = destination_ea_field(entry)
    return [
        constraint
        for constraint in entry.constraints
        if constraint.get("field") == symbol
        or (constraint.get("destination") and symbol == destination)
    ]


def ea_value_allowed(value: int, constraints: list[dict[str, Any]]) -> bool:
    for constraint in constraints:
        if "allow" in constraint:
            ranges = [parse_range(item) for item in constraint.get("allow") or []]
            if not any(low <= value <= high for low, high in ranges):
                return False
        if "exclude" in constraint:
            predicate_name = str(constraint["exclude"])
            predicate = PREDICATES.get(predicate_name)
            if predicate is None:
                raise ValueError(f"unknown EA constraint predicate: {predicate_name}")
            if predicate(value):
                return False
    return True


def entry_ea_fields(entry: AllocationEntry, form: str) -> list[tuple[str, str]]:
    operand_count = len(split_form_operands(form))
    fields: list[tuple[str, str]] = []
    for symbol, spec in ordered_entry_fields(entry):
        if spec.get("kind") != "ea7":
            continue
        operand = field_operand(form, symbol)
        role = operand_role(operand[0], operand_count) if operand else "operand"
        fields.append((symbol, role))
    return fields


def latex_ea_addressing_mode_tables(model: IsaModel, entry: AllocationEntry, symbol: str) -> str:
    return latex_ea_availability_summary(ea_availability_summary(model, entry, symbol))


def field_description_label(symbol: str, spec: dict[str, Any], inst: InstructionDef) -> str:
    kind = str(spec.get("kind", "field"))
    if kind == "size":
        name = "Size field"
    elif kind == "ea7":
        name = "Effective Address field"
    elif kind in {"rn", "freg", "vreg", "creg", "sreg"}:
        name = "Register field"
    elif kind == "condition":
        name = "Condition field"
    elif kind == "immediate":
        name = "Immediate field"
    elif symbol == "o" and inst.attributes.get("memory_ordering"):
        name = "Memory-order field"
    else:
        name = f"{display_text(kind).capitalize()} field"
    return f"{latex_escape(name)} {tex_code(symbol)}"


def field_description_text(
    model: IsaModel,
    inst: InstructionDef,
    entry: AllocationEntry,
    form: str,
    symbol: str,
    spec: dict[str, Any],
) -> str:
    operand = field_operand(form, symbol)
    role = operand_role(operand[0], len(split_form_operands(form))) if operand else ""
    kind = spec.get("kind")
    values = field_constraint_values(model, inst, entry, symbol, spec)
    if kind == "size":
        choices = field_size_choices(form, symbol)
        return latex_escape(f"Selects {choices}." if choices else "Selects the operand size.")
    if kind == "ea7":
        target = f"the {role}" if role else "the operand"
        return latex_escape(
            f"Specifies {target}. Availability is summarized by category; compact mode bits are defined by "
            "Compact EA Encoding, and extended descriptors are defined by the Extended EA profiles."
        )
    if kind in {"rn", "freg", "vreg", "creg", "sreg"}:
        target = f"the {role}" if role else "a register operand"
        return latex_escape(f"Selects {target}.")
    if kind == "condition":
        text = "Selects the condition code."
    elif kind == "immediate":
        text = "Encodes the immediate value."
    elif symbol == "o" and inst.attributes.get("memory_ordering"):
        text = "Selects the memory ordering."
    else:
        text = f"Encodes the {display_text(kind)} value."
    if values:
        text += f" Allowed values: {values}."
    return latex_escape(text)


def latex_field_explanation_block(
    model: IsaModel,
    inst: InstructionDef,
    entry: AllocationEntry,
    form: str,
) -> str:
    parts: list[str] = []
    if entry.cls not in {"extrashort", "short"}:
        parts.append(
            r"\manualinstructionfielddescription{Length field \texttt{L}}"
            r"{Encodes the total instruction length as $3+L$ bytes. "
            r"The selected length must cover all required bytes.}"
        )
    for symbol, spec in ordered_entry_fields(entry):
        if spec.get("kind") == "ea7":
            parts.append(r"\Needspace{1.15in}")
        parts.append(
            rf"\manualinstructionfielddescription{{{field_description_label(symbol, spec, inst)}}}"
            rf"{{{field_description_text(model, inst, entry, form, symbol, spec)}}}"
        )
        if spec.get("kind") == "ea7":
            parts.append(latex_ea_addressing_mode_tables(model, entry, symbol))
    if not parts:
        return ""
    return "\n".join([r"\manualinstructionfieldsheading", *parts])


def latex_allocated_instruction_form_block(
    model: IsaModel,
    inst: InstructionDef,
    entry: AllocationEntry,
    *,
    include_forms_heading: bool = False,
) -> str:
    form = allocation_form_text(entry.text)
    length = instruction_length(entry, form, model.metadata.get("ea"))
    form_privilege = inst.attributes.get("privilege", "unprivileged")
    for form_metadata in inst.forms.values():
        if not isinstance(form_metadata, dict):
            continue
        if form_metadata.get("allocation") == entry.entry_id:
            form_privilege = form_metadata.get("privilege", form_privilege)
            break
    rows = [
        ("Encoding class", latex_escape(entry.cls)),
        ("Required bytes", latex_escape(required_bytes_label(length))),
        ("Privilege", latex_escape(privilege_text(form_privilege))),
    ]
    ea_field_count = len(entry_ea_fields(entry, form))
    needspace = "2.75in" if ea_field_count == 0 else "3.65in"
    return "\n".join(
        [
            rf"\begin{{manualformblock}}{{{needspace}}}",
            *([r"\manualinstructionformsheading"] if include_forms_heading else []),
            rf"\textbf{{{tex_code(form)}}}\par",
            rf"\manualformmetadata{{{rows[0][1]}}}{{{rows[1][1]}}}{{{rows[2][1]}}}",
            r"\manualinstructionformatheading",
            latex_entry_bit_diagram(entry, form),
            latex_field_explanation_block(model, inst, entry, form),
            r"\end{manualformblock}",
        ]
    )


def latex_instruction_forms_block(model: IsaModel, inst: InstructionDef) -> str:
    blocks: list[str] = []
    for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
        blocks.append(
            latex_allocated_instruction_form_block(
                model,
                inst,
                entry,
                include_forms_heading=not blocks,
            )
        )
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
            blocks.append(
                latex_instruction_form_block(
                    fallback_form_syntax(inst, form),
                    rows,
                    needspace="1.25in",
                    include_forms_heading=not blocks,
                )
            )
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


def fptransa_contracts(model: IsaModel) -> list[tuple[int, InstructionDef, dict[str, Any]]]:
    contracts: list[tuple[int, InstructionDef, dict[str, Any]]] = []
    for inst in model.instructions:
        approximation = inst.approximation
        if not approximation:
            continue
        raw_id = compact_text(approximation.get("contract_id"))
        try:
            contract_id = int(raw_id, 0)
        except ValueError as exc:
            raise ValueError(f"{inst.path}: invalid approximation contract_id {raw_id!r}") from exc
        contracts.append((contract_id, inst, approximation))
    return sorted(contracts, key=lambda item: item[0])


def latex_fptransa_contract_table(model: IsaModel) -> str:
    rows: list[list[str]] = []
    for contract_id, inst, approximation in fptransa_contracts(model):
        max_ulp = approximation.get("max_ulp") or {}
        if not isinstance(max_ulp, dict):
            max_ulp = {}
        accuracy = f"S <= {compact_text(max_ulp.get('S'))} ULP; D <= {compact_text(max_ulp.get('D'))} ULP"
        rows.append(
            [
                tex_code(f"0x{contract_id:04x}"),
                rf"\hyperref[{instruction_label(inst.mnemonic)}]{{{tex_code(inst.mnemonic)}}}",
                latex_escape(compact_text(approximation.get("reference_function"))),
                latex_escape(compact_text(approximation.get("domain"))),
                latex_escape(accuracy),
            ]
        )
    return latex_longtable(
        ["Contract ID", "Mnemonic", "Reference", "Domain", "ISA maximum"],
        rows,
        ["0.72in", "0.78in", "1.20in", "2.05in", "0.90in"],
        "FPTRANSA Accuracy Contracts",
    )


def latex_cpuid_feature_discovery_section(model: IsaModel) -> str:
    return render_latex_template(
        "cpuid_feature_discovery.tex",
        {
            "CPUID_INSTRUCTION_TABLE": latex_instruction_links(
                model, ["CPUID"], "The normative instruction entry is"
            ),
            "FPTRANSA_CONTRACT_TABLE": latex_fptransa_contract_table(model),
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
            "SAVE_RESTORE_INSTRUCTION_TABLE": latex_instruction_links(
                model, [row[0] for row in instruction_rows], "The normative instruction entries are"
            ),
        },
    )


def latex_data_formats_section(model: IsaModel) -> str:
    return render_latex_template("data_formats.tex", data_format_template_values(model))


def latex_instruction_word_formats_section(model: IsaModel) -> str:
    values = encoding_class_template_values(model)
    values["INSTRUCTION_PAYLOAD_ORDERING_SECTION"] = render_latex_template(
        "fragments/instruction_payload_ordering.tex",
        data_format_template_values(model),
    )
    return render_latex_template(
        "instruction_word_formats.tex",
        values,
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
    sreg_rows = [
        [reg.get("name", ""), bits_text(reg["sreg_encoding"], 3), reg.get("sreg_use", "")]
        for reg in sorted(
            (
                reg
                for reg in segment_data.get("segment_registers", []) or []
                if reg.get("sreg_encoding") is not None
            ),
            key=lambda reg: reg["sreg_encoding"],
        )
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
            "SREG_TABLE": latex_code_table(
                ["SREG", "Bits", "Use"],
                sreg_rows,
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
    ext0_section = render_latex_template("ext0_addressing_modes.tex", {})
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
    supervisor_control_flow_table = latex_instruction_links(
        model,
        ["SYSCALL", "SYSRET", "LRET", "ERET"],
        "Normative control-flow behavior is defined by",
    )
    return render_latex_template(
        "privileged_programming_model.tex",
        {"SUPERVISOR_CONTROL_FLOW_TABLE": supervisor_control_flow_table},
    )


def latex_exception_processing_section(model: IsaModel) -> str:
    exception_instruction_table = latex_instruction_links(
        model, ["BKPT", "ERET", "RESET"], "Related normative instruction entries are"
    )
    return render_latex_template(
        "interrupt_model.tex",
        {"EXCEPTION_INSTRUCTION_TABLE": exception_instruction_table},
    )


def instruction_label(mnemonic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", mnemonic.lower()).strip("-")
    return f"instr:{slug or 'unknown'}"


def instruction_details_tex(inst: InstructionDef) -> str:
    path = inst.details_path
    if not path.exists():
        return ""
    if not path.is_file():
        raise ValueError(f"{path}: expected a regular details.tex file")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"{path}: details.tex must not be empty")
    numbered_heading = re.search(r"\\(?:sub)*section\s*(?!\*)\{", text)
    toc_entry = re.search(r"\\addcontentsline\s*\{toc\}", text)
    forbidden_document_command = re.search(
        r"\\(?:input|include|documentclass)\b|\\begin\s*\{document\}|\\end\s*\{document\}",
        text,
    )
    if numbered_heading or toc_entry or forbidden_document_command:
        raise ValueError(f"{path}: details.tex contains a forbidden document-structure command")
    return text


def latex_instruction_summary_table(title: str, instructions: list[InstructionDef]) -> str:
    rows = []
    for inst in instructions:
        summary = compact_text(inst.doc.get("summary", "")) or compact_text(inst.doc.get("title", inst.mnemonic))
        rows.append(
            [
                rf"\manualsummarymnemonic{{{instruction_label(inst.mnemonic)}}}{{{latex_escape(inst.mnemonic)}}}",
                latex_escape(summary),
            ]
        )
    return latex_longtable(
        ["Mnemonic", "Brief description"],
        rows,
        ["1.05in", "4.35in"],
        title,
    )


def latex_instruction_entry(model: IsaModel, inst: InstructionDef, *, first_in_group: bool = False) -> str:
    parts: list[str] = [r"\Needspace{5.5in}" if first_in_group else r"\clearpage"]
    title = compact_text(inst.doc.get("title", inst.mnemonic)) or inst.mnemonic
    parts.append(
        rf"\begin{{manualinstruction}}{{{latex_escape(inst.mnemonic)}}}{{{latex_escape(title)}}}{{{instruction_label(inst.mnemonic)}}}"
    )
    description = compact_text(inst.doc.get("description", ""))
    if not description:
        raise ValueError(f"{inst.path}: doc.description must be a non-empty string")
    parts.append(latex_instruction_field("Description", latex_escape(description)))
    syntax_lines = assembler_syntax_lines(model, inst)
    if syntax_lines:
        parts.append(
            latex_instruction_field(
                "Assembler Syntax",
                latex_ragged_block([tex_code(line) for line in syntax_lines]),
            )
        )
    parts.append(latex_instruction_field("Attributes", latex_attributes_block(inst, model)))
    status = latex_flag_status(inst)
    if status:
        parts.append(status)
    approximation = latex_approximation_field(inst)
    if approximation:
        parts.append(approximation)
    constant_ids = latex_instruction_constant_ids(inst)
    if constant_ids:
        parts.append(constant_ids)
    details_tex = instruction_details_tex(inst)
    if details_tex:
        parts.append(r"\manualinstructiondescriptionheading{Detailed Semantics}")
        parts.append(details_tex)
    forms_block = latex_instruction_forms_block(model, inst)
    if forms_block:
        parts.append(forms_block)
    parts.append(r"\end{manualinstruction}")
    return "\n".join(parts)


def latex_reading_instruction_description_section() -> str:
    return render_latex_template("instruction_description_intro.tex")


def latex_instruction_reference_section(model: IsaModel, instructions: list[InstructionDef]) -> str:
    parts: list[str] = [latex_reading_instruction_description_section()]
    for set_name, title, group in instruction_set_groups(instructions):
        parts.append(str(LatexTopSection(title)))
        intro_template = INSTRUCTION_SET_SECTION_INTRO_TEMPLATES.get(set_name)
        if intro_template:
            parts.append(render_latex_template(intro_template))
        parts.extend(
            [
                r"\subsection{Summary}",
                latex_instruction_summary_table(f"{title} Summary", group),
            ]
        )
        parts.extend(
            latex_instruction_entry(model, inst, first_in_group=index == 0)
            for index, inst in enumerate(group)
        )
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
