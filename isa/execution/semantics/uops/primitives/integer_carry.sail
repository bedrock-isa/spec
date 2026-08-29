union clause Uop_kind = UopIntegerCarry : Integer_carry_uop_operation

function clause execute_uop(UopIntegerCarry(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let carry = if flag_c(speculative.flags) then 1 else 0;
            let generated_result : (bits(64), bits(4)) = match operation {
                IntegerCarryAdd => add_with_flags(left, right, carry, uop.width),
                IntegerCarrySubtract => sub_with_flags(left, right, carry, uop.width),
            };
            let (value, generated) = generated_result;
            match uop_location_write(uop.destination, value, uop.width, instruction.form.operation,
                                     speculative, values) {
                Some((next_state, next_values)) => {
                    var updated = next_state;
                    updated.flags = generated;
                    uop_step_continue(updated, next_values)
                },
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }
