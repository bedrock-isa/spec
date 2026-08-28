function clause register_result_extension(Op_YIELD) = RegisterZeroExtend

function clause repeat_semantics(Op_YIELD) = RepeatObserveDestination

function lower_YIELD_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCoreAction(CoreActionYield), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]

function execute_YIELD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_YIELD_uops(instruction), instruction, state))
