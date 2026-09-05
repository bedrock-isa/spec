function vector_fp_uop_image_commit(
    image : Vector_fp_image,
    uop : Uop,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Uop_step
) = {
    let operation = instruction.form.operation;
    if (image.generated_causes & vector_fp_allowed_causes(operation)) != image.generated_causes then {
        uop_step_fault(faulted(before, operation, InvalidControlState, "vector FP primitive reported an impossible cause"))
    } else {
        if fp_traps(before.fstatus, image.generated_causes) then {
            uop_step_fault(fp_fault_with_causes(before, operation, image.generated_causes))
        } else {
            match vector_writable_operand(instruction.operands) {
                None() => uop_step_fault(faulted(before, operation, InvalidControlState, "missing vector FP destination")),
                Some(destination) => {
                    var updated = speculative;
                    updated.fflags = updated.fflags | image.generated_causes;
                    if image.generated_causes != fflags_none then {
                        updated.fp_state_modified = true
                    };
                    if destination.operand_type == OperandType_Vn then {
                        let index = unsigned(destination.value[4 .. 0]);
                        updated.vector_registers[index] = vector_replace_low_bytes(
                            speculative.vector_registers[index], image.bytes,
                            vector_current_length_bytes(speculative));
                        updated.vector_state_modified = true;
                        uop_step_continue(updated, values)
                    } else {
                        if destination.operand_type == OperandType_Pn then {
                            let index = unsigned(destination.value[3 .. 0]);
                            updated.predicate_registers[index] = vector_replace_low_bytes(
                                speculative.predicate_registers[index], image.bytes,
                                tdiv_int(vector_current_length_bytes(speculative), 8));
                            updated.vector_state_modified = true;
                            uop_step_continue(updated, values)
                        } else {
                            if destination.operand_type == OperandType_VEA then {
                                uop_step_continue(
                                    updated,
                                    uop_value_set(
                                        values,
                                        uop.destination.index,
                                        {
                                            uop_value_empty() with
                                            body_bytes = image.bytes,
                                        },
                                    ),
                                )
                            } else {
                                uop_step_fault(
                                    faulted(before, operation, InvalidControlState, "unsupported vector FP destination"),
                                )
                            }
                        }
                    }
                },
            }
        }
    }
}

function vector_fp_uop_execute(
    operation : Semantic_operation,
    uop : Uop,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Uop_step
) =
    if instruction.form.operation != operation then {
        uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector FP uop does not match its instruction",
            ),
        )
    } else {
        match vector_memory_operand(instruction.operands) {
            None() => if vector_fp_reduction_operation(operation) then {
                match vector_register_index(instruction, Operand_src) {
                    Some(source) => vector_fp_reduction_commit(
                        instruction,
                        speculative,
                        speculative,
                        speculative.vector_registers[unsigned(source)],
                        values,
                    ),
                    None() => uop_step_fault(
                        faulted(before, operation, InvalidControlState, "missing vector FP reduction source"),
                    ),
                }
            } else {
                match vector_fp_evaluate_image(instruction, speculative, [||]) {
                    Some(image) => vector_fp_uop_image_commit(
                        image, uop, values, instruction, before, speculative,
                    ),
                    None() => uop_step_fault(
                        faulted(before, operation, InvalidControlState, "local vector FP evaluation failed"),
                    ),
                }
            },
            Some(_) => match uop_value_get(values, uop.auxiliary.index) {
                Some(memory_value) => if byte_count(memory_value.body_bytes)
                                        != vector_current_length_bytes(before) then {
                    uop_step_fault(
                        faulted(before, operation, InvalidControlState, "vector FP memory response length mismatch"),
                    )
                } else {
                    if vector_fp_reduction_operation(operation) then {
                        vector_fp_reduction_commit(
                            instruction, before, speculative, memory_value.body_bytes, values,
                        )
                    } else {
                        match vector_fp_evaluate_image(instruction, before, memory_value.body_bytes) {
                            Some(image) => vector_fp_uop_image_commit(
                                image,
                                uop,
                                values,
                                instruction,
                                before,
                                speculative,
                            ),
                            None() => uop_step_fault(
                                faulted(
                                    before,
                                    operation,
                                    InvalidControlState,
                                    "local vector FP memory evaluation failed",
                                ),
                            ),
                        }
                    }
                },
                None() => uop_step_fault(
                    faulted(before, operation, InvalidControlState, "vector FP memory response is unavailable"),
                ),
            },
        }
    }
