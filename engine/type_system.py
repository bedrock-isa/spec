"""Typed field and payload definition namespaces for one ISA tree."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

import yaml

from .extension import ExtensionSetCatalog
from .reference import Reference, ReferenceIndex

if TYPE_CHECKING:
    from .register import RegisterGroup


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
    CONTROL_REGISTER_SELECTOR = "control_register_selector"


@dataclass(frozen=True, slots=True)
class FieldValue:
    """One authored value/code pair for a selector field."""

    value: int
    code: str


@dataclass(frozen=True, slots=True)
class FieldType:
    """A type that occupies bits inside the primary instruction encoding."""

    reference: Reference["FieldType"]
    source: Path
    owner: str
    id: str
    kind: FieldTypeKind
    bits: int
    value_type: str | None = None
    register_group: Reference["RegisterGroup"] | None = None
    profile: str | None = None
    values: tuple[FieldValue, ...] = ()

    @classmethod
    def from_mapping(
        cls,
        reference: Reference["FieldType"],
        source: Path,
        owner: str,
        type_id: str,
        data: Mapping[str, Any],
    ) -> "FieldType":
        _reject_unknown_properties(
            type_id,
            data,
            {"type", "bits", "value_type", "register_group", "profile", "values"},
        )
        raw_kind = _required_string(type_id, data, "type")
        try:
            kind = FieldTypeKind(raw_kind)
        except ValueError as error:
            raise ValueError(
                f"{source}: {type_id}: unknown field type kind {raw_kind!r}"
            ) from error
        bits = _positive_int(type_id, data.get("bits"), "bits")
        values = _field_values(type_id, data.get("values", ()), bits)
        value_type = _optional_string(type_id, data, "value_type")
        register_group = _optional_reference(type_id, data, "register_group")
        profile = _optional_string(type_id, data, "profile")

        if kind == FieldTypeKind.SIZE_SELECTOR and not values:
            raise ValueError(f"{source}: {type_id}: size_selector requires values")
        if kind == FieldTypeKind.EFFECTIVE_ADDRESS and profile is None:
            raise ValueError(
                f"{source}: {type_id}: effective_address requires profile"
            )
        if kind == FieldTypeKind.IMMEDIATE and value_type is None:
            raise ValueError(f"{source}: {type_id}: immediate requires value_type")
        if (
            kind
            in {
                FieldTypeKind.REGISTER,
                FieldTypeKind.REGISTER_SELECTOR,
                FieldTypeKind.REGISTER_PAIR_SELECTOR,
            }
            and register_group is None
        ):
            raise ValueError(f"{source}: {type_id}: {kind} requires register_group")

        return cls(
            reference=reference,
            source=source,
            owner=owner,
            id=type_id,
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

    reference: Reference["PayloadType"]
    source: Path
    owner: str
    id: str
    kind: PayloadTypeKind
    bytes: int
    value_type: str | None = None
    signed: bool | None = None
    register_group: Reference["RegisterGroup"] | None = None

    @classmethod
    def from_mapping(
        cls,
        reference: Reference["PayloadType"],
        source: Path,
        owner: str,
        type_id: str,
        data: Mapping[str, Any],
    ) -> "PayloadType":
        _reject_unknown_properties(
            type_id,
            data,
            {"type", "bytes", "value_type", "signed", "register_group"},
        )
        raw_kind = _required_string(type_id, data, "type")
        try:
            kind = PayloadTypeKind(raw_kind)
        except ValueError as error:
            raise ValueError(
                f"{source}: {type_id}: unknown payload type kind {raw_kind!r}"
            ) from error
        byte_count = _positive_int(type_id, data.get("bytes"), "bytes")
        value_type = _optional_string(type_id, data, "value_type")
        signed = data.get("signed")
        if signed is not None and not isinstance(signed, bool):
            raise ValueError(f"{source}: {type_id}: signed must be a boolean")
        if kind == PayloadTypeKind.IMMEDIATE and value_type is None:
            raise ValueError(f"{source}: {type_id}: immediate requires value_type")
        if kind == PayloadTypeKind.PC_ABSOLUTE and signed is None:
            raise ValueError(f"{source}: {type_id}: pc_absolute requires signed")
        register_group = _optional_reference(type_id, data, "register_group")
        if kind == PayloadTypeKind.REGISTER_SELECTOR and register_group is None:
            raise ValueError(
                f"{source}: {type_id}: register_selector requires register_group"
            )
        return cls(
            reference,
            source,
            owner,
            type_id,
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
            for field_reference, field_definition in namespace.field_types.items():
                field_types.register(field_reference, field_definition)
            for payload_reference, payload_definition in namespace.payload_types.items():
                payload_types.register(payload_reference, payload_definition)

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
        reference: Reference[FieldType] = Reference(
            owner, ("field_types",), name
        )
        index.register(
            reference,
            FieldType.from_mapping(reference, path, owner, name, definition),
        )
    return index


def _load_payload_types(owner: str, path: Path) -> ReferenceIndex[PayloadType]:
    index = ReferenceIndex[PayloadType]()
    for name, definition in _load_definitions(path, "payload_types").items():
        reference: Reference[PayloadType] = Reference(
            owner, ("payload_types",), name
        )
        index.register(
            reference,
            PayloadType.from_mapping(reference, path, owner, name, definition),
        )
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
    type_id: str, data: Mapping[str, Any], allowed: set[str]
) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"{type_id}: unknown properties {unknown}")


def _required_string(type_id: str, data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{type_id}: {key} must be a non-empty string")
    return value


def _optional_string(
    type_id: str, data: Mapping[str, Any], key: str
) -> str | None:
    value = data.get(key)
    if value is not None and (not isinstance(value, str) or not value):
        raise ValueError(f"{type_id}: {key} must be a non-empty string")
    return value


def _optional_reference(
    type_id: str, data: Mapping[str, Any], key: str
) -> Reference["RegisterGroup"] | None:
    value = _optional_string(type_id, data, key)
    return None if value is None else Reference.parse(value)


def _positive_int(type_id: str, value: object, key: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{type_id}: {key} must be a positive integer")
    return value


def _field_values(
    type_id: str, raw_values: object, bits: int
) -> tuple[FieldValue, ...]:
    if not isinstance(raw_values, (list, tuple)):
        raise ValueError(f"{type_id}: values must be an array")
    values: list[FieldValue] = []
    for index, raw in enumerate(raw_values):
        if not isinstance(raw, Mapping) or set(raw) != {"value", "code"}:
            raise ValueError(
                f"{type_id}: values[{index}] must contain value and code"
            )
        value = raw["value"]
        code = raw["code"]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{type_id}: values[{index}].value must be an integer")
        if value < 0 or value >= 1 << bits:
            raise ValueError(
                f"{type_id}: selector value {value} does not fit in {bits} bits"
            )
        if not isinstance(code, str) or not code:
            raise ValueError(
                f"{type_id}: values[{index}].code must be a non-empty string"
            )
        values.append(FieldValue(value, code))
    if len({item.value for item in values}) != len(values):
        raise ValueError(f"{type_id}: selector values must be unique")
    if len({item.code for item in values}) != len(values):
        raise ValueError(f"{type_id}: selector codes must be unique")
    return tuple(values)
