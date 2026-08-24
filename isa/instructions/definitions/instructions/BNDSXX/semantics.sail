function execute_BNDSXX_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_BNDSXX then None()
  else {
    let result : Execution_result =
    match execute_bounds_comparison_local(instruction, state, false, false, true) {
            Some(result) => result,
            None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved bounds form")
    }
          };
    Some(result)
  }


function execute_BNDSXX(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_BNDSXX then None()
  else match execute_BNDSXX_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved bounds form")
    }),
  }
