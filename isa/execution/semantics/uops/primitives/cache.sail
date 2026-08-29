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
