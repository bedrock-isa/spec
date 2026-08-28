function clause register_result_extension(Op_SHR) = RegisterZeroExtend

function clause repeat_semantics(Op_SHR) = RepeatObserveDestination

function lower_SHR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_count), operand_named(instruction, Operand_dst)) {
    (Some(count_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let count = uop_operand_lower(count_operand, width, 0, true);
      let destination = uop_operand_lower(destination_operand, width, count.next_temporary, true);
      let operation = uop_make(UopIntegerShift(IntegerShiftRight), destination.value,
        count.value, destination.value, Operand_dst, width, CommitRegisters);
      Some(uop_program_build_operation(
        uop_program_append(count.program, destination.program), operation, destination.value, destination,
        Operand_dst, width, count.memory | destination.memory
      ))
    }, _ => None(),
  }
function execute_SHR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_SHR_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "SHR could not be lowered")),
  }
