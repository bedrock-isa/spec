union clause Uop_kind = UopMemoryProbe : unit

function clause execute_uop(UopMemoryProbe(), uop, values, instruction, before, _) =
    match uop_value_at(values, uop.source0.index) {
        Some(address) => uop_wait(
            0 - 1,
            uop_memory_request(MemoryProbe, address, uop.width, AccessStore, 0x0000000000000000, false),
            0x0000000000000000,
        ),
        None() => uop_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop probe address is unavailable"),
        ),
    }
