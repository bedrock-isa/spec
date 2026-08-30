"""Registry-backed LaTeX reference tables for encoding type definitions."""

from __future__ import annotations

from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


def _identifier(value: object) -> str:
    escaped = tex_escape(str(value)).replace(r"\_", r"\_\allowbreak{}")
    return rf"\texttt{{{escaped}}}"


def _details(definition, project) -> str:
    attributes = []
    for name in ("value_type", "profile"):
        value = getattr(definition, name, None)
        if value is not None:
            attributes.append(f"{name}={value}")
    register_group = getattr(definition, "register_group", None)
    if register_group is not None:
        group = project.registers.references.groups.resolve(register_group)
        attributes.append(f"register_group={group.id}")
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
                self._field_types(context.project),
                self._payload_types(context.project),
            )
        )
        return text.replace(self.PLACEHOLDER, replacement)

    @staticmethod
    def _field_types(project) -> str:
        rows = []
        for reference, definition in sorted(
            project.types.field_types.items(),
            key=lambda item: (item[1].owner, item[1].id),
        ):
            anchor = rf"\phantomsection\label{{{_label(project, reference)}}}"
            rows.append(
                f"{_identifier(definition.owner)}{anchor} & "
                f"{_identifier(definition.id)} & "
                f"{definition.bits} & {_identifier(definition.kind)} & "
                f"{_details(definition, project)}\\\\"
            )
        return "\n".join(
            [
                r"\BedrockTableCaption{Encoding Field-Type Registry}",
                r"\begin{BedrockDenseLongTable}{@{}>{\raggedright\arraybackslash}p{0.55in}>{\raggedright\arraybackslash}p{0.90in}>{\raggedright\arraybackslash}p{0.32in}>{\raggedright\arraybackslash}p{1.25in}>{\raggedright\arraybackslash}p{2.25in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bits} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \theBedrockTable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bits} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{BedrockDenseLongTable}",
            ]
        )

    @staticmethod
    def _payload_types(project) -> str:
        rows = []
        for reference, definition in sorted(
            project.types.payload_types.items(),
            key=lambda item: (item[1].owner, item[1].id),
        ):
            anchor = rf"\phantomsection\label{{{_label(project, reference)}}}"
            rows.append(
                f"{_identifier(definition.owner)}{anchor} & "
                f"{_identifier(definition.id)} & "
                f"{definition.bytes} & {_identifier(definition.kind)} & "
                f"{_details(definition, project)}\\\\"
            )
        return "\n".join(
            [
                r"\BedrockTableCaption{Encoding Payload-Type Registry}",
                r"\begin{BedrockDenseLongTable}{@{}>{\raggedright\arraybackslash}p{0.55in}>{\raggedright\arraybackslash}p{0.90in}>{\raggedright\arraybackslash}p{0.38in}>{\raggedright\arraybackslash}p{1.25in}>{\raggedright\arraybackslash}p{2.19in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bytes} & \textbf{Kind} & \textbf{Attributes}\\",
                r"\midrule",
                r"\endfirsthead",
                r"\multicolumn{5}{@{}l}{\scriptsize\itshape Table \theBedrockTable\ (continued)}\\",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Owner} & \textbf{Type} & \textbf{Bytes} & \textbf{Kind} & \textbf{Attributes}\\",
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
