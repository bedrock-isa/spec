"""Owner-local EA encoding and address-flow diagrams for the ISA reference."""

from __future__ import annotations

from dataclasses import dataclass
import re

from ..generate_ea_diagrams import (
    EAModeDiagramProjection,
    project_mode,
    render_mode,
)
from ..reference import Reference, ReferenceError, UnknownReferenceError
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


_DIRECTIVE_OPEN = "(:ea-diagram:"
_DIRECTIVE_RE = re.compile(
    r"(?m)^[ \t]*\(:ea-diagram:([A-Za-z0-9_.-]+):\)[ \t]*$"
)


@dataclass(frozen=True, slots=True)
class EaDiagramProjection:
    """One owner-local EA mode selected for a reader-facing diagram."""

    diagram: EAModeDiagramProjection


class EaDiagramFragmentRenderer(DocumentFragmentProvider):
    """Expand explicit EA diagrams in the topic owned by the same namespace."""

    PLACEHOLDER = _DIRECTIVE_OPEN

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        matches = tuple(_DIRECTIVE_RE.finditer(text))
        if text.count(_DIRECTIVE_OPEN) != len(matches):
            raise ValueError(
                f"{context.source}: (:ea-diagram:...:) must occupy a standalone line"
            )
        if not matches:
            return text

        placed: list[Reference[object]] = []

        def replacement(match: re.Match[str]) -> str:
            projection = self.project(context, match.group(1))
            reference = projection.diagram.reference
            if reference in placed:
                raise ValueError(
                    f"{context.source}: duplicate EA diagram {match.group(1)!r}"
                )
            placed.append(reference)
            return render_mode(projection.diagram)

        return _DIRECTIVE_RE.sub(replacement, text)

    @staticmethod
    def project(context: DocumentFragmentContext, raw_reference: str) -> EaDiagramProjection:
        """Resolve one EA diagram placement against its owning topic."""

        source = context.source.resolve() if context.source is not None else None
        topics = tuple(
            topic
            for topic in context.project.model.document_topics.values()
            if source is not None and topic.document.resolve() == source
        )
        if len(topics) != 1:
            raise ValueError(f"{context.source}: EA diagram placement requires one topic owner")
        try:
            reference = Reference.parse(raw_reference)
            mode = context.project.catalog.ea_modes.resolve(reference)
        except (ReferenceError, UnknownReferenceError) as error:
            raise ValueError(
                f"{context.source}: unknown EA diagram {raw_reference!r}"
            ) from error
        if reference.owner != topics[0].owner:
            raise ValueError(
                f"{context.source}: EA mode owner {reference.owner!r} does not "
                f"match topic owner {topics[0].owner!r}"
            )
        return EaDiagramProjection(project_mode(mode))
