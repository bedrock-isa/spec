function vector_predicate_binary_compute(instruction : Decoded_instruction, state : Cpu_state) -> option(Vector_compute_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true then {
        match (predicate_register_index(instruction, Operand_src), predicate_register_index(instruction, Operand_dst)) {
            (Some(source), Some(destination)) => {
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = predicate_raw_binary(
                    state.predicate_registers[unsigned(destination)],
                    state.predicate_registers[unsigned(source)],
                    operation,
                );
                Some(VectorComputeState(updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

function vector_predicate_slide_compute(instruction : Decoded_instruction, state : Cpu_state) -> option(Vector_compute_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true then {
        match (predicate_register_index(instruction, Operand_dst), operand_named(instruction, Operand_count)) {
            (Some(destination), Some(count_operand)) => {
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = predicate_slide_image(
                    operation,
                    state.predicate_registers[unsigned(destination)],
                    empty,
                    empty,
                    0,
                    lanes,
                    element_bytes,
                    unsigned(immediate_value(count_operand)),
                );
                Some(VectorComputeState(updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

function vector_predicate_pair_compute(instruction : Decoded_instruction, state : Cpu_state) -> option(Vector_compute_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true | true | true | true then {
        match (
            predicate_register_index(instruction, Operand_lhs),
            predicate_register_index(instruction, Operand_rhs),
            predicate_register_index(instruction, Operand_dst),
        ) {
            (Some(left), Some(right), Some(destination)) => {
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = predicate_pair_image(
                    operation,
                    state.predicate_registers[unsigned(left)],
                    state.predicate_registers[unsigned(right)],
                    empty,
                    0,
                    lanes,
                    element_bytes,
                );
                Some(VectorComputeState(updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}
