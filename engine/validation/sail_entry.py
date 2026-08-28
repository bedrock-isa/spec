"""Validate instruction-owned Sail entry declarations."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

try:
    from ..composition import InstructionSemantics
    from ..project import InstructionBundle
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from composition import InstructionSemantics
    from project import InstructionBundle

if TYPE_CHECKING:
    from ..composition import SailProgram


class SailEntryValidator:
    def missing_semantics(
        self, semantics: "InstructionSemantics"
    ) -> tuple[str, ...]:
        source = semantics.source
        if not source.is_file():
            return ()
        text = source.read_text(encoding="utf-8")
        return tuple(
            entry
            for entry in semantics.entries
            if re.search(rf"(?m)^function\s+{re.escape(entry)}\s*\(", text) is None
        )

    def missing(self, bundle: InstructionBundle) -> tuple[str, ...]:
        return self.missing_semantics(InstructionSemantics(bundle))

    def require(self, program: "SailProgram") -> None:
        for semantics in program.instruction_semantics:
            missing = self.missing_semantics(semantics)
            if missing:
                raise ValueError(
                    f"{semantics.bundle.instruction.source}: Sail entry {missing[0]} "
                    f"is not defined by {semantics.source}"
                )
