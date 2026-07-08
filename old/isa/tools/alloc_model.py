"""Shared allocation data model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Field:
    name: str
    kind: str
    width: int
    source: str
    storage: str
    value: int | None = None
    value_label: str = ""
    placement: str = ""


@dataclass(frozen=True)
class Candidate:
    id: str
    mnemonic: str
    category: str
    group: str
    extension_family: str
    operands: tuple[str, ...]
    origin: str
    compact_fields: tuple[Field, ...]
    descriptor_fields: tuple[Field, ...]
    compact_bits: int
    compact_slots: int | None
    descriptor_bits: int
    descriptor_words: int
    weight: int
    must_compact: bool
    can_extend: bool
    fixed_payload: int | None
    shape_hint: str
    min_words: int
    max_words: int
    allow_memory_memory: bool
    fixed_size_suffix: str
    privilege: str
    allocation_cluster: str


@dataclass(frozen=True)
class OpcodeSpace:
    id: str
    bits: int

    @property
    def slots(self) -> int:
        return 1 << self.bits


@dataclass(frozen=True)
class SemanticSection:
    path: str
    category: str
    default_weight: int


@dataclass(frozen=True)
class AllocationModel:
    primary: OpcodeSpace
    extended: OpcodeSpace
    primary_extension_headroom_slots: int
    high_primary_payload_start: int
    semantic_sections: tuple[SemanticSection, ...]
    compact_exclude: tuple[str, ...]
    compact_prefer: tuple[str, ...]
    extension_family_rank: dict[str, int]
    extension_profile_rank: dict[str, dict[str, int]]
    extension_member_rank: dict[str, dict[str, int]]


def allocation_model(spec: dict[str, Any]) -> AllocationModel:
    opcodes = spec.get("opcodes") or {}
    instructions = spec.get("instructions") or {}
    allocation = instructions.get("allocation") or {}
    spaces = opcodes.get("opcode_spaces") or {}
    primary_space = spaces.get("primary") or {}
    extended_space = spaces.get("extended") or {}
    compactness = allocation.get("compactness_policy") or {}

    primary_bits = bit_range_width(((opcodes.get("word0") or {}).get("payload") or {}).get("bits"))
    primary = OpcodeSpace(id=str(primary_space["id"]), bits=primary_bits)
    extended = OpcodeSpace(id=str(extended_space["id"]), bits=int(extended_space["bits"]))

    high_region = primary_space.get("extension_root_region") or {}
    start_fraction = high_region.get("start_fraction") or [0, 1]
    if not isinstance(start_fraction, list) or len(start_fraction) != 2:
        raise ValueError("opcodes.opcode_spaces.primary.extension_root_region.start_fraction must be [numerator, denominator]")
    high_start = primary.slots * int(start_fraction[0]) // int(start_fraction[1])

    semantic_sections = tuple(
        SemanticSection(
            path=str(section["path"]),
            category=str(section["category"]),
            default_weight=int(section["default_weight"]),
        )
        for section in allocation.get("semantic_sections", []) or []
    )
    return AllocationModel(
        primary=primary,
        extended=extended,
        primary_extension_headroom_slots=int(primary_space["reserved_unallocated_headroom_slots"]),
        high_primary_payload_start=high_start,
        semantic_sections=semantic_sections,
        compact_exclude=tuple(str(item) for item in compactness.get("exclude", []) or []),
        compact_prefer=tuple(str(item) for item in compactness.get("prefer", []) or []),
        extension_family_rank=rank_map(allocation.get("extension_family_order", []) or []),
        extension_profile_rank={
            str(family): rank_map(profiles)
            for family, profiles in (allocation.get("extension_profile_order", {}) or {}).items()
            if isinstance(profiles, list)
        },
        extension_member_rank={
            str(family): rank_map(members)
            for family, members in (allocation.get("extension_member_order", {}) or {}).items()
            if isinstance(members, list)
        },
    )


def bit_range_width(value: Any) -> int:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("opcode payload bits must be a [high, low] range")
    high = int(value[0])
    low = int(value[1])
    return abs(high - low) + 1


def rank_map(values: list[Any]) -> dict[str, int]:
    return {str(value): index for index, value in enumerate(values)}

def profile_form_parts(fields: tuple[Field, ...]) -> list[str]:
    parts = []
    for field in fields:
        if field.source == "size" or field.kind == "condition":
            continue
        part = profile_part_for_field(field)
        if part:
            parts.append(part)
    return parts


def profile_part_for_field(field: Field) -> str:
    if field.kind == "EA":
        return "EA"
    if field.kind == "DREG":
        return "D"
    if field.kind == "DBANK":
        return "DB"
    if field.kind == "AREG":
        return "A"
    if field.kind == "SREG":
        return "S"
    if field.kind == "SPREG":
        return "SP"
    if field.kind == "FREG":
        return "F"
    if field.kind == "D_or_A":
        return "R"
    if field.kind == "selector6":
        return "I6"
    if field.kind == "small_selector":
        return "N"
    if field.kind == "memory_order":
        return ""
    if field.kind.endswith("bitmap16"):
        return "BITMAP"
    if "imm" in field.kind.lower():
        return "IMM"
    return ""


def size_tag_from_fields(fields: tuple[Field, ...]) -> str:
    for field in fields:
        if field.source == "size":
            return field.kind
    return ""


def profile_candidate_id(candidate: Candidate, fields: tuple[Field, ...]) -> str:
    parts = profile_form_parts(fields)
    ident = candidate.mnemonic if not parts else f"{candidate.mnemonic}.{ '_TO_'.join(parts) }"
    if candidate.id != ident and candidate.id.startswith(f"{candidate.mnemonic}."):
        return candidate.id
    return ident
