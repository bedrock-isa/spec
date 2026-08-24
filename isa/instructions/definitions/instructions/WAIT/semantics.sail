function execute_WAIT_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WAIT then None()
  else {
    let result : Execution_result =
    completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(NoEffect, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  );
    Some(result)
  }


function execute_WAIT(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WAIT then None()
  else match execute_WAIT_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(NoEffect, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  )),
  }
