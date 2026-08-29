union clause Uop_kind = UopIntegerExtend : Integer_extend_uop_operation

function clause execute_uop(UopIntegerExtend(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(source) => {
            let value = if operation == IntegerExtendSigned then sign_extend_width(source, uop.width)
                        else narrow_bits(source, uop.width);
            let destination_width = unsigned(uop.auxiliary.immediate);
            match uop_location_write(uop.destination, value, destination_width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "uop source is unavailable")),
    }
