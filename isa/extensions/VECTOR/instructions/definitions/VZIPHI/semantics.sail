function clause register_result_extension(Op_VZIPHI) = RegisterZeroExtend

function clause repeat_semantics(Op_VZIPHI) = RepeatObserveDestination

function clause vector_semantics(Op_VZIPHI) =
    {
        vector_default_semantics() with
        permute = Some(VectorZipHigh),
    }

function execute_VZIPHI_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true | true | true | true | true | true | true | true then {
        match (vector_register_index(instruction, Operand_dst), predicate_register_index(instruction, Operand_govern)) {
            (Some(destination), Some(predicate)) => {
                let source : list(bits(8)) = match vector_register_index(instruction, Operand_src) {
                    Some(index) => state.vector_registers[unsigned(index)],
                    None() => zero_vector,
                };
                let count : int = match operand_named(instruction, Operand_count) {
                    Some(count_operand) => unsigned(immediate_value(count_operand)),
                    None() => 0,
                };
                let original = state.vector_registers[unsigned(destination)];
                var updated = state;
                updated.vector_registers[unsigned(destination)] = vector_permute_image(
                    operation,
                    original,
                    source,
                    original,
                    state.predicate_registers[unsigned(predicate)],
                    0,
                    lanes,
                    element_bytes,
                    count,
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VZIPHI : unit

function clause execute_uop(UopInstruction_VZIPHI(), _, values, instruction, before, speculative) =
    match execute_VZIPHI_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VZIPHI local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VZIPHI(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VZIPHI(),
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
