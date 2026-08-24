function execute_PTAIL(instruction : Decoded_instruction, state : Cpu_state)
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
       | true | true then
    match predicate_register_index(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        let boundary : int = if operation == Op_PHEAD | operation == Op_PTAIL then
          match value_named(instruction, state, "count") {
            Some(value) => tmod_int(unsigned(value), lanes), None() => 0,
          }
          else 0;
        let first = if operation == Op_PHEAD then boundary else 0;
        let last = if operation == Op_PFALSE then 0
                   else if operation == Op_PTAIL then boundary else lanes;
        var updated = state;
        updated.predicate_registers[unsigned(destination)] =
          predicate_fill_typed(empty, 0, lanes, element_bytes, first, last);
        Some(vector_finish(instruction, state, updated))
      },
    }
  else None()
}
