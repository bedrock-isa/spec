"""Structured debug-trigger slot words and fields."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .entity import Entity
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class DebugTriggerField(Entity):
    reference: Reference["DebugTriggerField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1


@dataclass(frozen=True, slots=True)
class DebugTriggerWord(Entity):
    reference: Reference["DebugTriggerWord"]
    source: Path
    id: str
    bank: int
    bits: int
    fields: tuple[DebugTriggerField, ...]


@dataclass(frozen=True, slots=True)
class DebugTriggerSlot(Entity):
    reference: Reference["DebugTriggerSlot"]
    source: Path
    id: str
    words: Mapping[str, DebugTriggerWord]


@dataclass(frozen=True, slots=True)
class DebugTriggerReferenceIndexes:
    slots: ReferenceIndex[DebugTriggerSlot]
    words: ReferenceIndex[DebugTriggerWord]
    fields: ReferenceIndex[DebugTriggerField]


@dataclass(frozen=True, slots=True)
class DebugTriggerCatalog:
    slot: DebugTriggerSlot
    references: DebugTriggerReferenceIndexes

    @classmethod
    def load(cls, isa_root: str | Path) -> "DebugTriggerCatalog":
        root = Path(isa_root).resolve()
        source = root / "debug/definitions/trigger_slot.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, root / "schemas/debug-trigger-slot.yaml"
        )
        slot_reference: Reference[DebugTriggerSlot] = Reference(
            "base", ("debug", "triggers"), raw["id"]
        )
        words = ReferenceIndex[DebugTriggerWord]()
        fields = ReferenceIndex[DebugTriggerField]()
        loaded_words: dict[str, DebugTriggerWord] = {}
        for raw_word in raw["words"]:
            word_reference: Reference[DebugTriggerWord] = Reference(
                slot_reference.owner,
                (*slot_reference.path, slot_reference.element),
                raw_word["id"],
            )
            loaded_fields = tuple(
                DebugTriggerField(
                    Reference(
                        word_reference.owner,
                        (*word_reference.path, word_reference.element),
                        raw_field["id"],
                    ),
                    source,
                    raw_field["id"],
                    raw_field["lsb"],
                    raw_field["bits"],
                )
                for raw_field in raw_word.get("fields", ())
            )
            word = DebugTriggerWord(
                word_reference,
                source,
                raw_word["id"],
                raw_word["bank"],
                raw["word_bits"],
                loaded_fields,
            )
            _validate_fields(word)
            words.register(word.reference, word)
            for field in loaded_fields:
                fields.register(field.reference, field)
            loaded_words[word.id] = word
        slot = DebugTriggerSlot(
            slot_reference, source, raw["id"], MappingProxyType(loaded_words)
        )
        slots = ReferenceIndex[DebugTriggerSlot]()
        slots.register(slot.reference, slot)
        return cls(slot, DebugTriggerReferenceIndexes(slots, words, fields))


def _validate_fields(word: DebugTriggerWord) -> None:
    for index, field in enumerate(word.fields):
        if field.msb >= word.bits:
            raise ValueError(
                f"{word.source}: debug-trigger field {field.id!r} exceeds "
                f"the {word.bits}-bit {word.id} word"
            )
        conflict = next(
            (
                other
                for other in word.fields[index + 1 :]
                if field.lsb <= other.msb and other.lsb <= field.msb
            ),
            None,
        )
        if conflict is not None:
            raise ValueError(
                f"{word.source}: debug-trigger fields {field.id!r} and "
                f"{conflict.id!r} overlap in {word.id}"
            )
