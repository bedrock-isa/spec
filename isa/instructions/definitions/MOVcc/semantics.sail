function clause register_result_extension(Op_MOVcc) = RegisterZeroExtend

function clause repeat_semantics(Op_MOVcc) = RepeatObserveDestination

function lower_MOVcc_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(src), Some(dst)) => {
      let width = operation_width(instruction);
      let source = uop_operand_lower(src, width, 0, true);
      let destination = uop_operand_lower(dst, width, source.next_temporary, false);
      Some(uop_program_build_transfer(uop_program_append(
        [|uop_make(UopPredicateGuard(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
                   Operand_dst, 0, CommitControl)|],
        uop_program_append(source.program, destination.program)), source.value, destination,
        Operand_dst, width, source.memory | destination.memory))
    }, _ => None(),
  }

function execute_MOVcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MOVcc_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_MOVcc, IllegalInstruction, "MOVcc could not be lowered")),
  }
