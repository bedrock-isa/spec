function execute_setcc(instruction : Decoded_instruction, state : Cpu_state) -> Execution_result =
  match find_operand_by_name("dst", instruction.operands) {
    Some(dst) =>
      if dst.type_name == "Rn" then {
        let selected = predicate_holds(instruction, state);
        let value : bits(64) = if selected then 0x0000000000000001 else 0x0000000000000000;
        var updated = advance_pc(state, instruction);
        let index = unsigned(dst.value[3 .. 0]);
        updated.registers[index] = merge_narrow(state.registers[index], value, operation_width(instruction));
        completed(state, updated, CommitRegisters, [||])
      }
      else match start_memory_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction,
                          "missing SETcc memory destination"),
      },
    None() => faulted(state, instruction.form.operation, IllegalInstruction, "SETcc destination"),
  }

function route_environment(instruction : Decoded_instruction, state : Cpu_state,
                           effect_kind : Effect_kind, commit_kind : Commit_kind,
                           suppress_fault : bool) -> Execution_result = {
  let address : bits(64) = match first_ea_operand(instruction.operands) {
    Some(operand) => operand.value,
    None() => 0x0000000000000000,
  };
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  let kind = if operation == Op_RFENCE | operation == Op_WFENCE | operation == Op_AFENCE
    then FenceCompletion
    else if instruction.form.route == RouteAtomics then AtomicReadModifyWrite
    else if instruction.form.route == RouteCache then
      if operation == Op_PREFETCH | operation == Op_PREFETCHNT then PrefetchHint
      else CacheMaintenanceBlock
    else if instruction.form.route == RouteTlbContext then
      if operation == Op_INVASID | operation == Op_INVPAGE | operation == Op_INVTLB
        then TlbInvalidateRequest
      else if operation == Op_PTQUERY | operation == Op_VTOP then TranslationQueryRequest
      else if operation == Op_SAVE then StateSaveRequest
      else if operation == Op_RESTORE then StateRestoreRequest
      else ContextSwitchRequest
    else if operation == Op_REPcc | operation == Op_REPG then RepeatBodyFetch
    else if operation == Op_CPUID then CpuidQueryRequest
    else if operation == Op_RDPMC then PerformanceCounterRequest
    else if operation == Op_WRCR then ControlTransitionRequest
    else if operation == Op_RESET then ResetSerializeRequest
    else ExternalIntegerRequest;
  let phase = if kind == AtomicReadModifyWrite then PhaseAtomicRmw
    else if kind == CacheMaintenanceBlock | kind == PrefetchHint then PhaseCacheMaintenance
    else if kind == FenceCompletion then PhaseFenceCompletion
    else if kind == TlbInvalidateRequest then PhaseTlbOperation
    else if kind == TranslationQueryRequest then PhaseTranslationQuery
    else if kind == ContextSwitchRequest then PhaseContextSwitch
    else if kind == StateSaveRequest then PhaseStateSave
    else if kind == StateRestoreRequest then PhaseStateRestore
    else if kind == RepeatBodyFetch then PhaseRepeatFetch
    else if kind == CpuidQueryRequest then PhaseCpuidQuery
    else if kind == PerformanceCounterRequest then PhasePerformanceCounter
    else if kind == ControlTransitionRequest then PhaseControlTransition
    else if kind == ResetSerializeRequest then PhaseResetSerialize
    else PhaseIntegerExternal;
  struct {
    state = state,
    pending = { empty_pending(state, advance_pc(state, instruction),
                              instruction.form.operation, commit_kind) with
      destination = commit_destination_for(instruction.operands, width),
      instruction = Some(instruction), phase = phase },
    request = { empty_primitive_request() with
      kind = kind, role = instruction.form.family, width = width,
      access = NoTransactionAccess, commit_point = true, suppress_fault = suppress_fault,
      selector = if operation == Op_RESET then 0x000000000000003F
                 else 0x0000000000000000,
      expected = if operation == Op_RESET then state.controls[23]
                 else 0x0000000000000000,
      state_image = state },
    effects = [|typed_effect(effect_kind, instruction, state, address, 0x0000000000000000,
                            width, 0, suppress_fault)|],
    fault = None(),
    awaiting_environment = true
  }
}

val resume_transaction : (Execution_result, Transaction_response) -> Execution_result
val execute_full : (Decoded_instruction, Cpu_state) -> Execution_result

function sign_extend_width(value : bits(64), width : int) -> bits(64) =
  if width == 1 then sail_sign_extend(value[7 .. 0], 64)
  else if width == 2 then sail_sign_extend(value[15 .. 0], 64)
  else if width == 4 then sail_sign_extend(value[31 .. 0], 64)
  else value

function signed_width(value : bits(64), width : int) -> int =
  signed(sign_extend_width(value, width))

function width_modulus(width : int) -> int = unsigned(width_mask(width)) + 1
function width_bits(width : int) -> int = width * 8

function narrow_bits(value : bits(64), width : int) -> bits(64) = value & width_mask(width)

function bits_from_int(value : int) -> bits(64) = get_slice_int(64, value, 0)

function immediate_value(operand : Decoded_operand) -> bits(64) =
  if operand.type_name == "imm8s" then sail_sign_extend(operand.value[7 .. 0], 64)
  else if operand.type_name == "imm16s" then sail_sign_extend(operand.value[15 .. 0], 64)
  else if operand.type_name == "imm32s" then sail_sign_extend(operand.value[31 .. 0], 64)
  else operand.value

function ea_field_value(ea : Decoded_ea, symbol : string) -> option(int) =
  match find_decoded_field(symbol, ea.fields) {
    Some(field) => Some(field.value),
    None() => None(),
  }

function local_ea_value(state : Cpu_state, ea : Decoded_ea) -> option(bits(64)) =
  if ea.kind == "register" then
    if ea.register_name == "SP" then Some(state.sp)
    else match ea_field_value(ea, "r") {
      Some(index) => Some(state.registers[unsigned(get_slice_int(4, index, 0))]),
      None() => None(),
    }
  else if ea.kind == "immediate" then
    if ea.payload_signed then Some(sign_extend_width(ea.payload, tdiv_int(ea.payload_width, 8)))
    else Some(ea.payload)
  else None()

function local_operand_value(state : Cpu_state, operand : Decoded_operand) -> option(bits(64)) =
  if operand.type_name == "Rn" then Some(state.registers[unsigned(operand.value[3 .. 0])])
  else if operand.type_name == "SP" then Some(state.sp)
  else if operand.type_name == "CS" then Some(state.segments[0])
  else if operand.type_name == "SREG" then
    Some(state.segments[unsigned(operand.value[2 .. 0]) + 1])
  else if operand.type_name == "EA" then match operand.ea {
    Some(ea) => local_ea_value(state, ea),
    None() => None(),
  }
  else Some(immediate_value(operand))

function local_destination(operand : Decoded_operand, width : int) -> option(Commit_destination) =
  if operand.type_name == "Rn" then Some(struct {
    kind = "Rn", index = operand.value[3 .. 0], width = width
  })
  else if operand.type_name == "SP" then Some(struct {
    kind = "SP", index = 0x0, width = width
  })
  else if operand.type_name == "EA" then match operand.ea {
    Some(ea) => if ea.kind == "register" then
      if ea.register_name == "SP" then Some(struct {
        kind = "SP", index = 0x0, width = width
      })
      else match ea_field_value(ea, "r") {
        Some(index) => Some(struct {
          kind = "Rn", index = get_slice_int(4, index, 0), width = width
        }),
        None() => None(),
      }
    else None(),
    None() => None(),
  }
  else None()

function write_local_destination(state : Cpu_state, destination : Commit_destination,
                                 value : bits(64)) -> Cpu_state = {
  var updated = state;
  if destination.kind == "Rn" then {
    let index = unsigned(destination.index);
    updated.registers[index] = merge_narrow(
      state.registers[index], value, destination.width
    )
  }
  else if destination.kind == "SP" then
    updated.sp = merge_narrow(state.sp, value, destination.width)
  else ();
  updated
}

function operand_named(instruction : Decoded_instruction, name : string) -> option(Decoded_operand) =
  find_operand_by_name(name, instruction.operands)

function value_named(instruction : Decoded_instruction, state : Cpu_state,
                     name : string) -> option(bits(64)) =
  match operand_named(instruction, name) {
    Some(operand) => local_operand_value(state, operand),
    None() => None(),
  }

function destination_named(instruction : Decoded_instruction, name : string,
                           width : int) -> option(Commit_destination) =
  match operand_named(instruction, name) {
    Some(operand) => local_destination(operand, width),
    None() => None(),
  }

function add_with_flags(lhs : bits(64), rhs : bits(64), carry_in : int,
                        width : int) -> (bits(64), bits(4)) = {
  let modulus = width_modulus(width);
  let left = unsigned(narrow_bits(lhs, width));
  let right = unsigned(narrow_bits(rhs, width));
  let complete = left + right + carry_in;
  let result = bits_from_int(tmod_int(complete, modulus)) & width_mask(width);
  let signed_complete = signed_width(lhs, width) + signed_width(rhs, width) + carry_in;
  let signed_limit = tdiv_int(modulus, 2);
  let overflow = signed_complete < -signed_limit | signed_complete >= signed_limit;
  (result, flags_value(result == 0x0000000000000000, width_sign(result, width),
                       complete >= modulus, overflow))
}

function sub_with_flags(lhs : bits(64), rhs : bits(64), borrow_in : int,
                        width : int) -> (bits(64), bits(4)) = {
  let modulus = width_modulus(width);
  let left = unsigned(narrow_bits(lhs, width));
  let right = unsigned(narrow_bits(rhs, width));
  let complete = left - right - borrow_in;
  let normalized = tmod_int(tmod_int(complete, modulus) + modulus, modulus);
  let result = bits_from_int(normalized) & width_mask(width);
  let signed_complete = signed_width(lhs, width) - signed_width(rhs, width) - borrow_in;
  let signed_limit = tdiv_int(modulus, 2);
  let overflow = signed_complete < -signed_limit | signed_complete >= signed_limit;
  (result, flags_value(result == 0x0000000000000000, width_sign(result, width),
                       left < right + borrow_in, overflow))
}

function set_flag_z_only(flags : bits(4), value : bool) -> bits(4) =
  (if value then bitone else bitzero) @ flags[2 .. 0]

function set_flag_v_only(flags : bits(4), value : bool) -> bits(4) =
  flags[3 .. 1] @ (if value then bitone else bitzero)

function bit_count_from(value : bits(64), index : int, limit : int) -> int =
  if index >= limit then 0
  else (if sail_shiftright(value, index)[0] == bitone then 1 else 0)
       + bit_count_from(value, index + 1, limit)

function count_from_low(value : bits(64), index : int, limit : int, bit_value : bit) -> int =
  if index >= limit then limit
  else if sail_shiftright(value, index)[0] == bit_value
       then count_from_low(value, index + 1, limit, bit_value)
  else index

function count_from_high(value : bits(64), remaining : int, bit_value : bit) -> int =
  if remaining <= 0 then 0
  else if sail_shiftright(value, remaining - 1)[0] == bit_value then
    1 + count_from_high(value, remaining - 1, bit_value)
  else 0

function reverse_bytes_int(value : int, remaining : int, accumulated : int) -> int =
  if remaining <= 0 then accumulated
  else reverse_bytes_int(tdiv_int(value, 256), remaining - 1,
                         accumulated * 256 + tmod_int(value, 256))

function reverse_bytes(value : bits(64), width : int) -> bits(64) =
  bits_from_int(reverse_bytes_int(unsigned(narrow_bits(value, width)), width, 0))

function carryless_loop(lhs : bits(128), rhs : bits(64), index : int,
                        accumulated : bits(128)) -> bits(128) =
  if index >= 64 then accumulated
  else carryless_loop(lhs, rhs, index + 1,
    if sail_shiftright(rhs, index)[0] == bitone
    then xor_vec(accumulated, sail_shiftleft(lhs, index)) else accumulated)

function carryless_product(value : bits(64), source : bits(64)) -> bits(128) =
  carryless_loop(sail_zero_extend(value, 128), source, 0,
    0x00000000000000000000000000000000)

function carryless_high(product : bits(128), width : int) -> bits(64) =
  if width == 1 then sail_zero_extend(product[15 .. 8], 64)
  else if width == 2 then sail_zero_extend(product[31 .. 16], 64)
  else if width == 4 then sail_zero_extend(product[63 .. 32], 64)
  else product[127 .. 64]

function signed_minimum(width : int) -> int = -tdiv_int(width_modulus(width), 2)

function local_result(state : Cpu_state, instruction : Decoded_instruction,
                      updated : Cpu_state, kind : Commit_kind) -> Execution_result =
  completed(state, { updated with pc = next_pc(state, instruction) }, kind, [||])

function first_binary_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail =>
      if operand.name == "cc" then first_binary_operand(tail)
      else if operand.name == "src" | operand.name == "lhs" then Some(operand)
      else first_binary_operand(tail),
  }

function second_binary_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail =>
      if operand.name == "dst" | operand.name == "rhs" then Some(operand)
      else second_binary_operand(tail),
  }

function execute_binary_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  if not_bool(operation == Op_CMP | operation == Op_TEST | operation == Op_ADC
              | operation == Op_SBB | operation == Op_ADD | operation == Op_SUB
              | operation == Op_AND | operation == Op_OR | operation == Op_XOR
              | operation == Op_MOV | operation == Op_MOVCU | operation == Op_MOVUC
              | operation == Op_MOVUU | operation == Op_MOVcc) then None()
  else match (first_binary_operand(instruction.operands), second_binary_operand(instruction.operands)) {
    (Some(source_operand), Some(destination_operand)) =>
      match (local_operand_value(state, source_operand),
             local_operand_value(state, destination_operand)) {
        (Some(source), Some(destination)) => {
          if operation == Op_CMP then {
            let (ignored, flags) = sub_with_flags(destination, source, 0, width);
            let updated = { state with flags = flags };
            Some(local_result(state, instruction, updated, CommitRegisters))
          }
          else if operation == Op_TEST then {
            let value = narrow_bits(destination & source, width);
            let updated = { state with flags = flags_value(
              value == 0x0000000000000000, width_sign(value, width), false, false
            ) };
            Some(local_result(state, instruction, updated, CommitRegisters))
          }
          else match local_destination(destination_operand, width) {
            None() => None(),
            Some(destination_ref) => {
              let (value, flags) = if operation == Op_ADC then
                add_with_flags(destination, source, if flag_c(state.flags) then 1 else 0, width)
              else if operation == Op_SBB then
                sub_with_flags(destination, source, if flag_c(state.flags) then 1 else 0, width)
              else if operation == Op_ADD then
                (bits_from_int(unsigned(narrow_bits(destination, width))
                               + unsigned(narrow_bits(source, width))), state.flags)
              else if operation == Op_SUB then
                (bits_from_int(unsigned(narrow_bits(destination, width))
                               - unsigned(narrow_bits(source, width))), state.flags)
              else if operation == Op_AND then (destination & source, state.flags)
              else if operation == Op_OR then (destination | source, state.flags)
              else if operation == Op_XOR then (xor_vec(destination, source), state.flags)
              else (source, state.flags);
              var updated = write_local_destination(state, destination_ref,
                                                      narrow_bits(value, width));
              updated.flags = flags;
              Some(local_result(state, instruction, updated, CommitRegisters))
            },
          }
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_sp_arithmetic_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (value_named(instruction, state, "imm"), destination_named(instruction, "dst", 8)) {
    (Some(source), Some(destination)) => if destination.kind == "SP" then {
      let value = if instruction.form.operation == Op_ADD
        then add_bits(state.sp, source) else sub_bits(state.sp, source);
      let updated = write_local_destination(state, destination, value);
      Some(local_result(state, instruction, updated, CommitRegisters))
    } else None(),
    _ => None(),
  }

function execute_unary_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  if not_bool(operation == Op_CLR | operation == Op_INC | operation == Op_INCF
              | operation == Op_DEC | operation == Op_DECF | operation == Op_NEG
              | operation == Op_ABS | operation == Op_NOT) then None()
  else match operand_named(instruction, "dst") {
    None() => None(),
    Some(operand) => match (local_operand_value(state, operand), local_destination(operand, width)) {
      (Some(old), Some(destination)) => {
        let value = if operation == Op_CLR then 0x0000000000000000
          else if operation == Op_INC | operation == Op_INCF then add_bits(old, 0x0000000000000001)
          else if operation == Op_DEC | operation == Op_DECF then sub_bits(old, 0x0000000000000001)
          else if operation == Op_NEG then sub_bits(0x0000000000000000, old)
          else if operation == Op_ABS then
            if width_sign(old, width) then sub_bits(0x0000000000000000, old) else old
          else not_vec(old);
        var updated = write_local_destination(state, destination, narrow_bits(value, width));
        if operation == Op_INCF then {
          let (ignored, flags) = add_with_flags(old, 0x0000000000000001, 0, width);
          updated.flags = flags
        }
        else if operation == Op_DECF then {
          let (ignored, flags) = sub_with_flags(old, 0x0000000000000001, 0, width);
          updated.flags = flags
        }
        else ();
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
      _ => None(),
    },
  }
}

function execute_shift_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "count"), operand_named(instruction, "dst")) {
    (Some(count), Some(operand)) =>
      match (local_operand_value(state, operand), local_destination(operand, width)) {
        (Some(old), Some(destination)) => {
          let value = shift_result(instruction.form.operation, old, count, width);
          let updated = write_local_destination(state, destination, value);
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_bit_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "bit_index"), operand_named(instruction, "dst")) {
    (Some(raw_index), Some(operand)) => match local_operand_value(state, operand) {
      None() => None(),
      Some(old) => {
        let index = unsigned(raw_index[5 .. 0]);
        let mask = sail_shiftleft(0x0000000000000001, index);
        let selected_old = narrow_bits(old, width);
        let was_clear = (selected_old & mask) == 0x0000000000000000;
        let operation = instruction.form.operation;
        let new_flags = set_flag_z_only(state.flags, was_clear);
        if operation == Op_BTEST then {
          let updated = { state with flags = new_flags };
          Some(local_result(state, instruction, updated, CommitRegisters))
        }
        else match local_destination(operand, width) {
          None() => None(),
          Some(destination) => {
            let value = if operation == Op_BSET then selected_old | mask
              else if operation == Op_BCLR then selected_old & not_vec(mask)
              else xor_vec(selected_old, mask);
            var updated = write_local_destination(state, destination, value);
            updated.flags = new_flags;
            Some(local_result(state, instruction, updated, CommitRegisters))
          },
        }
      },
    },
    _ => None(),
  }
}

function execute_count_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), operand_named(instruction, "dst")) {
    (Some(source), Some(operand)) => match local_destination(operand, 8) {
      None() => None(),
      Some(destination) => {
        let value = narrow_bits(source, width);
        let bits = width_bits(width);
        let count = if instruction.form.operation == Op_CLZ then
            count_from_high(value, bits, bitzero)
          else if instruction.form.operation == Op_CLS then
            count_from_high(value, bits, bitone)
          else if instruction.form.operation == Op_CTZ then
            count_from_low(value, 0, bits, bitzero)
          else if instruction.form.operation == Op_CTS then
            count_from_low(value, 0, bits, bitone)
          else bit_count_from(value, 0, bits);
        let updated = write_local_destination(state, destination, bits_from_int(count));
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
    },
    _ => None(),
  }
}

function execute_parity_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), destination_named(instruction, "dst", width)) {
    (Some(source), Some(destination)) => {
      let parity = tmod_int(bit_count_from(narrow_bits(source, width), 0, width_bits(width)), 2);
      let updated = write_local_destination(state, destination, bits_from_int(parity));
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function execute_revbyte_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match operand_named(instruction, "dst") {
    Some(operand) => match (local_operand_value(state, operand), local_destination(operand, width)) {
      (Some(old), Some(destination)) => {
        let updated = write_local_destination(state, destination, reverse_bytes(old, width));
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
      _ => None(),
    },
    None() => None(),
  }
}

function product_high(lhs : bits(64), rhs : bits(64), width : int,
                      lhs_signed : bool, rhs_signed : bool) -> bits(64) = {
  let left = if lhs_signed then signed_width(lhs, width) else unsigned(narrow_bits(lhs, width));
  let right = if rhs_signed then signed_width(rhs, width) else unsigned(narrow_bits(rhs, width));
  let product : bits(128) = get_slice_int(128, left * right, 0);
  if width == 1 then sail_zero_extend(product[15 .. 8], 64)
  else if width == 2 then sail_zero_extend(product[31 .. 16], 64)
  else if width == 4 then sail_zero_extend(product[63 .. 32], 64)
  else product[127 .. 64]
}

function execute_math_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  if not_bool(operation == Op_MUL | operation == Op_MULHU | operation == Op_MULHS
              | operation == Op_MULHSU | operation == Op_CLMUL | operation == Op_CLMULH
              | operation == Op_MINU | operation == Op_MAXU | operation == Op_MINS
              | operation == Op_MAXS) then None()
  else match (value_named(instruction, state, "src"), operand_named(instruction, "dst")) {
    (Some(source), Some(operand)) =>
      match (local_operand_value(state, operand), local_destination(operand, width)) {
        (Some(old), Some(destination)) => {
          let value = if operation == Op_MUL then
              bits_from_int(unsigned(narrow_bits(old, width)) * unsigned(narrow_bits(source, width)))
            else if operation == Op_MULHU then product_high(old, source, width, false, false)
            else if operation == Op_MULHS then product_high(old, source, width, true, true)
            else if operation == Op_MULHSU then product_high(old, source, width, true, false)
            else if operation == Op_CLMUL then carryless_product(
              narrow_bits(old, width), narrow_bits(source, width))[63 .. 0]
            else if operation == Op_CLMULH then carryless_high(
              carryless_product(narrow_bits(old, width), narrow_bits(source, width)), width
            )
            else if operation == Op_MINU then
              if unsigned(narrow_bits(old, width)) <= unsigned(narrow_bits(source, width))
              then old else source
            else if operation == Op_MAXU then
              if unsigned(narrow_bits(old, width)) >= unsigned(narrow_bits(source, width))
              then old else source
            else if operation == Op_MINS then
              if signed_width(old, width) <= signed_width(source, width) then old else source
            else if signed_width(old, width) >= signed_width(source, width) then old else source;
          let updated = write_local_destination(state, destination, narrow_bits(value, width));
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_divide_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), operand_named(instruction, "dst")) {
    (Some(source), Some(operand)) =>
      match (local_operand_value(state, operand), local_destination(operand, width)) {
        (Some(dividend), Some(destination)) => {
          let divisor_u = unsigned(narrow_bits(source, width));
          if divisor_u == 0 then Some(faulted(
            state, instruction.form.operation, DivideByZero, "zero divisor"
          ))
          else {
            let signed_operation = instruction.form.operation == Op_DIVS
                                   | instruction.form.operation == Op_MODS;
            let modulo_operation = instruction.form.operation == Op_MODS
                                   | instruction.form.operation == Op_MODU;
            if signed_operation & signed_width(dividend, width) == signed_minimum(width)
               & signed_width(source, width) == -1 then Some(faulted(
              state, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"
            ))
            else {
              let quotient = if signed_operation then
                  tdiv_int(signed_width(dividend, width), signed_width(source, width))
                else tdiv_int(unsigned(narrow_bits(dividend, width)), divisor_u);
              let remainder = if signed_operation then
                  signed_width(dividend, width) - quotient * signed_width(source, width)
                else tmod_int(unsigned(narrow_bits(dividend, width)), divisor_u);
              let value = bits_from_int(if modulo_operation then remainder else quotient);
              let updated = write_local_destination(state, destination, narrow_bits(value, width));
              Some(local_result(state, instruction, updated, CommitRegisters))
            }
          }
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_divmod_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "src"), operand_named(instruction, "quotient"),
         operand_named(instruction, "remainder")) {
    (Some(source), Some(quotient_operand), Some(remainder_operand)) =>
      match (local_operand_value(state, quotient_operand),
             local_destination(quotient_operand, width),
             local_destination(remainder_operand, width)) {
        (Some(dividend), Some(quotient_destination), Some(remainder_destination)) =>
          if quotient_destination.kind == remainder_destination.kind
             & quotient_destination.index == remainder_destination.index then Some(faulted(
            state, instruction.form.operation, IllegalInstruction, "DIVMOD destinations overlap"
          ))
          else if unsigned(narrow_bits(source, width)) == 0 then Some(faulted(
            state, instruction.form.operation, DivideByZero, "zero divisor"
          ))
          else {
            let signed_operation = instruction.form.operation == Op_DIVMODS;
            if signed_operation & signed_width(dividend, width) == signed_minimum(width)
               & signed_width(source, width) == -1 then Some(faulted(
              state, instruction.form.operation, DivideOverflow, "signed minimum divided by -1"
            ))
            else {
              let quotient = if signed_operation then
                  tdiv_int(signed_width(dividend, width), signed_width(source, width))
                else tdiv_int(unsigned(narrow_bits(dividend, width)),
                              unsigned(narrow_bits(source, width)));
              let remainder = if signed_operation then
                  signed_width(dividend, width) - quotient * signed_width(source, width)
                else tmod_int(unsigned(narrow_bits(dividend, width)),
                              unsigned(narrow_bits(source, width)));
              let after_quotient = write_local_destination(
                state, quotient_destination, bits_from_int(quotient)
              );
              let updated = write_local_destination(
                after_quotient, remainder_destination, bits_from_int(remainder)
              );
              Some(local_result(state, instruction, updated, CommitRegisters))
            }
          },
        _ => None(),
      },
    _ => None(),
  }
}

function concatenated_pair(high : bits(64), low : bits(64), width : int) -> bits(128) =
  if width == 1 then sail_zero_extend(high[7 .. 0] @ low[7 .. 0], 128)
  else if width == 2 then sail_zero_extend(high[15 .. 0] @ low[15 .. 0], 128)
  else if width == 4 then sail_zero_extend(high[31 .. 0] @ low[31 .. 0], 128)
  else high @ low

function execute_extract_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "offset"), value_named(instruction, state, "high"),
         operand_named(instruction, "low_dst")) {
    (Some(offset_value), Some(high), Some(low_operand)) =>
      match (local_operand_value(state, low_operand), local_destination(low_operand, width)) {
        (Some(low), Some(destination)) => {
          let offset = unsigned(offset_value[6 .. 0]);
          let value : bits(64) = if offset >= width_bits(width) * 2 then 0x0000000000000000
            else sail_shiftright(concatenated_pair(high, low, width), offset)[63 .. 0];
          let updated = write_local_destination(state, destination, narrow_bits(value, width));
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_extend_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let source_width = operation_width(instruction);
  let destination_width = extension_destination_width(instruction.form.operation);
  match (value_named(instruction, state, "src"),
         destination_named(instruction, "dst", destination_width)) {
    (Some(source), Some(destination)) => {
      let signed_operation = instruction.form.operation == Op_EXTSW
                           | instruction.form.operation == Op_EXTSL
                           | instruction.form.operation == Op_EXTSQ;
      let value = if signed_operation then sign_extend_width(source, source_width)
                  else narrow_bits(source, source_width);
      let updated = write_local_destination(state, destination, value);
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function execute_xchg_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (operand_named(instruction, "lhs"), operand_named(instruction, "rhs")) {
    (Some(lhs_operand), Some(rhs_operand)) =>
      match (local_operand_value(state, lhs_operand), local_operand_value(state, rhs_operand),
             local_destination(lhs_operand, width), local_destination(rhs_operand, width)) {
        (Some(lhs), Some(rhs), Some(lhs_destination), Some(rhs_destination)) => {
          let after_lhs = write_local_destination(state, lhs_destination, rhs);
          let updated = write_local_destination(after_lhs, rhs_destination, lhs);
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }
}

function execute_set_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match destination_named(instruction, "dst", width) {
    Some(destination) => {
      let updated = write_local_destination(state, destination, 0x0000000000000001);
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    None() => None(),
  }
}

function execute_move_sp_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (operand_named(instruction, "src"), operand_named(instruction, "dst")) {
    (Some(source_operand), Some(destination_operand)) =>
      match (local_operand_value(state, source_operand), local_destination(destination_operand, 8)) {
        (Some(source), Some(destination)) => {
          let updated = write_local_destination(state, destination, source);
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
        _ => None(),
      },
    _ => None(),
  }

function execute_bounds_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  match (value_named(instruction, state, "lo"), value_named(instruction, state, "value"),
         value_named(instruction, state, "hi")) {
    (Some(low), Some(value), Some(high)) => {
      let operation = instruction.form.operation;
      let inclusive_low = operation == Op_BNDSII | operation == Op_BNDSIX
                        | operation == Op_BNDUII | operation == Op_BNDUIX;
      let inclusive_high = operation == Op_BNDSII | operation == Op_BNDSXI
                         | operation == Op_BNDUII | operation == Op_BNDUXI;
      let signed_operation = operation == Op_BNDSII | operation == Op_BNDSIX
                           | operation == Op_BNDSXI | operation == Op_BNDSXX;
      let low_value = if signed_operation then signed_width(low, width)
                      else unsigned(narrow_bits(low, width));
      let tested_value = if signed_operation then signed_width(value, width)
                         else unsigned(narrow_bits(value, width));
      let high_value = if signed_operation then signed_width(high, width)
                       else unsigned(narrow_bits(high, width));
      let below = if inclusive_low then tested_value < low_value else tested_value <= low_value;
      let above = if inclusive_high then tested_value > high_value else tested_value >= high_value;
      let updated = { state with flags = set_flag_v_only(state.flags, below | above) };
      Some(local_result(state, instruction, updated, CommitRegisters))
    },
    _ => None(),
  }
}

function control_target_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(bits(64)) =
  match operand_named(instruction, "target") {
    None() => None(),
    Some(operand) => match local_operand_value(state, operand) {
      None() => None(),
      Some(value) => if operand.type_name == "imm8s" | operand.type_name == "imm16s"
                        | operand.type_name == "imm32s" then
          Some(add_bits(next_pc(state, instruction), value))
        else Some(narrow_bits(value, operation_width(instruction))),
    },
  }

function execute_compare_jump_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match (value_named(instruction, state, "src"), value_named(instruction, state, "dst"),
         value_named(instruction, state, "target"), condition_field(instruction.fields)) {
    (Some(source), Some(destination), Some(relative), Some(condition)) => {
      let width = operation_width(instruction);
      let temporary_flags = if instruction.form.operation == Op_CMPJcc then {
        let (ignored, flags) = sub_with_flags(destination, source, 0, width);
        flags
      } else {
        let value = narrow_bits(destination & source, width);
        flags_value(value == 0x0000000000000000, width_sign(value, width), false, false)
      };
      let pc = if condition_holds(condition, temporary_flags)
        then add_bits(next_pc(state, instruction), relative)
        else next_pc(state, instruction);
      Some(completed(state, { state with pc = pc }, CommitControl, [||]))
    },
    _ => None(),
  }

val start_control_transaction : (Decoded_instruction, Cpu_state) -> option(Execution_result)

function execute_count_jump(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let condition : int = match condition_field(instruction.fields) {
    Some(value) => value, None() => 0
  };
  if instruction.form.operation == Op_DJcc then match operand_named(instruction, "counter") {
    None() => faulted(state, Op_DJcc, IllegalInstruction, "missing DJcc counter"),
    Some(counter_operand) => {
      let index = unsigned(counter_operand.value[3 .. 0]);
      let count = sub_bits(state.registers[index], 0x0000000000000001);
      var staged = state;
      staged.registers[index] = count;
      if count != 0x0000000000000000 & condition_holds(condition, state.flags) then
        match start_control_transaction(instruction, staged) {
          Some(result) => { result with state = state,
            pending = { result.pending with before = state } },
          None() => faulted(state, Op_DJcc, IllegalInstruction, "missing DJcc target"),
        }
      else completed(state, { staged with pc = next_pc(state, instruction) }, CommitControl, [||])
    },
  }
  else match (operand_named(instruction, "index"), operand_named(instruction, "bound")) {
    (Some(index_operand), Some(bound_operand)) => {
      let index = unsigned(index_operand.value[3 .. 0]);
      let bound = unsigned(bound_operand.value[3 .. 0]);
      let index_value = add_bits(state.registers[index], 0x0000000000000001);
      var staged = state;
      staged.registers[index] = index_value;
      if index_value != state.registers[bound] & condition_holds(condition, state.flags) then
        match start_control_transaction(instruction, staged) {
          Some(result) => { result with state = state,
            pending = { result.pending with before = state } },
          None() => faulted(state, Op_IJcc, IllegalInstruction, "missing IJcc target"),
        }
      else completed(state, { staged with pc = next_pc(state, instruction) }, CommitControl, [||])
    },
    _ => faulted(state, Op_IJcc, IllegalInstruction, "missing IJcc operands"),
  }
}

