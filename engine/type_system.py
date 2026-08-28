"""Typed field and payload definition namespaces for one ISA tree."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

try:
    from .extension import ExtensionSetCatalog
    from .reference import Reference, ReferenceIndex
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from extension import ExtensionSetCatalog
    from reference import Reference, ReferenceIndex


class FieldTypeKind(StrEnum):
    """Architectural interpretation of a primary-encoding field."""

    REGISTER_SELECTOR = "register_selector"
    EFFECTIVE_ADDRESS = "effective_address"
    REGISTER = "register"
    ENUM_CONDITION = "enum_condition"
    REGISTER_PAIR_SELECTOR = "register_pair_selector"
    PAGE_TABLE_LEVEL = "page_table_level"
    FLAGS = "flags"
    IMMEDIATE = "immediate"
    MEMORY_ORDER = "memory_order"
    SIZE_SELECTOR = "size_selector"


class PayloadTypeKind(StrEnum):
    """Architectural interpretation of an appended instruction payload."""

    IMMEDIATE = "immediate"
    PC_DISPLACEMENT = "pc_displacement"
    PC_ABSOLUTE = "pc_absolute"
    FLOATING_POINT_CONSTANT_ID = "floating_point_constant_id"
    REGISTER_SELECTOR = "register_selector"


@dataclass(frozen=True, slots=True)
class FieldValue:
    """One authored value/code pair for a selector field."""

    value: int
    code: str


@dataclass(frozen=True, slots=True)
class FieldType:
    """A type that occupies bits inside the primary instruction encoding."""

    reference: Reference
    source: Path
    kind: FieldTypeKind
    bits: int
    value_type: str | None = None
    register_group: str | None = None
    profile: str | None = None
    values: tuple[FieldValue, ...] = ()

    @classmethod
    def from_mapping(
        cls, reference: Reference, source: Path, data: Mapping[str, Any]
    ) -> "FieldType":
        _reject_unknown_properties(
            reference,
            data,
            {"type", "bits", "value_type", "register_group", "profile", "values"},
        )
        raw_kind = _required_string(reference, data, "type")
        try:
            kind = FieldTypeKind(raw_kind)
        except ValueError as error:
            raise ValueError(
                f"{source}: {reference}: unknown field type kind {raw_kind!r}"
            ) from error
        bits = _positive_int(reference, data.get("bits"), "bits")
        values = _field_values(reference, data.get("values", ()), bits)
        value_type = _optional_string(reference, data, "value_type")
        register_group = _optional_string(reference, data, "register_group")
        profile = _optional_string(reference, data, "profile")

        if kind == FieldTypeKind.SIZE_SELECTOR and not values:
            raise ValueError(f"{source}: {reference}: size_selector requires values")
        if kind == FieldTypeKind.EFFECTIVE_ADDRESS and profile is None:
            raise ValueError(
                f"{source}: {reference}: effective_address requires profile"
            )
        if kind == FieldTypeKind.IMMEDIATE and value_type is None:
            raise ValueError(f"{source}: {reference}: immediate requires value_type")
        if (
            kind
            in {
                FieldTypeKind.REGISTER,
                FieldTypeKind.REGISTER_SELECTOR,
                FieldTypeKind.REGISTER_PAIR_SELECTOR,
            }
            and register_group is None
        ):
            raise ValueError(f"{source}: {reference}: {kind} requires register_group")

        return cls(
            reference=reference,
            source=source,
            kind=kind,
            bits=bits,
            value_type=value_type,
            register_group=register_group,
            profile=profile,
            values=values,
        )


@dataclass(frozen=True, slots=True)
class PayloadType:
    """A byte-sized type appended after the primary instruction encoding."""

    reference: Reference
    source: Path
    kind: PayloadTypeKind
    bytes: int
    value_type: str | None = None
    signed: bool | None = None
    register_group: str | None = None

    @classmethod
    def from_mapping(
        cls, reference: Reference, source: Path, data: Mapping[str, Any]
    ) -> "PayloadType":
        _reject_unknown_properties(
            reference,
            data,
            {"type", "bytes", "value_type", "signed", "register_group"},
        )
        raw_kind = _required_string(reference, data, "type")
        try:
            kind = PayloadTypeKind(raw_kind)
        except ValueError as error:
            raise ValueError(
                f"{source}: {reference}: unknown payload type kind {raw_kind!r}"
            ) from error
        byte_count = _positive_int(reference, data.get("bytes"), "bytes")
        value_type = _optional_string(reference, data, "value_type")
        signed = data.get("signed")
        if signed is not None and not isinstance(signed, bool):
            raise ValueError(f"{source}: {reference}: signed must be a boolean")
        if kind == PayloadTypeKind.IMMEDIATE and value_type is None:
            raise ValueError(f"{source}: {reference}: immediate requires value_type")
        if kind == PayloadTypeKind.PC_ABSOLUTE and signed is None:
            raise ValueError(f"{source}: {reference}: pc_absolute requires signed")
        register_group = _optional_string(reference, data, "register_group")
        if kind == PayloadTypeKind.REGISTER_SELECTOR and register_group is None:
            raise ValueError(
                f"{source}: {reference}: register_selector requires register_group"
            )
        return cls(
            reference,
            source,
            kind,
            byte_count,
            value_type,
            signed,
            register_group,
        )


@dataclass(frozen=True, slots=True)
class TypeNamespace:
    """Field and payload types owned by base or one declared extension."""

    owner: str
    root: Path
    field_types: ReferenceIndex[FieldType]
    payload_types: ReferenceIndex[PayloadType]

    @classmethod
    def load(cls, owner: str, root: str | Path) -> "TypeNamespace":
        namespace_root = Path(root)
        return cls(
            owner=owner,
            root=namespace_root,
            field_types=_load_field_types(owner, namespace_root / "field_types.yaml"),
            payload_types=_load_payload_types(
                owner, namespace_root / "payload_types.yaml"
            ),
        )


@dataclass(frozen=True, slots=True)
class TypeSystem:
    """Global type indexes projected from base and declared extension namespaces."""

    base: TypeNamespace
    extensions: Mapping[str, TypeNamespace]
    field_types: ReferenceIndex[FieldType]
    payload_types: ReferenceIndex[PayloadType]

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "TypeSystem":
        root = Path(isa_root).resolve()
        catalog = extension_catalog or ExtensionSetCatalog.load(root)
        base = TypeNamespace.load("base", root)
        extensions: dict[str, TypeNamespace] = {}
        for extension_id in catalog.declared:
            extension_root = catalog.root / extension_id
            if extension_root.is_dir():
                extensions[extension_id] = TypeNamespace.load(
                    extension_id, extension_root
                )

        field_types = ReferenceIndex[FieldType]()
        payload_types = ReferenceIndex[PayloadType]()
        for namespace in (base, *extensions.values()):
            for reference, definition in namespace.field_types.items():
                field_types.register(reference, definition)
            for reference, definition in namespace.payload_types.items():
                payload_types.register(reference, definition)

        return cls(
            base=base,
            extensions=MappingProxyType(extensions),
            field_types=field_types,
            payload_types=payload_types,
        )

    def namespace(self, owner: str) -> TypeNamespace:
        """Resolve the type namespace owned by base or a declared extension."""

        if owner == "base":
            return self.base
        try:
            return self.extensions[owner]
        except KeyError as error:
            raise ValueError(f"unknown type namespace {owner!r}") from error


def _load_field_types(owner: str, path: Path) -> ReferenceIndex[FieldType]:
    index = ReferenceIndex[FieldType]()
    for name, definition in _load_definitions(path, "field_types").items():
        reference = Reference(owner, ("field_types",), name)
        index.register(reference, FieldType.from_mapping(reference, path, definition))
    return index


def _load_payload_types(owner: str, path: Path) -> ReferenceIndex[PayloadType]:
    index = ReferenceIndex[PayloadType]()
    for name, definition in _load_definitions(path, "payload_types").items():
        reference = Reference(owner, ("payload_types",), name)
        index.register(reference, PayloadType.from_mapping(reference, path, definition))
    return index


def _load_definitions(path: Path, collection: str) -> dict[str, Mapping[str, Any]]:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8") as stream:
        document = yaml.safe_load(stream)
    if not isinstance(document, Mapping):
        raise ValueError(f"{path}: expected a YAML mapping")
    definitions = document.get(collection)
    if not isinstance(definitions, Mapping):
        raise ValueError(f"{path}: {collection} must be a mapping")
    result: dict[str, Mapping[str, Any]] = {}
    for name, definition in definitions.items():
        if not isinstance(name, str) or not isinstance(definition, Mapping):
            raise ValueError(f"{path}: {collection} entries must be named mappings")
        result[name] = definition
    return result


def _reject_unknown_properties(
    reference: Reference, data: Mapping[str, Any], allowed: set[str]
) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"{reference}: unknown properties {unknown}")


def _required_string(reference: Reference, data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{reference}: {key} must be a non-empty string")
    return value


def _optional_string(
    reference: Reference, data: Mapping[str, Any], key: str
) -> str | None:
    value = data.get(key)
    if value is not None and (not isinstance(value, str) or not value):
        raise ValueError(f"{reference}: {key} must be a non-empty string")
    return value


def _positive_int(reference: Reference, value: object, key: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{reference}: {key} must be a positive integer")
    return value


def _field_values(
    reference: Reference, raw_values: object, bits: int
) -> tuple[FieldValue, ...]:
    if not isinstance(raw_values, (list, tuple)):
        raise ValueError(f"{reference}: values must be an array")
    values: list[FieldValue] = []
    for index, raw in enumerate(raw_values):
        if not isinstance(raw, Mapping) or set(raw) != {"value", "code"}:
            raise ValueError(
                f"{reference}: values[{index}] must contain value and code"
            )
        value = raw["value"]
        code = raw["code"]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{reference}: values[{index}].value must be an integer")
        if value < 0 or value >= 1 << bits:
            raise ValueError(
                f"{reference}: selector value {value} does not fit in {bits} bits"
            )
        if not isinstance(code, str) or not code:
            raise ValueError(
                f"{reference}: values[{index}].code must be a non-empty string"
            )
        values.append(FieldValue(value, code))
    if len({item.value for item in values}) != len(values):
        raise ValueError(f"{reference}: selector values must be unique")
    if len({item.code for item in values}) != len(values):
        raise ValueError(f"{reference}: selector codes must be unique")
    return tuple(values)
