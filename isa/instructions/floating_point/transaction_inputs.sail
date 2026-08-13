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

