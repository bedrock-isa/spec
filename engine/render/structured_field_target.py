"""Explicit public-target placement for owner-specific structured fields."""

from __future__ import annotations

from pathlib import Path
import re

from ..cpuid import CpuidField
from ..debug_trigger import DebugTriggerField, DebugTriggerWord
from ..entity import Entity
from ..event_structure import (
    EventFrameField,
    EventFrameSlot,
    EventPayloadField,
)
from ..instruction_header import InstructionHeaderField
from ..reference import Reference, UnknownReferenceError
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


class _ExplicitTargetRenderer(DocumentFragmentProvider):
    target_open: str
    target_re: re.Pattern[str]
    entity_types: tuple[type[Entity], ...]
    label_prefix: str
    description: str

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.target_open,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        matches = tuple(self.target_re.finditer(text))
        if text.count(self.target_open) != len(matches):
            raise ValueError(
                f"{context.source}: malformed {self.description} target directive"
            )

        def replacement(match: re.Match[str]) -> str:
            reference = Reference.parse(match.group(1))
            self._require_entity_type(
                context.project, reference, context.source
            )
            return (
                rf"\phantomsection\label{{"
                rf"{context.public_targets.label(reference)}}}"
            )

        return self.target_re.sub(replacement, text)

    @classmethod
    def public_targets(
        cls, project, sources: tuple[Path, ...]
    ) -> tuple[tuple[Reference[object], str], ...]:
        targets: list[tuple[Reference[object], str]] = []
        placed: dict[Reference[object], Path] = {}
        for source in sources:
            if source.suffix == ".sty":
                continue
            text = source.read_text(encoding="utf-8")
            matches = tuple(cls.target_re.finditer(text))
            if text.count(cls.target_open) != len(matches):
                raise ValueError(
                    f"{source}: malformed {cls.description} target directive"
                )
            for match in matches:
                reference = Reference.parse(match.group(1))
                cls._require_entity_type(project, reference, source)
                previous = placed.get(reference)
                if previous is not None:
                    raise ValueError(
                        f"{source}: duplicate public {cls.description} target "
                        f"{match.group(1)!r}; first placed by {previous}"
                    )
                placed[reference] = source
                slug = re.sub(
                    r"[^a-z0-9]+",
                    "-",
                    ".".join(
                        (reference.owner, *reference.path, reference.element)
                    ).lower(),
                ).strip("-")
                targets.append((reference, f"{cls.label_prefix}:{slug}"))
        return tuple(targets)

    @classmethod
    def _require_entity_type(
        cls, project, reference, source: Path | None
    ) -> None:
        try:
            entity = project.entities.resolve(reference)
        except UnknownReferenceError as error:
            raise ValueError(
                f"{source}: unknown {cls.description} target reference"
            ) from error
        if not isinstance(entity, cls.entity_types):
            raise ValueError(
                f"{source}: {cls.description} target resolves to "
                f"{type(entity).__name__}"
            )


class DebugTriggerTargetRenderer(_ExplicitTargetRenderer):
    target_open = "(:debug-trigger-target:"
    target_re = re.compile(r"\(:debug-trigger-target:([A-Za-z0-9_.-]+):\)")
    entity_types = (DebugTriggerWord, DebugTriggerField)
    label_prefix = "debug-trigger"
    description = "debug-trigger"


class EventStructureTargetRenderer(_ExplicitTargetRenderer):
    target_open = "(:event-structure-target:"
    target_re = re.compile(r"\(:event-structure-target:([A-Za-z0-9_.-]+):\)")
    entity_types = (
        EventFrameSlot,
        EventFrameField,
        EventPayloadField,
    )
    label_prefix = "event-structure"
    description = "event-structure"


class InstructionHeaderFieldTargetRenderer(_ExplicitTargetRenderer):
    target_open = "(:instruction-header-field-target:"
    target_re = re.compile(
        r"\(:instruction-header-field-target:([A-Za-z0-9_.-]+):\)"
    )
    entity_types = (InstructionHeaderField,)
    label_prefix = "instruction-header-field"
    description = "instruction-header field"


class CpuidFieldTargetRenderer(_ExplicitTargetRenderer):
    target_open = "(:cpuid-field-target:"
    target_re = re.compile(r"\(:cpuid-field-target:([A-Za-z0-9_.-]+):\)")
    entity_types = (CpuidField,)
    label_prefix = "cpuid-field"
    description = "CPUID field"
