union clause Uop_kind = UopFpContractQuery : unit
union clause Uop_kind = UopFpContractValidate : unit

function clause execute_uop(UopFpContractQuery(), uop, _, instruction, before, _) =
    match fp_semantics(instruction.form.operation) {
        Some(semantics) => uop_wait(
            uop.destination.index,
            {
                empty_primitive_request() with
                kind = CpuidQueryRequest,
                role = RequestRoleFpApproximationContractQuery,
                selector = fp_approx_cpuid_selector(semantics.contract_id),
            },
            0x0000000000000000,
        ),
        None() => uop_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "missing FP approximation semantics"),
        ),
    }

function clause execute_uop(UopFpContractValidate(), uop, values, instruction, before, speculative) =
    match (fp_semantics(instruction.form.operation), uop_value_at(values, uop.source0.index)) {
        (Some(semantics), Some(response)) => {
            let lookup = fp_approx_contract_lookup(semantics.contract_id, response.value);
            if    not_bool(response.known)
               |  lookup.status
               == FpApproxContractUnknown
               |  not_bool(response.present)
               |  lookup.status
               == FpApproxContractAbsent then {
                uop_fault(
                    faulted_with_error_code(
                        before,
                        instruction.form.operation,
                        IllegalInstruction,
                        "FP approximation contract absent or unknown",
                        0x0000000000000003,
                    ),
                )
            } else {
                if lookup.status == FpApproxContractMalformed then {
                    uop_fault(
                        faulted(
                            before,
                            instruction.form.operation,
                            InvalidControlState,
                            "FP approximation contract malformed",
                        ),
                    )
                } else {
                    uop_continue(speculative, values)
                }
            }
        },
        _ => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "FP approximation contract response is unavailable",
            ),
        ),
    }
