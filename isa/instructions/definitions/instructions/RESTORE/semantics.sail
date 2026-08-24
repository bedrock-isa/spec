function execute_RESTORE_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RESTORE then None()
  else Some(start_tlb_context_transaction(instruction, state))


function execute_RESTORE(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RESTORE then None()
  else match execute_RESTORE_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_tlb_context_transaction(instruction, state)),
  }
