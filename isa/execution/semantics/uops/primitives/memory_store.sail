union clause Uop_kind = UopMemoryStore : unit

function clause execute_uop(UopMemoryStore(), uop, program, cursor, values, instruction, before, speculative) =
    match (uop_value_at(values, uop.source1.index), uop_location_value(uop.source0, speculative, values)) {
        (Some(address), Some(value)) => waiting_uop(
            program,
            cursor + 1,
            values,
            0,
            instruction,
            before,
            speculative,
            PhaseUopMemoryWrite,
            uop_memory_request(MemoryStore, address, uop.width, AccessStore, value, true),
            value,
        ),
        _ => faulted(before, instruction.form.operation, InvalidControlState, "uop store input is unavailable"),
    }
