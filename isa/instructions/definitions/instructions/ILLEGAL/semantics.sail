function execute_ILLEGAL_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_ILLEGAL then None()
  else {
    let result : Execution_result =
    faulted(state, Op_ILLEGAL, IllegalInstruction, "explicit ILLEGAL");
    Some(result)
  }


function execute_ILLEGAL(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_ILLEGAL then None()
  else match execute_ILLEGAL_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(faulted(state, Op_ILLEGAL, IllegalInstruction, "explicit ILLEGAL")),
  }
