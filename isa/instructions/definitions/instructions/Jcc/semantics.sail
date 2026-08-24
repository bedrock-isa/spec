function execute_Jcc_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_Jcc then None()
  else {
    let result : Execution_result =
    match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_Jcc, IllegalInstruction, "missing Jcc target")
  };
    Some(result)
  }


function execute_Jcc(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_Jcc then None()
  else match execute_Jcc_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_Jcc, IllegalInstruction, "missing Jcc target")
  }),
  }
