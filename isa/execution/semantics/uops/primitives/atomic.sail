union clause Uop_kind = UopAtomicIssue : Atomic_uop_operation
union clause Uop_kind = UopAtomicComplete : Atomic_uop_operation

function uop_atomic_selector(operation : Atomic_uop_operation) -> bits(64) = match operation {
    AtomicCompareExchange => 0x0000000000000000,
    AtomicFetchAdd => 0x0000000000000001,
    AtomicFetchAnd => 0x0000000000000002,
    AtomicFetchOr => 0x0000000000000003,
    AtomicFetchSubtract => 0x0000000000000004,
    AtomicFetchXor => 0x0000000000000005,
}

function clause execute_uop(UopAtomicIssue(operation), uop, values, instruction, before, speculative) =
    match (uop_value_get(values, uop.source0.index),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values),
           uop_location_read(uop.auxiliary, speculative, values)) {
        (Some(address), Some(first), Some(second), Some(order_value)) => {
            let compare = operation == AtomicCompareExchange;
            let request = { uop_memory_request_make(AtomicReadModifyWrite, address, uop.width,
                AccessReadModifyWrite, if compare then 0x0000000000000000 else first, true) with
                memory_order = unsigned(order_value[2 .. 0]),
                selector = uop_atomic_selector(operation),
                expected = if compare then narrow_bits(first, uop.width) else 0x0000000000000000,
                desired = if compare then narrow_bits(second, uop.width) else 0x0000000000000000 };
            uop_step_wait(uop.destination.index, request, first)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "atomic uop input is unavailable")),
    }

function clause execute_uop(UopAtomicComplete(operation), uop, values, instruction, before, speculative) =
    match (uop_value_get(values, uop.source0.index),
           uop_location_read(uop.source1, speculative, values)) {
        (Some(response), Some(expected)) => {
            let compare = operation == AtomicCompareExchange;
            let equal = narrow_bits(response.value, uop.width) == narrow_bits(expected, uop.width);
            if compare & response.atomic_store_happened != equal then
                uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                  "inconsistent CMPXCHG atomic acknowledgement"))
            else if not_bool(compare) & not_bool(response.atomic_store_happened) then
                uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                  "atomic operation did not acknowledge its store"))
            else match uop_location_write(uop.destination, response.value, uop.width,
                                           instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => {
                    var updated = next_state;
                    if compare then updated.flags = flags_value(equal, false, false, false) else ();
                    uop_step_continue(updated, next_values)
                },
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                            "atomic destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "atomic response is unavailable")),
    }
