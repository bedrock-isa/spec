"""Explicit owner-local projection of byte-addressed memory records."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import re

from ..memory_record import (
    ElementByteSize,
    LinearByteExpression,
    MemoryRecord,
    MemoryRecordBitField,
    MemoryRecordComponent,
)
from ..reference import Reference, ReferenceError, UnknownReferenceError
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


_DIRECTIVE_OPEN = "(:memory-record:"
_DIRECTIVE_RE = re.compile(
    r"(?m)^[ \t]*\(:memory-record:"
    r"((?:base|[A-Z][A-Z0-9_]*)\.records\.[A-Z][A-Z0-9_]*):\)[ \t]*$"
)


@dataclass(frozen=True, slots=True)
class MemoryRecordRowProjection:
    """One visible member row or one omitted middle run."""

    index: int | None
    height: Fraction
    ellipsis: bool = False


@dataclass(frozen=True, slots=True)
class MemoryRecordComponentProjection:
    """One component projected at its derived byte offset."""

    component: MemoryRecordComponent
    offset: LinearByteExpression
    size: LinearByteExpression
    rows: tuple[MemoryRecordRowProjection, ...]

    @property
    def height(self) -> Fraction:
        return sum((row.height for row in self.rows), start=Fraction(0))


@dataclass(frozen=True, slots=True)
class MemoryRecordPaddingProjection:
    """Derived trailing storage needed to meet record alignment."""

    offset: LinearByteExpression
    values: tuple[int, ...]
    height: Fraction


@dataclass(frozen=True, slots=True)
class MemoryRecordProjection:
    """The public layout selected by one memory-record directive."""

    record: MemoryRecord
    components: tuple[MemoryRecordComponentProjection, ...]
    padding: MemoryRecordPaddingProjection | None

    @classmethod
    def create(cls, record: MemoryRecord) -> "MemoryRecordProjection":
        cursor = LinearByteExpression()
        components: list[MemoryRecordComponentProjection] = []
        for component in record.components:
            size = component.element_bytes.expression() * component.count
            row_height = _row_height(record, component.element_bytes)
            indexes: tuple[int | None, ...]
            if component.count <= 5:
                indexes = tuple(range(component.count))
            else:
                indexes = (0, 1, None, component.count - 2, component.count - 1)
            rows = tuple(
                MemoryRecordRowProjection(
                    index=index,
                    height=row_height,
                    ellipsis=index is None,
                )
                for index in indexes
            )
            components.append(
                MemoryRecordComponentProjection(component, cursor, size, rows)
            )
            cursor += size

        padding_values = tuple(
            sorted(
                {
                    record.padding_bytes(parameter_value)
                    for parameter_value in record.parameter_values
                }
            )
        )
        padding = None
        if any(padding_values):
            padding = MemoryRecordPaddingProjection(
                cursor,
                padding_values,
                max(Fraction(1), Fraction(min(padding_values), 8)),
            )
        return cls(record, tuple(components), padding)

    @property
    def height(self) -> Fraction:
        component_height = sum(
            (component.height for component in self.components), start=Fraction(0)
        )
        return component_height + (
            self.padding.height if self.padding is not None else Fraction(0)
        )


class MemoryRecordFragmentRenderer(DocumentFragmentProvider):
    """Render a catalog record only where its owning topic places it."""

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((_DIRECTIVE_OPEN,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        matches = tuple(_DIRECTIVE_RE.finditer(text))
        if text.count(_DIRECTIVE_OPEN) != len(matches):
            raise ValueError(
                f"{context.source}: (:memory-record:...:) must occupy a "
                "standalone line"
            )
        if not matches:
            return text

        placed: set[Reference[MemoryRecord]] = set()

        def replacement(match: re.Match[str]) -> str:
            raw_reference = match.group(1)
            projection = self.project(context, raw_reference)
            if projection.record.reference in placed:
                raise ValueError(
                    f"{context.source}: duplicate memory-record placement "
                    f"{raw_reference!r}"
                )
            placed.add(projection.record.reference)
            return self.render(projection)

        return _DIRECTIVE_RE.sub(replacement, text)

    @staticmethod
    def project(
        context: DocumentFragmentContext, raw_reference: str
    ) -> MemoryRecordProjection:
        """Resolve one record against the owner of its containing topic."""

        source = context.source.resolve() if context.source is not None else None
        topics = tuple(
            topic
            for topic in context.project.model.document_topics.values()
            if source is not None and topic.document.resolve() == source
        )
        if len(topics) != 1:
            raise ValueError(
                f"{context.source}: memory-record placement requires one topic owner"
            )
        try:
            reference: Reference[MemoryRecord] = Reference.parse(raw_reference)
            record = context.project.memory_records.resolve(reference)
        except (ReferenceError, UnknownReferenceError, ValueError) as error:
            raise ValueError(
                f"{context.source}: unknown memory record {raw_reference!r}"
            ) from error
        if record.owner != topics[0].owner:
            raise ValueError(
                f"{context.source}: memory-record owner {record.owner!r} does not "
                f"match topic owner {topics[0].owner!r}"
            )
        return MemoryRecordProjection.create(record)

    @staticmethod
    def render(projection: MemoryRecordProjection) -> str:
        record = projection.record
        lines = [_shape_sentence(record), "", *_render_record_diagram(projection)]
        formatted = tuple(
            component
            for component in projection.components
            if component.component.bit_format is not None
        )
        if formatted:
            lines.extend(("", *_render_bit_formats(record, formatted)))
        return "\n".join(lines)


def _row_height(record: MemoryRecord, size: ElementByteSize) -> Fraction:
    parameter_value = (
        record.parameter.values[0] if record.parameter is not None else None
    )
    return max(Fraction(1), Fraction(size.evaluate(parameter_value), 8))


def _shape_sentence(record: MemoryRecord) -> str:
    alignment = record.alignment_bytes
    if record.parameter is None:
        total = record.total_bytes()
        return f"This record is {total} bytes and {alignment}-byte aligned."
    parameter = record.parameter
    values = ", ".join(str(value) for value in parameter.values)
    total = _aligned_total_tex(record)
    return (
        rf"Let ${tex_escape(parameter.id)}$ be {tex_escape(parameter.description)}, "
        rf"with ${tex_escape(parameter.id)} \in \{{{values}\}}$. "
        f"This record is {alignment}-byte aligned and has total size "
        rf"${total}$ bytes."
    )


def _aligned_total_tex(record: MemoryRecord) -> str:
    expression = record.payload_expression
    alignment = record.alignment_bytes
    if not expression.coefficient:
        return str(record.total_bytes())
    parameter = tex_escape(expression.parameter or "")
    if expression.constant % alignment == 0:
        prefix = (
            rf"\texttt{{{_hex(expression.constant)}}} + "
            if expression.constant
            else ""
        )
        numerator = expression.coefficient.numerator
        denominator = expression.coefficient.denominator * alignment
        term = _fractional_parameter_tex(numerator, denominator, parameter)
        return rf"{prefix}{alignment}\lceil {term}\rceil"
    inner = _linear_tex(expression, constants_as_hex=True)
    return rf"{alignment}\lceil ({inner})/{alignment}\rceil"


def _render_record_diagram(projection: MemoryRecordProjection) -> list[str]:
    record = projection.record
    needspace = float(Fraction(4, 5) + projection.height * Fraction(4, 25))
    lines = [
        rf"\begin{{BedrockMemoryRecordDiagram}}{{{tex_escape(record.name)}}}"
        rf"{{{needspace:.2f}in}}"
    ]
    for projected in projection.components:
        component = projected.component
        offset = _offset_tex(projected.offset)
        if component.count == 1:
            label = (
                f"{tex_escape(component.label)} "
                f"({_element_size_tex(component.element_bytes)} bytes"
                f"{'; 0' if component.fixed_value == 'zero' else ''})"
            )
            macro = (
                "BedrockMemoryRecordZeroSlot"
                if component.fixed_value == "zero"
                else "BedrockMemoryRecordSlot"
            )
            lines.append(
                rf"\{macro}{{{offset}}}{{{_number(projected.rows[0].height)}}}"
                rf"{{{label}}}"
            )
            continue

        aggregate = _linear_tex(projected.size, constants_as_hex=False)
        lines.append(
            rf"\BedrockMemoryRecordSeriesBegin{{{offset}}}"
            rf"{{${aggregate}$ bytes}}"
        )
        for row in projected.rows:
            if row.ellipsis:
                lines.append(
                    rf"\BedrockMemoryRecordSeriesEllipsis"
                    rf"{{{_number(row.height)}}}"
                )
                continue
            assert row.index is not None
            label = (
                f"{tex_escape(component.label)}{row.index} "
                f"({_element_size_tex(component.element_bytes)} bytes)"
            )
            lines.append(
                rf"\BedrockMemoryRecordSeriesRow{{{_number(row.height)}}}"
                rf"{{{label}}}"
            )
        lines.append(r"\BedrockMemoryRecordSeriesEnd")

    if projection.padding is not None:
        values = _value_list(projection.padding.values)
        lines.append(
            rf"\BedrockMemoryRecordZeroSlot{{{_offset_tex(projection.padding.offset)}}}"
            rf"{{{_number(projection.padding.height)}}}"
            rf"{{Padding ({values} bytes; 0)}}"
        )
    lines.append(r"\end{BedrockMemoryRecordDiagram}")
    return lines


def _render_bit_formats(
    record: MemoryRecord,
    components: tuple[MemoryRecordComponentProjection, ...],
) -> list[str]:
    lines = [
        rf"\begin{{BedrockListedFormatDiagram}}"
        rf"{{{tex_escape(record.name)} Bit Layouts}}"
    ]
    for projected in components:
        component = projected.component
        bit_format = component.bit_format
        assert bit_format is not None
        fields = tuple(sorted(bit_format.fields, key=lambda field: field.lsb, reverse=True))
        label = _format_row_label(component, fields, bit_format.bits)
        lines.append(
            rf"\BedrockFormatRowRange{{{label}}}"
            rf"{{{bit_format.bits - 1}}}{{0}}{{%"
        )
        cursor = bit_format.bits
        for field in fields:
            gap = cursor - field.msb - 1
            if gap:
                lines.append(rf"\BedrockFormatReserved{{0}}{{{gap}}}")
            display = tex_escape(field.diagram_label or field.label)
            lines.append(rf"\BedrockFormatField{{{display}}}{{{field.bits}}}")
            cursor = field.lsb
        if cursor:
            lines.append(rf"\BedrockFormatReserved{{0}}{{{cursor}}}")
        lines.append("}")
    lines.append(r"\end{BedrockListedFormatDiagram}")
    return lines


def _format_row_label(
    component: MemoryRecordComponent,
    fields: tuple[MemoryRecordBitField, ...],
    bits: int,
) -> str:
    title = f"{tex_escape(component.label)}[{bits - 1}:0]"
    legends = []
    for field in sorted(fields, key=lambda item: item.lsb):
        if field.diagram_label is None or field.diagram_label == field.label:
            continue
        bit_range = str(field.lsb) if field.bits == 1 else f"{field.msb}:{field.lsb}"
        legends.append(
            rf"{tex_escape(field.diagram_label)} = "
            rf"{tex_escape(field.label)}[{bit_range}]"
        )
    if not legends:
        return title
    return r"\shortstack{" + r"\\".join((title, *legends)) + "}"


def _offset_tex(expression: LinearByteExpression) -> str:
    if not expression.coefficient:
        return rf"\texttt{{{_hex(expression.constant)}}}"
    return rf"${_linear_tex(expression, constants_as_hex=True)}$"


def _element_size_tex(size: ElementByteSize) -> str:
    if size.fixed is not None:
        return str(size.fixed)
    assert size.parameter is not None
    parameter = tex_escape(size.parameter)
    if size.divisor == 1:
        return rf"${parameter}$"
    return rf"${parameter}/{size.divisor}$"


def _linear_tex(
    expression: LinearByteExpression, *, constants_as_hex: bool
) -> str:
    parts: list[str] = []
    if expression.constant:
        parts.append(
            rf"\texttt{{{_hex(expression.constant)}}}"
            if constants_as_hex
            else str(expression.constant)
        )
    if expression.coefficient:
        parameter = tex_escape(expression.parameter or "")
        coefficient = expression.coefficient
        parts.append(
            _fractional_parameter_tex(
                coefficient.numerator, coefficient.denominator, parameter
            )
        )
    return " + ".join(parts) if parts else "0"


def _fractional_parameter_tex(
    numerator: int, denominator: int, parameter: str
) -> str:
    numerator_text = parameter if numerator == 1 else f"{numerator}{parameter}"
    if denominator == 1:
        return numerator_text
    return f"{numerator_text}/{denominator}"


def _hex(value: int) -> str:
    width = max(2, len(f"{value:x}"))
    return f"0x{value:0{width}x}"


def _number(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.3f}".rstrip("0").rstrip(".")


def _value_list(values: tuple[int, ...]) -> str:
    if len(values) == 1:
        return str(values[0])
    if len(values) == 2:
        return f"{values[0]} or {values[1]}"
    return ", ".join(str(value) for value in values[:-1]) + f", or {values[-1]}"


__all__ = [
    "MemoryRecordComponentProjection",
    "MemoryRecordFragmentRenderer",
    "MemoryRecordPaddingProjection",
    "MemoryRecordProjection",
    "MemoryRecordRowProjection",
]
