union clause Uop_kind = UopVectorFp : Semantic_operation
union clause Uop_kind = UopVectorCompute : Semantic_operation

val vector_fp_uop_execute : (
        Semantic_operation,
        Uop,
        list(Uop_value),
        Decoded_instruction,
        Cpu_state,
        Cpu_state,
    ) -> Uop_step

val vector_register_compute_result : (
        Semantic_operation,
        Decoded_instruction,
        Cpu_state,
    ) -> option(Vector_compute_result)

function vector_instruction_uses_fp(instruction : Decoded_instruction) -> bool = {
    let operation = instruction.form.operation;
    let semantics = vector_semantics(operation);
    let fp_capable = semantics.fp_basic | semantics.fp_conversion
                   | semantics.fp_reduction_operation != None();
    let integer_capable = semantics.integer_binary != None()
                        | semantics.integer_unary != None()
                        | semantics.integer_compare != None()
                        | semantics.integer_reduction != None();
    let fp_size : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    let fp_reduction_destination : bool = match operand_named(instruction, Operand_dst) {
        Some(destination) => destination.operand_type == OperandType_Fn,
        None() => false,
    };
    fp_capable & (not_bool(integer_capable) | fp_size | fp_reduction_destination)
}

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
                updated.vector_component_modified = true;
                uop_step_complete(updated, CommitRegisters)
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "PLOOP operands are unavailable")),
    }

function clause execute_uop(UopVectorFp(operation), uop, values, instruction, before, speculative) =
    vector_fp_uop_execute(operation, uop, values, instruction, before, speculative)
