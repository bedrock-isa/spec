"""Architectural instruction framing and opcode-class grammar."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType


ARCHITECTURE_SOURCE_PATH = Path(__file__).resolve()

EXTRASHORT_FRAMING_BITS = 1
SHORT_FRAMING_BITS = 2
EXTENDED_FRAMING_BITS = 6
EXTENDED_SELECTOR_BITS = 8
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
        return tuple(
            selector.replace("x", "?")
            + "?" * (self.allocation_bits - len(selector))
            for selector in self.selectors
        )


ENCODING_CLASSES = (
    EncodingClass("extrashort", 1, EXTRASHORT_FRAMING_BITS),
    EncodingClass("short", 2, SHORT_FRAMING_BITS),
    EncodingClass(
        "medium",
        3,
        EXTENDED_FRAMING_BITS,
        ("0xxxxxxx", "10xxxxxx", "110xxxxx", "1110xxxx"),
    ),
    EncodingClass("long", 4, EXTENDED_FRAMING_BITS, ("11110xxx", "111110xx")),
    EncodingClass("extralong", 5, EXTENDED_FRAMING_BITS, ("1111110x", "11111110")),
    EncodingClass("xxlong", 6, EXTENDED_FRAMING_BITS, ("11111111",)),
)
ENCODING_CLASSES_BY_NAME = MappingProxyType(
    {encoding_class.name: encoding_class for encoding_class in ENCODING_CLASSES}
)


OPERATOR_SPACE_PREFIX_BITS = 10


@dataclass(frozen=True)
class OperatorSpacePrefix:
    """A front-end allocation prefix that selects an operator space."""

    encoding_class: str
    pattern: str
    operator_space: str


OPERATOR_SPACE_PREFIXES = (
    OperatorSpacePrefix("extralong", "111111000?", "base"),
    OperatorSpacePrefix("extralong", "111111001?", "fpu"),
    OperatorSpacePrefix("extralong", "11111101??", "vector"),
    OperatorSpacePrefix("xxlong", "1111111100", "vector"),
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


def _pattern_is_subset(pattern: str, container: str) -> bool:
    """Return whether every value selected by pattern is selected by container."""
    return all(
        container_bit in "x?" or pattern_bit == container_bit
        for pattern_bit, container_bit in zip(pattern, container, strict=True)
    )


def _patterns_overlap(left: str, right: str) -> bool:
    return all(
        left_bit in "x?" or right_bit in "x?" or left_bit == right_bit
        for left_bit, right_bit in zip(left, right, strict=True)
    )


def operator_space_from_prefix(encoding_class: str, prefix: str) -> str | None:
    """Resolve a 10-bit front-end prefix to its instruction-set operator space.

    A valid but currently unallocated prefix returns ``None``. A prefix outside
    the named encoding class is rejected so identical bit text cannot be
    interpreted without its framing class.
    """
    architecture_class = ENCODING_CLASSES_BY_NAME.get(encoding_class)
    if architecture_class is None:
        raise ValueError(f"unknown encoding class {encoding_class!r}")
    if len(prefix) != OPERATOR_SPACE_PREFIX_BITS or set(prefix) - set("01x?"):
        raise ValueError(
            f"operator-space prefix must be {OPERATOR_SPACE_PREFIX_BITS} bits, "
            f"got {prefix!r}"
        )
    if not any(
        _pattern_is_subset(prefix[:EXTENDED_SELECTOR_BITS], selector)
        for selector in architecture_class.selectors
    ):
        raise ValueError(
            f"prefix {prefix!r} is outside the {encoding_class} selector grammar"
        )
    matches = [
        allocation.operator_space
        for allocation in OPERATOR_SPACE_PREFIXES
        if allocation.encoding_class == encoding_class
        and _pattern_is_subset(prefix, allocation.pattern)
    ]
    if len(matches) > 1:  # pragma: no cover - guarded by import-time validation
        raise ValueError(
            f"prefix {prefix!r} ambiguously selects operator spaces {matches}"
        )
    return matches[0] if matches else None


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
                    f"{encoding_class.name}: selector overlap at 0b{min(overlap):08b}"
                )
            claimed_selectors.update(values)
    if claimed_selectors != set(range(1 << EXTENDED_SELECTOR_BITS)):
        raise ValueError(
            "extended opcode selectors do not cover the eight-bit selector space"
        )
    for index, allocation in enumerate(OPERATOR_SPACE_PREFIXES):
        encoding_class = ENCODING_CLASSES_BY_NAME.get(allocation.encoding_class)
        if encoding_class is None:
            raise ValueError(
                f"operator space references unknown class {allocation.encoding_class!r}"
            )
        if (
            len(allocation.pattern) != OPERATOR_SPACE_PREFIX_BITS
            or set(allocation.pattern) - set("01x?")
        ):
            raise ValueError(
                f"{allocation.encoding_class}: invalid operator-space prefix "
                f"{allocation.pattern!r}"
            )
        if not any(
            _pattern_is_subset(
                allocation.pattern[:EXTENDED_SELECTOR_BITS], selector
            )
            for selector in encoding_class.selectors
        ):
            raise ValueError(
                f"operator-space prefix {allocation.pattern!r} is outside the "
                f"{allocation.encoding_class} selector grammar"
            )
        for previous in OPERATOR_SPACE_PREFIXES[:index]:
            if (
                previous.encoding_class == allocation.encoding_class
                and _patterns_overlap(previous.pattern, allocation.pattern)
            ):
                raise ValueError(
                    f"{allocation.encoding_class}: overlapping operator-space "
                    f"prefixes {previous.pattern!r} and {allocation.pattern!r}"
                )


_validate_architecture()
