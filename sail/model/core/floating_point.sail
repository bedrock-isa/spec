function floating_value_named(instruction : Decoded_instruction, state : Cpu_state,
                              name : string) -> option(bits(64)) =
  match operand_named(instruction, name) {
    Some(operand) => if operand.type_name == "Fn" then
      Some(state.floating_registers[unsigned(operand.value[3 .. 0])])
      else None(),
    None() => None(),
  }

function commit_fp_local_value(instruction : Decoded_instruction, state : Cpu_state,
                               value : bits(64)) -> option(Execution_result) =
  match operand_named(instruction, "dst") {
    Some(destination) => {
      var updated = advance_pc(state, instruction);
      let width = operation_width(instruction);
      if destination.type_name == "Fn" then {
        updated.floating_registers[unsigned(destination.value[3 .. 0])] =
          if width == 4 then 0x00000000 @ value[31 .. 0] else value;
        updated.fp_component_modified = true;
        Some(completed(state, updated, CommitRegisters, [||]))
      }
      else if destination.type_name == "Rn" then {
        updated.registers[unsigned(destination.value[3 .. 0])] = value;
        Some(completed(state, updated, CommitRegisters, [||]))
      }
      else None()
    },
    None() => None(),
  }

function execute_fp_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let width = operation_width(instruction);
  if operation == Op_FCLR then commit_fp_local_value(
    instruction, state, fp_bitwise_fclr()
  )
  else if operation == Op_FMOV | operation == Op_FMOVcc
       | operation == Op_FABS | operation == Op_FNEG then
    match floating_value_named(instruction, state, "src") {
      None() => None(),
      Some(source) => {
        let value = if operation == Op_FABS then fp_bitwise_fabs(source, width)
          else if operation == Op_FNEG then fp_bitwise_fneg(source, width)
          else fp_bitwise_fmov(source, width);
        match value {
          Some(result) => commit_fp_local_value(instruction, state, result),
          None() => None(),
        }
      },
    }
  else if operation == Op_FCOPYSIGN then match (
    floating_value_named(instruction, state, "sign_src"),
    floating_value_named(instruction, state, "magnitude_src")
  ) {
    (Some(sign_source), Some(magnitude_source)) => match fp_bitwise_fcopysign(
      sign_source, magnitude_source, width
    ) {
      Some(result) => commit_fp_local_value(instruction, state, result),
      None() => None(),
    },
    _ => None(),
  }
  else if operation == Op_FCLASS then match floating_value_named(instruction, state, "src") {
    Some(source) => match fp_fclass(source, width) {
      Some(result) => commit_fp_local_value(instruction, state, result),
      None() => None(),
    },
    None() => None(),
  }
  else if operation == Op_FMOVCR then match operand_named(instruction, "constant_id") {
    Some(constant_operand) => match fp_fmovcr(constant_operand.value[15 .. 0]) {
      Some(result) => commit_fp_local_value(instruction, state, result),
      None() => None(),
    },
    None() => None(),
  }
  else if operation == Op_FXCHG then match (
    operand_named(instruction, "lhs"), operand_named(instruction, "rhs")
  ) {
    (Some(lhs), Some(rhs)) => {
      let left = unsigned(lhs.value[3 .. 0]);
      let right = unsigned(rhs.value[3 .. 0]);
      let exchange = fp_bitwise_fxchg(
        state.floating_registers[left], state.floating_registers[right]
      );
      var updated = advance_pc(state, instruction);
      updated.floating_registers[left] = exchange.lhs;
      updated.floating_registers[right] = exchange.rhs;
      updated.fp_component_modified = true;
      Some(completed(state, updated, CommitRegisters, [||]))
    },
    _ => None(),
  }
  else None()
}

function fp_source_candidate(operand : Decoded_operand) -> bool =
  (operand.access == AccessRead | operand.access == AccessReadWrite)
  & (operand.type_name == "Fn" | operand.type_name == "Rn"
     | operand.type_name == "EA" | operand.type_name == "imm64")

function fp_source_at(operands : list(Decoded_operand), wanted : int,
                      current : int) -> option(Decoded_operand) = match operands {
  [||] => None(),
  operand :: tail =>
    if fp_source_candidate(operand) then
      if current == wanted then Some(operand)
      else fp_source_at(tail, wanted, current + 1)
    else fp_source_at(tail, wanted, current),
}

function fp_destination_is_fn(instruction : Decoded_instruction) -> bool =
  match operand_named(instruction, "dst") {
    Some(destination) => destination.type_name == "Fn",
    None() => false,
  }

function fp_operand_kind_for(instruction : Decoded_instruction,
                             operand : Decoded_operand, width : int) -> Fp_value_kind =
  if operand.type_name == "Fn" then
    if (instruction.form.operation == Op_FCVT | instruction.form.operation == Op_FCVTU)
       & fp_destination_is_fn(instruction) then
      if width == 4 then FpBits64 else FpBits32
    else if width == 4 then FpBits32 else FpBits64
  else if (instruction.form.operation == Op_FCVT
           | instruction.form.operation == Op_FCVTU)
          & fp_destination_is_fn(instruction) then
    if instruction.form.operation == Op_FCVTU then FpUnsigned64 else FpSigned64
  else if operand.type_name == "Rn" then FpRaw64
  else if width == 4 then FpBits32 else FpBits64

function fp_decoded_operand_image(instruction : Decoded_instruction, state : Cpu_state,
                                  operand : Decoded_operand,
                                  width : int) -> Fp_operand_image = {
  let raw = if operand.type_name == "Fn" then
    state.floating_registers[unsigned(operand.value[3 .. 0])]
  else if operand.type_name == "Rn" then state.registers[unsigned(operand.value[3 .. 0])]
  else operand.value;
  let kind = fp_operand_kind_for(instruction, operand, width);
  struct { valid = operand.type_name != "EA",
           kind = kind,
           bits = if kind == FpBits32 then 0x00000000 @ raw[31 .. 0] else raw }
}

function fp_pending_raw_slots(pending : Fp_pending_image) -> Fp_operand_slots = struct {
  operand0 = pending.raw0, operand1 = pending.raw1, operand2 = pending.raw2
}

function fp_pending_with_slots(pending : Fp_pending_image,
                               slots : Fp_operand_slots) -> Fp_pending_image =
  { pending with raw0 = slots.operand0, raw1 = slots.operand1, raw2 = slots.operand2,
                 source_valid = fp_operand_valid_bitmap(slots) }

function fp_initial_slots(instruction : Decoded_instruction, state : Cpu_state,
                          count : int, index : int,
                          slots : Fp_operand_slots) -> Fp_operand_slots =
  if index >= count then slots
  else match fp_source_at(instruction.operands, index, 0) {
    None() => slots,
    Some(operand) => match fp_operand_slot_set(
      slots, index, fp_decoded_operand_image(instruction, state, operand,
                                             operation_width(instruction))
    ) {
      Some(updated) => fp_initial_slots(instruction, state, count, index + 1, updated),
      None() => slots,
    },
  }

function fp_first_missing_source(slots : Fp_operand_slots, count : int,
                                 index : int) -> int =
  if index >= count then count
  else match fp_operand_slot_get(slots, index) {
    Some(operand) => if operand.valid then fp_first_missing_source(slots, count, index + 1)
                     else index,
    None() => count,
  }

function fp_writable_fn_at(operands : list(Decoded_operand), wanted : int,
                           current : int) -> option(Decoded_operand) = match operands {
  [||] => None(),
  operand :: tail =>
    if operand.type_name == "Fn"
       & (operand.access == AccessWrite | operand.access == AccessReadWrite) then
      if current == wanted then Some(operand)
      else fp_writable_fn_at(tail, wanted, current + 1)
    else fp_writable_fn_at(tail, wanted, current),
}

function fp_contract_selector(instruction : Decoded_instruction) -> bits(64) =
  match fp_semantics(instruction.form.operation) {
    Some(semantics) => fptrans_cpuid_selector(semantics.contract_id),
    None() => 0x0000000000000000,
  }

function fp_waiting(before : Cpu_state, after : Cpu_state,
                    instruction : Decoded_instruction, phase : Continuation_phase,
                    ordinal : int, request : Primitive_request,
                    fp_pending : Fp_pending_image) -> Execution_result = {
  let waiting = waiting_transaction(
    before, after, instruction, CommitRegisters,
    commit_destination_for(instruction.operands, operation_width(instruction)),
    phase, ordinal, 0x0000000000000000, 0x0000000000000000, request
  );
  { waiting with pending = { waiting.pending with fp_pending = fp_pending } }
}

function fp_preserve_repeat_parent(previous : Execution_result,
                                   next : Execution_result) -> Execution_result =
  { next with pending = { next.pending with
      repeat_prefix = previous.pending.repeat_prefix,
      repeat_body = previous.pending.repeat_body,
      repeat_bytes = previous.pending.repeat_bytes,
      repeat_tail = previous.pending.repeat_tail,
      repeat_tail_length = previous.pending.repeat_tail_length,
      repeat_parent_active = previous.pending.repeat_parent_active,
      repeat_parent_grouped = previous.pending.repeat_parent_grouped,
      boundary_class = previous.pending.boundary_class } }

function fp_fault_with_causes(state : Cpu_state, operation : Semantic_operation,
                              causes : bits(5)) -> Execution_result = {
  let base = faulted(state, operation, FloatingPointFault,
                     "enabled floating-point exception");
  { base with fault = Some(struct {
      kind = FloatingPointFault, operation = operation,
      detail = "enabled floating-point exception",
      error_code = sail_zero_extend(causes, 64), bus_error = false
    }) }
}

val fp_start_compute : (Decoded_instruction, Cpu_state, Cpu_state,
                        Fp_pending_image, bits(64), int) -> Execution_result

function fp_commit_candidate(before : Cpu_state, after : Cpu_state,
                             instruction : Decoded_instruction,
                             candidate : Fp_candidate_result,
                             fp_pending : Fp_pending_image,
                             ordinal : int) -> Execution_result =
  if not_bool(candidate.shape_valid) then faulted(
    before, instruction.form.operation, InvalidControlState,
    "invalid floating-point response shape or echo"
  )
  else if candidate.trap then
    fp_fault_with_causes(before, instruction.form.operation, candidate.trap_errors)
  else {
    var updated = after;
    updated.fflags = updated.fflags | candidate.generated_causes;
    updated.flags = (updated.flags & not_vec(candidate.flags_mask))
                  | (candidate.flags_value & candidate.flags_mask);
    let destination_kind = fp_derive_destination_kind(instruction.form);
    if destination_kind == FpDestinationFn then match fp_writable_fn_at(
      instruction.operands, 0, 0
    ) {
      Some(destination) => {
        let index = unsigned(destination.value[3 .. 0]);
        updated.floating_registers[index] = if candidate.result_kind == FpResultBits32
          then 0x00000000 @ candidate.primary[31 .. 0] else candidate.primary;
        updated.fp_component_modified = true
      },
      None() => return faulted(before, instruction.form.operation,
                               InvalidControlState, "missing FP destination"),
    }
    else if destination_kind == FpDestinationFnPair then match (
      fp_writable_fn_at(instruction.operands, 0, 0),
      fp_writable_fn_at(instruction.operands, 1, 0)
    ) {
      (Some(first), Some(second)) => {
        updated.floating_registers[unsigned(first.value[3 .. 0])] =
          if candidate.result_kind == FpResultPair32
          then 0x00000000 @ candidate.primary[31 .. 0] else candidate.primary;
        updated.floating_registers[unsigned(second.value[3 .. 0])] =
          if candidate.result_kind == FpResultPair32
          then 0x00000000 @ candidate.secondary[31 .. 0] else candidate.secondary;
        updated.fp_component_modified = true
      },
      _ => return faulted(before, instruction.form.operation,
                          InvalidControlState, "missing FP pair destination"),
    }
    else if destination_kind == FpDestinationRn then match operand_named(instruction, "dst") {
      Some(destination) => updated.registers[unsigned(destination.value[3 .. 0])]
                         = candidate.primary,
      None() => return faulted(before, instruction.form.operation,
                               InvalidControlState, "missing integer FP destination"),
    }
    else ();
    if candidate.generated_causes != 0b00000 then updated.fp_component_modified = true else ();
    if destination_kind == FpDestinationMemory then {
      let evaluated = evaluate_instruction_eas(
        instruction.operands, instruction.form.operation, before, before.pc,
        operation_width(instruction)
      );
      match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
        None() => faulted(before, instruction.form.operation, InvalidControlState,
                          "missing FP memory destination"),
        Some(destination) => {
          let staged_pending = { fp_pending with
            candidate0 = candidate.primary, candidate1 = candidate.secondary,
            candidate_flags = candidate.flags_value,
            candidate_causes = candidate.generated_causes };
          fp_waiting(
            before, updated, instruction, PhaseFpDestinationWrite, ordinal,
            request_for_evaluation(MemoryStore, ordinal, destination, AccessStore,
                                   candidate.primary, true), staged_pending
          )
        },
      }
    }
    else completed(before, updated, CommitRegisters, [||])
  }

function fp_start_compute(instruction : Decoded_instruction, before : Cpu_state,
                          after : Cpu_state, fp_pending : Fp_pending_image,
                          contract_word : bits(64), ordinal : int) -> Execution_result =
  match (fp_form_path(instruction.form),
         fp_derive_result_kind(instruction.form, operation_width(instruction))) {
    (Some(path), Some(result_kind)) => match fp_build_request(
      instruction.form.operation, instruction.form, path, result_kind,
      fp_pending_raw_slots(fp_pending), before.fstatus, contract_word
    ) {
      None() => faulted(before, instruction.form.operation, InvalidControlState,
                        "invalid floating-point request image"),
      Some(request_image) => {
        let prepared_pending = { fp_pending with
          effective0 = request_image.operand0, effective1 = request_image.operand1,
          effective2 = request_image.operand2, result_kind = result_kind,
          flags_mask = request_image.flags_mask, contract_id = request_image.contract_id,
          contract_word = request_image.contract_word };
        let selector : bits(64) = match operand_named(instruction, "constant_id") {
          Some(value) => value.value, None() => 0x0000000000000000,
        };
        match fp_local_response(request_image, selector) {
          Some(local_response) => fp_commit_candidate(
            before, after, instruction,
            fp_finalize_response(request_image, local_response, before.fstatus),
            prepared_pending, ordinal
          ),
          None() => fp_waiting(
            before, after, instruction, PhaseFpCompute, ordinal,
            { empty_primitive_request() with
              kind = FloatingPointRequest, ordinal = ordinal,
              role = "floating_point_compute", width = operation_width(instruction),
              commit_point = false, fp_request = request_image,
              state_image = before }, prepared_pending
          ),
        }
      },
    },
    _ => faulted(before, instruction.form.operation, InvalidControlState,
                 "missing floating-point form semantics"),
  }

function fp_continue_after_sources(instruction : Decoded_instruction,
                                   before : Cpu_state, after : Cpu_state,
                                   fp_pending : Fp_pending_image,
                                   contract_word : bits(64), ordinal : int)
  -> Execution_result = {
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, before, before.pc,
    operation_width(instruction)
  );
  match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
    Some(destination) => fp_waiting(
      before, after, instruction, PhaseFpDestinationProbe, ordinal,
      request_for_evaluation(MemoryProbe, ordinal, destination, AccessStore,
                             0x0000000000000000, false), fp_pending
    ),
    None() => fp_start_compute(
      instruction, before, after, fp_pending, contract_word, ordinal
    ),
  }
}

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
          kind = CpuidQueryRequest, role = "fptrans_contract_query",
          selector = fptrans_cpuid_selector(semantics.contract_id),
          state_image = state }, empty_fp_pending()
      )
      else fp_start_operands(instruction, state, 0x0000000000000000),
    None() => faulted(state, instruction.form.operation, IllegalInstruction,
                      "unknown floating-point operation"),
  }

function execute_external_route(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = match instruction.form.route {
  RouteIntegerAlu => match start_memory_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form")
  },
  RouteIntegerUnary => match start_memory_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer unary form")
  },
  RouteIntegerBitfield => match start_memory_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved bitfield form")
  },
  RouteIntegerMulDiv => match start_memory_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved multiply/divide form")
  },
  RouteDataMovement => match start_stack_transaction(instruction, state) {
    Some(result) => result,
    None() => match start_memory_transaction(instruction, state) {
      Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form")
    }
  },
  RouteBounds => match start_memory_transaction(instruction, state) {
    Some(result) => result,
    None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved bounds form")
  },
  RouteAtomics => match start_atomic_transaction(instruction, state) {
    Some(result) => result,
    None() => faulted(state, instruction.form.operation, IllegalInstruction,
                      "missing atomic memory operand"),
  },
  RouteCache =>
    if instruction.form.operation == Op_MOVNT then match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, Op_MOVNT, IllegalInstruction,
                        "missing non-temporal store operand"),
    }
    else match start_cache_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction,
                        "missing cache address operand"),
    },
  RouteEaUtility => match execute_lea_transaction(instruction, state) {
    Some(result) => result,
    None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved EA utility form")
  },
  RouteFpu => start_fp_transaction(instruction, state),
  RouteFpuTranscendental => start_fp_transaction(instruction, state),
  RouteSystemRegisters => start_system_request(instruction, state),
  RouteTlbContext => start_tlb_context_transaction(instruction, state),
  RouteControlFlow => execute_control_exact(instruction, state),
  RouteCoreControl => execute_core_exact(instruction, state),
}

