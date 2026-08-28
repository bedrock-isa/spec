
function execute_SETcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    match find_operand_by_name(Operand_dst, instruction.operands) {
        Some(dst) => if dst.operand_type == OperandType_Rn then {
            let selected = predicate_holds(instruction, state);
            let value : bits(64) = if selected then { 0x0000000000000001 } else { 0x0000000000000000 };
            var updated = advance_pc(state, instruction);
            let index = unsigned(dst.value[3 .. 0]);
            updated.registers[index] = canonical_register_result(
                instruction.form.operation,
                value,
                operation_width(instruction),
            );
            Some(completed(state, updated, CommitRegisters, [||]))
        } else {
            match start_memory_transaction(instruction, state) {
                Some(result) => Some(result),
                None() => Some(
                    faulted(state, instruction.form.operation, IllegalInstruction, "missing SETcc memory destination"),
                ),
            }
        },
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "SETcc destination")),
    }
}
