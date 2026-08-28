"""Registry-backed LaTeX reference tables for CPUID query entities."""

from __future__ import annotations

from ..entity import entity_label
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


def _bits(field) -> str:
    if field.bits == 1:
        return _identifier(field.lsb)
    return _identifier(f"{field.msb}..{field.lsb}")


class CpuidEntityReferenceRenderer(DocumentFragmentProvider):
    """Render a complete exact-ID index for CPUID queries and result fields."""

    PLACEHOLDER = r"\BedrockGeneratedCpuidEntityRegistry"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if self.PLACEHOLDER not in text:
            return text
        catalog = context.project.cpuid.references
        replacement = "\n\n".join(
            (self._queries(catalog), self._fields(catalog))
        )
        return text.replace(self.PLACEHOLDER, replacement)

    @staticmethod
    def _queries(catalog) -> str:
        rows = []
        for reference, query in sorted(
            catalog.queries.items(), key=lambda item: str(item[0])
        ):
            leaf = ".".join((*reference.path[1:],))
            rows.append(
                rf"\phantomsection\label{{{entity_label(reference)}}}"
                f"{_identifier(reference.owner)} & {_identifier(leaf)} & "
                f"{_identifier(query.id)} & {_index_range(query.indexes)} & "
                f"{len(query.fields)}\\\\"
            )
        return "\n".join(
            [
                r"\manualtablecaption{CPUID Query Registry}",
                r"\begin{manualdenselongtable}{@{}>{\raggedright\arraybackslash}p{0.58in}>{\raggedright\arraybackslash}p{1.45in}>{\raggedright\arraybackslash}p{1.45in}>{\raggedright\arraybackslash}p{0.75in}>{\raggedright\arraybackslash}p{0.55in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Class.Leaf} & \textbf{Query} & \textbf{Index} & \textbf{Fields}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Class.Leaf} & \textbf{Query} & \textbf{Index} & \textbf{Fields}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{manualdenselongtable}",
            ]
        )

    @staticmethod
    def _fields(catalog) -> str:
        rows = []
        for reference, field in sorted(
            catalog.fields.items(), key=lambda item: str(item[0])
        ):
            query = ".".join(reference.path[1:])
            rows.append(
                rf"\phantomsection\label{{{entity_label(reference)}}}"
                f"{_identifier(reference.owner)} & {_identifier(query)} & "
                f"{_identifier(field.id)} & {_bits(field)}\\\\"
            )
        return "\n".join(
            [
                r"\manualtablecaption{CPUID Result-Field Registry}",
                r"\begin{manualdenselongtable}{@{}>{\raggedright\arraybackslash}p{0.58in}>{\raggedright\arraybackslash}p{2.60in}>{\raggedright\arraybackslash}p{1.65in}>{\raggedright\arraybackslash}p{0.65in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Class.Leaf.Query} & \textbf{Field} & \textbf{Bits}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{4}{@{}l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Class.Leaf.Query} & \textbf{Field} & \textbf{Bits}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{manualdenselongtable}",
            ]
        )
