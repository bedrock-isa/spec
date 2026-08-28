union clause Uop_kind = UopMove : unit
union clause Uop_kind = UopPredicateValue : unit
union clause Uop_kind = UopRegisterPairMove : unit

function clause execute_uop(UopMove(), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(value) => match uop_location_write(
            uop.destination,
            narrow_bits(value, uop.width),
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
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable"),
        ),
    }

function clause execute_uop(UopPredicateValue(), uop, values, instruction, before, speculative) = {
    let value : bits(64) = if predicate_holds(instruction, speculative)
        then 0x0000000000000001 else 0x0000000000000000;
    match uop_location_write(uop.destination, value, uop.width,
                             instruction.form.operation, speculative, values) {
        Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
        None() => uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "predicate destination is not writable")),
    }
}

function clause execute_uop(UopRegisterPairMove(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values)) {
        (Some(first), Some(second)) => match uop_location_write(
            uop.destination, first, uop.width, instruction.form.operation, speculative, values) {
            Some((first_state, first_values)) => match uop_location_write(
                uop.destination2, second, uop.width, instruction.form.operation,
                first_state, first_values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "second pair destination is not writable")),
            },
            None() => uop_step_fault(faulted(before, instruction.form.operation,
                InvalidControlState, "first pair destination is not writable")),
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "pair source is unavailable")),
    }
