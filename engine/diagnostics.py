"""Structured diagnostics shared by ISA authoring commands."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    NOTE = "note"


@dataclass(frozen=True, slots=True)
class RelatedLocation:
    source: Path
    message: str
    path: tuple[str | int, ...] = ()


@dataclass(frozen=True, slots=True)
class Diagnostic:
    severity: Severity
    code: str
    source: Path
    message: str
    path: tuple[str | int, ...] = ()
    related: tuple[RelatedLocation, ...] = ()

    def location(self) -> str:
        suffix = "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}" for part in self.path
        )
        return f"{self.source}{suffix}"


class DiagnosticBag(Sequence[Diagnostic]):
    """An ordered collection that can be rendered for people or automation."""

    def __init__(self, diagnostics: Iterable[Diagnostic] = ()) -> None:
        self._diagnostics = list(diagnostics)

    def add(self, diagnostic: Diagnostic) -> None:
        self._diagnostics.append(diagnostic)

    def extend(self, diagnostics: Iterable[Diagnostic]) -> None:
        self._diagnostics.extend(diagnostics)

    @property
    def has_errors(self) -> bool:
        return any(item.severity is Severity.ERROR for item in self._diagnostics)

    def render_text(self) -> str:
        blocks: list[str] = []
        for item in self._diagnostics:
            lines = [
                f"{item.location()}: {item.severity.value}[{item.code}]: {item.message}"
            ]
            lines.extend(
                f"  related: {related.source}: {related.message}"
                for related in item.related
            )
            blocks.append("\n".join(lines))
        return "\n".join(blocks)

    def render_json(self) -> str:
        return json.dumps(
            [
                {
                    "severity": item.severity.value,
                    "code": item.code,
                    "source": str(item.source),
                    "path": list(item.path),
                    "message": item.message,
                    "related": [
                        {
                            "source": str(related.source),
                            "path": list(related.path),
                            "message": related.message,
                        }
                        for related in item.related
                    ],
                }
                for item in self._diagnostics
            ],
            indent=2,
            sort_keys=True,
        )

    def __getitem__(self, index: int | slice) -> Diagnostic | list[Diagnostic]:
        return self._diagnostics[index]

    def __iter__(self) -> Iterator[Diagnostic]:
        return iter(self._diagnostics)

    def __len__(self) -> int:
        return len(self._diagnostics)
