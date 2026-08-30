struct Vector_fp_reduction = {
  value : bits(64),
  generated_causes : bits(5),
}

struct Vector_fp_image = {
  bytes : list(bits(8)),
  generated_causes : bits(5),
}

function vector_fp_reduction_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).fp_reduction_operation != None()

function vector_fp_reduction_scalar_operation(operation : Semantic_operation) -> Semantic_operation =
    match vector_semantics(operation).fp_reduction_operation {
        Some(scalar_operation) => scalar_operation,
        None() => operation,
    }

function vector_fp_value_kind(element_bytes : int) -> bits(8) =
    if element_bytes == 2 then { 0x06 } else { if element_bytes == 4 then { 0x01 } else { 0x02 } }

function vector_fp_result_kind(element_bytes : int) -> bits(8) =
    if element_bytes == 8 then { 0x02 } else { 0x01 }

function vector_fp_reduction_identity(operation : Semantic_operation, element_bytes : int) -> bits(64) = {
    let identity = vector_semantics(operation).fp_reduction_identity;
    if identity == VectorFpReductionZero then {
        0x0000000000000000
    } else {
        if identity == VectorFpReductionPositiveInfinity then {
            if element_bytes == 2 then {
                0x0000000000007C00
            } else {
                if element_bytes == 4 then { 0x000000007F800000 } else { 0x7FF0000000000000 }
            }
        } else {
            if element_bytes == 2 then {
                0x000000000000FC00
            } else {
                if element_bytes == 4 then { 0x00000000FF800000 } else { 0xFFF0000000000000 }
            }
        }
    }
}

function vector_fp_reduce_lanes(
    operation : Semantic_operation,
    source : list(bits(8)),
    predicate : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    control : bits(8),
    accumulator : bits(64),
    generated_causes : bits(5),
) -> (
    option(Vector_fp_reduction)
) =
    if lane >= lanes then {
        Some(struct { value = accumulator, generated_causes = generated_causes })
    } else {
        if not_bool(predicate_bit(predicate, lane * element_bytes)) then {
            vector_fp_reduce_lanes(
                operation,
                source,
                predicate,
                lane + 1,
                lanes,
                element_bytes,
                control,
                accumulator,
                generated_causes,
            )
        } else {
            match fp_primitive_evaluate(
                vector_fp_reduction_scalar_operation(operation),
                element_bytes,
                vector_fp_result_kind(element_bytes),
                control,
                2,
                vector_fp_value_kind(element_bytes),
                get_slice_int(64, vector_lane_unsigned(source, lane, element_bytes), 0),
                vector_fp_value_kind(element_bytes),
                accumulator,
                0x00,
                0x0000000000000000,
                false,
            ) {
                None() => None(),
                Some(evaluation) => vector_fp_reduce_lanes(
                    operation,
                    source,
                    predicate,
                    lane + 1,
                    lanes,
                    element_bytes,
                    control,
                    evaluation.primary,
                    generated_causes | evaluation.generated_causes,
                ),
            }
        }
    }

function vector_fp_reduction_commit(
    instruction : Decoded_instruction,
    before : Cpu_state,
    after : Cpu_state,
    source : list(bits(8)),
    values : list(Uop_value),
) -> (
    Uop_step
) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(before.vector_length_bytes, element_bytes);
    let predicate = vector_memory_predicate(instruction, before);
    let control = fp_primitive_control(
        fp_fstatus_rounding_mode(before.fstatus),
        fp_fstatus_ftz(before.fstatus),
        fp_fstatus_daz(before.fstatus),
        fp_fstatus_dn(before.fstatus),
    );
    match vector_fp_reduce_lanes(
        operation,
        source,
        predicate,
        0,
        lanes,
        element_bytes,
        control,
        vector_fp_reduction_identity(operation, element_bytes),
        fflags_none,
    ) {
        None() => uop_step_fault(faulted(before, operation, InvalidControlState, "vector FP reduction primitive failed")),
        Some(reduction) => if (reduction.generated_causes & vector_fp_allowed_causes(operation)) !=
            reduction.generated_causes then {
            uop_step_fault(faulted(before, operation, InvalidControlState, "vector FP reduction reported an impossible cause"))
        } else {
            if fp_traps(before.fstatus, reduction.generated_causes) then {
                uop_step_fault(fp_fault_with_causes(before, operation, reduction.generated_causes))
            } else {
                match operand_named(instruction, Operand_dst) {
                    None() => uop_step_fault(faulted(before, operation, InvalidControlState, "missing vector FP reduction destination")),
                    Some(destination) => {
                        var updated = after;
                        updated.floating_registers[unsigned(destination.value[3 .. 0])] = reduction.value;
                        updated.fflags = updated.fflags | reduction.generated_causes;
                        updated.fp_component_modified = true;
                        uop_step_continue(updated, values)
                    },
                }
            }
        },
    }
}

function vector_fp_scalar_operation(operation : Semantic_operation) -> Semantic_operation =
    match vector_semantics(operation).fp_scalar_operation {
        Some(scalar_operation) => scalar_operation,
        None() => operation,
    }

function vector_fp_primitive_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).fp_primitive

function vector_fp_exact_operation(operation : Semantic_operation) -> bool =
    vector_semantics(operation).fp_exact != None()
