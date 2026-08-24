function execute_SUB_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SUB then None()
  else {
    let local_candidate : option(Execution_result) = match execute_sp_arithmetic_local(instruction, state) {
    Some(result) => Some(result), None() => execute_binary_local(instruction, state)
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form")
    }
          };
    Some(result)
  }


function execute_SUB(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SUB then None()
  else match execute_SUB_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form")
    }),
  }
