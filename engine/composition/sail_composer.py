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
        bundles = tuple(
            project.catalog.instructions.resolve(reference)
            for reference in project.catalog.instruction_order
            if reference.owner in owners
        )
        sail_units = tuple(
            project.model.sail_units[reference]
            for reference in project.model.sail_order
            if project.model.sail_units[reference].owner in owners
        )
        instruction_semantics = tuple(InstructionSemantics(bundle) for bundle in bundles)
        return SailProgram(
            project,
            configuration,
            instruction_semantics,
            sail_units,
        )
