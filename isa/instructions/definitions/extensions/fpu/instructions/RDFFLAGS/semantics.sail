function execute_RDFFLAGS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDFFLAGS then None()
  else {
    let result : Execution_result =
    match Some(read_state_register(instruction, state, sail_zero_extend(state.fflags, 64))) {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_RDFFLAGS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDFFLAGS then None()
  else match execute_RDFFLAGS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
