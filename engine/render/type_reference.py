"""Registry-backed LaTeX reference tables for encoding type definitions."""

from __future__ import annotations

from ..entity import entity_label
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


def _identifier(value: object) -> str:
    escaped = tex_escape(str(value)).replace(r"\_", r"\_\allowbreak{}")
    return rf"\texttt{{{escaped}}}"


def _details(definition) -> str:
    attributes = []
    for name in ("value_type", "register_group", "profile"):
        value = getattr(definition, name, None)
        if value is not None:
            attributes.append(f"{name}={value}")
    signed = getattr(definition, "signed", None)
    if signed is not None:
        attributes.append(f"signed={'true' if signed else 'false'}")
    values = getattr(definition, "values", ())
    if values:
        attributes.append(
            "values=" + ", ".join(f"{item.code}:{item.value}" for item in values)
        )
    return ", ".join(_identifier(item) for item in attributes) or "--"


class EncodingTypeReferenceRenderer(DocumentFragmentProvider):
    """Render the canonical field/payload type indexes from TypeSystem."""

    PLACEHOLDER = r"\BedrockGeneratedEncodingTypeRegistry"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if self.PLACEHOLDER not in text:
            return text
        replacement = "\n\n".join(
            (
                self._field_types(context.project.types),
                self._payload_types(context.project.types),
            )
        )
        return text.replace(self.PLACEHOLDER, replacement)

    @staticmethod
    def _field_types(types) -> str:
        rows = []
        for reference, definition in sorted(
            types.field_types.items(), key=lambda item: str(item[0])
        ):
            rows.append(
                rf"\phantomsection\label{{{entity_label(reference)}}}"
                f"{_identifier(reference.owner)} & {_identifier(reference.element)} & "
                f"{definition.bits} & {_identifier(definition.kind)} & "
                f"{_details(definition)}\\\\"
            )
        return "\n".join(
            [
                r"\manualtablecaption{Encoding Field-Type Registry}",
                r"\begin{manualdenselongtable}{@{}>{\raggedright\arraybackslash}p{0.55in}>{\raggedright\arraybackslash}p{0.90in}>{\raggedright\arraybackslash}p{0.32in}>{\raggedright\arraybackslash}p{1.25in}>{\raggedright\arraybackslash}p{2.25in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bits} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bits} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{manualdenselongtable}",
            ]
        )

    @staticmethod
    def _payload_types(types) -> str:
        rows = []
        for reference, definition in sorted(
            types.payload_types.items(), key=lambda item: str(item[0])
        ):
            rows.append(
                rf"\phantomsection\label{{{entity_label(reference)}}}"
                f"{_identifier(reference.owner)} & {_identifier(reference.element)} & "
                f"{definition.bytes} & {_identifier(definition.kind)} & "
                f"{_details(definition)}\\\\"
            )
        return "\n".join(
            [
                r"\manualtablecaption{Encoding Payload-Type Registry}",
                r"\begin{manualdenselongtable}{@{}>{\raggedright\arraybackslash}p{0.55in}>{\raggedright\arraybackslash}p{0.90in}>{\raggedright\arraybackslash}p{0.38in}>{\raggedright\arraybackslash}p{1.25in}>{\raggedright\arraybackslash}p{2.19in}@{}}",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bytes} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \themanualtable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bytes} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{manualdenselongtable}",
            ]
        )
