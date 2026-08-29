function vector_fp_lane_exact(
    operation : Semantic_operation,
    element_bytes : int,
    source : bits(64),
    destination : bits(64),
    source_present : bool,
) -> (
    option(bits(64))
) = {
    let kind = vector_semantics(operation).fp_exact;
    if kind == Some(VectorFpNegate) then {
        fp_exact_arithmetic(FpArithmeticNegate, if source_present then source else destination, element_bytes)
    } else {
        if kind == Some(VectorFpAbsolute) then {
            fp_exact_arithmetic(FpArithmeticAbsolute, if source_present then source else destination, element_bytes)
        } else {
            if kind == Some(VectorFpCopySign) then {
                fp_exact_data(FpDataCopySign, source, destination, element_bytes)
            } else {
                fp_exact_data(
                    FpDataClassify,
                    if source_present then source else destination,
                    0x0000000000000000,
                    element_bytes,
                )
            }
        }
    }
}

function vector_fp_arithmetic_lanes(
    operation : Semantic_operation,
    source : list(bits(8)),
    lhs : list(bits(8)),
    rhs : list(bits(8)),
    destination : list(bits(8)),
    predicate : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    control : bits(8),
    result : list(bits(8)),
    generated_causes : bits(5),
    source_present : bool,
) -> (
    option(Vector_fp_image)
) =
    if lane >= lanes then {
        Some(struct { bytes = result, generated_causes = generated_causes })
    } else {
        if not_bool(predicate_bit(predicate, lane * element_bytes)) then {
            vector_fp_arithmetic_lanes(
                operation,
                source,
                lhs,
                rhs,
                destination,
                predicate,
                lane + 1,
                lanes,
                element_bytes,
                control,
                result,
                generated_causes,
                source_present,
            )
        } else {
            let source_value = get_slice_int(64, vector_lane_unsigned(source, lane, element_bytes), 0);
            let lhs_value = get_slice_int(64, vector_lane_unsigned(lhs, lane, element_bytes), 0);
            let rhs_value = get_slice_int(64, vector_lane_unsigned(rhs, lane, element_bytes), 0);
            let destination_value = get_slice_int(64, vector_lane_unsigned(destination, lane, element_bytes), 0);
            if vector_fp_exact_operation(operation) then {
                match vector_fp_lane_exact(operation, element_bytes, source_value, destination_value, source_present) {
                    None() => None(),
                    Some(value) => vector_fp_arithmetic_lanes(
                        operation,
                        source,
                        lhs,
                        rhs,
                        destination,
                        predicate,
                        lane + 1,
                        lanes,
                        element_bytes,
                        control,
                        vector_write_lane(result, lane, element_bytes, unsigned(value)),
                        generated_causes,
                        source_present,
                    ),
                }
            } else {
                let arity = vector_semantics(operation).fp_arity;
                let fused = arity == 3;
                let unary = arity == 1;
                match fp_primitive_evaluate(
                    vector_fp_scalar_operation(operation),
                    element_bytes,
                    vector_fp_result_kind(element_bytes),
                    control,
                    if fused then 3 else if unary then 1 else 2,
                    vector_fp_value_kind(element_bytes),
                    if fused
                    then lhs_value
                    else if unary & source_present
                         then source_value
                         else if unary then destination_value else source_value,
                    vector_fp_value_kind(element_bytes),
                    if fused then rhs_value else destination_value,
                    vector_fp_value_kind(element_bytes),
                    destination_value,
                    false,
                ) {
                    None() => None(),
                    Some(evaluation) => vector_fp_arithmetic_lanes(
                        operation,
                        source,
                        lhs,
                        rhs,
                        destination,
                        predicate,
                        lane + 1,
                        lanes,
                        element_bytes,
                        control,
                        vector_write_lane(result, lane, element_bytes, unsigned(evaluation.primary)),
                        generated_causes | evaluation.generated_causes,
                        source_present,
                    ),
                }
            }
        }
    }

function vector_fp_condition_selected(flags : bits(4), condition : int) -> bool = {
    let unordered = flags[0] == bitone;
    let less = flags[1] == bitone;
    let equal = flags[3] == bitone;
    let greater = not_bool(unordered | less | equal);
    if condition == 2 then {
        equal
    } else {
        if condition == 3 then {
            not_bool(equal)
        } else {
            if condition == 8 then {
                unordered
            } else {
                if condition == 9 then {
                    not_bool(unordered)
                } else {
                    if condition == 12 then {
                        less
                    } else {
                        if condition == 13 then {
                            greater | equal
                        } else {
                            if condition == 14 then {
                                less | equal
                            } else {
                                if condition == 15 then { greater } else { false }
                            }
                        }
                    }
                }
            }
        }
    }
}

function vector_fp_compare_lanes(
    left : list(bits(8)),
    right : list(bits(8)),
    predicate : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    control : bits(8),
    condition : int,
    result : list(bits(8)),
    generated_causes : bits(5),
) -> (
    option(Vector_fp_image)
) =
    if lane >= lanes then {
        Some(struct { bytes = result, generated_causes = generated_causes })
    } else {
        if not_bool(predicate_bit(predicate, lane * element_bytes)) then {
            vector_fp_compare_lanes(
                left,
                right,
                predicate,
                lane + 1,
                lanes,
                element_bytes,
                control,
                condition,
                result,
                generated_causes,
            )
        } else {
            match fp_primitive_evaluate(
                fp_compare_semantic_operation(FpCompareOrdered),
                element_bytes,
                0x05,
                control,
                2,
                vector_fp_value_kind(element_bytes),
                get_slice_int(64, vector_lane_unsigned(right, lane, element_bytes), 0),
                vector_fp_value_kind(element_bytes),
                get_slice_int(64, vector_lane_unsigned(left, lane, element_bytes), 0),
                0x00,
                0x0000000000000000,
                false,
            ) {
                None() => None(),
                Some(evaluation) => vector_fp_compare_lanes(
                    left,
                    right,
                    predicate,
                    lane + 1,
                    lanes,
                    element_bytes,
                    control,
                    condition,
                    predicate_set_bit(
                        result,
                        lane * element_bytes,
                        vector_fp_condition_selected(evaluation.flags_value, condition),
                    ),
                    generated_causes | evaluation.generated_causes,
                ),
            }
        }
    }
