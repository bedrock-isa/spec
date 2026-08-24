function execute_LCALL_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_LCALL then None()
  else {
    let result : Execution_result =
    match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LCALL, IllegalInstruction, "missing LCALL target")
  };
    Some(result)
  }


function execute_LCALL(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_LCALL then None()
  else match execute_LCALL_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LCALL, IllegalInstruction, "missing LCALL target")
  }),
  }
