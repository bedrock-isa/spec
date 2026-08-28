"""Reader-facing manual artifact projection."""

from __future__ import annotations

from pathlib import Path

from engine.composition import DocumentComposition
from engine.render import LatexDocumentRenderer
from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


class ManualArtifactGenerator(ArtifactGenerator):
    """Generate one complete LaTeX manual from its artifact definition."""

    def __init__(
        self,
        definition: ArtifactDefinition,
        renderer: LatexDocumentRenderer | None = None,
    ) -> None:
        super().__init__(definition)
        self.renderer = renderer or LatexDocumentRenderer()

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        project = context.require_provider("isa")
        composition = DocumentComposition.load(self.definition.source, project)
        output = self.definition.data["output"]
        graph_output = self.definition.data["dependency-graph"]
        if not isinstance(output, str):
            raise ValueError(f"{self.definition.source}: output must be a path")
        if not isinstance(graph_output, str):
            raise ValueError(
                f"{self.definition.source}: dependency-graph must be a path"
            )
        rendered = self.renderer.render(composition, project)
        return GeneratedArtifactSet(
            (
                GeneratedArtifact(
                    Path(output),
                    rendered,
                ),
                GeneratedArtifact(
                    Path(graph_output),
                    self.renderer.dependencies.render_json(
                        project.entities, project.root
                    ),
                ),
            ),
            artifact_id=self.artifact_id,
        )


Generator = ManualArtifactGenerator
