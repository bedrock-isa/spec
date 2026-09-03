function clause register_result_extension(Op_CLRLINK) = RegisterZeroExtend

function clause repeat_semantics(Op_CLRLINK) = RepeatObserveDestination

function lower_CLRLINK_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopLinkClear(), uop_location_make_none(), uop_location_make_none(),
    uop_location_make_none(), Operand_target, 0, CommitControl),
  uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(),
    uop_location_make_none(), Operand_target, 0, CommitControl)
|]

function execute_CLRLINK(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_CLRLINK_uops(instruction), instruction, state))
