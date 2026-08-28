function clause register_result_extension(Op_HALT) = RegisterZeroExtend

function clause repeat_semantics(Op_HALT) = RepeatObserveDestination

function lower_HALT_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCoreAction(CoreActionHalt), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]

function execute_HALT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_HALT_uops(instruction), instruction, state))
