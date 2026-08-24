function execute_BPALL(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if true | true | true then match
    predicate_register_index(instruction, "predicate") {
    None() => None(),
    Some(source) => {
      let any = predicate_any(state.predicate_registers[unsigned(source)]);
      let take = if operation == Op_BPANY then any
                 else if operation == Op_BPNONE then not_bool(any)
                 else predicate_all_typed(state.predicate_registers[unsigned(source)], 0, lanes, element_bytes);
      if take then start_control_transaction(instruction, state)
      else Some(completed(state, advance_pc(state, instruction), CommitControl, [||]))
    },
  }
  else None()
}
