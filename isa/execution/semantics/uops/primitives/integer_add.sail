union clause Uop_kind = UopIntegerAdd : unit

function clause execute_uop(UopIntegerAdd(), uop, program, cursor, values, instruction, before, speculative) =
    match (uop_location_value(uop.source0, speculative, values), uop_location_value(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => match uop_write_location(
            uop.destination,
            narrow_bits(add_bits(left, right), uop.width),
            uop.width,
            instruction.form.operation,
            speculative,
            values,
        ) {
            Some((next_state, next_values)) => run_uop_program(
                program,
                cursor + 1,
                next_values,
                instruction,
                before,
                next_state,
            ),
            None() => faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "uop destination is not writable",
            ),
        },
        _ => faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable"),
    }
