function execute_SET_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SET then None()
  else {
    let result : Execution_result =
    match execute_set_local(instruction, state) {
    Some(result) => result,
    None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => route_environment(instruction, state, IntegerCompute, CommitMemory, false),
    },
  };
    Some(result)
  }


function execute_SET(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SET then None()
  else match execute_SET_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match execute_set_local(instruction, state) {
    Some(result) => result,
    None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => route_environment(instruction, state, IntegerCompute, CommitMemory, false),
    },
  }),
  }
