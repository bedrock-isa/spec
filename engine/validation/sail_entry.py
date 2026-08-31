"""Validate instruction-owned Sail entry declarations."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..composition import InstructionSemantics
from ..project import InstructionBundle

if TYPE_CHECKING:
    from ..composition import SailProgram


class SailEntryValidator:
    def missing_semantics(
        self, semantics: "InstructionSemantics"
    ) -> str | None:
        source = semantics.source
        if not source.is_file():
            return None
        text = source.read_text(encoding="utf-8")
        return (
            semantics.entry
            if re.search(
                rf"(?m)^function\s+{re.escape(semantics.entry)}\s*\(", text
            )
            is None
            else None
        )

    def missing(self, bundle: InstructionBundle) -> str | None:
        return self.missing_semantics(InstructionSemantics(bundle))

    def require(self, program: "SailProgram") -> None:
        for semantics in program.instruction_semantics:
            missing = self.missing_semantics(semantics)
            if missing is not None:
                raise ValueError(
                    f"{semantics.bundle.instruction.source}: Sail entry {missing} "
                    f"is not defined by {semantics.source}"
                )
