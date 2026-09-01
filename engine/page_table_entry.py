"""Structured page-table-entry layouts and field lookup."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .entity import Entity
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


class PageTableEntryLayoutId(StrEnum):
    LEAF = "leaf"
    TABLE_POINTER = "table_pointer"


@dataclass(frozen=True, slots=True)
class PageTableEntryField(Entity):
    """One named field in a page-table-entry layout."""

    reference: Reference["PageTableEntryField"]
    source: Path
    id: str
    lsb: int
    bits: int

    @property
    def msb(self) -> int:
        return self.lsb + self.bits - 1

    def overlaps(self, other: "PageTableEntryField") -> bool:
        return self.lsb <= other.msb and other.lsb <= self.msb


@dataclass(frozen=True, slots=True)
class PageTableEntryLayout:
    """Fields active in one value-selected PTE layout branch."""

    id: PageTableEntryLayoutId
    fields: tuple[PageTableEntryField, ...]


@dataclass(frozen=True, slots=True)
class PageTableEntry(Entity):
    """The base ISA page-table-entry format."""

    reference: Reference["PageTableEntry"]
    source: Path
    id: str
    bits: int
    common_fields: tuple[PageTableEntryField, ...]
    layouts: Mapping[PageTableEntryLayoutId, PageTableEntryLayout]

    @property
    def fields(self) -> tuple[PageTableEntryField, ...]:
        return (
            *self.common_fields,
            *(field for layout in self.layouts.values() for field in layout.fields),
        )


@dataclass(frozen=True, slots=True)
class PageTableEntryReferenceIndexes:
    entries: ReferenceIndex[PageTableEntry]
    fields: ReferenceIndex[PageTableEntryField]


@dataclass(frozen=True, slots=True)
class PageTableEntryCatalog:
    """The base ISA page-table-entry definition and typed references."""

    entry: PageTableEntry
    references: PageTableEntryReferenceIndexes

    @classmethod
    def load(cls, isa_root: str | Path) -> "PageTableEntryCatalog":
        root = Path(isa_root).resolve()
        source = root / "memory/translation/definitions/page_table_entry.yaml"
        schema = root / "schemas/page-table-entry.yaml"
        raw = SchemaValidatedYamlLoader().load(source, schema)
        entry_reference: Reference[PageTableEntry] = Reference(
            "base", ("memory", "translation"), raw["id"]
        )

        fields = ReferenceIndex[PageTableEntryField]()

        def load_fields(values) -> tuple[PageTableEntryField, ...]:
            result: list[PageTableEntryField] = []
            for value in values:
                field = PageTableEntryField(
                    Reference(
                        entry_reference.owner,
                        (*entry_reference.path, entry_reference.element),
                        value["id"],
                    ),
                    source,
                    value["id"],
                    value["lsb"],
                    value["bits"],
                )
                fields.register(field.reference, field)
                result.append(field)
            return tuple(result)

        common_fields = load_fields(raw["common_fields"])
        layouts = {
            PageTableEntryLayoutId(layout_id): PageTableEntryLayout(
                PageTableEntryLayoutId(layout_id), load_fields(layout["fields"])
            )
            for layout_id, layout in raw["layouts"].items()
        }
        entry = PageTableEntry(
            entry_reference,
            source,
            raw["id"],
            raw["bits"],
            common_fields,
            MappingProxyType(layouts),
        )
        _validate_layouts(entry)
        entries = ReferenceIndex[PageTableEntry]()
        entries.register(entry.reference, entry)
        return cls(entry, PageTableEntryReferenceIndexes(entries, fields))


def _validate_layouts(entry: PageTableEntry) -> None:
    for layout in entry.layouts.values():
        active = (*entry.common_fields, *layout.fields)
        for index, field in enumerate(active):
            if field.msb >= entry.bits:
                raise ValueError(
                    f"{entry.source}: PTE field {field.id!r} exceeds "
                    f"the {entry.bits}-bit entry"
                )
            conflict = next(
                (other for other in active[index + 1 :] if field.overlaps(other)),
                None,
            )
            if conflict is not None:
                raise ValueError(
                    f"{entry.source}: PTE fields {field.id!r} and "
                    f"{conflict.id!r} overlap in {layout.id.value} layout"
                )
