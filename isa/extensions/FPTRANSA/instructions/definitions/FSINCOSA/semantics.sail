function clause fp_semantics(Op_FSINCOSA) =
  Some(fp_info(FpPathR, 1, FpResultFnPairByFormat, 0b10010,
                                fp_flags_none, true, 4))


function clause register_result_extension(Op_FSINCOSA) = RegisterZeroExtend

function clause repeat_semantics(Op_FSINCOSA) = RepeatObserveDestination

function lower_FSINCOSA_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (
        fp_source_at(instruction.operands, 0, 0),
        operand_named(instruction, Operand_sin_dst),
        operand_named(instruction, Operand_cos_dst),
    ) {
        (Some(source_operand), Some(sin_destination), Some(cos_destination))
          if sin_destination.value[3 .. 0] != cos_destination.value[3 .. 0] => {
            let width = operation_width(instruction);
            let source = uop_operand_lower(source_operand, width, 0, true);
            let contract = uop_location_make_temporary(32);
            let compute = {
                uop_make_pair(
                    UopFpOperation(Op_FSINCOSA),
                    source.value,
                    uop_location_make_none(),
                    uop_operand_location(sin_destination),
                    uop_operand_location(cos_destination),
                    Operand_sin_dst,
                    width,
                    CommitRegisters,
                ) with
                auxiliary = contract,
            };
            Some(
                uop_program_append(
                    [|
                        uop_make(UopFpContractQuery(), uop_location_make_none(), uop_location_make_none(), contract, Operand_src, width, CommitNone),
                        uop_make(
                            UopFpContractValidate(),
                            contract,
                            uop_location_make_none(),
                            uop_location_make_none(),
                            Operand_src,
                            width,
                            CommitNone,
                        ),
                    |],
                    uop_program_append(
                        source.program,
                        [|
                            compute,
                            uop_make(
                                UopCommit(),
                                uop_location_make_none(),
                                uop_location_make_none(),
                                uop_location_make_none(),
                                Operand_sin_dst,
                                width,
                                CommitRegisters,
                            ),
                        |],
                    ),
                ),
            )
        },
        _ => None(),
    }

function execute_FSINCOSA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FSINCOSA_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FSINCOSA could not be lowered to micro-operations",
            ),
        ),
    }
