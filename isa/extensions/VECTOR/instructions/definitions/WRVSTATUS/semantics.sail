function clause register_result_extension(Op_WRVSTATUS) = RegisterZeroExtend

function clause repeat_semantics(Op_WRVSTATUS) = RepeatObserveDestination

function lower_WRVSTATUS_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    Some([|
        uop_make(UopVectorStateWrite(), uop_location_make_none(), uop_location_make_none(),
                 uop_location_make_none(), Operand_dst, operation_width(instruction), CommitRegisters),
        uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(),
                 uop_location_make_none(), Operand_dst, operation_width(instruction), CommitRegisters),
    |])

function execute_WRVSTATUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_WRVSTATUS_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "WRVSTATUS could not be lowered to micro-operations")),
    }
