function clause register_result_extension(Op_PREFETCHNT) = RegisterZeroExtend

function clause repeat_semantics(Op_PREFETCHNT) = RepeatObserveDestination

function lower_PREFETCHNT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_src) {
    Some(operand) => {
      let address = uop_operand_lower(operand, 8, 0, false);
      Some(uop_program_build_cache(address, CachePrefetchNonTemporal, Operand_src))
    }, None() => None(),
  }

function execute_PREFETCHNT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_PREFETCHNT_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "cache address could not be lowered")),
  }
