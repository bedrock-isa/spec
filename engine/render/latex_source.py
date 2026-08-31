"""Preprocessing for authored LaTeX sources."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from ..dependency import DependencyGraph
from ..entity import PublicTargetCatalog
from ..semantic_text import SemanticText, TextOrigin
from .document_fragment import DocumentFragmentPipeline
from .vector_diagram import VectorDiagramPlacementRenderer


LOCAL_INPUT_RE = re.compile(r"\\input\{((?!/)(?![^}]*\.\.)[^}]+)\}")


@dataclass(frozen=True, slots=True)
class LatexSourceInputProjection:
    requested: str
    source: "LatexSourceProjection"


@dataclass(frozen=True, slots=True)
class LatexSourceProjection:
    """One expanded source node before semantic TeX serialization."""

    source: Path
    semantic: SemanticText | None
    style_text: str | None
    inputs: tuple[LatexSourceInputProjection, ...]


class LatexSourcePreprocessor:
    """Expand and semantically resolve one repository-local LaTeX source tree."""

    def __init__(
        self,
        fragments: DocumentFragmentPipeline,
        semantic,
        dependencies: DependencyGraph | None = None,
        diagrams: VectorDiagramPlacementRenderer | None = None,
    ) -> None:
        self.fragments = fragments
        self.semantic = semantic
        self.dependencies = dependencies or DependencyGraph()
        self.diagrams = diagrams or VectorDiagramPlacementRenderer()

    def render(
        self,
        source: str | Path,
        project,
        public_targets: PublicTargetCatalog,
        owner=None,
    ) -> str:
        repository = project.root.parent.resolve()
        path = Path(source).resolve()
        self._require_source(path, repository, str(source))
        projection = self._project(
            path, project, public_targets, repository, (), owner
        )
        return self._render_projection(
            projection, project, public_targets
        ).rstrip()

    def project(
        self,
        source: str | Path,
        project,
        public_targets: PublicTargetCatalog,
        owner=None,
    ) -> LatexSourceProjection:
        repository = project.root.parent.resolve()
        path = Path(source).resolve()
        self._require_source(path, repository, str(source))
        return self._project(path, project, public_targets, repository, (), owner)

    def _project(
        self,
        path: Path,
        project,
        public_targets: PublicTargetCatalog,
        repository: Path,
        active: tuple[Path, ...],
        owner,
    ) -> LatexSourceProjection:
        if path in active:
            cycle = " -> ".join(str(item) for item in (*active, path))
            raise RuntimeError(f"cyclic TeX input: {cycle}")
        text = path.read_text(encoding="utf-8")
        semantic = None
        style_text = None
        if path.suffix != ".sty":
            text = self.fragments.expand(text, project, public_targets, path)
            text = self.diagrams.expand(text, project, path, owner)
            semantic = SemanticText.parse(text, origin=TextOrigin(path))
            if owner is not None:
                self.dependencies.record(owner, semantic)
        else:
            style_text = text

        inputs: list[LatexSourceInputProjection] = []
        for match in LOCAL_INPUT_RE.finditer(text):
            requested = match.group(1)
            included = (repository / requested).resolve()
            if included.suffix == "":
                included = included.with_suffix(".tex")
            self._require_source(included, repository, requested)
            inputs.append(
                LatexSourceInputProjection(
                    requested,
                    self._project(
                        included,
                        project,
                        public_targets,
                        repository,
                        (*active, path),
                        owner,
                    ),
                )
            )
        return LatexSourceProjection(path, semantic, style_text, tuple(inputs))

    def _render_projection(
        self,
        projection: LatexSourceProjection,
        project,
        public_targets: PublicTargetCatalog,
    ) -> str:
        if projection.semantic is not None:
            text = self.semantic.render(
                projection.semantic,
                project.terminology,
                public_targets=public_targets,
                escape_literals=False,
            )
        else:
            assert projection.style_text is not None
            text = projection.style_text

        inputs = iter(projection.inputs)

        def replace(match: re.Match[str]) -> str:
            projected = next(inputs)
            if match.group(1) != projected.requested:
                raise RuntimeError("source projection input order changed")
            content = self._render_projection(
                projected.source, project, public_targets
            )
            if projected.source.source.suffix == ".sty":
                content = re.sub(r"(?m)^\\endinput\s*$", "", content).rstrip()
            return (
                f"% begin input: {projected.requested}\n{content}\n"
                f"% end input: {projected.requested}"
            )

        return LOCAL_INPUT_RE.sub(replace, text)

    @staticmethod
    def _require_source(path: Path, repository: Path, requested: str) -> None:
        if not path.is_relative_to(repository) or not path.is_file():
            raise RuntimeError(f"cannot preprocess TeX source {requested!r}")
