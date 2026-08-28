function clause register_result_extension(Op_BKPT) = RegisterZeroExtend

function clause repeat_semantics(Op_BKPT) = RepeatObserveDestination

function lower_BKPT_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopEventControl(EventControlBreakpoint), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 0, CommitEvent)
|]

function execute_BKPT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_BKPT_uops(instruction), instruction, state))
