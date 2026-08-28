union clause Uop_kind = UopMove : unit

function clause execute_uop(UopMove(), uop, program, cursor, values, instruction, before, speculative) =
    match uop_location_value(uop.source0, speculative, values) {
        Some(value) => match uop_write_location(
            uop.destination,
            narrow_bits(value, uop.width),
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
        None() => faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable"),
    }
