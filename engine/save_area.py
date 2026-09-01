"""Structured SAVE/RESTORE base-header fields."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .entity import Entity
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class SaveAreaField(Entity):
    reference: Reference["SaveAreaField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1


@dataclass(frozen=True, slots=True)
class SaveAreaHeader(Entity):
    reference: Reference["SaveAreaHeader"]
    source: Path
    id: str
    bits: int
    fields: tuple[SaveAreaField, ...]


@dataclass(frozen=True, slots=True)
class SaveAreaReferenceIndexes:
    headers: ReferenceIndex[SaveAreaHeader]
    fields: ReferenceIndex[SaveAreaField]


@dataclass(frozen=True, slots=True)
class SaveAreaCatalog:
    header: SaveAreaHeader
    references: SaveAreaReferenceIndexes

    @classmethod
    def load(cls, isa_root: str | Path) -> "SaveAreaCatalog":
        root = Path(isa_root).resolve()
        source = root / "state/definitions/save_area_header.yaml"
        raw = SchemaValidatedYamlLoader().load(
            source, root / "schemas/save-area-header.yaml"
        )
        header_reference: Reference[SaveAreaHeader] = Reference(
            "base", ("state", "save_area"), raw["id"]
        )
        fields = tuple(
            SaveAreaField(
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
        header = SaveAreaHeader(
            header_reference, source, raw["id"], raw["bits"], fields
        )
        _validate_fields(header)
        headers = ReferenceIndex[SaveAreaHeader]()
        headers.register(header.reference, header)
        field_index = ReferenceIndex[SaveAreaField]()
        for field in fields:
            field_index.register(field.reference, field)
        return cls(header, SaveAreaReferenceIndexes(headers, field_index))


def _validate_fields(header: SaveAreaHeader) -> None:
    for index, field in enumerate(header.fields):
        if field.msb >= header.bits:
            raise ValueError(
                f"{header.source}: save-area field {field.id!r} exceeds "
                f"the {header.bits}-bit header"
            )
        conflict = next(
            (
                other
                for other in header.fields[index + 1 :]
                if field.lsb <= other.msb and other.lsb <= field.msb
            ),
            None,
        )
        if conflict is not None:
            raise ValueError(
                f"{header.source}: save-area fields {field.id!r} and "
                f"{conflict.id!r} overlap"
            )
