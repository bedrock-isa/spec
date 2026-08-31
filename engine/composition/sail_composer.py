"""Projection of a loaded ISA project into a Sail program."""

from __future__ import annotations

from ..project import IsaProject
from .configuration import IsaConfiguration
from .sail_program import InstructionSemantics, SailProgram


class SailComposer:
    """Select configuration-owned sources without rendering or writing them."""

    def compose(
        self,
        project: IsaProject,
        configuration: IsaConfiguration,
    ) -> SailProgram:
        owners = configuration.owners
        ordered_bundles = tuple(
            project.catalog.instructions.resolve(reference)
            for reference in project.catalog.instruction_order
        )
        bundles = tuple(bundle for bundle in ordered_bundles if bundle.owner in owners)
        sail_units = tuple(
            project.model.sail_units[reference]
            for reference in project.model.sail_order
            if project.model.sail_units[reference].owner in owners
        )
        providers = tuple(
            namespace.execution_provider
            for namespace in (project.model.base, *project.model.extensions.values())
            if namespace.owner in owners
            and namespace.execution_provider is not None
        )
        if len(providers) > 1:
            sources = ", ".join(str(provider.source) for provider in providers)
            raise ValueError(
                "selected ISA configuration has multiple execution "
                f"providers: {sources}"
            )
        instruction_semantics = tuple(InstructionSemantics(bundle) for bundle in bundles)
        return SailProgram(
            project,
            configuration,
            instruction_semantics,
            sail_units,
            providers[0] if providers else None,
        )
