function clause register_result_extension(Op_ILLEGAL) = RegisterZeroExtend

function clause repeat_semantics(Op_ILLEGAL) = RepeatObserveDestination

function lower_ILLEGAL_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCoreAction(CoreActionIllegal), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]

function execute_ILLEGAL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_ILLEGAL_uops(instruction), instruction, state))
