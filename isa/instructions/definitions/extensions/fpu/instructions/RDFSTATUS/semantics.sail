function execute_RDFSTATUS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDFSTATUS then None()
  else {
    let result : Execution_result =
    match Some(read_state_register(instruction, state, narrow_bits(state.fstatus, 2))) {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_RDFSTATUS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDFSTATUS then None()
  else match execute_RDFSTATUS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
