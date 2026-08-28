union clause Uop_kind = UopCommit : unit
union clause Uop_kind = UopCoreAction : Core_action_uop_operation
union clause Uop_kind = UopEnvironment : Environment_uop_operation
union clause Uop_kind = UopSystemRequest : System_request_uop_operation
union clause Uop_kind = UopSystemState : System_state_uop_operation
union clause Uop_kind = UopTlbContext : Tlb_context_uop_operation

function clause execute_uop(UopCommit(), uop, _, _, _, speculative) =
    uop_step_complete(speculative, uop.commit_kind)

function clause execute_uop(UopCoreAction(operation), uop, values, instruction, before, speculative) =
    if operation == CoreActionIllegal then
        uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction, "explicit ILLEGAL"))
    else if operation == CoreActionHalt then {
        var updated = speculative;
        updated.halted = true;
        updated.run_state = Halted;
        uop_step_complete_with_effects(updated, CommitControl, [|typed_effect(
            HaltProcessor, instruction, before, 0x0000000000000000,
            0x0000000000000000, 0, 0, false)|])
    } else if operation == CoreActionTrace then
        match uop_location_read(uop.source0, speculative, values) {
            Some(marker) => uop_step_complete_with_effects(speculative, CommitControl, [|typed_effect(
                TraceMarker, instruction, before, before.pc, marker, 2, 0, false)|]),
            None() => uop_step_fault(faulted(before, instruction.form.operation,
                                        InvalidControlState, "TRACE marker is unavailable")),
        }
    else uop_step_complete_with_effects(speculative, CommitControl, [|typed_effect(
        NoEffect, instruction, before, 0x0000000000000000,
        0x0000000000000000, 0, 0, false)|])

function clause execute_uop(UopEnvironment(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(route_environment(instruction, speculative, operation.family,
        operation.request_kind, operation.effect_kind, operation.commit_kind,
        operation.suppress_fault))

function clause execute_uop(UopSystemRequest(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(start_system_request(operation, instruction, speculative))

function clause execute_uop(UopSystemState(operation), _, _, instruction, before, speculative) = {
    if operation == SystemReadControl then match (value_named(instruction, speculative, Operand_cr),
                                                   destination_named(instruction, Operand_dst, 8)) {
        (Some(raw), Some(destination)) => match control_index(unsigned(raw[15 .. 0])) {
            Some(index) => uop_step_complete(write_local_destination(speculative, instruction.form.operation,
                                                                 destination, speculative.controls[unsigned(index)]),
                                        CommitRegisters),
            None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                        "unknown control-register selector")),
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "RDCR operands are unavailable")),
    }
    else if operation == SystemReadFlags then match destination_named(instruction, Operand_dst, 8) {
        Some(destination) => uop_step_complete(write_local_destination(speculative, instruction.form.operation,
            destination, sail_zero_extend(speculative.flags, 64)), CommitRegisters),
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "RDFLAGS destination is unavailable")),
    }
    else if operation == SystemReadSegment then match (operand_named(instruction, Operand_seg),
                                                        destination_named(instruction, Operand_dst, 8)) {
        (Some(segment), Some(destination)) => uop_step_complete(write_local_destination(
            speculative, instruction.form.operation, destination, speculative.segments[sreg_index(segment)]),
            CommitRegisters),
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "RDSEG operands are unavailable")),
    }
    else if operation == SystemReadStatus then match destination_named(instruction, Operand_dst, 8) {
        Some(destination) => uop_step_complete(write_local_destination(speculative, instruction.form.operation,
            destination, narrow_bits(speculative.status, 2)), CommitRegisters),
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "RDSTATUS destination is unavailable")),
    }
    else if operation == SystemSetFlags then match value_named(instruction, speculative, Operand_mask) {
        Some(mask) => uop_step_complete({ speculative with flags = mask[3 .. 0] }, CommitRegisters),
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "SETF mask is unavailable")),
    }
    else if operation == SystemWriteFlags then match value_named(instruction, speculative, Operand_src) {
        Some(source) => if (source & 0x000000000000FFF0) != 0x0000000000000000 then
            uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction, "reserved FLAGS bits"))
          else uop_step_complete({ speculative with flags = source[3 .. 0] }, CommitRegisters),
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "WRFLAGS source is unavailable")),
    }
    else if operation == SystemWriteSegment then match (value_named(instruction, speculative, Operand_src),
                                                         operand_named(instruction, Operand_seg)) {
        (Some(source), Some(segment)) => if not_bool(segment_image_valid(source)) then
            uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "invalid segment image"))
          else { var updated = speculative; updated.segments[sreg_index(segment)] = source;
                 uop_step_complete(updated, CommitRegisters) },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "WRSEG operands are unavailable")),
    }
    else if operation == SystemWriteStatus then match value_named(instruction, speculative, Operand_src) {
        Some(source) => {
            let candidate = source & 0x000000000000FFFF;
            if (candidate & 0x000000000000F800) != 0x0000000000000000
               | (candidate & 0x00000000000007D1) != (speculative.status & 0x00000000000007D1) then
                uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                  "reserved or immutable STATUS bits"))
            else uop_step_complete({ speculative with status = candidate }, CommitRegisters)
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "WRSTATUS source is unavailable")),
    }
    else match (value_named(instruction, speculative, Operand_src),
                value_named(instruction, speculative, Operand_cr)) {
        (Some(source), Some(raw_selector)) => {
            let selector = unsigned(raw_selector[15 .. 0]);
            let needs_transition = selector == 0 | selector == 1 | selector == 272 | selector == 4097
              | (selector == 2 & source[0] == bitone & speculative.controls[2][0] == bitzero)
              | ((selector >= 264 & selector <= 270)
                 & (speculative.controls[11][32] == bitone | (selector == 269 & source[32] == bitone)));
            if needs_transition then uop_step_delegate(start_system_request(
                SystemWriteControl, instruction, speculative))
            else match control_index(selector) {
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                            "unknown control-register selector")),
                Some(index) => {
                    let invalid = (control_segment_requires_valid_image(selector) & not_bool(segment_image_valid(source)))
                      | (control_pointer_requires_alignment(selector) & (source & 0x000000000000003F) != 0x0000000000000000)
                      | (selector == 4352 & (source & 0xFFFFFFFFFFFFFFFE) != 0x0000000000000000)
                      | (selector == 2 & ((source & 0xFFFFFFFFFFFFF07E) != 0x0000000000000000
                                         | (source[0] == bitone & not_bool(event_control_bank_valid(speculative)))))
                      | (selector == 269 & ((source & 0xFFFFFFFE00000000) != 0x0000000000000000
                                            | (source & 0x00000000FFD10000) != 0x0000000000000000
                                            | source[15 .. 4] != 0x000))
                      | (selector == 270 & source[63 .. 32] != 0x00000000);
                    if invalid then uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                                      "invalid control-register image"))
                    else { var updated = speculative;
                      updated.controls[unsigned(index)] = if selector == 2 then
                        (source & 0x0000000000000F01) | (speculative.controls[2] & 0x0000000000000080)
                        else source;
                      uop_step_complete(updated, CommitControl) }
                },
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "WRCR operands are unavailable")),
    }
}

function clause execute_uop(UopTlbContext(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(start_tlb_context_transaction(operation, instruction, speculative))
