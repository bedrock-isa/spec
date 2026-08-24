function execute_MAXU_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_MAXU then None()
  else {
    let result : Execution_result =
    match execute_math_local(instruction, state) {
            Some(result) => result,
            None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form")
    }
          };
    Some(result)
  }


function execute_MAXU(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_MAXU then None()
  else match execute_MAXU_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form")
    }),
  }
