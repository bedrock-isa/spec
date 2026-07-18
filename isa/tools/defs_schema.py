"""Versioned, strict dataclass decoders for every supported ISA YAML document."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from pathlib import PurePosixPath
import re
from typing import Any, Iterable

import yaml


SCHEMA_VERSION = 0
SCHEMA_FAMILIES = (
    "instruction",
    "encodings",
    "instruction_index",
    "extension",
    "operands",
    "sizes",
    "registers",
    "conditions",
    "effective_address",
    "abi_vectors",
    "memory_validation",
)
SCHEMA_LOCK_PATH = Path(__file__).resolve().parents[1] / "defs" / "schema.lock"
SCHEMA_DOCUMENT_PATH = Path(__file__).resolve().parents[1] / "defs" / "SCHEMA.md"

PRIVILEGES = frozenset({"unprivileged", "supervisor", "any"})
REPEAT_CONTEXTS = frozenset({"REP", "REPcc", "REPG", "REPGF"})
OPERAND_ACCESS = frozenset({"read", "write", "read_write", "address"})
OPERAND_DOMAINS = frozenset({"user"})
OPERAND_KINDS = frozenset(
    {
        "register",
        "fixed_register",
        "effective_address",
        "enum",
        "ea_immediate",
        "bitmap",
        "immediate",
        "relative_immediate",
    }
)
FLAG_BANKS = {
    "FLAGS": ("Z", "N", "C", "V"),
    "FFLAGS": ("NV", "DZ", "OF", "UF", "NX"),
}


class DecodeError(ValueError):
    """A YAML document does not satisfy its declared shape."""


def verify_schema_lock(lock_path: Path = SCHEMA_LOCK_PATH) -> None:
    """Reject an unversioned edit to the frozen decoder contract."""
    try:
        lines = lock_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise DecodeError(f"{lock_path}: missing schema lock: {exc}") from exc
    values: dict[str, str] = {}
    for line in lines:
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or key in values:
            raise DecodeError(f"{lock_path}: malformed schema lock line {line!r}")
        values[key] = value
    expected_keys = {"version", "families", "decoder_sha256", "contract_sha256"}
    if set(values) != expected_keys:
        raise DecodeError(f"{lock_path}: expected fields {', '.join(sorted(expected_keys))}")
    try:
        version = int(values["version"])
        family_count = int(values["families"])
    except ValueError as exc:
        raise DecodeError(f"{lock_path}: version and families must be integers") from exc
    if version != SCHEMA_VERSION:
        raise DecodeError(
            f"{lock_path}: lock version {version} does not match decoder {SCHEMA_VERSION}"
        )
    if family_count != len(SCHEMA_FAMILIES):
        raise DecodeError(
            f"{lock_path}: lock family count {family_count} does not match "
            f"decoder {len(SCHEMA_FAMILIES)}"
        )
    digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", values["decoder_sha256"]):
        raise DecodeError(f"{lock_path}: invalid decoder_sha256")
    if values["decoder_sha256"] != digest:
        raise DecodeError(
            f"{lock_path}: decoder changed without updating the versioned schema lock"
        )
    contract_digest = hashlib.sha256(SCHEMA_DOCUMENT_PATH.read_bytes()).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", values["contract_sha256"]):
        raise DecodeError(f"{lock_path}: invalid contract_sha256")
    if values["contract_sha256"] != contract_digest:
        raise DecodeError(
            f"{lock_path}: displayed contract changed without updating the versioned schema lock"
        )


def _where(path: Path, field_path: str = "") -> str:
    return f"{path}:{field_path}" if field_path else str(path)


def _mapping(value: Any, path: Path, field_path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DecodeError(f"{_where(path, field_path)}: expected mapping")
    if not all(isinstance(key, str) for key in value):
        raise DecodeError(f"{_where(path, field_path)}: keys must be strings")
    return value


def _list(value: Any, path: Path, field_path: str) -> list[Any]:
    if not isinstance(value, list):
        raise DecodeError(f"{_where(path, field_path)}: expected list")
    return value


def _string(value: Any, path: Path, field_path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DecodeError(f"{_where(path, field_path)}: expected non-empty string")
    return value


def _integer(value: Any, path: Path, field_path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise DecodeError(f"{_where(path, field_path)}: expected integer")
    return value


def _nonnegative_integer(value: Any, path: Path, field_path: str) -> int:
    result = _integer(value, path, field_path)
    if result < 0:
        raise DecodeError(f"{_where(path, field_path)}: expected non-negative integer")
    return result


def _positive_integer(value: Any, path: Path, field_path: str) -> int:
    result = _integer(value, path, field_path)
    if result <= 0:
        raise DecodeError(f"{_where(path, field_path)}: expected positive integer")
    return result


def _boolean(value: Any, path: Path, field_path: str) -> bool:
    if not isinstance(value, bool):
        raise DecodeError(f"{_where(path, field_path)}: expected boolean")
    return value


def _integer_or_string(value: Any, path: Path, field_path: str) -> int | str:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise DecodeError(f"{_where(path, field_path)}: expected integer or string")
    if isinstance(value, str) and not value.strip():
        raise DecodeError(f"{_where(path, field_path)}: expected non-empty string")
    return value


def _enum_string(
    value: Any,
    path: Path,
    field_path: str,
    allowed: frozenset[str],
) -> str:
    result = _string(value, path, field_path)
    if result not in allowed:
        raise DecodeError(
            f"{_where(path, field_path)}: expected one of {', '.join(sorted(allowed))}"
        )
    return result


def _relative_reference(value: Any, path: Path, field_path: str) -> str:
    result = _string(value, path, field_path)
    reference = PurePosixPath(result)
    if (
        reference.is_absolute()
        or str(reference) != result
        or any(part in {"", ".", ".."} for part in reference.parts)
    ):
        raise DecodeError(f"{_where(path, field_path)}: expected normalized relative path")
    return result


def _unique(values: Iterable[Any], path: Path, field_path: str) -> None:
    seen: set[Any] = set()
    for value in values:
        if value in seen:
            raise DecodeError(f"{_where(path, field_path)}: duplicate value {value}")
        seen.add(value)


def _byte_list(value: Any, path: Path, field_path: str) -> tuple[int, ...]:
    result: list[int] = []
    for index, item in enumerate(_list(value, path, field_path)):
        byte = _integer(item, path, f"{field_path}[{index}]")
        if not 0 <= byte <= 0xFF:
            raise DecodeError(f"{_where(path, field_path + f'[{index}]')}: byte out of range")
        result.append(byte)
    return tuple(result)


def _keys(
    value: dict[str, Any],
    path: Path,
    field_path: str,
    *,
    required: Iterable[str] = (),
    optional: Iterable[str] = (),
) -> None:
    required_set = set(required)
    allowed = required_set | set(optional)
    missing = required_set - value.keys()
    if missing:
        raise DecodeError(
            f"{_where(path, field_path)}: missing fields {', '.join(sorted(missing))}"
        )
    unknown = value.keys() - allowed
    if unknown:
        raise DecodeError(
            f"{_where(path, field_path)}: unknown fields {', '.join(sorted(unknown))}"
        )


def _string_list(value: Any, path: Path, field_path: str) -> list[str]:
    return [
        _string(item, path, f"{field_path}[{index}]")
        for index, item in enumerate(_list(value, path, field_path))
    ]


@dataclass(frozen=True)
class InstructionAttributes:
    instruction_class: str
    family: str
    privilege: str
    repeat: tuple[str, ...] = ()


@dataclass(frozen=True)
class InstructionDocument:
    mnemonic: str
    title: str
    summary: str
    description: str
    attributes: InstructionAttributes
    flag_effects: dict[str, dict[str, str]] = field(default_factory=dict)
    additional_assembler_syntax: tuple[str, ...] = ()
    additional_description: str | None = None


@dataclass(frozen=True)
class EncodingOperand:
    name: str
    type: str
    access: str
    field: str | None = None
    domain: str | None = None


@dataclass(frozen=True)
class EncodingField:
    type: str


@dataclass(frozen=True)
class EncodingConstraint:
    field: str
    allow: tuple[int | str, ...] = ()
    exclude: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class EncodingForm:
    id: str
    encoding_class: str
    bits: str
    syntax: str
    operands: tuple[EncodingOperand, ...] = ()
    sizes: tuple[str, ...] = ()
    fields: dict[str, EncodingField] = field(default_factory=dict)
    constraints: tuple[EncodingConstraint, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class EncodingsDocument:
    forms: tuple[EncodingForm, ...]


@dataclass(frozen=True)
class InstructionSetIndex:
    title: str
    include: tuple[str, ...]
    introduction: str | None = None


@dataclass(frozen=True)
class CpuidAvailability:
    feature: str
    selector_class: int
    leaf: int
    index: int
    bit: int


@dataclass(frozen=True)
class ExtensionManifest:
    name: str
    instructions: str | None = None
    operands: str | None = None
    registers: str | None = None
    sizes: str | None = None
    extensions: tuple[str, ...] = ()
    availability: CpuidAvailability | None = None


@dataclass(frozen=True)
class ExtensionCatalog:
    extensions: tuple[str, ...]


@dataclass(frozen=True)
class OperandEnumValue:
    value: int | str
    name: str
    registers: tuple[str, ...] = ()
    value_bits: str | None = None


@dataclass(frozen=True)
class OperandBit:
    bit: int
    name: str


@dataclass(frozen=True)
class OperandType:
    kind: str
    field_width: int
    register_group: str | None = None
    register: str | None = None
    encoding_ref: str | None = None
    values_ref: str | None = None
    signed: bool | None = None
    operation_size_extension: str | None = None
    values: tuple[OperandEnumValue, ...] = ()
    reserved_values: tuple[OperandEnumValue, ...] = ()
    bits: tuple[OperandBit, ...] = ()
    result_bits_format: str | None = None


@dataclass(frozen=True)
class OperandRegistry:
    operand_types: dict[str, OperandType]


@dataclass(frozen=True)
class SizeCode:
    suffix: str
    bytes: int


@dataclass(frozen=True)
class SizeKindValue:
    value: int
    code: str | None = None
    name: str | None = None


@dataclass(frozen=True)
class SizeKind:
    field: str
    values: tuple[SizeKindValue, ...]
    reserved_values: tuple[SizeKindValue, ...] = ()


@dataclass(frozen=True)
class SizeRegistry:
    size_codes: dict[str, SizeCode]
    size_kinds: dict[str, SizeKind]


@dataclass(frozen=True)
class RegisterEntry:
    name: str
    width: int
    encoding: int | None = None
    role: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class RegisterGroup:
    entries: tuple[RegisterEntry, ...]


@dataclass(frozen=True)
class RegisterRegistry:
    registers: dict[str, RegisterGroup]


@dataclass(frozen=True)
class ConditionDefinition:
    name: str
    value: int
    expression: str
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConditionRegistry:
    conditions: tuple[ConditionDefinition, ...]


@dataclass(frozen=True)
class EaPayload:
    kind: str
    field_width: int
    signed: bool


@dataclass(frozen=True)
class EaField:
    type: str
    role: str


@dataclass(frozen=True)
class EaUpdate:
    target: str
    mode: str


@dataclass(frozen=True)
class EaForm:
    name: str
    pattern: tuple[str, ...]
    syntax: str
    kind: str | None = None
    fields: dict[str, EaField] = field(default_factory=dict)
    segment: str | None = None
    payload: str | None = None
    base: str | None = None
    register: str | None = None
    descriptor: str | None = None
    update: EaUpdate | None = None


@dataclass(frozen=True)
class EaRegistry:
    payloads: dict[str, EaPayload]
    compact_field_width: int
    compact_forms: tuple[EaForm, ...]
    ext0_kind: str
    ext0_forms: tuple[EaForm, ...]


@dataclass(frozen=True)
class AbiDisplacement:
    offset: int
    width_bits: int
    byte_order: str


@dataclass(frozen=True)
class AbiInstruction:
    assembly: str
    offset: int
    opcode_bytes: tuple[int, ...]
    total_bytes: int
    displacement: AbiDisplacement


@dataclass(frozen=True)
class AbiRelocation:
    type: str
    place: str
    addend: int
    calculation: str
    effective_displacement: str


@dataclass(frozen=True)
class AbiPadding:
    offset: int
    length: int
    byte: int


@dataclass(frozen=True)
class AbiGotSlot:
    size: int
    alignment: int
    contents: str
    immutable_after_publication: bool


@dataclass(frozen=True)
class AbiRelocationVector:
    entry_address: int
    got_slot_address: int
    place: int
    addend: int
    encoded_little_endian: tuple[int, ...]
    result: int | None = None
    result_signed: int | None = None


@dataclass(frozen=True)
class AbiVectorsDocument:
    entry_size: int
    alignment: int
    instruction: AbiInstruction
    relocation: AbiRelocation
    padding: AbiPadding
    got_slot: AbiGotSlot
    relocation_vectors: tuple[AbiRelocationVector, ...]


@dataclass(frozen=True)
class MemoryValidationTarget:
    afence_is_full_cumulative: bool
    one_global_sc_order: bool
    isolated_fenced_scalar_is_sc: bool
    failed_seqcst_cmpxchg_is_sc_load: bool
    compare_exchange_uses_order_join: bool
    failed_release_component_creates_release_sequence: bool


@dataclass(frozen=True)
class LitmusFamily:
    id: str
    purpose: str


@dataclass(frozen=True)
class MemoryValidationDocument:
    status: str
    target: MemoryValidationTarget
    litmus_families: tuple[LitmusFamily, ...]
    failure_action: tuple[str, ...]


DecodedDocument = (
    InstructionDocument
    | EncodingsDocument
    | InstructionSetIndex
    | ExtensionManifest
    | ExtensionCatalog
    | OperandRegistry
    | SizeRegistry
    | RegisterRegistry
    | ConditionRegistry
    | EaRegistry
    | AbiVectorsDocument
    | MemoryValidationDocument
)


def decode_instruction(path: Path, raw: Any) -> InstructionDocument:
    data = _mapping(raw, path, "")
    _keys(
        data,
        path,
        "",
        required=("mnemonic", "title", "summary", "description", "attributes"),
        optional=("flag_effects", "additional_assembler_syntax", "additional_description"),
    )
    attrs = _mapping(data["attributes"], path, "attributes")
    _keys(
        attrs,
        path,
        "attributes",
        required=("class", "family", "privilege"),
        optional=("repeat",),
    )
    repeat = tuple(
        _enum_string(value, path, f"attributes.repeat[{index}]", REPEAT_CONTEXTS)
        for index, value in enumerate(
            _list(attrs.get("repeat", []), path, "attributes.repeat")
        )
    )
    _unique(repeat, path, "attributes.repeat")
    extra_syntax = tuple(
        _string_list(
            data.get("additional_assembler_syntax", []),
            path,
            "additional_assembler_syntax",
        )
    )
    _unique(extra_syntax, path, "additional_assembler_syntax")
    raw_flag_effects = _mapping(data.get("flag_effects", {}), path, "flag_effects")
    unknown_banks = raw_flag_effects.keys() - FLAG_BANKS.keys()
    if unknown_banks:
        raise DecodeError(
            f"{_where(path, 'flag_effects')}: unknown flag banks "
            f"{', '.join(sorted(unknown_banks))}"
        )
    flag_effects: dict[str, dict[str, str]] = {}
    for bank, valid_flags in FLAG_BANKS.items():
        if bank not in raw_flag_effects:
            continue
        raw_effects = _mapping(raw_flag_effects[bank], path, f"flag_effects.{bank}")
        if not raw_effects:
            raise DecodeError(
                f"{_where(path, f'flag_effects.{bank}')}: expected non-empty mapping"
            )
        unknown_flags = raw_effects.keys() - set(valid_flags)
        if unknown_flags:
            raise DecodeError(
                f"{_where(path, f'flag_effects.{bank}')}: unknown flags "
                f"{', '.join(sorted(unknown_flags))}"
            )
        flag_effects[bank] = {
            flag: _string(raw_effects[flag], path, f"flag_effects.{bank}.{flag}")
            for flag in valid_flags
            if flag in raw_effects
        }
    additional_description = data.get("additional_description")
    if additional_description is not None:
        additional_description = _relative_reference(
            additional_description, path, "additional_description"
        )
        if not additional_description.endswith(".tex"):
            raise DecodeError(f"{_where(path, 'additional_description')}: expected .tex file")
    mnemonic = _string(data["mnemonic"], path, "mnemonic")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", mnemonic):
        raise DecodeError(f"{_where(path, 'mnemonic')}: invalid mnemonic")
    return InstructionDocument(
        mnemonic=mnemonic,
        title=_string(data["title"], path, "title"),
        summary=_string(data["summary"], path, "summary"),
        description=_string(data["description"], path, "description"),
        attributes=InstructionAttributes(
            instruction_class=_string(attrs["class"], path, "attributes.class"),
            family=_string(attrs["family"], path, "attributes.family"),
            privilege=_enum_string(
                attrs["privilege"], path, "attributes.privilege", PRIVILEGES
            ),
            repeat=repeat,
        ),
        flag_effects=flag_effects,
        additional_assembler_syntax=extra_syntax,
        additional_description=additional_description,
    )


def decode_encodings(path: Path, raw: Any) -> EncodingsDocument:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("forms",))
    forms: list[EncodingForm] = []
    ids: set[str] = set()
    for index, raw_form in enumerate(_list(data["forms"], path, "forms")):
        field_path = f"forms[{index}]"
        form = _mapping(raw_form, path, field_path)
        _keys(
            form,
            path,
            field_path,
            required=("id", "class", "bits", "syntax"),
            optional=("operands", "sizes", "fields", "constraints", "notes"),
        )
        form_id = _string(form["id"], path, f"{field_path}.id")
        if form_id in ids:
            raise DecodeError(f"{_where(path, field_path)}: duplicate id {form_id}")
        ids.add(form_id)
        bits = _string(form["bits"], path, f"{field_path}.bits")
        if any(char not in "01?abcdefghijklmnopqrstuvwxyz" for char in bits):
            raise DecodeError(f"{_where(path, field_path + '.bits')}: invalid bit pattern")
        encoding_class = _string(form["class"], path, field_path + ".class")
        if not re.fullmatch(r"[a-z][a-z0-9_]*\.[a-z0-9_.]+", form_id):
            raise DecodeError(f"{_where(path, field_path + '.id')}: invalid stable form id")
        if not form_id.startswith(encoding_class + "."):
            raise DecodeError(
                f"{_where(path, field_path + '.id')}: id must start with class {encoding_class}."
            )

        operands: list[EncodingOperand] = []
        operand_fields: set[str] = set()
        for operand_index, raw_operand in enumerate(
            _list(form.get("operands", []), path, f"{field_path}.operands")
        ):
            operand_path = f"{field_path}.operands[{operand_index}]"
            operand = _mapping(raw_operand, path, operand_path)
            _keys(
                operand,
                path,
                operand_path,
                required=("name", "type", "access"),
                optional=("field", "domain"),
            )
            marker = operand.get("field")
            if marker is not None:
                marker = _string(marker, path, operand_path + ".field")
                if len(marker) != 1 or marker not in bits:
                    raise DecodeError(
                        f"{_where(path, operand_path + '.field')}: marker must occur in bits"
                    )
                if marker in operand_fields:
                    raise DecodeError(
                        f"{_where(path, operand_path + '.field')}: duplicate operand field {marker}"
                    )
                operand_fields.add(marker)
            domain = operand.get("domain")
            if domain is not None:
                domain = _string(domain, path, operand_path + ".domain")
            operands.append(
                EncodingOperand(
                    name=_string(operand["name"], path, operand_path + ".name"),
                    type=_string(operand["type"], path, operand_path + ".type"),
                    access=_enum_string(
                        operand["access"], path, operand_path + ".access", OPERAND_ACCESS
                    ),
                    field=marker,
                    domain=(
                        _enum_string(domain, path, operand_path + ".domain", OPERAND_DOMAINS)
                        if domain is not None
                        else None
                    ),
                )
            )

        fields: dict[str, EncodingField] = {}
        raw_fields = _mapping(form.get("fields", {}), path, f"{field_path}.fields")
        for marker, raw_field in raw_fields.items():
            item_path = f"{field_path}.fields.{marker}"
            if len(marker) != 1 or marker not in bits or marker in operand_fields:
                raise DecodeError(f"{_where(path, item_path)}: invalid or duplicate marker")
            item = _mapping(raw_field, path, item_path)
            _keys(item, path, item_path, required=("type",))
            fields[marker] = EncodingField(
                type=_string(item["type"], path, item_path + ".type")
            )
        declared_markers = operand_fields | set(fields)
        actual_markers = {char for char in bits if char not in "01?"}
        if declared_markers != actual_markers:
            missing = actual_markers - declared_markers
            extra = declared_markers - actual_markers
            raise DecodeError(
                f"{_where(path, field_path)}: field declarations differ from bits "
                f"(missing={sorted(missing)}, extra={sorted(extra)})"
            )

        constraints: list[EncodingConstraint] = []
        for constraint_index, raw_constraint in enumerate(
            _list(form.get("constraints", []), path, f"{field_path}.constraints")
        ):
            item_path = f"{field_path}.constraints[{constraint_index}]"
            item = _mapping(raw_constraint, path, item_path)
            _keys(
                item,
                path,
                item_path,
                required=("field", "reason"),
                optional=("allow", "exclude"),
            )
            if ("allow" in item) == ("exclude" in item):
                raise DecodeError(
                    f"{_where(path, item_path)}: exactly one of allow/exclude is required"
                )
            marker = _string(item["field"], path, item_path + ".field")
            if len(marker) != 1 or marker not in bits:
                raise DecodeError(f"{_where(path, item_path + '.field')}: missing marker")
            allow: tuple[int | str, ...] = ()
            if "allow" in item:
                raw_allow = _list(item["allow"], path, item_path + ".allow")
                if not all(
                    (isinstance(value, int) and not isinstance(value, bool))
                    or isinstance(value, str)
                    for value in raw_allow
                ):
                    raise DecodeError(
                        f"{_where(path, item_path + '.allow')}: expected integer/range values"
                    )
                allow = tuple(raw_allow)
            exclude = item.get("exclude")
            if exclude is not None:
                exclude = _string(exclude, path, item_path + ".exclude")
            reason = _string(item["reason"], path, item_path + ".reason")
            constraints.append(
                EncodingConstraint(marker, allow, exclude, reason)
            )

        sizes = tuple(_string_list(form.get("sizes", []), path, field_path + ".sizes"))
        _unique(sizes, path, field_path + ".sizes")
        forms.append(
            EncodingForm(
                id=form_id,
                encoding_class=encoding_class,
                bits=bits,
                syntax=_string(form["syntax"], path, field_path + ".syntax"),
                operands=tuple(operands),
                sizes=sizes,
                fields=fields,
                constraints=tuple(constraints),
                notes=tuple(_string_list(form.get("notes", []), path, field_path + ".notes")),
            )
        )
    return EncodingsDocument(tuple(forms))


def decode_instruction_index(path: Path, raw: Any) -> InstructionSetIndex:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("title", "include"), optional=("introduction",))
    introduction = data.get("introduction")
    if introduction is not None:
        introduction = _relative_reference(introduction, path, "introduction")
        if not introduction.endswith(".tex"):
            raise DecodeError(f"{_where(path, 'introduction')}: expected .tex file")
    include = tuple(
        _relative_reference(value, path, f"include[{index}]")
        for index, value in enumerate(_list(data["include"], path, "include"))
    )
    if not include:
        raise DecodeError(f"{_where(path, 'include')}: expected non-empty list")
    _unique(include, path, "include")
    return InstructionSetIndex(
        title=_string(data["title"], path, "title"),
        include=include,
        introduction=introduction,
    )


def decode_extension_catalog(path: Path, raw: Any) -> ExtensionCatalog:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("extensions",))
    extensions = tuple(
        _relative_reference(value, path, f"extensions[{index}]")
        for index, value in enumerate(_list(data["extensions"], path, "extensions"))
    )
    _unique(extensions, path, "extensions")
    return ExtensionCatalog(extensions)


def decode_extension_manifest(path: Path, raw: Any) -> ExtensionManifest:
    data = _mapping(raw, path, "")
    _keys(
        data,
        path,
        "",
        required=("name",),
        optional=(
            "instructions",
            "operands",
            "registers",
            "sizes",
            "extensions",
            "availability",
        ),
    )
    refs: dict[str, str | None] = {}
    for key in ("instructions", "operands", "registers", "sizes"):
        value = data.get(key)
        refs[key] = _relative_reference(value, path, key) if value is not None else None
    availability = None
    if "availability" in data:
        avail = _mapping(data["availability"], path, "availability")
        _keys(avail, path, "availability", required=("cpuid",))
        cpuid = _mapping(avail["cpuid"], path, "availability.cpuid")
        _keys(
            cpuid,
            path,
            "availability.cpuid",
            required=("feature", "class", "leaf", "index", "bit"),
        )
        selector_class = _nonnegative_integer(
            cpuid["class"], path, "availability.cpuid.class"
        )
        leaf = _nonnegative_integer(cpuid["leaf"], path, "availability.cpuid.leaf")
        index = _nonnegative_integer(cpuid["index"], path, "availability.cpuid.index")
        bit = _nonnegative_integer(cpuid["bit"], path, "availability.cpuid.bit")
        if bit >= 64:
            raise DecodeError(f"{_where(path, 'availability.cpuid.bit')}: expected 0..63")
        availability = CpuidAvailability(
            feature=_string(cpuid["feature"], path, "availability.cpuid.feature"),
            selector_class=selector_class,
            leaf=leaf,
            index=index,
            bit=bit,
        )
    extensions = tuple(
        _relative_reference(value, path, f"extensions[{index}]")
        for index, value in enumerate(
            _list(data.get("extensions", []), path, "extensions")
        )
    )
    _unique(extensions, path, "extensions")
    return ExtensionManifest(
        name=_string(data["name"], path, "name"),
        instructions=refs["instructions"],
        operands=refs["operands"],
        registers=refs["registers"],
        sizes=refs["sizes"],
        extensions=extensions,
        availability=availability,
    )


def _validate_item_keys(
    path: Path,
    field_path: str,
    value: Any,
    *,
    required: Iterable[str] = (),
    optional: Iterable[str] = (),
) -> dict[str, Any]:
    item = _mapping(value, path, field_path)
    _keys(item, path, field_path, required=required, optional=optional)
    return item


def _decode_operand_values(
    value: Any, path: Path, field_path: str
) -> tuple[OperandEnumValue, ...]:
    result: list[OperandEnumValue] = []
    for index, raw_item in enumerate(_list(value, path, field_path)):
        item_path = f"{field_path}[{index}]"
        item = _mapping(raw_item, path, item_path)
        _keys(
            item,
            path,
            item_path,
            required=("value", "name"),
            optional=("registers", "value_bits"),
        )
        registers = tuple(
            _string_list(item.get("registers", []), path, item_path + ".registers")
        )
        _unique(registers, path, item_path + ".registers")
        value_bits = item.get("value_bits")
        result.append(
            OperandEnumValue(
                value=_integer_or_string(item["value"], path, item_path + ".value"),
                name=_string(item["name"], path, item_path + ".name"),
                registers=registers,
                value_bits=(
                    _string(value_bits, path, item_path + ".value_bits")
                    if value_bits is not None
                    else None
                ),
            )
        )
    _unique((item.value for item in result), path, field_path + ".value")
    _unique((item.name for item in result), path, field_path + ".name")
    return tuple(result)


def decode_operand_registry(path: Path, raw: Any) -> OperandRegistry:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("operand_types",))
    raw_types = _mapping(data["operand_types"], path, "operand_types")
    operand_types: dict[str, OperandType] = {}
    common_optional = {
        "register_group",
        "register",
        "encoding_ref",
        "values_ref",
        "signed",
        "operation_size_extension",
        "values",
        "reserved_values",
        "bits",
        "result_bits_format",
    }
    allowed_by_kind = {
        "register": {"register_group"},
        "fixed_register": {"register"},
        "effective_address": {"encoding_ref"},
        "enum": {"values_ref", "values", "reserved_values", "result_bits_format"},
        "ea_immediate": {"encoding_ref"},
        "bitmap": {"bits"},
        "immediate": {"signed", "operation_size_extension"},
        "relative_immediate": {"signed", "operation_size_extension"},
    }
    required_by_kind = {
        "register": {"register_group"},
        "fixed_register": {"register"},
        "effective_address": {"encoding_ref"},
        "ea_immediate": {"encoding_ref"},
        "bitmap": {"bits"},
        "immediate": {"signed"},
        "relative_immediate": {"signed"},
    }
    for name, raw_item in raw_types.items():
        item_path = f"operand_types.{name}"
        item = _mapping(raw_item, path, item_path)
        _keys(
            item,
            path,
            item_path,
            required=("kind", "field_width"),
            optional=common_optional,
        )
        kind = _enum_string(item["kind"], path, item_path + ".kind", OPERAND_KINDS)
        irrelevant = (set(item) - {"kind", "field_width"}) - allowed_by_kind[kind]
        if irrelevant:
            raise DecodeError(
                f"{_where(path, item_path)}: fields not valid for {kind}: "
                f"{', '.join(sorted(irrelevant))}"
            )
        missing = required_by_kind.get(kind, set()) - set(item)
        if missing:
            raise DecodeError(
                f"{_where(path, item_path)}: {kind} requires {', '.join(sorted(missing))}"
            )
        if kind == "enum" and ("values" in item) == ("values_ref" in item):
            raise DecodeError(
                f"{_where(path, item_path)}: enum requires exactly one of values/values_ref"
            )
        values = _decode_operand_values(item.get("values", []), path, item_path + ".values")
        reserved = _decode_operand_values(
            item.get("reserved_values", []), path, item_path + ".reserved_values"
        )
        _unique(
            (entry.value for entry in (*values, *reserved)),
            path,
            item_path + ".values",
        )
        bits: list[OperandBit] = []
        for index, raw_bit in enumerate(
            _list(item.get("bits", []), path, item_path + ".bits")
        ):
            bit_path = f"{item_path}.bits[{index}]"
            bit = _mapping(raw_bit, path, bit_path)
            _keys(bit, path, bit_path, required=("bit", "name"))
            bits.append(
                OperandBit(
                    bit=_nonnegative_integer(bit["bit"], path, bit_path + ".bit"),
                    name=_string(bit["name"], path, bit_path + ".name"),
                )
            )
        _unique((bit.bit for bit in bits), path, item_path + ".bits.bit")
        _unique((bit.name for bit in bits), path, item_path + ".bits.name")
        field_width = _nonnegative_integer(
            item["field_width"], path, item_path + ".field_width"
        )
        if any(bit.bit >= field_width for bit in bits):
            raise DecodeError(f"{_where(path, item_path + '.bits')}: bit exceeds field width")

        def optional_string(key: str) -> str | None:
            child = item.get(key)
            return (
                _string(child, path, item_path + "." + key)
                if child is not None
                else None
            )

        signed = item.get("signed")
        operand_types[name] = OperandType(
            kind=kind,
            field_width=field_width,
            register_group=optional_string("register_group"),
            register=optional_string("register"),
            encoding_ref=optional_string("encoding_ref"),
            values_ref=optional_string("values_ref"),
            signed=(
                _boolean(signed, path, item_path + ".signed")
                if signed is not None
                else None
            ),
            operation_size_extension=optional_string("operation_size_extension"),
            values=values,
            reserved_values=reserved,
            bits=tuple(bits),
            result_bits_format=optional_string("result_bits_format"),
        )
    return OperandRegistry(operand_types)


def _decode_size_values(
    value: Any, path: Path, field_path: str, *, reserved: bool
) -> tuple[SizeKindValue, ...]:
    result: list[SizeKindValue] = []
    for index, raw_item in enumerate(_list(value, path, field_path)):
        item_path = f"{field_path}[{index}]"
        item = _mapping(raw_item, path, item_path)
        required = ("value", "name") if reserved else ("value", "code")
        _keys(item, path, item_path, required=required)
        result.append(
            SizeKindValue(
                value=_nonnegative_integer(item["value"], path, item_path + ".value"),
                code=(
                    _string(item["code"], path, item_path + ".code")
                    if "code" in item
                    else None
                ),
                name=(
                    _string(item["name"], path, item_path + ".name")
                    if "name" in item
                    else None
                ),
            )
        )
    _unique((item.value for item in result), path, field_path + ".value")
    return tuple(result)


def decode_size_registry(path: Path, raw: Any) -> SizeRegistry:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("size_codes", "size_kinds"))
    size_codes: dict[str, SizeCode] = {}
    for name, value in _mapping(data["size_codes"], path, "size_codes").items():
        item_path = f"size_codes.{name}"
        item = _validate_item_keys(path, item_path, value, required=("suffix", "bytes"))
        suffix = _string(item["suffix"], path, item_path + ".suffix")
        if not suffix.startswith("."):
            raise DecodeError(f"{_where(path, item_path + '.suffix')}: expected dotted suffix")
        size_codes[name] = SizeCode(
            suffix=suffix,
            bytes=_positive_integer(item["bytes"], path, item_path + ".bytes"),
        )
    size_kinds: dict[str, SizeKind] = {}
    for name, value in _mapping(data["size_kinds"], path, "size_kinds").items():
        item_path = f"size_kinds.{name}"
        item = _validate_item_keys(
            path,
            item_path,
            value,
            required=("field", "values"),
            optional=("reserved_values",),
        )
        marker = _string(item["field"], path, item_path + ".field")
        if not re.fullmatch(r"[a-z]", marker):
            raise DecodeError(f"{_where(path, item_path + '.field')}: invalid marker")
        values = _decode_size_values(
            item["values"], path, item_path + ".values", reserved=False
        )
        reserved_values = _decode_size_values(
            item.get("reserved_values", []),
            path,
            item_path + ".reserved_values",
            reserved=True,
        )
        if not values:
            raise DecodeError(f"{_where(path, item_path + '.values')}: expected non-empty list")
        _unique(
            (entry.value for entry in (*values, *reserved_values)),
            path,
            item_path + ".values",
        )
        size_kinds[name] = SizeKind(marker, values, reserved_values)
    return SizeRegistry(size_codes, size_kinds)


def decode_register_registry(path: Path, raw: Any) -> RegisterRegistry:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("registers",))
    registers: dict[str, RegisterGroup] = {}
    for group, value in _mapping(data["registers"], path, "registers").items():
        group_path = f"registers.{group}"
        item = _validate_item_keys(path, group_path, value, required=("entries",))
        entries: list[RegisterEntry] = []
        for index, child in enumerate(_list(item["entries"], path, group_path + ".entries")):
            child_path = f"{group_path}.entries[{index}]"
            child_map = _mapping(child, path, child_path)
            _keys(
                child_map,
                path,
                child_path,
                required=("name", "width"),
                optional=("encoding", "role", "description"),
            )
            encoding = child_map.get("encoding")
            role = child_map.get("role")
            description = child_map.get("description")
            entries.append(
                RegisterEntry(
                    name=_string(child_map["name"], path, child_path + ".name"),
                    width=_positive_integer(
                        child_map["width"], path, child_path + ".width"
                    ),
                    encoding=(
                        _nonnegative_integer(encoding, path, child_path + ".encoding")
                        if encoding is not None
                        else None
                    ),
                    role=(
                        _string(role, path, child_path + ".role")
                        if role is not None
                        else None
                    ),
                    description=(
                        _string(description, path, child_path + ".description")
                        if description is not None
                        else None
                    ),
                )
            )
        if not entries:
            raise DecodeError(f"{_where(path, group_path + '.entries')}: expected non-empty list")
        _unique((entry.name for entry in entries), path, group_path + ".entries.name")
        _unique(
            (entry.encoding for entry in entries if entry.encoding is not None),
            path,
            group_path + ".entries.encoding",
        )
        registers[group] = RegisterGroup(tuple(entries))
    return RegisterRegistry(registers)


def decode_condition_registry(path: Path, raw: Any) -> ConditionRegistry:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("conditions",))
    conditions: list[ConditionDefinition] = []
    for index, value in enumerate(_list(data["conditions"], path, "conditions")):
        item_path = f"conditions[{index}]"
        item = _validate_item_keys(
            path,
            item_path,
            value,
            required=("name", "value", "expression"),
            optional=("aliases",),
        )
        aliases = tuple(
            _string_list(item.get("aliases", []), path, item_path + ".aliases")
        )
        _unique(aliases, path, item_path + ".aliases")
        conditions.append(
            ConditionDefinition(
                name=_string(item["name"], path, item_path + ".name"),
                value=_nonnegative_integer(item["value"], path, item_path + ".value"),
                expression=_string(item["expression"], path, item_path + ".expression"),
                aliases=aliases,
            )
        )
    if not conditions:
        raise DecodeError(f"{_where(path, 'conditions')}: expected non-empty list")
    _unique((item.value for item in conditions), path, "conditions.value")
    names = [item.name for item in conditions]
    names.extend(alias for item in conditions for alias in item.aliases)
    _unique(names, path, "conditions.name/aliases")
    return ConditionRegistry(tuple(conditions))


def _decode_ea_forms(
    value: Any,
    path: Path,
    field_path: str,
    *,
    compact: bool,
    compact_width: int | None = None,
) -> tuple[EaForm, ...]:
    forms: list[EaForm] = []
    for index, raw_item in enumerate(_list(value, path, field_path)):
        item_path = f"{field_path}[{index}]"
        item = _mapping(raw_item, path, item_path)
        required = (
            ("name", "pattern", "syntax", "kind")
            if compact
            else ("name", "pattern", "syntax")
        )
        optional = (
            {"fields", "segment", "payload", "base", "register", "descriptor"}
            if compact
            else {"fields", "segment", "base", "update"}
        )
        _keys(item, path, item_path, required=required, optional=optional)
        raw_pattern = item["pattern"]
        if compact:
            patterns = (_string(raw_pattern, path, item_path + ".pattern"),)
        else:
            patterns = tuple(_string_list(raw_pattern, path, item_path + ".pattern"))
            if not patterns:
                raise DecodeError(
                    f"{_where(path, item_path + '.pattern')}: expected non-empty list"
                )
        if compact_width is not None and any(
            len(pattern) != compact_width for pattern in patterns
        ):
            raise DecodeError(f"{_where(path, item_path + '.pattern')}: width mismatch")
        if not compact and any(len(pattern) != 8 for pattern in patterns):
            raise DecodeError(
                f"{_where(path, item_path + '.pattern')}: EXT0 bytes must be 8 bits"
            )
        if any(
            set(pattern) - set("01abcdefghijklmnopqrstuvwxyz") for pattern in patterns
        ):
            raise DecodeError(f"{_where(path, item_path + '.pattern')}: invalid bit pattern")
        raw_fields = _mapping(item.get("fields", {}), path, item_path + ".fields")
        fields: dict[str, EaField] = {}
        for marker, raw_field in raw_fields.items():
            marker_path = item_path + ".fields." + marker
            if not re.fullmatch(r"[a-z]", marker):
                raise DecodeError(f"{_where(path, marker_path)}: invalid marker")
            field_item = _mapping(raw_field, path, marker_path)
            _keys(field_item, path, marker_path, required=("type", "role"))
            fields[marker] = EaField(
                type=_string(field_item["type"], path, marker_path + ".type"),
                role=_string(field_item["role"], path, marker_path + ".role"),
            )
        actual_markers = {
            character
            for pattern in patterns
            for character in pattern
            if character not in "01"
        }
        if set(fields) != actual_markers:
            raise DecodeError(
                f"{_where(path, item_path + '.fields')}: declarations differ from pattern"
            )
        update = None
        if "update" in item:
            raw_update = _mapping(item["update"], path, item_path + ".update")
            _keys(raw_update, path, item_path + ".update", required=("target", "mode"))
            target = _string(
                raw_update["target"], path, item_path + ".update.target"
            )
            if target not in fields:
                raise DecodeError(
                    f"{_where(path, item_path + '.update.target')}: unknown field"
                )
            mode = _enum_string(
                raw_update["mode"],
                path,
                item_path + ".update.mode",
                frozenset({"postincrement", "predecrement"}),
            )
            update = EaUpdate(target, mode)

        def optional_string(key: str) -> str | None:
            child = item.get(key)
            return (
                _string(child, path, item_path + "." + key)
                if child is not None
                else None
            )

        forms.append(
            EaForm(
                name=_string(item["name"], path, item_path + ".name"),
                pattern=patterns,
                syntax=_string(item["syntax"], path, item_path + ".syntax"),
                kind=optional_string("kind"),
                fields=fields,
                segment=optional_string("segment"),
                payload=optional_string("payload"),
                base=optional_string("base"),
                register=optional_string("register"),
                descriptor=optional_string("descriptor"),
                update=update,
            )
        )
    _unique((form.name for form in forms), path, field_path + ".name")
    return tuple(forms)


def decode_ea_registry(path: Path, raw: Any) -> EaRegistry:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("payloads", "compact", "ext0"))
    payloads: dict[str, EaPayload] = {}
    for name, value in _mapping(data["payloads"], path, "payloads").items():
        item_path = f"payloads.{name}"
        item = _validate_item_keys(
            path, item_path, value, required=("kind", "field_width", "signed")
        )
        payloads[name] = EaPayload(
            kind=_string(item["kind"], path, item_path + ".kind"),
            field_width=_positive_integer(
                item["field_width"], path, item_path + ".field_width"
            ),
            signed=_boolean(item["signed"], path, item_path + ".signed"),
        )
    compact_data = _mapping(data["compact"], path, "compact")
    _keys(compact_data, path, "compact", required=("field_width", "forms"))
    compact_width = _positive_integer(
        compact_data["field_width"], path, "compact.field_width"
    )
    compact_forms = _decode_ea_forms(
        compact_data["forms"],
        path,
        "compact.forms",
        compact=True,
        compact_width=compact_width,
    )
    ext0_data = _mapping(data["ext0"], path, "ext0")
    _keys(ext0_data, path, "ext0", required=("kind", "forms"))
    ext0_forms = _decode_ea_forms(
        ext0_data["forms"], path, "ext0.forms", compact=False
    )
    for form in compact_forms:
        if form.payload is not None and form.payload not in payloads:
            raise DecodeError(
                f"{_where(path, 'compact.forms')}: unknown payload {form.payload}"
            )
    return EaRegistry(
        payloads=payloads,
        compact_field_width=compact_width,
        compact_forms=compact_forms,
        ext0_kind=_string(ext0_data["kind"], path, "ext0.kind"),
        ext0_forms=ext0_forms,
    )


def decode_abi_vectors(path: Path, raw: Any) -> AbiVectorsDocument:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("ordinary_plt",))
    plt = _mapping(data["ordinary_plt"], path, "ordinary_plt")
    _keys(
        plt,
        path,
        "ordinary_plt",
        required=(
            "entry_size", "alignment", "instruction", "relocation", "padding",
            "got_slot", "relocation_vectors",
        ),
    )
    raw_instruction = _validate_item_keys(
        path,
        "ordinary_plt.instruction",
        plt["instruction"],
        required=("assembly", "offset", "opcode_bytes", "total_bytes", "displacement"),
    )
    raw_displacement = _validate_item_keys(
        path,
        "ordinary_plt.instruction.displacement",
        raw_instruction["displacement"],
        required=("offset", "width_bits", "byte_order"),
    )
    displacement = AbiDisplacement(
        offset=_nonnegative_integer(
            raw_displacement["offset"],
            path,
            "ordinary_plt.instruction.displacement.offset",
        ),
        width_bits=_positive_integer(
            raw_displacement["width_bits"],
            path,
            "ordinary_plt.instruction.displacement.width_bits",
        ),
        byte_order=_string(
            raw_displacement["byte_order"],
            path,
            "ordinary_plt.instruction.displacement.byte_order",
        ),
    )
    instruction = AbiInstruction(
        assembly=_string(
            raw_instruction["assembly"], path, "ordinary_plt.instruction.assembly"
        ),
        offset=_nonnegative_integer(
            raw_instruction["offset"], path, "ordinary_plt.instruction.offset"
        ),
        opcode_bytes=_byte_list(
            raw_instruction["opcode_bytes"],
            path,
            "ordinary_plt.instruction.opcode_bytes",
        ),
        total_bytes=_positive_integer(
            raw_instruction["total_bytes"],
            path,
            "ordinary_plt.instruction.total_bytes",
        ),
        displacement=displacement,
    )
    raw_relocation = _validate_item_keys(
        path,
        "ordinary_plt.relocation",
        plt["relocation"],
        required=("type", "place", "addend", "calculation", "effective_displacement"),
    )
    relocation = AbiRelocation(
        type=_string(raw_relocation["type"], path, "ordinary_plt.relocation.type"),
        place=_string(raw_relocation["place"], path, "ordinary_plt.relocation.place"),
        addend=_integer(raw_relocation["addend"], path, "ordinary_plt.relocation.addend"),
        calculation=_string(
            raw_relocation["calculation"], path, "ordinary_plt.relocation.calculation"
        ),
        effective_displacement=_string(
            raw_relocation["effective_displacement"],
            path,
            "ordinary_plt.relocation.effective_displacement",
        ),
    )
    raw_padding = _validate_item_keys(
        path,
        "ordinary_plt.padding",
        plt["padding"],
        required=("offset", "length", "byte"),
    )
    padding_byte = _integer(raw_padding["byte"], path, "ordinary_plt.padding.byte")
    if not 0 <= padding_byte <= 0xFF:
        raise DecodeError(f"{_where(path, 'ordinary_plt.padding.byte')}: byte out of range")
    padding = AbiPadding(
        offset=_nonnegative_integer(
            raw_padding["offset"], path, "ordinary_plt.padding.offset"
        ),
        length=_nonnegative_integer(
            raw_padding["length"], path, "ordinary_plt.padding.length"
        ),
        byte=padding_byte,
    )
    raw_got = _validate_item_keys(
        path,
        "ordinary_plt.got_slot",
        plt["got_slot"],
        required=("size", "alignment", "contents", "immutable_after_publication"),
    )
    got_slot = AbiGotSlot(
        size=_positive_integer(raw_got["size"], path, "ordinary_plt.got_slot.size"),
        alignment=_positive_integer(
            raw_got["alignment"], path, "ordinary_plt.got_slot.alignment"
        ),
        contents=_string(raw_got["contents"], path, "ordinary_plt.got_slot.contents"),
        immutable_after_publication=_boolean(
            raw_got["immutable_after_publication"],
            path,
            "ordinary_plt.got_slot.immutable_after_publication",
        ),
    )
    vectors: list[AbiRelocationVector] = []
    for index, value in enumerate(
        _list(plt["relocation_vectors"], path, "ordinary_plt.relocation_vectors")
    ):
        item_path = f"ordinary_plt.relocation_vectors[{index}]"
        item = _mapping(value, path, item_path)
        _keys(
            item,
            path,
            item_path,
            required=("entry_address", "got_slot_address", "place", "addend", "encoded_little_endian"),
            optional=("result", "result_signed"),
        )
        if ("result" in item) == ("result_signed" in item):
            raise DecodeError(
                f"{_where(path, item_path)}: exactly one of result/result_signed is required"
            )
        vectors.append(
            AbiRelocationVector(
                entry_address=_nonnegative_integer(
                    item["entry_address"], path, item_path + ".entry_address"
                ),
                got_slot_address=_nonnegative_integer(
                    item["got_slot_address"], path, item_path + ".got_slot_address"
                ),
                place=_nonnegative_integer(item["place"], path, item_path + ".place"),
                addend=_integer(item["addend"], path, item_path + ".addend"),
                encoded_little_endian=_byte_list(
                    item["encoded_little_endian"],
                    path,
                    item_path + ".encoded_little_endian",
                ),
                result=(
                    _integer(item["result"], path, item_path + ".result")
                    if "result" in item
                    else None
                ),
                result_signed=(
                    _integer(item["result_signed"], path, item_path + ".result_signed")
                    if "result_signed" in item
                    else None
                ),
            )
        )
    return AbiVectorsDocument(
        entry_size=_positive_integer(plt["entry_size"], path, "ordinary_plt.entry_size"),
        alignment=_positive_integer(plt["alignment"], path, "ordinary_plt.alignment"),
        instruction=instruction,
        relocation=relocation,
        padding=padding,
        got_slot=got_slot,
        relocation_vectors=tuple(vectors),
    )


def decode_memory_validation(path: Path, raw: Any) -> MemoryValidationDocument:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("status", "target", "litmus_families", "failure_action"))
    target = _mapping(data["target"], path, "target")
    target_fields = (
        "afence_is_full_cumulative",
        "one_global_sc_order",
        "isolated_fenced_scalar_is_sc",
        "failed_seqcst_cmpxchg_is_sc_load",
        "compare_exchange_uses_order_join",
        "failed_release_component_creates_release_sequence",
    )
    _keys(
        target,
        path,
        "target",
        required=target_fields,
    )
    target_document = MemoryValidationTarget(
        **{name: _boolean(target[name], path, f"target.{name}") for name in target_fields}
    )
    litmus_families: list[LitmusFamily] = []
    for index, value in enumerate(
        _list(data["litmus_families"], path, "litmus_families")
    ):
        item_path = f"litmus_families[{index}]"
        item = _validate_item_keys(path, item_path, value, required=("id", "purpose"))
        litmus_families.append(
            LitmusFamily(
                id=_string(item["id"], path, item_path + ".id"),
                purpose=_string(item["purpose"], path, item_path + ".purpose"),
            )
        )
    _unique((item.id for item in litmus_families), path, "litmus_families.id")
    failure_action = tuple(_string_list(data["failure_action"], path, "failure_action"))
    _unique(failure_action, path, "failure_action")
    return MemoryValidationDocument(
        status=_string(data["status"], path, "status"),
        target=target_document,
        litmus_families=tuple(litmus_families),
        failure_action=failure_action,
    )


def decode_yaml(path: Path) -> DecodedDocument:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise DecodeError(f"{path}: {exc}") from exc
    name = path.name
    if name == "instruction.yaml":
        return decode_instruction(path, raw)
    if name == "encodings.yaml":
        return decode_encodings(path, raw)
    if name == "instructions.yaml":
        return decode_instruction_index(path, raw)
    if name == "extension.yaml":
        return decode_extension_manifest(path, raw)
    if name == "extensions.yaml":
        return decode_extension_catalog(path, raw)
    if name == "operands.yaml":
        return decode_operand_registry(path, raw)
    if name == "sizes.yaml":
        return decode_size_registry(path, raw)
    if name == "registers.yaml":
        return decode_register_registry(path, raw)
    if name == "conditions.yaml":
        return decode_condition_registry(path, raw)
    if name == "ea.yaml":
        return decode_ea_registry(path, raw)
    if path.match("*/abi/plt_golden_vectors.yaml"):
        return decode_abi_vectors(path, raw)
    if path.match("*/memory_model/validation.yaml"):
        return decode_memory_validation(path, raw)
    raise DecodeError(f"{path}: unknown YAML document kind")
