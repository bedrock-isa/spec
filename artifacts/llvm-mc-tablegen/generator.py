"""Generate LLVM TableGen records from the canonical ISA catalog."""

from __future__ import annotations

from pathlib import Path
import re
from typing import TYPE_CHECKING, NamedTuple

from engine.encoding_architecture import ENCODING_CLASSES_BY_WIDTH
from engine.encoding import EncodingForm
from engine.generation import (
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.project import IsaProject
from engine.reference import Reference
from engine.type_system import FieldTypeKind, PayloadTypeKind

if TYPE_CHECKING:
    from engine.register import RegisterGroup


_OUTPUT = Path("BedrockGenISACatalog.td")


class _RenderedForm(NamedTuple):
    record_name: str
    identifier: str
    mnemonic: str
    syntax: str
    pattern: str
    encoding_class: str
    owner: str
    primary_bytes: int
    fixed_payload_bytes: int
    has_effective_address: bool
    has_variable_length: bool
    tablegen_codec_candidate: bool
    field_markers: str
    field_roles: str
    field_types: str
    payload_roles: str
    payload_types: str


class _VectorOperand(NamedTuple):
    kind: int
    field: int
    width: int
    allow_immediate_ea: bool


class _VectorForm(NamedTuple):
    record_name: str
    identifier: str
    mnemonic: str
    owner: str
    pattern: str
    suffixes: str
    encoding_class: int
    suffix_field: int
    allowed_suffix_mask: int
    allowed_condition_mask: int
    has_condition: bool
    has_width_only_aliases: bool
    operands: tuple[_VectorOperand, ...]
    distinct_operand_a: int
    distinct_operand_b: int


class _RepeatEntry(NamedTuple):
    record_name: str
    mnemonic: str
    has_condition: bool
    allows_rep: bool
    allows_repcc: bool


class _ScalarOperand(NamedTuple):
    kind: int
    field: int
    width: int
    signed: bool
    allow_immediate_ea: bool
    fixed_value: int
    allowed_mask: int


class _ScalarForm(NamedTuple):
    record_name: str
    identifier: str
    mnemonic: str
    pattern: str
    fixed_payload_bytes: int
    suffixes: str
    suffix_field: int
    allowed_suffix_mask: int
    condition_field: int
    allowed_condition_mask: int
    operands: tuple[_ScalarOperand, ...]
    distinct_operand_a: int
    distinct_operand_b: int


class _RegisterSelector(NamedTuple):
    group: int
    name: str
    encoding: int


class TableGenProjection(NamedTuple):
    """Typed records selected for the LLVM TableGen consumer."""

    forms: tuple[_RenderedForm, ...]
    scalar_forms: tuple[_ScalarForm, ...]
    vector_forms: tuple[_VectorForm, ...]
    repeat_entries: tuple[_RepeatEntry, ...]
    register_selectors: tuple[_RegisterSelector, ...]


_OPERAND_NONE = 0
_OPERAND_CONDITION = 1
_OPERAND_GPR = 2
_OPERAND_FPR = 3
_OPERAND_VECTOR = 4
_OPERAND_PREDICATE = 5
_OPERAND_EA = 6
_OPERAND_VEA = 7
_OPERAND_IMMEDIATE = 8
_OPERAND_TAIL_SIGNED = 9
_OPERAND_TAIL_UNSIGNED = 10
_OPERAND_SEGMENT = 11
_OPERAND_FIXED_SP = 12
_OPERAND_FIXED_CS = 13
_OPERAND_FIXED_IMMEDIATE = 14
_OPERAND_FEA = 15
_OPERAND_MEMORY_ORDER = 16
_OPERAND_REGISTER_SELECTOR = 17

_VECTOR_ENCODING_CLASS = {"long": 0, "extralong": 1, "xxlong": 2}


class Generator(ArtifactGenerator):
    """Project every canonical instruction form into searchable TableGen data."""

    projection: TableGenProjection

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        project = context.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("isa provider must be an IsaProject")
        forms: list[_RenderedForm] = []
        vector_forms: list[_VectorForm] = []
        scalar_forms: list[_ScalarForm] = []
        repeat_entries: list[_RepeatEntry] = []
        used_names: set[str] = set()
        selector_group_references = sorted(
            {
                payload_type.register_group
                for payload_type in project.types.payload_types.values()
                if payload_type.kind == PayloadTypeKind.REGISTER_SELECTOR
                and payload_type.register_group is not None
            }
        )
        selector_group_ids = {
            group_name: index + 1
            for index, group_name in enumerate(selector_group_references)
        }
        register_selectors = [
            _RegisterSelector(
                selector_group_ids[group_name],
                register.id.lower(),
                register.encoding,
            )
            for group_name in selector_group_references
            for register in project.registers.references.groups.resolve(
                group_name
            ).registers.values()
            if register.encoding is not None
        ]
        for bundle in project.catalog.instructions.values():
            bundle_id = f"{bundle.owner}.{bundle.instruction.mnemonic}"
            owner = bundle.owner
            for form in bundle.encodings.forms:
                encoding_class = ENCODING_CLASSES_BY_WIDTH[form.pattern.bit_width]
                field_types = tuple(
                    project.types.field_types.resolve(field.type)
                    for field in form.fields
                )
                payload_types = tuple(
                    project.types.payload_types.resolve(payload.type)
                    for payload in form.payloads
                )
                has_effective_address = any(
                    field_type.kind == FieldTypeKind.EFFECTIVE_ADDRESS
                    for field_type in field_types
                )
                fixed_payload_bytes = sum(payload.bytes for payload in payload_types)
                has_variable_length = has_effective_address
                total_fixed_bytes = (
                    encoding_class.opcode_space_bytes + fixed_payload_bytes
                )
                identifier = f"{bundle_id}.{form.id}"
                record_name = _record_name(identifier, used_names)
                forms.append(
                    _RenderedForm(
                        record_name=record_name,
                        identifier=identifier,
                        mnemonic=form.syntax.mnemonic.lower(),
                        syntax=form.syntax.code,
                        pattern=form.pattern.code,
                        encoding_class=encoding_class.name,
                        owner=owner,
                        primary_bytes=encoding_class.opcode_space_bytes,
                        fixed_payload_bytes=fixed_payload_bytes,
                        has_effective_address=has_effective_address,
                        has_variable_length=has_variable_length,
                        tablegen_codec_candidate=(
                            not has_variable_length and total_fixed_bytes <= 8
                        ),
                        field_markers=";".join(field.marker for field in form.fields),
                        field_roles=";".join(field.role for field in form.fields),
                        field_types=";".join(
                            field_type.id for field_type in field_types
                        ),
                        payload_roles=";".join(
                            payload.role for payload in form.payloads
                        ),
                        payload_types=";".join(
                            payload_type.id for payload_type in payload_types
                        ),
                    )
                )
                if bundle.instruction.route == "vector":
                    vector_forms.append(
                        _render_vector_form(
                            project, bundle, form, identifier, used_names
                        )
                    )
                else:
                    scalar_form = _render_scalar_form(
                        project,
                        bundle,
                        form,
                        identifier,
                        used_names,
                        selector_group_ids,
                    )
                    if scalar_form is not None:
                        scalar_forms.append(scalar_form)

            instruction = dict(bundle.instruction)
            mnemonic = str(instruction["mnemonic"])
            has_condition = mnemonic.endswith("cc")
            repeat = instruction.get("repeat", {})
            repeat_type = repeat.get("type")
            repeat_entries.append(
                _RepeatEntry(
                    record_name=_record_name(f"repeat.{bundle_id}", used_names),
                    mnemonic=(mnemonic[:-2] if has_condition else mnemonic).lower(),
                    has_condition=has_condition,
                    allows_rep=repeat_type in {"rep", "repcc"},
                    allows_repcc=repeat_type == "repcc",
                )
            )

        self.projection = TableGenProjection(
            tuple(forms),
            tuple(scalar_forms),
            tuple(vector_forms),
            tuple(repeat_entries),
            tuple(register_selectors),
        )
        return GeneratedArtifactSet(
            (
                GeneratedArtifact(
                    _OUTPUT,
                    _render(
                        self.projection.forms,
                        self.projection.scalar_forms,
                        self.projection.vector_forms,
                        self.projection.repeat_entries,
                        self.projection.register_selectors,
                    ),
                ),
            ),
            self.artifact_id,
        )


def _constraint_values(form: EncodingForm, role: str, width: int) -> set[int]:
    values = set(range(1 << width))
    for constraint in form.constraints:
        if constraint.role != role or not constraint.allow:
            continue
        values = set()
        for item in constraint.allow:
            if isinstance(item, int):
                values.add(item)
                continue
            text = str(item)
            if ".." in text:
                low, high = text.split("..", 1)
                values.update(range(int(low, 0), int(high, 0) + 1))
            else:
                values.add(int(text, 0))
    return values


def _render_vector_form(
    project, bundle, form: EncodingForm, identifier: str, used_names: set[str]
) -> _VectorForm:
    encoding_class = ENCODING_CLASSES_BY_WIDTH[form.pattern.bit_width]
    if encoding_class.name not in _VECTOR_ENCODING_CLASS:
        raise ValueError(f"{identifier}: vector form uses {encoding_class.name}")

    mnemonic = form.syntax.mnemonic.lower()
    has_condition = mnemonic.endswith("cc")
    if has_condition:
        mnemonic = mnemonic[:-2]

    suffixes = ""
    suffix_field = 0
    allowed_suffix_mask = 1
    if form.syntax.fixed_size_suffix is not None:
        mnemonic += form.syntax.fixed_size_suffix.lower()
    elif form.syntax.selected_size_codes:
        if form.syntax.size_field is None:
            raise ValueError(f"{identifier}: selected suffix has no size field")
        suffix_field = ord(form.syntax.size_field)
        binding = form.field_for_marker(form.syntax.size_field)
        if binding is None:
            raise ValueError(f"{identifier}: size field has no binding")
        field_type = project.types.field_types.resolve(binding.type)
        selected = set(form.syntax.selected_size_codes)
        allowed = _constraint_values(form, binding.role, field_type.bits)
        width = max((value.value for value in field_type.values), default=-1) + 1
        suffix_chars = ["?"] * width
        allowed_suffix_mask = 0
        for value in field_type.values:
            if value.code not in selected or value.value not in allowed:
                continue
            suffix_chars[value.value] = value.code.lower()
            allowed_suffix_mask |= 1 << value.value
        suffixes = "".join(suffix_chars)

    operands: list[_VectorOperand] = []
    condition_fields = [
        field
        for field in form.fields
        if project.types.field_types.resolve(field.type).kind
        == FieldTypeKind.ENUM_CONDITION
    ]
    for field in condition_fields:
        operands.append(_VectorOperand(_OPERAND_CONDITION, ord(field.marker), 0, False))

    payload_index = 0
    explicit_roles: list[str] = []
    for operand in form.syntax.displayed_operands:
        if operand.kind != "reference":
            continue
        if operand.field is not None:
            binding = form.field_for_marker(operand.field)
            if binding is None:
                raise ValueError(
                    f"{identifier}: operand field {operand.field!r} has no binding"
                )
            field_type = project.types.field_types.resolve(binding.type)
            kind = _field_operand_kind(project, field_type, identifier)
            access = binding.access
            if access is None:
                logical = dict(bundle.instruction)["operands"].get(binding.role, {})
                access = logical.get("access")
            excludes_immediate = any(
                constraint.role == binding.role and "immediate" in constraint.exclude
                for constraint in form.constraints
            )
            operands.append(
                _VectorOperand(
                    kind,
                    ord(binding.marker),
                    field_type.bits if kind == _OPERAND_IMMEDIATE else 0,
                    kind == _OPERAND_EA
                    and access != "write"
                    and not excludes_immediate,
                )
            )
            explicit_roles.append(binding.role)
            continue

        if payload_index >= len(form.payloads):
            raise ValueError(f"{identifier}: unbound displayed operand {operand.name}")
        payload_binding = form.payloads[payload_index]
        payload_index += 1
        payload_type = project.types.payload_types.resolve(payload_binding.type)
        signed = (
            payload_type.value_type == "signed_integer"
            or payload_type.id.endswith("S")
            or (operand.name or "").lower().endswith("s")
        )
        operands.append(
            _VectorOperand(
                _OPERAND_TAIL_SIGNED if signed else _OPERAND_TAIL_UNSIGNED,
                0,
                payload_type.bytes * 8,
                False,
            )
        )
        explicit_roles.append(payload_binding.role)

    if payload_index != len(form.payloads):
        raise ValueError(f"{identifier}: payload has no displayed operand")
    if len(operands) > 6:
        raise ValueError(f"{identifier}: more than six vector operands")
    operands.extend([_VectorOperand(_OPERAND_NONE, 0, 0, False)] * (6 - len(operands)))

    distinct_a = distinct_b = -1
    if form.overlaps:
        overlap = form.overlaps[0]
        try:
            distinct_a = explicit_roles.index(overlap.operands[0])
            distinct_b = explicit_roles.index(overlap.operands[1])
        except ValueError as error:
            raise ValueError(
                f"{identifier}: overlap operand is not displayed"
            ) from error

    allowed_condition_mask = 0xFFFF
    if condition_fields:
        condition = condition_fields[0]
        field_type = project.types.field_types.resolve(condition.type)
        allowed_condition_mask = sum(
            1 << value
            for value in _constraint_values(form, condition.role, field_type.bits)
        )

    assembly = dict(bundle.instruction).get("assembly", {})
    return _VectorForm(
        record_name=_record_name("vector." + identifier, used_names),
        identifier=identifier,
        mnemonic=mnemonic,
        owner=bundle.owner,
        pattern=form.pattern.code,
        suffixes=suffixes,
        encoding_class=_VECTOR_ENCODING_CLASS[encoding_class.name],
        suffix_field=suffix_field,
        allowed_suffix_mask=allowed_suffix_mask,
        allowed_condition_mask=allowed_condition_mask,
        has_condition=has_condition,
        has_width_only_aliases=bool(assembly.get("width_suffix_aliases", False)),
        operands=tuple(operands),
        distinct_operand_a=distinct_a,
        distinct_operand_b=distinct_b,
    )


def _render_scalar_form(
    project,
    bundle,
    form: EncodingForm,
    identifier: str,
    used_names: set[str],
    selector_group_ids: dict[Reference["RegisterGroup"], int] | None = None,
) -> _ScalarForm | None:
    """Return the common fixed-width scalar/FP codec projection, if applicable."""

    field_types = {
        field.marker: project.types.field_types.resolve(field.type)
        for field in form.fields
    }
    if any(
        operand.kind not in {"reference", "decimal"} for operand in form.syntax.operands
    ):
        return None

    mnemonic = form.syntax.mnemonic.lower()
    condition_fields = [
        field
        for field in form.fields
        if field_types[field.marker].kind == FieldTypeKind.ENUM_CONDITION
    ]
    if len(condition_fields) > 1:
        return None
    condition_field = ord(condition_fields[0].marker) if condition_fields else 0
    if condition_fields:
        if not mnemonic.endswith("cc"):
            return None
        mnemonic = mnemonic[:-2]

    suffixes = ""
    suffix_field = 0
    allowed_suffix_mask = 1
    if form.syntax.fixed_size_suffix is not None:
        mnemonic += form.syntax.fixed_size_suffix.lower()
    elif form.syntax.selected_size_codes:
        if form.syntax.size_field is None:
            return None
        suffix_field = ord(form.syntax.size_field)
        binding = form.field_for_marker(form.syntax.size_field)
        if binding is None:
            return None
        definition = field_types[binding.marker]
        selected = set(form.syntax.selected_size_codes)
        allowed = _constraint_values(form, binding.role, definition.bits)
        count = max((value.value for value in definition.values), default=-1) + 1
        chars = ["?"] * count
        allowed_suffix_mask = 0
        for value in definition.values:
            if value.code in selected and value.value in allowed:
                chars[value.value] = value.code.lower()
                allowed_suffix_mask |= 1 << value.value
        suffixes = "".join(chars)

    operands: list[_ScalarOperand] = []
    explicit_roles: list[str] = []
    consumed_fields: set[str] = set()
    payload_index = 0
    if form.syntax.order_field is not None:
        binding = form.field_for_marker(form.syntax.order_field)
        if binding is None:
            return None
        definition = field_types[binding.marker]
        if definition.kind != FieldTypeKind.MEMORY_ORDER:
            return None
        operands.append(
            _ScalarOperand(
                _OPERAND_MEMORY_ORDER,
                ord(binding.marker),
                definition.bits,
                False,
                False,
                0,
                sum(
                    1 << value
                    for value in _constraint_values(form, binding.role, definition.bits)
                ),
            )
        )
        explicit_roles.append(binding.role)
        consumed_fields.add(binding.marker)
    for operand in form.syntax.operands:
        if operand.kind == "decimal":
            operands.append(
                _ScalarOperand(
                    _OPERAND_FIXED_IMMEDIATE,
                    0,
                    0,
                    False,
                    False,
                    operand.literal or 0,
                    1,
                )
            )
            explicit_roles.append("")
            continue
        if operand.field is None:
            if operand.angled and payload_index < len(form.payloads):
                payload = form.payloads[payload_index]
                definition = project.types.payload_types.resolve(payload.type)
                if definition.kind not in {
                    PayloadTypeKind.IMMEDIATE,
                    PayloadTypeKind.PC_DISPLACEMENT,
                    PayloadTypeKind.FLOATING_POINT_CONSTANT_ID,
                    PayloadTypeKind.REGISTER_SELECTOR,
                }:
                    return None
                signed = (
                    definition.kind == PayloadTypeKind.PC_DISPLACEMENT
                    or definition.value_type == "signed_integer"
                    or (
                        definition.kind == PayloadTypeKind.IMMEDIATE
                        and definition.bytes == 8
                    )
                    or (operand.name or "").lower().endswith("s")
                )
                operands.append(
                    _ScalarOperand(
                        (
                            _OPERAND_REGISTER_SELECTOR
                            if definition.kind == PayloadTypeKind.REGISTER_SELECTOR
                            else (
                                _OPERAND_TAIL_SIGNED
                                if signed
                                else _OPERAND_TAIL_UNSIGNED
                            )
                        ),
                        0,
                        definition.bytes * 8,
                        signed,
                        False,
                        (
                            _selector_group_id(
                                selector_group_ids, definition.register_group
                            )
                            if definition.kind == PayloadTypeKind.REGISTER_SELECTOR
                            else 0
                        ),
                        1,
                    )
                )
                explicit_roles.append(payload.role)
                payload_index += 1
                continue
            fixed = (operand.name or "").upper()
            kind = {"SP": _OPERAND_FIXED_SP, "CS": _OPERAND_FIXED_CS}.get(fixed)
            if kind is None:
                return None
            operands.append(_ScalarOperand(kind, 0, 0, False, False, 0, 1))
            explicit_roles.append("")
            continue
        binding = form.field_for_marker(operand.field)
        if binding is None:
            return None
        definition = field_types[binding.marker]
        kind = _scalar_field_operand_kind(project, definition)
        if kind is None:
            return None
        allowed = _constraint_values(form, binding.role, definition.bits)
        if definition.bits > 8:
            return None
        excludes_immediate = any(
            constraint.role == binding.role and "immediate" in constraint.exclude
            for constraint in form.constraints
        )
        access = binding.access
        if access is None:
            access = (
                dict(bundle.instruction)["operands"].get(binding.role, {}).get("access")
            )
        operands.append(
            _ScalarOperand(
                kind,
                ord(binding.marker),
                definition.bits,
                definition.value_type == "signed_integer",
                kind in {_OPERAND_EA, _OPERAND_FEA}
                and access != "write"
                and not excludes_immediate,
                0,
                sum(1 << value for value in allowed),
            )
        )
        explicit_roles.append(binding.role)
        consumed_fields.add(binding.marker)

    implicit_fields = {
        chr(suffix_field) if suffix_field else "",
        chr(condition_field) if condition_field else "",
    }
    if any(
        field.marker not in consumed_fields and field.marker not in implicit_fields
        for field in form.fields
    ):
        return None
    if payload_index != len(form.payloads):
        return None
    if len(operands) > 4:
        return None
    operands.extend(
        [_ScalarOperand(_OPERAND_NONE, 0, 0, False, False, 0, 1)] * (4 - len(operands))
    )

    distinct_a = distinct_b = -1
    if form.overlaps:
        if len(form.overlaps) != 1:
            return None
        try:
            distinct_a = explicit_roles.index(form.overlaps[0].operands[0])
            distinct_b = explicit_roles.index(form.overlaps[0].operands[1])
        except ValueError:
            return None

    condition_mask = 0xFFFF
    if condition_fields:
        binding = condition_fields[0]
        condition_mask = sum(
            1 << value
            for value in _constraint_values(
                form, binding.role, field_types[binding.marker].bits
            )
        )

    return _ScalarForm(
        record_name=_record_name("scalar." + identifier, used_names),
        identifier=identifier,
        mnemonic=mnemonic,
        pattern=form.pattern.code,
        fixed_payload_bytes=sum(
            project.types.payload_types.resolve(payload.type).bytes
            for payload in form.payloads
        ),
        suffixes=suffixes,
        suffix_field=suffix_field,
        allowed_suffix_mask=allowed_suffix_mask,
        condition_field=condition_field,
        allowed_condition_mask=condition_mask,
        operands=tuple(operands),
        distinct_operand_a=distinct_a,
        distinct_operand_b=distinct_b,
    )


def _selector_group_id(
    selector_group_ids: dict[Reference["RegisterGroup"], int] | None,
    reference: Reference["RegisterGroup"] | None,
) -> int:
    if reference is None:
        return 0
    return (selector_group_ids or {}).get(reference, 0)


def _scalar_field_operand_kind(project, field_type) -> int | None:
    if field_type.kind == FieldTypeKind.EFFECTIVE_ADDRESS:
        return _OPERAND_FEA if field_type.profile == "fea" else _OPERAND_EA
    if field_type.kind in {
        FieldTypeKind.IMMEDIATE,
        FieldTypeKind.REGISTER_PAIR_SELECTOR,
        FieldTypeKind.PAGE_TABLE_LEVEL,
        FieldTypeKind.FLAGS,
    }:
        return _OPERAND_IMMEDIATE
    if field_type.kind in {FieldTypeKind.REGISTER, FieldTypeKind.REGISTER_SELECTOR}:
        group = _register_group_id(project, field_type.register_group)
        if group == "GPR":
            return _OPERAND_GPR
        if group == "FPR":
            return _OPERAND_FPR
        if group == "SEGMENT":
            return _OPERAND_SEGMENT
    return None


def _register_group_id(project, reference) -> str | None:
    if reference is None:
        return None
    return project.registers.references.groups.resolve(reference).id


def _field_operand_kind(project, field_type, identifier: str) -> int:
    if field_type.kind == FieldTypeKind.EFFECTIVE_ADDRESS:
        return _OPERAND_VEA if field_type.profile == "vea" else _OPERAND_EA
    if field_type.kind == FieldTypeKind.IMMEDIATE:
        return _OPERAND_IMMEDIATE
    if field_type.kind in {
        FieldTypeKind.REGISTER,
        FieldTypeKind.REGISTER_SELECTOR,
        FieldTypeKind.REGISTER_PAIR_SELECTOR,
    }:
        group = _register_group_id(project, field_type.register_group)
        if group == "GPR":
            return _OPERAND_GPR
        if group == "FPR":
            return _OPERAND_FPR
        if group == "VECTOR":
            return _OPERAND_VECTOR
        if group == "PREDICATE":
            return _OPERAND_PREDICATE
    raise ValueError(
        f"{identifier}: unsupported vector operand field type {field_type.id}"
    )


def _record_name(identifier: str, used: set[str]) -> str:
    stem = "BRForm_" + re.sub(r"[^A-Za-z0-9_]+", "_", identifier).strip("_")
    candidate = stem
    suffix = 2
    while candidate in used:
        candidate = f"{stem}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def _td_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _td_bool(value: bool) -> str:
    return "1" if value else "0"


def _render(
    forms: list[_RenderedForm],
    scalar_forms: list[_ScalarForm],
    vector_forms: list[_VectorForm],
    repeat_entries: list[_RepeatEntry],
    register_selectors: list[_RegisterSelector],
) -> str:
    lines = [
        "//===-- BedrockGenISACatalog.td - generated ISA catalog -*- tablegen -*-===//",
        "//",
        "// Generated by spec/artifacts/llvm-mc-tablegen. Do not edit.",
        "//",
        "//===----------------------------------------------------------------------===//",
        "",
        "class BedrockISAForm<string id, string mnemonic, string syntax,",
        "                     string pattern, string encodingClass, string owner,",
        "                     bits<8> primaryBytes, bits<8> fixedPayloadBytes,",
        "                     bit hasEffectiveAddress, bit hasVariableLength,",
        "                     bit tableGenCodecCandidate, string fieldMarkers,",
        "                     string fieldRoles, string fieldTypes,",
        "                     string payloadRoles, string payloadTypes> {",
        "  string Id = id;",
        "  string Mnemonic = mnemonic;",
        "  string Syntax = syntax;",
        "  string Pattern = pattern;",
        "  string EncodingClass = encodingClass;",
        "  string Owner = owner;",
        "  bits<8> PrimaryBytes = primaryBytes;",
        "  bits<8> FixedPayloadBytes = fixedPayloadBytes;",
        "  bit HasEffectiveAddress = hasEffectiveAddress;",
        "  bit HasVariableLength = hasVariableLength;",
        "  bit TableGenCodecCandidate = tableGenCodecCandidate;",
        "  string FieldMarkers = fieldMarkers;",
        "  string FieldRoles = fieldRoles;",
        "  string FieldTypes = fieldTypes;",
        "  string PayloadRoles = payloadRoles;",
        "  string PayloadTypes = payloadTypes;",
        "}",
        "",
        "def BedrockISAForms : GenericTable {",
        '  let FilterClass = "BedrockISAForm";',
        '  let Fields = ["Id", "Mnemonic", "Syntax", "Pattern",',
        '                "EncodingClass", "Owner", "PrimaryBytes",',
        '                "FixedPayloadBytes", "HasEffectiveAddress",',
        '                "HasVariableLength", "TableGenCodecCandidate",',
        '                "FieldMarkers", "FieldRoles", "FieldTypes",',
        '                "PayloadRoles", "PayloadTypes"];',
        "}",
        "",
        "def lookupBedrockISAFormById : SearchIndex {",
        "  let Table = BedrockISAForms;",
        '  let Key = ["Id"];',
        "}",
        "",
    ]
    for form in forms:
        args = (
            _td_string(form.identifier),
            _td_string(form.mnemonic),
            _td_string(form.syntax),
            _td_string(form.pattern),
            _td_string(form.encoding_class),
            _td_string(form.owner),
            str(form.primary_bytes),
            str(form.fixed_payload_bytes),
            _td_bool(form.has_effective_address),
            _td_bool(form.has_variable_length),
            _td_bool(form.tablegen_codec_candidate),
            _td_string(form.field_markers),
            _td_string(form.field_roles),
            _td_string(form.field_types),
            _td_string(form.payload_roles),
            _td_string(form.payload_types),
        )
        lines.extend(
            (
                f"def {form.record_name} : BedrockISAForm<",
                "  " + ", ".join(args[:6]) + ",",
                "  " + ", ".join(args[6:11]) + ",",
                "  " + ", ".join(args[11:]) + ">;",
            )
        )
    lines.extend(_render_scalar_table(scalar_forms))
    lines.extend(_render_register_selector_table(register_selectors))
    lines.extend(_render_vector_tables(vector_forms))
    lines.extend(_render_repeat_table(repeat_entries))
    lines.append("")
    return "\n".join(lines)


def _render_register_selector_table(
    selectors: list[_RegisterSelector],
) -> list[str]:
    lines = [
        "",
        "class BedrockRegisterSelector<bits<8> group, string name,",
        "                              bits<64> encoding> {",
        "  bits<8> Group = group;",
        "  string Name = name;",
        "  bits<64> Encoding = encoding;",
        "}",
        "",
        "def BedrockRegisterSelectors : GenericTable {",
        '  let FilterClass = "BedrockRegisterSelector";',
        '  let CppTypeName = "RegisterSelector";',
        '  let Fields = ["Group", "Name", "Encoding"];',
        "}",
        "",
    ]
    for index, selector in enumerate(selectors):
        lines.append(
            f"def BRRegisterSelector_{index} : BedrockRegisterSelector<"
            f"{selector.group}, {_td_string(selector.name)}, "
            f"{selector.encoding}>;"
        )
    return lines


def _render_scalar_table(forms: list[_ScalarForm]) -> list[str]:
    operand_parameters = []
    operand_assignments = []
    operand_fields = []
    for index in range(4):
        for name, field_type in (
            ("Kind", "bits<8>"),
            ("Field", "bits<8>"),
            ("Width", "bits<8>"),
            ("Signed", "bit"),
            ("AllowImmediateEA", "bit"),
            ("FixedValue", "bits<64>"),
            ("AllowedMask0", "bits<64>"),
            ("AllowedMask1", "bits<64>"),
            ("AllowedMask2", "bits<64>"),
            ("AllowedMask3", "bits<64>"),
        ):
            field = f"Operand{index}{name}"
            parameter = field[0].lower() + field[1:]
            operand_parameters.append(f"{field_type} {parameter}")
            operand_assignments.append(f"  {field_type} {field} = {parameter};")
            operand_fields.append(f'"{field}"')
    lines = [
        "",
        "class BedrockScalarEncodingForm<",
        "    string id, string mnemonic, string pattern, bits<8> fixedPayloadBytes,",
        "    string suffixes,",
        "    bits<8> suffixField, bits<16> allowedSuffixMask,",
        "    bits<8> conditionField, bits<16> allowedConditionMask,",
        "    bits<8> operandCount, " + ", ".join(operand_parameters) + ",",
        "    bits<8> distinctOperandA, bits<8> distinctOperandB> {",
        "  string Id = id;",
        "  string Mnemonic = mnemonic;",
        "  string Pattern = pattern;",
        "  bits<8> FixedPayloadBytes = fixedPayloadBytes;",
        "  string Suffixes = suffixes;",
        "  bits<8> SuffixField = suffixField;",
        "  bits<16> AllowedSuffixMask = allowedSuffixMask;",
        "  bits<8> ConditionField = conditionField;",
        "  bits<16> AllowedConditionMask = allowedConditionMask;",
        "  bits<8> OperandCount = operandCount;",
        *operand_assignments,
        "  bits<8> DistinctOperandA = distinctOperandA;",
        "  bits<8> DistinctOperandB = distinctOperandB;",
        "}",
        "",
        "def BedrockScalarEncodingForms : GenericTable {",
        '  let FilterClass = "BedrockScalarEncodingForm";',
        '  let CppTypeName = "ScalarEncodingForm";',
        '  let Fields = ["Id", "Mnemonic", "Pattern",',
        '                "FixedPayloadBytes", "Suffixes",',
        '                "SuffixField", "AllowedSuffixMask",',
        '                "ConditionField", "AllowedConditionMask",',
        '                "OperandCount",',
        "                " + ", ".join(operand_fields) + ",",
        '                "DistinctOperandA", "DistinctOperandB"];',
        "}",
        "",
    ]
    for form in forms:
        values = [
            _td_string(form.identifier),
            _td_string(form.mnemonic),
            _td_string(form.pattern),
            str(form.fixed_payload_bytes),
            _td_string(form.suffixes),
            str(form.suffix_field),
            str(form.allowed_suffix_mask),
            str(form.condition_field),
            str(form.allowed_condition_mask),
            str(sum(operand.kind != _OPERAND_NONE for operand in form.operands)),
        ]
        for operand in form.operands:
            values.extend(
                (
                    str(operand.kind),
                    str(operand.field),
                    str(operand.width),
                    _td_bool(operand.signed),
                    _td_bool(operand.allow_immediate_ea),
                    str(operand.fixed_value),
                    *(
                        str((operand.allowed_mask >> (64 * index)) & ((1 << 64) - 1))
                        for index in range(4)
                    ),
                )
            )
        values.extend(
            (str(form.distinct_operand_a & 0xFF), str(form.distinct_operand_b & 0xFF))
        )
        lines.extend(
            (
                f"def {form.record_name} : BedrockScalarEncodingForm<",
                "  " + ", ".join(values[:10]) + ",",
                "  " + ", ".join(values[10:28]) + ",",
                "  " + ", ".join(values[28:]) + ">;",
            )
        )
    return lines


def _render_vector_tables(forms: list[_VectorForm]) -> list[str]:
    operand_parameters = []
    operand_assignments = []
    operand_fields = []
    for index in range(6):
        for name, field_type in (
            ("Kind", "bits<8>"),
            ("Field", "bits<8>"),
            ("Width", "bits<8>"),
            ("AllowImmediateEA", "bit"),
        ):
            field = f"Operand{index}{name}"
            parameter = field[0].lower() + field[1:]
            operand_parameters.append(f"{field_type} {parameter}")
            operand_assignments.append(f"  {field_type} {field} = {parameter};")
            operand_fields.append(f'"{field}"')

    lines = [
        "",
        "class BedrockVectorEncodingForm<",
        "    string id, string mnemonic, string owner, string pattern, string suffixes,",
        "    bits<8> encodingClass, bits<8> suffixField,",
        "    bits<8> allowedSuffixMask, bits<16> allowedConditionMask,",
        "    bit hasCondition, bit hasWidthOnlyAliases, bits<8> operandCount,",
        "    " + ", ".join(operand_parameters) + ",",
        "    bits<8> distinctOperandA, bits<8> distinctOperandB> {",
        "  string Id = id;",
        "  string Mnemonic = mnemonic;",
        "  string Owner = owner;",
        "  string Pattern = pattern;",
        "  string Suffixes = suffixes;",
        "  bits<8> EncodingClass = encodingClass;",
        "  bits<8> SuffixField = suffixField;",
        "  bits<8> AllowedSuffixMask = allowedSuffixMask;",
        "  bits<16> AllowedConditionMask = allowedConditionMask;",
        "  bit HasCondition = hasCondition;",
        "  bit HasWidthOnlyAliases = hasWidthOnlyAliases;",
        "  bits<8> OperandCount = operandCount;",
        *operand_assignments,
        "  bits<8> DistinctOperandA = distinctOperandA;",
        "  bits<8> DistinctOperandB = distinctOperandB;",
        "}",
        "",
        "def BedrockVectorEncodingForms : GenericTable {",
        '  let FilterClass = "BedrockVectorEncodingForm";',
        '  let CppTypeName = "VectorEncodingForm";',
        '  let Fields = ["Id", "Mnemonic", "Owner", "Pattern", "Suffixes",',
        '                "EncodingClass", "SuffixField",',
        '                "AllowedSuffixMask", "AllowedConditionMask",',
        '                "HasCondition", "HasWidthOnlyAliases",',
        '                "OperandCount",',
        "                " + ", ".join(operand_fields) + ",",
        '                "DistinctOperandA", "DistinctOperandB"];',
        "}",
        "",
    ]
    for form in forms:
        values = [
            _td_string(form.identifier),
            _td_string(form.mnemonic),
            _td_string(form.owner),
            _td_string(form.pattern),
            _td_string(form.suffixes),
            str(form.encoding_class),
            str(form.suffix_field),
            str(form.allowed_suffix_mask),
            str(form.allowed_condition_mask),
            _td_bool(form.has_condition),
            _td_bool(form.has_width_only_aliases),
            str(sum(operand.kind != _OPERAND_NONE for operand in form.operands)),
        ]
        for operand in form.operands:
            values.extend(
                (
                    str(operand.kind),
                    str(operand.field),
                    str(operand.width),
                    _td_bool(operand.allow_immediate_ea),
                )
            )
        values.extend(
            (
                str(form.distinct_operand_a & 0xFF),
                str(form.distinct_operand_b & 0xFF),
            )
        )
        lines.extend(
            (
                f"def {form.record_name} : BedrockVectorEncodingForm<",
                "  " + ", ".join(values[:12]) + ",",
                "  " + ", ".join(values[12:28]) + ",",
                "  " + ", ".join(values[28:]) + ">;",
            )
        )
    return lines


def _render_repeat_table(entries: list[_RepeatEntry]) -> list[str]:
    lines = [
        "",
        "class BedrockRepeatEligibility<string mnemonic, bit hasCondition,",
        "                                bit allowsREP, bit allowsREPcc> {",
        "  string Mnemonic = mnemonic;",
        "  bit HasCondition = hasCondition;",
        "  bit AllowsREP = allowsREP;",
        "  bit AllowsREPcc = allowsREPcc;",
        "}",
        "",
        "def BedrockRepeatEligibilityTable : GenericTable {",
        '  let FilterClass = "BedrockRepeatEligibility";',
        '  let CppTypeName = "RepeatEligibility";',
        '  let Fields = ["Mnemonic", "HasCondition", "AllowsREP",',
        '                "AllowsREPcc"];',
        "}",
        "",
    ]
    for entry in entries:
        lines.append(
            f"def {entry.record_name} : BedrockRepeatEligibility<"
            f"{_td_string(entry.mnemonic)}, {_td_bool(entry.has_condition)}, "
            f"{_td_bool(entry.allows_rep)}, {_td_bool(entry.allows_repcc)}>;"
        )
    return lines
