"""Strict dataclass decoders for every supported ISA YAML document."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from pathlib import PurePosixPath
import re
from typing import Any, Iterable

import yaml


SCHEMA_FAMILIES = (
    "operation",
    "encodings",
    "instruction_index",
    "extension",
    "cpuid_flags",
    "operands",
    "sizes",
    "registers",
    "conditions",
    "semantic_conditions",
    "named_values",
    "flag_effect_definitions",
    "effective_address",
    "abi_vectors",
    "memory_validation",
)
SCHEMA_LOCK_PATH = (
    Path(__file__).resolve().parents[1] / "instructions" / "definitions" / "schema.lock"
)
SCHEMA_DOCUMENT_PATH = (
    Path(__file__).resolve().parents[1] / "instructions" / "definitions" / "SCHEMA.md"
)

PRIVILEGES = frozenset({"unprivileged", "supervisor", "any"})
REPEAT_CONTEXTS = frozenset({"REP", "REPcc"})
REPEAT_OBSERVED_KINDS = frozenset({"computed", "result", "source"})
DESTINATION_OVERLAP_RULES = frozenset({"same_value", "illegal_instruction"})
OPERAND_ACCESS = frozenset({"read", "write", "read_write", "address"})
OPERAND_DOMAINS = frozenset({"user"})
EA_ROLES = frozenset({"value", "address", "control_target"})
EA_WIDTHS = frozenset({"operation_size", "predicate", "B", "W", "L", "Q"})
EA_OPERAND_TYPES = frozenset({"EA", "FEA", "VEA"})
EA_PROFILES = frozenset({"ea", "fea", "vea"})
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
FLAG_BANK_FLAGS = {
    "FLAGS": ("Z", "N", "C", "V"),
    "FFLAGS": ("NV", "DZ", "OF", "UF", "NX"),
}
OPERATION_ROLES = frozenset(
    {
        "source",
        "destination",
        "address",
        "control_target",
        "governing_predicate",
        "count",
        "bit_index",
        "segment_selector",
        "counter",
        "implicit",
    }
)
OPERATION_REPEAT_KINDS = frozenset({"not_eligible", "rep", "rep_and_repcc"})
EXECUTION_ROUTE_CONSTRUCTORS = {
    "atomics": "RouteAtomics",
    "bounds": "RouteBounds",
    "cache": "RouteCache",
    "control_flow": "RouteControlFlow",
    "core_control": "RouteCoreControl",
    "data_movement": "RouteDataMovement",
    "ea_utility": "RouteEaUtility",
    "fpu": "RouteFpu",
    "fpu_transcendental_approx": "RouteFpuTranscendental",
    "integer_alu": "RouteIntegerAlu",
    "integer_bitfield": "RouteIntegerBitfield",
    "integer_mul_div": "RouteIntegerMulDiv",
    "integer_unary": "RouteIntegerUnary",
    "system_registers": "RouteSystemRegisters",
    "tlb_and_context": "RouteTlbContext",
    "vector": "RouteVector",
}
EXECUTION_ROUTES = frozenset(EXECUTION_ROUTE_CONSTRUCTORS)
OPERATION_VALUE_DOMAINS = frozenset(
    {"integer", "floating", "vector", "predicate"}
)
NUMERIC_VALUE_DOMAINS = frozenset({"integer", "floating"})
NUMERIC_FORMAT_CODES = frozenset({"B", "W", "L", "Q", "H", "S", "D"})
CONVERSION_BEHAVIORS = frozenset(
    {"exact", "sign_extend", "zero_extend", "convert"}
)
PREDICATE_KINDS = frozenset(
    {
        "none",
        "annul_on_false",
        "produce_boolean",
        "test_temporary",
        "counter_and_condition",
    }
)
FLAG_BANK_COMPLETION_KINDS = frozenset({"complete_image", "accrued_causes"})
FLAG_EFFECT_KINDS = frozenset(
    {
        "preserve",
        "clear",
        "set",
        "write_expression",
        "write_condition",
        "accrue_source",
    }
)
FLAG_EFFECT_DEFINITION_KINDS = frozenset(
    {"expression", "condition", "accrued_source"}
)
NAMED_VALUE_KINDS = frozenset({"condition_code_image"})
FLAG_EFFECT_REFERENCE_KIND = {
    "write_expression": "expression",
    "write_condition": "condition",
    "accrue_source": "accrued_source",
}
DESCRIPTION_ARTIFACT_KINDS = frozenset({"tex", "markdown"})


class DecodeError(ValueError):
    """A YAML document does not satisfy its declared shape."""


@dataclass(frozen=True)
class AssemblyTemplateOperand:
    """One parsed operand or operand-group node in an assembly template."""

    kind: str
    name: str | None = None
    angled: bool = False
    field: str | None = None
    literal: int | None = None
    group_style: str | None = None
    members: tuple["AssemblyTemplateOperand", ...] = ()


@dataclass(frozen=True)
class AssemblyTemplate:
    """Parsed canonical assembly-template structure."""

    mnemonic: str
    fixed_size_suffix: str | None = None
    selected_size_codes: tuple[str, ...] = ()
    size_field: str | None = None
    order_field: str | None = None
    operands: tuple[AssemblyTemplateOperand, ...] = ()


class _AssemblyTemplateParser:
    def __init__(self, value: str, source: str) -> None:
        self.value = value
        self.source = source
        self.index = 0

    def fail(self, message: str) -> None:
        raise DecodeError(f"{self.source}: {message} at character {self.index + 1}")

    def take(self, literal: str) -> bool:
        if self.value.startswith(literal, self.index):
            self.index += len(literal)
            return True
        return False

    def require(self, literal: str) -> None:
        if not self.take(literal):
            self.fail(f"expected {literal!r}")

    def identifier(self, label: str, *, mnemonic: bool = False) -> str:
        pattern = r"[A-Za-z][A-Za-z0-9]*" if mnemonic else r"[A-Za-z][A-Za-z0-9_]*"
        match = re.match(pattern, self.value[self.index :])
        if match is None:
            self.fail(f"expected {label}")
        result = match.group(0)
        self.index += len(result)
        return result

    def field_expression(self) -> str:
        self.require("(")
        if self.index >= len(self.value) or self.value[self.index] not in "abcdefghijklmnopqrstuvwxyz":
            self.fail("expected lowercase field marker")
        marker = self.value[self.index]
        self.index += 1
        self.require(")")
        return marker

    def operand_reference(self) -> tuple[str, bool]:
        angled = self.take("<")
        name = self.identifier("operand name")
        if angled:
            self.require(">")
        return name, angled

    def address_expression(self, kind: str) -> AssemblyTemplateOperand:
        members: list[AssemblyTemplateOperand] = []
        while True:
            if self.index >= len(self.value):
                self.fail("unterminated address expression")
            if self.take("]"):
                return AssemblyTemplateOperand(kind=kind, members=tuple(members))
            if self.value[self.index].isspace():
                self.index += 1
                continue
            if self.take("["):
                members.append(self.address_expression("lane_index"))
                continue
            if self.value[self.index] in "+*":
                members.append(
                    AssemblyTemplateOperand(
                        kind="operator", name=self.value[self.index]
                    )
                )
                self.index += 1
                continue
            decimal = re.match(r"[0-9]+", self.value[self.index :])
            if decimal is not None:
                spelling = decimal.group(0)
                self.index += len(spelling)
                members.append(
                    AssemblyTemplateOperand(kind="decimal", literal=int(spelling, 10))
                )
                continue
            name, angled = self.operand_reference()
            marker = (
                self.field_expression()
                if self.index < len(self.value) and self.value[self.index] == "("
                else None
            )
            members.append(
                AssemblyTemplateOperand(
                    kind="scale" if name == "scale" else "reference",
                    name=name,
                    angled=angled,
                    field=marker,
                )
            )

    def operand(self) -> AssemblyTemplateOperand:
        if self.take("["):
            return self.address_expression("address")
        if self.take("{ "):
            name, angled = self.operand_reference()
            self.require("... }")
            return AssemblyTemplateOperand(
                kind="group", name=name, angled=angled, group_style="braced"
            )
        if self.take("("):
            name, angled = self.operand_reference()
            self.require(")")
            return AssemblyTemplateOperand(
                kind="group", name=name, angled=angled, group_style="parenthesized"
            )
        decimal = re.match(r"[0-9]+", self.value[self.index :])
        if decimal is not None:
            spelling = decimal.group(0)
            self.index += len(spelling)
            return AssemblyTemplateOperand(kind="decimal", literal=int(spelling, 10))
        name, angled = self.operand_reference()
        marker = self.field_expression() if self.index < len(self.value) and self.value[self.index] == "(" else None
        return AssemblyTemplateOperand(
            kind="reference", name=name, angled=angled, field=marker
        )

    def parse(self) -> AssemblyTemplate:
        mnemonic = self.identifier("mnemonic name", mnemonic=True)
        fixed_size_suffix: str | None = None
        selected_size_codes: tuple[str, ...] = ()
        size_field: str | None = None
        order_field: str | None = None
        if self.take("."):
            if self.take("{"):
                codes = [self.identifier("public size suffix")]
                while self.take("|"):
                    codes.append(self.identifier("public size suffix"))
                self.require("}")
                if len(set(codes)) != len(codes):
                    self.fail("repeated public size suffix")
                selected_size_codes = tuple(codes)
                size_field = self.field_expression()
                if self.take("/order"):
                    order_field = self.field_expression()
            else:
                fixed_size_suffix = "." + self.identifier("fixed size suffix")

        operands: list[AssemblyTemplateOperand] = []
        if self.index < len(self.value):
            self.require(" ")
            operands.append(self.operand())
            while self.index < len(self.value):
                self.require(", ")
                operands.append(self.operand())
        if self.index != len(self.value):
            self.fail("unexpected text")
        return AssemblyTemplate(
            mnemonic=mnemonic,
            fixed_size_suffix=fixed_size_suffix,
            selected_size_codes=selected_size_codes,
            size_field=size_field,
            order_field=order_field,
            operands=tuple(operands),
        )


def parse_assembly_template(value: str, source: str = "assembly template") -> AssemblyTemplate:
    """Parse one value using the canonical assembly-template grammar."""

    if not isinstance(value, str) or not value:
        raise DecodeError(f"{source}: expected non-empty string")
    return _AssemblyTemplateParser(value, source).parse()


def displayed_assembly_operands(
    template: AssemblyTemplate,
) -> tuple[AssemblyTemplateOperand, ...]:
    """Return displayed operands with bracketed address members flattened in order."""

    def address_references(
        operand: AssemblyTemplateOperand,
    ) -> list[AssemblyTemplateOperand]:
        result: list[AssemblyTemplateOperand] = []
        for member in operand.members:
            if member.kind == "reference":
                result.append(member)
            elif member.kind == "lane_index":
                result.extend(address_references(member))
        return result

    result: list[AssemblyTemplateOperand] = []
    for operand in template.operands:
        if operand.kind == "address":
            result.extend(address_references(operand))
        elif operand.kind != "group":
            result.append(operand)
    return tuple(result)


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
    expected_keys = {"families", "decoder_sha256", "diagram_decoder_sha256", "contract_sha256"}
    if set(values) != expected_keys:
        raise DecodeError(f"{lock_path}: expected fields {', '.join(sorted(expected_keys))}")
    try:
        family_count = int(values["families"])
    except ValueError as exc:
        raise DecodeError(f"{lock_path}: families must be an integer") from exc
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
            f"{lock_path}: decoder changed without updating the schema lock"
        )
    diagram_digest = hashlib.sha256(
        Path(__file__).with_name("vector_diagrams.py").read_bytes()
    ).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", values["diagram_decoder_sha256"]):
        raise DecodeError(f"{lock_path}: invalid diagram_decoder_sha256")
    if values["diagram_decoder_sha256"] != diagram_digest:
        raise DecodeError(
            f"{lock_path}: vector diagram decoder changed without updating the schema lock"
        )
    contract_digest = hashlib.sha256(SCHEMA_DOCUMENT_PATH.read_bytes()).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", values["contract_sha256"]):
        raise DecodeError(f"{lock_path}: invalid contract_sha256")
    if values["contract_sha256"] != contract_digest:
        raise DecodeError(
            f"{lock_path}: displayed contract changed without updating the schema lock"
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
class PublicInstructionRef:
    mnemonic: str
    aliases: tuple[str, ...] = ()
    width_suffix_aliases: bool = False


@dataclass(frozen=True)
class OperationComputedRepeatObservation:
    kind: str = field(default="computed", init=False)


@dataclass(frozen=True)
class OperationResultRepeatObservation:
    operand: str
    kind: str = field(default="result", init=False)


@dataclass(frozen=True)
class OperationSourceRepeatObservation:
    operand: str
    kind: str = field(default="source", init=False)


OperationRepeatObservation = (
    OperationComputedRepeatObservation
    | OperationResultRepeatObservation
    | OperationSourceRepeatObservation
)


@dataclass(frozen=True)
class OperationRepeatEligibility:
    kind: str
    observed: OperationRepeatObservation | None = None


@dataclass(frozen=True)
class LogicalOperandDefinition:
    id: str
    role: str
    access: str
    value_domain: str
    profiles: tuple[str, ...]


@dataclass(frozen=True)
class SelectorApplicability:
    domain: str
    values: tuple[str, ...]


@dataclass(frozen=True)
class OperandProfileApplicability:
    operand: str
    profiles: tuple[str, ...]


@dataclass(frozen=True)
class FormApplicability:
    forms: tuple[str, ...]
    selectors: tuple[SelectorApplicability, ...] = ()
    operand_profiles: tuple[OperandProfileApplicability, ...] = ()


@dataclass(frozen=True)
class PredicateContract:
    kind: str
    condition_operand: str | None = None
    destination_operand: str | None = None
    counter_operand: str | None = None
    observed: str | None = None


@dataclass(frozen=True)
class OperationFlagEffect:
    flag: str
    effect: str
    reference: str | None = None


@dataclass(frozen=True)
class OperationFlagBankContract:
    bank: str
    completion: str
    effects: tuple[OperationFlagEffect, ...]


@dataclass(frozen=True)
class OperationEventContract:
    event: str
    condition: str
    cause: str | None = None


@dataclass(frozen=True)
class ConversionSignature:
    """Typed numeric conversion owned by one operation case.

    Formats use the public size-code vocabulary. Selector-domain names remain
    encoding implementation detail; the loader relates this signature to the
    selected codes of each applicable form.
    """

    source_domain: str
    source_formats: tuple[str, ...]
    destination_domain: str
    destination_formats: tuple[str, ...]
    integer_signedness: str | None
    behavior: str


@dataclass(frozen=True)
class OperationCase:
    id: str
    applies_to: FormApplicability
    additional_requirements: tuple[str, ...]
    predicate: PredicateContract
    flags: tuple[OperationFlagBankContract, ...]
    events: tuple[OperationEventContract, ...]
    sail_entry: str
    conversion: ConversionSignature | None = None


@dataclass(frozen=True)
class OperationArtifactRef:
    path: str
    kind: str


@dataclass(frozen=True)
class DiagramArtifactRef:
    id: str
    path: str
    kind: str
    case: str | None
    caption: str
    alt_text: str


@dataclass(frozen=True)
class OperationArtifacts:
    semantics: OperationArtifactRef
    description: OperationArtifactRef
    diagrams: tuple[DiagramArtifactRef, ...] = ()
    bundle_root: str | None = None
    manifest_path: str | None = None


@dataclass(frozen=True)
class OperationDocument:
    id: str
    title: str
    summary: str
    public_instruction: PublicInstructionRef
    execution_route: str
    privilege: str
    repeat: OperationRepeatEligibility
    operands: tuple[LogicalOperandDefinition, ...]
    cases: tuple[OperationCase, ...]
    artifacts: OperationArtifacts


@dataclass(frozen=True)
class SemanticConditionDefinition:
    id: str
    reader_text: str


@dataclass(frozen=True)
class SemanticConditionRegistry:
    conditions: tuple[SemanticConditionDefinition, ...]


@dataclass(frozen=True)
class NamedValueDefinition:
    id: str
    kind: str
    reader_term: str


@dataclass(frozen=True)
class NamedValueRegistry:
    values: tuple[NamedValueDefinition, ...]


@dataclass(frozen=True)
class FlagEffectDefinition:
    id: str
    kind: str
    reader_text: str


@dataclass(frozen=True)
class FlagEffectDefinitionRegistry:
    definitions: tuple[FlagEffectDefinition, ...]


@dataclass(frozen=True)
class EncodingOperand:
    name: str
    type: str
    access: str
    field: str | None = None
    domain: str | None = None
    ea_role: str | None = None
    ea_width: str | None = None


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
class DestinationOverlap:
    operands: tuple[str, str]
    rule: str


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
    destination_overlap: tuple[DestinationOverlap, ...] = ()


@dataclass(frozen=True)
class EncodingsDocument:
    forms: tuple[EncodingForm, ...]


@dataclass(frozen=True)
class InstructionSetIndex:
    title: str
    include: tuple[str, ...]
    introduction: str | None = None


@dataclass(frozen=True)
class CpuidFlagLocation:
    selector_class: int
    leaf: int
    index: int
    bit: int


@dataclass(frozen=True)
class CpuidFlag:
    id: str
    token: str
    location: CpuidFlagLocation


@dataclass(frozen=True)
class CpuidFlagRegistry:
    cpuid_flags: tuple[CpuidFlag, ...]


@dataclass(frozen=True)
class ExtensionAvailability:
    required_cpuid_flags: tuple[str, ...]


@dataclass(frozen=True)
class ExtensionManifest:
    name: str
    instructions: str | None = None
    operands: str | None = None
    registers: str | None = None
    sizes: str | None = None
    extensions: tuple[str, ...] = ()
    availability: ExtensionAvailability | None = None


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
    bit_width: int
    register_group: str | None = None
    register: str | None = None
    encoding_ref: str | None = None
    profile: str | None = None
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
    values: tuple[SizeKindValue, ...]
    reserved_values: tuple[SizeKindValue, ...] = ()


@dataclass(frozen=True)
class SizeRegistry:
    size_codes: dict[str, SizeCode]
    size_kinds: dict[str, SizeKind]


@dataclass(frozen=True)
class RegisterEntry:
    name: str
    width: int | str
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
    bit_width: int
    signed: bool
    format: str | None = None


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
class EaProfileOverride:
    pattern: str
    reserved: bool
    form: EaForm | None = None


@dataclass(frozen=True)
class EaProfile:
    name: str
    operand_type: str
    overrides: tuple[EaProfileOverride, ...]
    immediate_conversion: str | None = None
    lane_model: str | None = None
    base_update: str | None = None
    index_update: str | None = None
    predicate_affects_update: bool | None = None
    scatter_gather: str | None = None


@dataclass(frozen=True)
class EaRegistry:
    payloads: dict[str, EaPayload]
    compact_field_width: int
    compact_forms: tuple[EaForm, ...]
    compact_profiles: dict[str, EaProfile]
    ext1_kind: str
    ext1_forms: tuple[EaForm, ...]
    ext2_kind: str
    ext2_forms: tuple[EaForm, ...]


@dataclass(frozen=True)
class AbiDisplacement:
    offset: int
    width_bits: int
    byte_order: str


@dataclass(frozen=True)
class AbiInstruction:
    assembly: str
    offset: int
    opcode_space_bytes: tuple[int, ...]
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
    OperationDocument
    | EncodingsDocument
    | InstructionSetIndex
    | ExtensionManifest
    | ExtensionCatalog
    | CpuidFlagRegistry
    | OperandRegistry
    | SizeRegistry
    | RegisterRegistry
    | ConditionRegistry
    | SemanticConditionRegistry
    | NamedValueRegistry
    | FlagEffectDefinitionRegistry
    | EaRegistry
    | AbiVectorsDocument
    | MemoryValidationDocument
)


def _stable_id(value: Any, path: Path, field_path: str) -> str:
    result = _string(value, path, field_path)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", result):
        raise DecodeError(f"{_where(path, field_path)}: invalid stable identifier")
    return result


def decode_operation(path: Path, raw: Any) -> OperationDocument:
    """Strictly decode one canonical operation bundle manifest."""

    data = _mapping(raw, path, "")
    _keys(
        data,
        path,
        "",
        required=(
            "operation",
            "title",
            "summary",
            "public_instruction",
            "execution_route",
            "privilege",
            "repeat",
            "operands",
            "cases",
            "artifacts",
        ),
    )
    operation_id = _stable_id(data["operation"], path, "operation")
    title = _string(data["title"], path, "title")
    summary = _string(data["summary"], path, "summary")

    public_raw = _mapping(data["public_instruction"], path, "public_instruction")
    _keys(
        public_raw,
        path,
        "public_instruction",
        required=("mnemonic",),
        optional=("aliases", "width_suffix_aliases"),
    )
    mnemonic = _string(public_raw["mnemonic"], path, "public_instruction.mnemonic")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", mnemonic):
        raise DecodeError(
            f"{_where(path, 'public_instruction.mnemonic')}: invalid mnemonic"
        )
    aliases = tuple(
        _string_list(public_raw.get("aliases", []), path, "public_instruction.aliases")
    )
    _unique(aliases, path, "public_instruction.aliases")
    if mnemonic in aliases:
        raise DecodeError(
            f"{_where(path, 'public_instruction.aliases')}: canonical mnemonic cannot be an alias"
        )
    width_suffix_aliases = public_raw.get("width_suffix_aliases", False)
    if not isinstance(width_suffix_aliases, bool):
        raise DecodeError(
            f"{_where(path, 'public_instruction.width_suffix_aliases')}: expected boolean"
        )
    for index, alias in enumerate(aliases):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", alias):
            raise DecodeError(
                f"{_where(path, f'public_instruction.aliases[{index}]')}: invalid mnemonic"
            )

    repeat_raw = _mapping(data["repeat"], path, "repeat")
    _keys(repeat_raw, path, "repeat", required=("kind",), optional=("observed",))
    repeat_kind = _enum_string(
        repeat_raw["kind"], path, "repeat.kind", OPERATION_REPEAT_KINDS
    )
    repeat_observed: OperationRepeatObservation | None = None
    if "observed" in repeat_raw:
        observed_raw = _mapping(repeat_raw["observed"], path, "repeat.observed")
        _keys(
            observed_raw,
            path,
            "repeat.observed",
            required=("kind",),
            optional=("operand",),
        )
        observed_kind = _enum_string(
            observed_raw["kind"],
            path,
            "repeat.observed.kind",
            REPEAT_OBSERVED_KINDS,
        )
        observed_operand = observed_raw.get("operand")
        if observed_operand is not None:
            observed_operand = _stable_id(
                observed_operand, path, "repeat.observed.operand"
            )
        if observed_kind == "computed" and observed_operand is not None:
            raise DecodeError(
                f"{_where(path, 'repeat.observed')}: computed observation has no operand"
            )
        if observed_kind in {"result", "source"} and observed_operand is None:
            raise DecodeError(
                f"{_where(path, 'repeat.observed')}: {observed_kind} observation requires exactly operand"
            )
        if observed_kind == "computed":
            repeat_observed = OperationComputedRepeatObservation()
        elif observed_kind == "result":
            assert observed_operand is not None
            repeat_observed = OperationResultRepeatObservation(observed_operand)
        else:
            assert observed_operand is not None
            repeat_observed = OperationSourceRepeatObservation(observed_operand)
    if (repeat_kind == "rep_and_repcc") != (repeat_observed is not None):
        raise DecodeError(
            f"{_where(path, 'repeat')}: observed is required exactly for rep_and_repcc"
        )

    operands: list[LogicalOperandDefinition] = []
    for index, raw_operand in enumerate(_list(data["operands"], path, "operands")):
        item_path = f"operands[{index}]"
        item = _mapping(raw_operand, path, item_path)
        _keys(
            item,
            path,
            item_path,
            required=("id", "role", "access", "value_domain", "profiles"),
        )
        profiles = tuple(
            _stable_id(value, path, f"{item_path}.profiles[{profile_index}]")
            for profile_index, value in enumerate(
                _list(item["profiles"], path, item_path + ".profiles")
            )
        )
        if not profiles:
            raise DecodeError(f"{_where(path, item_path + '.profiles')}: expected non-empty list")
        _unique(profiles, path, item_path + ".profiles")
        operands.append(
            LogicalOperandDefinition(
                id=_stable_id(item["id"], path, item_path + ".id"),
                role=_enum_string(item["role"], path, item_path + ".role", OPERATION_ROLES),
                access=_enum_string(item["access"], path, item_path + ".access", OPERAND_ACCESS),
                value_domain=_enum_string(
                    item["value_domain"],
                    path,
                    item_path + ".value_domain",
                    OPERATION_VALUE_DOMAINS,
                ),
                profiles=profiles,
            )
        )
    _unique((operand.id for operand in operands), path, "operands.id")
    operand_ids = {operand.id for operand in operands}
    repeat_operand = getattr(repeat_observed, "operand", None)
    if repeat_operand is not None and repeat_operand not in operand_ids:
        raise DecodeError(
            f"{_where(path, 'repeat.observed.operand')}: unknown logical operand"
        )

    cases: list[OperationCase] = []
    for case_index, raw_case in enumerate(_list(data["cases"], path, "cases")):
        case_path = f"cases[{case_index}]"
        item = _mapping(raw_case, path, case_path)
        _keys(
            item,
            path,
            case_path,
            required=(
                "id",
                "applies_to",
                "additional_requirements",
                "predicate",
                "flags",
                "events",
                "sail_entry",
            ),
            optional=("conversion",),
        )
        applies_raw = _mapping(item["applies_to"], path, case_path + ".applies_to")
        _keys(
            applies_raw,
            path,
            case_path + ".applies_to",
            required=("forms",),
            optional=("selectors", "operand_profiles"),
        )
        applies_forms = tuple(
            _string(value, path, f"{case_path}.applies_to.forms[{index}]")
            for index, value in enumerate(
                _list(applies_raw["forms"], path, case_path + ".applies_to.forms")
            )
        )
        if not applies_forms:
            raise DecodeError(
                f"{_where(path, case_path + '.applies_to.forms')}: expected non-empty list"
            )
        for form_index, form_id in enumerate(applies_forms):
            if not re.fullmatch(r"[a-z][a-z0-9_]*\.[a-z0-9_.]+", form_id):
                raise DecodeError(
                    f"{_where(path, f'{case_path}.applies_to.forms[{form_index}]')}: "
                    "invalid stable form id"
                )
        _unique(applies_forms, path, case_path + ".applies_to.forms")

        selectors: list[SelectorApplicability] = []
        for selector_index, raw_selector in enumerate(
            _list(applies_raw.get("selectors", []), path, case_path + ".applies_to.selectors")
        ):
            selector_path = f"{case_path}.applies_to.selectors[{selector_index}]"
            selector = _mapping(raw_selector, path, selector_path)
            _keys(selector, path, selector_path, required=("domain", "values"))
            values = tuple(
                _stable_id(value, path, f"{selector_path}.values[{index}]")
                for index, value in enumerate(
                    _list(selector["values"], path, selector_path + ".values")
                )
            )
            if not values:
                raise DecodeError(f"{_where(path, selector_path + '.values')}: expected non-empty list")
            _unique(values, path, selector_path + ".values")
            selectors.append(
                SelectorApplicability(
                    _stable_id(selector["domain"], path, selector_path + ".domain"),
                    values,
                )
            )
        _unique((selector.domain for selector in selectors), path, case_path + ".applies_to.selectors.domain")

        operand_profiles: list[OperandProfileApplicability] = []
        for profile_index, raw_profile in enumerate(
            _list(
                applies_raw.get("operand_profiles", []),
                path,
                case_path + ".applies_to.operand_profiles",
            )
        ):
            profile_path = f"{case_path}.applies_to.operand_profiles[{profile_index}]"
            profile = _mapping(raw_profile, path, profile_path)
            _keys(profile, path, profile_path, required=("operand", "profiles"))
            operand = _stable_id(profile["operand"], path, profile_path + ".operand")
            if operand not in operand_ids:
                raise DecodeError(f"{_where(path, profile_path + '.operand')}: unknown logical operand")
            profile_values = tuple(
                _stable_id(value, path, f"{profile_path}.profiles[{index}]")
                for index, value in enumerate(
                    _list(profile["profiles"], path, profile_path + ".profiles")
                )
            )
            if not profile_values:
                raise DecodeError(f"{_where(path, profile_path + '.profiles')}: expected non-empty list")
            _unique(profile_values, path, profile_path + ".profiles")
            operand_profiles.append(OperandProfileApplicability(operand, profile_values))
        _unique((selector.operand for selector in operand_profiles), path, case_path + ".applies_to.operand_profiles.operand")

        predicate_raw = _mapping(item["predicate"], path, case_path + ".predicate")
        _keys(
            predicate_raw,
            path,
            case_path + ".predicate",
            required=("kind",),
            optional=("condition_operand", "destination_operand", "counter_operand", "observed"),
        )
        predicate_kind = _enum_string(
            predicate_raw["kind"], path, case_path + ".predicate.kind", PREDICATE_KINDS
        )
        predicate_refs: dict[str, str | None] = {}
        for key in ("condition_operand", "destination_operand", "counter_operand"):
            value = predicate_raw.get(key)
            predicate_refs[key] = (
                _stable_id(value, path, case_path + f".predicate.{key}")
                if value is not None
                else None
            )
            if predicate_refs[key] is not None and predicate_refs[key] not in operand_ids:
                raise DecodeError(
                    f"{_where(path, case_path + f'.predicate.{key}')}: unknown logical operand"
                )
        observed_value = predicate_raw.get("observed")
        observed_value = (
            _stable_id(observed_value, path, case_path + ".predicate.observed")
            if observed_value is not None
            else None
        )
        required_predicate_fields = {
            "none": set(),
            "annul_on_false": {"condition_operand"},
            "produce_boolean": {"condition_operand", "destination_operand"},
            "test_temporary": {"condition_operand", "observed"},
            "counter_and_condition": {"counter_operand", "condition_operand"},
        }[predicate_kind]
        present_predicate_fields = {
            key for key, value in {**predicate_refs, "observed": observed_value}.items() if value is not None
        }
        if present_predicate_fields != required_predicate_fields:
            raise DecodeError(
                f"{_where(path, case_path + '.predicate')}: {predicate_kind} requires exactly "
                f"{', '.join(sorted(required_predicate_fields)) or 'no reference fields'}"
            )

        flags: list[OperationFlagBankContract] = []
        for bank_index, raw_bank in enumerate(_list(item["flags"], path, case_path + ".flags")):
            bank_path = f"{case_path}.flags[{bank_index}]"
            bank = _mapping(raw_bank, path, bank_path)
            _keys(bank, path, bank_path, required=("bank", "completion", "effects"))
            bank_name = _enum_string(
                bank["bank"], path, bank_path + ".bank", frozenset(FLAG_BANK_FLAGS)
            )
            completion = _enum_string(
                bank["completion"],
                path,
                bank_path + ".completion",
                FLAG_BANK_COMPLETION_KINDS,
            )
            expected_completion = {
                "FLAGS": "complete_image",
                "FFLAGS": "accrued_causes",
            }[bank_name]
            if completion != expected_completion:
                raise DecodeError(
                    f"{_where(path, bank_path + '.completion')}: {bank_name} requires "
                    f"{expected_completion}"
                )
            effects: list[OperationFlagEffect] = []
            for effect_index, raw_effect in enumerate(
                _list(bank["effects"], path, bank_path + ".effects")
            ):
                effect_path = f"{bank_path}.effects[{effect_index}]"
                effect = _mapping(raw_effect, path, effect_path)
                _keys(
                    effect,
                    path,
                    effect_path,
                    required=("flag", "effect"),
                    optional=("reference",),
                )
                flag_name = _enum_string(
                    effect["flag"],
                    path,
                    effect_path + ".flag",
                    frozenset(FLAG_BANK_FLAGS[bank_name]),
                )
                effect_kind = _enum_string(
                    effect["effect"], path, effect_path + ".effect", FLAG_EFFECT_KINDS
                )
                reference = effect.get("reference")
                if reference is not None:
                    reference = _stable_id(
                        reference, path, effect_path + ".reference"
                    )
                requires_reference = effect_kind in FLAG_EFFECT_REFERENCE_KIND
                if requires_reference != (reference is not None):
                    raise DecodeError(
                        f"{_where(path, effect_path)}: {effect_kind} requires exactly "
                        f"{'reference' if requires_reference else 'no reference fields'}"
                    )
                allowed_effects = (
                    {"preserve", "accrue_source"}
                    if completion == "accrued_causes"
                    else {
                        "preserve",
                        "clear",
                        "set",
                        "write_expression",
                        "write_condition",
                    }
                )
                if effect_kind not in allowed_effects:
                    raise DecodeError(
                        f"{_where(path, effect_path + '.effect')}: {effect_kind} is not "
                        f"valid for {completion}"
                    )
                effects.append(OperationFlagEffect(flag_name, effect_kind, reference))
            if not effects:
                raise DecodeError(f"{_where(path, bank_path + '.effects')}: expected non-empty list")
            _unique((effect.flag for effect in effects), path, bank_path + ".effects.flag")
            effects_by_flag = {effect.flag: effect for effect in effects}
            flags.append(
                OperationFlagBankContract(
                    bank_name,
                    completion,
                    tuple(
                        effects_by_flag.get(
                            flag_name,
                            OperationFlagEffect(flag_name, "preserve"),
                        )
                        for flag_name in FLAG_BANK_FLAGS[bank_name]
                    ),
                )
            )
        _unique((bank.bank for bank in flags), path, case_path + ".flags.bank")

        events: list[OperationEventContract] = []
        for event_index, raw_event in enumerate(_list(item["events"], path, case_path + ".events")):
            event_path = f"{case_path}.events[{event_index}]"
            event = _mapping(raw_event, path, event_path)
            _keys(
                event,
                path,
                event_path,
                required=("event", "condition"),
                optional=("cause",),
            )
            event_name = _string(event["event"], path, event_path + ".event")
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", event_name):
                raise DecodeError(f"{_where(path, event_path + '.event')}: invalid event name")
            cause = (
                _string(event["cause"], path, event_path + ".cause")
                if "cause" in event
                else None
            )
            if cause is not None and not re.fullmatch(r"[A-Z][A-Z0-9_]*", cause):
                raise DecodeError(f"{_where(path, event_path + '.cause')}: invalid cause name")
            events.append(
                OperationEventContract(
                    event_name,
                    _stable_id(event["condition"], path, event_path + ".condition"),
                    cause,
                )
            )
        _unique(
            ((event.event, event.condition) for event in events),
            path,
            case_path + ".events",
        )

        requirements = tuple(
            _stable_id(value, path, f"{case_path}.additional_requirements[{index}]")
            for index, value in enumerate(
                _list(item["additional_requirements"], path, case_path + ".additional_requirements")
            )
        )
        _unique(requirements, path, case_path + ".additional_requirements")
        sail_entry = _string(item["sail_entry"], path, case_path + ".sail_entry")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", sail_entry):
            raise DecodeError(f"{_where(path, case_path + '.sail_entry')}: invalid Sail identifier")
        conversion: ConversionSignature | None = None
        if "conversion" in item:
            conversion_raw = _mapping(item["conversion"], path, case_path + ".conversion")
            _keys(
                conversion_raw,
                path,
                case_path + ".conversion",
                required=(
                    "source_domain",
                    "source_formats",
                    "destination_domain",
                    "destination_formats",
                    "behavior",
                ),
                optional=("integer_signedness",),
            )
            source_formats = tuple(
                _enum_string(
                    value,
                    path,
                    f"{case_path}.conversion.source_formats[{index}]",
                    NUMERIC_FORMAT_CODES,
                )
                for index, value in enumerate(
                    _list(
                        conversion_raw["source_formats"],
                        path,
                        case_path + ".conversion.source_formats",
                    )
                )
            )
            destination_formats = tuple(
                _enum_string(
                    value,
                    path,
                    f"{case_path}.conversion.destination_formats[{index}]",
                    NUMERIC_FORMAT_CODES,
                )
                for index, value in enumerate(
                    _list(
                        conversion_raw["destination_formats"],
                        path,
                        case_path + ".conversion.destination_formats",
                    )
                )
            )
            if not source_formats or not destination_formats:
                raise DecodeError(
                    f"{_where(path, case_path + '.conversion')}: source and destination formats must be non-empty"
                )
            _unique(source_formats, path, case_path + ".conversion.source_formats")
            _unique(destination_formats, path, case_path + ".conversion.destination_formats")
            source_domain = _enum_string(
                conversion_raw["source_domain"], path,
                case_path + ".conversion.source_domain", NUMERIC_VALUE_DOMAINS,
            )
            destination_domain = _enum_string(
                conversion_raw["destination_domain"], path,
                case_path + ".conversion.destination_domain", NUMERIC_VALUE_DOMAINS,
            )
            integer_signedness = conversion_raw.get("integer_signedness")
            if source_domain == "integer" or destination_domain == "integer":
                integer_signedness = _enum_string(
                    integer_signedness, path,
                    case_path + ".conversion.integer_signedness", {"signed", "unsigned"},
                )
            elif integer_signedness is not None:
                raise DecodeError(
                    f"{_where(path, case_path + '.conversion.integer_signedness')}: "
                    "requires an integer conversion domain"
                )
            conversion = ConversionSignature(
                source_domain=source_domain,
                source_formats=source_formats,
                destination_domain=destination_domain,
                destination_formats=destination_formats,
                integer_signedness=integer_signedness,
                behavior=_enum_string(
                    conversion_raw["behavior"],
                    path,
                    case_path + ".conversion.behavior",
                    CONVERSION_BEHAVIORS,
                ),
            )
        cases.append(
            OperationCase(
                id=_stable_id(item["id"], path, case_path + ".id"),
                applies_to=FormApplicability(tuple(applies_forms), tuple(selectors), tuple(operand_profiles)),
                additional_requirements=requirements,
                predicate=PredicateContract(
                    predicate_kind,
                    predicate_refs["condition_operand"],
                    predicate_refs["destination_operand"],
                    predicate_refs["counter_operand"],
                    observed_value,
                ),
                flags=tuple(flags),
                events=tuple(events),
                sail_entry=sail_entry,
                conversion=conversion,
            )
        )
    if not cases:
        raise DecodeError(f"{_where(path, 'cases')}: expected non-empty list")
    _unique((case.id for case in cases), path, "cases.id")

    artifacts_raw = _mapping(data["artifacts"], path, "artifacts")
    _keys(
        artifacts_raw,
        path,
        "artifacts",
        required=("semantics", "description"),
        optional=("diagrams",),
    )

    def artifact_ref(field_path: str, allowed_kinds: frozenset[str]) -> OperationArtifactRef:
        item = _mapping(artifacts_raw[field_path], path, "artifacts." + field_path)
        _keys(item, path, "artifacts." + field_path, required=("path", "kind"))
        return OperationArtifactRef(
            _relative_reference(item["path"], path, "artifacts." + field_path + ".path"),
            _enum_string(item["kind"], path, "artifacts." + field_path + ".kind", allowed_kinds),
        )

    semantics = artifact_ref("semantics", frozenset({"sail"}))
    description = artifact_ref("description", DESCRIPTION_ARTIFACT_KINDS)
    diagrams: list[DiagramArtifactRef] = []
    for index, raw_diagram in enumerate(
        _list(artifacts_raw.get("diagrams", []), path, "artifacts.diagrams")
    ):
        item_path = f"artifacts.diagrams[{index}]"
        item = _mapping(raw_diagram, path, item_path)
        _keys(
            item,
            path,
            item_path,
            required=("id", "path", "kind", "caption", "alt_text"),
            optional=("case",),
        )
        diagrams.append(
            DiagramArtifactRef(
                _stable_id(item["id"], path, item_path + ".id"),
                _relative_reference(item["path"], path, item_path + ".path"),
                _stable_id(item["kind"], path, item_path + ".kind"),
                (
                    _stable_id(item["case"], path, item_path + ".case")
                    if item.get("case") is not None
                    else None
                ),
                _string(item["caption"], path, item_path + ".caption"),
                _string(item["alt_text"], path, item_path + ".alt_text"),
            )
        )
    _unique((diagram.id for diagram in diagrams), path, "artifacts.diagrams.id")
    _unique((diagram.path for diagram in diagrams), path, "artifacts.diagrams.path")
    return OperationDocument(
        id=operation_id,
        title=title,
        summary=summary,
        public_instruction=PublicInstructionRef(mnemonic, aliases, width_suffix_aliases),
        execution_route=_enum_string(
            data["execution_route"], path, "execution_route", EXECUTION_ROUTES
        ),
        privilege=_enum_string(data["privilege"], path, "privilege", PRIVILEGES),
        repeat=OperationRepeatEligibility(repeat_kind, repeat_observed),
        operands=tuple(operands),
        cases=tuple(cases),
        artifacts=OperationArtifacts(semantics, description, tuple(diagrams)),
    )


def decode_semantic_condition_registry(
    path: Path, raw: Any
) -> SemanticConditionRegistry:
    """Decode the registry that owns operation-event condition prose."""

    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("conditions",))
    conditions: list[SemanticConditionDefinition] = []
    for index, raw_condition in enumerate(
        _list(data["conditions"], path, "conditions")
    ):
        item_path = f"conditions[{index}]"
        item = _mapping(raw_condition, path, item_path)
        _keys(item, path, item_path, required=("id", "reader_text"))
        conditions.append(
            SemanticConditionDefinition(
                id=_stable_id(item["id"], path, item_path + ".id"),
                reader_text=_string(
                    item["reader_text"], path, item_path + ".reader_text"
                ),
            )
        )
    if not conditions:
        raise DecodeError(f"{_where(path, 'conditions')}: expected non-empty list")
    _unique((condition.id for condition in conditions), path, "conditions.id")
    return SemanticConditionRegistry(tuple(conditions))


def decode_named_value_registry(path: Path, raw: Any) -> NamedValueRegistry:
    """Decode the finite registry of operation-defined semantic values."""

    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("values",))
    values: list[NamedValueDefinition] = []
    for index, raw_value in enumerate(_list(data["values"], path, "values")):
        item_path = f"values[{index}]"
        item = _mapping(raw_value, path, item_path)
        _keys(item, path, item_path, required=("id", "kind", "reader_term"))
        values.append(
            NamedValueDefinition(
                id=_stable_id(item["id"], path, item_path + ".id"),
                kind=_enum_string(
                    item["kind"], path, item_path + ".kind", NAMED_VALUE_KINDS
                ),
                reader_term=_string(
                    item["reader_term"], path, item_path + ".reader_term"
                ),
            )
        )
    if not values:
        raise DecodeError(f"{_where(path, 'values')}: expected non-empty list")
    _unique((value.id for value in values), path, "values.id")
    return NamedValueRegistry(tuple(values))


def decode_flag_effect_definition_registry(
    path: Path, raw: Any
) -> FlagEffectDefinitionRegistry:
    """Decode the registry that owns typed flag-reference reader text."""

    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("definitions",))
    definitions: list[FlagEffectDefinition] = []
    for index, raw_definition in enumerate(
        _list(data["definitions"], path, "definitions")
    ):
        item_path = f"definitions[{index}]"
        item = _mapping(raw_definition, path, item_path)
        _keys(item, path, item_path, required=("id", "kind", "reader_text"))
        definitions.append(
            FlagEffectDefinition(
                id=_stable_id(item["id"], path, item_path + ".id"),
                kind=_enum_string(
                    item["kind"],
                    path,
                    item_path + ".kind",
                    FLAG_EFFECT_DEFINITION_KINDS,
                ),
                reader_text=_string(
                    item["reader_text"], path, item_path + ".reader_text"
                ),
            )
        )
    if not definitions:
        raise DecodeError(f"{_where(path, 'definitions')}: expected non-empty list")
    _unique((definition.id for definition in definitions), path, "definitions.id")
    return FlagEffectDefinitionRegistry(tuple(definitions))


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
            optional=(
                "operands",
                "sizes",
                "fields",
                "constraints",
                "destination_overlap",
            ),
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
                optional=("field", "domain", "ea_role", "ea_width"),
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
            operand_type = _string(operand["type"], path, operand_path + ".type")
            access = _enum_string(
                operand["access"], path, operand_path + ".access", OPERAND_ACCESS
            )
            ea_role = operand.get("ea_role")
            ea_width = operand.get("ea_width")
            if operand_type in EA_OPERAND_TYPES:
                if ea_role is None or ea_width is None:
                    raise DecodeError(
                        f"{_where(path, operand_path)}: effective-address operands require "
                        "ea_role and ea_width"
                    )
                ea_role = _enum_string(
                    ea_role, path, operand_path + ".ea_role", EA_ROLES
                )
                ea_width = _enum_string(
                    ea_width, path, operand_path + ".ea_width", EA_WIDTHS
                )
                if ea_role == "address" and access != "address":
                    raise DecodeError(
                        f"{_where(path, operand_path)}: address role requires address access"
                    )
                if ea_role == "control_target" and access != "read":
                    raise DecodeError(
                        f"{_where(path, operand_path)}: control_target role requires read access"
                    )
                if ea_role == "value" and access == "address":
                    raise DecodeError(
                        f"{_where(path, operand_path)}: value role cannot use address access"
                    )
            elif ea_role is not None or ea_width is not None:
                raise DecodeError(
                    f"{_where(path, operand_path)}: ea_role and ea_width apply only to "
                    "effective-address operands"
                )
            operands.append(
                EncodingOperand(
                    name=_string(operand["name"], path, operand_path + ".name"),
                    type=operand_type,
                    access=access,
                    field=marker,
                    domain=(
                        _enum_string(domain, path, operand_path + ".domain", OPERAND_DOMAINS)
                        if domain is not None
                        else None
                    ),
                    ea_role=ea_role,
                    ea_width=ea_width,
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
        writable_names = {
            operand.name
            for operand in operands
            if operand.field is not None and operand.access in {"write", "read_write"}
        }
        def operands_can_overlap(
            left: EncodingOperand,
            right: EncodingOperand,
        ) -> bool:
            return left.type == right.type

        expected_overlap_pairs = {
            tuple(sorted((left.name, right.name)))
            for left_index, left in enumerate(operands)
            for right in operands[left_index + 1 :]
            if left.field is not None
            and right.field is not None
            and left.access in {"write", "read_write"}
            and right.access in {"write", "read_write"}
            and operands_can_overlap(left, right)
        }
        destination_overlap: list[DestinationOverlap] = []
        declared_overlap_pairs: set[tuple[str, str]] = set()
        for relation_index, raw_relation in enumerate(
            _list(
                form.get("destination_overlap", []),
                path,
                field_path + ".destination_overlap",
            )
        ):
            item_path = f"{field_path}.destination_overlap[{relation_index}]"
            item = _mapping(raw_relation, path, item_path)
            _keys(item, path, item_path, required=("operands", "rule"))
            names = tuple(
                _string_list(item["operands"], path, item_path + ".operands")
            )
            if len(names) != 2 or names[0] == names[1]:
                raise DecodeError(
                    f"{_where(path, item_path + '.operands')}: expected two distinct operands"
                )
            if any(name not in writable_names for name in names):
                raise DecodeError(
                    f"{_where(path, item_path + '.operands')}: relation requires writable field operands"
                )
            pair = tuple(sorted(names))
            if pair in declared_overlap_pairs:
                raise DecodeError(
                    f"{_where(path, item_path + '.operands')}: duplicate overlap pair"
                )
            declared_overlap_pairs.add(pair)
            destination_overlap.append(
                DestinationOverlap(
                    operands=(names[0], names[1]),
                    rule=_enum_string(
                        item["rule"],
                        path,
                        item_path + ".rule",
                        DESTINATION_OVERLAP_RULES,
                    ),
                )
            )
        if declared_overlap_pairs != expected_overlap_pairs:
            raise DecodeError(
                f"{_where(path, field_path + '.destination_overlap')}: "
                "must define every writable field-operand pair"
            )
        syntax = _string(form["syntax"], path, field_path + ".syntax")
        parse_assembly_template(syntax, _where(path, field_path + ".syntax"))
        forms.append(
            EncodingForm(
                id=form_id,
                encoding_class=encoding_class,
                bits=bits,
                syntax=syntax,
                operands=tuple(operands),
                sizes=sizes,
                fields=fields,
                constraints=tuple(constraints),
                destination_overlap=tuple(destination_overlap),
            )
        )
    return EncodingsDocument(tuple(forms))


def decode_instruction_set_index(path: Path, raw: Any) -> InstructionSetIndex:
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


def decode_cpuid_flag_registry(path: Path, raw: Any) -> CpuidFlagRegistry:
    data = _mapping(raw, path, "")
    _keys(data, path, "", required=("cpuid_flags",))
    flags: list[CpuidFlag] = []
    for index, raw_flag in enumerate(
        _list(data["cpuid_flags"], path, "cpuid_flags")
    ):
        flag_path = f"cpuid_flags[{index}]"
        flag = _mapping(raw_flag, path, flag_path)
        _keys(flag, path, flag_path, required=("id", "token", "location"))
        token = _string(flag["token"], path, flag_path + ".token")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", token):
            raise DecodeError(f"{_where(path, flag_path + '.token')}: invalid public token")
        location_path = flag_path + ".location"
        location = _mapping(flag["location"], path, location_path)
        _keys(
            location,
            path,
            location_path,
            required=("class", "leaf", "index", "bit"),
        )
        selector_class = _nonnegative_integer(
            location["class"], path, location_path + ".class"
        )
        leaf = _nonnegative_integer(location["leaf"], path, location_path + ".leaf")
        result_index = _nonnegative_integer(
            location["index"], path, location_path + ".index"
        )
        bit = _nonnegative_integer(location["bit"], path, location_path + ".bit")
        if bit >= 64:
            raise DecodeError(f"{_where(path, location_path + '.bit')}: expected 0..63")
        flags.append(
            CpuidFlag(
                id=_stable_id(flag["id"], path, flag_path + ".id"),
                token=token,
                location=CpuidFlagLocation(
                    selector_class=selector_class,
                    leaf=leaf,
                    index=result_index,
                    bit=bit,
                ),
            )
        )
    _unique((flag.id for flag in flags), path, "cpuid_flags.id")
    _unique((flag.token for flag in flags), path, "cpuid_flags.token")
    _unique(
        (
            (
                flag.location.selector_class,
                flag.location.leaf,
                flag.location.index,
                flag.location.bit,
            )
            for flag in flags
        ),
        path,
        "cpuid_flags.location",
    )
    return CpuidFlagRegistry(tuple(flags))


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
        _keys(avail, path, "availability", required=("required_cpuid_flags",))
        required_cpuid_flags = tuple(
            _stable_id(
                value,
                path,
                f"availability.required_cpuid_flags[{index}]",
            )
            for index, value in enumerate(
                _list(
                    avail["required_cpuid_flags"],
                    path,
                    "availability.required_cpuid_flags",
                )
            )
        )
        if not required_cpuid_flags:
            raise DecodeError(
                f"{_where(path, 'availability.required_cpuid_flags')}: expected non-empty list"
            )
        _unique(
            required_cpuid_flags, path, "availability.required_cpuid_flags"
        )
        availability = ExtensionAvailability(required_cpuid_flags)
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
        "profile",
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
        "effective_address": {"encoding_ref", "profile"},
        "enum": {"values_ref", "values", "reserved_values", "result_bits_format"},
        "ea_immediate": {"encoding_ref"},
        "bitmap": {"bits"},
        "immediate": {"signed", "operation_size_extension"},
        "relative_immediate": {"signed", "operation_size_extension"},
    }
    required_by_kind = {
        "register": {"register_group"},
        "fixed_register": {"register"},
        "effective_address": {"encoding_ref", "profile"},
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
            required=("kind", "bit_width"),
            optional=common_optional,
        )
        kind = _enum_string(item["kind"], path, item_path + ".kind", OPERAND_KINDS)
        irrelevant = (set(item) - {"kind", "bit_width"}) - allowed_by_kind[kind]
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
        bit_width = _nonnegative_integer(
            item["bit_width"], path, item_path + ".bit_width"
        )
        if any(bit.bit >= bit_width for bit in bits):
            raise DecodeError(f"{_where(path, item_path + '.bits')}: bit exceeds bit width")

        def optional_string(key: str) -> str | None:
            child = item.get(key)
            return (
                _string(child, path, item_path + "." + key)
                if child is not None
                else None
            )

        signed = item.get("signed")
        profile = item.get("profile")
        decoded_profile = (
            _enum_string(profile, path, item_path + ".profile", EA_PROFILES)
            if profile is not None
            else None
        )
        if kind == "effective_address":
            expected_operand_types = {"EA": "ea", "FEA": "fea", "VEA": "vea"}
            expected_profile = expected_operand_types.get(name)
            if expected_profile is not None and decoded_profile != expected_profile:
                raise DecodeError(
                    f"{_where(path, item_path + '.profile')}: {name} requires profile "
                    f"{expected_profile}"
                )
        operand_types[name] = OperandType(
            kind=kind,
            bit_width=bit_width,
            register_group=optional_string("register_group"),
            register=optional_string("register"),
            encoding_ref=optional_string("encoding_ref"),
            profile=decoded_profile,
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
            required=("values",),
            optional=("reserved_values",),
        )
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
        size_kinds[name] = SizeKind(values, reserved_values)
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
                    width=(
                        _positive_integer(child_map["width"], path, child_path + ".width")
                        if isinstance(child_map["width"], int)
                        else _enum_string(
                            child_map["width"],
                            path,
                            child_path + ".width",
                            frozenset({"VLEN", "VLEN_bytes"}),
                        )
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
    descriptor_bytes: int | None = None,
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
                f"{_where(path, item_path + '.pattern')}: descriptor bytes must be 8 bits"
            )
        if descriptor_bytes is not None and len(patterns) != descriptor_bytes:
            raise DecodeError(
                f"{_where(path, item_path + '.pattern')}: expected exactly "
                f"{descriptor_bytes} descriptor byte pattern(s)"
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
    _keys(
        data,
        path,
        "",
        required=("payloads", "compact", "ext1", "ext2"),
    )
    payloads: dict[str, EaPayload] = {}
    for name, value in _mapping(data["payloads"], path, "payloads").items():
        item_path = f"payloads.{name}"
        item = _validate_item_keys(
            path,
            item_path,
            value,
            required=("kind", "bit_width", "signed"),
            optional=("format",),
        )
        payload_format = item.get("format")
        payloads[name] = EaPayload(
            kind=_string(item["kind"], path, item_path + ".kind"),
            bit_width=_positive_integer(
                item["bit_width"], path, item_path + ".bit_width"
            ),
            signed=_boolean(item["signed"], path, item_path + ".signed"),
            format=(
                _enum_string(
                    payload_format,
                    path,
                    item_path + ".format",
                    frozenset({"binary32", "binary64"}),
                )
                if payload_format is not None
                else None
            ),
        )
        if (payloads[name].kind == "float_immediate") != (
            payloads[name].format is not None
        ):
            raise DecodeError(
                f"{_where(path, item_path)}: float_immediate payloads require format "
                "and no other payload kind permits it"
            )
    compact_data = _mapping(data["compact"], path, "compact")
    _keys(
        compact_data,
        path,
        "compact",
        required=("field_width", "profiles", "forms"),
    )
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
    raw_profiles = _mapping(compact_data["profiles"], path, "compact.profiles")
    if set(raw_profiles) != {"ea", "fea", "vea"}:
        raise DecodeError(
            f"{_where(path, 'compact.profiles')}: expected exactly ea, fea, and vea"
        )
    compact_profiles: dict[str, EaProfile] = {}
    expected_operand_types = {"ea": "EA", "fea": "FEA", "vea": "VEA"}
    profile_optional = (
        "immediate_conversion",
        "lane_model",
        "base_update",
        "index_update",
        "predicate_affects_update",
        "scatter_gather",
    )
    for profile_name, raw_profile in raw_profiles.items():
        profile_path = f"compact.profiles.{profile_name}"
        profile = _mapping(raw_profile, path, profile_path)
        _keys(
            profile,
            path,
            profile_path,
            required=("operand_type", "overrides"),
            optional=profile_optional,
        )
        operand_type = _string(
            profile["operand_type"], path, profile_path + ".operand_type"
        )
        if operand_type != expected_operand_types[profile_name]:
            raise DecodeError(
                f"{_where(path, profile_path + '.operand_type')}: expected "
                f"{expected_operand_types[profile_name]}"
            )
        overrides: list[EaProfileOverride] = []
        for index, raw_override in enumerate(
            _list(profile["overrides"], path, profile_path + ".overrides")
        ):
            override_path = f"{profile_path}.overrides[{index}]"
            override = _mapping(raw_override, path, override_path)
            pattern = _string(override.get("pattern"), path, override_path + ".pattern")
            if len(pattern) != compact_width or set(pattern) - {"0", "1"}:
                raise DecodeError(
                    f"{_where(path, override_path + '.pattern')}: profile overrides "
                    "must select one exact compact value"
                )
            reserved = override.get("reserved")
            if reserved is not None:
                _keys(
                    override,
                    path,
                    override_path,
                    required=("pattern", "reserved"),
                )
                if not _boolean(reserved, path, override_path + ".reserved"):
                    raise DecodeError(
                        f"{_where(path, override_path + '.reserved')}: expected true"
                    )
                overrides.append(EaProfileOverride(pattern, True))
            else:
                form = _decode_ea_forms(
                    [override],
                    path,
                    override_path + ".form",
                    compact=True,
                    compact_width=compact_width,
                )[0]
                overrides.append(EaProfileOverride(pattern, False, form))
        _unique(
            (override.pattern for override in overrides),
            path,
            profile_path + ".overrides.pattern",
        )
        compact_profiles[profile_name] = EaProfile(
            name=profile_name,
            operand_type=operand_type,
            overrides=tuple(overrides),
            immediate_conversion=(
                _enum_string(
                    profile["immediate_conversion"],
                    path,
                    profile_path + ".immediate_conversion",
                    frozenset({"ieee754"}),
                )
                if "immediate_conversion" in profile
                else None
            ),
            lane_model=(
                _enum_string(
                    profile["lane_model"],
                    path,
                    profile_path + ".lane_model",
                    frozenset({"contiguous"}),
                )
                if "lane_model" in profile
                else None
            ),
            base_update=(
                _enum_string(
                    profile["base_update"],
                    path,
                    profile_path + ".base_update",
                    frozenset({"vlen_bytes"}),
                )
                if "base_update" in profile
                else None
            ),
            index_update=(
                _enum_string(
                    profile["index_update"],
                    path,
                    profile_path + ".index_update",
                    frozenset({"element_count_before_scale"}),
                )
                if "index_update" in profile
                else None
            ),
            predicate_affects_update=(
                _boolean(
                    profile["predicate_affects_update"],
                    path,
                    profile_path + ".predicate_affects_update",
                )
                if "predicate_affects_update" in profile
                else None
            ),
            scatter_gather=(
                _enum_string(
                    profile["scatter_gather"],
                    path,
                    profile_path + ".scatter_gather",
                    frozenset({"separate_instructions"}),
                )
                if "scatter_gather" in profile
                else None
            ),
        )
    if compact_profiles["ea"].overrides:
        raise DecodeError(
            f"{_where(path, 'compact.profiles.ea.overrides')}: scalar EA is the "
            "unchanged compact form baseline"
        )
    ext1_data = _mapping(data["ext1"], path, "ext1")
    _keys(ext1_data, path, "ext1", required=("kind", "forms"))
    ext1_forms = _decode_ea_forms(
        ext1_data["forms"], path, "ext1.forms", compact=False, descriptor_bytes=1
    )
    ext2_data = _mapping(data["ext2"], path, "ext2")
    _keys(ext2_data, path, "ext2", required=("kind", "forms"))
    ext2_forms = _decode_ea_forms(
        ext2_data["forms"], path, "ext2.forms", compact=False, descriptor_bytes=2
    )
    descriptor_families = {"ext1", "ext2"}
    profile_forms = [
        override.form
        for profile in compact_profiles.values()
        for override in profile.overrides
        if override.form is not None
    ]
    for form in (*compact_forms, *profile_forms):
        if form.payload is not None and form.payload not in payloads:
            raise DecodeError(
                f"{_where(path, 'compact.forms')}: unknown payload {form.payload}"
            )
        if form.descriptor is not None and form.descriptor not in descriptor_families:
            raise DecodeError(
                f"{_where(path, 'compact.forms')}: unknown descriptor family "
                f"{form.descriptor}"
            )
        if (form.kind == "escape") != (form.descriptor is not None):
            raise DecodeError(
                f"{_where(path, 'compact.forms')}: escape forms must reference exactly "
                "one declared descriptor family"
            )
    return EaRegistry(
        payloads=payloads,
        compact_field_width=compact_width,
        compact_forms=compact_forms,
        compact_profiles=compact_profiles,
        ext1_kind=_string(ext1_data["kind"], path, "ext1.kind"),
        ext1_forms=ext1_forms,
        ext2_kind=_string(ext2_data["kind"], path, "ext2.kind"),
        ext2_forms=ext2_forms,
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
        required=("assembly", "offset", "opcode_space_bytes", "total_bytes", "displacement"),
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
        opcode_space_bytes=_byte_list(
            raw_instruction["opcode_space_bytes"],
            path,
            "ordinary_plt.instruction.opcode_space_bytes",
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
    if "diagrams" in path.parts and path.suffix == ".yaml":
        from vector_diagrams import VectorDiagramError, load as load_vector_diagram

        try:
            return load_vector_diagram(path)  # type: ignore[return-value]
        except VectorDiagramError as exc:
            raise DecodeError(str(exc)) from exc
    if name == "operation.yaml":
        return decode_operation(path, raw)
    if name == "encodings.yaml":
        return decode_encodings(path, raw)
    if name == "instructions.yaml":
        return decode_instruction_set_index(path, raw)
    if name == "extension.yaml":
        return decode_extension_manifest(path, raw)
    if name == "extensions.yaml":
        return decode_extension_catalog(path, raw)
    if name == "cpuid_flags.yaml":
        return decode_cpuid_flag_registry(path, raw)
    if name == "operands.yaml":
        return decode_operand_registry(path, raw)
    if name == "sizes.yaml":
        return decode_size_registry(path, raw)
    if name == "registers.yaml":
        return decode_register_registry(path, raw)
    if name == "conditions.yaml":
        return decode_condition_registry(path, raw)
    if name == "semantic_conditions.yaml":
        return decode_semantic_condition_registry(path, raw)
    if name == "named_values.yaml":
        return decode_named_value_registry(path, raw)
    if name == "flag_effect_definitions.yaml":
        return decode_flag_effect_definition_registry(path, raw)
    if name == "definition.yaml" and path.parent.name == "effective_address":
        return decode_ea_registry(path, raw)
    if path.match("*/interfaces/abi/plt_conformance_vectors.yaml"):
        return decode_abi_vectors(path, raw)
    if path.match("*/memory/ordering/formal/validation.yaml"):
        return decode_memory_validation(path, raw)
    raise DecodeError(f"{path}: unknown YAML document kind")
