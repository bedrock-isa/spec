function execute_VREDMINU(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  match
    (vector_register_index(instruction, Operand_src),
     predicate_register_index(instruction, Operand_govern),
     operand_named(instruction, Operand_dst)) {
    (Some(source), Some(predicate), Some(destination)) => {
      var updated = state;
      updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
        64,
        vector_integer_reduction_image(
          operation, state.vector_registers[unsigned(source)],
          state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes,
          vector_integer_reduction_identity(operation, element_bytes)
        ),
        0
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
}
