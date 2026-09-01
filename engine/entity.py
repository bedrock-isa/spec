"""Common entity contract and unified logical-reference catalogs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re
from types import MappingProxyType
from typing import Iterable, Mapping, cast

from .reference import Reference, ReferenceIndex


class EntityDisplayStyle(StrEnum):
    TEXT = "text"
    CODE = "code"


class Entity:
    """Nominal parent of every provider-local referencable domain object."""

    __slots__ = ()

    reference: Reference["Entity"]
    source: Path


@dataclass(frozen=True, slots=True)
class EntityPresentation:
    """Provider-owned default spelling used by explicit public projections."""

    display: str
    display_style: EntityDisplayStyle = EntityDisplayStyle.TEXT


@dataclass(frozen=True, slots=True)
class EntityCatalog:
    references: ReferenceIndex[Entity]
    presentations: Mapping[Reference[Entity], EntityPresentation]

    @classmethod
    def create(
        cls,
        entries: Iterable[
            tuple[Entity, str, EntityDisplayStyle]
            | tuple[Entity, str]
        ],
    ) -> "EntityCatalog":
        references = ReferenceIndex[Entity]()
        presentations: dict[Reference[Entity], EntityPresentation] = {}
        for entry in entries:
            entity, display = entry[:2]
            style = (
                entry[2]
                if len(entry) == 3
                else EntityDisplayStyle.TEXT
            )
            if not isinstance(entity, Entity):
                raise TypeError("entity catalog entries must inherit Entity")
            if not isinstance(entity.reference, Reference):
                raise TypeError("entity reference must be a Reference")
            if not isinstance(entity.source, Path):
                raise TypeError("entity source must be a Path")
            reference = cast(Reference[Entity], entity.reference)
            references.register(reference, entity)
            presentations[reference] = EntityPresentation(display, style)
        return cls(references, MappingProxyType(presentations))

    def resolve(self, reference: Reference[Entity]) -> Entity:
        return self.references.resolve(reference)

    def presentation(
        self, reference: Reference[object]
    ) -> EntityPresentation:
        normalized = cast(Reference[Entity], reference)
        self.resolve(normalized)
        return self.presentations[normalized]


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
