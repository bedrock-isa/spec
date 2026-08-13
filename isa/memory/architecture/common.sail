function warm_reset_state(state : Cpu_state) -> Cpu_state = {
  var reset = initial_cpu();
  reset.fp_enabled = state.fp_enabled;
  reset.fptrans_enabled = state.fptrans_enabled;
  reset.cache_maintenance_granule = state.cache_maintenance_granule;
  reset.save_area_size = state.save_area_size;
  reset.save_fixed_size = state.save_fixed_size;
  reset.save_format = state.save_format;
  reset.save_bitmap_words = state.save_bitmap_words;
  reset.fp_component_present = state.fp_component_present;
  reset.fp_component_id = state.fp_component_id;
  reset.fp_component_bitmap_bit = state.fp_component_bitmap_bit;
  reset.fp_component_offset = state.fp_component_offset;
  reset.fp_component_size = state.fp_component_size;
  reset.fp_component_alignment = state.fp_component_alignment;
  reset.fp_component_init_policy = state.fp_component_init_policy;
  reset.controls[23] = state.controls[23];
  reset.controls[24] = state.controls[24];
  reset.pc = state.controls[23];
  reset.status = 0x0000000000000010;
  reset.supervisor = true;
  reset.halted = false;
  reset.run_state = Running;
  reset
}

function evaluation_named(name : string, evaluations : list(Ea_evaluation))
  -> option(Ea_evaluation) = match evaluations {
  [||] => None(),
  evaluation :: tail => if evaluation.operand_name == name then Some(evaluation)
                        else evaluation_named(name, tail),
}

function memory_evaluation_for(operands : list(Decoded_operand), evaluations : list(Ea_evaluation),
                               source : bool) -> option(Ea_evaluation) = match operands {
  [||] => None(),
  operand :: tail => match evaluation_named(operand.name, evaluations) {
    Some(evaluation) =>
      if evaluation.kind == "memory"
         & (if source then operand.access == AccessRead | operand.access == AccessReadWrite
            else operand.access == AccessWrite | operand.access == AccessReadWrite)
      then Some(evaluation)
      else memory_evaluation_for(tail, evaluations, source),
    None() => memory_evaluation_for(tail, evaluations, source),
  },
}

function next_memory_source(operands : list(Decoded_operand), evaluations : list(Ea_evaluation),
                            previous_name : string) -> option(Ea_evaluation) = match operands {
  [||] => None(),
  operand :: tail => match evaluation_named(operand.name, evaluations) {
    Some(evaluation) =>
      if evaluation.kind == "memory" & evaluation.operand_name != previous_name
         & (operand.access == AccessRead | operand.access == AccessReadWrite)
      then Some(evaluation)
      else next_memory_source(tail, evaluations, previous_name),
    None() => next_memory_source(tail, evaluations, previous_name),
  },
}

function evaluation_option_named(value : option(Ea_evaluation), name : string) -> bool = match value {
  Some(item) => item.operand_name == name,
  None() => false,
}

function evaluation_option_name(value : option(Ea_evaluation)) -> string = match value {
  Some(item) => item.operand_name,
  None() => "",
}

function request_for_evaluation(kind : Primitive_request_kind, ordinal : int,
                                evaluation : Ea_evaluation, access : Transaction_access,
                                value : bits(64), commit_point : bool) -> Primitive_request = struct {
  kind = kind, ordinal = ordinal, role = evaluation.role, domain = evaluation.domain,
  segment = evaluation.segment, segment_image = evaluation.segment_image,
  width = evaluation.width, range_start = evaluation.effective_address,
  range_end = add_bits(evaluation.effective_address, get_slice_int(64, evaluation.width, 0)),
  range_length = evaluation.width,
  range_wrap = unsigned(evaluation.effective_address) + evaluation.width > 18446744073709551616,
  range_end_at_modulus = unsigned(evaluation.effective_address) + evaluation.width
                         == 18446744073709551616,
  effective_address = evaluation.effective_address, linear_address = evaluation.linear_address,
  access = access, value = value, address_translation = true, commit_point = commit_point,
  memory_order = ordinal, address_type = 0, cache_policy = 0,
  suppress_fault = false, staged_updates = evaluation.staged_updates
  , selector = 0x0000000000000000, expected = 0x0000000000000000,
  desired = 0x0000000000000000, auxiliary = 0x0000000000000000, body_length = 0,
  payload_bytes = [||], fp_request = empty_fp_request(),
  state_image = initial_cpu()
}

function waiting_transaction(before : Cpu_state, after : Cpu_state,
                             instruction : Decoded_instruction, kind : Commit_kind,
                             destination : Commit_destination, phase : Continuation_phase,
                             ordinal : int, first : bits(64), second : bits(64),
                             request : Primitive_request) -> Execution_result = struct {
  state = before,
  pending = { empty_pending(before, after, instruction.form.operation, kind) with
    destination = destination, instruction = Some(instruction), phase = phase,
    ordinal = ordinal, captured_first = first, captured_second = second },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

function source_value_for_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> bits(64) = if instruction.form.operation == Op_SET then 0x0000000000000001
  else match value_named(instruction, state, "src") {
  Some(value) => value,
  None() => match value_named(instruction, state, "reg") {
    Some(value) => value,
    None() => 0x0000000000000000,
  },
}

function start_memory_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, state, state.pc, width
  );
  let source = memory_evaluation_for(instruction.operands, evaluated.evaluations, true);
  let destination = memory_evaluation_for(instruction.operands, evaluated.evaluations, false);
  let after = advance_pc(evaluated.image, instruction);
  let commit_target = commit_destination_for(instruction.operands, width);
  match source {
    Some(evaluation) => Some(waiting_transaction(
      state, after, instruction, CommitMemory, commit_target, PhaseSourceRead, 0,
      0x0000000000000000, 0x0000000000000000,
      request_for_evaluation(MemoryRead, 0, evaluation, AccessLoad,
                             0x0000000000000000, false)
    )),
    None() => match destination {
      Some(evaluation) => {
        let raw_value = source_value_for_transaction(instruction, state);
        let signed_extension = instruction.form.operation == Op_EXTSW
                            | instruction.form.operation == Op_EXTSL
                            | instruction.form.operation == Op_EXTSQ;
        let extension = instruction.form.operation == Op_EXTZW
                      | instruction.form.operation == Op_EXTSW
                      | instruction.form.operation == Op_EXTZL
                      | instruction.form.operation == Op_EXTSL
                      | instruction.form.operation == Op_EXTZQ
                      | instruction.form.operation == Op_EXTSQ;
        let value = if extension then
          if signed_extension then sign_extend_width(raw_value, width)
          else narrow_bits(raw_value, width)
        else raw_value;
        Some(waiting_transaction(
          state, after, instruction, CommitMemory, commit_target, PhaseDestinationWrite, 0,
          value, 0x0000000000000000,
          request_for_evaluation(
            if instruction.form.operation == Op_MOVNT then NonTemporalStore else MemoryStore,
            0, evaluation, AccessStore, value, true
          )
        ))
      },
      None() => None(),
    },
  }
}

function atomic_selector(operation : Semantic_operation) -> bits(64) =
  if operation == Op_CMPXCHG then 0x0000000000000000
  else if operation == Op_FETCHADD then 0x0000000000000001
  else if operation == Op_FETCHAND then 0x0000000000000002
  else if operation == Op_FETCHOR then 0x0000000000000003
  else if operation == Op_FETCHSUB then 0x0000000000000004
  else 0x0000000000000005

function start_atomic_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, state, state.pc, width
  );
  match evaluation_named("memory", evaluated.evaluations) {
    None() => None(),
    Some(memory) => {
      let operation = instruction.form.operation;
      let order : int = match value_named(instruction, state, "order") {
        Some(value) => unsigned(value[2 .. 0]), None() => 0
      };
      let expected : bits(64) = match value_named(instruction, state, "expected") {
        Some(value) => narrow_bits(value, width), None() => 0x0000000000000000
      };
      let source : bits(64) = match value_named(instruction, state, "src") {
        Some(value) => narrow_bits(value, width), None() => 0x0000000000000000
      };
      let desired : bits(64) = match value_named(instruction, state, "desired") {
        Some(value) => narrow_bits(value, width), None() => 0x0000000000000000
      };
      let destination = if operation == Op_CMPXCHG
        then commit_destination_for([|match operand_named(instruction, "expected") {
          Some(operand) => operand,
          None() => return None(),
        }|], width)
        else commit_destination_for([|match operand_named(instruction, "src") {
          Some(operand) => operand,
          None() => return None(),
        }|], width);
      let request = { request_for_evaluation(
        AtomicReadModifyWrite, 0, memory, AccessReadModifyWrite, source, true
      ) with memory_order = order, selector = atomic_selector(operation), expected = expected,
             desired = desired, state_image = state };
      Some(waiting_transaction(
        state, advance_pc(evaluated.image, instruction), instruction, CommitMemory,
        destination, PhaseAtomicRmw, 0, expected, source, request
      ))
    },
  }
}

