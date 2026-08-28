function clause register_result_extension(Op_TRACE) = RegisterZeroExtend

function clause repeat_semantics(Op_TRACE) = RepeatObserveDestination

function lower_TRACE_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_marker) {
    Some(marker) => Some([|uop_make(UopCoreAction(CoreActionTrace),
      uop_operand_location(marker), uop_location_make_none(), uop_location_make_none(), Operand_marker, 0, CommitControl)|]),
    None() => None(),
  }

function execute_TRACE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_TRACE_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "TRACE marker is missing")),
  }
