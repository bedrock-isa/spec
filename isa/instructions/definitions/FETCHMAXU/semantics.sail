function clause register_result_extension(Op_FETCHMAXU) = RegisterZeroExtend
function clause repeat_semantics(Op_FETCHMAXU) = RepeatObserveDestination
function lower_FETCHMAXU_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_src),
         operand_named(instruction, Operand_order)) {
    (Some(memory), Some(src), Some(order)) => {
      let width = operation_width(instruction); let lowered = uop_operand_lower(memory, width, 0, false);
      let source = uop_operand_location(src);
      Some(uop_program_build_atomic(lowered, source, source, uop_operand_location(order),
        AtomicFetchMaximumUnsigned, Operand_src, width))
    }, _ => None(),
  }
function execute_FETCHMAXU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_FETCHMAXU_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "FETCHMAXU could not be lowered")),
  }
