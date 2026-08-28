struct Fp_source_lowering = {
  program : list(Uop),
  source0 : Uop_location,
  source1 : Uop_location,
  source2 : Uop_location,
}

struct Fp_unary_operand_lowering = {
  before_compute : list(Uop),
  after_compute : list(Uop),
  source : Uop_location,
  destination : Uop_location,
  commit_kind : Commit_kind,
}

function fp_operands_lower_unary(instruction : Decoded_instruction) -> option(Fp_unary_operand_lowering) =
    match (fp_source_at(instruction.operands, 0, 0), operand_named(instruction, Operand_dst)) {
        (Some(source_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = uop_operand_lower(source_operand, width, 0, true);
            let destination = uop_operand_lower(destination_operand, width, source.next_temporary, false);
            if destination.memory then {
                let result = uop_location_make_temporary(destination.next_temporary);
                Some(
                    struct {
                        before_compute =
                            uop_program_append(
                                source.program,
                                uop_program_append(
                                    destination.program,
                                    [|
                                        uop_make(
                                            UopMemoryProbe(),
                                            destination.address,
                                            uop_location_make_none(),
                                            uop_location_make_none(),
                                            Operand_dst,
                                            width,
                                            CommitMemory,
                                        ),
                                    |],
                                ),
                            ),
                        after_compute =
                            [|
                                uop_make(
                                    UopMemoryStore(),
                                    result,
                                    destination.address,
                                    uop_location_make_none(),
                                    Operand_dst,
                                    width,
                                    CommitMemory,
                                ),
                            |],
                        source = source.value,
                        destination = result,
                        commit_kind = CommitMemory,
                    },
                )
            } else {
                Some(
                    struct {
                        before_compute = source.program,
                        after_compute = [||],
                        source = source.value,
                        destination = destination.value,
                        commit_kind = CommitRegisters,
                    },
                )
            }
        },
        _ => None(),
    }

function fp_operands_lower_binary(instruction : Decoded_instruction) -> option(Fp_source_lowering) =
    match (fp_source_at(instruction.operands, 0, 0), fp_source_at(instruction.operands, 1, 0)) {
        (Some(first_operand), Some(second_operand)) => {
            let width = operation_width(instruction);
            let first = uop_operand_lower(first_operand, width, 0, true);
            let second = uop_operand_lower(second_operand, width, first.next_temporary, true);
            Some(
                struct {
                    program = uop_program_append(first.program, second.program),
                    source0 = first.value,
                    source1 = second.value,
                    source2 = uop_location_make_none(),
                },
            )
        },
        _ => None(),
    }

function fp_operands_lower_ternary(instruction : Decoded_instruction) -> option(Fp_source_lowering) =
    match (
        fp_source_at(instruction.operands, 0, 0),
        fp_source_at(instruction.operands, 1, 0),
        fp_source_at(instruction.operands, 2, 0),
    ) {
        (Some(first_operand), Some(second_operand), Some(third_operand)) => {
            let width = operation_width(instruction);
            let first = uop_operand_lower(first_operand, width, 0, true);
            let second = uop_operand_lower(second_operand, width, first.next_temporary, true);
            let third = uop_operand_lower(third_operand, width, second.next_temporary, true);
            Some(
                struct {
                    program = uop_program_append(first.program, uop_program_append(second.program, third.program)),
                    source0 = first.value,
                    source1 = second.value,
                    source2 = third.value,
                },
            )
        },
        _ => None(),
    }
