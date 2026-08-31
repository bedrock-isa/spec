function clause register_result_extension(Op_CRC32) = RegisterZeroExtend
function clause repeat_semantics(Op_CRC32) = RepeatObserveDestination
function lower_CRC32_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(src), Some(dst)) => {
      let width = operation_width(instruction); let source = uop_operand_lower(src, width, 0, true);
      let destination = uop_operand_location(dst);
      let operation = uop_make(UopIntegerCrc(IntegerCrc32), source.value, destination,
        destination, Operand_dst, width, CommitRegisters);
      Some(uop_program_build(source.program, [|operation|], Operand_dst, 4,
        if source.memory then CommitMemory else CommitRegisters))
    }, _ => None(),
  }
function execute_CRC32(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_CRC32_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "CRC32 could not be lowered")),
  }
