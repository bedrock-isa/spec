function floating_value_named(instruction : Decoded_instruction, state : Cpu_state,
                              name : Operand_id) -> option(bits(64)) =
  match operand_named(instruction, name) {
    Some(operand) => if operand.operand_type == OperandType_Fn then
      Some(state.floating_registers[unsigned(operand.value[3 .. 0])])
      else None(),
    None() => None(),
  }
