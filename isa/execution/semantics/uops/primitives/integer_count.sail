union clause Uop_kind = UopIntegerCount : Integer_count_uop_operation

function clause execute_uop(UopIntegerCount(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(source) => {
            let narrowed = narrow_bits(source, uop.width);
            let bits = width_bits(uop.width);
            let count : int = match operation {
                IntegerCountLeadingZero => count_from_high(narrowed, bits, bitzero),
                IntegerCountLeadingOne => count_from_high(narrowed, bits, bitone),
                IntegerCountTrailingZero => count_from_low(narrowed, 0, bits, bitzero),
                IntegerCountTrailingOne => count_from_low(narrowed, 0, bits, bitone),
                IntegerCountPopulation => bit_count_from(narrowed, 0, bits),
                IntegerCountParity => tmod_int(bit_count_from(narrowed, 0, bits), 2),
                IntegerReverseBytes => unsigned(reverse_bytes(narrowed, uop.width)),
                IntegerReverseBits => unsigned(reverse_bits(narrowed, uop.width)),
            };
            let destination_width = if operation == IntegerReverseBytes | operation == IntegerReverseBits
                then uop.width else 8;
            match uop_location_write(uop.destination, bits_from_int(count), destination_width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "uop source is unavailable")),
    }
