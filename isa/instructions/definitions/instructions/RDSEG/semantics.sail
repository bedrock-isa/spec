function execute_RDSEG_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDSEG then None()
  else {
    let local_candidate : option(Execution_result) = match (operand_named(instruction, "seg"), destination_named(instruction, "dst", 8)) {
    (Some(segment_operand), Some(destination)) => {
      let index = sreg_index(segment_operand);
      let updated = write_local_destination(state, instruction.form.operation, destination, state.segments[index]);
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_RDSEG(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDSEG then None()
  else match execute_RDSEG_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
