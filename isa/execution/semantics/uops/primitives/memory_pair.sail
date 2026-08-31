union clause Uop_kind = UopMemoryLoadPair : unit
union clause Uop_kind = UopMemoryLoadPairComplete : unit
union clause Uop_kind = UopMemoryStorePair : unit

function clause execute_uop(UopMemoryLoadPair(), uop, values, instruction, before, _) =
    match uop_value_get(values, uop.source0.index) {
        Some(address) => uop_step_wait(
            uop.destination.index,
            uop_memory_request_make(MemoryRead, address, 16, AccessLoad,
                                    0x0000000000000000, false),
            0x0000000000000000,
        ),
        None() => uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "pair-load address is unavailable")),
    }

function clause execute_uop(UopMemoryLoadPairComplete(), uop, values, instruction, before, speculative) =
    match uop_value_get(values, uop.source0.index) {
        Some(response) => match uop_location_write(
            uop.destination, response.value, 8, instruction.form.operation, speculative, values
        ) {
            Some((low_state, low_values)) => match uop_location_write(
                { uop.destination with index = uop.destination.index + 1 },
                response.secondary_value, 8, instruction.form.operation, low_state, low_values
            ) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "pair-load high destination is not writable")),
            },
            None() => uop_step_fault(faulted(before, instruction.form.operation,
                InvalidControlState, "pair-load low destination is not writable")),
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "pair-load response is unavailable")),
    }

function clause execute_uop(UopMemoryStorePair(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_value_get(values, uop.source2.index)) {
        (Some(low), Some(high), Some(address)) => uop_step_wait(
            0 - 1,
            { uop_memory_request_make(CompoundMemoryStore, address, 16, AccessStore,
                                      low, true) with auxiliary = high },
            low,
        ),
        _ => uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "pair-store input is unavailable")),
    }
