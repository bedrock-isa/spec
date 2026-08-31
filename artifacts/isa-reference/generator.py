"""Reader-facing manual artifact projection."""

from __future__ import annotations

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
        outputs = self.definition.outputs
        rendered = self.renderer.render(composition, project)
        return GeneratedArtifactSet(
            (
                GeneratedArtifact(
                    outputs["document"],
                    rendered,
                ),
                GeneratedArtifact(
                    outputs["dependencies"],
                    self.renderer.dependencies.render_json(
                        project.entities, project.root
                    ),
                ),
            ),
            artifact_id=self.artifact_id,
        )


Generator = ManualArtifactGenerator
