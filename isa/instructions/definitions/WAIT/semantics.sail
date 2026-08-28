function clause register_result_extension(Op_WAIT) = RegisterZeroExtend

function clause repeat_semantics(Op_WAIT) = RepeatObserveDestination

function lower_WAIT_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCoreAction(CoreActionWait), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]

function execute_WAIT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_WAIT_uops(instruction), instruction, state))
