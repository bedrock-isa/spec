function vector_response_length(instruction : Decoded_instruction, state : Cpu_state) -> int = {
    let memory_kind = vector_semantics(instruction.form.operation).memory;
    let active_bytes = vector_current_length_bytes(state);
    if memory_kind == Some(VectorPredicateMove) then {
        tdiv_int(active_bytes, 8)
    } else {
        if memory_kind == Some(VectorGather) then {
            operation_width(instruction)
        } else {
            active_bytes
        }
    }
}

function vector_memory_source_result(
    instruction : Decoded_instruction,
    before : Cpu_state,
    after : Cpu_state,
    memory : list(bits(8)),
) -> (
    option(Cpu_state)
) = {
    let operation = instruction.form.operation;
    let memory_kind = vector_semantics(operation).memory;
    if memory_kind == Some(VectorPredicateMove) then {
        match predicate_register_index(instruction, Operand_dst) {
            None() => None(),
            Some(destination) => {
                var updated = after;
                updated.predicate_registers[unsigned(destination)] = vector_replace_low_bytes(
                    before.predicate_registers[unsigned(destination)], memory,
                    tdiv_int(vector_current_length_bytes(before), 8));
                updated.vector_state_modified = true;
                Some(updated)
            },
        }
    } else {
        let element_bytes = operation_width(instruction);
        let active_bytes = vector_current_length_bytes(before);
        let active_predicate_bytes = tdiv_int(active_bytes, 8);
        let lanes = tdiv_int(active_bytes, element_bytes);
        let predicate = vector_memory_predicate(instruction, before);
        if memory_kind == Some(VectorMoveMerge) | memory_kind == Some(VectorMoveReplace) then {
            match vector_register_index(instruction, Operand_dst) {
                None() => None(),
                Some(destination) => {
                    var updated = after;
                    updated.vector_registers[unsigned(destination)] =
                        if memory_kind == Some(VectorMoveReplace) then {
                            vector_replace_low_bytes(
                                before.vector_registers[unsigned(destination)],
                                memory,
                                active_bytes)
                        } else {
                            vector_merge_image(
                                before.vector_registers[unsigned(destination)],
                                memory,
                                predicate,
                                0,
                                lanes,
                                element_bytes,
                            )
                        };
                    updated.vector_state_modified = true;
                    Some(updated)
                },
            }
        } else {
            if vector_integer_binary_operation(operation) then {
                match vector_register_index(instruction, Operand_dst) {
                    None() => None(),
                    Some(destination) => {
                        var updated = after;
                        updated.vector_registers[unsigned(destination)] = vector_integer_binary_image(
                            operation,
                            before.vector_registers[unsigned(destination)],
                            memory,
                            predicate,
                            0,
                            lanes,
                            element_bytes,
                        );
                        updated.vector_state_modified = true;
                        Some(updated)
                    },
                }
            } else {
                if vector_integer_unary_operation(operation) then {
                    match vector_register_index(instruction, Operand_dst) {
                        None() => None(),
                        Some(destination) => {
                            var updated = after;
                            updated.vector_registers[unsigned(destination)] = vector_integer_unary_source_image(
                                operation,
                                before.vector_registers[unsigned(destination)],
                                memory,
                                predicate,
                                0,
                                lanes,
                                element_bytes,
                            );
                            updated.vector_state_modified = true;
                            Some(updated)
                        },
                    }
                } else {
                    if vector_integer_reduction_operation(operation) then {
                        match operand_named(instruction, Operand_dst) {
                            None() => None(),
                            Some(destination) => {
                                var updated = after;
                                updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
                                    64,
                                    vector_integer_reduction_image(
                                        operation,
                                        memory,
                                        predicate,
                                        0,
                                        lanes,
                                        element_bytes,
                                        vector_integer_reduction_identity(operation, element_bytes),
                                    ),
                                    0,
                                );
                                Some(updated)
                            },
                        }
                    } else {
                        if vector_shift_operation_p(operation) then {
                            match vector_register_index(instruction, Operand_dst) {
                                None() => None(),
                                Some(destination) => {
                                    var updated = after;
                                    updated.vector_registers[unsigned(destination)] = vector_shift_image(
                                        operation,
                                        before.vector_registers[unsigned(destination)],
                                        memory,
                                        0,
                                        true,
                                        predicate,
                                        0,
                                        lanes,
                                        element_bytes,
                                    );
                                    updated.vector_state_modified = true;
                                    Some(updated)
                                },
                            }
                        } else {
                            if vector_integer_compare_operation(operation) then {
                                match (
                                    vector_register_index(instruction, Operand_lhs),
                                    predicate_register_index(instruction, Operand_govern),
                                    predicate_register_index(instruction, Operand_dst),
                                ) {
                                    (Some(left), Some(govern), Some(destination)) => {
                                        let condition : int = match operand_named(instruction, Operand_cc) {
                                            Some(value) => unsigned(value.value[3 .. 0]),
                                            None() => 0,
                                        };
                                        var updated = after;
                                        updated.predicate_registers[unsigned(destination)] = vector_integer_compare_image(
                                            operation,
                                            condition,
                                            before.vector_registers[unsigned(left)],
                                            memory,
                                            before.predicate_registers[unsigned(govern)],
                                            vector_zero_low_bytes(
                                                before.predicate_registers[unsigned(destination)],
                                                active_predicate_bytes),
                                            0,
                                            lanes,
                                            element_bytes,
                                        );
                                        updated.vector_state_modified = true;
                                        Some(updated)
                                    },
                                    _ => None(),
                                }
                            } else {
                                None()
                            }
                        }
                    }
                }
            }
        }
    }
}

function vector_memory_destination_result(
    instruction : Decoded_instruction,
    before : Cpu_state,
    memory : list(bits(8)),
) -> (
    option(list(bits(8)))
) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let active_bytes = vector_current_length_bytes(before);
    let lanes = tdiv_int(active_bytes, element_bytes);
    let predicate = vector_memory_predicate(instruction, before);
    if vector_integer_binary_operation(operation) then {
        match vector_register_index(instruction, Operand_src) {
            Some(source) => Some(
                vector_integer_binary_image(
                    operation,
                    memory,
                    before.vector_registers[unsigned(source)],
                    predicate,
                    0,
                    lanes,
                    element_bytes,
                ),
            ),
            None() => None(),
        }
    } else {
        if vector_shift_operation_p(operation) then {
            let counts : list(bits(8)) = match vector_register_index(instruction, Operand_src) {
                Some(source) => before.vector_registers[unsigned(source)],
                None() => zero_vector_bytes(active_bytes),
            };
            let vector_counts = vector_register_index(instruction, Operand_src) != None();
            let immediate : int = match operand_named(instruction, Operand_count) {
                Some(value) => unsigned(immediate_value(value)),
                None() => 0,
            };
            Some(
                vector_shift_image(
                    operation,
                    memory,
                    counts,
                    immediate,
                    vector_counts,
                    predicate,
                    0,
                    lanes,
                    element_bytes,
                ),
            )
        } else {
            None()
        }
    }
}
