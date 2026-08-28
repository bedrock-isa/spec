"""Logical references shared by ISA definition formats."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
import re
from typing import Generic, TypeVar


_OWNER_RE = re.compile(r"base|[A-Z][A-Z0-9_]*")
_SEGMENT_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
_DOMAIN_RE = re.compile(r"[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*")
_T = TypeVar("_T")


class ReferenceError(ValueError):
    """Base class for invalid logical reference operations."""


class DuplicateReferenceError(ReferenceError):
    """Raised when an index receives the same logical reference twice."""


class UnknownReferenceError(ReferenceError):
    """Raised when an index cannot resolve a logical reference."""


@dataclass(frozen=True, order=True, slots=True)
class Reference:
    """A ``<owner>(.<path>)*.<element>`` logical reference."""

    owner: str
    path: tuple[str, ...]
    element: str

    def __post_init__(self) -> None:
        if not isinstance(self.owner, str) or not _OWNER_RE.fullmatch(self.owner):
            raise ReferenceError(
                "reference owner must be 'base' or an uppercase extension ID"
            )
        if not isinstance(self.path, tuple):
            object.__setattr__(self, "path", tuple(self.path))
        for segment in (*self.path, self.element):
            if not isinstance(segment, str) or not _SEGMENT_RE.fullmatch(segment):
                raise ReferenceError(f"invalid reference segment {segment!r}")

    @classmethod
    def parse(cls, value: str | "Reference") -> "Reference":
        """Parse a dotted reference, returning existing references unchanged."""

        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise ReferenceError("reference must be a string")
        parts = value.split(".")
        if len(parts) < 2:
            raise ReferenceError("reference must contain an owner and an element")
        return cls(owner=parts[0], path=tuple(parts[1:-1]), element=parts[-1])

    def __str__(self) -> str:
        return ".".join((self.owner, *self.path, self.element))


@dataclass(frozen=True, order=True, slots=True)
class QualifiedReference:
    """A workspace domain paired with one provider-local reference."""

    domain: str
    local: Reference

    def __post_init__(self) -> None:
        if not isinstance(self.domain, str) or not _DOMAIN_RE.fullmatch(self.domain):
            raise ReferenceError(
                "reference domain must be a lowercase dotted identifier"
            )
        if not isinstance(self.local, Reference):
            object.__setattr__(self, "local", Reference.parse(self.local))

    @classmethod
    def parse(
        cls,
        value: str | "QualifiedReference",
        *,
        current_domain: str | None = None,
    ) -> "QualifiedReference":
        """Parse ``<domain>:<local>`` or qualify a local reference in context."""

        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise ReferenceError("qualified reference must be a string")
        if ":" in value:
            domain, local = value.split(":", 1)
        else:
            if current_domain is None:
                raise ReferenceError(
                    "local reference requires an explicit current domain"
                )
            domain, local = current_domain, value
        if not domain or not local or ":" in local:
            raise ReferenceError(f"invalid qualified reference {value!r}")
        return cls(domain, Reference.parse(local))

    def __str__(self) -> str:
        return f"{self.domain}:{self.local}"


class ReferenceIndex(Mapping[Reference, _T], Generic[_T]):
    """A filesystem-independent mapping from logical references to values."""

    def __init__(self) -> None:
        self._entries: dict[Reference, _T] = {}

    def register(self, reference: str | Reference, value: _T) -> Reference:
        """Register ``value`` and return its normalized reference."""

        normalized = Reference.parse(reference)
        if normalized in self._entries:
            raise DuplicateReferenceError(f"duplicate reference {normalized}")
        self._entries[normalized] = value
        return normalized

    def resolve(self, reference: str | Reference) -> _T:
        """Resolve a logical reference or raise ``UnknownReferenceError``."""

        normalized = Reference.parse(reference)
        try:
            return self._entries[normalized]
        except KeyError as error:
            raise UnknownReferenceError(f"unknown reference {normalized}") from error

    def __getitem__(self, reference: str | Reference) -> _T:
        return self.resolve(reference)

    def __contains__(self, reference: object) -> bool:
        if not isinstance(reference, (str, Reference)):
            return False
        try:
            normalized = Reference.parse(reference)
        except ReferenceError:
            return False
        return normalized in self._entries

    def __iter__(self) -> Iterator[Reference]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
