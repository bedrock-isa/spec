function response_matches_request(
    request : Primitive_request,
    kind : Transaction_response_kind,
) -> bool =
    match request.kind {
        TranslationExecuteProbe => kind == ResponseTranslation,
        MemoryProbe => kind == ResponseProbe,
        MemoryRead => kind == ResponseRead,
        MemoryStore => kind == ResponseStoreAck,
        CompoundMemoryStore => kind == ResponseStoreAck,
        NonTemporalStore => kind == ResponseStoreAck,
        StackRange => kind == ResponseStackRange,
        SegmentBoundsPoint => kind == ResponseSegmentBounds,
        AtomicReadModifyWrite => kind == ResponseAtomic,
        AddressWait => kind == ResponseAddressWait,
        AddressWake => kind == ResponseAddressWake,
        AddressTranslateRequest => kind == ResponseAddressTranslation,
        PhysicalPteRead => kind == ResponsePteRead,
        CacheMaintenanceBlock => kind == ResponseCacheMaintenance,
        PrefetchHint => kind == ResponseCacheMaintenance,
        FenceCompletion => kind == ResponseFenceCompletion,
        TlbInvalidateRequest => kind == ResponseTlbOperation,
        TranslationQueryRequest => kind == ResponseTranslationQuery,
        ContextSwitchRequest => kind == ResponseContextSwitch,
        StateSaveRequest => kind == ResponseStateSave,
        StateRestoreRequest => kind == ResponseStateRestore,
        RepeatBodyFetch => kind == ResponseRepeatFetch,
        EventFrameAccess => kind == ResponseEventFrame,
        CpuidQueryRequest => kind == ResponseCpuidQuery,
        PerformanceCounterRequest => kind == ResponsePerformanceCounter,
        ControlTransitionRequest => kind == ResponseControlTransition,
        ResetSerializeRequest => kind == ResponseResetSerialize,
        VectorMemoryRead => kind == ResponseVectorMemory,
        VectorMemoryWrite => kind == ResponseVectorMemory,
        ExternalIntegerRequest => kind == ResponseIntegerExternal,
        NoPrimitiveRequest => false,
    }

function response_matches_phase(
    phase : Continuation_phase,
    request : Primitive_request,
    kind : Transaction_response_kind,
) -> (
    bool
) =
    match phase {
        PhaseSourceRead => kind == ResponseRead,
        PhaseDestinationProbe => if request.kind == MemoryRead then {
            kind == ResponseRead
        } else {
            if request.kind == MemoryProbe then {
                kind == ResponseProbe
            } else {
                false
            }
        },
        PhaseDestinationWrite => kind == ResponseStoreAck,
        PhaseMemoryWriteFirst => kind == ResponseStoreAck,
        PhaseMemoryWriteSecond => kind == ResponseStoreAck,
        PhaseTargetRead => kind == ResponseRead,
        PhaseTargetExecuteProbe => kind == ResponseTranslation,
        PhaseStackRange => kind == ResponseStackRange,
        PhaseStackReadFirst => kind == ResponseRead,
        PhaseStackReadSecond => kind == ResponseRead,
        PhaseStackWriteFirst => kind == ResponseStoreAck,
        PhaseIntegerExternal => kind == ResponseIntegerExternal,
        PhaseCacheTranslate => kind == ResponseAddressTranslation,
        PhaseCacheMaintenance => kind == ResponseCacheMaintenance,
        PhaseFenceCompletion => kind == ResponseFenceCompletion,
        PhaseTlbOperation => kind == ResponseTlbOperation,
        PhaseTranslationQuery => kind == ResponseTranslationQuery,
        PhasePteRead => kind == ResponsePteRead,
        PhaseContextSwitch => kind == ResponseContextSwitch,
        PhaseStateSave => kind == ResponseStateSave,
        PhaseStateRestoreHeader => kind == ResponseStateRestore,
        PhaseStateRestoreRange => kind == ResponseStateRestore,
        PhaseStateRestore => kind == ResponseStateRestore,
        PhaseRepeatFetch => kind == ResponseRepeatFetch,
        PhaseEventFrameHeader => kind == ResponseEventFrame,
        PhaseEventFrame => kind == ResponseEventFrame,
        PhaseEventTargetProbe => kind == ResponseTranslation,
        PhaseEventStackProbe => kind == ResponseStackRange,
        PhaseEventFrameStore => kind == ResponseEventFrame,
        PhaseEventReturnExecute => kind == ResponseTranslation,
        PhaseCpuidQuery => kind == ResponseCpuidQuery,
        PhasePerformanceCounter => kind == ResponsePerformanceCounter,
        PhaseControlTransition => kind == ResponseControlTransition,
        PhaseResetSerialize => kind == ResponseResetSerialize,
        ContinuationNone => false,
        _ => false,
    }

function transaction_faulted(previous : Execution_result, kind : Fault_kind, detail : string) -> Execution_result =
    struct {
        state = previous.state,
        pending = previous.pending,
        request = previous.request,
        effects = [||],
        fault =
            Some(
                struct {
                    kind = kind,
                    operation = previous.pending.operation,
                    detail = detail,
                    error_code = if kind == AccessFault then 0x0000000047000000 else 0x0000000000000000,
                    bus_error = kind == AccessFault,
                },
            ),
        debug_stop = None(),
        awaiting_environment = false,
    }

function address_context_error_code(request : Primitive_request, cause : int) -> bits(64) = {
    let access : int = if request.access == AccessLoad | request.access == AccessStackRead then {
            1
        } else {
            if    request.access
               == AccessStore
               |  request.access
               == AccessReadModifyWrite
               |  request.access
               == AccessStackWrite then {
                2
            } else {
                if request.access == AccessExecute then { 3 } else { 0 }
            }
        };
    let size : int = if request.width == 1 then {
            1
        } else {
            if request.width == 2 then {
                2
            } else {
                if request.width == 4 then { 3 } else { if request.width == 8 then { 4 } else { 0 } }
            }
        };
      bits_from_int(cause)
    | sail_shiftleft(bits_from_int(access), 8)
    | (if request.domain == RequestDomainUser then 0x0000000000000400 else 0x0000000000000000)
    | (if request.access == AccessReadModifyWrite then 0x0000000000000800 else 0x0000000000000000)
    | sail_shiftleft(bits_from_int(size), 27)
}

function architectural_memory_fault(
    previous : Execution_result,
    kind : Fault_kind,
    cause : int,
    detail : string,
) -> (
    Execution_result
) =
    struct {
        state = previous.state,
        pending = previous.pending,
        request = previous.request,
        effects = [||],
        fault =
            Some(
                struct {
                    kind = kind,
                    operation = previous.pending.operation,
                    detail = detail,
                    error_code = address_context_error_code(previous.request, cause),
                    bus_error = false,
                },
            ),
        debug_stop = None(),
        awaiting_environment = false,
    }

function mmio_scalar_request(previous : Execution_result) -> bool = {
    let request = previous.request;
       previous.pending.repeat_parent == None()
    &  request.kind
    != VectorMemoryRead
    &  request.kind
    != VectorMemoryWrite
    &  (   request.kind
       == MemoryRead
       |  request.kind
       == MemoryStore
       |  request.kind
       == MemoryProbe
       |  request.kind
       == NonTemporalStore)
    &  (request.width == 1 | request.width == 2 | request.width == 4 | request.width == 8)
}

function mmio_naturally_aligned(request : Primitive_request) -> bool =
    request.width > 0 & tmod_int(unsigned(request.linear_address), request.width) == 0
