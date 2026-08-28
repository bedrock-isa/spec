union clause Uop_kind = UopMemoryLoad : unit

function clause execute_uop(UopMemoryLoad(), uop, values, instruction, before, _) =
    match uop_value_at(values, uop.source0.index) {
        Some(address) => uop_wait(
            uop.destination.index,
            uop_memory_request(MemoryRead, address, uop.width, AccessLoad, 0x0000000000000000, false),
            0x0000000000000000,
        ),
        None() => uop_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop load address is unavailable"),
        ),
    }
