"""Resolve and validate encoding fields from the merged type registries."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import re
from typing import Any

from defs_schema import (
    AssemblyTemplate,
    AssemblyTemplateOperand,
    EncodingConstraint,
    EncodingForm,
    EncodingOperand,
    parse_assembly_template,
)


@dataclass(frozen=True)
class FieldTypeSpec:
    """Resolved metadata shared by validators, allocation tools, and docs."""

    name: str
    width: int
    allocation_kind: str
    operand_kind: str | None = None
    fixed_register: str | None = None
    valid_values: tuple[int | str, ...] = ()
    reserved_values: tuple[int | str, ...] = ()
    size_codes: tuple[str, ...] = ()


@dataclass(frozen=True)
class FieldTypeRegistry:
    types: dict[str, FieldTypeSpec]
    size_codes: frozenset[str]
    size_suffixes: dict[str, str]


def _allocation_kind(name: str, definition: dict[str, Any]) -> str:
    named = {
        "Rn": "rn",
        "Fn": "freg",
        "EA": "ea7",
        "condition": "condition",
    }
    if name in named:
        return named[name]
    if definition.get("kind") in {
        "ea_immediate",
        "immediate",
        "relative_immediate",
    } or name in {"flags_bitmap", "PAIRn", "FPAIRn", "pt_level", "fconst_id"}:
        return "immediate"
    return "bits"


def _registry_values(definition: dict[str, Any], key: str) -> tuple[int | str, ...]:
    values = definition.get(key) or []
    return tuple(item["value"] for item in values if isinstance(item, dict))


def build_field_type_registry(
    operand_types: dict[str, Any],
    size_definitions: dict[str, Any],
) -> FieldTypeRegistry:
    """Merge operand and size domains into the authoritative field-type registry."""
    types: dict[str, FieldTypeSpec] = {}
    for name, raw_definition in operand_types.items():
        definition = dict(raw_definition)
        types[name] = FieldTypeSpec(
            name=name,
            width=int(definition["bit_width"]),
            allocation_kind=_allocation_kind(name, definition),
            operand_kind=str(definition["kind"]),
            fixed_register=(
                str(definition["register"])
                if definition.get("register") is not None
                else None
            ),
            valid_values=_registry_values(definition, "values"),
            reserved_values=_registry_values(definition, "reserved_values"),
        )

    size_suffixes = {
        str(code): str(definition["suffix"])
        for code, definition in size_definitions["size_codes"].items()
    }
    if len(set(size_suffixes.values())) != len(size_suffixes):
        raise ValueError("size-code suffixes must be unique")
    size_codes = frozenset(size_suffixes)
    for kind, raw_definition in size_definitions["size_kinds"].items():
        definition = dict(raw_definition)
        values = tuple(definition.get("values") or [])
        reserved = tuple(definition.get("reserved_values") or [])
        numeric_values = tuple(int(item["value"]) for item in (*values, *reserved))
        width = max(1, max(numeric_values).bit_length())
        expected_values = set(range(1 << width))
        if set(numeric_values) != expected_values:
            raise ValueError(
                f"size kind {kind!r} must define every {width}-bit value as valid or reserved"
            )
        codes = tuple(str(item["code"]) for item in values)
        unknown_codes = set(codes) - size_codes
        if unknown_codes:
            raise ValueError(
                f"size kind {kind!r} references unknown size codes {sorted(unknown_codes)}"
            )
        name = f"size.{kind}"
        if name in types:
            raise ValueError(f"duplicate field type {name!r}")
        types[name] = FieldTypeSpec(
            name=name,
            width=width,
            allocation_kind="size",
            valid_values=tuple(int(item["value"]) for item in values),
            reserved_values=tuple(int(item["value"]) for item in reserved),
            size_codes=codes,
        )
    return FieldTypeRegistry(
        types=types,
        size_codes=size_codes,
        size_suffixes=size_suffixes,
    )


def _template_operand_matches(
    displayed: AssemblyTemplateOperand,
    operand: EncodingOperand,
    registry: FieldTypeRegistry,
) -> bool:
    spec = registry.types[operand.type]
    if operand.field is not None:
        if displayed.kind != "reference" or displayed.field != operand.field:
            return False
        if operand.type == "EA":
            return displayed.angled and displayed.name == "ea"
        return not displayed.angled and displayed.name == operand.type
    if spec.operand_kind == "fixed_register":
        return (
            displayed.kind == "reference"
            and not displayed.angled
            and displayed.field is None
            and displayed.name == spec.fixed_register
        )
    if displayed.kind == "decimal":
        return spec.operand_kind == "ea_immediate"
    return (
        displayed.kind == "reference"
        and displayed.angled
        and displayed.field is None
        and displayed.name == operand.type
    )


def validate_encoding_template(
    form: EncodingForm,
    mnemonic: str,
    registry: FieldTypeRegistry,
    path: Path,
    *,
    syntax: str | None = None,
    alias: bool = False,
) -> AssemblyTemplate:
    """Validate one parsed template against its instruction, form, and registries."""

    template_text = form.syntax if syntax is None else syntax
    template = parse_assembly_template(template_text, f"{path}: form {form.id} syntax")

    def reject(message: str) -> None:
        raise ValueError(f"{path}: form {form.id} syntax {message}")

    if not alias and template.mnemonic != mnemonic:
        reject(f"names {template.mnemonic}, expected {mnemonic}")

    size_fields = [
        (marker, field.type.removeprefix("size."))
        for marker, field in form.fields.items()
        if field.type.startswith("size.")
    ]
    if template.selected_size_kind is not None:
        expected = (template.size_field, template.selected_size_kind)
        if form.sizes or size_fields != [expected]:
            reject(
                f"selects size kind {template.selected_size_kind} on field "
                f"{template.size_field}, but the form declares {size_fields or form.sizes}"
            )
        spec = registry.types.get(f"size.{template.selected_size_kind}")
        if spec is None or not spec.size_codes:
            reject(f"uses unknown size kind {template.selected_size_kind}")
    elif template.fixed_size_suffix is not None:
        codes = [
            code
            for code, suffix in registry.size_suffixes.items()
            if suffix == template.fixed_size_suffix
        ]
        if len(codes) != 1:
            reject(f"uses unknown fixed size suffix {template.fixed_size_suffix}")
        if size_fields or form.sizes != (codes[0],):
            reject(
                f"uses fixed size suffix {template.fixed_size_suffix}, but the form "
                f"declares {size_fields or form.sizes}"
            )
    elif size_fields:
        reject("omits its selected-size suffix")

    condition_operands = [
        operand
        for operand in form.operands
        if operand.name == "cc" or operand.type == "condition"
    ]
    if mnemonic.endswith("cc"):
        if not (
            len(condition_operands) == 1
            and condition_operands[0].name == "cc"
            and condition_operands[0].type == "condition"
            and condition_operands[0].field is not None
        ):
            reject("does not have the required encoded cc condition selector")
    elif condition_operands:
        reject("has a condition selector for a mnemonic without terminal cc")

    order_operands = [
        operand
        for operand in form.operands
        if operand.name == "order" or operand.type == "memory_order"
    ]
    if template.order_field is not None:
        if template.selected_size_kind is None:
            reject("places /order without a selected-size suffix")
        if not (
            len(order_operands) == 1
            and order_operands[0].name == "order"
            and order_operands[0].type == "memory_order"
            and order_operands[0].field == template.order_field
        ):
            reject(f"/order does not bind field {template.order_field} to the order operand")
    elif order_operands:
        reject("omits its /order selector")

    represented = set(condition_operands) | set(order_operands)
    encoding_operands = [operand for operand in form.operands if operand not in represented]
    groups = [operand for operand in template.operands if operand.kind == "group"]
    displayed = [operand for operand in template.operands if operand.kind != "group"]
    displayed_index = 0
    for operand in encoding_operands:
        if operand.type not in registry.types:
            reject(f"references unknown operand type {operand.type}")
        if displayed_index < len(displayed) and _template_operand_matches(
            displayed[displayed_index], operand, registry
        ):
            displayed_index += 1
        elif groups and operand.field is None:
            continue
        else:
            reject(f"does not correspond to operand {operand.name} of type {operand.type}")
    if displayed_index != len(displayed):
        reject("contains a displayed operand without an EncodingOperand")
    return template


def _constraint_allows(constraint: EncodingConstraint, value: int) -> bool:
    for item in constraint.allow:
        if isinstance(item, int):
            if item == value:
                return True
            continue
        match = re.fullmatch(r"([^.]*)\.\.([^.]*)", item)
        if match:
            low = int(match.group(1), 0)
            high = int(match.group(2), 0)
            if low <= value <= high:
                return True
        elif int(item, 0) == value:
            return True
    return False


def resolve_encoding_form(
    form: EncodingForm,
    registry: FieldTypeRegistry,
    path: Path,
) -> EncodingForm:
    """Validate all declared fields and return a form with effective sizes."""

    def validate_field(type_name: str, marker: str | None, label: str) -> FieldTypeSpec:
        spec = registry.types.get(type_name)
        if spec is None:
            raise ValueError(
                f"{path}: form {form.id} {label} uses unknown type {type_name!r}"
            )
        if marker is not None:
            actual_width = form.bits.count(marker)
            if actual_width != spec.width:
                raise ValueError(
                    f"{path}: form {form.id} {label} has {actual_width} bits, "
                    f"but {type_name} requires {spec.width}"
                )
        return spec

    size_fields: list[tuple[str | None, FieldTypeSpec]] = []
    for operand in form.operands:
        spec = validate_field(operand.type, operand.field, f"operand {operand.name}")
        if spec.size_codes:
            size_fields.append((operand.field, spec))

    for marker, field in form.fields.items():
        spec = validate_field(field.type, marker, f"field {marker}")
        if spec.size_codes:
            size_fields.append((marker, spec))

    if size_fields:
        if form.sizes:
            raise ValueError(
                f"{path}: form {form.id} duplicates size-selector metadata in sizes"
            )
        effective_sizes_list: list[str] = []
        for marker, spec in size_fields:
            for reserved in spec.reserved_values:
                if not isinstance(reserved, int):
                    continue
                allow_constraints = [
                    constraint
                    for constraint in form.constraints
                    if constraint.field == marker and constraint.allow
                ]
                if not any(
                    not _constraint_allows(constraint, reserved)
                    for constraint in allow_constraints
                ):
                    raise ValueError(
                        f"{path}: form {form.id} does not exclude reserved {spec.name} "
                        f"value {reserved} from field {marker}"
                    )
            for code in spec.size_codes:
                if code not in effective_sizes_list:
                    effective_sizes_list.append(code)
        effective_sizes = tuple(effective_sizes_list)
    else:
        effective_sizes = form.sizes
        unknown_sizes = set(effective_sizes) - registry.size_codes
        if unknown_sizes:
            raise ValueError(
                f"{path}: form {form.id} uses unknown sizes {sorted(unknown_sizes)}"
            )

    for operand in form.operands:
        if operand.type == "EA" and operand.ea_width == "operation_size" and not effective_sizes:
            raise ValueError(
                f"{path}: form {form.id} operand {operand.name} uses operation_size "
                "without a size domain"
            )
    return replace(form, sizes=effective_sizes)
