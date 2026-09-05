function predicate_pair_lane(
    operation : Semantic_operation,
    left : list(bits(8)),
    right : list(bits(8)),
    output_lane : int,
    lanes : int,
    element_bytes : int,
) -> (
    bool
) = {
    let kind = vector_semantics(operation).predicate_pair;
    if kind == Some(PredicateZipLow) | kind == Some(PredicateZipHigh) then {
        let base = if kind == Some(PredicateZipHigh) then {
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
        if kind == Some(PredicateUnzipLow) | kind == Some(PredicateUnzipHigh) then {
            let parity = if kind == Some(PredicateUnzipHigh) then { 1 } else { 0 };
            if output_lane < tdiv_int(lanes, 2) then {
                predicate_bit(left, (2 * output_lane + parity) * element_bytes)
            } else {
                predicate_bit(right, (2 * (output_lane - tdiv_int(lanes, 2)) + parity) * element_bytes)
            }
        } else {
            let parity = if kind == Some(PredicateTransposeHigh) then { 1 } else { 0 };
            let source_lane = 2 * tdiv_int(output_lane, 2) + parity;
            if tmod_int(output_lane, 2) == 0 then {
                predicate_bit(left, source_lane * element_bytes)
            } else {
                predicate_bit(right, source_lane * element_bytes)
            }
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
        let kind = vector_semantics(operation).predicate_slide;
        let selected = if kind == Some(PredicateSlideUp) then {
                if lane >= count then {
                    predicate_bit(destination, (lane - count) * element_bytes)
                } else {
                    false
                }
            } else {
                if kind == Some(PredicateSlideDown) then {
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

function predicate_any(image : list(bits(8)), remaining : int) -> bool =
    if remaining <= 0 then false
    else match image {
        [||] => false,
        head :: tail => head != 0x00 | predicate_any(tail, remaining - 1),
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
