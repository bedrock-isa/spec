function clause register_result_extension(Op_SWPT) = RegisterZeroExtend

function clause repeat_semantics(Op_SWPT) = RepeatObserveDestination

function lower_SWPT_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbSwitchPageTable), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_SWPT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_SWPT_uops(instruction), instruction, state))
