
function execute_WRCR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match (
        value_named(instruction, state, Operand_src),
        value_named(instruction, state, Operand_cr),
    ) {
        (Some(source), Some(raw_selector)) => {
            let selector = unsigned(raw_selector[15 .. 0]);
            let needs_transition =    selector
                                   == 0
                                   |  selector
                                   == 1
                                   |  selector
                                   == 272
                                   |  selector
                                   == 4097
                                   |  (selector == 2 & source[0] == bitone & state.controls[2][0] == bitzero)
                                   |  ((selector >= 264 & selector <= 270) &
                                          (state.controls[11][32] == bitone | (selector == 269 & source[32] == bitone)));
            if needs_transition then {
                None()
            } else {
                match control_index(selector) {
                    None() => Some(faulted(state, Op_WRCR, InvalidControlState, "unknown control-register selector")),
                    Some(index) => {
                        let segment_invalid = control_segment_requires_valid_image(selector) &
                                not_bool(segment_image_valid(source));
                        let stack_invalid =    control_pointer_requires_alignment(selector)
                                            &  (source & 0x000000000000003F)
                                            != 0x0000000000000000;
                        let pmc_invalid = selector == 4352 & (source & 0xFFFFFFFFFFFFFFFE) != 0x0000000000000000;
                        let ecr_invalid =    selector
                                          == 2
                                          &  (   (source & 0xFFFFFFFFFFFFF07E)
                                             != 0x0000000000000000
                                             |  (source[0] == bitone & not_bool(event_control_bank_valid(state))));
                        let uctl_invalid =    selector
                                           == 269
                                           &  (   (source & 0xFFFFFFFE00000000)
                                              != 0x0000000000000000
                                              |  (source & 0x00000000FFD10000)
                                              != 0x0000000000000000
                                              |  source[15 .. 4]
                                              != 0x000);
                        let uinfo_invalid = selector == 270 & source[63 .. 32] != 0x00000000;
                        if segment_invalid | stack_invalid | pmc_invalid | ecr_invalid | uctl_invalid | uinfo_invalid then {
                            Some(faulted(state, Op_WRCR, InvalidControlState, "invalid control-register image"))
                        } else {
                            var updated = state;
                            updated.controls[unsigned(index)] =
                                if selector == 2 then {
                                    (source & 0x0000000000000F01) | (state.controls[2] & 0x0000000000000080)
                                } else {
                                    source
                                };
                            Some(local_result(state, instruction, updated, CommitControl))
                        }
                    },
                }
            }
        },
        _ => None(),
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}
