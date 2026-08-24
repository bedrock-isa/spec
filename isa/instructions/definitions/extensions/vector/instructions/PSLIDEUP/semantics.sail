function execute_PSLIDEUP(instruction : Decoded_instruction, state : Cpu_state)
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
    (predicate_register_index(instruction, "dst"), operand_named(instruction, "count")) {
    (Some(destination), Some(count_operand)) => {
      let source = if operation == Op_PSLICE then match
        predicate_register_index(instruction, "src") {
          Some(index) => state.predicate_registers[unsigned(index)], None() => empty,
        } else empty;
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = predicate_slide_image(
        operation, state.predicate_registers[unsigned(destination)], source, empty,
        0, lanes, element_bytes, unsigned(immediate_value(count_operand))
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else None()
}
