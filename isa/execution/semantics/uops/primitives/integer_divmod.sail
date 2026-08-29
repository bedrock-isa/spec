union clause Uop_kind = UopIntegerDivmod : bool

function clause execute_uop(UopIntegerDivmod(signed_operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(dividend), Some(divisor)) => {
            let divisor_u = unsigned(narrow_bits(divisor, uop.width));
            if uop.destination.kind == uop.destination2.kind & uop.destination.index == uop.destination2.index then
                uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction, "DIVMOD destinations overlap"))
            else if divisor_u == 0 then uop_step_fault(faulted(before, instruction.form.operation, DivideByZero, "zero divisor"))
            else if signed_operation & signed_width(dividend, uop.width) == signed_minimum(uop.width)
                 & signed_width(divisor, uop.width) == -1 then
                uop_step_fault(faulted(before, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"))
            else {
                let quotient = if signed_operation then tdiv_int(signed_width(dividend, uop.width), signed_width(divisor, uop.width))
                               else tdiv_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                let remainder = if signed_operation then signed_width(dividend, uop.width) - quotient * signed_width(divisor, uop.width)
                                else tmod_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                match uop_location_write(uop.destination, bits_from_int(quotient), uop.width,
                                         instruction.form.operation, speculative, values) {
                    Some((quotient_state, quotient_values)) => match uop_location_write(
                        uop.destination2, bits_from_int(remainder), uop.width, instruction.form.operation,
                        quotient_state, quotient_values) {
                        Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "remainder destination is not writable")),
                    },
                    None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "quotient destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
