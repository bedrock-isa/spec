function continue_with_request(previous : Execution_result, phase : Continuation_phase,
                               ordinal : int, first : bits(64), second : bits(64),
                               request : Primitive_request) -> Execution_result = struct {
  state = previous.state,
  pending = { previous.pending with phase = phase, ordinal = ordinal,
              captured_first = first, captured_second = second },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

struct Resolved_execution = {
  state : Cpu_state,
  destination_value : bits(64),
}

function register_operand_uses(index : int, operand : Decoded_operand,
                               except_name : string) -> bool =
  operand.name != except_name & operand.type_name == "Rn"
  & unsigned(operand.value[3 .. 0]) == index

function register_is_used(index : int, operands : list(Decoded_operand),
                          except_name : string) -> bool = match operands {
  [||] => false,
  operand :: tail => register_operand_uses(index, operand, except_name)
                     | register_is_used(index, tail, except_name),
}

function available_scratch(operands : list(Decoded_operand), except_name : string,
                           candidate : int) -> int =
  if candidate < 0 then 15
  else if register_is_used(candidate, operands, except_name)
       then available_scratch(operands, except_name, candidate - 1)
       else candidate

function option_operand_writes(value : option(Decoded_operand)) -> bool = match value {
  Some(operand) => operand.access == AccessWrite | operand.access == AccessReadWrite,
  None() => false,
}

function operand_access_named(name : string, operands : list(Decoded_operand)) -> Metadata_access =
  match operands {
    [||] => AccessRead,
    operand :: tail => if operand.name == name then operand.access
                       else operand_access_named(name, tail),
  }

function resolved_operand(operand : Decoded_operand, first_name : string, first_value : bits(64),
                          second_name : string, second_value : bits(64), scratch : int)
  -> Decoded_operand =
  if operand.name != first_name & operand.name != second_name then operand
  else {
    let value = if operand.name == first_name then first_value else second_value;
    if operand.access == AccessWrite | operand.access == AccessReadWrite then
      { operand with type_name = "Rn", value = get_slice_int(64, scratch, 0),
                     fixed_identity = "", ea = None() }
    else { operand with type_name = "imm64", value = value,
                        fixed_identity = "", ea = None() }
  }

function resolved_operand_list(operands : list(Decoded_operand),
                               first_name : string, first_value : bits(64),
                               second_name : string, second_value : bits(64), scratch : int)
  -> list(Decoded_operand) = match operands {
  [||] => [||],
  operand :: tail => resolved_operand(
    operand, first_name, first_value, second_name, second_value, scratch
  ) :: resolved_operand_list(tail, first_name, first_value, second_name, second_value, scratch),
}

function execute_resolved_operands(instruction : Decoded_instruction, image : Cpu_state,
                                   first_name : string, first_value : bits(64),
                                   second_name : string, second_value : bits(64))
  -> option(Resolved_execution) = {
  let destination_name = if second_name != "" then second_name else first_name;
  let scratch = available_scratch(instruction.operands, destination_name, 15);
  let destination_operand = find_operand_by_name(destination_name, instruction.operands);
  let destination_is_memory_write = option_operand_writes(destination_operand);
  var execution_image = image;
  let saved_scratch = image_register(image, scratch);
  if destination_is_memory_write then {
    let initial_value = if destination_name == first_name then first_value else second_value;
    execution_image.registers[unsigned(get_slice_int(4, scratch, 0))] = initial_value
  } else ();
  let synthetic = { instruction with operands = resolved_operand_list(
    instruction.operands, first_name, first_value, second_name, second_value, scratch
  ) };
  let result = execute_route_exact(synthetic, execution_image);
  if result.awaiting_environment | result.fault != None() then None()
  else {
    let destination_value = image_register(result.state, scratch);
    var final_state = result.state;
    if destination_is_memory_write then
      final_state.registers[unsigned(get_slice_int(4, scratch, 0))] = saved_scratch
    else ();
    Some(struct { state = final_state, destination_value = destination_value })
  }
}

function commit_response_destination(previous : Execution_result, value : bits(64),
                                     response : Transaction_response) -> Execution_result = {
  let fp_route = semantic_route(previous.pending.operation) == RouteFpu
               | semantic_route(previous.pending.operation) == RouteFpuTranscendental;
  let destination = previous.pending.destination;
  let initial_operand : Fp_operand_image = struct {
    valid = destination.kind == "Fn",
    kind = if destination.width == 4 then FpBits32 else FpBits64,
    bits = value
  };
  let post = if fp_route & destination.kind == "Fn" then fp_postprocess(
    initial_operand, previous.pending.before.fstatus,
    semantic_route(previous.pending.operation) == RouteFpuTranscendental,
    response.generated_fflags
  ) else struct { value = initial_operand, generated_causes = response.generated_fflags };
  let generated = post.generated_causes;
  if fp_route & not_bool(fp_operation_causes_valid(previous.pending.operation, generated)) then
    faulted(previous.pending.before, previous.pending.operation, InvalidControlState,
            "floating-point response reported an impossible cause")
  else if fp_route & fp_traps(previous.pending.before.fstatus, generated) then {
    let base = faulted(previous.pending.before, previous.pending.operation,
                       FloatingPointFault, "enabled floating-point exception");
    { base with fault = Some(struct {
        kind = FloatingPointFault, operation = previous.pending.operation,
        detail = "enabled floating-point exception",
        error_code = sail_zero_extend(generated, 64), bus_error = false
      }) }
  }
  else {
  var updated = previous.pending.after;
  if destination.kind == "Rn" then {
    let index = unsigned(destination.index);
    updated.registers[index] = merge_narrow(updated.registers[index], value, destination.width)
  }
  else if destination.kind == "Fn" then {
    let index = unsigned(destination.index);
    updated.floating_registers[index] = if destination.width == 4
      then 0x00000000 @ post.value.bits[31 .. 0] else post.value.bits
    ; updated.fp_component_modified = true
  }
  else if destination.kind == "SP" then
    updated.sp = merge_narrow(updated.sp, value, destination.width)
  else ();
  if response.write_flags & fp_route then match fp_semantics(previous.pending.operation) {
    Some(semantics) => updated.flags = (updated.flags & not_vec(semantics.flags_mask))
                                     | (response.flags & semantics.flags_mask),
    None() => (),
  }
  else if response.write_flags then updated.flags = response.flags else ();
  updated.fflags = updated.fflags | generated;
  if generated != 0b00000 then updated.fp_component_modified = true else ();
  completed(previous.state, updated, previous.pending.kind, [||])
  }
}

