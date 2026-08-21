function execute_binary_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  if not_bool(operation == Op_CMP | operation == Op_TEST | operation == Op_ADC
              | operation == Op_SBB | operation == Op_ADD | operation == Op_SUB
              | operation == Op_AND | operation == Op_OR | operation == Op_XOR
              | operation == Op_MOV | operation == Op_MOVCU | operation == Op_MOVUC
              | operation == Op_MOVUU | operation == Op_MOVcc) then None()
  else match (first_binary_operand(instruction.operands), second_binary_operand(instruction.operands)) {
    (Some(source_operand), Some(destination_operand)) =>
      match (local_operand_value(state, source_operand),
             local_operand_value(state, destination_operand)) {
        (Some(source), Some(destination)) => {
          if operation == Op_CMP then {
            let (ignored, flags) = sub_with_flags(destination, source, 0, width);
            let updated = { state with flags = flags };
            Some(local_result(state, instruction, updated, CommitRegisters))
          }
          else if operation == Op_TEST then {
            let value = narrow_bits(destination & source, width);
            let updated = { state with flags = flags_value(
              value == 0x0000000000000000, width_sign(value, width), false, false
            ) };
            Some(local_result(state, instruction, updated, CommitRegisters))
          }
          else match local_destination(destination_operand, width) {
            None() => None(),
            Some(destination_ref) => {
              let (value, flags) = if operation == Op_ADC then
                add_with_flags(destination, source, if flag_c(state.flags) then 1 else 0, width)
              else if operation == Op_SBB then
                sub_with_flags(destination, source, if flag_c(state.flags) then 1 else 0, width)
              else if operation == Op_ADD then
                (bits_from_int(unsigned(narrow_bits(destination, width))
                               + unsigned(narrow_bits(source, width))), state.flags)
              else if operation == Op_SUB then
                (bits_from_int(unsigned(narrow_bits(destination, width))
                               - unsigned(narrow_bits(source, width))), state.flags)
              else if operation == Op_AND then (destination & source, state.flags)
              else if operation == Op_OR then (destination | source, state.flags)
              else if operation == Op_XOR then (xor_vec(destination, source), state.flags)
              else (source, state.flags);
              var updated = write_local_destination(state, destination_ref,
                                                      narrow_bits(value, width));
              updated.flags = flags;
              Some(local_result(state, instruction, updated, CommitRegisters))
            },
          }
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_sp_arithmetic_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (value_named(instruction, state, "imm"), destination_named(instruction, "dst", 8)) {
    (Some(source), Some(destination)) => if destination.kind == "SP" then {
      let value = if instruction.form.operation == Op_ADD
        then add_bits(state.sp, source) else sub_bits(state.sp, source);
      let updated = write_local_destination(state, destination, value);
      Some(local_result(state, instruction, updated, CommitRegisters))
    } else None(),
    _ => None(),
  }

function execute_unary_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  if not_bool(operation == Op_CLR | operation == Op_INC | operation == Op_INCF
              | operation == Op_DEC | operation == Op_DECF | operation == Op_NEG
              | operation == Op_ABS | operation == Op_NOT) then None()
  else match operand_named(instruction, "dst") {
    None() => None(),
    Some(operand) => match (local_operand_value(state, operand), local_destination(operand, width)) {
      (Some(old), Some(destination)) => {
        let value = if operation == Op_CLR then 0x0000000000000000
          else if operation == Op_INC | operation == Op_INCF then add_bits(old, 0x0000000000000001)
          else if operation == Op_DEC | operation == Op_DECF then sub_bits(old, 0x0000000000000001)
          else if operation == Op_NEG then sub_bits(0x0000000000000000, old)
          else if operation == Op_ABS then
            if width_sign(old, width) then sub_bits(0x0000000000000000, old) else old
          else not_vec(old);
        var updated = write_local_destination(state, destination, narrow_bits(value, width));
        if operation == Op_INCF then {
          let (ignored, flags) = add_with_flags(old, 0x0000000000000001, 0, width);
          updated.flags = flags
        }
        else if operation == Op_DECF then {
          let (ignored, flags) = sub_with_flags(old, 0x0000000000000001, 0, width);
          updated.flags = flags
        }
        else ();
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
      _ => None(),
    },
  }
}

function execute_shift_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "count"), operand_named(instruction, "dst")) {
    (Some(count), Some(operand)) =>
      match (local_operand_value(state, operand), local_destination(operand, width)) {
        (Some(old), Some(destination)) => {
          let value = shift_result(instruction.form.operation, old, count, width);
          let updated = write_local_destination(state, destination, value);
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_bit_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "bit_index"), operand_named(instruction, "dst")) {
    (Some(raw_index), Some(operand)) => match local_operand_value(state, operand) {
      None() => None(),
      Some(old) => {
        let index = unsigned(raw_index[5 .. 0]);
        let mask = sail_shiftleft(0x0000000000000001, index);
        let selected_old = narrow_bits(old, width);
        let was_clear = (selected_old & mask) == 0x0000000000000000;
        let operation = instruction.form.operation;
        let new_flags = flags_value(was_clear, false, false, false);
        if operation == Op_BTEST then {
          let updated = { state with flags = new_flags };
          Some(local_result(state, instruction, updated, CommitRegisters))
        }
        else match local_destination(operand, width) {
          None() => None(),
          Some(destination) => {
            let value = if operation == Op_BSET then selected_old | mask
              else if operation == Op_BCLR then selected_old & not_vec(mask)
              else xor_vec(selected_old, mask);
            var updated = write_local_destination(state, destination, value);
            updated.flags = new_flags;
            Some(local_result(state, instruction, updated, CommitRegisters))
          },
        }
      },
    },
    _ => None(),
  }
}

function execute_count_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), operand_named(instruction, "dst")) {
    (Some(source), Some(operand)) => match local_destination(operand, 8) {
      None() => None(),
      Some(destination) => {
        let value = narrow_bits(source, width);
        let bits = width_bits(width);
        let count = if instruction.form.operation == Op_CLZ then
            count_from_high(value, bits, bitzero)
          else if instruction.form.operation == Op_CLS then
            count_from_high(value, bits, bitone)
          else if instruction.form.operation == Op_CTZ then
            count_from_low(value, 0, bits, bitzero)
          else if instruction.form.operation == Op_CTS then
            count_from_low(value, 0, bits, bitone)
          else bit_count_from(value, 0, bits);
        let updated = write_local_destination(state, destination, bits_from_int(count));
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
    },
    _ => None(),
  }
}

function execute_parity_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), destination_named(instruction, "dst", width)) {
    (Some(source), Some(destination)) => {
      let parity = tmod_int(bit_count_from(narrow_bits(source, width), 0, width_bits(width)), 2);
      let updated = write_local_destination(state, destination, bits_from_int(parity));
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function execute_revbyte_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match operand_named(instruction, "dst") {
    Some(operand) => match (local_operand_value(state, operand), local_destination(operand, width)) {
      (Some(old), Some(destination)) => {
        let updated = write_local_destination(state, destination, reverse_bytes(old, width));
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
      _ => None(),
    },
    None() => None(),
  }
}

function product_high(lhs : bits(64), rhs : bits(64), width : int,
                      lhs_signed : bool, rhs_signed : bool) -> bits(64) = {
  let left = if lhs_signed then signed_width(lhs, width) else unsigned(narrow_bits(lhs, width));
  let right = if rhs_signed then signed_width(rhs, width) else unsigned(narrow_bits(rhs, width));
  let product : bits(128) = get_slice_int(128, left * right, 0);
  if width == 1 then sail_zero_extend(product[15 .. 8], 64)
  else if width == 2 then sail_zero_extend(product[31 .. 16], 64)
  else if width == 4 then sail_zero_extend(product[63 .. 32], 64)
  else product[127 .. 64]
}

function execute_math_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  if not_bool(operation == Op_MUL | operation == Op_MULHU | operation == Op_MULHS
              | operation == Op_MULHSU | operation == Op_CLMUL | operation == Op_CLMULH
              | operation == Op_MINU | operation == Op_MAXU | operation == Op_MINS
              | operation == Op_MAXS) then None()
  else match (value_named(instruction, state, "src"), operand_named(instruction, "dst")) {
    (Some(source), Some(operand)) =>
      match (local_operand_value(state, operand), local_destination(operand, width)) {
        (Some(old), Some(destination)) => {
          let value = if operation == Op_MUL then
              bits_from_int(unsigned(narrow_bits(old, width)) * unsigned(narrow_bits(source, width)))
            else if operation == Op_MULHU then product_high(old, source, width, false, false)
            else if operation == Op_MULHS then product_high(old, source, width, true, true)
            else if operation == Op_MULHSU then product_high(old, source, width, true, false)
            else if operation == Op_CLMUL then carryless_product(
              narrow_bits(old, width), narrow_bits(source, width))[63 .. 0]
            else if operation == Op_CLMULH then carryless_high(
              carryless_product(narrow_bits(old, width), narrow_bits(source, width)), width
            )
            else if operation == Op_MINU then
              if unsigned(narrow_bits(old, width)) <= unsigned(narrow_bits(source, width))
              then old else source
            else if operation == Op_MAXU then
              if unsigned(narrow_bits(old, width)) >= unsigned(narrow_bits(source, width))
              then old else source
            else if operation == Op_MINS then
              if signed_width(old, width) <= signed_width(source, width) then old else source
            else if signed_width(old, width) >= signed_width(source, width) then old else source;
          let updated = write_local_destination(state, destination, narrow_bits(value, width));
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_divide_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), operand_named(instruction, "dst")) {
    (Some(source), Some(operand)) =>
      match (local_operand_value(state, operand), local_destination(operand, width)) {
        (Some(dividend), Some(destination)) => {
          let divisor_u = unsigned(narrow_bits(source, width));
          if divisor_u == 0 then Some(faulted(
            state, instruction.form.operation, DivideByZero, "zero divisor"
          ))
          else {
            let signed_operation = instruction.form.operation == Op_DIVS
                                   | instruction.form.operation == Op_MODS;
            let modulo_operation = instruction.form.operation == Op_MODS
                                   | instruction.form.operation == Op_MODU;
            if signed_operation & signed_width(dividend, width) == signed_minimum(width)
               & signed_width(source, width) == -1 then Some(faulted(
              state, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"
            ))
            else {
              let quotient = if signed_operation then
                  tdiv_int(signed_width(dividend, width), signed_width(source, width))
                else tdiv_int(unsigned(narrow_bits(dividend, width)), divisor_u);
              let remainder = if signed_operation then
                  signed_width(dividend, width) - quotient * signed_width(source, width)
                else tmod_int(unsigned(narrow_bits(dividend, width)), divisor_u);
              let value = bits_from_int(if modulo_operation then remainder else quotient);
              let updated = write_local_destination(state, destination, narrow_bits(value, width));
              Some(local_result(state, instruction, updated, CommitRegisters))
            }
          }
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_divmod_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), operand_named(instruction, "quotient"),
         operand_named(instruction, "remainder")) {
    (Some(source), Some(quotient_operand), Some(remainder_operand)) =>
      match (local_operand_value(state, quotient_operand),
             local_destination(quotient_operand, width),
             local_destination(remainder_operand, width)) {
        (Some(dividend), Some(quotient_destination), Some(remainder_destination)) =>
          if quotient_destination.kind == remainder_destination.kind
             & quotient_destination.index == remainder_destination.index then Some(faulted(
            state, instruction.form.operation, IllegalInstruction, "DIVMOD destinations overlap"
          ))
          else if unsigned(narrow_bits(source, width)) == 0 then Some(faulted(
            state, instruction.form.operation, DivideByZero, "zero divisor"
          ))
          else {
            let signed_operation = instruction.form.operation == Op_DIVMODS;
            if signed_operation & signed_width(dividend, width) == signed_minimum(width)
               & signed_width(source, width) == -1 then Some(faulted(
              state, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"
            ))
            else {
              let quotient = if signed_operation then
                  tdiv_int(signed_width(dividend, width), signed_width(source, width))
                else tdiv_int(unsigned(narrow_bits(dividend, width)),
                              unsigned(narrow_bits(source, width)));
              let remainder = if signed_operation then
                  signed_width(dividend, width) - quotient * signed_width(source, width)
                else tmod_int(unsigned(narrow_bits(dividend, width)),
                              unsigned(narrow_bits(source, width)));
              let after_quotient = write_local_destination(
                state, quotient_destination, bits_from_int(quotient)
              );
              let updated = write_local_destination(
                after_quotient, remainder_destination, bits_from_int(remainder)
              );
              Some(local_result(state, instruction, updated, CommitRegisters))
            }
          },
        _ => None(),
      },
    _ => None(),
  }
}
