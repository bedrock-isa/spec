"""Structured extended-instruction header fields."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .entity import Entity
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class InstructionHeaderField(Entity):
    reference: Reference["InstructionHeaderField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1


@dataclass(frozen=True, slots=True)
class InstructionHeader(Entity):
    reference: Reference["InstructionHeader"]
    source: Path
    id: str
    bits: int
    fields: tuple[InstructionHeaderField, ...]


@dataclass(frozen=True, slots=True)
class InstructionHeaderReferenceIndexes:
    headers: ReferenceIndex[InstructionHeader]
    fields: ReferenceIndex[InstructionHeaderField]


@dataclass(frozen=True, slots=True)
class InstructionHeaderCatalog:
    header: InstructionHeader
    references: InstructionHeaderReferenceIndexes

    @classmethod
    def load(cls, isa_root: str | Path) -> "InstructionHeaderCatalog":
        root = Path(isa_root).resolve()
        source = root / "encoding/definitions/extended_header.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, root / "schemas/instruction-header.yaml"
        )
        header_reference: Reference[InstructionHeader] = Reference(
            "base", ("encoding", "instruction"), raw["id"]
        )
        fields = tuple(
            InstructionHeaderField(
                Reference(
                    header_reference.owner,
                    (*header_reference.path, header_reference.element),
                    value["id"],
                ),
                source,
                value["id"],
                value["lsb"],
                value["bits"],
            )
            for value in raw["fields"]
        )
        header = InstructionHeader(
            header_reference, source, raw["id"], raw["bits"], fields
        )
        for field in fields:
            if field.msb >= header.bits:
                raise ValueError(
                    f"{source}: instruction-header field {field.id!r} exceeds "
                    f"the {header.bits}-bit header"
                )
        headers = ReferenceIndex[InstructionHeader]()
        headers.register(header.reference, header)
        field_index = ReferenceIndex[InstructionHeaderField]()
        for field in fields:
            field_index.register(field.reference, field)
        return cls(header, InstructionHeaderReferenceIndexes(headers, field_index))
