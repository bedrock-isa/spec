function clause fp_semantics(Op_RDFFLAGS) = None()

function clause register_result_extension(Op_RDFFLAGS) = RegisterZeroExtend

function clause repeat_semantics(Op_RDFFLAGS) = RepeatObserveDestination

function lower_RDFFLAGS_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    Some([|
        uop_make(UopFpState(FpStateReadFlags), uop_location_make_none(), uop_location_make_none(),
                 uop_location_make_none(), Operand_dst, operation_width(instruction), CommitRegisters),
        uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(),
                 uop_location_make_none(), Operand_dst, operation_width(instruction), CommitRegisters),
    |])

function execute_RDFFLAGS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_RDFFLAGS_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "RDFFLAGS could not be lowered to micro-operations")),
    }
