function clause execute_uop(UopVectorMemoryStore(), uop, values, instruction, before, speculative) =
    match vector_memory_operand(instruction.operands) {
        None() => uop_step_continue(speculative, values),
        Some(memory_operand) => if not_bool(vector_operand_writes(memory_operand.name, instruction.operands)) then {
            uop_step_continue(speculative, values)
        } else {
            match (uop_value_get(values, uop.source0.index), uop_value_get(values, uop.source1.index)) {
                (Some(address), Some(output)) => uop_step_wait(
                    0 - 1,
                    vector_uop_memory_request_make(
                        Write,
                        instruction,
                        speculative,
                        address,
                        output.body_bytes,
                        AccessStore,
                    ),
                    0x0000000000000000,
                ),
                _ => uop_step_fault(
                    faulted(
                        before,
                        instruction.form.operation,
                        InvalidControlState,
                        "vector uop store input is unavailable",
                    ),
                ),
            }
        },
    }

function clause execute_uop(UopVectorCompute(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState,
                    "vector compute uop does not match its instruction"),
        )
    } else match vector_memory_operand(instruction.operands) {
        Some(_) => execute_uop(UopVectorMemoryCompute(operation), uop, values, instruction, before, speculative),
        None() => match vector_register_compute_result(operation, instruction, speculative) {
            Some(VectorComputeState(updated)) => uop_step_continue(updated, values),
            Some(VectorComputeFault(result)) => uop_step_fault(result),
            None() => uop_step_fault(
                faulted(before, operation, IllegalInstruction,
                        "vector register operation rejected its instruction"),
            ),
        },
    }

function vector_integer_binary_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).integer_binary != None()

function vector_integer_unary_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).integer_unary != None()

function vector_shift_operation_p(operation : Semantic_operation) -> bool =
    vector_semantics(operation).shift != None()

function vector_integer_compare_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).integer_compare != None()

function vector_memory_direct_store_image(
    instruction : Decoded_instruction,
    state : Cpu_state,
    predicate : list(bits(8)),
    lanes : int,
    element_bytes : int,
) -> (
    option(list(bits(8)))
) = {
    let operation = instruction.form.operation;
    let memory_kind = vector_semantics(operation).memory;
    if memory_kind == Some(VectorPredicateMove) then {
        match predicate_register_index(instruction, Operand_src) {
            Some(index) => Some(vector_low_bytes(
                state.predicate_registers[unsigned(index)],
                tdiv_int(vector_current_length_bytes(state), 8))),
            None() => None(),
        }
    } else {
        match vector_register_index(instruction, Operand_src) {
            None() => None(),
            Some(index) => {
                let source = state.vector_registers[unsigned(index)];
                if memory_kind == Some(VectorMoveMerge) then {
                    Some(source)
                } else {
                    if vector_integer_unary_operation(operation) then {
                        Some(
                            vector_integer_unary_source_image(
                                operation,
                                zero_vector_bytes(vector_current_length_bytes(state)),
                                source,
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
            },
        }
    }
}
