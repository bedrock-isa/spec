function clause register_result_extension(Op_WRSEG) = RegisterZeroExtend

function clause repeat_semantics(Op_WRSEG) = RepeatObserveDestination

function lower_WRSEG_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemWriteSegment), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_src, 8, CommitRegisters)
|]

function execute_WRSEG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_WRSEG_uops(instruction), instruction, state))
