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
