union clause Uop_kind = UopFpArithmetic : Fp_arithmetic_operation
union clause Uop_kind = UopFpCompare : Fp_compare_operation
union clause Uop_kind = UopFpConvert : Fp_conversion_operation
union clause Uop_kind = UopFpData : Fp_data_operation
union clause Uop_kind = UopFpOperation : Semantic_operation
union clause Uop_kind = UopFpPairMove : unit

function clause execute_uop(UopFpPairMove(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(first), Some(second)) => if    uop.destination.kind
                                          != UopLocationFpRegister
                                          |  uop.destination2.kind
                                          != UopLocationFpRegister then {
            uop_step_fault(
                faulted(
                    before,
                    instruction.form.operation,
                    InvalidControlState,
                    "floating-point pair destination is not writable",
                ),
            )
        } else {
            var updated = speculative;
            updated.floating_registers[unsigned(get_slice_int(4, uop.destination.index, 0))] = first;
            updated.floating_registers[unsigned(get_slice_int(4, uop.destination2.index, 0))] = second;
            updated.fp_component_modified = true;
            uop_step_continue(updated, values)
        },
        _ => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "floating-point pair source is unavailable",
            ),
        ),
    }

function fp_uop_operand_read(
    instruction : Decoded_instruction,
    state : Cpu_state,
    values : list(Uop_value),
    location : Uop_location,
    source_index : int,
) -> (
    option(Fp_operand_image)
) =
    match (fp_source_at(instruction.operands, source_index, 0), uop_location_read(location, state, values)) {
        (Some(operand), Some(value)) => {
            let kind = fp_operand_kind_for(instruction, operand, operation_width(instruction));
            Some(
                struct {
                    valid = true,
                    kind = kind,
                    bits =
                        if kind == FpBits32 then {
                            0x00000000 @ value[31 .. 0]
                        } else {
                            value
                        },
                },
            )
        },
        _ => None(),
    }

function fp_uop_slots_build_arithmetic(
    uop : Uop,
    instruction : Decoded_instruction,
    state : Cpu_state,
    values : list(Uop_value),
) -> (
    option(Fp_operand_slots)
) = {
    let source_count : int = match fp_semantics(instruction.form.operation) {
        Some(semantics) => semantics.source_count,
        None() => 0,
    };
    match (
        if source_count > 0 then {
            fp_uop_operand_read(instruction, state, values, uop.source0, 0)
        } else {
            Some(empty_fp_operand())
        },
        if source_count > 1 then {
            fp_uop_operand_read(instruction, state, values, uop.source1, 1)
        } else {
            Some(empty_fp_operand())
        },
        if source_count > 2 then {
            fp_uop_operand_read(instruction, state, values, uop.source2, 2)
        } else {
            Some(empty_fp_operand())
        },
    ) {
        (Some(operand0), Some(operand1), Some(operand2)) => Some(
            struct { operand0 = operand0, operand1 = operand1, operand2 = operand2 },
        ),
        _ => None(),
    }
}

function fp_uop_result_commit(
    candidate : Fp_candidate_result,
    uop : Uop,
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
    values : list(Uop_value),
) -> (
    Uop_step
) =
    if not_bool(candidate.shape_valid) then {
        uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "invalid floating-point response shape or echo",
            ),
        )
    } else {
        if candidate.trap then {
            uop_step_fault(fp_fault_with_causes(before, instruction.form.operation, candidate.trap_errors))
        } else {
            let destination_kind = fp_derive_destination_kind(instruction.form);
            if    destination_kind
               != FpDestinationFlags
               &  destination_kind
               != FpDestinationFnPair
               &  uop.destination.kind
               != UopLocationFpRegister
               &  uop.destination.kind
               != UopLocationRegister
               &  uop.destination.kind
               != UopLocationTemporary then {
                uop_step_fault(
                    faulted(
                        before,
                        instruction.form.operation,
                        InvalidControlState,
                        "floating-point destination is not writable",
                    ),
                )
            } else {
                let result = if candidate.result_kind == FpResultBits32 | candidate.result_kind == FpResultPair32 then {
                        0x00000000 @ candidate.primary[31 .. 0]
                    } else {
                        candidate.primary
                    };
                let written = if destination_kind == FpDestinationFlags then {
                        Some((speculative, values))
                    } else {
                        if destination_kind == FpDestinationFnPair then {
                            if    uop.destination.kind
                               != UopLocationFpRegister
                               |  uop.destination2.kind
                               != UopLocationFpRegister then {
                                None()
                            } else {
                                var state = speculative;
                                state.floating_registers[unsigned(get_slice_int(4, uop.destination.index, 0))] = result;
                                state.floating_registers[unsigned(get_slice_int(4, uop.destination2.index, 0))] =
                                    if candidate.result_kind == FpResultPair32 then {
                                        0x00000000 @ candidate.secondary[31 .. 0]
                                    } else {
                                        candidate.secondary
                                    };
                                Some((state, values))
                            }
                        } else {
                            if uop.destination.kind == UopLocationFpRegister then {
                                var state = speculative;
                                state.floating_registers[unsigned(get_slice_int(4, uop.destination.index, 0))] = result;
                                Some((state, values))
                            } else {
                                if uop.destination.kind == UopLocationRegister then {
                                    var state = speculative;
                                    state.registers[unsigned(get_slice_int(4, uop.destination.index, 0))] =
                                        candidate.primary;
                                    Some((state, values))
                                } else {
                                    uop_location_write(
                                        uop.destination,
                                        result,
                                        uop.width,
                                        instruction.form.operation,
                                        speculative,
                                        values,
                                    )
                                }
                            }
                        }
                    };
                match written {
                    None() => uop_step_fault(
                        faulted(
                            before,
                            instruction.form.operation,
                            InvalidControlState,
                            "floating-point destination write failed",
                        ),
                    ),
                    Some((written_state, written_values)) => {
                        var updated = written_state;
                        updated.fflags = updated.fflags | candidate.generated_causes;
                        updated.flags =
                            (updated.flags & not_vec(candidate.flags_mask)) |
                                (candidate.flags_value & candidate.flags_mask);
                        updated.fp_component_modified = true;
                        uop_step_continue(updated, written_values)
                    },
                }
            }
        }
    }

function fp_uop_execute(
    expected_operation : Semantic_operation,
    uop : Uop,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Uop_step
) =
    if not_bool(fp_fstatus_valid(before.fstatus)) then {
        uop_step_fault(
            faulted_with_error_code(
                before,
                instruction.form.operation,
                InvalidControlState,
                "reserved FSTATUS bits are nonzero",
                0x0000000000000001,
            ),
        )
    } else {
        if instruction.form.operation != expected_operation then {
            uop_step_fault(
                faulted(
                    before,
                    instruction.form.operation,
                    InvalidControlState,
                    "floating-point uop does not match its instruction",
                ),
            )
        } else {
            match (
                fp_uop_slots_build_arithmetic(uop, instruction, speculative, values),
                fp_form_path(instruction.form),
                fp_derive_result_kind(instruction.form, operation_width(instruction)),
            ) {
                (Some(slots), Some(path), Some(result_kind)) => {
                    let contract_word : bits(64) = match uop_location_read(uop.auxiliary, speculative, values) {
                        Some(value) => value,
                        None() => 0x0000000000000000,
                    };
                    match fp_build_request(
                        instruction.form.operation,
                        instruction.form,
                        path,
                        result_kind,
                        operation_width(instruction),
                        slots,
                        before.fstatus,
                        contract_word,
                    ) {
                        Some(request) => {
                            let selector : bits(64) = match operand_named(instruction, Operand_constant_id) {
                                Some(operand) => operand.value,
                                None() => 0x0000000000000000,
                            };
                            match fp_local_response(request, selector) {
                                Some(response) => fp_uop_result_commit(
                                    fp_finalize_response(request, response, before.fstatus),
                                    uop,
                                    instruction,
                                    before,
                                    speculative,
                                    values,
                                ),
                                None() => uop_step_fault(
                                    faulted(
                                        before,
                                        instruction.form.operation,
                                        InvalidControlState,
                                        "floating-point primitive rejected a valid request",
                                    ),
                                ),
                            }
                        },
                        None() => uop_step_fault(
                            faulted(
                                before,
                                instruction.form.operation,
                                InvalidControlState,
                                "invalid floating-point request image",
                            ),
                        ),
                    }
                },
                _ => uop_step_fault(
                    faulted(
                        before,
                        instruction.form.operation,
                        InvalidControlState,
                        "missing floating-point uop operands or form semantics",
                    ),
                ),
            }
        }
    }

function clause execute_uop(UopFpArithmetic(operation), uop, values, instruction, before, speculative) =
    fp_uop_execute(fp_arithmetic_semantic_operation(operation), uop, values, instruction, before, speculative)

function clause execute_uop(UopFpCompare(operation), uop, values, instruction, before, speculative) =
    fp_uop_execute(fp_compare_semantic_operation(operation), uop, values, instruction, before, speculative)

function clause execute_uop(UopFpConvert(operation), uop, values, instruction, before, speculative) =
    fp_uop_execute(fp_conversion_semantic_operation(operation), uop, values, instruction, before, speculative)

function clause execute_uop(UopFpData(operation), uop, values, instruction, before, speculative) =
    fp_uop_execute(fp_data_semantic_operation(operation), uop, values, instruction, before, speculative)

function clause execute_uop(UopFpOperation(operation), uop, values, instruction, before, speculative) =
    fp_uop_execute(operation, uop, values, instruction, before, speculative)
