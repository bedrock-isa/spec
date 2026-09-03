function response_matches_request(
    request : Primitive_request,
    kind : Transaction_response_kind,
) -> bool =
    match request.kind {
        TranslationExecuteProbe => kind == ResponseTranslation,
        MemoryProbe => kind == ResponseProbe,
        Read => kind == ResponseRead,
        Write => kind == ResponseWrite,
        StackRange => kind == ResponseStackRange,
        SegmentBoundsPoint => kind == ResponseSegmentBounds,
        Atomic => kind == ResponseAtomic,
        AddressWake => kind == ResponseAddressWake,
        AddressTranslateRequest => kind == ResponseAddressTranslation,
        PhysicalPteRead => kind == ResponsePteRead,
        CacheMaintenanceBlock => kind == ResponseCacheMaintenance,
        PrefetchHint => kind == ResponseCacheMaintenance,
        FenceCompletion => kind == ResponseFenceCompletion,
        TlbInvalidateRequest => kind == ResponseTlbOperation,
        TranslationQueryRequest => kind == ResponseTranslationQuery,
        ContextSwitchRequest => kind == ResponseContextSwitch,
        RepeatBodyFetch => kind == ResponseRepeatFetch,
        EventFrameAccess => kind == ResponseEventFrame,
        CpuidQueryRequest => kind == ResponseCpuidQuery,
        PerformanceCounterRequest => kind == ResponsePerformanceCounter,
        ControlTransitionRequest => kind == ResponseControlTransition,
        ResetSerializeRequest => kind == ResponseResetSerialize,
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
        PhaseDestinationProbe => if request.kind == Read then {
            kind == ResponseRead
        } else {
            if request.kind == MemoryProbe then {
                kind == ResponseProbe
            } else {
                false
            }
        },
        PhaseDestinationWrite => kind == ResponseWrite,
        PhaseMemoryWriteFirst => kind == ResponseWrite,
        PhaseMemoryWriteSecond => kind == ResponseWrite,
        PhaseTargetRead => kind == ResponseRead,
        PhaseTargetExecuteProbe => kind == ResponseTranslation,
        PhaseStackRange => kind == ResponseStackRange,
        PhaseStackReadFirst => kind == ResponseRead,
        PhaseStackReadSecond => kind == ResponseRead,
        PhaseStackWriteFirst => kind == ResponseWrite,
        PhaseIntegerExternal => kind == ResponseIntegerExternal,
        PhaseCacheTranslate => kind == ResponseAddressTranslation,
        PhaseCacheMaintenance => kind == ResponseCacheMaintenance,
        PhaseFenceCompletion => kind == ResponseFenceCompletion,
        PhaseTlbOperation => kind == ResponseTlbOperation,
        PhaseTranslationQuery => kind == ResponseTranslationQuery,
        PhasePteRead => kind == ResponsePteRead,
        PhaseContextSwitch => kind == ResponseContextSwitch,
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
    &  (request.kind == Read | request.kind == Write | request.kind == MemoryProbe)
    &  request.range_length == request.width
    &  request.selector == 0x0000000000000000
    &  (request.width == 1 | request.width == 2 | request.width == 4 | request.width == 8)
}

function mmio_naturally_aligned(request : Primitive_request) -> bool =
    request.width > 0 & tmod_int(unsigned(request.linear_address), request.width) == 0
