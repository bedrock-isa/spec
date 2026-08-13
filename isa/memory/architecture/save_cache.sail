function first_evaluation(evaluations : list(Ea_evaluation)) -> option(Ea_evaluation) =
  match evaluations {
    [||] => None(),
    evaluation :: _ => Some(evaluation),
  }

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

function serialize_saved_segments(segments : Segment_registers, index : int) -> list(bits(8)) =
  if index >= 9 then [||]
  else append_bytes(le64_bytes(image_segment({ initial_cpu() with segments = segments }, index)),
                    serialize_saved_segments(segments, index + 1))

function save_layout_valid(state : Cpu_state) -> bool =
  state.save_format == 0x0
  & state.save_bitmap_words == 1
  & state.save_fixed_size == 192
  & state.save_area_size >= state.save_fixed_size
  & tmod_int(state.save_area_size, 64) == 0
  & (if state.fp_component_present then
       state.fp_component_id == 1
       & state.fp_component_bitmap_bit == 0
       & state.fp_component_offset == 192
       & state.fp_component_alignment == 64
       & state.fp_component_size == 192
       & state.fp_component_offset + state.fp_component_size <= state.save_area_size
       & state.fp_component_init_policy == 1
     else true)

function save_header(state : Cpu_state) -> bits(64) =
  sail_shiftleft(state.status & 0x000000000000FFFF, 36)
  | sail_shiftleft(sail_zero_extend(state.flags, 64), 20)
  | 0x00000000000003F0
  | sail_zero_extend(state.save_format, 64)

function fp_save_payload(state : Cpu_state) -> list(bits(8)) = {
  let raw = append_bytes(
    serialize_fp_file(state.floating_registers, 0),
    append_bytes(le64_bytes(sail_zero_extend(state.fflags, 64)), le64_bytes(state.fstatus))
  );
  append_bytes(raw, zero_byte_count(state.fp_component_size - 144))
}

function save_image_bytes(state : Cpu_state) -> list(bits(8)) = {
  let include_fp = state.fp_component_present & state.fp_enabled & state.fp_component_modified;
  let bitmap : bits(64) = if include_fp then 0x0000000000000001 else 0x0000000000000000;
  let fixed = append_bytes(
    le64_bytes(save_header(state)),
    append_bytes(le64_bytes(bitmap),
      append_bytes(serialize_register_file(state.registers, 0),
                   serialize_saved_segments(state.segments, 3)))
  );
  let to_component = append_bytes(
    fixed, zero_byte_count((if state.fp_component_present then state.fp_component_offset
                            else state.save_area_size) - state.save_fixed_size)
  );
  if state.fp_component_present then {
    let component = if include_fp then fp_save_payload(state)
                    else zero_byte_count(state.fp_component_size);
    append_bytes(
      append_bytes(to_component, component),
      zero_byte_count(state.save_area_size - state.fp_component_offset
                      - state.fp_component_size)
    )
  }
  else to_component
}

function start_cache_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let evaluated = evaluate_instruction_eas(
    instruction.operands, operation, state, state.pc, 8
  );
  match first_evaluation(evaluated.evaluations) {
    None() => None(),
    Some(address) => {
      let prefetch = operation == Op_PREFETCH | operation == Op_PREFETCHNT;
      let request = { request_for_evaluation(
        AddressTranslateRequest,
        0, address, AccessAddressOnly, 0x0000000000000000, false
      ) with role = "cache_translate", suppress_fault = prefetch, selector =
        if operation == Op_FLSHDCACHE then 0x0000000000000000
        else if operation == Op_INVDCACHE then 0x0000000000000001
        else if operation == Op_INVICACHE then 0x0000000000000002
        else if operation == Op_WRBKDCACHE then 0x0000000000000003
        else if operation == Op_SYNCCACHE then 0x0000000000000004
        else if operation == Op_PREFETCHNT then 0x0000000000000006
        else 0x0000000000000005,
        auxiliary = bits_from_int(state.cache_maintenance_granule), state_image = state };
      Some(waiting_transaction(
        state, advance_pc(evaluated.image, instruction), instruction, CommitControl,
        empty_destination(), PhaseCacheTranslate, 0,
        address.effective_address, 0x0000000000000000, request
      ))
    },
  }
}

