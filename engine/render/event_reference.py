"""Explicit LaTeX projection of normative architectural-event code assignments."""

from __future__ import annotations

from dataclasses import dataclass
import re

from ..reference import Reference
from ..event import ArchitecturalEvent
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


def _identifier(value: str) -> str:
    escaped = tex_escape(value).replace(r"\_", r"\_\allowbreak{}")
    return rf"\texttt{{{escaped}}}"


@dataclass(frozen=True, slots=True)
class EventCodeRow:
    """One explicitly selected fixed event-code assignment."""

    reference: Reference[ArchitecturalEvent]
    code: int
    event_id: str


def _code(row: EventCodeRow) -> str:
    return rf"\texttt{{0x{row.code:08X}}}"


_EVENT_CODE_DIRECTIVE_OPEN = "(:event-code:"
_EVENT_CODE_DIRECTIVE_RE = re.compile(
    r"(?m)^[ \t]*\(:event-code:([A-Za-z0-9_.-]+):\)[ \t]*$"
)


class EventReferenceRenderer(DocumentFragmentProvider):
    """Render class metadata and explicitly placed fixed event-code rows."""

    CODE_REFERENCE_PLACEHOLDER = r"\BedrockGeneratedEventCodeReference"
    EVENT_CODE_ROW_PLACEHOLDER = _EVENT_CODE_DIRECTIVE_OPEN

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset(
            (self.CODE_REFERENCE_PLACEHOLDER, self.EVENT_CODE_ROW_PLACEHOLDER)
        )

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if self.CODE_REFERENCE_PLACEHOLDER in text:
            text = text.replace(
                self.CODE_REFERENCE_PLACEHOLDER,
                self.render_code_reference(context.project, context.public_targets),
            )
        matches = tuple(_EVENT_CODE_DIRECTIVE_RE.finditer(text))
        if text.count(_EVENT_CODE_DIRECTIVE_OPEN) != len(matches):
            raise ValueError(
                f"{context.source}: (:event-code:...:) must occupy a standalone line"
            )
        if not matches:
            return text

        placed: set[Reference[object]] = set()

        def replacement(match: re.Match[str]) -> str:
            reference = Reference.parse(match.group(1))
            try:
                row = self.project_row(context.project.events, reference)
            except (KeyError, ValueError) as error:
                raise ValueError(
                    f"{context.source}: cannot place architectural event "
                    f"{match.group(1)!r}"
                ) from error
            if reference in placed:
                raise ValueError(
                    f"{context.source}: duplicate event-code placement {reference}"
                )
            placed.add(reference)
            anchor = ""
            if context.public_targets.contains(reference):
                anchor = (
                    rf"\phantomsection\label{{{context.public_targets.label(reference)}}}"
                )
            return f"{_code(row)}{anchor} & {_identifier(row.event_id)}\\\\"

        return _EVENT_CODE_DIRECTIVE_RE.sub(replacement, text)

    @staticmethod
    def project_row(catalog, reference: Reference[object]) -> EventCodeRow:
        """Select the public row owned by one fixed architectural event."""

        resolved = next(
            (
                item
                for item in catalog.resolved_events()
                if item.event.reference == reference
            ),
            None,
        )
        if resolved is None:
            raise KeyError(reference)
        if resolved.code.value is None:
            raise ValueError(f"event {reference} has no fixed event-code assignment")
        return EventCodeRow(
            resolved.event.reference,
            resolved.code.value,
            resolved.event.id,
        )

    @staticmethod
    def event_target(event: ArchitecturalEvent) -> str:
        """Return the label owned by one public normative event row."""

        return f"event:{event.id.lower().replace('_', '-')}"

    @staticmethod
    def public_targets(
        project, referenced: frozenset[Reference[object]]
    ) -> tuple[tuple[Reference[object], str], ...]:
        """Declare targets owned by rows in the two normative event tables."""

        targets: list[tuple[Reference[object], str]] = []
        seen_classes = set()
        for namespace in project.events.namespaces.values():
            for event_class in namespace.classes.values():
                root = project.events.root_class(event_class)
                if root.reference in referenced and root.reference not in seen_classes:
                    targets.append(
                        (
                            root.reference,
                            f"event-class:{root.id.lower().replace('_', '-')}",
                        )
                    )
                    seen_classes.add(root.reference)
        targets.extend(
            (resolved.event.reference, EventReferenceRenderer.event_target(resolved.event))
            for resolved in project.events.resolved_events()
            if resolved.event.reference in referenced
        )
        return tuple(targets)

    def render_code_reference(self, project, public_targets) -> str:
        catalog = project.events
        classes = []
        seen = set()
        for namespace in catalog.namespaces.values():
            for event_class in namespace.classes.values():
                root = catalog.root_class(event_class)
                if root.reference in seen:
                    continue
                seen.add(root.reference)
                anchor = ""
                if public_targets.contains(root.reference):
                    anchor = rf"\phantomsection\label{{{public_targets.label(root.reference)}}}"
                classes.append(
                    rf"\texttt{{0x{root.value:02X}}}{anchor} & "
                    rf"{_identifier(root.id)} & "
                    rf"{tex_escape(root.name)} & "
                    rf"{tex_escape(root.selector.kind)} {root.selector.bits}-bit selector\\"
                )
        return "\n".join(
            [
                r"\begin{BedrockListedFormatDiagram}{Architectural Event Code}",
                r"\BedrockFormatRow{EVENT\_CODE[31:0]}{%",
                r"\BedrockFormatField{CLASS}{8}",
                r"\BedrockFormatField{SELECTOR}{24}",
                "}",
                r"\end{BedrockListedFormatDiagram}",
                "",
                r"\BedrockTableCaption{Architectural Event Classes}",
                r"\begin{BedrockTabular}{@{}>{\raggedright\arraybackslash}p{0.60in}>{\raggedright\arraybackslash}p{1.10in}>{\raggedright\arraybackslash}p{1.65in}>{\raggedright\arraybackslash}p{2.10in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Value} & \textbf{Class} & \textbf{Name} & \textbf{Selector policy}\\",
                r"\midrule",
                *classes,
                r"\bottomrule",
                r"\end{BedrockTabular}",
                "",
                r"Class values not listed above are reserved. Fixed selectors are assigned by this specification; platform and source selectors are supplied by the corresponding event source.",
            ]
        )
