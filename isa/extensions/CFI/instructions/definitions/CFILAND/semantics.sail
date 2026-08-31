function clause register_result_extension(Op_CFILAND) = RegisterZeroExtend

function clause repeat_semantics(Op_CFILAND) = RepeatObserveDestination

function lower_CFILAND_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(),
           uop_location_make_none(), Operand_dst, 0, CommitControl)
|]

function execute_CFILAND(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_CFILAND_uops(instruction), instruction, state))
