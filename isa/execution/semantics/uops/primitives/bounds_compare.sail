union clause Uop_kind = UopBoundsCompare : Bounds_uop_operation

function clause execute_uop(UopBoundsCompare(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values)) {
        (Some(low), Some(value), Some(high)) => {
            let low_value = if operation.signed_operation then signed_width(low, uop.width)
                            else unsigned(narrow_bits(low, uop.width));
            let tested_value = if operation.signed_operation then signed_width(value, uop.width)
                               else unsigned(narrow_bits(value, uop.width));
            let high_value = if operation.signed_operation then signed_width(high, uop.width)
                             else unsigned(narrow_bits(high, uop.width));
            let below = if operation.inclusive_low then tested_value < low_value else tested_value <= low_value;
            let above = if operation.inclusive_high then tested_value > high_value else tested_value >= high_value;
            var updated = speculative;
            updated.flags = flags_value(false, false, false, below | above);
            uop_step_continue(updated, values)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "bounds input is unavailable")),
    }
