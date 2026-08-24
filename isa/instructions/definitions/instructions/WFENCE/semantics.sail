function execute_WFENCE_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WFENCE then None()
  else {
    let result : Execution_result =
    route_environment(instruction, state, FenceOperation, CommitControl, false);
    Some(result)
  }


function execute_WFENCE(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WFENCE then None()
  else match execute_WFENCE_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(route_environment(instruction, state, FenceOperation, CommitControl, false)),
  }
