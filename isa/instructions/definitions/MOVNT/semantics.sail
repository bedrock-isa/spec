function clause register_result_extension(Op_MOVNT) = RegisterZeroExtend

function clause repeat_semantics(Op_MOVNT) = RepeatObserveSource

function lower_MOVNT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(src), Some(dst)) => {
      let width = operation_width(instruction);
      let source = uop_operand_lower(src, width, 0, true);
      let destination = uop_operand_lower(dst, width, source.next_temporary, false);
      let store = uop_make(UopNonTemporalStore(), source.value, destination.address,
        uop_location_make_none(), Operand_dst, width, CommitMemory);
      Some(uop_program_build(uop_program_append(source.program, destination.program),
        [|store|], Operand_dst, width, CommitMemory))
    }, _ => None(),
  }

function execute_MOVNT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MOVNT_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_MOVNT, IllegalInstruction, "MOVNT could not be lowered")),
  }
