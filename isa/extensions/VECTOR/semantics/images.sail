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

function vector_low_bytes(bytes : list(bits(8)), count : int) -> list(bits(8)) =
    if count <= 0 then [||]
    else match bytes {
        [||] => [||],
        head :: tail => head :: vector_low_bytes(tail, count - 1),
    }

function vector_replace_low_bytes(
    destination : list(bits(8)), source : list(bits(8)), count : int,
) -> list(bits(8)) =
    if count <= 0 then destination
    else match (destination, source) {
        (_destination_head :: destination_tail, source_head :: source_tail) =>
            source_head :: vector_replace_low_bytes(destination_tail, source_tail, count - 1),
        _ => destination,
    }

function vector_zero_low_bytes(image : list(bits(8)), count : int) -> list(bits(8)) =
    vector_replace_low_bytes(image, zero_vector_bytes(count), count)

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
    remaining : int,
) -> (
    list(bits(8))
) =
    if remaining <= 0 then [||]
    else match (left, right) {
        (left_head :: left_tail, right_head :: right_tail) => (match vector_semantics(operation).predicate_binary {
            Some(PredicateBinaryAnd) => (left_head & right_head),
            Some(PredicateBinaryOr) => (left_head | right_head),
            _ => xor_vec(left_head, right_head),
        }) ::
            predicate_raw_binary(left_tail, right_tail, operation, remaining - 1),
        _ => [||],
    }

function predicate_raw_not(image : list(bits(8)), remaining : int) -> list(bits(8)) =
    if remaining <= 0 then [||]
    else match image {
        [||] => [||],
        head :: tail => xor_vec(head, 0xFF) :: predicate_raw_not(tail, remaining - 1),
    }

function predicate_raw_select(
    select : list(bits(8)),
    source : list(bits(8)),
    destination : list(bits(8)),
    remaining : int,
) -> (
    list(bits(8))
) =
    if remaining <= 0 then [||]
    else match (select, source, destination) {
        (select_head :: select_tail, source_head :: source_tail, destination_head :: destination_tail) => ((destination_head &
            xor_vec(select_head, 0xFF)) |
            (source_head & select_head)) ::
            predicate_raw_select(select_tail, source_tail, destination_tail, remaining - 1),
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
