function clause register_result_extension(Op_TCANCEL) = RegisterZeroExtend

function clause repeat_semantics(Op_TCANCEL) = RepeatObserveDestination

function lower_TCANCEL_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTime(TimeCancel), uop_location_make_none(), uop_location_make_none(),
           uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_TCANCEL(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_TCANCEL_uops(instruction), instruction, state))
