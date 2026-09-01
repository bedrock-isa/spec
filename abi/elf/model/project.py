"""Hierarchical typed project for the Bedrock ELF ABI."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, TypeVar, cast

from engine.entity import (
    Entity,
    EntityCatalog,
    EntityDisplayStyle,
    EntityKind,
)
from engine.dependency import EntityDependency
from engine.inventory import DirectoryInventory
from engine.reference import QualifiedReference, Reference, ReferenceIndex
from engine.yaml_document import SchemaValidatedYamlLoader

from .relocation_metasyntax import RelocationMetasyntax

if TYPE_CHECKING:
    from engine.project import InstructionBundle, IsaProject
    from engine.register import Register, RegisterGroup
    from engine.type_system import FieldType, PayloadType


_T = TypeVar("_T")


class RelocationResultKind(StrEnum):
    NONE = "none"
    INTEGER = "integer"
    BYTES = "bytes"
    PAIR = "pair"


class DebugRegisterRangeErrorReason(StrEnum):
    EMPTY = "empty"
    NONCONTIGUOUS = "noncontiguous"
    UNBOUNDED_NOT_LAST = "unbounded_not_last"
    UNBOUNDED_ASSIGNED = "unbounded_assigned"
    REVERSED = "reversed"
    ASSIGNMENT_WIDTH = "assignment_width"
    RESERVED_ASSIGNED = "reserved_assigned"
    MISSING_UNBOUNDED_TAIL = "missing_unbounded_tail"


class DebugRegisterRangeError(ValueError):
    """A DWARF register-number range violates the range topology."""

    def __init__(
        self, reason: DebugRegisterRangeErrorReason, message: str
    ) -> None:
        self.reason = reason
        super().__init__(message)


@dataclass(frozen=True, slots=True)
class RelocationResult:
    kind: RelocationResultKind
    width_bits: int | None
    signed: bool | None


@dataclass(frozen=True, slots=True)
class Relocation:
    reference: Reference["Relocation"]
    source: Path
    root: Path
    id: str
    value: int
    result: RelocationResult
    calculation: RelocationMetasyntax
    family: str | None
    field: QualifiedReference[FieldType] | QualifiedReference[PayloadType] | None
    relaxations: tuple[Reference["Relocation"], ...]


@dataclass(frozen=True, slots=True)
class LinkageStep:
    instruction: QualifiedReference[InstructionBundle]
    form: str | None
    relocation: QualifiedReference["Relocation"] | None


@dataclass(frozen=True, slots=True)
class StateContract:
    registers: tuple[QualifiedReference[Register], ...]
    disposition: str


@dataclass(frozen=True, slots=True)
class LinkageProtocol:
    reference: Reference["LinkageProtocol"]
    source: Path
    root: Path
    id: str
    steps: tuple[LinkageStep, ...]
    state: tuple[StateContract, ...]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class TlsModel:
    reference: Reference["TlsModel"]
    source: Path
    root: Path
    id: str
    base_register: QualifiedReference[Register] | None
    protocol: Reference["LinkageProtocol"] | None
    relocations: tuple[Reference[Relocation], ...]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class CodeModel:
    reference: Reference["CodeModel"]
    source: Path
    root: Path
    id: str
    default_relocations: tuple[Reference[Relocation], ...]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class DwarfRegisterRange:
    source: Path
    group: str | None
    register_group: QualifiedReference[RegisterGroup] | None
    first: int
    last: int | None
    status: str
    register_names: tuple[str, ...] | None
    condition: str | None


@dataclass(frozen=True, slots=True)
class DebugRegisterAssignment:
    source: Path
    group: str
    first: int
    last: int | None
    status: str
    registers: tuple[QualifiedReference[Register], ...]
    condition: str | None


@dataclass(frozen=True, slots=True)
class DebugRegisterRangeTopology:
    """A validated contiguous DWARF register-number assignment topology."""

    assignments: tuple[DebugRegisterAssignment, ...]

    @classmethod
    def create(
        cls, assignments: tuple[DebugRegisterAssignment, ...]
    ) -> "DebugRegisterRangeTopology":
        _validate_debug_register_ranges(assignments)
        return cls(assignments)


@dataclass(frozen=True, slots=True)
class EntryState:
    source: Path
    root: Path
    entry_point: QualifiedReference[Register]
    entry_point_source: str
    stack: QualifiedReference[Register]
    stack_alignment_bytes: int
    stack_permissions: tuple[str, ...]
    segment_contexts: Mapping[str, QualifiedReference[Register]]
    tls_base: QualifiedReference[Register] | None
    readiness: tuple[str, ...]
    cleared: tuple[QualifiedReference[Register], ...]
    payload_owner: str


@dataclass(frozen=True, slots=True)
class ElfRegisterGroup:
    reference: Reference["ElfRegisterGroup"]
    source: Path
    root: Path
    id: str
    register_group: QualifiedReference[RegisterGroup]
    dwarf: tuple[DwarfRegisterRange, ...]


@dataclass(frozen=True, slots=True)
class ElfAbiNamespace:
    owner: str
    root: Path
    relocation_inventory: DirectoryInventory
    linkage_protocol_inventory: DirectoryInventory
    tls_model_inventory: DirectoryInventory
    code_model_inventory: DirectoryInventory
    register_group_inventory: DirectoryInventory
    relocations: Mapping[str, Relocation]
    linkage_protocols: Mapping[str, LinkageProtocol]
    tls_models: Mapping[str, TlsModel]
    code_models: Mapping[str, CodeModel]
    register_groups: Mapping[str, ElfRegisterGroup]
    reserved_dwarf_ranges: tuple[DwarfRegisterRange, ...]
    process_entry: EntryState


@dataclass(frozen=True, slots=True)
class ElfAbiProject:
    root: Path
    namespaces: Mapping[str, ElfAbiNamespace]
    relocations: ReferenceIndex[Relocation]
    linkage_protocols: ReferenceIndex[LinkageProtocol]
    tls_models: ReferenceIndex[TlsModel]
    code_models: ReferenceIndex[CodeModel]
    register_groups: ReferenceIndex[ElfRegisterGroup]
    dwarf_ranges: tuple[DwarfRegisterRange, ...]
    process_entry: EntryState
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path, isa: "IsaProject") -> "ElfAbiProject":
        domain_root = Path(root).resolve()
        schemas = domain_root / "schemas"
        relocations = ReferenceIndex[Relocation]()
        protocols = ReferenceIndex[LinkageProtocol]()
        tls_models = ReferenceIndex[TlsModel]()
        code_models = ReferenceIndex[CodeModel]()
        register_groups = ReferenceIndex[ElfRegisterGroup]()
        base = _load_namespace(
            "base",
            domain_root,
            schemas,
            relocations,
            protocols,
            tls_models,
            code_models,
            register_groups,
            isa,
        )
        namespaces = MappingProxyType({"base": base})
        entities = _build_entities(
            relocations,
            protocols,
            tls_models,
            code_models,
            register_groups,
        )
        return cls(
            domain_root,
            namespaces,
            relocations,
            protocols,
            tls_models,
            code_models,
            register_groups,
            tuple(
                item
                for group in base.register_groups.values()
                for item in group.dwarf
            ) + base.reserved_dwarf_ranges,
            base.process_entry,
            entities,
        )

    def resolve(self, reference: Reference[_T]) -> _T:
        entity = self.entities.resolve(cast(Reference[Entity], reference))
        return cast(_T, entity.value)

    def entity_dependencies(self) -> tuple[EntityDependency, ...]:
        """Return the ELF ABI relationships intentionally exposed to tooling."""

        result: list[EntityDependency] = []

        def add(
            source: Reference[object],
            target: QualifiedReference[object],
            kind: str,
        ) -> None:
            result.append(EntityDependency(source, target, kind))

        def local(reference: Reference[object]) -> QualifiedReference[object]:
            return QualifiedReference("abi.elf", reference)

        for definition in self.relocations.values():
            source = cast(Reference[object], definition.reference)
            if definition.field is not None:
                add(
                    source,
                    cast(QualifiedReference[object], definition.field),
                    "relocation-field-type",
                )
            for target in definition.relaxations:
                add(
                    source,
                    local(cast(Reference[object], target)),
                    "relaxation",
                )
        for definition in self.linkage_protocols.values():
            source = cast(Reference[object], definition.reference)
            for step in definition.steps:
                add(
                    source,
                    cast(QualifiedReference[object], step.instruction),
                    "linkage-instruction",
                )
                if step.relocation is not None:
                    add(
                        source,
                        cast(QualifiedReference[object], step.relocation),
                        "linkage-relocation",
                    )
            for state in definition.state:
                for target in state.registers:
                    add(
                        source,
                        cast(QualifiedReference[object], target),
                        "linkage-register",
                    )
        for definition in self.tls_models.values():
            source = cast(Reference[object], definition.reference)
            if definition.base_register is not None:
                add(
                    source,
                    cast(QualifiedReference[object], definition.base_register),
                    "tls-base-register",
                )
            if definition.protocol is not None:
                add(
                    source,
                    local(cast(Reference[object], definition.protocol)),
                    "tls-protocol",
                )
            for target in definition.relocations:
                add(
                    source,
                    local(cast(Reference[object], target)),
                    "tls-relocation",
                )
        for definition in self.code_models.values():
            source = cast(Reference[object], definition.reference)
            for target in definition.default_relocations:
                add(
                    source,
                    local(cast(Reference[object], target)),
                    "code-model-relocation",
                )
        for definition in self.register_groups.values():
            source = cast(Reference[object], definition.reference)
            add(
                source,
                cast(QualifiedReference[object], definition.register_group),
                "dwarf-register-group",
            )
            for item in definition.dwarf:
                if item.register_group is not None:
                    add(
                        source,
                        cast(QualifiedReference[object], item.register_group),
                        "dwarf-register-group",
                    )
        return tuple(result)

    def validate(self, workspace) -> None:
        """Resolve structured ISA and ELF references."""

        for relocation_definition in self.relocations.values():
            if relocation_definition.field is not None:
                workspace.resolve(relocation_definition.field)
            for relaxation_reference in relocation_definition.relaxations:
                self.relocations.resolve(relaxation_reference)
        values: dict[int, Relocation] = {}
        for relocation_definition in self.relocations.values():
            previous_relocation = values.get(relocation_definition.value)
            if previous_relocation is not None:
                raise ValueError(
                    f"{relocation_definition.source}: relocation value "
                    f"{relocation_definition.value} is also assigned to "
                    f"{previous_relocation.id}"
                )
            values[relocation_definition.value] = relocation_definition
        for protocol_definition in self.linkage_protocols.values():
            for step in protocol_definition.steps:
                workspace.resolve(step.instruction)
                if step.relocation is not None:
                    target = workspace.resolve(step.relocation)
                    if not isinstance(target, Relocation):
                        raise ValueError(
                            f"{protocol_definition.source}: linkage step names "
                            "an entity outside the ELF relocation catalog"
                        )
            for state_contract in protocol_definition.state:
                for state_register in state_contract.registers:
                    workspace.resolve(state_register)
        for tls_model in self.tls_models.values():
            if tls_model.base_register is not None:
                workspace.resolve(tls_model.base_register)
            if tls_model.protocol is not None:
                self.linkage_protocols.resolve(tls_model.protocol)
            for tls_relocation in tls_model.relocations:
                self.relocations.resolve(tls_relocation)
        for code_model in self.code_models.values():
            for code_relocation in code_model.default_relocations:
                self.relocations.resolve(code_relocation)
        debug_assignments = sorted(
            self.resolved_debug_registers(workspace), key=lambda item: item.first
        )
        DebugRegisterRangeTopology.create(tuple(debug_assignments))
        for assignment in debug_assignments:
            for assigned_register in assignment.registers:
                workspace.resolve(assigned_register)
        entry_state = self.process_entry
        for entry_register in (
            entry_state.entry_point,
            entry_state.stack,
            *entry_state.segment_contexts.values(),
            *entry_state.cleared,
        ):
            workspace.resolve(entry_register)
        if entry_state.tls_base is not None:
            workspace.resolve(entry_state.tls_base)

    def resolved_debug_registers(self, workspace) -> tuple[DebugRegisterAssignment, ...]:
        result: list[DebugRegisterAssignment] = []
        for item in self.dwarf_ranges:
            if item.register_group is None:
                registers: tuple[QualifiedReference[Register], ...] = ()
                group = "RESERVED"
            else:
                definition = workspace.resolve(item.register_group)
                available = definition.registers
                names = tuple(available) if item.register_names is None else item.register_names
                missing = tuple(name for name in names if name not in available)
                if missing:
                    raise ValueError(
                        f"{item.source}: registers {missing} are not in "
                        f"register group {definition.id}"
                    )
                registers = tuple(
                    _register_reference(
                        item.register_group.domain, available[name]
                    )
                    for name in names
                )
                group = item.group or definition.id
            last = item.last
            if last is None and registers:
                last = item.first + len(registers) - 1
            result.append(
                DebugRegisterAssignment(
                    item.source, group, item.first, last, item.status,
                    registers, item.condition,
                )
            )
        return tuple(result)


def _load_namespace(
    owner: str,
    root: Path,
    schemas: Path,
    relocation_index: ReferenceIndex[Relocation],
    protocol_index: ReferenceIndex[LinkageProtocol],
    tls_index: ReferenceIndex[TlsModel],
    code_model_index: ReferenceIndex[CodeModel],
    register_group_index: ReferenceIndex[ElfRegisterGroup],
    isa: "IsaProject",
) -> ElfAbiNamespace:
    relocation_inventory = _inventory(owner, root, "relocation", "relocations")
    protocol_inventory = _inventory(
        owner, root, "linkage-protocol", "linkage_protocols"
    )
    tls_inventory = _inventory(owner, root, "tls-model", "tls_models")
    code_inventory = _inventory(owner, root, "code-model", "code_models")
    register_group_inventory = DirectoryInventory.load_strict(
        owner=owner,
        kind="elf-register-group",
        source=root / "registers/groups/groups.yaml",
        root=root / "registers/groups",
        key="groups",
    )

    relocations: dict[str, Relocation] = {}
    for entity_id in relocation_inventory.declared:
        entity_root = relocation_inventory.root / entity_id
        source = entity_root / "relocation.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "relocation.yaml"
        )
        _matching_id(source, entity_id, raw)
        relocation_reference: Reference[Relocation] = Reference(
            owner, ("relocations",), entity_id
        )
        result = raw["result"]
        field = (
            QualifiedReference.parse(raw["field"])
            if "field" in raw
            else None
        )
        relocation_definition = Relocation(
            relocation_reference,
            source,
            entity_root,
            entity_id,
            int(raw["value"]),
            RelocationResult(
                RelocationResultKind(result["kind"]),
                result.get("width_bits"),
                result.get("signed"),
            ),
            RelocationMetasyntax.parse(raw["calculation"]),
            raw.get("family"),
            field,
            tuple(Reference.parse(item) for item in raw.get("relaxations", ())),
        )
        relocation_index.register(relocation_reference, relocation_definition)
        relocations[entity_id] = relocation_definition

    protocols: dict[str, LinkageProtocol] = {}
    for entity_id in protocol_inventory.declared:
        entity_root = protocol_inventory.root / entity_id
        source = entity_root / "protocol.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "linkage-protocol.yaml"
        )
        _matching_id(source, entity_id, raw)
        protocol_reference: Reference[LinkageProtocol] = Reference(
            owner, ("linkage_protocols",), entity_id
        )
        protocol_definition = LinkageProtocol(
            protocol_reference,
            source,
            entity_root,
            entity_id,
            tuple(
                LinkageStep(
                    QualifiedReference.parse(step["instruction"]),
                    step.get("form"),
                    QualifiedReference.parse(step["relocation"])
                    if "relocation" in step
                    else None,
                )
                for step in raw.get("steps", ())
            ),
            tuple(
                StateContract(
                    tuple(
                        QualifiedReference.parse(register)
                        for register in item["registers"]
                    ),
                    item["disposition"],
                )
                for item in raw.get("state", ())
            ),
            MappingProxyType(raw),
        )
        protocol_index.register(protocol_reference, protocol_definition)
        protocols[entity_id] = protocol_definition

    tls_models: dict[str, TlsModel] = {}
    for entity_id in tls_inventory.declared:
        entity_root = tls_inventory.root / entity_id
        source = entity_root / "model.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "tls-model.yaml")
        _matching_id(source, entity_id, raw)
        tls_reference: Reference[TlsModel] = Reference(
            owner, ("tls_models",), entity_id
        )
        tls_definition = TlsModel(
            tls_reference,
            source,
            entity_root,
            entity_id,
            QualifiedReference.parse(raw["base_register"])
            if "base_register" in raw
            else None,
            Reference.parse(raw["protocol"]) if "protocol" in raw else None,
            tuple(Reference.parse(item) for item in raw.get("relocations", ())),
            MappingProxyType(raw),
        )
        tls_index.register(tls_reference, tls_definition)
        tls_models[entity_id] = tls_definition

    code_models: dict[str, CodeModel] = {}
    for entity_id in code_inventory.declared:
        entity_root = code_inventory.root / entity_id
        source = entity_root / "model.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "code-model.yaml")
        _matching_id(source, entity_id, raw)
        code_reference: Reference[CodeModel] = Reference(
            owner, ("code_models",), entity_id
        )
        code_definition = CodeModel(
            code_reference,
            source,
            entity_root,
            entity_id,
            tuple(
                Reference.parse(item) for item in raw.get("default_relocations", ())
            ),
            MappingProxyType(raw),
        )
        code_model_index.register(code_reference, code_definition)
        code_models[entity_id] = code_definition

    register_groups: dict[str, ElfRegisterGroup] = {}
    entry_point: tuple[QualifiedReference[Register], str] | None = None
    stack: tuple[QualifiedReference[Register], int, tuple[str, ...]] | None = None
    segments: dict[str, QualifiedReference[Register]] = {}
    tls_base: QualifiedReference[Register] | None = None
    cleared: list[QualifiedReference[Register]] = []
    for entity_id in register_group_inventory.declared:
        entity_root = register_group_inventory.root / entity_id
        source = entity_root / "group.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "register-group.yaml")
        _matching_id(source, entity_id, raw)
        register_group: QualifiedReference[RegisterGroup] = QualifiedReference.parse(
            raw["register_group"]
        )
        if register_group.domain != "isa":
            raise ValueError(f"{source}: register group must belong to isa")
        register_group_definition = isa.registers.references.groups.resolve(
            register_group.local
        )
        dwarf = tuple(
            DwarfRegisterRange(
                source,
                entity_id,
                register_group,
                int(item["first"]),
                None,
                str(item.get("status", "assigned")),
                None if item["registers"] == "all" else tuple(item["registers"]),
                item.get("condition"),
            )
            for item in raw.get("dwarf", ())
        )
        elf_group_reference: Reference[ElfRegisterGroup] = Reference(
            owner, ("registers",), entity_id
        )
        elf_group = ElfRegisterGroup(
            elf_group_reference,
            source,
            entity_root,
            entity_id,
            register_group,
            dwarf,
        )
        register_group_index.register(elf_group_reference, elf_group)
        register_groups[entity_id] = elf_group
        for name, declaration in raw.get("entry", {}).items():
            try:
                register_definition = register_group_definition.registers[name]
            except KeyError as error:
                raise ValueError(
                    f"{source}: unknown register {name!r} in group "
                    f"{register_group_definition.id!r}"
                ) from error
            register = _register_reference(
                register_group.domain, register_definition
            )
            role = declaration["role"]
            if role == "entry_point":
                entry_point = (register, str(declaration["source"]))
            elif role == "stack_pointer":
                stack = (
                    register,
                    int(declaration["alignment_bytes"]),
                    tuple(declaration["permissions"]),
                )
            elif role == "segment_context":
                segments[str(declaration["context"])] = register
            elif role == "tls_base":
                tls_base = register
            elif role == "cleared":
                cleared.append(register)

    dwarf_raw = SchemaValidatedYamlLoader().load(
        root / "registers/dwarf.yaml", schemas / "dwarf.yaml"
    )
    reserved = tuple(
        DwarfRegisterRange(
            root / "registers/dwarf.yaml", None, None, int(item["first"]),
            None if item["last"] == "unbounded" else int(item["last"]),
            "reserved", (), None,
        )
        for item in dwarf_raw["reserved_ranges"]
    )
    process_source = root / "process_entry.yaml"
    process_raw = SchemaValidatedYamlLoader().load(
        process_source, schemas / "process-entry.yaml"
    )
    if entry_point is None or stack is None or set(segments) != {"code", "data", "stack"}:
        raise ValueError(f"{process_source}: register-group entry declarations are incomplete")
    process_entry = EntryState(
        process_source,
        root,
        entry_point[0],
        entry_point[1],
        stack[0],
        stack[1],
        stack[2],
        MappingProxyType(segments),
        tls_base,
        tuple(process_raw["readiness"]),
        tuple(cleared),
        str(process_raw["payload_owner"]),
    )
    return ElfAbiNamespace(
        owner,
        root,
        relocation_inventory,
        protocol_inventory,
        tls_inventory,
        code_inventory,
        register_group_inventory,
        MappingProxyType(relocations),
        MappingProxyType(protocols),
        MappingProxyType(tls_models),
        MappingProxyType(code_models),
        MappingProxyType(register_groups),
        reserved,
        process_entry,
    )


def _validate_debug_register_ranges(
    assignments: list[DebugRegisterAssignment],
) -> None:
    if not assignments:
        raise DebugRegisterRangeError(
            DebugRegisterRangeErrorReason.EMPTY,
            "DWARF register numbering requires at least one assignment",
        )
    previous_last = -1
    for index, assignment in enumerate(assignments):
        if assignment.first != previous_last + 1:
            raise DebugRegisterRangeError(
                DebugRegisterRangeErrorReason.NONCONTIGUOUS,
                f"{assignment.source}: DWARF register numbering must be contiguous"
            )
        if assignment.last is None:
            if index != len(assignments) - 1:
                raise DebugRegisterRangeError(
                    DebugRegisterRangeErrorReason.UNBOUNDED_NOT_LAST,
                    f"{assignment.source}: unbounded DWARF register range must be last"
                )
            if assignment.registers:
                raise DebugRegisterRangeError(
                    DebugRegisterRangeErrorReason.UNBOUNDED_ASSIGNED,
                    f"{assignment.source}: unbounded DWARF register range cannot "
                    "assign registers"
                )
            return
        if assignment.last < assignment.first:
            raise DebugRegisterRangeError(
                DebugRegisterRangeErrorReason.REVERSED,
                f"{assignment.source}: DWARF register range ends before it begins"
            )
        width = assignment.last - assignment.first + 1
        if assignment.status in {"assigned", "extension"}:
            if len(assignment.registers) != width:
                raise DebugRegisterRangeError(
                    DebugRegisterRangeErrorReason.ASSIGNMENT_WIDTH,
                    f"{assignment.source}: DWARF register range has width {width} "
                    f"but assigns {len(assignment.registers)} registers"
                )
        elif assignment.registers:
            raise DebugRegisterRangeError(
                DebugRegisterRangeErrorReason.RESERVED_ASSIGNED,
                f"{assignment.source}: reserved DWARF register range cannot assign "
                "registers"
            )
        previous_last = assignment.last
    raise DebugRegisterRangeError(
        DebugRegisterRangeErrorReason.MISSING_UNBOUNDED_TAIL,
        f"{assignments[-1].source}: DWARF register numbering must end with an "
        "unbounded reserved range"
    )


def _inventory(
    owner: str, root: Path, kind: str, plural: str
) -> DirectoryInventory:
    return DirectoryInventory.load_strict(
        owner=owner,
        kind=kind,
        source=root / plural / f"{plural}.yaml",
        root=root / plural,
        key=plural,
    )


def _register_reference(domain: str, register: Register) -> QualifiedReference[Register]:
    return QualifiedReference(domain, register.reference)


def _matching_id(source: Path, expected: str, raw: Mapping[str, object]) -> None:
    if raw.get("id") != expected:
        raise ValueError(
            f"{source}: entity ID {raw.get('id')!r} does not match "
            f"directory {expected!r}"
        )


def _build_entities(
    relocations: ReferenceIndex[Relocation],
    protocols: ReferenceIndex[LinkageProtocol],
    tls_models: ReferenceIndex[TlsModel],
    code_models: ReferenceIndex[CodeModel],
    register_groups: ReferenceIndex[ElfRegisterGroup],
) -> EntityCatalog:
    index = ReferenceIndex[Entity]()
    catalogs: tuple[tuple[EntityKind, ReferenceIndex[object]], ...] = (
        (EntityKind.ELF_RELOCATION, cast(ReferenceIndex[object], relocations)),
        (EntityKind.ELF_LINKAGE_PROTOCOL, cast(ReferenceIndex[object], protocols)),
        (EntityKind.ELF_TLS_MODEL, cast(ReferenceIndex[object], tls_models)),
        (EntityKind.ELF_CODE_MODEL, cast(ReferenceIndex[object], code_models)),
        (EntityKind.ELF_DEBUG_REGISTER, cast(ReferenceIndex[object], register_groups)),
    )
    for kind, values in catalogs:
        for typed_reference, value in values.items():
            reference = cast(Reference[Entity], typed_reference)
            display = getattr(value, "id", None)
            if not isinstance(display, str):
                raise ValueError("ELF entity must provide a display identifier")
            index.register(
                reference,
                Entity(
                    reference,
                    kind,
                    display,
                    value.source,
                    value,
                    EntityDisplayStyle.CODE,
                ),
            )
    return EntityCatalog(index)
