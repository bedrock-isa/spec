union clause Uop_kind = UopIntegerAdd : unit

function clause execute_uop(UopIntegerAdd(), uop, values, instruction, before, speculative) =
    match (uop_location_value(uop.source0, speculative, values), uop_location_value(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => match uop_write_location(
            uop.destination,
            narrow_bits(add_bits(left, right), uop.width),
            uop.width,
            instruction.form.operation,
            speculative,
            values,
        ) {
            Some((next_state, next_values)) => uop_continue(next_state, next_values),
            None() => uop_fault(
                faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable"),
            ),
        },
        _ => uop_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
