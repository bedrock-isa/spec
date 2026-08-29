union clause Uop_kind = UopIntegerBit : Integer_bit_uop_operation

function clause execute_uop(UopIntegerBit(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(old), Some(raw_index)) => {
            let mask = sail_shiftleft(0x0000000000000001, unsigned(raw_index[5 .. 0]));
            let selected = narrow_bits(old, uop.width);
            var updated = speculative;
            updated.flags = flags_value((selected & mask) == 0x0000000000000000, false, false, false);
            if operation == IntegerBitTest then uop_step_continue(updated, values)
            else {
                let value : bits(64) = match operation {
                    IntegerBitSet => selected | mask,
                    IntegerBitClear => selected & not_vec(mask),
                    IntegerBitChange => xor_vec(selected, mask),
                    IntegerBitTest => selected,
                };
                match uop_location_write(uop.destination, value, uop.width,
                                         instruction.form.operation, updated, values) {
                    Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                    None() => uop_step_fault(faulted(before, instruction.form.operation,
                        InvalidControlState, "uop destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }
