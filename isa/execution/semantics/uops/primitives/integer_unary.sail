union clause Uop_kind = UopIntegerUnary : Integer_unary_uop_operation

function clause execute_uop(UopIntegerUnary(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(source) => {
            let value : bits(64) = match operation {
                IntegerUnaryNegate => sub_bits(0x0000000000000000, source),
                IntegerUnaryComplement => not_vec(source),
                IntegerUnaryIncrement => add_bits(source, 0x0000000000000001),
                IntegerUnaryDecrement => sub_bits(source, 0x0000000000000001),
                IntegerUnaryIncrementFlags => add_bits(source, 0x0000000000000001),
                IntegerUnaryDecrementFlags => sub_bits(source, 0x0000000000000001),
                IntegerUnaryAbsolute => if width_sign(source, uop.width) then
                    sub_bits(0x0000000000000000, source) else source,
            };
            match uop_location_write(
                uop.destination,
                narrow_bits(value, uop.width),
                uop.width,
                instruction.form.operation,
                speculative,
                values,
            ) {
                Some((next_state, next_values)) => {
                    var updated = next_state;
                    if operation == IntegerUnaryIncrementFlags then {
                        let (_, generated) = add_with_flags(source, 0x0000000000000001, 0, uop.width);
                        updated.flags = generated
                    } else if operation == IntegerUnaryDecrementFlags then {
                        let (_, generated) = sub_with_flags(source, 0x0000000000000001, 0, uop.width);
                        updated.flags = generated
                    } else ();
                    uop_step_continue(updated, next_values)
                },
                None() => uop_step_fault(
                    faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable"),
                ),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }
