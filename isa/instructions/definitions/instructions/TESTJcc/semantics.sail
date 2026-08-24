function execute_TESTJcc_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_TESTJcc then None()
  else {
    let result : Execution_result =
    match execute_compare_jump_local(instruction, state) {
    Some(result) => result,
    None() => faulted(state, Op_TESTJcc, IllegalInstruction, "TESTJcc local operands"),
  };
    Some(result)
  }


function execute_TESTJcc(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_TESTJcc then None()
  else match execute_TESTJcc_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match execute_compare_jump_local(instruction, state) {
    Some(result) => result,
    None() => faulted(state, Op_TESTJcc, IllegalInstruction, "TESTJcc local operands"),
  }),
  }
