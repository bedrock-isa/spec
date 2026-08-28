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
            fallback = (
                "faulted(state, instruction.form.operation, IllegalInstruction, "
                '"local operation entry rejected its owning form")'
            )
            if len(semantics.entries) == 1:
                entry = semantics.entries[0]
                execution = (
                    f"match {entry}(instruction, state) {{ Some(result) => result, "
                    f"None() => {fallback} }}"
                )
            else:
                execution = fallback
                for entry in reversed(semantics.entries):
                    execution = (
                        f"match {entry}(instruction, state) {{ Some(result) => result, "
                        f"None() => {execution} }}"
                    )
            lines.append(f"  {semantics.operation} => {execution},")
        lines.extend(["}", ""])
        return "\n".join(lines)
