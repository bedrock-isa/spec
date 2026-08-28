"""Typed catalogs for the Bedrock C target interface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from collections.abc import Mapping
from typing import TYPE_CHECKING

from engine.reference import QualifiedReference, Reference, ReferenceIndex
from engine.yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader

if TYPE_CHECKING:
    from engine.workspace import SpecWorkspace


@dataclass(frozen=True, slots=True)
class InterfaceGroup:
    reference: Reference
    id: str
    title: str
    source: Path
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class InterfaceType:
    reference: Reference
    id: str
    owner: str
    group: str
    kind: str
    source: Path
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class InterfaceIntrinsic:
    reference: Reference
    id: str
    owner: str
    group: str
    source: Path
    operation: QualifiedReference
    data: Mapping[str, object]

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
    reference: Reference
    id: str
    owner: str
    group: str
    kind: str
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

    @classmethod
    def load(cls, root: str | Path) -> "CInterfaceProject":
        domain_root = Path(root).resolve()
        extensions = _load_extensions(domain_root)
        type_groups, types = _load_groups(
            domain_root, "types", "type", extensions
        )
        intrinsic_groups, intrinsics = _load_groups(
            domain_root, "intrinsics", "intrinsic", extensions
        )
        utility_groups, utilities = _load_groups(
            domain_root, "utilities", "utility", extensions
        )
        collections = _load_collections(domain_root, intrinsic_groups)
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
        )

    def resolve(self, reference: str | Reference) -> object:
        normalized = Reference.parse(reference)
        indexes: tuple[ReferenceIndex[object], ...] = (
            self.type_groups,
            self.intrinsic_groups,
            self.utility_groups,
            self.types,
            self.intrinsics,
            self.utilities,
        )
        for index in indexes:
            if normalized in index:
                return index.resolve(normalized)
        raise ValueError(f"unknown interfaces.c reference {normalized}")

    def validate(self, workspace: "SpecWorkspace") -> None:
        """Resolve every cross-domain and local entity reference."""

        for intrinsic in self.intrinsics.values():
            workspace.resolve(intrinsic.operation)
            allowed_isa_owners = self._allowed_isa_owners(intrinsic.owner)
            if intrinsic.operation.local.owner not in allowed_isa_owners:
                raise ValueError(
                    f"{intrinsic.source}: owner {intrinsic.owner!r} cannot lower "
                    f"to {intrinsic.operation}; allowed ISA owners are "
                    f"{sorted(allowed_isa_owners)}"
                )
            signature = intrinsic.data["signature"]
            type_names = [signature["result"]]
            type_names.extend(
                parameter["type"] for parameter in signature["parameters"]
            )
            for type_name in type_names:
                if isinstance(type_name, str) and _looks_like_local_reference(
                    type_name
                ):
                    workspace.resolve(type_name, current_domain="interfaces.c")
        for interface_type in self.types.values():
            values = interface_type.data.get("values")
            if isinstance(values, Mapping) and isinstance(values.get("source"), str):
                workspace.resolve(str(values["source"]))

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


def _load_groups(
    root: Path,
    kind: str,
    singular: str,
    extensions: Mapping[str, InterfaceExtension],
) -> tuple[ReferenceIndex[InterfaceGroup], ReferenceIndex]:
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
    entities = ReferenceIndex()
    for group_id in declared:
        group_root = groups_root / group_id
        group_data = SchemaValidatedYamlLoader().load(
            group_root / "group.yaml", group_schema
        )
        if group_data["id"] != group_id:
            raise ValueError(
                f"{group_root}/group.yaml: group ID must match directory {group_id!r}"
            )
        group_reference = Reference("base", (kind,), group_id)
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
            reference = Reference(owner, (kind, group_id), entity_id)
            if kind == "types":
                entity = InterfaceType(
                    reference,
                    entity_id,
                    owner,
                    group_id,
                    str(data["kind"]),
                    source,
                    MappingProxyType(data),
                )
            elif kind == "intrinsics":
                operation = QualifiedReference.parse(str(data["lowering"]["operation"]))
                if operation.domain != "isa":
                    raise ValueError(f"{source}: lowering operation must be in isa")
                entity = InterfaceIntrinsic(
                    reference,
                    entity_id,
                    owner,
                    group_id,
                    source,
                    operation,
                    MappingProxyType(data),
                )
            else:
                entity = InterfaceUtility(
                    reference,
                    entity_id,
                    owner,
                    group_id,
                    str(data["kind"]),
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
