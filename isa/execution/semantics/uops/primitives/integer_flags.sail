union clause Uop_kind = UopIntegerFlags : Integer_flags_uop_operation

function clause execute_uop(UopIntegerFlags(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let flags : bits(4) = match operation {
                IntegerFlagsCompare => {
                    let (_, generated) = sub_with_flags(left, right, 0, uop.width);
                    generated
                },
                IntegerFlagsTest => {
                    let value = narrow_bits(left & right, uop.width);
                    flags_value(value == 0x0000000000000000, width_sign(value, uop.width), false, false)
                },
            };
            var updated = speculative;
            updated.flags = flags;
            uop_step_continue(updated, values)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
