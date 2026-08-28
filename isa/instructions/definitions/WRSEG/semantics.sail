
function execute_WRSEG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match (
        value_named(instruction, state, Operand_src),
        operand_named(instruction, Operand_seg),
    ) {
        (Some(source), Some(segment_operand)) => if not_bool(segment_image_valid(source)) then {
            Some(faulted(state, Op_WRSEG, InvalidControlState, "invalid segment image"))
        } else {
            var updated = state;
            updated.segments[sreg_index(segment_operand)] = source;
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
