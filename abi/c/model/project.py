"""Hierarchical typed project for the Bedrock C ABI."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
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


@dataclass(frozen=True, slots=True)
class CType:
    reference: Reference
    source: Path
    root: Path
    id: str
    spelling: str
    call_kind: str
    size_bits: int | str
    alignment_bytes: int
    representation: str | None


@dataclass(frozen=True, slots=True)
class RegisterClass:
    reference: Reference
    source: Path
    root: Path
    id: str
    arguments: tuple[QualifiedReference, ...]
    results: tuple[QualifiedReference, ...]
    allocation: str
    tuple_alignment: int
    exhaustion: str


@dataclass(frozen=True, slots=True)
class LocationPolicy:
    mode: str
    register_class: Reference | None
    units: int | None
    alignment_units: int
    direct_maximum_bytes: int | None
    fallback: str | None


@dataclass(frozen=True, slots=True)
class ValueClass:
    reference: Reference
    source: Path
    root: Path
    id: str
    kinds: tuple[str, ...]
    argument: LocationPolicy
    result: LocationPolicy


@dataclass(frozen=True, slots=True)
class Promotion:
    reference: Reference
    source: Path
    root: Path
    id: str
    source_kinds: tuple[str, ...]
    target_kind: str


@dataclass(frozen=True, slots=True)
class StackConvention:
    pointer: QualifiedReference
    growth: str
    entry_alignment_bytes: int
    first_argument_offset_bytes: int
    argument_slot_bytes: int
    sret_register: QualifiedReference
    red_zone_bytes: int


@dataclass(frozen=True, slots=True)
class PreservationSet:
    registers: tuple[QualifiedReference, ...]
    disposition: str


@dataclass(frozen=True, slots=True)
class CallingConvention:
    source: Path
    root: Path
    stack: StackConvention
    register_class_inventory: DirectoryInventory
    value_class_inventory: DirectoryInventory
    promotion_inventory: DirectoryInventory
    register_classes: tuple[Reference, ...]
    value_classes: tuple[Reference, ...]
    promotions: tuple[Reference, ...]
    preservation: tuple[PreservationSet, ...]


@dataclass(frozen=True, slots=True)
class RuntimeHelper:
    reference: Reference
    source: Path
    root: Path
    id: str
    symbol: str
    result: Reference
    parameters: tuple[Reference, ...]


@dataclass(frozen=True, slots=True)
class MemoryOrderMapping:
    reference: Reference
    source: Path
    root: Path
    id: str
    instruction_order: str
    load: tuple[str | QualifiedReference, ...] | None
    store: tuple[str | QualifiedReference, ...] | None
    thread_fence: tuple[str | QualifiedReference, ...]


@dataclass(frozen=True, slots=True)
class AtomicLowering:
    reference: Reference
    source: Path
    root: Path
    id: str
    c_operations: tuple[str, ...]
    strategy: str
    instructions: tuple[QualifiedReference, ...]


@dataclass(frozen=True, slots=True)
class ResolvedRegisterClass:
    definition: RegisterClass
    arguments: tuple[object, ...]
    results: tuple[object, ...]


@dataclass(frozen=True, slots=True)
class ResolvedValueClass:
    definition: ValueClass
    argument_register_class: ResolvedRegisterClass | None
    result_register_class: ResolvedRegisterClass | None


@dataclass(frozen=True, slots=True)
class ResolvedCallingConvention:
    definition: CallingConvention
    stack_pointer: object
    sret_register: object
    register_classes: Mapping[Reference, ResolvedRegisterClass]
    value_classes: Mapping[str, ResolvedValueClass]
    promotions: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class CAbiNamespace:
    owner: str
    root: Path
    type_inventory: DirectoryInventory
    register_class_inventory: DirectoryInventory
    value_class_inventory: DirectoryInventory
    promotion_inventory: DirectoryInventory
    runtime_helper_inventory: DirectoryInventory
    memory_order_inventory: DirectoryInventory
    atomic_lowering_inventory: DirectoryInventory
    types: Mapping[str, CType]
    calling_convention: CallingConvention
    runtime_helpers: Mapping[str, RuntimeHelper]
    memory_orders: Mapping[str, MemoryOrderMapping]
    atomic_lowerings: Mapping[str, AtomicLowering]


@dataclass(frozen=True, slots=True)
class CAbiProject:
    root: Path
    namespaces: Mapping[str, CAbiNamespace]
    types: ReferenceIndex[CType]
    calling_convention: CallingConvention
    register_classes: ReferenceIndex[RegisterClass]
    value_classes: ReferenceIndex[ValueClass]
    promotions: ReferenceIndex[Promotion]
    runtime_helpers: ReferenceIndex[RuntimeHelper]
    memory_orders: ReferenceIndex[MemoryOrderMapping]
    atomic_lowerings: ReferenceIndex[AtomicLowering]
    document_catalog: DomainDocumentCatalog
    document_topics: ReferenceIndex[DomainDocumentTopic]
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path) -> "CAbiProject":
        domain_root = Path(root).resolve()
        indexes = _Indexes.create()
        base = _load_namespace("base", domain_root, indexes)
        document_catalog = DomainDocumentCatalog.load(
            owner="base",
            documents_root=domain_root / "documents",
            schema=domain_root / "schemas/document-topic.yaml",
        )
        entities = _build_entities(indexes, document_catalog.topics)
        return cls(
            domain_root,
            MappingProxyType({"base": base}),
            indexes.types,
            base.calling_convention,
            indexes.register_classes,
            indexes.value_classes,
            indexes.promotions,
            indexes.runtime_helpers,
            indexes.memory_orders,
            indexes.atomic_lowerings,
            document_catalog,
            document_catalog.topics,
            entities,
        )

    def resolve(self, reference: str | Reference) -> object:
        normalized = Reference.parse(reference)
        for index in (
            self.types,
            self.register_classes,
            self.value_classes,
            self.promotions,
            self.runtime_helpers,
            self.memory_orders,
            self.atomic_lowerings,
            self.document_topics,
        ):
            if normalized in index:
                return index.resolve(normalized)
        return self.entities.resolve(normalized)

    def validate(self, workspace) -> None:
        """Resolve every local and cross-domain relationship."""

        self.document_catalog.validate(workspace)
        kind_owners: dict[str, ValueClass] = {}
        for c_type in self.types.values():
            if c_type.call_kind not in {
                kind
                for value_class in self.value_classes.values()
                for kind in value_class.kinds
            }:
                raise ValueError(
                    f"{c_type.source}: call kind {c_type.call_kind!r} has no value class"
                )
        for register_class in self.register_classes.values():
            for register in (*register_class.arguments, *register_class.results):
                workspace.resolve(register)
        for value_class in self.value_classes.values():
            for kind in value_class.kinds:
                previous = kind_owners.get(kind)
                if previous is not None:
                    raise ValueError(
                        f"{value_class.source}: call kind {kind!r} is also "
                        f"classified by {previous.reference}"
                    )
                kind_owners[kind] = value_class
            for policy in (value_class.argument, value_class.result):
                if policy.register_class is not None:
                    self.register_classes.resolve(policy.register_class)
        convention = self.calling_convention
        workspace.resolve(convention.stack.pointer)
        workspace.resolve(convention.stack.sret_register)
        allocated_registers: dict[QualifiedReference, Reference] = {}
        for reference in convention.register_classes:
            register_class = self.register_classes.resolve(reference)
            for register in register_class.arguments:
                previous = allocated_registers.get(register)
                if previous is not None:
                    raise ValueError(
                        f"{register_class.source}: argument register {register} "
                        f"is also allocated by {previous}"
                    )
                allocated_registers[register] = reference
        for reference in convention.value_classes:
            self.value_classes.resolve(reference)
        promotion_sources: dict[str, Reference] = {}
        for reference in convention.promotions:
            promotion = self.promotions.resolve(reference)
            if promotion.target_kind not in kind_owners:
                raise ValueError(
                    f"{promotion.source}: target kind {promotion.target_kind!r} "
                    "has no value class"
                )
            for kind in promotion.source_kinds:
                if kind not in kind_owners:
                    raise ValueError(
                        f"{promotion.source}: source kind {kind!r} has no value class"
                    )
                previous = promotion_sources.get(kind)
                if previous is not None:
                    raise ValueError(
                        f"{promotion.source}: source kind {kind!r} is also "
                        f"promoted by {previous}"
                    )
                promotion_sources[kind] = reference
        preserved: dict[QualifiedReference, str] = {}
        for preservation in convention.preservation:
            for register in preservation.registers:
                workspace.resolve(register)
                previous = preserved.get(register)
                if previous is not None:
                    raise ValueError(
                        f"{convention.source}: register {register} has both "
                        f"{previous!r} and {preservation.disposition!r} dispositions"
                    )
                preserved[register] = preservation.disposition
        for helper in self.runtime_helpers.values():
            self.types.resolve(helper.result)
            for parameter in helper.parameters:
                self.types.resolve(parameter)
        for mapping in self.memory_orders.values():
            for sequence in (mapping.load, mapping.store, mapping.thread_fence):
                for operation in sequence or ():
                    if isinstance(operation, QualifiedReference):
                        workspace.resolve(operation)
        operation_owners: dict[str, AtomicLowering] = {}
        for lowering in self.atomic_lowerings.values():
            for operation in lowering.c_operations:
                previous = operation_owners.get(operation)
                if previous is not None:
                    raise ValueError(
                        f"{lowering.source}: C operation {operation!r} is also "
                        f"lowered by {previous.reference}"
                    )
                operation_owners[operation] = lowering
            for instruction in lowering.instructions:
                workspace.resolve(instruction)

    def resolved_calling_convention(self, workspace) -> ResolvedCallingConvention:
        convention = self.calling_convention
        resolved_registers: dict[Reference, ResolvedRegisterClass] = {}
        for item in convention.register_classes:
            definition = self.register_classes.resolve(item)
            resolved_registers[item] = ResolvedRegisterClass(
                definition,
                tuple(workspace.resolve(register) for register in definition.arguments),
                tuple(workspace.resolve(register) for register in definition.results),
            )
        resolved_values: dict[str, ResolvedValueClass] = {}
        for item in convention.value_classes:
            definition = self.value_classes.resolve(item)
            argument_class = (
                resolved_registers[definition.argument.register_class]
                if definition.argument.register_class is not None
                else None
            )
            result_class = (
                resolved_registers[definition.result.register_class]
                if definition.result.register_class is not None
                else None
            )
            resolved = ResolvedValueClass(definition, argument_class, result_class)
            for kind in definition.kinds:
                resolved_values[kind] = resolved
        promotions: dict[str, str] = {}
        for item in convention.promotions:
            promotion = self.promotions.resolve(item)
            for kind in promotion.source_kinds:
                promotions[kind] = promotion.target_kind
        return ResolvedCallingConvention(
            convention,
            workspace.resolve(convention.stack.pointer),
            workspace.resolve(convention.stack.sret_register),
            MappingProxyType(resolved_registers),
            MappingProxyType(resolved_values),
            MappingProxyType(promotions),
        )


@dataclass(frozen=True, slots=True)
class _Indexes:
    types: ReferenceIndex[CType]
    register_classes: ReferenceIndex[RegisterClass]
    value_classes: ReferenceIndex[ValueClass]
    promotions: ReferenceIndex[Promotion]
    runtime_helpers: ReferenceIndex[RuntimeHelper]
    memory_orders: ReferenceIndex[MemoryOrderMapping]
    atomic_lowerings: ReferenceIndex[AtomicLowering]

    @classmethod
    def create(cls) -> "_Indexes":
        return cls(
            ReferenceIndex[CType](),
            ReferenceIndex[RegisterClass](),
            ReferenceIndex[ValueClass](),
            ReferenceIndex[Promotion](),
            ReferenceIndex[RuntimeHelper](),
            ReferenceIndex[MemoryOrderMapping](),
            ReferenceIndex[AtomicLowering](),
        )


def _load_namespace(owner: str, root: Path, indexes: _Indexes) -> CAbiNamespace:
    schemas = root / "schemas"
    type_inventory = _inventory(owner, root, "type", "types")
    register_inventory = _inventory(
        owner, root, "register-class", "register_classes"
    )
    value_inventory = _inventory(owner, root, "value-class", "value_classes")
    promotion_inventory = _inventory(owner, root, "promotion", "promotions")
    helper_inventory = _inventory(owner, root, "runtime-helper", "runtime_helpers")
    order_inventory = _inventory(owner, root, "memory-order", "memory_orders")
    atomic_inventory = _inventory(
        owner, root, "atomic-lowering", "atomic_lowerings"
    )

    types: dict[str, CType] = {}
    for entity_id in type_inventory.declared:
        entity_root = type_inventory.root / entity_id
        source = entity_root / "type.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schemas / "type.yaml")
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("types",), entity_id)
        entity = CType(
            reference,
            source,
            entity_root,
            entity_id,
            raw["spelling"],
            raw["call_kind"],
            raw["size_bits"],
            raw["alignment_bytes"],
            raw.get("representation"),
        )
        indexes.types.register(reference, entity)
        types[entity_id] = entity

    for child_id in register_inventory.declared:
        child_root = register_inventory.root / child_id
        child_source = child_root / "register_class.yaml"
        child = SchemaValidatedYamlLoader().load(
            child_source, schemas / "register-class.yaml"
        )
        _matching_id(child_source, child_id, child)
        reference = Reference(owner, ("register_classes",), child_id)
        indexes.register_classes.register(
            reference,
            RegisterClass(
                reference, child_source, child_root, child_id,
                tuple(QualifiedReference.parse(item) for item in child["arguments"]),
                tuple(QualifiedReference.parse(item) for item in child["results"]),
                child["allocation"], child.get("tuple_alignment", 1),
                child["exhaustion"],
            ),
        )
    for child_id in value_inventory.declared:
        child_root = value_inventory.root / child_id
        child_source = child_root / "value_class.yaml"
        child = SchemaValidatedYamlLoader().load(
            child_source, schemas / "value-class.yaml"
        )
        _matching_id(child_source, child_id, child)
        reference = Reference(owner, ("value_classes",), child_id)
        indexes.value_classes.register(
            reference,
            ValueClass(
                reference, child_source, child_root, child_id,
                tuple(child["kinds"]), _location_policy(child["argument"]),
                _location_policy(child["result"]),
            ),
        )
    for child_id in promotion_inventory.declared:
        child_root = promotion_inventory.root / child_id
        child_source = child_root / "promotion.yaml"
        child = SchemaValidatedYamlLoader().load(
            child_source, schemas / "promotion.yaml"
        )
        _matching_id(child_source, child_id, child)
        reference = Reference(owner, ("promotions",), child_id)
        indexes.promotions.register(
            reference,
            Promotion(
                reference, child_source, child_root, child_id,
                tuple(child["source_kinds"]), child["target_kind"],
            ),
        )

    source = root / "calling_convention.yaml"
    raw = SchemaValidatedYamlLoader().load(
        source, schemas / "calling-convention.yaml"
    )
    stack = raw["stack"]
    convention = CallingConvention(
            source,
            root,
            StackConvention(
                QualifiedReference.parse(stack["pointer"]),
                stack["growth"],
                stack["entry_alignment_bytes"],
                stack["first_argument_offset_bytes"],
                stack["argument_slot_bytes"],
                QualifiedReference.parse(stack["sret_register"]),
                stack.get("red_zone_bytes", 0),
            ),
            register_inventory,
            value_inventory,
            promotion_inventory,
            tuple(
                Reference(owner, ("register_classes",), item)
                for item in register_inventory.declared
            ),
            tuple(
                Reference(owner, ("value_classes",), item)
                for item in value_inventory.declared
            ),
            tuple(
                Reference(owner, ("promotions",), item)
                for item in promotion_inventory.declared
            ),
            tuple(
                PreservationSet(
                    tuple(
                        QualifiedReference.parse(register)
                        for register in item["registers"]
                    ),
                    item["disposition"],
                )
                for item in raw["preservation"]
            ),
        )

    helpers: dict[str, RuntimeHelper] = {}
    for entity_id in helper_inventory.declared:
        entity_root = helper_inventory.root / entity_id
        source = entity_root / "runtime_helper.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "runtime-helper.yaml"
        )
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("runtime_helpers",), entity_id)
        entity = RuntimeHelper(
            reference,
            source,
            entity_root,
            entity_id,
            raw["symbol"],
            Reference.parse(raw["result"]),
            tuple(Reference.parse(item) for item in raw["parameters"]),
        )
        indexes.runtime_helpers.register(reference, entity)
        helpers[entity_id] = entity

    orders: dict[str, MemoryOrderMapping] = {}
    for entity_id in order_inventory.declared:
        entity_root = order_inventory.root / entity_id
        source = entity_root / "memory_order.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "memory-order.yaml"
        )
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("memory_orders",), entity_id)
        entity = MemoryOrderMapping(
            reference,
            source,
            entity_root,
            entity_id,
            str(raw["instruction_order"]),
            _memory_order_sequence(raw.get("load")),
            _memory_order_sequence(raw.get("store")),
            _memory_order_sequence(raw["thread_fence"]) or (),
        )
        indexes.memory_orders.register(reference, entity)
        orders[entity_id] = entity

    atomic_lowerings: dict[str, AtomicLowering] = {}
    for entity_id in atomic_inventory.declared:
        entity_root = atomic_inventory.root / entity_id
        source = entity_root / "lowering.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "atomic-lowering.yaml"
        )
        _matching_id(source, entity_id, raw)
        reference = Reference(owner, ("atomic_lowerings",), entity_id)
        entity = AtomicLowering(
            reference,
            source,
            entity_root,
            entity_id,
            tuple(raw["c_operations"]),
            str(raw["strategy"]),
            tuple(QualifiedReference.parse(item) for item in raw["instructions"]),
        )
        indexes.atomic_lowerings.register(reference, entity)
        atomic_lowerings[entity_id] = entity

    return CAbiNamespace(
        owner,
        root,
        type_inventory,
        register_inventory,
        value_inventory,
        promotion_inventory,
        helper_inventory,
        order_inventory,
        atomic_inventory,
        MappingProxyType(types),
        convention,
        MappingProxyType(helpers),
        MappingProxyType(orders),
        MappingProxyType(atomic_lowerings),
    )


def _inventory(owner: str, root: Path, kind: str, plural: str) -> DirectoryInventory:
    return DirectoryInventory.load(
        owner=owner,
        kind=kind,
        source=root / plural / f"{plural}.yaml",
        root=root / plural,
        key=plural,
    )


def _location_policy(raw: Mapping[str, object]) -> LocationPolicy:
    return LocationPolicy(
        str(raw["mode"]),
        Reference.parse(raw["register_class"])
        if "register_class" in raw
        else None,
        int(raw["units"]) if "units" in raw else None,
        int(raw.get("alignment_units", 1)),
        int(raw["direct_maximum_bytes"])
        if "direct_maximum_bytes" in raw
        else None,
        str(raw["fallback"]) if "fallback" in raw else None,
    )


def _memory_order_sequence(
    raw: object,
) -> tuple[str | QualifiedReference, ...] | None:
    if raw is None:
        return None
    return tuple(
        item if item == "access" else QualifiedReference.parse(item)
        for item in raw
    )


def _matching_id(source: Path, expected: str, raw: Mapping[str, object]) -> None:
    if raw.get("id") != expected:
        raise ValueError(
            f"{source}: entity ID {raw.get('id')!r} does not match "
            f"directory {expected!r}"
        )


def _build_entities(
    indexes: _Indexes,
    document_topics: ReferenceIndex[DomainDocumentTopic],
) -> EntityCatalog:
    result = ReferenceIndex[Entity]()
    for kind, values in (
        (EntityKind.C_ABI_TYPE, indexes.types),
        (EntityKind.C_REGISTER_CLASS, indexes.register_classes),
        (EntityKind.C_VALUE_CLASS, indexes.value_classes),
        (EntityKind.C_PROMOTION, indexes.promotions),
        (EntityKind.C_RUNTIME_HELPER, indexes.runtime_helpers),
        (EntityKind.C_MEMORY_ORDER, indexes.memory_orders),
        (EntityKind.C_ATOMIC_LOWERING, indexes.atomic_lowerings),
        (EntityKind.TOPIC, document_topics),
    ):
        for reference, value in values.items():
            display = (
                value.symbol
                if isinstance(value, RuntimeHelper)
                else value.title
                if isinstance(value, DomainDocumentTopic)
                else value.id
            )
            result.register(
                reference,
                Entity(
                    reference,
                    kind,
                    display,
                    value,
                    entity_label(reference),
                    EntityDisplayStyle.TEXT
                    if isinstance(value, DomainDocumentTopic)
                    else EntityDisplayStyle.CODE,
                ),
            )
    return EntityCatalog(result)
