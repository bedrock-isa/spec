function append_bytes(left : list(bits(8)), right : list(bits(8))) -> list(bits(8)) =
  match left {
    [||] => right,
    byte :: tail => byte :: append_bytes(tail, right),
  }

function zero_byte_count(count : int) -> list(bits(8)) =
  if count <= 0 then [||] else 0x00 :: zero_byte_count(count - 1)

function le64_bytes(value : bits(64)) -> list(bits(8)) = [|
  value[7 .. 0], value[15 .. 8], value[23 .. 16], value[31 .. 24],
  value[39 .. 32], value[47 .. 40], value[55 .. 48], value[63 .. 56]
|]

function serialize_register_file(registers : Registers, index : int) -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(le64_bytes(registers[unsigned(get_slice_int(4, index, 0))]),
                    serialize_register_file(registers, index + 1))

function serialize_fp_file(registers : Floating_registers, index : int) -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(le64_bytes(registers[unsigned(get_slice_int(4, index, 0))]),
                    serialize_fp_file(registers, index + 1))

function serialize_vector_file(registers : Vector_registers, index : int) -> list(bits(8)) =
  if index >= 32 then [||]
  else append_bytes(registers[unsigned(get_slice_int(5, index, 0))],
                    serialize_vector_file(registers, index + 1))

function serialize_predicate_file(registers : Predicate_registers, index : int)
  -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(registers[unsigned(get_slice_int(4, index, 0))],
                    serialize_predicate_file(registers, index + 1))

function valid_vector_length_bytes(bytes : int) -> bool =
  bytes == 16 | bytes == 32 | bytes == 64 | bytes == 128
  | bytes == 256

function serialize_saved_segments(segments : Segment_registers, index : int) -> list(bits(8)) =
  if index >= 9 then [||]
  else append_bytes(le64_bytes(image_segment({ initial_cpu() with segments = segments }, index)),
                    serialize_saved_segments(segments, index + 1))

function fp_save_layout_valid(state : Cpu_state) -> bool =
  if state.fp_component_present then
    state.fp_component_id == 1
    & state.fp_component_bitmap_bit == 0
    & state.fp_component_offset == 192
    & state.fp_component_alignment == 64
    & state.fp_component_size == 192
    & state.fp_component_offset + state.fp_component_size <= state.save_area_size
    & state.fp_component_init_policy == 1
  else true

function vector_save_layout_valid(state : Cpu_state) -> bool =
  if state.vector_component_present then
    state.vector_enabled
    & valid_vector_length_bytes(state.vector_length_bytes)
    & state.vector_component_id == 2
    & state.vector_component_bitmap_bit == 1
    & state.vector_component_alignment == 64
    & tmod_int(state.vector_component_offset, 64) == 0
    & state.vector_component_size ==
        tdiv_int(34 * state.vector_length_bytes + 63, 64) * 64
    & state.vector_component_offset + state.vector_component_size <= state.save_area_size
    & state.vector_component_init_policy == 1
    & (not_bool(state.fp_component_present)
       | state.vector_component_offset >= state.fp_component_offset + state.fp_component_size)
  else not_bool(state.vector_enabled)

function save_layout_valid(state : Cpu_state) -> bool =
  state.save_format == 0x0
  & state.save_bitmap_words == 1
  & state.save_fixed_size == 192
  & state.save_area_size >= state.save_fixed_size
  & tmod_int(state.save_area_size, 64) == 0
  & fp_save_layout_valid(state)
  & vector_save_layout_valid(state)

function save_header(state : Cpu_state) -> bits(64) =
  sail_shiftleft(state.status & 0x000000000000FFFF, 36)
  | sail_shiftleft(sail_zero_extend(state.flags, 64), 20)
  | (if state.current_dfa then 0x0000000000000400 else 0x0000000000000000)
  | 0x00000000000003F0
  | sail_zero_extend(state.save_format, 64)

function restored_event_state_valid(state : Cpu_state, saved_status : bits(64),
                                    saved_dfa : bool) -> bool = {
  let privileged = saved_status[4] == bitone;
  let active = saved_status[0] == bitone;
  let depth = status_event_depth(saved_status);
  let user_origin = status_user_origin(saved_status);
  if saved_status[15 .. 11] != 0b00000 | (saved_dfa & not_bool(active)) then false
  else if privileged & active then
    depth > 0 & (not_bool(user_origin) | state.controls[11][32] == bitone)
  else if privileged then depth == 0 & not_bool(user_origin) & not_bool(saved_dfa)
  else not_bool(active) & depth == 0 & not_bool(user_origin) & not_bool(saved_dfa)
}

function fp_save_payload(state : Cpu_state) -> list(bits(8)) = {
  let raw = append_bytes(
    serialize_fp_file(state.floating_registers, 0),
    append_bytes(le64_bytes(sail_zero_extend(state.fflags, 64)), le64_bytes(state.fstatus))
  );
  append_bytes(raw, zero_byte_count(state.fp_component_size - 144))
}

function vector_save_payload(state : Cpu_state) -> list(bits(8)) = {
  let raw = append_bytes(
    serialize_vector_file(state.vector_registers, 0),
    serialize_predicate_file(state.predicate_registers, 0)
  );
  append_bytes(raw, zero_byte_count(state.vector_component_size
                                    - 34 * state.vector_length_bytes))
}

function save_image_bytes(state : Cpu_state) -> list(bits(8)) = {
  let include_fp = state.fp_component_present & state.fp_enabled & state.fp_component_modified;
  let include_vector = state.vector_component_present & state.vector_enabled
                     & state.vector_component_modified;
  let bitmap : bits(64) = (if include_fp then 0x0000000000000001
                           else 0x0000000000000000)
                        | (if include_vector then 0x0000000000000002
                           else 0x0000000000000000);
  let fixed = append_bytes(
    le64_bytes(save_header(state)),
    append_bytes(le64_bytes(bitmap),
      append_bytes(serialize_register_file(state.registers, 0),
                   serialize_saved_segments(state.segments, 3)))
  );
  let first_offset = if state.fp_component_present then state.fp_component_offset
    else if state.vector_component_present then state.vector_component_offset
    else state.save_area_size;
  let to_component = append_bytes(fixed, zero_byte_count(first_offset - state.save_fixed_size));
  let after_fp = if state.fp_component_present then {
    let component = if include_fp then fp_save_payload(state)
                    else zero_byte_count(state.fp_component_size);
    append_bytes(to_component, component)
  }
  else to_component;
  let after_fp_offset = if state.fp_component_present
    then state.fp_component_offset + state.fp_component_size else first_offset;
  let to_vector = if state.vector_component_present then append_bytes(
    after_fp, zero_byte_count(state.vector_component_offset - after_fp_offset)
  ) else after_fp;
  let after_vector = if state.vector_component_present then append_bytes(
    to_vector,
    if include_vector then vector_save_payload(state)
    else zero_byte_count(state.vector_component_size)
  ) else to_vector;
  let used = if state.vector_component_present
    then state.vector_component_offset + state.vector_component_size
    else if state.fp_component_present then state.fp_component_offset + state.fp_component_size
    else state.save_fixed_size;
  append_bytes(after_vector, zero_byte_count(state.save_area_size - used))
}
