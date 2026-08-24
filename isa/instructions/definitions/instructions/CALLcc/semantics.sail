function execute_CALLcc_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_CALLcc then None()
  else {
    let result : Execution_result =
    match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_CALLcc, IllegalInstruction, "missing CALLcc target")
  };
    Some(result)
  }


function execute_CALLcc(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_CALLcc then None()
  else match execute_CALLcc_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_CALLcc, IllegalInstruction, "missing CALLcc target")
  }),
  }
