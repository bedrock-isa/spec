function clause register_result_extension(Op_DIVMODS) = RegisterSignExtend

function clause repeat_semantics(Op_DIVMODS) = RepeatObserveDestination

function lower_DIVMODS_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_quotient),
         operand_named(instruction, Operand_remainder)) {
    (Some(source_operand), Some(quotient_operand), Some(remainder_operand)) => {
      let width = operation_width(instruction);
      let source = uop_operand_lower(source_operand, width, 0, true);
      let quotient = uop_operand_location(quotient_operand);
      let remainder = uop_operand_location(remainder_operand);
      let operation = uop_make_pair(UopIntegerDivmod(true), quotient, source.value, quotient,
                      remainder, Operand_quotient, width, CommitRegisters);
      Some(uop_program_build(source.program, [|operation|], Operand_quotient, width,
        if source.memory then CommitMemory else CommitRegisters))
    }, _ => None(),
  }

function execute_DIVMODS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_DIVMODS_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "DIVMODS could not be lowered")),
  }
