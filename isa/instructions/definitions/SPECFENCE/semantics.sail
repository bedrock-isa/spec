function clause register_result_extension(Op_SPECFENCE) = RegisterZeroExtend

function clause repeat_semantics(Op_SPECFENCE) = RepeatObserveDestination

function lower_SPECFENCE_uops(_ : Decoded_instruction) -> list(Uop) =
  [|uop_make(UopCoreAction(CoreActionSpeculationFence),
             uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]

function execute_SPECFENCE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_SPECFENCE_uops(instruction), instruction, state))
