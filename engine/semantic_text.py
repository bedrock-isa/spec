"""Renderer-independent strings containing typed semantic references."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re

from .reference import Reference, ReferenceError


_ESCAPE_START_RE = re.compile(r"\(:([a-z][a-z0-9_-]*):")


class SemanticTextError(ValueError):
    """Raised when a semantic-text escape is malformed."""


class TermForm(StrEnum):
    """A registered presentation of one terminology entry."""

    CANONICAL = "canonical"
    PLURAL = "plural"
    ADJECTIVE = "adjective"
    SHORT = "short"
    FIRST = "first"


@dataclass(frozen=True, slots=True)
class TextOrigin:
    """The authored location from which a semantic string was loaded."""

    source: Path
    path: tuple[str | int, ...] = ()


@dataclass(frozen=True, slots=True)
class LiteralText:
    value: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class EntityReferenceText:
    reference: Reference
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class TermReferenceText:
    reference: Reference
    form: TermForm
    start: int
    end: int


SemanticTextPart = LiteralText | EntityReferenceText | TermReferenceText


@dataclass(frozen=True, slots=True)
class SemanticText:
    """An immutable parsed string using ``(:ref:...:)`` style escapes."""

    raw: str
    origin: TextOrigin
    parts: tuple[SemanticTextPart, ...]

    @classmethod
    def parse(cls, raw: str, *, origin: TextOrigin) -> "SemanticText":
        if not isinstance(raw, str):
            raise SemanticTextError("semantic text must be a string")
        parts: list[SemanticTextPart] = []
        cursor = 0
        while match := _ESCAPE_START_RE.search(raw, cursor):
            if match.start() > cursor:
                parts.append(
                    LiteralText(raw[cursor : match.start()], cursor, match.start())
                )
            end = raw.find(":)", match.end())
            if end < 0:
                raise _syntax_error(
                    origin, match.start(), "unterminated semantic escape"
                )
            kind = match.group(1)
            payload = raw[match.end() : end]
            escape_end = end + 2
            parts.append(
                _parse_escape(kind, payload, origin, match.start(), escape_end)
            )
            cursor = escape_end
        if cursor < len(raw) or not parts:
            parts.append(LiteralText(raw[cursor:], cursor, len(raw)))
        return cls(raw, origin, tuple(parts))

    @property
    def dependencies(self) -> tuple[Reference, ...]:
        return tuple(
            part.reference
            for part in self.parts
            if isinstance(part, (EntityReferenceText, TermReferenceText))
        )


def _parse_escape(
    kind: str,
    payload: str,
    origin: TextOrigin,
    start: int,
    end: int,
) -> SemanticTextPart:
    if kind not in {"ref", "term"}:
        raise _syntax_error(origin, start, f"unknown semantic escape kind {kind!r}")
    pieces = payload.split("|")
    if not pieces[0] or len(pieces) > 2:
        raise _syntax_error(origin, start, f"invalid {kind} escape payload")
    try:
        reference = Reference.parse(pieces[0])
    except ReferenceError as error:
        raise _syntax_error(origin, start, str(error)) from error
    if kind == "ref":
        if len(pieces) != 1:
            raise _syntax_error(origin, start, "ref escapes do not accept a modifier")
        return EntityReferenceText(reference, start, end)
    raw_form = pieces[1] if len(pieces) == 2 else TermForm.CANONICAL.value
    try:
        form = TermForm(raw_form)
    except ValueError as error:
        raise _syntax_error(origin, start, f"unknown term form {raw_form!r}") from error
    return TermReferenceText(reference, form, start, end)


def _syntax_error(origin: TextOrigin, offset: int, message: str) -> SemanticTextError:
    location = ".".join(map(str, origin.path))
    where = f" at {location}" if location else ""
    return SemanticTextError(f"{origin.source}{where}, offset {offset}: {message}")
