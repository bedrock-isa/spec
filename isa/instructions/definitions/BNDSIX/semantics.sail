function clause register_result_extension(Op_BNDSIX) = RegisterZeroExtend

function clause repeat_semantics(Op_BNDSIX) = RepeatObserveBoolean

function lower_BNDSIX_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_lo), operand_named(instruction, Operand_value),
         operand_named(instruction, Operand_hi)) {
    (Some(low_operand), Some(value_operand), Some(high_operand)) => {
      let width = operation_width(instruction);
      let low = uop_operand_lower(low_operand, width, 0, true);
      let value = uop_operand_lower(value_operand, width, low.next_temporary, true);
      let high = uop_operand_lower(high_operand, width, value.next_temporary, true);
      let descriptor : Bounds_uop_operation = struct {
        inclusive_low = true, inclusive_high = false, signed_operation = true
      };
      let operation = uop_make_ternary(UopBoundsCompare(descriptor), low.value, value.value,
        high.value, uop_location_make_none(), Operand_value, width, CommitRegisters);
      Some(uop_program_build(uop_program_append(low.program,
        uop_program_append(value.program, high.program)), [|operation|], Operand_value, width,
        if low.memory | value.memory | high.memory then CommitMemory else CommitRegisters))
    }, _ => None(),
  }

function execute_BNDSIX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_BNDSIX_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "BNDSIX could not be lowered")),
  }
