"""Generate the complete MkDocs publication from current document artifacts."""

from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile

from engine.composition import DocumentComposition
from engine.generation import (
    ArtifactGenerationContext,
    ArtifactGenerator,
    ArtifactGeneratorRegistry,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.site.build import SiteDocument, SiteOutputError, render_site_output
from engine.site.model import DocumentSiteSpec, build_site, scoped_target
from engine.site.structure import parse_latex_structure
from engine.site.visual import extract_visuals


_DOCUMENTS = (
    (
        "isa-reference",
        "isa",
        "Programmer's Reference Manual",
        "isa_reference.pdf",
    ),
    (
        "elf-abi",
        "elf-abi",
        "ELF ABI",
        "bedrock-elf-abi.pdf",
    ),
    ("c-abi", "c-abi", "C ABI", "bedrock-c-abi.pdf"),
    (
        "c-target-intrinsics",
        "target-intrinsics",
        "Target Intrinsics",
        "bedrock-target-intrinsics.pdf",
    ),
)


class Generator(ArtifactGenerator):
    """Stage current TeX projections, PDFs, Pandoc pages, visuals, and MkDocs."""

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        project = context.require_provider("isa")
        registry = ArtifactGeneratorRegistry.discover(context.workspace)
        composition = DocumentComposition.load(
            registry.generator("isa-reference").definition.source, project
        )
        environment = dict(os.environ)
        environment["TEXINPUTS"] = os.pathsep.join(
            (
                str(context.workspace.root),
                str(context.workspace.root / "style"),
                "",
            )
        )

        with tempfile.TemporaryDirectory(prefix="bedrock-reference-site-") as raw:
            stage = Path(raw)
            sources = stage / "documents"
            pdfs = stage / "pdfs"
            sources.mkdir()
            pdfs.mkdir()
            documents = []
            for artifact_id, site_id, title, pdf_name in _DOCUMENTS:
                document_generator = registry.generator(artifact_id)
                output = document_generator.definition.outputs["document"]
                artifact = registry.generate(
                    artifact_id, context.workspace, context.output_root
                ).artifact(output)
                if not isinstance(artifact.content, str):
                    raise TypeError(f"{artifact_id}: TeX artifact must be text")
                source = sources / Path(output).name
                source.write_text(artifact.content, encoding="utf-8")
                pdf = self._compile_pdf(
                    artifact_id,
                    source,
                    pdfs / artifact_id,
                    context.workspace.root,
                    environment,
                )
                documents.append(
                    SiteDocument(artifact_id, site_id, title, source, pdf, pdf_name)
                )

            site_root = stage / "site"
            metrics = render_site_output(
                documents,
                composition,
                site_root,
                source_revision=self._revision(context.workspace.root),
                pandoc=os.environ.get("PANDOC", "pandoc"),
                latexpand=os.environ.get("LATEXPAND", "latexpand"),
                mkdocs=os.environ.get("MKDOCS", "mkdocs"),
                latexmk=os.environ.get("LATEXMK", "latexmk"),
                environment=environment,
            )
            reference = {
                "documents": [item[2] for item in _DOCUMENTS],
                "metrics": asdict(metrics),
            }
            assets = site_root / "assets"
            assets.mkdir(exist_ok=True)
            (assets / "reference.json").write_text(
                json.dumps(reference, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            artifacts = tuple(
                GeneratedArtifact(Path("site") / path.relative_to(site_root), path.read_bytes())
                for path in sorted(site_root.rglob("*"))
                if path.is_file()
            )
        return GeneratedArtifactSet(artifacts, artifact_id=self.artifact_id)

    def validate(self, context: ArtifactGenerationContext) -> None:
        """Validate the public site projection without compiling or publishing it."""

        project = context.require_provider("isa")
        registry = ArtifactGeneratorRegistry.discover(context.workspace)
        composition = DocumentComposition.load(
            registry.generator("isa-reference").definition.source, project
        )
        documents = []
        preserved_targets: set[str] = set()
        for artifact_id, site_id, title, pdf_name in _DOCUMENTS:
            generator = registry.generator(artifact_id)
            document_output = generator.definition.outputs["document"]
            artifact = registry.generate(
                artifact_id, context.workspace, context.output_root
            ).artifact(document_output)
            if not isinstance(artifact.content, str):
                raise TypeError(f"{artifact_id}: TeX artifact must be text")

            structure = parse_latex_structure(artifact.content)
            visualized = extract_visuals(site_id, artifact.content, structure)
            transformed = parse_latex_structure(visualized.text)
            original_labels = {label.name for label in structure.labels}
            transformed_labels = {label.name for label in transformed.labels}
            missing = sorted(original_labels - transformed_labels)
            if missing:
                raise SiteOutputError(
                    f"{site_id}: visual projection changed public labels; "
                    f"missing={missing}"
                )
            preserved_targets.update(
                scoped_target(site_id, label) for label in transformed_labels
            )
            documents.append(
                DocumentSiteSpec(
                    site_id,
                    title,
                    PurePosixPath("downloads") / pdf_name,
                    structure,
                )
            )

        site = build_site(tuple(documents), composition)
        expected_anchors = {
            name
            for name, target in site.registry.targets.items()
            if target.anchor is not None
        }
        missing = sorted(expected_anchors - preserved_targets)
        if missing:
            raise SiteOutputError(
                f"source anchor ownership mismatch; missing={missing}"
            )

        publication = self.definition.outputs["publication"]
        self.definition.validate_generated(
            GeneratedArtifactSet(
                (GeneratedArtifact(publication / "index.html", b""),),
                artifact_id=self.artifact_id,
            )
        )

    @staticmethod
    def _compile_pdf(
        artifact_id: str,
        source: Path,
        output: Path,
        repository: Path,
        environment: dict[str, str],
    ) -> Path:
        output.mkdir(parents=True)
        result = subprocess.run(
            [
                os.environ.get("LATEXMK", "latexmk"),
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                f"-outdir={output}",
                str(source),
            ],
            cwd=repository,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        pdf = output / source.with_suffix(".pdf").name
        if (
            result.returncode
            or not pdf.is_file()
            or not pdf.read_bytes().startswith(b"%PDF-")
        ):
            detail = "\n".join(part for part in (result.stdout, result.stderr) if part)
            raise ValueError(f"{artifact_id} PDF compilation failed:\n{detail[-12000:]}")
        return pdf

    @staticmethod
    def _revision(repository: Path) -> str:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository,
            text=True,
            capture_output=True,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
