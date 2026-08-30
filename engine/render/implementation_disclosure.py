"""LaTeX rendering for implementation-defined disclosure data."""

from __future__ import annotations

from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


class ImplementationDisclosureRenderer(DocumentFragmentProvider):
    PLACEHOLDER = r"\BedrockGeneratedImplementationDisclosures"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        return text.replace(
            self.PLACEHOLDER, self.render(context.project.disclosures)
        )

    def render(self, catalog) -> str:
        rows = [
            f"{tex_escape(disclosure.item)} & "
            f"{tex_escape(', '.join(disclosure.defining_rules))} & "
            f"{tex_escape(disclosure.publication)}\\\\"
            for disclosure in catalog.disclosures
        ]
        return "\n".join(
            [
                r"\Needspace{3.0in}",
                r"\BedrockTableCaption{Implementation-Defined Disclosure Register}",
                r"\begin{BedrockLongTable}{@{}>{\raggedright\arraybackslash}p{1.35in}>{\raggedright\arraybackslash}p{2.20in}>{\raggedright\arraybackslash}p{2.10in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Item} & \textbf{Defining rule} & \textbf{Publication}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{3}{l}{\scriptsize\itshape Table \theBedrockTable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Item} & \textbf{Defining rule} & \textbf{Publication}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{BedrockLongTable}",
            ]
        )
