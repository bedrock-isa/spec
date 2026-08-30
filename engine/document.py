"""TeX validation and gated PDF compilation for the ISA reference."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

from .composition import DocumentComposition
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


PLACEHOLDER_RE = re.compile(r"@[A-Z0-9_]+@")


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
        form_count = tex.count(r"\begin{BedrockFormBlock}")
        if form_count != expected_forms:
            errors.append(f"rendered {form_count} forms; expected {expected_forms}")
        if tex.count(r"\begin{document}") != 1 or tex.count(r"\end{document}") != 1:
            errors.append("TeX must contain exactly one document environment")
        placeholders = sorted(set(PLACEHOLDER_RE.findall(tex)))
        if placeholders:
            errors.append(f"unresolved TeX placeholders: {placeholders}")
        return TexValidationReport(
            passed=not errors,
            errors=tuple(errors),
            quantitative={
                "bytes": len(tex),
                "new_topics": topic_count,
                "new_encoding_forms": form_count,
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
        project: IsaProject,
        output_root: str | Path,
        *,
        compile_pdf: bool,
        latexmk: str = "latexmk",
    ) -> DocumentBuildResult:
        output = Path(output_root).resolve()
        repository = project.root.parent.resolve()
        if output in {Path("/").resolve(), Path.home().resolve(), repository}:
            raise ValueError(f"refusing unsafe document output root: {output}")
        generator = self.generator
        if generator is None:
            discovered = ArtifactGeneratorRegistry.discover(project).generator(
                "isa-reference"
            )
            generator = discovered
        context = ArtifactGenerationContext.create(project, output)
        tex = generator.generate(context).artifact(
            "tex/isa-reference.tex"
        ).content
        composition = DocumentComposition.load(generator.definition.source, project)
        expected_forms = sum(
            len(bundle.encodings.forms) for bundle in project.select()
        )
        report = self.validator.validate(
            tex,
            expected_topics=len(project.model.document_orders[composition.artifact]),
            expected_forms=expected_forms,
        )
        artifacts = GeneratedArtifactSet(
            (
                GeneratedArtifact(Path("tex/isa-reference.tex"), tex),
                GeneratedArtifact(Path("tex/isa-reference-validate.json"), report.render_json()),
            )
        )
        written = self.writer.write(artifacts, output)
        tex_path, report_path = written
        result = DocumentBuildResult(report, tex_path, report_path)
        if not compile_pdf or not report.passed:
            return result
        compiled = self.compiler.compile(tex_path, output, repository, latexmk)
        pdf_metrics = self.pdf_validator.validate(compiled)
        (pdf_report,) = self.writer.write(
            GeneratedArtifactSet(
                (
                    GeneratedArtifact(
                        Path("pdf/isa-reference-validate.json"),
                        json.dumps(pdf_metrics, indent=2, sort_keys=True) + "\n",
                    ),
                )
            ),
            output,
        )
        return DocumentBuildResult(
            report,
            tex_path,
            report_path,
            compiled.pdf,
            compiled.log,
            pdf_report,
        )
