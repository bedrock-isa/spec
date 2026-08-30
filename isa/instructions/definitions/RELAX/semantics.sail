function clause register_result_extension(Op_RELAX) = RegisterZeroExtend

function clause repeat_semantics(Op_RELAX) = RepeatObserveDestination

function lower_RELAX_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCoreAction(CoreActionWait), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]

function execute_RELAX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RELAX_uops(instruction), instruction, state))
