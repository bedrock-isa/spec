function clause register_result_extension(Op_SAVE) = RegisterZeroExtend

function clause repeat_semantics(Op_SAVE) = RepeatObserveDestination

function lower_SAVE_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbStateSave), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_SAVE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_SAVE_uops(instruction), instruction, state))
