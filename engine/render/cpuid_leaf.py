"""Explicit owner-local projection of public CPUID leaf contracts."""

from __future__ import annotations

from dataclasses import dataclass
import re

from ..cpuid import CpuidField, CpuidLeaf
from ..reference import Reference, ReferenceError, UnknownReferenceError
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider
from .latex_document import tex_escape


_DIRECTIVE_OPEN = "(:cpuid-leaf:"
_DIRECTIVE_RE = re.compile(
    r"(?m)^[ \t]*\(:cpuid-leaf:([A-Za-z0-9_.-]+):\)[ \t]*$"
)


@dataclass(frozen=True, slots=True)
class _ProjectedQuery:
    id: str
    first: int
    last: int
    stride: int
    fields: tuple[CpuidField, ...]


def _identifier(value: object) -> str:
    escaped = tex_escape(str(value)).replace(r"\_", r"\_\allowbreak{}")
    return rf"\texttt{{{escaped}}}"


def _index(first: int, last: int, stride: int) -> str:
    if first == last:
        return f"0x{first:04X}"
    result = f"0x{first:04X}--0x{last:04X}"
    return result if stride == 1 else f"{result}/{stride}"


def _root_leaf(catalog, leaf: CpuidLeaf) -> CpuidLeaf:
    active: set[Reference[object]] = set()
    while leaf.extends is not None:
        if leaf.reference in active:
            raise ValueError(f"circular CPUID leaf overlay at {leaf.reference}")
        active.add(leaf.reference)
        leaf = catalog.references.leaves.resolve(leaf.extends)
    return leaf


def _projected_queries(catalog, root: CpuidLeaf) -> tuple[_ProjectedQuery, ...]:
    fields_by_query: dict[tuple[str, int, int, int], list[CpuidField]] = {}
    for namespace in catalog.namespaces.values():
        for cpuid_class in namespace.classes.values():
            for leaf in cpuid_class.leaves.values():
                if _root_leaf(catalog, leaf).reference != root.reference:
                    continue
                for query in leaf.queries:
                    key = (
                        query.id,
                        query.indexes.first,
                        query.indexes.last,
                        query.indexes.stride,
                    )
                    fields_by_query.setdefault(key, []).extend(query.fields)

    return tuple(
        _ProjectedQuery(
            query_id,
            first,
            last,
            stride,
            tuple(sorted(fields, key=lambda field: field.lsb)),
        )
        for (query_id, first, last, stride), fields in sorted(
            fields_by_query.items(),
            key=lambda item: (item[0][1], item[0][2], item[0][3], item[0][0]),
        )
    )


def _diagram_labels(fields: tuple[CpuidField, ...]) -> dict[Reference[object], str]:
    labels: dict[Reference[object], str] = {}
    used: set[str] = set()
    for field in fields:
        candidates = [
            field.id,
            "".join(part[0] for part in field.id.split("_") if part),
            *(character for character in field.id if character != "_"),
        ]
        label = next(
            (
                candidate
                for candidate in candidates
                if candidate
                and len(candidate) <= field.bits
                and candidate not in used
            ),
            "?",
        )
        if label == "?":
            raise ValueError(f"cannot assign a CPUID diagram label to {field.reference}")
        labels[field.reference] = label
        used.add(label)
    return labels


def _bit_range(field: CpuidField) -> str:
    return str(field.lsb) if field.bits == 1 else f"{field.msb}:{field.lsb}"


def _query_diagram_label(
    query: _ProjectedQuery,
    fields: tuple[CpuidField, ...], labels: dict[Reference[object], str]
) -> str:
    lines = [
        rf"index {_identifier(_index(query.first, query.last, query.stride))}: "
        f"{_identifier(query.id)}"
    ]
    entries = []
    for field in fields:
        label = labels[field.reference]
        name = (
            _identifier(field.id)
            if label == field.id
            else f"{_identifier(label)} = {_identifier(field.id)}"
        )
        entries.append(f"{name}[{_identifier(_bit_range(field))}]")
    lines.extend(
        ", ".join(entries[index : index + 2])
        for index in range(0, len(entries), 2)
    )
    return r"\shortstack{" + r"\\".join(lines) + "}"


def _format_fields(
    fields: tuple[CpuidField, ...], labels: dict[Reference[object], str]
) -> tuple[str, ...]:
    parts: list[str] = []
    cursor = 64
    for field in sorted(fields, key=lambda item: item.lsb, reverse=True):
        gap = cursor - field.msb - 1
        if gap:
            parts.append(rf"\BedrockFormatReserved{{reserved}}{{{gap}}}")
        parts.append(
            rf"\BedrockFormatField{{{tex_escape(labels[field.reference])}}}"
            rf"{{{field.bits}}}"
        )
        cursor = field.lsb
    if cursor:
        parts.append(rf"\BedrockFormatReserved{{reserved}}{{{cursor}}}")
    return tuple(parts)


class CpuidLeafFragmentRenderer(DocumentFragmentProvider):
    """Render one explicitly placed, root-owned CPUID leaf contract."""

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((_DIRECTIVE_OPEN,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        matches = tuple(_DIRECTIVE_RE.finditer(text))
        if text.count(_DIRECTIVE_OPEN) != len(matches):
            raise ValueError(
                f"{context.source}: (:cpuid-leaf:...:) must occupy a standalone line"
            )
        if not matches:
            return text

        source = context.source.resolve() if context.source is not None else None
        topics = tuple(
            topic
            for topic in context.project.model.document_topics.values()
            if source is not None and topic.document.resolve() == source
        )
        if len(topics) != 1:
            raise ValueError(
                f"{context.source}: CPUID leaf placement requires one topic owner"
            )
        topic = topics[0]
        placed: set[Reference[object]] = set()

        def replacement(match: re.Match[str]) -> str:
            raw_reference = match.group(1)
            try:
                reference = Reference.parse(raw_reference)
                leaf = context.project.cpuid.references.leaves.resolve(reference)
            except (ReferenceError, UnknownReferenceError) as error:
                raise ValueError(
                    f"{context.source}: unknown CPUID leaf {raw_reference!r}"
                ) from error
            if reference.owner != topic.owner:
                raise ValueError(
                    f"{context.source}: CPUID leaf owner {reference.owner!r} does not "
                    f"match topic owner {topic.owner!r}"
                )
            if leaf.extends is not None:
                raise ValueError(
                    f"{context.source}: CPUID leaf placement must name the root leaf, "
                    f"not overlay {reference}"
                )
            if reference in placed:
                raise ValueError(
                    f"{context.source}: duplicate CPUID leaf placement {reference}"
                )
            placed.add(reference)
            return self.render(context.project.cpuid, leaf)

        return _DIRECTIVE_RE.sub(replacement, text)

    @staticmethod
    def render(catalog, leaf: CpuidLeaf) -> str:
        queries = _projected_queries(catalog, leaf)
        labels = {query: _diagram_labels(query.fields) for query in queries}
        rows = [
            f"{_identifier(_index(query.first, query.last, query.stride))} & "
            f"{_identifier(query.id)}\\\\"
            for query in queries
        ]
        diagram_rows: list[str] = []
        for query in queries:
            label = _query_diagram_label(query, query.fields, labels[query])
            diagram_rows.extend(
                (
                    rf"\BedrockFormatRowRange{{{label}}}{{63}}{{0}}{{%",
                    *_format_fields(query.fields, labels[query]),
                    "}",
                )
            )

        caption = tex_escape(leaf.name)
        return "\n".join(
            (
                rf"\BedrockTableCaption{{{caption} CPUID Query Allocations}}",
                r"\begin{BedrockTabular}{@{}>{\raggedright\arraybackslash}p{1.55in}>{\raggedright\arraybackslash}p{4.10in}@{}}",
                r"\toprule",
                r"\rowcolor{BedrockHeaderFill}",
                r"\textbf{Index} & \textbf{Query}\\",
                r"\midrule",
                *rows,
                r"\bottomrule",
                r"\end{BedrockTabular}",
                "",
                rf"\begin{{BedrockListedFormatDiagram}}{{{caption} CPUID Result Formats}}",
                *diagram_rows,
                r"\end{BedrockListedFormatDiagram}",
            )
        )


__all__ = ["CpuidLeafFragmentRenderer"]
