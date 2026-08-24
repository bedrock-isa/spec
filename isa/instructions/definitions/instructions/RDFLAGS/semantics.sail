function execute_RDFLAGS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDFLAGS then None()
  else {
    let result : Execution_result =
    match Some(read_state_register(instruction, state, sail_zero_extend(state.flags, 64))) {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_RDFLAGS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDFLAGS then None()
  else match execute_RDFLAGS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
