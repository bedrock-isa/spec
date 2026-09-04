"""Structured architectural-event frame and payload fields."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .entity import Entity
from .inventory import DirectoryInventory
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class EventFrameField(Entity):
    reference: Reference["EventFrameField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1


@dataclass(frozen=True, slots=True)
class EventFrameSlot(Entity):
    reference: Reference["EventFrameSlot"]
    source: Path
    id: str
    offset: int
    bits: int
    fields: tuple[EventFrameField, ...]


@dataclass(frozen=True, slots=True)
class EventFrame(Entity):
    reference: Reference["EventFrame"]
    source: Path
    id: str
    slots: Mapping[str, EventFrameSlot]


@dataclass(frozen=True, slots=True)
class EventFrameReferenceIndexes:
    frames: ReferenceIndex[EventFrame]
    slots: ReferenceIndex[EventFrameSlot]
    fields: ReferenceIndex[EventFrameField]


@dataclass(frozen=True, slots=True)
class EventFrameCatalog:
    frame: EventFrame
    references: EventFrameReferenceIndexes

    @classmethod
    def load(cls, isa_root: str | Path) -> "EventFrameCatalog":
        root = Path(isa_root).resolve()
        source = root / "events/definitions/event_frame.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, root / "schemas/event-frame.yaml"
        )
        frame_reference: Reference[EventFrame] = Reference(
            "base", ("events", "frame"), raw["id"]
        )
        slot_index = ReferenceIndex[EventFrameSlot]()
        field_index = ReferenceIndex[EventFrameField]()
        loaded_slots: dict[str, EventFrameSlot] = {}
        for raw_slot in raw["slots"]:
            slot_reference: Reference[EventFrameSlot] = Reference(
                frame_reference.owner,
                (*frame_reference.path, frame_reference.element),
                raw_slot["id"],
            )
            fields = tuple(
                EventFrameField(
                    Reference(
                        slot_reference.owner,
                        (*slot_reference.path, slot_reference.element),
                        value["id"],
                    ),
                    source,
                    value["id"],
                    value["lsb"],
                    value["bits"],
                )
                for value in raw_slot.get("fields", ())
            )
            slot = EventFrameSlot(
                slot_reference,
                source,
                raw_slot["id"],
                raw_slot["offset"],
                raw["slot_bits"],
                fields,
            )
            _validate_fields(slot.source, slot.id, slot.bits, slot.fields)
            slot_index.register(slot.reference, slot)
            for field in fields:
                field_index.register(field.reference, field)
            loaded_slots[slot.id] = slot
        frame = EventFrame(
            frame_reference, source, raw["id"], MappingProxyType(loaded_slots)
        )
        frames = ReferenceIndex[EventFrame]()
        frames.register(frame.reference, frame)
        return cls(frame, EventFrameReferenceIndexes(frames, slot_index, field_index))


@dataclass(frozen=True, slots=True)
class EventPayloadField(Entity):
    reference: Reference["EventPayloadField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1


@dataclass(frozen=True, slots=True)
class EventPayloadFormat(Entity):
    reference: Reference["EventPayloadFormat"]
    source: Path
    id: str
    bits: int
    fields: tuple[EventPayloadField, ...]


@dataclass(frozen=True, slots=True)
class EventPayloadReferenceIndexes:
    formats: ReferenceIndex[EventPayloadFormat]
    fields: ReferenceIndex[EventPayloadField]


@dataclass(frozen=True, slots=True)
class EventPayloadCatalog:
    inventory: DirectoryInventory
    formats: Mapping[str, EventPayloadFormat]
    references: EventPayloadReferenceIndexes

    @classmethod
    def load(cls, isa_root: str | Path) -> "EventPayloadCatalog":
        root = Path(isa_root).resolve()
        payload_root = root / "events/payloads"
        inventory = DirectoryInventory.load_strict(
            owner="base",
            kind="event-payload",
            source=payload_root / "payloads.yaml",
            root=payload_root,
            key="payloads",
            name_pattern=r"[A-Z][A-Z0-9_]*",
        )
        format_index = ReferenceIndex[EventPayloadFormat]()
        field_index = ReferenceIndex[EventPayloadField]()
        formats: dict[str, EventPayloadFormat] = {}
        for format_id in inventory.declared:
            source = payload_root / format_id / "payload.yaml"
            raw = SchemaValidatedYamlLoader().load(
                source, root / "schemas/event-payload.yaml"
            )
            format_reference: Reference[EventPayloadFormat] = Reference(
                "base", ("events", "payloads"), format_id
            )
            fields = tuple(
                EventPayloadField(
                    Reference(
                        format_reference.owner,
                        (*format_reference.path, format_reference.element),
                        value["id"],
                    ),
                    source,
                    value["id"],
                    value["lsb"],
                    value["bits"],
                )
                for value in raw["fields"]
            )
            payload = EventPayloadFormat(
                format_reference, source, format_id, raw["bits"], fields
            )
            _validate_fields(source, format_id, payload.bits, fields)
            format_index.register(payload.reference, payload)
            for field in fields:
                field_index.register(field.reference, field)
            formats[format_id] = payload
        return cls(
            inventory,
            MappingProxyType(formats),
            EventPayloadReferenceIndexes(format_index, field_index),
        )


def _validate_fields(source: Path, owner: str, bits: int, fields) -> None:
    for index, field in enumerate(fields):
        if field.msb >= bits:
            raise ValueError(
                f"{source}: field {field.id!r} exceeds the {bits}-bit {owner}"
            )
        conflict = next(
            (
                other
                for other in fields[index + 1 :]
                if field.lsb <= other.msb and other.lsb <= field.msb
            ),
            None,
        )
        if conflict is not None:
            raise ValueError(
                f"{source}: fields {field.id!r} and {conflict.id!r} "
                f"overlap in {owner}"
            )
