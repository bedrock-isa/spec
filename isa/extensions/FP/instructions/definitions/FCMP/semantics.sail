function clause fp_semantics(Op_FCMP) =
  Some(fp_info(FpPathR, 2, FpResultFlags, fflags_nv,
                            fp_flags_all, false, 0))


function clause register_result_extension(Op_FCMP) = RegisterZeroExtend

function clause repeat_semantics(Op_FCMP) = RepeatObserveDestination

function lower_FCMP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_binary(instruction) {
        Some(sources) => {
            let width = operation_width(instruction);
            let destination : Uop_location = match operand_named(instruction, Operand_dst) {
                Some(operand) => uop_operand_location(operand),
                None() => uop_location_make_none(),
            };
            let compute = uop_make(
                UopFpCompare(FpCompareOrdered),
                sources.source0,
                sources.source1,
                destination,
                Operand_dst,
                width,
                CommitRegisters,
            );
            Some(
                uop_program_append(
                    sources.program,
                    [|
                        compute,
                        uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, width, CommitRegisters),
                    |],
                ),
            )
        },
        None() => None(),
    }

function execute_FCMP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCMP_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCMP could not be lowered to micro-operations",
            ),
        ),
    }
