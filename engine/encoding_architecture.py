"""Architectural opcode classes and named operator-space partitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EncodingClass:
    """One allocation namespace in the instruction framing grammar."""

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


@dataclass(frozen=True, slots=True)
class OperatorSpace:
    """A named prefix partition within one encoding class."""

    encoding_class: str
    name: str
    prefix: str


ENCODING_CLASSES = (
    EncodingClass("extrashort", 1, 1),
    EncodingClass("short", 2, 2),
    EncodingClass(
        "medium",
        3,
        6,
        ("0xxxxxxx", "10xxxxxx", "110xxxxx", "1110xxxx"),
    ),
    EncodingClass("long", 4, 6, ("11110xxx", "111110xx")),
    EncodingClass("extralong", 5, 6, ("1111110x", "11111110")),
    EncodingClass("xxlong", 6, 6, ("11111111",)),
)
ENCODING_CLASSES_BY_NAME = {item.name: item for item in ENCODING_CLASSES}
ENCODING_CLASSES_BY_WIDTH = {item.allocation_bits: item for item in ENCODING_CLASSES}

OPERATOR_SPACES = (
    OperatorSpace("extralong", "base", "111111000?"),
    OperatorSpace("extralong", "fpu", "111111001?"),
    OperatorSpace("extralong", "vector", "11111101??"),
    OperatorSpace("xxlong", "vector", "1111111100"),
)

OPERATOR_SPACE_PREFIX_BITS = 10


def encoding_class(value: str) -> EncodingClass:
    """Resolve an encoding class by its architectural name."""

    result = ENCODING_CLASSES_BY_NAME.get(value)
    if result is None:
        names = ", ".join(item.name for item in ENCODING_CLASSES)
        raise ValueError(f"unknown encoding class {value!r}; choose one of: {names}")
    return result


def operator_space(class_name: str, name: str) -> OperatorSpace:
    """Resolve a named operator space scoped by encoding class."""

    result = next(
        (
            item
            for item in OPERATOR_SPACES
            if item.encoding_class == class_name and item.name == name
        ),
        None,
    )
    if result is None:
        available = sorted(
            item.name for item in OPERATOR_SPACES if item.encoding_class == class_name
        )
        suffix = f"; choose one of: {', '.join(available)}" if available else ""
        raise ValueError(
            f"encoding class {class_name!r} has no operator space {name!r}{suffix}"
        )
    return result


def _patterns_overlap(left: str, right: str) -> bool:
    return all(
        a == "?" or b == "?" or a == b
        for a, b in zip(left.replace("x", "?"), right.replace("x", "?"), strict=True)
    )


def _pattern_subset(pattern: str, container: str) -> bool:
    return all(
        outer in "x?" or inner == outer
        for inner, outer in zip(pattern, container, strict=True)
    )


def _validate() -> None:
    if len(ENCODING_CLASSES_BY_NAME) != len(ENCODING_CLASSES):
        raise ValueError("duplicate encoding class name")
    if len(ENCODING_CLASSES_BY_WIDTH) != len(ENCODING_CLASSES):
        raise ValueError("duplicate encoding class width")
    for item in ENCODING_CLASSES:
        if any(len(pattern) != item.allocation_bits for pattern in item.namespace):
            raise ValueError(f"{item.name}: namespace width mismatch")
    for index, space in enumerate(OPERATOR_SPACES):
        owner = encoding_class(space.encoding_class)
        pattern = space.prefix.replace("x", "?") + "?" * (
            owner.allocation_bits - len(space.prefix)
        )
        if len(space.prefix) > owner.allocation_bits or set(space.prefix) - set("01x?"):
            raise ValueError(f"{space.name}: invalid operator-space prefix")
        if not any(_pattern_subset(pattern, namespace) for namespace in owner.namespace):
            raise ValueError(f"{space.name}: prefix is outside {owner.name}")
        for previous in OPERATOR_SPACES[:index]:
            if (
                previous.encoding_class == space.encoding_class
                and _patterns_overlap(previous.prefix, space.prefix)
            ):
                raise ValueError(f"overlapping operator spaces: {previous}, {space}")


_validate()
