#!/usr/bin/env python3
"""Generate the combinational Bedrock D0/D1 SystemVerilog decoder."""

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
)


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


def _gather(signal: str, positions: tuple[int, ...]) -> str:
    if not positions:
        return "64'd0"
    bits = ", ".join(f"{signal}[{position}]" for position in positions)
    return f"{{{bits}}}"


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
    if constraint.kind == "exclude_rn_direct":
        return not 0 <= value <= 0x0F
    if constraint.kind == "exclude_reg_direct":
        return not (0 <= value <= 0x0F or value == 0x68)
    if constraint.kind == "exclude_immediate":
        return not 0x6C <= value <= 0x6F
    raise ValueError(f"unknown constraint kind {constraint.kind}")


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
    return (
        "success",
        {
            "compact_form": compact.name,
            "descriptor_form": descriptor_form.name if descriptor_form else "",
            "descriptor": descriptor,
            "payload": payload,
            "payload_width": compact.payload_width,
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
    field_symbol: dict[str, str]
    field_kind: dict[str, str]
    operand_name: dict[str, str]
    operand_type: dict[str, str]
    access: dict[str, str]
    domain: dict[str, str]
    ea_role: dict[str, str]
    ea_width: dict[str, str]
    fixed_identity: dict[str, str]
    overlap_rule: dict[str, str]
    observed_kind: dict[str, str]
    ea_form: dict[str, str]
    ea_kind: dict[str, str]
    ea_family: dict[str, str]
    ea_payload: dict[str, str]
    ea_payload_kind: dict[str, str]
    ea_field_symbol: dict[str, str]
    ea_field_role: dict[str, str]
    ea_segment: dict[str, str]
    ea_base: dict[str, str]
    ea_register: dict[str, str]
    update_target: dict[str, str]
    update_mode: dict[str, str]


@dataclass(frozen=True)
class PublicLayout:
    size_order: tuple[str, ...]
    touched_flag_order: tuple[str, ...]
    possible_event_order: tuple[str, ...]
    ea_field_slots: int


def derive_public_layout(ir: decode_ir.DecodeIR) -> PublicLayout:
    """Derive public mask orders and the combined EA field bound from live IR."""
    families = {
        family.name: family
        for family in ir.effective_addresses.descriptor_families
    }
    ea_field_counts = []
    for compact in ir.effective_addresses.compact_forms:
        if compact.referenced_descriptor_family:
            ea_field_counts.extend(
                len(compact.fields) + len(descriptor.fields)
                for descriptor in families[compact.referenced_descriptor_family].forms
            )
        else:
            ea_field_counts.append(len(compact.fields))
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
        ea_field_slots=max(ea_field_counts, default=0),
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
    field_symbol = add("field_symbol_e", "FIELD_SYMBOL", _ordered(x.symbol for f in forms for x in f.fields))
    field_kind = add("field_kind_e", "FIELD_KIND", _ordered(x.kind for f in forms for x in f.fields))
    operand_name = add("operand_name_e", "OPERAND_NAME", _ordered(x.name for f in forms for x in f.operands))
    operand_type = add("operand_type_e", "OPERAND_TYPE", _ordered(x.type_name for f in forms for x in f.operands))
    access = add("operand_access_e", "ACCESS", _ordered(x.access for f in forms for x in f.operands))
    domain = add("operand_domain_e", "DOMAIN", _ordered(x.domain for f in forms for x in f.operands))
    ea_role = add("operand_ea_role_e", "EA_ROLE", _ordered(x.ea_role for f in forms for x in f.operands))
    ea_width = add("operand_ea_width_e", "EA_WIDTH", _ordered(x.ea_width for f in forms for x in f.operands))
    fixed_identity = add(
        "fixed_identity_e",
        "FIXED_IDENTITY",
        _ordered(
            x.source.identity
            for f in forms
            for x in f.operands
            if isinstance(x.source, decode_ir.FixedSourceIR)
        ),
    )
    overlap_rule = add("overlap_rule_e", "OVERLAP", _ordered(x.rule for f in forms for x in f.overlaps))
    observed_kind = add("repeat_observed_e", "REPEAT_OBSERVED", _ordered(f.control.repeat.observed_kind for f in forms))
    ea_form = add("ea_form_e", "EA_FORM", _ordered(x.name for x in ea_forms))
    ea_kind = add("ea_kind_e", "EA_KIND", _ordered(x.kind for x in ea_forms))
    ea_family = add(
        "ea_descriptor_family_e",
        "EA_DESCRIPTOR_FAMILY",
        _ordered(
            {""}
            | {
                family.name
                for family in ir.effective_addresses.descriptor_families
            }
        ),
    )
    ea_payload = add(
        "ea_payload_e",
        "EA_PAYLOAD",
        _ordered({""} | {x.name for x in ir.effective_addresses.payloads}),
    )
    ea_payload_kind = add("ea_payload_kind_e", "EA_PAYLOAD_KIND", _ordered(x.kind for x in ir.effective_addresses.payloads))
    ea_field_symbol = add("ea_field_symbol_e", "EA_FIELD_SYMBOL", _ordered(x.symbol for f in ea_forms for x in f.fields))
    ea_field_role = add("ea_field_role_e", "EA_FIELD_ROLE", _ordered(x.role for f in ea_forms for x in f.fields))
    ea_segment = add("ea_segment_e", "EA_SEGMENT", _ordered(x.segment for x in ea_forms))
    ea_base = add("ea_base_e", "EA_BASE", _ordered(x.base for x in ea_forms))
    ea_register = add("ea_register_e", "EA_REGISTER", _ordered(x.register_name for x in ea_forms))
    update_target = add("ea_update_target_e", "EA_UPDATE_TARGET", _ordered(x.update_target for x in ea_forms))
    update_mode = add("ea_update_mode_e", "EA_UPDATE_MODE", _ordered(x.update_mode for x in ea_forms))
    names = Names(
        opcode_class, form, operation, route, instruction_set, instruction_class,
        privilege, predicate, field_symbol, field_kind, operand_name, operand_type,
        access, domain, ea_role, ea_width, fixed_identity, overlap_rule,
        observed_kind, ea_form, ea_kind, ea_family, ea_payload, ea_payload_kind,
        ea_field_symbol, ea_field_role, ea_segment, ea_base, ea_register,
        update_target, update_mode,
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

  typedef enum logic [2:0] {
    OPERAND_SOURCE_INVALID = 3'd0,
    OPERAND_SOURCE_ENCODED_FIELD = 3'd1,
    OPERAND_SOURCE_FIXED = 3'd2,
    OPERAND_SOURCE_APPENDED_PAYLOAD = 3'd3,
    OPERAND_SOURCE_EFFECTIVE_ADDRESS = 3'd4
  } operand_source_e;""",
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
  localparam logic [9:0] BEDROCK_FIELD_SLOTS = 10'd{ir.limits.max_fields};
  localparam logic [9:0] BEDROCK_OPERAND_SLOTS = 10'd{ir.limits.max_operands};
  localparam logic [9:0] BEDROCK_EA_SLOTS = 10'd{ir.limits.max_ea_operands};
  localparam logic [9:0] BEDROCK_EA_FIELD_SLOTS = 10'd{public_layout.ea_field_slots};
  localparam logic [9:0] BEDROCK_SIZE_MASK_BITS = 10'd{len(public_layout.size_order)};
  localparam logic [9:0] BEDROCK_TOUCHED_FLAG_MASK_BITS = 10'd{len(public_layout.touched_flag_order)};
  localparam logic [9:0] BEDROCK_POSSIBLE_EVENT_MASK_BITS = 10'd{len(public_layout.possible_event_order)};

{mask_constants}

  {enum_text}

  typedef struct packed {{
    d0_status_e status;
    opcode_class_e opcode_class;
    form_id_e form;
    logic [BEDROCK_OPCODE_BITS-1:0] opcode;
  }} d0_result_t;

  typedef struct packed {{
    logic valid;
    field_symbol_e symbol;
    field_kind_e kind;
    logic [6:0] width;
    logic [63:0] value;
  }} decoded_field_t;

  typedef struct packed {{
    logic valid;
    ea_field_symbol_e symbol;
    ea_field_role_e role;
    logic [6:0] width;
    logic [63:0] value;
  }} decoded_ea_field_t;

  typedef struct packed {{
    logic valid;
    operand_name_e name;
    operand_type_e type_name;
    operand_access_e access;
    operand_domain_e domain;
    operand_ea_role_e ea_role;
    operand_ea_width_e ea_width;
    operand_source_e source;
    fixed_identity_e fixed_identity;
    logic [6:0] width;
    logic [63:0] value;
    logic payload_signed;
    logic statically_legal;
    logic ea_valid;
    logic [0:0] ea_slot;
  }} decoded_operand_t;

  typedef struct packed {{
    logic valid;
    ea_form_e compact_form;
    ea_form_e descriptor_form;
    ea_kind_e kind;
    ea_descriptor_family_e descriptor_family;
    ea_segment_e segment;
    ea_base_e base;
    ea_register_e register_name;
    operand_ea_width_e operand_width;
    ea_payload_e payload_name;
    ea_payload_kind_e payload_kind;
    ea_update_target_e update_target;
    ea_update_mode_e update_mode;
    logic [6:0] raw;
    logic [1:0] descriptor_bytes;
    logic [15:0] descriptor;
    logic [2:0] field_count;
    decoded_ea_field_t [BEDROCK_EA_FIELD_SLOTS-1:0] fields;
    logic [63:0] payload;
    logic [6:0] payload_width;
    logic payload_signed;
    logic base_field_valid;
    logic [3:0] base_register;
    logic index_field_valid;
    logic [3:0] index_register;
    logic segment_field_valid;
    logic [3:0] segment_register;
    logic [5:0] consumed_bytes;
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
    decode_stage_e stage;
    d0_status_e d0_status;
    opcode_class_e opcode_class;
    form_id_e form;
    operation_e operation;
    logic [BEDROCK_OPCODE_BITS-1:0] opcode;
    control_metadata_t control;
    logic [BEDROCK_SIZE_MASK_BITS-1:0] size_mask;
    logic [3:0] field_count;
    decoded_field_t [BEDROCK_FIELD_SLOTS-1:0] fields;
    logic [2:0] operand_count;
    decoded_operand_t [BEDROCK_OPERAND_SLOTS-1:0] operands;
    logic [1:0] ea_count;
    decoded_ea_t [BEDROCK_EA_SLOTS-1:0] eas;
    overlap_descriptor_t overlap;
    logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] touched_flag_mask;
    logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] possible_event_mask;
    logic [5:0] required_bytes;
    logic [4:0] encoded_bytes;
  }} d1_result_t;

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
    if constraint.kind == "exclude_rn_direct":
        return f"!({gathered} <= {_hex(width, 0x0F)})"
    if constraint.kind == "exclude_reg_direct":
        return f"!(({gathered} <= {_hex(width, 0x0F)}) || ({gathered} == {_hex(width, 0x68)}))"
    if constraint.kind == "exclude_immediate":
        return f"!(({gathered} >= {_hex(width, 0x6C)}) && ({gathered} <= {_hex(width, 0x6F)}))"
    raise ValueError(f"unknown constraint kind {constraint.kind}")


def _constraint_signal(form_index: int, constraint_index: int) -> str:
    return f"form_{form_index:03d}_constraint_{constraint_index}_value"


def _render_d0(ir: decode_ir.DecodeIR, names: Names) -> str:
    by_class: dict[str, list[decode_ir.FormIR]] = {}
    for form in ir.forms:
        by_class.setdefault(form.opcode_class, []).append(form)
    constraint_declarations: list[str] = []
    constraint_assignments: list[str] = []
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
    class_cases = []
    for opcode_class in sorted(by_class):
        lines = [f"      {names.opcode_class[opcode_class]}: begin"]
        for form in by_class[opcode_class]:
            raw = f"((opcode_i & {_hex(34, form.opcode_mask)}) == {_hex(34, form.opcode_value)})"
            predicates = [
                _constraint_sv(
                    constraint,
                    _constraint_signal(form.index, constraint_index),
                )
                for constraint_index, constraint in enumerate(form.constraints)
            ]
            lines.extend(
                [
                    f"        // form {form.index}: {form.key}",
                    f"        if ({raw}) begin",
                    "          raw_match = 1'b1;",
                ]
            )
            if predicates:
                lines.extend(["          if (", "            !selected &&"])
                for predicate_index, predicate in enumerate(predicates):
                    suffix = " &&" if predicate_index + 1 < len(predicates) else ""
                    lines.append(f"            {predicate}{suffix}")
                lines.append("          ) begin")
            else:
                lines.append("          if (!selected) begin")
            lines.extend(
                [
                    "            selected = 1'b1;",
                    f"            result_o.form = {names.form[form.key]};",
                    "          end",
                    "        end",
                ]
            )
        lines.append("      end")
        class_cases.append("\n".join(lines))
    return f"""// Generated from canonical Decode IR. Do not edit.
module bedrock_decode_d0
  import bedrock_decode_pkg::*;
(
  input  logic valid_i,
  input  opcode_class_e opcode_class_i,
  input  logic [BEDROCK_OPCODE_BITS-1:0] opcode_i,
  output d0_result_t result_o
);
  logic raw_match;
  logic selected;
{chr(10).join(constraint_declarations)}

{chr(10).join(constraint_assignments)}

  always_comb begin
    result_o = '0;
    result_o.status = D0_INVALID_INPUT;
    result_o.opcode_class = opcode_class_i;
    result_o.opcode = opcode_i;
    raw_match = 1'b0;
    selected = 1'b0;
    if (valid_i) begin
      result_o.status = D0_UNALLOCATED_OPCODE;
      unique case (opcode_class_i)
{chr(10).join(class_cases)}
        default: begin end
      endcase
      if (selected)
        result_o.status = D0_SUCCESS;
      else if (raw_match)
        result_o.status = D0_CONSTRAINT_REJECTED;
    end
  end
endmodule
"""


def _ea_static_assignments(
    target: str,
    form: decode_ir.EaFormIR,
    names: Names,
    *,
    field_offset: int,
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
    for offset, field in enumerate(form.fields, field_offset):
        value = _gather(raw_signal, field.positions)
        lines.extend(
            [
                f"{target}.fields[{offset}].valid = 1'b1;",
                f"{target}.fields[{offset}].symbol = {names.ea_field_symbol[field.symbol]};",
                f"{target}.fields[{offset}].role = {names.ea_field_role[field.role]};",
                f"{target}.fields[{offset}].width = 7'd{field.width};",
                f"{target}.fields[{offset}].value = 64'({value});",
            ]
        )
        if field.role == "base":
            lines.extend([f"{target}.base_field_valid = 1'b1;", f"{target}.base_register = 4'({value});"])
        elif field.role == "index":
            lines.extend([f"{target}.index_field_valid = 1'b1;", f"{target}.index_register = 4'({value});"])
        elif field.role == "segment":
            lines.extend([f"{target}.segment_field_valid = 1'b1;", f"{target}.segment_register = 4'({value});"])
    lines.append(f"{target}.field_count = 3'd{field_offset + len(form.fields)};")
    return lines


def _indent(lines: Iterable[str], spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line for line in lines)


def _render_ea_function(ir: decode_ir.DecodeIR, names: Names) -> str:
    payloads = {item.name: item for item in ir.effective_addresses.payloads}
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
                f"        parse_one_ea.ea.compact_form = {names.ea_form[compact.name]};",
                f"        parse_one_ea.ea.descriptor_family = {names.ea_family[compact.referenced_descriptor_family]};",
                f"        parse_one_ea.ea.payload_name = {names.ea_payload[compact.payload_name]};",
                f"        parse_one_ea.ea.payload_kind = {names.ea_payload_kind[payloads[compact.payload_name].kind] if compact.payload_name else 'EA_PAYLOAD_KIND_INVALID'};",
                f"        parse_one_ea.ea.payload_width = 7'd{compact.payload_width};",
                f"        parse_one_ea.ea.payload_signed = 1'b{int(compact.payload_signed)};",
                f"        parse_one_ea.ea.descriptor_bytes = 2'd{compact.descriptor_bytes};",
            ]
        )
        lines.extend("        " + x for x in _ea_static_assignments("parse_one_ea.ea", compact, names, field_offset=0, raw_signal="compact_raw"))
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
            lines.extend(["          parse_one_ea.ea.descriptor = descriptor;", "          descriptor_match = 1'b0;"])
            for descriptor_form in family.forms:
                lines.extend(
                    [
                        f"          if (!descriptor_match && ((descriptor & {_hex(16, descriptor_form.mask)}) == {_hex(16, descriptor_form.value)})) begin // {descriptor_form.name}",
                        "            descriptor_match = 1'b1;",
                        f"            parse_one_ea.ea.descriptor_form = {names.ea_form[descriptor_form.name]};",
                    ]
                )
                lines.extend("            " + x for x in _ea_static_assignments("parse_one_ea.ea", descriptor_form, names, field_offset=len(compact.fields), raw_signal="descriptor"))
                lines.append("          end")
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
                "        parse_one_ea.ea.consumed_bytes = cursor[5:0] - cursor_in;",
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
      parse_one_ea.ea.raw = compact_raw;
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


def _source_enum(source: decode_ir.OperandSourceIR) -> str:
    if isinstance(source, decode_ir.EncodedFieldSourceIR):
        return "OPERAND_SOURCE_ENCODED_FIELD"
    if isinstance(source, decode_ir.FixedSourceIR):
        return "OPERAND_SOURCE_FIXED"
    if isinstance(source, decode_ir.AppendedPayloadSourceIR):
        return "OPERAND_SOURCE_APPENDED_PAYLOAD"
    if isinstance(source, decode_ir.EffectiveAddressSourceIR):
        return "OPERAND_SOURCE_EFFECTIVE_ADDRESS"
    raise TypeError(source)


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
            f"        result_o.field_count = 4'd{len(form.fields)};",
            f"        result_o.operand_count = 3'd{len(form.operands)};",
            f"        result_o.ea_count = 2'd{sum(isinstance(x.source, decode_ir.EffectiveAddressSourceIR) for x in form.operands)};",
            f"        cursor = 6'd{form.opcode_bytes};",
        ]
    )
    observed_slot = next((i for i, x in enumerate(form.operands) if x.name == form.control.repeat.observed_operand), 0)
    lines.append(f"        result_o.control.repeat_observed_operand = 2'd{observed_slot};")
    field_slots = {field.symbol: slot for slot, field in enumerate(form.fields)}
    for slot, field in enumerate(form.fields):
        lines.extend(
            [
                f"        result_o.fields[{slot}].valid = 1'b1;",
                f"        result_o.fields[{slot}].symbol = {names.field_symbol[field.symbol]};",
                f"        result_o.fields[{slot}].kind = {names.field_kind[field.kind]};",
                f"        result_o.fields[{slot}].width = 7'd{field.width};",
                f"        result_o.fields[{slot}].value = 64'({_gather('d0_i.opcode', field.positions)});",
            ]
        )
    ea_slot = 0
    for slot, operand in enumerate(form.operands):
        source = operand.source
        lines.extend(
            [
                f"        result_o.operands[{slot}].valid = 1'b1;",
                f"        result_o.operands[{slot}].name = {names.operand_name[operand.name]};",
                f"        result_o.operands[{slot}].type_name = {names.operand_type[operand.type_name]};",
                f"        result_o.operands[{slot}].access = {names.access[operand.access]};",
                f"        result_o.operands[{slot}].domain = {names.domain[operand.domain]};",
                f"        result_o.operands[{slot}].ea_role = {names.ea_role[operand.ea_role]};",
                f"        result_o.operands[{slot}].ea_width = {names.ea_width[operand.ea_width]};",
                f"        result_o.operands[{slot}].source = {_source_enum(source)};",
                f"        result_o.operands[{slot}].width = 7'd{operand.type_width};",
                f"        result_o.operands[{slot}].payload_signed = 1'b{int(isinstance(source, decode_ir.AppendedPayloadSourceIR) and source.signed)};",
                f"        result_o.operands[{slot}].statically_legal = 1'b1;",
            ]
        )
        if isinstance(source, (decode_ir.EncodedFieldSourceIR, decode_ir.EffectiveAddressSourceIR)):
            lines.append(f"        result_o.operands[{slot}].value = result_o.fields[{field_slots[source.field_symbol]}].value;")
        elif isinstance(source, decode_ir.FixedSourceIR):
            lines.extend(
                [
                    f"        result_o.operands[{slot}].fixed_identity = {names.fixed_identity[source.identity]};",
                    f"        result_o.operands[{slot}].value = 64'h{(source.value or 0):016x};",
                ]
            )
        if isinstance(source, decode_ir.EffectiveAddressSourceIR):
            lines.extend(
                [
                    f"        result_o.operands[{slot}].ea_valid = 1'b1;",
                    f"        result_o.operands[{slot}].ea_slot = 1'd{ea_slot};",
                ]
            )
            ea_slot += 1
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
    ea_slot = 0
    operand_slots = {operand.name: index for index, operand in enumerate(form.operands)}
    for layout in form.layout:
        slot = operand_slots[layout.operand_name]
        if isinstance(layout, decode_ir.ParseEaIR):
            lines.extend(
                [
                    "        if (!layout_failed) begin",
                    f"          ea_parse = parse_one_ea(result_o.operands[{slot}].value[6:0], result_o.operands[{slot}].ea_width, record_i, byte_count_i, cursor);",
                    "          cursor = ea_parse.next_cursor;",
                    "          if (!ea_parse.ok) begin",
                    "            layout_failed = 1'b1;",
                    "            result_o.stage = ea_parse.stage;",
                    "          end else begin",
                    f"            result_o.eas[{ea_slot}] = ea_parse.ea;",
                    "          end",
                    "        end",
                ]
            )
            ea_slot += 1
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
                    f"          result_o.operands[{slot}].statically_legal = 1'b0;",
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
  output d1_result_t result_o
);
  integer unsigned cursor;
  logic layout_failed;
  ea_parse_result_t ea_parse;

{_render_ea_function(ir, names)}

  always_comb begin
    result_o = '0;
    result_o.stage = D1_STAGE_D0_REJECTED;
    result_o.d0_status = d0_i.status;
    result_o.opcode_class = d0_i.opcode_class;
    result_o.form = d0_i.form;
    result_o.opcode = d0_i.opcode;
    result_o.encoded_bytes = byte_count_i;
    cursor = 0;
    layout_failed = 1'b0;
    ea_parse = '0;
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


def render_outputs(build_dir: Path) -> dict[Path, str]:
    ir = decode_ir.load_decode_ir(ROOT / "isa" / "defs")
    package, names = _render_package(ir)
    return {
        build_dir / OUTPUT_NAMES[0]: package,
        build_dir / OUTPUT_NAMES[1]: _render_d0(ir, names),
        build_dir / OUTPUT_NAMES[2]: _render_d1(ir, names),
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
