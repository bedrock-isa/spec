"""Distributed architectural control-register definitions and lookup."""

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
from .register import (
    ConstantReset,
    LifecycleReset,
    RegisterField,
    RegisterLayout,
    ResetSpec,
    SourcedReset,
)
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class ControlRegisterInventory(DirectoryInventory):
    """One owner-local closed-world control-register inventory."""

    generated_state_registers: tuple[str, ...]
    reset: ResetSpec | None


@dataclass(frozen=True, slots=True)
class ControlRegister(Entity):
    """One register in the architectural RDCR/WRCR selector space."""

    reference: Reference["ControlRegister"]
    source: Path
    root: Path
    owner: str
    id: str
    selector: int
    summary: str
    reset: ResetSpec | None
    layout: RegisterLayout | None
    semantics: Path

    @property
    def width(self) -> int:
        return 64


@dataclass(frozen=True, slots=True)
class ControlRegisterNamespace(Entity):
    """Control registers owned by base or one declared extension."""

    reference: Reference["ControlRegisterNamespace"]
    owner: str
    root: Path
    inventory: ControlRegisterInventory
    registers: Mapping[str, ControlRegister]

    @property
    def id(self) -> str:
        return "control_registers"

    @property
    def source(self) -> Path:
        return self.inventory.source


@dataclass(frozen=True, slots=True)
class ControlRegisterReferenceIndexes:
    """Typed logical references for namespaces, registers, and fields."""

    namespaces: ReferenceIndex[ControlRegisterNamespace]
    registers: ReferenceIndex[ControlRegister]
    fields: ReferenceIndex[RegisterField]


@dataclass(frozen=True, slots=True)
class ControlRegisterCatalog:
    """The distributed global control-register selector registry."""

    namespaces: Mapping[str, ControlRegisterNamespace]
    references: ControlRegisterReferenceIndexes

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "ControlRegisterCatalog":
        root = Path(isa_root).resolve()
        extensions = extension_catalog or ExtensionSetCatalog.load(root)
        references = ControlRegisterReferenceIndexes(
            ReferenceIndex[ControlRegisterNamespace](),
            ReferenceIndex[ControlRegister](),
            ReferenceIndex[RegisterField](),
        )
        namespaces: dict[str, ControlRegisterNamespace] = {}
        selectors: dict[int, ControlRegister] = {}
        for owner, namespace_root in extensions.owner_roots():
            namespace = _load_namespace(owner, namespace_root, root, references)
            references.namespaces.register(namespace.reference, namespace)
            namespaces[owner] = namespace
            for register in namespace.registers.values():
                previous = selectors.get(register.selector)
                if previous is not None:
                    raise ValueError(
                        f"{register.source}: control-register selector "
                        f"0x{register.selector:04x} is also defined by "
                        f"{previous.source}"
                    )
                selectors[register.selector] = register
        return cls(MappingProxyType(namespaces), references)

    @property
    def base(self) -> ControlRegisterNamespace:
        return self.namespaces["base"]

    def namespace(self, owner: str) -> ControlRegisterNamespace:
        try:
            return self.namespaces[owner]
        except KeyError as error:
            raise ValueError(f"unknown control-register namespace {owner!r}") from error

    def selected(
        self, owners: set[str] | frozenset[str]
    ) -> tuple[ControlRegister, ...]:
        return tuple(
            register
            for owner, namespace in self.namespaces.items()
            if owner in owners
            for register in namespace.registers.values()
        )


def _load_namespace(
    owner: str,
    namespace_root: Path,
    isa_root: Path,
    references: ControlRegisterReferenceIndexes,
) -> ControlRegisterNamespace:
    definitions_root = namespace_root / "control_registers/definitions"
    inventory = _load_inventory(owner, definitions_root)
    registers: dict[str, ControlRegister] = {}
    for register_id in inventory.declared:
        register_root = definitions_root / register_id
        if register_id in registers or not register_root.is_dir():
            continue
        register = _load_register(
            owner,
            register_root,
            isa_root,
            inventory.reset,
        )
        references.registers.register(register.reference, register)
        if register.layout is not None:
            for field in register.layout.fields:
                references.fields.register(field.reference, field)
        registers[register_id] = register
    return ControlRegisterNamespace(
        Reference(owner, (), "control_registers"),
        owner,
        namespace_root,
        inventory,
        MappingProxyType(registers),
    )


def _load_inventory(owner: str, root: Path) -> ControlRegisterInventory:
    source = root / "control_registers.yaml"
    membership = DirectoryInventory.inspect(
        owner=owner,
        kind="control-register",
        source=source,
        root=root,
        key="control_registers",
        allow_missing=True,
    )
    if not source.is_file():
        return ControlRegisterInventory(
            membership.owner,
            membership.kind,
            membership.source,
            membership.root,
            membership.declared,
            membership.actual,
            (),
            None,
        )
    raw = _load_mapping(source)
    values = membership.declared
    generated_state_registers = raw.get("generated_state_registers", list(values))
    if not isinstance(generated_state_registers, list) or any(
        not isinstance(value, str) for value in generated_state_registers
    ):
        raise ValueError(
            f"{source}: expected a generated_state_registers list of strings"
        )
    unknown_state_registers = tuple(
        register_id
        for register_id in generated_state_registers
        if register_id not in values
    )
    if unknown_state_registers:
        raise ValueError(
            f"{source}: generated-state control registers are not declared members: "
            f"{unknown_state_registers}"
        )
    duplicate_state_registers = tuple(
        dict.fromkeys(
            register_id
            for register_id in generated_state_registers
            if generated_state_registers.count(register_id) > 1
        )
    )
    if duplicate_state_registers:
        raise ValueError(
            f"{source}: generated-state control registers are listed more than once: "
            f"{duplicate_state_registers}"
        )
    return ControlRegisterInventory(
        membership.owner,
        membership.kind,
        membership.source,
        membership.root,
        values,
        membership.actual,
        tuple(generated_state_registers),
        _decode_reset(raw.get("reset")),
    )


def _load_register(
    owner: str,
    root: Path,
    isa_root: Path,
    default_reset: ResetSpec | None,
) -> ControlRegister:
    source = root / "register.yaml"
    raw = SchemaValidatedYamlLoader().load(
        source, isa_root / "schemas/control-register.yaml"
    )
    register_id = raw["id"]
    if register_id != root.name:
        raise ValueError(
            f"{source}: control-register ID {register_id!r} does not match "
            f"directory {root.name!r}"
        )
    reference: Reference[ControlRegister] = Reference(
        owner, ("control_registers",), register_id
    )
    return ControlRegister(
        reference,
        source,
        root,
        owner,
        register_id,
        raw["selector"],
        raw["summary"],
        _decode_reset(raw["reset"]) if "reset" in raw else default_reset,
        _load_layout(
            root / "layout.yaml",
            isa_root / "schemas/register-layout.yaml",
            reference,
        ),
        root / "semantics.sail",
    )


def _load_layout(
    source: Path,
    schema: Path,
    owner: Reference[object],
) -> RegisterLayout | None:
    if not source.is_file():
        return None
    raw = SchemaValidatedYamlLoader().load(source, schema)
    if raw["bits"] != 64:
        raise ValueError(f"{source}: control-register layout must be 64 bits")
    return RegisterLayout(
        source,
        raw["bits"],
        tuple(
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


def _decode_reset(raw: object) -> ResetSpec | None:
    if raw is None:
        return None
    if isinstance(raw, int) and not isinstance(raw, bool):
        return ConstantReset(raw)
    assert isinstance(raw, Mapping)
    if "from" in raw:
        return SourcedReset(Reference.parse(raw["from"]))
    return LifecycleReset(raw["cold"], raw["warm"])


def _load_mapping(path: Path) -> dict[str, Any]:
    return YamlDocumentLoader().mapping(path)
