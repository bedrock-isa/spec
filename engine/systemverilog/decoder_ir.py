#!/usr/bin/env python3
"""Project the canonical ISA into the decoder rendering model."""

from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field, fields, is_dataclass
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from ..encoding_architecture import ENCODING_CLASSES_BY_NAME
from ..reference import Reference


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEFS_ROOT = ROOT / "isa"
MAX_VALUE_WIDTH = 64
MAX_RECORD_BYTES = 18

@dataclass(frozen=True)
class BitPatternIR:
    width: int
    value: int
    mask: int


@dataclass(frozen=True)
class FieldIR:
    symbol: str
    type_name: str
    kind: str
    width: int
    positions: tuple[int, ...]


@dataclass(frozen=True)
class ConstraintRangeIR:
    lower: int
    upper: int


@dataclass(frozen=True)
class ConstraintIR:
    field_symbol: str
    positions: tuple[int, ...]
    kind: str
    ranges: tuple[ConstraintRangeIR, ...]
    reason: str


@dataclass(frozen=True)
class EncodedFieldSourceIR:
    field_symbol: str
    positions: tuple[int, ...]
    tag: str = dataclass_field(default="encoded-field", init=False)


@dataclass(frozen=True)
class FixedSourceIR:
    value: int | None
    identity: str
    tag: str = dataclass_field(default="fixed", init=False)


@dataclass(frozen=True)
class AppendedPayloadSourceIR:
    width: int
    signed: bool
    tag: str = dataclass_field(default="appended-payload", init=False)


@dataclass(frozen=True)
class EffectiveAddressSourceIR:
    field_symbol: str
    positions: tuple[int, ...]
    profile: str
    tag: str = dataclass_field(default="effective-address", init=False)


OperandSourceIR = (
    EncodedFieldSourceIR
    | FixedSourceIR
    | AppendedPayloadSourceIR
    | EffectiveAddressSourceIR
)


@dataclass(frozen=True)
class OperandIR:
    name: str
    type_name: str
    type_width: int
    access: str
    domain: str
    ea_role: str
    ea_width: str
    legal_values: tuple[int, ...]
    source: OperandSourceIR


@dataclass(frozen=True)
class ParseEaIR:
    operand_name: str
    field_symbol: str
    profile: str
    minimum_bytes: int
    maximum_bytes: int
    tag: str = dataclass_field(default="ParseEa", init=False)


@dataclass(frozen=True)
class ReadPayloadIR:
    operand_name: str
    width: int
    signed: bool
    tag: str = dataclass_field(default="ReadPayload", init=False)


LayoutOpIR = ParseEaIR | ReadPayloadIR


@dataclass(frozen=True)
class RepeatControlIR:
    rep: bool
    repcc: bool
    observed_kind: str
    observed_operand: str


@dataclass(frozen=True)
class ControlIR:
    route: str
    instruction_set: str
    instruction_class: str
    family: str
    privilege: str
    predicate_mode: str
    has_ea_operand: bool
    repeat: RepeatControlIR


@dataclass(frozen=True)
class CpuidFlagIR:
    id: str
    token: str
    selector_class: int
    leaf: int
    index: int
    bit: int


@dataclass(frozen=True)
class AvailabilitySelectorIR:
    domain: str
    field_symbol: str
    positions: tuple[int, ...]
    encoded_values: tuple[int, ...]


@dataclass(frozen=True)
class AvailabilityOperandProfileIR:
    operand_name: str
    type_names: tuple[str, ...]


@dataclass(frozen=True)
class AvailabilityRuleIR:
    case_id: str
    selectors: tuple[AvailabilitySelectorIR, ...]
    operand_profiles: tuple[AvailabilityOperandProfileIR, ...]
    required_cpuid_flags: tuple[str, ...]


@dataclass(frozen=True)
class OperandOverlapIR:
    left: str
    right: str
    rule: str


@dataclass(frozen=True)
class FormIR:
    key: str
    index: int
    mnemonic: str
    syntax: str
    opcode_class: str
    opcode_space_bytes: int
    opcode_width: int
    opcode_value: int
    opcode_mask: int
    fields: tuple[FieldIR, ...]
    constraints: tuple[ConstraintIR, ...]
    operands: tuple[OperandIR, ...]
    layout: tuple[LayoutOpIR, ...]
    sizes: tuple[str, ...]
    overlaps: tuple[OperandOverlapIR, ...]
    control: ControlIR
    availability_rules: tuple[AvailabilityRuleIR, ...]
    fixed_required_bytes: int
    minimum_required_bytes: int
    maximum_required_bytes: int
    representative_record: tuple[int, ...] | None


@dataclass(frozen=True)
class EaPayloadIR:
    name: str
    kind: str
    width: int
    signed: bool
    format: str


@dataclass(frozen=True)
class EaFieldIR:
    symbol: str
    type_name: str
    role: str
    width: int
    positions: tuple[int, ...]


@dataclass(frozen=True)
class EaFormIR:
    name: str
    member_of_descriptor_family: str
    descriptor_bytes: int
    patterns: tuple[BitPatternIR, ...]
    width: int
    value: int
    mask: int
    kind: str
    fields: tuple[EaFieldIR, ...]
    segment: str
    payload_name: str
    payload_width: int
    payload_signed: bool
    base: str
    register_name: str
    referenced_descriptor_family: str
    update_target: str
    update_mode: str


@dataclass(frozen=True)
class CompactEaEntryIR:
    raw: int
    valid: bool
    reserved: bool
    invalid_reason: str
    form_name: str
    kind: str
    descriptor_family: str
    descriptor_bytes: int
    payload_name: str
    payload_width: int
    payload_signed: bool
    consumed_bytes: int


@dataclass(frozen=True)
class EaDescriptorFamilyIR:
    name: str
    descriptor_bytes: int
    kind: str
    forms: tuple[EaFormIR, ...]


@dataclass(frozen=True)
class EaProfileIR:
    name: str
    operand_type: str
    compact_forms: tuple[EaFormIR, ...]
    compact_entries: tuple[CompactEaEntryIR, ...]
    immediate_conversion: str
    lane_model: str
    base_update: str
    index_update: str
    predicate_affects_update: bool | None
    scatter_gather: str


@dataclass(frozen=True)
class EffectiveAddressIR:
    compact_width: int
    payloads: tuple[EaPayloadIR, ...]
    compact_forms: tuple[EaFormIR, ...]
    compact_entries: tuple[CompactEaEntryIR, ...]
    profiles: tuple[EaProfileIR, ...]
    descriptor_families: tuple[EaDescriptorFamilyIR, ...]


@dataclass(frozen=True)
class DerivedLimitsIR:
    form_count: int
    mnemonic_count: int
    max_opcode_width: int
    max_operands: int
    max_ea_operands: int
    max_overlaps: int
    max_fields: int
    max_layout_ops: int
    max_fixed_required_bytes: int
    max_required_bytes: int
    max_record_bytes: int
    compact_ea_values: int
    max_descriptor_bytes: int


@dataclass(frozen=True)
class DecodeIR:
    cpuid_flags: tuple[CpuidFlagIR, ...]
    mnemonics: tuple[str, ...]
    operations: tuple[Any, ...]
    limits: DerivedLimitsIR
    forms: tuple[FormIR, ...]
    effective_addresses: EffectiveAddressIR

def pattern_value_mask(pattern: str) -> tuple[int, int]:
    value = 0
    mask = 0
    for character in pattern:
        value <<= 1
        mask <<= 1
        if character in "01":
            mask |= 1
            value |= int(character)
    return value, mask


def gather_positions(pattern: str, symbol: str) -> tuple[int, ...]:
    return tuple(
        len(pattern) - index - 1
        for index, character in enumerate(pattern)
        if character == symbol
    )


def normalize_range(value: int | str) -> ConstraintRangeIR:
    if isinstance(value, int):
        return ConstraintRangeIR(value, value)
    text = value.replace("_", "")
    if ".." in text:
        lower, upper = text.split("..", 1)
        return ConstraintRangeIR(int(lower, 0), int(upper, 0))
    parsed = int(text, 0)
    return ConstraintRangeIR(parsed, parsed)


def _pattern_ir(pattern: str) -> BitPatternIR:
    value, mask = pattern_value_mask(pattern)
    return BitPatternIR(len(pattern), value, mask)


def _derive_limits(
    forms_ir: tuple[FormIR, ...],
    effective_addresses: EffectiveAddressIR,
) -> DerivedLimitsIR:
    return DerivedLimitsIR(
        form_count=len(forms_ir),
        mnemonic_count=len({form.mnemonic for form in forms_ir}),
        max_opcode_width=max(
            item.allocation_bits for item in ENCODING_CLASSES_BY_NAME.values()
        ),
        max_operands=max(len(form.operands) for form in forms_ir),
        max_ea_operands=max(
            sum(
                isinstance(operand.source, EffectiveAddressSourceIR)
                for operand in form.operands
            )
            for form in forms_ir
        ),
        max_overlaps=max(len(form.overlaps) for form in forms_ir),
        max_fields=max(len(form.fields) for form in forms_ir),
        max_layout_ops=max(len(form.layout) for form in forms_ir),
        max_fixed_required_bytes=max(form.fixed_required_bytes for form in forms_ir),
        max_required_bytes=max(form.maximum_required_bytes for form in forms_ir),
        max_record_bytes=MAX_RECORD_BYTES,
        compact_ea_values=len(effective_addresses.compact_entries),
        max_descriptor_bytes=max(
            family.descriptor_bytes
            for family in effective_addresses.descriptor_families
        ),
    )

def _operand_type_name(definition: Any) -> str:
    name = definition.id
    semantic_names = {
        "CC": "condition",
        "FLBMP": "flags_bitmap",
        "MORDER": "memory_order",
        "PTLVL": "pt_level",
        "FCONSTID": "fconst_id",
    }
    if name in semantic_names:
        return semantic_names[name]
    if name.startswith(("IMM", "DISP", "ABS")):
        return name.lower()
    return name


def _is_signed(definition: Any) -> bool:
    if getattr(definition, "signed", None) is not None:
        return bool(definition.signed)
    value_type = getattr(definition, "value_type", None)
    return value_type == "signed_integer" or definition.id.endswith("S")


def _legal_values(type_name: str, authored: tuple[int, ...]) -> tuple[int, ...]:
    if authored:
        return authored
    if type_name == "memory_order":
        return tuple(range(5))
    if type_name in {"PAIRn", "FPAIRn"}:
        return tuple(range(8))
    if type_name == "pt_level":
        return tuple(range(1, 6))
    if type_name == "fconst_id":
        return (
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
            16, 17, 18, 19, 20, 21, 22, 23,
            32, 33, 34, 35, 36, 37, 38,
            256, 257, 258, 259, 260, 261,
            272, 273, 274, 275, 276, 277, 278, 279, 280,
        )
    return ()


def _ea_form(
    project: Any,
    mode: Any,
    encoding: dict[str, Any],
    encoding_index: int,
    *,
    family: str = "",
    kind_override: str | None = None,
) -> EaFormIR:
    patterns = encoding["pattern"]
    chunks = (patterns,) if isinstance(patterns, str) else tuple(patterns)
    joined = "".join(chunks)
    value, mask = pattern_value_mask(joined)
    payloads = encoding.get("payloads", ())
    payload_binding = payloads[0] if payloads else None
    payload_definition = (
        project.types.payload_types.resolve(mode.payload_type_reference(encoding_index, 0))
        if payload_binding is not None
        else None
    )
    payload_name = (
        payload_definition.id.lower()
        if payload_definition is not None
        else ""
    )
    mode_id = mode["id"]
    if family:
        update = encoding.get("autoupdate")
        name = mode_id + (f"_{update['type']}" if update else "")
    elif mode_id == "register":
        name = "register_indirect" if not payload_name else f"register_{payload_name}"
    elif mode_id in {"stack_pointer_displaced", "program_counter_displaced"}:
        name = f"{mode_id.removesuffix('_displaced')}_{payload_name}"
    elif mode_id == "absolute":
        name = f"absolute_{payload_name.removeprefix('abs')}"
    elif mode_id == "immediate":
        suffix = payload_name.removeprefix("imm")
        name = f"immediate_{suffix}"
    elif mode_id in {"ext1", "ext2"}:
        name = mode_id if not payload_name else f"{mode_id}_{payload_name}"
    else:
        name = mode_id

    fields_ir = []
    for symbol, raw_field in sorted(mode.to_dict().get("fields", {}).items()):
        definition = project.types.field_types.resolve(mode.field_type_reference(symbol))
        fields_ir.append(
            EaFieldIR(
                symbol,
                _operand_type_name(definition),
                raw_field["role"],
                definition.bits,
                gather_positions(joined, symbol),
            )
        )
    segment = mode.to_dict().get("segment")
    if segment is None:
        segment_name = "default" if mode["kind"] == "memory" else ""
    elif segment["source"] == "fixed":
        segment_name = segment["register"]
    else:
        segment_name = "explicit"
    pseudocode = mode.to_dict().get("pseudocode", "")
    if "SP" in pseudocode:
        base = "SP"
    elif "PC" in pseudocode:
        base = "PC"
    elif "base" in pseudocode:
        base = ""
    elif "0" in pseudocode:
        base = "zero"
    else:
        base = ""
    extension = mode.to_dict().get("extension", {})
    update = encoding.get("autoupdate") or {}
    return EaFormIR(
        name=name,
        member_of_descriptor_family=family.lower(),
        descriptor_bytes=len(chunks) if family else int(extension.get("bytes", 0)),
        patterns=tuple(_pattern_ir(chunk) for chunk in chunks),
        width=len(joined),
        value=value,
        mask=mask,
        kind=kind_override or ("escape" if mode["kind"] == "extension" else mode["kind"]),
        fields=tuple(fields_ir),
        segment=segment_name,
        payload_name=payload_name,
        payload_width=payload_definition.bytes * 8 if payload_definition else 0,
        payload_signed=_is_signed(payload_definition) if payload_definition else False,
        base=base,
        register_name="",
        referenced_descriptor_family=str(extension.get("id", "")).lower(),
        update_target=next(
            (
                symbol
                for symbol, field in mode.to_dict().get("fields", {}).items()
                if field["role"] == update.get("target")
            ),
            "",
        ),
        update_mode=str(update.get("type", "")),
    )


def _load_mode_catalog(project: Any, catalog: Path) -> tuple[Any, ...]:
    from ..ea_mode import EAMode
    from ..yaml_document import YamlDocumentLoader

    raw = YamlDocumentLoader().mapping(catalog)
    return tuple(
        EAMode.load(catalog.parent / name / "mode.yaml", project.root, project.types)
        for name in raw.get("modes", ())
    )


def _effective_addresses(project: Any) -> EffectiveAddressIR:
    base_root = project.root / "ea" / "modes"
    compact_modes = _load_mode_catalog(project, base_root / "compact" / "modes.yaml")
    family_modes = {
        family: _load_mode_catalog(project, base_root / family / "modes.yaml")
        for family in ("EXT1", "EXT2")
    }
    descriptor_families = tuple(
        EaDescriptorFamilyIR(
            family.lower(),
            1 if family == "EXT1" else 2,
            "memory",
            tuple(
                _ea_form(project, mode, encoding, index, family=family)
                for mode in family_modes[family]
                for index, encoding in enumerate(mode["encodings"])
            ),
        )
        for family in ("EXT1", "EXT2")
    )

    scalar_forms = tuple(
        _ea_form(project, mode, encoding, index)
        for mode in compact_modes
        for index, encoding in enumerate(mode["encodings"])
    )
    profile_overrides: dict[str, tuple[EaFormIR, ...]] = {"ea": ()}
    extension_profiles = {
        "fea": project.root / "extensions" / "FP" / "fea" / "modes" / "compact" / "modes.yaml",
        "vea": project.root / "extensions" / "VECTOR" / "vea" / "modes" / "compact" / "modes.yaml",
    }
    for profile, catalog in extension_profiles.items():
        modes = _load_mode_catalog(project, catalog)
        profile_overrides[profile] = tuple(
            _ea_form(
                project,
                mode,
                encoding,
                index,
                kind_override="float_immediate" if profile == "fea" else None,
            )
            for mode in modes
            for index, encoding in enumerate(mode["encodings"])
        )

    profiles = []
    for profile in ("ea", "fea", "vea"):
        overrides = profile_overrides[profile]
        forms = tuple(
            form
            for form in scalar_forms
            if not (profile == "fea" and form.kind == "immediate")
            and not (profile == "vea" and form.kind == "immediate")
            and not (
                profile in {"fea", "vea"}
                and form.name == "stack_pointer_indirect"
            )
        ) + overrides
        entries = []
        for raw in range(128):
            matches = [form for form in forms if raw & form.mask == form.value]
            if len(matches) == 1:
                form = matches[0]
                entries.append(
                    CompactEaEntryIR(
                        raw,
                        True,
                        False,
                        "",
                        form.name,
                        form.kind,
                        form.referenced_descriptor_family,
                        form.descriptor_bytes,
                        form.payload_name,
                        form.payload_width,
                        form.payload_signed,
                        form.descriptor_bytes + form.payload_width // 8,
                    )
                )
            else:
                entries.append(
                    CompactEaEntryIR(
                        raw,
                        False,
                        True,
                        f"unallocated compact {profile.upper()} value",
                        "",
                        "invalid",
                        "",
                        0,
                        "",
                        0,
                        False,
                        0,
                    )
                )
        profiles.append(
            EaProfileIR(
                profile,
                profile.upper(),
                forms,
                tuple(entries),
                "",
                "",
                "",
                "",
                None,
                "",
            )
        )
    payloads = tuple(
        EaPayloadIR(
            definition.id.lower(),
            str(definition.kind),
            definition.bytes * 8,
            _is_signed(definition),
            "",
        )
        for definition in project.types.payload_types.values()
    )
    return EffectiveAddressIR(
        7,
        payloads,
        scalar_forms,
        profiles[0].compact_entries,
        tuple(profiles),
        descriptor_families,
    )


def _operand_ir(project: Any, bundle: Any, form: Any) -> tuple[OperandIR, ...]:
    instruction_operands = bundle.instruction.to_dict()["operands"]
    field_by_marker = {binding.marker: binding for binding in form.fields}
    unused_payloads = list(form.payloads)
    used_roles: set[str] = set()
    result = []

    def add_binding(
        role: str,
        reference: Any,
        marker: str | None = None,
        type_name: str | None = None,
    ) -> None:
        if role in used_roles:
            return
        logical = instruction_operands.get(role, {})
        access = next(
            (
                binding.access
                for binding in (*form.fields, *form.payloads)
                if binding.role == role and binding.access is not None
            ),
            None,
        ) or logical.get("access", "read")
        source: OperandSourceIR
        if marker is not None:
            definition = project.types.field_types.resolve(reference)
            positions = gather_positions(form.pattern.code, marker)
            if definition.kind.value == "effective_address":
                source = EffectiveAddressSourceIR(marker, positions, definition.profile or "ea")
                operand_role = logical.get("role", "source")
                ea_role = (
                    operand_role
                    if operand_role in {"control_target", "address"}
                    else "value"
                )
                if logical.get("value_type") == "predicate":
                    ea_width = "predicate"
                elif ea_role in {"control_target", "address"}:
                    ea_width = "Q"
                else:
                    ea_width = "operation_size"
            else:
                source = EncodedFieldSourceIR(marker, positions)
                ea_role = ""
                ea_width = ""
            width = definition.bits
            authored_values = tuple(item.value for item in definition.values)
        else:
            definition = project.types.payload_types.resolve(reference)
            source = AppendedPayloadSourceIR(
                definition.bytes * 8, _is_signed(definition)
            )
            width = definition.bytes * 8
            authored_values = ()
            ea_role = ""
            ea_width = ""
        result.append(
            OperandIR(
                role,
                type_name or _operand_type_name(definition),
                width,
                access,
                logical.get("domain", ""),
                ea_role,
                ea_width,
                _legal_values(
                    type_name or _operand_type_name(definition),
                    authored_values,
                ),
                source,
            )
        )
        used_roles.add(role)

    if form.syntax.order_field is not None:
        binding = field_by_marker[form.syntax.order_field]
        add_binding(binding.role, binding.type, form.syntax.order_field)

    displayed_fields = {
        node.field
        for node in form.syntax.displayed_operands
        if node.field is not None
    }
    for binding in form.fields:
        if (
            binding.role in instruction_operands
            and binding.marker not in displayed_fields
            and binding.marker != form.syntax.size_field
            and binding.marker != form.syntax.order_field
        ):
            add_binding(binding.role, binding.type, binding.marker)

    displayed_operands = form.syntax.displayed_operands
    for node_index, node in enumerate(displayed_operands):
        if node.field is not None and node.field in field_by_marker:
            binding = field_by_marker[node.field]
            add_binding(binding.role, binding.type, node.field)
            continue
        if node.angled:
            match = next(
                (
                    binding
                    for binding in unused_payloads
                    if _operand_type_name(
                        project.types.payload_types.resolve(binding.type)
                    ).lower()
                    == (node.name or "").lower()
                ),
                unused_payloads[0] if unused_payloads else None,
            )
            if match is not None:
                unused_payloads.remove(match)
                public_type = (
                    node.name
                    or _operand_type_name(
                        project.types.payload_types.resolve(match.type)
                    )
                ).lower()
                if public_type.startswith("disp"):
                    public_type = "imm" + public_type.removeprefix("disp")
                elif public_type.startswith("abs"):
                    public_type = "imm" + public_type.removeprefix("abs")
                add_binding(match.role, match.type, type_name=public_type)
                continue
        if node.kind == "decimal" and "imm" in instruction_operands:
            logical = instruction_operands["imm"]
            result.append(
                OperandIR(
                    "imm",
                    "imm",
                    7,
                    logical["access"],
                    logical.get("domain", ""),
                    "",
                    "",
                    (),
                    FixedSourceIR(node.literal, ""),
                )
            )
            used_roles.add("imm")
            continue
        if node.kind == "reference" and node.name in {"SP", "CS"}:
            candidates = [role for role in instruction_operands if role not in used_roles]
            if node.name == "CS":
                role = candidates[0]
            elif node_index + 1 == len(displayed_operands):
                role = next(
                    (
                        candidate
                        for candidate in candidates
                        if instruction_operands[candidate]["role"] == "destination"
                    ),
                    candidates[-1],
                )
            else:
                role = next(
                    (
                        candidate
                        for candidate in candidates
                        if instruction_operands[candidate]["role"] == "source"
                    ),
                    candidates[0],
                )
            logical = instruction_operands[role]
            result.append(
                OperandIR(
                    role,
                    node.name,
                    0,
                    logical["access"],
                    logical.get("domain", ""),
                    "",
                    "",
                    (),
                    FixedSourceIR(None, node.name),
                )
            )
            used_roles.add(role)

    for binding in form.fields:
        if binding.role in instruction_operands:
            add_binding(binding.role, binding.type, binding.marker)
    for binding in form.payloads:
        if binding.role in instruction_operands:
            add_binding(binding.role, binding.type)
    return tuple(result)


def _form_ir(project: Any, bundle: Any, form: Any, index: int) -> FormIR:
    encoding_class = next(
        item
        for item in ENCODING_CLASSES_BY_NAME.values()
        if item.allocation_bits == form.pattern.bit_width
    )
    operands = _operand_ir(project, bundle, form)
    fields_ir = tuple(
        FieldIR(
            binding.marker,
            _operand_type_name(project.types.field_types.resolve(binding.type)),
            project.types.field_types.resolve(binding.type).kind.value,
            project.types.field_types.resolve(binding.type).bits,
            gather_positions(form.pattern.code, binding.marker),
        )
        for binding in form.fields
    )
    constraints = []
    for constraint in form.constraints:
        binding = form.field_for_role(constraint.role)
        if binding is None:
            raise ValueError(
                f"{bundle.instruction.mnemonic}:{form.id}: constraint has no field"
            )
        ranges = tuple(normalize_range(value) for value in constraint.allow)
        kind = "allow_ranges" if ranges else f"exclude_{constraint.exclude[0]}"
        constraints.append(
            ConstraintIR(
                binding.marker,
                gather_positions(form.pattern.code, binding.marker),
                kind,
                ranges,
                constraint.reason,
            )
        )
    layout = tuple(
        ParseEaIR(
            operand.name,
            operand.source.field_symbol,
            operand.source.profile,
            0,
            10,
        )
        if isinstance(operand.source, EffectiveAddressSourceIR)
        else ReadPayloadIR(
            operand.name,
            operand.source.width,
            operand.source.signed,
        )
        for operand in operands
        if isinstance(
            operand.source,
            (EffectiveAddressSourceIR, AppendedPayloadSourceIR),
        )
    )
    repeat = bundle.instruction.to_dict().get("repeat")
    if repeat is None:
        repeat_ir = RepeatControlIR(False, False, "", "")
    elif repeat["type"] == "rep":
        repeat_ir = RepeatControlIR(True, False, "", "")
    else:
        observed = repeat["observed_value"]
        observed_kind = "computed" if observed == "computed" else (
            "source"
            if bundle.instruction.to_dict()["operands"][observed]["role"] == "source"
            else "result"
        )
        repeat_ir = RepeatControlIR(True, True, observed_kind, "" if observed == "computed" else observed)
    privilege = "supervisor" if bundle.instruction.privileged else "unprivileged"
    sizes = form.syntax.selected_size_codes
    if not sizes and form.syntax.fixed_size_suffix:
        sizes = (form.syntax.fixed_size_suffix.removeprefix("."),)
    fixed_bytes = encoding_class.opcode_space_bytes + sum(
        item.width // 8 for item in layout if isinstance(item, ReadPayloadIR)
    )
    required_flags = tuple(
        field.id for field in bundle.required_cpuid_flags
    )
    key = f"{bundle.owner}.{bundle.instruction.mnemonic}.{form.id}"
    return FormIR(
        key,
        index,
        bundle.instruction.mnemonic,
        form.syntax.code,
        encoding_class.name,
        encoding_class.opcode_space_bytes,
        form.pattern.bit_width,
        form.pattern.fixed_value,
        form.pattern.fixed_mask,
        fields_ir,
        tuple(constraints),
        operands,
        layout,
        tuple(sizes),
        tuple(
            OperandOverlapIR(item.operands[0], item.operands[1], item.type)
            for item in form.overlaps
        ),
        ControlIR(
            bundle.instruction.route,
            {
                "base": "base",
                "FP": "fpu",
                "FPTRANSA": "fpu.transcendental_approx",
                "VECTOR": "vector",
            }[bundle.owner],
            "",
            "",
            privilege,
            "conditional" if "cc" in bundle.instruction.to_dict()["operands"] else "none",
            any(isinstance(item.source, EffectiveAddressSourceIR) for item in operands),
            repeat_ir,
        ),
        (AvailabilityRuleIR("all_forms", (), (), required_flags),),
        fixed_bytes,
        fixed_bytes,
        fixed_bytes + sum(10 for item in layout if isinstance(item, ParseEaIR)),
        None,
    )


@lru_cache(maxsize=1)
def _load_decode_ir(root: Path) -> DecodeIR:
    from ..project import IsaProject

    project = IsaProject.load(root)
    effective_addresses = _effective_addresses(project)
    pending = []
    for reference in project.catalog.instruction_order:
        bundle = project.catalog.instructions.resolve(reference)
        for form in bundle.encodings.forms:
            key = f"{bundle.owner}.{bundle.instruction.mnemonic}.{form.id}"
            pending.append((key, bundle, form))
    pending.sort(key=lambda item: item[0])
    forms_ir = tuple(
        _form_ir(project, bundle, form, index)
        for index, (_, bundle, form) in enumerate(pending)
    )
    flags = tuple(
        CpuidFlagIR(name, name, 0, 0, 0, index)
        for index, name in enumerate(("FP", "FPTRANSA", "VECTOR"))
    )
    return DecodeIR(
        flags,
        tuple(sorted({form.mnemonic for form in forms_ir})),
        (),
        _derive_limits(forms_ir, effective_addresses),
        forms_ir,
        effective_addresses,
    )


def load_decode_ir(defs_root: Path = DEFAULT_DEFS_ROOT) -> DecodeIR:
    candidate = Path(defs_root).resolve()
    root = next(
        (
            path
            for path in (candidate, *candidate.parents)
            if (path / "schemas" / "instruction.yaml").is_file()
            and (path / "model.yaml").is_file()
        ),
        None,
    )
    if root is None:
        raise ValueError(f"cannot locate current ISA root from {candidate}")
    return _load_decode_ir(root)

def decode_ir_dict(ir: DecodeIR) -> dict[str, Any]:
    def value(item: Any) -> Any:
        if is_dataclass(item):
            return {field.name: value(getattr(item, field.name)) for field in fields(item)}
        if isinstance(item, tuple):
            return [value(member) for member in item]
        if isinstance(item, dict):
            return {str(key): value(item[key]) for key in sorted(item, key=str)}
        return item

    return value(ir)


def decode_ir_json(ir: DecodeIR, *, indent: int | None = 2) -> str:
    return json.dumps(
        decode_ir_dict(ir),
        indent=indent,
        sort_keys=True,
        separators=(",", ":") if indent is None else None,
    ) + "\n"
