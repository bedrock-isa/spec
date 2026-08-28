function execute_VLCNT_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
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
        match operand_named(instruction, Operand_dst) {
            Some(dst) => {
                var updated = state;
                updated.registers[unsigned(dst.value[3 .. 0])] = get_slice_int(64, lanes, 0);
                Some(vector_finish(instruction, state, updated))
            },
            None()    => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VLCNT : unit

function clause execute_uop(UopInstruction_VLCNT(), _, values, instruction, before, speculative) =
    match execute_VLCNT_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VLCNT local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VLCNT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_VLCNT(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                make_uop(
                    UopCommit(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
            instruction,
            state,
        ),
    )
