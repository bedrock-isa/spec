function segment_image_valid(image : bits(64)) -> bool = {
  let mantissa = unsigned(image[6 .. 1]);
  if mantissa == 0 then true
  else {
    let exponent = unsigned(image[11 .. 7]);
    let base = unsigned(image & 0xFFFFFFFFFFFFF000);
    let span_bits : bits(128) = sail_shiftleft(sail_zero_extend(image[6 .. 1], 128),
                                               exponent + 12);
    base + unsigned(span_bits) <= width_modulus(8)
  }
}

function sreg_index(operand : Decoded_operand) -> range(0, 8) =
  if operand.operand_type == OperandType_CS then 0 else unsigned(operand.value[2 .. 0]) + 1

function control_index(selector : int) -> option(bits(5)) =
  if selector == 0 then Some(0b00000)
  else if selector == 1 then Some(0b00001)
  else if selector == 2 then Some(0b00010)
  else if selector == 264 then Some(0b00110)
  else if selector == 265 then Some(0b00111)
  else if selector == 266 then Some(0b01000)
  else if selector == 267 then Some(0b01001)
  else if selector == 268 then Some(0b01010)
  else if selector == 269 then Some(0b01011)
  else if selector == 270 then Some(0b11010)
  else if selector == 272 then Some(0b01100)
  else if selector == 273 then Some(0b01101)
  else if selector == 274 then Some(0b01110)
  else if selector == 512 then Some(0b01111)
  else if selector == 513 then Some(0b10000)
  else if selector == 528 then Some(0b10001)
  else if selector == 529 then Some(0b10010)
  else if selector == 544 then Some(0b10011)
  else if selector == 545 then Some(0b10100)
  else if selector == 560 then Some(0b10101)
  else if selector == 561 then Some(0b10110)
  else if selector == 4096 then Some(0b10111)
  else if selector == 4097 then Some(0b11000)
  else if selector == 4352 then Some(0b11001)
  else None()

function write_control_locally(selector : int) -> bool = selector != 2 & selector != 272

function control_segment_requires_valid_image(selector : int) -> bool =
  selector == 273 | selector == 274 | selector == 512 | selector == 528
  | selector == 544 | selector == 560

function control_pointer_requires_alignment(selector : int) -> bool =
  selector == 513 | selector == 529 | selector == 545 | selector == 561

val paging_canonical : (bits(64), bits(64)) -> bool

function event_stack_pair_valid(segment_image : bits(64), stack_top : bits(64)) -> bool =
  segment_image_valid(segment_image)
  & (stack_top & 0x000000000000003F) == 0x0000000000000000
  & segment_point(segment_image, sub_bits(stack_top, 0x0000000000000060)).in_bounds

function event_control_bank_valid(state : Cpu_state) -> bool =
  segment_image_valid(state.controls[13])
  & segment_image_valid(state.controls[14])
  & (state.controls[12] & 0x000000000000000F) == 0x0000000000000000
  & paging_canonical(state.controls[12], state.controls[0])
  & segment_point(state.controls[13], state.controls[12]).in_bounds
  & event_stack_pair_valid(state.controls[15], state.controls[16])
  & event_stack_pair_valid(state.controls[17], state.controls[18])
  & event_stack_pair_valid(state.controls[19], state.controls[20])
  & event_stack_pair_valid(state.controls[21], state.controls[22])

function uinfo_event_code_valid(value : bits(64)) -> bool = {
  let class = unsigned(value[31 .. 24]);
  let id = value[23 .. 0];
  value[63 .. 32] == 0x00000000
  & ((class == 0 & (id == 0x000000 | id == 0x000002 | id == 0x000003
                    | id == 0x000008 | id == 0x000009 | id == 0x00000A
                    | id == 0x00000B | id == 0x00000D | id == 0x00000E
                    | id == 0x000018 | id == 0x000019 | id == 0x00001A
                    | id == 0x000020))
     | class == 1 | class == 2)
}

function user_return_bank_image_valid(state : Cpu_state) -> bool = {
  let uctl = state.controls[11];
  let saved_status = sail_shiftright(uctl, 16) & 0x000000000000FFFF;
  let saved_flags = uctl & 0x000000000000FFFF;
  uctl[32] == bitone
  & (uctl & 0xFFFFFFFE00000000) == 0x0000000000000000
  & (saved_status & 0xFFFFFFFFFFFFF800) == 0x0000000000000000
  & (saved_status & 0x00000000000007D1) == 0x0000000000000000
  & (saved_flags & 0xFFFFFFFFFFFFFFF0) == 0x0000000000000000
  & uinfo_event_code_valid(state.controls[26])
  & segment_image_valid(state.controls[8])
  & segment_image_valid(state.controls[9])
  & segment_image_valid(state.controls[10])
  & segment_point(state.controls[10], state.controls[7]).in_bounds
  & paging_canonical(state.controls[6], state.controls[0])
  & segment_point(state.controls[8], state.controls[6]).in_bounds
}

function state_with_control_write(state : Cpu_state, selector : int,
                                  value : bits(64)) -> Cpu_state = {
  var candidate = state;
  match control_index(selector) {
    Some(index) => candidate.controls[unsigned(index)] = value,
    None() => (),
  };
  candidate
}

function target_probe_request(ordinal : int, segment_image : bits(64), target : bits(64))
  -> Primitive_request = {
  let point = segment_point(segment_image, target);
  struct {
    kind = TranslationExecuteProbe, ordinal = ordinal, role = RequestRoleControlTarget, domain = RequestDomainCode,
    segment = 0, segment_image = segment_image, width = 1, range_start = target,
    range_end = add_bits(target, 0x0000000000000001), effective_address = target,
    range_length = 1, range_wrap = false,
    range_end_at_modulus = target == 0xFFFFFFFFFFFFFFFF,
    linear_address = point.linear, access = AccessExecute, value = 0x0000000000000000,
    address_translation = true, commit_point = false, memory_order = ordinal,
    cache_policy = 0, suppress_fault = false, staged_updates = [||],
    selector = 0x0000000000000000, expected = 0x0000000000000000,
    desired = 0x0000000000000000, auxiliary = 0x0000000000000000, body_length = 0,
    payload_bytes = [||]
  }
}

function read_state_register(instruction : Decoded_instruction, state : Cpu_state,
                             value : bits(64)) -> Execution_result =
  match destination_named(instruction, Operand_dst, 8) {
    Some(destination) => {
      let updated = write_local_destination(
        state, instruction.form.operation, destination, value
      );
      local_result(state, instruction, updated, CommitRegisters)
    },
    None() => faulted(state, instruction.form.operation, IllegalInstruction,
                      "missing state-register destination"),
  }
