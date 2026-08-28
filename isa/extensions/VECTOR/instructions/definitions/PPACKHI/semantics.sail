function execute_PPACKHI(instruction : Decoded_instruction, state : Cpu_state)
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
       | true | true then match
    (predicate_register_index(instruction, Operand_src),
     predicate_register_index(instruction, Operand_dst)) {
    (Some(source), Some(destination)) => {
      let source_image = state.predicate_registers[unsigned(source)];
      let image = if operation == Op_PUNPKLO | operation == Op_PUNPKHI then
        predicate_unpack_image(source_image, empty, 0, lanes, element_bytes,
                               operation == Op_PUNPKHI)
      else predicate_pack_image(source_image, empty, 0, lanes, element_bytes,
                                operation == Op_PPACKHI);
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = image;
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else None()
}
