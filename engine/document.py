"""TeX validation and gated PDF compilation for the ISA reference."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import tempfile

from .composition import DocumentComposition, InstructionSetBlock, TopicBlock
from .document_pipeline import (
    LatexCompiler,
    PdfArtifactValidator,
)
from .generation import (
    ArtifactGenerationContext,
    ArtifactGenerator,
    ArtifactGeneratorRegistry,
    ArtifactWriter,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from .project import IsaProject
from .workspace import SpecWorkspace


PLACEHOLDER_RE = re.compile(r"@[A-Z0-9_]+@")
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
HYPER_REFERENCE_RE = re.compile(r"\\hyperref\[([^\]]+)\]")
STANDARD_REFERENCE_RE = re.compile(r"\\(?:auto|page)?ref\{([^{}]+)\}")
INSTRUCTION_TARGET_RE = re.compile(
    r"^\\begin\{BedrockInstruction\}.*\{([^{}\n]+)\}\s*$", re.MULTILINE
)
INSTRUCTION_BLOCK_RE = re.compile(
    r"\\begin\{BedrockInstruction\}.*?\\end\{BedrockInstruction\}",
    re.DOTALL,
)
LISTED_DIAGRAM_TARGET_RE = re.compile(
    r"^\\begin\{BedrockListed(?:Bit|Format)Diagram\}.*\[([^\]\n]+)\]\s*$",
    re.MULTILINE,
)
SUMMARY_REFERENCE_RE = re.compile(r"\\BedrockSummaryMnemonic\{([^{}]+)\}")


@dataclass(frozen=True, slots=True)
class TexValidationReport:
    passed: bool
    errors: tuple[str, ...]
    quantitative: dict[str, object]
    qualitative_review: dict[str, object]

    def render_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


class TexValidator:
    """Validate structure derived from the current specification model."""

    def validate(
        self,
        tex: str,
        *,
        expected_topics: int,
        expected_forms: int,
    ) -> TexValidationReport:
        errors: list[str] = []
        topic_count = tex.count("% topic:")
        if topic_count != expected_topics:
            errors.append(f"rendered {topic_count} topics; expected {expected_topics}")
        form_count = sum(
            block.count(r"\begin{BedrockFormBlock}")
            for block in INSTRUCTION_BLOCK_RE.findall(tex)
        )
        if form_count != expected_forms:
            errors.append(f"rendered {form_count} forms; expected {expected_forms}")
        if tex.count(r"\begin{document}") != 1 or tex.count(r"\end{document}") != 1:
            errors.append("TeX must contain exactly one document environment")
        placeholders = sorted(set(PLACEHOLDER_RE.findall(tex)))
        if placeholders:
            errors.append(f"unresolved TeX placeholders: {placeholders}")
        targets = (
            LABEL_RE.findall(tex)
            + INSTRUCTION_TARGET_RE.findall(tex)
            + LISTED_DIAGRAM_TARGET_RE.findall(tex)
        )
        duplicate_targets = sorted(
            target for target, count in Counter(targets).items() if count > 1
        )
        if duplicate_targets:
            errors.append(f"duplicate public TeX targets: {duplicate_targets}")
        references = set(
            HYPER_REFERENCE_RE.findall(tex)
            + STANDARD_REFERENCE_RE.findall(tex)
            + SUMMARY_REFERENCE_RE.findall(tex)
        )
        missing_targets = sorted(references.difference(targets))
        if missing_targets:
            errors.append(f"unresolved public TeX targets: {missing_targets}")
        return TexValidationReport(
            passed=not errors,
            errors=tuple(errors),
            quantitative={
                "bytes": len(tex),
                "new_topics": topic_count,
                "new_encoding_forms": form_count,
                "public_targets": len(set(targets)),
                "public_references": len(references),
            },
            qualitative_review={},
        )


@dataclass(frozen=True, slots=True)
class DocumentBuildResult:
    report: TexValidationReport
    tex: Path
    report_path: Path
    pdf: Path | None = None
    log: Path | None = None
    pdf_report: Path | None = None


class DocumentBuilder:
    """Generate, validate, and conditionally compile the ISA reference."""

    def __init__(
        self,
        generator: ArtifactGenerator | None = None,
        validator: TexValidator | None = None,
        writer: ArtifactWriter | None = None,
        compiler: LatexCompiler | None = None,
        pdf_validator: PdfArtifactValidator | None = None,
    ) -> None:
        self.generator = generator
        self.validator = validator or TexValidator()
        self.writer = writer or ArtifactWriter()
        self.compiler = compiler or LatexCompiler()
        self.pdf_validator = pdf_validator or PdfArtifactValidator()

    def build(
        self,
        workspace: SpecWorkspace,
        output_root: str | Path,
        *,
        compile_pdf: bool,
        latexmk: str = "latexmk",
    ) -> DocumentBuildResult:
        provider = workspace.require_provider("isa")
        if not isinstance(provider, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        project = provider
        output = Path(output_root).resolve()
        repository = workspace.root
        if output in {Path("/").resolve(), Path.home().resolve(), repository}:
            raise ValueError(f"refusing unsafe document output root: {output}")
        generator = self.generator
        if generator is None:
            discovered = ArtifactGeneratorRegistry.discover(workspace).generator(
                "isa-reference"
            )
            generator = discovered
        context = ArtifactGenerationContext.create(workspace, output)
        generated = generator.generate(context)
        generator.definition.validate_generated(generated)
        document_output = generator.definition.outputs["document"]
        tex = generated.artifact(document_output).content
        if not isinstance(tex, str):
            raise TypeError("ISA reference TeX artifact must be text")
        composition = DocumentComposition.load(generator.definition.source, project)
        expected_topics = sum(
            1
            if isinstance(block, TopicBlock)
            else len(block.introduction)
            if isinstance(block, InstructionSetBlock)
            else 0
            for block in composition.blocks
        )
        expected_forms = sum(
            len(bundle.encodings.forms)
            for block in composition.blocks
            if isinstance(block, InstructionSetBlock)
            for bundle in block.instructions
        )
        report = self.validator.validate(
            tex,
            expected_topics=expected_topics,
            expected_forms=expected_forms,
        )
        derived = generator.definition.derived_outputs
        validated = GeneratedArtifactSet(
            (
                *generated.artifacts,
                GeneratedArtifact(derived["tex-validation"], report.render_json()),
            ),
            artifact_id=generator.artifact_id,
        )
        generator.definition.validate_owned(validated)
        self.writer.write(validated, output)
        tex_path = output / document_output
        report_path = output / derived["tex-validation"]
        result = DocumentBuildResult(report, tex_path, report_path)
        if not compile_pdf or not report.passed:
            return result
        with tempfile.TemporaryDirectory(prefix="bedrock-document-build-") as directory:
            compiled = self.compiler.compile(
                tex_path, Path(directory), repository, latexmk
            )
            pdf_metrics = self.pdf_validator.validate(compiled)
            published = GeneratedArtifactSet(
                (
                    *validated.artifacts,
                    GeneratedArtifact(
                        derived["compiled-document"], compiled.pdf.read_bytes()
                    ),
                    GeneratedArtifact(
                        derived["compile-log"], compiled.log.read_bytes()
                    ),
                    GeneratedArtifact(
                        derived["pdf-validation"],
                        json.dumps(pdf_metrics, indent=2, sort_keys=True) + "\n",
                    ),
                ),
                artifact_id=generator.artifact_id,
            )
            generator.definition.validate_owned(published)
            self.writer.write(published, output)
            pdf = output / derived["compiled-document"]
            log = output / derived["compile-log"]
            pdf_report = output / derived["pdf-validation"]
        return DocumentBuildResult(
            report,
            tex_path,
            report_path,
            pdf,
            log,
            pdf_report,
        )
