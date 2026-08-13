function resume_repeat_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseRepeatFetch => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing repeat continuation"),
      Some(prefix) => {
        let repeat_context = previous.pending.after.repeat_state;
        let bytes = if response.body_bytes == [||] then repeat_context.fixed_body
                    else response.body_bytes;
        let same_body = repeat_context.fixed_body == [||] | bytes == repeat_context.fixed_body;
        if not_bool(same_body) then faulted(
          previous.pending.before, prefix.form.operation,
          InvalidControlState, "repeat body changed after entry"
        )
        else if repeat_context.grouped then {
          let length = unsigned(repeat_context.body_bytes);
          if length == 0 | byte_list_length(bytes) != length
             | not_bool(valid_repg_body(bytes, length, previous.pending.before))
          then faulted(previous.pending.before, Op_REPG,
                       IllegalInstruction, "invalid REPG body boundary or eligibility")
          else if repeat_context.remaining == 0x0000000000000000 then {
            var updated = previous.pending.after;
            updated.repeat_state = { repeat_context with active = false, fixed_body = bytes };
            updated.pc = add_bits(repeat_context.body_start, bits_from_int(length));
            let done = completed(previous.pending.before, updated, CommitControl, [||]);
            { done with pending = { done.pending with boundary_class = BoundaryRepeatGroup } }
          }
          else {
            var iteration_state = previous.pending.after;
            iteration_state.pc = repeat_context.body_start;
            iteration_state.repeat_state = { repeat_context with fixed_body = bytes };
            run_repeat_group_tail(bytes, bytes, length, iteration_state)
          }
        }
        else match decode_full_record(bytes) {
          None() => faulted(previous.pending.before, Op_REPcc,
                            IllegalInstruction, "malformed REPcc body"),
          Some(body) =>
            if not_bool(if unsigned(repeat_context.condition) == 0
                        then body.form.repeat_rep else body.form.repeat_repcc)
               | not_bool(repeat_body_available(body, previous.pending.before))
               | repeat_body_control_forbidden(body)
            then faulted(previous.pending.before, Op_REPcc,
                         IllegalInstruction, "ineligible REPcc body")
            else if byte_list_length(bytes) != body.encoded_length then faulted(
              previous.pending.before, Op_REPcc, IllegalInstruction,
              "REPcc body fetch must contain exactly one record"
            )
            else if repeat_context.remaining == 0x0000000000000000 then {
              var updated = previous.pending.after;
              updated.repeat_state = { repeat_context with active = false, fixed_body = bytes };
              updated.pc = add_bits(repeat_context.body_start, bits_from_int(body.encoded_length));
              let done = completed(previous.pending.before, updated, CommitControl, [||]);
              { done with pending = {
                  done.pending with boundary_class = BoundaryRepeatIteration } }
            }
            else {
              var iteration_state = previous.pending.after;
              iteration_state.pc = repeat_context.body_start;
              iteration_state.repeat_state = { repeat_context with fixed_body = bytes };
              run_repeat_single(body, bytes, iteration_state)
            },
        }
      },
    },
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
