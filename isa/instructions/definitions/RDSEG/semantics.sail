function clause register_result_extension(Op_RDSEG) = RegisterZeroExtend

function clause repeat_semantics(Op_RDSEG) = RepeatObserveDestination

function lower_RDSEG_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemReadSegment), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitRegisters)
|]

function execute_RDSEG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RDSEG_uops(instruction), instruction, state))
