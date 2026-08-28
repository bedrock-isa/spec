"""Reusable projection for an authored repository-local TeX source."""

from __future__ import annotations

from pathlib import Path

from ..document_pipeline import TexInputExpander
from .artifact import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


class AuthoredTexArtifactGenerator(ArtifactGenerator):
    """Validate local includes and publish one authored TeX source unchanged."""

    def __init__(
        self,
        definition: ArtifactDefinition,
        expander: TexInputExpander | None = None,
    ) -> None:
        super().__init__(definition)
        self.expander = expander or TexInputExpander()

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        raw_source = self.definition.data.get("source")
        raw_output = self.definition.data.get("output")
        if not isinstance(raw_source, str):
            raise ValueError(f"{self.definition.source}: source must be a TeX path")
        if not isinstance(raw_output, str):
            raise ValueError(f"{self.definition.source}: output must be a TeX path")
        source = (context.workspace.root / raw_source).resolve()
        if (
            not source.is_relative_to(context.workspace.root)
            or source.suffix != ".tex"
            or not source.is_file()
        ):
            raise ValueError(f"{self.definition.source}: invalid TeX source {raw_source!r}")
        content = source.read_text(encoding="utf-8")
        self.expander.expand(content, context.workspace.root)
        return GeneratedArtifactSet(
            (GeneratedArtifact(Path(raw_output), content),),
            artifact_id=self.artifact_id,
        )
