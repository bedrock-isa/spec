function execute_SWPT_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SWPT then None()
  else {
    let result : Execution_result = start_tlb_context_transaction(instruction, state);
    Some(result)
  }


function execute_SWPT(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SWPT then None()
  else match execute_SWPT_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_tlb_context_transaction(instruction, state)),
  }
