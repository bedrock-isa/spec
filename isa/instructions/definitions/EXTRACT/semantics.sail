function clause register_result_extension(Op_EXTRACT) = RegisterZeroExtend

function clause repeat_semantics(Op_EXTRACT) = RepeatObserveDestination

function lower_EXTRACT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_offset), operand_named(instruction, Operand_high),
         operand_named(instruction, Operand_low_dst)) {
    (Some(offset_operand), Some(high_operand), Some(low_operand)) => {
      let width = operation_width(instruction);
      let offset = uop_operand_location(offset_operand);
      let high = uop_operand_location(high_operand);
      let low = uop_operand_location(low_operand);
      let operation = uop_make_ternary(UopIntegerExtract(), low, high, offset, low,
        Operand_low_dst, width, CommitRegisters);
      Some(uop_program_build([||], [|operation|], Operand_low_dst, width,
        CommitRegisters))
    }, _ => None(),
  }

function execute_EXTRACT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_EXTRACT_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "EXTRACT could not be lowered")),
  }
