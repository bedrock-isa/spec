function execute_WRSEG_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRSEG then None()
  else {
    let local_candidate : option(Execution_result) = match (value_named(instruction, state, "src"), operand_named(instruction, "seg")) {
    (Some(source), Some(segment_operand)) => if not_bool(segment_image_valid(source)) then Some(faulted(state, Op_WRSEG, InvalidControlState, "invalid segment image"))
    else { var updated = state; updated.segments[sreg_index(segment_operand)] = source; Some(local_result(state, instruction, updated, CommitRegisters)) },
    _ => None(),
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_WRSEG(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRSEG then None()
  else match execute_WRSEG_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
