function execute_VINSERT(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if not_bool(fp_form) then match
    (value_named(instruction, state, Operand_src), value_named(instruction, state, Operand_index),
     vector_register_index(instruction, Operand_dst)) {
    (Some(source), Some(index_value), Some(destination)) => {
      let index = unsigned(index_value);
      if index >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "VINSERT lane index exceeds the lane count",
        0x0000000000000001
      ))
      else {
        var updated = state;
        updated.vector_registers[unsigned(destination)] = vector_write_lane(
          state.vector_registers[unsigned(destination)], index, element_bytes, unsigned(source)
        );
        Some(vector_finish(instruction, state, updated))
      }
    }, _ => None(),
  }
  else None()
}
