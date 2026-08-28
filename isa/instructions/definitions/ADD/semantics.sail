function clause register_result_extension(Op_ADD) = RegisterZeroExtend

function clause repeat_semantics(Op_ADD) = RepeatObserveDestination

function add_source_operand(instruction : Decoded_instruction) -> option(Decoded_operand) =
    match operand_named(instruction, Operand_src) {
        Some(source) => Some(source),
        None() => operand_named(instruction, Operand_imm),
    }

function lower_ADD_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (add_source_operand(instruction), operand_named(instruction, Operand_dst)) {
        (Some(source_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = uop_operand_lower(source_operand, width, 0, true);
            let destination = uop_operand_lower(destination_operand, width, source.next_temporary, true);
            let arithmetic = uop_make(
                UopIntegerAdd(),
                destination.value,
                source.value,
                destination.value,
                Operand_dst,
                width,
                CommitRegisters,
            );
            Some(uop_program_build_operation(
              uop_program_append(source.program, destination.program), arithmetic, destination.value, destination,
              Operand_dst, width, source.memory | destination.memory
            ))
        },
        _ => None(),
    }

function execute_ADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_ADD_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "ADD could not be lowered to micro-operations",
            ),
        ),
    }
