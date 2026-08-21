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
  if operand.type_name == "CS" then 0 else unsigned(operand.value[2 .. 0]) + 1

function control_index(selector : int) -> option(bits(5)) =
  if selector == 0 then Some(0b00000)
  else if selector == 1 then Some(0b00001)
  else if selector == 2 then Some(0b00010)
  else if selector == 256 then Some(0b00011)
  else if selector == 257 then Some(0b00100)
  else if selector == 258 then Some(0b00101)
  else if selector == 264 then Some(0b00110)
  else if selector == 265 then Some(0b00111)
  else if selector == 266 then Some(0b01000)
  else if selector == 267 then Some(0b01001)
  else if selector == 268 then Some(0b01010)
  else if selector == 269 then Some(0b01011)
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
  selector == 273 | selector == 274 | selector == 528
  | selector == 544 | selector == 560

function control_pointer_requires_alignment(selector : int) -> bool =
  selector == 529 | selector == 545 | selector == 561

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
  & event_stack_pair_valid(state.controls[17], state.controls[18])
  & event_stack_pair_valid(state.controls[19], state.controls[20])
  & event_stack_pair_valid(state.controls[21], state.controls[22])

function read_state_register(instruction : Decoded_instruction, state : Cpu_state,
                             value : bits(64)) -> Execution_result =
  match destination_named(instruction, "dst", 8) {
    Some(destination) => {
      let updated = write_local_destination(
        state, instruction.form.operation, destination, value
      );
      local_result(state, instruction, updated, CommitRegisters)
    },
    None() => faulted(state, instruction.form.operation, IllegalInstruction,
                      "missing state-register destination"),
  }

function execute_system_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  if operation == Op_SETF then match value_named(
    instruction, state, "mask"
  ) {
    Some(mask) => {
      let selected = mask[3 .. 0];
      Some(local_result(state, instruction, { state with flags = selected }, CommitRegisters))
    },
    None() => None(),
  }
  else if operation == Op_RDFLAGS then Some(read_state_register(
    instruction, state, sail_zero_extend(state.flags, 64)
  ))
  else if operation == Op_RDSTATUS then Some(read_state_register(
    instruction, state, narrow_bits(state.status, 2)
  ))
  else if operation == Op_RDFFLAGS then Some(read_state_register(
    instruction, state, sail_zero_extend(state.fflags, 64)
  ))
  else if operation == Op_RDFSTATUS then Some(read_state_register(
    instruction, state, narrow_bits(state.fstatus, 2)
  ))
  else if operation == Op_WRFLAGS | operation == Op_WRSTATUS
       | operation == Op_WRFFLAGS | operation == Op_WRFSTATUS then
    match value_named(instruction, state, "src") {
      None() => None(),
      Some(source) => if operation == Op_WRFLAGS then
        if (source & 0x000000000000FFF0) != 0x0000000000000000 then Some(faulted(
          state, operation, IllegalInstruction, "reserved FLAGS bits"
        )) else Some(local_result(
          state, instruction, { state with flags = source[3 .. 0] }, CommitRegisters
        ))
      else if operation == Op_WRSTATUS then {
        let candidate = source & 0x000000000000FFFF;
        if (candidate & 0x000000000000FFC0) != 0x0000000000000000
           | (candidate & 0x0000000000000011) != (state.status & 0x0000000000000011)
        then Some(faulted(state, operation, InvalidControlState,
                          "reserved or immutable STATUS bits"))
        else Some(local_result(
          state, instruction, { state with status = candidate }, CommitRegisters
        ))
      }
      else if operation == Op_WRFFLAGS then
        if (source & 0x000000000000FFE0) != 0x0000000000000000 then Some(faulted(
          state, operation, InvalidControlState, "reserved FFLAGS bits"
        )) else Some(local_result(
          state, instruction, { state with fflags = source[4 .. 0],
                                           fp_component_modified = true }, CommitRegisters
        ))
      else if (source & 0x000000000000FC00) != 0x0000000000000000 then Some(faulted(
        state, operation, InvalidControlState, "reserved FSTATUS bits"
      )) else Some(local_result(
        state, instruction, { state with fstatus = source & 0x00000000000003FF,
                                         fp_component_modified = true }, CommitRegisters
      )),
    }
  else if operation == Op_RDSEG then
    match (operand_named(instruction, "seg"), destination_named(instruction, "dst", 8)) {
      (Some(segment_operand), Some(destination)) => {
        let index = sreg_index(segment_operand);
        let updated = write_local_destination(
          state, instruction.form.operation, destination, state.segments[index]
        );
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
      _ => None(),
    }
  else if operation == Op_WRSEG then
    match (value_named(instruction, state, "src"), operand_named(instruction, "seg")) {
      (Some(source), Some(segment_operand)) =>
        if not_bool(segment_image_valid(source)) then Some(faulted(
          state, operation, InvalidControlState, "invalid segment image"
        )) else {
          var updated = state;
          updated.segments[sreg_index(segment_operand)] = source;
          Some(local_result(state, instruction, updated, CommitRegisters))
        },
      _ => None(),
    }
  else if operation == Op_RDCR then match value_named(instruction, state, "cr") {
    None() => None(),
    Some(raw_selector) => {
      let selector = unsigned(raw_selector[15 .. 0]);
      match control_index(selector) {
        Some(index) => Some(read_state_register(
          instruction, state, state.controls[unsigned(index)]
        )),
        None() => Some(faulted(
          state, operation, InvalidControlState, "unknown control-register selector"
        )),
      }
    },
  }
  else if operation == Op_WRCR then
    match (value_named(instruction, state, "src"), value_named(instruction, state, "cr")) {
      (Some(source), Some(raw_selector)) => {
        let selector = unsigned(raw_selector[15 .. 0]);
        let needs_transition = selector == 0 | selector == 1 | selector == 256
                             | selector == 272 | selector == 4097
                             | (selector == 2 & source[0] == bitone & state.controls[2][0] == bitzero)
                             | (selector == 269 & source[32] == bitone);
        if needs_transition then None()
        else match control_index(selector) {
          None() => Some(faulted(
            state, operation, InvalidControlState, "unknown control-register selector"
          )),
          Some(index) => {
            let segment_invalid = control_segment_requires_valid_image(selector)
                                & not_bool(segment_image_valid(source));
            let stack_invalid = control_pointer_requires_alignment(selector)
                              & (source & 0x000000000000003F) != 0x0000000000000000;
            let pmc_invalid = selector == 4352
                            & (source & 0xFFFFFFFFFFFFFFFE) != 0x0000000000000000;
            let ecr_invalid = selector == 2
                            & ((source & 0xFFFFFFFFFFFFF07E) != 0x0000000000000000
                               | (source[0] == bitone
                                  & not_bool(event_control_bank_valid(state))));
            let urctl_invalid = selector == 269
              & ((source & 0xFFFFFFFE00000000) != 0x0000000000000000
                 | source[31 .. 22] != 0b0000000000 | source[15 .. 4] != 0x000);
            if segment_invalid | stack_invalid | pmc_invalid | ecr_invalid | urctl_invalid
            then Some(faulted(state, operation, InvalidControlState,
                              "invalid control-register image"))
            else {
              var updated = state;
              updated.controls[unsigned(index)] = if selector == 2 then
                (source & 0x0000000000000F01) | (state.controls[2] & 0x0000000000000080)
                else source;
              Some(local_result(state, instruction, updated, CommitControl))
            }
          },
        }
      },
      _ => None(),
    }
  else None()
}

function execute_tlb_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation == Op_VTOP & state.controls[0][0] == bitzero then
    match (value_named(instruction, state, "virt"), destination_named(instruction, "phys", 8)) {
      (Some(address), Some(destination)) => {
        var updated = write_local_destination(
          state, instruction.form.operation, destination, address
        );
        updated.flags = 0b1111;
        Some(local_result(state, instruction, updated, CommitRegisters))
      },
      _ => None(),
    }
  else None()

function execute_data_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation == Op_XCHG then execute_xchg_local(instruction, state)
  else if instruction.form.operation == Op_MOV then match execute_move_sp_local(instruction, state) {
    Some(result) => Some(result),
    None() => execute_binary_local(instruction, state),
  }
  else execute_binary_local(instruction, state)

function execute_integer_local(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = match instruction.form.operation {
  Op_ADD => match execute_sp_arithmetic_local(instruction, state) {
    Some(result) => Some(result), None() => execute_binary_local(instruction, state)
  },
  Op_SUB => match execute_sp_arithmetic_local(instruction, state) {
    Some(result) => Some(result), None() => execute_binary_local(instruction, state)
  },
  Op_ADC => execute_binary_local(instruction, state),
  Op_SBB => execute_binary_local(instruction, state),
  Op_AND => execute_binary_local(instruction, state),
  Op_OR => execute_binary_local(instruction, state),
  Op_XOR => execute_binary_local(instruction, state),
  Op_CMP => execute_binary_local(instruction, state),
  Op_TEST => execute_binary_local(instruction, state),
  Op_CLR => execute_unary_local(instruction, state),
  Op_INC => execute_unary_local(instruction, state),
  Op_INCF => execute_unary_local(instruction, state),
  Op_DEC => execute_unary_local(instruction, state),
  Op_DECF => execute_unary_local(instruction, state),
  Op_NEG => execute_unary_local(instruction, state),
  Op_ABS => execute_unary_local(instruction, state),
  Op_NOT => execute_unary_local(instruction, state),
  Op_SHL => execute_shift_local(instruction, state),
  Op_SHR => execute_shift_local(instruction, state),
  Op_SAR => execute_shift_local(instruction, state),
  Op_ROL => execute_shift_local(instruction, state),
  Op_ROR => execute_shift_local(instruction, state),
  Op_BSET => execute_bit_local(instruction, state),
  Op_BCLR => execute_bit_local(instruction, state),
  Op_BCHG => execute_bit_local(instruction, state),
  Op_BTEST => execute_bit_local(instruction, state),
  Op_CLZ => execute_count_local(instruction, state),
  Op_CLS => execute_count_local(instruction, state),
  Op_CTZ => execute_count_local(instruction, state),
  Op_CTS => execute_count_local(instruction, state),
  Op_POPCNT => execute_count_local(instruction, state),
  Op_PARITY => execute_parity_local(instruction, state),
  Op_REVBYTE => execute_revbyte_local(instruction, state),
  Op_EXTRACT => execute_extract_local(instruction, state),
  Op_MUL => execute_math_local(instruction, state),
  Op_MULHU => execute_math_local(instruction, state),
  Op_MULHS => execute_math_local(instruction, state),
  Op_MULHSU => execute_math_local(instruction, state),
  Op_CLMUL => execute_math_local(instruction, state),
  Op_CLMULH => execute_math_local(instruction, state),
  Op_MINU => execute_math_local(instruction, state),
  Op_MAXU => execute_math_local(instruction, state),
  Op_MINS => execute_math_local(instruction, state),
  Op_MAXS => execute_math_local(instruction, state),
  Op_DIVU => execute_divide_local(instruction, state),
  Op_DIVS => execute_divide_local(instruction, state),
  Op_MODU => execute_divide_local(instruction, state),
  Op_MODS => execute_divide_local(instruction, state),
  Op_DIVMODU => execute_divmod_local(instruction, state),
  Op_DIVMODS => execute_divmod_local(instruction, state),
  Op_EXTZW => execute_extend_local(instruction, state),
  Op_EXTSW => execute_extend_local(instruction, state),
  Op_EXTZL => execute_extend_local(instruction, state),
  Op_EXTSL => execute_extend_local(instruction, state),
  Op_EXTZQ => execute_extend_local(instruction, state),
  Op_EXTSQ => execute_extend_local(instruction, state),
  _ => None(),
}
