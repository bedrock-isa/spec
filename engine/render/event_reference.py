"""Registry-backed LaTeX renderers for architectural-event references."""

from __future__ import annotations

from ..event import ArchitecturalEvent, ResolvedEvent
from ..entity import entity_label
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


def _identifier(value: str) -> str:
    escaped = tex_escape(value).replace(r"\_", r"\_\allowbreak{}")
    return rf"\texttt{{{escaped}}}"


def _code(resolved: ResolvedEvent) -> str:
    if resolved.code.value is not None:
        return rf"\texttt{{0x{resolved.code.value:08X}}}"
    return (
        rf"\texttt{{0x{resolved.code.class_value:02X}:"
        rf"{tex_escape(resolved.code.selector.kind)}}}"
    )


def _payload(event: ArchitecturalEvent) -> str:
    if not event.payload:
        return "none"
    return ", ".join(_identifier(item) for item in event.payload)


class EventReferenceRenderer(DocumentFragmentProvider):
    """Render the event tables whose facts are wholly owned by EventCatalog."""

    PLACEHOLDERS = {
        r"\BedrockGeneratedEventCodeReference": "render_code_reference",
        r"\BedrockGeneratedArchitecturalEvents": "render_event_contracts",
        r"\BedrockGeneratedArchitecturalEventIndex": "render_index",
    }

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset(self.PLACEHOLDERS)

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        for placeholder, method_name in self.PLACEHOLDERS.items():
            replacement = getattr(self, method_name)(context.project.events)
            text = text.replace(placeholder, replacement)
        return text

    def render_code_reference(self, catalog) -> str:
        classes = []
        seen = set()
        for namespace in catalog.namespaces.values():
            for event_class in namespace.classes.values():
                root = catalog.root_class(event_class)
                if root.reference in seen:
                    continue
                seen.add(root.reference)
                assert root.value is not None and root.selector is not None
                classes.append(
                    rf"\phantomsection\label{{{entity_label(root.reference)}}}"
                    rf"\texttt{{0x{root.value:02X}}} & {_identifier(root.id)} & "
                    rf"{tex_escape(root.name or root.id)} & "
                    rf"{tex_escape(root.selector.kind)} {root.selector.bits}-bit selector\\"
                )
        return "\n".join(
            [
                r"\begin{manuallistedformatdiagram}{Architectural Event Code}",
                r"\manualformatrow{EVENT\_CODE[31:0]}{%",
                r"\manualformatfield{CLASS}{8}",
                r"\manualformatfield{SELECTOR}{24}",
                "}",
                r"\end{manuallistedformatdiagram}",
                "",
                r"\manualtablecaption{Architectural Event Classes}",
                r"\begin{manualtabular}{@{}>{\raggedright\arraybackslash}p{0.60in}>{\raggedright\arraybackslash}p{1.10in}>{\raggedright\arraybackslash}p{1.65in}>{\raggedright\arraybackslash}p{2.10in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Value} & \textbf{Class} & \textbf{Name} & \textbf{Selector policy}\\",
                r"\midrule",
                *classes,
                r"\bottomrule",
                r"\end{manualtabular}",
                "",
                r"Class values not listed above are reserved. Fixed selectors are allocated by this specification; platform and source selectors are supplied by the corresponding event source.",
            ]
        )

    def render_event_contracts(self, catalog) -> str:
        rows = []
        for resolved in catalog.resolved_events():
            event = resolved.event
            rows.extend(
                (
                    rf"\phantomsection\label{{{entity_label(event.reference)}}}"
                    f"{_code(resolved)} & {_identifier(event.id)} & "
                    f"{_identifier(event.family) if event.family else '--'} & "
                    f"{_identifier(event.frame.upper())} & {_payload(event)}\\\\",
                    r"\multicolumn{5}{@{}p{5.67in}@{}}{\scriptsize "
                    + tex_escape(event.summary)
                    + r"}\\[2pt]",
                )
            )
        return "\n".join(
            [
                r"\begingroup\footnotesize",
                r"\Needspace{1.25in}",
                r"\manualtablecaption{Architectural Leaf Event Contracts}",
                r"\begin{manuallongtable}{@{}>{\raggedright\arraybackslash}p{0.82in}>{\raggedright\arraybackslash}p{1.55in}>{\raggedright\arraybackslash}p{1.30in}>{\raggedright\arraybackslash}p{0.65in}>{\raggedright\arraybackslash}p{1.35in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Code} & \textbf{Event} & \textbf{Family} & \textbf{Frame} & \textbf{Payload}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Code} & \textbf{Event} & \textbf{Family} & \textbf{Frame} & \textbf{Payload}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{manuallongtable}",
                r"\endgroup",
            ]
        )

    def render_index(self, catalog) -> str:
        rows = []
        for resolved in catalog.resolved_events():
            event = resolved.event
            rows.append(
                f"{_code(resolved)} & {_identifier(event.id)} & "
                f"{_identifier(resolved.owner)} & "
                f"{_identifier(event.family) if event.family else '--'} & "
                f"{_identifier(event.frame.upper())} & "
                rf"\hyperref[{entity_label(event.reference)}]{{definition}} "
                r"(p.~\pageref{section:event-code-and-sources})\\"
            )
        return "\n".join(
            [
                r"\enlargethispage{1.5\baselineskip}",
                r"\manualtablecaption{Architectural Event Index}",
                r"\begin{manualdenselongtable}{@{}>{\raggedright\arraybackslash}p{0.82in}>{\raggedright\arraybackslash}p{1.45in}>{\raggedright\arraybackslash}p{0.55in}>{\raggedright\arraybackslash}p{1.15in}>{\raggedright\arraybackslash}p{0.65in}>{\raggedright\arraybackslash}p{0.80in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Code} & \textbf{Event} & \textbf{Owner} & \textbf{Family} & \textbf{Frame} & \textbf{Definition}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{6}{@{}l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Code} & \textbf{Event} & \textbf{Owner} & \textbf{Family} & \textbf{Frame} & \textbf{Definition}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{manualdenselongtable}",
            ]
        )
