function clause register_result_extension(Op_TARM) = RegisterZeroExtend

function clause repeat_semantics(Op_TARM) = RepeatObserveDestination

function lower_TARM_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTime(TimeArm), uop_location_make_none(), uop_location_make_none(),
           uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_TARM(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_TARM_uops(instruction), instruction, state))
