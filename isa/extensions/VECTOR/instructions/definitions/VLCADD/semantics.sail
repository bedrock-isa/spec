function clause register_result_extension(Op_VLCADD) = RegisterZeroExtend

function clause repeat_semantics(Op_VLCADD) = RepeatObserveDestination

function clause vector_semantics(Op_VLCADD) = vector_default_semantics()

function execute_VLCADD_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true then {
        match (operand_named(instruction, Operand_offset), operand_named(instruction, Operand_dst)) {
            (Some(offset), Some(dst)) => {
                let index = unsigned(dst.value[3 .. 0]);
                var updated = state;
                updated.registers[index] = add_bits(
                    state.registers[index],
                    get_slice_int(64, signed(immediate_value(offset)) * lanes, 0),
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VLCADD : unit

function clause execute_uop(UopInstruction_VLCADD(), _, values, instruction, before, speculative) =
    match execute_VLCADD_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VLCADD local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VLCADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VLCADD(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                uop_make(
                    UopCommit(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
            instruction,
            state,
        ),
    )
