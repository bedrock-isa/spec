union clause Uop_kind = UopIntegerMath : Integer_math_uop_operation

function clause execute_uop(UopIntegerMath(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let value : bits(64) = match operation {
                IntegerMultiplyLow => bits_from_int(unsigned(narrow_bits(left, uop.width)) * unsigned(narrow_bits(right, uop.width))),
                IntegerMultiplyHighUnsigned => product_high(left, right, uop.width, false, false),
                IntegerMultiplyHighSigned => product_high(left, right, uop.width, true, true),
                IntegerMultiplyHighSignedUnsigned => product_high(left, right, uop.width, true, false),
                IntegerCarrylessMultiplyLow => carryless_product(narrow_bits(left, uop.width), narrow_bits(right, uop.width))[63 .. 0],
                IntegerCarrylessMultiplyHigh => carryless_high(carryless_product(narrow_bits(left, uop.width), narrow_bits(right, uop.width)), uop.width),
                IntegerMinimumUnsigned => if unsigned(narrow_bits(left, uop.width)) <= unsigned(narrow_bits(right, uop.width)) then left else right,
                IntegerMaximumUnsigned => if unsigned(narrow_bits(left, uop.width)) >= unsigned(narrow_bits(right, uop.width)) then left else right,
                IntegerMinimumSigned => if signed_width(left, uop.width) <= signed_width(right, uop.width) then left else right,
                IntegerMaximumSigned => if signed_width(left, uop.width) >= signed_width(right, uop.width) then left else right,
            };
            match uop_location_write(uop.destination, narrow_bits(value, uop.width), uop.width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }
