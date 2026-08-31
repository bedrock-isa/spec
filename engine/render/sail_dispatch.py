"""Render exhaustive instruction-entry dispatch."""

from ..composition import SailProgram


class SailDispatchRenderer:
    def render(self, program: SailProgram) -> str:
        lines = [
            "// Generated from instruction-local Sail entry declarations. Do not edit.",
            "",
            "function execute_operation_entry(instruction : Decoded_instruction, state : Cpu_state)",
            "  -> Execution_result = match instruction.form.operation {",
        ]
        for semantics in program.instruction_semantics:
            rejection = (
                "faulted(state, instruction.form.operation, IllegalInstruction, "
                '"local operation entry rejected its owning form")'
            )
            execution = (
                f"match {semantics.entry}(instruction, state) "
                f"{{ Some(result) => result, None() => {rejection} }}"
            )
            lines.append(f"  {semantics.operation} => {execution},")
        lines.extend(["}", ""])
        return "\n".join(lines)
