"""Executable full-Sail-model artifact projection."""

from __future__ import annotations

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

    def project_program(self, context: ArtifactGenerationContext):
        """Return the configured program projected by this artifact."""

        raw_extensions = self.definition.data.get("extensions")
        extensions = (
            None
            if raw_extensions is None
            else tuple(str(item) for item in raw_extensions)
        )
        project = context.require_provider("isa")
        configuration = IsaConfiguration.resolve(project, extensions)
        return self.composer.compose(project, configuration)

    def declared_sources(self, context: ArtifactGenerationContext) -> tuple[Path, ...]:
        """Return every authored Sail source consumed by the projection."""

        program = self.project_program(context)
        sources = [
            source
            for unit in program.sail_units
            for source in unit.sources
        ]
        sources.extend(item.source for item in program.instruction_semantics)
        if program.execution_provider is not None:
            sources.append(program.execution_provider.provider)
        sources.append(program.project.model.base.root / "control_registers/semantics/types.sail")
        for owner, namespace in program.project.control_registers.namespaces.items():
            if owner not in program.configuration.owners:
                continue
            sources.extend(register.semantics for register in namespace.registers.values())
        return tuple(dict.fromkeys(path.resolve() for path in sources))

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        program = self.project_program(context)
        outputs = self.definition.outputs
        registry_path = outputs["registry"]
        catalog_path = outputs["catalog"]
        dispatch_path = outputs["dispatch"]
        project_path = outputs["project"]
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
