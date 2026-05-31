"""Shared allocation data model and constants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PRIMARY_SPACE_ID = "PRIMARY_PAYLOAD"
PRIMARY_BITS = 12
PRIMARY_SLOTS = 1 << PRIMARY_BITS
EXTENDED_SPACE_ID = "EXTENDED_OPCODE_WORD"
EXTENDED_BITS = 16
EXTENDED_SLOTS = 1 << EXTENDED_BITS
PRIMARY_EXTENSION_HEADROOM_SLOTS = 64
F_REGISTER_BITS = 5
HIGH_PRIMARY_PAYLOAD_START = PRIMARY_SLOTS * 7 // 8

SEMANTIC_SECTIONS = (
    ("integer_instructions", "integer", 70),
    ("atomic_system_cache_instructions", "system", 55),
    ("fpu.instructions", "fpu", 45),
)

TRANSCENDENTAL_FPU = {
    "FSIN",
    "FCOS",
    "FSINCOS",
    "FTAN",
    "FASIN",
    "FACOS",
    "FATAN",
    "FSINH",
    "FCOSH",
    "FTANH",
    "FATANH",
    "FLOGN",
    "FLOGNP1",
    "FLOG2",
    "FLOG10",
    "FETOX",
    "FETOXM1",
    "FTWOTOX",
    "FTENTOX",
}

DEFAULT_COMPACT_EXCLUDE = (
    "FPU",
    "cache_management",
    "tlb_management",
    "system_core_except_core_control",
    "transcendental_fpu",
)

DEFAULT_COMPACT_PREFER = (
    "D_D_integer_alu",
    "MOV_LQ_EA_D",
    "MOV_LQ_D_EA",
    "INC_DEC_D",
    "PUSH_POP",
    "Jcc",
    "CALL",
    "RET",
    "NOP",
    "SYSCALL",
    "BKPT",
    "WAIT",
    "YIELD",
    "fences",
)

CORE_CONTROL_COMPACT_MNEMONICS = {
    "RESET",
    "SYSRET",
    "IRET",
    "NOP",
    "SYSCALL",
    "BKPT",
    "WAIT",
    "YIELD",
    "RFENCE",
    "WFENCE",
    "AFENCE",
}

CACHE_MANAGEMENT_MNEMONICS = {
    "PREFETCH",
    "INVDCACHE",
    "INVICACHE",
    "FLSHDCACHE",
    "WRBKDCACHE",
    "SYNCCACHE",
}

TLB_MANAGEMENT_MNEMONICS = {
    "SWPT",
    "SWPTA",
    "VTOP",
    "PTATTR",
    "PTQUERY",
    "INVTLB",
    "INVPAGE",
    "INVASID",
}

FENCE_MNEMONICS = {"RFENCE", "WFENCE", "AFENCE"}

INTEGER_MINMAX_MNEMONICS = {"MINU", "MINS", "MAXU", "MAXS"}
INTEGER_MINMAX_ORDER = ("MINU", "MINS", "MAXU", "MAXS")
INTEGER_MUL_DIV_COMPACT_MNEMONICS = {"MULU", "MULS", "DIVU", "DIVS", "MODU", "MODS"}
INTEGER_MUL_DIV_COMPACT_ORDER = ("MULU", "MULS", "DIVU", "DIVS", "MODU", "MODS")

EXTENSION_FAMILY_RANK = {
    "integer_alu": 0,
    "integer_bounds": 1,
    "integer_mul_div": 2,
    "integer_mac": 3,
    "integer_bitfield": 4,
    "data_movement": 5,
    "ea_utility": 6,
    "control_flow": 7,
    "conditional_control": 8,
    "atomic_memory": 9,
    "cache_hint": 10,
    "tlb_cache": 11,
    "system_core": 12,
    "fpu_move_compare": 13,
    "fpu_arithmetic": 14,
    "fpu_transcendental": 15,
    "misc": 16,
}

EXTENSION_PROFILE_RANK = {
    "integer_alu": {
        "EA_TO_D": 0,
        "EA_TO_A": 1,
        "D_TO_EA": 3,
    }
}


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
    if field.kind == "IMM_EA":
        return "IMM"
    if field.kind == "DREG":
        return "D"
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
    if field.kind == "small_selector":
        return "N"
    if field.kind == "memory_order":
        return ""
    if field.kind == "bitmap16":
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
    tag = size_tag_from_fields(fields)
    if candidate.shape_hint == "declared_extended_form" and tag and tag not in {"Q", "LQ"}:
        ident = f"{ident}.{tag}"
    elif not tag and candidate.fixed_size_suffix:
        ident = f"{ident}.{candidate.fixed_size_suffix}"
    return ident


def default_field_layout_policy() -> dict[str, Any]:
    return {
        "field_score": {
            "formula": "candidate_weight_times_field_width",
            "default_multiplier": 1,
            "signature_multipliers": {"default": 1},
        },
        "subfield_affinities": [],
    }
