function clause fp_semantics(Op_FBNDIX) =
  Some(fp_info(FpPathR, 3, FpResultFlagsVOnly, fflags_nv,
                              fp_flags_all, false, 0))


function clause register_result_extension(Op_FBNDIX) = RegisterZeroExtend

function clause repeat_semantics(Op_FBNDIX) = RepeatObserveDestination

function lower_FBNDIX_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_ternary(instruction) {
        Some(sources) => Some(
            uop_program_append(
                sources.program,
                [|
                    uop_make_ternary(
                        UopFpOperation(Op_FBNDIX),
                        sources.source0,
                        sources.source1,
                        sources.source2,
                        uop_location_make_none(),
                        Operand_value,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                    uop_make(
                        UopCommit(),
                        uop_location_make_none(),
                        uop_location_make_none(),
                        uop_location_make_none(),
                        Operand_value,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                |],
            ),
        ),
        None() => None(),
    }

function execute_FBNDIX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FBNDIX_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FBNDIX could not be lowered to micro-operations",
            ),
        ),
    }
