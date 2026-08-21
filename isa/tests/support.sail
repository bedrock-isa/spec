function operation_count(operations : list(Semantic_operation)) -> int = match operations {
  [||] => 0,
  operation :: tail => {
    let _ = semantic_route(operation);
    1 + operation_count(tail)
  },
}

function catalog_count(entries : list(Catalog_entry)) -> int = match entries {
  [||] => 0,
  _ :: tail => 1 + catalog_count(tail),
}

function no_async_ingress() -> Async_ingress = struct {
  machine_check_pending = false, machine_check_code = 0x00000000,
  machine_check_error_code = 0x0000000000000000,
  machine_check_fault_ea = 0x0000000000000000,
  machine_check_fault_linear = 0x0000000000000000,
  machine_check_event_aux = 0x0000000000000000,
  nmi_pending = false, nmi_source = 0x000000,
  interrupt_pending = false, interrupt_id = 0x000000
}

function legal_representative_bytes(record : Representative_record) -> list(bits(8)) =
  if record.form_id == "long.ptquery_pt_level_i_ea_e_rn_d"
  then [|0xC7, 0xEF, 0x08, 0x00|]
  else if record.form_id == "extralong.divmods_x_ea_e_rn_q_rn_r"
  then [|0xCB, 0xF0, 0x80, 0x08, 0x80|]
  else if record.form_id == "extralong.divmodu_x_ea_e_rn_q_rn_r"
  then [|0xCB, 0xF0, 0x80, 0x00, 0x80|]
  else if record.form_id == "long.fsincosa_x_fn_s_fn_d_fn_c"
  then [|0xCB, 0xF0, 0x24, 0x00, 0x01|]
  else record.bytes

function successful_response(kind : Transaction_response_kind, value : bits(64),
                             bounds : bool) -> Transaction_response = struct {
  kind = kind, success = true, fault_kind = NoFault, detail = "", value = value,
  secondary_value = 0x0000000000000000, flags = 0x0, write_flags = false,
  generated_fflags = 0b00000, bounds_passed = bounds,
  cache_policy = 0, atomic_store_happened = false, body_bytes = [||],
  state_image = initial_cpu(), known = true, present = true,
  fp_response = empty_fp_response()
}

function failing_response(kind : Transaction_response_kind) -> Transaction_response = struct {
  kind = kind, success = false, fault_kind = AccessFault, detail = "test access fault",
  value = 0x0000000000000000, secondary_value = 0x0000000000000000,
  flags = 0x0, write_flags = false, generated_fflags = 0b00000, bounds_passed = false,
  cache_policy = 0, atomic_store_happened = false, body_bytes = [||],
  state_image = initial_cpu(), known = false, present = false,
  fp_response = empty_fp_response()
}

function response_bytes(kind : Transaction_response_kind, bytes : list(bits(8)))
  -> Transaction_response =
  { successful_response(kind, 0x0000000000000000, true) with body_bytes = bytes }

function pte_response(value : bits(64)) -> Transaction_response =
  successful_response(ResponsePteRead, value, true)

function operands_local(state : Cpu_state, operands : list(Decoded_operand)) -> bool =
  match operands {
    [||] => true,
    operand :: tail => match local_operand_value(state, operand) {
      Some(_) => operands_local(state, tail),
      None() => false,
    },
  }

function one_registers() -> Registers = [
  0x0000000000000001, 0x0000000000000001, 0x0000000000000001, 0x0000000000000001,
  0x0000000000000001, 0x0000000000000001, 0x0000000000000001, 0x0000000000000001,
  0x0000000000000001, 0x0000000000000001, 0x0000000000000001, 0x0000000000000001,
  0x0000000000000001, 0x0000000000000001, 0x0000000000000001, 0x0000000000000001
]

function expect_operand_value(instruction : Decoded_instruction, name : string,
                              expected : bits(64)) -> unit =
  match find_operand_by_name(name, instruction.operands) {
    Some(operand) => assert(operand.value == expected),
    None() => assert(false),
  }

function expect_ea_payload(instruction : Decoded_instruction, name : string,
                           expected : bits(64), width : int) -> unit =
  match find_operand_by_name(name, instruction.operands) {
    Some(operand) => match operand.ea {
      Some(ea) => {
        assert(ea.payload == expected);
        assert(ea.payload_width == width)
      },
      None() => assert(false),
    },
    None() => assert(false),
  }

function expect_ea_field(fields : list(Decoded_field), symbol : string, expected : int) -> unit =
  match find_decoded_field(symbol, fields) {
    Some(field) => assert(field.value == expected),
    None() => assert(false),
  }
