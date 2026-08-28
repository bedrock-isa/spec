"""Pure LaTeX renderers for the ISA reference document."""

from __future__ import annotations

from itertools import groupby
import re

from ..dependency import DependencyGraph
from ..entity import (
    EntityDisplayStyle,
    entity_label,
    instruction_label,
    term_group_label as entity_term_group_label,
    term_label as entity_term_label,
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
from .document_fragment import DocumentFragmentPipeline
from .latex_source import LatexSourcePreprocessor


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


def term_group_label(group: TermGroup) -> str:
    return entity_term_group_label(group.reference)


def term_label(term: Term) -> str:
    return entity_term_label(term.reference)


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
                        f"{text.origin.source}: no entity catalog is available for "
                        f"{part.reference}"
                    )
                entity = entities.resolve(part.reference)
                if entity.latex_label is None:
                    raise ValueError(
                        f"{text.origin.source}: entity {part.reference} "
                        "has no target in this LaTeX artifact"
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
            display = self._term_form(term, part.form)
            parts.append(
                rf"\hyperref[{term_label(term)}]{{{tex_escape(display)}}}"
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
            f"term {term.reference} does not define form {form.value!r}"
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
                rf"\label{{{term_group_label(group)}}}",
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
            rf"\phantomsection\label{{{term_label(term)}}}" + "\n"
            + f"{subject} is {definition}"
        )


class InstructionEntryRenderer:
    """Render one instruction bundle from the current typed model."""

    def render(self, bundle: InstructionBundle, description: str | None = None) -> str:
        instruction = bundle.instruction
        mnemonic = instruction.mnemonic
        parts = [
            r"\clearpage",
            rf"\begin{{manualinstruction}}{{{tex_escape(mnemonic)}}}"
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
                        tex_code(field.reference)
                        for field in bundle.required_cpuid_flags
                    ),
                )
            )
        repeat = instruction.to_dict().get("repeat")
        if repeat:
            text = "REP eligible"
            if repeat["type"] == "repcc":
                text += "; REPcc observes " + tex_code(repeat["observed_value"])
            parts.append(self._field("Repeat eligibility", text))
        parts.append(self._operand_block(bundle))
        if description is None:
            description = bundle.artifacts.description.read_text(
                encoding="utf-8"
            ).strip()
        parts.extend(
            [
                r"\manualinstructiondescriptionheading{Detailed Semantics}",
                description,
                self._forms(bundle),
                r"\end{manualinstruction}",
            ]
        )
        return "\n".join(part for part in parts if part)

    @staticmethod
    def _field(label: str, value: str) -> str:
        return rf"\manualoperationfield{{{tex_escape(label)}}}{{{value}}}"

    @staticmethod
    def _ragged(lines) -> str:
        rendered = "".join(rf"\noindent {line}\par " for line in lines)
        return rf"\begin{{manualraggedblock}}{rendered}\end{{manualraggedblock}}"

    def _operand_block(self, bundle: InstructionBundle) -> str:
        operands = bundle.instruction.to_dict()["operands"]
        lines = []
        for name, operand in operands.items():
            details = ", ".join(
                str(operand[key]).replace("_", " ")
                for key in ("role", "access", "value_type")
            )
            lines.append(tex_code(name) + ": " + tex_escape(details))
        return self._field("Logical operands", self._ragged(lines))

    def _forms(self, bundle: InstructionBundle) -> str:
        blocks = [r"\begin{manualinstructionforms}", r"\manualinstructionformsheading"]
        for form in bundle.encodings.forms:
            blocks.extend(
                [
                    r"\begin{manualformblock}{2.75in}",
                    rf"\textbf{{{tex_code(form.syntax.code)}}}\par",
                    r"\manualinstructionformatheading",
                    rf"Allocation pattern: {tex_code(form.pattern.code)}\par",
                    self._pattern_diagram(form.syntax.code, form.pattern.code),
                ]
            )
            if form.fields or form.payloads or form.constraints or form.overlaps:
                blocks.append(r"\manualinstructionfieldsheading")
            for field in form.fields:
                blocks.append(
                    rf"\manualinstructionfielddescription{{{tex_code(field.marker)}}}"
                    rf"{{{tex_code(field.role)}; {tex_code(field.type)}}}"
                )
            for payload in form.payloads:
                blocks.append(
                    rf"\manualinstructionfielddescription{{Payload}}"
                    rf"{{{tex_code(payload.role)}; {tex_code(payload.type)}}}"
                )
            for constraint in form.constraints:
                values = constraint.allow or constraint.exclude
                verb = "allows" if constraint.allow else "excludes"
                blocks.append(
                    rf"\manualinstructionfielddescription{{Constraint}}"
                    rf"{{{tex_code(constraint.role)} {verb} "
                    + ", ".join(tex_code(value) for value in values)
                    + rf" ({tex_code(constraint.reason)})}}"
                )
            for overlap in form.overlaps:
                blocks.append(
                    rf"\manualinstructionfielddescription{{Operand overlap}}"
                    rf"{{{tex_code(overlap.operands[0])} and "
                    rf"{tex_code(overlap.operands[1])}: {tex_code(overlap.type)}}}"
                )
            blocks.append(r"\end{manualformblock}")
        blocks.append(r"\end{manualinstructionforms}")
        return "\n".join(blocks)

    @staticmethod
    def _pattern_diagram(syntax: str, pattern: str) -> str:
        fields = []
        for character, run in groupby(pattern):
            width = len(tuple(run))
            if character in "01":
                fields.append(rf"\manualbitfixed{{{character * width}}}{{{width}}}")
            else:
                fields.append(rf"\manualbitfieldcode{{{character}}}{{{width}}}")
        return "\n".join(
            [
                rf"\begin{{manualbitdiagram}}{{Allocation bits for {tex_escape(syntax)}}}",
                rf"\manualbitrow{{allocation[{len(pattern) - 1}:0]}}{{%",
                *fields,
                "}",
                r"\end{manualbitdiagram}",
            ]
        )


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
        artifact = Reference("base", ("artifacts",), composition.artifact)
        parts = [
            self.sources.render(composition.preamble, project, artifact),
            self.sources.render(composition.title_page, project, artifact),
        ]
        for block in composition.blocks:
            if isinstance(block, TopicBlock):
                parts.extend(
                    [
                        f"% topic: {block.topic.reference}",
                        self._topic(block.topic, project),
                    ]
                )
            elif isinstance(block, TermGroupBlock):
                parts.extend(
                    [
                        f"% term-group: {block.group.reference}",
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
                                f"% topic: {topic.reference}",
                                self._topic(topic, project),
                            )
                        ),
                        *(
                            self.instruction.render(
                                bundle,
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
        reference = Reference.parse(topic.reference)
        rendered = self.sources.render(topic.document, project, reference)
        anchor = rf"\phantomsection\label{{{entity_label(reference)}}}"
        heading = re.compile(
            r"(\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"
            r"(?:\\label\{[^{}]*\})*)"
        )
        return heading.sub(lambda match: match.group(1) + anchor, rendered, count=1)
