union clause Uop_kind = UopMemoryProbe : unit
union clause Uop_kind = UopAtomicIssue : Atomic_uop_operation
union clause Uop_kind = UopAtomicComplete : Atomic_uop_operation
union clause Uop_kind = UopCacheTranslate : Cache_uop_operation
union clause Uop_kind = UopCacheMaintain : Cache_uop_operation
union clause Uop_kind = UopNonTemporalStore : unit

function uop_cache_selector(operation : Cache_uop_operation) -> bits(64) =
    if operation == CacheFlushData then 0x0000000000000000
    else if operation == CacheInvalidateData then 0x0000000000000001
    else if operation == CacheInvalidateInstruction then 0x0000000000000002
    else if operation == CacheWriteBackData then 0x0000000000000003
    else if operation == CacheSynchronize then 0x0000000000000004
    else if operation == CachePrefetchNonTemporal then 0x0000000000000006
    else 0x0000000000000005

function uop_cache_prefetch_p(operation : Cache_uop_operation) -> bool =
    operation == CachePrefetch | operation == CachePrefetchNonTemporal

function clause execute_uop(UopMemoryProbe(), uop, values, instruction, before, _) =
    match uop_value_get(values, uop.source0.index) {
        Some(address) => uop_step_wait(
            0 - 1,
            uop_memory_request_make(MemoryProbe, address, uop.width, AccessStore, 0x0000000000000000, false),
            0x0000000000000000,
        ),
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop probe address is unavailable"),
        ),
    }

function clause execute_uop(UopCacheTranslate(operation), uop, values, instruction, before, speculative) =
    match uop_value_get(values, uop.source0.index) {
        Some(address) => {
            let request = { uop_memory_request_make(AddressTranslateRequest, address, 8, AccessAddressOnly,
                                                0x0000000000000000, false) with
                role = RequestRoleCacheTranslate,
                suppress_fault = uop_cache_prefetch_p(operation),
                selector = uop_cache_selector(operation),
                auxiliary = speculative.cache_maintenance_granule };
            uop_step_wait(uop.destination.index, request, address.effective_address)
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "cache address is unavailable")),
    }

function clause execute_uop(UopCacheMaintain(operation), uop, values, instruction, before, speculative) =
    match uop_value_get(values, uop.source0.index) {
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "cache translation result is unavailable")),
        Some(translated) => {
            let prefetch = uop_cache_prefetch_p(operation);
            let granule = unsigned(speculative.cache_maintenance_granule);
            let physical = translated.value;
            let block_start = physical & not_vec(bits_from_int(granule - 1));
            if prefetch & translated.access_class == MmioAccess then uop_step_continue(speculative, values)
            else {
                let request = { empty_primitive_request() with
                    kind = if prefetch then PrefetchHint else CacheMaintenanceBlock,
                    role = if prefetch then RequestRolePhysicalPrefetch else RequestRolePhysicalCacheBlock,
                    width = 8,
                    range_start = if prefetch then physical else block_start,
                    range_end = if prefetch then add_bits(physical, 0x0000000000000001)
                                else add_bits(block_start, bits_from_int(granule)),
                    range_length = if prefetch then 1 else granule,
                    effective_address = physical, linear_address = physical,
                    access = AccessAddressOnly, address_translation = false, commit_point = true,
                    cache_policy = translated.cache_policy, suppress_fault = prefetch,
                    selector = uop_cache_selector(operation) };
                uop_step_wait(0 - 1, request, physical)
            }
        },
    }

function clause execute_uop(UopNonTemporalStore(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_value_get(values, uop.source1.index)) {
        (Some(value), Some(address)) => uop_step_wait(0 - 1,
            uop_memory_request_make(NonTemporalStore, address, uop.width, AccessStore, value, true), value),
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "non-temporal store input is unavailable")),
    }

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
