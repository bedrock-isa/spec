
function execute_RDSEG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match (
        operand_named(instruction, Operand_seg),
        destination_named(instruction, Operand_dst, 8),
    ) {
        (Some(segment_operand), Some(destination)) => {
            let index = sreg_index(segment_operand);
            let updated = write_local_destination(state, instruction.form.operation, destination, state.segments[index]);
            Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}
