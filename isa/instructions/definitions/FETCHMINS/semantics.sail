function clause register_result_extension(Op_FETCHMINS) = RegisterSignExtend
function clause repeat_semantics(Op_FETCHMINS) = RepeatObserveDestination
function lower_FETCHMINS_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_src),
         operand_named(instruction, Operand_order)) {
    (Some(memory), Some(src), Some(order)) => {
      let width = operation_width(instruction); let lowered = uop_operand_lower(memory, width, 0, false);
      let source = uop_operand_location(src);
      Some(uop_program_build_atomic(lowered, source, source, uop_operand_location(order),
        AtomicFetchMinimumSigned, Operand_src, width))
    }, _ => None(),
  }
function execute_FETCHMINS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_FETCHMINS_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "FETCHMINS could not be lowered")),
  }
