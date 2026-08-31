union clause Uop_kind = UopIntegerBitfield : Integer_bitfield_uop_operation

function bitfield_low_mask(count : int) -> bits(64) =
    if count >= 64 then 0xFFFFFFFFFFFFFFFF
    else sail_shiftright(0xFFFFFFFFFFFFFFFF, 64 - count)

function clause execute_uop(UopIntegerBitfield(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values)) {
        (Some(source), Some(raw_offset), Some(raw_width_minus1)) => {
            let offset = unsigned(raw_offset[5 .. 0]);
            let count = unsigned(raw_width_minus1[5 .. 0]) + 1;
            let operation_bits = uop.width * 8;
            if offset + count > operation_bits then
                uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                       "bitfield range exceeds the selected width"))
            else {
                let low_mask = bitfield_low_mask(count);
                let extracted = sail_shiftright(narrow_bits(source, uop.width), offset) & low_mask;
                let value : bits(64) = if operation == IntegerBitfieldExtractUnsigned then extracted
                    else if operation == IntegerBitfieldExtractSigned then {
                        let sign = sail_shiftleft(0x0000000000000001, count - 1);
                        if (extracted & sign) != 0x0000000000000000
                            then extracted | not_vec(low_mask) else extracted
                    }
                    else match uop_location_read(uop.destination, speculative, values) {
                        Some(destination) => {
                            let positioned_mask = sail_shiftleft(low_mask, offset);
                            (destination & not_vec(positioned_mask))
                            | (sail_shiftleft(source & low_mask, offset) & positioned_mask)
                        },
                        None() => 0x0000000000000000,
                    };
                match uop_location_write(uop.destination, narrow_bits(value, uop.width), uop.width,
                                         instruction.form.operation, speculative, values) {
                    Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                    None() => uop_step_fault(faulted(before, instruction.form.operation,
                        InvalidControlState, "bitfield destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "bitfield input is unavailable")),
    }
