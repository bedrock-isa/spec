"""Distributed CPUID allocation loading and logical lookup."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, cast

try:
    from .extension import ExtensionSetCatalog
    from .reference import Reference, ReferenceIndex
    from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from extension import ExtensionSetCatalog
    from reference import Reference, ReferenceIndex
    from yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class CpuidInventory:
    """One closed-world directory inventory in a CPUID namespace."""

    owner: str
    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CpuidIndexRange:
    """An inclusive arithmetic progression of CPUID query indexes."""

    first: int
    last: int
    stride: int = 1

    @property
    def count(self) -> int:
        if self.last < self.first:
            return 0
        return (self.last - self.first) // self.stride + 1

    def contains(self, value: int) -> bool:
        return (
            self.first <= value <= self.last and (value - self.first) % self.stride == 0
        )

    def overlaps(self, other: "CpuidIndexRange") -> bool:
        smaller, larger = (self, other) if self.count <= other.count else (other, self)
        return any(
            larger.contains(value)
            for value in range(smaller.first, smaller.last + 1, smaller.stride)
        )


@dataclass(frozen=True, slots=True)
class CpuidField:
    """One named allocation in a 64-bit CPUID result."""

    reference: Reference["CpuidField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1

    def overlaps(self, other: "CpuidField") -> bool:
        return self.lsb <= other.msb and other.lsb <= self.msb


@dataclass(frozen=True, slots=True)
class CpuidQuery:
    """One fixed or indexed CPUID query allocation."""

    reference: Reference["CpuidQuery"]
    source: Path
    id: str
    indexes: CpuidIndexRange
    fields: tuple[CpuidField, ...]


@dataclass(frozen=True, slots=True)
class CpuidLeaf:
    """One authored leaf definition or overlay fragment."""

    reference: Reference["CpuidLeaf"]
    source: Path
    root: Path
    id: str
    name: str
    value: int | None
    extends: Reference["CpuidLeaf"] | None
    queries: tuple[CpuidQuery, ...]


@dataclass(frozen=True, slots=True)
class CpuidClass:
    """One authored class definition or overlay fragment."""

    reference: Reference["CpuidClass"]
    source: Path
    root: Path
    id: str
    name: str
    value: int | None
    extends: Reference["CpuidClass"] | None
    leaf_inventory: CpuidInventory
    leaves: Mapping[str, CpuidLeaf]


@dataclass(frozen=True, slots=True)
class CpuidNamespace:
    """All CPUID allocations authored by base or one extension."""

    owner: str
    root: Path
    class_inventory: CpuidInventory
    classes: Mapping[str, CpuidClass]


@dataclass(frozen=True, slots=True)
class CpuidReferenceIndexes:
    """Typed global CPUID logical-reference indexes."""

    classes: ReferenceIndex[CpuidClass]
    leaves: ReferenceIndex[CpuidLeaf]
    queries: ReferenceIndex[CpuidQuery]
    fields: ReferenceIndex[CpuidField]


@dataclass(frozen=True, slots=True)
class CpuidCatalog:
    """The union of distributed base and extension CPUID allocations."""

    namespaces: Mapping[str, CpuidNamespace]
    references: CpuidReferenceIndexes

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "CpuidCatalog":
        root = Path(isa_root).resolve()
        extensions = extension_catalog or ExtensionSetCatalog.load(root)
        references = CpuidReferenceIndexes(
            ReferenceIndex[CpuidClass](),
            ReferenceIndex[CpuidLeaf](),
            ReferenceIndex[CpuidQuery](),
            ReferenceIndex[CpuidField](),
        )
        namespaces: dict[str, CpuidNamespace] = {}
        for owner, namespace_root in (
            ("base", root),
            *(
                (extension_id, extensions.root / extension_id)
                for extension_id in extensions.declared
            ),
        ):
            namespace = _load_namespace(owner, namespace_root, root, references)
            namespaces[owner] = namespace
        return cls(MappingProxyType(namespaces), references)

    @property
    def base(self) -> CpuidNamespace:
        return self.namespaces["base"]

    def namespace(self, owner: str) -> CpuidNamespace:
        try:
            return self.namespaces[owner]
        except KeyError as error:
            raise ValueError(f"unknown CPUID namespace {owner!r}") from error


def compose_selector(class_value: int, leaf_value: int, index: int) -> int:
    """Compose the fixed architectural CPUID selector representation."""

    for name, value, limit in (
        ("class", class_value, 1 << 32),
        ("leaf", leaf_value, 1 << 16),
        ("index", index, 1 << 16),
    ):
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value < limit
        ):
            raise ValueError(f"CPUID {name} value {value!r} is out of range")
    return class_value << 32 | leaf_value << 16 | index


def _load_namespace(
    owner: str,
    namespace_root: Path,
    isa_root: Path,
    references: CpuidReferenceIndexes,
) -> CpuidNamespace:
    classes_root = namespace_root / "cpuid/classes"
    inventory = _load_inventory(owner, classes_root, "classes")
    classes: dict[str, CpuidClass] = {}
    for class_id in inventory.declared:
        class_root = classes_root / class_id
        if class_id in classes or not class_root.is_dir():
            continue
        cpuid_class = _load_class(owner, class_root, isa_root, references)
        references.classes.register(cpuid_class.reference, cpuid_class)
        classes[class_id] = cpuid_class
    return CpuidNamespace(owner, namespace_root, inventory, MappingProxyType(classes))


def _load_class(
    owner: str,
    root: Path,
    isa_root: Path,
    references: CpuidReferenceIndexes,
) -> CpuidClass:
    source = root / "class.yaml"
    document = _load_validated(source, isa_root / "schemas/cpuid-class.yaml")
    class_id = document["id"]
    if class_id != root.name:
        raise ValueError(
            f"{source}: class ID {class_id!r} does not match directory {root.name!r}"
        )
    reference: Reference[CpuidClass] = Reference(owner, ("cpuid",), class_id)
    leaves_root = root / "leaves"
    inventory = _load_inventory(owner, leaves_root, "leaves")
    leaves: dict[str, CpuidLeaf] = {}
    for leaf_id in inventory.declared:
        leaf_root = leaves_root / leaf_id
        if leaf_id in leaves or not leaf_root.is_dir():
            continue
        leaf = _load_leaf(owner, class_id, leaf_root, isa_root, references)
        references.leaves.register(leaf.reference, leaf)
        leaves[leaf_id] = leaf
    return CpuidClass(
        reference=reference,
        source=source,
        root=root,
        id=class_id,
        name=document["name"],
        value=document.get("value"),
        extends=_optional_class_reference(document.get("extends")),
        leaf_inventory=inventory,
        leaves=MappingProxyType(leaves),
    )


def _load_leaf(
    owner: str,
    class_id: str,
    root: Path,
    isa_root: Path,
    references: CpuidReferenceIndexes,
) -> CpuidLeaf:
    source = root / "leaf.yaml"
    document = _load_validated(source, isa_root / "schemas/cpuid-leaf.yaml")
    leaf_id = document["id"]
    if leaf_id != root.name:
        raise ValueError(
            f"{source}: leaf ID {leaf_id!r} does not match directory {root.name!r}"
        )
    reference: Reference[CpuidLeaf] = Reference(
        owner, ("cpuid", class_id), leaf_id
    )
    layouts = document.get("layouts", {})
    queries: list[CpuidQuery] = []
    for raw_query in document["queries"]:
        query_id = raw_query["id"]
        query_reference: Reference[CpuidQuery] = Reference(
            owner, ("cpuid", class_id, leaf_id), query_id
        )
        raw_fields: list[Mapping[str, Any]] = []
        layout_id = raw_query.get("layout")
        if layout_id is not None:
            layout = layouts.get(layout_id)
            if layout is None:
                raise ValueError(
                    f"{source}: query {query_id!r} uses unknown layout {layout_id!r}"
                )
            raw_fields.extend(layout["fields"])
        raw_fields.extend(raw_query.get("fields", ()))
        fields = tuple(
            CpuidField(
                reference=Reference(
                    owner, ("cpuid", class_id, leaf_id, query_id), raw_field["id"]
                ),
                source=source,
                id=raw_field["id"],
                lsb=raw_field["lsb"],
                bits=raw_field["bits"],
            )
            for raw_field in raw_fields
        )
        query = CpuidQuery(
            reference=query_reference,
            source=source,
            id=query_id,
            indexes=_parse_indexes(raw_query["index"]),
            fields=fields,
        )
        references.queries.register(query.reference, query)
        for field in fields:
            references.fields.register(field.reference, field)
        queries.append(query)
    return CpuidLeaf(
        reference=reference,
        source=source,
        root=root,
        id=leaf_id,
        name=document["name"],
        value=document.get("value"),
        extends=_optional_leaf_reference(document.get("extends")),
        queries=tuple(queries),
    )


def _parse_indexes(raw: object) -> CpuidIndexRange:
    if isinstance(raw, int) and not isinstance(raw, bool):
        return CpuidIndexRange(raw, raw)
    if not isinstance(raw, Mapping):
        raise ValueError(f"invalid CPUID index allocation {raw!r}")
    return CpuidIndexRange(raw["first"], raw["last"], raw.get("stride", 1))


def _optional_class_reference(raw: object) -> Reference[CpuidClass] | None:
    return None if raw is None else Reference.parse(cast(str, raw))


def _optional_leaf_reference(raw: object) -> Reference[CpuidLeaf] | None:
    return None if raw is None else Reference.parse(cast(str, raw))


def _load_inventory(owner: str, root: Path, key: str) -> CpuidInventory:
    source = root / f"{key}.yaml"
    if not source.is_file():
        return CpuidInventory(owner, source, root, (), _actual_directories(root))
    document = _load_mapping(source)
    values = document.get(key)
    if not isinstance(values, list) or any(
        not isinstance(value, str) for value in values
    ):
        raise ValueError(f"{source}: expected a {key} list of strings")
    return CpuidInventory(owner, source, root, tuple(values), _actual_directories(root))


def _actual_directories(root: Path) -> tuple[str, ...]:
    if not root.is_dir():
        return ()
    return tuple(
        sorted(
            path.name
            for path in root.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
    )


def _load_validated(source: Path, schema_path: Path) -> dict[str, Any]:
    return SchemaValidatedYamlLoader().load(source, schema_path)


def _load_mapping(path: Path) -> dict[str, Any]:
    return YamlDocumentLoader().mapping(path)
