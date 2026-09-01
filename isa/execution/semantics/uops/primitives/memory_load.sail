union clause Uop_kind = UopMemoryLoad : unit
union clause Uop_kind = UopMemoryLoadAcquire : unit

function clause execute_uop(UopMemoryLoad(), uop, values, instruction, before, _) =
    match uop_value_get(values, uop.source0.index) {
        Some(address) => uop_step_wait(
            uop.destination.index,
            uop_memory_request_make(Read, address, uop.width, AccessLoad, 0x0000000000000000, false),
            0x0000000000000000,
        ),
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop load address is unavailable"),
        ),
    }

function clause execute_uop(UopMemoryLoadAcquire(), uop, values, instruction, before, _) =
    match uop_value_get(values, uop.source0.index) {
        Some(address) => uop_step_wait(
            uop.destination.index,
            { uop_memory_request_make(Read, address, uop.width, AccessLoad,
                                      0x0000000000000000, false) with memory_order = 1 },
            0x0000000000000000,
        ),
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState,
                    "acquire-load address is unavailable"),
        ),
    }
