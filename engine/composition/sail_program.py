"""Immutable Sail composition model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..model import SailUnit
from ..project import InstructionBundle, IsaProject
from .configuration import IsaConfiguration


@dataclass(frozen=True, slots=True)
class InstructionSemantics:
    """One instruction-owned contribution to the executable Sail model."""

    bundle: InstructionBundle

    @property
    def operation(self) -> str:
        return f"Op_{self.bundle.instruction.mnemonic}"

    @property
    def source(self) -> Path:
        return self.bundle.artifacts.semantics

    @property
    def entry(self) -> str:
        return f"execute_{self.bundle.instruction.mnemonic}"


@dataclass(frozen=True, slots=True)
class SailProgram:
    """Selected instruction and shared-model sources for one ISA configuration."""

    project: IsaProject
    configuration: IsaConfiguration
    instruction_semantics: tuple[InstructionSemantics, ...]
    sail_units: tuple[SailUnit, ...]

    @property
    def bundles(self) -> tuple[InstructionBundle, ...]:
        """Instruction projection shared by non-semantic Sail renderers."""

        return tuple(semantics.bundle for semantics in self.instruction_semantics)
