function execute_VCMPcc_integer(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if (true | true | true)
       & not_bool(fp_form) then match
    (vector_register_index(instruction, "lhs"), vector_register_index(instruction, "rhs"),
     predicate_register_index(instruction, "govern"),
     predicate_register_index(instruction, "dst")) {
    (Some(left), Some(right), Some(govern), Some(destination)) => {
      let condition : int = match operand_named(instruction, "cc") {
        Some(value) => unsigned(value.value[3 .. 0]), None() => 0,
      };
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = vector_integer_compare_image(
        operation, condition, state.vector_registers[unsigned(left)],
        state.vector_registers[unsigned(right)], state.predicate_registers[unsigned(govern)],
        empty, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else None()
}

function execute_VCMPcc_floating(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  start_vector_fp_transaction(instruction, state)
