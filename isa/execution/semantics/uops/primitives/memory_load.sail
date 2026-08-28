union clause Uop_kind = UopMemoryLoad : unit

function clause execute_uop(UopMemoryLoad(), uop, program, cursor, values, instruction, before, speculative) =
    match uop_value_at(values, uop.source0.index) {
        Some(address) => waiting_uop(
            program,
            cursor + 1,
            values,
            uop.destination.index,
            instruction,
            before,
            speculative,
            PhaseUopMemoryRead,
            uop_memory_request(MemoryRead, address, uop.width, AccessLoad, 0x0000000000000000, false),
            0x0000000000000000,
        ),
        None() => faulted(before, instruction.form.operation, InvalidControlState, "uop load address is unavailable"),
    }
