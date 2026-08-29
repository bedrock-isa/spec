union clause Uop_kind = UopIntegerExtract : unit

function clause execute_uop(UopIntegerExtract(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values)) {
        (Some(low), Some(high), Some(offset_value)) => {
            let offset = unsigned(offset_value[6 .. 0]);
            let value : bits(64) = if offset >= width_bits(uop.width) * 2 then 0x0000000000000000
                else sail_shiftright(concatenated_pair(high, low, uop.width), offset)[63 .. 0];
            match uop_location_write(uop.destination, narrow_bits(value, uop.width), uop.width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
