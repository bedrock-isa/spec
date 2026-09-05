function vector_register_index(instruction : Decoded_instruction, name : Operand_id) -> option(bits(5)) =
    match operand_named(instruction, name) {
        Some(operand) => Some(operand.value[4 .. 0]),
        None() => None(),
    }

function vector_finish(instruction : Decoded_instruction, before : Cpu_state, after : Cpu_state) -> Execution_result = {
    var committed = after;
    committed.pc = next_pc(before, instruction);
    committed.vector_state_modified = true;
    completed(before, committed, CommitRegisters, [||])
}

function vector_operand_writes(name : Operand_id, operands : list(Decoded_operand)) -> bool =
    match operands {
        [||] => false,
        operand :: tail => if operand.name == name then {
            operand.access == AccessWrite | operand.access == AccessReadWrite
        } else {
            vector_operand_writes(name, tail)
        },
    }

function vector_vstatus_valid(image : bits(64)) -> bool = {
    let selector = unsigned(image[2 .. 0]);
    (image & 0xFFFFFFFFFFFF0000) == 0x0000000000000000
    & (image & 0x000000000000FFF8) == 0x0000000000000000
    & selector != 1 & selector != 2
}

function vector_current_length_bytes(state : Cpu_state) -> int = {
    let selector = unsigned(state.vstatus[2 .. 0]);
    let selected = if selector == 0 then state.max_vector_length_bytes
                   else vector_power_of_two(selector + 1);
    if selected < state.max_vector_length_bytes then selected
    else state.max_vector_length_bytes
}

union clause Uop_kind = UopVectorStateRead : unit
union clause Uop_kind = UopVectorStateWrite : unit

function clause execute_uop(UopVectorStateRead(), _, values, instruction,
                            before, speculative) =
    match operand_named(instruction, Operand_dst) {
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, IllegalInstruction,
                    "vector state read has no destination"),
        ),
        Some(destination) => {
            var updated = speculative;
            updated.registers[unsigned(destination.value[3 .. 0])] =
                0x000000000000 @ speculative.vstatus[15 .. 0];
            uop_step_continue(updated, values)
        },
    }

function clause execute_uop(UopVectorStateWrite(), _, values, instruction,
                            before, speculative) =
    match value_named(instruction, speculative, Operand_src) {
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, IllegalInstruction,
                    "vector state write has no source"),
        ),
        Some(source) => {
            let image = 0x000000000000 @ source[15 .. 0];
            if not_bool(vector_vstatus_valid(image)) then {
                uop_step_fault(
                    faulted(before, instruction.form.operation, InvalidControlState,
                            "invalid VSTATUS image"),
                )
            } else {
                var updated = speculative;
                updated.vstatus = image;
                updated.vector_state_modified =
                    if image != speculative.vstatus then true
                    else speculative.vector_state_modified;
                uop_step_continue(updated, values)
            }
        },
    }

function vector_memory_predicate(instruction : Decoded_instruction, state : Cpu_state) -> list(bits(8)) =
    match predicate_register_index(instruction, Operand_govern) {
        Some(index) => state.predicate_registers[unsigned(index)],
    None() => zero_vector_bytes(tdiv_int(vector_current_length_bytes(state), 8)),
    }

function vector_ea_operand_ordinal(
    instruction : Decoded_instruction, operands : list(Decoded_operand), ordinal : int
) -> int = match operands {
    [||] => if operand_named(instruction, Operand_address) != None()
            then operand_ordinal(instruction, Operand_address)
            else operand_ordinal(instruction, Operand_base),
    operand :: tail => match operand.ea {
        Some(_) => ordinal,
        None() => vector_ea_operand_ordinal(instruction, tail, ordinal + 1),
    },
}

function vector_memory_operand_ordinal(instruction : Decoded_instruction) -> int =
    vector_ea_operand_ordinal(instruction, instruction.operands, 0)

function vector_active_memory_ranges(
    predicate : list(bits(8)), effective_address : bits(64), linear_address : bits(64),
    lane : int, lanes : int, element_bytes : int
) -> list(Memory_access_range) =
    if lane >= lanes then [||]
    else {
        let tail = vector_active_memory_ranges(
            predicate, effective_address, linear_address,
            lane + 1, lanes, element_bytes);
        let offset = lane * element_bytes;
        if predicate_bit(predicate, offset) then
            struct {
                effective_address = add_bits(effective_address, bits_from_int(offset)),
                linear_address = add_bits(linear_address, bits_from_int(offset)),
                width = element_bytes,
                buffer_offset = offset,
            } :: tail
        else tail
    }

function vector_memory_ranges(
    predicate_move : bool, predicate : list(bits(8)),
    effective_address : bits(64), linear_address : bits(64),
    length : int, element_bytes : int
) -> list(Memory_access_range) =
    if length <= 0 then [||]
    else if predicate_move then [|struct {
        effective_address = effective_address,
        linear_address = linear_address,
        width = length,
        buffer_offset = 0,
    }|]
    else vector_active_memory_ranges(
        predicate, effective_address, linear_address,
        0, tdiv_int(length, element_bytes), element_bytes)

function vector_fp_basic_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).fp_basic

function vector_fp_convert_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).fp_conversion

function vector_reduce_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).reduction

function vector_fp_compute_operation(operation : Semantic_operation) -> bool =
    vector_fp_basic_operation(operation) | vector_fp_convert_operation(operation) | vector_reduce_operation(operation)

function vector_writable_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) =
    match operands {
        [||] => None(),
        operand :: tail => if operand.access == AccessWrite | operand.access == AccessReadWrite then {
            Some(operand)
        } else {
            vector_writable_operand(tail)
        },
    }

function vector_fp_allowed_causes(operation : Semantic_operation) -> bits(5) =
    vector_semantics(operation).fp_allowed_causes
function clause ea_update_amount(EaUpdateDifference_vlen_bytes, state, _) =
    vector_current_length_bytes(state)

function clause ea_update_amount(EaUpdateDifference_element_count, state, width) =
    tdiv_int(vector_current_length_bytes(state), width)
