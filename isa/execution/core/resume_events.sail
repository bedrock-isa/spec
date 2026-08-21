function resume_events_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseEventTargetProbe => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) =>
        if not_bool(event_stack_state_valid(event, previous.pending.before)) then
          event_delivery_failed(previous, 1)
        else if event_uses_user_bank(previous.pending.before)
           & event_payload_slots(event.frame_type) == 0 then {
          var updated = committed_event_entry(
            previous.pending.before, event,
            event_stack_top(event, previous.pending.before),
            event_stack_segment(event, previous.pending.before)
          );
          if event.kind == EventNmi then {
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
          let done = completed(previous.pending.before, updated, CommitEvent, [||]);
          { done with pending = { done.pending with boundary_class = BoundaryEventEntry } }
        }
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
        var updated = committed_event_entry(
          previous.pending.before, event,
          previous.request.range_start, previous.request.segment_image
        );
        if event.kind == EventNmi then {
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
    PhaseEventReturnExecute => completed(
      previous.pending.before, previous.pending.after, CommitEvent, [||]
    ),
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
