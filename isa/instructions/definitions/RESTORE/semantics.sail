function clause register_result_extension(Op_RESTORE) = RegisterZeroExtend

function clause repeat_semantics(Op_RESTORE) = RepeatObserveDestination

function lower_RESTORE_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbStateRestore), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_RESTORE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RESTORE_uops(instruction), instruction, state))
