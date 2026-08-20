function concatenated_pair(high : bits(64), low : bits(64), width : int) -> bits(128) =
  if width == 1 then sail_zero_extend(high[7 .. 0] @ low[7 .. 0], 128)
  else if width == 2 then sail_zero_extend(high[15 .. 0] @ low[15 .. 0], 128)
  else if width == 4 then sail_zero_extend(high[31 .. 0] @ low[31 .. 0], 128)
  else high @ low

function execute_extract_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "offset"), value_named(instruction, state, "high"),
         operand_named(instruction, "low_dst")) {
    (Some(offset_value), Some(high), Some(low_operand)) =>
      match (local_operand_value(state, low_operand), local_destination(low_operand, width)) {
        (Some(low), Some(destination)) => {
          let offset = unsigned(offset_value[6 .. 0]);
          let value : bits(64) = if offset >= width_bits(width) * 2 then 0x0000000000000000
            else sail_shiftright(concatenated_pair(high, low, width), offset)[63 .. 0];
          let updated = write_local_destination(state, destination, narrow_bits(value, width));
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
  match (value_named(instruction, state, "src"),
         destination_named(instruction, "dst", destination_width)) {
    (Some(source), Some(destination)) => {
      let signed_operation = instruction.form.operation == Op_EXTSW
                           | instruction.form.operation == Op_EXTSL
                           | instruction.form.operation == Op_EXTSQ;
      let value = if signed_operation then sign_extend_width(source, source_width)
                  else narrow_bits(source, source_width);
      let updated = write_local_destination(state, destination, value);
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function execute_xchg_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (operand_named(instruction, "lhs"), operand_named(instruction, "rhs")) {
    (Some(lhs_operand), Some(rhs_operand)) =>
      match (local_operand_value(state, lhs_operand), local_operand_value(state, rhs_operand),
             local_destination(lhs_operand, width), local_destination(rhs_operand, width)) {
        (Some(lhs), Some(rhs), Some(lhs_destination), Some(rhs_destination)) => {
          let after_lhs = write_local_destination(state, lhs_destination, rhs);
          let updated = write_local_destination(after_lhs, rhs_destination, lhs);
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
  match destination_named(instruction, "dst", width) {
    Some(destination) => {
      let updated = write_local_destination(state, destination, 0x0000000000000001);
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    None() => None(),
  }
}

function execute_move_sp_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (operand_named(instruction, "src"), operand_named(instruction, "dst")) {
    (Some(source_operand), Some(destination_operand)) =>
      match (local_operand_value(state, source_operand), local_destination(destination_operand, 8)) {
        (Some(source), Some(destination)) => {
          let updated = write_local_destination(state, destination, source);
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }

function execute_bounds_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "lo"), value_named(instruction, state, "value"),
         value_named(instruction, state, "hi")) {
    (Some(low), Some(value), Some(high)) => {
      let operation = instruction.form.operation;
      let inclusive_low = operation == Op_BNDSII | operation == Op_BNDSIX
                        | operation == Op_BNDUII | operation == Op_BNDUIX;
      let inclusive_high = operation == Op_BNDSII | operation == Op_BNDSXI
                         | operation == Op_BNDUII | operation == Op_BNDUXI;
      let signed_operation = operation == Op_BNDSII | operation == Op_BNDSIX
                           | operation == Op_BNDSXI | operation == Op_BNDSXX;
      let low_value = if signed_operation then signed_width(low, width)
                      else unsigned(narrow_bits(low, width));
      let tested_value = if signed_operation then signed_width(value, width)
                         else unsigned(narrow_bits(value, width));
      let high_value = if signed_operation then signed_width(high, width)
                       else unsigned(narrow_bits(high, width));
      let below = if inclusive_low then tested_value < low_value else tested_value <= low_value;
      let above = if inclusive_high then tested_value > high_value else tested_value >= high_value;
      let updated = { state with flags = set_flag_v_only(state.flags, below | above) };
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function control_target_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(bits(64)) =
  match operand_named(instruction, "target") {
    None() => None(),
    Some(operand) => match local_operand_value(state, operand) {
      None() => None(),
      Some(value) => if operand.type_name == "imm8s" | operand.type_name == "imm16s"
                        | operand.type_name == "imm32s" then
          Some(add_bits(next_pc(state, instruction), value))
        else Some(narrow_bits(value, operation_width(instruction))),
    },
  }

function execute_compare_jump_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (value_named(instruction, state, "src"), value_named(instruction, state, "dst"),
         value_named(instruction, state, "target"), condition_field(instruction.fields)) {
    (Some(source), Some(destination), Some(relative), Some(condition)) => {
      let width = operation_width(instruction);
      let temporary_flags = if instruction.form.operation == Op_CMPJcc then {
        let (ignored, flags) = sub_with_flags(destination, source, 0, width);
        flags
      } else {
        let value = narrow_bits(destination & source, width);
        flags_value(value == 0x0000000000000000, width_sign(value, width), false, false)
      };
      let pc = if condition_holds(condition, temporary_flags)
        then add_bits(next_pc(state, instruction), relative)
        else next_pc(state, instruction);
      Some(completed(state, { state with pc = pc }, CommitControl, [||]))
    },
    _ => None(),
  }

