#!/usr/bin/env python3
"""Generate the combinational Bedrock D0, D1 opcode, and EA decoders."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
import tempfile
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
ISA_TOOLS = ROOT / "isa" / "tools"
sys.path.insert(0, str(ISA_TOOLS))

import decode_ir


OUTPUT_NAMES = (
    "bedrock_decode_pkg.sv",
    "bedrock_decode_d0.sv",
    "bedrock_decode_d1.sv",
    "bedrock_decode_ea.sv",
)

EA_LOW_POSITIONS = (6, 5, 4, 3, 2, 1, 0)
EA_HIGH_POSITIONS = (13, 12, 11, 10, 9, 8, 7)
EA_MEDIUM_ALT_POSITIONS = (16, 15, 14, 3, 2, 1, 0)

EA_LAYOUT_NONE = "EA_LAYOUT_NONE"
EA_LAYOUT_LOW = "EA_LAYOUT_LOW"
EA_LAYOUT_ALT = "EA_LAYOUT_ALT"
EA_LAYOUT_ALT_THEN_LOW = "EA_LAYOUT_ALT_THEN_LOW"


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_build_dir(raw_build_dir: Path) -> Path:
    """Accept only a repository build subtree or a dedicated external temp path."""
    build_dir = raw_build_dir.expanduser().resolve()
    repository_build = (ROOT / "build").resolve()
    if _is_within(build_dir, repository_build):
        return build_dir
    temp_roots = {
        Path(tempfile.gettempdir()).resolve(),
        Path("/private/tmp").resolve(),
        Path("/tmp").resolve(),
        Path("/var/tmp").resolve(),
    }
    if not _is_within(build_dir, ROOT) and any(
        build_dir != root and _is_within(build_dir, root) for root in temp_roots
    ):
        return build_dir
    raise ValueError(
        f"refusing SystemVerilog build directory outside {repository_build} "
        f"or an external temporary directory: {build_dir}"
    )


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
    if form.opcode_class in ("long", "extralong") and source.positions == EA_HIGH_POSITIONS:
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
    if slots == (1, 0) and form.opcode_class in ("long", "extralong"):
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
    compact_raw: int,
    record: bytes | tuple[int, ...] | list[int],
    byte_count: int,
    cursor: int,
) -> tuple[str, dict[str, object] | None, int]:
    """Reference one IR-owned EA parse, including descriptor and payload byte order."""
    entry = ir.effective_addresses.compact_entries[compact_raw]
    if not entry.valid:
        return "ea_descriptor", None, cursor
    compact = next(
        form
        for form in ir.effective_addresses.compact_forms
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
        if next_cursor + family.descriptor_bytes > byte_count or next_cursor + family.descriptor_bytes > ir.limits.max_record_bytes:
            return "ea_descriptor", None, next_cursor + family.descriptor_bytes
        for byte in record[next_cursor : next_cursor + family.descriptor_bytes]:
            descriptor = (descriptor << 8) | byte
        descriptor_form = next(
            (
                form
                for form in family.forms
                if descriptor & form.mask == form.value
            ),
            None,
        )
        if descriptor_form is None:
            return "ea_descriptor", None, cursor
        next_cursor += family.descriptor_bytes
    payload_bytes = compact.payload_width // 8
    if next_cursor + payload_bytes > byte_count or next_cursor + payload_bytes > ir.limits.max_record_bytes:
        return "ea_payload", None, next_cursor + payload_bytes
    payload = sum(
        record[next_cursor + offset] << (offset * 8)
        for offset in range(payload_bytes)
    )
    next_cursor += payload_bytes
    canonical_form = descriptor_form or compact
    canonical_fields = {
        "direct_register_valid": False,
        "direct_register": 0,
        "base_register_valid": False,
        "base_register": 0,
        "index_register_valid": False,
        "index_register": 0,
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
            "payload": payload,
            "payload_width": compact.payload_width,
            "payload_signed": compact.payload_signed,
            "kind": canonical_form.kind,
            "segment": canonical_form.segment,
            "base": canonical_form.base,
            "register_name": canonical_form.register_name,
            "update_target": canonical_form.update_target,
            "update_mode": canonical_form.update_mode,
            **canonical_fields,
        },
        next_cursor,
    )


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
    cursor = form.opcode_bytes
    for layout in form.layout:
        operand = next(item for item in form.operands if item.name == layout.operand_name)
        if isinstance(layout, decode_ir.ParseEaIR):
            stage, decoded, next_cursor = reference_ea(
                ir, values[operand.name] & 0x7F, record, byte_count, cursor
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
    overlap_rule: dict[str, str]
    observed_kind: dict[str, str]
    ea_kind: dict[str, str]
    ea_segment: dict[str, str]
    ea_base: dict[str, str]
    ea_register: dict[str, str]
    update_target: dict[str, str]
    update_mode: dict[str, str]
    ea_payload_width: dict[str, str]


@dataclass(frozen=True)
class PublicLayout:
    size_order: tuple[str, ...]
    touched_flag_order: tuple[str, ...]
    possible_event_order: tuple[str, ...]


def derive_public_layout(ir: decode_ir.DecodeIR) -> PublicLayout:
    """Derive public mask orders from live IR."""
    return PublicLayout(
        size_order=tuple(sorted({size for form in ir.forms for size in form.sizes})),
        touched_flag_order=tuple(
            sorted(
                {
                    flag
                    for form in ir.forms
                    for flag in form.annotations.touched_flags
                }
            )
        ),
        possible_event_order=tuple(
            sorted(
                {
                    event
                    for form in ir.forms
                    for event in form.annotations.possible_events
                }
            )
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


def _all_ea_forms(ir: decode_ir.DecodeIR) -> tuple[decode_ir.EaFormIR, ...]:
    return ir.effective_addresses.compact_forms + tuple(
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

    opcode_classes = _ordered(
        (form.opcode_class for form in forms), empty_first=False
    )
    opcode_class = add("opcode_class_e", "OPCODE_CLASS", opcode_classes)
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
    overlap_rule = add("overlap_rule_e", "OVERLAP", _ordered(x.rule for f in forms for x in f.overlaps))
    observed_kind = add("repeat_observed_e", "REPEAT_OBSERVED", _ordered(f.control.repeat.observed_kind for f in forms))
    ea_kind = add("ea_kind_e", "EA_KIND", _ordered(x.kind for x in ea_forms))
    ea_segment = add("ea_segment_e", "EA_SEGMENT", _ordered(x.segment for x in ea_forms))
    ea_base = add("ea_base_e", "EA_BASE", _ordered(x.base for x in ea_forms))
    ea_register = add("ea_register_e", "EA_REGISTER", _ordered(x.register_name for x in ea_forms))
    update_target = add("ea_update_target_e", "EA_UPDATE_TARGET", _ordered(x.update_target for x in ea_forms))
    update_mode = add("ea_update_mode_e", "EA_UPDATE_MODE", _ordered(x.update_mode for x in ea_forms))
    ea_payload_width = add(
        "ea_payload_width_e",
        "EA_PAYLOAD_WIDTH",
        tuple(
            str(width)
            for width in sorted(
                {item.payload_width for item in ir.effective_addresses.compact_forms}
            )
        ),
    )
    names = Names(
        opcode_class, form, operation, route, instruction_set, instruction_class,
        privilege, predicate, operand_type, access, ea_width, overlap_rule,
        observed_kind, ea_kind, ea_segment, ea_base, ea_register, update_target,
        update_mode, ea_payload_width,
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
                "BEDROCK_TOUCHED_FLAG_MASK_BITS",
                "TOUCHED_FLAG",
                public_layout.touched_flag_order,
            ),
            _render_mask_constants(
                "BEDROCK_POSSIBLE_EVENT_MASK_BITS",
                "POSSIBLE_EVENT",
                public_layout.possible_event_order,
            ),
        )
    )
    text = f"""// Generated from canonical Decode IR. Do not edit.
package bedrock_decode_pkg;
  localparam logic [9:0] BEDROCK_OPCODE_BITS = 10'd{ir.limits.max_opcode_width};
  localparam logic [9:0] BEDROCK_RECORD_BYTES = 10'd{ir.limits.max_record_bytes};
  localparam logic [9:0] BEDROCK_FORM_COUNT = 10'd{ir.limits.form_count};
  localparam logic [9:0] BEDROCK_OPERAND_SLOTS = 10'd{ir.limits.max_operands};
  localparam logic [9:0] BEDROCK_EA_SLOTS = 10'd{ir.limits.max_ea_operands};
  localparam logic [9:0] BEDROCK_SIZE_MASK_BITS = 10'd{len(public_layout.size_order)};
  localparam logic [9:0] BEDROCK_TOUCHED_FLAG_MASK_BITS = 10'd{len(public_layout.touched_flag_order)};
  localparam logic [9:0] BEDROCK_POSSIBLE_EVENT_MASK_BITS = 10'd{len(public_layout.possible_event_order)};
  localparam logic [0:0] BEDROCK_EA_LOW_SLOT = 1'd0;
  localparam logic [0:0] BEDROCK_EA_ALT_SLOT = 1'd1;

{mask_constants}

  {enum_text}

  typedef struct packed {{
    d0_status_e status;
    opcode_class_e opcode_class;
    form_id_e form;
    logic [BEDROCK_OPCODE_BITS-1:0] opcode;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
  }} d0_result_t;

  typedef struct packed {{
    d0_status_e status;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
    logic [6:0] low_raw;
    logic [6:0] alt_raw;
    logic [3:0] base_cursor;
    logic [3:0] post_alt_cursor;
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
    ea_kind_e kind;
    ea_segment_e segment;
    ea_base_e base;
    ea_register_e register_name;
    operand_ea_width_e operand_width;
    ea_update_target_e update_target;
    ea_update_mode_e update_mode;
    ea_payload_width_e payload_width;
    logic payload_signed;
    logic direct_register_valid;
    logic [3:0] direct_register;
    logic base_register_valid;
    logic [3:0] base_register;
    logic index_register_valid;
    logic [3:0] index_register;
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
    logic repeat_repg;
    logic [1:0] repeat_observed_operand;
    logic has_ea_operand;
  }} control_metadata_t;

  typedef struct packed {{
    logic valid;
    logic [3:0] encoded_bytes;
  }} ea_span_result_t;

  typedef struct packed {{
    logic valid;
    decode_stage_e stage;
    form_id_e form;
    operation_e operation;
    control_metadata_t control;
    logic [BEDROCK_SIZE_MASK_BITS-1:0] size_mask;
    logic [2:0] operand_count;
    decoded_operand_t [BEDROCK_OPERAND_SLOTS-1:0] operands;
    overlap_descriptor_t overlap;
    logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] touched_flag_mask;
    logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] possible_event_mask;
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
endpackage
"""
    return text, names


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
        return "(" + " || ".join(parts) + ")"
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
    class_bytes: dict[str, int] = {}
    for form in ir.forms:
        previous = class_bytes.setdefault(form.opcode_class, form.opcode_bytes)
        if previous != form.opcode_bytes:
            raise ValueError(f"opcode class {form.opcode_class} has mixed widths")
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
            raw = f"((opcode_i & {_hex(34, form.opcode_mask)}) == {_hex(34, form.opcode_value)})"
            low_width, alt_width = _ea_candidate_widths(form, names)
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
    return f"""// Generated from canonical Decode IR. Do not edit.
module bedrock_decode_d0
  import bedrock_decode_pkg::*;
(
  input  logic valid_i,
  input  opcode_class_e opcode_class_i,
  input  logic [BEDROCK_OPCODE_BITS-1:0] opcode_i,
  output d0_result_t result_o,
  output d0_ea_result_t ea_result_o
);
  typedef struct packed {{
    logic valid;
    form_id_e form;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
  }} d0_selection_t;

  logic class_raw_match;
  d0_selection_t class_selection;
  {form_bits_type} class_form;
  ea_span_result_t alt_span;
{chr(10).join(constraint_declarations)}
{chr(10).join(form_declarations)}
{chr(10).join(tree_declarations)}

{_render_ea_span_function(ir)}

{_render_opcode_class_bytes_function(ir)}

{chr(10).join(constraint_assignments)}
{chr(10).join(form_assignments)}
{chr(10).join(tree_assignments)}

  always_comb begin
    result_o = '0;
    result_o.status = D0_INVALID_INPUT;
    result_o.opcode_class = opcode_class_i;
    result_o.opcode = opcode_i;
    ea_result_o = '0;
    ea_result_o.low_raw = opcode_i[6:0];
    unique case (opcode_class_i)
      OPCODE_CLASS_MEDIUM: begin
        ea_result_o.alt_raw = {{opcode_i[16:14], opcode_i[3:0]}};
      end
      OPCODE_CLASS_LONG, OPCODE_CLASS_EXTRALONG: begin
        ea_result_o.alt_raw = opcode_i[13:7];
      end
      default: begin end
    endcase
    ea_result_o.base_cursor = opcode_class_bytes(opcode_class_i);
    ea_result_o.post_alt_cursor = ea_result_o.base_cursor;
    alt_span = encoded_ea_span(ea_result_o.alt_raw);
    if (alt_span.valid)
      ea_result_o.post_alt_cursor =
        ea_result_o.base_cursor + {{2'b0, alt_span.encoded_bytes}};
    class_raw_match = 1'b0;
    class_selection = '0;
    class_form = '0;
    unique case (opcode_class_i)
{chr(10).join(class_cases)}
      default: begin end
    endcase
    if (valid_i) begin
      result_o.status = D0_UNALLOCATED_OPCODE;
      if (class_selection.valid) begin
        result_o.status = D0_SUCCESS;
        result_o.form = form_id_e'(class_form);
        result_o.ea_layout = class_selection.ea_layout;
        result_o.ea_widths = class_selection.ea_widths;
      end else if (class_raw_match) begin
        result_o.status = D0_CONSTRAINT_REJECTED;
      end
    end
    ea_result_o.status = result_o.status;
    ea_result_o.ea_layout = result_o.ea_layout;
    ea_result_o.ea_widths = result_o.ea_widths;
  end
endmodule
"""


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


def _render_ea_span_function(ir: decode_ir.DecodeIR) -> str:
    compact_by_name = {
        item.name: item for item in ir.effective_addresses.compact_forms
    }
    cases = []
    for entry in ir.effective_addresses.compact_entries:
        lines = [
            f"      7'h{entry.raw:02x}: begin // "
            f"{entry.form_name or entry.invalid_reason}"
        ]
        if entry.valid:
            compact = compact_by_name[entry.form_name]
            encoded_bytes = compact.descriptor_bytes + compact.payload_width // 8
            lines.extend(
                [
                    "        encoded_ea_span.valid = 1'b1;",
                    f"        encoded_ea_span.encoded_bytes = 4'd{encoded_bytes};",
                ]
            )
        lines.append("      end")
        cases.append("\n".join(lines))
    return f"""  function automatic ea_span_result_t encoded_ea_span(
    input logic [6:0] compact_raw
  );
    begin
      encoded_ea_span = '0;
      unique case (compact_raw)
{chr(10).join(cases)}
        default: begin end
      endcase
    end
  endfunction"""


def _render_ea_function(ir: decode_ir.DecodeIR, names: Names) -> str:
    families = {item.name: item for item in ir.effective_addresses.descriptor_families}
    entries = {item.raw: item for item in ir.effective_addresses.compact_entries}
    compact_by_name = {item.name: item for item in ir.effective_addresses.compact_forms}
    cases: list[str] = []
    for raw in range(128):
        entry = entries[raw]
        lines = [f"      7'h{raw:02x}: begin // {entry.form_name or entry.invalid_reason}"]
        if not entry.valid:
            lines.extend(["        parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;", "      end"])
            cases.append("\n".join(lines))
            continue
        compact = compact_by_name[entry.form_name]
        lines.extend(
            [
                "        parse_one_ea.ea.valid = 1'b1;",
                f"        parse_one_ea.ea.payload_width = {names.ea_payload_width[str(compact.payload_width)]};",
                f"        parse_one_ea.ea.payload_signed = 1'b{int(compact.payload_signed)};",
            ]
        )
        lines.extend(
            "        " + x
            for x in _ea_static_assignments(
                "parse_one_ea.ea", compact, names, raw_signal="compact_raw"
            )
        )
        if compact.referenced_descriptor_family:
            family = families[compact.referenced_descriptor_family]
            descriptor_bytes = family.descriptor_bytes
            lines.extend(
                [
                    f"        if ((cursor + {descriptor_bytes}) > byte_count || (cursor + {descriptor_bytes}) > BEDROCK_RECORD_BYTES) begin",
                    "          parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                    f"          cursor = cursor + {descriptor_bytes};",
                    "        end else begin",
                ]
            )
            if descriptor_bytes == 1:
                lines.append("          descriptor = {8'd0, record[(cursor * 8) +: 8]};")
            else:
                lines.append("          descriptor = {record[(cursor * 8) +: 8], record[((cursor + 1) * 8) +: 8]};")
            lines.append("          descriptor_match = 1'b0;")
            descriptor_width = descriptor_bytes * 8
            lines.append(
                f"          unique casez (descriptor[{descriptor_width - 1}:0])"
            )
            for descriptor_form in family.forms:
                lines.extend(
                    [
                        f"            {_casez(descriptor_width, descriptor_form.value, descriptor_form.mask)}: begin // {descriptor_form.name}",
                        "              descriptor_match = 1'b1;",
                    ]
                )
                lines.extend(
                    "              " + x
                    for x in _ea_static_assignments(
                        "parse_one_ea.ea",
                        descriptor_form,
                        names,
                        raw_signal="descriptor",
                    )
                )
                lines.append("            end")
            lines.extend(
                [
                    "            default: begin end",
                    "          endcase",
                ]
            )
            lines.extend(
                [
                    "          if (!descriptor_match) begin",
                    "            parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;",
                    "          end else begin",
                    f"            cursor = cursor + {descriptor_bytes};",
                ]
            )
            payload_indent = "            "
            close_descriptor = True
        else:
            payload_indent = "        "
            close_descriptor = False
        payload_bytes = compact.payload_width // 8
        if payload_bytes:
            lines.extend(
                [
                    f"{payload_indent}if ((cursor + {payload_bytes}) > byte_count || (cursor + {payload_bytes}) > BEDROCK_RECORD_BYTES) begin",
                    f"{payload_indent}  parse_one_ea.stage = D1_STAGE_EA_PAYLOAD;",
                    f"{payload_indent}  cursor = cursor + {payload_bytes};",
                    f"{payload_indent}end else begin",
                ]
            )
            for byte in range(payload_bytes):
                lines.append(
                    f"{payload_indent}  parse_one_ea.ea.payload[{byte * 8} +: 8] = record[((cursor + {byte}) * 8) +: 8];"
                )
            lines.extend(
                [
                    f"{payload_indent}  cursor = cursor + {payload_bytes};",
                    f"{payload_indent}  parse_one_ea.ok = 1'b1;",
                    f"{payload_indent}  parse_one_ea.stage = D1_STAGE_SUCCESS;",
                    f"{payload_indent}end",
                ]
            )
        else:
            lines.extend(
                [
                    f"{payload_indent}parse_one_ea.ok = 1'b1;",
                    f"{payload_indent}parse_one_ea.stage = D1_STAGE_SUCCESS;",
                ]
            )
        if close_descriptor:
            lines.extend(["          end", "        end"])
        lines.extend(
            [
                "        parse_one_ea.next_cursor = cursor[5:0];",
                "      end",
            ]
        )
        cases.append("\n".join(lines))
    return f"""  function automatic ea_parse_result_t parse_one_ea(
    input logic [6:0] compact_raw,
    input operand_ea_width_e operand_width,
    input logic [BEDROCK_RECORD_BYTES*8-1:0] record,
    input logic [4:0] byte_count,
    input logic [5:0] cursor_in
  );
    integer unsigned cursor;
    logic [15:0] descriptor;
    logic descriptor_match;
    begin
      parse_one_ea = '0;
      parse_one_ea.stage = D1_STAGE_EA_DESCRIPTOR;
      parse_one_ea.next_cursor = cursor_in;
      parse_one_ea.ea.operand_width = operand_width;
      cursor = cursor_in;
      descriptor = '0;
      descriptor_match = 1'b0;
      unique case (compact_raw)
{chr(10).join(cases)}
        default: begin end
      endcase
    end
  endfunction"""


def _render_form_case(
    form: decode_ir.FormIR,
    ir: decode_ir.DecodeIR,
    names: Names,
    public_layout: PublicLayout,
) -> str:
    size_names = _mask_names("SIZE", public_layout.size_order)
    flag_names = _mask_names("TOUCHED_FLAG", public_layout.touched_flag_order)
    event_names = _mask_names("POSSIBLE_EVENT", public_layout.possible_event_order)
    lines = [
        f"      {names.form[form.key]}: begin // {form.index}: {form.key}",
        f"        result_o.operation = {names.operation[form.mnemonic]};",
        f"        result_o.control.route = {names.route[form.control.route]};",
        f"        result_o.control.instruction_set = {names.instruction_set[form.control.instruction_set]};",
        f"        result_o.control.instruction_class = {names.instruction_class[form.control.instruction_class]};",
        f"        result_o.control.privilege = {names.privilege[form.control.privilege]};",
        f"        result_o.control.predicate_mode = {names.predicate[form.control.predicate_mode]};",
        f"        result_o.control.repeat_observed = {names.observed_kind[form.control.repeat.observed_kind]};",
        f"        result_o.control.repeat_rep = 1'b{int(form.control.repeat.rep)};",
        f"        result_o.control.repeat_repcc = 1'b{int(form.control.repeat.repcc)};",
        f"        result_o.control.repeat_repg = 1'b{int(form.control.repeat.repg)};",
        f"        result_o.control.has_ea_operand = 1'b{int(form.control.has_ea_operand)};",
    ]
    lines.extend(_render_mask_assignment("result_o.size_mask", form.sizes, size_names))
    lines.extend(
        _render_mask_assignment(
            "result_o.touched_flag_mask",
            form.annotations.touched_flags,
            flag_names,
        )
    )
    lines.extend(
        _render_mask_assignment(
            "result_o.possible_event_mask",
            form.annotations.possible_events,
            event_names,
        )
    )
    lines.extend(
        [
            f"        result_o.operand_count = 3'd{len(form.operands)};",
            f"        cursor = 6'd{form.opcode_bytes};",
        ]
    )
    observed_slot = next((i for i, x in enumerate(form.operands) if x.name == form.control.repeat.observed_operand), 0)
    lines.append(f"        result_o.control.repeat_observed_operand = 2'd{observed_slot};")
    for slot, operand in enumerate(form.operands):
        source = operand.source
        lines.extend(
            [
                f"        result_o.operands[{slot}].valid = 1'b1;",
                f"        result_o.operands[{slot}].type_name = {names.operand_type[operand.type_name]};",
                f"        result_o.operands[{slot}].access = {names.access[operand.access]};",
                f"        result_o.operands[{slot}].ea_width = {names.ea_width[operand.ea_width]};",
                f"        result_o.operands[{slot}].payload_signed = 1'b{int(isinstance(source, decode_ir.AppendedPayloadSourceIR) and source.signed)};",
            ]
        )
        if isinstance(source, (decode_ir.EncodedFieldSourceIR, decode_ir.EffectiveAddressSourceIR)):
            lines.append(
                f"        result_o.operands[{slot}].value = "
                f"64'({_gather('d0_i.opcode', source.positions)});"
            )
        elif isinstance(source, decode_ir.FixedSourceIR):
            lines.append(
                f"        result_o.operands[{slot}].value = "
                f"64'h{(source.value or 0):016x};"
            )
        if isinstance(source, decode_ir.EffectiveAddressSourceIR):
            candidate_slot = _ea_candidate_slot(form, operand)
            lines.extend(
                [
                    f"        result_o.operands[{slot}].ea_valid = 1'b1;",
                    f"        result_o.operands[{slot}].ea_slot = 1'd{candidate_slot};",
                ]
            )
    if form.overlaps:
        overlap = form.overlaps[0]
        slots = {operand.name: index for index, operand in enumerate(form.operands)}
        lines.extend(
            [
                "        result_o.overlap.valid = 1'b1;",
                f"        result_o.overlap.rule = {names.overlap_rule[overlap.rule]};",
                f"        result_o.overlap.left_operand = 2'd{slots[overlap.left]};",
                f"        result_o.overlap.right_operand = 2'd{slots[overlap.right]};",
            ]
        )
    operand_slots = {operand.name: index for index, operand in enumerate(form.operands)}
    for layout in form.layout:
        slot = operand_slots[layout.operand_name]
        if isinstance(layout, decode_ir.ParseEaIR):
            lines.extend(
                [
                    "        if (!layout_failed) begin",
                    f"          ea_span = encoded_ea_span(result_o.operands[{slot}].value[6:0]);",
                    "          if (!ea_span.valid) begin",
                    "            layout_failed = 1'b1;",
                    "            result_o.stage = D1_STAGE_EA_DESCRIPTOR;",
                    "          end else begin",
                    "            cursor = cursor + ea_span.encoded_bytes;",
                    "          end",
                    "        end",
                ]
            )
        else:
            byte_width = layout.width // 8
            lines.extend(
                [
                    "        if (!layout_failed) begin",
                    f"          if ((cursor + {byte_width}) > byte_count_i || (cursor + {byte_width}) > BEDROCK_RECORD_BYTES) begin",
                    "            layout_failed = 1'b1;",
                    "            result_o.stage = D1_STAGE_STANDALONE_PAYLOAD;",
                    f"            cursor = cursor + {byte_width};",
                    "          end else begin",
                ]
            )
            for byte in range(byte_width):
                lines.append(f"            result_o.operands[{slot}].value[{byte * 8} +: 8] = record_i[((cursor + {byte}) * 8) +: 8];")
            lines.extend([f"            cursor = cursor + {byte_width};", "          end", "        end"])
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
                    f"            (result_o.operands[{slot}].value == 64'h{value:016x}){suffix}"
                )
            lines.extend(
                [
                    "          )",
                    "        ) begin",
                    "          layout_failed = 1'b1;",
                    "          result_o.stage = D1_STAGE_STATIC_LEGALITY;",
                    "        end",
                ]
            )
    lines.extend(
        [
            "        result_o.required_bytes = cursor;",
            "        if (!layout_failed) begin",
            "          if (cursor > byte_count_i || cursor > BEDROCK_RECORD_BYTES)",
            "            result_o.stage = D1_STAGE_RECORD_LENGTH;",
            "          else begin",
            "            result_o.valid = 1'b1;",
            "            result_o.stage = D1_STAGE_SUCCESS;",
            "          end",
            "        end",
            "      end",
        ]
    )
    return "\n".join(lines)


def _render_d1(ir: decode_ir.DecodeIR, names: Names) -> str:
    public_layout = derive_public_layout(ir)
    cases = "\n".join(
        _render_form_case(form, ir, names, public_layout) for form in ir.forms
    )
    return f"""// Generated from canonical Decode IR. Do not edit.
module bedrock_decode_d1
  import bedrock_decode_pkg::*;
(
  input  d0_result_t d0_i,
  input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i,
  input  logic [4:0] byte_count_i,
  output d1_opcode_result_t result_o
);
  integer unsigned cursor;
  logic layout_failed;
  ea_span_result_t ea_span;

{_render_ea_span_function(ir)}

  always_comb begin
    result_o = '0;
    result_o.stage = D1_STAGE_D0_REJECTED;
    result_o.form = d0_i.form;
    result_o.encoded_bytes = byte_count_i;
    cursor = 0;
    layout_failed = 1'b0;
    ea_span = '0;
    if (d0_i.status == D0_SUCCESS) begin
      if (byte_count_i > BEDROCK_RECORD_BYTES) begin
        result_o.stage = D1_STAGE_RECORD_BOUNDS;
      end else unique case (d0_i.form)
{cases}
        default: result_o.stage = D1_STAGE_D0_REJECTED;
      endcase
    end
  end
endmodule
"""


def _render_ea_decoder(ir: decode_ir.DecodeIR, names: Names) -> str:
    return f"""// Generated from canonical Decode IR. Do not edit.
module bedrock_decode_ea
  import bedrock_decode_pkg::*;
(
  input  d0_ea_result_t d0_i,
  input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i,
  input  logic [4:0] byte_count_i,
  output ea_decode_result_t result_o
);
  logic [5:0] low_cursor;
  ea_parse_result_t low_parse;
  ea_parse_result_t alt_parse;

{_render_ea_function(ir, names)}

  always_comb begin
    result_o = '0;
    result_o.stage = D1_STAGE_D0_REJECTED;
    low_cursor = d0_i.base_cursor;
    if (d0_i.ea_layout == EA_LAYOUT_ALT_THEN_LOW)
      low_cursor = d0_i.post_alt_cursor;
    alt_parse = parse_one_ea(
      d0_i.alt_raw,
      d0_i.ea_widths[BEDROCK_EA_ALT_SLOT],
      record_i,
      byte_count_i,
      d0_i.base_cursor
    );
    low_parse = parse_one_ea(
      d0_i.low_raw,
      d0_i.ea_widths[BEDROCK_EA_LOW_SLOT],
      record_i,
      byte_count_i,
      low_cursor
    );
    if (d0_i.status == D0_SUCCESS) begin
      if (byte_count_i > BEDROCK_RECORD_BYTES) begin
        result_o.stage = D1_STAGE_RECORD_BOUNDS;
      end else begin
        if (low_parse.ok &&
            (d0_i.ea_layout != EA_LAYOUT_ALT_THEN_LOW || alt_parse.ok))
          result_o.eas[BEDROCK_EA_LOW_SLOT] = low_parse.ea;
        if (alt_parse.ok)
          result_o.eas[BEDROCK_EA_ALT_SLOT] = alt_parse.ea;
        unique case (d0_i.ea_layout)
        EA_LAYOUT_NONE: begin
          result_o.valid = 1'b1;
          result_o.stage = D1_STAGE_SUCCESS;
        end
        EA_LAYOUT_LOW: begin
          result_o.ea_count = 2'd1;
          result_o.required_bytes = low_parse.next_cursor;
          if (low_parse.ok) begin
            result_o.valid = 1'b1;
            result_o.stage = D1_STAGE_SUCCESS;
          end else begin
            result_o.stage = low_parse.stage;
          end
        end
        EA_LAYOUT_ALT: begin
          result_o.ea_count = 2'd1;
          result_o.required_bytes = alt_parse.next_cursor;
          if (alt_parse.ok) begin
            result_o.valid = 1'b1;
            result_o.stage = D1_STAGE_SUCCESS;
          end else begin
            result_o.stage = alt_parse.stage;
          end
        end
        EA_LAYOUT_ALT_THEN_LOW: begin
          result_o.ea_count = 2'd2;
          if (!alt_parse.ok) begin
            result_o.required_bytes = alt_parse.next_cursor;
            result_o.stage = alt_parse.stage;
          end else begin
            result_o.required_bytes = low_parse.next_cursor;
            if (!low_parse.ok) begin
              result_o.stage = low_parse.stage;
            end else begin
              result_o.valid = 1'b1;
              result_o.stage = D1_STAGE_SUCCESS;
            end
          end
        end
        endcase
      end
    end
  end
endmodule
"""


def render_outputs(build_dir: Path) -> dict[Path, str]:
    ir = decode_ir.load_decode_ir(ROOT / "isa" / "instructions" / "definitions")
    package, names = _render_package(ir)
    return {
        build_dir / OUTPUT_NAMES[0]: package,
        build_dir / OUTPUT_NAMES[1]: _render_d0(ir, names),
        build_dir / OUTPUT_NAMES[2]: _render_d1(ir, names),
        build_dir / OUTPUT_NAMES[3]: _render_ea_decoder(ir, names),
    }


def write_outputs(build_dir: Path) -> None:
    build_dir = validate_build_dir(build_dir)
    for path, text in render_outputs(build_dir).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def check_outputs(build_dir: Path) -> bool:
    build_dir = validate_build_dir(build_dir)
    return all(
        path.exists() and path.read_text(encoding="utf-8") == expected
        for path, expected in render_outputs(build_dir).items()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "build_dir",
        metavar="BUILD_DIR",
        type=Path,
        help="directory beneath repository build/ or a dedicated external temp directory",
    )
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args(argv)
    try:
        build_dir = validate_build_dir(args.build_dir)
        outputs = render_outputs(build_dir)
    except (OSError, ValueError) as error:
        print(f"SystemVerilog decoder generation failed: {error}", file=sys.stderr)
        return 1
    if args.check:
        stale = [
            path
            for path, expected in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        for path in stale:
            print(f"stale generated output: {path}", file=sys.stderr)
        return int(bool(stale))
    write_outputs(build_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
