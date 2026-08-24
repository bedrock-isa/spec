function execute_RET_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RET then None()
  else {
    let result : Execution_result =
    match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_RET, IllegalInstruction, "invalid RET form")
  };
    Some(result)
  }


function execute_RET(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RET then None()
  else match execute_RET_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_RET, IllegalInstruction, "invalid RET form")
  }),
  }
