function execute_DIVMODS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_DIVMODS then None()
  else {
    let result : Execution_result =
    match execute_divmod_local(instruction, state) {
      Some(result) => result,
      None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved multiply/divide form")
    },
    };
    Some(result)
  }


function execute_DIVMODS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_DIVMODS then None()
  else match execute_DIVMODS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved multiply/divide form")
    }),
  }
