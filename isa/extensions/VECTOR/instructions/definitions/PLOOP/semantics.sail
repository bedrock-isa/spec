function execute_PLOOP(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if true then match
    (operand_named(instruction, Operand_remaining), operand_named(instruction, Operand_offset),
     predicate_register_index(instruction, Operand_predicate)) {
    (Some(remaining_operand), Some(offset_operand), Some(predicate)) => {
      let remaining_index = unsigned(remaining_operand.value[3 .. 0]);
      let offset_index = unsigned(offset_operand.value[3 .. 0]);
      let remaining = unsigned(state.registers[remaining_index]);
      let offset = unsigned(state.registers[offset_index]);
      if remaining == 0 then start_control_transaction(instruction, state)
      else if offset >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "PLOOP offset exceeds the lane count",
        0x0000000000000000
      ))
      else {
        let active = if remaining < lanes - offset then remaining else lanes - offset;
        var updated = state;
        updated.predicate_registers[unsigned(predicate)] = predicate_fill_typed(
          empty, 0, lanes, element_bytes, offset, offset + active
        );
        updated.registers[remaining_index] = get_slice_int(64, remaining - active, 0);
        updated.registers[offset_index] = 0x0000000000000000;
        Some(vector_finish(instruction, state, updated))
      }
    }, _ => None(),
  }
  else None()
}
