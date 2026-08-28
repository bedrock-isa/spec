function route_environment(
    instruction : Decoded_instruction,
    state : Cpu_state,
    family : Transaction_family,
    kind : Primitive_request_kind,
    effect_kind : Effect_kind,
    commit_kind : Commit_kind,
    suppress_fault : bool,
) -> (
    Execution_result
) = {
    let address : bits(64) = match first_ea_operand(instruction.operands) {
        Some(operand) => operand.value,
        None() => 0x0000000000000000,
    };
    let width = operation_width(instruction);
    let phase = if kind == CacheMaintenanceBlock | kind == PrefetchHint then {
                PhaseCacheMaintenance
            } else {
                if kind == FenceCompletion then {
                    PhaseFenceCompletion
                } else {
                    if kind == TlbInvalidateRequest then {
                        PhaseTlbOperation
                    } else {
                        if kind == TranslationQueryRequest then {
                            PhaseTranslationQuery
                        } else {
                            if kind == ContextSwitchRequest then {
                                PhaseContextSwitch
                            } else {
                                if kind == StateSaveRequest then {
                                    PhaseStateSave
                                } else {
                                    if kind == StateRestoreRequest then {
                                        PhaseStateRestore
                                    } else {
                                        if kind == RepeatBodyFetch then {
                                            PhaseRepeatFetch
                                        } else {
                                            if kind == CpuidQueryRequest then {
                                                PhaseCpuidQuery
                                            } else {
                                                if kind == PerformanceCounterRequest then {
                                                    PhasePerformanceCounter
                                                } else {
                                                    if kind == ControlTransitionRequest then {
                                                        PhaseControlTransition
                                                    } else {
                                                        if kind == ResetSerializeRequest then {
                                                            PhaseResetSerialize
                                                        } else {
                                                            PhaseIntegerExternal
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
            };
    struct {
        state = state,
        pending =
            {
                empty_pending(Some(advance_pc(state, instruction)), instruction.form.operation, commit_kind) with
                destination = commit_destination_for(instruction.operands, width),
                instruction = Some(instruction),
                continuation = pending_for_family(family, {
                    empty_transaction_continuation() with
                    phase = phase,
                }),
            },
        request =
            {
                empty_primitive_request() with
                kind = kind,
                role = RequestRoleNone,
                width = width,
                access = NoTransactionAccess,
                commit_point = true,
                suppress_fault = suppress_fault,
                selector = if kind == ResetSerializeRequest then 0x000000000000003F else 0x0000000000000000,
                expected = if kind == ResetSerializeRequest then state.controls[23] else 0x0000000000000000,
            },
        effects =
            [|typed_effect(effect_kind, instruction, state, address, 0x0000000000000000, width, 0, suppress_fault)|],
        fault = None(),
        awaiting_environment = true,
    }
}

// Legacy control routing removed; instruction-local uops own control assembly.
