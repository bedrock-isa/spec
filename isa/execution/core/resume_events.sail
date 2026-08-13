function resume_events_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseEventTargetProbe => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) =>
        if not_bool(event_stack_state_valid(event, previous.pending.before)) then
          event_delivery_failed(previous, 1)
        else if not_bool(event_frame_address_valid(event, previous.pending.before)) then {
          let request = event_stack_range_request(
            event, previous.pending.before, previous.pending.ordinal + 1
          );
          event_delivery_failed({ previous with request = request }, 2)
        }
        else continue_with_request(
          previous, PhaseEventStackProbe, previous.pending.ordinal + 1,
          previous.pending.captured_first, previous.pending.captured_second,
          event_stack_range_request(event, previous.pending.before,
                                    previous.pending.ordinal + 1)
        ),
    },
    PhaseEventStackProbe => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) => continue_with_request(
        previous, PhaseEventFrameStore, previous.pending.ordinal + 1,
        previous.pending.captured_first, previous.pending.captured_second,
        event_frame_store_request(event, previous.pending.before,
                                  previous.pending.ordinal + 1)
      ),
    },
    PhaseEventFrameStore => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) => {
        var updated = previous.pending.before;
        updated.sp = previous.request.range_start;
        updated.pc = previous.pending.before.controls[12];
        updated.segments[0] = previous.pending.before.controls[13];
        updated.segments[1] = previous.pending.before.controls[14];
        updated.segments[2] = previous.request.segment_image;
        updated.status = (previous.pending.before.status & 0x0000000000000002)
                       | 0x0000000000000011;
        if event.kind == EventNmi then {
          updated.status = updated.status | 0x0000000000000002;
          if previous.pending.before.nmi_relatched then {
            updated.controls[2] = updated.controls[2] | 0x0000000000000080;
            updated.nmi_latched_source = previous.pending.before.nmi_relatched_source
          }
          else {
            updated.controls[2] = updated.controls[2] & 0xFFFFFFFFFFFFFF7F;
            updated.nmi_latched_source = 0x000000
          };
          updated.nmi_relatched = false;
          updated.nmi_relatched_source = 0x000000
        } else ();
        if event.code == 0x00000019 then {
          updated.machine_check_pending = false;
          updated.machine_check_payload = 0x00000000;
          updated.machine_check_error_code = 0x0000000000000000;
          updated.machine_check_fault_ea = 0x0000000000000000;
          updated.machine_check_fault_linear = 0x0000000000000000;
          updated.machine_check_event_aux = 0x0000000000000000
        } else ();
        updated.supervisor = true;
        updated.event_depth = previous.pending.before.event_depth + 1;
        updated.event_stack_level = if event_retain_stack(event, previous.pending.before)
          then previous.pending.before.event_stack_level else event_requested_level(event);
        updated.repeat_state = { updated.repeat_state with active = false };
        updated.run_state = Running;
        updated.halted = false;
        let done = completed(previous.pending.before, updated, CommitEvent, [||]);
        { done with pending = { done.pending with boundary_class = BoundaryEventEntry } }
      },
    },
    PhaseEventFrameHeader =>
      let control : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      } in
      if byte_list_length(response.body_bytes) < 8
         | not_bool(valid_frame_control(control, previous.pending.before)) then faulted(
        previous.pending.before, Op_ERET, InvalidControlState, "invalid FRAME_CONTROL"
      )
      else {
        let frame_bytes = unsigned(control[7 .. 0]) * 8;
        let request = { stack_request(
          EventFrameAccess, previous.pending.ordinal + 1, previous.pending.before,
          previous.pending.before.sp,
          add_bits(previous.pending.before.sp, bits_from_int(frame_bytes)),
          AccessStackRead, 0x0000000000000000, false
        ) with selector = 0x0000000000000001, expected = control,
               width = frame_bytes, range_length = frame_bytes,
               state_image = previous.pending.before };
        continue_with_request(
          previous, PhaseEventFrame, previous.pending.ordinal + 1,
          control, 0x0000000000000000, request
        )
      },
    PhaseEventFrame => continue_event_return(previous, response.body_bytes),
    PhaseEventReturnBody => {
      let repeat_state = previous.pending.after.repeat_state;
      let bytes = if repeat_state.grouped then response.body_bytes
                  else match decode_next_record(response.body_bytes) {
                    Some(body) => take_bytes(response.body_bytes, body.encoded_length),
                    None() => [||],
                  };
      let valid : bool = if repeat_state.grouped then
        if byte_list_length(bytes) != unsigned(repeat_state.body_bytes) then false
        else if not_bool(valid_repg_body(
          bytes, unsigned(repeat_state.body_bytes), previous.pending.after
        )) then false
        else repg_offset_is_boundary(bytes, repeat_state.group_progress)
      else match decode_full_record(bytes) {
        Some(body) => {
          let eligible : bool = if unsigned(repeat_state.condition) == 0
            then body.form.repeat_rep else body.form.repeat_repcc;
          if not_bool(eligible) then false
          else if not_bool(repeat_body_available(body, previous.pending.after)) then false
          else not_bool(repeat_body_control_forbidden(body))
        },
        None() => false,
      };
      if not_bool(valid) then faulted(
        previous.pending.before, Op_ERET, InvalidControlState,
        "invalid restored repeat body"
      )
      else {
        var candidate = previous.pending.after;
        candidate.repeat_state = { repeat_state with fixed_body = bytes };
        let staged = { previous with pending = { previous.pending with after = candidate } };
        continue_with_request(
          staged, PhaseEventReturnExecute, previous.pending.ordinal + 1,
          previous.pending.captured_first, previous.pending.captured_second,
          target_probe_request(previous.pending.ordinal + 1,
                               previous.pending.captured_second,
                               previous.pending.captured_first)
        )
      }
    },
    PhaseEventReturnExecute => completed(
      previous.pending.before, previous.pending.after, CommitEvent, [||]
    ),
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
