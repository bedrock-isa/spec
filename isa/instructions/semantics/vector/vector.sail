function vector_byte_at(bytes : list(bits(8)), index : int) -> bits(8) = match bytes {
  [||] => 0x00,
  head :: tail => if index <= 0 then head else vector_byte_at(tail, index - 1),
}

function vector_replace_byte(bytes : list(bits(8)), index : int, value : bits(8))
  -> list(bits(8)) = match bytes {
  [||] => [||],
  head :: tail => if index <= 0 then value :: tail
                  else head :: vector_replace_byte(tail, index - 1, value),
}

function vector_power_of_two(exponent : int) -> int =
  if exponent <= 0 then 1 else 2 * vector_power_of_two(exponent - 1)

function predicate_bit(image : list(bits(8)), index : int) -> bool = {
  let byte = vector_byte_at(image, tdiv_int(index, 8));
  tmod_int(tdiv_int(unsigned(byte), vector_power_of_two(tmod_int(index, 8))), 2) == 1
}

function predicate_set_bit(image : list(bits(8)), index : int, selected : bool)
  -> list(bits(8)) = {
  let byte_index = tdiv_int(index, 8);
  let byte = unsigned(vector_byte_at(image, byte_index));
  let mask = vector_power_of_two(tmod_int(index, 8));
  let present = tmod_int(tdiv_int(byte, mask), 2) == 1;
  let updated = if selected then (if present then byte else byte + mask)
                else (if present then byte - mask else byte);
  vector_replace_byte(image, byte_index, get_slice_int(8, updated, 0))
}

function predicate_fill_typed(image : list(bits(8)), lane : int, lanes : int,
                              element_bytes : int, first : int, last : int)
  -> list(bits(8)) =
  if lane >= lanes then image
  else predicate_fill_typed(
    predicate_set_bit(image, lane * element_bytes, lane >= first & lane < last),
    lane + 1, lanes, element_bytes, first, last
  )

function predicate_raw_binary(left : list(bits(8)), right : list(bits(8)),
                              operation : Semantic_operation) -> list(bits(8)) =
  match (left, right) {
    (left_head :: left_tail, right_head :: right_tail) =>
      (if operation == Op_PAND then left_head & right_head
       else if operation == Op_POR then left_head | right_head
       else xor_vec(left_head, right_head))
      :: predicate_raw_binary(left_tail, right_tail, operation),
    _ => [||],
  }

function predicate_raw_not(image : list(bits(8))) -> list(bits(8)) = match image {
  [||] => [||],
  head :: tail => xor_vec(head, 0xFF) :: predicate_raw_not(tail),
}

function predicate_raw_select(select : list(bits(8)), source : list(bits(8)),
                              destination : list(bits(8))) -> list(bits(8)) =
  match (select, source, destination) {
    (select_head :: select_tail, source_head :: source_tail,
     destination_head :: destination_tail) =>
      ((destination_head & xor_vec(select_head, 0xFF)) | (source_head & select_head))
      :: predicate_raw_select(select_tail, source_tail, destination_tail),
    _ => [||],
  }

function vector_lane_unsigned_loop(bytes : list(bits(8)), base : int, remaining : int,
                                   scale : int, accumulated : int) -> int =
  if remaining <= 0 then accumulated
  else vector_lane_unsigned_loop(
    bytes, base + 1, remaining - 1, scale * 256,
    accumulated + unsigned(vector_byte_at(bytes, base)) * scale
  )

function vector_lane_unsigned(bytes : list(bits(8)), lane : int, element_bytes : int) -> int =
  vector_lane_unsigned_loop(bytes, lane * element_bytes, element_bytes, 1, 0)

function vector_write_lane_loop(image : list(bits(8)), base : int, index : int,
                                element_bytes : int, value : int, scale : int)
  -> list(bits(8)) =
  if index >= element_bytes then image
  else vector_write_lane_loop(
    vector_replace_byte(image, base + index,
                        get_slice_int(8, tmod_int(tdiv_int(value, scale), 256), 0)),
    base, index + 1, element_bytes, value, scale * 256
  )

function vector_write_lane(image : list(bits(8)), lane : int,
                           element_bytes : int, value : int) -> list(bits(8)) =
  vector_write_lane_loop(image, lane * element_bytes, 0, element_bytes, value, 1)

function vector_merge_image(destination : list(bits(8)), source : list(bits(8)),
                            predicate : list(bits(8)), lane : int, lanes : int,
                            element_bytes : int) -> list(bits(8)) =
  if lane >= lanes then destination
  else vector_merge_image(
    if predicate_bit(predicate, lane * element_bytes)
    then vector_write_lane(destination, lane, element_bytes,
                           vector_lane_unsigned(source, lane, element_bytes))
    else destination,
    source, predicate, lane + 1, lanes, element_bytes
  )

function vector_duplicate_image(image : list(bits(8)), lane : int, lanes : int,
                                element_bytes : int, value : int) -> list(bits(8)) =
  if lane >= lanes then image
  else vector_duplicate_image(
    vector_write_lane(image, lane, element_bytes, value),
    lane + 1, lanes, element_bytes, value
  )

function vector_index_image(image : list(bits(8)), lane : int, lanes : int,
                            element_bytes : int) -> list(bits(8)) =
  if lane >= lanes then image
  else vector_index_image(
    vector_write_lane(image, lane, element_bytes, lane),
    lane + 1, lanes, element_bytes
  )

function vector_normalized(value : int, modulus : int) -> int =
  tmod_int(tmod_int(value, modulus) + modulus, modulus)

function vector_signed_lane(value : int, element_bytes : int) -> int = {
  let modulus = width_modulus(element_bytes);
  let sign = tdiv_int(modulus, 2);
  if value >= sign then value - modulus else value
}

function vector_integer_binary_value(operation : Semantic_operation,
                                     destination : int, source : int,
                                     element_bytes : int) -> int = {
  let modulus = width_modulus(element_bytes);
  let bits = element_bytes * 8;
  let signed_destination = vector_signed_lane(destination, element_bytes);
  let signed_source = vector_signed_lane(source, element_bytes);
  if operation == Op_VADD then vector_normalized(destination + source, modulus)
  else if operation == Op_VSUB then vector_normalized(destination - source, modulus)
  else if operation == Op_VAND then unsigned(bits_from_int(destination) & bits_from_int(source))
  else if operation == Op_VOR then unsigned(bits_from_int(destination) | bits_from_int(source))
  else if operation == Op_VXOR then unsigned(xor_vec(bits_from_int(destination), bits_from_int(source)))
  else if operation == Op_VMINS then
    vector_normalized(if signed_destination < signed_source then signed_destination else signed_source,
                      modulus)
  else if operation == Op_VMINU then if destination < source then destination else source
  else if operation == Op_VMAXS then
    vector_normalized(if signed_destination > signed_source then signed_destination else signed_source,
                      modulus)
  else if operation == Op_VMAXU then if destination > source then destination else source
  else if operation == Op_VMUL then tmod_int(destination * source, modulus)
  else if operation == Op_VMULHU then tdiv_int(destination * source, modulus)
  else if operation == Op_VMULHS then
    tdiv_int(vector_normalized(signed_destination * signed_source, modulus * modulus), modulus)
  else if operation == Op_VMULHSU then
    tdiv_int(vector_normalized(signed_destination * source, modulus * modulus), modulus)
  else 0
}

function vector_integer_binary_image(operation : Semantic_operation,
                                     destination : list(bits(8)), source : list(bits(8)),
                                     predicate : list(bits(8)), lane : int, lanes : int,
                                     element_bytes : int) -> list(bits(8)) =
  if lane >= lanes then destination
  else vector_integer_binary_image(
    operation,
    if predicate_bit(predicate, lane * element_bytes) then vector_write_lane(
      destination, lane, element_bytes,
      vector_integer_binary_value(
        operation, vector_lane_unsigned(destination, lane, element_bytes),
        vector_lane_unsigned(source, lane, element_bytes), element_bytes
      )
    ) else destination,
    source, predicate, lane + 1, lanes, element_bytes
  )

function vector_integer_reduction_operation(operation : Semantic_operation) -> bool =
  operation == Op_VREDADD | operation == Op_VREDMINS | operation == Op_VREDMINU
  | operation == Op_VREDMAXS | operation == Op_VREDMAXU | operation == Op_VREDAND
  | operation == Op_VREDOR | operation == Op_VREDXOR

function vector_integer_reduction_identity(operation : Semantic_operation,
                                           element_bytes : int) -> int = {
  let modulus : int = width_modulus(element_bytes);
  let sign : int = tdiv_int(modulus, 2);
  if operation == Op_VREDAND | operation == Op_VREDMINU then modulus - 1
  else if operation == Op_VREDMINS then sign - 1
  else if operation == Op_VREDMAXS then sign
  else 0
}

function vector_integer_reduction_value(operation : Semantic_operation,
                                        accumulator : int, value : int,
                                        element_bytes : int) -> int = {
  let modulus : int = width_modulus(element_bytes);
  if operation == Op_VREDADD then tmod_int(accumulator + value, modulus)
  else if operation == Op_VREDAND then
    unsigned(bits_from_int(accumulator) & bits_from_int(value))
  else if operation == Op_VREDOR then
    unsigned(bits_from_int(accumulator) | bits_from_int(value))
  else if operation == Op_VREDXOR then
    unsigned(xor_vec(bits_from_int(accumulator), bits_from_int(value)))
  else if operation == Op_VREDMINS then vector_normalized(
    if vector_signed_lane(accumulator, element_bytes) < vector_signed_lane(value, element_bytes)
    then vector_signed_lane(accumulator, element_bytes) else vector_signed_lane(value, element_bytes),
    modulus
  )
  else if operation == Op_VREDMINU then if accumulator < value then accumulator else value
  else if operation == Op_VREDMAXS then vector_normalized(
    if vector_signed_lane(accumulator, element_bytes) > vector_signed_lane(value, element_bytes)
    then vector_signed_lane(accumulator, element_bytes) else vector_signed_lane(value, element_bytes),
    modulus
  )
  else if operation == Op_VREDMAXU then if accumulator > value then accumulator else value
  else 0
}

function vector_integer_reduction_image(operation : Semantic_operation,
                                        source : list(bits(8)),
                                        predicate : list(bits(8)), lane : int,
                                        lanes : int, element_bytes : int,
                                        accumulator : int) -> int =
  if lane >= lanes then accumulator
  else vector_integer_reduction_image(
    operation, source, predicate, lane + 1, lanes, element_bytes,
    if predicate_bit(predicate, lane * element_bytes) then vector_integer_reduction_value(
      operation, accumulator, vector_lane_unsigned(source, lane, element_bytes), element_bytes
    ) else accumulator
  )

function vector_integer_unary_value(operation : Semantic_operation,
                                    value : int, element_bytes : int) -> int = {
  let modulus = width_modulus(element_bytes);
  let bits = element_bytes * 8;
  let image = bits_from_int(value) & width_mask(element_bytes);
  if operation == Op_VNEG then vector_normalized(-value, modulus)
  else if operation == Op_VABS then {
    let signed_value = vector_signed_lane(value, element_bytes);
    vector_normalized(if signed_value < 0 then -signed_value else signed_value, modulus)
  }
  else if operation == Op_VNOT then unsigned(xor_vec(image, width_mask(element_bytes)))
  else if operation == Op_VCLZ then count_from_high(image, bits, bitzero)
  else if operation == Op_VCTZ then count_from_low(image, 0, bits, bitzero)
  else if operation == Op_VCLS then count_from_high(image, bits, bitone)
  else if operation == Op_VCTS then count_from_low(image, 0, bits, bitone)
  else if operation == Op_VPOPCNT then bit_count_from(image, 0, bits)
  else if operation == Op_VREVBYTE then unsigned(reverse_bytes(image, element_bytes))
  else 0
}

function vector_integer_unary_image(operation : Semantic_operation,
                                    destination : list(bits(8)), predicate : list(bits(8)),
                                    lane : int, lanes : int, element_bytes : int)
  -> list(bits(8)) =
  if lane >= lanes then destination
  else vector_integer_unary_image(
    operation,
    if predicate_bit(predicate, lane * element_bytes) then vector_write_lane(
      destination, lane, element_bytes,
      vector_integer_unary_value(
        operation, vector_lane_unsigned(destination, lane, element_bytes), element_bytes
      )
    ) else destination,
    predicate, lane + 1, lanes, element_bytes
  )

function vector_integer_unary_source_image(operation : Semantic_operation,
                                           destination : list(bits(8)),
                                           source : list(bits(8)),
                                           predicate : list(bits(8)), lane : int,
                                           lanes : int, element_bytes : int)
  -> list(bits(8)) =
  if lane >= lanes then destination
  else vector_integer_unary_source_image(
    operation,
    if predicate_bit(predicate, lane * element_bytes) then vector_write_lane(
      destination, lane, element_bytes,
      vector_integer_unary_value(
        operation, vector_lane_unsigned(source, lane, element_bytes), element_bytes
      )
    ) else destination,
    source, predicate, lane + 1, lanes, element_bytes
  )

function vector_shift_operation(operation : Semantic_operation) -> Semantic_operation =
  if operation == Op_VSHL then Op_SHL
  else if operation == Op_VSHR then Op_SHR
  else if operation == Op_VSAR then Op_SAR
  else if operation == Op_VROL then Op_ROL
  else Op_ROR

function vector_shift_image(operation : Semantic_operation,
                            destination : list(bits(8)), counts : list(bits(8)),
                            scalar_count : int, vector_counts : bool,
                            predicate : list(bits(8)), lane : int, lanes : int,
                            element_bytes : int) -> list(bits(8)) =
  if lane >= lanes then destination
  else {
    let count = if vector_counts then vector_lane_unsigned(counts, lane, element_bytes)
                else scalar_count;
    let old = get_slice_int(64, vector_lane_unsigned(destination, lane, element_bytes), 0);
    let shifted = shift_result(vector_shift_operation(operation), old,
                               get_slice_int(64, count, 0), element_bytes);
    vector_shift_image(
      operation,
      if predicate_bit(predicate, lane * element_bytes)
      then vector_write_lane(destination, lane, element_bytes, unsigned(shifted))
      else destination,
      counts, scalar_count, vector_counts, predicate, lane + 1, lanes, element_bytes
    )
  }

function vector_integer_condition(condition : int, left : int, right : int,
                                  element_bytes : int) -> bool =
  if condition == 2 then left == right
  else if condition == 3 then left != right
  else if condition == 4 then left < right
  else if condition == 5 then left >= right
  else if condition == 10 then left <= right
  else if condition == 11 then left > right
  else if condition == 12 then vector_signed_lane(left, element_bytes)
                                    < vector_signed_lane(right, element_bytes)
  else if condition == 13 then vector_signed_lane(left, element_bytes)
                                    >= vector_signed_lane(right, element_bytes)
  else if condition == 14 then vector_signed_lane(left, element_bytes)
                                    <= vector_signed_lane(right, element_bytes)
  else if condition == 15 then vector_signed_lane(left, element_bytes)
                                    > vector_signed_lane(right, element_bytes)
  else { assert(false); false }

function vector_integer_compare_image(operation : Semantic_operation, condition : int,
                                      left : list(bits(8)), right : list(bits(8)),
                                      govern : list(bits(8)), image : list(bits(8)),
                                      lane : int, lanes : int, element_bytes : int)
  -> list(bits(8)) =
  if lane >= lanes then image
  else {
    let lhs = vector_lane_unsigned(left, lane, element_bytes);
    let rhs = vector_lane_unsigned(right, lane, element_bytes);
    let selected = if not_bool(predicate_bit(govern, lane * element_bytes)) then false
      else if operation == Op_VCMPcc then vector_integer_condition(condition, lhs, rhs, element_bytes)
      else if operation == Op_VTESTZ then unsigned(bits_from_int(lhs) & bits_from_int(rhs)) == 0
      else unsigned(bits_from_int(lhs) & bits_from_int(rhs)) != 0;
    vector_integer_compare_image(
      operation, condition, left, right, govern,
      predicate_set_bit(image, lane * element_bytes, selected),
      lane + 1, lanes, element_bytes
    )
  }

function vector_width_change_destination_bytes(operation : Semantic_operation) -> int =
  if operation == Op_VEXTZW | operation == Op_VEXTSW | operation == Op_VTRUNCW then 2
  else if operation == Op_VEXTZL | operation == Op_VEXTSL | operation == Op_VTRUNCL then 4
  else if operation == Op_VEXTZQ | operation == Op_VEXTSQ then 8
  else 1

function vector_write_at_base(image : list(bits(8)), base : int, index : int,
                              width : int, value : int, scale : int)
  -> list(bits(8)) =
  if index >= width then image
  else vector_write_at_base(
    vector_replace_byte(image, base + index,
      get_slice_int(8, tmod_int(tdiv_int(value, scale), 256), 0)),
    base, index + 1, width, value, scale * 256
  )

function vector_width_change_image(operation : Semantic_operation,
                                   destination : list(bits(8)),
                                   source : list(bits(8)),
                                   predicate : list(bits(8)),
                                   container : int, containers : int,
                                   source_bytes : int, destination_bytes : int)
  -> list(bits(8)) =
  if container >= containers then destination
  else {
    let base = container * (if source_bytes > destination_bytes
                            then source_bytes else destination_bytes);
    let source_value = vector_lane_unsigned_loop(source, base, source_bytes, 1, 0);
    let result = if operation == Op_VEXTSW | operation == Op_VEXTSL
                    | operation == Op_VEXTSQ then
      vector_normalized(vector_signed_lane(source_value, source_bytes),
                        width_modulus(destination_bytes))
      else source_value;
    vector_width_change_image(
      operation,
      if predicate_bit(predicate, base)
      then vector_write_at_base(destination, base, 0, destination_bytes, result, 1)
      else destination,
      source, predicate, container + 1, containers, source_bytes, destination_bytes
    )
  }

function vector_permute_value(operation : Semantic_operation,
                              destination : list(bits(8)), source : list(bits(8)),
                              lane : int, lanes : int, element_bytes : int,
                              count : int) -> int =
  if operation == Op_VPERM then {
    let index = vector_lane_unsigned(source, lane, element_bytes);
    if index < lanes then vector_lane_unsigned(destination, index, element_bytes) else 0
  }
  else if operation == Op_VSLIDEUP then
    if lane >= count then vector_lane_unsigned(destination, lane - count, element_bytes) else 0
  else if operation == Op_VSLIDEDN then
    if lane + count < lanes
    then vector_lane_unsigned(destination, lane + count, element_bytes) else 0
  else if operation == Op_VSLICE then {
    let index = lane + count;
    if index < lanes then vector_lane_unsigned(destination, index, element_bytes)
    else if index < 2 * lanes then vector_lane_unsigned(source, index - lanes, element_bytes)
    else 0
  }
  else if operation == Op_VZIPLO | operation == Op_VZIPHI then {
    let base = if operation == Op_VZIPHI then tdiv_int(lanes, 2) else 0;
    let index = base + tdiv_int(lane, 2);
    if tmod_int(lane, 2) == 0
    then vector_lane_unsigned(destination, index, element_bytes)
    else vector_lane_unsigned(source, index, element_bytes)
  }
  else if operation == Op_VUZIPLO | operation == Op_VUZIPHI then {
    let parity = if operation == Op_VUZIPHI then 1 else 0;
    if lane < tdiv_int(lanes, 2)
    then vector_lane_unsigned(destination, 2 * lane + parity, element_bytes)
    else vector_lane_unsigned(source,
      2 * (lane - tdiv_int(lanes, 2)) + parity, element_bytes)
  }
  else {
    let parity = if operation == Op_VTRNHI then 1 else 0;
    let index = 2 * tdiv_int(lane, 2) + parity;
    if tmod_int(lane, 2) == 0
    then vector_lane_unsigned(destination, index, element_bytes)
    else vector_lane_unsigned(source, index, element_bytes)
  }

function vector_permute_image(operation : Semantic_operation,
                              original : list(bits(8)), source : list(bits(8)),
                              image : list(bits(8)), predicate : list(bits(8)),
                              lane : int, lanes : int, element_bytes : int,
                              count : int) -> list(bits(8)) =
  if lane >= lanes then image
  else vector_permute_image(
    operation, original, source,
    if predicate_bit(predicate, lane * element_bytes)
    then vector_write_lane(image, lane, element_bytes,
      vector_permute_value(operation, original, source, lane, lanes, element_bytes, count))
    else image,
    predicate, lane + 1, lanes, element_bytes, count
  )

function predicate_pair_lane(operation : Semantic_operation, left : list(bits(8)),
                             right : list(bits(8)), output_lane : int,
                             lanes : int, element_bytes : int) -> bool =
  if operation == Op_PZIPLO | operation == Op_PZIPHI then {
    let base = if operation == Op_PZIPHI then tdiv_int(lanes, 2) else 0;
    let source_lane = base + tdiv_int(output_lane, 2);
    if tmod_int(output_lane, 2) == 0
    then predicate_bit(left, source_lane * element_bytes)
    else predicate_bit(right, source_lane * element_bytes)
  }
  else if operation == Op_PUZIPLO | operation == Op_PUZIPHI then {
    let parity = if operation == Op_PUZIPHI then 1 else 0;
    if output_lane < tdiv_int(lanes, 2)
    then predicate_bit(left, (2 * output_lane + parity) * element_bytes)
    else predicate_bit(right,
      (2 * (output_lane - tdiv_int(lanes, 2)) + parity) * element_bytes)
  }
  else {
    let parity = if operation == Op_PTRNHI then 1 else 0;
    let source_lane = 2 * tdiv_int(output_lane, 2) + parity;
    if tmod_int(output_lane, 2) == 0
    then predicate_bit(left, source_lane * element_bytes)
    else predicate_bit(right, source_lane * element_bytes)
  }

function predicate_pair_image(operation : Semantic_operation, left : list(bits(8)),
                              right : list(bits(8)), image : list(bits(8)),
                              lane : int, lanes : int, element_bytes : int)
  -> list(bits(8)) =
  if lane >= lanes then image
  else predicate_pair_image(
    operation, left, right,
    predicate_set_bit(
      image, lane * element_bytes,
      predicate_pair_lane(operation, left, right, lane, lanes, element_bytes)
    ), lane + 1, lanes, element_bytes
  )

function predicate_unpack_image(source : list(bits(8)), image : list(bits(8)),
                                 lane : int, lanes : int, element_bytes : int,
                                 high : bool) -> list(bits(8)) =
  if lane >= tdiv_int(lanes, 2) then image
  else {
    let source_lane = lane + (if high then tdiv_int(lanes, 2) else 0);
    predicate_unpack_image(
      source,
      predicate_set_bit(image, lane * element_bytes * 2,
                        predicate_bit(source, source_lane * element_bytes)),
      lane + 1, lanes, element_bytes, high
    )
  }

function predicate_pack_image(source : list(bits(8)), image : list(bits(8)),
                               lane : int, lanes : int, element_bytes : int,
                               high : bool) -> list(bits(8)) =
  if lane >= lanes then image
  else {
    let destination_bytes = tdiv_int(element_bytes, 2);
    let destination_lane = lane + (if high then lanes else 0);
    predicate_pack_image(
      source,
      predicate_set_bit(image, destination_lane * destination_bytes,
                        predicate_bit(source, lane * element_bytes)),
      lane + 1, lanes, element_bytes, high
    )
  }

function predicate_permute_image(source : list(bits(8)), indices : list(bits(8)),
                                  image : list(bits(8)), lane : int, lanes : int,
                                  element_bytes : int) -> list(bits(8)) =
  if lane >= lanes then image
  else {
    let index = vector_lane_unsigned(indices, lane, element_bytes);
    predicate_permute_image(
      source, indices,
      predicate_set_bit(image, lane * element_bytes,
        if index < lanes then predicate_bit(source, index * element_bytes) else false),
      lane + 1, lanes, element_bytes
    )
  }

function predicate_slide_image(operation : Semantic_operation,
                                destination : list(bits(8)), source : list(bits(8)),
                                image : list(bits(8)), lane : int, lanes : int,
                                element_bytes : int, count : int) -> list(bits(8)) =
  if lane >= lanes then image
  else {
    let selected = if operation == Op_PSLIDEUP then
        if lane >= count then predicate_bit(destination, (lane - count) * element_bytes)
        else false
      else if operation == Op_PSLIDEDN then
        if lane + count < lanes then predicate_bit(destination, (lane + count) * element_bytes)
        else false
      else {
        let index = lane + count;
        if index < lanes then predicate_bit(destination, index * element_bytes)
        else if index < 2 * lanes then predicate_bit(source, (index - lanes) * element_bytes)
        else false
      };
    predicate_slide_image(
      operation, destination, source,
      predicate_set_bit(image, lane * element_bytes, selected),
      lane + 1, lanes, element_bytes, count
    )
  }

function predicate_count(image : list(bits(8)), lane : int, lanes : int,
                         element_bytes : int, count : int) -> int =
  if lane >= lanes then count
  else predicate_count(image, lane + 1, lanes, element_bytes,
    count + (if predicate_bit(image, lane * element_bytes) then 1 else 0))

function predicate_first(image : list(bits(8)), lane : int, lanes : int,
                         element_bytes : int) -> int =
  if lane >= lanes then -1
  else if predicate_bit(image, lane * element_bytes) then lane
  else predicate_first(image, lane + 1, lanes, element_bytes)

function predicate_last(image : list(bits(8)), lane : int, element_bytes : int) -> int =
  if lane < 0 then -1
  else if predicate_bit(image, lane * element_bytes) then lane
  else predicate_last(image, lane - 1, element_bytes)

function predicate_any(image : list(bits(8))) -> bool = match image {
  [||] => false,
  head :: tail => head != 0x00 | predicate_any(tail),
}

function predicate_all_typed(image : list(bits(8)), lane : int, lanes : int,
                             element_bytes : int) -> bool =
  if lane >= lanes then true
  else predicate_bit(image, lane * element_bytes)
       & predicate_all_typed(image, lane + 1, lanes, element_bytes)

function predicate_register_index(instruction : Decoded_instruction, name : string)
  -> option(bits(4)) =
  match operand_named(instruction, name) {
    Some(operand) => Some(operand.value[3 .. 0]),
    None() => None(),
  }

function vector_register_index(instruction : Decoded_instruction, name : string)
  -> option(bits(5)) =
  match operand_named(instruction, name) {
    Some(operand) => Some(operand.value[4 .. 0]),
    None() => None(),
  }

function vector_finish(instruction : Decoded_instruction, before : Cpu_state,
                       after : Cpu_state) -> Execution_result = {
  var committed = after;
  committed.pc = next_pc(before, instruction);
  committed.vector_component_modified = true;
  completed(before, committed, CommitRegisters, [||])
}

function vector_operand_writes(name : string, operands : list(Decoded_operand)) -> bool =
  match operands {
    [||] => false,
    operand :: tail => if operand.name == name
      then operand.access == AccessWrite | operand.access == AccessReadWrite
      else vector_operand_writes(name, tail),
  }

function vector_memory_predicate(instruction : Decoded_instruction, state : Cpu_state)
  -> list(bits(8)) = match predicate_register_index(instruction, "govern") {
  Some(index) => state.predicate_registers[unsigned(index)],
  None() => zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8)),
}

function vector_fp_basic_operation(operation : Semantic_operation) -> bool =
  operation == Op_VADD | operation == Op_VSUB | operation == Op_VMUL
  | operation == Op_VNEG | operation == Op_VABS | operation == Op_VMIN
  | operation == Op_VMAX | operation == Op_VDIV | operation == Op_VMADD
  | operation == Op_VMSUB | operation == Op_VNMADD | operation == Op_VNMSUB
  | operation == Op_VSQRT | operation == Op_VCOPYSIGN | operation == Op_VROUND
  | operation == Op_VTRUNC | operation == Op_VFLOOR | operation == Op_VCEIL
  | operation == Op_VCLASS | operation == Op_VCMPcc

function vector_fp_convert_operation(operation : Semantic_operation) -> bool =
  operation == Op_VCVTH | operation == Op_VCVTUH | operation == Op_VCVTS
  | operation == Op_VCVTUS | operation == Op_VCVTD | operation == Op_VCVTUD
  | operation == Op_VCVTL | operation == Op_VCVTUL | operation == Op_VCVTQ
  | operation == Op_VCVTUQ

function vector_reduce_operation(operation : Semantic_operation) -> bool =
  operation == Op_VREDADD | operation == Op_VREDMINS
  | operation == Op_VREDMINU | operation == Op_VREDMAXS | operation == Op_VREDMAXU
  | operation == Op_VREDAND | operation == Op_VREDOR | operation == Op_VREDXOR
  | operation == Op_VREDMIN | operation == Op_VREDMAX

function vector_fp_compute_operation(operation : Semantic_operation) -> bool =
  vector_fp_basic_operation(operation)
  | vector_fp_convert_operation(operation)
  | vector_reduce_operation(operation)

function vector_writable_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail =>
      if operand.access == AccessWrite | operand.access == AccessReadWrite then Some(operand)
      else vector_writable_operand(tail),
  }

function vector_fp_payload(operands : list(Decoded_operand), state : Cpu_state,
                           memory : list(bits(8))) -> list(bits(8)) = match operands {
  [||] => [||],
  operand :: tail => {
    let rest = vector_fp_payload(tail, state, memory);
    if operand.type_name == "Vn" then append_bytes(
      state.vector_registers[unsigned(operand.value[4 .. 0])], rest
    )
    else if operand.type_name == "VEA" then append_bytes(memory, rest)
    else rest
  },
}

function vector_fp_result_length(instruction : Decoded_instruction,
                                 state : Cpu_state) -> int =
  match vector_writable_operand(instruction.operands) {
    Some(operand) => if operand.type_name == "Vn" | operand.type_name == "VEA"
      then state.vector_length_bytes
      else if operand.type_name == "Pn" then tdiv_int(state.vector_length_bytes, 8)
      else 8,
    None() => 0,
  }

function vector_fp_allowed_causes(operation : Semantic_operation) -> bits(5) =
  if operation == Op_VCOPYSIGN | operation == Op_VCLASS
     | operation == Op_VREDAND | operation == Op_VREDOR | operation == Op_VREDXOR
     | operation == Op_VREDMINS | operation == Op_VREDMINU
     | operation == Op_VREDMAXS | operation == Op_VREDMAXU then fflags_none
  else if operation == Op_VMIN | operation == Op_VMAX | operation == Op_VCMPcc
          | operation == Op_VREDMIN | operation == Op_VREDMAX then fflags_nv
  else if operation == Op_VROUND | operation == Op_VTRUNC
          | operation == Op_VFLOOR | operation == Op_VCEIL then fflags_nv | fflags_nx
  else if operation == Op_VDIV then fflags_all
  else 0b10111

function vector_fp_request(instruction : Decoded_instruction, state : Cpu_state,
                           memory : list(bits(8))) -> Primitive_request = {
  let selector : bits(64) = match condition_size_field(instruction.fields) {
    Some(value) => get_slice_int(64, value, 0), None() => 0x0000000000000000,
  };
  let condition : bits(64) = match operand_named(instruction, "cc") {
    Some(value) => value.value, None() => 0x0000000000000000,
  };
  let predicate : list(bits(8)) = vector_memory_predicate(instruction, state);
  { empty_primitive_request() with
    kind = VectorFloatingPointRequest, role = instruction.form.form_id,
    width = operation_width(instruction), commit_point = false,
    selector = selector, expected = state.fstatus, auxiliary = condition,
    body_length = vector_fp_result_length(instruction, state),
    payload_bytes = append_bytes(
      predicate, vector_fp_payload(instruction.operands, state, memory)
    ), state_image = state }
}

function vector_fp_waiting(instruction : Decoded_instruction, before : Cpu_state,
                           after : Cpu_state, phase : Continuation_phase,
                           request : Primitive_request, memory : list(bits(8)))
  -> Execution_result = struct {
  state = before,
  pending = { empty_pending(before, after, instruction.form.operation, CommitRegisters) with
    instruction = Some(instruction), phase = phase, vector_payload0 = memory },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

function execute_vector_fp_bridge(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  if not_bool(vector_instruction_requires_fp(instruction)) then None()
  else if operation == Op_VDUP then match
    (floating_value_named(instruction, state, "src"),
     vector_register_index(instruction, "dst")) {
    (Some(source), Some(destination)) => {
      let element_bytes = operation_width(instruction);
      var updated = advance_pc(state, instruction);
      updated.vector_registers[unsigned(destination)] = vector_duplicate_image(
        zero_vector_bytes(state.vector_length_bytes), 0,
        tdiv_int(state.vector_length_bytes, element_bytes), element_bytes, unsigned(source)
      );
      updated.vector_component_modified = true;
      Some(completed(state, updated, CommitRegisters, [||]))
    }, _ => None(),
  }
  else if operation == Op_VEXTRACT then match
    (vector_register_index(instruction, "src"), value_named(instruction, state, "index"),
     operand_named(instruction, "dst")) {
    (Some(source), Some(index_bits), Some(destination)) => {
      let element_bytes = operation_width(instruction);
      let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
      let index = unsigned(index_bits);
      if index >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "VEXTRACT lane index exceeds the lane count",
        0x0000000000000001
      ))
      else {
        var updated = advance_pc(state, instruction);
        updated.floating_registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
          64, vector_lane_unsigned(state.vector_registers[unsigned(source)], index, element_bytes), 0
        );
        updated.fp_component_modified = true;
        Some(completed(state, updated, CommitRegisters, [||]))
      }
    }, _ => None(),
  }
  else if operation == Op_VINSERT then match
    (floating_value_named(instruction, state, "src"), value_named(instruction, state, "index"),
     vector_register_index(instruction, "dst")) {
    (Some(source), Some(index_bits), Some(destination)) => {
      let element_bytes = operation_width(instruction);
      let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
      let index = unsigned(index_bits);
      if index >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "VINSERT lane index exceeds the lane count",
        0x0000000000000001
      ))
      else {
        var updated = advance_pc(state, instruction);
        updated.vector_registers[unsigned(destination)] = vector_write_lane(
          state.vector_registers[unsigned(destination)], index, element_bytes, unsigned(source)
        );
        updated.vector_component_modified = true;
        Some(completed(state, updated, CommitRegisters, [||]))
      }
    }, _ => None(),
  }
  else None()
}

function vector_memory_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail => match operand.ea {
      Some(_) => Some(operand), None() => vector_memory_operand(tail),
    },
  }

function vector_memory_stride(instruction : Decoded_instruction, state : Cpu_state,
                              element_bytes : int) -> (bool, bits(64)) =
  match vector_memory_operand(instruction.operands) {
    None() => (false, get_slice_int(64, element_bytes, 0)),
    Some(operand) => match operand.ea {
      None() => (false, get_slice_int(64, element_bytes, 0)),
      Some(ea) => if ea.descriptor_name == "vector_stride_descriptor" then
        match ea_field_role("stride", ea.fields) {
          Some(index) => (true, image_register(state, index)),
          None() => (true, 0x0000000000000000),
        }
      else (false, get_slice_int(64, element_bytes, 0)),
    },
  }

function vector_memory_request(kind : Primitive_request_kind,
                               instruction : Decoded_instruction,
                               state : Cpu_state, evaluation : Ea_evaluation,
                               predicate : list(bits(8)), values : list(bits(8)),
                               element_bytes : int, access : Transaction_access)
  -> Primitive_request = {
  let (strided, stride) = vector_memory_stride(instruction, state, element_bytes);
  let length = if instruction.form.operation == Op_PMOV
               then tdiv_int(state.vector_length_bytes, 8)
               else state.vector_length_bytes;
  struct {
    kind = kind, ordinal = 0, role = evaluation.role, domain = evaluation.domain,
    segment = evaluation.segment, segment_image = evaluation.segment_image,
    width = element_bytes, range_start = evaluation.effective_address,
    range_end = add_bits(evaluation.effective_address, get_slice_int(64, length, 0)),
    range_length = length,
    range_wrap = unsigned(evaluation.effective_address) + length > 18446744073709551616,
    range_end_at_modulus = unsigned(evaluation.effective_address) + length
                           == 18446744073709551616,
    effective_address = evaluation.effective_address,
    linear_address = evaluation.linear_address, access = access,
    value = 0x0000000000000000, address_translation = true, commit_point = true,
    memory_order = 0, cache_policy = 0, suppress_fault = false,
    staged_updates = evaluation.staged_updates,
    selector = if strided then 0x0000000000000001 else 0x0000000000000000,
    expected = 0x0000000000000000, desired = 0x0000000000000000,
    auxiliary = stride, body_length = length,
    payload_bytes = append_bytes(predicate, values), fp_request = empty_fp_request(),
    state_image = state
  }
}

function vector_memory_waiting(instruction : Decoded_instruction, before : Cpu_state,
                               after : Cpu_state, phase : Continuation_phase,
                               request : Primitive_request) -> Execution_result = struct {
  state = before,
  pending = { empty_pending(before, after, instruction.form.operation, CommitMemory) with
    instruction = Some(instruction), phase = phase },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

function start_vector_fp_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  if not_bool(vector_instruction_requires_fp(instruction)
              & vector_fp_compute_operation(operation)) then None()
  else match vector_memory_operand(instruction.operands) {
    None() => Some(vector_fp_waiting(
      instruction, state, advance_pc(state, instruction), PhaseVectorFpCompute,
      vector_fp_request(instruction, state, [||]), [||]
    )),
    Some(memory_operand) => match evaluate_vector_instruction_ea(
      instruction.operands, state, state.pc, operation_width(instruction)
    ) {
      None() => Some(faulted(state, operation, InvalidControlState,
                             "missing vector FP memory address")),
      Some((evaluation, evaluated_state)) => {
        let memory_destination = vector_operand_writes(
          memory_operand.name, instruction.operands
        );
        Some(vector_fp_waiting(
          instruction, state, advance_pc(evaluated_state, instruction),
          PhaseVectorFpMemoryRead,
          vector_memory_request(
            VectorMemoryRead, instruction, state, evaluation,
            vector_memory_predicate(instruction, state), [||],
            operation_width(instruction),
            if memory_destination then AccessReadModifyWrite else AccessLoad
          ), [||]
        ))
      },
    },
  }
}

function vector_integer_binary_operation(operation : Semantic_operation) -> bool =
  operation == Op_VADD | operation == Op_VSUB | operation == Op_VAND
  | operation == Op_VOR | operation == Op_VXOR | operation == Op_VMINS
  | operation == Op_VMINU | operation == Op_VMAXS | operation == Op_VMAXU
  | operation == Op_VMUL | operation == Op_VMULHS | operation == Op_VMULHU
  | operation == Op_VMULHSU

function vector_integer_unary_operation(operation : Semantic_operation) -> bool =
  operation == Op_VNEG | operation == Op_VABS | operation == Op_VNOT
  | operation == Op_VCLZ | operation == Op_VCTZ | operation == Op_VCLS
  | operation == Op_VCTS | operation == Op_VPOPCNT | operation == Op_VREVBYTE

function vector_shift_operation_p(operation : Semantic_operation) -> bool =
  operation == Op_VSHL | operation == Op_VSHR | operation == Op_VSAR
  | operation == Op_VROL | operation == Op_VROR

function vector_integer_compare_operation(operation : Semantic_operation) -> bool =
  operation == Op_VCMPcc | operation == Op_VTESTZ | operation == Op_VTESTNZ

function vector_memory_direct_store_image(instruction : Decoded_instruction,
                                          state : Cpu_state, predicate : list(bits(8)),
                                          lanes : int, element_bytes : int)
  -> option(list(bits(8))) = {
  let operation = instruction.form.operation;
  if operation == Op_PMOV then match predicate_register_index(instruction, "src") {
    Some(index) => Some(state.predicate_registers[unsigned(index)]), None() => None(),
  }
  else match vector_register_index(instruction, "src") {
    None() => None(),
    Some(index) => {
      let source = state.vector_registers[unsigned(index)];
      if operation == Op_VMOV then Some(source)
      else if vector_integer_unary_operation(operation) then Some(
        vector_integer_unary_source_image(
          operation, zero_vector_bytes(state.vector_length_bytes), source,
          predicate, 0, lanes, element_bytes
        )
      )
      else None()
    },
  }
}

function start_vector_memory_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let memory_operation = operation == Op_PMOV | operation == Op_VMOV
    | operation == Op_VMOVZ | vector_integer_binary_operation(operation)
    | vector_integer_unary_operation(operation) | vector_shift_operation_p(operation)
    | vector_integer_compare_operation(operation)
    | vector_integer_reduction_operation(operation);
  if not_bool(memory_operation) then None()
  else match vector_memory_operand(instruction.operands) {
  None() => None(),
  Some(memory_operand) => {
    let element_bytes = if operation == Op_PMOV then tdiv_int(state.vector_length_bytes, 8)
                        else operation_width(instruction);
    let fp_form : bool = operation != Op_PMOV & (match condition_size_field(instruction.fields) {
      Some(selector) => selector >= 5, None() => false,
    });
    if fp_form then None()
    else {
      let evaluated = if operation == Op_PMOV then match memory_operand.ea {
        None() => None(),
        Some(ea) => Some(evaluate_decoded_ea(
          memory_operand, ea, state, state.pc, element_bytes
        )),
      }
      else evaluate_vector_instruction_ea(
        instruction.operands, state, state.pc, element_bytes
      );
      match evaluated {
        None() => None(),
        Some((evaluation, evaluated_state)) => {
          let after = advance_pc(evaluated_state, instruction);
          let predicate = if operation == Op_PMOV then [||]
                          else vector_memory_predicate(instruction, state);
          let lanes = if operation == Op_PMOV then 1
                      else tdiv_int(state.vector_length_bytes, element_bytes);
          let memory_destination = vector_operand_writes(
            memory_operand.name, instruction.operands
          );
          let needs_read = not_bool(memory_destination)
            | vector_integer_binary_operation(operation)
            | vector_shift_operation_p(operation);
          if needs_read then Some(vector_memory_waiting(
            instruction, state, after, PhaseVectorMemoryRead,
            vector_memory_request(
              VectorMemoryRead, instruction, state, evaluation,
              predicate, [||], element_bytes,
              if memory_destination then AccessReadModifyWrite else AccessLoad
            )
          ))
          else match vector_memory_direct_store_image(
            instruction, state, predicate, lanes, element_bytes
          ) {
            None() => None(),
            Some(values) => Some(vector_memory_waiting(
              instruction, state, after, PhaseVectorMemoryWrite,
              vector_memory_request(
                VectorMemoryWrite, instruction, state, evaluation,
                predicate, values, element_bytes, AccessStore
              )
            )),
          }
        },
      }
    }
  },
  }
}

function vector_response_length(instruction : Decoded_instruction, state : Cpu_state) -> int =
  if instruction.form.operation == Op_PMOV then tdiv_int(state.vector_length_bytes, 8)
  else state.vector_length_bytes

function vector_memory_source_result(instruction : Decoded_instruction,
                                     before : Cpu_state, after : Cpu_state,
                                     memory : list(bits(8))) -> option(Cpu_state) = {
  let operation = instruction.form.operation;
  if operation == Op_PMOV then match predicate_register_index(instruction, "dst") {
    None() => None(),
    Some(destination) => {
      var updated = after;
      updated.predicate_registers[unsigned(destination)] = memory;
      updated.vector_component_modified = true;
      Some(updated)
    },
  }
  else {
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(before.vector_length_bytes, element_bytes);
    let predicate = vector_memory_predicate(instruction, before);
    if operation == Op_VMOV | operation == Op_VMOVZ then match
      vector_register_index(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        var updated = after;
        updated.vector_registers[unsigned(destination)] = if operation == Op_VMOVZ
          then memory
          else vector_merge_image(
            before.vector_registers[unsigned(destination)], memory, predicate,
            0, lanes, element_bytes
          );
        updated.vector_component_modified = true;
        Some(updated)
      },
    }
    else if vector_integer_binary_operation(operation) then match
      vector_register_index(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        var updated = after;
        updated.vector_registers[unsigned(destination)] = vector_integer_binary_image(
          operation, before.vector_registers[unsigned(destination)], memory,
          predicate, 0, lanes, element_bytes
        );
        updated.vector_component_modified = true;
        Some(updated)
      },
    }
    else if vector_integer_unary_operation(operation) then match
      vector_register_index(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        var updated = after;
        updated.vector_registers[unsigned(destination)] =
          vector_integer_unary_source_image(
            operation, before.vector_registers[unsigned(destination)], memory,
            predicate, 0, lanes, element_bytes
          );
        updated.vector_component_modified = true;
        Some(updated)
      },
    }
    else if vector_integer_reduction_operation(operation) then match
      operand_named(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        var updated = after;
        updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
          64,
          vector_integer_reduction_image(
            operation, memory, predicate, 0, lanes, element_bytes,
            vector_integer_reduction_identity(operation, element_bytes)
          ),
          0
        );
        Some(updated)
      },
    }
    else if vector_shift_operation_p(operation) then match
      vector_register_index(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        var updated = after;
        updated.vector_registers[unsigned(destination)] = vector_shift_image(
          operation, before.vector_registers[unsigned(destination)], memory,
          0, true, predicate, 0, lanes, element_bytes
        );
        updated.vector_component_modified = true;
        Some(updated)
      },
    }
    else if vector_integer_compare_operation(operation) then match
      (vector_register_index(instruction, "lhs"),
       predicate_register_index(instruction, "govern"),
       predicate_register_index(instruction, "dst")) {
      (Some(left), Some(govern), Some(destination)) => {
        let condition : int = match operand_named(instruction, "cc") {
          Some(value) => unsigned(value.value[3 .. 0]), None() => 0,
        };
        var updated = after;
        updated.predicate_registers[unsigned(destination)] = vector_integer_compare_image(
          operation, condition, before.vector_registers[unsigned(left)], memory,
          before.predicate_registers[unsigned(govern)],
          zero_vector_bytes(tdiv_int(before.vector_length_bytes, 8)),
          0, lanes, element_bytes
        );
        updated.vector_component_modified = true;
        Some(updated)
      },
      _ => None(),
    }
    else None()
  }
}

function vector_memory_destination_result(instruction : Decoded_instruction,
                                          before : Cpu_state,
                                          memory : list(bits(8)))
  -> option(list(bits(8))) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(before.vector_length_bytes, element_bytes);
  let predicate = vector_memory_predicate(instruction, before);
  if vector_integer_binary_operation(operation) then match
    vector_register_index(instruction, "src") {
    Some(source) => Some(vector_integer_binary_image(
      operation, memory, before.vector_registers[unsigned(source)],
      predicate, 0, lanes, element_bytes
    )),
    None() => None(),
  }
  else if vector_shift_operation_p(operation) then {
    let counts : list(bits(8)) = match vector_register_index(instruction, "src") {
      Some(source) => before.vector_registers[unsigned(source)],
      None() => zero_vector_bytes(before.vector_length_bytes),
    };
    let vector_counts = vector_register_index(instruction, "src") != None();
    let immediate : int = match operand_named(instruction, "count") {
      Some(value) => unsigned(immediate_value(value)), None() => 0,
    };
    Some(vector_shift_image(
      operation, memory, counts, immediate, vector_counts,
      predicate, 0, lanes, element_bytes
    ))
  }
  else None()
}

function vector_fp_commit_response(previous : Execution_result,
                                   instruction : Decoded_instruction,
                                   response : Transaction_response) -> Execution_result = {
  let before = previous.pending.before;
  let causes = response.generated_fflags;
  if (causes & vector_fp_allowed_causes(instruction.form.operation)) != causes then
    faulted(before, instruction.form.operation, InvalidControlState,
            "vector FP response reported an impossible cause")
  else if byte_count(response.body_bytes) != vector_fp_result_length(instruction, before) then
    faulted(before, instruction.form.operation, InvalidControlState,
            "vector FP response length mismatch")
  else if fp_traps(before.fstatus, causes) then
    fp_fault_with_causes(before, instruction.form.operation, causes)
  else match vector_writable_operand(instruction.operands) {
    None() => faulted(before, instruction.form.operation, InvalidControlState,
                      "missing vector FP destination"),
    Some(destination) => {
      var updated = previous.pending.after;
      updated.fflags = updated.fflags | causes;
      if causes != fflags_none then updated.fp_component_modified = true else ();
      if destination.type_name == "Vn" then {
        updated.vector_registers[unsigned(destination.value[4 .. 0])] = response.body_bytes;
        updated.vector_component_modified = true;
        completed(before, updated, CommitRegisters, [||])
      }
      else if destination.type_name == "Pn" then {
        updated.predicate_registers[unsigned(destination.value[3 .. 0])] = response.body_bytes;
        updated.vector_component_modified = true;
        completed(before, updated, CommitRegisters, [||])
      }
      else if destination.type_name == "Rn" then match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => {
          updated.registers[unsigned(destination.value[3 .. 0])] = value;
          completed(before, updated, CommitRegisters, [||])
        },
        None() => faulted(before, instruction.form.operation, InvalidControlState,
                          "truncated vector integer reduction result"),
      }
      else if destination.type_name == "Fn" then match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => {
          updated.floating_registers[unsigned(destination.value[3 .. 0])] = value;
          updated.fp_component_modified = true;
          completed(before, updated, CommitRegisters, [||])
        },
        None() => faulted(before, instruction.form.operation, InvalidControlState,
                          "truncated vector FP reduction result"),
      }
      else if destination.type_name == "VEA" then match evaluate_vector_instruction_ea(
        instruction.operands, before, before.pc, operation_width(instruction)
      ) {
        None() => faulted(before, instruction.form.operation, InvalidControlState,
                          "missing vector FP memory destination"),
        Some((evaluation, _)) => vector_fp_waiting(
          instruction, before, updated, PhaseVectorFpMemoryWrite,
          vector_memory_request(
            VectorMemoryWrite, instruction, before, evaluation,
            vector_memory_predicate(instruction, before), response.body_bytes,
            operation_width(instruction), AccessStore
          ), previous.pending.vector_payload0
        ),
      }
      else faulted(before, instruction.form.operation, InvalidControlState,
                   "unsupported vector FP destination")
    },
  }
}

function resume_vector_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
  PhaseVectorFpMemoryWrite => completed(
    previous.pending.before, previous.pending.after, CommitMemory, [||]
  ),
  PhaseVectorFpMemoryRead => match previous.pending.instruction {
    None() => faulted(previous.pending.before, previous.pending.operation,
                      InvalidControlState, "missing vector FP memory continuation"),
    Some(instruction) => if byte_count(response.body_bytes)
                            != previous.pending.before.vector_length_bytes then
      faulted(previous.pending.before, instruction.form.operation, InvalidControlState,
              "vector FP memory response length mismatch")
    else vector_fp_waiting(
      instruction, previous.pending.before, previous.pending.after, PhaseVectorFpCompute,
      vector_fp_request(instruction, previous.pending.before, response.body_bytes),
      response.body_bytes
    ),
  },
  PhaseVectorFpCompute => match previous.pending.instruction {
    Some(instruction) => vector_fp_commit_response(previous, instruction, response),
    None() => faulted(previous.pending.before, previous.pending.operation,
                      InvalidControlState, "missing vector FP compute continuation"),
  },
  PhaseVectorMemoryWrite => completed(
    previous.pending.before, previous.pending.after, CommitMemory, [||]
  ),
  PhaseVectorMemoryRead => match previous.pending.instruction {
    None() => faulted(previous.pending.before, previous.pending.operation,
                      InvalidControlState, "missing vector memory continuation"),
    Some(instruction) => {
      let before = previous.pending.before;
      if byte_count(response.body_bytes) != vector_response_length(instruction, before) then
        faulted(before, instruction.form.operation, InvalidControlState,
                "vector memory response length mismatch")
      else match vector_memory_operand(instruction.operands) {
        None() => faulted(before, instruction.form.operation, InvalidControlState,
                          "missing vector memory operand"),
        Some(memory_operand) => if vector_operand_writes(
          memory_operand.name, instruction.operands
        ) then match vector_memory_destination_result(
          instruction, before, response.body_bytes
        ) {
          None() => faulted(before, instruction.form.operation, IllegalInstruction,
                            "unsupported vector memory destination continuation"),
          Some(values) => {
            let element_bytes = operation_width(instruction);
            match evaluate_vector_instruction_ea(
              instruction.operands, before, before.pc, element_bytes
            ) {
              None() => faulted(before, instruction.form.operation, InvalidControlState,
                                "missing vector memory address continuation"),
              Some((evaluation, _)) => vector_memory_waiting(
                instruction, before, previous.pending.after, PhaseVectorMemoryWrite,
                vector_memory_request(
                  VectorMemoryWrite, instruction, before, evaluation,
                  vector_memory_predicate(instruction, before), values,
                  element_bytes, AccessStore
                )
              ),
            }
          },
        }
        else match vector_memory_source_result(
          instruction, before, previous.pending.after, response.body_bytes
        ) {
          Some(updated) => completed(before, updated, CommitMemory, [||]),
          None() => faulted(before, instruction.form.operation, IllegalInstruction,
                            "unsupported vector memory source continuation"),
        }
      }
    },
  },
  _ => faulted(previous.pending.before, previous.pending.operation,
               InvalidControlState, "unexpected vector memory continuation"),
}

function execute_vector_predicate(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let element_bytes = operation_width(instruction);
  let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
  let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
  let zero_vector = zero_vector_bytes(state.vector_length_bytes);
  let fp_form : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5, None() => false,
  };
  if operation == Op_VCLR then match vector_register_index(instruction, "dst") {
    Some(destination) => {
      var updated = state;
      updated.vector_registers[unsigned(destination)] = zero_vector;
      Some(vector_finish(instruction, state, updated))
    }, None() => None(),
  }
  else if operation == Op_VMOV then match
    (vector_register_index(instruction, "src"), vector_register_index(instruction, "dst")) {
    (Some(source), Some(destination)) => {
      var updated = state;
      updated.vector_registers[unsigned(destination)] = match
        predicate_register_index(instruction, "govern") {
          Some(predicate) => vector_merge_image(
            state.vector_registers[unsigned(destination)],
            state.vector_registers[unsigned(source)],
            state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes
          ),
          None() => state.vector_registers[unsigned(source)],
        };
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_VDUP & not_bool(fp_form) then match
    (value_named(instruction, state, "src"), value_named(instruction, state, "immediate"),
     vector_register_index(instruction, "dst")) {
    (Some(source), _, Some(destination)) => {
      let image = vector_duplicate_image(
        zero_vector, 0, lanes, element_bytes, unsigned(source)
      );
      var updated = state;
      updated.vector_registers[unsigned(destination)] = image;
      Some(vector_finish(instruction, state, updated))
    },
    (_, Some(source), Some(destination)) => {
      let image = vector_duplicate_image(
        zero_vector, 0, lanes, element_bytes, unsigned(source)
      );
      var updated = state;
      updated.vector_registers[unsigned(destination)] = image;
      Some(vector_finish(instruction, state, updated))
    },
    _ => None(),
  }
  else if operation == Op_VEXTRACT & not_bool(fp_form) then match
    (vector_register_index(instruction, "src"), value_named(instruction, state, "index"),
     operand_named(instruction, "dst")) {
    (Some(source), Some(index_value), Some(destination)) => {
      let index = unsigned(index_value);
      if index >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "VEXTRACT lane index exceeds the lane count",
        0x0000000000000001
      ))
      else {
        var updated = state;
        updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
          64, vector_lane_unsigned(state.vector_registers[unsigned(source)], index, element_bytes), 0
        );
        Some(vector_finish(instruction, state, updated))
      }
    }, _ => None(),
  }
  else if operation == Op_VINSERT & not_bool(fp_form) then match
    (value_named(instruction, state, "src"), value_named(instruction, state, "index"),
     vector_register_index(instruction, "dst")) {
    (Some(source), Some(index_value), Some(destination)) => {
      let index = unsigned(index_value);
      if index >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "VINSERT lane index exceeds the lane count",
        0x0000000000000001
      ))
      else {
        var updated = state;
        updated.vector_registers[unsigned(destination)] = vector_write_lane(
          state.vector_registers[unsigned(destination)], index, element_bytes, unsigned(source)
        );
        Some(vector_finish(instruction, state, updated))
      }
    }, _ => None(),
  }
  else if operation == Op_VINDEX then match vector_register_index(instruction, "dst") {
    Some(destination) => {
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_index_image(
        zero_vector, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, None() => None(),
  }
  else if (operation == Op_VADD | operation == Op_VSUB | operation == Op_VAND
       | operation == Op_VOR | operation == Op_VXOR | operation == Op_VMINS
       | operation == Op_VMINU | operation == Op_VMAXS | operation == Op_VMAXU
       | operation == Op_VMUL | operation == Op_VMULHS | operation == Op_VMULHU
       | operation == Op_VMULHSU) & not_bool(fp_form) then match
    (vector_register_index(instruction, "src"), vector_register_index(instruction, "dst"),
     predicate_register_index(instruction, "govern")) {
    (Some(source), Some(destination), Some(predicate)) => {
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_integer_binary_image(
        operation, state.vector_registers[unsigned(destination)],
        state.vector_registers[unsigned(source)], state.predicate_registers[unsigned(predicate)],
        0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if (operation == Op_VNEG | operation == Op_VABS | operation == Op_VNOT
       | operation == Op_VCLZ | operation == Op_VCTZ | operation == Op_VCLS
       | operation == Op_VCTS | operation == Op_VPOPCNT | operation == Op_VREVBYTE)
       & not_bool(fp_form) then match
    (vector_register_index(instruction, "dst"),
     predicate_register_index(instruction, "govern")) {
    (Some(destination), Some(predicate)) => {
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_integer_unary_image(
        operation, state.vector_registers[unsigned(destination)],
        state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_VSHL | operation == Op_VSHR | operation == Op_VSAR
       | operation == Op_VROL | operation == Op_VROR then match
    (vector_register_index(instruction, "dst"),
     predicate_register_index(instruction, "govern")) {
    (Some(destination), Some(predicate)) => {
      let count_vector = vector_register_index(instruction, "src");
      let counts : list(bits(8)) = match count_vector {
        Some(index) => state.vector_registers[unsigned(index)], None() => zero_vector,
      };
      let scalar_count : int = match operand_named(instruction, "count") {
        Some(count_operand) => unsigned(immediate_value(count_operand)), None() => 0,
      };
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_shift_image(
        operation, state.vector_registers[unsigned(destination)], counts,
        scalar_count, count_vector != None(),
        state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if (operation == Op_VCMPcc | operation == Op_VTESTZ | operation == Op_VTESTNZ)
       & not_bool(fp_form) then match
    (vector_register_index(instruction, "lhs"), vector_register_index(instruction, "rhs"),
     predicate_register_index(instruction, "govern"),
     predicate_register_index(instruction, "dst")) {
    (Some(left), Some(right), Some(govern), Some(destination)) => {
      let condition : int = match operand_named(instruction, "cc") {
        Some(value) => unsigned(value.value[3 .. 0]), None() => 0,
      };
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = vector_integer_compare_image(
        operation, condition, state.vector_registers[unsigned(left)],
        state.vector_registers[unsigned(right)], state.predicate_registers[unsigned(govern)],
        empty, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if vector_integer_reduction_operation(operation) then match
    (vector_register_index(instruction, "src"),
     predicate_register_index(instruction, "govern"),
     operand_named(instruction, "dst")) {
    (Some(source), Some(predicate), Some(destination)) => {
      var updated = state;
      updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
        64,
        vector_integer_reduction_image(
          operation, state.vector_registers[unsigned(source)],
          state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes,
          vector_integer_reduction_identity(operation, element_bytes)
        ),
        0
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_VEXTZW | operation == Op_VEXTSW
       | operation == Op_VEXTZL | operation == Op_VEXTSL
       | operation == Op_VEXTZQ | operation == Op_VEXTSQ
       | operation == Op_VTRUNCB | operation == Op_VTRUNCW
       | operation == Op_VTRUNCL then match
    (vector_register_index(instruction, "src"), vector_register_index(instruction, "dst"),
     predicate_register_index(instruction, "govern")) {
    (Some(source), Some(destination), Some(predicate)) => {
      let destination_bytes = vector_width_change_destination_bytes(operation);
      let container_bytes = if element_bytes > destination_bytes
                            then element_bytes else destination_bytes;
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_width_change_image(
        operation, state.vector_registers[unsigned(destination)],
        state.vector_registers[unsigned(source)],
        state.predicate_registers[unsigned(predicate)], 0,
        tdiv_int(state.vector_length_bytes, container_bytes),
        element_bytes, destination_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_VPERM | operation == Op_VSLIDEUP
       | operation == Op_VSLIDEDN | operation == Op_VSLICE
       | operation == Op_VZIPLO | operation == Op_VZIPHI
       | operation == Op_VUZIPLO | operation == Op_VUZIPHI
       | operation == Op_VTRNLO | operation == Op_VTRNHI then match
    (vector_register_index(instruction, "dst"),
     predicate_register_index(instruction, "govern")) {
    (Some(destination), Some(predicate)) => {
      let source : list(bits(8)) = match vector_register_index(instruction, "src") {
        Some(index) => state.vector_registers[unsigned(index)], None() => zero_vector,
      };
      let count : int = match operand_named(instruction, "count") {
        Some(count_operand) => unsigned(immediate_value(count_operand)), None() => 0,
      };
      let original = state.vector_registers[unsigned(destination)];
      var updated = state;
      updated.vector_registers[unsigned(destination)] = vector_permute_image(
        operation, original, source, original,
        state.predicate_registers[unsigned(predicate)], 0, lanes, element_bytes, count
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_RDVL | operation == Op_RDCNT then match operand_named(instruction, "dst") {
    Some(dst) => {
      var updated = state;
      updated.registers[unsigned(dst.value[3 .. 0])] = get_slice_int(
        64, if operation == Op_RDVL then state.vector_length_bytes else lanes, 0
      );
      Some(vector_finish(instruction, state, updated))
    }, None() => None(),
  }
  else if operation == Op_ADDVL | operation == Op_ADDPL then
    match (operand_named(instruction, "offset"), operand_named(instruction, "dst")) {
      (Some(offset), Some(dst)) => {
        let scale = if operation == Op_ADDVL then state.vector_length_bytes
                    else tdiv_int(state.vector_length_bytes, 8);
        let index = unsigned(dst.value[3 .. 0]);
        var updated = state;
        updated.registers[index] = add_bits(
          state.registers[index], get_slice_int(64, signed(immediate_value(offset)) * scale, 0)
        );
        Some(vector_finish(instruction, state, updated))
      }, _ => None(),
    }
  else if operation == Op_PTRUE | operation == Op_PFALSE
       | operation == Op_PHEAD | operation == Op_PTAIL then
    match predicate_register_index(instruction, "dst") {
      None() => None(),
      Some(destination) => {
        let boundary : int = if operation == Op_PHEAD | operation == Op_PTAIL then
          match value_named(instruction, state, "count") {
            Some(value) => tmod_int(unsigned(value), lanes), None() => 0,
          }
          else 0;
        let first = if operation == Op_PHEAD then boundary else 0;
        let last = if operation == Op_PFALSE then 0
                   else if operation == Op_PTAIL then boundary else lanes;
        var updated = state;
        updated.predicate_registers[unsigned(destination)] =
          predicate_fill_typed(empty, 0, lanes, element_bytes, first, last);
        Some(vector_finish(instruction, state, updated))
      },
    }
  else if operation == Op_PAND | operation == Op_POR | operation == Op_PXOR then
    match (predicate_register_index(instruction, "src"),
           predicate_register_index(instruction, "dst")) {
      (Some(source), Some(destination)) => {
        var updated = state;
        updated.predicate_registers[unsigned(destination)] = predicate_raw_binary(
          state.predicate_registers[unsigned(destination)],
          state.predicate_registers[unsigned(source)], operation
        );
        Some(vector_finish(instruction, state, updated))
      }, _ => None(),
    }
  else if operation == Op_PNOT then match predicate_register_index(instruction, "dst") {
    Some(destination) => {
      var updated = state;
      updated.predicate_registers[unsigned(destination)] =
        predicate_raw_not(state.predicate_registers[unsigned(destination)]);
      Some(vector_finish(instruction, state, updated))
    }, None() => None(),
  }
  else if operation == Op_PSEL then match
    (predicate_register_index(instruction, "select"),
     predicate_register_index(instruction, "src"),
     predicate_register_index(instruction, "dst")) {
    (Some(select), Some(source), Some(destination)) => {
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = predicate_raw_select(
        state.predicate_registers[unsigned(select)],
        state.predicate_registers[unsigned(source)],
        state.predicate_registers[unsigned(destination)]
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_PUNPKLO | operation == Op_PUNPKHI
       | operation == Op_PPACKLO | operation == Op_PPACKHI then match
    (predicate_register_index(instruction, "src"),
     predicate_register_index(instruction, "dst")) {
    (Some(source), Some(destination)) => {
      let source_image = state.predicate_registers[unsigned(source)];
      let image = if operation == Op_PUNPKLO | operation == Op_PUNPKHI then
        predicate_unpack_image(source_image, empty, 0, lanes, element_bytes,
                               operation == Op_PUNPKHI)
      else predicate_pack_image(source_image, empty, 0, lanes, element_bytes,
                                operation == Op_PPACKHI);
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = image;
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_PZIPLO | operation == Op_PZIPHI
       | operation == Op_PUZIPLO | operation == Op_PUZIPHI
       | operation == Op_PTRNLO | operation == Op_PTRNHI then match
    (predicate_register_index(instruction, "lhs"),
     predicate_register_index(instruction, "rhs"),
     predicate_register_index(instruction, "dst")) {
    (Some(left), Some(right), Some(destination)) => {
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = predicate_pair_image(
        operation, state.predicate_registers[unsigned(left)],
        state.predicate_registers[unsigned(right)],
        empty, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_PPERM then match
    (vector_register_index(instruction, "index"),
     predicate_register_index(instruction, "dst")) {
    (Some(indices), Some(destination)) => {
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = predicate_permute_image(
        state.predicate_registers[unsigned(destination)],
        state.vector_registers[unsigned(indices)], empty, 0, lanes, element_bytes
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_PSLIDEUP | operation == Op_PSLIDEDN | operation == Op_PSLICE then match
    (predicate_register_index(instruction, "dst"), operand_named(instruction, "count")) {
    (Some(destination), Some(count_operand)) => {
      let source = if operation == Op_PSLICE then match
        predicate_register_index(instruction, "src") {
          Some(index) => state.predicate_registers[unsigned(index)], None() => empty,
        } else empty;
      var updated = state;
      updated.predicate_registers[unsigned(destination)] = predicate_slide_image(
        operation, state.predicate_registers[unsigned(destination)], source, empty,
        0, lanes, element_bytes, unsigned(immediate_value(count_operand))
      );
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_PCOUNT | operation == Op_PFIRST | operation == Op_PLAST then match
    (predicate_register_index(instruction, "predicate"), operand_named(instruction, "dst")) {
    (Some(source), Some(destination)) => {
      let result = if operation == Op_PCOUNT
        then predicate_count(state.predicate_registers[unsigned(source)], 0, lanes, element_bytes, 0)
        else if operation == Op_PFIRST
        then predicate_first(state.predicate_registers[unsigned(source)], 0, lanes, element_bytes)
        else predicate_last(state.predicate_registers[unsigned(source)], lanes - 1, element_bytes);
      var updated = state;
      updated.registers[unsigned(destination.value[3 .. 0])] =
        if result < 0 then 0xFFFFFFFFFFFFFFFF else get_slice_int(64, result, 0);
      Some(vector_finish(instruction, state, updated))
    }, _ => None(),
  }
  else if operation == Op_BPANY | operation == Op_BPNONE | operation == Op_BPALL then match
    predicate_register_index(instruction, "predicate") {
    None() => None(),
    Some(source) => {
      let any = predicate_any(state.predicate_registers[unsigned(source)]);
      let take = if operation == Op_BPANY then any
                 else if operation == Op_BPNONE then not_bool(any)
                 else predicate_all_typed(state.predicate_registers[unsigned(source)], 0, lanes, element_bytes);
      if take then start_control_transaction(instruction, state)
      else Some(completed(state, advance_pc(state, instruction), CommitControl, [||]))
    },
  }
  else if operation == Op_PLOOP then match
    (operand_named(instruction, "remaining"), operand_named(instruction, "offset"),
     predicate_register_index(instruction, "predicate")) {
    (Some(remaining_operand), Some(offset_operand), Some(predicate)) => {
      let remaining_index = unsigned(remaining_operand.value[3 .. 0]);
      let offset_index = unsigned(offset_operand.value[3 .. 0]);
      let remaining = unsigned(state.registers[remaining_index]);
      let offset = unsigned(state.registers[offset_index]);
      if remaining == 0 then start_control_transaction(instruction, state)
      else if offset >= lanes then Some(faulted_with_error_code(
        state, operation, VectorRangeFault, "PLOOP offset exceeds the lane count",
        0x0000000000000000
      ))
      else {
        let active = if remaining < lanes - offset then remaining else lanes - offset;
        var updated = state;
        updated.predicate_registers[unsigned(predicate)] = predicate_fill_typed(
          empty, 0, lanes, element_bytes, offset, offset + active
        );
        updated.registers[remaining_index] = get_slice_int(64, remaining - active, 0);
        updated.registers[offset_index] = 0x0000000000000000;
        Some(vector_finish(instruction, state, updated))
      }
    }, _ => None(),
  }
  else None()
}

function execute_vector_instruction(instruction : Decoded_instruction,
                                    state : Cpu_state) -> Execution_result =
  match execute_vector_fp_bridge(instruction, state) {
    Some(result) => result,
    None() => match start_vector_fp_transaction(instruction, state) {
      Some(result) => result,
      None() => match start_vector_memory_transaction(instruction, state) {
        Some(result) => result,
        None() => match execute_vector_predicate(instruction, state) {
          Some(result) => result,
          None() => faulted(state, instruction.form.operation, IllegalInstruction,
                            "missing vector semantics"),
        },
      },
    },
  }
