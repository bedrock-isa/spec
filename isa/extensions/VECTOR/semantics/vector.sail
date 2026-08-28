function vector_byte_at(bytes : list(bits(8)), index : int) -> bits(8) = match bytes {
    [||] => 0x00,
    head :: tail => if index <= 0 then {
        head
    } else {
        vector_byte_at(tail, index - 1)
    },
}

function vector_replace_byte(bytes : list(bits(8)), index : int, value : bits(8)) -> list(bits(8)) =
    match bytes {
        [||] => [||],
        head :: tail => if index <= 0 then {
            value :: tail
        } else {
            head :: vector_replace_byte(tail, index - 1, value)
        },
    }

function vector_power_of_two(exponent : int) -> int =
    if exponent <= 0 then {
        1
    } else {
        2 * vector_power_of_two(exponent - 1)
    }

function predicate_bit(image : list(bits(8)), index : int) -> bool = {
    let byte = vector_byte_at(image, tdiv_int(index, 8));
    tmod_int(tdiv_int(unsigned(byte), vector_power_of_two(tmod_int(index, 8))), 2) == 1
}

function predicate_set_bit(image : list(bits(8)), index : int, selected : bool) -> list(bits(8)) = {
    let byte_index = tdiv_int(index, 8);
    let byte = unsigned(vector_byte_at(image, byte_index));
    let mask = vector_power_of_two(tmod_int(index, 8));
    let present = tmod_int(tdiv_int(byte, mask), 2) == 1;
    let updated = if selected then {
            if present then {
                byte
            } else {
                byte + mask
            }
        } else {
            if present then {
                byte - mask
            } else {
                byte
            }
        };
    vector_replace_byte(image, byte_index, get_slice_int(8, updated, 0))
}

function predicate_fill_typed(
    image : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    first : int,
    last : int,
) -> (
    list(bits(8))
) =
    if lane >= lanes then {
        image
    } else {
        predicate_fill_typed(
            predicate_set_bit(image, lane * element_bytes, lane >= first & lane < last),
            lane + 1,
            lanes,
            element_bytes,
            first,
            last,
        )
    }

function predicate_raw_binary(
    left : list(bits(8)),
    right : list(bits(8)),
    operation : Semantic_operation,
) -> (
    list(bits(8))
) =
    match (left, right) {
        (left_head :: left_tail, right_head :: right_tail) => (if operation == Op_PAND
                                                              then left_head & right_head
                                                              else if operation == Op_POR
                                                                   then left_head | right_head
                                                                   else xor_vec(left_head, right_head)) ::
            predicate_raw_binary(left_tail, right_tail, operation),
        _ => [||],
    }

function predicate_raw_not(image : list(bits(8))) -> list(bits(8)) = match image {
    [||] => [||],
    head :: tail => xor_vec(head, 0xFF) :: predicate_raw_not(tail),
}

function predicate_raw_select(
    select : list(bits(8)),
    source : list(bits(8)),
    destination : list(bits(8)),
) -> (
    list(bits(8))
) =
    match (select, source, destination) {
        (select_head :: select_tail, source_head :: source_tail, destination_head :: destination_tail) => ((destination_head &
            xor_vec(select_head, 0xFF)) |
            (source_head & select_head)) ::
            predicate_raw_select(select_tail, source_tail, destination_tail),
        _ => [||],
    }

function vector_lane_unsigned_loop(
    bytes : list(bits(8)),
    base : int,
    remaining : int,
    scale : int,
    accumulated : int,
) -> (
    int
) =
    if remaining <= 0 then {
        accumulated
    } else {
        vector_lane_unsigned_loop(
            bytes,
            base + 1,
            remaining - 1,
            scale * 256,
            accumulated + unsigned(vector_byte_at(bytes, base)) * scale,
        )
    }

function vector_lane_unsigned(bytes : list(bits(8)), lane : int, element_bytes : int) -> int =
    vector_lane_unsigned_loop(bytes, lane * element_bytes, element_bytes, 1, 0)

function vector_write_lane_loop(
    image : list(bits(8)),
    base : int,
    index : int,
    element_bytes : int,
    value : int,
    scale : int,
) -> (
    list(bits(8))
) =
    if index >= element_bytes then {
        image
    } else {
        vector_write_lane_loop(
            vector_replace_byte(image, base + index, get_slice_int(8, tmod_int(tdiv_int(value, scale), 256), 0)),
            base,
            index + 1,
            element_bytes,
            value,
            scale * 256,
        )
    }

function vector_write_lane(image : list(bits(8)), lane : int, element_bytes : int, value : int) -> list(bits(8)) =
    vector_write_lane_loop(image, lane * element_bytes, 0, element_bytes, value, 1)

function vector_merge_image(
    destination : list(bits(8)),
    source : list(bits(8)),
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
        vector_merge_image(
            if predicate_bit(predicate, lane * element_bytes)
            then vector_write_lane(destination, lane, element_bytes, vector_lane_unsigned(source, lane, element_bytes))
            else destination,
            source,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function vector_duplicate_image(
    image : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    value : int,
) -> (
    list(bits(8))
) =
    if lane >= lanes then {
        image
    } else {
        vector_duplicate_image(
            vector_write_lane(image, lane, element_bytes, value),
            lane + 1,
            lanes,
            element_bytes,
            value,
        )
    }

function vector_index_image(image : list(bits(8)), lane : int, lanes : int, element_bytes : int) -> list(bits(8)) =
    if lane >= lanes then {
        image
    } else {
        vector_index_image(vector_write_lane(image, lane, element_bytes, lane), lane + 1, lanes, element_bytes)
    }

function vector_normalized(value : int, modulus : int) -> int =
    tmod_int(tmod_int(value, modulus) + modulus, modulus)

function vector_signed_lane(value : int, element_bytes : int) -> int = {
    let modulus = width_modulus(element_bytes);
    let sign = tdiv_int(modulus, 2);
    if value >= sign then {
        value - modulus
    } else {
        value
    }
}

function vector_integer_binary_value(
    operation : Semantic_operation,
    destination : int,
    source : int,
    element_bytes : int,
) -> (
    int
) = {
    let modulus = width_modulus(element_bytes);
    let bits = element_bytes * 8;
    let signed_destination = vector_signed_lane(destination, element_bytes);
    let signed_source = vector_signed_lane(source, element_bytes);
    if operation == Op_VADD then {
        vector_normalized(destination + source, modulus)
    } else {
        if operation == Op_VSUB then {
            vector_normalized(destination - source, modulus)
        } else {
            if operation == Op_VAND then {
                unsigned(bits_from_int(destination) & bits_from_int(source))
            } else {
                if operation == Op_VOR then {
                    unsigned(bits_from_int(destination) | bits_from_int(source))
                } else {
                    if operation == Op_VXOR then {
                        unsigned(xor_vec(bits_from_int(destination), bits_from_int(source)))
                    } else {
                        if operation == Op_VMINS then {
                            vector_normalized(
                                if signed_destination < signed_source then signed_destination else signed_source,
                                modulus,
                            )
                        } else {
                            if operation == Op_VMINU then {
                                if destination < source then { destination } else { source }
                            } else {
                                if operation == Op_VMAXS then {
                                    vector_normalized(
                                        if signed_destination > signed_source then signed_destination else signed_source,
                                        modulus,
                                    )
                                } else {
                                    if operation == Op_VMAXU then {
                                        if destination > source then { destination } else { source }
                                    } else {
                                        if operation == Op_VMUL then {
                                            tmod_int(destination * source, modulus)
                                        } else {
                                            if operation == Op_VMULHU then {
                                                tdiv_int(destination * source, modulus)
                                            } else {
                                                if operation == Op_VMULHS then {
                                                    tdiv_int(
                                                        vector_normalized(
                                                            signed_destination * signed_source,
                                                            modulus * modulus,
                                                        ),
                                                        modulus,
                                                    )
                                                } else {
                                                    if operation == Op_VMULHSU then {
                                                        tdiv_int(
                                                            vector_normalized(
                                                                signed_destination * source,
                                                                modulus * modulus,
                                                            ),
                                                            modulus,
                                                        )
                                                    } else {
                                                        0
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
            }
        }
    }
}

function vector_integer_binary_image(
    operation : Semantic_operation,
    destination : list(bits(8)),
    source : list(bits(8)),
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
        vector_integer_binary_image(
            operation,
            if predicate_bit(predicate, lane * element_bytes)
            then vector_write_lane(
                destination,
                lane,
                element_bytes,
                vector_integer_binary_value(
                    operation,
                    vector_lane_unsigned(destination, lane, element_bytes),
                    vector_lane_unsigned(source, lane, element_bytes),
                    element_bytes,
                ),
            )
            else destination,
            source,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function vector_integer_reduction_operation(operation : Semantic_operation) -> bool =
       operation
    == Op_VREDADD
    |  operation
    == Op_VREDMINS
    |  operation
    == Op_VREDMINU
    |  operation
    == Op_VREDMAXS
    |  operation
    == Op_VREDMAXU
    |  operation
    == Op_VREDAND
    |  operation
    == Op_VREDOR
    |  operation
    == Op_VREDXOR

function vector_integer_reduction_identity(operation : Semantic_operation, element_bytes : int) -> int = {
    let modulus : int = width_modulus(element_bytes);
    let sign : int = tdiv_int(modulus, 2);
    if operation == Op_VREDAND | operation == Op_VREDMINU then {
        modulus - 1
    } else {
        if operation == Op_VREDMINS then {
            sign - 1
        } else {
            if operation == Op_VREDMAXS then { sign } else { 0 }
        }
    }
}

function vector_integer_reduction_value(
    operation : Semantic_operation,
    accumulator : int,
    value : int,
    element_bytes : int,
) -> (
    int
) = {
    let modulus : int = width_modulus(element_bytes);
    if operation == Op_VREDADD then {
        tmod_int(accumulator + value, modulus)
    } else {
        if operation == Op_VREDAND then {
            unsigned(bits_from_int(accumulator) & bits_from_int(value))
        } else {
            if operation == Op_VREDOR then {
                unsigned(bits_from_int(accumulator) | bits_from_int(value))
            } else {
                if operation == Op_VREDXOR then {
                    unsigned(xor_vec(bits_from_int(accumulator), bits_from_int(value)))
                } else {
                    if operation == Op_VREDMINS then {
                        vector_normalized(
                            if vector_signed_lane(accumulator, element_bytes) < vector_signed_lane(value, element_bytes)
                            then vector_signed_lane(accumulator, element_bytes)
                            else vector_signed_lane(value, element_bytes),
                            modulus,
                        )
                    } else {
                        if operation == Op_VREDMINU then {
                            if accumulator < value then { accumulator } else { value }
                        } else {
                            if operation == Op_VREDMAXS then {
                                vector_normalized(
                                    if vector_signed_lane(accumulator, element_bytes) >
                                        vector_signed_lane(value, element_bytes)
                                    then vector_signed_lane(accumulator, element_bytes)
                                    else vector_signed_lane(value, element_bytes),
                                    modulus,
                                )
                            } else {
                                if operation == Op_VREDMAXU then {
                                    if accumulator > value then { accumulator } else { value }
                                } else {
                                    0
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

function vector_integer_reduction_image(
    operation : Semantic_operation,
    source : list(bits(8)),
    predicate : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    accumulator : int,
) -> (
    int
) =
    if lane >= lanes then {
        accumulator
    } else {
        vector_integer_reduction_image(
            operation,
            source,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
            if predicate_bit(predicate, lane * element_bytes)
            then vector_integer_reduction_value(
                operation,
                accumulator,
                vector_lane_unsigned(source, lane, element_bytes),
                element_bytes,
            )
            else accumulator,
        )
    }

function vector_integer_unary_value(operation : Semantic_operation, value : int, element_bytes : int) -> int = {
    let modulus = width_modulus(element_bytes);
    let bits = element_bytes * 8;
    let image = bits_from_int(value) & width_mask(element_bytes);
    if operation == Op_VNEG then {
        vector_normalized(-value, modulus)
    } else {
        if operation == Op_VABS then {
            let signed_value = vector_signed_lane(value, element_bytes);
            vector_normalized(if signed_value < 0 then -signed_value else signed_value, modulus)
        } else {
            if operation == Op_VNOT then {
                unsigned(xor_vec(image, width_mask(element_bytes)))
            } else {
                if operation == Op_VCLZ then {
                    count_from_high(image, bits, bitzero)
                } else {
                    if operation == Op_VCTZ then {
                        count_from_low(image, 0, bits, bitzero)
                    } else {
                        if operation == Op_VCLS then {
                            count_from_high(image, bits, bitone)
                        } else {
                            if operation == Op_VCTS then {
                                count_from_low(image, 0, bits, bitone)
                            } else {
                                if operation == Op_VPOPCNT then {
                                    bit_count_from(image, 0, bits)
                                } else {
                                    if operation == Op_VREVBYTE then {
                                        unsigned(reverse_bytes(image, element_bytes))
                                    } else {
                                        0
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

function vector_integer_unary_image(
    operation : Semantic_operation,
    destination : list(bits(8)),
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
        vector_integer_unary_image(
            operation,
            if predicate_bit(predicate, lane * element_bytes)
            then vector_write_lane(
                destination,
                lane,
                element_bytes,
                vector_integer_unary_value(
                    operation,
                    vector_lane_unsigned(destination, lane, element_bytes),
                    element_bytes,
                ),
            )
            else destination,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function vector_integer_unary_source_image(
    operation : Semantic_operation,
    destination : list(bits(8)),
    source : list(bits(8)),
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
        vector_integer_unary_source_image(
            operation,
            if predicate_bit(predicate, lane * element_bytes)
            then vector_write_lane(
                destination,
                lane,
                element_bytes,
                vector_integer_unary_value(operation, vector_lane_unsigned(source, lane, element_bytes), element_bytes),
            )
            else destination,
            source,
            predicate,
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function vector_shift_operation(operation : Semantic_operation) -> Semantic_operation =
    if operation == Op_VSHL then {
        Op_SHL
    } else {
        if operation == Op_VSHR then {
            Op_SHR
        } else {
            if operation == Op_VSAR then { Op_SAR } else { if operation == Op_VROL then { Op_ROL } else { Op_ROR } }
        }
    }

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
        let shifted = shift_result(vector_shift_operation(operation), old, get_slice_int(64, count, 0), element_bytes);
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
                if operation == Op_VCMPcc then {
                    vector_integer_condition(condition, lhs, rhs, element_bytes)
                } else {
                    if operation == Op_VTESTZ then {
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
    if operation == Op_VEXTZW | operation == Op_VEXTSW | operation == Op_VTRUNCW then {
        2
    } else {
        if operation == Op_VEXTZL | operation == Op_VEXTSL | operation == Op_VTRUNCL then {
            4
        } else {
            if operation == Op_VEXTZQ | operation == Op_VEXTSQ then { 8 } else { 1 }
        }
    }

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
        let result = if operation == Op_VEXTSW | operation == Op_VEXTSL | operation == Op_VEXTSQ then {
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
) =
    if operation == Op_VPERM then {
        let index = vector_lane_unsigned(source, lane, element_bytes);
        if index < lanes then {
            vector_lane_unsigned(destination, index, element_bytes)
        } else {
            0
        }
    } else {
        if operation == Op_VSLIDEUP then {
            if lane >= count then {
                vector_lane_unsigned(destination, lane - count, element_bytes)
            } else {
                0
            }
        } else {
            if operation == Op_VSLIDEDN then {
                if lane + count < lanes then {
                    vector_lane_unsigned(destination, lane + count, element_bytes)
                } else {
                    0
                }
            } else {
                if operation == Op_VSLICE then {
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
                    if operation == Op_VZIPLO | operation == Op_VZIPHI then {
                        let base = if operation == Op_VZIPHI then {
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
                        if operation == Op_VUZIPLO | operation == Op_VUZIPHI then {
                            let parity = if operation == Op_VUZIPHI then { 1 } else { 0 };
                            if lane < tdiv_int(lanes, 2) then {
                                vector_lane_unsigned(destination, 2 * lane + parity, element_bytes)
                            } else {
                                vector_lane_unsigned(source, 2 * (lane - tdiv_int(lanes, 2)) + parity, element_bytes)
                            }
                        } else {
                            let parity = if operation == Op_VTRNHI then { 1 } else { 0 };
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

function predicate_pair_lane(
    operation : Semantic_operation,
    left : list(bits(8)),
    right : list(bits(8)),
    output_lane : int,
    lanes : int,
    element_bytes : int,
) -> (
    bool
) =
    if operation == Op_PZIPLO | operation == Op_PZIPHI then {
        let base = if operation == Op_PZIPHI then {
                tdiv_int(lanes, 2)
            } else {
                0
            };
        let source_lane = base + tdiv_int(output_lane, 2);
        if tmod_int(output_lane, 2) == 0 then {
            predicate_bit(left, source_lane * element_bytes)
        } else {
            predicate_bit(right, source_lane * element_bytes)
        }
    } else {
        if operation == Op_PUZIPLO | operation == Op_PUZIPHI then {
            let parity = if operation == Op_PUZIPHI then { 1 } else { 0 };
            if output_lane < tdiv_int(lanes, 2) then {
                predicate_bit(left, (2 * output_lane + parity) * element_bytes)
            } else {
                predicate_bit(right, (2 * (output_lane - tdiv_int(lanes, 2)) + parity) * element_bytes)
            }
        } else {
            let parity = if operation == Op_PTRNHI then { 1 } else { 0 };
            let source_lane = 2 * tdiv_int(output_lane, 2) + parity;
            if tmod_int(output_lane, 2) == 0 then {
                predicate_bit(left, source_lane * element_bytes)
            } else {
                predicate_bit(right, source_lane * element_bytes)
            }
        }
    }

function predicate_pair_image(
    operation : Semantic_operation,
    left : list(bits(8)),
    right : list(bits(8)),
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
        predicate_pair_image(
            operation,
            left,
            right,
            predicate_set_bit(
                image,
                lane * element_bytes,
                predicate_pair_lane(operation, left, right, lane, lanes, element_bytes),
            ),
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function predicate_unpack_image(
    source : list(bits(8)),
    image : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    high : bool,
) -> (
    list(bits(8))
) =
    if lane >= tdiv_int(lanes, 2) then {
        image
    } else {
        let source_lane = lane + (if high then tdiv_int(lanes, 2) else 0);
        predicate_unpack_image(
            source,
            predicate_set_bit(image, lane * element_bytes * 2, predicate_bit(source, source_lane * element_bytes)),
            lane + 1,
            lanes,
            element_bytes,
            high,
        )
    }

function predicate_pack_image(
    source : list(bits(8)),
    image : list(bits(8)),
    lane : int,
    lanes : int,
    element_bytes : int,
    high : bool,
) -> (
    list(bits(8))
) =
    if lane >= lanes then {
        image
    } else {
        let destination_bytes = tdiv_int(element_bytes, 2);
        let destination_lane = lane + (if high then lanes else 0);
        predicate_pack_image(
            source,
            predicate_set_bit(image, destination_lane * destination_bytes, predicate_bit(source, lane * element_bytes)),
            lane + 1,
            lanes,
            element_bytes,
            high,
        )
    }

function predicate_permute_image(
    source : list(bits(8)),
    indices : list(bits(8)),
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
        let index = vector_lane_unsigned(indices, lane, element_bytes);
        predicate_permute_image(
            source,
            indices,
            predicate_set_bit(
                image,
                lane * element_bytes,
                if index < lanes then predicate_bit(source, index * element_bytes) else false,
            ),
            lane + 1,
            lanes,
            element_bytes,
        )
    }

function predicate_slide_image(
    operation : Semantic_operation,
    destination : list(bits(8)),
    source : list(bits(8)),
    image : list(bits(8)),
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
        let selected = if operation == Op_PSLIDEUP then {
                if lane >= count then {
                    predicate_bit(destination, (lane - count) * element_bytes)
                } else {
                    false
                }
            } else {
                if operation == Op_PSLIDEDN then {
                    if lane + count < lanes then {
                        predicate_bit(destination, (lane + count) * element_bytes)
                    } else {
                        false
                    }
                } else {
                    let index = lane + count;
                    if index < lanes then {
                        predicate_bit(destination, index * element_bytes)
                    } else {
                        if index < 2 * lanes then {
                            predicate_bit(source, (index - lanes) * element_bytes)
                        } else {
                            false
                        }
                    }
                }
            };
        predicate_slide_image(
            operation,
            destination,
            source,
            predicate_set_bit(image, lane * element_bytes, selected),
            lane + 1,
            lanes,
            element_bytes,
            count,
        )
    }

function predicate_count(image : list(bits(8)), lane : int, lanes : int, element_bytes : int, count : int) -> int =
    if lane >= lanes then {
        count
    } else {
        predicate_count(
            image,
            lane + 1,
            lanes,
            element_bytes,
            count + (if predicate_bit(image, lane * element_bytes) then 1 else 0),
        )
    }

function predicate_first(image : list(bits(8)), lane : int, lanes : int, element_bytes : int) -> int =
    if lane >= lanes then {
        -1
    } else {
        if predicate_bit(image, lane * element_bytes) then {
            lane
        } else {
            predicate_first(image, lane + 1, lanes, element_bytes)
        }
    }

function predicate_last(image : list(bits(8)), lane : int, element_bytes : int) -> int =
    if lane < 0 then {
        -1
    } else {
        if predicate_bit(image, lane * element_bytes) then {
            lane
        } else {
            predicate_last(image, lane - 1, element_bytes)
        }
    }

function predicate_any(image : list(bits(8))) -> bool = match image {
    [||] => false,
    head :: tail => head != 0x00 | predicate_any(tail),
}

function predicate_all_typed(image : list(bits(8)), lane : int, lanes : int, element_bytes : int) -> bool =
    if lane >= lanes then {
        true
    } else {
        predicate_bit(image, lane * element_bytes) & predicate_all_typed(image, lane + 1, lanes, element_bytes)
    }

function predicate_register_index(instruction : Decoded_instruction, name : Operand_id) -> option(bits(4)) =
    match operand_named(instruction, name) {
        Some(operand) => Some(operand.value[3 .. 0]),
        None() => None(),
    }

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
       operation
    == Op_VADD
    |  operation
    == Op_VSUB
    |  operation
    == Op_VMUL
    |  operation
    == Op_VNEG
    |  operation
    == Op_VABS
    |  operation
    == Op_VMIN
    |  operation
    == Op_VMAX
    |  operation
    == Op_VDIV
    |  operation
    == Op_VMADD
    |  operation
    == Op_VMSUB
    |  operation
    == Op_VNMADD
    |  operation
    == Op_VNMSUB
    |  operation
    == Op_VSQRT
    |  operation
    == Op_VCOPYSIGN
    |  operation
    == Op_VROUND
    |  operation
    == Op_VTRUNC
    |  operation
    == Op_VFLOOR
    |  operation
    == Op_VCEIL
    |  operation
    == Op_VCLASS
    |  operation
    == Op_VCMPcc

function vector_fp_convert_operation(operation : Semantic_operation) -> bool =
       operation
    == Op_VCVTH
    |  operation
    == Op_VCVTUH
    |  operation
    == Op_VCVTS
    |  operation
    == Op_VCVTUS
    |  operation
    == Op_VCVTD
    |  operation
    == Op_VCVTUD
    |  operation
    == Op_VCVTL
    |  operation
    == Op_VCVTUL
    |  operation
    == Op_VCVTQ
    |  operation
    == Op_VCVTUQ

function vector_reduce_operation(operation : Semantic_operation) -> bool =
       operation
    == Op_VREDADD
    |  operation
    == Op_VREDMINS
    |  operation
    == Op_VREDMINU
    |  operation
    == Op_VREDMAXS
    |  operation
    == Op_VREDMAXU
    |  operation
    == Op_VREDAND
    |  operation
    == Op_VREDOR
    |  operation
    == Op_VREDXOR
    |  operation
    == Op_VREDMIN
    |  operation
    == Op_VREDMAX

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
    if    operation
       == Op_VNEG
       |  operation
       == Op_VABS
       |  operation
       == Op_VCOPYSIGN
       |  operation
       == Op_VCLASS
       |  operation
       == Op_VDUP
       |  operation
       == Op_VEXTRACT
       |  operation
       == Op_VINSERT
       |  operation
       == Op_VREDAND
       |  operation
       == Op_VREDOR
       |  operation
       == Op_VREDXOR
       |  operation
       == Op_VREDMINS
       |  operation
       == Op_VREDMINU
       |  operation
       == Op_VREDMAXS
       |  operation
       == Op_VREDMAXU then {
        fflags_none
    } else {
        if    operation
           == Op_VMIN
           |  operation
           == Op_VMAX
           |  operation
           == Op_VCMPcc
           |  operation
           == Op_VREDMIN
           |  operation
           == Op_VREDMAX then {
            fflags_nv
        } else {
            if    operation
               == Op_VROUND
               |  operation
               == Op_VTRUNC
               |  operation
               == Op_VFLOOR
               |  operation
               == Op_VCEIL
               |  operation
               == Op_VSQRT then {
                fflags_nv | fflags_nx
            } else {
                if operation == Op_VDIV then { fflags_all } else { 0b10111 }
            }
        }
    }

struct Vector_fp_reduction = {
  value : bits(64),
  generated_causes : bits(5),
}

struct Vector_fp_image = {
  bytes : list(bits(8)),
  generated_causes : bits(5),
}

function vector_fp_reduction_operation(operation : Semantic_operation) -> bool =
    operation == Op_VREDADD | operation == Op_VREDMIN | operation == Op_VREDMAX

function vector_fp_reduction_scalar_operation(operation : Semantic_operation) -> Semantic_operation =
    if operation == Op_VREDADD then {
        fp_arithmetic_semantic_operation(FpArithmeticAdd)
    } else {
        if operation == Op_VREDMIN then {
            fp_compare_semantic_operation(FpCompareMinimum)
        } else {
            fp_compare_semantic_operation(FpCompareMaximum)
        }
    }

function vector_fp_value_kind(element_bytes : int) -> bits(8) =
    if element_bytes == 2 then { 0x06 } else { if element_bytes == 4 then { 0x01 } else { 0x02 } }

function vector_fp_result_kind(element_bytes : int) -> bits(8) =
    if element_bytes == 8 then { 0x02 } else { 0x01 }

function vector_fp_reduction_identity(operation : Semantic_operation, element_bytes : int) -> bits(64) =
    if operation == Op_VREDADD then {
        0x0000000000000000
    } else {
        if operation == Op_VREDMIN then {
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
) -> (
    Execution_result
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
        None() => faulted(before, operation, InvalidControlState, "vector FP reduction primitive failed"),
        Some(reduction) => if (reduction.generated_causes & vector_fp_allowed_causes(operation)) !=
            reduction.generated_causes then {
            faulted(before, operation, InvalidControlState, "vector FP reduction reported an impossible cause")
        } else {
            if fp_traps(before.fstatus, reduction.generated_causes) then {
                fp_fault_with_causes(before, operation, reduction.generated_causes)
            } else {
                match operand_named(instruction, Operand_dst) {
                    None() => faulted(before, operation, InvalidControlState, "missing vector FP reduction destination"),
                    Some(destination) => {
                        var updated = after;
                        updated.floating_registers[unsigned(destination.value[3 .. 0])] = reduction.value;
                        updated.fflags = updated.fflags | reduction.generated_causes;
                        updated.fp_component_modified = true;
                        completed(before, updated, CommitRegisters, [||])
                    },
                }
            }
        },
    }
}

function vector_fp_scalar_operation(operation : Semantic_operation) -> Semantic_operation =
    if operation == Op_VADD then {
        fp_arithmetic_semantic_operation(FpArithmeticAdd)
    } else {
        if operation == Op_VSUB then {
            fp_arithmetic_semantic_operation(FpArithmeticSubtract)
        } else {
            if operation == Op_VMUL then {
                fp_arithmetic_semantic_operation(FpArithmeticMultiply)
            } else {
                if operation == Op_VDIV then {
                    fp_arithmetic_semantic_operation(FpArithmeticDivide)
                } else {
                    if operation == Op_VMIN then {
                        fp_compare_semantic_operation(FpCompareMinimum)
                    } else {
                        if operation == Op_VMAX then {
                            fp_compare_semantic_operation(FpCompareMaximum)
                        } else {
                            if operation == Op_VMADD then {
                                fp_arithmetic_semantic_operation(FpArithmeticFusedMultiplyAdd)
                            } else {
                                if operation == Op_VMSUB then {
                                    fp_arithmetic_semantic_operation(FpArithmeticFusedMultiplySubtract)
                                } else {
                                    if operation == Op_VNMADD then {
                                        fp_arithmetic_semantic_operation(FpArithmeticFusedNegatedMultiplyAdd)
                                    } else {
                                        if operation == Op_VNMSUB then {
                                            fp_arithmetic_semantic_operation(FpArithmeticFusedNegatedMultiplySubtract)
                                        } else {
                                            if operation == Op_VSQRT then {
                                                fp_arithmetic_semantic_operation(FpArithmeticSquareRoot)
                                            } else {
                                                if operation == Op_VROUND then {
                                                    fp_conversion_semantic_operation(FpConvertRound)
                                                } else {
                                                    if operation == Op_VTRUNC then {
                                                        fp_conversion_semantic_operation(FpConvertTruncate)
                                                    } else {
                                                        if operation == Op_VFLOOR then {
                                                            fp_conversion_semantic_operation(FpConvertFloor)
                                                        } else {
                                                            fp_conversion_semantic_operation(FpConvertCeiling)
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
                }
            }
        }
    }

function vector_fp_primitive_operation(operation : Semantic_operation) -> bool =
       operation
    == Op_VADD
    |  operation
    == Op_VSUB
    |  operation
    == Op_VMUL
    |  operation
    == Op_VDIV
    |  operation
    == Op_VMIN
    |  operation
    == Op_VMAX
    |  operation
    == Op_VMADD
    |  operation
    == Op_VMSUB
    |  operation
    == Op_VNMADD
    |  operation
    == Op_VNMSUB
    |  operation
    == Op_VSQRT
    |  operation
    == Op_VROUND
    |  operation
    == Op_VTRUNC
    |  operation
    == Op_VFLOOR
    |  operation
    == Op_VCEIL

function vector_fp_exact_operation(operation : Semantic_operation) -> bool =
    operation == Op_VNEG | operation == Op_VABS | operation == Op_VCOPYSIGN | operation == Op_VCLASS

function vector_fp_lane_exact(
    operation : Semantic_operation,
    element_bytes : int,
    source : bits(64),
    destination : bits(64),
    source_present : bool,
) -> (
    option(bits(64))
) =
    if operation == Op_VNEG then {
        fp_exact_arithmetic(FpArithmeticNegate, if source_present then source else destination, element_bytes)
    } else {
        if operation == Op_VABS then {
            fp_exact_arithmetic(FpArithmeticAbsolute, if source_present then source else destination, element_bytes)
        } else {
            if operation == Op_VCOPYSIGN then {
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
                let fused =    operation
                            == Op_VMADD
                            |  operation
                            == Op_VMSUB
                            |  operation
                            == Op_VNMADD
                            |  operation
                            == Op_VNMSUB;
                let unary =    operation
                            == Op_VSQRT
                            |  operation
                            == Op_VROUND
                            |  operation
                            == Op_VTRUNC
                            |  operation
                            == Op_VFLOOR
                            |  operation
                            == Op_VCEIL;
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

function vector_fp_conversion_destination_bytes(operation : Semantic_operation) -> int =
    if operation == Op_VCVTH | operation == Op_VCVTUH then {
        2
    } else {
        if operation == Op_VCVTS | operation == Op_VCVTUS | operation == Op_VCVTL | operation == Op_VCVTUL then {
            4
        } else {
            8
        }
    }

function vector_fp_conversion_destination_fp(operation : Semantic_operation) -> bool =
       operation
    == Op_VCVTH
    |  operation
    == Op_VCVTUH
    |  operation
    == Op_VCVTS
    |  operation
    == Op_VCVTUS
    |  operation
    == Op_VCVTD
    |  operation
    == Op_VCVTUD

function vector_fp_conversion_source_kind(
    instruction : Decoded_instruction,
    source_bytes : int,
    conversion : Fp_conversion_operation,
) -> (
    bits(8)
) = {
    let operation = instruction.form.operation;
    if vector_fp_conversion_destination_fp(operation) & conversion == FpConvertUnsigned then {
        0x05
    } else {
        if vector_fp_conversion_destination_fp(operation) then {
            match instruction.form.sizes {
                Size_L :: _ => 0x04,
                Size_Q :: _ => 0x04,
                _ => vector_fp_value_kind(source_bytes),
            }
        } else {
            vector_fp_value_kind(source_bytes)
        }
    }
}

function vector_fp_conversion_lanes(
    instruction : Decoded_instruction,
    source : list(bits(8)),
    destination : list(bits(8)),
    predicate : list(bits(8)),
    offset : int,
    vector_bytes : int,
    source_bytes : int,
    destination_bytes : int,
    control : bits(8),
    result : list(bits(8)),
    generated_causes : bits(5),
) -> (
    option(Vector_fp_image)
) =
    if offset >= vector_bytes then {
        Some(struct { bytes = result, generated_causes = generated_causes })
    } else {
        let container_bytes = if source_bytes > destination_bytes then { source_bytes } else { destination_bytes };
        if not_bool(predicate_bit(predicate, offset)) then {
            vector_fp_conversion_lanes(
                instruction,
                source,
                destination,
                predicate,
                offset + container_bytes,
                vector_bytes,
                source_bytes,
                destination_bytes,
                control,
                result,
                generated_causes,
            )
        } else {
            let conversion = if    instruction.form.operation
                                == Op_VCVTUH
                                |  instruction.form.operation
                                == Op_VCVTUS
                                |  instruction.form.operation
                                == Op_VCVTUD
                                |  instruction.form.operation
                                == Op_VCVTUL
                                |  instruction.form.operation
                                == Op_VCVTUQ then {
                    FpConvertUnsigned
                } else {
                    FpConvertSigned
                };
            match fp_primitive_evaluate(
                instruction.form.operation,
                source_bytes,
                if vector_fp_conversion_destination_fp(instruction.form.operation)
                then vector_fp_result_kind(destination_bytes)
                else 0x04,
                control,
                1,
                vector_fp_conversion_source_kind(instruction, source_bytes, conversion),
                get_slice_int(64, vector_lane_unsigned_loop(source, offset, source_bytes, 1, 0), 0),
                0x00,
                0x0000000000000000,
                0x00,
                0x0000000000000000,
                false,
            ) {
                None() => None(),
                Some(evaluation) => vector_fp_conversion_lanes(
                    instruction,
                    source,
                    destination,
                    predicate,
                    offset + container_bytes,
                    vector_bytes,
                    source_bytes,
                    destination_bytes,
                    control,
                    vector_write_lane(
                        result,
                        tdiv_int(offset, destination_bytes),
                        destination_bytes,
                        unsigned(evaluation.primary),
                    ),
                    generated_causes | evaluation.generated_causes,
                ),
            }
        }
    }

function vector_fp_named_image(
    instruction : Decoded_instruction,
    state : Cpu_state,
    memory : list(bits(8)),
    name : Operand_id,
) -> (
    option(list(bits(8)))
) =
    match operand_named(instruction, name) {
        Some(operand) => if operand.operand_type == OperandType_Vn then {
            Some(state.vector_registers[unsigned(operand.value[4 .. 0])])
        } else {
            if operand.operand_type == OperandType_VEA then {
                Some(memory)
            } else {
                None()
            }
        },
        None() => None(),
    }

function vector_fp_commit_image(
    instruction : Decoded_instruction,
    before : Cpu_state,
    image : Vector_fp_image,
) -> (
    Execution_result
) = {
    let operation = instruction.form.operation;
    if (image.generated_causes & vector_fp_allowed_causes(operation)) != image.generated_causes then {
        faulted(before, operation, InvalidControlState, "vector FP primitive reported an impossible cause")
    } else {
        if fp_traps(before.fstatus, image.generated_causes) then {
            fp_fault_with_causes(before, operation, image.generated_causes)
        } else {
            match vector_writable_operand(instruction.operands) {
                None() => faulted(before, operation, InvalidControlState, "missing vector FP destination"),
                Some(destination) => {
                    var updated = advance_pc(before, instruction);
                    updated.fflags = updated.fflags | image.generated_causes;
                    if image.generated_causes != fflags_none then {
                        updated.fp_component_modified = true
                    };
                    if destination.operand_type == OperandType_Vn then {
                        updated.vector_registers[unsigned(destination.value[4 .. 0])] = image.bytes;
                        updated.vector_component_modified = true;
                        completed(before, updated, CommitRegisters, [||])
                    } else {
                        if destination.operand_type == OperandType_Pn then {
                            updated.predicate_registers[unsigned(destination.value[3 .. 0])] = image.bytes;
                            updated.vector_component_modified = true;
                            completed(before, updated, CommitRegisters, [||])
                        } else {
                            faulted(before, operation, InvalidControlState, "unsupported local vector FP destination")
                        }
                    }
                },
            }
        }
    }
}

function vector_fp_evaluate_image(
    instruction : Decoded_instruction,
    state : Cpu_state,
    memory : list(bits(8)),
) -> (
    option(Vector_fp_image)
) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let predicate = vector_memory_predicate(instruction, state);
    let empty_vector = zero_vector_bytes(state.vector_length_bytes);
    let control = fp_primitive_control(
        fp_fstatus_rounding_mode(state.fstatus),
        fp_fstatus_ftz(state.fstatus),
        fp_fstatus_daz(state.fstatus),
        fp_fstatus_dn(state.fstatus),
    );
    let compare_right : option(list(bits(8))) = match vector_fp_named_image(instruction, state, memory, Operand_rhs) {
        Some(image) => Some(image),
        None() => vector_fp_named_image(instruction, state, memory, Operand_src),
    };
    if operation == Op_VCMPcc then {
        match (vector_fp_named_image(instruction, state, memory, Operand_lhs), compare_right) {
            (Some(left), Some(right)) => {
                let condition : int = match operand_named(instruction, Operand_cc) {
                    Some(value) => unsigned(value.value[3 .. 0]),
                    None() => 0,
                };
                match vector_fp_compare_lanes(
                    left,
                    right,
                    predicate,
                    0,
                    lanes,
                    element_bytes,
                    control,
                    condition,
                    zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8)),
                    fflags_none,
                ) {
                    Some(image) => Some(image),
                    None() => None(),
                }
            },
            _ => None(),
        }
    } else {
        if vector_fp_convert_operation(operation) then {
            match (
                vector_fp_named_image(instruction, state, memory, Operand_src),
                vector_fp_named_image(instruction, state, memory, Operand_dst),
            ) {
                (Some(source), Some(destination)) => match vector_fp_conversion_lanes(
                    instruction,
                    source,
                    destination,
                    predicate,
                    0,
                    state.vector_length_bytes,
                    element_bytes,
                    vector_fp_conversion_destination_bytes(operation),
                    control,
                    destination,
                    fflags_none,
                ) {
                    Some(image) => Some(image),
                    None() => None(),
                },
                _ => None(),
            }
        } else {
            if vector_fp_primitive_operation(operation) | vector_fp_exact_operation(operation) then {
                match vector_fp_named_image(instruction, state, memory, Operand_dst) {
                    None() => None(),
                    Some(destination) => {
                        let source_image = vector_fp_named_image(instruction, state, memory, Operand_src);
                        let source : list(bits(8)) = match source_image {
                            Some(image) => image,
                            None() => empty_vector,
                        };
                        let lhs : list(bits(8)) = match vector_fp_named_image(instruction, state, memory, Operand_lhs) {
                            Some(image) => image,
                            None() => empty_vector,
                        };
                        let rhs : list(bits(8)) = match vector_fp_named_image(instruction, state, memory, Operand_rhs) {
                            Some(image) => image,
                            None() => empty_vector,
                        };
                        match vector_fp_arithmetic_lanes(
                            operation,
                            source,
                            lhs,
                            rhs,
                            destination,
                            predicate,
                            0,
                            lanes,
                            element_bytes,
                            control,
                            destination,
                            fflags_none,
                            source_image != None(),
                        ) {
                            Some(image) => Some(image),
                            None() => None(),
                        }
                    },
                }
            } else {
                None()
            }
        }
    }
}

function execute_vector_fp_register(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    if not_bool(
        vector_fp_basic_operation(instruction.form.operation) | vector_fp_convert_operation(instruction.form.operation),
    ) then {
        None()
    } else {
        match vector_fp_evaluate_image(instruction, state, [||]) {
            Some(image) => Some(vector_fp_commit_image(instruction, state, image)),
            None() => Some(
                faulted(state, instruction.form.operation, InvalidControlState, "local vector FP evaluation failed"),
            ),
        }
    }

union clause Uop_kind = UopVectorFp : Semantic_operation

val execute_vector_fp_uop : (
        Semantic_operation,
        Micro_operation,
        list(Uop_value),
        Decoded_instruction,
        Cpu_state,
        Cpu_state,
    ) -> Uop_step

function vector_local_result_uop_step(
    result : Execution_result,
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
    values : list(Uop_value),
) -> (
    Uop_step
) =
    uop_local_result_step(result, speculative, values)

function clause execute_uop(UopVectorFp(operation), uop, values, instruction, before, speculative) =
    execute_vector_fp_uop(operation, uop, values, instruction, before, speculative)

function vector_memory_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) =
    match operands {
        [||] => None(),
        operand :: tail => match operand.ea {
            Some(_) => Some(operand),
            None() => vector_memory_operand(tail),
        },
    }

function vector_memory_request(
    kind : Primitive_request_kind,
    instruction : Decoded_instruction,
    state : Cpu_state,
    evaluation : Ea_evaluation,
    predicate : list(bits(8)),
    values : list(bits(8)),
    element_bytes : int,
    access : Transaction_access,
) -> (
    Primitive_request
) = {
    let length = if instruction.form.operation == Op_PMOV then {
            tdiv_int(state.vector_length_bytes, 8)
        } else {
            state.vector_length_bytes
        };
    struct {
        kind = kind,
        ordinal = 0,
        role = request_role_for_ea(evaluation.role),
        domain = request_domain_for_operand(evaluation.domain),
        segment = evaluation.segment,
        segment_image = evaluation.segment_image,
        width = element_bytes,
        range_start = evaluation.effective_address,
        range_end = add_bits(evaluation.effective_address, get_slice_int(64, length, 0)),
        range_length = length,
        range_wrap = unsigned(evaluation.effective_address) + length > 18446744073709551616,
        range_end_at_modulus = unsigned(evaluation.effective_address) + length == 18446744073709551616,
        effective_address = evaluation.effective_address,
        linear_address = evaluation.linear_address,
        access = access,
        value = 0x0000000000000000,
        address_translation = true,
        commit_point = true,
        memory_order = 0,
        cache_policy = 0,
        suppress_fault = false,
        staged_updates = evaluation.staged_updates,
        selector = 0x0000000000000000,
        expected = 0x0000000000000000,
        desired = 0x0000000000000000,
        auxiliary = get_slice_int(64, element_bytes, 0),
        body_length = length,
        payload_bytes = append_bytes(predicate, values),
    }
}

union clause Uop_kind = UopVectorCalcEa : unit
union clause Uop_kind = UopVectorMemoryLoad : unit
union clause Uop_kind = UopVectorMemoryStore : unit
union clause Uop_kind = UopVectorMemoryCompute : Semantic_operation

val vector_integer_binary_operation : Semantic_operation -> bool
val vector_shift_operation_p : Semantic_operation -> bool
val vector_memory_direct_store_image : (Decoded_instruction, Cpu_state, list(bits(8)), int, int) -> option(
        list(bits(8)),
    )
val vector_response_length : (Decoded_instruction, Cpu_state) -> int
val vector_memory_source_result : (Decoded_instruction, Cpu_state, Cpu_state, list(bits(8))) -> option(Cpu_state)
val vector_memory_destination_result : (Decoded_instruction, Cpu_state, list(bits(8))) -> option(list(bits(8)))

function vector_uop_address_value(evaluation : Ea_evaluation) -> Uop_value =
    {
        empty_uop_value() with
        address = true,
        segment = evaluation.segment,
        segment_image = evaluation.segment_image,
        effective_address = evaluation.effective_address,
        linear_address = evaluation.linear_address,
        domain = request_domain_for_operand(evaluation.domain),
    }

function vector_uop_memory_request(
    kind : Primitive_request_kind,
    instruction : Decoded_instruction,
    state : Cpu_state,
    address : Uop_value,
    values : list(bits(8)),
    access : Transaction_access,
) -> (
    Primitive_request
) = {
    let element_bytes = if instruction.form.operation == Op_PMOV then {
            tdiv_int(state.vector_length_bytes, 8)
        } else {
            operation_width(instruction)
        };
    let length = if instruction.form.operation == Op_PMOV then {
            tdiv_int(state.vector_length_bytes, 8)
        } else {
            state.vector_length_bytes
        };
    struct {
        kind = kind,
        ordinal = 0,
        role = RequestRoleValue,
        domain = address.domain,
        segment = address.segment,
        segment_image = address.segment_image,
        width = element_bytes,
        range_start = address.effective_address,
        range_end = add_bits(address.effective_address, get_slice_int(64, length, 0)),
        range_length = length,
        range_wrap = unsigned(address.effective_address) + length > 18446744073709551616,
        range_end_at_modulus = unsigned(address.effective_address) + length == 18446744073709551616,
        effective_address = address.effective_address,
        linear_address = address.linear_address,
        access = access,
        value = 0x0000000000000000,
        address_translation = true,
        commit_point = true,
        memory_order = 0,
        cache_policy = 0,
        suppress_fault = false,
        staged_updates = [||],
        selector = 0x0000000000000000,
        expected = 0x0000000000000000,
        desired = 0x0000000000000000,
        auxiliary = get_slice_int(64, element_bytes, 0),
        body_length = length,
        payload_bytes = append_bytes(vector_memory_predicate(instruction, state), values),
    }
}

function clause execute_uop(UopVectorCalcEa(), uop, values, instruction, before, speculative) =
    match vector_memory_operand(instruction.operands) {
        None() => uop_continue(speculative, values),
        Some(memory_operand) => {
            let evaluated = if instruction.form.operation == Op_PMOV then {
                    match memory_operand.ea {
                        None() => None(),
                        Some(ea) => Some(
                            evaluate_decoded_ea(
                                memory_operand,
                                ea,
                                speculative,
                                speculative.pc,
                                tdiv_int(speculative.vector_length_bytes, 8),
                            ),
                        ),
                    }
                } else {
                    evaluate_vector_instruction_ea(
                        instruction.operands,
                        speculative,
                        speculative.pc,
                        operation_width(instruction),
                    )
                };
            match evaluated {
                Some((evaluation, evaluated_state)) => uop_continue(
                    evaluated_state,
                    uop_value_set(values, uop.destination.index, vector_uop_address_value(evaluation)),
                ),
                None() => uop_fault(
                    faulted(
                        before,
                        instruction.form.operation,
                        InvalidControlState,
                        "missing vector uop memory address",
                    ),
                ),
            }
        },
    }

function clause execute_uop(UopVectorMemoryLoad(), uop, values, instruction, before, speculative) =
    match vector_memory_operand(instruction.operands) {
        None() => uop_continue(speculative, values),
        Some(memory_operand) => {
            let memory_destination = vector_operand_writes(memory_operand.name, instruction.operands);
            let needs_read =   not_bool(memory_destination)
                             | vector_fp_compute_operation(instruction.form.operation)
                             | vector_integer_binary_operation(instruction.form.operation)
                             | vector_shift_operation_p(instruction.form.operation);
            if not_bool(needs_read) then {
                uop_continue(speculative, values)
            } else {
                match uop_value_at(values, uop.source0.index) {
                    Some(address) => uop_wait(
                        uop.destination.index,
                        vector_uop_memory_request(
                            VectorMemoryRead,
                            instruction,
                            speculative,
                            address,
                            [||],
                            if vector_operand_writes(memory_operand.name, instruction.operands)
                            then AccessReadModifyWrite
                            else AccessLoad,
                        ),
                        0x0000000000000000,
                    ),
                    None() => uop_fault(
                        faulted(
                            before,
                            instruction.form.operation,
                            InvalidControlState,
                            "vector uop load address is unavailable",
                        ),
                    ),
                }
            }
        },
    }

function clause execute_uop(UopVectorMemoryCompute(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector memory uop does not match its instruction",
            ),
        )
    } else {
        match vector_memory_operand(instruction.operands) {
            None() => uop_fault(
                faulted(before, operation, InvalidControlState, "vector memory uop has no memory operand"),
            ),
            Some(memory_operand) => {
                let memory_destination = vector_operand_writes(memory_operand.name, instruction.operands);
                if memory_destination then {
                    let computed = if vector_integer_binary_operation(operation) | vector_shift_operation_p(operation) then {
                            match uop_value_at(values, uop.auxiliary.index) {
                                Some(memory) => vector_memory_destination_result(instruction, before, memory.body_bytes),
                                None() => None(),
                            }
                        } else {
                            let predicate = if operation == Op_PMOV then {
                                    [||]
                                } else {
                                    vector_memory_predicate(instruction, before)
                                };
                            let element_bytes = if operation == Op_PMOV then {
                                    tdiv_int(before.vector_length_bytes, 8)
                                } else {
                                    operation_width(instruction)
                                };
                            let lanes = if operation == Op_PMOV then {
                                    1
                                } else {
                                    tdiv_int(before.vector_length_bytes, element_bytes)
                                };
                            vector_memory_direct_store_image(instruction, before, predicate, lanes, element_bytes)
                        };
                    match computed {
                        Some(output) => uop_continue(
                            speculative,
                            uop_value_set(values, uop.destination.index, { empty_uop_value() with body_bytes = output }),
                        ),
                        None() => uop_fault(
                            faulted(before, operation, IllegalInstruction, "unsupported vector memory destination uop"),
                        ),
                    }
                } else {
                    match uop_value_at(values, uop.auxiliary.index) {
                        Some(memory) => if byte_count(memory.body_bytes) != vector_response_length(instruction, before) then {
                            uop_fault(
                                faulted(
                                    before,
                                    operation,
                                    InvalidControlState,
                                    "vector memory response length mismatch",
                                ),
                            )
                        } else {
                            match vector_memory_source_result(instruction, before, speculative, memory.body_bytes) {
                                Some(updated) => uop_continue(updated, values),
                                None() => uop_fault(
                                    faulted(
                                        before,
                                        operation,
                                        IllegalInstruction,
                                        "unsupported vector memory source uop",
                                    ),
                                ),
                            }
                        },
                        None() => uop_fault(
                            faulted(before, operation, InvalidControlState, "vector memory response is unavailable"),
                        ),
                    }
                }
            },
        }
    }

function vector_fp_uop_commit_image(
    image : Vector_fp_image,
    uop : Micro_operation,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Uop_step
) = {
    let operation = instruction.form.operation;
    if (image.generated_causes & vector_fp_allowed_causes(operation)) != image.generated_causes then {
        uop_fault(faulted(before, operation, InvalidControlState, "vector FP primitive reported an impossible cause"))
    } else {
        if fp_traps(before.fstatus, image.generated_causes) then {
            uop_fault(fp_fault_with_causes(before, operation, image.generated_causes))
        } else {
            match vector_writable_operand(instruction.operands) {
                None() => uop_fault(faulted(before, operation, InvalidControlState, "missing vector FP destination")),
                Some(destination) => {
                    var updated = speculative;
                    updated.fflags = updated.fflags | image.generated_causes;
                    if image.generated_causes != fflags_none then {
                        updated.fp_component_modified = true
                    };
                    if destination.operand_type == OperandType_Vn then {
                        updated.vector_registers[unsigned(destination.value[4 .. 0])] = image.bytes;
                        updated.vector_component_modified = true;
                        uop_continue(updated, values)
                    } else {
                        if destination.operand_type == OperandType_Pn then {
                            updated.predicate_registers[unsigned(destination.value[3 .. 0])] = image.bytes;
                            updated.vector_component_modified = true;
                            uop_continue(updated, values)
                        } else {
                            if destination.operand_type == OperandType_VEA then {
                                uop_continue(
                                    updated,
                                    uop_value_set(
                                        values,
                                        uop.destination.index,
                                        {
                                            empty_uop_value() with
                                            body_bytes = image.bytes,
                                        },
                                    ),
                                )
                            } else {
                                uop_fault(
                                    faulted(before, operation, InvalidControlState, "unsupported vector FP destination"),
                                )
                            }
                        }
                    }
                },
            }
        }
    }
}

function execute_vector_fp_uop(
    operation : Semantic_operation,
    uop : Micro_operation,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Uop_step
) =
    if instruction.form.operation != operation then {
        uop_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector FP uop does not match its instruction",
            ),
        )
    } else {
        match vector_memory_operand(instruction.operands) {
            None() => if vector_fp_reduction_operation(operation) then {
                match vector_register_index(instruction, Operand_src) {
                    Some(source) => vector_local_result_uop_step(
                        vector_fp_reduction_commit(
                            instruction,
                            speculative,
                            speculative,
                            speculative.vector_registers[unsigned(source)],
                        ),
                        instruction,
                        before,
                        speculative,
                        values,
                    ),
                    None() => uop_fault(
                        faulted(before, operation, InvalidControlState, "missing vector FP reduction source"),
                    ),
                }
            } else {
                match execute_vector_fp_register(instruction, speculative) {
                    Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
                    None() => uop_fault(
                        faulted(before, operation, InvalidControlState, "local vector FP evaluation failed"),
                    ),
                }
            },
            Some(_) => match uop_value_at(values, uop.auxiliary.index) {
                Some(memory_value) => if byte_count(memory_value.body_bytes) != before.vector_length_bytes then {
                    uop_fault(
                        faulted(before, operation, InvalidControlState, "vector FP memory response length mismatch"),
                    )
                } else {
                    if vector_fp_reduction_operation(operation) then {
                        vector_local_result_uop_step(
                            vector_fp_reduction_commit(instruction, before, speculative, memory_value.body_bytes),
                            instruction,
                            before,
                            speculative,
                            values,
                        )
                    } else {
                        match vector_fp_evaluate_image(instruction, before, memory_value.body_bytes) {
                            Some(image) => vector_fp_uop_commit_image(
                                image,
                                uop,
                                values,
                                instruction,
                                before,
                                speculative,
                            ),
                            None() => uop_fault(
                                faulted(
                                    before,
                                    operation,
                                    InvalidControlState,
                                    "local vector FP memory evaluation failed",
                                ),
                            ),
                        }
                    }
                },
                None() => uop_fault(
                    faulted(before, operation, InvalidControlState, "vector FP memory response is unavailable"),
                ),
            },
        }
    }

function clause execute_uop(UopVectorMemoryStore(), uop, values, instruction, before, speculative) =
    match vector_memory_operand(instruction.operands) {
        None() => uop_continue(speculative, values),
        Some(memory_operand) => if not_bool(vector_operand_writes(memory_operand.name, instruction.operands)) then {
            uop_continue(speculative, values)
        } else {
            match (uop_value_at(values, uop.source0.index), uop_value_at(values, uop.source1.index)) {
                (Some(address), Some(output)) => uop_wait(
                    0 - 1,
                    vector_uop_memory_request(
                        VectorMemoryWrite,
                        instruction,
                        speculative,
                        address,
                        output.body_bytes,
                        AccessStore,
                    ),
                    0x0000000000000000,
                ),
                _ => uop_fault(
                    faulted(
                        before,
                        instruction.form.operation,
                        InvalidControlState,
                        "vector uop store input is unavailable",
                    ),
                ),
            }
        },
    }

function vector_integer_binary_operation(operation : Semantic_operation) -> bool =
       operation
    == Op_VADD
    |  operation
    == Op_VSUB
    |  operation
    == Op_VAND
    |  operation
    == Op_VOR
    |  operation
    == Op_VXOR
    |  operation
    == Op_VMINS
    |  operation
    == Op_VMINU
    |  operation
    == Op_VMAXS
    |  operation
    == Op_VMAXU
    |  operation
    == Op_VMUL
    |  operation
    == Op_VMULHS
    |  operation
    == Op_VMULHU
    |  operation
    == Op_VMULHSU

function vector_integer_unary_operation(operation : Semantic_operation) -> bool =
       operation
    == Op_VNEG
    |  operation
    == Op_VABS
    |  operation
    == Op_VNOT
    |  operation
    == Op_VCLZ
    |  operation
    == Op_VCTZ
    |  operation
    == Op_VCLS
    |  operation
    == Op_VCTS
    |  operation
    == Op_VPOPCNT
    |  operation
    == Op_VREVBYTE

function vector_shift_operation_p(operation : Semantic_operation) -> bool =
    operation == Op_VSHL | operation == Op_VSHR | operation == Op_VSAR | operation == Op_VROL | operation == Op_VROR

function vector_integer_compare_operation(operation : Semantic_operation) -> bool =
    operation == Op_VCMPcc | operation == Op_VTESTZ | operation == Op_VTESTNZ

function vector_memory_direct_store_image(
    instruction : Decoded_instruction,
    state : Cpu_state,
    predicate : list(bits(8)),
    lanes : int,
    element_bytes : int,
) -> (
    option(list(bits(8)))
) = {
    let operation = instruction.form.operation;
    if operation == Op_PMOV then {
        match predicate_register_index(instruction, Operand_src) {
            Some(index) => Some(state.predicate_registers[unsigned(index)]),
            None() => None(),
        }
    } else {
        match vector_register_index(instruction, Operand_src) {
            None() => None(),
            Some(index) => {
                let source = state.vector_registers[unsigned(index)];
                if operation == Op_VMOV then {
                    Some(source)
                } else {
                    if vector_integer_unary_operation(operation) then {
                        Some(
                            vector_integer_unary_source_image(
                                operation,
                                zero_vector_bytes(state.vector_length_bytes),
                                source,
                                predicate,
                                0,
                                lanes,
                                element_bytes,
                            ),
                        )
                    } else {
                        None()
                    }
                }
            },
        }
    }
}

function vector_step_operation(operation : Semantic_operation) -> bool =
    operation == Op_VGATHER1 | operation == Op_VSCATTER1

function vector_lane_bytes_loop(image : list(bits(8)), index : int, remaining : int) -> list(bits(8)) =
    if remaining <= 0 then {
        [||]
    } else {
        vector_byte_at(image, index) :: vector_lane_bytes_loop(image, index + 1, remaining - 1)
    }

function vector_lane_bytes(image : list(bits(8)), lane : int, element_bytes : int) -> list(bits(8)) =
    vector_lane_bytes_loop(image, lane * element_bytes, element_bytes)

function vector_step_register_index(instruction : Decoded_instruction, name : Operand_id) -> option(bits(4)) =
    match operand_named(instruction, name) {
        Some(operand) => Some(operand.value[3 .. 0]),
        None() => None(),
    }

function vector_step_overlap_conflict(instruction : Decoded_instruction) -> bool =
    match vector_step_register_index(instruction, Operand_cursor) {
        None() => false,
        Some(cursor) => {
            let base_conflict : bool = match vector_step_register_index(instruction, Operand_base) {
                Some(base) => cursor == base,
                None() => false,
            };
            let stride_conflict : bool = match vector_step_register_index(instruction, Operand_stride) {
                Some(stride) => cursor == stride,
                None() => false,
            };
            base_conflict | stride_conflict
        },
    }

function vector_step_payload(instruction : Decoded_instruction, name : Operand_id, exact : bool) -> int =
    match operand_named(instruction, name) {
        None() => 0,
        Some(operand) => if exact then {
            unsigned(immediate_value(operand))
        } else {
            signed(immediate_value(operand))
        },
    }

function vector_step_address(
    instruction : Decoded_instruction,
    state : Cpu_state,
    lane : int,
    element_bytes : int,
) -> (
    option(bits(64))
) = {
    let form_id = instruction.form.form_id;
    if    form_id
       == Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_rn_i_mul_rn_s_vn_v
       |  form_id
       == Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_rn_i_mul_rn_s then {
        match (
            vector_step_register_index(instruction, Operand_base),
            vector_step_register_index(instruction, Operand_stride),
        ) {
            (Some(base), Some(stride)) => Some(
                get_slice_int(
                    64,
                    unsigned(state.registers[unsigned(base)]) + lane * signed(state.registers[unsigned(stride)]),
                    0,
                ),
            ),
            _ => None(),
        }
    } else {
        match vector_register_index(instruction, Operand_address) {
            None() => None(),
            Some(address) => {
                let lane_value = vector_lane_unsigned(state.vector_registers[unsigned(address)], lane, element_bytes);
                if    form_id
                   == Form_xxlong_vgather1_l_pn_p_vn_x_rn_i_vn_v
                   |  form_id
                   == Form_xxlong_vgather1_q_pn_p_vn_x_rn_i_vn_v
                   |  form_id
                   == Form_xxlong_vscatter1_l_pn_p_vn_v_vn_x_rn_i
                   |  form_id
                   == Form_xxlong_vscatter1_q_pn_p_vn_v_vn_x_rn_i then {
                    Some(get_slice_int(64, lane_value, 0))
                } else {
                    match vector_step_register_index(instruction, Operand_base) {
                        None() => None(),
                        Some(base) => {
                            let lane_offset = if    form_id
                                                 == Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_vn_v
                                                 |  form_id
                                                 == Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i then {
                                    vector_signed_lane(lane_value, element_bytes)
                                } else {
                                    lane_value * element_bytes
                                };
                            let displacement = if    form_id
                                                  == Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp8s_vn_v
                                                  |  form_id
                                                  == Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp8s then {
                                    vector_step_payload(instruction, Operand_disp8s, false)
                                } else {
                                    if    form_id
                                       == Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp16s_vn_v
                                       |  form_id
                                       == Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp16s then {
                                        vector_step_payload(instruction, Operand_disp16s, false)
                                    } else {
                                        if    form_id
                                           == Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp32s_vn_v
                                           |  form_id
                                           == Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp32s then {
                                            vector_step_payload(instruction, Operand_disp32s, false)
                                        } else {
                                            if    form_id
                                               == Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp64_vn_v
                                               |  form_id
                                               == Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp64 then {
                                                vector_step_payload(instruction, Operand_disp64, true)
                                            } else {
                                                0
                                            }
                                        }
                                    }
                                };
                            Some(
                                get_slice_int(
                                    64,
                                    unsigned(state.registers[unsigned(base)]) + lane_offset + displacement,
                                    0,
                                ),
                            )
                        },
                    }
                }
            },
        }
    }
}

function vector_step_request(
    instruction : Decoded_instruction,
    state : Cpu_state,
    address : bits(64),
    element_bytes : int,
    values : list(bits(8)),
) -> (
    Primitive_request
) = {
    let operation = instruction.form.operation;
    let segment_image = state.segments[1];
    let point = segment_point(segment_image, address);
    let total = unsigned(address) + element_bytes;
    struct {
        kind = if operation == Op_VGATHER1 then VectorMemoryRead else VectorMemoryWrite,
        ordinal = 0,
        role = RequestRoleValue,
        domain = RequestDomainCurrent,
        segment = 1,
        segment_image = segment_image,
        width = element_bytes,
        range_start = address,
        range_end = add_bits(address, get_slice_int(64, element_bytes, 0)),
        range_length = element_bytes,
        range_wrap = total > 18446744073709551616,
        range_end_at_modulus = total == 18446744073709551616,
        effective_address = address,
        linear_address = point.linear,
        access = if operation == Op_VGATHER1 then AccessLoad else AccessStore,
        value = 0x0000000000000000,
        address_translation = true,
        commit_point = true,
        memory_order = 0,
        cache_policy = 0,
        suppress_fault = false,
        staged_updates = [||],
        selector = 0x0000000000000000,
        expected = 0x0000000000000000,
        desired = 0x0000000000000000,
        auxiliary = get_slice_int(64, element_bytes, 0),
        body_length = element_bytes,
        payload_bytes = append_bytes([|0x01|], values),
    }
}

union clause Uop_kind = UopVectorStepPrepare : Semantic_operation
union clause Uop_kind = UopVectorStepIssue : Semantic_operation
union clause Uop_kind = UopVectorStepCommit : Semantic_operation

function clause execute_uop(UopVectorStepPrepare(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector step uop does not match its instruction",
            ),
        )
    } else {
        if vector_step_overlap_conflict(instruction) then {
            uop_fault(faulted(before, operation, IllegalInstruction, "vector step cursor overlaps its base or stride"))
        } else {
            match (
                vector_step_register_index(instruction, Operand_cursor),
                predicate_register_index(instruction, Operand_govern),
            ) {
                (Some(cursor), Some(govern)) => {
                    let element_bytes = operation_width(instruction);
                    let lane = unsigned(speculative.registers[unsigned(cursor)]);
                    let lanes = tdiv_int(speculative.vector_length_bytes, element_bytes);
                    if lane >= lanes then {
                        uop_fault(
                            faulted_with_error_code(
                                before,
                                operation,
                                VectorRangeFault,
                                "vector step lane cursor exceeds the lane count",
                                0x0000000000000001,
                            ),
                        )
                    } else {
                        let active = predicate_bit(
                            speculative.predicate_registers[unsigned(govern)],
                            lane * element_bytes,
                        );
                        var updated = speculative;
                        updated.registers[unsigned(cursor)] = add_bits(
                            speculative.registers[unsigned(cursor)],
                            0x0000000000000001,
                        );
                        uop_continue(
                            updated,
                            uop_value_set(
                                values,
                                uop.destination.index,
                                {
                                    empty_uop_value() with
                                    value = get_slice_int(64, lane, 0),
                                    present = active,
                                },
                            ),
                        )
                    }
                },
                _ => uop_fault(
                    faulted(before, operation, InvalidControlState, "missing vector step cursor or predicate"),
                ),
            }
        }
    }

function clause execute_uop(UopVectorStepIssue(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector step issue does not match its instruction",
            ),
        )
    } else {
        match uop_value_at(values, uop.source0.index) {
            Some(prepared) => if not_bool(prepared.present) then {
                uop_continue(speculative, values)
            } else {
                let lane = unsigned(prepared.value);
                let element_bytes = operation_width(instruction);
                match vector_step_address(instruction, before, lane, element_bytes) {
                    None() => uop_fault(
                        faulted(before, operation, InvalidControlState, "missing vector step address operand"),
                    ),
                    Some(address) => {
                        let payload : list(bits(8)) = if operation == Op_VSCATTER1 then {
                                match vector_register_index(instruction, Operand_src) {
                                    Some(source) => vector_lane_bytes(
                                        before.vector_registers[unsigned(source)],
                                        lane,
                                        element_bytes,
                                    ),
                                    None() => [||],
                                }
                            } else {
                                [||]
                            };
                        uop_wait(
                            uop.destination.index,
                            vector_step_request(instruction, before, address, element_bytes, payload),
                            0x0000000000000000,
                        )
                    },
                }
            },
            None() => uop_fault(
                faulted(before, operation, InvalidControlState, "vector step preparation is unavailable"),
            ),
        }
    }

function clause execute_uop(UopVectorStepCommit(operation), uop, values, instruction, before, speculative) =
    if instruction.form.operation != operation then {
        uop_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "vector step commit does not match its instruction",
            ),
        )
    } else {
        match uop_value_at(values, uop.source0.index) {
            Some(prepared) => if not_bool(prepared.present) then {
                uop_complete(speculative, CommitRegisters)
            } else {
                if operation == Op_VSCATTER1 then {
                    uop_complete(speculative, CommitMemory)
                } else {
                    match (vector_register_index(instruction, Operand_dst), uop_value_at(values, uop.source1.index)) {
                        (Some(destination), Some(response)) => {
                            let element_bytes = operation_width(instruction);
                            let lane = unsigned(prepared.value);
                            if byte_count(response.body_bytes) != element_bytes then {
                                uop_fault(
                                    faulted(
                                        before,
                                        operation,
                                        InvalidControlState,
                                        "vector gather response length mismatch",
                                    ),
                                )
                            } else {
                                var updated = speculative;
                                updated.vector_registers[unsigned(destination)] = vector_write_lane(
                                    before.vector_registers[unsigned(destination)],
                                    lane,
                                    element_bytes,
                                    vector_lane_unsigned(response.body_bytes, 0, element_bytes),
                                );
                                updated.vector_component_modified = true;
                                uop_complete(updated, CommitMemory)
                            }
                        },
                        _ => uop_fault(
                            faulted(
                                before,
                                operation,
                                InvalidControlState,
                                "missing vector gather destination or response",
                            ),
                        ),
                    }
                }
            },
            None() => uop_fault(
                faulted(before, operation, InvalidControlState, "vector step preparation is unavailable"),
            ),
        }
    }

function vector_response_length(instruction : Decoded_instruction, state : Cpu_state) -> int =
    if instruction.form.operation == Op_PMOV then {
        tdiv_int(state.vector_length_bytes, 8)
    } else {
        if instruction.form.operation == Op_VGATHER1 then {
            operation_width(instruction)
        } else {
            state.vector_length_bytes
        }
    }

function vector_memory_source_result(
    instruction : Decoded_instruction,
    before : Cpu_state,
    after : Cpu_state,
    memory : list(bits(8)),
) -> (
    option(Cpu_state)
) = {
    let operation = instruction.form.operation;
    if operation == Op_PMOV then {
        match predicate_register_index(instruction, Operand_dst) {
            None() => None(),
            Some(destination) => {
                var updated = after;
                updated.predicate_registers[unsigned(destination)] = memory;
                updated.vector_component_modified = true;
                Some(updated)
            },
        }
    } else {
        let element_bytes = operation_width(instruction);
        let lanes = tdiv_int(before.vector_length_bytes, element_bytes);
        let predicate = vector_memory_predicate(instruction, before);
        if operation == Op_VMOV | operation == Op_VMOVZ then {
            match vector_register_index(instruction, Operand_dst) {
                None() => None(),
                Some(destination) => {
                    var updated = after;
                    updated.vector_registers[unsigned(destination)] =
                        if operation == Op_VMOVZ then {
                            memory
                        } else {
                            vector_merge_image(
                                before.vector_registers[unsigned(destination)],
                                memory,
                                predicate,
                                0,
                                lanes,
                                element_bytes,
                            )
                        };
                    updated.vector_component_modified = true;
                    Some(updated)
                },
            }
        } else {
            if vector_integer_binary_operation(operation) then {
                match vector_register_index(instruction, Operand_dst) {
                    None() => None(),
                    Some(destination) => {
                        var updated = after;
                        updated.vector_registers[unsigned(destination)] = vector_integer_binary_image(
                            operation,
                            before.vector_registers[unsigned(destination)],
                            memory,
                            predicate,
                            0,
                            lanes,
                            element_bytes,
                        );
                        updated.vector_component_modified = true;
                        Some(updated)
                    },
                }
            } else {
                if vector_integer_unary_operation(operation) then {
                    match vector_register_index(instruction, Operand_dst) {
                        None() => None(),
                        Some(destination) => {
                            var updated = after;
                            updated.vector_registers[unsigned(destination)] = vector_integer_unary_source_image(
                                operation,
                                before.vector_registers[unsigned(destination)],
                                memory,
                                predicate,
                                0,
                                lanes,
                                element_bytes,
                            );
                            updated.vector_component_modified = true;
                            Some(updated)
                        },
                    }
                } else {
                    if vector_integer_reduction_operation(operation) then {
                        match operand_named(instruction, Operand_dst) {
                            None() => None(),
                            Some(destination) => {
                                var updated = after;
                                updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
                                    64,
                                    vector_integer_reduction_image(
                                        operation,
                                        memory,
                                        predicate,
                                        0,
                                        lanes,
                                        element_bytes,
                                        vector_integer_reduction_identity(operation, element_bytes),
                                    ),
                                    0,
                                );
                                Some(updated)
                            },
                        }
                    } else {
                        if vector_shift_operation_p(operation) then {
                            match vector_register_index(instruction, Operand_dst) {
                                None() => None(),
                                Some(destination) => {
                                    var updated = after;
                                    updated.vector_registers[unsigned(destination)] = vector_shift_image(
                                        operation,
                                        before.vector_registers[unsigned(destination)],
                                        memory,
                                        0,
                                        true,
                                        predicate,
                                        0,
                                        lanes,
                                        element_bytes,
                                    );
                                    updated.vector_component_modified = true;
                                    Some(updated)
                                },
                            }
                        } else {
                            if vector_integer_compare_operation(operation) then {
                                match (
                                    vector_register_index(instruction, Operand_lhs),
                                    predicate_register_index(instruction, Operand_govern),
                                    predicate_register_index(instruction, Operand_dst),
                                ) {
                                    (Some(left), Some(govern), Some(destination)) => {
                                        let condition : int = match operand_named(instruction, Operand_cc) {
                                            Some(value) => unsigned(value.value[3 .. 0]),
                                            None() => 0,
                                        };
                                        var updated = after;
                                        updated.predicate_registers[unsigned(destination)] = vector_integer_compare_image(
                                            operation,
                                            condition,
                                            before.vector_registers[unsigned(left)],
                                            memory,
                                            before.predicate_registers[unsigned(govern)],
                                            zero_vector_bytes(tdiv_int(before.vector_length_bytes, 8)),
                                            0,
                                            lanes,
                                            element_bytes,
                                        );
                                        updated.vector_component_modified = true;
                                        Some(updated)
                                    },
                                    _ => None(),
                                }
                            } else {
                                None()
                            }
                        }
                    }
                }
            }
        }
    }
}

function vector_memory_destination_result(
    instruction : Decoded_instruction,
    before : Cpu_state,
    memory : list(bits(8)),
) -> (
    option(list(bits(8)))
) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(before.vector_length_bytes, element_bytes);
    let predicate = vector_memory_predicate(instruction, before);
    if vector_integer_binary_operation(operation) then {
        match vector_register_index(instruction, Operand_src) {
            Some(source) => Some(
                vector_integer_binary_image(
                    operation,
                    memory,
                    before.vector_registers[unsigned(source)],
                    predicate,
                    0,
                    lanes,
                    element_bytes,
                ),
            ),
            None() => None(),
        }
    } else {
        if vector_shift_operation_p(operation) then {
            let counts : list(bits(8)) = match vector_register_index(instruction, Operand_src) {
                Some(source) => before.vector_registers[unsigned(source)],
                None() => zero_vector_bytes(before.vector_length_bytes),
            };
            let vector_counts = vector_register_index(instruction, Operand_src) != None();
            let immediate : int = match operand_named(instruction, Operand_count) {
                Some(value) => unsigned(immediate_value(value)),
                None() => 0,
            };
            Some(
                vector_shift_image(
                    operation,
                    memory,
                    counts,
                    immediate,
                    vector_counts,
                    predicate,
                    0,
                    lanes,
                    element_bytes,
                ),
            )
        } else {
            None()
        }
    }
}
