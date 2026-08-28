"""Executable full-Sail-model artifact projection."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from engine.composition import IsaConfiguration, SailComposer
from engine.render import (
    SailCatalogRenderer,
    SailDispatchRenderer,
    SailProjectRenderer,
    SailRegistryRenderer,
)
from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)


class SailModelArtifactGenerator(ArtifactGenerator):
    """Generate a configured Sail program and its generated support modules."""

    def __init__(
        self,
        definition: ArtifactDefinition,
        composer: SailComposer | None = None,
        registry: SailRegistryRenderer | None = None,
        catalog: SailCatalogRenderer | None = None,
        dispatch: SailDispatchRenderer | None = None,
        project: SailProjectRenderer | None = None,
    ) -> None:
        super().__init__(definition)
        self.composer = composer or SailComposer()
        self.registry = registry or SailRegistryRenderer()
        self.catalog = catalog or SailCatalogRenderer()
        self.dispatch = dispatch or SailDispatchRenderer()
        self.project = project or SailProjectRenderer()

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        raw_extensions = self.definition.data.get("extensions")
        extensions = (
            None
            if raw_extensions is None
            else tuple(str(item) for item in raw_extensions)
        )
        project = context.require_provider("isa")
        configuration = IsaConfiguration.resolve(project, extensions)
        program = self.composer.compose(project, configuration)
        outputs = self.definition.data["outputs"]
        if not isinstance(outputs, Mapping):
            raise ValueError(f"{self.definition.source}: outputs must be a mapping")
        registry_path = Path(str(outputs["registry"]))
        catalog_path = Path(str(outputs["catalog"]))
        dispatch_path = Path(str(outputs["dispatch"]))
        project_path = Path(str(outputs["project"]))
        return GeneratedArtifactSet(
            (
                GeneratedArtifact(registry_path, self.registry.render(program)),
                GeneratedArtifact(catalog_path, self.catalog.render(program)),
                GeneratedArtifact(dispatch_path, self.dispatch.render(program)),
                GeneratedArtifact(
                    project_path,
                    self.project.render(program, context.output_root),
                ),
            ),
            artifact_id=self.artifact_id,
        )


Generator = SailModelArtifactGenerator
