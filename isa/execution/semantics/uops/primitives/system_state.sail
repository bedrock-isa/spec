union clause Uop_kind = UopSystemState : System_state_uop_operation

function clause execute_uop(UopSystemState(operation), _, _, instruction, before, speculative) = {
    if operation == SystemReadControl then match (value_named(instruction, speculative, Operand_cr),
                                                   destination_named(instruction, Operand_dst, 8)) {
        (Some(raw), Some(destination)) => match control_register_from_selector(unsigned(raw[15 .. 0])) {
            Some(control) => uop_step_complete(write_local_destination(speculative, instruction.form.operation,
                                                                 destination, control_register_value(speculative, control)),
                                        CommitRegisters),
            None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlSelectorFault,
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
            match control_register_from_selector(selector) {
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlSelectorFault,
                                            "unknown control-register selector")),
                Some(control) => {
                    if control_register_write_needs_transition(control, source, speculative) then
                      uop_step_delegate(start_system_request(
                        SystemWriteControl, instruction, speculative
                      ))
                    else {
                      let written = control_register_written_value(
                        control, source, speculative
                      );
                      let candidate = control_register_with_value(
                        speculative, control, written
                      );
                      match control_register_write_fault(
                        control, source, speculative, candidate
                      ) {
                        Some(kind) => uop_step_fault(faulted(
                          before, instruction.form.operation, kind,
                          "invalid control-register write"
                        )),
                        None() => uop_step_complete(candidate, CommitControl),
                      }
                    }
                },
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "WRCR operands are unavailable")),
    }
}
