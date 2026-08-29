union clause Uop_kind = UopFpState : Fp_state_uop_operation

function clause execute_uop(UopFpState(operation), _, values, instruction, before, speculative) =
    if operation == FpStateReadFlags | operation == FpStateReadStatus then {
        match operand_named(instruction, Operand_dst) {
            None() => uop_step_fault(
                faulted(before, instruction.form.operation, IllegalInstruction,
                        "floating-point state read has no destination"),
            ),
            Some(destination) => {
                var updated = speculative;
                updated.registers[unsigned(destination.value[3 .. 0])] =
                    if operation == FpStateReadFlags
                    then sail_zero_extend(speculative.fflags, 64)
                    else narrow_bits(speculative.fstatus, 2);
                uop_step_continue(updated, values)
            },
        }
    } else match value_named(instruction, speculative, Operand_src) {
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, IllegalInstruction,
                    "floating-point state write has no source"),
        ),
        Some(source) => {
            let reserved = if operation == FpStateWriteFlags
                           then (source & 0x000000000000FFE0) != 0x0000000000000000
                           else (source & 0x000000000000FC00) != 0x0000000000000000;
            if reserved then {
                uop_step_fault(
                    faulted(before, instruction.form.operation, InvalidControlState,
                            "reserved floating-point state bits"),
                )
            } else {
                var updated = speculative;
                if operation == FpStateWriteFlags then updated.fflags = source[4 .. 0]
                else updated.fstatus = source & 0x00000000000003FF;
                updated.fp_component_modified = true;
                uop_step_continue(updated, values)
            }
        },
    }
