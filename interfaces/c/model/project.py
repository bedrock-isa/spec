"""Typed catalogs for the Bedrock C target interface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from collections.abc import Mapping
from typing import TYPE_CHECKING, TypeAlias, TypeVar, cast

from engine.dependency import EntityDependency
from engine.entity import (
    Entity,
    EntityCatalog,
    EntityDisplayStyle,
    EntityKind,
)
from engine.reference import QualifiedReference, Reference, ReferenceIndex
from engine.yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader

if TYPE_CHECKING:
    from engine.project import InstructionBundle
    from engine.register import RegisterGroup
    from engine.workspace import SpecWorkspace


SignatureType: TypeAlias = str | QualifiedReference["InterfaceType"]
_T = TypeVar("_T")


@dataclass(frozen=True, slots=True)
class InterfaceGroup:
    reference: Reference["InterfaceGroup"]
    id: str
    title: str
    source: Path
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class InterfaceType:
    reference: Reference["InterfaceType"]
    id: str
    owner: str
    group: str
    kind: str
    source: Path
    data: Mapping[str, object]
    enum_source: QualifiedReference["RegisterGroup"] | None
    field_types: tuple[SignatureType, ...]


@dataclass(frozen=True, slots=True)
class InterfaceIntrinsic:
    reference: Reference["InterfaceIntrinsic"]
    id: str
    owner: str
    group: str
    source: Path
    operation: QualifiedReference["InstructionBundle"]
    data: Mapping[str, object]
    result_type: SignatureType
    parameter_types: tuple[SignatureType, ...]

    @property
    def c_spelling(self) -> str:
        return f"__bedrock_{self.id}"

    @property
    def clang_builtin(self) -> str:
        return f"__builtin_bedrock_{self.id}"


@dataclass(frozen=True, slots=True)
class InterfaceExtension:
    id: str
    requires: tuple[str, ...]
    requires_isa: tuple[str, ...]
    source: Path


@dataclass(frozen=True, slots=True)
class InterfaceUtility:
    reference: Reference["InterfaceUtility"]
    id: str
    owner: str
    group: str
    source: Path
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class InterfaceCollection:
    id: str
    groups: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CInterfaceProject:
    """Loaded C target-interface groups, types, and intrinsics."""

    root: Path
    extensions: Mapping[str, InterfaceExtension]
    type_groups: ReferenceIndex[InterfaceGroup]
    intrinsic_groups: ReferenceIndex[InterfaceGroup]
    utility_groups: ReferenceIndex[InterfaceGroup]
    types: ReferenceIndex[InterfaceType]
    intrinsics: ReferenceIndex[InterfaceIntrinsic]
    utilities: ReferenceIndex[InterfaceUtility]
    collections: Mapping[str, InterfaceCollection]
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path) -> "CInterfaceProject":
        domain_root = Path(root).resolve()
        extensions = _load_extensions(domain_root)
        type_groups, loaded_types = _load_groups(
            domain_root, "types", "type", extensions
        )
        intrinsic_groups, loaded_intrinsics = _load_groups(
            domain_root, "intrinsics", "intrinsic", extensions
        )
        utility_groups, loaded_utilities = _load_groups(
            domain_root, "utilities", "utility", extensions
        )
        types = cast(ReferenceIndex[InterfaceType], loaded_types)
        intrinsics = cast(ReferenceIndex[InterfaceIntrinsic], loaded_intrinsics)
        utilities = cast(ReferenceIndex[InterfaceUtility], loaded_utilities)
        collections = _load_collections(domain_root, intrinsic_groups)
        entities = _build_entities(
            type_groups,
            intrinsic_groups,
            utility_groups,
            types,
            intrinsics,
            utilities,
        )
        return cls(
            domain_root,
            extensions,
            type_groups,
            intrinsic_groups,
            utility_groups,
            types,
            intrinsics,
            utilities,
            collections,
            entities,
        )

    def resolve(self, reference: Reference[_T]) -> _T:
        entity = self.entities.resolve(cast(Reference[Entity], reference))
        return cast(_T, entity.value)

    def entity_dependencies(self) -> tuple[EntityDependency, ...]:
        """Return target-interface relationships intentionally exposed to tooling."""

        result: list[EntityDependency] = []
        for definition in self.types.values():
            source = cast(Reference[object], definition.reference)
            if definition.enum_source is not None:
                result.append(
                    EntityDependency(
                        source,
                        cast(QualifiedReference[object], definition.enum_source),
                        "enum-register-group",
                    )
                )
            for target in definition.field_types:
                if isinstance(target, QualifiedReference):
                    result.append(
                        EntityDependency(
                            source,
                            cast(QualifiedReference[object], target),
                            "interface-field-type",
                        )
                    )
        for definition in self.intrinsics.values():
            source = cast(Reference[object], definition.reference)
            result.append(
                EntityDependency(
                    source,
                    cast(QualifiedReference[object], definition.operation),
                    "intrinsic-instruction",
                )
            )
            for target in (definition.result_type, *definition.parameter_types):
                if isinstance(target, QualifiedReference):
                    result.append(
                        EntityDependency(
                            source,
                            cast(QualifiedReference[object], target),
                            "signature-type",
                        )
                    )
        return tuple(result)

    def validate(self, workspace: "SpecWorkspace") -> None:
        """Resolve every cross-domain and local entity reference."""

        for intrinsic in self.intrinsics.values():
            operation = workspace.resolve(intrinsic.operation)
            allowed_isa_owners = self._allowed_isa_owners(intrinsic.owner)
            if operation.owner not in allowed_isa_owners:
                raise ValueError(
                    f"{intrinsic.source}: owner {intrinsic.owner!r} cannot lower "
                    f"to ISA owner {operation.owner!r}; "
                    f"allowed ISA owners are "
                    f"{sorted(allowed_isa_owners)}"
                )
            for type_name in (intrinsic.result_type, *intrinsic.parameter_types):
                if isinstance(type_name, QualifiedReference):
                    target_type = workspace.resolve(type_name)
                    if not isinstance(target_type, InterfaceType):
                        raise ValueError(
                            f"{intrinsic.source}: signature reference does not "
                            "name an interface type"
                        )
        for interface_type in self.types.values():
            if interface_type.enum_source is not None:
                workspace.resolve(interface_type.enum_source)
            for field_type in interface_type.field_types:
                if isinstance(field_type, QualifiedReference):
                    target_type = workspace.resolve(field_type)
                    if not isinstance(target_type, InterfaceType):
                        raise ValueError(
                            f"{interface_type.source}: field reference does not "
                            "name an interface type"
                        )

    def _allowed_isa_owners(self, owner: str) -> set[str]:
        allowed = {"base"}
        pending = [owner] if owner != "base" else []
        seen: set[str] = set()
        while pending:
            extension_id = pending.pop()
            if extension_id in seen:
                continue
            seen.add(extension_id)
            extension = self.extensions[extension_id]
            allowed.update(extension.requires_isa)
            pending.extend(extension.requires)
        return allowed


def _build_entities(
    type_groups: ReferenceIndex[InterfaceGroup],
    intrinsic_groups: ReferenceIndex[InterfaceGroup],
    utility_groups: ReferenceIndex[InterfaceGroup],
    types: ReferenceIndex[InterfaceType],
    intrinsics: ReferenceIndex[InterfaceIntrinsic],
    utilities: ReferenceIndex[InterfaceUtility],
) -> EntityCatalog:
    index = ReferenceIndex[Entity]()
    catalogs: tuple[tuple[EntityKind, ReferenceIndex[object], EntityDisplayStyle], ...] = (
        (
            EntityKind.INTERFACE_TYPE_GROUP,
            cast(ReferenceIndex[object], type_groups),
            EntityDisplayStyle.TEXT,
        ),
        (
            EntityKind.INTERFACE_INTRINSIC_GROUP,
            cast(ReferenceIndex[object], intrinsic_groups),
            EntityDisplayStyle.TEXT,
        ),
        (
            EntityKind.INTERFACE_UTILITY_GROUP,
            cast(ReferenceIndex[object], utility_groups),
            EntityDisplayStyle.TEXT,
        ),
        (
            EntityKind.INTERFACE_TYPE,
            cast(ReferenceIndex[object], types),
            EntityDisplayStyle.CODE,
        ),
        (
            EntityKind.INTERFACE_INTRINSIC,
            cast(ReferenceIndex[object], intrinsics),
            EntityDisplayStyle.CODE,
        ),
        (
            EntityKind.INTERFACE_UTILITY,
            cast(ReferenceIndex[object], utilities),
            EntityDisplayStyle.CODE,
        ),
    )
    for kind, values, style in catalogs:
        for typed_reference, value in values.items():
            reference = cast(Reference[Entity], typed_reference)
            display = (
                value.title if isinstance(value, InterfaceGroup) else value.id
            )
            index.register(
                reference,
                Entity(reference, kind, display, value.source, value, style),
            )
    return EntityCatalog(index)


def _load_groups(
    root: Path,
    kind: str,
    singular: str,
    extensions: Mapping[str, InterfaceExtension],
) -> tuple[ReferenceIndex[InterfaceGroup], ReferenceIndex[object]]:
    groups_root = root / kind / "groups"
    declared = _load_inventory(groups_root / "groups.yaml", "groups")
    actual = _actual_directories(groups_root)
    if declared != actual:
        raise ValueError(
            f"{groups_root}: declared {kind} groups {declared} do not match "
            f"actual groups {actual}"
        )
    group_schema = root / "schemas/group.yaml"
    entity_schema = root / f"schemas/{singular}.yaml"
    groups = ReferenceIndex[InterfaceGroup]()
    entities = ReferenceIndex[object]()
    for group_id in declared:
        group_root = groups_root / group_id
        group_data = SchemaValidatedYamlLoader().load(
            group_root / "group.yaml", group_schema
        )
        if group_data["id"] != group_id:
            raise ValueError(
                f"{group_root}/group.yaml: group ID must match directory {group_id!r}"
            )
        group_reference: Reference[InterfaceGroup] = Reference(
            "base", (kind,), group_id
        )
        groups.register(
            group_reference,
            InterfaceGroup(
                group_reference,
                group_id,
                str(group_data["title"]),
                group_root / "group.yaml",
                MappingProxyType(group_data),
            ),
        )
        entities_root = group_root / kind
        entity_ids = _load_inventory(entities_root / f"{kind}.yaml", kind)
        actual_entities = _actual_directories(entities_root)
        if entity_ids != actual_entities:
            raise ValueError(
                f"{entities_root}: declared {kind} {entity_ids} do not match "
                f"actual entries {actual_entities}"
            )
        for entity_id in entity_ids:
            source = entities_root / entity_id / f"{singular}.yaml"
            data = SchemaValidatedYamlLoader().load(source, entity_schema)
            if data["id"] != entity_id:
                raise ValueError(f"{source}: ID must match directory {entity_id!r}")
            owner = str(data["owner"])
            if owner != "base" and owner not in extensions:
                raise ValueError(f"{source}: unknown interface owner {owner!r}")
            reference: Reference[object] = Reference(
                owner, (kind, group_id), entity_id
            )
            entity: object
            if kind == "types":
                enum_source = _enum_source(data)
                field_types = _struct_field_types(data, source)
                entity = InterfaceType(
                    cast(Reference[InterfaceType], reference),
                    entity_id,
                    owner,
                    group_id,
                    str(data["kind"]),
                    source,
                    MappingProxyType(data),
                    enum_source,
                    field_types,
                )
            elif kind == "intrinsics":
                operation = cast(
                    "QualifiedReference[InstructionBundle]",
                    QualifiedReference.parse(data["lowering"]["operation"]),
                )
                if operation.domain != "isa":
                    raise ValueError(f"{source}: lowering operation must be in isa")
                result_type, parameter_types = _signature_types(data, source)
                entity = InterfaceIntrinsic(
                    cast(Reference[InterfaceIntrinsic], reference),
                    entity_id,
                    owner,
                    group_id,
                    source,
                    operation,
                    MappingProxyType(data),
                    result_type,
                    parameter_types,
                )
            else:
                entity = InterfaceUtility(
                    cast(Reference[InterfaceUtility], reference),
                    entity_id,
                    owner,
                    group_id,
                    source,
                    MappingProxyType(data),
                )
            entities.register(reference, entity)
    return groups, entities


def _load_inventory(path: Path, key: str) -> tuple[str, ...]:
    values = YamlDocumentLoader().mapping(path).get(key)
    if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
        raise ValueError(f"{path}: expected a {key} list of strings")
    if len(set(values)) != len(values):
        raise ValueError(f"{path}: duplicate {key} entries")
    return tuple(values)


def _actual_directories(root: Path) -> tuple[str, ...]:
    return tuple(
        sorted(
            path.name
            for path in root.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
    )


def _load_extensions(root: Path) -> Mapping[str, InterfaceExtension]:
    extensions_root = root / "extensions"
    declared = _load_inventory(extensions_root / "extensions.yaml", "extensions")
    actual = _actual_directories(extensions_root)
    if declared != actual:
        raise ValueError(
            f"{extensions_root}: declared extensions {declared} do not match "
            f"actual extensions {actual}"
        )
    schema = root / "schemas/extension.yaml"
    loaded: dict[str, InterfaceExtension] = {}
    for extension_id in declared:
        source = extensions_root / extension_id / "extension.yaml"
        data = SchemaValidatedYamlLoader().load(source, schema)
        if data["id"] != extension_id:
            raise ValueError(f"{source}: ID must match directory {extension_id!r}")
        loaded[extension_id] = InterfaceExtension(
            extension_id,
            tuple(data.get("requires", ())),
            tuple(data.get("requires-isa", ())),
            source,
        )
    for extension in loaded.values():
        unknown = sorted(set(extension.requires) - set(loaded))
        if unknown:
            raise ValueError(f"{extension.source}: unknown requirements {unknown}")
    _validate_extension_cycles(loaded)
    return MappingProxyType(loaded)


def _validate_extension_cycles(extensions: Mapping[str, InterfaceExtension]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(extension_id: str) -> None:
        if extension_id in visiting:
            raise ValueError(f"cyclic interface extension dependency at {extension_id}")
        if extension_id in visited:
            return
        visiting.add(extension_id)
        for required in extensions[extension_id].requires:
            visit(required)
        visiting.remove(extension_id)
        visited.add(extension_id)

    for extension_id in extensions:
        visit(extension_id)


def _looks_like_local_reference(value: str) -> bool:
    return value.startswith("base.") or bool(
        value and value.split(".", 1)[0].isupper() and "." in value
    )


def _signature_type(value: object, source: Path) -> SignatureType:
    if not isinstance(value, str):
        raise ValueError(f"{source}: signature type must be a string")
    if ":" not in value and not _looks_like_local_reference(value):
        return value
    return cast(
        QualifiedReference[InterfaceType],
        QualifiedReference.parse(value, current_domain="interfaces.c"),
    )


def _signature_types(
    data: Mapping[str, object], source: Path
) -> tuple[SignatureType, tuple[SignatureType, ...]]:
    signature = data["signature"]
    if not isinstance(signature, Mapping):
        raise ValueError(f"{source}: signature must be a mapping")
    parameters = signature["parameters"]
    if not isinstance(parameters, list):
        raise ValueError(f"{source}: signature parameters must be a list")
    return (
        _signature_type(signature["result"], source),
        tuple(
            _signature_parameter_type(parameter, source) for parameter in parameters
        ),
    )


def _signature_parameter_type(parameter: object, source: Path) -> SignatureType:
    if not isinstance(parameter, Mapping):
        raise ValueError(f"{source}: signature parameter must be a mapping")
    return _signature_type(parameter["type"], source)


def _struct_field_types(
    data: Mapping[str, object], source: Path
) -> tuple[SignatureType, ...]:
    fields = data.get("fields", ())
    if not isinstance(fields, (list, tuple)):
        raise ValueError(f"{source}: struct fields must be a list")
    result: list[SignatureType] = []
    for field in fields:
        if not isinstance(field, Mapping):
            raise ValueError(f"{source}: struct field must be a mapping")
        result.append(_signature_type(field.get("type"), source))
    return tuple(result)


def _enum_source(
    data: Mapping[str, object],
) -> QualifiedReference[RegisterGroup] | None:
    values = data.get("values")
    if not isinstance(values, Mapping) or "source" not in values:
        return None
    return cast(
        "QualifiedReference[RegisterGroup]",
        QualifiedReference.parse(values["source"]),
    )


def _load_collections(
    root: Path, groups: ReferenceIndex[InterfaceGroup]
) -> Mapping[str, InterfaceCollection]:
    source = root / "intrinsics/collections/collections.yaml"
    raw = YamlDocumentLoader().mapping(source).get("collections")
    if not isinstance(raw, list):
        raise ValueError(f"{source}: expected a collections list")
    available = {group.id for group in groups.values()}
    collections: dict[str, InterfaceCollection] = {}
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError(f"{source}: collection entries must be mappings")
        collection_id = item.get("id")
        members = item.get("groups")
        if not isinstance(collection_id, str) or not isinstance(members, list):
            raise ValueError(f"{source}: collection needs id and groups")
        if collection_id in collections:
            raise ValueError(f"{source}: duplicate collection {collection_id!r}")
        member_ids = tuple(str(member) for member in members)
        unknown = sorted(set(member_ids) - available)
        if unknown:
            raise ValueError(f"{source}: unknown groups {unknown}")
        collections[collection_id] = InterfaceCollection(
            collection_id, member_ids
        )
    return MappingProxyType(collections)
