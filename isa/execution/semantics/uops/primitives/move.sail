union clause Uop_kind = UopMove : unit

function clause execute_uop(UopMove(), uop, values, instruction, before, speculative) =
    match uop_location_value(uop.source0, speculative, values) {
        Some(value) => match uop_write_location(
            uop.destination,
            narrow_bits(value, uop.width),
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
        None() => uop_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable"),
        ),
    }
