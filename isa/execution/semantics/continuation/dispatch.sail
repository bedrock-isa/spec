function resume_transaction_inner(previous : Execution_result, response : Transaction_response) -> Execution_result =
    if not_bool(previous.awaiting_environment) then {
        previous
    } else {
        if not_bool(response_matches_phase(previous.pending.phase, previous.request, response.kind)) then {
            faulted(
                previous.state,
                previous.pending.operation,
                InvalidControlState,
                "transaction response kind mismatch",
            )
        } else {
            if not_bool(response.success) & previous.pending.phase == PhaseEventTargetProbe then {
                event_delivery_failed(previous, 0)
            } else {
                if not_bool(response.success) & previous.pending.phase == PhaseEventStackProbe then {
                    event_delivery_failed(previous, 2)
                } else {
                    if not_bool(response.success) & previous.pending.phase == PhaseEventFrameStore then {
                        event_delivery_failed(previous, 3)
                    } else {
                        if not_bool(response.success) & previous.request.suppress_fault then {
                            completed(previous.state, pending_after(previous), previous.pending.kind, [||])
                        } else {
                            if not_bool(response.success) &
                                (response.fault_kind == TranslationFault | response.fault_kind == AccessFault) then {
                                architectural_memory_fault(
                                    previous,
                                    response.fault_kind,
                                    response.fault_cause,
                                    response.detail,
                                )
                            } else {
                                if not_bool(response.success) then {
                                    transaction_faulted(previous, response.fault_kind, response.detail)
                                } else {
                                    if    previous.request.address_translation
                                       &  response.physical_class
                                       == DevicePhysical
                                       &  response.access_class
                                       == NormalAccess then {
                                        architectural_memory_fault(
                                            previous,
                                            TranslationFault,
                                            6,
                                            "Normal access class selected Device physical memory",
                                        )
                                    } else {
                                        if    previous.request.address_translation
                                           &  response.access_class
                                           == MmioAccess
                                           &  not_bool(mmio_scalar_request(previous))
                                           &  not_bool(previous.request.suppress_fault) then {
                                            architectural_memory_fault(
                                                previous,
                                                AccessFault,
                                                2,
                                                "operation is not permitted for MMIO",
                                            )
                                        } else {
                                            if    previous.request.address_translation
                                               &  response.access_class
                                               == MmioAccess
                                               &  not_bool(mmio_naturally_aligned(previous.request))
                                               &  not_bool(previous.request.suppress_fault) then {
                                                architectural_memory_fault(
                                                    previous,
                                                    AccessFault,
                                                    1,
                                                    "MMIO scalar is not naturally aligned",
                                                )
                                            } else {
                                                match previous.pending.phase {
                                                    PhaseSourceRead => resume_memory_phase(previous, response),
                                                    PhaseDestinationProbe => resume_memory_phase(previous, response),
                                                    PhaseDestinationWrite => resume_memory_phase(previous, response),
                                                    PhaseMemoryWriteFirst => resume_memory_phase(previous, response),
                                                    PhaseMemoryWriteSecond => resume_memory_phase(previous, response),
                                                    PhaseAtomicRmw => resume_memory_phase(previous, response),
                                                    PhaseTargetRead => resume_control_phase(previous, response),
                                                    PhaseTargetExecuteProbe => resume_control_phase(previous, response),
                                                    PhaseStackRange => resume_control_phase(previous, response),
                                                    PhaseStackWriteFirst => resume_control_phase(previous, response),
                                                    PhaseStackReadFirst => resume_control_phase(previous, response),
                                                    PhaseStackReadSecond => resume_control_phase(previous, response),
                                                    PhaseCpuidQuery => resume_control_phase(previous, response),
                                                    PhasePerformanceCounter => resume_control_phase(previous, response),
                                                    PhaseControlTransition => resume_control_phase(previous, response),
                                                    PhaseResetSerialize => resume_control_phase(previous, response),
                                                    PhaseIntegerExternal => resume_control_phase(previous, response),
                                                    PhaseCacheTranslate => resume_system_phase(previous, response),
                                                    PhaseCacheMaintenance => resume_system_phase(previous, response),
                                                    PhaseFenceCompletion => resume_system_phase(previous, response),
                                                    PhaseTlbOperation => resume_system_phase(previous, response),
                                                    PhaseTranslationQuery => resume_system_phase(previous, response),
                                                    PhasePteRead => resume_system_phase(previous, response),
                                                    PhaseContextSwitch => resume_system_phase(previous, response),
                                                    PhaseStateSave => resume_system_phase(previous, response),
                                                    PhaseStateRestoreHeader => resume_system_phase(previous, response),
                                                    PhaseStateRestoreRange => resume_system_phase(previous, response),
                                                    PhaseStateRestore => resume_system_phase(previous, response),
                                                    PhaseRepeatFetch => resume_repeat_phase(previous, response),
                                                    PhaseEventTargetProbe => resume_events_phase(previous, response),
                                                    PhaseEventStackProbe => resume_events_phase(previous, response),
                                                    PhaseEventFrameStore => resume_events_phase(previous, response),
                                                    PhaseEventFrameHeader => resume_events_phase(previous, response),
                                                    PhaseEventFrame => resume_events_phase(previous, response),
                                                    PhaseEventReturnExecute => resume_events_phase(previous, response),
                                                    PhaseUopWait => resume_uop_phase(previous, response),
                                                    ContinuationNone => faulted(
                                                        previous.state,
                                                        previous.pending.operation,
                                                        InvalidControlState,
                                                        "unexpected transaction phase",
                                                    ),
                                                    _ => faulted(
                                                        previous.state,
                                                        previous.pending.operation,
                                                        InvalidControlState,
                                                        "unexpected transaction phase",
                                                    ),
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

function resume_transaction(previous : Execution_result, response : Transaction_response) -> Execution_result = {
    let result = resume_transaction_inner(previous, response);
    if result.awaiting_environment | result.fault != None() then {
        result
    } else {
        if previous.pending.repeat_parent_active then {
            match previous.pending.repeat_body {
                None() => faulted(
                    previous.state,
                    previous.pending.operation,
                    InvalidControlState,
                    "missing repeat parent body",
                ),
                Some(body) => finish_repeat_single(
                    body,
                    previous.pending.repeat_bytes,
                    previous.state,
                    result.state,
                    previous.pending.captured_first,
                ),
            }
        } else {
            result
        }
    }
}
