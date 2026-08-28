function fp_start_operands(instruction : Decoded_instruction, state : Cpu_state,
                           contract_word : bits(64)) -> Execution_result =
  if not_bool(fp_fstatus_valid(state.fstatus)) then faulted_with_error_code(
    state, instruction.form.operation, InvalidControlState,
    "reserved FSTATUS bits are nonzero", 0x0000000000000001
  )
  else match fp_semantics(instruction.form.operation) {
    None() => faulted(state, instruction.form.operation, IllegalInstruction,
                      "missing floating-point semantics"),
    Some(semantics) => {
      let evaluated = evaluate_instruction_eas(
        instruction.operands, instruction.form.operation, state, state.pc,
        operation_width(instruction)
      );
      let slots = fp_initial_slots(
        instruction, state, semantics.source_count, 0, empty_fp_operand_slots()
      );
      let missing = fp_first_missing_source(slots, semantics.source_count, 0);
      let path : Fp_path = match fp_form_path(instruction.form) {
        Some(value) => value, None() => FpPathR,
      };
      let result_kind : Fp_result_kind = match fp_derive_result_kind(
        instruction.form, operation_width(instruction)
      ) { Some(value) => value, None() => FpResultValueNone };
      let pending = fp_pending_with_slots(
        { empty_fp_pending() with valid = true, path = path, next_source = missing,
          fstatus_image = state.fstatus[9 .. 0],
          destination_kind = fp_derive_destination_kind(instruction.form),
          result_kind = result_kind, contract_word = contract_word }, slots
      );
      let after = advance_pc(evaluated.image, instruction);
      if missing < semantics.source_count then match fp_source_at(
        instruction.operands, missing, 0
      ) {
        Some(source) => match evaluation_named(source.name, evaluated.evaluations) {
          Some(evaluation) => fp_waiting(
            state, after, instruction, PhaseFpSourceRead, 0,
            request_for_evaluation(MemoryRead, 0, evaluation, AccessLoad,
                                   0x0000000000000000, false), pending
          ),
          None() => faulted(state, instruction.form.operation, InvalidControlState,
                            "missing FP source evaluation"),
        },
        None() => faulted(state, instruction.form.operation, InvalidControlState,
                          "missing FP source operand"),
      }
      else fp_continue_after_sources(
        instruction, state, after, pending, contract_word, 0
      )
    },
  }

function start_fp_transaction(instruction : Decoded_instruction,
                              state : Cpu_state) -> Execution_result =
  if instruction.form.operation == Op_FPUSHP | instruction.form.operation == Op_FPOPP then
    match start_stack_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction,
                        "invalid floating-point stack form"),
    }
  else match fp_semantics(instruction.form.operation) {
    Some(semantics) =>
      if semantics.transcendental then fp_waiting(
        state, state, instruction, PhaseFpContractQuery, 0,
        { empty_primitive_request() with
          kind = CpuidQueryRequest, role = RequestRoleFpApproximationContractQuery,
          selector = fp_approx_cpuid_selector(semantics.contract_id) }, empty_fp_pending()
      )
      else fp_start_operands(instruction, state, 0x0000000000000000),
    None() => faulted(state, instruction.form.operation, IllegalInstruction,
                      "unknown floating-point operation"),
  }
