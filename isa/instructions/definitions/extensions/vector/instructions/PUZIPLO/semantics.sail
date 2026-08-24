function execute_PUZIPLO(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if true | true
       | true | true
       | true | true then match
    (predicate_register_index(instruction, "lhs"),
     predicate_register_index(instruction, "rhs"),
     predicate_register_index(instruction, "dst")) {
    (Some(left), Some(right), Some(destination)) => {
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = predicate_pair_image(
        operation, state.predicate_registers[unsigned(left)],
        state.predicate_registers[unsigned(right)],
        empty, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else None()
}
