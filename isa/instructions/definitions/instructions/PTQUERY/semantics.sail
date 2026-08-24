function execute_PTQUERY_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_PTQUERY then None()
  else Some(start_tlb_context_transaction(instruction, state))


function execute_PTQUERY(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_PTQUERY then None()
  else match execute_PTQUERY_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_tlb_context_transaction(instruction, state)),
  }
