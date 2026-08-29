function vector_register_index(instruction : Decoded_instruction, name : Operand_id) -> option(bits(5)) =
    match operand_named(instruction, name) {
        Some(operand) => Some(operand.value[4 .. 0]),
        None() => None(),
    }

function vector_finish(instruction : Decoded_instruction, before : Cpu_state, after : Cpu_state) -> Execution_result = {
    var committed = after;
    committed.pc = next_pc(before, instruction);
    committed.vector_component_modified = true;
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

function vector_memory_predicate(instruction : Decoded_instruction, state : Cpu_state) -> list(bits(8)) =
    match predicate_register_index(instruction, Operand_govern) {
        Some(index) => state.predicate_registers[unsigned(index)],
        None() => zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8)),
    }

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
