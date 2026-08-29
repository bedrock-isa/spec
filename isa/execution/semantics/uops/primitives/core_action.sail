union clause Uop_kind = UopCoreAction : Core_action_uop_operation

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
