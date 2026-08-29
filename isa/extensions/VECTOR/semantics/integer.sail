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
    let kind = vector_semantics(operation).integer_binary;
    if kind == Some(VectorIntegerAdd) then {
        vector_normalized(destination + source, modulus)
    } else {
        if kind == Some(VectorIntegerSubtract) then {
            vector_normalized(destination - source, modulus)
        } else {
            if kind == Some(VectorIntegerAnd) then {
                unsigned(bits_from_int(destination) & bits_from_int(source))
            } else {
                if kind == Some(VectorIntegerOr) then {
                    unsigned(bits_from_int(destination) | bits_from_int(source))
                } else {
                    if kind == Some(VectorIntegerXor) then {
                        unsigned(xor_vec(bits_from_int(destination), bits_from_int(source)))
                    } else {
                        if kind == Some(VectorIntegerMinimumSigned) then {
                            vector_normalized(
                                if signed_destination < signed_source then signed_destination else signed_source,
                                modulus,
                            )
                        } else {
                            if kind == Some(VectorIntegerMinimumUnsigned) then {
                                if destination < source then { destination } else { source }
                            } else {
                                if kind == Some(VectorIntegerMaximumSigned) then {
                                    vector_normalized(
                                        if signed_destination > signed_source then signed_destination else signed_source,
                                        modulus,
                                    )
                                } else {
                                    if kind == Some(VectorIntegerMaximumUnsigned) then {
                                        if destination > source then { destination } else { source }
                                    } else {
                                        if kind == Some(VectorIntegerMultiplyLow) then {
                                            tmod_int(destination * source, modulus)
                                        } else {
                                            if kind == Some(VectorIntegerMultiplyHighUnsigned) then {
                                                tdiv_int(destination * source, modulus)
                                            } else {
                                                if kind == Some(VectorIntegerMultiplyHighSigned) then {
                                                    tdiv_int(
                                                        vector_normalized(
                                                            signed_destination * signed_source,
                                                            modulus * modulus,
                                                        ),
                                                        modulus,
                                                    )
                                                } else {
                                                    if kind == Some(VectorIntegerMultiplyHighSignedUnsigned) then {
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
    vector_semantics(operation).integer_reduction != None()

function vector_integer_reduction_identity(operation : Semantic_operation, element_bytes : int) -> int = {
    let modulus : int = width_modulus(element_bytes);
    let sign : int = tdiv_int(modulus, 2);
    let kind = vector_semantics(operation).integer_reduction;
    if kind == Some(VectorReduceAnd) | kind == Some(VectorReduceMinimumUnsigned) then {
        modulus - 1
    } else {
        if kind == Some(VectorReduceMinimumSigned) then {
            sign - 1
        } else {
            if kind == Some(VectorReduceMaximumSigned) then { sign } else { 0 }
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
    let kind = vector_semantics(operation).integer_reduction;
    if kind == Some(VectorReduceAdd) then {
        tmod_int(accumulator + value, modulus)
    } else {
        if kind == Some(VectorReduceAnd) then {
            unsigned(bits_from_int(accumulator) & bits_from_int(value))
        } else {
            if kind == Some(VectorReduceOr) then {
                unsigned(bits_from_int(accumulator) | bits_from_int(value))
            } else {
                if kind == Some(VectorReduceXor) then {
                    unsigned(xor_vec(bits_from_int(accumulator), bits_from_int(value)))
                } else {
                    if kind == Some(VectorReduceMinimumSigned) then {
                        vector_normalized(
                            if vector_signed_lane(accumulator, element_bytes) < vector_signed_lane(value, element_bytes)
                            then vector_signed_lane(accumulator, element_bytes)
                            else vector_signed_lane(value, element_bytes),
                            modulus,
                        )
                    } else {
                        if kind == Some(VectorReduceMinimumUnsigned) then {
                            if accumulator < value then { accumulator } else { value }
                        } else {
                            if kind == Some(VectorReduceMaximumSigned) then {
                                vector_normalized(
                                    if vector_signed_lane(accumulator, element_bytes) >
                                        vector_signed_lane(value, element_bytes)
                                    then vector_signed_lane(accumulator, element_bytes)
                                    else vector_signed_lane(value, element_bytes),
                                    modulus,
                                )
                            } else {
                                if kind == Some(VectorReduceMaximumUnsigned) then {
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
    let kind = vector_semantics(operation).integer_unary;
    if kind == Some(VectorUnaryNegate) then {
        vector_normalized(-value, modulus)
    } else {
        if kind == Some(VectorUnaryAbsolute) then {
            let signed_value = vector_signed_lane(value, element_bytes);
            vector_normalized(if signed_value < 0 then -signed_value else signed_value, modulus)
        } else {
            if kind == Some(VectorUnaryNot) then {
                unsigned(xor_vec(image, width_mask(element_bytes)))
            } else {
                if kind == Some(VectorUnaryCountLeadingZeros) then {
                    count_from_high(image, bits, bitzero)
                } else {
                    if kind == Some(VectorUnaryCountTrailingZeros) then {
                        count_from_low(image, 0, bits, bitzero)
                    } else {
                        if kind == Some(VectorUnaryCountLeadingSign) then {
                            count_from_high(image, bits, bitone)
                        } else {
                            if kind == Some(VectorUnaryCountTrailingSign) then {
                                count_from_low(image, 0, bits, bitone)
                            } else {
                                if kind == Some(VectorUnaryPopulationCount) then {
                                    bit_count_from(image, 0, bits)
                                } else {
                                    if kind == Some(VectorUnaryReverseBytes) then {
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
