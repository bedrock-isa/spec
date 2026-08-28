union clause Uop_kind = UopMemoryStore : unit

function clause execute_uop(UopMemoryStore(), uop, values, instruction, before, speculative) =
    match (uop_value_at(values, uop.source1.index), uop_location_value(uop.source0, speculative, values)) {
        (Some(address), Some(value)) => uop_wait(
            0 - 1,
            uop_memory_request(MemoryStore, address, uop.width, AccessStore, value, true),
            value,
        ),
        _ => uop_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop store input is unavailable"),
        ),
    }
