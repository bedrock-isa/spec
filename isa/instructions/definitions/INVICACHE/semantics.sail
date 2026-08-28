function clause register_result_extension(Op_INVICACHE) = RegisterZeroExtend

function clause repeat_semantics(Op_INVICACHE) = RepeatObserveDestination

function lower_INVICACHE_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_target) {
    Some(operand) => {
      let address = uop_operand_lower(operand, 8, 0, false);
      Some(uop_program_build_cache(address, CacheInvalidateInstruction, Operand_target))
    }, None() => None(),
  }

function execute_INVICACHE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_INVICACHE_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "cache address could not be lowered")),
  }
