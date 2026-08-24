function execute_TRACE_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_TRACE then None()
  else {
    let result : Execution_result =
    completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(TraceMarker, instruction, state, state.pc,
                   match value_named(instruction, state, "marker") {
                     Some(value) => value, None() => 0x0000000000000000
                   }, 2, 0, false)|]
  );
    Some(result)
  }


function execute_TRACE(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_TRACE then None()
  else match execute_TRACE_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(TraceMarker, instruction, state, state.pc,
                   match value_named(instruction, state, "marker") {
                     Some(value) => value, None() => 0x0000000000000000
                   }, 2, 0, false)|]
  )),
  }
