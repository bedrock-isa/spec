function cfi_jump_program(program : list(Uop), instruction : Decoded_instruction,
                          state : Cpu_state) -> list(Uop) =
  if cfi_key_configured(state) & cfi_indirect_target(instruction)
  then cfi_with_landing_check(program) else program

function cfi_execute_optional_call(program : option(list(Uop)),
                                   instruction : Decoded_instruction,
                                   state : Cpu_state) -> Execution_result =
  match program {
    Some(selected) => uop_program_execute(
      cfi_call_program(selected, instruction, state), instruction, state
    ),
    None() => faulted(
      state, instruction.form.operation, IllegalInstruction,
      "CFI could not lower call operation"
    ),
  }

function cfi_execute_optional_jump(program : option(list(Uop)),
                                   instruction : Decoded_instruction,
                                   state : Cpu_state) -> Execution_result =
  match program {
    Some(selected) => uop_program_execute(
      cfi_jump_program(selected, instruction, state), instruction, state
    ),
    None() => faulted(
      state, instruction.form.operation, IllegalInstruction,
      "CFI could not lower jump operation"
    ),
  }

function cpuid_flag_enabled(flag : Cpuid_flag, state : Cpu_state) -> bool =
  if flag == CpuidFlag_CFI then true else base_cpuid_flag_enabled(flag, state)

function execute_operation_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result =
  match instruction.form.operation {
    Op_CALL => cfi_execute_optional_call(lower_CALL_uops(instruction), instruction, state),
    Op_CALLcc => cfi_execute_optional_call(lower_CALLcc_uops(instruction), instruction, state),
    Op_FCALL => cfi_execute_optional_call(lower_FCALL_uops(instruction), instruction, state),
    Op_LCALL => cfi_execute_optional_call(lower_LCALL_uops(instruction), instruction, state),
    Op_JMP => cfi_execute_optional_jump(lower_JMP_uops(instruction), instruction, state),
    Op_LJMP => cfi_execute_optional_jump(lower_LJMP_uops(instruction), instruction, state),
    Op_IJcc => cfi_execute_optional_jump(lower_IJcc_uops(instruction), instruction, state),
    Op_DJcc => cfi_execute_optional_jump(lower_DJcc_uops(instruction), instruction, state),
    Op_RET => uop_program_execute(lower_RET_uops(instruction, state), instruction, state),
    Op_LRET => uop_program_execute(lower_LRET_uops(instruction), instruction, state),
    _ => execute_base_operation_entry(instruction, state),
  }

function event_from_fault(result : Execution_result) -> Event_record =
  match result.fault {
    Some(fault) =>
      if fault.kind == CfiViolationFault then {
        var event = make_event(
          EventSynchronous, EventFrameError, 0x00000044, 3, result.state.pc
        );
        event.error_code = fault.error_code;
        event
      }
      else base_event_from_fault(result),
    None() => base_event_from_fault(result),
  }
