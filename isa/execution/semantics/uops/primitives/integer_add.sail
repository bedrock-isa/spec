union clause Uop_kind = UopIntegerAdd : unit

union clause Uop_kind = UopIntegerAlu : Integer_alu_uop_operation
union clause Uop_kind = UopIntegerUnary : Integer_unary_uop_operation
union clause Uop_kind = UopIntegerFlags : Integer_flags_uop_operation
union clause Uop_kind = UopIntegerCarry : Integer_carry_uop_operation
union clause Uop_kind = UopIntegerShift : Integer_shift_uop_operation
union clause Uop_kind = UopIntegerBit : Integer_bit_uop_operation
union clause Uop_kind = UopIntegerCount : Integer_count_uop_operation
union clause Uop_kind = UopIntegerExtend : Integer_extend_uop_operation
union clause Uop_kind = UopIntegerMath : Integer_math_uop_operation
union clause Uop_kind = UopIntegerDivide : Integer_divide_uop_operation
union clause Uop_kind = UopIntegerDivmod : bool
union clause Uop_kind = UopIntegerExtract : unit
union clause Uop_kind = UopBoundsCompare : Bounds_uop_operation

function clause execute_uop(UopIntegerAdd(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => match uop_location_write(
            uop.destination,
            narrow_bits(add_bits(left, right), uop.width),
            uop.width,
            instruction.form.operation,
            speculative,
            values,
        ) {
            Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
            None() => uop_step_fault(
                faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable"),
            ),
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }

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

function clause execute_uop(UopIntegerFlags(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let flags : bits(4) = match operation {
                IntegerFlagsCompare => {
                    let (_, generated) = sub_with_flags(left, right, 0, uop.width);
                    generated
                },
                IntegerFlagsTest => {
                    let value = narrow_bits(left & right, uop.width);
                    flags_value(value == 0x0000000000000000, width_sign(value, uop.width), false, false)
                },
            };
            var updated = speculative;
            updated.flags = flags;
            uop_step_continue(updated, values)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerCarry(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let carry = if flag_c(speculative.flags) then 1 else 0;
            let generated_result : (bits(64), bits(4)) = match operation {
                IntegerCarryAdd => add_with_flags(left, right, carry, uop.width),
                IntegerCarrySubtract => sub_with_flags(left, right, carry, uop.width),
            };
            let (value, generated) = generated_result;
            match uop_location_write(uop.destination, value, uop.width, instruction.form.operation,
                                     speculative, values) {
                Some((next_state, next_values)) => {
                    var updated = next_state;
                    updated.flags = generated;
                    uop_step_continue(updated, next_values)
                },
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerShift(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(value), Some(count)) => {
            let kind : Shift_kind = match operation {
                IntegerShiftLeft => ShiftLeft,
                IntegerShiftRight => ShiftRightLogical,
                IntegerShiftArithmeticRight => ShiftRightArithmetic,
                IntegerRotateLeft => RotateLeft,
                IntegerRotateRight => RotateRight,
            };
            match uop_location_write(uop.destination, shift_result(kind, value, count, uop.width),
                                     uop.width, instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerBit(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(old), Some(raw_index)) => {
            let mask = sail_shiftleft(0x0000000000000001, unsigned(raw_index[5 .. 0]));
            let selected = narrow_bits(old, uop.width);
            var updated = speculative;
            updated.flags = flags_value((selected & mask) == 0x0000000000000000, false, false, false);
            if operation == IntegerBitTest then uop_step_continue(updated, values)
            else {
                let value : bits(64) = match operation {
                    IntegerBitSet => selected | mask,
                    IntegerBitClear => selected & not_vec(mask),
                    IntegerBitChange => xor_vec(selected, mask),
                    IntegerBitTest => selected,
                };
                match uop_location_write(uop.destination, value, uop.width,
                                         instruction.form.operation, updated, values) {
                    Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                    None() => uop_step_fault(faulted(before, instruction.form.operation,
                        InvalidControlState, "uop destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerCount(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(source) => {
            let narrowed = narrow_bits(source, uop.width);
            let bits = width_bits(uop.width);
            let count : int = match operation {
                IntegerCountLeadingZero => count_from_high(narrowed, bits, bitzero),
                IntegerCountLeadingOne => count_from_high(narrowed, bits, bitone),
                IntegerCountTrailingZero => count_from_low(narrowed, 0, bits, bitzero),
                IntegerCountTrailingOne => count_from_low(narrowed, 0, bits, bitone),
                IntegerCountPopulation => bit_count_from(narrowed, 0, bits),
                IntegerCountParity => tmod_int(bit_count_from(narrowed, 0, bits), 2),
                IntegerReverseBytes => unsigned(reverse_bytes(narrowed, uop.width)),
            };
            let destination_width = if operation == IntegerReverseBytes then uop.width else 8;
            match uop_location_write(uop.destination, bits_from_int(count), destination_width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerExtend(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(source) => {
            let value = if operation == IntegerExtendSigned then sign_extend_width(source, uop.width)
                        else narrow_bits(source, uop.width);
            let destination_width = unsigned(uop.auxiliary.immediate);
            match uop_location_write(uop.destination, value, destination_width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerMath(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(left), Some(right)) => {
            let value : bits(64) = match operation {
                IntegerMultiplyLow => bits_from_int(unsigned(narrow_bits(left, uop.width)) * unsigned(narrow_bits(right, uop.width))),
                IntegerMultiplyHighUnsigned => product_high(left, right, uop.width, false, false),
                IntegerMultiplyHighSigned => product_high(left, right, uop.width, true, true),
                IntegerMultiplyHighSignedUnsigned => product_high(left, right, uop.width, true, false),
                IntegerCarrylessMultiplyLow => carryless_product(narrow_bits(left, uop.width), narrow_bits(right, uop.width))[63 .. 0],
                IntegerCarrylessMultiplyHigh => carryless_high(carryless_product(narrow_bits(left, uop.width), narrow_bits(right, uop.width)), uop.width),
                IntegerMinimumUnsigned => if unsigned(narrow_bits(left, uop.width)) <= unsigned(narrow_bits(right, uop.width)) then left else right,
                IntegerMaximumUnsigned => if unsigned(narrow_bits(left, uop.width)) >= unsigned(narrow_bits(right, uop.width)) then left else right,
                IntegerMinimumSigned => if signed_width(left, uop.width) <= signed_width(right, uop.width) then left else right,
                IntegerMaximumSigned => if signed_width(left, uop.width) >= signed_width(right, uop.width) then left else right,
            };
            match uop_location_write(uop.destination, narrow_bits(value, uop.width), uop.width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation,
                    InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerDivide(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(dividend), Some(divisor)) => {
            let divisor_u = unsigned(narrow_bits(divisor, uop.width));
            let signed_operation = operation == IntegerDivideSigned | operation == IntegerRemainderSigned;
            if divisor_u == 0 then uop_step_fault(faulted(before, instruction.form.operation, DivideByZero, "zero divisor"))
            else if signed_operation & signed_width(dividend, uop.width) == signed_minimum(uop.width)
                 & signed_width(divisor, uop.width) == -1 then
                uop_step_fault(faulted(before, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"))
            else {
                let quotient = if signed_operation then tdiv_int(signed_width(dividend, uop.width), signed_width(divisor, uop.width))
                               else tdiv_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                let remainder = if signed_operation then signed_width(dividend, uop.width) - quotient * signed_width(divisor, uop.width)
                                else tmod_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                let result = if operation == IntegerRemainderUnsigned | operation == IntegerRemainderSigned then remainder else quotient;
                match uop_location_write(uop.destination, bits_from_int(result), uop.width,
                                         instruction.form.operation, speculative, values) {
                    Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                    None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerDivmod(signed_operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values), uop_location_read(uop.source1, speculative, values)) {
        (Some(dividend), Some(divisor)) => {
            let divisor_u = unsigned(narrow_bits(divisor, uop.width));
            if uop.destination.kind == uop.destination2.kind & uop.destination.index == uop.destination2.index then
                uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction, "DIVMOD destinations overlap"))
            else if divisor_u == 0 then uop_step_fault(faulted(before, instruction.form.operation, DivideByZero, "zero divisor"))
            else if signed_operation & signed_width(dividend, uop.width) == signed_minimum(uop.width)
                 & signed_width(divisor, uop.width) == -1 then
                uop_step_fault(faulted(before, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"))
            else {
                let quotient = if signed_operation then tdiv_int(signed_width(dividend, uop.width), signed_width(divisor, uop.width))
                               else tdiv_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                let remainder = if signed_operation then signed_width(dividend, uop.width) - quotient * signed_width(divisor, uop.width)
                                else tmod_int(unsigned(narrow_bits(dividend, uop.width)), divisor_u);
                match uop_location_write(uop.destination, bits_from_int(quotient), uop.width,
                                         instruction.form.operation, speculative, values) {
                    Some((quotient_state, quotient_values)) => match uop_location_write(
                        uop.destination2, bits_from_int(remainder), uop.width, instruction.form.operation,
                        quotient_state, quotient_values) {
                        Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "remainder destination is not writable")),
                    },
                    None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "quotient destination is not writable")),
                }
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }

function clause execute_uop(UopIntegerExtract(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values)) {
        (Some(low), Some(high), Some(offset_value)) => {
            let offset = unsigned(offset_value[6 .. 0]);
            let value : bits(64) = if offset >= width_bits(uop.width) * 2 then 0x0000000000000000
                else sail_shiftright(concatenated_pair(high, low, uop.width), offset)[63 .. 0];
            match uop_location_write(uop.destination, narrow_bits(value, uop.width), uop.width,
                                     instruction.form.operation, speculative, values) {
                Some((next_state, next_values)) => uop_step_continue(next_state, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop destination is not writable")),
            }
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState, "uop source is unavailable")),
    }

function clause execute_uop(UopBoundsCompare(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values)) {
        (Some(low), Some(value), Some(high)) => {
            let low_value = if operation.signed_operation then signed_width(low, uop.width)
                            else unsigned(narrow_bits(low, uop.width));
            let tested_value = if operation.signed_operation then signed_width(value, uop.width)
                               else unsigned(narrow_bits(value, uop.width));
            let high_value = if operation.signed_operation then signed_width(high, uop.width)
                             else unsigned(narrow_bits(high, uop.width));
            let below = if operation.inclusive_low then tested_value < low_value else tested_value <= low_value;
            let above = if operation.inclusive_high then tested_value > high_value else tested_value >= high_value;
            var updated = speculative;
            updated.flags = flags_value(false, false, false, below | above);
            uop_step_continue(updated, values)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "bounds input is unavailable")),
    }
