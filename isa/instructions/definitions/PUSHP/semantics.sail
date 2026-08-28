function clause register_result_extension(Op_PUSHP) = RegisterZeroExtend

function clause repeat_semantics(Op_PUSHP) = RepeatObserveDestination

function lower_PUSHP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_pair_id) {
    Some(pair) => {
      let first = unsigned(pair.value[2 .. 0]) * 2;
      Some(uop_program_build_stack_pair_push(
        uop_location_make_register(first), uop_location_make_register(first + 1), Operand_pair_id))
    }, None() => None(),
  }

function execute_PUSHP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_PUSHP_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "PUSHP could not be lowered")),
  }
