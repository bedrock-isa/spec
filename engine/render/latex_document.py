"""Pure LaTeX renderers for the ISA reference document."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, cast

from ..dependency import DependencyGraph
from ..entity import (
    Entity,
    EntityDisplayStyle,
    instruction_label,
)
from ..reference import Reference
from ..composition.document import (
    DocumentComposition,
    InstructionSetBlock,
    TermGroupBlock,
    TopicBlock,
)
from ..project import InstructionBundle
from ..semantic_text import (
    EntityReferenceText,
    LiteralText,
    SemanticText,
    TermForm,
    TermReferenceText,
)
from ..terminology import Term, TermCatalog, TermGroup
from ..type_system import FieldTypeKind
from .document_fragment import DocumentFragmentPipeline
from .latex_source import LatexSourcePreprocessor

if TYPE_CHECKING:
    from ..encoding import EncodingForm, FieldBinding
    from ..type_system import FieldType, TypeSystem


def tex_escape(value: object) -> str:
    """Escape untrusted plain text before insertion into TeX."""

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "|": r"\textbar{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
        "'": r"\textquotesingle{}",
    }
    return "".join(replacements.get(character, character) for character in str(value))


def tex_code(value: object) -> str:
    return r"\texttt{" + tex_escape(value).replace("--", r"{-}{-}") + "}"


def _entity_label(project, reference: Reference[object]) -> str:
    entities = getattr(project, "entities", project)
    label = entities.resolve(cast(Reference[Entity], reference)).latex_label
    if label is None:
        raise ValueError("entity has no target in this LaTeX artifact")
    return label


class LatexSemanticTextRenderer:
    """Render resolved terminology references inside SemanticText to LaTeX."""

    def render(
        self,
        text: SemanticText,
        catalog: TermCatalog,
        *,
        entities=None,
        escape_literals: bool = True,
    ) -> str:
        parts: list[str] = []
        for part in text.parts:
            if isinstance(part, LiteralText):
                parts.append(tex_escape(part.value) if escape_literals else part.value)
                continue
            if isinstance(part, EntityReferenceText):
                if entities is None:
                    raise ValueError(
                        f"{text.origin.source}: no entity catalog is available"
                    )
                entity = entities.resolve(part.reference)
                if entity.latex_label is None:
                    raise ValueError(
                        f"{text.origin.source}: entity has no target in this "
                        "LaTeX artifact"
                    )
                display = (
                    tex_code(entity.display)
                    if entity.display_style is EntityDisplayStyle.CODE
                    else tex_escape(entity.display)
                )
                parts.append(rf"\hyperref[{entity.latex_label}]{{{display}}}")
                continue
            assert isinstance(part, TermReferenceText)
            term = catalog.references.terms.resolve(part.reference)
            if entities is None:
                raise ValueError(
                    f"{text.origin.source}: no entity catalog is available"
                )
            display = self._term_form(term, part.form)
            parts.append(
                rf"\hyperref[{_entity_label(entities, term.reference)}]"
                rf"{{{tex_escape(display)}}}"
            )
        return "".join(parts)

    @staticmethod
    def _term_form(term: Term, form: TermForm) -> str:
        if form is TermForm.CANONICAL:
            return term.forms.canonical
        if form is TermForm.PLURAL and term.forms.plural is not None:
            return term.forms.plural
        if form is TermForm.ADJECTIVE and term.forms.adjective is not None:
            return term.forms.adjective
        if term.abbreviation is not None:
            if form is TermForm.SHORT:
                return term.abbreviation.canonical
            if form is TermForm.FIRST:
                return f"{term.forms.canonical} ({term.abbreviation.canonical})"
        raise ValueError(
            f"term {term.forms.canonical!r} does not define form {form.value!r}"
        )


class TermGroupRenderer:
    """Render one terminology group as a manual subsection."""

    def __init__(self, semantic: LatexSemanticTextRenderer | None = None) -> None:
        self.semantic = semantic or LatexSemanticTextRenderer()

    def render(self, group: TermGroup, project, dependencies=None) -> str:
        catalog = project.terminology
        return "\n\n".join(
            (
                rf"\subsection{{{tex_escape(group.title)}}}"
                rf"\label{{{_entity_label(project, group.reference)}}}",
                *(
                    self._term(term, project, dependencies)
                    for term in group.terms.values()
                ),
            )
        )

    def _term(self, term: Term, project, dependencies=None) -> str:
        display = term.forms.canonical
        if term.abbreviation is not None:
            display += f" ({term.abbreviation.canonical})"
        if term.article is not None:
            subject = f"{term.article.capitalize()} \\emph{{{tex_escape(display)}}}"
        else:
            display = display[:1].upper() + display[1:]
            subject = rf"\emph{{{tex_escape(display)}}}"
        if dependencies is not None:
            dependencies.record(term.reference, term.definition)
        definition = self.semantic.render(
            term.definition,
            project.terminology,
            entities=project.entities,
        )
        return (
            rf"\phantomsection\label{{{_entity_label(project, term.reference)}}}" + "\n"
            + f"{subject} is {definition}"
        )


class InstructionEntryRenderer:
    """Render one instruction bundle from the current typed model."""

    def render(
        self,
        bundle: InstructionBundle,
        types: "TypeSystem",
        description: str | None = None,
    ) -> str:
        instruction = bundle.instruction
        mnemonic = instruction.mnemonic
        parts = [
            r"\clearpage",
            rf"\begin{{BedrockInstruction}}{{{tex_escape(mnemonic)}}}"
            rf"{{{tex_escape(instruction.name)}}}{{{instruction_label(mnemonic)}}}",
            self._field("Operation", tex_escape(instruction.summary)),
            self._field(
                "Assembler Syntax",
                self._ragged(tex_code(form.syntax.code) for form in bundle.encodings.forms),
            ),
            self._field(
                "Privilege",
                "Supervisor only" if instruction.privileged else "Unprivileged",
            ),
        ]
        if bundle.required_cpuid_flags:
            parts.append(
                self._field(
                    "Required CPUID flags",
                    self._ragged(
                        tex_code(field.id) for field in bundle.required_cpuid_flags
                    ),
                )
            )
        repeat = instruction.to_dict().get("repeat")
        if repeat:
            text = "REP eligible"
            if repeat["type"] == "repcc":
                text += "; REPcc observes " + tex_code(repeat["observed_value"])
            parts.append(self._field("Repeat eligibility", text))
        if description is None:
            description = bundle.artifacts.description.read_text(
                encoding="utf-8"
            ).strip()
        parts.extend(
            [
                r"\BedrockInstructionDescriptionHeading{Detailed Semantics}",
                description,
                self._forms(bundle, types),
                r"\end{BedrockInstruction}",
            ]
        )
        return "\n".join(part for part in parts if part)

    @staticmethod
    def _field(label: str, value: str) -> str:
        return rf"\BedrockOperationField{{{tex_escape(label)}}}{{{value}}}"

    @staticmethod
    def _ragged(lines) -> str:
        rendered = "".join(rf"\noindent {line}\par " for line in lines)
        return rf"\begin{{BedrockRaggedBlock}}{rendered}\end{{BedrockRaggedBlock}}"

    def _forms(self, bundle: InstructionBundle, types: "TypeSystem") -> str:
        blocks = [r"\begin{BedrockInstructionForms}"]
        for index, form in enumerate(bundle.encodings.forms):
            blocks.extend(
                [
                    r"\begin{BedrockFormBlock}{2.75in}",
                    *([r"\BedrockInstructionFormsHeading"] if index == 0 else []),
                    rf"\textbf{{{tex_code(form.syntax.code)}}}\par",
                    r"\BedrockInstructionFormatHeading",
                    self._instruction_diagram(form),
                ]
            )
            descriptions = self._field_descriptions(bundle, form, types)
            if descriptions:
                blocks.append(r"\BedrockInstructionFieldsHeading")
                blocks.extend(descriptions)
            blocks.append(r"\end{BedrockFormBlock}")
        blocks.append(r"\end{BedrockInstructionForms}")
        return "\n".join(blocks)

    def _field_descriptions(
        self,
        bundle: InstructionBundle,
        form: "EncodingForm",
        types: "TypeSystem",
    ) -> list[str]:
        descriptions: list[str] = []
        if form.pattern.bit_width >= 18:
            descriptions.append(
                r"\BedrockInstructionFieldDescription{Length field \texttt{L}}"
                r"{Encodes the encoded instruction length as $3+L$ bytes. "
                r"The encoded length must cover the required instruction length; "
                r"trailing bytes are uninterpreted padding.}"
            )

        for field in self._ordered_fields(form):
            field_type = types.field_types.resolve(field.type)
            label = self._field_label(field, field_type)
            description = self._field_description(bundle, form, field, field_type)
            descriptions.append(
                rf"\BedrockInstructionFieldDescription{{{label}}}{{{description}}}"
            )

        for overlap in form.overlaps:
            left, right = (
                self._operand_name(operand) for operand in overlap.operands
            )
            subjects = f"the {left} and {right} operands"
            if overlap.type == "same_value":
                meaning = (
                    f"When {subjects} designate the same architectural register, "
                    "the final value equals that register's initial value."
                )
            else:
                meaning = (
                    f"When {subjects} designate the same architectural register, "
                    "the instruction raises "
                    "ILLEGAL_INSTRUCTION.INVALID_OPERAND_RELATION before "
                    "architectural effects."
                )
            descriptions.append(
                r"\BedrockInstructionFieldDescription{Operand overlap}"
                rf"{{{tex_escape(meaning)}}}"
            )
        return descriptions

    @staticmethod
    def _ordered_fields(form: "EncodingForm") -> tuple["FieldBinding", ...]:
        ordered: list[FieldBinding] = []
        seen: set[str] = set()
        for marker in form.pattern.code:
            if marker in "01" or marker in seen:
                continue
            field = form.field_for_marker(marker)
            if field is None:
                raise ValueError(
                    f"encoding form {form.id!r} has no binding for field {marker!r}"
                )
            ordered.append(field)
            seen.add(marker)
        ordered.extend(field for field in form.fields if field.marker not in seen)
        return tuple(ordered)

    @staticmethod
    def _field_label(field: "FieldBinding", field_type: "FieldType") -> str:
        names = {
            FieldTypeKind.SIZE_SELECTOR: "Size field",
            FieldTypeKind.EFFECTIVE_ADDRESS: "Effective Address field",
            FieldTypeKind.REGISTER_SELECTOR: "Register field",
            FieldTypeKind.REGISTER: "Register field",
            FieldTypeKind.REGISTER_PAIR_SELECTOR: "Register-pair field",
            FieldTypeKind.ENUM_CONDITION: "Condition field",
            FieldTypeKind.IMMEDIATE: "Immediate field",
            FieldTypeKind.MEMORY_ORDER: "Memory-order field",
            FieldTypeKind.FLAGS: "Flags field",
            FieldTypeKind.PAGE_TABLE_LEVEL: "Page-table-level field",
        }
        return f"{names[field_type.kind]} {tex_code(field.marker)}"

    def _field_description(
        self,
        bundle: InstructionBundle,
        form: "EncodingForm",
        field: "FieldBinding",
        field_type: "FieldType",
    ) -> str:
        kind = field_type.kind
        target = self._operand_target(bundle, field.role)
        if kind is FieldTypeKind.SIZE_SELECTOR:
            choices = form.syntax.selected_size_codes or tuple(
                value.code for value in field_type.values
            )
            text = (
                f"Selects {'/'.join(choices)}."
                if choices
                else "Selects the operand size."
            )
        elif kind is FieldTypeKind.EFFECTIVE_ADDRESS:
            text = f"Specifies {target}."
            if any(
                constraint.role == field.role
                and "immediate" in constraint.exclude
                for constraint in form.constraints
            ):
                text += " Immediate addressing is unavailable in this form."
        elif kind in {
            FieldTypeKind.REGISTER_SELECTOR,
            FieldTypeKind.REGISTER,
        }:
            text = f"Selects {target}."
        elif kind is FieldTypeKind.REGISTER_PAIR_SELECTOR:
            text = f"Selects {target} as a register pair."
        elif kind is FieldTypeKind.ENUM_CONDITION:
            text = "Selects the condition code."
        elif kind is FieldTypeKind.IMMEDIATE:
            text = "Encodes the immediate value."
        elif kind is FieldTypeKind.MEMORY_ORDER:
            text = "Selects the memory ordering."
        elif kind is FieldTypeKind.FLAGS:
            text = "Selects the architectural flags."
        elif kind is FieldTypeKind.PAGE_TABLE_LEVEL:
            text = "Selects the page-table level."
        else:  # pragma: no cover - exhaustive over FieldTypeKind
            raise ValueError(f"unsupported field type kind {kind!r}")

        allowed = self._allowed_values(form, field.role)
        if allowed and kind is not FieldTypeKind.SIZE_SELECTOR:
            text += f" Allowed encoded values: {self._value_ranges(allowed)}."
        return tex_escape(text)

    @staticmethod
    def _operand_target(bundle: InstructionBundle, role: str) -> str:
        operands = bundle.instruction.to_dict().get("operands", {})
        operand = operands.get(role) if isinstance(operands, dict) else None
        if isinstance(operand, dict):
            semantic_role = str(operand.get("role", "")).replace("_", "-")
            if semantic_role:
                return f"the {semantic_role} operand"
        return "the operand"

    @staticmethod
    def _operand_name(role: str) -> str:
        special = {
            "dst": "destination",
            "src": "source",
            "lhs": "left-hand",
            "rhs": "right-hand",
            "govern": "governing-predicate",
            "sin_dst": "sine destination",
            "cos_dst": "cosine destination",
        }
        return special.get(role, role.replace("_", "-"))

    @staticmethod
    def _allowed_values(form: "EncodingForm", role: str) -> set[int]:
        allowed: set[int] = set()
        for constraint in form.constraints:
            if constraint.role != role:
                continue
            for item in constraint.allow:
                if isinstance(item, int):
                    allowed.add(item)
                    continue
                bounds = item.split("..", maxsplit=1)
                low = int(bounds[0], 0)
                high = int(bounds[-1], 0)
                allowed.update(range(low, high + 1))
        return allowed

    @staticmethod
    def _value_ranges(values: set[int]) -> str:
        runs: list[tuple[int, int]] = []
        start = previous = min(values)
        for value in sorted(values)[1:]:
            if value == previous + 1:
                previous = value
                continue
            runs.append((start, previous))
            start = previous = value
        runs.append((start, previous))
        return ", ".join(
            str(low) if low == high else f"{low}-{high}"
            for low, high in runs
        )

    @classmethod
    def _instruction_diagram(cls, form: "EncodingForm") -> str:
        byte_segments = cls._instruction_bytes(form)
        fields: list[str] = []
        for byte_index, segments in enumerate(byte_segments):
            if byte_index:
                fields.append(r"\BedrockBitGap{1}")
            for label, width in segments:
                macro = (
                    "BedrockBitFixed"
                    if set(label) <= {"0", "1"}
                    else "BedrockBitVariable"
                )
                fields.append(rf"\{macro}{{{tex_escape(label)}}}{{{width}}}")
        return "\n".join(
            [
                rf"\begin{{BedrockBitDiagram}}{{Format: Instruction format for "
                rf"{tex_escape(form.syntax.code)}}}",
                rf"\BedrockBitFieldRow{{}}{{\BedrockByteRowLabels{{0}}"
                rf"{{{len(byte_segments)}}}}}{{%",
                *fields,
                "}",
                r"\end{BedrockBitDiagram}",
            ]
        )

    @classmethod
    def _instruction_bytes(
        cls, form: "EncodingForm"
    ) -> list[list[tuple[str, int]]]:
        pattern = form.pattern.code
        width = form.pattern.bit_width
        if width == 7:
            segments = [("0", 1), *cls._bit_segments(pattern)]
            first, remaining = cls._split_segments(segments, 8)
            byte_segments = [first]
        elif width == 14:
            segments = [("10", 2), *cls._bit_segments(pattern)]
            first, second = cls._split_segments(segments, 8)
            byte_segments = [first, second]
            remaining = []
        elif width in {18, 26, 34, 42}:
            header = [("11", 2), ("L", 4), *cls._bit_segments(pattern[:10])]
            first, second = cls._split_segments(header, 8)
            byte_segments = [first, second]
            remaining_pattern = pattern[10:]
            while remaining_pattern:
                byte_segments.append(cls._bit_segments(remaining_pattern[:8]))
                remaining_pattern = remaining_pattern[8:]
            remaining = []
        else:
            raise ValueError(
                f"encoding form {form.id!r} has unsupported primary width {width}"
            )
        if remaining:
            raise ValueError(
                f"encoding form {form.id!r} does not end at a byte boundary"
            )
        for byte_index, byte in enumerate(byte_segments):
            byte_width = sum(segment_width for _label, segment_width in byte)
            if byte_width != 8:
                raise ValueError(
                    f"encoding form {form.id!r} byte {byte_index} has "
                    f"{byte_width} bits; expected 8"
                )
        return byte_segments

    @staticmethod
    def _bit_segments(bits: str) -> list[tuple[str, int]]:
        if not bits:
            return []
        segments: list[tuple[str, int]] = []
        start = 0

        def segment_class(character: str) -> str:
            return "fixed" if character in "01" else character

        current = segment_class(bits[0])
        for index, character in enumerate(bits[1:], start=1):
            kind = segment_class(character)
            if kind == current:
                continue
            chunk = bits[start:index]
            segments.append(
                (chunk if current == "fixed" else chunk[0], len(chunk))
            )
            start = index
            current = kind
        chunk = bits[start:]
        segments.append((chunk if current == "fixed" else chunk[0], len(chunk)))
        return segments

    @staticmethod
    def _split_segments(
        segments: list[tuple[str, int]], width: int
    ) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
        left: list[tuple[str, int]] = []
        right: list[tuple[str, int]] = []
        remaining = width
        for label, segment_width in segments:
            if remaining <= 0:
                right.append((label, segment_width))
            elif segment_width <= remaining:
                left.append((label, segment_width))
                remaining -= segment_width
            else:
                left_label = label
                right_label = label
                if len(label) == segment_width and set(label) <= {"0", "1"}:
                    left_label = label[:remaining]
                    right_label = label[remaining:]
                left.append((left_label, remaining))
                right.append((right_label, segment_width - remaining))
                remaining = 0
        return left, right


class LatexDocumentRenderer:
    """Render one validated composition into a monolithic TeX source."""

    def __init__(
        self,
        instruction: InstructionEntryRenderer | None = None,
        terms: TermGroupRenderer | None = None,
        fragments: DocumentFragmentPipeline | None = None,
    ) -> None:
        self.instruction = instruction or InstructionEntryRenderer()
        self.terms = terms or TermGroupRenderer()
        self.fragments = fragments or DocumentFragmentPipeline.default()
        self.dependencies = DependencyGraph()
        self.sources = LatexSourcePreprocessor(
            self.fragments, self.terms.semantic, self.dependencies
        )

    def render(self, composition: DocumentComposition, project) -> str:
        self.dependencies.clear()
        artifact: Reference[Entity] = Reference(
            "base", ("artifacts",), composition.artifact
        )
        parts = [
            self.sources.render(composition.preamble, project, artifact),
            self.sources.render(composition.title_page, project, artifact),
        ]
        for block in composition.blocks:
            if isinstance(block, TopicBlock):
                parts.extend(
                    [
                        f"% topic: {block.topic.id}",
                        self._topic(block.topic, project),
                    ]
                )
            elif isinstance(block, TermGroupBlock):
                parts.extend(
                    [
                        f"% term-group: {block.group.id}",
                        self.terms.render(block.group, project, self.dependencies),
                    ]
                )
            elif isinstance(block, InstructionSetBlock):
                slug = re.sub(r"[^a-z0-9]+", "-", block.owner.lower()).strip("-")
                parts.extend(
                    [
                        f"% instruction-set: {block.owner}",
                        r"\clearpage",
                        rf"\section{{{tex_escape(block.title)}}}",
                        rf"\label{{page:instruction-group-{slug}}}",
                        *(
                            item
                            for topic in block.introduction
                            for item in (
                                f"% topic: {topic.id}",
                                self._topic(topic, project),
                            )
                        ),
                        *(
                            self.instruction.render(
                                bundle,
                                project.types,
                                self.sources.render(
                                    bundle.artifacts.description,
                                    project,
                                    bundle.reference,
                                ),
                            )
                            for bundle in block.instructions
                        ),
                    ]
                )
        parts.append(self.sources.render(composition.postamble, project, artifact))
        return "\n\n".join(parts) + "\n"

    def _topic(self, topic, project) -> str:
        reference = topic.reference
        rendered = self.sources.render(topic.document, project, reference)
        anchor = rf"\phantomsection\label{{{_entity_label(project, reference)}}}"
        heading = re.compile(
            r"(\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"
            r"(?:\\label\{[^{}]*\})*)"
        )
        return heading.sub(lambda match: match.group(1) + anchor, rendered, count=1)
