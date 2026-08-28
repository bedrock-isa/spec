function execute_VSLIDEDN(instruction : Decoded_instruction, state : Cpu_state)
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
       | true | true
       | true | true
       | true | true then match
    (vector_register_index(instruction, Operand_dst),
     predicate_register_index(instruction, Operand_govern)) {
    (Some(destination), Some(predicate)) => {
      let source : list(bits(8)) = match vector_register_index(instruction, Operand_src) {
        Some(index) => state.vector_registers[unsigned(index)], None() => zero_vector,
      };
      let count : int = match operand_named(instruction, Operand_count) {
        Some(count_operand) => unsigned(immediate_value(count_operand)), None() => 0,
      };
      let original = state.vector_registers[unsigned(destination)];
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_permute_image(
        operation, original, source, original,
        state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes, count
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else None()
}
