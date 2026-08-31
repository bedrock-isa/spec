"""Hierarchical architectural-register definitions and lookup."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, cast

from .extension import ExtensionSetCatalog
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class VariableRegisterWidth:
    """One symbolic register width and its permitted concrete bit widths."""

    expression: str
    values: tuple[int, ...]

    @property
    def minimum(self) -> int:
        return self.values[0]

    @property
    def maximum(self) -> int:
        return self.values[-1]


RegisterWidth = int | VariableRegisterWidth


@dataclass(frozen=True, slots=True)
class ResetSpec:
    """One static reset value, register source, or lifecycle policy."""

    value: int | None = None
    source: Reference["Register"] | None = None
    cold: str | None = None
    warm: str | None = None


@dataclass(frozen=True, slots=True)
class RegisterField:
    """One named field in an architectural register image."""

    id: str
    lsb: int
    bits: int
    summary: str | None = None

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1

    def overlaps(self, other: "RegisterField") -> bool:
        return self.lsb <= other.msb and other.lsb <= self.msb


@dataclass(frozen=True, slots=True)
class RegisterLayout:
    """A fixed companion describing one shared or register-local image."""

    source: Path
    bits: int
    fields: tuple[RegisterField, ...]


@dataclass(frozen=True, slots=True)
class Register:
    """One architectural register, authored explicitly or expanded from a series."""

    reference: Reference["Register"]
    source: Path
    root: Path
    owner: str
    group: str
    id: str
    width: RegisterWidth
    encoding: int | None
    summary: str | None
    reset: ResetSpec | None
    layout: RegisterLayout | None


@dataclass(frozen=True, slots=True)
class RegisterInventory:
    """One closed-world group or explicit-register directory inventory."""

    owner: str
    kind: str
    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RegisterSeries:
    """One homogeneous, consecutively encoded register family."""

    prefix: str
    count: int


@dataclass(frozen=True, slots=True)
class RegisterGroup:
    """A homogeneous architectural register group."""

    reference: Reference["RegisterGroup"]
    source: Path
    root: Path
    owner: str
    id: str
    width: RegisterWidth
    summary: str | None
    reset: ResetSpec | None
    layout: RegisterLayout | None
    series: RegisterSeries | None
    register_inventory: RegisterInventory | None
    registers: Mapping[str, Register]


@dataclass(frozen=True, slots=True)
class RegisterNamespace:
    """Register groups owned by base or one declared extension."""

    owner: str
    root: Path
    group_inventory: RegisterInventory
    groups: Mapping[str, RegisterGroup]


@dataclass(frozen=True, slots=True)
class RegisterReferenceIndexes:
    """Typed logical-reference indexes for groups and registers."""

    groups: ReferenceIndex[RegisterGroup]
    registers: ReferenceIndex[Register]


@dataclass(frozen=True, slots=True)
class RegisterCatalog:
    """The union of hierarchical base and extension register namespaces."""

    namespaces: Mapping[str, RegisterNamespace]
    references: RegisterReferenceIndexes

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "RegisterCatalog":
        root = Path(isa_root).resolve()
        extensions = extension_catalog or ExtensionSetCatalog.load(root)
        schema_root = root / "schemas"
        namespace_roots = (
            root,
            *(extensions.root / extension_id for extension_id in extensions.declared),
        )
        manifests = tuple(
            namespace_root / "registers/groups/groups.yaml"
            for namespace_root in namespace_roots
        )
        schemas = (
            {
                "group": _load_mapping(schema_root / "register-group.yaml"),
                "register": _load_mapping(schema_root / "register.yaml"),
                "layout": _load_mapping(schema_root / "register-layout.yaml"),
            }
            if any(path.is_file() for path in manifests)
            else {}
        )
        references = RegisterReferenceIndexes(
            ReferenceIndex[RegisterGroup](), ReferenceIndex[Register]()
        )
        namespaces: dict[str, RegisterNamespace] = {}
        for owner, namespace_root in zip(
            ("base", *extensions.declared), namespace_roots, strict=True
        ):
            namespaces[owner] = _load_namespace(
                owner, namespace_root, schemas, references
            )
        return cls(MappingProxyType(namespaces), references)

    @property
    def base(self) -> RegisterNamespace:
        return self.namespaces["base"]

    def namespace(self, owner: str) -> RegisterNamespace:
        try:
            return self.namespaces[owner]
        except KeyError as error:
            raise ValueError(f"unknown register namespace {owner!r}") from error


def _load_namespace(
    owner: str,
    namespace_root: Path,
    schemas: Mapping[str, Mapping[str, object]],
    references: RegisterReferenceIndexes,
) -> RegisterNamespace:
    groups_root = namespace_root / "registers/groups"
    inventory = _load_inventory(owner, "group", groups_root, "groups")
    groups: dict[str, RegisterGroup] = {}
    for group_id in inventory.declared:
        group_root = groups_root / group_id
        if group_id in groups or not group_root.is_dir():
            continue
        group = _load_group(owner, group_root, schemas, references)
        references.groups.register(group.reference, group)
        groups[group_id] = group
    return RegisterNamespace(owner, namespace_root, inventory, MappingProxyType(groups))


def _load_group(
    owner: str,
    root: Path,
    schemas: Mapping[str, Mapping[str, object]],
    references: RegisterReferenceIndexes,
) -> RegisterGroup:
    source = root / "group.yaml"
    raw = _load_validated(source, schemas["group"])
    group_id = raw["id"]
    if group_id != root.name:
        raise ValueError(
            f"{source}: register group ID {group_id!r} does not match directory {root.name!r}"
        )
    reference: Reference[RegisterGroup] = Reference(
        owner, ("registers",), group_id
    )
    width = _decode_width(raw["width"], source)
    reset = _decode_reset(raw.get("reset"))
    layout = _load_layout(root / "layout.yaml", schemas["layout"])
    registers_root = root / "registers"
    has_series = "series" in raw
    has_explicit = registers_root.is_dir()
    if has_series == has_explicit:
        raise ValueError(
            f"{source}: register group must own exactly one of a series or a registers directory"
        )

    register_inventory: RegisterInventory | None = None
    series_spec: RegisterSeries | None = None
    registers: dict[str, Register] = {}
    if has_series:
        series = raw["series"]
        series_spec = RegisterSeries(series["prefix"], series["count"])
        for encoding in range(series_spec.count):
            register_id = f"{series_spec.prefix}{encoding}"
            register = Register(
                reference=Reference(owner, ("registers", group_id), register_id),
                source=source,
                root=root,
                owner=owner,
                group=group_id,
                id=register_id,
                width=width,
                encoding=encoding,
                summary=None,
                reset=reset,
                layout=layout,
            )
            references.registers.register(register.reference, register)
            registers[register_id] = register
    else:
        register_inventory = _load_inventory(
            owner, "register", registers_root, "registers"
        )
        for register_id in register_inventory.declared:
            register_root = registers_root / register_id
            if register_id in registers or not register_root.is_dir():
                continue
            register = _load_register(
                owner,
                group_id,
                register_root,
                width,
                reset,
                layout,
                schemas,
            )
            references.registers.register(register.reference, register)
            registers[register_id] = register

    return RegisterGroup(
        reference=reference,
        source=source,
        root=root,
        owner=owner,
        id=group_id,
        width=width,
        summary=raw.get("summary"),
        reset=reset,
        layout=layout,
        series=series_spec,
        register_inventory=register_inventory,
        registers=MappingProxyType(registers),
    )


def _load_register(
    owner: str,
    group_id: str,
    root: Path,
    width: RegisterWidth,
    group_reset: ResetSpec | None,
    group_layout: RegisterLayout | None,
    schemas: Mapping[str, Mapping[str, object]],
) -> Register:
    source = root / "register.yaml"
    raw = _load_validated(source, schemas["register"])
    register_id = raw["id"]
    if register_id != root.name:
        raise ValueError(
            f"{source}: register ID {register_id!r} does not match directory {root.name!r}"
        )
    local_layout = _load_layout(root / "layout.yaml", schemas["layout"])
    if group_layout is not None and local_layout is not None:
        raise ValueError(
            f"{root}: register-local layout cannot replace the group's fixed layout"
        )
    return Register(
        reference=Reference(owner, ("registers", group_id), register_id),
        source=source,
        root=root,
        owner=owner,
        group=group_id,
        id=register_id,
        width=width,
        encoding=raw.get("encoding"),
        summary=raw.get("summary"),
        reset=_decode_reset(raw["reset"]) if "reset" in raw else group_reset,
        layout=local_layout or group_layout,
    )


def _decode_width(raw: Any, source: Path) -> RegisterWidth:
    if isinstance(raw, int):
        return raw
    if not isinstance(raw, dict) or len(raw) != 1:
        raise ValueError(
            f"{source}: variable register width must contain exactly one expression"
        )
    expression, raw_values = next(iter(raw.items()))
    values = tuple(raw_values)
    if values != tuple(sorted(set(values))):
        raise ValueError(
            f"{source}: widths for {expression!r} must be unique and increasing"
        )
    return VariableRegisterWidth(expression, values)


def _load_layout(source: Path, schema: Mapping[str, object]) -> RegisterLayout | None:
    if not source.is_file():
        return None
    raw = _load_validated(source, schema)
    return RegisterLayout(
        source=source,
        bits=raw["bits"],
        fields=tuple(
            RegisterField(
                field["id"], field["lsb"], field["bits"], field.get("summary")
            )
            for field in raw["fields"]
        ),
    )


def _load_inventory(owner: str, kind: str, root: Path, key: str) -> RegisterInventory:
    source = root / f"{key}.yaml"
    declared = _load_name_list(source, key) if source.is_file() else ()
    actual = (
        tuple(
            sorted(
                path.name
                for path in root.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            )
        )
        if root.is_dir()
        else ()
    )
    return RegisterInventory(owner, kind, source, root, declared, actual)


def _decode_reset(raw: object) -> ResetSpec | None:
    if raw is None:
        return None
    if isinstance(raw, int) and not isinstance(raw, bool):
        return ResetSpec(value=raw)
    assert isinstance(raw, Mapping)
    if "from" in raw:
        return ResetSpec(source=Reference.parse(raw["from"]))
    return ResetSpec(cold=raw.get("cold"), warm=raw.get("warm"))


def _load_name_list(path: Path, key: str) -> tuple[str, ...]:
    raw = _load_mapping(path)
    values = raw.get(key)
    if not isinstance(values, list) or any(
        not isinstance(value, str) for value in values
    ):
        raise ValueError(f"{path}: expected a {key} list of strings")
    return tuple(values)


def _load_validated(path: Path, schema: Mapping[str, object]) -> dict[str, Any]:
    return SchemaValidatedYamlLoader().load(path, schema)


def _load_mapping(path: Path) -> dict[str, Any]:
    return YamlDocumentLoader().mapping(path)
