"""Resolve and validate encoding fields from the merged type registries."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import re
from typing import Any

from defs_schema import EncodingConstraint, EncodingForm


@dataclass(frozen=True)
class FieldTypeSpec:
    """Resolved metadata shared by validators, allocation tools, and docs."""

    name: str
    width: int
    allocation_kind: str
    valid_values: tuple[int | str, ...] = ()
    reserved_values: tuple[int | str, ...] = ()
    size_codes: tuple[str, ...] = ()


@dataclass(frozen=True)
class FieldTypeRegistry:
    types: dict[str, FieldTypeSpec]
    size_codes: frozenset[str]


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
    } or name in {"flags_bitmap", "pair_id", "fp_pair_id", "pt_level", "fconst_id"}:
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
            width=int(definition["field_width"]),
            allocation_kind=_allocation_kind(name, definition),
            valid_values=_registry_values(definition, "values"),
            reserved_values=_registry_values(definition, "reserved_values"),
        )

    size_codes = frozenset(str(code) for code in size_definitions["size_codes"])
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
    return FieldTypeRegistry(types=types, size_codes=size_codes)


def size_type_for_codes(registry: FieldTypeRegistry, codes: tuple[str, ...]) -> str:
    matches = [
        spec.name
        for spec in registry.types.values()
        if spec.size_codes == codes
    ]
    if len(matches) != 1:
        raise ValueError(f"cannot resolve a unique size field type for {list(codes)!r}")
    return matches[0]


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
