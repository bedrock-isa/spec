union clause Uop_kind = UopIntegerShift : Integer_shift_uop_operation

function clause execute_uop(UopIntegerShift(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(value), Some(count)) => {
            let kind : Shift_kind = match operation {
                IntegerShiftLeft => ShiftLeft,
                IntegerShiftRight => ShiftRightLogical,
                IntegerShiftArithmeticRight => ShiftRightArithmetic,
                IntegerRotateLeft => RotateLeft,
                IntegerRotateRight => RotateRight,
            };
            match uop_location_write(uop.destination, shift_result(kind, value, count, uop.width),
                                     uop.width, instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }
