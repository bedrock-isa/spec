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
        dispatch_function = (
            "execute_base_operation_entry"
            if program.execution_provider is not None
            else "execute_operation_entry"
        )
        lines = [
            "// Generated from instruction-local Sail entry declarations. Do not edit.",
            "",
            f"function {dispatch_function}(instruction : Decoded_instruction, state : Cpu_state)",
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
        if program.execution_provider is None:
            lines.extend(
                [
                    "function control_register_write_valid(",
                    "  control : Control_register, source : bits(64), before : Cpu_state,",
                    "  candidate : Cpu_state",
                    ") -> bool =",
                    "  base_control_register_write_valid(control, source, before, candidate)",
                    "",
                    "function event_from_fault(result : Execution_result) -> Event_record =",
                    "  base_event_from_fault(result)",
                    "",
                    "function cpuid_flag_enabled(flag : Cpuid_flag, state : Cpu_state) -> bool =",
                    "  base_cpuid_flag_enabled(flag, state)",
                    "",
                ]
            )
        return "\n".join(lines)
