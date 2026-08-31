"""Unified logical-entity index assembled from typed ISA registries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re
from types import MappingProxyType
from typing import Iterable, Mapping, TypeVar, cast

from .reference import Reference, ReferenceIndex
_T = TypeVar("_T")


class EntityKind(StrEnum):
    TOPIC = "topic"
    INSTRUCTION = "instruction"
    EA_MODE = "ea-mode"
    FIELD_TYPE = "field-type"
    PAYLOAD_TYPE = "payload-type"
    CPUID_CLASS = "cpuid-class"
    CPUID_LEAF = "cpuid-leaf"
    CPUID_QUERY = "cpuid-query"
    CPUID_FIELD = "cpuid-field"
    EVENT_CLASS = "event-class"
    EVENT = "event"
    REGISTER_GROUP = "register-group"
    REGISTER = "register"
    CONTROL_REGISTER_NAMESPACE = "control-register-namespace"
    CONTROL_REGISTER = "control-register"
    TERM_GROUP = "term-group"
    TERM = "term"
    ELF_RELOCATION = "elf-relocation"
    ELF_LINKAGE_PROTOCOL = "elf-linkage-protocol"
    ELF_TLS_MODEL = "elf-tls-model"
    ELF_CODE_MODEL = "elf-code-model"
    ELF_DEBUG_REGISTER = "elf-debug-register"
    C_ABI_TYPE = "c-abi-type"
    C_REGISTER_CLASS = "c-register-class"
    C_VALUE_CLASS = "c-value-class"
    C_PROMOTION = "c-promotion"
    C_RUNTIME_HELPER = "c-runtime-helper"
    C_MEMORY_ORDER = "c-memory-order"
    C_ATOMIC_LOWERING = "c-atomic-lowering"
    INTERFACE_TYPE_GROUP = "interface-type-group"
    INTERFACE_INTRINSIC_GROUP = "interface-intrinsic-group"
    INTERFACE_UTILITY_GROUP = "interface-utility-group"
    INTERFACE_TYPE = "interface-type"
    INTERFACE_INTRINSIC = "interface-intrinsic"
    INTERFACE_UTILITY = "interface-utility"


class EntityDisplayStyle(StrEnum):
    TEXT = "text"
    CODE = "code"


@dataclass(frozen=True, slots=True)
class Entity:
    reference: Reference["Entity"]
    kind: EntityKind
    display: str
    source: Path
    value: object
    display_style: EntityDisplayStyle = EntityDisplayStyle.TEXT


@dataclass(frozen=True, slots=True)
class EntityCatalog:
    references: ReferenceIndex[Entity]

    @classmethod
    def build(
        cls,
        types,
        sources,
        cpuid,
        events,
        registers,
        control_registers,
        terminology,
        model,
    ) -> "EntityCatalog":
        index = ReferenceIndex[Entity]()

        def add(
            reference: Reference[_T],
            kind: EntityKind,
            display: str,
            source: Path,
            value,
            *,
            style: EntityDisplayStyle = EntityDisplayStyle.TEXT,
        ) -> None:
            normalized = cast(Reference[Entity], reference)
            index.register(
                normalized,
                Entity(normalized, kind, display, source, value, style),
            )

        for topic in model.document_topics.values():
            reference = cast(Reference[Entity], topic.reference)
            add(
                reference,
                EntityKind.TOPIC,
                _humanize(topic.id),
                topic.source,
                topic,
            )
        for reference, bundle in sources.instructions.items():
            add(
                reference,
                EntityKind.INSTRUCTION,
                bundle.instruction.mnemonic,
                bundle.instruction.source,
                bundle,
                style=EntityDisplayStyle.CODE,
            )
        for reference, mode in sources.ea_modes.items():
            add(
                reference,
                EntityKind.EA_MODE,
                mode.id,
                mode.source,
                mode,
                style=EntityDisplayStyle.CODE,
            )
        for reference, definition in types.field_types.items():
            add(
                reference,
                EntityKind.FIELD_TYPE,
                definition.id,
                definition.source,
                definition,
                style=EntityDisplayStyle.CODE,
            )
        for reference, definition in types.payload_types.items():
            add(
                reference,
                EntityKind.PAYLOAD_TYPE,
                definition.id,
                definition.source,
                definition,
                style=EntityDisplayStyle.CODE,
            )
        for kind, typed_index in (
            (EntityKind.CPUID_CLASS, cpuid.references.classes),
            (EntityKind.CPUID_LEAF, cpuid.references.leaves),
            (EntityKind.CPUID_QUERY, cpuid.references.queries),
            (EntityKind.CPUID_FIELD, cpuid.references.fields),
            (EntityKind.EVENT_CLASS, events.references.classes),
            (EntityKind.EVENT, events.references.events),
            (EntityKind.REGISTER_GROUP, registers.references.groups),
            (EntityKind.REGISTER, registers.references.registers),
            (
                EntityKind.CONTROL_REGISTER_NAMESPACE,
                control_registers.references.namespaces,
            ),
            (EntityKind.CONTROL_REGISTER, control_registers.references.registers),
        ):
            for reference, value in typed_index.items():
                display = getattr(value, "name", None) or getattr(value, "id", None)
                add(
                    reference,
                    kind,
                    str(
                        value.id
                        if kind
                        in {
                            EntityKind.REGISTER,
                            EntityKind.CONTROL_REGISTER,
                            EntityKind.EVENT,
                            EntityKind.CPUID_LEAF,
                            EntityKind.CPUID_QUERY,
                            EntityKind.CPUID_FIELD,
                        }
                        else display
                    ),
                    value.source,
                    value,
                    style=(
                        EntityDisplayStyle.CODE
                        if kind
                        in {
                            EntityKind.REGISTER,
                            EntityKind.EVENT,
                            EntityKind.CPUID_LEAF,
                            EntityKind.CPUID_QUERY,
                            EntityKind.CPUID_FIELD,
                        }
                        else EntityDisplayStyle.TEXT
                    ),
                )
        for reference, group in terminology.references.groups.items():
            add(
                reference,
                EntityKind.TERM_GROUP,
                group.title,
                group.source,
                group,
            )
        for reference, term in terminology.references.terms.items():
            add(
                reference,
                EntityKind.TERM,
                term.forms.canonical,
                term.source,
                term,
            )
        return cls(index)

    def resolve(self, reference: Reference[Entity]) -> Entity:
        return self.references.resolve(reference)


@dataclass(frozen=True, slots=True)
class PublicTargetCatalog:
    """The entity targets deliberately emitted by one public projector."""

    entities: EntityCatalog
    labels: Mapping[Reference[Entity], str]

    @classmethod
    def create(
        cls,
        entities: EntityCatalog,
        targets: Iterable[tuple[Reference[object], str]],
    ) -> "PublicTargetCatalog":
        labels: dict[Reference[Entity], str] = {}
        owners: dict[str, Reference[Entity]] = {}
        for reference, label in targets:
            normalized = cast(Reference[Entity], reference)
            entities.resolve(normalized)
            previous = labels.get(normalized)
            if previous is not None and previous != label:
                raise ValueError(
                    f"public entity target {normalized!r} has conflicting labels"
                )
            owner = owners.get(label)
            if owner is not None and owner != normalized:
                raise ValueError(
                    f"public TeX label {label!r} is shared by distinct entities"
                )
            labels[normalized] = label
            owners[label] = normalized
        return cls(entities, MappingProxyType(labels))

    def resolve(self, reference: Reference[Entity]) -> tuple[Entity, str]:
        try:
            label = self.labels[reference]
        except KeyError as error:
            raise ValueError(
                f"entity {reference!r} has no target in this public projection"
            ) from error
        return self.entities.resolve(reference), label

    def label(self, reference: Reference[object]) -> str:
        normalized = cast(Reference[Entity], reference)
        return self.resolve(normalized)[1]


    def contains(self, reference: Reference[object]) -> bool:
        return cast(Reference[Entity], reference) in self.labels


def instruction_label(mnemonic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", mnemonic.lower()).strip("-")
    return f"instr:{slug}"


def _humanize(value: str) -> str:
    return value.replace("-", " ").replace("_", " ")
