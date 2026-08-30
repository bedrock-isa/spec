"""Unified logical-entity index assembled from typed ISA registries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TypeVar, cast

from .reference import Reference, ReferenceIndex
from .yaml_document import YamlDocumentLoader


_T = TypeVar("_T")


class EntityKind(StrEnum):
    ARTIFACT = "artifact"
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
    TERM_GROUP = "term-group"
    TERM = "term"
    ELF_RELOCATION = "elf-relocation"
    ELF_LINKAGE_PROTOCOL = "elf-linkage-protocol"
    ELF_TLS_MODEL = "elf-tls-model"
    ELF_CODE_MODEL = "elf-code-model"
    ELF_DEBUG_REGISTER = "elf-debug-register"
    ELF_ENTRY_STATE = "elf-entry-state"
    C_ABI_TYPE = "c-abi-type"
    C_CALLING_CONVENTION = "c-calling-convention"
    C_REGISTER_CLASS = "c-register-class"
    C_VALUE_CLASS = "c-value-class"
    C_PROMOTION = "c-promotion"
    C_RUNTIME_HELPER = "c-runtime-helper"
    C_MEMORY_ORDER = "c-memory-order"
    C_ATOMIC_LOWERING = "c-atomic-lowering"


class EntityDisplayStyle(StrEnum):
    TEXT = "text"
    CODE = "code"


@dataclass(frozen=True, slots=True)
class Entity:
    reference: Reference["Entity"]
    kind: EntityKind
    display: str
    value: object
    latex_label: str | None = None
    display_style: EntityDisplayStyle = EntityDisplayStyle.TEXT


@dataclass(frozen=True, slots=True)
class EntityCatalog:
    references: ReferenceIndex[Entity]

    @classmethod
    def build(
        cls,
        root: Path,
        types,
        sources,
        cpuid,
        events,
        registers,
        terminology,
        model,
    ) -> "EntityCatalog":
        index = ReferenceIndex[Entity]()

        def add(
            reference: Reference[_T],
            kind: EntityKind,
            display: str,
            value,
            *,
            label: str | None = None,
            style: EntityDisplayStyle = EntityDisplayStyle.TEXT,
        ) -> None:
            normalized = cast(Reference[Entity], reference)
            index.register(
                normalized,
                Entity(normalized, kind, display, value, label, style),
            )

        for path in sorted((root.parent / "artifacts").glob("*/artifact.yaml")):
            raw = YamlDocumentLoader().mapping(path)
            artifact_id = raw.get("id")
            if not isinstance(artifact_id, str):
                continue
            reference: Reference[Entity] = Reference(
                "base", ("artifacts",), artifact_id
            )
            add(reference, EntityKind.ARTIFACT, artifact_id, path)
        for topic in model.document_topics.values():
            reference = cast(Reference[Entity], topic.reference)
            add(
                reference,
                EntityKind.TOPIC,
                _humanize(topic.id),
                topic,
                label=opaque_entity_label(len(index)),
            )
        for reference, bundle in sources.instructions.items():
            add(
                reference,
                EntityKind.INSTRUCTION,
                bundle.instruction.mnemonic,
                bundle,
                label=instruction_label(bundle.instruction.mnemonic),
                style=EntityDisplayStyle.CODE,
            )
        for reference, mode in sources.ea_modes.items():
            add(
                reference,
                EntityKind.EA_MODE,
                mode.id,
                mode,
                label=opaque_entity_label(len(index)),
                style=EntityDisplayStyle.CODE,
            )
        for reference, definition in types.field_types.items():
            add(
                reference,
                EntityKind.FIELD_TYPE,
                definition.id,
                definition,
                label=opaque_entity_label(len(index)),
                style=EntityDisplayStyle.CODE,
            )
        for reference, definition in types.payload_types.items():
            add(
                reference,
                EntityKind.PAYLOAD_TYPE,
                definition.id,
                definition,
                label=opaque_entity_label(len(index)),
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
        ):
            for reference, value in typed_index.items():
                display = getattr(value, "name", None) or getattr(value, "id", None)
                label = None
                if kind in {EntityKind.REGISTER_GROUP, EntityKind.REGISTER}:
                    label = opaque_entity_label(len(index))
                elif kind in {EntityKind.EVENT_CLASS, EntityKind.CPUID_CLASS}:
                    if value.extends is None:
                        label = opaque_entity_label(len(index))
                elif kind in {EntityKind.EVENT, EntityKind.CPUID_LEAF}:
                    if getattr(value, "extends", None) is None:
                        label = opaque_entity_label(len(index))
                elif kind in {EntityKind.CPUID_QUERY, EntityKind.CPUID_FIELD}:
                    label = opaque_entity_label(len(index))
                add(
                    reference,
                    kind,
                    str(
                        value.id
                        if kind
                        in {
                            EntityKind.REGISTER,
                            EntityKind.EVENT,
                            EntityKind.CPUID_LEAF,
                            EntityKind.CPUID_QUERY,
                            EntityKind.CPUID_FIELD,
                        }
                        else display
                    ),
                    value,
                    label=label,
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
                group,
                label=opaque_entity_label(len(index)),
            )
        for reference, term in terminology.references.terms.items():
            add(
                reference,
                EntityKind.TERM,
                term.forms.canonical,
                term,
                label=opaque_entity_label(len(index)),
            )
        return cls(index)

    def resolve(self, reference: Reference[Entity]) -> Entity:
        return self.references.resolve(reference)


def opaque_entity_label(ordinal: int) -> str:
    """Return a deterministic opaque TeX anchor for a catalog position."""

    return f"entity:{ordinal:08d}"


def instruction_label(mnemonic: str) -> str:
    import re

    slug = re.sub(r"[^a-z0-9]+", "-", mnemonic.lower()).strip("-")
    return f"instr:{slug}"


def _humanize(value: str) -> str:
    return value.replace("-", " ").replace("_", " ")
