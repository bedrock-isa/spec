function execute_INVASID_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_INVASID then None()
  else {
    let result : Execution_result = start_tlb_context_transaction(instruction, state);
    Some(result)
  }


function execute_INVASID(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_INVASID then None()
  else match execute_INVASID_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_tlb_context_transaction(instruction, state)),
  }
