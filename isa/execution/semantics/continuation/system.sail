function resume_system_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match pending_transaction(previous.pending).phase {
    PhaseFenceCompletion => completed(
      previous.state, pending_after(previous), previous.pending.kind, [||]
    ),
    PhaseTlbOperation => completed(
      previous.state, pending_after(previous), previous.pending.kind, [||]
    ),
    PhaseTranslationQuery => faulted(
      previous.state, previous.pending.operation, InvalidControlState,
      "opaque translation-query response is not accepted"
    ),
    PhasePteRead => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing PTE-walk continuation"),
      Some(instruction) => {
        let level = unsigned(previous.request.selector);
        let target_level = unsigned(previous.request.expected);
        let raw = response.value;
        let valid = pte_structurally_valid(raw, level);
        if previous.request.role == RequestRolePtqueryPte & level == target_level then
          query_result(previous, raw, valid)
        else if not_bool(valid) then query_result(
          previous, 0x0000000000000000, false
        )
        else if raw[1] == bitzero then {
          if previous.request.role == RequestRolePtqueryPte then
            query_result(previous, 0x0000000000000000, false)
          else {
          let physical = (raw & paging_leaf_pfn_mask(
                            control_register_value(previous.state,
                                                   ControlRegister_BASE_PTCR)))
                       | (previous.request.value & paging_leaf_offset_mask(level));
          query_result(previous, physical, true)
          }
        }
        else {
          let next_level = level - 1;
          let table = raw & paging_next_table_mask(
            control_register_value(previous.state, ControlRegister_BASE_PTCR));
          continue_with_request(
            previous, PhasePteRead, pending_transaction(previous.pending).ordinal + 1,
            pending_transaction(previous.pending).captured_first, pending_transaction(previous.pending).captured_second,
            pte_read_request(previous.state, previous.request.role == RequestRolePtqueryPte,
                             previous.request.value,
                             table, next_level, target_level, pending_transaction(previous.pending).ordinal + 1)
          )
        }
      },
    },
    PhaseContextSwitch => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing context-switch continuation"),
      Some(instruction) => {
        var updated = pending_after(previous);
        updated = control_register_with_value(
          updated, ControlRegister_BASE_PTCR,
          pending_transaction(previous.pending).captured_first);
        updated = control_register_with_value(
          updated, ControlRegister_BASE_ASCR,
          if previous.request.auxiliary == 0x0000000000000001
          then sail_shiftleft(pending_transaction(previous.pending).captured_second & 0x000000000000FFFF, 16)
               | 0x0000000000000001 else 0x0000000000000000);
        completed(previous.state, updated, CommitControl, [||])
      },
    },
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
