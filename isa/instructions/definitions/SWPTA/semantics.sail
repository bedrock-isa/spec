function clause register_result_extension(Op_SWPTA) = RegisterZeroExtend

function clause repeat_semantics(Op_SWPTA) = RepeatObserveDestination

function lower_SWPTA_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbSwitchPageTableAsid), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_SWPTA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_SWPTA_uops(instruction), instruction, state))
