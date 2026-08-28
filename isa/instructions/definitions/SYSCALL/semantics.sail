function clause register_result_extension(Op_SYSCALL) = RegisterZeroExtend

function clause repeat_semantics(Op_SYSCALL) = RepeatObserveDestination

function lower_SYSCALL_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopEventControl(EventControlSyscall), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 0, CommitEvent)
|]

function execute_SYSCALL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_SYSCALL_uops(instruction), instruction, state))
