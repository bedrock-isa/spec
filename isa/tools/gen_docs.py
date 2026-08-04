#!/usr/bin/env python3
"""Generate draft ISA reference documents from rewrite YAML sources."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
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
    namespace_size,
    parse_range,
)
from alloc_notes import allocation_form_text  # noqa: E402
from defs_loader import (  # noqa: E402
    load_extensions,
    load_instruction_sets,
    load_operand_types,
    load_register_groups,
    load_size_definitions,
    load_yaml,
)
from artifact_overlay import read_source, resolve_source  # noqa: E402
from validate_isa import allocation_mnemonic  # noqa: E402
from encoding_store import allocation_entry_dict, load_encoding_store  # noqa: E402
from encoding_architecture import (  # noqa: E402
    ARCHITECTURE_SOURCE_PATH,
    ENCODING_CLASSES,
    EXTENDED_BYTE1_PATTERN,
    EXTRASHORT_BYTE0_PATTERN,
    SHORT_BYTE0_PATTERN,
    extended_instruction_lengths,
    extended_length_byte0_pattern,
)
from defs_schema import FLAG_BANKS, decode_instruction  # noqa: E402
from validate_reference_navigation import validate_path as load_reference_navigation  # noqa: E402
from latex_builder.common import (  # noqa: E402
    LatexTopSection,
    TextTex,
    TrustedRawTex,
    latex_longtable,
    latex_tabular,
    render_latex_template as render_typed_latex_template,
    tex_code,
    tex_escape as latex_escape,
)


ROOT = Path(__file__).resolve().parents[2]
DEF_ROOT = ROOT / "isa" / "defs"
EA_FRAGMENT_DIR = ROOT / "isa" / "tools" / "latex_builder" / "templates" / "fragments"
INSTRUCTION_FILENAME = "instruction.yaml"
CONFORMANCE_MANIFEST_PATH = ROOT / "isa" / "reference" / "conformance_manifest.yaml"
ARCHITECTURE_TABLES_PATH = ROOT / "isa" / "reference" / "architecture_tables.yaml"
REFERENCE_NAVIGATION_PATH = ROOT / "isa" / "reference" / "reference_navigation.yaml"


def render_latex_template(
    name: str,
    values: dict[str, Any] | None = None,
) -> str:
    """Render generator-owned TeX fragments through the explicit trusted boundary."""
    typed_values: dict[str, TextTex | TrustedRawTex] = {}
    for key, value in (values or {}).items():
        if isinstance(value, str):
            typed_values[key] = TrustedRawTex(value)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            typed_values[key] = TextTex(value)
        else:
            raise TypeError(
                f"{name}: template value {key} must be rendered TeX or a text scalar"
            )
    return render_typed_latex_template(name, typed_values)


@dataclass(frozen=True)
class InstructionDef:
    path: Path
    instruction_set: str
    mnemonic: str
    data: dict[str, Any]

    @property
    def doc(self) -> dict[str, Any]:
        attributes = self.attributes
        return {
            "title": self.data["title"],
            "summary": self.data["summary"],
            "description": self.data["description"],
            "instruction_class": attributes["class"],
            "instruction_family": attributes["family"],
        }

    @property
    def attributes(self) -> dict[str, Any]:
        value = self.data.get("attributes")
        return value if isinstance(value, dict) else {}

    @property
    def details_path(self) -> Path | None:
        relative = self.data.get("additional_description")
        return self.path.parent / relative if isinstance(relative, str) else None

    @property
    def additional_assembler_syntax(self) -> list[str]:
        value = self.data.get("additional_assembler_syntax", [])
        return list(value) if isinstance(value, list) else []

    @property
    def flag_effects(self) -> dict[str, dict[str, str]]:
        value = self.data.get("flag_effects")
        if not isinstance(value, dict):
            return {}
        return {
            str(bank): {
                str(flag): str(effect)
                for flag, effect in effects.items()
                if isinstance(flag, str) and isinstance(effect, str)
            }
            for bank, effects in value.items()
            if isinstance(bank, str) and isinstance(effects, dict)
        }


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
    destination_overlap: list[dict[str, Any]] = field(default_factory=list)
    operands: tuple[dict[str, Any], ...] = ()
    sizes: tuple[str, ...] = ()
    instruction_bytes: int | None = None

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
    metadata: dict[str, Any]
    instructions: list[InstructionDef]
    allocation_classes: list[AllocationClass]
    allocated_by_mnemonic: dict[str, list[AllocationEntry]]


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


def instruction_definition_paths(defs_root: Path) -> list[tuple[str, Path]]:
    extensions = load_extensions(defs_root)

    paths: list[tuple[str, Path]] = []
    for instruction_set in load_instruction_sets(defs_root, extensions):
        name = instruction_set.name
        include = instruction_set.include
        data = load_yaml(include)
        if not isinstance(data, dict):
            raise ValueError(f"{include}: expected mapping")
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
    for instruction_set, path in instruction_definition_paths(defs_root):
        data = load_yaml(path)
        decoded = decode_instruction(path, data)
        mnemonic = decoded.mnemonic
        if path.parent.name != str(mnemonic):
            raise ValueError(
                f"{path}: directory name {path.parent.name!r} does not match mnemonic {mnemonic!r}"
            )
        instructions.append(InstructionDef(path, instruction_set, str(mnemonic), data))
    return instructions


def load_allocations(defs_root: Path) -> list[AllocationClass]:
    store = load_encoding_store(defs_root)
    classes: list[AllocationClass] = []
    for encoding_class in store.classes:
        namespaces = list(encoding_class.namespace)
        entries: list[AllocationEntry] = []
        skipped = Counter()
        overlaps: list[str] = []
        by_value: dict[int, str] = {}
        assigned_values: set[int] = set()
        for located in store.for_class(encoding_class.name):
            raw = allocation_entry_dict(located, store.field_types)
            claims, entry_skipped = entry_claims(
                located.path,
                encoding_class.payload_bits,
                namespaces,
                raw,
            )
            skipped.update(entry_skipped)
            for value, claim in claims:
                previous = by_value.get(value)
                if previous is not None:
                    overlaps.append(
                        f"0x{value:x}: {previous} overlaps {claim.entry_id}"
                    )
                else:
                    by_value[value] = claim.entry_id
                    assigned_values.add(value)
            entries.append(
                AllocationEntry(
                    path=located.path,
                    cls=encoding_class.name,
                    payload_bits=encoding_class.payload_bits,
                    entry_id=located.form.id,
                    bits=compact_bits(located.form.bits),
                    text=located.form.syntax,
                    assigned=len(claims),
                    skipped=sum(entry_skipped.values()),
                    fields=raw["fields"],
                    constraints=raw["constraints"],
                    destination_overlap=raw.get("destination_overlap", []),
                    operands=tuple(
                        {
                            "name": operand.name,
                            "type": operand.type,
                            "access": operand.access,
                            **({"field": operand.field} if operand.field else {}),
                            **({"domain": operand.domain} if operand.domain else {}),
                            **({"ea_role": operand.ea_role} if operand.ea_role else {}),
                            **({"ea_width": operand.ea_width} if operand.ea_width else {}),
                        }
                        for operand in located.form.operands
                    ),
                    sizes=located.form.sizes,
                    instruction_bytes=encoding_class.instruction_bytes,
                )
            )
        total = namespace_size(namespaces)
        classes.append(
            AllocationClass(
                path=ARCHITECTURE_SOURCE_PATH,
                cls=encoding_class.name,
                payload_bits=encoding_class.payload_bits,
                summary={
                    "total": total,
                    "allocated": len(assigned_values),
                    "reserved_total": total - len(assigned_values),
                    "claimed": len(by_value),
                    "constraint_skipped": sum(skipped.values()),
                },
                skipped_by_reason=skipped,
                overlaps=overlaps,
                entries=entries,
            )
        )
    return classes


def load_metadata(defs_root: Path) -> dict[str, Any]:
    names = [
        "conditions",
        "ea",
    ]
    out: dict[str, Any] = {}
    for name in names:
        path = defs_root / f"{name}.yaml"
        if path.exists():
            out[name] = load_yaml(path)
    extensions = load_extensions(defs_root)
    out["instruction_sets"] = [
        {
            "name": item.name,
            "title": item.title,
            "introduction": item.introduction,
        }
        for item in load_instruction_sets(defs_root, extensions)
    ]
    out["operand_types"] = load_operand_types(defs_root, extensions)
    out["sizes"] = load_size_definitions(defs_root, extensions)
    out["extensions"] = {
        name: extension.data
        for name, extension in extensions.items()
    }
    out["registers"] = {"registers": load_register_groups(defs_root, extensions)}
    return out


def load_model(defs_root: Path) -> IsaModel:
    instructions = load_instructions(defs_root)
    allocation_classes = load_allocations(defs_root)
    allocated_by_mnemonic: dict[str, list[AllocationEntry]] = defaultdict(list)
    for cls in allocation_classes:
        for entry in cls.entries:
            mnemonic = entry.mnemonic
            if mnemonic:
                allocated_by_mnemonic[mnemonic].append(entry)
    return IsaModel(
        defs_root=defs_root,
        metadata=load_metadata(defs_root),
        instructions=instructions,
        allocation_classes=allocation_classes,
        allocated_by_mnemonic=dict(sorted(allocated_by_mnemonic.items())),
    )


def instruction_family(instruction: InstructionDef) -> str:
    return label_text(instruction.doc.get("instruction_family", "-")) or "-"


def instruction_class(instruction: InstructionDef) -> str:
    return label_text(instruction.doc.get("instruction_class", "-")) or "-"


def instruction_feature(model: IsaModel, inst: InstructionDef) -> str:
    extension = (model.metadata.get("extensions") or {}).get(inst.instruction_set)
    if not isinstance(extension, dict):
        return ""
    availability = extension.get("availability")
    cpuid = availability.get("cpuid") if isinstance(availability, dict) else None
    return compact_text(cpuid.get("feature")) if isinstance(cpuid, dict) else ""


def instruction_repeat_contract(inst: InstructionDef) -> dict[str, Any] | None:
    repeat = inst.data.get("repeat")
    return repeat if isinstance(repeat, dict) else None


def instruction_set_groups(
    model: IsaModel,
    instructions: list[InstructionDef],
) -> list[tuple[str, str, Path | None, list[InstructionDef]]]:
    by_set: dict[str, list[InstructionDef]] = defaultdict(list)
    for inst in instructions:
        by_set[inst.instruction_set].append(inst)

    definitions = model.metadata.get("instruction_sets") or []
    groups: list[tuple[str, str, Path | None, list[InstructionDef]]] = []
    declared: set[str] = set()
    for item in definitions:
        name = str(item["name"])
        if name not in by_set:
            continue
        declared.add(name)
        introduction = item.get("introduction")
        groups.append((name, str(item["title"]), introduction, by_set[name]))
    missing = set(by_set) - declared
    if missing:
        raise ValueError(f"instruction sets lack index metadata: {sorted(missing)}")
    return groups


def data_format_template_values(model: IsaModel) -> dict[str, Any]:
    sizes = model.metadata.get("sizes") or {}
    size_codes = sizes.get("size_codes") or {}
    values: dict[str, Any] = {}
    for code in ("B", "W", "L", "Q", "S", "D"):
        body = size_codes.get(code)
        if not isinstance(body, dict):
            continue
        byte_count = int(body.get("bytes", 0) or 0)
        values[f"{code}_SUFFIX"] = body.get("suffix", f".{code}")
        values[f"{code}_BITS"] = byte_count * 8
        values[f"{code}_BYTES"] = byte_count
    operand_types = model.metadata.get("operand_types") or {}
    for name in ("pair_id", "pt_level", "flags_bitmap", "imm6", "imm7"):
        spec = operand_types.get(name)
        if not isinstance(spec, dict):
            continue
        key = str(name).upper()
        field_width = int(spec.get("field_width", 0) or 0)
        values[f"{key}_WIDTH"] = field_width
        if name == "imm6":
            values["IMM6_EXTENSION_THRESHOLD"] = field_width
        enum_values = [
            item.get("value")
            for item in (spec.get("values") or [])
            if isinstance(item, dict) and isinstance(item.get("value"), int)
        ]
        if enum_values:
            values[f"{key}_RANGE"] = f"{min(enum_values)}..{max(enum_values)}"
        elif field_width <= 0:
            values[f"{key}_RANGE"] = "-"
        elif spec.get("signed"):
            values[f"{key}_RANGE"] = (
                f"{-1 << (field_width - 1)}..{(1 << (field_width - 1)) - 1}"
            )
        else:
            values[f"{key}_RANGE"] = f"0..{(1 << field_width) - 1}"
    return values


def encoding_architecture_template_values() -> dict[str, str]:
    length_rows = [
        rf"\texttt{{{EXTRASHORT_BYTE0_PATTERN}}} & -- & 1\\",
        rf"\texttt{{{SHORT_BYTE0_PATTERN}}} & \texttt{{xxxxxxxx}} & 2\\",
    ]
    length_rows.extend(
        rf"\texttt{{{extended_length_byte0_pattern(instruction_bytes)}}} & "
        rf"\texttt{{{EXTENDED_BYTE1_PATTERN}}} & {instruction_bytes}\\"
        for instruction_bytes in extended_instruction_lengths()
    )

    class_rows = []
    namespace_rows = []
    for encoding_class in ENCODING_CLASSES:
        if not encoding_class.selectors:
            namespace_rows.append(
                rf"\manualformatrow{{{encoding_class.name}}}{{%" "\n"
                rf"\manualformatfield{{payload}}"
                rf"{{{encoding_class.payload_bits}}}" "\n"
                "}"
            )
        if encoding_class.name == "extrashort":
            selection = rf"\texttt{{{EXTRASHORT_BYTE0_PATTERN}}}"
            validity = "exactly 1 byte"
        elif encoding_class.name == "short":
            selection = rf"\texttt{{{SHORT_BYTE0_PATTERN}}}"
            validity = "exactly 2 bytes"
        else:
            selection = ", ".join(
                rf"\texttt{{{selector}}}" for selector in encoding_class.selectors
            )
            validity = (
                "any extended instruction length"
                if encoding_class.instruction_bytes == 3
                else f"instruction length at least {encoding_class.instruction_bytes} bytes"
            )
        class_rows.append(
            rf"\texttt{{{encoding_class.name}}} & {encoding_class.payload_bits} & "
            rf"{selection} & {encoding_class.instruction_bytes} & {validity}\\"
        )

        for selector in encoding_class.selectors:
            group = (
                f" group {encoding_class.selectors.index(selector)}"
                if len(encoding_class.selectors) > 1
                else ""
            )
            selector_macro = (
                "manualformatfieldcode" if "x" in selector else "manualformatfixed"
            )
            suffix_bits = encoding_class.payload_bits - len(selector)
            namespace_rows.append(
                rf"\manualformatrow{{{encoding_class.name}{group}}}{{%" "\n"
                rf"\{selector_macro}{{{selector}}}{{{len(selector)}}}" "\n"
                rf"\manualformatfield{{payload}}"
                rf"{{{suffix_bits}}}" "\n"
                "}"
            )

    return {
        "INSTRUCTION_LENGTH_TRUTH_TABLE_ROWS": "\n".join(length_rows),
        "ENCODING_CLASS_SUMMARY_ROWS": "\n".join(class_rows),
        "OPCODE_PAYLOAD_NAMESPACE_ROWS": "\n".join(namespace_rows),
    }


def form_allows_memory_memory(operands: Any) -> bool:
    return sum(
        isinstance(operand, dict) and operand.get("type") == "EA"
        for operand in operands
    ) >= 2


def memory_memory_instruction_names(model: IsaModel) -> list[str]:
    return [
        inst.mnemonic
        for inst in model.instructions
        if any(
            form_allows_memory_memory(entry.operands)
            for entry in model.allocated_by_mnemonic.get(inst.mnemonic, [])
        )
    ]


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
    feature = instruction_feature(model, inst)
    if feature:
        lines.append(rf"{latex_escape('Feature')} = {tex_code(feature)}")
    repeat = instruction_repeat_contract(inst)
    if repeat:
        contexts = repeat.get("contexts") or []
        lines.append(
            rf"{latex_escape('Repeat')} = "
            + ", ".join(tex_code(str(context)) for context in contexts)
        )
        observed = repeat.get("observed")
        if isinstance(observed, dict):
            kind = str(observed.get("kind"))
            operand = observed.get("operand")
            value = tex_code(kind)
            if operand:
                value += " " + tex_code(str(operand))
            lines.append(rf"{latex_escape('REPcc observation')} = {value}")
    else:
        lines.append(rf"{latex_escape('Repeat')} = {tex_code('none')}")
    return latex_ragged_block(lines)


def instruction_uses_operand_type(
    model: IsaModel,
    inst: InstructionDef,
    operand_type: str,
) -> bool:
    return any(
        operand.get("type") == operand_type
        for entry in model.allocated_by_mnemonic.get(inst.mnemonic, [])
        for operand in entry.operands
        if isinstance(operand, dict)
    )


def latex_instruction_operand_value_tables(
    model: IsaModel,
    inst: InstructionDef,
) -> str:
    """Render rich enum operands without instruction-specific generator code."""
    operands_by_type: dict[str, str] = {}
    for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
        for operand in entry.operands:
            operand_type = str(operand.get("type", ""))
            operand_name = str(operand.get("name", operand_type))
            if operand_type:
                operands_by_type.setdefault(operand_type, operand_name)

    tables: list[str] = []
    registry = model.metadata.get("operand_types") or {}
    for operand_type, operand_name in operands_by_type.items():
        spec = registry.get(operand_type)
        if not isinstance(spec, dict):
            continue
        values = spec.get("values")
        if not isinstance(values, list) or not values:
            continue
        if not all(isinstance(item, dict) and "value_bits" in item for item in values):
            continue

        rows: list[list[str]] = []
        seen_ids: set[str] = set()
        for index, item in enumerate(values):
            value = compact_text(item.get("value"))
            name = compact_text(item.get("name"))
            value_bits = compact_text(item.get("value_bits"))
            if not value or not name or not value_bits:
                raise ValueError(
                    f"{operand_type}.values[{index}] requires value, name, and value_bits"
                )
            if value in seen_ids:
                raise ValueError(f"{inst.path}: duplicate {operand_type} value {value}")
            seen_ids.add(value)
            rows.append([tex_code(value), latex_escape(display_text(name)), tex_code(value_bits)])

        display_name = " ".join(
            "ID" if part.lower() == "id" else part.capitalize()
            for part in display_text(operand_name).split()
        )
        if not display_name.endswith("s"):
            display_name += "s"
        title = f"{inst.mnemonic} {display_name}"
        result_format = compact_text(spec.get("result_bits_format", ""))
        if result_format:
            title += f" ({result_format})"
        tables.append(
            latex_longtable(
                ["ID", "Constant", "Result bits"],
                rows,
                ["0.75in", "2.35in", "2.30in"],
                title,
            )
        )
    return "\n".join(tables)


def assembler_syntax_lines(model: IsaModel, inst: InstructionDef) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for entry in model.allocated_by_mnemonic.get(inst.mnemonic, []):
        form = allocation_form_text(entry.text)
        if form and form not in seen:
            lines.append(form)
            seen.add(form)
    for syntax in inst.additional_assembler_syntax:
        if syntax not in seen:
            lines.append(syntax)
            seen.add(syntax)
    return lines


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


def ea_operand_role(entry: AllocationEntry, symbol: str, fallback: str) -> str:
    for operand in entry.operands:
        if operand.get("field") != symbol or operand.get("type") != "EA":
            continue
        role = operand.get("ea_role")
        if role == "address":
            return "address operand"
        if role == "control_target":
            return "control target"
        access = operand.get("access")
        if access == "read":
            return "source operand"
        if access == "write":
            return "destination operand"
        if access == "read_write":
            return "read/write operand"
    return fallback


def allocation_opcode_bytes(entry: AllocationEntry) -> int:
    if entry.instruction_bytes is None:
        raise ValueError(f"{entry.entry_id}: encoding class lacks instruction_bytes")
    return entry.instruction_bytes


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
    payloads = ea_data.get("payloads") or {}
    sizes: dict[str, int] = {}
    for name, spec in payloads.items():
        if not isinstance(spec, dict) or "field_width" not in spec:
            raise ValueError(f"invalid EA payload definition: {name!r}")
        field_width = int(spec["field_width"])
        if field_width <= 0 or field_width % 8:
            raise ValueError(f"EA payload {name!r} must have a positive byte-aligned field width")
        sizes[str(name)] = field_width // 8

    ext0 = ea_data.get("ext0") or {}
    descriptor_sizes = {
        len(form.get("pattern") or [])
        for form in (ext0.get("forms") or [])
        if isinstance(form, dict) and isinstance(form.get("pattern"), list) and form.get("pattern")
    }
    if not descriptor_sizes:
        descriptor_sizes = {1}

    compact = ea_data.get("compact") or {}
    lengths: set[int] = set()
    for form in compact.get("forms", []) or []:
        if not isinstance(form, dict):
            continue
        payload_bytes = named_payload_bytes(form.get("payload"), sizes)
        if form.get("kind") == "escape":
            lengths.update(size + payload_bytes for size in descriptor_sizes)
            continue
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
            out.append((bit_label(chunk), len(chunk)))
            start = index
            current = cls
    chunk = bits[start:]
    out.append((bit_label(chunk), len(chunk)))
    return out


# Eight encoded bytes plus seven one-bit gutters fit the fixed-width manual body.
MAX_INSTRUCTION_BYTES_PER_DIAGRAM_ROW = 8


def instruction_byte_row_segments(
    byte_index: int,
    byte_segments: list[list[tuple[str, int]]],
) -> str:
    if not 1 <= len(byte_segments) <= MAX_INSTRUCTION_BYTES_PER_DIAGRAM_ROW:
        raise ValueError(
            f"instruction diagram row at byte {byte_index} contains {len(byte_segments)} bytes; "
            f"expected 1-{MAX_INSTRUCTION_BYTES_PER_DIAGRAM_ROW}"
        )

    def field(text: str, width: int) -> str:
        if set(text) <= {"0", "1"}:
            macro = "manualbitfixed"
        elif set(text) <= {"-"}:
            macro = "manualbitreserved"
        else:
            macro = "manualbitvariable"
        return rf"\{macro}{{{latex_escape(text)}}}{{{width}}}"

    fields: list[str] = []
    for row_byte_index, segments in enumerate(byte_segments):
        if row_byte_index:
            fields.append(r"\manualbitgap{1}")
        fields.extend(field(text, width) for text, width in segments if width > 0)
    labels = rf"\manualbyterowlabels{{{byte_index}}}{{{len(byte_segments)}}}"
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
            byte_segments[index : index + MAX_INSTRUCTION_BYTES_PER_DIAGRAM_ROW],
        )
        for index in range(0, len(byte_segments), MAX_INSTRUCTION_BYTES_PER_DIAGRAM_ROW)
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

    if symbol == "o" and instruction_uses_operand_type(model, inst, "memory_order"):
        memory_order = (model.metadata.get("operand_types") or {}).get("memory_order") or {}
        names = {
            int(item["value"]): display_text(item["name"])
            for item in memory_order.get("values") or []
            if isinstance(item, dict) and "value" in item and "name" in item
        }
        if allowed <= names.keys():
            return ", ".join(names[value] for value in sorted(allowed))

    return decimal_value_ranges(allowed)


@dataclass(frozen=True)
class CompactEaDisplayRow:
    syntax: str
    kind: str
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
    compact = ea_data.get("compact") or {}
    for item in compact.get("forms", []) or []:
        if not isinstance(item, dict):
            continue
        bits = compact_bits(str(item.get("pattern", "")))
        syntax = compact_text(item.get("syntax"))
        kind = compact_text(item.get("kind"))
        if len(bits) != 7 or ".." in bits or not syntax:
            raise ValueError(f"invalid compact EA display form: bits={bits!r}, syntax={syntax!r}")
        rows.append(
            CompactEaDisplayRow(
                syntax=syntax,
                kind=kind,
                mode_bits=bits[:3],
                form_bits=bits[3:],
                values=frozenset(expand_pattern(bits)),
            )
        )
    if not rows:
        raise ValueError("EA metadata defines no displayable compact EA forms")
    return rows


def compact_ea_category(kind: str) -> str:
    categories = {
        "register": "Register",
        "memory": "Memory",
        "immediate": "Immediate",
        "escape": "EXT0",
    }
    try:
        return categories[kind]
    except KeyError as exc:
        raise ValueError(f"uncategorized compact EA kind: {kind!r}") from exc


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
        members = tuple(row.syntax for row in rows if compact_ea_category(row.kind) == name)
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
    for category in summary.categories:
        if category.mode == "all":
            allowed_terms.append(category.name)
        elif category.mode == "except":
            allowed_terms.append(f"{category.name} except {latex_ea_syntax_list(category.exceptions)}")
        elif category.mode == "only":
            allowed_terms.append(f"{category.name} only {latex_ea_syntax_list(category.exceptions)}")
    return rf"\manualeasummary{{{'; '.join(allowed_terms) or 'none'}}}"


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
        fallback = operand_role(operand[0], operand_count) if operand else "operand"
        role = ea_operand_role(entry, symbol, fallback)
        fields.append((symbol, role))
    return fields


def latex_ea_addressing_mode_tables(model: IsaModel, entry: AllocationEntry, symbol: str) -> str:
    return latex_ea_availability_summary(ea_availability_summary(model, entry, symbol))


def field_description_label(
    model: IsaModel,
    symbol: str,
    spec: dict[str, Any],
    inst: InstructionDef,
) -> str:
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
    elif symbol == "o" and instruction_uses_operand_type(model, inst, "memory_order"):
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
    fallback = operand_role(operand[0], len(split_form_operands(form))) if operand else ""
    role = ea_operand_role(entry, symbol, fallback)
    kind = spec.get("kind")
    values = field_constraint_values(model, inst, entry, symbol, spec)
    if kind == "size":
        choices = "/".join(str(item) for item in spec.get("size_choices", []))
        return latex_escape(f"Selects {choices}." if choices else "Selects the operand size.")
    if kind == "ea7":
        target = f"the {role}" if role else "the operand"
        return latex_escape(f"Specifies {target}.")
    if kind in {"rn", "freg", "vreg", "creg", "sreg"}:
        target = f"the {role}" if role else "a register operand"
        return latex_escape(f"Selects {target}.")
    if kind == "condition":
        text = "Selects the condition code."
    elif kind == "immediate":
        text = "Encodes the immediate value."
    elif symbol == "o" and instruction_uses_operand_type(model, inst, "memory_order"):
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
            r"The selected length must cover all required bytes; trailing bytes are uninterpreted padding.}"
        )
    for symbol, spec in ordered_entry_fields(entry):
        if spec.get("kind") == "ea7":
            parts.append(r"\Needspace{1.15in}")
        parts.append(
            rf"\manualinstructionfielddescription{{{field_description_label(model, symbol, spec, inst)}}}"
            rf"{{{field_description_text(model, inst, entry, form, symbol, spec)}}}"
        )
        if spec.get("kind") == "ea7":
            parts.append(latex_ea_addressing_mode_tables(model, entry, symbol))
    for relation in entry.destination_overlap:
        operands = relation.get("operands") or []
        if len(operands) != 2:
            continue
        pair = f"{operands[0]} = {operands[1]}"
        if relation.get("rule") == "same_value":
            meaning = (
                f"When {pair} designate the same architectural register, "
                "the final value equals that register's initial value."
            )
        else:
            meaning = (
                f"When {pair} designate the same architectural register, "
                "the instruction raises ILLEGAL_INSTRUCTION.INVALID_OPERAND_RELATION "
                "before architectural effects."
            )
        parts.append(
            rf"\manualinstructionfielddescription{{Destination overlap}}"
            rf"{{{latex_escape(meaning)}}}"
        )
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
            "CONFORMANCE_SECTION": latex_conformance_section(),
            "CPUID_SECTION": latex_cpuid_feature_discovery_section(model),
            "SAVE_RESTORE_SECTION": latex_save_restore_section(),
            "DATA_FORMATS_SECTION": latex_data_formats_section(model),
            "CONDITION_CODES_SECTION": latex_condition_section(model),
            "CONDITION_CODE_COMPUTATION_SECTION": latex_condition_code_computation_section(),
            "EFFECTIVE_ADDRESS_SECTION": latex_ea_section(model),
            "PRIVILEGED_PROGRAMMING_SECTION": latex_privileged_programming_model_section(),
            "EXCEPTION_PROCESSING_SECTION": latex_exception_processing_section(),
            "INSTRUCTION_WORD_FORMATS_SECTION": latex_instruction_word_formats_section(model),
            "EXECUTION_MODEL_SECTION": latex_execution_model_section(model),
            "STREAMING_EXECUTION_SECTION": latex_streaming_model_section(),
            "INSTRUCTION_REFERENCE_SECTION": latex_instruction_reference_section(model, instructions),
            "REFERENCE_NAVIGATION_SECTION": latex_reference_navigation_section(
                model, instructions
            ),
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


def extension_directory_entries(model: IsaModel) -> list[tuple[int, int, int, int, str, str]]:
    entries: list[tuple[int, int, int, int, str, str]] = []
    for qualified_name, extension in (model.metadata.get("extensions") or {}).items():
        if not isinstance(extension, dict):
            continue
        availability = extension.get("availability")
        cpuid = availability.get("cpuid") if isinstance(availability, dict) else None
        if not isinstance(cpuid, dict):
            continue
        entries.append(
            (
                int(cpuid["class"]),
                int(cpuid["leaf"]),
                int(cpuid["index"]),
                int(cpuid["bit"]),
                str(cpuid["feature"]),
                qualified_name,
            )
        )
    if not entries:
        raise ValueError("no extension CPUID availability entries are defined")
    entries.sort(key=lambda entry: entry[:4])
    return entries


def latex_extension_directory_diagram(model: IsaModel) -> str:
    grouped: dict[tuple[int, int, int], list[tuple[int, str]]] = {}
    for class_id, leaf_id, index, bit, feature, _qualified_name in extension_directory_entries(model):
        grouped.setdefault((class_id, leaf_id, index), []).append((bit, feature))

    lines = [r"\begin{manuallistedformatdiagram}{Optional-Extension Directory Result}"]
    for (_class_id, _leaf_id, index), fields in sorted(grouped.items()):
        cursor = 63
        lines.append(rf"\manualformatrowrange{{index {index}}}{{63}}{{0}}{{%")
        for bit, feature in sorted(fields, reverse=True):
            if bit > cursor or bit < 0:
                raise ValueError(f"invalid extension CPUID feature bit {bit}")
            if cursor > bit:
                lines.append(rf"\manualformatreserved{{reserved}}{{{cursor - bit}}}")
            # Feature names live in the table immediately below the diagram.
            # One-bit cells stay unlabeled so every diagram can use the same
            # fixed physical width per bit without text overlapping neighbors.
            lines.append(r"\manualformatfield{}{1}")
            cursor = bit - 1
        if cursor >= 0:
            lines.append(rf"\manualformatreserved{{reserved}}{{{cursor + 1}}}")
        lines.append("}")
    lines.append(r"\end{manuallistedformatdiagram}")
    return "\n".join(lines)


def latex_extension_directory_table(model: IsaModel) -> str:
    rows = [
        [
            f"0x{class_id:08x}",
            f"0x{leaf_id:04x}",
            str(index),
            str(bit),
            feature,
            qualified_name,
        ]
        for class_id, leaf_id, index, bit, feature, qualified_name in extension_directory_entries(model)
    ]
    return latex_code_table(
        ["Class", "Leaf", "Index", "Bit", "Feature", "Extension"],
        rows,
        ["0.75in", "0.55in", "0.45in", "0.35in", "0.80in", "2.10in"],
        "Optional-Extension Feature Bits",
        {0, 1, 2, 3, 4},
    )


def latex_cpuid_feature_discovery_section(model: IsaModel) -> str:
    return render_latex_template(
        "cpuid_feature_discovery.tex",
        {
            "EXTENSION_DIRECTORY_DIAGRAM": latex_extension_directory_diagram(model),
            "EXTENSION_DIRECTORY_TABLE": latex_extension_directory_table(model),
        },
    )


def latex_save_restore_section() -> str:
    return render_latex_template("save_restore_area.tex", {})


def latex_conformance_section() -> str:
    document = load_yaml(CONFORMANCE_MANIFEST_PATH)
    items = document.get("implementation_defined") if isinstance(document, dict) else None
    if not isinstance(items, list):
        raise ValueError(
            f"{CONFORMANCE_MANIFEST_PATH}: expected implementation_defined list"
        )
    rows: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(
                f"{CONFORMANCE_MANIFEST_PATH}: implementation_defined[{index}] "
                "must be a mapping"
            )
        rows.append(
            " & ".join(
                [
                    tex_code(item.get("id", "")),
                    latex_escape(item.get("definition", "")),
                    latex_escape(item.get("publication", "")),
                ]
            )
            + r"\\"
        )
    return render_latex_template(
        "conformance.tex",
        {"IMPLEMENTATION_DEFINED_ROWS": "\n".join(rows)},
    )


def navigation_link(anchor: str, text: str = "definition") -> str:
    return (
        rf"\hyperref[{anchor}]{{{latex_escape(text)}}} "
        rf"(p.~\pageref{{{anchor}}})"
    )


def navigation_code_link(anchor: str, text: str) -> str:
    code = ", ".join(
        tex_breakable_code(part) for part in text.split(", ")
    )
    return (
        rf"\hyperref[{anchor}]{{{code}}} "
        rf"(p.~\pageref{{{anchor}}})"
    )


def architecture_table_data() -> dict[str, Any]:
    data = load_yaml(ARCHITECTURE_TABLES_PATH)
    if not isinstance(data, dict):
        raise ValueError(f"{ARCHITECTURE_TABLES_PATH}: expected mapping")
    return data


def canonical_field_index(navigation: dict[str, Any]) -> str:
    rows = [
        [
            tex_code(group["owner"]),
            ", ".join(tex_code(field) for field in group["fields"]),
            navigation_link(group["definition"]),
        ]
        for group in navigation["canonical_field_groups"]
    ]
    return latex_longtable(
        ["Owner", "Canonical fields", "Normative definition"],
        rows,
        ["1.15in", "2.90in", "1.30in"],
        "Canonical Field Names",
        style="dense",
    )


def reset_value_map(architecture: dict[str, Any]) -> dict[str, str]:
    values: dict[str, str] = {}
    for row in architecture["reset_state"]:
        for state in row["state"]:
            name = str(state)
            if name == "F0_F15":
                for index in range(16):
                    values[f"F{index}"] = str(row["value"])
            else:
                values[name] = str(row["value"])
    return values


def grouped_reset_text(members: list[str], reset_values: dict[str, str]) -> str:
    grouped: dict[str, list[str]] = defaultdict(list)
    for member in members:
        grouped[reset_values.get(member, "not listed")].append(member)
    if len(grouped) == 1:
        return tex_breakable_code(next(iter(grouped)))
    return "; ".join(
        tex_breakable_code(f"{', '.join(names)}={value}")
        for value, names in grouped.items()
    )


def state_member_text(members: list[str]) -> str:
    for prefix in ("R", "F"):
        expected = [f"{prefix}{index}" for index in range(16)]
        if members == expected:
            return f"{prefix}0--{prefix}15"
    return ", ".join(members)


def state_index_rows(
    navigation: dict[str, Any],
    architecture: dict[str, Any],
) -> list[list[str]]:
    reset_values = reset_value_map(architecture)
    rows: list[list[str]] = []
    for group in navigation["state_groups"]:
        members = list(group["members"])
        fields = list(group["fields"])
        state_text = state_member_text(members)
        rows.append(
            [
                navigation_code_link(group["definition"], state_text),
                ", ".join(tex_code(field) for field in fields) or "--",
                latex_escape(group["readers"]),
                latex_escape(group["writers"]),
                grouped_reset_text(members, reset_values),
            ]
        )

    field_groups = {
        item["owner"]: item["fields"]
        for item in navigation["canonical_field_groups"]
    }
    for control in architecture["control_registers"]:
        name = str(control["name"])
        rows.append(
            [
                navigation_code_link("section:control-registers", name),
                ", ".join(tex_code(field) for field in field_groups.get(name, []))
                or "--",
                tex_code("RDCR"),
                tex_code("WRCR") + " and named architectural transitions",
                tex_breakable_code(reset_values.get(name, "not listed")),
            ]
        )
    return rows


def state_index(
    navigation: dict[str, Any],
    architecture: dict[str, Any],
) -> str:
    return latex_longtable(
        ["State", "Fields", "Readers", "Writers", "Reset"],
        state_index_rows(navigation, architecture),
        ["0.90in", "1.05in", "1.35in", "1.45in", "0.65in"],
        "Architectural State Index",
        style="dense",
    )


def event_instruction_producers(
    instructions: list[InstructionDef],
) -> dict[str, list[str]]:
    producers: dict[str, list[str]] = defaultdict(list)
    for instruction in instructions:
        exceptions = instruction.data.get("exceptions")
        if not isinstance(exceptions, list):
            continue
        for exception in exceptions:
            if not isinstance(exception, dict):
                continue
            event = exception.get("event")
            if isinstance(event, str) and instruction.mnemonic not in producers[event]:
                producers[event].append(instruction.mnemonic)
    return producers


def event_index_rows(
    architecture: dict[str, Any],
    instructions: list[InstructionDef],
) -> list[list[str]]:
    instruction_producers = event_instruction_producers(instructions)
    rows: list[list[str]] = []
    for event in architecture["architectural_events"]:
        event_class = str(event["event_class"])
        event_id = event["id"]
        code = (
            f"EXC:{int(event_id):02x}"
            if event_class == "EXCEPTION"
            else f"{event_class}:{event_id}"
        )
        producer_links = [
            rf"\hyperref[{instruction_label(mnemonic)}]{{{tex_code(mnemonic)}}}"
            for mnemonic in sorted(instruction_producers.get(str(event["name"]), []))
        ]
        producer = latex_escape(event["producer"])
        if producer_links:
            producer += "; " + ", ".join(producer_links)
        rows.append(
            [
                tex_breakable_code(code),
                tex_breakable_code(str(event["name"])),
                producer,
                tex_code(event["priority"]),
                tex_code(event["frame"]),
                navigation_link("section:event-code-and-sources"),
            ]
        )
    return rows


def event_index(
    architecture: dict[str, Any],
    instructions: list[InstructionDef],
) -> str:
    return latex_longtable(
        ["Code", "Event", "Producer", "Priority", "Frame", "Definition"],
        event_index_rows(architecture, instructions),
        ["0.70in", "0.85in", "1.75in", "0.45in", "0.70in", "0.85in"],
        "Architectural Event Index",
        style="dense",
    )


def extension_register_state(
    model: IsaModel,
    qualified_name: str,
    architecture: dict[str, Any],
) -> str:
    extensions = load_extensions(model.defs_root)
    candidates = [
        name
        for name in extensions
        if qualified_name == name or qualified_name.startswith(name + ".")
    ]
    candidates.sort(key=len, reverse=True)
    registers: list[str] = []
    owner_feature = ""
    for name in candidates:
        extension = extensions[name]
        availability = extension.data.get("availability")
        cpuid = availability.get("cpuid") if isinstance(availability, dict) else None
        if isinstance(cpuid, dict) and not owner_feature:
            owner_feature = str(cpuid.get("feature", ""))
        register_ref = extension.data.get("registers")
        if not isinstance(register_ref, str):
            continue
        register_doc = load_yaml(extension.path.parent / register_ref)
        groups = register_doc.get("registers") if isinstance(register_doc, dict) else None
        if isinstance(groups, dict):
            for group in groups.values():
                entries = group.get("entries") if isinstance(group, dict) else None
                if isinstance(entries, list):
                    registers.extend(
                        str(entry["name"])
                        for entry in entries
                        if isinstance(entry, dict) and "name" in entry
                    )
        break
    if registers and registers == [f"F{index}" for index in range(16)]:
        state = "F0--F15, FFLAGS, FSTATUS"
    else:
        state = ", ".join(registers) or owner_feature or qualified_name
    components = architecture["cpuid"]["save_area_layout"]["components"]
    component_names = {
        str(item["name"]) for item in components if isinstance(item, dict)
    }
    matching_feature = ""
    for name in reversed(candidates):
        availability = extensions[name].data.get("availability")
        cpuid = availability.get("cpuid") if isinstance(availability, dict) else None
        if isinstance(cpuid, dict) and str(cpuid.get("feature", "")) in component_names:
            matching_feature = str(cpuid["feature"])
            break
    if matching_feature:
        state += f", SAVE component {matching_feature}"
    return state


def feature_index_rows(
    model: IsaModel,
    instructions: list[InstructionDef],
    architecture: dict[str, Any],
) -> list[list[str]]:
    rows: list[list[str]] = []
    for qualified_name, extension in sorted(
        model.metadata["extensions"].items(),
        key=lambda item: (
            int(item[1]["availability"]["cpuid"]["class"]),
            int(item[1]["availability"]["cpuid"]["leaf"]),
            int(item[1]["availability"]["cpuid"]["index"]),
            int(item[1]["availability"]["cpuid"]["bit"]),
        ),
    ):
        cpuid = extension["availability"]["cpuid"]
        selector = (
            f"{int(cpuid['class']):08x}:"
            f"{int(cpuid['leaf']):04x}:"
            f"{int(cpuid['index'])}/bit{int(cpuid['bit'])}"
        )
        gated = sorted(
            (
                instruction
                for instruction in instructions
                if instruction.instruction_set == qualified_name
            ),
            key=lambda item: item.mnemonic,
        )
        related_state = extension_register_state(
            model, qualified_name, architecture
        )
        for instruction in gated:
            rows.append(
                [
                    navigation_code_link(
                        "section:cpuid-extension-directory",
                        str(cpuid["feature"]),
                    ),
                    tex_breakable_code(selector),
                    rf"\hyperref[{instruction_label(instruction.mnemonic)}]"
                    rf"{{{tex_code(instruction.mnemonic)}}}",
                    latex_escape(related_state),
                ]
            )
    return rows


def feature_index(
    model: IsaModel,
    instructions: list[InstructionDef],
    architecture: dict[str, Any],
) -> str:
    return latex_longtable(
        ["Predicate", "Class:leaf:index/bit", "Gated instruction", "Related state or component"],
        feature_index_rows(model, instructions, architecture),
        ["0.80in", "1.35in", "1.15in", "2.05in"],
        "CPUID Feature Index",
        style="dense",
    )


def revision_history_table(navigation: dict[str, Any]) -> str:
    history = navigation["revision_history"]
    unreleased = history["unreleased"]
    rows = [
        [
            latex_escape(unreleased["status"]),
            "--",
            latex_escape("; ".join(unreleased["changes"])),
        ]
    ]
    for release in history["released"]:
        rows.append(
            [
                latex_escape(release["title"]),
                tex_code(release["architecture_revision"]),
                latex_escape(
                    f"{release['compatibility']}: "
                    + "; ".join(release["changes"])
                ),
            ]
        )
    return latex_longtable(
        ["Status", "Architecture revision", "Changes"],
        rows,
        ["0.85in", "0.90in", "3.65in"],
        "Architecture Revision History",
    )


def latex_reference_navigation_section(
    model: IsaModel,
    instructions: list[InstructionDef],
) -> str:
    navigation = load_reference_navigation(REFERENCE_NAVIGATION_PATH)
    architecture = architecture_table_data()
    return render_latex_template(
        "reference_navigation.tex",
        {
            "CANONICAL_FIELD_INDEX": canonical_field_index(navigation),
            "STATE_INDEX": state_index(navigation, architecture),
            "EVENT_INDEX": event_index(architecture, instructions),
            "FEATURE_INDEX": feature_index(model, instructions, architecture),
            "REVISION_HISTORY": revision_history_table(navigation),
        },
    )


def latex_data_formats_section(model: IsaModel) -> str:
    all_values = data_format_template_values(model)
    scalar_values = {
        key: value
        for key, value in all_values.items()
        if key.startswith(("B_", "W_", "L_", "Q_", "S_", "D_"))
    }
    return render_latex_template("data_formats.tex", scalar_values)


def latex_instruction_word_formats_section(model: IsaModel) -> str:
    architecture_values = encoding_architecture_template_values()
    instruction_encoding_diagrams = render_latex_template(
        "fragments/instruction_encoding_diagrams.tex",
        {
            "OPCODE_PAYLOAD_NAMESPACE_ROWS": architecture_values[
                "OPCODE_PAYLOAD_NAMESPACE_ROWS"
            ]
        },
    )
    data_values = data_format_template_values(model)
    operand_values = {
        key: value
        for key, value in data_values.items()
        if not key.startswith(("B_", "W_", "L_", "Q_", "S_", "D_"))
    }
    instruction_payload_ordering = render_latex_template(
        "fragments/instruction_payload_ordering.tex",
        operand_values,
    )
    return render_latex_template(
        "instruction_word_formats.tex",
        {
            "INSTRUCTION_LENGTH_TRUTH_TABLE_ROWS": architecture_values[
                "INSTRUCTION_LENGTH_TRUTH_TABLE_ROWS"
            ],
            "ENCODING_CLASS_SUMMARY_ROWS": architecture_values[
                "ENCODING_CLASS_SUMMARY_ROWS"
            ],
            "INSTRUCTION_ENCODING_DIAGRAMS": instruction_encoding_diagrams,
            "INSTRUCTION_PAYLOAD_ORDERING_SECTION": instruction_payload_ordering,
        },
    )


def tex_breakable_code(value: str) -> str:
    escaped = latex_escape(value).replace("--", r"{-}{-}")
    escaped = escaped.replace(r"\_", r"\_\allowbreak{}")
    escaped = escaped.replace(".", r".\allowbreak{}")
    escaped = escaped.replace("/", r"/\allowbreak{}")
    escaped = escaped.replace(":", r":\allowbreak{}")
    escaped = escaped.replace("=", r"=\allowbreak{}")
    return r"\texttt{" + escaped + "}"


def latex_register_section(model: IsaModel) -> str:
    data = model.metadata.get("registers") or {}
    register_groups = data.get("registers") or {}
    segment_registers = (register_groups.get("segment") or {}).get("entries") or []
    sreg_rows = [
        [
            reg.get("name", ""),
            bits_text(reg["encoding"], 3),
            reg.get("role", ""),
            reg.get("description", ""),
        ]
        for reg in sorted(
            (
                reg
                for reg in segment_registers
                if reg.get("encoding") is not None
            ),
            key=lambda reg: reg["encoding"],
        )
    ]
    return render_latex_template(
        "register_model.tex",
        {
            "SREG_TABLE": latex_code_table(
                ["Segment", "Bits", "Role", "Use"],
                sreg_rows,
                ["0.60in", "0.50in", "0.70in", "3.60in"],
                "Segment Register Operand Encoding",
                {0, 1},
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


def latex_condition_code_computation_section() -> str:
    return render_latex_template("condition_code_computation.tex")


def latex_ea_payload_rows(data: dict[str, Any]) -> str:
    rows: list[str] = []
    for name, spec in (data.get("payloads") or {}).items():
        if not isinstance(spec, dict):
            continue
        kind = compact_text(spec.get("kind"))
        field_width = int(spec.get("field_width", 0))
        byte_width = field_width // 8
        signed = bool(spec.get("signed"))
        value = "signed" if signed else "unsigned"
        if kind == "displacement":
            use = "displacement added to base/index expression"
        elif kind == "absolute" and signed:
            use = "absolute address, sign-extended before use"
        elif kind == "absolute":
            use = "absolute address payload"
        elif kind == "immediate":
            use = "immediate operand payload"
        else:
            raise ValueError(f"unknown EA payload kind: {kind!r}")
        rows.append(f"{name} & {byte_width} & {value} & {use}\\\\")
    rows.append(
        "EXT0 descriptor & 1 or 2 & encoded & extended EA descriptor; present only for EXT0 escapes\\\\"
    )
    return "\n".join(rows)


def ea_form_index(data: dict[str, Any], section: str) -> dict[str, dict[str, Any]]:
    section_data = data.get(section) or {}
    return {
        str(form["name"]): form
        for form in section_data.get("forms", []) or []
        if isinstance(form, dict) and form.get("name")
    }


def latex_ea_syntax(forms: list[dict[str, Any]]) -> str:
    return "\n".join(
        rf"\manualeaprofilesyntax{{{compact_text(form.get('syntax')).replace('--', '{-}{-}')}}}"
        for form in forms
    )


def latex_ea_encoding(text: str, label: str = "EA encoding") -> str:
    return rf"\manualeaprofileline{{{label}}}{{{text}}}"


def joined_words(items: list[str], conjunction: str = "and") -> str:
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} {conjunction} {items[1]}"
    return f"{', '.join(items[:-1])}, {conjunction} {items[-1]}"


def compact_ea_fragment_values(data: dict[str, Any]) -> dict[str, str]:
    forms = ea_form_index(data, "compact")

    def selected(*names: str) -> list[dict[str, Any]]:
        return [forms[name] for name in names]

    register = selected("register", "stack_pointer")
    rn_memory = selected(
        "register_indirect",
        "register_disp8s",
        "register_disp16s",
        "register_disp32s",
        "register_disp64",
    )
    sp_memory = selected(
        "stack_pointer_indirect",
        "stack_pointer_disp8s",
        "stack_pointer_disp16s",
        "stack_pointer_disp32s",
        "stack_pointer_disp64",
    )
    pc_memory = selected(
        "program_counter_disp8s",
        "program_counter_disp16s",
        "program_counter_disp32s",
        "program_counter_disp64",
    )
    absolute = selected("absolute_32s", "absolute_64")
    immediate = selected("immediate_8s", "immediate_16s", "immediate_32s", "immediate_64")
    ext0 = selected("ext0", "ext0_disp8s", "ext0_disp16s", "ext0_disp32s", "ext0_disp64")

    def patterns(items: list[dict[str, Any]]) -> list[str]:
        return [compact_text(item.get("pattern")) for item in items]

    def payloads(items: list[dict[str, Any]]) -> list[str]:
        return [compact_text(item.get("payload")) for item in items]

    return {
        "REGISTER_DIRECT_SYNTAX": latex_ea_syntax(register),
        "REGISTER_DIRECT_ENCODING": latex_ea_encoding(
            f"{patterns(register)[0]} selects {compact_text(register[0].get('syntax'))}; "
            f"{patterns(register)[1]} selects {compact_text(register[1].get('syntax'))}."
        ),
        "RN_MEMORY_SYNTAX": latex_ea_syntax(rn_memory),
        "RN_MEMORY_ENCODING": latex_ea_encoding(
            f"{patterns(rn_memory)[0]} has no displacement; "
            f"{joined_words(patterns(rn_memory[1:]))} select {joined_words(payloads(rn_memory[1:]))}."
        ),
        "SP_MEMORY_SYNTAX": latex_ea_syntax(sp_memory),
        "SP_MEMORY_ENCODING": latex_ea_encoding(
            f"{patterns(sp_memory)[0]} has no displacement; "
            f"{joined_words(patterns(sp_memory[1:]))} select {joined_words(payloads(sp_memory[1:]))}."
        ),
        "PC_MEMORY_SYNTAX": latex_ea_syntax(pc_memory),
        "PC_MEMORY_ENCODING": latex_ea_encoding(
            f"{joined_words(patterns(pc_memory))} select {joined_words(payloads(pc_memory))}."
        ),
        "ABSOLUTE_MEMORY_SYNTAX": latex_ea_syntax(absolute),
        "ABSOLUTE_MEMORY_ENCODING": latex_ea_encoding(
            f"{patterns(absolute)[0]} selects {payloads(absolute)[0]}; "
            f"{patterns(absolute)[1]} selects {payloads(absolute)[1]}."
        ),
        "IMMEDIATE_SYNTAX": latex_ea_syntax(immediate),
        "IMMEDIATE_ENCODING": latex_ea_encoding(
            f"{joined_words(patterns(immediate))} select {joined_words(payloads(immediate))}."
        ),
        "EXT0_ESCAPE_SYNTAX": latex_ea_syntax(ext0),
        "EXT0_ESCAPE_ENCODING": latex_ea_encoding(
            f"{patterns(ext0)[0]} selects no displacement; "
            f"{joined_words(patterns(ext0[1:]))} select {joined_words(payloads(ext0[1:]))}."
        ),
    }


def ext0_fragment_values(data: dict[str, Any]) -> dict[str, str]:
    forms = ea_form_index(data, "ext0")

    def selected(*names: str) -> list[dict[str, Any]]:
        return [forms[name] for name in names]

    def descriptor_parts(form: dict[str, Any]) -> list[str]:
        pattern = form.get("pattern") or []
        return [compact_text(byte) for byte in pattern]

    explicit_base = selected("explicit_segment_base")
    explicit_indexed = selected(
        "explicit_segment_index",
        "explicit_segment_index_postincrement",
        "explicit_segment_index_predecrement",
    )
    explicit_zero = selected("explicit_segment_zero_base")
    explicit_base_update = selected(
        "explicit_segment_base_postincrement",
        "explicit_segment_base_predecrement",
    )
    explicit_zero_indexed = selected(
        "explicit_segment_zero_base_index",
        "explicit_segment_zero_base_index_postincrement",
        "explicit_segment_zero_base_index_predecrement",
    )
    sp_pc_indexed = selected(
        "stack_pointer_index",
        "stack_pointer_index_postincrement",
        "stack_pointer_index_predecrement",
        "program_counter_index",
        "program_counter_index_postincrement",
        "program_counter_index_predecrement",
    )
    default_base_update = selected(
        "default_segment_base_postincrement",
        "default_segment_base_predecrement",
    )

    return {
        "EXPLICIT_SEGMENT_BASE_SYNTAX": latex_ea_syntax(explicit_base),
        "EXPLICIT_SEGMENT_BASE_DESCRIPTOR": latex_ea_encoding(
            f"{descriptor_parts(explicit_base[0])[0]}, one byte.", "Descriptor"
        ),
        "EXPLICIT_SEGMENT_INDEXED_SYNTAX": latex_ea_syntax(explicit_indexed),
        "EXPLICIT_SEGMENT_INDEXED_DESCRIPTOR": latex_ea_encoding(
            "Byte 0 is "
            + joined_words(
                [rf"\texttt{{{descriptor_parts(form)[0]}}}" for form in explicit_indexed],
                "or",
            )
            + " for no update, postincrement, or predecrement. Byte 1 is "
            + rf"\texttt{{{descriptor_parts(explicit_indexed[0])[1]}}}.",
            "Descriptor",
        ),
        "EXPLICIT_SEGMENT_ZERO_BASE_SYNTAX": latex_ea_syntax(explicit_zero),
        "EXPLICIT_SEGMENT_ZERO_BASE_DESCRIPTOR": latex_ea_encoding(
            f"{descriptor_parts(explicit_zero[0])[0]}, one byte.", "Descriptor"
        ),
        "EXPLICIT_SEGMENT_BASE_UPDATE_SYNTAX": latex_ea_syntax(explicit_base_update),
        "EXPLICIT_SEGMENT_BASE_UPDATE_DESCRIPTOR": latex_ea_encoding(
            rf"Byte 0 is \texttt{{{descriptor_parts(explicit_base_update[0])[0]}}}. Byte 1 is "
            rf"\texttt{{{descriptor_parts(explicit_base_update[0])[1]}}} for base postincrement or "
            rf"\texttt{{{descriptor_parts(explicit_base_update[1])[1]}}} for base predecrement.",
            "Descriptor",
        ),
        "EXPLICIT_SEGMENT_ZERO_BASE_INDEXED_SYNTAX": latex_ea_syntax(explicit_zero_indexed),
        "EXPLICIT_SEGMENT_ZERO_BASE_INDEXED_DESCRIPTOR": latex_ea_encoding(
            rf"Byte 0 is \texttt{{{descriptor_parts(explicit_zero_indexed[0])[0]}}}. Byte 1 is "
            + joined_words(
                [rf"\texttt{{{descriptor_parts(form)[1]}}}" for form in explicit_zero_indexed],
                "or",
            )
            + " for no update, postincrement, or predecrement.",
            "Descriptor",
        ),
        "SP_PC_INDEXED_SYNTAX": latex_ea_syntax(sp_pc_indexed),
        "SP_PC_INDEXED_DESCRIPTOR": latex_ea_encoding(
            rf"Byte 0 is \texttt{{{descriptor_parts(sp_pc_indexed[0])[0]}}} for SP or "
            rf"\texttt{{{descriptor_parts(sp_pc_indexed[3])[0]}}} for PC. Byte 1 is "
            + joined_words(
                [rf"\texttt{{{descriptor_parts(form)[1]}}}" for form in sp_pc_indexed[:3]],
                "or",
            )
            + " for no update, postincrement, or predecrement.",
            "Descriptor",
        ),
        "DEFAULT_SEGMENT_BASE_UPDATE_SYNTAX": latex_ea_syntax(default_base_update),
        "DEFAULT_SEGMENT_BASE_UPDATE_DESCRIPTOR": latex_ea_encoding(
            f"{descriptor_parts(default_base_update[0])[0]} for base postincrement; "
            f"{descriptor_parts(default_base_update[1])[0]} for base predecrement. One byte.",
            "Descriptor",
        ),
    }


def render_ea_reference_fragments(data: dict[str, Any]) -> dict[Path, str]:
    outputs = {
        "compact_ea_reference_blocks.tex": render_latex_template(
            "fragments/compact_ea_reference_blocks.tex.in",
            compact_ea_fragment_values(data),
        ),
        "ext0_reference_blocks.tex": render_latex_template(
            "fragments/ext0_reference_blocks.tex.in",
            ext0_fragment_values(data),
        ),
    }
    return {EA_FRAGMENT_DIR / name: text for name, text in outputs.items()}


def latex_ea_section(model: IsaModel) -> str:
    data = model.metadata.get("ea") or {}
    compact = data.get("compact") or {}
    compact_rows = []
    for form in compact.get("forms", []) or []:
        kind = compact_text(form.get("kind"))
        table_class = "ext0_escape" if kind == "escape" else kind
        memory = kind == "memory" if kind in {"register", "memory", "immediate"} else ""
        compact_rows.append(
            [form.get("pattern", ""), form.get("syntax", table_class), table_class, display_text(memory)]
        )
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
            "EA_PAYLOAD_ROWS": latex_ea_payload_rows(data),
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


def latex_streaming_model_section() -> str:
    return render_latex_template("streaming_execution_model.tex")


def latex_privileged_programming_model_section() -> str:
    return render_latex_template("privileged_programming_model.tex", {})


def latex_exception_processing_section() -> str:
    return render_latex_template("interrupt_model.tex", {})


def instruction_label(mnemonic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", mnemonic.lower()).strip("-")
    return f"instr:{slug or 'unknown'}"


def instruction_set_page_label(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise ValueError("instruction set name has no stable page identifier")
    return f"page:instruction-group-{slug}"


def instruction_details_tex(inst: InstructionDef) -> str:
    path = inst.details_path
    if path is None:
        return ""
    resolved = resolve_source(path, ROOT)
    if not resolved.exists():
        return ""
    if not resolved.is_file():
        raise ValueError(f"{path}: expected a regular details.tex file")
    text = read_source(path, ROOT).strip()
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


def latex_instruction_flag_effects(inst: InstructionDef) -> str:
    parts: list[str] = []
    for bank, valid_flags in FLAG_BANKS.items():
        effects = inst.flag_effects.get(bank)
        if not effects:
            continue
        ordered = [
            (flag, effects.get(flag, "preserved"))
            for flag in valid_flags
        ]
        parts.extend(
            [
                rf"\begin{{manualflageffects}}{{{bank}}}",
                *(
                    rf"\manualflageffect{{{flag}}}{{{latex_escape(effect)}}}"
                    for flag, effect in ordered
                ),
                r"\end{manualflageffects}",
            ]
        )
    return "\n".join(parts)


def latex_instruction_exceptions(inst: InstructionDef) -> str:
    raw_exceptions = inst.data.get("exceptions")
    if not isinstance(raw_exceptions, list) or not raw_exceptions:
        return ""
    lines: list[str] = []
    for item in raw_exceptions:
        if not isinstance(item, dict):
            continue
        event = tex_code(str(item.get("event", "")))
        condition = latex_escape(str(item.get("when", "")))
        forms = item.get("forms")
        if isinstance(forms, list) and forms:
            form_text = ", ".join(tex_code(str(form)) for form in forms)
            condition += rf" ({latex_escape('forms')}: {form_text})"
        lines.append(event + ": " + condition)
    return latex_ragged_block(lines)


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
        raise ValueError(f"{inst.path}: description must be a non-empty string")
    parts.append(latex_instruction_field("Operation", latex_escape(description)))
    syntax_lines = assembler_syntax_lines(model, inst)
    if syntax_lines:
        parts.append(
            latex_instruction_field(
                "Assembler Syntax",
                latex_ragged_block([tex_code(line) for line in syntax_lines]),
            )
        )
    parts.append(latex_instruction_field("Attributes", latex_attributes_block(inst, model)))
    exceptions = latex_instruction_exceptions(inst)
    if exceptions:
        parts.append(latex_instruction_field("Exceptions", exceptions))
    operand_value_tables = latex_instruction_operand_value_tables(model, inst)
    if operand_value_tables:
        parts.append(operand_value_tables)
    flag_effects = latex_instruction_flag_effects(inst)
    details_tex = instruction_details_tex(inst)
    if flag_effects or details_tex:
        parts.append(r"\manualinstructiondescriptionheading{Detailed Semantics}")
        if flag_effects:
            parts.append(flag_effects)
        if details_tex:
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
    for set_name, title, introduction, group in instruction_set_groups(model, instructions):
        parts.extend(
            [
                str(LatexTopSection(title)),
                rf"\label{{{instruction_set_page_label(set_name)}}}",
            ]
        )
        if introduction:
            if not introduction.is_file():
                raise FileNotFoundError(f"instruction-set introduction not found: {introduction}")
            parts.append(introduction.read_text(encoding="utf-8").strip())
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
