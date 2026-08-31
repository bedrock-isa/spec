function cfi_fault(state : Cpu_state, operation : Semantic_operation,
                   cause : int, detail : string) -> Execution_result =
  faulted_with_error_code(
    state, operation, CfiViolationFault, detail, bits_from_int(cause)
  )

function cfi_shadow_request(kind : Primitive_request_kind, state : Cpu_state,
                            address : bits(64), access : Transaction_access,
                            low : bits(64), high : bits(64), commit : bool)
  -> Primitive_request = {
  let image = control_register_value(state, ControlRegister_CFI_CFISS);
  let point = segment_point(image, address);
  {
    empty_primitive_request() with
    kind = kind,
    role = RequestRoleStack,
    domain = RequestDomainStack,
    segment = 0,
    segment_image = image,
    width = 16,
    range_start = address,
    range_end = add_bits(address, 0x0000000000000010),
    range_length = 16,
    range_wrap = unsigned(add_bits(address, 0x0000000000000010))
                 < unsigned(address),
    range_end_at_modulus = add_bits(address, 0x0000000000000010)
                           == 0x0000000000000000,
    effective_address = address,
    linear_address = point.linear,
    access = access,
    value = low,
    address_translation = true,
    commit_point = commit,
    auxiliary = high,
  }
}

function cfi_landing_request(target : bits(64), cs_image : bits(64))
  -> Primitive_request =
  {
    empty_primitive_request() with
    kind = RepeatBodyFetch,
    role = RequestRoleControlTarget,
    domain = RequestDomainCode,
    segment = 0,
    segment_image = cs_image,
    width = 1,
    range_start = target,
    range_end = target,
    range_length = 0,
    effective_address = target,
    linear_address = segment_point(cs_image, target).linear,
    access = AccessExecute,
    address_translation = true,
    body_length = 0,
  }

union clause Uop_kind = UopCfiLandingFetch : unit
union clause Uop_kind = UopCfiLandingCheck : unit
union clause Uop_kind = UopCfiShadowPushPrepare : unit
union clause Uop_kind = UopCfiShadowPush : unit
union clause Uop_kind = UopCfiShadowLoad : unit
union clause Uop_kind = UopCfiShadowCheck : unit

function clause execute_uop(UopCfiLandingFetch(), uop, values, instruction,
                            before, speculative) =
  match (uop_location_read(uop.source0, speculative, values),
         uop_location_read(uop.source1, speculative, values)) {
    (Some(target), Some(cs_image)) =>
      if not_bool(segment_image_valid(cs_image))
         | not_bool(segment_point(cs_image, target).in_bounds) then
        uop_step_fault(cfi_fault(
          before, instruction.form.operation, 4, "invalid CFI landing target state"
        ))
      else uop_step_wait(
        uop.destination.index,
        cfi_landing_request(target, cs_image),
        target,
      ),
    _ => uop_step_fault(cfi_fault(
      before, instruction.form.operation, 4, "unavailable CFI landing target"
    )),
  }

function clause execute_uop(UopCfiLandingCheck(), uop, values, instruction,
                            before, speculative) =
  match uop_value_get(values, uop.source0.index) {
    None() => uop_step_fault(cfi_fault(
      before, instruction.form.operation, 4, "missing CFI landing fetch response"
    )),
    Some(response) => match decode_full_record(response.body_bytes) {
      Some(target) =>
        if target.form.operation == Op_CFILAND
           & byte_list_length(response.body_bytes) == target.encoded_length then
          uop_step_continue(speculative, values)
        else uop_step_fault(cfi_fault(
          before, instruction.form.operation, 1, "indirect target is not CFILAND"
        )),
      None() => uop_step_fault(cfi_fault(
        before, instruction.form.operation, 1, "indirect target is not decodable CFILAND"
      )),
    },
  }

function clause execute_uop(UopCfiShadowPushPrepare(), _, values, instruction,
                            before, speculative) =
  if not_bool(cfi_shadow_push_state_valid(speculative)) then
    uop_step_fault(cfi_fault(
      before, instruction.form.operation, 4, "invalid CFI shadow-push state"
    ))
  else {
    var updated = speculative;
    updated = control_register_with_value(
      updated, ControlRegister_CFI_CFISP,
      sub_bits(control_register_value(speculative, ControlRegister_CFI_CFISP),
               0x0000000000000010));
    uop_step_continue(updated, values)
  }

function clause execute_uop(UopCfiShadowPush(), uop, values, instruction,
                            before, speculative) =
  match (uop_location_read(uop.source0, speculative, values),
         uop_location_read(uop.source1, speculative, values)) {
    (Some(return_pc), Some(return_cs)) =>
      if not_bool(cfi_shadow_pop_state_valid(speculative)) then
        uop_step_fault(cfi_fault(
          before, instruction.form.operation, 4, "invalid CFI shadow-push state"
        ))
      else {
        uop_step_wait(
          0 - 1,
          cfi_shadow_request(
            CompoundMemoryStore, speculative,
            control_register_value(speculative, ControlRegister_CFI_CFISP),
            AccessStackWrite,
            return_pc, return_cs, true
          ),
          return_pc,
        )
      },
    _ => uop_step_fault(cfi_fault(
      before, instruction.form.operation, 4, "unavailable CFI shadow-push value"
    )),
  }

function clause execute_uop(UopCfiShadowLoad(), uop, _, instruction,
                            before, speculative) =
  if not_bool(cfi_shadow_pop_state_valid(speculative)) then
    uop_step_fault(cfi_fault(
      before, instruction.form.operation, 4, "invalid CFI shadow-pop state"
    ))
  else uop_step_wait(
    uop.destination.index,
    cfi_shadow_request(
      MemoryRead, speculative,
      control_register_value(speculative, ControlRegister_CFI_CFISP), AccessStackRead,
      0x0000000000000000, 0x0000000000000000, false
    ),
    0x0000000000000000,
  )

function clause execute_uop(UopCfiShadowCheck(), uop, values, instruction,
                            before, speculative) =
  match (uop_value_get(values, uop.source0.index),
         uop_location_read(uop.source1, speculative, values),
         uop_location_read(uop.source2, speculative, values)) {
    (Some(shadow), Some(return_pc), Some(return_cs)) =>
      if shadow.value != return_pc then
        uop_step_fault(cfi_fault(
          before, instruction.form.operation, 2, "shadow return PC mismatch"
        ))
      else if shadow.secondary_value != return_cs then
        uop_step_fault(cfi_fault(
          before, instruction.form.operation, 3, "shadow return CS mismatch"
        ))
      else {
        var updated = speculative;
        updated = control_register_with_value(
          updated, ControlRegister_CFI_CFISP,
          add_bits(control_register_value(speculative, ControlRegister_CFI_CFISP),
                   0x0000000000000010));
        uop_step_continue(updated, values)
      },
    _ => uop_step_fault(cfi_fault(
      before, instruction.form.operation, 4, "unavailable CFI shadow-return value"
    )),
  }

function cfi_with_shadow_push(program : list(Uop)) -> list(Uop) =
  match program {
    [||] => [||],
    uop :: tail => match uop.kind {
      UopNextPc() => uop :: uop_make(
        UopCfiShadowPushPrepare(), uop_location_make_none(),
        uop_location_make_none(), uop_location_make_none(),
        Operand_target, 16, CommitControl
      ) :: uop_make(
        UopCfiShadowPush(), uop.destination, uop_location_make_segment(0),
        uop_location_make_none(), Operand_target, 16, CommitMemory
      ) :: tail,
      _ => uop :: cfi_with_shadow_push(tail),
    },
  }

function cfi_with_landing_check(program : list(Uop)) -> list(Uop) =
  match program {
    [||] => [||],
    uop :: tail => match uop.kind {
      UopControlCommit(_) => [|
        uop_make(
          UopCfiLandingFetch(), uop.source0, uop.source1,
          uop_location_make_temporary(62), Operand_target, 1, CommitControl
        ),
        uop_make(
          UopCfiLandingCheck(), uop_location_make_temporary(62),
          uop_location_make_none(), uop_location_make_none(),
          Operand_target, 1, CommitControl
        ),
        uop
      |],
      _ => uop :: cfi_with_landing_check(tail),
    },
  }

function cfi_with_shadow_return(program : list(Uop)) -> list(Uop) =
  match program {
    [||] => [||],
    uop :: tail => match uop.kind {
      UopControlCommit(_) => [|
        uop_make(
          UopCfiShadowLoad(), uop_location_make_none(), uop_location_make_none(),
          uop_location_make_temporary(62), Operand_target, 16, CommitMemory
        ),
        uop_make_ternary(
          UopCfiShadowCheck(), uop_location_make_temporary(62),
          uop.source0, uop.source1, uop_location_make_none(),
          Operand_target, 16, CommitControl
        ),
        uop
      |],
      _ => uop :: cfi_with_shadow_return(tail),
    },
  }
