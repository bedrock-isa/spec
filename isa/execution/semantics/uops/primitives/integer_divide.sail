union clause Uop_kind = UopIntegerDivide : Integer_divide_uop_operation

function clause execute_uop(UopIntegerDivide(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(dividend), Some(divisor)) => {
            let divisor_u = unsigned(narrow_bits(divisor, uop.width));
            let signed_operation = operation == IntegerDivideSigned | operation == IntegerRemainderSigned;
            if divisor_u == 0 then uop_step_fault(faulted(before, instruction.form.operation, DivideByZero, "zero divisor"))
            else if signed_operation & signed_width(dividend, uop.width) == signed_minimum(uop.width)
                 & signed_width(divisor, uop.width) == -1 then
                uop_step_fault(faulted(before, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"))
            else {
                let quotient = if signed_operation then tdiv_int(signed_width(dividend, uop.width), signed_width(divisor, uop.width))
                               else tdiv_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                let remainder = if signed_operation then signed_width(dividend, uop.width) - quotient * signed_width(divisor, uop.width)
                                else tmod_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                let result = if operation == IntegerRemainderUnsigned | operation == IntegerRemainderSigned then remainder else quotient;
                match uop_location_write(uop.destination, bits_from_int(result), uop.width,
                                         instruction.form.operation, speculative, values) {
                    Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                    None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
