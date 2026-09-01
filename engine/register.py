"""Hierarchical architectural-register definitions and lookup."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from .entity import Entity
from .extension import ExtensionSetCatalog
from .inventory import DirectoryInventory
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


class RegisterGroupSourceConflictError(ValueError):
    """A register group declares more than one member source topology."""


class RegisterWidthDomainOrderError(ValueError):
    """A variable-width domain is not a strictly increasing set."""


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
class RegisterField(Entity):
    """One named field in an architectural register image."""

    reference: Reference["RegisterField"]
    source: Path
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
class Register(Entity):
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


class RegisterInventory(DirectoryInventory):
    """One closed-world group or explicit-register directory inventory."""


@dataclass(frozen=True, slots=True)
class RegisterSeries:
    """One homogeneous, consecutively encoded register family."""

    prefix: str
    count: int


@dataclass(frozen=True, slots=True)
class RegisterGroup(Entity):
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
    """Typed logical-reference indexes for groups, registers, and fields."""

    groups: ReferenceIndex[RegisterGroup]
    registers: ReferenceIndex[Register]
    fields: ReferenceIndex[RegisterField]


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
        owner_roots = extensions.owner_roots()
        manifests = tuple(
            namespace_root / "registers/groups/groups.yaml"
            for _, namespace_root in owner_roots
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
            ReferenceIndex[RegisterGroup](),
            ReferenceIndex[Register](),
            ReferenceIndex[RegisterField](),
        )
        namespaces: dict[str, RegisterNamespace] = {}
        for owner, namespace_root in owner_roots:
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
    layout = _load_layout(root / "layout.yaml", schemas["layout"], reference)
    if layout is not None:
        for field in layout.fields:
            references.fields.register(field.reference, field)
    registers_root = root / "registers"
    has_series = "series" in raw
    has_explicit = registers_root.is_dir()
    if has_series == has_explicit:
        raise RegisterGroupSourceConflictError(
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
            if register.layout is not None and register.layout is not layout:
                for field in register.layout.fields:
                    references.fields.register(field.reference, field)
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
    reference: Reference[Register] = Reference(
        owner, ("registers", group_id), register_id
    )
    local_layout = _load_layout(
        root / "layout.yaml", schemas["layout"], reference
    )
    if group_layout is not None and local_layout is not None:
        raise ValueError(
            f"{root}: register-local layout cannot replace the group's fixed layout"
        )
    return Register(
        reference=reference,
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
        raise RegisterWidthDomainOrderError(
            f"{source}: widths for {expression!r} must be unique and increasing"
        )
    return VariableRegisterWidth(expression, values)


def _load_layout(
    source: Path,
    schema: Mapping[str, object],
    owner: Reference[object],
) -> RegisterLayout | None:
    if not source.is_file():
        return None
    raw = _load_validated(source, schema)
    return RegisterLayout(
        source=source,
        bits=raw["bits"],
        fields=tuple(
            RegisterField(
                reference=Reference(
                    owner.owner,
                    (*owner.path, owner.element),
                    field["id"],
                ),
                source=source,
                id=field["id"],
                lsb=field["lsb"],
                bits=field["bits"],
                summary=field.get("summary"),
            )
            for field in raw["fields"]
        ),
    )


def _load_inventory(owner: str, kind: str, root: Path, key: str) -> RegisterInventory:
    return RegisterInventory.inspect(
        owner=owner,
        kind=kind,
        source=root / f"{key}.yaml",
        root=root,
        key=key,
        allow_missing=True,
    )


def _decode_reset(raw: object) -> ResetSpec | None:
    if raw is None:
        return None
    if isinstance(raw, int) and not isinstance(raw, bool):
        return ResetSpec(value=raw)
    assert isinstance(raw, Mapping)
    if "from" in raw:
        return ResetSpec(source=Reference.parse(raw["from"]))
    return ResetSpec(cold=raw.get("cold"), warm=raw.get("warm"))


def _load_validated(path: Path, schema: Mapping[str, object]) -> dict[str, Any]:
    return SchemaValidatedYamlLoader().load(path, schema)


def _load_mapping(path: Path) -> dict[str, Any]:
    return YamlDocumentLoader().mapping(path)
