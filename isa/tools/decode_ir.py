#!/usr/bin/env python3
"""Build and inspect the canonical target-independent ISA Decode IR."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field as dataclass_field, fields, is_dataclass
import json
from functools import lru_cache
from pathlib import Path
import sys
from typing import Any

from encoding_architecture import ENCODING_CLASSES_BY_NAME, extended_instruction_lengths
from defs_schema import (
    EXECUTION_ROUTES,
    FLAG_BANK_FLAGS,
    FLAG_EFFECT_KINDS,
    FLAG_EFFECT_REFERENCE_KIND,
    FormApplicability,
    LogicalOperandDefinition,
    OperationArtifacts,
    OperationEventContract,
    OperationFlagBankContract,
    OperationRepeatEligibility,
    PredicateContract,
    PublicInstructionRef,
    parse_assembly_template,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEFS_ROOT = ROOT / "isa" / "instructions" / "definitions"
DEFAULT_EA_DEFINITION = ROOT / "isa" / "addressing" / "effective_address" / "definition.yaml"
MAX_VALUE_WIDTH = 64
MAX_RECORD_BYTES = max(extended_instruction_lengths())


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
class FlagEffectAnnotationIR:
    bank: str
    flag: str
    effect_text: str


@dataclass(frozen=True)
class ExceptionAnnotationIR:
    event: str
    condition_text: str
    forms: tuple[str, ...]


@dataclass(frozen=True)
class AnnotationsIR:
    flag_effects: tuple[FlagEffectAnnotationIR, ...]
    exception_conditions: tuple[ExceptionAnnotationIR, ...]
    touched_flags: tuple[str, ...]
    possible_events: tuple[str, ...]


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
class DestinationOverlapIR:
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
    overlaps: tuple[DestinationOverlapIR, ...]
    control: ControlIR
    annotations: AnnotationsIR
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
    max_fields: int
    max_layout_ops: int
    max_fixed_required_bytes: int
    max_required_bytes: int
    max_record_bytes: int
    compact_ea_values: int
    max_descriptor_bytes: int


@dataclass(frozen=True)
class OperationCaseIR:
    id: str | None
    applies_to: FormApplicability
    additional_requirements: tuple[str, ...]
    resolved_requirements: tuple[str, ...]
    predicate: PredicateContract | None
    flags: tuple[OperationFlagBankContract, ...] | None
    events: tuple[OperationEventContract, ...] | None
    sail_entry: str | None
    conversion: Any | None


@dataclass(frozen=True)
class OperationIR:
    id: str
    public_instruction: PublicInstructionRef
    execution_route: str | None
    privilege: str
    base_requirements: tuple[str, ...]
    repeat: OperationRepeatEligibility
    logical_operand_ids: tuple[str, ...]
    operands: tuple[LogicalOperandDefinition, ...] | None
    forms: tuple[str, ...]
    cases: tuple[OperationCaseIR, ...]
    artifacts: OperationArtifacts | None


@dataclass(frozen=True)
class DecodeIR:
    cpuid_flags: tuple[CpuidFlagIR, ...]
    mnemonics: tuple[str, ...]
    operations: tuple[OperationIR, ...]
    limits: DerivedLimitsIR
    forms: tuple[FormIR, ...]
    effective_addresses: EffectiveAddressIR


@dataclass(frozen=True)
class DecodeInputs:
    store: Any
    operand_types: dict[str, Any]
    ea_registry: Any
    operations: dict[str, Any]
    cpuid_flags: dict[str, Any]
    size_definitions: dict[str, Any]


def pattern_value_mask(pattern: str) -> tuple[int, int]:
    """Return the fixed-bit value and mask for one schema-decoded pattern."""
    value = 0
    mask = 0
    for char in pattern:
        value <<= 1
        mask <<= 1
        if char in "01":
            mask |= 1
            value |= int(char)
    return value, mask


def gather_positions(pattern: str, symbol: str) -> tuple[int, ...]:
    """Return field positions in encoded MSB-to-LSB gather order."""
    return tuple(
        len(pattern) - index - 1
        for index, char in enumerate(pattern)
        if char == symbol
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


def _set_gather_value(payload: int, positions: tuple[int, ...], value: int) -> int:
    for value_bit, position in zip(range(len(positions) - 1, -1, -1), positions):
        if (value >> value_bit) & 1:
            payload |= 1 << position
        else:
            payload &= ~(1 << position)
    return payload


def _operand_legal_values(raw: dict[str, Any]) -> tuple[int, ...]:
    return tuple(
        int(item["value"], 0) if isinstance(item["value"], str) else int(item["value"])
        for item in raw.get("values", ())
    )


@lru_cache(maxsize=None)
def _instruction_set_roots(defs_root: Path) -> tuple[tuple[str, Path], ...]:
    from defs_loader import load_instruction_sets

    resolved = defs_root.resolve()
    return tuple(
        (item.name, item.root.resolve())
        for item in load_instruction_sets(resolved)
    )


def instruction_set_name(defs_root: Path, encoding_path: Path) -> str:
    """Resolve an encoding path through the authoritative instruction-set loader."""
    path = encoding_path.resolve()
    candidates = [
        (len(root.parts), name)
        for name, root in _instruction_set_roots(defs_root.resolve())
        if path.is_relative_to(root / "instructions")
    ]
    if not candidates:
        raise ValueError(f"encoding path is outside every loaded instruction set: {path}")
    return max(candidates)[1]


def load_decode_inputs(defs_root: Path = DEFAULT_DEFS_ROOT) -> DecodeInputs:
    """Load the existing typed schema/loader/store owners used by Decode IR."""
    from defs_loader import (
        extension_cpuid_requirements,
        load_cpuid_flags,
        load_extensions,
        load_operation,
        load_operand_types,
        load_size_definitions,
        load_yaml,
    )
    from defs_schema import decode_ea_registry
    from defs_loader import (
        load_architectural_event_causes, load_architectural_event_ids,
        load_flag_effect_definitions, load_named_values, load_semantic_conditions,
    )
    from encoding_store import load_encoding_store

    resolved = defs_root.resolve()
    store = load_encoding_store(resolved)
    extensions = load_extensions(resolved)
    cpuid_flags = load_cpuid_flags(resolved)
    operand_types = load_operand_types(resolved, extensions)
    size_definitions = load_size_definitions(resolved, extensions)
    ea_path = (
        DEFAULT_EA_DEFINITION
        if resolved == DEFAULT_DEFS_ROOT.resolve()
        else resolved / "ea.yaml"
    )
    ea_registry = decode_ea_registry(ea_path, load_yaml(ea_path))
    known_cpuid_flags, requirements_by_set = extension_cpuid_requirements(
        extensions, cpuid_flags
    )

    known_event_ids = load_architectural_event_ids(ROOT / "isa" / "conformance" / "architecture_tables.yaml")
    known_event_causes = load_architectural_event_causes(ROOT / "isa" / "conformance" / "architecture_tables.yaml")
    known_conditions = frozenset(load_semantic_conditions(resolved))
    known_named_values = frozenset(load_named_values(resolved))
    known_flag_definitions = load_flag_effect_definitions(resolved)
    operations: dict[str, Any] = {}
    for located in store.encodings:
        if located.mnemonic in operations:
            continue
        instruction_set = instruction_set_name(resolved, located.path)
        operation = load_operation(
            located.path.parent,
            operand_types=operand_types,
            size_definitions=load_size_definitions(resolved, extensions),
            base_requirements=requirements_by_set[instruction_set],
            known_cpuid_flags=known_cpuid_flags,
            known_event_ids=known_event_ids,
            known_event_causes=known_event_causes,
            known_condition_ids=known_conditions,
            known_named_value_ids=known_named_values,
            known_diagram_kinds=frozenset({"vector-example"}),
            known_flag_effect_definitions=known_flag_definitions,
        )
        operations[located.mnemonic] = operation
    return DecodeInputs(
        store, operand_types, ea_registry, operations, cpuid_flags, size_definitions
    )


def _operation_predicate_mode(operation: Any, form_id: str) -> str:
    """Project the unique runtime predicate mode from typed covering cases."""
    constructors = {
        "none": "none",
        "produce_boolean": "write_boolean",
        "test_temporary": "temporary",
        "counter_and_condition": "counter_and_condition",
        "annul_on_false": "annul_on_false",
    }
    modes = {
        constructors[case.predicate.kind]
        for case in operation.cases
        if form_id in case.applies_to.forms and case.predicate is not None
    }
    if len(modes) != 1:
        raise ValueError(
            f"{operation.id}: form {form_id} has no unique typed predicate mode: {sorted(modes)}"
        )
    return next(iter(modes))


def _normalized_fields(form: Any, field_types: Any) -> tuple[FieldIR, ...]:
    declarations: dict[str, str] = {}
    for operand in form.operands:
        if operand.field is not None:
            declarations[operand.field] = operand.type
    for symbol, field in form.fields.items():
        declarations[symbol] = field.type
    return tuple(
        FieldIR(
            symbol=symbol,
            type_name=type_name,
            kind=field_types.types[type_name].allocation_kind,
            width=field_types.types[type_name].width,
            positions=gather_positions(form.bits, symbol),
        )
        for symbol, type_name in sorted(declarations.items())
    )


def _normalized_constraints(form: Any) -> tuple[ConstraintIR, ...]:
    result = []
    for constraint in form.constraints:
        if constraint.allow:
            kind = "allow_ranges"
            ranges = tuple(normalize_range(item) for item in constraint.allow)
        else:
            kind = f"exclude_{constraint.exclude}"
            ranges = ()
        result.append(
            ConstraintIR(
                field_symbol=constraint.field,
                positions=gather_positions(form.bits, constraint.field),
                kind=kind,
                ranges=ranges,
                reason=constraint.reason or "",
            )
        )
    return tuple(result)


def _normalized_operands(
    form: Any,
    operand_types: dict[str, Any],
) -> tuple[OperandIR, ...]:
    from defs_schema import displayed_assembly_operands, parse_assembly_template

    template = parse_assembly_template(form.syntax, form.id)
    decimal_literals = [
        item.literal for item in displayed_assembly_operands(template)
        if item.kind == "decimal"
    ]
    result: list[OperandIR] = []
    for operand in form.operands:
        raw = operand_types[operand.type]
        positions = gather_positions(form.bits, operand.field) if operand.field else ()
        if raw.get("kind") == "effective_address":
            source: OperandSourceIR = EffectiveAddressSourceIR(
                field_symbol=operand.field or "",
                positions=positions,
                profile=str(raw["profile"]),
            )
        elif operand.field is not None:
            source = EncodedFieldSourceIR(operand.field, positions)
        elif raw.get("kind") == "fixed_register":
            source = FixedSourceIR(None, str(raw.get("register", "")))
        elif operand.type == "imm" and decimal_literals:
            source = FixedSourceIR(int(decimal_literals.pop(0)), "")
        else:
            source = AppendedPayloadSourceIR(
                width=int(raw["bit_width"]),
                signed=bool(raw.get("signed", False)),
            )
        result.append(
            OperandIR(
                name=operand.name,
                type_name=operand.type,
                type_width=int(raw["bit_width"]),
                access=operand.access,
                domain=operand.domain or "",
                ea_role=operand.ea_role or "",
                ea_width=operand.ea_width or "",
                legal_values=_operand_legal_values(raw),
                source=source,
            )
        )
    return tuple(result)


def _pattern_ir(pattern: str) -> BitPatternIR:
    value, mask = pattern_value_mask(pattern)
    return BitPatternIR(len(pattern), value, mask)


def _ea_form_ir(
    form: Any,
    *,
    member_of_descriptor_family: str,
    descriptor_bytes: int,
    default_kind: str,
    payloads: dict[str, Any],
    field_types: Any,
) -> EaFormIR:
    joined = "".join(form.pattern)
    value, mask = pattern_value_mask(joined)
    payload = payloads.get(form.payload) if form.payload else None
    return EaFormIR(
        name=form.name,
        member_of_descriptor_family=member_of_descriptor_family,
        descriptor_bytes=descriptor_bytes,
        patterns=tuple(_pattern_ir(pattern) for pattern in form.pattern),
        width=len(joined),
        value=value,
        mask=mask,
        kind=form.kind or default_kind,
        fields=tuple(
            EaFieldIR(
                symbol=symbol,
                type_name=field.type,
                role=field.role,
                width=field_types.types[field.type].width,
                positions=gather_positions(joined, symbol),
            )
            for symbol, field in sorted(form.fields.items())
        ),
        segment=form.segment or "",
        payload_name=form.payload or "",
        payload_width=payload.bit_width if payload else 0,
        payload_signed=payload.signed if payload else False,
        base=form.base or "",
        register_name=form.register or "",
        referenced_descriptor_family=form.descriptor or "",
        update_target=form.update.target if form.update else "",
        update_mode=form.update.mode if form.update else "",
    )


def _build_effective_addresses(ea_registry: Any, field_types: Any) -> EffectiveAddressIR:
    family_specs = (
        ("ext1", ea_registry.ext1_kind, ea_registry.ext1_forms),
        ("ext2", ea_registry.ext2_kind, ea_registry.ext2_forms),
    )
    descriptor_lengths: dict[str, int] = {}
    for name, _, forms in family_specs:
        pattern_lengths = {len(form.pattern) for form in forms}
        if len(pattern_lengths) != 1:
            raise ValueError(f"{name}: descriptor forms have inconsistent byte lengths")
        descriptor_lengths[name] = pattern_lengths.pop()
    scalar_compact_forms = tuple(
        _ea_form_ir(
            form,
            member_of_descriptor_family="",
            descriptor_bytes=descriptor_lengths.get(form.descriptor or "", 0),
            default_kind="",
            payloads=ea_registry.payloads,
            field_types=field_types,
        )
        for form in ea_registry.compact_forms
    )
    descriptor_families = tuple(
        EaDescriptorFamilyIR(
            name=name,
            descriptor_bytes=descriptor_lengths[name],
            kind=kind,
            forms=tuple(
                _ea_form_ir(
                    form,
                    member_of_descriptor_family=name,
                    descriptor_bytes=descriptor_lengths[name],
                    default_kind=kind,
                    payloads=ea_registry.payloads,
                    field_types=field_types,
                )
                for form in forms
            ),
        )
        for name, kind, forms in family_specs
    )
    profiles: list[EaProfileIR] = []
    for profile_name, profile in ea_registry.compact_profiles.items():
        override_by_raw = {
            int(override.pattern, 2): override for override in profile.overrides
        }
        replacement_forms = tuple(
            _ea_form_ir(
                override.form,
                member_of_descriptor_family="",
                descriptor_bytes=descriptor_lengths.get(
                    override.form.descriptor or "", 0
                ),
                default_kind="",
                payloads=ea_registry.payloads,
                field_types=field_types,
            )
            for override in profile.overrides
            if override.form is not None
        )
        compact_forms = scalar_compact_forms + replacement_forms
        entries: list[CompactEaEntryIR] = []
        used_forms: dict[str, EaFormIR] = {}
        for raw in range(1 << ea_registry.compact_field_width):
            override = override_by_raw.get(raw)
            if override is not None and override.reserved:
                matches = []
            elif override is not None:
                matches = [
                    form for form in replacement_forms if raw & form.mask == form.value
                ]
            else:
                matches = [
                    form for form in scalar_compact_forms if raw & form.mask == form.value
                ]
            if not matches:
                entries.append(
                    CompactEaEntryIR(
                        raw=raw,
                        valid=False,
                        reserved=True,
                        invalid_reason=f"unallocated compact {profile_name.upper()} value",
                        form_name="",
                        kind="invalid",
                        descriptor_family="",
                        descriptor_bytes=0,
                        payload_name="",
                        payload_width=0,
                        payload_signed=False,
                        consumed_bytes=0,
                    )
                )
                continue
            if len(matches) != 1:
                raise ValueError(
                    f"compact {profile_name.upper()} 0x{raw:02x} matches multiple forms"
                )
            form = matches[0]
            used_forms[form.name] = form
            entries.append(
                CompactEaEntryIR(
                    raw=raw,
                    valid=True,
                    reserved=False,
                    invalid_reason="",
                    form_name=form.name,
                    kind=form.kind,
                    descriptor_family=form.referenced_descriptor_family,
                    descriptor_bytes=form.descriptor_bytes,
                    payload_name=form.payload_name,
                    payload_width=form.payload_width,
                    payload_signed=form.payload_signed,
                    consumed_bytes=form.descriptor_bytes + form.payload_width // 8,
                )
            )
        profiles.append(
            EaProfileIR(
                name=profile.name,
                operand_type=profile.operand_type,
                compact_forms=tuple(used_forms.values()),
                compact_entries=tuple(entries),
                immediate_conversion=profile.immediate_conversion or "",
                lane_model=profile.lane_model or "",
                base_update=profile.base_update or "",
                index_update=profile.index_update or "",
                predicate_affects_update=profile.predicate_affects_update,
                scatter_gather=profile.scatter_gather or "",
            )
        )
    profile_index = {profile.name: profile for profile in profiles}
    scalar_profile = profile_index["ea"]
    return EffectiveAddressIR(
        compact_width=ea_registry.compact_field_width,
        payloads=tuple(
            EaPayloadIR(
                name,
                payload.kind,
                payload.bit_width,
                payload.signed,
                payload.format or "",
            )
            for name, payload in sorted(ea_registry.payloads.items())
        ),
        compact_forms=scalar_profile.compact_forms,
        compact_entries=scalar_profile.compact_entries,
        profiles=tuple(profiles),
        descriptor_families=descriptor_families,
    )


def build_representative_record(
    form: Any,
    operand_types: dict[str, Any],
    opcode_space_bytes: int,
) -> tuple[int, ...] | None:
    """Build the canonical representative record for one resolved schema form."""
    value, _ = pattern_value_mask(form.bits)
    for constraint in form.constraints:
        selected = normalize_range(constraint.allow[0]).lower if constraint.allow else 0x10
        value = _set_gather_value(
            value,
            gather_positions(form.bits, constraint.field),
            selected,
        )
    operands = _normalized_operands(form, operand_types)
    appended_bytes = sum(
        operand.source.width // 8
        for operand in operands
        if isinstance(operand.source, AppendedPayloadSourceIR)
    )
    total = opcode_space_bytes + appended_bytes
    if opcode_space_bytes == 1:
        record = [value]
    elif opcode_space_bytes == 2:
        full = (0b10 << 14) | value
        record = [(full >> 8) & 0xFF, full & 0xFF]
    else:
        if total > MAX_RECORD_BYTES:
            return None
        record = [
            0b11000000
            | ((total - 3) << 2)
            | ((value >> ((opcode_space_bytes - 1) * 8)) & 0x3)
        ]
        record.extend(
            (value >> shift) & 0xFF
            for shift in range((opcode_space_bytes - 2) * 8, -1, -8)
        )
    record.extend([0] * appended_bytes)
    return tuple(record)


def _operation_annotations(operation: Any, form_id: str) -> AnnotationsIR:
    """Project one form's annotations from every typed covering operation case."""

    cases = tuple(
        case for case in operation.cases if form_id in case.applies_to.forms
    )
    flag_effects = tuple(
        dict.fromkeys(
            FlagEffectAnnotationIR(bank.bank, effect.flag, effect.effect)
            for case in cases
            for bank in case.flags
            for effect in bank.effects
            if effect.effect != "preserve"
        )
    )
    exceptions = tuple(
        dict.fromkeys(
            ExceptionAnnotationIR(
                event.event, event.condition, case.applies_to.forms
            )
            for case in cases
            for event in case.events
        )
    )
    return AnnotationsIR(
        flag_effects=flag_effects,
        exception_conditions=exceptions,
        touched_flags=tuple(
            dict.fromkeys(f"{item.bank}.{item.flag}" for item in flag_effects)
        ),
        possible_events=tuple(dict.fromkeys(item.event for item in exceptions)),
    )


def _operation_repeat_control(repeat: OperationRepeatEligibility) -> RepeatControlIR:
    observed = repeat.observed
    return RepeatControlIR(
        rep=repeat.kind in {"rep", "rep_and_repcc"},
        repcc=repeat.kind == "rep_and_repcc",
        observed_kind=observed.kind if observed is not None else "",
        observed_operand=(getattr(observed, "operand", None) or "")
        if observed is not None
        else "",
    )


def _availability_rules(
    operation: Any,
    form: Any,
    normalized_fields: tuple[FieldIR, ...],
    size_definitions: dict[str, Any],
) -> tuple[AvailabilityRuleIR, ...]:
    """Project the exact typed case partition covering one encoded form."""

    field_by_domain = {
        field.type_name.removeprefix("size."): field
        for field in normalized_fields
        if field.type_name.startswith("size.")
    }
    rules: list[AvailabilityRuleIR] = []
    for case in operation.cases:
        if form.id not in case.applies_to.forms:
            continue
        selectors: list[AvailabilitySelectorIR] = []
        for selector in case.applies_to.selectors:
            field = field_by_domain.get(selector.domain)
            if field is None:
                raise ValueError(
                    f"{operation.id}:{case.id}: selector {selector.domain!r} "
                    f"has no encoded field on {form.id}"
                )
            kind = size_definitions.get("size_kinds", {}).get(selector.domain)
            if not isinstance(kind, dict) or not isinstance(kind.get("values"), list):
                raise ValueError(
                    f"{operation.id}:{case.id}: unknown size domain {selector.domain!r}"
                )
            code_values = {
                str(item["code"]): (
                    int(item["value"], 0)
                    if isinstance(item["value"], str)
                    else int(item["value"])
                )
                for item in kind["values"]
            }
            unknown = set(selector.values) - code_values.keys()
            if unknown:
                raise ValueError(
                    f"{operation.id}:{case.id}: selector {selector.domain!r} "
                    f"has unknown values {sorted(unknown)}"
                )
            selectors.append(
                AvailabilitySelectorIR(
                    domain=selector.domain,
                    field_symbol=field.symbol,
                    positions=field.positions,
                    encoded_values=tuple(code_values[value] for value in selector.values),
                )
            )
        rules.append(
            AvailabilityRuleIR(
                case_id=case.id or "",
                selectors=tuple(selectors),
                operand_profiles=tuple(
                    AvailabilityOperandProfileIR(item.operand, item.profiles)
                    for item in case.applies_to.operand_profiles
                ),
                required_cpuid_flags=case.resolved_requirements,
            )
        )
    if not rules:
        raise ValueError(f"{operation.id}: form {form.id} has no availability rule")
    return tuple(rules)


def _build_form(
    index: int,
    located: Any,
    operand_types: dict[str, Any],
    operation: Any,
    effective_addresses: EffectiveAddressIR,
    store: Any,
    size_definitions: dict[str, Any],
) -> FormIR:
    form = located.form
    encoding_class = store.classes_by_name[form.encoding_class]
    value, mask = pattern_value_mask(form.bits)
    operands = _normalized_operands(form, operand_types)
    layout: tuple[LayoutOpIR, ...] = tuple(
        ParseEaIR(
            operand_name=operand.name,
            field_symbol=operand.source.field_symbol,
            profile=operand.source.profile,
            minimum_bytes=min(
                entry.consumed_bytes
                for profile in effective_addresses.profiles
                if profile.name == operand.source.profile
                for entry in profile.compact_entries
                if entry.valid
            ),
            maximum_bytes=max(
                entry.consumed_bytes
                for profile in effective_addresses.profiles
                if profile.name == operand.source.profile
                for entry in profile.compact_entries
                if entry.valid
            ),
        )
        for operand in operands
        if isinstance(operand.source, EffectiveAddressSourceIR)
    ) + tuple(
        ReadPayloadIR(
            operand_name=operand.name,
            width=operand.source.width,
            signed=operand.source.signed,
        )
        for operand in operands
        if isinstance(operand.source, AppendedPayloadSourceIR)
    )
    fixed_required_bytes = encoding_class.opcode_space_bytes + sum(
        op.width // 8 for op in layout if isinstance(op, ReadPayloadIR)
    )
    if operation.execution_route is None:
        raise ValueError(f"{operation.id}: Form IR requires an execution route")
    route = operation.execution_route
    instruction_class = ""
    family = ""
    privilege = operation.privilege
    predicate_mode = _operation_predicate_mode(operation, form.id)
    repeat_control = _operation_repeat_control(operation.repeat)
    annotations = _operation_annotations(operation, form.id)
    normalized_fields = _normalized_fields(form, store.field_types)
    return FormIR(
        key=form.id,
        index=index,
        mnemonic=parse_assembly_template(
            form.syntax, f"{located.path}:{form.id}"
        ).mnemonic,
        syntax=form.syntax,
        opcode_class=form.encoding_class,
        opcode_space_bytes=encoding_class.opcode_space_bytes,
        opcode_width=len(form.bits),
        opcode_value=value,
        opcode_mask=mask,
        fields=normalized_fields,
        constraints=_normalized_constraints(form),
        operands=operands,
        layout=layout,
        sizes=form.sizes,
        overlaps=tuple(
            DestinationOverlapIR(item.operands[0], item.operands[1], item.rule)
            for item in form.destination_overlap
        ),
        control=ControlIR(
            route=route,
            instruction_set=instruction_set_name(store.defs_root, located.path),
            instruction_class=instruction_class,
            family=family,
            privilege=privilege,
            predicate_mode=predicate_mode,
            has_ea_operand=any(
                isinstance(operand.source, EffectiveAddressSourceIR)
                for operand in operands
            ),
            repeat=repeat_control,
        ),
        annotations=annotations,
        availability_rules=_availability_rules(
            operation, form, normalized_fields, size_definitions
        ),
        fixed_required_bytes=fixed_required_bytes,
        minimum_required_bytes=fixed_required_bytes
        + sum(op.minimum_bytes for op in layout if isinstance(op, ParseEaIR)),
        maximum_required_bytes=fixed_required_bytes
        + sum(op.maximum_bytes for op in layout if isinstance(op, ParseEaIR)),
        representative_record=build_representative_record(
            form, operand_types, encoding_class.opcode_space_bytes
        ),
    )


def _derive_limits(
    forms_ir: tuple[FormIR, ...],
    effective_addresses: EffectiveAddressIR,
) -> DerivedLimitsIR:
    return DerivedLimitsIR(
        form_count=len(forms_ir),
        mnemonic_count=len({form.mnemonic for form in forms_ir}),
        max_opcode_width=max(
            (encoding_class.allocation_bits for encoding_class in ENCODING_CLASSES_BY_NAME.values()),
            default=0,
        ),
        max_operands=max((len(form.operands) for form in forms_ir), default=0),
        max_ea_operands=max(
            (
                sum(
                    isinstance(operand.source, EffectiveAddressSourceIR)
                    for operand in form.operands
                )
                for form in forms_ir
            ),
            default=0,
        ),
        max_fields=max((len(form.fields) for form in forms_ir), default=0),
        max_layout_ops=max((len(form.layout) for form in forms_ir), default=0),
        max_fixed_required_bytes=max(
            (form.fixed_required_bytes for form in forms_ir), default=0
        ),
        max_required_bytes=max(
            (form.maximum_required_bytes for form in forms_ir), default=0
        ),
        max_record_bytes=MAX_RECORD_BYTES,
        compact_ea_values=len(effective_addresses.compact_entries),
        max_descriptor_bytes=max(
            (
                family.descriptor_bytes
                for family in effective_addresses.descriptor_families
            ),
            default=0,
        ),
    )


def build_decode_ir(
    store: Any,
    operand_types: dict[str, Any],
    ea_registry: Any,
    operations: dict[str, Any] | None = None,
    cpuid_flags: dict[str, Any] | None = None,
    size_definitions: dict[str, Any] | None = None,
) -> DecodeIR:
    """Normalize existing authoritative decoded inputs into the canonical IR."""
    if operations is None or cpuid_flags is None or size_definitions is None:
        inputs = load_decode_inputs(store.defs_root)
        if operations is None:
            operations = inputs.operations
        if cpuid_flags is None:
            cpuid_flags = inputs.cpuid_flags
        if size_definitions is None:
            size_definitions = inputs.size_definitions
    missing_operations = {
        located.mnemonic
        for located in store.encodings
        if located.mnemonic not in operations
    }
    if missing_operations:
        raise ValueError(
            "encoding forms require canonical operations: "
            + ", ".join(sorted(missing_operations))
        )
    effective_addresses = _build_effective_addresses(ea_registry, store.field_types)
    located_forms = sorted(store.encodings, key=lambda item: item.form.id)
    forms_ir = tuple(
        _build_form(
            index,
            located,
            operand_types,
            operations[located.mnemonic],
            effective_addresses,
            store,
            size_definitions,
        )
        for index, located in enumerate(located_forms)
    )
    operations_ir = tuple(
        OperationIR(
            id=operation.id,
            public_instruction=operation.public_instruction,
            execution_route=operation.execution_route,
            privilege=operation.privilege,
            base_requirements=operation.base_requirements,
            repeat=operation.repeat,
            logical_operand_ids=operation.logical_operand_ids,
            operands=operation.operands,
            forms=operation.forms,
            cases=tuple(
                OperationCaseIR(
                    id=case.id,
                    applies_to=case.applies_to,
                    additional_requirements=case.additional_requirements,
                    resolved_requirements=case.resolved_requirements,
                    predicate=case.predicate,
                    flags=case.flags,
                    events=case.events,
                    sail_entry=case.sail_entry,
                    conversion=case.conversion,
                )
                for case in operation.cases
            ),
            artifacts=operation.artifacts,
        )
        for operation in sorted(operations.values(), key=lambda item: item.id)
    )
    ir = DecodeIR(
        cpuid_flags=tuple(
            CpuidFlagIR(
                id=flag.id,
                token=flag.token,
                selector_class=flag.location.selector_class,
                leaf=flag.location.leaf,
                index=flag.location.index,
                bit=flag.location.bit,
            )
            for flag in cpuid_flags.values()
        ),
        mnemonics=tuple(sorted({form.mnemonic for form in forms_ir})),
        operations=operations_ir,
        limits=_derive_limits(forms_ir, effective_addresses),
        forms=forms_ir,
        effective_addresses=effective_addresses,
    )
    validate_decode_ir(ir)
    return ir


def load_decode_ir(defs_root: Path = DEFAULT_DEFS_ROOT) -> DecodeIR:
    inputs = load_decode_inputs(defs_root)
    return build_decode_ir(
        inputs.store,
        inputs.operand_types,
        inputs.ea_registry,
        inputs.operations,
        inputs.cpuid_flags,
        inputs.size_definitions,
    )


def _validate_positions(
    positions: tuple[int, ...],
    *,
    width: int,
    expected_count: int,
    context: str,
) -> None:
    if len(positions) != expected_count:
        raise ValueError(f"{context}: gather width mismatch")
    if any(position < 0 or position >= width for position in positions):
        raise ValueError(f"{context}: gather position out of range")
    if len(set(positions)) != len(positions) or any(
        left <= right for left, right in zip(positions, positions[1:])
    ):
        raise ValueError(f"{context}: gather positions must be unique MSB-to-LSB")


def _validate_ea(ir: DecodeIR) -> None:
    ea = ir.effective_addresses
    if ea.compact_width != 7:
        raise ValueError("compact EA width must be exactly 7 bits")
    payloads = {payload.name: payload for payload in ea.payloads}
    if len(payloads) != len(ea.payloads) or any(
        payload.width <= 0 or payload.width % 8 for payload in ea.payloads
    ):
        raise ValueError("EA payload names and byte widths must be valid")

    def validate_form(form: EaFormIR, context: str) -> None:
        value = 0
        mask = 0
        total_width = 0
        for pattern in form.patterns:
            if (
                pattern.width <= 0
                or pattern.width > MAX_VALUE_WIDTH
                or pattern.value & ~pattern.mask
                or pattern.mask >= 1 << pattern.width
            ):
                raise ValueError(f"{context}: invalid byte mask/value pattern")
            value = (value << pattern.width) | pattern.value
            mask = (mask << pattern.width) | pattern.mask
            total_width += pattern.width
        if (form.width, form.value, form.mask) != (total_width, value, mask):
            raise ValueError(f"{context}: combined mask/value mismatch")
        form_fields = {field.symbol: field for field in form.fields}
        if len(form_fields) != len(form.fields):
            raise ValueError(f"{context}: duplicate field symbol")
        claimed_positions: set[int] = set()
        for ea_field in form.fields:
            _validate_positions(
                ea_field.positions,
                width=form.width,
                expected_count=ea_field.width,
                context=f"{context}/{ea_field.symbol}",
            )
            overlap = claimed_positions & set(ea_field.positions)
            if overlap:
                raise ValueError(f"{context}: fields overlap at bit {max(overlap)}")
            claimed_positions.update(ea_field.positions)
        variable_positions = {
            position for position in range(form.width) if not form.mask & (1 << position)
        }
        if claimed_positions != variable_positions:
            raise ValueError(f"{context}: fields do not cover the variable pattern bits")
        if form.update_target and form.update_target not in form_fields:
            raise ValueError(f"{context}: update target references an unknown field")
        payload = payloads.get(form.payload_name) if form.payload_name else None
        if form.payload_name and payload is None:
            raise ValueError(f"{context}: unknown payload reference")
        if payload is None:
            expected_payload = (0, False)
        else:
            expected_payload = (payload.width, payload.signed)
        if (form.payload_width, form.payload_signed) != expected_payload:
            raise ValueError(f"{context}: payload reference mismatch")

    expected_raw = tuple(range(1 << ea.compact_width))
    profile_names = tuple(profile.name for profile in ea.profiles)
    if profile_names != ("ea", "fea", "vea"):
        raise ValueError("compact profiles must be ordered EA, FEA, and VEA")
    if tuple(profile.operand_type for profile in ea.profiles) != ("EA", "FEA", "VEA"):
        raise ValueError("compact profile operand types do not match their profiles")
    scalar_profile = ea.profiles[0]
    if (
        ea.compact_forms != scalar_profile.compact_forms
        or ea.compact_entries != scalar_profile.compact_entries
    ):
        raise ValueError("scalar compact EA compatibility aliases differ from profile EA")
    family_names = tuple(family.name for family in ea.descriptor_families)
    families = {family.name: family for family in ea.descriptor_families}
    if family_names != ("ext1", "ext2"):
        raise ValueError("descriptor families must be EXT1 and EXT2")
    if (
        families["ext1"].descriptor_bytes != 1
        or families["ext2"].descriptor_bytes != 2
    ):
        raise ValueError("EXT1 and EXT2 descriptor lengths must be 1 and 2")

    for profile in ea.profiles:
        if tuple(entry.raw for entry in profile.compact_entries) != expected_raw:
            raise ValueError(
                f"compact {profile.name.upper()} table must contain all ordered raw values"
            )
        compact_names = {form.name for form in profile.compact_forms}
        if len(compact_names) != len(profile.compact_forms):
            raise ValueError(f"duplicate compact {profile.name.upper()} form name")
        for form in profile.compact_forms:
            context = f"compact {profile.name.upper()} {form.name}"
            validate_form(form, context)
            if form.width != ea.compact_width or len(form.patterns) != 1:
                raise ValueError(f"{context}: invalid pattern width")
            if form.member_of_descriptor_family:
                raise ValueError(f"{context}: unexpected descriptor family tag")
            if form.referenced_descriptor_family:
                family = families.get(form.referenced_descriptor_family)
                if family is None or form.descriptor_bytes != family.descriptor_bytes:
                    raise ValueError(
                        f"{context}: descriptor length is not fixed by its family"
                    )
            elif form.descriptor_bytes != 0:
                raise ValueError(f"{context}: unexpected descriptor length")

    for family in ea.descriptor_families:
        if len({form.name for form in family.forms}) != len(family.forms):
            raise ValueError(f"{family.name}: duplicate descriptor form name")
        for form in family.forms:
            validate_form(form, f"{family.name}/{form.name}")
            if form.member_of_descriptor_family != family.name:
                raise ValueError(f"{family.name}/{form.name}: family reference mismatch")
            if form.referenced_descriptor_family:
                raise ValueError(
                    f"{family.name}/{form.name}: descriptor member references a family"
                )
            if form.descriptor_bytes != family.descriptor_bytes:
                raise ValueError(f"{family.name}/{form.name}: descriptor length mismatch")
            if form.width != family.descriptor_bytes * 8:
                raise ValueError(f"{family.name}/{form.name}: descriptor width mismatch")
            if len(form.patterns) != family.descriptor_bytes or any(
                pattern.width != 8 for pattern in form.patterns
            ):
                raise ValueError(f"{family.name}/{form.name}: descriptor byte pattern mismatch")

    for profile in ea.profiles:
        for entry in profile.compact_entries:
            matches = [
                form
                for form in profile.compact_forms
                if entry.raw & form.mask == form.value
            ]
            context = f"compact {profile.name.upper()} 0x{entry.raw:02x}"
            if not matches:
                if entry.valid or not entry.reserved or not entry.invalid_reason:
                    raise ValueError(f"{context}: invalid entry not explicit")
                continue
            if len(matches) != 1:
                raise ValueError(f"{context}: ambiguous form")
            form = matches[0]
            expected_consumed = form.descriptor_bytes + form.payload_width // 8
            if (
                not entry.valid
                or entry.reserved
                or entry.form_name != form.name
                or entry.descriptor_family != form.referenced_descriptor_family
                or entry.descriptor_bytes != form.descriptor_bytes
                or entry.payload_name != form.payload_name
                or entry.payload_width != form.payload_width
                or entry.payload_signed != form.payload_signed
                or entry.kind != form.kind
                or entry.consumed_bytes != expected_consumed
            ):
                raise ValueError(f"{context}: table entry mismatch")


def validate_decode_ir(ir: DecodeIR) -> None:
    """Validate every invariant owned by the normalized Decode IR."""
    cpuid_flags = {flag.id: flag for flag in ir.cpuid_flags}
    if len(cpuid_flags) != len(ir.cpuid_flags):
        raise ValueError("CPUID flag IDs must be unique")
    if len({flag.token for flag in ir.cpuid_flags}) != len(ir.cpuid_flags):
        raise ValueError("CPUID flag public tokens must be unique")
    if len(
        {
            (flag.selector_class, flag.leaf, flag.index, flag.bit)
            for flag in ir.cpuid_flags
        }
    ) != len(ir.cpuid_flags):
        raise ValueError("CPUID flag locations must be unique")
    keys = tuple(form.key for form in ir.forms)
    if len(set(keys)) != len(keys) or keys != tuple(sorted(keys)):
        raise ValueError("form keys must be unique and ordered")
    if tuple(form.index for form in ir.forms) != tuple(range(len(ir.forms))):
        raise ValueError("form indices must be unique, dense, and ordered")
    if ir.mnemonics != tuple(sorted(set(ir.mnemonics))):
        raise ValueError("mnemonics must be unique and ordered")
    if set(ir.mnemonics) != {form.mnemonic for form in ir.forms}:
        raise ValueError("mnemonic inventory does not match forms")
    operation_ids = tuple(operation.id for operation in ir.operations)
    if operation_ids != tuple(sorted(set(operation_ids))):
        raise ValueError("operation IDs must be unique and ordered")
    public_token_owners: dict[str, str] = {}
    for operation in ir.operations:
        public_tokens = (
            operation.public_instruction.mnemonic,
            *operation.public_instruction.aliases,
        )
        if len(set(public_tokens)) != len(public_tokens):
            raise ValueError(f"{operation.id}: duplicate public instruction token")
        for token in public_tokens:
            previous_owner = public_token_owners.get(token)
            if previous_owner is not None:
                raise ValueError(
                    f"public instruction token {token!r} belongs to both "
                    f"{previous_owner} and {operation.id}"
                )
            public_token_owners[token] = operation.id
    claimed_forms: dict[str, str] = {}
    for operation in ir.operations:
        if operation.execution_route not in EXECUTION_ROUTES:
            raise ValueError(f"{operation.id}: execution route is invalid")
        if operation.operands is None:
            raise ValueError(
                f"{operation.id}: operation has no logical operand definitions"
            )
        if (
            operation.artifacts is None
            or operation.artifacts.bundle_root is None
            or operation.artifacts.manifest_path is None
        ):
            raise ValueError(f"{operation.id}: artifact provenance is incomplete")
        bundle_root = Path(operation.artifacts.bundle_root)
        manifest_path = Path(operation.artifacts.manifest_path)
        if not bundle_root.is_absolute() or manifest_path != bundle_root / "operation.yaml":
            raise ValueError(f"{operation.id}: artifact provenance is invalid")
        if len(set(operation.logical_operand_ids)) != len(
            operation.logical_operand_ids
        ):
            raise ValueError(f"{operation.id}: duplicate logical operand ID")
        if operation.operands is not None and tuple(
            operand.id for operand in operation.operands
        ) != operation.logical_operand_ids:
            raise ValueError(
                f"{operation.id}: complete logical operands do not match membership"
            )
        repeat = operation.repeat
        if repeat.kind not in {"not_eligible", "rep", "rep_and_repcc"}:
            raise ValueError(f"{operation.id}: unknown repeat eligibility")
        if (repeat.kind == "rep_and_repcc") != (repeat.observed is not None):
            raise ValueError(f"{operation.id}: repeat observation presence is invalid")
        if repeat.observed is not None:
            observed_operand = getattr(repeat.observed, "operand", None)
            if repeat.observed.kind == "computed":
                if observed_operand is not None:
                    raise ValueError(
                        f"{operation.id}: computed repeat observation has a payload"
                    )
            elif repeat.observed.kind in {"result", "source"}:
                if (
                    observed_operand is None
                    or observed_operand not in operation.logical_operand_ids
                ):
                    raise ValueError(
                        f"{operation.id}: repeat observation references an unknown "
                        "logical operand"
                    )
            else:
                raise ValueError(f"{operation.id}: unknown repeat observation")
        if len(set(operation.forms)) != len(operation.forms):
            raise ValueError(f"{operation.id}: duplicate operation form reference")
        if len({case.id for case in operation.cases}) != len(operation.cases):
            raise ValueError(f"{operation.id}: duplicate operation case ID")
        case_form_refs = {
            form_id
            for case in operation.cases
            for form_id in case.applies_to.forms
        }
        if case_form_refs != set(operation.forms):
            raise ValueError(f"{operation.id}: case form membership is incomplete")
        for case in operation.cases:
            expected_resolved = tuple(
                sorted(
                    set(operation.base_requirements)
                    | set(case.additional_requirements)
                )
            )
            if case.resolved_requirements != expected_resolved:
                raise ValueError(
                    f"{operation.id}: case CPUID requirements are not resolved"
                )
            unknown_requirements = set(case.resolved_requirements) - cpuid_flags.keys()
            if unknown_requirements:
                raise ValueError(
                    f"{operation.id}: unknown resolved CPUID flags "
                    f"{sorted(unknown_requirements)}"
                )
            if case.flags is not None:
                bank_names = tuple(bank.bank for bank in case.flags)
                if len(set(bank_names)) != len(bank_names):
                    raise ValueError(f"{operation.id}: duplicate flag bank contract")
                for bank in case.flags:
                    expected_flags = FLAG_BANK_FLAGS.get(bank.bank)
                    if expected_flags is None:
                        raise ValueError(f"{operation.id}: unknown flag bank contract")
                    if tuple(effect.flag for effect in bank.effects) != expected_flags:
                        raise ValueError(
                            f"{operation.id}: {bank.bank} effects are not a canonical TotalMap"
                        )
                    expected_completion = {
                        "FLAGS": "complete_image",
                        "FFLAGS": "accrued_causes",
                    }[bank.bank]
                    if bank.completion != expected_completion:
                        raise ValueError(
                            f"{operation.id}: {bank.bank} has invalid flag completion mode"
                        )
                    for effect in bank.effects:
                        if effect.effect not in FLAG_EFFECT_KINDS:
                            raise ValueError(
                                f"{operation.id}: unknown typed flag effect"
                            )
                        requires_reference = (
                            effect.effect in FLAG_EFFECT_REFERENCE_KIND
                        )
                        if requires_reference != (effect.reference is not None):
                            raise ValueError(
                                f"{operation.id}: typed flag reference shape is invalid"
                            )
            if (
                case.id is None
                or case.predicate is None
                or case.flags is None
                or case.events is None
                or case.sail_entry is None
            ):
                raise ValueError(f"{operation.id}: case has missing contract data")
            if case.conversion is not None and (
                not case.conversion.source_formats
                or not case.conversion.destination_formats
            ):
                raise ValueError(f"{operation.id}: conversion signature has an empty format set")
        for form_id in operation.forms:
            if form_id in claimed_forms:
                raise ValueError(
                    f"{form_id}: form belongs to both {claimed_forms[form_id]} and {operation.id}"
                )
            claimed_forms[form_id] = operation.id
    if set(claimed_forms) != {form.key for form in ir.forms}:
        raise ValueError("operation form membership does not match forms")
    forms_by_operation: dict[str, list[FormIR]] = {
        operation.id: [] for operation in ir.operations
    }
    for form in ir.forms:
        forms_by_operation[claimed_forms[form.key]].append(form)
    for operation in ir.operations:
        form_operand_ids = {
            operand.name
            for form in forms_by_operation[operation.id]
            for operand in form.operands
        }
        if set(operation.logical_operand_ids) != form_operand_ids:
            raise ValueError(
                f"{operation.id}: logical operand membership does not match forms"
            )
    for form in ir.forms:
        operation_id = claimed_forms[form.key]
        if public_token_owners.get(form.mnemonic) != operation_id:
            raise ValueError(
                f"{form.key}: form public token {form.mnemonic!r} is not owned by "
                f"operation {operation_id}"
            )

    _validate_ea(ir)
    operations_by_id = {operation.id: operation for operation in ir.operations}
    profiles = {
        profile.name: profile for profile in ir.effective_addresses.profiles
    }
    for form in ir.forms:
        owning_operation = operations_by_id[claimed_forms[form.key]]
        expected_cases = tuple(
            case
            for case in owning_operation.cases
            if form.key in case.applies_to.forms
        )
        if tuple(rule.case_id for rule in form.availability_rules) != tuple(
            case.id for case in expected_cases
        ):
            raise ValueError(f"{form.key}: availability rules do not match case owners")
        for rule, case in zip(form.availability_rules, expected_cases):
            if rule.required_cpuid_flags != case.resolved_requirements:
                raise ValueError(
                    f"{form.key}/{rule.case_id}: availability requirements differ from owner"
                )
            if set(rule.required_cpuid_flags) - cpuid_flags.keys():
                raise ValueError(
                    f"{form.key}/{rule.case_id}: availability references unknown CPUID flag"
                )
            for selector in rule.selectors:
                if not selector.positions or not selector.encoded_values:
                    raise ValueError(
                        f"{form.key}/{rule.case_id}: empty availability selector"
                    )
                if max(selector.encoded_values) >= 1 << len(selector.positions):
                    raise ValueError(
                        f"{form.key}/{rule.case_id}: availability selector value exceeds field"
                    )
        encoding_class = ENCODING_CLASSES_BY_NAME.get(form.opcode_class)
        if encoding_class is None:
            raise ValueError(f"{form.key}: unknown opcode class")
        if not 0 < form.opcode_width <= MAX_VALUE_WIDTH:
            raise ValueError(f"{form.key}: opcode width out of range")
        if form.opcode_value & ~form.opcode_mask:
            raise ValueError(f"{form.key}: opcode value contains an unmasked bit")
        if form.opcode_mask >= 1 << form.opcode_width:
            raise ValueError(f"{form.key}: opcode mask exceeds width")
        if (
            form.opcode_space_bytes != encoding_class.opcode_space_bytes
            or form.opcode_width != encoding_class.allocation_bits
        ):
            raise ValueError(f"{form.key}: opcode byte/width mismatch")
        fields_by_symbol = {field.symbol: field for field in form.fields}
        if len(fields_by_symbol) != len(form.fields):
            raise ValueError(f"{form.key}: duplicate field symbol")
        for field in form.fields:
            _validate_positions(
                field.positions,
                width=form.opcode_width,
                expected_count=field.width,
                context=f"{form.key}/{field.symbol}",
            )
        for constraint in form.constraints:
            field = fields_by_symbol.get(constraint.field_symbol)
            if field is None or constraint.positions != field.positions:
                raise ValueError(f"{form.key}: constraint references an unknown field")
            if constraint.kind == "allow_ranges":
                if not constraint.ranges or any(
                    item.lower < 0
                    or item.lower > item.upper
                    or item.upper >= 1 << field.width
                    for item in constraint.ranges
                ):
                    raise ValueError(f"{form.key}: invalid allowed constraint range")
            elif constraint.kind != "exclude_immediate" or constraint.ranges:
                raise ValueError(f"{form.key}: invalid normalized constraint")

        operands_by_name = {operand.name: operand for operand in form.operands}
        if len(operands_by_name) != len(form.operands):
            raise ValueError(f"{form.key}: duplicate operand name")
        for operand in form.operands:
            source = operand.source
            if operand.type_width < 0 or any(
                value < 0
                or operand.type_width == 0
                or value >= 1 << operand.type_width
                for value in operand.legal_values
            ):
                raise ValueError(f"{form.key}/{operand.name}: operand width/domain mismatch")
            if isinstance(source, (EncodedFieldSourceIR, EffectiveAddressSourceIR)):
                field = fields_by_symbol.get(source.field_symbol)
                if (
                    field is None
                    or source.positions != field.positions
                    or field.width != operand.type_width
                ):
                    raise ValueError(f"{form.key}/{operand.name}: source field mismatch")
                if (
                    isinstance(source, EffectiveAddressSourceIR)
                    and source.profile not in profiles
                ):
                    raise ValueError(
                        f"{form.key}/{operand.name}: unknown effective-address profile"
                    )
            elif isinstance(source, AppendedPayloadSourceIR):
                if (
                    source.width <= 0
                    or source.width % 8
                    or source.width != operand.type_width
                ):
                    raise ValueError(f"{form.key}/{operand.name}: payload width must be bytes")
            elif isinstance(source, FixedSourceIR):
                if source.value is None and not source.identity:
                    raise ValueError(f"{form.key}/{operand.name}: fixed source has no value")
                if source.value is not None and (
                    source.value < 0
                    or operand.type_width <= 0
                    or source.value >= 1 << operand.type_width
                ):
                    raise ValueError(f"{form.key}/{operand.name}: fixed value exceeds type")
            else:  # pragma: no cover - union exhaustiveness guard
                raise ValueError(f"{form.key}/{operand.name}: unknown source variant")

        if any(
            overlap.left not in operands_by_name or overlap.right not in operands_by_name
            for overlap in form.overlaps
        ):
            raise ValueError(f"{form.key}: overlap references an unknown operand")
        expected_has_ea = any(
            isinstance(operand.source, EffectiveAddressSourceIR)
            for operand in form.operands
        )
        valid_control_owner = (
            form.control.route == owning_operation.execution_route
            and form.control.instruction_class == ""
            and form.control.family == ""
            and form.control.privilege == owning_operation.privilege
            and form.control.predicate_mode == _operation_predicate_mode(owning_operation, form.key)
        )
        if (
            form.control.has_ea_operand != expected_has_ea
            or not valid_control_owner
            or form.control.repeat
            != _operation_repeat_control(owning_operation.repeat)
        ):
            raise ValueError(f"{form.key}: invalid static control metadata")
        repeat = form.control.repeat
        if repeat.repcc != bool(repeat.observed_kind) or (
            bool(repeat.observed_operand) and not repeat.observed_kind
        ) or (
            bool(repeat.observed_operand)
            and repeat.observed_operand not in operands_by_name
        ):
            raise ValueError(f"{form.key}: invalid repeat control metadata")
        if form.annotations != _operation_annotations(owning_operation, form.key):
            raise ValueError(f"{form.key}: annotations do not match covering cases")

        expected_layout: tuple[LayoutOpIR, ...] = tuple(
            ParseEaIR(
                operand.name,
                operand.source.field_symbol,
                operand.source.profile,
                min(
                    entry.consumed_bytes
                    for entry in profiles[operand.source.profile].compact_entries
                    if entry.valid
                ),
                max(
                    entry.consumed_bytes
                    for entry in profiles[operand.source.profile].compact_entries
                    if entry.valid
                ),
            )
            for operand in form.operands
            if isinstance(operand.source, EffectiveAddressSourceIR)
        ) + tuple(
            ReadPayloadIR(
                operand.name,
                operand.source.width,
                operand.source.signed,
            )
            for operand in form.operands
            if isinstance(operand.source, AppendedPayloadSourceIR)
        )
        if form.layout != expected_layout:
            raise ValueError(f"{form.key}: layout must order ParseEa before ReadPayload")
        if any(op.operand_name not in operands_by_name for op in form.layout):
            raise ValueError(f"{form.key}: layout references an unknown operand")
        fixed_required = form.opcode_space_bytes + sum(
            op.width // 8 for op in form.layout if isinstance(op, ReadPayloadIR)
        )
        minimum_required = fixed_required + sum(
            op.minimum_bytes for op in form.layout if isinstance(op, ParseEaIR)
        )
        maximum_required = fixed_required + sum(
            op.maximum_bytes for op in form.layout if isinstance(op, ParseEaIR)
        )
        if (
            form.fixed_required_bytes != fixed_required
            or form.minimum_required_bytes != minimum_required
            or form.maximum_required_bytes != maximum_required
        ):
            raise ValueError(f"{form.key}: required lengths are inconsistent")
        if form.representative_record is not None and not all(
            0 <= byte <= 0xFF for byte in form.representative_record
        ):
            raise ValueError(f"{form.key}: representative record contains a non-byte")

    expected_limits = _derive_limits(ir.forms, ir.effective_addresses)
    if ir.limits != expected_limits:
        raise ValueError("derived Decode IR limits are not deterministic")
    if ir.limits.max_record_bytes != MAX_RECORD_BYTES:
        raise ValueError("record byte limit does not match the encoding architecture")
    if (
        ir.limits.max_operands < max((len(form.operands) for form in ir.forms), default=0)
        or ir.limits.max_ea_operands
        < max(
            (
                sum(
                    isinstance(operand.source, EffectiveAddressSourceIR)
                    for operand in form.operands
                )
                for form in ir.forms
            ),
            default=0,
        )
        or ir.limits.max_fields < max((len(form.fields) for form in ir.forms), default=0)
    ):
        raise ValueError("derived slot limits do not cover every form")


def _json_value(value: Any) -> Any:
    if is_dataclass(value):
        return {field.name: _json_value(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(value[key]) for key in sorted(value, key=str)}
    return value


def decode_ir_dict(ir: DecodeIR) -> dict[str, Any]:
    """Return the deterministic JSON-friendly inspection representation."""
    validate_decode_ir(ir)
    return _json_value(ir)


def decode_ir_json(ir: DecodeIR, *, indent: int | None = 2) -> str:
    return json.dumps(
        decode_ir_dict(ir),
        indent=indent,
        sort_keys=True,
        separators=(",", ":") if indent is None else None,
    ) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--defs-root",
        type=Path,
        default=DEFAULT_DEFS_ROOT,
        help=(
            "authoritative isa/instructions/definitions root "
            "(default: repository isa/instructions/definitions)"
        ),
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="emit compact deterministic JSON instead of indented JSON",
    )
    args = parser.parse_args(argv)
    try:
        output = decode_ir_json(
            load_decode_ir(args.defs_root), indent=None if args.compact else 2
        )
    except (OSError, ValueError) as error:
        print(f"Decode IR generation failed: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
