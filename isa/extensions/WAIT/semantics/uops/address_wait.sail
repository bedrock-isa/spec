union clause Uop_kind = UopAddressWait : unit
union clause Uop_kind = UopAddressWake : unit

function clause execute_uop(UopAddressWait(), uop, values, instruction, before, speculative) =
    match (uop_value_get(values, uop.source0.index), uop_location_read(uop.source1, speculative, values)) {
        (Some(address), Some(expected)) => {
            let request = {
                uop_memory_request_make(
                    AddressWait,
                    address,
                    uop.width,
                    AccessLoad,
                    0x0000000000000000,
                    false,
                ) with
                memory_order = 1,
                expected = narrow_bits(expected, uop.width),
            };
            uop_step_wait(0 - 1, request, expected)
        },
        _ => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "WAIT input is unavailable"),
        ),
    }

function clause execute_uop(UopAddressWake(), uop, values, instruction, before, _) =
    match uop_value_get(values, uop.source0.index) {
        Some(address) => uop_step_wait(
            0 - 1,
            uop_memory_request_make(
                AddressWake,
                address,
                1,
                AccessAddressOnly,
                0x0000000000000000,
                true,
            ),
            address.effective_address,
        ),
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "WAKE address is unavailable"),
        ),
    }
