union clause Uop_kind = UopVectorStepPrepare : Semantic_operation
union clause Uop_kind = UopVectorStepIssue : Semantic_operation
union clause Uop_kind = UopVectorStepCommit : Semantic_operation

function vector_step_finish_lane(
    instruction : Decoded_instruction,
    state : Cpu_state,
    lane : int,
) -> (
    Uop_step
) =
    match (
        predicate_register_index(instruction, Operand_govern),
        predicate_register_index(instruction, Operand_completion),
    ) {
        (Some(govern), Some(completion)) => {
            let element_bytes = operation_width(instruction);
            let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
            var updated = state;
            updated.predicate_registers[unsigned(completion)] = predicate_set_bit(
                state.predicate_registers[unsigned(completion)],
                lane * element_bytes,
                true,
            );
            updated.vector_state_modified = true;
            match vector_step_first_pending(
                updated.predicate_registers[unsigned(govern)],
                updated.predicate_registers[unsigned(completion)],
                0,
                lanes,
                element_bytes,
            ) {
                Some(_) => uop_step_complete_boundary(updated, CommitMemory, BoundaryVectorLane),
                None() => uop_step_complete(updated, CommitMemory),
            }
        },
        _ => uop_step_fault(
            faulted(state, instruction.form.operation, InvalidControlState, "missing vector completion predicate"),
        ),
    }

function clause execute_uop(UopVectorStepPrepare(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector step uop does not match its instruction",
            ),
        )
    } else if vector_step_predicate_overlap_conflict(instruction) then {
        uop_step_fault(
            faulted(before, operation, IllegalInstruction, "governing and completion predicates overlap"),
        )
    } else if vector_step_gather_address_overlap_conflict(instruction) then {
        uop_step_fault(
            faulted(before, operation, IllegalInstruction, "gather address and destination vectors overlap"),
        )
    } else {
        match (
            predicate_register_index(instruction, Operand_govern),
            predicate_register_index(instruction, Operand_completion),
        ) {
            (Some(govern), Some(completion)) => {
                let element_bytes = operation_width(instruction);
                let lanes = tdiv_int(speculative.vector_length_bytes, element_bytes);
                let govern_image = speculative.predicate_registers[unsigned(govern)];
                let normalized = vector_step_normalize_completion(
                    govern_image,
                    speculative.predicate_registers[unsigned(completion)],
                    zero_vector_bytes(tdiv_int(speculative.vector_length_bytes, 8)),
                    0,
                    lanes,
                    element_bytes,
                );
                var updated = speculative;
                updated.predicate_registers[unsigned(completion)] = normalized;
                updated.vector_state_modified = true;
                match vector_step_first_pending(govern_image, normalized, 0, lanes, element_bytes) {
                    Some(lane) => uop_step_continue(
                        updated,
                        uop_value_set(
                            values,
                            uop.destination.index,
                            {
                                uop_value_empty() with
                                value = get_slice_int(64, lane, 0),
                                present = true,
                            },
                        ),
                    ),
                    None() => uop_step_complete(updated, CommitRegisters),
                }
            },
            _ => uop_step_fault(
                faulted(before, operation, InvalidControlState, "missing vector predicates"),
            ),
        }
    }

function clause execute_uop(UopVectorStepIssue(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector step issue does not match its instruction",
            ),
        )
    } else {
        match uop_value_get(values, uop.source0.index) {
            Some(prepared) => {
                let lane = unsigned(prepared.value);
                let element_bytes = operation_width(instruction);
                match vector_step_address(instruction, speculative, lane, element_bytes) {
                    None() => uop_step_fault(
                        faulted(speculative, operation, InvalidControlState, "missing vector step address operand"),
                    ),
                    Some(address) => {
                        let payload : list(bits(8)) = if vector_semantics(operation).memory == Some(VectorScatter) then {
                                match vector_register_index(instruction, Operand_src) {
                                    Some(source) => vector_lane_bytes(
                                        speculative.vector_registers[unsigned(source)],
                                        lane,
                                        element_bytes,
                                    ),
                                    None() => [||],
                                }
                            } else {
                                [||]
                            };
                        uop_step_wait_committed(
                            uop.destination.index,
                            vector_step_request(instruction, speculative, address, element_bytes, payload),
                            0x0000000000000000,
                        )
                    },
                }
            },
            None() => uop_step_fault(
                faulted(speculative, operation, InvalidControlState, "vector step preparation is unavailable"),
            ),
        }
    }

function clause execute_uop(UopVectorStepCommit(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector step commit does not match its instruction",
            ),
        )
    } else {
        match (uop_value_get(values, uop.source0.index), uop_value_get(values, uop.source1.index)) {
            (Some(prepared), Some(response)) => {
                let lane = unsigned(prepared.value);
                if vector_semantics(operation).memory == Some(VectorScatter) then {
                    vector_step_finish_lane(instruction, speculative, lane)
                } else {
                    match vector_register_index(instruction, Operand_dst) {
                        Some(destination) => {
                            let element_bytes = operation_width(instruction);
                            if byte_count(response.body_bytes) != element_bytes then {
                                uop_step_fault(
                                    faulted(
                                        speculative,
                                        operation,
                                        InvalidControlState,
                                        "vector gather response length mismatch",
                                    ),
                                )
                            } else {
                                var updated = speculative;
                                updated.vector_registers[unsigned(destination)] = vector_write_lane(
                                    speculative.vector_registers[unsigned(destination)],
                                    lane,
                                    element_bytes,
                                    vector_lane_unsigned(response.body_bytes, 0, element_bytes),
                                );
                                updated.vector_state_modified = true;
                                vector_step_finish_lane(instruction, updated, lane)
                            }
                        },
                        None() => uop_step_fault(
                            faulted(speculative, operation, InvalidControlState, "missing vector gather destination"),
                        ),
                    }
                }
            },
            _ => uop_step_fault(
                faulted(speculative, operation, InvalidControlState, "vector step response is unavailable"),
            ),
        }
    }
