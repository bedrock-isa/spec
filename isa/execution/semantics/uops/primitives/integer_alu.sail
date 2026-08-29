union clause Uop_kind = UopIntegerAlu : Integer_alu_uop_operation

function clause execute_uop(UopIntegerAlu(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let value : bits(64) = match operation {
                IntegerAluSubtract => sub_bits(left, right),
                IntegerAluAnd => left & right,
                IntegerAluOr => left | right,
                IntegerAluXor => xor_vec(left, right),
            };
            match uop_location_write(
                uop.destination,
                narrow_bits(value, uop.width),
                uop.width,
                instruction.form.operation,
                speculative,
                values,
            ) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(
                    faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable"),
                ),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
