function execute_RDSTATUS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDSTATUS then None()
  else {
    let result : Execution_result =
    match Some(read_state_register(instruction, state, narrow_bits(state.status, 2))) {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_RDSTATUS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDSTATUS then None()
  else match execute_RDSTATUS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
