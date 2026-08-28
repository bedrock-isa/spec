function execute_PAND(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if true | true | true then
    match (predicate_register_index(instruction, Operand_src),
           predicate_register_index(instruction, Operand_dst)) {
      (Some(source), Some(destination)) => {
        var updated = state;
        updated.predicate_registers[unsigned(destination)] = predicate_raw_binary(
          state.predicate_registers[unsigned(destination)],
          state.predicate_registers[unsigned(source)], operation
        );
        Some(vector_finish(instruction, state, updated))
      }, _ => None(),
    }
  else None()
}
