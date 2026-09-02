"""Distributed CPUID definition loading and logical lookup."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, cast

from .entity import Entity
from .extension import ExtensionSetCatalog
from .inventory import DirectoryInventory
from .reference import Reference, ReferenceIndex, UnknownReferenceError
from .yaml_document import SchemaValidatedYamlLoader


class CpuidInventory(DirectoryInventory):
    """One closed-world directory inventory in a CPUID namespace."""


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
class CpuidField(Entity):
    """One named field in a 64-bit CPUID result."""

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
class CpuidLayout(Entity):
    """One reusable result layout owned by a CPUID leaf."""

    reference: Reference["CpuidLayout"]
    source: Path
    id: str
    fields: tuple[CpuidField, ...]


@dataclass(frozen=True, slots=True)
class CpuidCommonHeader(Entity):
    """The semantic fields shared by every CPUID index-zero header."""

    reference: Reference["CpuidCommonHeader"]
    source: Path
    id: str
    bits: int
    fields: tuple[CpuidField, ...]


@dataclass(frozen=True, slots=True)
class CpuidQuery(Entity):
    """One fixed or indexed CPUID query definition."""

    reference: Reference["CpuidQuery"]
    source: Path
    id: str
    indexes: CpuidIndexRange
    fields: tuple[CpuidField, ...]


@dataclass(frozen=True, slots=True)
class CpuidLeaf(Entity):
    """Common authored content of one CPUID leaf fragment."""

    reference: Reference["CpuidLeaf"]
    source: Path
    root: Path
    id: str
    name: str
    layouts: Mapping[str, CpuidLayout]
    queries: tuple[CpuidQuery, ...]


@dataclass(frozen=True, slots=True)
class CpuidLeafDefinition(CpuidLeaf):
    value: int


@dataclass(frozen=True, slots=True)
class CpuidLeafOverlay(CpuidLeaf):
    extends: Reference[CpuidLeaf]


@dataclass(frozen=True, slots=True)
class CpuidDiscoveryLeaf(CpuidLeaf):
    pass


@dataclass(frozen=True, slots=True)
class CpuidClass(Entity):
    """Common authored content of one CPUID class fragment."""

    reference: Reference["CpuidClass"]
    source: Path
    root: Path
    id: str
    name: str
    leaf_inventory: CpuidInventory
    leaves: Mapping[str, CpuidLeaf]


@dataclass(frozen=True, slots=True)
class CpuidClassDefinition(CpuidClass):
    value: int


@dataclass(frozen=True, slots=True)
class CpuidClassOverlay(CpuidClass):
    extends: Reference[CpuidClass]


@dataclass(frozen=True, slots=True)
class CpuidNamespace:
    """All CPUID fragments authored by base or one extension."""

    owner: str
    root: Path
    class_inventory: CpuidInventory
    classes: Mapping[str, CpuidClass]


@dataclass(frozen=True, slots=True)
class CpuidReferenceIndexes:
    """Typed global CPUID logical-reference indexes."""

    classes: ReferenceIndex[CpuidClass]
    leaves: ReferenceIndex[CpuidLeaf]
    layouts: ReferenceIndex[CpuidLayout]
    queries: ReferenceIndex[CpuidQuery]
    fields: ReferenceIndex[CpuidField]
    layout_fields: ReferenceIndex[CpuidField]
    common_headers: ReferenceIndex[CpuidCommonHeader]
    common_header_fields: ReferenceIndex[CpuidField]


class CpuidResolutionError(ValueError):
    """A source-located error while resolving a CPUID definition."""

    def __init__(self, source: Path, message: str) -> None:
        super().__init__(message)
        self.source = source


@dataclass(frozen=True, slots=True)
class ResolvedCpuidLeaf:
    """One leaf fragment joined with its root and numeric selector values."""

    leaf: CpuidLeaf
    root_leaf: CpuidLeaf
    class_value: int
    leaf_value: int


@dataclass(frozen=True, slots=True)
class CpuidCatalog:
    """The union of distributed base and extension CPUID definitions."""

    namespaces: Mapping[str, CpuidNamespace]
    common_header: CpuidCommonHeader
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
            ReferenceIndex[CpuidLayout](),
            ReferenceIndex[CpuidQuery](),
            ReferenceIndex[CpuidField](),
            ReferenceIndex[CpuidField](),
            ReferenceIndex[CpuidCommonHeader](),
            ReferenceIndex[CpuidField](),
        )
        common_header = _load_common_header(root, references)
        namespaces: dict[str, CpuidNamespace] = {}
        for owner, namespace_root in extensions.owner_roots():
            namespace = _load_namespace(owner, namespace_root, root, references)
            namespaces[owner] = namespace
        return cls(MappingProxyType(namespaces), common_header, references)

    @property
    def base(self) -> CpuidNamespace:
        return self.namespaces["base"]

    def namespace(self, owner: str) -> CpuidNamespace:
        try:
            return self.namespaces[owner]
        except KeyError as error:
            raise ValueError(f"unknown CPUID namespace {owner!r}") from error

    def root_class(self, cpuid_class: CpuidClass) -> CpuidClassDefinition:
        """Resolve a CPUID class overlay to its numeric class definition."""

        active: list[Reference[CpuidClass]] = []
        current = cpuid_class
        while isinstance(current, CpuidClassOverlay):
            if current.reference in active:
                raise CpuidResolutionError(
                    current.source, "circular CPUID class overlay"
                )
            active.append(current.reference)
            try:
                target = self.references.classes.resolve(current.extends)
            except UnknownReferenceError as error:
                raise CpuidResolutionError(
                    current.source, "unknown CPUID class overlay target"
                ) from error
            if current.id != target.id:
                raise CpuidResolutionError(
                    current.source,
                    f"class ID {current.id!r} does not match overlay target "
                    f"ID {target.id!r}",
                )
            current = target
        if not isinstance(current, CpuidClassDefinition):
            raise CpuidResolutionError(
                current.source, f"incomplete CPUID class definition {current.id!r}"
            )
        return current

    def _extension_discovery_leaf(
        self, cpuid_class: CpuidClass
    ) -> CpuidLeaf | None:
        root_class = self.root_class(cpuid_class)
        if not isinstance(cpuid_class, CpuidClassOverlay) or root_class.value != 1:
            return None
        roots = tuple(
            leaf
            for leaf in cpuid_class.leaves.values()
            if isinstance(leaf, CpuidDiscoveryLeaf)
        )
        if len(roots) != 1:
            raise CpuidResolutionError(
                cpuid_class.leaf_inventory.source,
                "a class-1 extension contribution must own one discovery leaf",
            )
        return roots[0]

    def resolve_leaf(self, leaf: CpuidLeaf) -> ResolvedCpuidLeaf:
        """Resolve one leaf fragment through its definition and overlays."""

        active: list[Reference[CpuidLeaf]] = []

        def resolve(current: CpuidLeaf) -> ResolvedCpuidLeaf:
            if current.reference in active:
                raise CpuidResolutionError(
                    current.source, "circular CPUID leaf overlay"
                )
            if (
                current.reference.path[:1] != ("cpuid",)
                or len(current.reference.path) != 2
            ):
                raise CpuidResolutionError(
                    current.source,
                    f"invalid CPUID leaf reference {current.reference!r}",
                )
            cpuid_class = self.references.classes.resolve(
                Reference(
                    current.reference.owner,
                    ("cpuid",),
                    current.reference.path[1],
                )
            )
            root_class = self.root_class(cpuid_class)
            discovery = self._extension_discovery_leaf(cpuid_class)

            if isinstance(current, CpuidLeafOverlay):
                active.append(current.reference)
                try:
                    target = self.references.leaves.resolve(current.extends)
                except UnknownReferenceError as error:
                    raise CpuidResolutionError(
                        current.source, "unknown CPUID leaf overlay target"
                    ) from error
                resolved = resolve(target)
                active.pop()
                if current.id != target.id:
                    raise CpuidResolutionError(
                        current.source,
                        f"leaf ID {current.id!r} does not match overlay target "
                        f"ID {target.id!r}",
                    )
                if resolved.class_value != root_class.value:
                    raise CpuidResolutionError(
                        current.source,
                        f"CPUID leaf overlay {current.id!r} crosses numeric classes",
                    )
                return ResolvedCpuidLeaf(
                    current,
                    resolved.root_leaf,
                    resolved.class_value,
                    resolved.leaf_value,
                )

            if current is discovery:
                directories = tuple(
                    candidate
                    for candidate in cpuid_class.leaves.values()
                    if isinstance(candidate, CpuidLeafOverlay)
                    and (
                        (resolved := resolve(candidate)).class_value,
                        resolved.leaf_value,
                    )
                    == (1, 0)
                )
                if len(directories) != 1:
                    raise CpuidResolutionError(
                        cpuid_class.leaf_inventory.source,
                        "a class-1 extension contribution must reopen leaf 0 once",
                    )
                directory = directories[0]
                if len(directory.queries) != 1 or len(directory.queries[0].fields) != 1:
                    raise CpuidResolutionError(
                        directory.source,
                        "a class-1 extension directory contribution must own one bit",
                    )
                query = directory.queries[0]
                field = query.fields[0]
                if query.indexes.count != 1 or field.bits != 1:
                    raise CpuidResolutionError(
                        directory.source,
                        "an extension directory bit requires one fixed query index",
                    )
                try:
                    leaf_value = extension_discovery_leaf_value(
                        query.indexes.first, field.lsb
                    )
                except ValueError as error:
                    raise CpuidResolutionError(directory.source, str(error)) from error
                return ResolvedCpuidLeaf(
                    current, current, root_class.value, leaf_value
                )

            if not isinstance(current, CpuidLeafDefinition):
                raise CpuidResolutionError(
                    current.source, f"incomplete CPUID leaf definition {current.id!r}"
                )
            return ResolvedCpuidLeaf(
                current, current, root_class.value, current.value
            )

        return resolve(leaf)

    def resolved_leaves(self) -> tuple[ResolvedCpuidLeaf, ...]:
        """Return all leaf fragments in owner and inventory order."""

        for cpuid_class in self.references.classes.values():
            self._extension_discovery_leaf(cpuid_class)
        return tuple(self.resolve_leaf(leaf) for leaf in self.references.leaves.values())

    def resolve_flag(self, raw_reference: str, source: Path) -> CpuidField:
        """Resolve one fixed-index, one-bit CPUID availability field."""

        reference: Reference[CpuidField] = Reference.parse(raw_reference)
        try:
            field = self.references.fields.resolve(reference)
        except UnknownReferenceError as error:
            raise ValueError(f"{source}: unknown CPUID flag reference") from error
        if field.bits != 1:
            raise ValueError(
                f"{source}: CPUID flag {field.id!r} names a {field.bits}-bit field"
            )
        query_reference: Reference[CpuidQuery] = Reference(
            reference.owner, reference.path[:-1], reference.path[-1]
        )
        query = self.references.queries.resolve(query_reference)
        if query.indexes.count != 1:
            raise ValueError(
                f"{source}: CPUID flag {field.id!r} belongs to an indexed query range"
            )
        return field


def extension_discovery_leaf_value(directory_index: int, directory_bit: int) -> int:
    """Map one class-1 directory slot to its one-to-one discovery leaf."""

    if not 1 <= directory_index <= 1023:
        raise ValueError(
            f"extension directory index {directory_index!r} is outside 1..1023"
        )
    if not 0 <= directory_bit < 64:
        raise ValueError(
            f"extension directory bit {directory_bit!r} is outside 0..63"
        )
    return 64 * (directory_index - 1) + directory_bit + 1


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


def _load_common_header(
    isa_root: Path, references: CpuidReferenceIndexes
) -> CpuidCommonHeader:
    source = isa_root / "cpuid/common_header.yaml"
    raw = _load_validated(source, isa_root / "schemas/cpuid-common-header.yaml")
    reference: Reference[CpuidCommonHeader] = Reference(
        "base", ("cpuid",), raw["id"]
    )
    fields = tuple(
        CpuidField(
            Reference(
                reference.owner,
                (*reference.path, reference.element),
                value["id"],
            ),
            source,
            value["id"],
            value["lsb"],
            value["bits"],
        )
        for value in raw["fields"]
    )
    header = CpuidCommonHeader(reference, source, raw["id"], raw["bits"], fields)
    references.common_headers.register(header.reference, header)
    for field in fields:
        references.common_header_fields.register(field.reference, field)
    return header


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
    common = (
        reference,
        source,
        root,
        class_id,
        document["name"],
        inventory,
        MappingProxyType(leaves),
    )
    if "extends" in document:
        return CpuidClassOverlay(
            *common, Reference.parse(cast(str, document["extends"]))
        )
    return CpuidClassDefinition(*common, document["value"])


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
    raw_layouts = document.get("layouts", {})
    layouts: dict[str, CpuidLayout] = {}
    for layout_id, raw_layout in raw_layouts.items():
        layout_reference: Reference[CpuidLayout] = Reference(
            owner, ("cpuid", class_id, leaf_id), layout_id
        )
        layout_fields = tuple(
            CpuidField(
                reference=Reference(
                    owner,
                    ("cpuid", class_id, leaf_id, layout_id),
                    raw_field["id"],
                ),
                source=source,
                id=raw_field["id"],
                lsb=raw_field["lsb"],
                bits=raw_field["bits"],
            )
            for raw_field in raw_layout["fields"]
        )
        layout = CpuidLayout(layout_reference, source, layout_id, layout_fields)
        references.layouts.register(layout.reference, layout)
        for field in layout_fields:
            references.layout_fields.register(field.reference, field)
        layouts[layout_id] = layout
    queries: list[CpuidQuery] = []
    for raw_query in document["queries"]:
        query_id = raw_query["id"]
        query_reference: Reference[CpuidQuery] = Reference(
            owner, ("cpuid", class_id, leaf_id), query_id
        )
        raw_fields: list[Mapping[str, Any]] = []
        layout_id = raw_query.get("layout")
        if layout_id is not None:
            layout = raw_layouts.get(layout_id)
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
    common = (
        reference,
        source,
        root,
        leaf_id,
        document["name"],
        MappingProxyType(layouts),
        tuple(queries),
    )
    if "extends" in document:
        return CpuidLeafOverlay(
            *common, Reference.parse(cast(str, document["extends"]))
        )
    if "value" in document:
        return CpuidLeafDefinition(*common, document["value"])
    return CpuidDiscoveryLeaf(*common)


def _parse_indexes(raw: object) -> CpuidIndexRange:
    if isinstance(raw, int) and not isinstance(raw, bool):
        return CpuidIndexRange(raw, raw)
    if not isinstance(raw, Mapping):
        raise ValueError(f"invalid CPUID index specification {raw!r}")
    return CpuidIndexRange(raw["first"], raw["last"], raw.get("stride", 1))


def _load_inventory(owner: str, root: Path, key: str) -> CpuidInventory:
    return CpuidInventory.inspect(
        owner=owner,
        kind={"classes": "class", "leaves": "leaf"}[key],
        source=root / f"{key}.yaml",
        root=root,
        key=key,
        allow_missing=True,
    )


def _load_validated(source: Path, schema_path: Path) -> dict[str, Any]:
    return SchemaValidatedYamlLoader().load(source, schema_path)
