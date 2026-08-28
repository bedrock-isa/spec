struct Lowered_fp_sources = {
  program : list(Micro_operation),
  source0 : Uop_location,
  source1 : Uop_location,
  source2 : Uop_location,
}

struct Lowered_fp_unary = {
  before_compute : list(Micro_operation),
  after_compute : list(Micro_operation),
  source : Uop_location,
  destination : Uop_location,
  commit_kind : Commit_kind,
}

function lower_fp_unary_operands(instruction : Decoded_instruction) -> option(Lowered_fp_unary) =
    match (fp_source_at(instruction.operands, 0, 0), operand_named(instruction, Operand_dst)) {
        (Some(source_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = lower_uop_operand(source_operand, width, 0, true);
            let destination = lower_uop_operand(destination_operand, width, source.next_temporary, false);
            if destination.memory then {
                let result = uop_temporary(destination.next_temporary);
                Some(
                    struct {
                        before_compute =
                            append_uops(
                                source.program,
                                append_uops(
                                    destination.program,
                                    [|
                                        make_uop(
                                            UopMemoryProbe(),
                                            destination.address,
                                            uop_none(),
                                            uop_none(),
                                            Operand_dst,
                                            width,
                                            CommitMemory,
                                        ),
                                    |],
                                ),
                            ),
                        after_compute =
                            [|
                                make_uop(
                                    UopMemoryStore(),
                                    result,
                                    destination.address,
                                    uop_none(),
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

function lower_fp_binary_sources(instruction : Decoded_instruction) -> option(Lowered_fp_sources) =
    match (fp_source_at(instruction.operands, 0, 0), fp_source_at(instruction.operands, 1, 0)) {
        (Some(first_operand), Some(second_operand)) => {
            let width = operation_width(instruction);
            let first = lower_uop_operand(first_operand, width, 0, true);
            let second = lower_uop_operand(second_operand, width, first.next_temporary, true);
            Some(
                struct {
                    program = append_uops(first.program, second.program),
                    source0 = first.value,
                    source1 = second.value,
                    source2 = uop_none(),
                },
            )
        },
        _ => None(),
    }

function lower_fp_ternary_sources(instruction : Decoded_instruction) -> option(Lowered_fp_sources) =
    match (
        fp_source_at(instruction.operands, 0, 0),
        fp_source_at(instruction.operands, 1, 0),
        fp_source_at(instruction.operands, 2, 0),
    ) {
        (Some(first_operand), Some(second_operand), Some(third_operand)) => {
            let width = operation_width(instruction);
            let first = lower_uop_operand(first_operand, width, 0, true);
            let second = lower_uop_operand(second_operand, width, first.next_temporary, true);
            let third = lower_uop_operand(third_operand, width, second.next_temporary, true);
            Some(
                struct {
                    program = append_uops(first.program, append_uops(second.program, third.program)),
                    source0 = first.value,
                    source1 = second.value,
                    source2 = third.value,
                },
            )
        },
        _ => None(),
    }
