#!/usr/bin/env python3
"""Lower canonical Decode IR into file-level SystemVerilog sections."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from . import decoder_ir as decode_ir
from .emitters import d0 as d0_emitter
from .emitters import d1 as d1_emitter
from .emitters import ea as ea_emitter
from .emitters import package as package_emitter
from ..encoding_architecture import (
    ENCODING_CLASSES,
    ENCODING_CLASSES_BY_NAME,
    OPERATOR_SPACE_PREFIX_BITS,
    OPERATOR_SPACES,
    OperatorSpace,
)


EA_LOW_POSITIONS = (6, 5, 4, 3, 2, 1, 0)
EA_HIGH_POSITIONS = (13, 12, 11, 10, 9, 8, 7)
EA_MEDIUM_ALT_POSITIONS = (16, 15, 14, 3, 2, 1, 0)

EA_LAYOUT_NONE = "EA_LAYOUT_NONE"
EA_LAYOUT_LOW = "EA_LAYOUT_LOW"
EA_LAYOUT_ALT = "EA_LAYOUT_ALT"
EA_LAYOUT_ALT_THEN_LOW = "EA_LAYOUT_ALT_THEN_LOW"


def _width(count: int) -> int:
    return max(1, (count - 1).bit_length())


def _identifier(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").upper()
    return text or "NONE"


def _identifiers(values: Iterable[str], prefix: str) -> dict[str, str]:
    result: dict[str, str] = {}
    used: dict[str, int] = {}
    for value in values:
        base = f"{prefix}_{_identifier(value)}"
        ordinal = used.get(base, 0)
        used[base] = ordinal + 1
        result[value] = base if ordinal == 0 else f"{base}_{ordinal + 1}"
    return result


def _enum(
    type_name: str,
    prefix: str,
    values: Iterable[str],
    *,
    invalid_name: str = "INVALID",
) -> tuple[str, dict[str, str]]:
    ordered = tuple(values)
    names = _identifiers(ordered, prefix)
    width = _width(len(ordered) + 1)
    items = [f"    {prefix}_{invalid_name} = {width}'d0"]
    items.extend(
        f"    // {value or '<empty>'}\n    {names[value]} = {width}'d{index}"
        for index, value in enumerate(ordered, 1)
    )
    return (
        f"typedef enum logic [{width - 1}:0] {{\n"
        + ",\n".join(items)
        + f"\n  }} {type_name};",
        names,
    )


def _ordered(values: Iterable[str], *, empty_first: bool = True) -> tuple[str, ...]:
    unique = set(values)
    if empty_first and "" in unique:
        return ("",) + tuple(sorted(unique - {""}))
    return tuple(sorted(unique))


def _hex(width: int, value: int) -> str:
    return f"{width}'h{value:0{(width + 3) // 4}x}"


def _casez(width: int, value: int, mask: int) -> str:
    limit = (1 << width) - 1
    if value & ~mask or (value | mask) & ~limit:
        raise ValueError(
            f"casez value/mask do not fit {width} bits: value={value:#x}, mask={mask:#x}"
        )
    bits = "".join(
        "1" if value & (1 << bit) else "0" if mask & (1 << bit) else "?"
        for bit in reversed(range(width))
    )
    grouped = "_".join(
        bits[index : index + 4] for index in range(0, len(bits), 4)
    )
    return f"{width}'b{grouped}"


def _gather(signal: str, positions: tuple[int, ...]) -> str:
    if not positions:
        return "64'd0"
    bits = ", ".join(f"{signal}[{position}]" for position in positions)
    return f"{{{bits}}}"


def _ea_operands(form: decode_ir.FormIR) -> tuple[decode_ir.OperandIR, ...]:
    return tuple(
        operand
        for operand in form.operands
        if isinstance(operand.source, decode_ir.EffectiveAddressSourceIR)
    )


def _ea_candidate_slot(form: decode_ir.FormIR, operand: decode_ir.OperandIR) -> int:
    source = operand.source
    if not isinstance(source, decode_ir.EffectiveAddressSourceIR):
        raise ValueError(f"non-EA operand {form.key}/{operand.name}")
    if source.positions == EA_LOW_POSITIONS:
        return 0
    if form.opcode_class == "medium" and source.positions == EA_MEDIUM_ALT_POSITIONS:
        return 1
    if form.opcode_class in ("long", "extralong", "xxlong") and source.positions == EA_HIGH_POSITIONS:
        return 1
    raise ValueError(
        f"unsupported EA candidate position in {form.key}/{operand.name}: "
        f"{source.positions}"
    )


def _ea_layout(form: decode_ir.FormIR) -> str:
    ea_operands = _ea_operands(form)
    slots = tuple(_ea_candidate_slot(form, operand) for operand in ea_operands)
    if not slots:
        return EA_LAYOUT_NONE
    if slots == (0,):
        return EA_LAYOUT_LOW
    if slots == (1,):
        return EA_LAYOUT_ALT
    if slots == (1, 0) and form.opcode_class in ("long", "extralong", "xxlong"):
        return EA_LAYOUT_ALT_THEN_LOW
    raise ValueError(f"unsupported EA candidate sequence in {form.key}: {slots}")


def _ea_candidate_widths(
    form: decode_ir.FormIR,
    names: Names,
) -> tuple[str, str]:
    widths = ["EA_WIDTH_INVALID", "EA_WIDTH_INVALID"]
    for operand in _ea_operands(form):
        widths[_ea_candidate_slot(form, operand)] = names.ea_width[operand.ea_width]
    return widths[0], widths[1]


def _ea_candidate_profiles(
    form: decode_ir.FormIR,
    names: Names,
) -> tuple[str, str]:
    profiles = ["EA_PROFILE_INVALID", "EA_PROFILE_INVALID"]
    for operand in _ea_operands(form):
        source = operand.source
        assert isinstance(source, decode_ir.EffectiveAddressSourceIR)
        profiles[_ea_candidate_slot(form, operand)] = names.ea_profile[source.profile]
    return profiles[0], profiles[1]


def _ea_static_payload_prefix_bytes(
    form: decode_ir.FormIR,
) -> tuple[int, int]:
    prefixes = [0, 0]
    appended_bytes = 0
    for operand in form.operands:
        source = operand.source
        if isinstance(source, decode_ir.AppendedPayloadSourceIR):
            appended_bytes += source.width // 8
        elif isinstance(source, decode_ir.EffectiveAddressSourceIR):
            prefixes[_ea_candidate_slot(form, operand)] = appended_bytes
    return prefixes[0], prefixes[1]


def _standalone_payload_cursor_expression(
    form: decode_ir.FormIR,
    target: decode_ir.ReadPayloadIR,
) -> str:
    terms = ["{2'b0, d0_i.base_cursor}"]
    for operand in _ea_operands(form):
        span = "low_span" if _ea_candidate_slot(form, operand) == 0 else "alt_span"
        terms.append(f"{{2'b0, {span}.descriptor_bytes}}")
    for layout in form.layout:
        if layout is target:
            break
        if isinstance(layout, decode_ir.ParseEaIR):
            operand = next(
                item for item in form.operands if item.name == layout.operand_name
            )
            span = "low_span" if _ea_candidate_slot(form, operand) == 0 else "alt_span"
            terms.append(f"{{2'b0, {span}.payload_bytes}}")
        else:
            terms.append(f"6'd{layout.width // 8}")
    return " + ".join(terms)


def _set_gather(payload: int, positions: tuple[int, ...], value: int) -> int:
    for value_bit, position in zip(range(len(positions) - 1, -1, -1), positions):
        if value & (1 << value_bit):
            payload |= 1 << position
        else:
            payload &= ~(1 << position)
    return payload


def representative_opcode(form: decode_ir.FormIR) -> int:
    """Return a live-form opcode satisfying the normalized D0 constraints."""
    opcode = form.opcode_value
    for constraint in form.constraints:
        selected = constraint.ranges[0].lower if constraint.ranges else 0x10
        opcode = _set_gather(opcode, constraint.positions, selected)
    return opcode


def _constraint_matches(constraint: decode_ir.ConstraintIR, opcode: int) -> bool:
    value = 0
    for position in constraint.positions:
        value = (value << 1) | ((opcode >> position) & 1)
    if constraint.kind == "allow_ranges":
        return any(item.lower <= value <= item.upper for item in constraint.ranges)
    if constraint.kind == "exclude_immediate":
        return not 0x5B <= value <= 0x5E
    raise ValueError(f"unknown constraint kind {constraint.kind}")


def _accepted_forms_overlap(
    left: decode_ir.FormIR, right: decode_ir.FormIR
) -> bool:
    """Return whether two same-class forms accept at least one common opcode."""
    if left.opcode_class != right.opcode_class:
        return False
    common_mask = left.opcode_mask & right.opcode_mask
    if (left.opcode_value ^ right.opcode_value) & common_mask:
        return False

    fixed_mask = left.opcode_mask | right.opcode_mask
    opcode = left.opcode_value | right.opcode_value
    variable_positions = sorted(
        {
            position
            for form in (left, right)
            for constraint in form.constraints
            for position in constraint.positions
            if not fixed_mask & (1 << position)
        }
    )
    if len(variable_positions) > 20:
        raise ValueError(
            "cannot prove D0 accepted-form exclusivity for "
            f"{left.key} and {right.key}: "
            f"{len(variable_positions)} variable constraint bits"
        )
    for assignment in range(1 << len(variable_positions)):
        candidate = opcode
        for index, position in enumerate(variable_positions):
            if assignment & (1 << index):
                candidate |= 1 << position
        if all(
            _constraint_matches(constraint, candidate)
            for form in (left, right)
            for constraint in form.constraints
        ):
            return True
    return False


def _validate_d0_accepted_exclusivity(ir: decode_ir.DecodeIR) -> None:
    """Fail closed unless every opcode class has at most one accepted form."""
    by_class: dict[str, list[decode_ir.FormIR]] = {}
    for form in ir.forms:
        by_class.setdefault(form.opcode_class, []).append(form)
    for opcode_class, forms in sorted(by_class.items()):
        for left_index, left in enumerate(forms):
            for right in forms[left_index + 1 :]:
                if _accepted_forms_overlap(left, right):
                    raise ValueError(
                        "D0 accepted forms overlap in opcode class "
                        f"{opcode_class}: {left.key} and {right.key}"
                    )


def reference_d0(
    ir: decode_ir.DecodeIR, valid: bool, opcode_class: str, opcode: int
) -> tuple[str, int | None]:
    """Reference the generated D0 priority and explicit result states."""
    if not valid:
        return "invalid_input", None
    raw = [
        form
        for form in ir.forms
        if form.opcode_class == opcode_class
        and opcode & form.opcode_mask == form.opcode_value
    ]
    accepted = [
        form for form in raw if all(_constraint_matches(item, opcode) for item in form.constraints)
    ]
    if accepted:
        return "success", accepted[0].index
    return ("constraint_rejected", None) if raw else ("unallocated_opcode", None)


def reference_ea(
    ir: decode_ir.DecodeIR,
    profile_name: str,
    compact_raw: int,
    record: bytes | tuple[int, ...] | list[int],
    byte_count: int,
    cursor: int,
) -> tuple[str, dict[str, object] | None, int]:
    """Reference one standalone EA parse using descriptor-then-payload order."""
    stage, decoded, payload_cursor = reference_ea_descriptor(
        ir, profile_name, compact_raw, record, byte_count, cursor
    )
    if stage != "success" or decoded is None:
        return stage, decoded, payload_cursor
    return reference_ea_payload(ir, decoded, record, byte_count, payload_cursor)


def reference_ea_descriptor(
    ir: decode_ir.DecodeIR,
    profile_name: str,
    compact_raw: int,
    record: bytes | tuple[int, ...] | list[int],
    byte_count: int,
    cursor: int,
) -> tuple[str, dict[str, object] | None, int]:
    """Decode one EA descriptor without consuming its trailing payload."""
    profile = next(
        item for item in ir.effective_addresses.profiles if item.name == profile_name
    )
    entry = profile.compact_entries[compact_raw]
    if not entry.valid:
        return "ea_descriptor", None, cursor
    compact = next(
        form
        for form in profile.compact_forms
        if form.name == entry.form_name
    )
    descriptor_form = None
    descriptor = 0
    next_cursor = cursor
    if compact.referenced_descriptor_family:
        family = next(
            item
            for item in ir.effective_addresses.descriptor_families
            if item.name == compact.referenced_descriptor_family
        )
        if (
            next_cursor + family.descriptor_bytes > byte_count
            or next_cursor + family.descriptor_bytes > ir.limits.max_record_bytes
        ):
            return "ea_descriptor", None, next_cursor + family.descriptor_bytes
        for byte in record[next_cursor : next_cursor + family.descriptor_bytes]:
            descriptor = (descriptor << 8) | byte
        descriptor_form = next(
            (form for form in family.forms if descriptor & form.mask == form.value),
            None,
        )
        if descriptor_form is None:
            return "ea_descriptor", None, cursor
        next_cursor += family.descriptor_bytes
    canonical_form = descriptor_form or compact
    canonical_fields = {
        "direct_register_valid": False,
        "direct_register": 0,
        "base_register_valid": False,
        "base_register": 0,
        "index_register_valid": False,
        "index_register": 0,
        "stride_register_valid": False,
        "stride_register": 0,
        "segment_register_valid": False,
        "segment_register": 0,
    }
    for form, raw in ((compact, compact_raw), (descriptor_form, descriptor)):
        if form is None:
            continue
        for field in form.fields:
            value = 0
            for position in field.positions:
                value = (value << 1) | ((raw >> position) & 1)
            target = {
                "value": "direct_register",
                "base": "base_register",
                "index": "index_register",
                "stride": "stride_register",
                "segment": "segment_register",
            }[field.role]
            canonical_fields[f"{target}_valid"] = True
            canonical_fields[target] = value
    return (
        "success",
        {
            "compact_form": compact.name,
            "descriptor_form": descriptor_form.name if descriptor_form else "",
            "descriptor": descriptor,
            "payload": 0,
            "payload_width": compact.payload_width,
            "payload_signed": compact.payload_signed,
            "kind": canonical_form.kind,
            "segment": canonical_form.segment,
            "base": canonical_form.base,
            "register_name": canonical_form.register_name,
            "update_target": canonical_form.update_target,
            "update_mode": canonical_form.update_mode,
            "update_difference": canonical_form.update_difference,
            **canonical_fields,
        },
        next_cursor,
    )


def reference_ea_payload(
    ir: decode_ir.DecodeIR,
    decoded: dict[str, object],
    record: bytes | tuple[int, ...] | list[int],
    byte_count: int,
    cursor: int,
) -> tuple[str, dict[str, object] | None, int]:
    """Consume one previously resolved EA's payload."""
    payload_bytes = int(decoded["payload_width"]) // 8
    next_cursor = cursor + payload_bytes
    if next_cursor > byte_count or next_cursor > ir.limits.max_record_bytes:
        return "ea_payload", None, next_cursor
    result = dict(decoded)
    result["payload"] = sum(
        record[cursor + offset] << (offset * 8) for offset in range(payload_bytes)
    )
    return "success", result, next_cursor


def reference_d1(
    ir: decode_ir.DecodeIR,
    form: decode_ir.FormIR,
    opcode: int,
    record: bytes | tuple[int, ...] | list[int],
    byte_count: int,
) -> tuple[str, dict[str, object]]:
    """Reference the generated form-indexed layout and static-legality chain."""
    fields: dict[str, int] = {}
    for field in form.fields:
        value = 0
        for position in field.positions:
            value = (value << 1) | ((opcode >> position) & 1)
        fields[field.symbol] = value
    values: dict[str, int] = {}
    eas: dict[str, dict[str, object]] = {}
    for operand in form.operands:
        source = operand.source
        if isinstance(source, (decode_ir.EncodedFieldSourceIR, decode_ir.EffectiveAddressSourceIR)):
            values[operand.name] = fields[source.field_symbol]
        elif isinstance(source, decode_ir.FixedSourceIR):
            values[operand.name] = source.value or 0
        else:
            values[operand.name] = 0
    descriptor_cursor = form.opcode_space_bytes
    for layout in form.layout:
        if not isinstance(layout, decode_ir.ParseEaIR):
            continue
        operand = next(
            item for item in form.operands if item.name == layout.operand_name
        )
        stage, decoded, next_cursor = reference_ea_descriptor(
            ir,
            layout.profile,
            values[operand.name] & 0x7F,
            record,
            byte_count,
            descriptor_cursor,
        )
        if stage != "success":
            return stage, {"required_bytes": next_cursor, "values": values, "eas": eas}
        eas[operand.name] = decoded or {}
        descriptor_cursor = next_cursor

    cursor = descriptor_cursor
    for layout in form.layout:
        operand = next(
            item for item in form.operands if item.name == layout.operand_name
        )
        if isinstance(layout, decode_ir.ParseEaIR):
            stage, decoded, next_cursor = reference_ea_payload(
                ir,
                eas[operand.name],
                record,
                byte_count,
                cursor,
            )
            if stage != "success":
                return stage, {"required_bytes": next_cursor, "values": values, "eas": eas}
            eas[operand.name] = decoded or {}
            cursor = next_cursor
        else:
            payload_bytes = layout.width // 8
            if cursor + payload_bytes > byte_count or cursor + payload_bytes > ir.limits.max_record_bytes:
                return "standalone_payload", {"required_bytes": cursor + payload_bytes, "values": values, "eas": eas}
            values[operand.name] = sum(
                record[cursor + offset] << (offset * 8)
                for offset in range(payload_bytes)
            )
            cursor += payload_bytes
    for operand in form.operands:
        if operand.legal_values and values[operand.name] not in operand.legal_values:
            return "static_legality", {"required_bytes": cursor, "values": values, "eas": eas}
    if cursor > byte_count or cursor > ir.limits.max_record_bytes:
        return "record_length", {"required_bytes": cursor, "values": values, "eas": eas}
    return "success", {"required_bytes": cursor, "values": values, "eas": eas}


@dataclass(frozen=True)
class Names:
    opcode_class: dict[str, str]
    form: dict[str, str]
    operation: dict[str, str]
    route: dict[str, str]
    instruction_set: dict[str, str]
    instruction_class: dict[str, str]
    privilege: dict[str, str]
    predicate: dict[str, str]
    operand_type: dict[str, str]
    access: dict[str, str]
    ea_width: dict[str, str]
    ea_profile: dict[str, str]
    overlap_rule: dict[str, str]
    observed_kind: dict[str, str]
    ea_kind: dict[str, str]
    ea_segment: dict[str, str]
    ea_base: dict[str, str]
    ea_register: dict[str, str]
    update_target: dict[str, str]
    update_mode: dict[str, str]
    update_difference: dict[str, str]
    ea_payload_width: dict[str, str]


@dataclass(frozen=True)
class PublicLayout:
    size_order: tuple[str, ...]
    cpuid_flag_order: tuple[str, ...]


def derive_public_layout(ir: decode_ir.DecodeIR) -> PublicLayout:
    """Derive mask orders from the current canonical decode model."""
    return PublicLayout(
        size_order=tuple(sorted({size for form in ir.forms for size in form.sizes})),
        cpuid_flag_order=tuple(
            item.id for item in sorted(ir.cpuid_flags, key=lambda item: item.index)
        ),
    )


def _mask_names(prefix: str, order: tuple[str, ...]) -> dict[str, str]:
    return {
        value: f"BEDROCK_{prefix}_MASK_{_identifier(value)}"
        for value in order
    }


def _render_mask_constants(
    dimension_name: str,
    prefix: str,
    order: tuple[str, ...],
) -> str:
    names = _mask_names(prefix, order)
    return "\n".join(
        f"  localparam logic [{dimension_name}-1:0] {names[value]} = "
        f"{_hex(len(order), 1 << index)}; // bit {index}: {value}"
        for index, value in enumerate(order)
    )


def _render_mask_assignment(
    target: str,
    values: Iterable[str],
    names: dict[str, str],
) -> list[str]:
    selected_values = set(values)
    selected = tuple(value for value in names if value in selected_values)
    if not selected:
        return [f"        {target} = '0;"]
    if len(selected) == 1:
        return [f"        {target} = {names[selected[0]]};"]
    return [
        f"        {target} =",
        *(
            f"          {names[value]}{' |' if index + 1 < len(selected) else ';'}"
            for index, value in enumerate(selected)
        ),
    ]


def _render_availability_assignment(
    form: decode_ir.FormIR,
    public_layout: PublicLayout,
) -> list[str]:
    names = _mask_names("CPUID_FLAG", public_layout.cpuid_flag_order)
    lines = ["        result_o.required_cpuid_flag_mask = '0;"]
    for index, rule in enumerate(form.availability_rules):
        conditions: list[list[str]] = []
        for selector in rule.selectors:
            gathered = _gather("d0_i.opcode", selector.positions)
            comparisons = [
                f"{gathered} == {len(selector.positions)}'d{value}"
                for value in selector.encoded_values
            ]
            conditions.append(
                [
                    f"({comparisons[0]}",
                    *[f" || {comparison}" for comparison in comparisons[1:]],
                    ")",
                ]
            )
        keyword = "if" if index == 0 else "else if"
        if not conditions:
            lines.append(f"        {keyword} (1'b1) begin")
        else:
            lines.append(f"        {keyword} (")
            for selector_index, selector_lines in enumerate(conditions):
                for line_index, condition_line in enumerate(selector_lines):
                    conjunction = (
                        " &&"
                        if selector_index + 1 < len(conditions)
                        and line_index + 1 == len(selector_lines)
                        else ""
                    )
                    lines.append(f"          {condition_line}{conjunction}")
            lines.append("        ) begin")
        assignment = _render_mask_assignment(
            "result_o.required_cpuid_flag_mask",
            rule.required_cpuid_flags,
            names,
        )
        lines.extend("  " + item for item in assignment)
        lines.append("        end")
    return lines


def _all_ea_forms(ir: decode_ir.DecodeIR) -> tuple[decode_ir.EaFormIR, ...]:
    return tuple(
        form
        for profile in ir.effective_addresses.profiles
        for form in profile.compact_forms
    ) + tuple(
        form
        for family in ir.effective_addresses.descriptor_families
        for form in family.forms
    )


def _render_package(ir: decode_ir.DecodeIR) -> tuple[str, Names]:
    forms = ir.forms
    ea_forms = _all_ea_forms(ir)
    public_layout = derive_public_layout(ir)
    enums: list[str] = []

    def add(type_name: str, prefix: str, values: Iterable[str]):
        text, mapping = _enum(type_name, prefix, tuple(values))
        enums.append(text)
        return mapping

    opcode_classes = tuple(item.name for item in ENCODING_CLASSES)
    opcode_class = add("opcode_class_e", "OPCODE_CLASS", opcode_classes)
    operator_spaces = tuple(dict.fromkeys(space.name for space in OPERATOR_SPACES))
    operator_space_text, _ = _enum(
        "operator_space_e",
        "OPERATOR_SPACE",
        operator_spaces,
        invalid_name="NONE",
    )
    enums.append(operator_space_text)
    form = add("form_id_e", "FORM", (item.key for item in forms))
    operation = add("operation_e", "OP", ir.mnemonics)
    route = add("route_e", "ROUTE", _ordered(item.control.route for item in forms))
    instruction_set = add(
        "instruction_set_e", "INSTRUCTION_SET", _ordered(item.control.instruction_set for item in forms)
    )
    instruction_class = add(
        "instruction_class_e", "INSTRUCTION_CLASS", _ordered(item.control.instruction_class for item in forms)
    )
    privilege = add("privilege_e", "PRIVILEGE", _ordered(item.control.privilege for item in forms))
    predicate = add("predicate_mode_e", "PREDICATE", _ordered(item.control.predicate_mode for item in forms))
    operand_type = add("operand_type_e", "OPERAND_TYPE", _ordered(x.type_name for f in forms for x in f.operands))
    access = add("operand_access_e", "ACCESS", _ordered(x.access for f in forms for x in f.operands))
    ea_width = add("operand_ea_width_e", "EA_WIDTH", _ordered(x.ea_width for f in forms for x in f.operands))
    ea_profile = add(
        "ea_profile_e",
        "EA_PROFILE",
        (profile.name for profile in ir.effective_addresses.profiles),
    )
    overlap_rule = add("overlap_rule_e", "OVERLAP", _ordered(x.rule for f in forms for x in f.overlaps))
    observed_kind = add("repeat_observed_e", "REPEAT_OBSERVED", _ordered(f.control.repeat.observed_kind for f in forms))
    ea_kind = add("ea_kind_e", "EA_KIND", _ordered(x.kind for x in ea_forms))
    ea_segment = add("ea_segment_e", "EA_SEGMENT", _ordered(x.segment for x in ea_forms))
    ea_base = add("ea_base_e", "EA_BASE", _ordered(x.base for x in ea_forms))
    ea_register = add("ea_register_e", "EA_REGISTER", _ordered(x.register_name for x in ea_forms))
    update_target = add("ea_update_target_e", "EA_UPDATE_TARGET", _ordered(x.update_target for x in ea_forms))
    update_mode = add("ea_update_mode_e", "EA_UPDATE_MODE", _ordered(x.update_mode for x in ea_forms))
    update_difference = add(
        "ea_update_difference_e",
        "EA_UPDATE_DIFFERENCE",
        _ordered(x.update_difference for x in ea_forms),
    )
    ea_payload_width = add(
        "ea_payload_width_e",
        "EA_PAYLOAD_WIDTH",
        tuple(
            str(width)
            for width in sorted(
                {
                    item.payload_width
                    for profile in ir.effective_addresses.profiles
                    for item in profile.compact_forms
                }
            )
        ),
    )
    names = Names(
        opcode_class, form, operation, route, instruction_set, instruction_class,
        privilege, predicate, operand_type, access, ea_width, ea_profile, overlap_rule,
        observed_kind, ea_kind, ea_segment, ea_base, ea_register, update_target,
        update_mode, update_difference, ea_payload_width,
    )
    enums.insert(
        0,
        """typedef enum logic [1:0] {
    D0_INVALID_INPUT = 2'd0,
    D0_UNALLOCATED_OPCODE = 2'd1,
    D0_CONSTRAINT_REJECTED = 2'd2,
    D0_SUCCESS = 2'd3
  } d0_status_e;

  typedef enum logic [3:0] {
    D1_STAGE_D0_REJECTED = 4'd0,
    D1_STAGE_RECORD_BOUNDS = 4'd1,
    D1_STAGE_EA_DESCRIPTOR = 4'd2,
    D1_STAGE_EA_PAYLOAD = 4'd3,
    D1_STAGE_STANDALONE_PAYLOAD = 4'd4,
    D1_STAGE_STATIC_LEGALITY = 4'd5,
    D1_STAGE_RECORD_LENGTH = 4'd6,
    D1_STAGE_SUCCESS = 4'd7
  } decode_stage_e;

  typedef enum logic [1:0] {
    EA_LAYOUT_NONE = 2'd0,
    EA_LAYOUT_LOW = 2'd1,
    EA_LAYOUT_ALT = 2'd2,
    EA_LAYOUT_ALT_THEN_LOW = 2'd3
  } ea_layout_e;

""",
    )
    enum_text = "\n\n  ".join(enums)
    mask_constants = "\n".join(
        (
            _render_mask_constants(
                "BEDROCK_SIZE_MASK_BITS", "SIZE", public_layout.size_order
            ),
            _render_mask_constants(
                "BEDROCK_CPUID_FLAG_MASK_BITS",
                "CPUID_FLAG",
                public_layout.cpuid_flag_order,
            ),
        )
    )
    declarations = f"""  localparam logic [9:0] BEDROCK_OPCODE_BITS = 10'd{ir.limits.max_opcode_width};
  localparam logic [9:0] BEDROCK_RECORD_BYTES = 10'd{ir.limits.max_record_bytes};
  localparam logic [9:0] BEDROCK_FORM_COUNT = 10'd{ir.limits.form_count};
  localparam logic [9:0] BEDROCK_OPERAND_SLOTS = 10'd{ir.limits.max_operands};
  localparam logic [9:0] BEDROCK_EA_SLOTS = 10'd{ir.limits.max_ea_operands};
  localparam logic [9:0] BEDROCK_OVERLAP_SLOTS = 10'd{ir.limits.max_overlaps};
  localparam logic [9:0] BEDROCK_SIZE_MASK_BITS = 10'd{len(public_layout.size_order)};
  localparam logic [9:0] BEDROCK_CPUID_FLAG_MASK_BITS = 10'd{len(public_layout.cpuid_flag_order)};
  localparam logic [0:0] BEDROCK_EA_LOW_SLOT = 1'd0;
  localparam logic [0:0] BEDROCK_EA_ALT_SLOT = 1'd1;

{mask_constants}

  {enum_text}

  typedef struct packed {{
    d0_status_e status;
    opcode_class_e opcode_class;
    operator_space_e operator_space;
    form_id_e form;
    logic [31:0] form_high_decode;
    logic [31:0] form_low_decode;
    logic [BEDROCK_OPCODE_BITS-1:0] opcode;
    logic [6:0] alt_raw;
    logic [3:0] base_cursor;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
    ea_profile_e [BEDROCK_EA_SLOTS-1:0] ea_profiles;
  }} d0_result_t;

  typedef struct packed {{
    d0_status_e status;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
    ea_profile_e [BEDROCK_EA_SLOTS-1:0] ea_profiles;
    logic [6:0] low_raw;
    logic [6:0] alt_raw;
    logic [3:0] base_cursor;
    logic [3:0] post_alt_cursor;
    logic [BEDROCK_EA_SLOTS-1:0][4:0] ea_static_payload_prefix_bytes;
  }} d0_ea_result_t;

  typedef struct packed {{
    logic valid;
    operand_type_e type_name;
    operand_access_e access;
    operand_ea_width_e ea_width;
    logic [63:0] value;
    logic payload_signed;
    logic ea_valid;
    logic [0:0] ea_slot;
  }} decoded_operand_t;

  typedef struct packed {{
    logic valid;
    ea_profile_e profile;
    ea_kind_e kind;
    ea_segment_e segment;
    ea_base_e base;
    ea_register_e register_name;
    operand_ea_width_e operand_width;
    ea_update_target_e update_target;
    ea_update_mode_e update_mode;
    ea_update_difference_e update_difference;
    ea_payload_width_e payload_width;
    logic payload_signed;
    logic direct_register_valid;
    logic [3:0] direct_register;
    logic base_register_valid;
    logic [3:0] base_register;
    logic index_register_valid;
    logic [3:0] index_register;
    logic stride_register_valid;
    logic [3:0] stride_register;
    logic segment_register_valid;
    logic [3:0] segment_register;
    logic [63:0] payload;
  }} decoded_ea_t;

  typedef struct packed {{
    logic valid;
    overlap_rule_e rule;
    logic [1:0] left_operand;
    logic [1:0] right_operand;
  }} overlap_descriptor_t;

  typedef struct packed {{
    route_e route;
    instruction_set_e instruction_set;
    instruction_class_e instruction_class;
    privilege_e privilege;
    predicate_mode_e predicate_mode;
    repeat_observed_e repeat_observed;
    logic repeat_rep;
    logic repeat_repcc;
    logic [1:0] repeat_observed_operand;
    logic has_ea_operand;
  }} control_metadata_t;

  typedef struct packed {{
    logic valid;
    logic [3:0] encoded_bytes;
    logic [3:0] descriptor_bytes;
    logic [3:0] payload_bytes;
  }} ea_span_result_t;

  typedef struct packed {{
    logic valid;
    decode_stage_e stage;
    form_id_e form;
    operation_e operation;
    control_metadata_t control;
    logic [BEDROCK_SIZE_MASK_BITS-1:0] size_mask;
    logic [BEDROCK_CPUID_FLAG_MASK_BITS-1:0] required_cpuid_flag_mask;
    logic [2:0] operand_count;
    decoded_operand_t [BEDROCK_OPERAND_SLOTS-1:0] operands;
    logic [1:0] overlap_count;
    overlap_descriptor_t [BEDROCK_OVERLAP_SLOTS-1:0] overlaps;
    logic [5:0] required_bytes;
    logic [4:0] encoded_bytes;
  }} d1_opcode_result_t;

  typedef struct packed {{
    logic valid;
    decode_stage_e stage;
    logic [1:0] ea_count;
    decoded_ea_t [BEDROCK_EA_SLOTS-1:0] eas;
    logic [5:0] required_bytes;
  }} ea_decode_result_t;

  typedef struct packed {{
    logic ok;
    decode_stage_e stage;
    logic [5:0] next_cursor;
    decoded_ea_t ea;
  }} ea_parse_result_t;
"""
    return package_emitter.render(declarations=declarations), names


def _constraint_sv(constraint: decode_ir.ConstraintIR, gathered: str) -> str:
    width = len(constraint.positions)
    if constraint.kind == "allow_ranges":
        parts = []
        for item in constraint.ranges:
            if item.lower == item.upper:
                parts.append(f"({gathered} == {_hex(width, item.lower)})")
            else:
                parts.append(
                    f"(({gathered} >= {_hex(width, item.lower)}) && "
                    f"({gathered} <= {_hex(width, item.upper)}))"
                )
        if len(parts) == 1:
            return "(" + parts[0] + ")"
        return "(\n      " + " ||\n      ".join(parts) + "\n    )"
    if constraint.kind == "exclude_immediate":
        return f"!(({gathered} >= {_hex(width, 0x5B)}) && ({gathered} <= {_hex(width, 0x5E)}))"
    raise ValueError(f"unknown constraint kind {constraint.kind}")


def _constraint_signal(form_index: int, constraint_index: int) -> str:
    return f"form_{form_index:03d}_constraint_{constraint_index}_value"


def _balanced_tree(
    leaves: list[str],
    *,
    prefix: str,
    type_name: str,
    expression: str,
) -> tuple[list[str], list[str], str, int]:
    """Render a balanced binary tree and return declarations, assignments, root, depth."""
    if not leaves:
        raise ValueError(f"empty balanced tree {prefix}")
    declarations: list[str] = []
    assignments: list[str] = []
    node_index = 0

    def build(items: list[str]) -> tuple[str, int]:
        nonlocal node_index
        if len(items) == 1:
            return items[0], 0
        midpoint = len(items) // 2
        left, left_depth = build(items[:midpoint])
        right, right_depth = build(items[midpoint:])
        node = f"{prefix}_node_{node_index:03d}"
        node_index += 1
        declarations.append(f"  {type_name} {node};")
        assignments.append(
            f"  assign {node} = "
            + expression.format(left=left, right=right)
            + ";"
        )
        return node, max(left_depth, right_depth) + 1

    root, depth = build(leaves)
    return declarations, assignments, root, depth


def _render_opcode_class_bytes_function(ir: decode_ir.DecodeIR) -> str:
    class_bytes = {item.name: item.opcode_space_bytes for item in ENCODING_CLASSES}
    byte_cases = "\n".join(
        f"        OPCODE_CLASS_{_identifier(opcode_class)}: "
        f"opcode_class_bytes = 6'd{class_bytes[opcode_class]};"
        for opcode_class in sorted(class_bytes)
    )
    return f"""  function automatic logic [5:0] opcode_class_bytes(
    input opcode_class_e opcode_class
  );
    begin
      opcode_class_bytes = '0;
      unique case (opcode_class)
{byte_cases}
        default: begin end
      endcase
    end
  endfunction"""


def _render_operator_space_function(names: Names) -> str:
    cases: list[str] = []
    allocations_by_class: dict[str, list[OperatorSpace]] = {}
    for allocation in OPERATOR_SPACES:
        allocations_by_class.setdefault(allocation.encoding_class, []).append(
            allocation
        )
    for encoding_class, allocations in sorted(allocations_by_class.items()):
        allocation_bits = ENCODING_CLASSES_BY_NAME[encoding_class].allocation_bits
        prefix_high = allocation_bits - 1
        rows = "\n".join(
            f"            {OPERATOR_SPACE_PREFIX_BITS}'b{allocation.prefix}: "
            f"operator_space_from_opcode = "
            f"OPERATOR_SPACE_{_identifier(allocation.name)};"
            for allocation in allocations
        )
        cases.append(
            "\n".join(
                [
                    f"        {names.opcode_class[encoding_class]}: begin",
                    f"          unique casez (opcode[{prefix_high} -: "
                    f"{OPERATOR_SPACE_PREFIX_BITS}])",
                    rows,
                    "            default: begin end",
                    "          endcase",
                    "        end",
                ]
            )
        )
    return f"""  function automatic operator_space_e operator_space_from_opcode(
    input opcode_class_e opcode_class,
    input logic [BEDROCK_OPCODE_BITS-1:0] opcode
  );
    begin
      operator_space_from_opcode = OPERATOR_SPACE_NONE;
      unique case (opcode_class)
{chr(10).join(cases)}
        default: begin end
      endcase
    end
  endfunction"""


def _render_d0(ir: decode_ir.DecodeIR, names: Names) -> str:
    _validate_d0_accepted_exclusivity(ir)
    form_bits_type = f"logic [{_width(len(ir.forms) + 1) - 1}:0]"
    by_class: dict[str, list[decode_ir.FormIR]] = {}
    for form in ir.forms:
        by_class.setdefault(form.opcode_class, []).append(form)
    constraint_declarations: list[str] = []
    constraint_assignments: list[str] = []
    form_declarations: list[str] = []
    form_assignments: list[str] = []
    tree_declarations: list[str] = []
    tree_assignments: list[str] = []
    class_cases: list[str] = []
    for form in ir.forms:
        for constraint_index, constraint in enumerate(form.constraints):
            signal = _constraint_signal(form.index, constraint_index)
            constraint_declarations.append(
                f"  logic [{len(constraint.positions) - 1}:0] {signal};"
            )
            constraint_assignments.extend(
                [
                    f"  assign {signal} = {{",
                    *(f"    opcode_i[{position}]," for position in constraint.positions[:-1]),
                    f"    opcode_i[{constraint.positions[-1]}]",
                    "  };",
                ]
            )
    for opcode_class in sorted(by_class):
        class_forms = by_class[opcode_class]
        class_name = _identifier(opcode_class).lower()
        raw_leaves: list[str] = []
        form_leaves: list[str] = []
        selection_leaves: list[str] = []
        for form in class_forms:
            raw_signal = f"form_{form.index:03d}_raw_match"
            accepted_signal = f"form_{form.index:03d}_accepted_match"
            form_signal = f"form_{form.index:03d}_onehot_form"
            selection_signal = f"form_{form.index:03d}_selection"
            raw_leaves.append(raw_signal)
            form_leaves.append(form_signal)
            selection_leaves.append(selection_signal)
            raw = (
                f"((opcode_i & {_hex(ir.limits.max_opcode_width, form.opcode_mask)}) == "
                f"{_hex(ir.limits.max_opcode_width, form.opcode_value)})"
            )
            low_width, alt_width = _ea_candidate_widths(form, names)
            low_profile, alt_profile = _ea_candidate_profiles(form, names)
            low_static_prefix, alt_static_prefix = _ea_static_payload_prefix_bytes(form)
            predicates = [
                _constraint_sv(
                    constraint,
                    _constraint_signal(form.index, constraint_index),
                )
                for constraint_index, constraint in enumerate(form.constraints)
            ]
            form_declarations.extend(
                [
                    f"  // form {form.index}: {form.key}",
                    f"  logic {raw_signal};",
                    f"  logic {accepted_signal};",
                    f"  d0_selection_t {selection_signal};",
                    f"  {form_bits_type} {form_signal};",
                ]
            )
            form_assignments.append(f"  assign {raw_signal} = {raw};")
            if predicates:
                form_assignments.append(
                    f"  assign {accepted_signal} = {raw_signal} &&"
                )
                for predicate_index, predicate in enumerate(predicates):
                    suffix = " &&" if predicate_index + 1 < len(predicates) else ""
                    form_assignments.append(f"    {predicate}{suffix}")
                form_assignments[-1] += ";"
            else:
                form_assignments.append(
                    f"  assign {accepted_signal} = {raw_signal};"
                )
            form_assignments.extend(
                [
                    f"  assign {selection_signal}.valid = {accepted_signal};",
                    f"  assign {selection_signal}.form = FORM_INVALID;",
                    f"  assign {form_signal} = {accepted_signal} ? "
                    f"{names.form[form.key]} : FORM_INVALID;",
                    f"  assign {selection_signal}.ea_layout = {_ea_layout(form)};",
                    f"  assign {selection_signal}.ea_widths[BEDROCK_EA_LOW_SLOT] = {low_width};",
                    f"  assign {selection_signal}.ea_widths[BEDROCK_EA_ALT_SLOT] = {alt_width};",
                    f"  assign {selection_signal}.ea_profiles[BEDROCK_EA_LOW_SLOT] = {low_profile};",
                    f"  assign {selection_signal}.ea_profiles[BEDROCK_EA_ALT_SLOT] = {alt_profile};",
                    f"  assign {selection_signal}.ea_static_payload_prefix_bytes[BEDROCK_EA_LOW_SLOT] = 5'd{low_static_prefix};",
                    f"  assign {selection_signal}.ea_static_payload_prefix_bytes[BEDROCK_EA_ALT_SLOT] = 5'd{alt_static_prefix};",
                ]
            )
        raw_declarations, raw_assignments, raw_root, raw_depth = _balanced_tree(
            raw_leaves,
            prefix=f"{class_name}_raw",
            type_name="logic",
            expression="({left} | {right})",
        )
        form_tree_declarations, form_tree_assignments, form_root, form_depth = (
            _balanced_tree(
                form_leaves,
                prefix=f"{class_name}_form",
                type_name=form_bits_type,
                expression="({left} | {right})",
            )
        )
        (
            selection_declarations,
            selection_assignments,
            selection_root,
            selection_depth,
        ) = _balanced_tree(
            selection_leaves,
            prefix=f"{class_name}_selection",
            type_name="d0_selection_t",
            expression="{left}.valid ? {left} : {right}",
        )
        if len(selection_declarations) != len(form_tree_declarations):
            raise ValueError(f"mismatched D0 tree nodes for {opcode_class}")
        # Keep corresponding tree lanes adjacent through elaboration. The
        # target Yosys/ABC flow maps this ordering materially better.
        selection_form_declarations = [
            declaration
            for pair in zip(selection_declarations, form_tree_declarations)
            for declaration in pair
        ]
        selection_form_assignments = [
            assignment
            for pair in zip(selection_assignments, form_tree_assignments)
            for assignment in pair
        ]
        tree_declarations.extend(
            [
                f"  // {opcode_class}: {len(class_forms)} parallel form leaves, "
                f"{selection_depth} balanced form-OR/EA-priority levels",
                *raw_declarations,
                *selection_form_declarations,
            ]
        )
        tree_assignments.extend([*raw_assignments, *selection_form_assignments])
        if raw_depth != form_depth or form_depth != selection_depth:
            raise ValueError(f"mismatched D0 tree depths for {opcode_class}")
        class_cases.append(
            "\n".join(
                [
                    f"      {names.opcode_class[opcode_class]}: begin",
                    f"        class_raw_match = {raw_root};",
                    f"        class_selection = {selection_root};",
                    f"        class_form = {form_root};",
                    "      end",
                ]
            )
        )
    return d0_emitter.render(
        {
            "FORM_BITS_TYPE": form_bits_type,
            "CONSTRAINT_DECLARATIONS": "\n".join(constraint_declarations),
            "FORM_DECLARATIONS": "\n".join(form_declarations),
            "TREE_DECLARATIONS": "\n".join(tree_declarations),
            "EA_SPAN_FUNCTION": _render_ea_span_function(ir, names),
            "OPCODE_CLASS_BYTES_FUNCTION": _render_opcode_class_bytes_function(ir),
            "OPERATOR_SPACE_FUNCTION": _render_operator_space_function(names),
            "CONSTRAINT_ASSIGNMENTS": "\n".join(constraint_assignments),
            "FORM_ASSIGNMENTS": "\n".join(form_assignments),
            "TREE_ASSIGNMENTS": "\n".join(tree_assignments),
            "CLASS_CASES": "\n".join(class_cases),
        }
    )


def _ea_static_assignments(
    target: str,
    form: decode_ir.EaFormIR,
    names: Names,
    *,
    raw_signal: str,
) -> list[str]:
    lines = [
        f"{target}.kind = {names.ea_kind[form.kind]};",
        f"{target}.segment = {names.ea_segment[form.segment]};",
        f"{target}.base = {names.ea_base[form.base]};",
        f"{target}.register_name = {names.ea_register[form.register_name]};",
        f"{target}.update_target = {names.update_target[form.update_target]};",
        f"{target}.update_mode = {names.update_mode[form.update_mode]};",
        f"{target}.update_difference = {names.update_difference[form.update_difference]};",
    ]
    for field in form.fields:
        value = _gather(raw_signal, field.positions)
        if field.role == "value":
            lines.extend(
                [
                    f"{target}.direct_register_valid = 1'b1;",
                    f"{target}.direct_register = 4'({value});",
                ]
            )
        elif field.role == "base":
            lines.extend(
                [
                    f"{target}.base_register_valid = 1'b1;",
                    f"{target}.base_register = 4'({value});",
                ]
            )
        elif field.role == "index":
            lines.extend(
                [
                    f"{target}.index_register_valid = 1'b1;",
                    f"{target}.index_register = 4'({value});",
                ]
            )
        elif field.role == "stride":
            lines.extend(
                [
                    f"{target}.stride_register_valid = 1'b1;",
                    f"{target}.stride_register = 4'({value});",
                ]
            )
        elif field.role == "segment":
            lines.extend(
                [
                    f"{target}.segment_register_valid = 1'b1;",
                    f"{target}.segment_register = 4'({value});",
                ]
            )
    return lines


def _indent(lines: Iterable[str], spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line for line in lines)


def _minimized_bit_patterns(values: set[int], width: int) -> tuple[str, ...]:
    if not values:
        return ()
    full_mask = (1 << width) - 1
    cubes = {(value, full_mask) for value in values}
    primes: set[tuple[int, int]] = set()
    while cubes:
        combined: set[tuple[int, int]] = set()
        used: set[tuple[int, int]] = set()
        by_mask: dict[int, list[tuple[int, int]]] = {}
        for cube in cubes:
            by_mask.setdefault(cube[1], []).append(cube)
        for mask, masked_cubes in by_mask.items():
            for left_index, left in enumerate(masked_cubes):
                for right in masked_cubes[left_index + 1 :]:
                    difference = (left[0] ^ right[0]) & mask
                    if difference.bit_count() == 1:
                        used.add(left)
                        used.add(right)
                        new_mask = mask & ~difference
                        combined.add((left[0] & new_mask, new_mask))
        primes.update(cube for cube in cubes if cube not in used)
        cubes = combined

    uncovered = set(values)
    selected: list[tuple[int, int]] = []
    while uncovered:
        cube = max(
            primes,
            key=lambda item: (
                sum(
                    (value & item[1]) == item[0]
                    for value in uncovered
                ),
                width - item[1].bit_count(),
                -item[0],
            ),
        )
        selected.append(cube)
        uncovered = {
            value for value in uncovered if (value & cube[1]) != cube[0]
        }
        primes.remove(cube)

    def render(cube: tuple[int, int]) -> str:
        value, mask = cube
        bits = "".join(
            str((value >> bit) & 1) if mask & (1 << bit) else "?"
            for bit in range(width - 1, -1, -1)
        )
        return f"{width}'b{bits}"

    return tuple(render(cube) for cube in selected)


def _render_ea_span_function(ir: decode_ir.DecodeIR, names: Names) -> str:
    profile_cases: list[str] = []
    for profile in ir.effective_addresses.profiles:
        compact_by_name = {item.name: item for item in profile.compact_forms}
        raw_cases = []
        for entry in profile.compact_entries:
            lines = [
                f"          7'h{entry.raw:02x}: begin // "
                f"{entry.form_name or entry.invalid_reason}"
            ]
            if entry.valid:
                compact = compact_by_name[entry.form_name]
                encoded_bytes = compact.descriptor_bytes + compact.payload_width // 8
                lines.extend(
                    [
                        "            encoded_ea_span.valid = 1'b1;",
                        f"            encoded_ea_span.encoded_bytes = 4'd{encoded_bytes};",
                        f"            encoded_ea_span.descriptor_bytes = 4'd{compact.descriptor_bytes};",
                        f"            encoded_ea_span.payload_bytes = 4'd{compact.payload_width // 8};",
                    ]
                )
            lines.append("          end")
            raw_cases.append("\n".join(lines))
        profile_cases.append(
            f"      {names.ea_profile[profile.name]}: begin\n"
            "        unique case (compact_raw)\n"
            + "\n".join(raw_cases)
            + "\n          default: begin end\n"
            "        endcase\n"
            "      end"
        )
    return f"""  function automatic ea_span_result_t encoded_ea_span(
    input ea_profile_e profile,
    input logic [6:0] compact_raw
  );
    begin
      encoded_ea_span = '0;
      unique case (profile)
{chr(10).join(profile_cases)}
        default: begin end
      endcase
    end
  endfunction"""


def _render_compact_ea_span_function(ir: decode_ir.DecodeIR, names: Names) -> str:
    universal: dict[int, tuple[int, int]] = {}
    for profile in ir.effective_addresses.profiles:
        compact_by_name = {item.name: item for item in profile.compact_forms}
        for entry in profile.compact_entries:
            if entry.valid:
                compact = compact_by_name[entry.form_name]
                spans = (compact.descriptor_bytes, compact.payload_width // 8)
                previous = universal.setdefault(entry.raw, spans)
                if previous != spans:
                    raise ValueError(
                        f"EA raw {entry.raw} has profile-dependent encoded span"
                    )

    by_span: dict[tuple[int, int], set[int]] = {}
    for raw, spans in universal.items():
        by_span.setdefault(spans, set()).add(raw)
    raw_cases = []
    for (descriptor_bytes, payload_bytes), raw_values in sorted(by_span.items()):
        for pattern in _minimized_bit_patterns(raw_values, 7):
            raw_cases.append(
                f"        {pattern}: begin\n"
                "          encoded_ea_span.valid = 1'b1;\n"
                f"          encoded_ea_span.encoded_bytes = 4'd{descriptor_bytes + payload_bytes};\n"
                f"          encoded_ea_span.descriptor_bytes = 4'd{descriptor_bytes};\n"
                f"          encoded_ea_span.payload_bytes = 4'd{payload_bytes};\n"
                "        end"
            )

    profile_cases: list[str] = []
    for profile in ir.effective_addresses.profiles:
        unavailable = {
            raw for raw in universal if not profile.compact_entries[raw].valid
        }
        patterns = _minimized_bit_patterns(unavailable, 7)
        if patterns:
            invalid_cases = "\n".join(
                f"          {pattern}: encoded_ea_span = '0;"
                for pattern in patterns
            )
            body = (
                "        casez (compact_raw)\n"
                f"{invalid_cases}\n"
                "          default: begin end\n"
                "        endcase"
            )
        else:
            body = "        begin end"
        profile_cases.append(
            f"      {names.ea_profile[profile.name]}: begin\n"
            f"{body}\n"
            "      end"
        )
    return f"""  function automatic ea_span_result_t encoded_ea_span(
    input ea_profile_e profile,
    input logic [6:0] compact_raw
  );
    begin
      encoded_ea_span = '0;
      casez (compact_raw)
{chr(10).join(raw_cases)}
        default: begin end
      endcase
      unique case (profile)
{chr(10).join(profile_cases)}
        default: encoded_ea_span = '0;
      endcase
    end
  endfunction"""


def _render_ea_function(ir: decode_ir.DecodeIR, names: Names) -> str:
    families = ir.effective_addresses.descriptor_families
    family_names = {
        family.name: f"EA_DESCRIPTOR_FAMILY_{_identifier(family.name)}"
        for family in families
    }
    family_width = _width(len(families) + 1)
    family_enum = [
        f"    EA_DESCRIPTOR_FAMILY_NONE = {family_width}'d0",
        *(
            f"    {family_names[family.name]} = {family_width}'d{index}"
            for index, family in enumerate(families, 1)
        ),
    ]

    def compact_assignments(compact: decode_ir.EaFormIR) -> tuple[str, ...]:
        descriptor_family = (
            family_names[compact.referenced_descriptor_family]
            if compact.referenced_descriptor_family
            else "EA_DESCRIPTOR_FAMILY_NONE"
        )
        return (
            "decode_compact_ea.valid = 1'b1;",
            f"decode_compact_ea.descriptor_family = {descriptor_family};",
            "decode_compact_ea.ea.valid = 1'b1;",
            f"decode_compact_ea.ea.payload_width = {names.ea_payload_width[str(compact.payload_width)]};",
            f"decode_compact_ea.ea.payload_signed = 1'b{int(compact.payload_signed)};",
            *_ea_static_assignments(
                "decode_compact_ea.ea",
                compact,
                names,
                raw_signal="compact_raw",
            ),
        )

    def compact_case(
        label: str, compact: decode_ir.EaFormIR, comment: str, *, indent: int
    ) -> str:
        prefix = " " * indent
        lines = [f"{prefix}{label}: begin // {comment}"]
        lines.extend(
            f"{prefix}  {assignment}" for assignment in compact_assignments(compact)
        )
        lines.append(f"{prefix}end")
        return "\n".join(lines)

    profile_forms: dict[str, dict[int, decode_ir.EaFormIR]] = {}
    for profile in ir.effective_addresses.profiles:
        compact_by_name = {item.name: item for item in profile.compact_forms}
        profile_forms[profile.name] = {
            entry.raw: compact_by_name[entry.form_name]
            for entry in profile.compact_entries
            if entry.valid
        }

    profiles = ir.effective_addresses.profiles
    common_raws = {
        raw
        for raw in range(1 << ir.effective_addresses.compact_width)
        if all(raw in profile_forms[profile.name] for profile in profiles)
        and len(
            {
                compact_assignments(profile_forms[profile.name][raw])
                for profile in profiles
            }
        )
        == 1
    }
    common_cases: list[str] = []
    covered_common_raws: set[int] = set()
    for raw in sorted(common_raws):
        if raw in covered_common_raws:
            continue
        compact = profile_forms[profiles[0].name][raw]
        pattern_raws = {
            candidate
            for candidate in range(1 << ir.effective_addresses.compact_width)
            if (candidate & compact.mask) == compact.value
        }
        signature = compact_assignments(compact)
        if not pattern_raws.issubset(common_raws) or any(
            compact_assignments(profile_forms[profiles[0].name][candidate])
            != signature
            for candidate in pattern_raws
        ):
            pattern_raws = {raw}
            label = _hex(ir.effective_addresses.compact_width, raw)
        else:
            label = _casez(
                ir.effective_addresses.compact_width,
                compact.value,
                compact.mask,
            )
        covered_common_raws.update(pattern_raws)
        common_cases.append(
            compact_case(label, compact, compact.name, indent=6)
        )

    profile_specific_cases: list[str] = []
    for profile in profiles:
        cases = [
            compact_case(
                _hex(ir.effective_addresses.compact_width, raw),
                compact,
                compact.name,
                indent=10,
            )
            for raw, compact in sorted(profile_forms[profile.name].items())
            if raw not in common_raws
        ]
        if not cases:
            continue
        profile_specific_cases.append(
            f"        {names.ea_profile[profile.name]}: begin\n"
            "          unique case (compact_raw)\n"
            + "\n".join(cases)
            + "\n            default: begin end\n"
            "          endcase\n"
            "        end"
        )
    valid_profiles = ", ".join(names.ea_profile[profile.name] for profile in profiles)

    descriptor_functions: list[str] = []
    for family in families:
        descriptor_width = family.descriptor_bytes * 8
        function_name = f"decode_{_identifier(family.name).lower()}_descriptor"
        lines = [
            f"  function automatic descriptor_decode_t {function_name}(",
            f"    input logic [{descriptor_width - 1}:0] descriptor",
            "  );",
            "    begin",
            f"      {function_name} = '0;",
            "      unique casez (descriptor)",
        ]
        for descriptor_form in family.forms:
            lines.extend(
                [
                    f"      {_casez(descriptor_width, descriptor_form.value, descriptor_form.mask)}: begin // {descriptor_form.name}",
                    f"        {function_name}.valid = 1'b1;",
                ]
            )
            lines.extend(
                "        " + assignment
                for assignment in _ea_static_assignments(
                    f"{function_name}.ea",
                    descriptor_form,
                    names,
                    raw_signal="descriptor",
                )
            )
            lines.append("      end")
        lines.extend(
            [
                "        default: begin end",
                "      endcase",
                "    end",
                "  endfunction",
            ]
        )
        descriptor_functions.append("\n".join(lines))

    payload_cases: list[str] = []
    payload_widths = sorted(
        {
            form.payload_width
            for profile in ir.effective_addresses.profiles
            for form in profile.compact_forms
        }
    )
    for payload_width in payload_widths:
        payload_bytes = payload_width // 8
        lines = [
            f"      {names.ea_payload_width[str(payload_width)]}: begin",
        ]
        if payload_bytes == 0:
            lines.extend(
                [
                    "        parse_ea_payload.ok = 1'b1;",
                    "        parse_ea_payload.stage = D1_STAGE_SUCCESS;",
                ]
            )
        else:
            lines.extend(
                [
                    f"        if ((cursor + {payload_bytes}) > byte_count || (cursor + {payload_bytes}) > BEDROCK_RECORD_BYTES) begin",
                    f"          parse_ea_payload.next_cursor = cursor + {payload_bytes};",
                    "        end else begin",
                ]
            )
            for byte in range(payload_bytes):
                lines.append(
                    f"          parse_ea_payload.ea.payload[{byte * 8} +: 8] = record[((cursor + {byte}) * 8) +: 8];"
                )
            lines.extend(
                [
                    f"          parse_ea_payload.next_cursor = cursor + {payload_bytes};",
                    "          parse_ea_payload.ok = 1'b1;",
                    "          parse_ea_payload.stage = D1_STAGE_SUCCESS;",
                    "        end",
                ]
            )
        lines.append("      end")
        payload_cases.append("\n".join(lines))

    descriptor_parse_cases: list[str] = []
    for family in families:
        descriptor_bytes = family.descriptor_bytes
        descriptor_signal = f"{_identifier(family.name).lower()}_decode"
        descriptor_parse_cases.append(
            f"""      {family_names[family.name]}: begin
        if ((cursor_in + {descriptor_bytes}) > byte_count ||
            (cursor_in + {descriptor_bytes}) > BEDROCK_RECORD_BYTES) begin
          resolve_ea_descriptor.next_cursor = cursor_in + {descriptor_bytes};
        end else if ({descriptor_signal}.valid) begin
          resolve_ea_descriptor.ok = 1'b1;
          resolve_ea_descriptor.stage = D1_STAGE_SUCCESS;
          resolve_ea_descriptor.next_cursor = cursor_in + {descriptor_bytes};
          resolve_ea_descriptor.ea = merge_descriptor_ea(
            compact_decode.ea,
            {descriptor_signal}.ea
          );
        end
      end"""
        )
    payload_byte_count_cases = [
        f"      {names.ea_payload_width[str(payload_width)]}: "
        f"ea_payload_byte_count = 6'd{payload_width // 8};"
        for payload_width in payload_widths
    ]
    descriptor_byte_count_cases = [
        f"      {family_names[family.name]}: "
        f"ea_descriptor_byte_count = 2'd{family.descriptor_bytes};"
        for family in families
    ]
    descriptor_inputs = "\n".join(
        f"    input descriptor_decode_t {_identifier(family.name).lower()}_decode,"
        for family in families
    )
    family_enum_text = ",\n".join(family_enum)

    return f"""  typedef enum logic [{family_width - 1}:0] {{
{family_enum_text}
  }} ea_descriptor_family_e;

  typedef struct packed {{
    logic valid;
    ea_descriptor_family_e descriptor_family;
    decoded_ea_t ea;
  }} compact_ea_decode_t;

  typedef struct packed {{
    logic valid;
    decoded_ea_t ea;
  }} descriptor_decode_t;

  function automatic compact_ea_decode_t decode_compact_ea(
    input ea_profile_e profile,
    input logic [6:0] compact_raw
  );
    begin
      decode_compact_ea = '0;
      unique case (profile)
      {valid_profiles}: begin
        unique casez (compact_raw)
{chr(10).join(common_cases)}
        default: begin
          unique case (profile)
{chr(10).join(profile_specific_cases)}
            default: begin end
          endcase
        end
        endcase
      end
        default: begin end
      endcase
    end
  endfunction

{chr(10).join(descriptor_functions)}

  function automatic decoded_ea_t merge_descriptor_ea(
    input decoded_ea_t compact_ea,
    input decoded_ea_t descriptor_ea
  );
    begin
      merge_descriptor_ea = compact_ea;
      merge_descriptor_ea.kind = descriptor_ea.kind;
      merge_descriptor_ea.segment = descriptor_ea.segment;
      merge_descriptor_ea.base = descriptor_ea.base;
      merge_descriptor_ea.register_name = descriptor_ea.register_name;
      merge_descriptor_ea.update_target = descriptor_ea.update_target;
      merge_descriptor_ea.update_mode = descriptor_ea.update_mode;
      merge_descriptor_ea.update_difference = descriptor_ea.update_difference;
      merge_descriptor_ea.direct_register_valid = descriptor_ea.direct_register_valid;
      merge_descriptor_ea.direct_register = descriptor_ea.direct_register;
      merge_descriptor_ea.base_register_valid = descriptor_ea.base_register_valid;
      merge_descriptor_ea.base_register = descriptor_ea.base_register;
      merge_descriptor_ea.index_register_valid = descriptor_ea.index_register_valid;
      merge_descriptor_ea.index_register = descriptor_ea.index_register;
      merge_descriptor_ea.stride_register_valid = descriptor_ea.stride_register_valid;
      merge_descriptor_ea.stride_register = descriptor_ea.stride_register;
      merge_descriptor_ea.segment_register_valid = descriptor_ea.segment_register_valid;
      merge_descriptor_ea.segment_register = descriptor_ea.segment_register;
    end
  endfunction

  function automatic ea_parse_result_t parse_ea_payload(
    input decoded_ea_t ea_in,
    input logic [BEDROCK_RECORD_BYTES*8-1:0] record,
    input logic [4:0] byte_count,
    input logic [5:0] cursor
  );
    begin
      parse_ea_payload = '0;
      parse_ea_payload.stage = D1_STAGE_EA_PAYLOAD;
      parse_ea_payload.next_cursor = cursor;
      parse_ea_payload.ea = ea_in;
      unique case (ea_in.payload_width)
{chr(10).join(payload_cases)}
        default: begin end
      endcase
    end
  endfunction

  function automatic logic [5:0] ea_payload_byte_count(
    input decoded_ea_t ea_in
  );
    begin
      ea_payload_byte_count = 6'd0;
      unique case (ea_in.payload_width)
{chr(10).join(payload_byte_count_cases)}
        default: begin end
      endcase
    end
  endfunction

  function automatic logic [1:0] ea_descriptor_byte_count(
    input compact_ea_decode_t compact_decode
  );
    begin
      ea_descriptor_byte_count = 2'd0;
      unique case (compact_decode.descriptor_family)
{chr(10).join(descriptor_byte_count_cases)}
        default: begin end
      endcase
    end
  endfunction

  function automatic ea_parse_result_t resolve_ea_descriptor(
    input ea_profile_e profile,
    input operand_ea_width_e operand_width,
    input compact_ea_decode_t compact_decode,
{descriptor_inputs}
    input logic [4:0] byte_count,
    input logic [5:0] cursor_in
  );
    begin
      resolve_ea_descriptor = '0;
      resolve_ea_descriptor.stage = D1_STAGE_EA_DESCRIPTOR;
      resolve_ea_descriptor.next_cursor = cursor_in;
      resolve_ea_descriptor.ea = compact_decode.ea;
      if (compact_decode.valid) unique case (compact_decode.descriptor_family)
      EA_DESCRIPTOR_FAMILY_NONE: begin
        resolve_ea_descriptor.ok = 1'b1;
        resolve_ea_descriptor.stage = D1_STAGE_SUCCESS;
      end
{chr(10).join(descriptor_parse_cases)}
        default: begin end
      endcase
      resolve_ea_descriptor.ea.profile = profile;
      resolve_ea_descriptor.ea.operand_width = operand_width;
    end
  endfunction

  function automatic ea_parse_result_t combine_ea_parse(
    input ea_parse_result_t descriptor_parse,
    input ea_parse_result_t payload_parse
  );
    begin
      combine_ea_parse = descriptor_parse;
      if (descriptor_parse.ok) begin
        combine_ea_parse.ok = payload_parse.ok;
        combine_ea_parse.stage = payload_parse.stage;
        combine_ea_parse.next_cursor = payload_parse.next_cursor;
        combine_ea_parse.ea.payload = payload_parse.ea.payload;
      end
    end
  endfunction"""


def _render_form_case(
    form: decode_ir.FormIR,
    ir: decode_ir.DecodeIR,
    names: Names,
    public_layout: PublicLayout,
    case_label: str | None = None,
) -> str:
    payload_layout = next(
        (layout for layout in form.layout if isinstance(layout, decode_ir.ReadPayloadIR)),
        None,
    )
    size_names = _mask_names("SIZE", public_layout.size_order)
    lines = [
        f"          {case_label or names.form[form.key]}: begin // {form.index}: {form.key}",
        f"        decoded_result.operation = {names.operation[form.mnemonic]};",
        f"        decoded_result.control.route = {names.route[form.control.route]};",
        f"        decoded_result.control.instruction_set = {names.instruction_set[form.control.instruction_set]};",
        f"        decoded_result.control.instruction_class = {names.instruction_class[form.control.instruction_class]};",
        f"        decoded_result.control.privilege = {names.privilege[form.control.privilege]};",
        f"        decoded_result.control.predicate_mode = {names.predicate[form.control.predicate_mode]};",
        f"        decoded_result.control.repeat_observed = {names.observed_kind[form.control.repeat.observed_kind]};",
        f"        decoded_result.control.repeat_rep = 1'b{int(form.control.repeat.rep)};",
        f"        decoded_result.control.repeat_repcc = 1'b{int(form.control.repeat.repcc)};",
        f"        decoded_result.control.has_ea_operand = 1'b{int(form.control.has_ea_operand)};",
    ]
    lines.extend(_render_mask_assignment("decoded_result.size_mask", form.sizes, size_names))
    lines.extend(
        line.replace("result_o.", "decoded_result.")
        for line in _render_availability_assignment(form, public_layout)
    )
    lines.extend(
        [
            f"        decoded_result.operand_count = 3'd{len(form.operands)};",
            "        decoded_result.required_bytes = {1'b0, layout_cursor};",
        ]
    )
    observed_slot = next((i for i, x in enumerate(form.operands) if x.name == form.control.repeat.observed_operand), 0)
    lines.append(f"        decoded_result.control.repeat_observed_operand = 2'd{observed_slot};")
    for slot, operand in enumerate(form.operands):
        source = operand.source
        lines.extend(
            [
                f"        decoded_result.operands[{slot}].valid = 1'b1;",
                f"        decoded_result.operands[{slot}].type_name = {names.operand_type[operand.type_name]};",
                f"        decoded_result.operands[{slot}].access = {names.access[operand.access]};",
                f"        decoded_result.operands[{slot}].ea_width = {names.ea_width[operand.ea_width]};",
                f"        decoded_result.operands[{slot}].payload_signed = 1'b{int(isinstance(source, decode_ir.AppendedPayloadSourceIR) and source.signed)};",
            ]
        )
        if isinstance(source, (decode_ir.EncodedFieldSourceIR, decode_ir.EffectiveAddressSourceIR)):
            lines.append(
                f"        decoded_result.operands[{slot}].value = "
                f"64'({_gather('d0_i.opcode', source.positions)});"
            )
        elif isinstance(source, decode_ir.FixedSourceIR):
            lines.append(
                f"        decoded_result.operands[{slot}].value = "
                f"64'h{(source.value or 0):016x};"
            )
        if isinstance(source, decode_ir.EffectiveAddressSourceIR):
            candidate_slot = _ea_candidate_slot(form, operand)
            lines.extend(
                [
                    f"        decoded_result.operands[{slot}].ea_valid = 1'b1;",
                    f"        decoded_result.operands[{slot}].ea_slot = 1'd{candidate_slot};",
                ]
            )
    if form.overlaps:
        slots = {operand.name: index for index, operand in enumerate(form.operands)}
        lines.append(f"        decoded_result.overlap_count = 2'd{len(form.overlaps)};")
        for index, overlap in enumerate(form.overlaps):
            lines.extend(
                [
                    f"        decoded_result.overlaps[{index}].valid = 1'b1;",
                    f"        decoded_result.overlaps[{index}].rule = {names.overlap_rule[overlap.rule]};",
                    f"        decoded_result.overlaps[{index}].left_operand = 2'd{slots[overlap.left]};",
                    f"        decoded_result.overlaps[{index}].right_operand = 2'd{slots[overlap.right]};",
                ]
            )
    operand_slots = {operand.name: index for index, operand in enumerate(form.operands)}
    lines.extend(
        [
            "        if (!layout_valid) begin",
            "          layout_failed = 1'b1;",
            "          decoded_result.stage = D1_STAGE_EA_DESCRIPTOR;",
            "        end",
        ]
    )
    if payload_layout is not None:
        slot = operand_slots[payload_layout.operand_name]
        byte_width = payload_layout.width // 8
        payload_cursor = _standalone_payload_cursor_expression(form, payload_layout)
        lines.extend(
            [
                "        if (!layout_failed) begin",
                f"          decoded_result.required_bytes = {{1'b0, layout_cursor}} + 6'd{byte_width};",
                "          if (decoded_result.required_bytes > byte_count_i || decoded_result.required_bytes > BEDROCK_RECORD_BYTES) begin",
                "            layout_failed = 1'b1;",
                "            decoded_result.stage = D1_STAGE_STANDALONE_PAYLOAD;",
                "          end else begin",
            ]
        )
        for byte in range(byte_width):
            lines.append(
                f"            decoded_result.operands[{slot}].value[{byte * 8} +: 8] = "
                f"record_i[((({payload_cursor}) + {byte}) * 8) +: 8];"
            )
        lines.extend(["          end", "        end"])
    for slot, operand in enumerate(form.operands):
        if operand.legal_values:
            lines.extend(
                [
                    f"        // legal values for operand {slot}: {operand.name}",
                    "        if (",
                    "          !layout_failed &&",
                    "          !(",
                ]
            )
            for value_index, value in enumerate(operand.legal_values):
                suffix = " ||" if value_index + 1 < len(operand.legal_values) else ""
                lines.append(
                    f"            (decoded_result.operands[{slot}].value == 64'h{value:016x}){suffix}"
                )
            lines.extend(
                [
                    "          )",
                    "        ) begin",
                    "          layout_failed = 1'b1;",
                    "          decoded_result.stage = D1_STAGE_STATIC_LEGALITY;",
                    "        end",
                ]
            )
    lines.extend(
        [
            "        if (!layout_failed) begin",
            "          if (decoded_result.required_bytes > byte_count_i || decoded_result.required_bytes > BEDROCK_RECORD_BYTES)",
            "            decoded_result.stage = D1_STAGE_RECORD_LENGTH;",
            "          else begin",
            "            decoded_result.valid = 1'b1;",
            "            decoded_result.stage = D1_STAGE_SUCCESS;",
            "          end",
            "        end",
            "      end",
        ]
    )
    return "\n".join(lines)


def _render_d1(ir: decode_ir.DecodeIR, names: Names) -> str:
    public_layout = derive_public_layout(ir)
    cases = []
    for form in ir.forms:
        value = form.index + 1
        high = value >> 5
        low = value & 31
        pattern = ["?"] * 64
        pattern[31 - high] = "1"
        pattern[32 + 31 - low] = "1"
        cases.append(
            _render_form_case(
                form,
                ir,
                names,
                public_layout,
                case_label=f"64'b{''.join(pattern)}",
            )
        )
    return d1_emitter.render(
        ea_span_function=_render_compact_ea_span_function(ir, names),
        form_cases="\n".join(cases),
    )


def _render_ea_decoder(ir: decode_ir.DecodeIR, names: Names) -> str:
    return ea_emitter.render(parsing_functions=_render_ea_function(ir, names))


@dataclass(frozen=True)
class LoweredOutputs:
    package: str
    d0: str
    d1: str
    ea: str


def lower(ir: decode_ir.DecodeIR) -> LoweredOutputs:
    """Lower one Decode IR snapshot without performing filesystem I/O."""
    package, names = _render_package(ir)
    return LoweredOutputs(
        package=package,
        d0=_render_d0(ir, names),
        d1=_render_d1(ir, names),
        ea=_render_ea_decoder(ir, names),
    )
