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

function drop_restore_bytes(bytes : list(bits(8)), count : int) -> list(bits(8)) =
  if count <= 0 then bytes
  else match bytes {
    [||] => [||],
    _head :: tail => drop_restore_bytes(tail, count - 1),
  }

function take_restore_bytes(bytes : list(bits(8)), count : int) -> list(bits(8)) =
  if count <= 0 then [||]
  else match bytes {
    [||] => [||],
    head :: tail => head :: take_restore_bytes(tail, count - 1),
  }

function restore_byte_slice(bytes : list(bits(8)), offset : int, count : int)
  -> list(bits(8)) = take_restore_bytes(drop_restore_bytes(bytes, offset), count)

function restore_vector_file(bytes : list(bits(8)), offset : int, bytes_per_register : int,
                             index : int, registers : Vector_registers)
  -> Vector_registers =
  if index >= 32 then registers
  else {
    var updated = registers;
    updated[unsigned(get_slice_int(5, index, 0))] =
      restore_byte_slice(bytes, offset + index * bytes_per_register, bytes_per_register);
    restore_vector_file(bytes, offset, bytes_per_register, index + 1, updated)
  }

function restore_predicate_file(bytes : list(bits(8)), offset : int,
                                bytes_per_register : int, index : int,
                                registers : Predicate_registers)
  -> Predicate_registers =
  if index >= 16 then registers
  else {
    var updated = registers;
    updated[unsigned(get_slice_int(4, index, 0))] =
      restore_byte_slice(bytes, offset + index * bytes_per_register, bytes_per_register);
    restore_predicate_file(bytes, offset, bytes_per_register, index + 1, updated)
  }

function restore_vector_component_and_complete(state : Cpu_state, updated : Cpu_state,
                                               bytes : list(bits(8)), bitmap : bits(64))
  -> Execution_result = {
  var candidate = updated;
  if bitmap[1] == bitzero then {
    if state.vector_component_present then {
      candidate.vector_registers = zero_vector_registers(state.vector_length_bytes);
      candidate.predicate_registers = zero_predicate_registers(state.vector_length_bytes);
      candidate.vector_component_modified = false
    } else ();
    completed(state, candidate, CommitMemory, [||])
  }
  else {
    let predicate_bytes = tdiv_int(state.vector_length_bytes, 8);
    let vector_registers = restore_vector_file(
      bytes, state.vector_component_offset, state.vector_length_bytes,
      0, state.vector_registers
    );
    let predicate_registers = restore_predicate_file(
      bytes, state.vector_component_offset + 32 * state.vector_length_bytes,
      predicate_bytes, 0, state.predicate_registers
    );
    candidate.vector_registers = vector_registers;
    candidate.predicate_registers = predicate_registers;
    candidate.vector_component_modified =
      vector_registers != zero_vector_registers(state.vector_length_bytes)
      | predicate_registers != zero_predicate_registers(state.vector_length_bytes);
    completed(state, candidate, CommitMemory, [||])
  }
}

function restore_raw_image(previous : Execution_result, bytes : list(bits(8)),
                           header : bits(64), bitmap : bits(64)) -> Execution_result = {
  let state = previous.state;
  let saved_status = sail_shiftright(header, 36) & 0x000000000000FFFF;
  let saved_flags = sail_shiftright(header, 20) & 0x000000000000FFFF;
  let saved_dfa = header[10] == bitone;
  let invalid_status = state.supervisor
    & (saved_status[4] != bitone
       | not_bool(restored_event_state_valid(state, saved_status, saved_dfa)));
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
          var updated = pending_after(previous);
          updated.registers = registers;
          updated.flags = saved_flags[3 .. 0];
          if state.supervisor then {
            updated.status = saved_status;
            updated.current_dfa = saved_dfa
          } else ();
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
            restore_vector_component_and_complete(state, updated, bytes, bitmap)
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
                restore_vector_component_and_complete(state, updated, bytes, bitmap)
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

function continue_event_return(previous : Execution_result, bytes : list(bits(8)))
  -> Execution_result = match (
    read_le_bits(bytes, 0, 64), read_le_bits(bytes, 8, 64),
    read_le_bits(bytes, 16, 64), read_le_bits(bytes, 24, 64),
    read_le_bits(bytes, 32, 64), read_le_bits(bytes, 40, 64),
    read_le_bits(bytes, 48, 64), read_le_bits(bytes, 56, 64)
  ) {
    (Some(control), Some(event_info), Some(saved_pc), Some(saved_sp), Some(saved_cs),
     Some(saved_ds), Some(saved_ss), Some(_padding)) => {
      let saved_flags = sail_shiftright(control, 32) & 0x000000000000000F;
      let saved_status = sail_shiftright(control, 36) & 0x000000000000FFFF;
      if control != pending_transaction(previous.pending).captured_first
         | byte_list_length(bytes) < unsigned(control[7 .. 0]) * 8
         | event_info[63 .. 32] != 0x00000000
         | saved_flags[15 .. 4] != 0x000
         | saved_status[15 .. 11] != 0b00000
         | saved_status[4] != bitone
         | not_bool(segment_image_valid(saved_cs))
         | not_bool(segment_image_valid(saved_ds))
         | not_bool(segment_image_valid(saved_ss))
         | not_bool(segment_point(saved_cs, saved_pc).in_bounds)
         | not_bool(segment_point(saved_ss, saved_sp).in_bounds) then
        faulted(previous.state, Op_ERET, InvalidControlState,
                "invalid raw event return frame")
      else {
          var candidate = previous.state;
          candidate.flags = saved_flags[3 .. 0];
          candidate.status = saved_status;
          candidate.supervisor = saved_status[4] == bitone;
          candidate.pc = saved_pc;
          candidate.sp = saved_sp;
          candidate.segments[0] = saved_cs;
          candidate.segments[1] = saved_ds;
          candidate.segments[2] = saved_ss;
          candidate.current_dfa = control[12] == bitone;
          candidate.repeat_state = { candidate.repeat_state with active = false };
          candidate.halted = false;
          candidate.run_state = Running;
          let staged = { previous with pending = { previous.pending with after = Some(candidate) } };
          continue_with_request(
            staged, PhaseEventReturnExecute, pending_transaction(previous.pending).ordinal + 1,
            saved_pc, saved_cs,
            target_probe_request(pending_transaction(previous.pending).ordinal + 1, saved_cs, saved_pc)
          )
      }
    },
    _ => faulted(previous.state, Op_ERET, InvalidControlState,
                 "truncated event return frame"),
  }
