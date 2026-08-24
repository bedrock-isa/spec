function execute_AFENCE_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_AFENCE then None()
  else {
    let result : Execution_result =
    route_environment(instruction, state, FenceOperation, CommitControl, false);
    Some(result)
  }


function execute_AFENCE(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_AFENCE then None()
  else match execute_AFENCE_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(route_environment(instruction, state, FenceOperation, CommitControl, false)),
  }
