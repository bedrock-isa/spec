function clause register_result_extension(Op_TEST) = RegisterZeroExtend

function clause repeat_semantics(Op_TEST) = RepeatObserveCompareFlags

function lower_TEST_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (first_binary_operand(instruction.operands), second_binary_operand(instruction.operands)) {
        (Some(left_operand), Some(right_operand)) => {
            let width = operation_width(instruction);
            let left = uop_operand_lower(left_operand, width, 0, true);
            let right = uop_operand_lower(right_operand, width, left.next_temporary, true);
            let test = uop_make(
                UopIntegerFlags(IntegerFlagsTest), left.value, right.value,
                uop_location_make_none(), Operand_dst, width, CommitRegisters
            );
            Some(uop_program_build(uop_program_append(left.program, right.program), [|test|],
                Operand_dst, width,
                if left.memory | right.memory then CommitMemory else CommitRegisters))
        },
        _ => None(),
    }

function execute_TEST(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_TEST_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "TEST could not be lowered to micro-operations")),
    }
