"""Pure LaTeX renderers for the ISA reference document."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from typing import TYPE_CHECKING

from ..dependency import DependencyGraph
from ..entity import (
    Entity,
    EntityDisplayStyle,
    PublicTargetCatalog,
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
from ..model import DocumentTopic
from ..semantic_text import (
    EntityReferenceText,
    LiteralText,
    SemanticText,
    TermForm,
    TermReferenceText,
    TextOrigin,
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


def _label_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


_LOCAL_INPUT_RE = re.compile(r"\\input\{((?!/)(?![^}]*\.\.)[^}]+)\}")
_SEMANTIC_REFERENCE_RE = re.compile(
    r"\(:(?:ref|term)(?:\[[a-z]+\])?:[^:\n]+:\)"
)


def _authored_semantic_references(
    composition: DocumentComposition, project
) -> frozenset[Reference[object]]:
    """Collect references actually authored into this document projection."""

    references: set[Reference[object]] = set()
    repository = project.root.parent.resolve()
    visited: set[Path] = set()

    def collect_semantic(semantic: SemanticText) -> None:
        for part in semantic.parts:
            if isinstance(part, (EntityReferenceText, TermReferenceText)):
                references.add(part.reference)

    def collect_source(source: Path) -> None:
        path = source.resolve()
        if path in visited:
            return
        visited.add(path)
        text = path.read_text(encoding="utf-8")
        if path.suffix != ".sty":
            for match in _SEMANTIC_REFERENCE_RE.finditer(text):
                collect_semantic(
                    SemanticText.parse(match.group(0), origin=TextOrigin(path))
                )
        for match in _LOCAL_INPUT_RE.finditer(text):
            included = (repository / match.group(1)).resolve()
            if included.suffix == "":
                included = included.with_suffix(".tex")
            if not included.is_relative_to(repository) or not included.is_file():
                raise RuntimeError(f"cannot inspect TeX source {match.group(1)!r}")
            collect_source(included)

    collect_source(composition.preamble)
    collect_source(composition.title_page)
    collect_source(composition.postamble)
    for block in composition.blocks:
        if isinstance(block, TopicBlock):
            collect_source(block.topic.document)
        elif isinstance(block, TermGroupBlock):
            for term in block.group.terms.values():
                collect_semantic(term.definition)
        elif isinstance(block, InstructionSetBlock):
            for topic in block.introduction:
                collect_source(topic.document)
            for bundle in block.instructions:
                collect_source(bundle.artifacts.description)
    return frozenset(references)


def _document_public_targets(
    composition: DocumentComposition, project
) -> PublicTargetCatalog:
    targets: list[tuple[Reference[object], str]] = []
    referenced = _authored_semantic_references(composition, project)

    for block in composition.blocks:
        if isinstance(block, TermGroupBlock):
            targets.extend(TermGroupRenderer.public_targets(block.group, referenced))
        elif isinstance(block, InstructionSetBlock):
            for bundle in block.instructions:
                targets.append(
                    (bundle.reference, instruction_label(bundle.instruction.mnemonic))
                )

    # Import locally because the event projector also uses TeX escaping from this
    # module.  It owns its public row labels; this composer only supplies the
    # references actually requested by authored prose.
    from .event_reference import EventReferenceRenderer

    targets.extend(EventReferenceRenderer.public_targets(project, referenced))

    return PublicTargetCatalog.create(project.entities, targets)


class LatexSemanticTextRenderer:
    """Render resolved terminology references inside SemanticText to LaTeX."""

    def render(
        self,
        text: SemanticText,
        catalog: TermCatalog,
        *,
        public_targets: PublicTargetCatalog,
        escape_literals: bool = True,
    ) -> str:
        parts: list[str] = []
        for part in text.parts:
            if isinstance(part, LiteralText):
                parts.append(tex_escape(part.value) if escape_literals else part.value)
                continue
            if isinstance(part, EntityReferenceText):
                entity, label = public_targets.resolve(part.reference)
                display = (
                    tex_code(entity.display)
                    if entity.display_style is EntityDisplayStyle.CODE
                    else tex_escape(entity.display)
                )
                parts.append(rf"\hyperref[{label}]{{{display}}}")
                continue
            assert isinstance(part, TermReferenceText)
            term = catalog.references.terms.resolve(part.reference)
            display = self._term_form(term, part.form)
            parts.append(
                rf"\hyperref[{public_targets.label(term.reference)}]"
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

    @staticmethod
    def public_targets(
        group: TermGroup, referenced: frozenset[Reference[object]]
    ) -> tuple[tuple[Reference[object], str], ...]:
        """Declare only terminology entries targeted by authored prose."""

        targets: list[tuple[Reference[object], str]] = []
        if group.reference in referenced:
            targets.append((group.reference, f"term-group:{_label_slug(group.id)}"))
        targets.extend(
            (term.reference, f"term:{_label_slug(term.id)}")
            for term in group.terms.values()
            if term.reference in referenced
        )
        return tuple(targets)

    def render(
        self,
        group: TermGroup,
        project,
        public_targets: PublicTargetCatalog,
        dependencies=None,
    ) -> str:
        heading = rf"\subsection{{{tex_escape(group.title)}}}"
        if public_targets.contains(group.reference):
            heading += rf"\label{{{public_targets.label(group.reference)}}}"
        return "\n\n".join(
            (
                heading,
                *(
                    self._term(term, project, public_targets, dependencies)
                    for term in group.terms.values()
                ),
            )
        )

    def _term(
        self,
        term: Term,
        project,
        public_targets: PublicTargetCatalog,
        dependencies=None,
    ) -> str:
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
            public_targets=public_targets,
        )
        anchor = ""
        if public_targets.contains(term.reference):
            anchor = (
                rf"\phantomsection\label{{{public_targets.label(term.reference)}}}"
                + "\n"
            )
        return anchor + f"{subject} is {definition}"


@dataclass(frozen=True, slots=True)
class InstructionBitSegment:
    label: str
    width: int
    fixed: bool


@dataclass(frozen=True, slots=True)
class InstructionByteProjection:
    index: int
    segments: tuple[InstructionBitSegment, ...]


@dataclass(frozen=True, slots=True)
class InstructionFormatProjection:
    """One instruction form split into its reader-facing byte layout."""

    form: "EncodingForm"
    bytes: tuple[InstructionByteProjection, ...]


class InstructionEntryRenderer:
    """Render one instruction bundle from the current typed model."""

    def render(
        self,
        bundle: InstructionBundle,
        types: "TypeSystem",
        description: str | None = None,
        formats: tuple[InstructionFormatProjection, ...] | None = None,
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
                self._forms(bundle, types, formats or self.project_formats(bundle)),
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

    @classmethod
    def project_formats(
        cls, bundle: InstructionBundle
    ) -> tuple[InstructionFormatProjection, ...]:
        return tuple(
            InstructionFormatProjection(
                form,
                tuple(
                    InstructionByteProjection(
                        index,
                        tuple(
                            InstructionBitSegment(
                                label,
                                width,
                                set(label) <= {"0", "1"},
                            )
                            for label, width in segments
                        ),
                    )
                    for index, segments in enumerate(cls._instruction_bytes(form))
                ),
            )
            for form in bundle.encodings.forms
        )

    def _forms(
        self,
        bundle: InstructionBundle,
        types: "TypeSystem",
        formats: tuple[InstructionFormatProjection, ...],
    ) -> str:
        blocks = [r"\begin{BedrockInstructionForms}"]
        for index, projected in enumerate(formats):
            form = projected.form
            blocks.extend(
                [
                    r"\begin{BedrockFormBlock}{2.75in}",
                    *([r"\BedrockInstructionFormsHeading"] if index == 0 else []),
                    rf"\textbf{{{tex_code(form.syntax.code)}}}\par",
                    r"\BedrockInstructionFormatHeading",
                    self._instruction_diagram(projected),
                ]
            )
            if form.additional_cpuid_flags:
                blocks.append(
                    r"\par\Needspace{0.36in}\noindent"
                    r"\textbf{Additional CPUID flags:}\enspace "
                    + ", ".join(
                        tex_code(field.id) for field in form.additional_cpuid_flags
                    )
                    + r"\par"
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
    def _instruction_diagram(cls, projected: InstructionFormatProjection) -> str:
        form = projected.form
        fields: list[str] = []
        for byte_index, byte in enumerate(projected.bytes):
            if byte_index:
                fields.append(r"\BedrockBitGap{1}")
            for segment in byte.segments:
                macro = "BedrockBitFixed" if segment.fixed else "BedrockBitVariable"
                fields.append(
                    rf"\{macro}{{{tex_escape(segment.label)}}}{{{segment.width}}}"
                )
        return "\n".join(
            [
                rf"\begin{{BedrockBitDiagram}}{{Format: Instruction format for "
                rf"{tex_escape(form.syntax.code)}}}",
                rf"\BedrockBitFieldRow{{}}{{\BedrockByteRowLabels{{0}}"
                rf"{{{len(projected.bytes)}}}}}{{%",
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


@dataclass(frozen=True, slots=True)
class ProjectedTopic:
    """One authored topic selected into the document projection."""

    topic: DocumentTopic
    content: str


@dataclass(frozen=True, slots=True)
class ProjectedTermGroup:
    """One selected terminology group and its rendered body."""

    block: TermGroupBlock
    content: str


@dataclass(frozen=True, slots=True)
class ProjectedInstructionEntry:
    """One selected instruction and its rendered body."""

    bundle: InstructionBundle
    formats: tuple[InstructionFormatProjection, ...]
    content: str


@dataclass(frozen=True, slots=True)
class InstructionSummaryRow:
    """One immediate instruction member in an owner-scoped public summary."""

    reference: Reference[InstructionBundle]
    mnemonic: str
    description: str
    target: str


@dataclass(frozen=True, slots=True)
class InstructionSetSummaryProjection:
    """The navigation summary owned by one public instruction-set section."""

    caption: str
    rows: tuple[InstructionSummaryRow, ...]


@dataclass(frozen=True, slots=True)
class ProjectedInstructionSet:
    """One instruction-set block with its immediate public members."""

    block: InstructionSetBlock
    summary: InstructionSetSummaryProjection
    introduction: tuple[ProjectedTopic, ...]
    instructions: tuple[ProjectedInstructionEntry, ...]


ProjectedDocumentBlock = ProjectedTopic | ProjectedTermGroup | ProjectedInstructionSet


@dataclass(frozen=True, slots=True)
class DocumentProjection:
    """The complete reader-facing selection before TeX serialization."""

    composition: DocumentComposition
    preamble: str
    title_page: str
    blocks: tuple[ProjectedDocumentBlock, ...]
    postamble: str


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

    @staticmethod
    def public_targets(
        composition: DocumentComposition, project
    ) -> PublicTargetCatalog:
        return _document_public_targets(composition, project)

    def project(
        self, composition: DocumentComposition, project
    ) -> DocumentProjection:
        self.dependencies.clear()
        public_targets = self.public_targets(composition, project)
        artifact: Reference[Entity] = Reference(
            "base", ("artifacts",), composition.artifact
        )
        projected: list[ProjectedDocumentBlock] = []
        for block in composition.blocks:
            if isinstance(block, TopicBlock):
                projected.append(
                    ProjectedTopic(
                        block.topic,
                        self._topic(block.topic, project, public_targets),
                    )
                )
            elif isinstance(block, TermGroupBlock):
                projected.append(
                    ProjectedTermGroup(
                        block,
                        self.terms.render(
                            block.group,
                            project,
                            public_targets,
                            self.dependencies,
                        ),
                    )
                )
            elif isinstance(block, InstructionSetBlock):
                projected.append(
                    ProjectedInstructionSet(
                        block,
                        self._instruction_summary(block, public_targets),
                        tuple(
                            ProjectedTopic(
                                topic,
                                self._topic(topic, project, public_targets),
                            )
                            for topic in block.introduction
                        ),
                        tuple(
                            self._instruction_entry(
                                bundle, project, public_targets
                            )
                            for bundle in block.instructions
                        ),
                    )
                )
        return DocumentProjection(
            composition,
            self.sources.render(
                composition.preamble, project, public_targets, artifact
            ),
            self.sources.render(
                composition.title_page, project, public_targets, artifact
            ),
            tuple(projected),
            self.sources.render(
                composition.postamble, project, public_targets, artifact
            ),
        )

    def render(self, composition: DocumentComposition, project) -> str:
        projection = self.project(composition, project)
        parts = [projection.preamble, projection.title_page]
        for projected in projection.blocks:
            if isinstance(projected, ProjectedTopic):
                parts.extend(
                    [
                        f"% topic: {projected.topic.id}",
                        projected.content,
                    ]
                )
            elif isinstance(projected, ProjectedTermGroup):
                parts.extend(
                    [
                        f"% term-group: {projected.block.group.id}",
                        projected.content,
                    ]
                )
            elif isinstance(projected, ProjectedInstructionSet):
                block = projected.block
                slug = re.sub(r"[^a-z0-9]+", "-", block.owner.lower()).strip("-")
                parts.extend(
                    [
                        f"% instruction-set: {block.owner}",
                        r"\clearpage",
                        rf"\section{{{tex_escape(block.title)}}}",
                        rf"\label{{page:instruction-group-{slug}}}",
                        self._render_instruction_summary(projected.summary),
                        *(
                            item
                            for topic in projected.introduction
                            for item in (
                                f"% topic: {topic.topic.id}",
                                topic.content,
                            )
                        ),
                        *(entry.content for entry in projected.instructions),
                    ]
                )
        parts.append(projection.postamble)
        return "\n\n".join(parts) + "\n"

    def _topic(
        self, topic, project, public_targets: PublicTargetCatalog
    ) -> str:
        return self.sources.render(
            topic.document, project, public_targets, topic.reference
        )

    def _instruction_entry(
        self,
        bundle: InstructionBundle,
        project,
        public_targets: PublicTargetCatalog,
    ) -> ProjectedInstructionEntry:
        formats = self.instruction.project_formats(bundle)
        description = self.sources.render(
            bundle.artifacts.description,
            project,
            public_targets,
            bundle.reference,
        )
        return ProjectedInstructionEntry(
            bundle,
            formats,
            self.instruction.render(
                bundle,
                project.types,
                description,
                formats,
            ),
        )

    @staticmethod
    def _instruction_summary(
        block: InstructionSetBlock,
        public_targets: PublicTargetCatalog,
    ) -> InstructionSetSummaryProjection:
        return InstructionSetSummaryProjection(
            f"{block.title} Summary (Informative)",
            tuple(
                InstructionSummaryRow(
                    bundle.reference,
                    bundle.instruction.mnemonic,
                    bundle.instruction.summary,
                    public_targets.label(bundle.reference),
                )
                for bundle in block.instructions
            ),
        )

    @staticmethod
    def _render_instruction_summary(
        projection: InstructionSetSummaryProjection,
    ) -> str:
        rows = (
            rf"\BedrockSummaryMnemonic{{{row.target}}}"
            rf"{{{tex_escape(row.mnemonic)}}} & "
            rf"{tex_escape(row.description)}\\"
            for row in projection.rows
        )
        header = (
            r"\toprule",
            r"\rowcolor{BedrockHeaderFill}",
            r"\textbf{Mnemonic} & \textbf{Brief description}\\",
            r"\midrule",
        )
        return "\n".join(
            (
                r"\subsection{Summary}",
                rf"\BedrockTableCaption{{{tex_escape(projection.caption)}}}",
                r"\begin{BedrockLongTable}{@{}>{\raggedright\arraybackslash}p{1.05in}>{\raggedright\arraybackslash}p{4.35in}@{}}",
                *header,
                r"\endfirsthead",
                r"\multicolumn{2}{l}{\scriptsize\itshape Table \theBedrockTable\ (continued)}\\",
                *header,
                r"\endhead",
                *rows,
                r"\bottomrule",
                r"\end{BedrockLongTable}",
            )
        )
