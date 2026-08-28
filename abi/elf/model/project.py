"""Hierarchical typed project for the Bedrock ELF ABI."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType

from engine.entity import (
    Entity,
    EntityCatalog,
    EntityDisplayStyle,
    EntityKind,
    entity_label,
)
from engine.document_topic import DomainDocumentCatalog, DomainDocumentTopic
from engine.inventory import DirectoryInventory
from engine.reference import QualifiedReference, Reference, ReferenceIndex
from engine.yaml_document import SchemaValidatedYamlLoader

from .relocation_metasyntax import RelocationMetasyntax


class RelocationResultKind(StrEnum):
    NONE = "none"
    INTEGER = "integer"
    BYTES = "bytes"
    PAIR = "pair"


@dataclass(frozen=True, slots=True)
class RelocationResult:
    kind: RelocationResultKind
    width_bits: int | None
    signed: bool | None


@dataclass(frozen=True, slots=True)
class Relocation:
    reference: Reference
    source: Path
    root: Path
    id: str
    value: int
    result: RelocationResult
    calculation: RelocationMetasyntax
    family: str | None
    field: QualifiedReference | None
    relaxations: tuple[Reference, ...]


@dataclass(frozen=True, slots=True)
class LinkageStep:
    instruction: QualifiedReference
    form: str | None
    relocation: QualifiedReference | None


@dataclass(frozen=True, slots=True)
class StateContract:
    registers: tuple[QualifiedReference, ...]
    disposition: str


@dataclass(frozen=True, slots=True)
class LinkageProtocol:
    reference: Reference
    source: Path
    root: Path
    id: str
    steps: tuple[LinkageStep, ...]
    state: tuple[StateContract, ...]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class TlsModel:
    reference: Reference
    source: Path
    root: Path
    id: str
    base_register: QualifiedReference | None
    protocol: Reference | None
    relocations: tuple[Reference, ...]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class CodeModel:
    reference: Reference
    source: Path
    root: Path
    id: str
    default_relocations: tuple[Reference, ...]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class DwarfRegisterRange:
    source: Path
    group: str | None
    register_group: QualifiedReference | None
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
    registers: tuple[QualifiedReference, ...]
    condition: str | None


@dataclass(frozen=True, slots=True)
class EntryState:
    source: Path
    root: Path
    entry_point: QualifiedReference
    entry_point_source: str
    stack: QualifiedReference
    stack_alignment_bytes: int
    stack_permissions: tuple[str, ...]
    segment_contexts: Mapping[str, QualifiedReference]
    tls_base: QualifiedReference | None
    readiness: tuple[str, ...]
    cleared: tuple[QualifiedReference, ...]
    payload_owner: str


@dataclass(frozen=True, slots=True)
class ElfRegisterGroup:
    reference: Reference
    source: Path
    root: Path
    id: str
    register_group: QualifiedReference
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
    document_catalog: DomainDocumentCatalog
    document_topics: ReferenceIndex[DomainDocumentTopic]
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path) -> "ElfAbiProject":
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
        )
        namespaces = MappingProxyType({"base": base})
        document_catalog = DomainDocumentCatalog.load(
            owner="base",
            documents_root=domain_root / "documents",
            schema=schemas / "document-topic.yaml",
        )
        entities = _build_entities(
            relocations,
            protocols,
            tls_models,
            code_models,
            register_groups,
            document_catalog.topics,
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
            document_catalog,
            document_catalog.topics,
            entities,
        )

    def resolve(self, reference: str | Reference) -> object:
        normalized = Reference.parse(reference)
        for index in (
            self.relocations,
            self.linkage_protocols,
            self.tls_models,
            self.code_models,
            self.register_groups,
            self.document_topics,
        ):
            if normalized in index:
                return index.resolve(normalized)
        return self.entities.resolve(normalized)

    def validate(self, workspace) -> None:
        """Resolve structured ISA and ELF references."""

        self.document_catalog.validate(workspace)
        for relocation in self.relocations.values():
            if relocation.field is not None:
                workspace.resolve(relocation.field)
            for relaxation in relocation.relaxations:
                self.relocations.resolve(relaxation)
        values: dict[int, Relocation] = {}
        for relocation in self.relocations.values():
            previous = values.get(relocation.value)
            if previous is not None:
                raise ValueError(
                    f"{relocation.source}: relocation value {relocation.value} "
                    f"is also assigned to {previous.reference}"
                )
            values[relocation.value] = relocation
        for protocol in self.linkage_protocols.values():
            for step in protocol.steps:
                workspace.resolve(step.instruction)
                if step.relocation is not None:
                    target = workspace.resolve(step.relocation)
                    if not isinstance(target, Relocation):
                        raise ValueError(
                            f"{protocol.source}: {step.relocation} names "
                            "an entity outside the ELF relocation catalog"
                        )
            for state in protocol.state:
                for register in state.registers:
                    workspace.resolve(register)
        for model in self.tls_models.values():
            if model.base_register is not None:
                workspace.resolve(model.base_register)
            if model.protocol is not None:
                self.linkage_protocols.resolve(model.protocol)
            for relocation in model.relocations:
                self.relocations.resolve(relocation)
        for model in self.code_models.values():
            for relocation in model.default_relocations:
                self.relocations.resolve(relocation)
        debug_assignments = sorted(
            self.resolved_debug_registers(workspace), key=lambda item: item.first
        )
        _validate_debug_register_ranges(debug_assignments)
        for assignment in debug_assignments:
            for register in assignment.registers:
                workspace.resolve(register)
        state = self.process_entry
        for register in (
            state.entry_point,
            state.stack,
            *state.segment_contexts.values(),
            *state.cleared,
        ):
            workspace.resolve(register)
        if state.tls_base is not None:
            workspace.resolve(state.tls_base)

    def resolved_debug_registers(self, workspace) -> tuple[DebugRegisterAssignment, ...]:
        result: list[DebugRegisterAssignment] = []
        for item in self.dwarf_ranges:
            if item.register_group is None:
                registers: tuple[QualifiedReference, ...] = ()
                group = "RESERVED"
            else:
                definition = workspace.resolve(item.register_group)
                available = definition.registers
                names = tuple(available) if item.register_names is None else item.register_names
                missing = tuple(name for name in names if name not in available)
                if missing:
                    raise ValueError(
                        f"{item.source}: registers {missing} are not in {item.register_group}"
                    )
                registers = tuple(_register_reference(item.register_group, name) for name in names)
                group = item.group or item.register_group.local.element
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
) -> ElfAbiNamespace:
    relocation_inventory = _inventory(owner, root, "relocation", "relocations")
    protocol_inventory = _inventory(
        owner, root, "linkage-protocol", "linkage_protocols"
    )
    tls_inventory = _inventory(owner, root, "tls-model", "tls_models")
    code_inventory = _inventory(owner, root, "code-model", "code_models")
    register_group_inventory = DirectoryInventory.load(
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
        reference = Reference(owner, ("relocations",), entity_id)
        result = raw["result"]
        field = (
            QualifiedReference.parse(str(raw["field"]))
            if "field" in raw
            else None
        )
        entity = Relocation(
            reference,
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
        relocation_index.register(reference, entity)
        relocations[entity_id] = entity

    protocols: dict[str, LinkageProtocol] = {}
    for entity_id in protocol_inventory.declared:
        entity_root = protocol_inventory.root / entity_id
        source = entity_root / "protocol.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "linkage-protocol.yaml"
        )
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("linkage_protocols",), entity_id)
        entity = LinkageProtocol(
            reference,
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
        protocol_index.register(reference, entity)
        protocols[entity_id] = entity

    tls_models: dict[str, TlsModel] = {}
    for entity_id in tls_inventory.declared:
        entity_root = tls_inventory.root / entity_id
        source = entity_root / "model.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "tls-model.yaml")
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("tls_models",), entity_id)
        entity = TlsModel(
            reference,
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
        tls_index.register(reference, entity)
        tls_models[entity_id] = entity

    code_models: dict[str, CodeModel] = {}
    for entity_id in code_inventory.declared:
        entity_root = code_inventory.root / entity_id
        source = entity_root / "model.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "code-model.yaml")
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("code_models",), entity_id)
        entity = CodeModel(
            reference,
            source,
            entity_root,
            entity_id,
            tuple(
                Reference.parse(item) for item in raw.get("default_relocations", ())
            ),
            MappingProxyType(raw),
        )
        code_model_index.register(reference, entity)
        code_models[entity_id] = entity

    register_groups: dict[str, ElfRegisterGroup] = {}
    entry_point: tuple[QualifiedReference, str] | None = None
    stack: tuple[QualifiedReference, int, tuple[str, ...]] | None = None
    segments: dict[str, QualifiedReference] = {}
    tls_base: QualifiedReference | None = None
    cleared: list[QualifiedReference] = []
    for entity_id in register_group_inventory.declared:
        entity_root = register_group_inventory.root / entity_id
        source = entity_root / "group.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "register-group.yaml")
        _matching_id(source, entity_id, raw)
        register_group = QualifiedReference.parse(raw["register_group"])
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
        reference = Reference(owner, ("registers",), entity_id)
        group = ElfRegisterGroup(
            reference, source, entity_root, entity_id, register_group, dwarf
        )
        register_group_index.register(reference, group)
        register_groups[entity_id] = group
        for name, declaration in raw.get("entry", {}).items():
            register = _register_reference(register_group, name)
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
        raise ValueError("DWARF register numbering requires at least one assignment")
    previous_last = -1
    for index, assignment in enumerate(assignments):
        if assignment.first != previous_last + 1:
            raise ValueError(
                f"{assignment.source}: DWARF register numbering must be contiguous"
            )
        if assignment.last is None:
            if index != len(assignments) - 1:
                raise ValueError(
                    f"{assignment.source}: unbounded DWARF register range must be last"
                )
            if assignment.registers:
                raise ValueError(
                    f"{assignment.source}: unbounded DWARF register range cannot "
                    "assign registers"
                )
            return
        if assignment.last < assignment.first:
            raise ValueError(
                f"{assignment.source}: DWARF register range ends before it begins"
            )
        width = assignment.last - assignment.first + 1
        if assignment.status in {"assigned", "extension"}:
            if len(assignment.registers) != width:
                raise ValueError(
                    f"{assignment.source}: DWARF register range has width {width} "
                    f"but assigns {len(assignment.registers)} registers"
                )
        elif assignment.registers:
            raise ValueError(
                f"{assignment.source}: reserved DWARF register range cannot assign "
                "registers"
            )
        previous_last = assignment.last
    raise ValueError(
        f"{assignments[-1].source}: DWARF register numbering must end with an "
        "unbounded reserved range"
    )


def _inventory(
    owner: str, root: Path, kind: str, plural: str
) -> DirectoryInventory:
    return DirectoryInventory.load(
        owner=owner,
        kind=kind,
        source=root / plural / f"{plural}.yaml",
        root=root / plural,
        key=plural,
    )


def _register_reference(
    group: QualifiedReference, name: str
) -> QualifiedReference:
    return QualifiedReference(
        group.domain,
        Reference(
            group.local.owner,
            (*group.local.path, group.local.element),
            name,
        ),
    )


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
    document_topics: ReferenceIndex[DomainDocumentTopic],
) -> EntityCatalog:
    index = ReferenceIndex[Entity]()
    for kind, values in (
        (EntityKind.ELF_RELOCATION, relocations),
        (EntityKind.ELF_LINKAGE_PROTOCOL, protocols),
        (EntityKind.ELF_TLS_MODEL, tls_models),
        (EntityKind.ELF_CODE_MODEL, code_models),
        (EntityKind.ELF_DEBUG_REGISTER, register_groups),
        (EntityKind.TOPIC, document_topics),
    ):
        for reference, value in values.items():
            index.register(
                reference,
                Entity(
                    reference,
                    kind,
                    value.title if isinstance(value, DomainDocumentTopic) else value.id,
                    value,
                    entity_label(reference),
                    EntityDisplayStyle.TEXT
                    if isinstance(value, DomainDocumentTopic)
                    else EntityDisplayStyle.CODE,
                ),
            )
    return EntityCatalog(index)
