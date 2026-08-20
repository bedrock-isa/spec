"""Architectural instruction framing and opcode-class grammar."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType


ARCHITECTURE_SOURCE_PATH = Path(__file__).resolve()

EXTRASHORT_FRAMING_BITS = 1
SHORT_FRAMING_BITS = 2
EXTENDED_FRAMING_BITS = 6
EXTENDED_SELECTOR_BITS = 6
EXTENDED_LENGTH_BASE_BYTES = 3
EXTENDED_LENGTH_FIELD_BITS = 4
EXTRASHORT_BYTE0_PATTERN = "0xxxxxxx"
SHORT_BYTE0_PATTERN = "10xxxxxx"
EXTENDED_BYTE1_PATTERN = "bbbbxxxx"


@dataclass(frozen=True)
class EncodingClass:
    """One class in the fixed architectural opcode grammar."""

    name: str
    opcode_space_bytes: int
    framing_bits: int
    selectors: tuple[str, ...] = ()

    @property
    def allocation_bits(self) -> int:
        return self.opcode_space_bytes * 8 - self.framing_bits

    @property
    def namespace(self) -> tuple[str, ...]:
        if not self.selectors:
            return ("?" * self.allocation_bits,)
        suffix_bits = self.allocation_bits - EXTENDED_SELECTOR_BITS
        return tuple(
            selector.replace("x", "?") + "?" * suffix_bits
            for selector in self.selectors
        )


ENCODING_CLASSES = (
    EncodingClass("extrashort", 1, EXTRASHORT_FRAMING_BITS),
    EncodingClass("short", 2, SHORT_FRAMING_BITS),
    EncodingClass(
        "medium",
        3,
        EXTENDED_FRAMING_BITS,
        ("0xxxxx", "10xxxx", "110xxx", "1110xx"),
    ),
    EncodingClass("long", 4, EXTENDED_FRAMING_BITS, ("11110x", "111110")),
    EncodingClass("extralong", 5, EXTENDED_FRAMING_BITS, ("111111",)),
)
ENCODING_CLASSES_BY_NAME = MappingProxyType(
    {encoding_class.name: encoding_class for encoding_class in ENCODING_CLASSES}
)


def extended_instruction_lengths() -> range:
    return range(
        EXTENDED_LENGTH_BASE_BYTES,
        EXTENDED_LENGTH_BASE_BYTES + (1 << EXTENDED_LENGTH_FIELD_BITS),
    )


def extended_length_byte0_pattern(instruction_bytes: int) -> str:
    length_code = instruction_bytes - EXTENDED_LENGTH_BASE_BYTES
    if length_code not in range(1 << EXTENDED_LENGTH_FIELD_BITS):
        raise ValueError(
            f"extended instruction length must be 3..18, got {instruction_bytes}"
        )
    return f"11{length_code:04b}oo"


def extended_record_is_sufficient(required_bytes: int, record: bytes) -> bool:
    """Return the architectural length result; trailing byte values are ignored."""
    if required_bytes not in extended_instruction_lengths():
        raise ValueError(f"required extended bytes must be 3..18, got {required_bytes}")
    if len(record) not in extended_instruction_lengths():
        raise ValueError(f"encoded extended bytes must be 3..18, got {len(record)}")
    return len(record) >= required_bytes


def _selector_values(pattern: str) -> set[int]:
    values = {0}
    for char in pattern:
        if char in "x?":
            values = {value << 1 | bit for value in values for bit in (0, 1)}
        elif char in "01":
            values = {value << 1 | int(char) for value in values}
        else:  # pragma: no cover - guarded by import-time validation
            raise ValueError(f"invalid selector character {char!r}")
    return values


def _validate_architecture() -> None:
    if len(ENCODING_CLASSES_BY_NAME) != len(ENCODING_CLASSES):
        raise ValueError("duplicate encoding class name")
    claimed_selectors: set[int] = set()
    for encoding_class in ENCODING_CLASSES:
        if encoding_class.allocation_bits <= 0:
            raise ValueError(f"{encoding_class.name}: allocation width must be positive")
        for namespace in encoding_class.namespace:
            if len(namespace) != encoding_class.allocation_bits:
                raise ValueError(f"{encoding_class.name}: namespace width mismatch")
        for selector in encoding_class.selectors:
            if (
                len(selector) != EXTENDED_SELECTOR_BITS
                or set(selector) - set("01x?")
            ):
                raise ValueError(f"{encoding_class.name}: invalid selector {selector!r}")
            values = _selector_values(selector)
            overlap = claimed_selectors & values
            if overlap:
                raise ValueError(
                    f"{encoding_class.name}: selector overlap at 0b{min(overlap):06b}"
                )
            claimed_selectors.update(values)
    if claimed_selectors != set(range(1 << EXTENDED_SELECTOR_BITS)):
        raise ValueError(
            "extended opcode selectors do not cover the six-bit selector space"
        )


_validate_architecture()
