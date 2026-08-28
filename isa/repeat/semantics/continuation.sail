function resume_repeat_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseRepeatFetch => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing repeat prefix"),
      Some(prefix) => {
        let repeat_context = pending_after(previous).repeat_state;
        let bytes = if response.body_bytes == [||] then repeat_context.fixed_body
                    else response.body_bytes;
        let same_body = repeat_context.fixed_body == [||] | bytes == repeat_context.fixed_body;
        if not_bool(same_body) then faulted(
          previous.state, prefix.form.operation,
          InvalidControlState, "repeat body changed after entry"
        )
        else match decode_full_record(bytes) {
          None() => faulted(previous.state, Op_REPcc,
                            IllegalInstruction, "malformed REPcc body"),
          Some(body) =>
            if not_bool(if unsigned(repeat_context.condition) == 0
                        then body.form.repeat_rep else body.form.repeat_repcc)
               | not_bool(repeat_body_available(body, previous.state))
               | repeat_body_control_forbidden(body)
            then faulted(previous.state, Op_REPcc,
                         IllegalInstruction, "ineligible REPcc body")
            else if byte_list_length(bytes) != body.encoded_length then faulted(
              previous.state, Op_REPcc, IllegalInstruction,
              "REPcc body fetch must contain exactly one record"
            )
            else if repeat_context.remaining == 0x0000000000000000 then {
              var updated = pending_after(previous);
              updated.repeat_state = { repeat_context with active = false, fixed_body = bytes };
              updated.pc = add_bits(repeat_context.body_start, bits_from_int(body.encoded_length));
              let done = completed(previous.state, updated, CommitControl, [||]);
              { done with pending = {
                  done.pending with boundary_class = BoundaryRepeatIteration } }
            }
            else {
              var iteration_state = pending_after(previous);
              iteration_state.pc = repeat_context.body_start;
              iteration_state.repeat_state = { repeat_context with fixed_body = bytes };
              run_repeat_single(body, bytes, iteration_state)
            },
        }
      },
    },
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
