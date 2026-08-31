"""Render executable instruction and effective-address Sail catalogs."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from ..composition import SailProgram
from ..encoding import EncodingForm, FieldBinding, PayloadBinding
from ..encoding_architecture import ENCODING_CLASSES_BY_WIDTH
from ..instruction_metasyntax import InstructionMetasyntaxOperand
from ..project import InstructionBundle
from ..reference import Reference
from ..type_system import FieldType, FieldTypeKind, PayloadType, PayloadTypeKind
from .sail_registry import ROUTE_CONSTRUCTORS, instruction_set_constructor


CLASS_CONSTRUCTORS = {
    "extrashort": "ExtraShort",
    "short": "Short",
    "medium": "Medium",
    "long": "Long",
    "extralong": "ExtraLong",
    "xxlong": "Xxlong",
}
ACCESS_CONSTRUCTORS = {
    "read": "AccessRead",
    "write": "AccessWrite",
    "read_write": "AccessReadWrite",
    "address": "AccessAddress",
}
PREDICATE_CONSTRUCTORS = {
    "MOVcc": "AnnulOnFalse",
    "FMOVcc": "AnnulOnFalse",
    "Jcc": "AnnulOnFalse",
    "CMPJcc": "Temporary",
    "TESTJcc": "Temporary",
    "IJcc": "CounterAndCondition",
    "DJcc": "CounterAndCondition",
    "REPcc": "CounterAndCondition",
    "SETcc": "WriteBoolean",
}
MAX_RECORD_BYTES = 18


def _constructor(prefix: str, value: str) -> str:
    suffix = re.sub(r"[^A-Za-z0-9_]", "_", value)
    if not suffix or suffix[0].isdigit():
        suffix = "N" + suffix
    return prefix + suffix


def _list(items: Iterable[str]) -> str:
    return "[|" + ", ".join(items) + "|]"


def _option(value: str | None, prefix: str) -> str:
    return "None()" if value is None else f"Some({_constructor(prefix, value)})"


def _positions(code: str, marker: str) -> tuple[int, ...]:
    width = len(code)
    return tuple(width - index - 1 for index, item in enumerate(code) if item == marker)


def _form_key(bundle: InstructionBundle, form: EncodingForm) -> str:
    owner = ENCODING_CLASSES_BY_WIDTH[form.pattern.bit_width]
    return f"{owner.name}.{bundle.instruction.mnemonic.lower()}.{form.id}"


def _field_type_name(definition: FieldType) -> str:
    name = definition.id
    semantic_names = {
        "CC": "condition",
        "PTLVL": "pt_level",
        "FLBMP": "flags_bitmap",
        "MORDER": "memory_order",
    }
    if name in semantic_names:
        return semantic_names[name]
    if name.startswith("SIZE_"):
        return "size_" + name.removeprefix("SIZE_")
    if name.startswith("IMM"):
        return name.lower()
    return name


def _payload_type_name(definition: PayloadType) -> str:
    name = definition.id
    if definition.kind in {
        PayloadTypeKind.IMMEDIATE,
        PayloadTypeKind.PC_DISPLACEMENT,
        PayloadTypeKind.PC_ABSOLUTE,
        PayloadTypeKind.REGISTER_SELECTOR,
    }:
        if name == "FCONST":
            return "fconst_id"
        signed = definition.signed is True or name.endswith("S")
        return f"imm{definition.bytes * 8}{'s' if signed else ''}"
    return name.lower()


def _field_kind(definition: FieldType) -> str:
    if definition.kind == FieldTypeKind.EFFECTIVE_ADDRESS:
        return "FieldEa"
    if definition.kind == FieldTypeKind.ENUM_CONDITION:
        return "FieldCondition"
    if definition.kind == FieldTypeKind.SIZE_SELECTOR:
        return "FieldSize"
    if definition.kind in {
        FieldTypeKind.IMMEDIATE,
        FieldTypeKind.PAGE_TABLE_LEVEL,
        FieldTypeKind.MEMORY_ORDER,
    }:
        return "FieldImmediate"
    if definition.kind in {
        FieldTypeKind.REGISTER_SELECTOR,
        FieldTypeKind.REGISTER_PAIR_SELECTOR,
    }:
        assert definition.register_group is not None
        return "FieldFreg" if definition.register_group.element == "FPR" else "FieldRn"
    return "FieldBits"


def _constraint_values(values: tuple[int | str, ...]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for value in values:
        if isinstance(value, int):
            ranges.append((value, value))
            continue
        text = value.replace("_", "")
        if ".." in text:
            lower, upper = text.split("..", 1)
            ranges.append((int(lower, 0), int(upper, 0)))
        elif text == "immediate":
            # Symbolic exclusions are represented by the constraint kind.
            continue
        else:
            parsed = int(text, 0)
            ranges.append((parsed, parsed))
    return ranges


def _constraint_lower(value: int | str) -> int:
    if isinstance(value, int):
        return value
    text = value.replace("_", "")
    return int(text.split("..", 1)[0], 0)


def _insert_field(pattern: str, marker: str, payload: int, value: int) -> int:
    positions = _positions(pattern, marker)
    for value_bit, position in zip(
        range(len(positions) - 1, -1, -1), positions, strict=True
    ):
        if (value >> value_bit) & 1:
            payload |= 1 << position
        else:
            payload &= ~(1 << position)
    return payload


def _representative_record(program: SailProgram, form: EncodingForm) -> tuple[int, ...]:
    encoding_class = ENCODING_CLASSES_BY_WIDTH[form.pattern.bit_width]
    value = form.pattern.fixed_value
    for constraint in form.constraints:
        field = form.field_for_role(constraint.role)
        assert field is not None
        selected = _constraint_lower(constraint.allow[0]) if constraint.allow else 0x10
        value = _insert_field(form.pattern.code, field.marker, value, selected)

    appended_bytes = sum(
        program.project.types.payload_types.resolve(payload.type).bytes
        for payload in form.payloads
    )
    total = encoding_class.opcode_space_bytes + appended_bytes
    if encoding_class.opcode_space_bytes == 1:
        record = [value]
    elif encoding_class.opcode_space_bytes == 2:
        framed = (0b10 << 14) | value
        record = [(framed >> 8) & 0xFF, framed & 0xFF]
    else:
        if total > MAX_RECORD_BYTES:
            raise ValueError(
                f"representative record requires {total} bytes; maximum is {MAX_RECORD_BYTES}"
            )
        record = [
            0b11000000
            | ((total - 3) << 2)
            | ((value >> ((encoding_class.opcode_space_bytes - 1) * 8)) & 0x3)
        ]
        record.extend(
            (value >> shift) & 0xFF
            for shift in range(
                (encoding_class.opcode_space_bytes - 2) * 8, -1, -8
            )
        )
    record.extend([0] * appended_bytes)
    return tuple(record)


def _render_constraint(form: EncodingForm, constraint) -> str:
    field = form.field_for_role(constraint.role)
    assert field is not None
    values = constraint.allow or constraint.exclude
    kind = "AllowRanges" if constraint.allow else "ExcludeImmediate"
    ranges = _list(
        f"struct {{ lower = {lower}, upper = {upper} }}"
        for lower, upper in _constraint_values(values)
    )
    positions = _list(map(str, _positions(form.pattern.code, field.marker)))
    return (
        f"struct {{ field_positions = {positions}, kind = {kind}, "
        f"ranges = {ranges}, reason = {json.dumps(constraint.reason)} }}"
    )


def _render_field(program: SailProgram, form: EncodingForm, field: FieldBinding) -> str:
    definition = program.project.types.field_types.resolve(field.type)
    positions = _list(map(str, _positions(form.pattern.code, field.marker)))
    return (
        f"struct {{ symbol = {_constructor('Field_', field.marker)}, "
        f"operand_type = {_constructor('OperandType_', _field_type_name(definition))}, "
        f"kind = {_field_kind(definition)}, positions = {positions} }}"
    )


@dataclass(frozen=True, slots=True)
class _OperandRepresentation:
    name: str
    type_name: str
    access: str
    field: FieldBinding | None = None
    payload: PayloadBinding | None = None
    fixed_name: str | None = None
    fixed_value: int | None = None


@dataclass(frozen=True, slots=True)
class SailOperandBindingProjection:
    """One logical operand bound to a field, payload, or fixed syntax value."""

    name: str
    type_name: str
    access: str
    field_marker: str | None
    payload_type: Reference[PayloadType] | None
    fixed_name: str | None
    fixed_value: int | None
    ea_profile: str | None


@dataclass(frozen=True, slots=True)
class SailFormProjection:
    """One selected instruction form lowered into the Sail decode catalog."""

    key: str
    operation: str
    owner: str
    route: str
    bundle: InstructionBundle
    form: EncodingForm
    operands: tuple[SailOperandBindingProjection, ...]
    representative_record: tuple[int, ...]


def _fixed_syntax_representations(
    bundle: InstructionBundle, form: EncodingForm
) -> dict[str, InstructionMetasyntaxOperand]:
    """Bind fixed syntax operands to logical roles used by this form.

    Field and payload bindings already identify their roles explicitly.  A
    literal such as ``8`` or a fixed register such as ``SP`` does not, so use
    its syntax position and the authored source/destination role instead of
    depending on mapping order in ``instruction.yaml``.
    """

    logical: Mapping[str, Mapping[str, object]] = bundle.instruction["operands"]
    used_roles = {
        *(field.role for field in form.fields),
        *(payload.role for payload in form.payloads),
    }
    result: dict[str, InstructionMetasyntaxOperand] = {}
    displayed = form.syntax.displayed_operands
    for index, item in enumerate(displayed):
        if item.kind == "decimal":
            preferred_role = "source"
        elif item.kind == "reference" and item.name in {"SP", "CS"}:
            preferred_role = (
                "destination" if index + 1 == len(displayed) else "source"
            )
        else:
            continue

        candidates = [name for name in logical if name not in used_roles]
        role: str | None
        if item.kind == "decimal" and "imm" in candidates:
            role = "imm"
        else:
            role = next(
                (
                    name
                    for name in candidates
                    if logical[name]["role"] == preferred_role
                ),
                candidates[0] if candidates else None,
            )
        if role is not None:
            result[role] = item
            used_roles.add(role)
    return result


def _operand_representations(
    program: SailProgram, bundle: InstructionBundle, form: EncodingForm
) -> tuple[_OperandRepresentation, ...]:
    logical: Mapping[str, Mapping[str, object]] = bundle.instruction["operands"]
    fixed_by_role = _fixed_syntax_representations(bundle, form)
    rendered: list[_OperandRepresentation] = []
    for name, metadata in logical.items():
        field = form.field_for_role(name)
        payload = next((item for item in form.payloads if item.role == name), None)
        if field is not None:
            field_definition = program.project.types.field_types.resolve(field.type)
            type_name = _field_type_name(field_definition)
            binding_access = field.access
        elif payload is not None:
            payload_definition = program.project.types.payload_types.resolve(
                payload.type
            )
            type_name = _payload_type_name(payload_definition)
            binding_access = payload.access
        else:
            syntax = fixed_by_role.get(name)
            if syntax is None:
                continue
            fixed_name = syntax.name if syntax is not None else None
            fixed_value = syntax.literal if syntax is not None else None
            type_name = fixed_name if fixed_name in {"SP", "CS"} else "imm"
            rendered.append(
                _OperandRepresentation(
                    name,
                    type_name,
                    str(metadata["access"]),
                    fixed_name=fixed_name,
                    fixed_value=fixed_value,
                )
            )
            continue
        rendered.append(
            _OperandRepresentation(
                name,
                type_name,
                str(binding_access or metadata["access"]),
                field=field,
                payload=payload,
            )
        )
    return tuple(rendered)


def _ea_metadata(
    program: SailProgram,
    bundle: InstructionBundle,
    form: EncodingForm,
    operand: _OperandRepresentation,
) -> tuple[str, str, str]:
    if operand.field is None:
        return "None()", "None()", "None()"
    definition = program.project.types.field_types.resolve(operand.field.type)
    if definition.kind != FieldTypeKind.EFFECTIVE_ADDRESS:
        return "None()", "None()", "None()"
    logical = bundle.instruction["operands"][operand.name]
    role = str(logical["role"])
    ea_role = {
        "address": "address",
        "control_target": "control_target",
        "bit_index": "index",
        "segment_selector": "segment",
    }.get(role, "value")
    sizes = form.syntax.selected_size_codes or (
        (form.syntax.fixed_size_suffix or "").removeprefix("."),
    )
    width = "operation_size" if any(sizes) else "Q"
    return (
        _option(ea_role, "EaRole_"),
        _option(width, "EaWidth_"),
        _option(definition.profile, "EaProfile_"),
    )


def _render_operand(
    program: SailProgram,
    bundle: InstructionBundle,
    form: EncodingForm,
    operand: _OperandRepresentation,
) -> str:
    field_symbol = "None()"
    positions: tuple[int, ...] = ()
    if operand.field is not None:
        field_symbol = f"Some({_constructor('Field_', operand.field.marker)})"
        positions = _positions(form.pattern.code, operand.field.marker)
    logical = bundle.instruction["operands"][operand.name]
    domain = _option(logical.get("domain"), "OperandDomain_")
    ea_role, ea_width, ea_profile = _ea_metadata(program, bundle, form, operand)
    fixed = operand.fixed_value is not None
    return (
        f"struct {{ name = {_constructor('Operand_', operand.name)}, "
        f"operand_type = {_constructor('OperandType_', operand.type_name)}, "
        f"access = {ACCESS_CONSTRUCTORS[operand.access]}, field_symbol = {field_symbol}, "
        f"field_positions = {_list(map(str, positions))}, domain = {domain}, "
        f"ea_role = {ea_role}, ea_width = {ea_width}, ea_profile = {ea_profile}, "
        f"has_fixed_value = {str(fixed).lower()}, fixed_value = {operand.fixed_value or 0}, "
        "legal_values = [||] }"
    )


def _render_payload(
    program: SailProgram,
    payload: PayloadBinding,
    operands: Mapping[str, _OperandRepresentation],
) -> str:
    definition = program.project.types.payload_types.resolve(payload.type)
    operand = operands[payload.role]
    signed = definition.signed is True or definition.id.endswith("S")
    return (
        f"struct {{ operand_name = {_constructor('Operand_', payload.role)}, "
        f"operand_type = {_constructor('OperandType_', operand.type_name)}, "
        f"width = {definition.bytes * 8}, signed = {str(signed).lower()} }}"
    )


def _cpuid_constructor(field) -> str:
    return _constructor("CpuidFlag_", field.id)


def _render_entry(program: SailProgram, bundle: InstructionBundle, form: EncodingForm) -> str:
    encoding_class = ENCODING_CLASSES_BY_WIDTH[form.pattern.bit_width]
    representations = _operand_representations(program, bundle, form)
    by_name = {item.name: item for item in representations}
    sizes = form.syntax.selected_size_codes
    if not sizes and form.syntax.fixed_size_suffix:
        sizes = (form.syntax.fixed_size_suffix.removeprefix("."),)
    required = _list(
        _cpuid_constructor(item) for item in bundle.required_cpuid_flags_for(form)
    )
    repeat = bundle.instruction.to_dict().get("repeat")
    repeat_rep = repeat is not None
    repeat_repcc = repeat is not None and repeat["type"] == "repcc"
    return (
        f"  struct {{ form_id = {_constructor('Form_', _form_key(bundle, form))}, "
        f"operation = Op_{bundle.instruction.mnemonic}, "
        f"route = {ROUTE_CONSTRUCTORS[bundle.instruction.route]}, "
        f"instruction_set = {instruction_set_constructor(program, bundle.owner)}, "
        f"privilege = {'SupervisorPrivilege' if bundle.instruction.privileged else 'UserPrivilege'}, "
        f"predicate_mode = {PREDICATE_CONSTRUCTORS.get(bundle.instruction.mnemonic, 'PredicateNone')}, "
        f"repeat_rep = {str(repeat_rep).lower()}, repeat_repcc = {str(repeat_repcc).lower()}, "
        f"encoding_class = {CLASS_CONSTRUCTORS[encoding_class.name]}, "
        f"value = 0x{form.pattern.fixed_value:016X}, mask = 0x{form.pattern.fixed_mask:016X}, "
        f"constraints = {_list(_render_constraint(form, item) for item in form.constraints)}, "
        f"fields = {_list(_render_field(program, form, item) for item in form.fields)}, "
        f"operands = {_list(_render_operand(program, bundle, form, item) for item in representations)}, "
        f"sizes = {_list(_constructor('Size_', item) for item in sizes)}, "
        f"appended_payloads = {_list(_render_payload(program, item, by_name) for item in form.payloads)}, "
        f"required_cpuid_flags = {required} }}"
    )


@dataclass(frozen=True, slots=True)
class SailEaFormProjection:
    name: str
    profile: str | None
    family: str | None
    descriptor_bytes: int
    patterns: tuple[str, ...]
    kind: str
    fields: Mapping[str, Mapping[str, str]]
    field_types: Mapping[str, Reference[FieldType]]
    segment: str | None
    payload_width: int
    payload_signed: bool
    base: str | None
    descriptor: str | None
    update_target: str | None
    update_mode: str | None
    update_difference: str | None


def _payload_suffix(definition: PayloadType) -> str:
    signed = definition.signed is True or definition.id.endswith("S")
    return f"{definition.bytes * 8}{'s' if signed else ''}"


def _compact_name(mode_id: str, definition: PayloadType | None) -> str:
    suffix = _payload_suffix(definition) if definition is not None else ""
    if mode_id == "register":
        return "register_indirect" if not suffix else f"register_disp{suffix}"
    if mode_id in {"stack_pointer_displaced", "program_counter_displaced"}:
        return mode_id.removesuffix("_displaced") + f"_disp{suffix}"
    if mode_id == "absolute":
        return f"absolute_{suffix}"
    if mode_id == "immediate":
        identity = (
            definition.id.lower().removeprefix("imm")
            if definition is not None
            else ""
        )
        return "immediate" if not identity else f"immediate_{identity}"
    return mode_id if not suffix else f"{mode_id}_disp{suffix}"


def _mode_segment(mode, raw: Mapping[str, object]) -> tuple[str | None, str | None]:
    segment = raw.get("segment")
    if isinstance(segment, Mapping):
        if segment.get("source") == "field":
            return "explicit", None
        register = str(segment.get("register"))
        return register, mode.base_source.value
    if raw.get("kind") == "memory":
        base = mode.base_source.value
        return "default", None if base in {"none", "encoded"} else base
    return None, None


def _ea_variants(program: SailProgram) -> tuple[SailEaFormProjection, ...]:
    variants = []
    for mode in program.project.catalog.ea_modes.values():
        if mode.catalog.owner not in program.configuration.owners:
            continue
        raw = mode.to_dict()
        mode_type = mode.catalog.mode_type
        mode_id = str(raw["id"])
        fields = raw.get("fields", {})
        field_types = {
            marker: mode.field_type_reference(marker) for marker in fields
        }
        segment, base = _mode_segment(mode, raw)
        for encoding_index, encoding in enumerate(raw["encodings"]):
            patterns = encoding["pattern"]
            chunks = (patterns,) if isinstance(patterns, str) else tuple(patterns)
            payloads = encoding.get("payloads", ())
            payload_definition = (
                program.project.types.payload_types.resolve(
                    mode.payload_type_reference(encoding_index, 0)
                )
                if payloads
                else None
            )
            autoupdate = encoding.get("autoupdate")
            update_mode = str(autoupdate["type"]) if autoupdate else None
            update_difference = None
            if autoupdate:
                difference = autoupdate["difference"]
                update_difference = (
                    f"constant_{difference}"
                    if isinstance(difference, int)
                    else str(difference)
                )
            update_role = str(autoupdate["target"]) if autoupdate else None
            update_target = None
            if update_role is not None:
                update_target = next(
                    marker for marker, value in fields.items() if value["role"] == update_role
                )
            if mode_type == "compact":
                name = _compact_name(mode_id, payload_definition)
                descriptor = raw.get("extension", {}).get("id")
                kind = str(raw["kind"])
                variants.append(SailEaFormProjection(
                    name,
                    mode.catalog.profile,
                    None,
                    int(raw.get("extension", {}).get("bytes", 0)),
                    chunks,
                    "escape" if raw["kind"] == "extension" else kind,
                    fields,
                    field_types,
                    segment,
                    payload_definition.bytes * 8 if payload_definition else 0,
                    bool(
                        payload_definition
                        and (
                            payload_definition.signed is True
                            or payload_definition.id.endswith("S")
                        )
                    ),
                    base,
                    str(descriptor).lower() if descriptor else None,
                    update_target,
                    update_mode,
                    update_difference,
                ))
            else:
                name = mode_id + (f"_{update_mode}" if update_mode else "")
                variants.append(
                    SailEaFormProjection(
                        name,
                        mode.catalog.profile,
                        mode_type.lower(),
                        len(chunks),
                        chunks,
                        str(raw["kind"]),
                        fields,
                        field_types,
                        segment,
                        0,
                        False,
                        base,
                        None,
                        update_target,
                        update_mode,
                        update_difference,
                    )
                )
    return tuple(variants)


def _render_ea_variant(program: SailProgram, variant: SailEaFormProjection) -> str:
    patterns = _list(
        f"struct {{ width = {len(code)}, value = 0x{int(''.join('1' if c == '1' else '0' for c in code), 2):04X}, "
        f"mask = 0x{int(''.join('1' if c in '01' else '0' for c in code), 2):04X} }}"
        for code in variant.patterns
    )
    joined = "".join(variant.patterns)
    fields = []
    for marker, raw in variant.fields.items():
        definition = program.project.types.field_types.resolve(variant.field_types[marker])
        fields.append(
            f"struct {{ symbol = {_constructor('Field_', marker)}, "
            f"operand_type = {_constructor('OperandType_', _field_type_name(definition))}, "
            f"role = {_constructor('EaRole_', str(raw['role']))}, "
            f"positions = {_list(map(str, _positions(joined, marker)))} }}"
        )
    return (
        f"  struct {{ name = {_constructor('EaForm_', variant.name)}, "
        f"profile = {_option(variant.profile, 'EaProfile_')}, "
        f"descriptor_family = {_option(variant.family, 'EaDescriptor_')}, "
        f"descriptor_bytes = {variant.descriptor_bytes}, patterns = {patterns}, "
        f"kind = {_constructor('EaKind_', variant.kind)}, fields = {_list(fields)}, "
        f"segment = {_option(variant.segment, 'EaSegment_')}, "
        f"payload_width = {variant.payload_width}, payload_signed = {str(variant.payload_signed).lower()}, "
        f"base = {_option(variant.base, 'EaBase_')}, descriptor = {_option(variant.descriptor, 'EaDescriptor_')}, "
        f"update_target = {_option(variant.update_target, 'EaUpdateTarget_')}, "
        f"update_mode = {_option(variant.update_mode, 'EaUpdateMode_')}, "
        f"update_difference = {_option(variant.update_difference, 'EaUpdateDifference_')} }}"
    )


@dataclass(frozen=True, slots=True)
class SailCatalogProjection:
    """Selected form and effective-address relations consumed by Sail."""

    forms: tuple[SailFormProjection, ...]
    ea_forms: tuple[SailEaFormProjection, ...]


class SailCatalogRenderer:
    """Project the selected typed ISA into the runtime decode catalogs."""

    _CATALOG_CHUNK_SIZE = 24

    def project(self, program: SailProgram) -> SailCatalogProjection:
        forms: list[SailFormProjection] = []
        for bundle in program.bundles:
            for form in bundle.encodings.forms:
                operands = []
                for operand in _operand_representations(program, bundle, form):
                    ea_profile = None
                    if operand.field is not None:
                        definition = program.project.types.field_types.resolve(
                            operand.field.type
                        )
                        if definition.kind is FieldTypeKind.EFFECTIVE_ADDRESS:
                            ea_profile = definition.profile
                    operands.append(
                        SailOperandBindingProjection(
                            operand.name,
                            operand.type_name,
                            operand.access,
                            operand.field.marker if operand.field is not None else None,
                            operand.payload.type
                            if operand.payload is not None
                            else None,
                            operand.fixed_name,
                            operand.fixed_value,
                            ea_profile,
                        )
                    )
                forms.append(
                    SailFormProjection(
                        _form_key(bundle, form),
                        f"Op_{bundle.instruction.mnemonic}",
                        bundle.owner,
                        bundle.instruction.route,
                        bundle,
                        form,
                        tuple(operands),
                        _representative_record(program, form),
                    )
                )
        return SailCatalogProjection(tuple(forms), _ea_variants(program))

    def render(self, program: SailProgram) -> str:
        projection = self.project(program)
        entries_by_class: dict[str, list[str]] = {
            name: [] for name in CLASS_CONSTRUCTORS
        }
        for projected in projection.forms:
            encoding_class = ENCODING_CLASSES_BY_WIDTH[
                projected.form.pattern.bit_width
            ]
            entries_by_class[encoding_class.name].append(
                _render_entry(program, projected.bundle, projected.form)
            )
        catalog_sections: list[str] = []
        for name, constructor in CLASS_CONSTRUCTORS.items():
            entries = entries_by_class[name]
            chunk_names: list[str] = []
            for index, start in enumerate(
                range(0, len(entries), self._CATALOG_CHUNK_SIZE)
            ):
                chunk_name = f"primary_form_catalog_{name}_chunk_{index}"
                chunk_names.append(chunk_name)
                catalog_sections.extend(
                    (
                        f"let {chunk_name} : list(Catalog_entry) = [|",
                        ",\n".join(
                            entries[start : start + self._CATALOG_CHUNK_SIZE]
                        ),
                        "|]",
                        "",
                    )
                )
            catalog_sections.extend(
                (
                    f"let primary_form_catalog_{name}_cache : list(Catalog_entry) =",
                    "  append_catalog_entry_chunks([|"
                    + ", ".join(chunk_names)
                    + "|])",
                    "",
                )
            )
        catalog_sections.extend(
            (
                "function primary_form_catalog_for(encoding_class : Encoding_class) -> list(Catalog_entry) =",
                "  match encoding_class {",
                *(f"    {constructor} => primary_form_catalog_{name}_cache,"
                  for name, constructor in CLASS_CONSTRUCTORS.items()),
                "  }",
                "",
            )
        )
        ea_entries = [
            _render_ea_variant(program, item) for item in projection.ea_forms
        ]
        representatives = [
            "  struct { form_id = "
            f"{_constructor('Form_', item.key)}, "
            "bytes = [|"
            + ", ".join(f"0x{byte:02X}" for byte in item.representative_record)
            + "|] }"
            for item in projection.forms
        ]
        return "\n".join(
            [
                "// Generated from the typed ISA project. Do not edit.",
                "",
                "function append_catalog_entries(left : list(Catalog_entry),",
                "                                right : list(Catalog_entry)) -> list(Catalog_entry) =",
                "  match left {",
                "    [||] => right,",
                "    head :: tail => head :: append_catalog_entries(tail, right),",
                "  }",
                "",
                "function append_catalog_entry_chunks(chunks : list(list(Catalog_entry))) -> list(Catalog_entry) =",
                "  match chunks {",
                "    [||] => [||],",
                "    chunk :: tail => append_catalog_entries(chunk, append_catalog_entry_chunks(tail)),",
                "  }",
                "",
                *catalog_sections,
                "let effective_address_catalog_cache : list(Ea_form) = [|",
                ",\n".join(ea_entries),
                "|]",
                "",
                "function effective_address_catalog() -> list(Ea_form) = effective_address_catalog_cache",
                "",
                "let representative_form_records_cache : list(Representative_record) = [|",
                ",\n".join(representatives),
                "|]",
                "",
                "function representative_form_records() -> list(Representative_record) = representative_form_records_cache",
                "",
            ]
        )


def catalog_id_declarations(program: SailProgram) -> list[str]:
    variants = _ea_variants(program)
    forms = [
        "Form_invalid",
        *(
            _constructor("Form_", _form_key(bundle, form))
            for bundle in program.bundles
            for form in bundle.encodings.forms
        ),
    ]
    operand_types: set[str] = {"imm", "SP", "CS"}
    fields: set[str] = set()
    operands: set[str] = set()
    sizes: set[str] = set()
    domains: set[str] = set()
    for bundle in program.bundles:
        operands.update(bundle.instruction["operands"])
        for metadata in bundle.instruction["operands"].values():
            if metadata.get("domain"):
                domains.add(str(metadata["domain"]))
        for form in bundle.encodings.forms:
            sizes.update(form.syntax.selected_size_codes)
            if form.syntax.fixed_size_suffix:
                sizes.add(form.syntax.fixed_size_suffix.removeprefix("."))
            for field in form.fields:
                fields.add(field.marker)
                operand_types.add(
                    _field_type_name(program.project.types.field_types.resolve(field.type))
                )
            for payload in form.payloads:
                operand_types.add(
                    _payload_type_name(program.project.types.payload_types.resolve(payload.type))
                )
    for variant in variants:
        fields.update(variant.fields)
        for reference in variant.field_types.values():
            operand_types.add(
                _field_type_name(
                    program.project.types.field_types.resolve(reference)
                )
            )
    groups = (
        ("Form_id", forms),
        ("Operand_type", [_constructor("OperandType_", item) for item in sorted(operand_types)]),
        ("Size_code", [_constructor("Size_", item) for item in sorted(sizes)]),
        ("Field_id", [_constructor("Field_", item) for item in sorted(fields)]),
        ("Operand_id", [_constructor("Operand_", item) for item in sorted(operands)]),
        ("Operand_domain", [_constructor("OperandDomain_", item) for item in sorted(domains)]),
        ("Ea_role", [_constructor("EaRole_", item) for item in ("address", "base", "control_target", "index", "segment", "value")]),
        ("Ea_width", [_constructor("EaWidth_", item) for item in ("B", "L", "Q", "W", "operation_size", "predicate")]),
        (
            "Ea_profile",
            sorted(
                {
                    _constructor("EaProfile_", item.profile)
                    for item in variants
                    if item.profile is not None
                }
            ),
        ),
        ("Ea_form_id", sorted({_constructor("EaForm_", item.name) for item in variants})),
        ("Ea_descriptor_family", [_constructor("EaDescriptor_", item) for item in ("ext1", "ext2")]),
        ("Ea_kind", [_constructor("EaKind_", item) for item in ("escape", "immediate", "memory")]),
        ("Ea_segment", [_constructor("EaSegment_", item) for item in ("CS", "SS", "default", "explicit")]),
        ("Ea_base", [_constructor("EaBase_", item) for item in ("PC", "SP", "zero")]),
        ("Ea_update_target", [_constructor("EaUpdateTarget_", item) for item in ("b", "i")]),
        ("Ea_update_mode", [_constructor("EaUpdateMode_", item) for item in ("postincrement", "predecrement")]),
        (
            "Ea_update_difference",
            sorted(
                {
                    _constructor("EaUpdateDifference_", item.update_difference)
                    for item in variants
                    if item.update_difference is not None
                }
            ),
        ),
    )
    declarations = []
    for name, constructors in groups:
        values = list(constructors)
        if not values or len(values) != len(set(values)):
            raise ValueError(f"{name} constructors are empty or collide")
        declarations.append(f"enum {name} = " + " | ".join(values))
    return declarations
