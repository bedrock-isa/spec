"""Authored reservations within architectural opcode spaces."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from .inventory import DirectoryInventory
from .yaml_document import SchemaValidatedYamlLoader


class EncodingReservationInventory(DirectoryInventory):
    """The closed-world base-architecture reservation inventory."""


@dataclass(frozen=True, slots=True)
class EncodingReservationRegion:
    """One encoding-class prefix owned by a reservation purpose."""

    encoding_class: str
    prefix: str


@dataclass(frozen=True, slots=True)
class EncodingReservation:
    """One purpose that withholds one or more opcode regions."""

    source: Path
    root: Path
    id: str
    summary: str
    regions: tuple[EncodingReservationRegion, ...]


@dataclass(frozen=True, slots=True)
class EncodingReservationCatalog:
    """All opcode reservations owned by the base encoding architecture."""

    inventory: EncodingReservationInventory
    reservations: Mapping[str, EncodingReservation]

    @classmethod
    def load(cls, isa_root: str | Path) -> "EncodingReservationCatalog":
        root = Path(isa_root).resolve()
        reservations_root = root / "encoding/reservations"
        inventory = _load_inventory(reservations_root)
        reservations: dict[str, EncodingReservation] = {}
        for reservation_id in inventory.declared:
            member_root = reservations_root / reservation_id
            if reservation_id in reservations or not member_root.is_dir():
                continue
            reservation = _load_reservation(member_root, root)
            reservations[reservation_id] = reservation
        return cls(inventory, MappingProxyType(reservations))


def _load_inventory(root: Path) -> EncodingReservationInventory:
    return EncodingReservationInventory.inspect(
        owner="base",
        kind="reservation",
        source=root / "reservations.yaml",
        root=root,
        key="reservations",
        allow_missing=True,
        exact_keys=True,
    )


def _load_reservation(root: Path, isa_root: Path) -> EncodingReservation:
    source = root / "reservation.yaml"
    raw = SchemaValidatedYamlLoader().load(
        source, isa_root / "schemas/encoding-reservation.yaml"
    )
    reservation_id = raw["id"]
    if reservation_id != root.name:
        raise ValueError(
            f"{source}: encoding-reservation ID {reservation_id!r} does not match "
            f"directory {root.name!r}"
        )
    return EncodingReservation(
        source=source,
        root=root,
        id=reservation_id,
        summary=raw["summary"],
        regions=tuple(
            EncodingReservationRegion(
                encoding_class=region["encoding_class"],
                prefix=region["prefix"],
            )
            for region in raw["regions"]
        ),
    )
