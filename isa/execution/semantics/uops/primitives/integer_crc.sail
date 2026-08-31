union clause Uop_kind = UopIntegerCrc : Integer_crc_uop_operation

function crc_reflected_bits(crc : bits(64), remaining : int, polynomial : bits(64)) -> bits(64) =
    if remaining <= 0 then crc & 0x00000000FFFFFFFF
    else {
        let shifted = sail_shiftright(crc, 1);
        let next = if crc[0] == bitone then xor_vec(shifted, polynomial) else shifted;
        crc_reflected_bits(next, remaining - 1, polynomial)
    }

function crc_reflected_bytes(crc : bits(64), source : bits(64), remaining : int,
                             polynomial : bits(64)) -> bits(64) =
    if remaining <= 0 then crc & 0x00000000FFFFFFFF
    else {
        let next = crc_reflected_bits(xor_vec(crc, source & 0x00000000000000FF), 8, polynomial);
        crc_reflected_bytes(next, sail_shiftright(source, 8), remaining - 1, polynomial)
    }

function clause execute_uop(UopIntegerCrc(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values)) {
        (Some(source), Some(accumulator)) => {
            let polynomial = if operation == IntegerCrc32
                then 0x00000000EDB88320 else 0x0000000082F63B78;
            let result = crc_reflected_bytes(accumulator & 0x00000000FFFFFFFF,
                narrow_bits(source, uop.width), uop.width, polynomial);
            match uop_location_write(uop.destination, result, 4,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "CRC destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation,
                                    InvalidControlState, "CRC input is unavailable")),
    }
