function clause register_result_extension(Op_NOP) = RegisterZeroExtend

function clause repeat_semantics(Op_NOP) = RepeatObserveDestination

function lower_NOP_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 0, CommitControl)|]

function execute_NOP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_NOP_uops(instruction), instruction, state))
