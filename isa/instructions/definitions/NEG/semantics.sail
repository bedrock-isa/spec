function clause register_result_extension(Op_NEG) = RegisterZeroExtend

function clause repeat_semantics(Op_NEG) = RepeatObserveDestination

function lower_NEG_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match operand_named(instruction, Operand_dst) {
        Some(destination_operand) => {
            let width = operation_width(instruction);
            let destination = uop_operand_lower(destination_operand, width, 0, true);
            let operation = uop_make(
                UopIntegerUnary(IntegerUnaryNegate), destination.value, uop_location_make_none(),
                destination.value, Operand_dst, width, CommitRegisters
            );
            Some(uop_program_build_operation(
              destination.program, operation, destination.value, destination,
              Operand_dst, width, destination.memory
            ))
        },
        None() => None(),
    }

function execute_NEG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_NEG_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "NEG could not be lowered to micro-operations")),
    }
