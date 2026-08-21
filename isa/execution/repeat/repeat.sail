function byte_list_length(bytes : list(bits(8))) -> int = match bytes {
  [||] => 0,
  _ :: tail => 1 + byte_list_length(tail),
}

function drop_bytes(bytes : list(bits(8)), count : int) -> list(bits(8)) =
  if count <= 0 then bytes
  else match bytes {
    [||] => [||],
    _ :: tail => drop_bytes(tail, count - 1),
  }

function take_bytes(bytes : list(bits(8)), count : int) -> list(bits(8)) =
  if count <= 0 then [||]
  else match bytes {
    [||] => [||],
    byte :: tail => byte :: take_bytes(tail, count - 1),
  }

function framed_prefix_length(bytes : list(bits(8))) -> int =
  match byte_at(bytes, 0) {
    None() => -1,
    Some(byte0) => if byte0[7] == bitzero then 1
      else if byte0[7 .. 6] == 0b10 then 2
      else 3 + unsigned(byte0[5 .. 2]),
  }

function decode_next_record(bytes : list(bits(8))) -> option(Decoded_instruction) = {
  let length = framed_prefix_length(bytes);
  if length <= 0 | byte_list_length(bytes) < length then None()
  else decode_full_record(take_bytes(bytes, length))
}

function repeat_body_available(instruction : Decoded_instruction, state : Cpu_state) -> bool =
  if instruction.form.instruction_set == FpuSet then state.fp_enabled
  else if instruction.form.instruction_set == FpuTranscendentalSet
    then state.fp_enabled & state.fptrans_enabled
  else true

function repeat_body_control_forbidden(instruction : Decoded_instruction) -> bool =
  instruction.form.operation == Op_CALL | instruction.form.operation == Op_CALLcc
  | instruction.form.operation == Op_RET | instruction.form.operation == Op_LCALL
  | instruction.form.operation == Op_LRET | instruction.form.operation == Op_LJMP
  | instruction.form.operation == Op_JMP | instruction.form.operation == Op_Jcc
  | instruction.form.operation == Op_DJcc | instruction.form.operation == Op_IJcc
  | instruction.form.operation == Op_CMPJcc | instruction.form.operation == Op_TESTJcc
  | instruction.form.operation == Op_REPcc | instruction.form.operation == Op_REPG
  | instruction.form.operation == Op_BKPT | instruction.form.operation == Op_ERET
  | instruction.form.operation == Op_SYSCALL | instruction.form.operation == Op_SYSRET
  | instruction.form.operation == Op_RESET | instruction.form.operation == Op_HALT

function valid_repg_body(bytes : list(bits(8)), remaining : int, state : Cpu_state) -> bool =
  if remaining == 0 then true
  else if remaining < 0 | byte_list_length(bytes) < remaining then false
  else match decode_next_record(bytes) {
    None() => false,
    Some(body) => body.encoded_length <= remaining
      & body.form.repeat_repg
      & repeat_body_available(body, state)
      & not_bool(repeat_body_control_forbidden(body))
      & valid_repg_body(drop_bytes(bytes, body.encoded_length),
                        remaining - body.encoded_length, state),
  }

function repg_offset_is_boundary(bytes : list(bits(8)), offset : int) -> bool =
  if offset == 0 then true
  else if offset < 0 then false
  else match decode_next_record(bytes) {
    None() => false,
    Some(body) => if body.encoded_length > offset then false
      else repg_offset_is_boundary(drop_bytes(bytes, body.encoded_length),
                                   offset - body.encoded_length),
  }

function repeat_fetch_request(prefix : Decoded_instruction, state : Cpu_state,
                              body_start : bits(64), body_length : int) -> Primitive_request =
  { empty_primitive_request() with
    kind = RepeatBodyFetch, role = if prefix.form.operation == Op_REPG then "group" else "single",
    domain = "CS", segment = 0, segment_image = state.segments[0],
    effective_address = body_start, linear_address = segment_point(
      state.segments[0], body_start
    ).linear,
    range_start = body_start,
    range_end = if body_length == 0 then body_start else add_bits(body_start, bits_from_int(body_length)),
    range_length = body_length, access = AccessExecute, address_translation = true,
    range_wrap = body_length > 0
      & unsigned(add_bits(body_start, bits_from_int(body_length))) < unsigned(body_start),
    range_end_at_modulus = body_length > 0
      & add_bits(body_start, bits_from_int(body_length)) == 0x0000000000000000,
    body_length = body_length, state_image = state }

function start_repeat_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = match operand_named(instruction, "counter") {
  None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing repeat counter"),
  Some(counter) => {
    let index = counter.value[3 .. 0];
    let body_start = next_pc(state, instruction);
    let body_length : int = if instruction.form.operation == Op_REPG then
      match value_named(instruction, state, "body_bytes") {
        Some(value) => unsigned(value[15 .. 0]), None() => 0
      }
      else 0;
    let condition : int = match condition_field(instruction.fields) {
      Some(value) => value, None() => 0
    };
    var staged = state;
    staged.repeat_state = struct {
      active = true, grouped = instruction.form.operation == Op_REPG,
      counter = index, remaining = image_register(state, unsigned(index)),
      condition = get_slice_int(4, condition, 0),
      body_bytes = get_slice_int(16, body_length, 0), body_start = body_start,
      fixed_body = [||], group_progress = 0
    };
    let request = repeat_fetch_request(instruction, staged, body_start, body_length);
    if instruction.form.operation == Op_REPG & body_length == 0 then
      faulted(state, Op_REPG, IllegalInstruction, "REPG body length is zero")
    else waiting_transaction(
      state, staged, instruction, CommitControl, empty_destination(), PhaseRepeatFetch,
      0, image_register(state, unsigned(index)), 0x0000000000000000, request
    )
  },
}

val run_repeat_single : (Decoded_instruction, list(bits(8)), Cpu_state)
  -> Execution_result
val finish_repeat_single : (Decoded_instruction, list(bits(8)),
                            Cpu_state, Cpu_state, bits(64)) -> Execution_result
val run_repeat_group_tail : (list(bits(8)), list(bits(8)), int,
                             Cpu_state) -> Execution_result

function attach_repeat_parent(result : Execution_result, body : Decoded_instruction,
                              all_bytes : list(bits(8)), tail : list(bits(8)),
                              tail_length : int, grouped : bool) -> Execution_result =
  { result with pending = { result.pending with
      repeat_body = Some(body), repeat_bytes = all_bytes,
      repeat_tail = tail, repeat_tail_length = tail_length,
      repeat_parent_active = true, repeat_parent_grouped = grouped,
      boundary_class = if grouped then BoundaryRepeatInterior
                       else BoundaryRepeatIteration } }

function repeat_observation_with_capture(body : Decoded_instruction, before : Cpu_state,
                                         after : Cpu_state, captured : bits(64)) -> bits(4) =
  if body.form.repeat_observed_kind == "computed" then {
    /* Reconstruct the body-derived value inside the same precise commit; this
       is not an architectural FLAGS observation boundary. */
    let operation = body.form.operation;
    if operation == Op_CMP | operation == Op_TEST then after.flags[3 .. 2] @ 0b00
    else if operation == Op_BTEST | operation == Op_BSET
          | operation == Op_BCLR | operation == Op_BCHG then after.flags
    else if operation == Op_BNDSII | operation == Op_BNDSIX
          | operation == Op_BNDSXI | operation == Op_BNDSXX
          | operation == Op_BNDUII | operation == Op_BNDUIX
          | operation == Op_BNDUXI | operation == Op_BNDUXX
          | operation == Op_SEGLEA then
      flags_value(after.flags[0] == bitzero, false, false, false)
    else flags_value(false, false, false, false)
  }
  else match operand_named(body, body.form.repeat_observed_operand) {
    None() => after.flags,
    Some(operand) => {
      let local = if body.form.repeat_observed_kind == "source"
        then local_operand_value(before, operand) else local_operand_value(after, operand);
      let value : bits(64) = match local { Some(item) => item, None() => captured };
      let width = operation_width(body);
      flags_value(narrow_bits(value, width) == 0x0000000000000000,
                  width_sign(value, width), false, false)
    },
  }

function finish_repeat_single(body : Decoded_instruction, bytes : list(bits(8)),
                              before : Cpu_state,
                              after : Cpu_state, captured : bits(64)) -> Execution_result = {
  let context = before.repeat_state;
  let remaining = sub_bits(context.remaining, 0x0000000000000001);
  let observed = repeat_observation_with_capture(body, before, after, captured);
  let continue = remaining != 0x0000000000000000
               & condition_holds(unsigned(context.condition), observed);
  var updated = after;
  updated.registers[unsigned(context.counter)] = remaining;
  updated.repeat_state = { context with remaining = remaining, fixed_body = bytes };
  if continue then {
    updated.pc = context.body_start;
    let done = completed(before, updated, CommitControl, [||]);
    { done with pending = { done.pending with boundary_class = BoundaryRepeatIteration } }
  }
  else {
    updated.repeat_state = { updated.repeat_state with active = false };
    updated.pc = add_bits(context.body_start, bits_from_int(body.encoded_length));
    let done = completed(before, updated, CommitControl, [||]);
    { done with pending = { done.pending with boundary_class = BoundaryRepeatIteration } }
  }
}

function run_repeat_single(body : Decoded_instruction, bytes : list(bits(8)),
                           state : Cpu_state) -> Execution_result = {
  var iteration_state = state;
  iteration_state.pc = state.repeat_state.body_start;
  let result = execute_full(body, iteration_state);
  if result.awaiting_environment then attach_repeat_parent(
    result, body, bytes, [||], 0, false
  )
  else if result.fault != None() then result
  else finish_repeat_single(body, bytes, iteration_state, result.state,
                            result.pending.captured_first)
}

function finish_repeat_group(bytes : list(bits(8)), before : Cpu_state,
                             state : Cpu_state) -> Execution_result = {
  let context = state.repeat_state;
  let current = state.registers[unsigned(context.counter)];
  let remaining = if current == 0x0000000000000000 then current
                  else sub_bits(current, 0x0000000000000001);
  var updated = state;
  updated.registers[unsigned(context.counter)] = remaining;
  updated.repeat_state = { context with remaining = remaining, fixed_body = bytes,
                                        group_progress = 0 };
  if remaining != 0x0000000000000000 then {
    updated.pc = context.body_start;
    let done = completed(before, updated, CommitControl, [||]);
    { done with pending = { done.pending with boundary_class = BoundaryRepeatGroup } }
  }
  else {
    updated.repeat_state = { updated.repeat_state with active = false };
    updated.pc = add_bits(context.body_start, bits_from_int(unsigned(context.body_bytes)));
    let done = completed(before, updated, CommitControl, [||]);
    { done with pending = { done.pending with boundary_class = BoundaryRepeatGroup } }
  }
}

function finish_repeat_group_step(bytes : list(bits(8)), next_remaining : int,
                                  before : Cpu_state,
                                  result : Execution_result) -> Execution_result = {
  var updated = result.state;
  updated.repeat_state = { updated.repeat_state with
    fixed_body = bytes,
    group_progress = unsigned(updated.repeat_state.body_bytes) - next_remaining };
  if next_remaining == 0 then finish_repeat_group(bytes, before, updated)
  else {
    updated.pc = add_bits(
      updated.repeat_state.body_start, bits_from_int(updated.repeat_state.group_progress)
    );
    let done = completed(before, updated, result.pending.kind, result.effects);
    { done with pending = { done.pending with boundary_class = BoundaryRepeatInterior } }
  }
}

function run_repeat_group_tail(all_bytes : list(bits(8)),
                               tail : list(bits(8)), remaining : int,
                               state : Cpu_state) -> Execution_result =
  if remaining == 0 then finish_repeat_group(all_bytes, state, state)
  else match decode_next_record(tail) {
    None() => faulted(state, Op_REPG, IllegalInstruction, "malformed cached REPG body"),
    Some(body) => {
      var instruction_state = state;
      instruction_state.repeat_state = { state.repeat_state with
        group_progress = unsigned(state.repeat_state.body_bytes) - remaining };
      instruction_state.pc = add_bits(
        state.repeat_state.body_start,
        bits_from_int(unsigned(state.repeat_state.body_bytes) - remaining)
      );
      let result = execute_full(body, instruction_state);
      let next_tail = drop_bytes(tail, body.encoded_length);
      let next_remaining = remaining - body.encoded_length;
      if result.awaiting_environment then attach_repeat_parent(
        result, body, all_bytes, next_tail, next_remaining, true
      )
      else if result.fault != None() then result
      else finish_repeat_group_step(all_bytes, next_remaining, instruction_state, result)
    },
  }
