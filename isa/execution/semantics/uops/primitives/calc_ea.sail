union clause Uop_kind = UopCalcEa : unit

function clause execute_uop(UopCalcEa(), uop, program, cursor, values, instruction, before, speculative) =
    match operand_named(instruction, uop.operand_name) {
        None() => faulted(before, instruction.form.operation, IllegalInstruction, "uop EA operand is missing"),
        Some(operand) => match operand.ea {
            None() => faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "uop EA operand has no decoded EA",
            ),
            Some(ea) => {
                let plain = { ea with update_target = None(),  update_mode = None() };
                let (evaluation, _) = evaluate_decoded_ea(operand, plain, speculative, before.pc, uop.width);
                let address : Uop_value = struct {
                        value = evaluation.effective_address,
                        address = true,
                        segment = evaluation.segment,
                        segment_image = evaluation.segment_image,
                        effective_address = evaluation.effective_address,
                        linear_address = evaluation.linear_address,
                        domain = request_domain_for_operand(evaluation.domain),
                    };
                run_uop_program(
                    program,
                    cursor + 1,
                    uop_value_set(values, uop.destination.index, address),
                    instruction,
                    before,
                    speculative,
                )
            },
        },
    }
