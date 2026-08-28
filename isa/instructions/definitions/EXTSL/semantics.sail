function clause register_result_extension(Op_EXTSL) = RegisterSignExtend

function clause repeat_semantics(Op_EXTSL) = RepeatObserveDestination

function lower_EXTSL_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) => {
      let source_width = operation_width(instruction);
      let source = uop_operand_lower(source_operand, source_width, 0, true);
      let destination = uop_operand_lower(destination_operand, 4, source.next_temporary, false);
      let output = if destination.memory then uop_location_make_temporary(destination.next_temporary)
                   else destination.value;
      let operation = { uop_make(UopIntegerExtend(IntegerExtendSigned), source.value, uop_location_make_none(),
          output, Operand_dst, source_width, CommitRegisters) with
          auxiliary = uop_location_make_immediate(bits_from_int(4)) };
      Some(uop_program_build_operation(
        uop_program_append(source.program, destination.program), operation, output, destination,
        Operand_dst, 4, source.memory | destination.memory
      ))
    }, _ => None(),
  }

function execute_EXTSL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_EXTSL_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "EXTSL could not be lowered")),
  }
