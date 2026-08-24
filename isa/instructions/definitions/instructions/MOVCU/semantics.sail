function execute_MOVCU_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_MOVCU then None()
  else {
    let result : Execution_result =
    match execute_binary_local(instruction, state) {
            Some(result) => result,
            None() => match start_stack_transaction(instruction, state) { Some(result) => result, None() => match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form") } }
          };
    Some(result)
  }


function execute_MOVCU(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_MOVCU then None()
  else match execute_MOVCU_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_stack_transaction(instruction, state) { Some(result) => result, None() => match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form") } }),
  }
