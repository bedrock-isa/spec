function execute_VINDEX(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if true then match vector_register_index(instruction, Operand_dst) {
    Some(destination) => {
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_index_image(
        zero_vector, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, None() => None(),
  }
  else None()
}
