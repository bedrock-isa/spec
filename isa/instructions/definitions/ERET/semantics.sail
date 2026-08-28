function clause register_result_extension(Op_ERET) = RegisterZeroExtend

function clause repeat_semantics(Op_ERET) = RepeatObserveDestination

function lower_ERET_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopEventControl(EventControlReturn), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 0, CommitEvent)
|]

function execute_ERET(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_ERET_uops(instruction), instruction, state))
