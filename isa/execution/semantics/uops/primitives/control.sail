union clause Uop_kind = UopControlTarget : bool
union clause Uop_kind = UopControlProbe : unit
union clause Uop_kind = UopControlCommit : Control_transfer_uop_operation
union clause Uop_kind = UopFusedJump : Fused_jump_uop_operation

function clause execute_uop(UopControlTarget(relative), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(raw) => {
            let target = if relative then add_bits(next_pc(speculative, instruction), raw)
                         else narrow_bits(raw, uop.width);
            match uop_location_write(uop.destination, target, 64, instruction.form.operation,
                                     speculative, values) {
                Some((updated, next_values)) => uop_step_continue(updated, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                            "control target destination is unavailable")),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "control target is unavailable")),
    }

function clause execute_uop(UopControlProbe(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values)) {
        (Some(target), Some(cs_image)) =>
            if not_bool(segment_image_valid(cs_image)) then
                uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                  "invalid target code segment"))
            else uop_step_wait(0 - 1, target_probe_request(0, cs_image, target), target),
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "control probe input is unavailable")),
    }

function clause execute_uop(UopControlCommit(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "control commit target is unavailable")),
        Some(target) => {
            var updated = speculative; updated.pc = target;
            if operation == ControlFarJump | operation == ControlFarCall | operation == ControlFarReturn then
                match uop_location_read(uop.source1, speculative, values) {
                    Some(cs_image) => if segment_image_valid(cs_image) then updated.segments[0] = cs_image
                                      else return uop_step_fault(faulted(before, instruction.form.operation,
                                                       InvalidControlState, "invalid target code segment")),
                    None() => return uop_step_fault(faulted(before, instruction.form.operation,
                                                       InvalidControlState, "missing target code segment")),
                }
            else ();
            uop_step_complete_control(updated, CommitControl)
        },
    }

function clause execute_uop(UopFusedJump(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values), condition_field(instruction.fields)) {
        (Some(source), Some(destination), Some(relative), Some(condition)) => {
            let width = uop.width;
            let temporary_flags = if operation == FusedCompareJump then {
                let (_, flags) = sub_with_flags(destination, source, 0, width); flags
            } else {
                let value = narrow_bits(integer_and_value(destination, source), width);
                flags_value(value == 0x0000000000000000, width_sign(value, width), false, false)
            };
            var updated = speculative;
            updated.pc = if condition_holds(condition, temporary_flags)
                         then add_bits(next_pc(speculative, instruction), relative)
                         else next_pc(speculative, instruction);
            uop_step_complete_control(updated, CommitControl)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "fused conditional jump operands are unavailable")),
    }
