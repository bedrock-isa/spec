function clause register_result_extension(Op_RDTIME) = RegisterZeroExtend

function clause repeat_semantics(Op_RDTIME) = RepeatObserveDestination

function lower_RDTIME_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTime(TimeRead), uop_location_make_none(), uop_location_make_none(),
           uop_location_make_none(), Operand_dst, 8, CommitRegisters)
|]

function execute_RDTIME(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_RDTIME_uops(instruction), instruction, state))
