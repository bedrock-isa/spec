"""Registry-backed LaTeX reference tables for CPUID query entities."""

from __future__ import annotations

from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


def _identifier(value: object) -> str:
    escaped = tex_escape(str(value)).replace(r"\_", r"\_\allowbreak{}")
    return rf"\texttt{{{escaped}}}"


def _index_range(value) -> str:
    if value.first == value.last:
        return _identifier(value.first)
    result = f"{value.first}--{value.last}"
    if value.stride != 1:
        result += f"/{value.stride}"
    return _identifier(result)


class CpuidEntityReferenceRenderer(DocumentFragmentProvider):
    """Render the reader-facing exact-ID index for CPUID queries."""

    PLACEHOLDER = r"\BedrockGeneratedCPUIDEntityRegistry"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if self.PLACEHOLDER not in text:
            return text
        replacement = self._queries(context.project)
        return text.replace(self.PLACEHOLDER, replacement)

    @staticmethod
    def _queries(project) -> str:
        catalog = project.cpuid
        rows = []
        entries = sorted(
            [
                (namespace.owner, cpuid_class.id, leaf.id, query)
                for namespace in catalog.namespaces.values()
                for cpuid_class in namespace.classes.values()
                for leaf in cpuid_class.leaves.values()
                for query in leaf.queries
            ],
            key=lambda item: item[:3],
        )
        for owner, class_id, leaf_id, query in entries:
            anchor = rf"\phantomsection\label{{{_label(project, query.reference)}}}"
            rows.append(
                f"{_identifier(owner)}{anchor} & "
                f"{_identifier(f'{class_id}.{leaf_id}')} & "
                f"{_identifier(query.id)} & {_index_range(query.indexes)} & "
                f"{len(query.fields)}\\\\"
            )
        return "\n".join(
            [
                r"\BedrockTableCaption{CPUID Query Registry}",
                r"\begin{BedrockDenseLongTable}{@{}>{\raggedright\arraybackslash}p{0.58in}>{\raggedright\arraybackslash}p{1.45in}>{\raggedright\arraybackslash}p{1.45in}>{\raggedright\arraybackslash}p{0.75in}>{\raggedright\arraybackslash}p{0.55in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Owner} & \textbf{Class.Leaf} & \textbf{Query} & \textbf{Index} & \textbf{Fields}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \theBedrockTable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Owner} & \textbf{Class.Leaf} & \textbf{Query} & \textbf{Index} & \textbf{Fields}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{BedrockDenseLongTable}",
            ]
        )


def _label(project, reference) -> str:
    label = project.entities.resolve(reference).latex_label
    if label is None:
        raise ValueError("entity has no target in this LaTeX artifact")
    return label
