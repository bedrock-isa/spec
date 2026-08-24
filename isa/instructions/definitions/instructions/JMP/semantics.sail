function execute_JMP_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_JMP then None()
  else {
    let result : Execution_result =
    match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_JMP, IllegalInstruction, "missing JMP target")
  };
    Some(result)
  }


function execute_JMP(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_JMP then None()
  else match execute_JMP_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_JMP, IllegalInstruction, "missing JMP target")
  }),
  }
