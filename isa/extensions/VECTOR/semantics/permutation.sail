function vector_shift_image(
    operation : Semantic_operation,
    destination : list(bits(8)),
    counts : list(bits(8)),
    scalar_count : int,
    vector_counts : bool,
    predicate : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
) -> (
    list(bits(8))
) =
    if lane >= lanes then {
        destination
    } else {
        let count = if vector_counts then {
                vector_lane_unsigned(counts, lane, element_bytes)
            } else {
                scalar_count
            };
        let old = get_slice_int(64, vector_lane_unsigned(destination, lane, element_bytes), 0);
        let shift : Shift_kind = match vector_semantics(operation).shift {
            Some(shift) => shift,
            None() => ShiftLeft,
        };
        let shifted = shift_result(shift, old, get_slice_int(64, count, 0), element_bytes);
        vector_shift_image(
            operation,
            if predicate_bit(predicate, lane * element_bytes)
            then vector_write_lane(destination, lane, element_bytes, unsigned(shifted))
            else destination,
            counts,
            scalar_count,
            vector_counts,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function vector_integer_condition(condition : int, left : int, right : int, element_bytes : int) -> bool =
    if condition == 2 then {
        left == right
    } else {
        if condition == 3 then {
            left != right
        } else {
            if condition == 4 then {
                left < right
            } else {
                if condition == 5 then {
                    left >= right
                } else {
                    if condition == 10 then {
                        left <= right
                    } else {
                        if condition == 11 then {
                            left > right
                        } else {
                            if condition == 12 then {
                                vector_signed_lane(left, element_bytes) < vector_signed_lane(right, element_bytes)
                            } else {
                                if condition == 13 then {
                                    vector_signed_lane(left, element_bytes) >= vector_signed_lane(right, element_bytes)
                                } else {
                                    if condition == 14 then {
                                        vector_signed_lane(left, element_bytes) <=
                                            vector_signed_lane(right, element_bytes)
                                    } else {
                                        if condition == 15 then {
                                            vector_signed_lane(left, element_bytes) >
                                                vector_signed_lane(right, element_bytes)
                                        } else {
                                            assert(false);
                                            false
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

function vector_integer_compare_image(
    operation : Semantic_operation,
    condition : int,
    left : list(bits(8)),
    right : list(bits(8)),
    govern : list(bits(8)),
    image : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
) -> (
    list(bits(8))
) =
    if lane >= lanes then {
        image
    } else {
        let lhs = vector_lane_unsigned(left, lane, element_bytes);
        let rhs = vector_lane_unsigned(right, lane, element_bytes);
        let selected = if not_bool(predicate_bit(govern, lane * element_bytes)) then {
                false
            } else {
                let kind = vector_semantics(operation).integer_compare;
                if kind == Some(VectorCompareCondition) then {
                    vector_integer_condition(condition, lhs, rhs, element_bytes)
                } else {
                    if kind == Some(VectorTestZero) then {
                        unsigned(bits_from_int(lhs) & bits_from_int(rhs)) == 0
                    } else {
                        unsigned(bits_from_int(lhs) & bits_from_int(rhs)) != 0
                    }
                }
            };
        vector_integer_compare_image(
            operation,
            condition,
            left,
            right,
            govern,
            predicate_set_bit(image, lane * element_bytes, selected),
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function vector_width_change_destination_bytes(operation : Semantic_operation) -> int =
    vector_semantics(operation).width_change_destination_bytes

function vector_write_at_base(
    image : list(bits(8)),
    base : int,
    index : int,
    width : int,
    value : int,
    scale : int,
) -> (
    list(bits(8))
) =
    if index >= width then {
        image
    } else {
        vector_write_at_base(
            vector_replace_byte(image, base + index, get_slice_int(8, tmod_int(tdiv_int(value, scale), 256), 0)),
            base,
            index + 1,
            width,
            value,
            scale * 256,
        )
    }

function vector_width_change_image(
    operation : Semantic_operation,
    destination : list(bits(8)),
    source : list(bits(8)),
    predicate : list(bits(8)),
    container : int,
    containers : int,
    source_bytes : int,
    destination_bytes : int,
) -> (
    list(bits(8))
) =
    if container >= containers then {
        destination
    } else {
        let base = container * (if source_bytes > destination_bytes then source_bytes else destination_bytes);
        let source_value = vector_lane_unsigned_loop(source, base, source_bytes, 1, 0);
        let result = if vector_semantics(operation).width_change == Some(VectorExtendSigned) then {
                vector_normalized(vector_signed_lane(source_value, source_bytes), width_modulus(destination_bytes))
            } else {
                source_value
            };
        vector_width_change_image(
            operation,
            if predicate_bit(predicate, base)
            then vector_write_at_base(destination, base, 0, destination_bytes, result, 1)
            else destination,
            source,
            predicate,
            container + 1,
            containers,
            source_bytes,
            destination_bytes,
        )
    }

function vector_permute_value(
    operation : Semantic_operation,
    destination : list(bits(8)),
    source : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    count : int,
) -> (
    int
) = {
    let kind = vector_semantics(operation).permute;
    if kind == Some(VectorPermuteIndexed) then {
        let index = vector_lane_unsigned(source, lane, element_bytes);
        if index < lanes then {
            vector_lane_unsigned(destination, index, element_bytes)
        } else {
            0
        }
    } else {
        if kind == Some(VectorSlideUp) then {
            if lane >= count then {
                vector_lane_unsigned(destination, lane - count, element_bytes)
            } else {
                0
            }
        } else {
            if kind == Some(VectorSlideDown) then {
                if lane + count < lanes then {
                    vector_lane_unsigned(destination, lane + count, element_bytes)
                } else {
                    0
                }
            } else {
                if kind == Some(VectorSlice) then {
                    let index = lane + count;
                    if index < lanes then {
                        vector_lane_unsigned(destination, index, element_bytes)
                    } else {
                        if index < 2 * lanes then {
                            vector_lane_unsigned(source, index - lanes, element_bytes)
                        } else {
                            0
                        }
                    }
                } else {
                    if kind == Some(VectorZipLow) | kind == Some(VectorZipHigh) then {
                        let base = if kind == Some(VectorZipHigh) then {
                                tdiv_int(lanes, 2)
                            } else {
                                0
                            };
                        let index = base + tdiv_int(lane, 2);
                        if tmod_int(lane, 2) == 0 then {
                            vector_lane_unsigned(destination, index, element_bytes)
                        } else {
                            vector_lane_unsigned(source, index, element_bytes)
                        }
                    } else {
                        if kind == Some(VectorUnzipLow) | kind == Some(VectorUnzipHigh) then {
                            let parity = if kind == Some(VectorUnzipHigh) then { 1 } else { 0 };
                            if lane < tdiv_int(lanes, 2) then {
                                vector_lane_unsigned(destination, 2 * lane + parity, element_bytes)
                            } else {
                                vector_lane_unsigned(source, 2 * (lane - tdiv_int(lanes, 2)) + parity, element_bytes)
                            }
                        } else {
                            let parity = if kind == Some(VectorTransposeHigh) then { 1 } else { 0 };
                            let index = 2 * tdiv_int(lane, 2) + parity;
                            if tmod_int(lane, 2) == 0 then {
                                vector_lane_unsigned(destination, index, element_bytes)
                            } else {
                                vector_lane_unsigned(source, index, element_bytes)
                            }
                        }
                    }
                }
            }
        }
    }
}

function vector_permute_image(
    operation : Semantic_operation,
    original : list(bits(8)),
    source : list(bits(8)),
    image : list(bits(8)),
    predicate : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    count : int,
) -> (
    list(bits(8))
) =
    if lane >= lanes then {
        image
    } else {
        vector_permute_image(
            operation,
            original,
            source,
            if predicate_bit(predicate, lane * element_bytes)
            then vector_write_lane(
                image,
                lane,
                element_bytes,
                vector_permute_value(operation, original, source, lane, lanes, element_bytes, count),
            )
            else image,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
            count,
        )
    }
