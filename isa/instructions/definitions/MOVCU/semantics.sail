function clause register_result_extension(Op_MOVCU) = RegisterZeroExtend

function clause repeat_semantics(Op_MOVCU) = RepeatObserveDestination

function lower_MOVCU_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let source = uop_operand_lower(source_operand, width, 0, true);
      let destination = uop_operand_lower(destination_operand, width, source.next_temporary, false);
      Some(uop_program_build_transfer(uop_program_append(source.program, destination.program),
        source.value, destination, Operand_dst, width, source.memory | destination.memory))
    }, _ => None(),
  }

function execute_MOVCU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MOVCU_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "MOVCU could not be lowered")),
  }
