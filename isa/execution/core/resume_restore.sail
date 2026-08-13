function restore_register_file(bytes : list(bits(8)), index : int, registers : Registers)
  -> option(Registers) =
  if index >= 16 then Some(registers)
  else match read_le_bits(bytes, 16 + index * 8, 64) {
    None() => None(),
    Some(value) => {
      var updated = registers;
      updated[unsigned(get_slice_int(4, index, 0))] = value;
      restore_register_file(bytes, index + 1, updated)
    },
  }

function restore_fp_file(bytes : list(bits(8)), offset : int, index : int,
                         registers : Floating_registers) -> option(Floating_registers) =
  if index >= 16 then Some(registers)
  else match read_le_bits(bytes, offset + index * 8, 64) {
    None() => None(),
    Some(value) => {
      var updated = registers;
      updated[unsigned(get_slice_int(4, index, 0))] = value;
      restore_fp_file(bytes, offset, index + 1, updated)
    },
  }

function restore_raw_image(previous : Execution_result, bytes : list(bits(8)),
                           header : bits(64), bitmap : bits(64)) -> Execution_result = {
  let state = previous.pending.before;
  let saved_status = sail_shiftright(header, 36) & 0x000000000000FFFF;
  let saved_flags = sail_shiftright(header, 20) & 0x000000000000FFFF;
  let invalid_status = state.supervisor
    & (saved_status[15 .. 6] != 0b0000000000
       | saved_status[4] != state.status[4] | saved_status[0] != state.status[0]);
  if byte_list_length(bytes) < state.save_area_size
     | saved_flags[15 .. 4] != 0x000 | invalid_status then
    faulted(state, Op_RESTORE, InvalidControlState, "invalid raw RESTORE image")
  else match restore_register_file(bytes, 0, state.registers) {
    None() => faulted(state, Op_RESTORE, InvalidControlState, "truncated RESTORE register block"),
    Some(registers) => match (
      read_le_bits(bytes, 144, 64), read_le_bits(bytes, 152, 64),
      read_le_bits(bytes, 160, 64), read_le_bits(bytes, 168, 64),
      read_le_bits(bytes, 176, 64), read_le_bits(bytes, 184, 64)
    ) {
      (Some(gs0), Some(gs1), Some(gs2), Some(gs3), Some(gs4), Some(gs5)) => {
        let invalid_segments =
          (header[4] == bitone & not_bool(segment_image_valid(gs0)))
          | (header[5] == bitone & not_bool(segment_image_valid(gs1)))
          | (header[6] == bitone & not_bool(segment_image_valid(gs2)))
          | (header[7] == bitone & not_bool(segment_image_valid(gs3)))
          | (header[8] == bitone & not_bool(segment_image_valid(gs4)))
          | (header[9] == bitone & not_bool(segment_image_valid(gs5)));
        if invalid_segments then faulted(
          state, Op_RESTORE, InvalidControlState, "invalid RESTORE segment image"
        )
        else {
          var updated = previous.pending.after;
          updated.registers = registers;
          updated.flags = saved_flags[3 .. 0];
          if state.supervisor then updated.status = saved_status else ();
          if header[4] == bitone then updated.segments[3] = gs0 else ();
          if header[5] == bitone then updated.segments[4] = gs1 else ();
          if header[6] == bitone then updated.segments[5] = gs2 else ();
          if header[7] == bitone then updated.segments[6] = gs3 else ();
          if header[8] == bitone then updated.segments[7] = gs4 else ();
          if header[9] == bitone then updated.segments[8] = gs5 else ();
          if bitmap[0] == bitzero then {
            if state.fp_component_present then {
              updated.floating_registers = zero_floating_registers();
              updated.fflags = 0b00000;
              updated.fstatus = 0x0000000000000000;
              updated.fp_component_modified = false
            } else ();
            completed(state, updated, CommitMemory, [||])
          }
          else match (
            restore_fp_file(bytes, state.fp_component_offset, 0,
                            state.floating_registers),
            read_le_bits(bytes, state.fp_component_offset + 128, 64),
            read_le_bits(bytes, state.fp_component_offset + 136, 64)
          ) {
            (Some(fp_registers), Some(fflags), Some(fstatus)) =>
              if (fflags & 0xFFFFFFFFFFFFFFE0) != 0x0000000000000000
                 | (fstatus & 0xFFFFFFFFFFFFFC00) != 0x0000000000000000 then
                faulted(state, Op_RESTORE, InvalidControlState,
                        "invalid RESTORE floating-point component")
              else {
                updated.floating_registers = fp_registers;
                updated.fflags = fflags[4 .. 0];
                updated.fstatus = fstatus;
                updated.fp_component_modified = fp_registers != zero_floating_registers()
                  | fflags != 0x0000000000000000 | fstatus != 0x0000000000000000;
                completed(state, updated, CommitMemory, [||])
              },
            _ => faulted(state, Op_RESTORE, InvalidControlState,
                         "truncated RESTORE floating-point component"),
          }
        }
      },
      _ => faulted(state, Op_RESTORE, InvalidControlState, "truncated RESTORE segment block"),
    },
  }
}

function decode_repeat_frame(control : bits(64), ext : bits(64), saved_pc : bits(64),
                             saved_cs : bits(64), state : Cpu_state) -> option(Repeat_state) =
  if control[18] == bitzero then
    if ext == 0x0000000000000000 then Some({ state.repeat_state with active = false })
    else None()
  else {
    let kind = unsigned(ext[9 .. 8]);
    let delta = sail_zero_extend(ext[31 .. 16], 64);
    let body_length = ext[47 .. 32];
    let grouped = kind == 1;
    let body_start = sub_bits(saved_pc, delta);
    let grouped_location_valid = not_bool(grouped) | (
      unsigned(delta) < unsigned(body_length)
      & unsigned(saved_pc) >= unsigned(delta)
      & segment_point(saved_cs, body_start).in_bounds
      & segment_point(saved_cs, add_bits(body_start,
          bits_from_int(unsigned(body_length) - 1))).in_bounds
    );
    if kind > 1 | ext[15 .. 10] != 0b000000 | ext[63 .. 48] != 0x0000
       | (kind == 0 & ext[7 .. 4] == 0x1)
       | (kind == 1 & ext[7 .. 4] != 0x0)
       | (not_bool(grouped) & (delta != 0x0000000000000000 | body_length != 0x0000))
       | (grouped & body_length == 0x0000)
       | not_bool(grouped_location_valid) then None()
    else {
      let counter = ext[3 .. 0];
      Some(struct {
        active = true, grouped = grouped, counter = counter,
        remaining = state.registers[unsigned(counter)], condition = ext[7 .. 4],
        body_bytes = body_length,
        body_start = if grouped then body_start else saved_pc,
        fixed_body = [||], group_progress = if grouped then unsigned(delta) else 0
      })
    }
  }

function continue_event_return(previous : Execution_result, bytes : list(bits(8)))
  -> Execution_result = match (
    read_le_bits(bytes, 0, 64), read_le_bits(bytes, 8, 64),
    read_le_bits(bytes, 16, 64), read_le_bits(bytes, 24, 64),
    read_le_bits(bytes, 32, 64), read_le_bits(bytes, 40, 64),
    read_le_bits(bytes, 48, 64), read_le_bits(bytes, 56, 64)
  ) {
    (Some(control), Some(event_info), Some(ext), Some(saved_pc), Some(saved_sp),
     Some(saved_cs), Some(saved_ds), Some(saved_ss)) => {
      let saved_flags = sail_shiftright(control, 32) & 0x000000000000FFFF;
      let saved_status = sail_shiftright(control, 48) & 0x000000000000FFFF;
      if control != previous.pending.captured_first
         | byte_list_length(bytes) < unsigned(control[7 .. 0]) * 8
         | event_info[63 .. 32] != 0x00000000
         | saved_flags[15 .. 4] != 0x000
         | saved_status[15 .. 6] != 0b0000000000
         | not_bool(segment_image_valid(saved_cs))
         | not_bool(segment_image_valid(saved_ds))
         | not_bool(segment_image_valid(saved_ss))
         | not_bool(segment_point(saved_cs, saved_pc).in_bounds)
         | not_bool(segment_point(saved_ss, saved_sp).in_bounds) then
        faulted(previous.pending.before, Op_ERET, InvalidControlState,
                "invalid raw event return frame")
      else match decode_repeat_frame(control, ext, saved_pc, saved_cs,
                                     previous.pending.before) {
        None() => faulted(previous.pending.before, Op_ERET, InvalidControlState,
                          "invalid FRAME_EXT1 repeat continuation"),
        Some(repeat_state) => {
          var candidate = previous.pending.before;
          candidate.flags = saved_flags[3 .. 0];
          candidate.status = saved_status;
          candidate.supervisor = saved_status[4] == bitone;
          candidate.pc = saved_pc;
          candidate.sp = saved_sp;
          candidate.segments[0] = saved_cs;
          candidate.segments[1] = saved_ds;
          candidate.segments[2] = saved_ss;
          candidate.event_depth = unsigned(control[15 .. 12]);
          candidate.event_stack_level = unsigned(control[17 .. 16]);
          candidate.repeat_state = repeat_state;
          candidate.halted = false;
          candidate.run_state = Running;
          let staged = { previous with pending = { previous.pending with after = candidate } };
          if repeat_state.active then {
            let fetch_length = if repeat_state.grouped
              then unsigned(repeat_state.body_bytes) else 18;
            let request = { empty_primitive_request() with
              kind = RepeatBodyFetch, ordinal = previous.pending.ordinal + 1,
              role = "eret_repeat_validate", domain = "CS", segment = 0,
              segment_image = saved_cs, width = fetch_length,
              range_start = repeat_state.body_start,
              range_end = add_bits(repeat_state.body_start, bits_from_int(fetch_length)),
              range_length = fetch_length,
              range_wrap = unsigned(add_bits(repeat_state.body_start,
                                              bits_from_int(fetch_length)))
                           < unsigned(repeat_state.body_start),
              range_end_at_modulus = add_bits(repeat_state.body_start,
                                               bits_from_int(fetch_length))
                                     == 0x0000000000000000,
              effective_address = repeat_state.body_start,
              linear_address = segment_point(saved_cs, repeat_state.body_start).linear,
              access = AccessExecute, address_translation = true,
              commit_point = false, body_length = fetch_length,
              state_image = previous.pending.before };
            continue_with_request(
              staged, PhaseEventReturnBody, previous.pending.ordinal + 1,
              saved_pc, saved_cs, request
            )
          }
          else continue_with_request(
            staged, PhaseEventReturnExecute, previous.pending.ordinal + 1,
            saved_pc, saved_cs,
            target_probe_request(previous.pending.ordinal + 1, saved_cs, saved_pc)
          )
        },
      }
    },
    _ => faulted(previous.pending.before, Op_ERET, InvalidControlState,
                 "truncated event return frame"),
  }

