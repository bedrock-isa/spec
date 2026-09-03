union clause Uop_kind = UopVectorCompute : Semantic_operation

val vector_register_compute_result : (
        Semantic_operation,
        Decoded_instruction,
        Cpu_state,
    ) -> option(Vector_compute_result)

union clause Uop_kind = UopVectorBranchGuard : Vector_branch_uop_operation
union clause Uop_kind = UopVectorLoopGuard : unit

function clause execute_uop(UopVectorBranchGuard(operation), _, values, instruction, before, speculative) =
    match predicate_register_index(instruction, Operand_predicate) {
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "vector branch predicate is unavailable")),
        Some(source) => {
            let element_bytes = operation_width(instruction);
            let lanes = tdiv_int(speculative.vector_length_bytes, element_bytes);
            let predicate = speculative.predicate_registers[unsigned(source)];
            let take = if operation == VectorBranchAny then predicate_any(predicate)
                       else if operation == VectorBranchNone then not_bool(predicate_any(predicate))
                       else predicate_all_typed(predicate, 0, lanes, element_bytes);
            if take then uop_step_continue(speculative, values) else uop_step_complete(speculative, CommitControl)
        },
    }

function clause execute_uop(UopVectorLoopGuard(), _, values, instruction, before, speculative) =
    match (operand_named(instruction, Operand_remaining), operand_named(instruction, Operand_offset),
           predicate_register_index(instruction, Operand_predicate)) {
        (Some(remaining_operand), Some(offset_operand), Some(predicate)) => {
            let remaining_index = unsigned(remaining_operand.value[3 .. 0]);
            let offset_index = unsigned(offset_operand.value[3 .. 0]);
            let remaining = unsigned(speculative.registers[remaining_index]);
            let offset = unsigned(speculative.registers[offset_index]);
            let element_bytes = operation_width(instruction);
            let lanes = tdiv_int(speculative.vector_length_bytes, element_bytes);
            if remaining == 0 then uop_step_continue(speculative, values)
            else if offset >= lanes then uop_step_fault(faulted_with_error_code(
                before, instruction.form.operation, VectorRangeFault,
                "PLOOP offset exceeds the lane count", 0x0000000000000000))
            else {
                let active = if remaining < lanes - offset then remaining else lanes - offset;
                var updated = speculative;
                updated.predicate_registers[unsigned(predicate)] = predicate_fill_typed(
                    zero_vector_bytes(tdiv_int(speculative.vector_length_bytes, 8)),
                    0, lanes, element_bytes, offset, offset + active);
                updated.registers[remaining_index] = get_slice_int(64, remaining - active, 0);
                updated.registers[offset_index] = 0x0000000000000000;
                updated.vector_state_modified = true;
                uop_step_complete(updated, CommitRegisters)
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "PLOOP operands are unavailable")),
    }
