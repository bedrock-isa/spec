"""Hierarchical typed project for the Bedrock C ABI."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, TypeVar, cast

from engine.entity import (
    Entity,
    EntityCatalog,
    EntityDisplayStyle,
)
from engine.dependency import EntityDependency
from engine.inventory import DirectoryInventory
from engine.reference import QualifiedReference, Reference, ReferenceIndex
from engine.yaml_document import SchemaValidatedYamlLoader

if TYPE_CHECKING:
    from engine.project import InstructionBundle
    from engine.register import Register


_T = TypeVar("_T")


@dataclass(frozen=True, slots=True)
class CType(Entity):
    reference: Reference["CType"]
    source: Path
    root: Path
    id: str
    spelling: str
    call_kind: str
    size_bits: int | str
    alignment_bytes: int
    representation: str | None


@dataclass(frozen=True, slots=True)
class RegisterClass(Entity):
    reference: Reference["RegisterClass"]
    source: Path
    root: Path
    id: str
    arguments: tuple[QualifiedReference[Register], ...]
    results: tuple[QualifiedReference[Register], ...]
    allocation: str
    tuple_alignment: int
    exhaustion: str


@dataclass(frozen=True, slots=True)
class LocationPolicy:
    mode: str
    register_class: Reference["RegisterClass"] | None
    units: int | None
    alignment_units: int
    direct_maximum_bytes: int | None


@dataclass(frozen=True, slots=True)
class ValueClass(Entity):
    reference: Reference["ValueClass"]
    source: Path
    root: Path
    id: str
    kinds: tuple[str, ...]
    argument: LocationPolicy
    result: LocationPolicy


@dataclass(frozen=True, slots=True)
class Promotion(Entity):
    reference: Reference["Promotion"]
    source: Path
    root: Path
    id: str
    source_kinds: tuple[str, ...]
    target_kind: str


@dataclass(frozen=True, slots=True)
class StackConvention:
    pointer: QualifiedReference[Register]
    growth: str
    entry_alignment_bytes: int
    first_argument_offset_bytes: int
    argument_slot_bytes: int
    sret_register: QualifiedReference[Register]
    red_zone_bytes: int


@dataclass(frozen=True, slots=True)
class PreservationSet:
    registers: tuple[QualifiedReference[Register], ...]
    disposition: str


@dataclass(frozen=True, slots=True)
class CallingConvention:
    source: Path
    root: Path
    stack: StackConvention
    register_class_inventory: DirectoryInventory
    value_class_inventory: DirectoryInventory
    promotion_inventory: DirectoryInventory
    register_classes: tuple[Reference[RegisterClass], ...]
    value_classes: tuple[Reference[ValueClass], ...]
    promotions: tuple[Reference[Promotion], ...]
    preservation: tuple[PreservationSet, ...]


@dataclass(frozen=True, slots=True)
class RuntimeHelper(Entity):
    reference: Reference["RuntimeHelper"]
    source: Path
    root: Path
    id: str
    symbol: str
    result: Reference[CType]
    parameters: tuple[Reference[CType], ...]


@dataclass(frozen=True, slots=True)
class MemoryOrderMapping(Entity):
    reference: Reference["MemoryOrderMapping"]
    source: Path
    root: Path
    id: str
    instruction_order: str
    load: tuple[str | QualifiedReference[InstructionBundle], ...] | None
    store: tuple[str | QualifiedReference[InstructionBundle], ...] | None
    thread_fence: tuple[str | QualifiedReference[InstructionBundle], ...]


@dataclass(frozen=True, slots=True)
class AtomicLowering(Entity):
    reference: Reference["AtomicLowering"]
    source: Path
    root: Path
    id: str
    c_operations: tuple[str, ...]
    strategy: str
    instructions: tuple[QualifiedReference[InstructionBundle], ...]


@dataclass(frozen=True, slots=True)
class ResolvedRegisterClass:
    definition: RegisterClass
    arguments: tuple[Register, ...]
    results: tuple[Register, ...]


@dataclass(frozen=True, slots=True)
class ResolvedValueClass:
    definition: ValueClass
    argument_register_class: ResolvedRegisterClass | None
    result_register_class: ResolvedRegisterClass | None


@dataclass(frozen=True, slots=True)
class ResolvedCallingConvention:
    definition: CallingConvention
    stack_pointer: Register
    sret_register: Register
    register_classes: Mapping[Reference[RegisterClass], ResolvedRegisterClass]
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
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path) -> "CAbiProject":
        domain_root = Path(root).resolve()
        indexes = _Indexes.create()
        base = _load_namespace("base", domain_root, indexes)
        entities = _build_entities(indexes)
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
            entities,
        )

    def resolve(self, reference: Reference[_T]) -> _T:
        return cast(
            _T,
            self.entities.resolve(cast(Reference[Entity], reference)),
        )

    def entity_dependencies(self) -> tuple[EntityDependency, ...]:
        """Return the C ABI relationships intentionally exposed to tooling."""

        result: list[EntityDependency] = []

        def add(
            source: Reference[object],
            target: QualifiedReference[object],
            kind: str,
        ) -> None:
            result.append(EntityDependency(source, target, kind))

        def local(reference: Reference[object]) -> QualifiedReference[object]:
            return QualifiedReference("abi.c", reference)

        for definition in self.register_classes.values():
            source = cast(Reference[object], definition.reference)
            for target in (*definition.arguments, *definition.results):
                add(
                    source,
                    cast(QualifiedReference[object], target),
                    "register-class-register",
                )
        for definition in self.value_classes.values():
            source = cast(Reference[object], definition.reference)
            for policy in (definition.argument, definition.result):
                if policy.register_class is not None:
                    add(
                        source,
                        local(cast(Reference[object], policy.register_class)),
                        "value-class-register-class",
                    )
        for definition in self.runtime_helpers.values():
            source = cast(Reference[object], definition.reference)
            for target in (definition.result, *definition.parameters):
                add(
                    source,
                    local(cast(Reference[object], target)),
                    "runtime-helper-type",
                )
        for definition in self.memory_orders.values():
            source = cast(Reference[object], definition.reference)
            sequences = (
                definition.load or (),
                definition.store or (),
                definition.thread_fence,
            )
            for sequence in sequences:
                for target in sequence:
                    if isinstance(target, QualifiedReference):
                        add(
                            source,
                            cast(QualifiedReference[object], target),
                            "memory-order-instruction",
                        )
        for definition in self.atomic_lowerings.values():
            source = cast(Reference[object], definition.reference)
            for target in definition.instructions:
                add(
                    source,
                    cast(QualifiedReference[object], target),
                    "atomic-lowering-instruction",
                )
        return tuple(result)

    def validate(self, workspace) -> None:
        """Resolve every local and cross-domain relationship."""

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
                call_kind_owner = kind_owners.get(kind)
                if call_kind_owner is not None:
                    raise ValueError(
                        f"{value_class.source}: call kind {kind!r} is also "
                        f"classified by {call_kind_owner.id}"
                    )
                kind_owners[kind] = value_class
            for policy in (value_class.argument, value_class.result):
                if policy.register_class is not None:
                    self.register_classes.resolve(policy.register_class)
        convention = self.calling_convention
        workspace.resolve(convention.stack.pointer)
        workspace.resolve(convention.stack.sret_register)
        allocated_registers: dict[
            QualifiedReference[Register], Reference[RegisterClass]
        ] = {}
        for register_class_reference in convention.register_classes:
            register_class = self.register_classes.resolve(register_class_reference)
            for register in register_class.arguments:
                allocation_owner = allocated_registers.get(register)
                if allocation_owner is not None:
                    previous_class = self.register_classes.resolve(allocation_owner)
                    register_target = workspace.resolve(register)
                    raise ValueError(
                        f"{register_class.source}: argument register "
                        f"{register_target.id} is also allocated by "
                        f"{previous_class.id}"
                    )
                allocated_registers[register] = register_class_reference
        for value_class_reference in convention.value_classes:
            self.value_classes.resolve(value_class_reference)
        promotion_sources: dict[str, Reference[Promotion]] = {}
        for promotion_reference in convention.promotions:
            promotion = self.promotions.resolve(promotion_reference)
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
                promotion_owner = promotion_sources.get(kind)
                if promotion_owner is not None:
                    previous_promotion = self.promotions.resolve(promotion_owner)
                    raise ValueError(
                        f"{promotion.source}: source kind {kind!r} is also "
                        f"promoted by {previous_promotion.id}"
                    )
                promotion_sources[kind] = promotion_reference
        preserved: dict[QualifiedReference[Register], str] = {}
        for preservation in convention.preservation:
            for register in preservation.registers:
                workspace.resolve(register)
                previous_disposition = preserved.get(register)
                if previous_disposition is not None:
                    register_target = workspace.resolve(register)
                    raise ValueError(
                        f"{convention.source}: register {register_target.id} has both "
                        f"{previous_disposition!r} and {preservation.disposition!r} dispositions"
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
                operation_owner = operation_owners.get(operation)
                if operation_owner is not None:
                    raise ValueError(
                        f"{lowering.source}: C operation {operation!r} is also "
                        f"lowered by {operation_owner.id}"
                    )
                operation_owners[operation] = lowering
            for instruction in lowering.instructions:
                workspace.resolve(instruction)

    def resolved_calling_convention(self, workspace) -> ResolvedCallingConvention:
        convention = self.calling_convention
        resolved_registers: dict[Reference[RegisterClass], ResolvedRegisterClass] = {}
        for register_class_reference in convention.register_classes:
            register_class = self.register_classes.resolve(register_class_reference)
            resolved_registers[register_class_reference] = ResolvedRegisterClass(
                register_class,
                tuple(workspace.resolve(register) for register in register_class.arguments),
                tuple(workspace.resolve(register) for register in register_class.results),
            )
        resolved_values: dict[str, ResolvedValueClass] = {}
        for value_class_reference in convention.value_classes:
            value_class = self.value_classes.resolve(value_class_reference)
            argument_class = (
                resolved_registers[value_class.argument.register_class]
                if value_class.argument.register_class is not None
                else None
            )
            result_class = (
                resolved_registers[value_class.result.register_class]
                if value_class.result.register_class is not None
                else None
            )
            resolved_value_class = ResolvedValueClass(
                value_class, argument_class, result_class
            )
            for kind in value_class.kinds:
                resolved_values[kind] = resolved_value_class
        promotions: dict[str, str] = {}
        for promotion_reference in convention.promotions:
            promotion = self.promotions.resolve(promotion_reference)
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
        c_type_reference: Reference[CType] = Reference(owner, ("types",), entity_id)
        c_type = CType(
            c_type_reference,
            source,
            entity_root,
            entity_id,
            raw["spelling"],
            raw["call_kind"],
            raw["size_bits"],
            raw["alignment_bytes"],
            raw.get("representation"),
        )
        indexes.types.register(c_type_reference, c_type)
        types[entity_id] = c_type

    for child_id in register_inventory.declared:
        child_root = register_inventory.root / child_id
        child_source = child_root / "register_class.yaml"
        child = SchemaValidatedYamlLoader().load(
            child_source, schemas / "register-class.yaml"
        )
        _matching_id(child_source, child_id, child)
        register_class_reference: Reference[RegisterClass] = Reference(
            owner, ("register_classes",), child_id
        )
        indexes.register_classes.register(
            register_class_reference,
            RegisterClass(
                register_class_reference, child_source, child_root, child_id,
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
        value_class_reference: Reference[ValueClass] = Reference(
            owner, ("value_classes",), child_id
        )
        indexes.value_classes.register(
            value_class_reference,
            ValueClass(
                value_class_reference, child_source, child_root, child_id,
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
        promotion_reference: Reference[Promotion] = Reference(
            owner, ("promotions",), child_id
        )
        indexes.promotions.register(
            promotion_reference,
            Promotion(
                promotion_reference, child_source, child_root, child_id,
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
        helper_reference: Reference[RuntimeHelper] = Reference(
            owner, ("runtime_helpers",), entity_id
        )
        helper = RuntimeHelper(
            helper_reference,
            source,
            entity_root,
            entity_id,
            raw["symbol"],
            Reference.parse(cast(str, raw["result"])),
            tuple(
                Reference.parse(cast(str, parameter))
                for parameter in cast(list[object], raw["parameters"])
            ),
        )
        indexes.runtime_helpers.register(helper_reference, helper)
        helpers[entity_id] = helper

    orders: dict[str, MemoryOrderMapping] = {}
    for entity_id in order_inventory.declared:
        entity_root = order_inventory.root / entity_id
        source = entity_root / "memory_order.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "memory-order.yaml"
        )
        _matching_id(source, entity_id, raw)
        memory_order_reference: Reference[MemoryOrderMapping] = Reference(
            owner, ("memory_orders",), entity_id
        )
        memory_order = MemoryOrderMapping(
            memory_order_reference,
            source,
            entity_root,
            entity_id,
            str(raw["instruction_order"]),
            _memory_order_sequence(raw.get("load")),
            _memory_order_sequence(raw.get("store")),
            _memory_order_sequence(raw["thread_fence"]) or (),
        )
        indexes.memory_orders.register(memory_order_reference, memory_order)
        orders[entity_id] = memory_order

    atomic_lowerings: dict[str, AtomicLowering] = {}
    for entity_id in atomic_inventory.declared:
        entity_root = atomic_inventory.root / entity_id
        source = entity_root / "lowering.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, schemas / "atomic-lowering.yaml"
        )
        _matching_id(source, entity_id, raw)
        atomic_lowering_reference: Reference[AtomicLowering] = Reference(
            owner, ("atomic_lowerings",), entity_id
        )
        atomic_lowering = AtomicLowering(
            atomic_lowering_reference,
            source,
            entity_root,
            entity_id,
            tuple(raw["c_operations"]),
            str(raw["strategy"]),
            tuple(
                QualifiedReference.parse(cast(str, instruction))
                for instruction in cast(list[object], raw["instructions"])
            ),
        )
        indexes.atomic_lowerings.register(atomic_lowering_reference, atomic_lowering)
        atomic_lowerings[entity_id] = atomic_lowering

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
    return DirectoryInventory.load_strict(
        owner=owner,
        kind=kind,
        source=root / plural / f"{plural}.yaml",
        root=root / plural,
        key=plural,
    )


def _location_policy(raw: Mapping[str, object]) -> LocationPolicy:
    return LocationPolicy(
        str(raw["mode"]),
        Reference.parse(cast(str, raw["register_class"]))
        if "register_class" in raw
        else None,
        int(cast(int | str, raw["units"])) if "units" in raw else None,
        int(cast(int | str, raw.get("alignment_units", 1))),
        int(cast(int | str, raw["direct_maximum_bytes"]))
        if "direct_maximum_bytes" in raw
        else None,
    )


def _memory_order_sequence(
    raw: object,
) -> tuple[str | QualifiedReference[InstructionBundle], ...] | None:
    if raw is None:
        return None
    return tuple(
        item if item == "access" else QualifiedReference.parse(item)
        for item in cast(list[str], raw)
    )


def _matching_id(source: Path, expected: str, raw: Mapping[str, object]) -> None:
    if raw.get("id") != expected:
        raise ValueError(
            f"{source}: entity ID {raw.get('id')!r} does not match "
            f"directory {expected!r}"
        )


def _build_entities(indexes: _Indexes) -> EntityCatalog:
    entries: list[tuple[Entity, str, EntityDisplayStyle]] = []
    for values in (
        indexes.types,
        indexes.register_classes,
        indexes.value_classes,
        indexes.promotions,
        indexes.runtime_helpers,
        indexes.memory_orders,
        indexes.atomic_lowerings,
    ):
        for value in values.values():
            display = value.symbol if isinstance(value, RuntimeHelper) else value.id
            entries.append((value, display, EntityDisplayStyle.CODE))
    return EntityCatalog.create(entries)
