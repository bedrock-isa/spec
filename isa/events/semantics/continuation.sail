function resume_events_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match pending_transaction(previous.pending).phase {
    PhaseEventTargetProbe => match pending_event_record(previous.pending) {
      None() => event_shutdown(previous.state),
      Some(event) =>
        if not_bool(event_stack_state_valid(event, previous.state)) then
          event_delivery_failed(previous, 1)
        else if event_uses_user_bank(previous.state)
           & event_payload_slots(event.frame_type) == 0 then {
          var updated = committed_event_entry(
            previous.state, event,
            event_stack_top(event, previous.state),
            event_stack_segment(event, previous.state)
          );
          if event.kind == EventNmi then {
            if previous.state.nmi_relatched then {
              updated.controls[2] = updated.controls[2] | 0x0000000000000080;
              updated.nmi_latched_source = previous.state.nmi_relatched_source
            }
            else {
              updated.controls[2] = updated.controls[2] & 0xFFFFFFFFFFFFFF7F;
              updated.nmi_latched_source = 0x000000
            };
            updated.nmi_relatched = false;
            updated.nmi_relatched_source = 0x000000
          } else ();
          let done = completed(previous.state, updated, CommitEvent, [||]);
          { done with pending = { done.pending with boundary_class = BoundaryEventEntry } }
        }
        else if not_bool(event_frame_address_valid(event, previous.state)) then {
          let request = event_stack_range_request(
            event, previous.state, pending_transaction(previous.pending).ordinal + 1
          );
          event_delivery_failed({ previous with request = request }, 2)
        }
        else continue_with_request(
          previous, PhaseEventStackProbe, pending_transaction(previous.pending).ordinal + 1,
          pending_transaction(previous.pending).captured_first, pending_transaction(previous.pending).captured_second,
          event_stack_range_request(event, previous.state,
                                    pending_transaction(previous.pending).ordinal + 1)
        ),
    },
    PhaseEventStackProbe => match pending_event_record(previous.pending) {
      None() => event_shutdown(previous.state),
      Some(event) => continue_with_request(
        previous, PhaseEventFrameStore, pending_transaction(previous.pending).ordinal + 1,
        pending_transaction(previous.pending).captured_first, pending_transaction(previous.pending).captured_second,
        event_frame_store_request(event, previous.state,
                                  pending_transaction(previous.pending).ordinal + 1)
      ),
    },
    PhaseEventFrameStore => match pending_event_record(previous.pending) {
      None() => event_shutdown(previous.state),
      Some(event) => {
        var updated = committed_event_entry(
          previous.state, event,
          previous.request.range_start, previous.request.segment_image
        );
        if event.kind == EventNmi then {
          if previous.state.nmi_relatched then {
            updated.controls[2] = updated.controls[2] | 0x0000000000000080;
            updated.nmi_latched_source = previous.state.nmi_relatched_source
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
        let done = completed(previous.state, updated, CommitEvent, [||]);
        { done with pending = { done.pending with boundary_class = BoundaryEventEntry } }
      },
    },
    PhaseEventFrameHeader =>
      let control : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      } in
      if byte_list_length(response.body_bytes) < 8
         | not_bool(valid_frame_control(control, previous.state)) then faulted(
        previous.state, Op_ERET, InvalidControlState, "invalid FRAME_CONTROL"
      )
      else {
        let frame_bytes = unsigned(control[7 .. 0]) * 8;
        let request = { stack_request(
          EventFrameAccess, pending_transaction(previous.pending).ordinal + 1, previous.state,
          previous.state.sp,
          add_bits(previous.state.sp, bits_from_int(frame_bytes)),
          AccessStackRead, 0x0000000000000000, false
        ) with selector = 0x0000000000000001, expected = control,
               width = frame_bytes, range_length = frame_bytes };
        continue_with_request(
          previous, PhaseEventFrame, pending_transaction(previous.pending).ordinal + 1,
          control, 0x0000000000000000, request
        )
      },
    PhaseEventFrame => continue_event_return(previous, response.body_bytes),
    PhaseEventReturnExecute => completed(
      previous.state, pending_after(previous), CommitEvent, [||]
    ),
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
