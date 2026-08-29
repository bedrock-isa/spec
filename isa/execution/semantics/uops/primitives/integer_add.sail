union clause Uop_kind = UopIntegerAdd : unit

function clause execute_uop(UopIntegerAdd(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => match uop_location_write(
            uop.destination,
            narrow_bits(add_bits(left, right), uop.width),
            uop.width,
            instruction.form.operation,
            speculative,
            values,
        ) {
            Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
            None() => uop_step_fault(
                faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable"),
            ),
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
