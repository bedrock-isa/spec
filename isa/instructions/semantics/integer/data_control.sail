function concatenated_pair(high : bits(64), low : bits(64), width : int) -> bits(128) =
  if width == 1 then sail_zero_extend(high[7 .. 0] @ low[7 .. 0], 128)
  else if width == 2 then sail_zero_extend(high[15 .. 0] @ low[15 .. 0], 128)
  else if width == 4 then sail_zero_extend(high[31 .. 0] @ low[31 .. 0], 128)
  else high @ low

function execute_extract_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, Operand_offset), value_named(instruction, state, Operand_high),
         operand_named(instruction, Operand_low_dst)) {
    (Some(offset_value), Some(high), Some(low_operand)) =>
      match (local_operand_value(state, low_operand), local_destination(low_operand, width)) {
        (Some(low), Some(destination)) => {
          let offset = unsigned(offset_value[6 .. 0]);
          let value : bits(64) = if offset >= width_bits(width) * 2 then 0x0000000000000000
            else sail_shiftright(concatenated_pair(high, low, width), offset)[63 .. 0];
          let updated = write_local_destination(
            state, instruction.form.operation, destination, narrow_bits(value, width)
          );
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_extend_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let source_width = operation_width(instruction);
  let destination_width = extension_destination_width(instruction.form.operation);
  match (value_named(instruction, state, Operand_src),
         destination_named(instruction, Operand_dst, destination_width)) {
    (Some(source), Some(destination)) => {
      let signed_operation = instruction.form.operation == Op_EXTSW
                           | instruction.form.operation == Op_EXTSL
                           | instruction.form.operation == Op_EXTSQ;
      let value = if signed_operation then sign_extend_width(source, source_width)
                  else narrow_bits(source, source_width);
      let updated = write_local_destination(
        state, instruction.form.operation, destination, value
      );
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function execute_xchg_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (operand_named(instruction, Operand_lhs), operand_named(instruction, Operand_rhs)) {
    (Some(lhs_operand), Some(rhs_operand)) =>
      match (local_operand_value(state, lhs_operand), local_operand_value(state, rhs_operand),
             local_destination(lhs_operand, width), local_destination(rhs_operand, width)) {
        (Some(lhs), Some(rhs), Some(lhs_destination), Some(rhs_destination)) => {
          let after_lhs = write_local_destination(
            state, instruction.form.operation, lhs_destination, rhs
          );
          let updated = write_local_destination(
            after_lhs, instruction.form.operation, rhs_destination, lhs
          );
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_set_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match destination_named(instruction, Operand_dst, width) {
    Some(destination) => {
      let updated = write_local_destination(
        state, instruction.form.operation, destination, 0x0000000000000001
      );
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    None() => None(),
  }
}

function execute_move_sp_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) =>
      if source_operand.operand_type != OperandType_SP
         & destination_operand.operand_type != OperandType_SP then None()
      else match (local_operand_value(state, source_operand), local_destination(destination_operand, 8)) {
        (Some(source), Some(destination)) => {
          let updated = write_local_destination(
            state, instruction.form.operation, destination, source
          );
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }

function execute_bounds_comparison_local(
  instruction : Decoded_instruction,
  state : Cpu_state,
  inclusive_low : bool,
  inclusive_high : bool,
  signed_operation : bool
)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, Operand_lo), value_named(instruction, state, Operand_value),
         value_named(instruction, state, Operand_hi)) {
    (Some(low), Some(value), Some(high)) => {
      let low_value = if signed_operation then signed_width(low, width)
                      else unsigned(narrow_bits(low, width));
      let tested_value = if signed_operation then signed_width(value, width)
                         else unsigned(narrow_bits(value, width));
      let high_value = if signed_operation then signed_width(high, width)
                       else unsigned(narrow_bits(high, width));
      let below = if inclusive_low then tested_value < low_value else tested_value <= low_value;
      let above = if inclusive_high then tested_value > high_value else tested_value >= high_value;
      let updated = { state with flags = flags_value(false, false, false, below | above) };
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function control_target_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(bits(64)) =
  match operand_named(instruction, Operand_target) {
    None() => None(),
    Some(operand) => match local_operand_value(state, operand) {
      None() => None(),
      Some(value) => if operand.operand_type == OperandType_imm8s
                        | operand.operand_type == OperandType_imm16s
                        | operand.operand_type == OperandType_imm32s then
          Some(add_bits(next_pc(state, instruction), value))
        else Some(narrow_bits(value, operation_width(instruction))),
    },
  }

function execute_subtract_compare_jump_local(
  instruction : Decoded_instruction,
  state : Cpu_state
)
  -> option(Execution_result) =
  match (value_named(instruction, state, Operand_src), value_named(instruction, state, Operand_dst),
         value_named(instruction, state, Operand_target), condition_field(instruction.fields)) {
    (Some(source), Some(destination), Some(relative), Some(condition)) => {
      let width = operation_width(instruction);
      let (_, temporary_flags) = sub_with_flags(destination, source, 0, width);
      let pc = if condition_holds(condition, temporary_flags)
        then add_bits(next_pc(state, instruction), relative)
        else next_pc(state, instruction);
      Some(completed(state, { state with pc = pc }, CommitControl, [||]))
    },
    _ => None(),
  }

function execute_and_compare_jump_local(
  instruction : Decoded_instruction,
  state : Cpu_state
)
  -> option(Execution_result) =
  match (value_named(instruction, state, Operand_src), value_named(instruction, state, Operand_dst),
         value_named(instruction, state, Operand_target), condition_field(instruction.fields)) {
    (Some(source), Some(destination), Some(relative), Some(condition)) => {
      let width = operation_width(instruction);
      let value = narrow_bits(
        integer_and_value(destination, source), width
      );
      let temporary_flags = flags_value(
        value == 0x0000000000000000, width_sign(value, width), false, false
      );
      let pc = if condition_holds(condition, temporary_flags)
        then add_bits(next_pc(state, instruction), relative)
        else next_pc(state, instruction);
      Some(completed(state, { state with pc = pc }, CommitControl, [||]))
    },
    _ => None(),
  }
