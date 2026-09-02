"""Exhaustive LaTeX projection of the architectural control-register space."""

from __future__ import annotations

from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


class ControlRegisterReferenceRenderer(DocumentFragmentProvider):
    """Render the normative global RDCR/WRCR selector allocation."""

    PLACEHOLDER = r"\BedrockGeneratedControlRegisterReference"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        return text.replace(
            self.PLACEHOLDER, self.render(context.project.control_registers)
        )

    @staticmethod
    def render(catalog) -> str:
        registers = sorted(
            catalog.references.registers.values(),
            key=lambda register: register.selector,
        )
        rows = [
            rf"\texttt{{0x{register.selector:04X}}} & "
            rf"\texttt{{{tex_escape(register.id)}}} & "
            rf"{tex_escape(register.summary)}\\"
            for register in registers
        ]
        return "\n".join(
            [
                r"\Needspace{1.25in}",
                r"\BedrockTableCaption{Control-Register Selector Allocations}",
                r"\begin{BedrockLongTable}{@{}>{\raggedright\arraybackslash}p{0.75in}>{\raggedright\arraybackslash}p{1.05in}>{\raggedright\arraybackslash}p{3.55in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Selector} & \textbf{Register} & \textbf{Use}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{3}{@{}l}{\scriptsize\itshape Table \theBedrockTable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Selector} & \textbf{Register} & \textbf{Use}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{BedrockLongTable}",
            ]
        )
