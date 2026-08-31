"""Render exhaustive instruction-entry dispatch."""

from dataclasses import dataclass

from ..composition import SailProgram


@dataclass(frozen=True, slots=True)
class SailDispatchEntry:
    operation: str
    entry: str


@dataclass(frozen=True, slots=True)
class SailDispatchProjection:
    """Selected operation-to-instruction-entry dispatch relation."""

    entries: tuple[SailDispatchEntry, ...]


class SailDispatchRenderer:
    def project(self, program: SailProgram) -> SailDispatchProjection:
        return SailDispatchProjection(
            tuple(
                SailDispatchEntry(semantics.operation, semantics.entry)
                for semantics in program.instruction_semantics
            )
        )

    def render(self, program: SailProgram) -> str:
        lines = [
            "// Generated from instruction-local Sail entry declarations. Do not edit.",
            "",
            "function execute_operation_entry(instruction : Decoded_instruction, state : Cpu_state)",
            "  -> Execution_result = match instruction.form.operation {",
        ]
        for entry in self.project(program).entries:
            rejection = (
                "faulted(state, instruction.form.operation, IllegalInstruction, "
                '"local operation entry rejected its owning form")'
            )
            execution = (
                f"match {entry.entry}(instruction, state) "
                f"{{ Some(result) => result, None() => {rejection} }}"
            )
            lines.append(f"  {entry.operation} => {execution},")
        lines.extend(["}", ""])
        return "\n".join(lines)
