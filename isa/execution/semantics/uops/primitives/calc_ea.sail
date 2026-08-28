union clause Uop_kind = UopCalcEa : unit

function clause execute_uop(UopCalcEa(), uop, values, instruction, before, speculative) =
    match operand_named(instruction, uop.operand_name) {
        None() => uop_fault(
            faulted(before, instruction.form.operation, IllegalInstruction, "uop EA operand is missing"),
        ),
        Some(operand) => match operand.ea {
            None() => uop_fault(
                faulted(before, instruction.form.operation, IllegalInstruction, "uop EA operand has no decoded EA"),
            ),
            Some(ea) => {
                let plain = { ea with update_target = None(),  update_mode = None() };
                let (evaluation, _) = evaluate_decoded_ea(operand, plain, speculative, before.pc, uop.width);
                let address : Uop_value = struct {
                        value = evaluation.effective_address,
                        secondary_value = 0x0000000000000000,
                        flags = 0x0,
                        write_flags = false,
                        generated_fflags = 0b00000,
                        bounds_passed = false,
                        cache_policy = 0,
                        access_class = NormalAccess,
                        physical_class = NormalPhysical,
                        atomic_store_happened = false,
                        body_bytes = [||],
                        known = false,
                        present = false,
                        address = true,
                        segment = evaluation.segment,
                        segment_image = evaluation.segment_image,
                        effective_address = evaluation.effective_address,
                        linear_address = evaluation.linear_address,
                        domain = request_domain_for_operand(evaluation.domain),
                    };
                uop_continue(speculative, uop_value_set(values, uop.destination.index, address))
            },
        },
    }
