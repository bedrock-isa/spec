function resume_transaction_inner(previous : Execution_result, response : Transaction_response) -> Execution_result =
    if not_bool(previous.awaiting_environment) then {
        previous
    } else {
        let response_matches : bool = match uop_continuation_get(previous.pending) {
            Some(continuation) => response_matches_request(previous.request, response.kind),
            None() => response_matches_phase(
                pending_transaction(previous.pending).phase,
                previous.request,
                response.kind,
            ),
        };
        if not_bool(response_matches) then {
            faulted(
                previous.state,
                previous.pending.operation,
                InvalidControlState,
                "transaction response kind mismatch",
            )
        } else {
            if not_bool(response.success) & pending_transaction(previous.pending).phase == PhaseEventTargetProbe then {
                event_delivery_failed(previous, 0)
            } else {
                if not_bool(response.success) & pending_transaction(previous.pending).phase == PhaseEventStackProbe then {
                    event_delivery_failed(previous, 2)
                } else {
                    if not_bool(response.success) & pending_transaction(previous.pending).phase == PhaseEventFrameStore then {
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
                                                match previous.pending.continuation {
                                                  PendingUop(_) => uop_program_resume(previous, response),
                                                  PendingSystem(_) => resume_system_phase(previous, response),
                                                  PendingRepeat(_) => resume_repeat_phase(previous, response),
                                                  PendingEvent(_) => resume_events_phase(previous, response),
                                                  PendingEventReturn(_) => resume_events_phase(previous, response),
                                                  PendingControl(_) => resume_control_phase(previous, response),
                                                  PendingNone(_) => faulted(
                                                    previous.state,
                                                    previous.pending.operation,
                                                    InvalidControlState,
                                                    "missing pending continuation",
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
        match previous.pending.repeat_parent {
            Some(parent) => finish_repeat_single(
                    parent.body,
                    parent.bytes,
                    previous.state,
                    result.state,
                    match uop_continuation_get(previous.pending) {
                        Some(continuation) => continuation.captured,
                        None() => pending_transaction(previous.pending).captured_first,
                    },
                ),
            None() => result,
        }
    }
}
