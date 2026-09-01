"""Typed field and payload definition namespaces for one ISA tree."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

import yaml

from .entity import Entity
from .extension import ExtensionSetCatalog
from .reference import Reference, ReferenceIndex

if TYPE_CHECKING:
    from .register import RegisterGroup


@dataclass(frozen=True, slots=True)
class FieldValue:
    """One authored value/code pair for a selector field."""

    value: int
    code: str


@dataclass(frozen=True, slots=True)
class FieldType(Entity):
    """Common identity and width of a primary-encoding field type."""

    reference: Reference["FieldType"]
    source: Path
    owner: str
    id: str
    bits: int

    @classmethod
    def from_mapping(
        cls,
        reference: Reference["FieldType"],
        source: Path,
        owner: str,
        type_id: str,
        data: Mapping[str, Any],
    ) -> "FieldType":
        raw_kind = _required_string(type_id, data, "type")
        bits = _positive_int(type_id, data.get("bits"), "bits")
        common = (reference, source, owner, type_id, bits)
        if raw_kind == "register_selector":
            _reject_unknown_properties(type_id, data, {"type", "bits", "register_group"})
            return RegisterSelectorFieldType(
                *common, _required_reference(type_id, data, "register_group")
            )
        if raw_kind == "effective_address":
            _reject_unknown_properties(type_id, data, {"type", "bits", "profile"})
            return EffectiveAddressFieldType(
                *common, _required_string(type_id, data, "profile")
            )
        if raw_kind == "register":
            _reject_unknown_properties(type_id, data, {"type", "bits", "register_group"})
            return RegisterFieldType(
                *common, _required_reference(type_id, data, "register_group")
            )
        if raw_kind == "enum_condition":
            _reject_unknown_properties(type_id, data, {"type", "bits"})
            return EnumConditionFieldType(*common)
        if raw_kind == "register_pair_selector":
            _reject_unknown_properties(type_id, data, {"type", "bits", "register_group"})
            return RegisterPairSelectorFieldType(
                *common, _required_reference(type_id, data, "register_group")
            )
        if raw_kind == "page_table_level":
            _reject_unknown_properties(type_id, data, {"type", "bits"})
            return PageTableLevelFieldType(*common)
        if raw_kind == "flags":
            _reject_unknown_properties(type_id, data, {"type", "bits"})
            return FlagsFieldType(*common)
        if raw_kind == "immediate":
            _reject_unknown_properties(type_id, data, {"type", "bits", "value_type"})
            return ImmediateFieldType(
                *common, _required_string(type_id, data, "value_type")
            )
        if raw_kind == "memory_order":
            _reject_unknown_properties(type_id, data, {"type", "bits"})
            return MemoryOrderFieldType(*common)
        if raw_kind == "size_selector":
            _reject_unknown_properties(type_id, data, {"type", "bits", "values"})
            values = _field_values(type_id, data.get("values", ()), bits)
            if not values:
                raise ValueError(f"{source}: {type_id}: size_selector requires values")
            return SizeSelectorFieldType(*common, values)
        raise ValueError(f"{source}: {type_id}: unknown field type {raw_kind!r}")


@dataclass(frozen=True, slots=True)
class RegisterSelectorFieldType(FieldType):
    register_group: Reference["RegisterGroup"]


@dataclass(frozen=True, slots=True)
class EffectiveAddressFieldType(FieldType):
    profile: str


@dataclass(frozen=True, slots=True)
class RegisterFieldType(FieldType):
    register_group: Reference["RegisterGroup"]


@dataclass(frozen=True, slots=True)
class EnumConditionFieldType(FieldType):
    pass


@dataclass(frozen=True, slots=True)
class RegisterPairSelectorFieldType(FieldType):
    register_group: Reference["RegisterGroup"]


@dataclass(frozen=True, slots=True)
class PageTableLevelFieldType(FieldType):
    pass


@dataclass(frozen=True, slots=True)
class FlagsFieldType(FieldType):
    pass


@dataclass(frozen=True, slots=True)
class ImmediateFieldType(FieldType):
    value_type: str


@dataclass(frozen=True, slots=True)
class MemoryOrderFieldType(FieldType):
    pass


@dataclass(frozen=True, slots=True)
class SizeSelectorFieldType(FieldType):
    values: tuple[FieldValue, ...]


@dataclass(frozen=True, slots=True)
class PayloadType(Entity):
    """Common identity and width of an appended payload type."""

    reference: Reference["PayloadType"]
    source: Path
    owner: str
    id: str
    bytes: int

    @classmethod
    def from_mapping(
        cls,
        reference: Reference["PayloadType"],
        source: Path,
        owner: str,
        type_id: str,
        data: Mapping[str, Any],
    ) -> "PayloadType":
        raw_kind = _required_string(type_id, data, "type")
        byte_count = _positive_int(type_id, data.get("bytes"), "bytes")
        common = (reference, source, owner, type_id, byte_count)
        if raw_kind == "immediate":
            _reject_unknown_properties(type_id, data, {"type", "bytes", "value_type"})
            return ImmediatePayloadType(
                *common, _required_string(type_id, data, "value_type")
            )
        if raw_kind == "pc_displacement":
            _reject_unknown_properties(type_id, data, {"type", "bytes"})
            return PcDisplacementPayloadType(*common)
        if raw_kind == "pc_absolute":
            _reject_unknown_properties(type_id, data, {"type", "bytes", "signed"})
            signed = data.get("signed")
            if not isinstance(signed, bool):
                raise ValueError(f"{source}: {type_id}: pc_absolute requires boolean signed")
            return PcAbsolutePayloadType(*common, signed)
        if raw_kind == "floating_point_constant_id":
            _reject_unknown_properties(type_id, data, {"type", "bytes"})
            return FloatingPointConstantIdPayloadType(*common)
        if raw_kind == "register_selector":
            _reject_unknown_properties(type_id, data, {"type", "bytes", "register_group"})
            return RegisterSelectorPayloadType(
                *common, _required_reference(type_id, data, "register_group")
            )
        if raw_kind == "control_register_selector":
            _reject_unknown_properties(type_id, data, {"type", "bytes"})
            return ControlRegisterSelectorPayloadType(*common)
        raise ValueError(f"{source}: {type_id}: unknown payload type {raw_kind!r}")


@dataclass(frozen=True, slots=True)
class ImmediatePayloadType(PayloadType):
    value_type: str


@dataclass(frozen=True, slots=True)
class PcDisplacementPayloadType(PayloadType):
    pass


@dataclass(frozen=True, slots=True)
class PcAbsolutePayloadType(PayloadType):
    signed: bool


@dataclass(frozen=True, slots=True)
class FloatingPointConstantIdPayloadType(PayloadType):
    pass


@dataclass(frozen=True, slots=True)
class RegisterSelectorPayloadType(PayloadType):
    register_group: Reference["RegisterGroup"]


@dataclass(frozen=True, slots=True)
class ControlRegisterSelectorPayloadType(PayloadType):
    pass


def field_type_source_name(definition: FieldType) -> str:
    """Return the authored type spelling for machine-facing projections."""

    names = {
        RegisterSelectorFieldType: "register_selector",
        EffectiveAddressFieldType: "effective_address",
        RegisterFieldType: "register",
        EnumConditionFieldType: "enum_condition",
        RegisterPairSelectorFieldType: "register_pair_selector",
        PageTableLevelFieldType: "page_table_level",
        FlagsFieldType: "flags",
        ImmediateFieldType: "immediate",
        MemoryOrderFieldType: "memory_order",
        SizeSelectorFieldType: "size_selector",
    }
    try:
        return names[type(definition)]
    except KeyError as error:
        raise TypeError(f"unsupported field type {type(definition).__name__}") from error


def payload_type_source_name(definition: PayloadType) -> str:
    """Return the authored type spelling for machine-facing projections."""

    names = {
        ImmediatePayloadType: "immediate",
        PcDisplacementPayloadType: "pc_displacement",
        PcAbsolutePayloadType: "pc_absolute",
        FloatingPointConstantIdPayloadType: "floating_point_constant_id",
        RegisterSelectorPayloadType: "register_selector",
        ControlRegisterSelectorPayloadType: "control_register_selector",
    }
    try:
        return names[type(definition)]
    except KeyError as error:
        raise TypeError(f"unsupported payload type {type(definition).__name__}") from error


def payload_type_is_signed(definition: PayloadType) -> bool:
    """Return the numeric signedness projected for an appended payload."""

    if isinstance(definition, PcAbsolutePayloadType):
        return definition.signed
    if isinstance(definition, ImmediatePayloadType):
        return definition.value_type == "signed_integer"
    return definition.id.endswith("S")


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
        owner_roots = catalog.owner_roots()
        base_owner, base_root = owner_roots[0]
        base = TypeNamespace.load(base_owner, base_root)
        extensions: dict[str, TypeNamespace] = {}
        for extension_id, extension_root in owner_roots[1:]:
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


def _required_reference(
    type_id: str, data: Mapping[str, Any], key: str
) -> Reference["RegisterGroup"]:
    return Reference.parse(_required_string(type_id, data, key))


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
