function execute_VLCADD(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if true then
    match (operand_named(instruction, "offset"), operand_named(instruction, "dst")) {
      (Some(offset), Some(dst)) => {
        let index = unsigned(dst.value[3 .. 0]);
        var updated = state;
        updated.registers[index] = add_bits(
          state.registers[index], get_slice_int(64, signed(immediate_value(offset)) * lanes, 0)
        );
        Some(vector_finish(instruction, state, updated))
      }, _ => None(),
    }
  else None()
}
