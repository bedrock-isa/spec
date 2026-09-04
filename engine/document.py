"""TeX validation and gated PDF compilation for the ISA reference."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from enum import StrEnum
import json
import logging
from pathlib import Path
import re
import tempfile

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
from .observability import log_phase
from .workspace import SpecWorkspace


PLACEHOLDER_RE = re.compile(r"@[A-Z0-9_]+@")
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
HYPER_REFERENCE_RE = re.compile(r"\\hyperref\[([^\]]+)\]")
STANDARD_REFERENCE_RE = re.compile(r"\\(?:auto|page)?ref\{([^{}]+)\}")
INSTRUCTION_TARGET_RE = re.compile(
    r"^\\begin\{BedrockInstruction\}.*\{([^{}\n]+)\}\s*$", re.MULTILINE
)
LISTED_DIAGRAM_TARGET_RE = re.compile(
    r"^\\begin\{BedrockListed(?:Bit|Format)Diagram\}.*\[([^\]\n]+)\]\s*$",
    re.MULTILINE,
)
SUMMARY_REFERENCE_RE = re.compile(r"\\BedrockSummaryMnemonic\{([^{}]+)\}")
_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TexValidationIssue:
    """One machine-readable document-validation failure."""

    code: "TexValidationCode"
    actual: int | None = None
    expected: int | None = None
    values: tuple[str, ...] = ()
    counts: tuple[tuple[str, int], ...] = ()


class TexValidationCode(StrEnum):
    DOCUMENT_ENVIRONMENT_COUNT = "document_environment_count"
    UNRESOLVED_PLACEHOLDERS = "unresolved_placeholders"
    DUPLICATE_PUBLIC_TARGETS = "duplicate_public_targets"
    UNRESOLVED_PUBLIC_TARGETS = "unresolved_public_targets"


@dataclass(frozen=True, slots=True)
class TexValidationReport:
    passed: bool
    issues: tuple[TexValidationIssue, ...]
    quantitative: dict[str, object]
    qualitative_review: dict[str, object]

    def render_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


class TexValidator:
    """Validate structure derived from the current specification model."""

    def validate(
        self,
        tex: str,
    ) -> TexValidationReport:
        issues: list[TexValidationIssue] = []
        document_begins = tex.count(r"\begin{document}")
        document_ends = tex.count(r"\end{document}")
        if document_begins != 1 or document_ends != 1:
            issues.append(
                TexValidationIssue(
                    TexValidationCode.DOCUMENT_ENVIRONMENT_COUNT,
                    counts=(("begin", document_begins), ("end", document_ends)),
                )
            )
        placeholders = sorted(set(PLACEHOLDER_RE.findall(tex)))
        if placeholders:
            issues.append(
                TexValidationIssue(
                    TexValidationCode.UNRESOLVED_PLACEHOLDERS,
                    values=tuple(placeholders),
                )
            )
        targets = (
            LABEL_RE.findall(tex)
            + INSTRUCTION_TARGET_RE.findall(tex)
            + LISTED_DIAGRAM_TARGET_RE.findall(tex)
        )
        duplicate_targets = sorted(
            target for target, count in Counter(targets).items() if count > 1
        )
        if duplicate_targets:
            issues.append(
                TexValidationIssue(
                    TexValidationCode.DUPLICATE_PUBLIC_TARGETS,
                    values=tuple(duplicate_targets),
                )
            )
        references = set(
            HYPER_REFERENCE_RE.findall(tex)
            + STANDARD_REFERENCE_RE.findall(tex)
            + SUMMARY_REFERENCE_RE.findall(tex)
        )
        missing_targets = sorted(references.difference(targets))
        if missing_targets:
            issues.append(
                TexValidationIssue(
                    TexValidationCode.UNRESOLVED_PUBLIC_TARGETS,
                    values=tuple(missing_targets),
                )
            )
        return TexValidationReport(
            passed=not issues,
            issues=tuple(issues),
            quantitative={
                "bytes": len(tex),
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
    """Generate, validate, and conditionally compile one document artifact."""

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
        with log_phase(
            _LOGGER, "document.build", compile_pdf=compile_pdf
        ) as phase:
            result = self._build(
                workspace,
                output_root,
                compile_pdf=compile_pdf,
                latexmk=latexmk,
            )
            phase["validation"] = "passed" if result.report.passed else "failed"
            phase["pdf"] = result.pdf is not None
            return result

    def _build(
        self,
        workspace: SpecWorkspace,
        output_root: str | Path,
        *,
        compile_pdf: bool,
        latexmk: str,
    ) -> DocumentBuildResult:
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
        with log_phase(
            _LOGGER, "document.generate", artifact=generator.artifact_id
        ) as phase:
            generated = generator.generate(context)
            generator.definition.validate_generated(generated)
            phase["files"] = len(generated.artifacts)
        document_output = generator.definition.outputs["document"]
        tex = generated.artifact(document_output).content
        if not isinstance(tex, str):
            raise TypeError(f"{generator.artifact_id}: TeX artifact must be text")
        derived = generator.definition.derived_outputs
        required_derived = {
            "tex-validation",
            "compiled-document",
            "compile-log",
            "pdf-validation",
        }
        missing_derived = sorted(required_derived - set(derived))
        if missing_derived:
            raise ValueError(
                f"{generator.artifact_id}: document artifact is missing derived "
                f"outputs {missing_derived}"
            )
        with log_phase(_LOGGER, "document.tex.validate") as phase:
            report = self.validator.validate(tex)
            phase["issues"] = len(report.issues)
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
        with tempfile.TemporaryDirectory(
            prefix=f"bedrock-{generator.artifact_id}-"
        ) as directory:
            scratch_root = Path(directory)
            with log_phase(
                _LOGGER,
                "document.latex.compile",
                executable=latexmk,
            ):
                compiled = self.compiler.compile(
                    tex_path, scratch_root, repository, latexmk
                )
            with log_phase(_LOGGER, "document.pdf.validate") as phase:
                pdf_metrics = self.pdf_validator.validate(compiled)
                phase["pages"] = pdf_metrics["pages"]
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
