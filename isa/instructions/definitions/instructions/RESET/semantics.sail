function execute_RESET_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RESET then None()
  else {
    let result : Execution_result =
    route_environment(instruction, state, ResetProcessor, CommitControl, false);
    Some(result)
  }


function execute_RESET(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RESET then None()
  else match execute_RESET_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(route_environment(instruction, state, ResetProcessor, CommitControl, false)),
  }
