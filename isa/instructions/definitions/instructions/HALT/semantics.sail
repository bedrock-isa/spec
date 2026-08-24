function execute_HALT_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_HALT then None()
  else {
    let result : Execution_result =
    completed(
    state, { advance_pc(state, instruction) with halted = true, run_state = Halted }, CommitControl,
    [|typed_effect(HaltProcessor, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  );
    Some(result)
  }


function execute_HALT(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_HALT then None()
  else match execute_HALT_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(completed(
    state, { advance_pc(state, instruction) with halted = true, run_state = Halted }, CommitControl,
    [|typed_effect(HaltProcessor, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  )),
  }
