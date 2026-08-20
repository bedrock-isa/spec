function floating_value_named(instruction : Decoded_instruction, state : Cpu_state,
                              name : string) -> option(bits(64)) =
  match operand_named(instruction, name) {
    Some(operand) => if operand.type_name == "Fn" then
      Some(state.floating_registers[unsigned(operand.value[3 .. 0])])
      else None(),
    None() => None(),
  }

function commit_fp_local_value(instruction : Decoded_instruction, state : Cpu_state,
                               value : bits(64)) -> option(Execution_result) =
  match operand_named(instruction, "dst") {
    Some(destination) => {
      var updated = advance_pc(state, instruction);
      let width = operation_width(instruction);
      if destination.type_name == "Fn" then {
        updated.floating_registers[unsigned(destination.value[3 .. 0])] =
          if width == 4 then 0x00000000 @ value[31 .. 0] else value;
        updated.fp_component_modified = true;
        Some(completed(state, updated, CommitRegisters, [||]))
      }
      else if destination.type_name == "Rn" then {
        updated.registers[unsigned(destination.value[3 .. 0])] = value;
        Some(completed(state, updated, CommitRegisters, [||]))
      }
      else None()
    },
    None() => None(),
  }

function execute_fp_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let width = operation_width(instruction);
  if operation == Op_FCLR then commit_fp_local_value(
    instruction, state, fp_bitwise_fclr()
  )
  else if operation == Op_FMOV | operation == Op_FMOVcc
       | operation == Op_FABS | operation == Op_FNEG then
    match floating_value_named(instruction, state, "src") {
      None() => None(),
      Some(source) => {
        let value = if operation == Op_FABS then fp_bitwise_fabs(source, width)
          else if operation == Op_FNEG then fp_bitwise_fneg(source, width)
          else fp_bitwise_fmov(source, width);
        match value {
          Some(result) => commit_fp_local_value(instruction, state, result),
          None() => None(),
        }
      },
    }
  else if operation == Op_FCOPYSIGN then match (
    floating_value_named(instruction, state, "sign_src"),
    floating_value_named(instruction, state, "magnitude_src")
  ) {
    (Some(sign_source), Some(magnitude_source)) => match fp_bitwise_fcopysign(
      sign_source, magnitude_source, width
    ) {
      Some(result) => commit_fp_local_value(instruction, state, result),
      None() => None(),
    },
    _ => None(),
  }
  else if operation == Op_FCLASS then match floating_value_named(instruction, state, "src") {
    Some(source) => match fp_fclass(source, width) {
      Some(result) => commit_fp_local_value(instruction, state, result),
      None() => None(),
    },
    None() => None(),
  }
  else if operation == Op_FMOVCR then match operand_named(instruction, "constant_id") {
    Some(constant_operand) => match fp_fmovcr(constant_operand.value[15 .. 0]) {
      Some(result) => commit_fp_local_value(instruction, state, result),
      None() => None(),
    },
    None() => None(),
  }
  else if operation == Op_FXCHG then match (
    operand_named(instruction, "lhs"), operand_named(instruction, "rhs")
  ) {
    (Some(lhs), Some(rhs)) => {
      let left = unsigned(lhs.value[3 .. 0]);
      let right = unsigned(rhs.value[3 .. 0]);
      let exchange = fp_bitwise_fxchg(
        state.floating_registers[left], state.floating_registers[right]
      );
      var updated = advance_pc(state, instruction);
      updated.floating_registers[left] = exchange.lhs;
      updated.floating_registers[right] = exchange.rhs;
      updated.fp_component_modified = true;
      Some(completed(state, updated, CommitRegisters, [||]))
    },
    _ => None(),
  }
  else None()
}

