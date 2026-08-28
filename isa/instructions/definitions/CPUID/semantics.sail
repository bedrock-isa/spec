function clause register_result_extension(Op_CPUID) = RegisterZeroExtend

function clause repeat_semantics(Op_CPUID) = RepeatObserveDestination

function lower_CPUID_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemRequest(SystemCpuid), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_CPUID(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_CPUID_uops(instruction), instruction, state))
