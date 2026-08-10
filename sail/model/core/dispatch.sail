function execute_route_exact(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = match instruction.form.route {
  RouteIntegerAlu => match execute_integer_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteIntegerUnary => match execute_integer_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteFpu => execute_external_route(instruction, state),
  RouteFpuTranscendental => execute_external_route(instruction, state),
  RouteIntegerBitfield => match execute_integer_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteIntegerMulDiv => match execute_integer_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteDataMovement => match execute_data_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteBounds => match execute_bounds_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteSystemRegisters => match execute_system_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteTlbContext => match execute_tlb_local(instruction, state) {
    Some(result) => result, None() => execute_external_route(instruction, state)
  },
  RouteControlFlow => execute_control_exact(instruction, state),
  RouteCoreControl => execute_core_exact(instruction, state),
  _ => execute_external_route(instruction, state),
}

function architectural_state_fault(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_fault) = {
  let operation = instruction.form.operation;
  let stack_operation = operation == Op_PUSH | operation == Op_POP | operation == Op_PUSHP
                      | operation == Op_POPP | operation == Op_FPUSHP | operation == Op_FPOPP
                      | operation == Op_CALL | operation == Op_CALLcc
                      | operation == Op_RET | operation == Op_LCALL | operation == Op_LRET;
  if instruction.form.route == RouteControlFlow & not_bool(segment_image_valid(state.segments[0])) then
    Some(struct { kind = InvalidControlState, operation = operation,
                  detail = "invalid current code segment",
                  error_code = 0x0000000000000002, bus_error = false })
  else if stack_operation & not_bool(segment_image_valid(state.segments[2])) then
    Some(struct { kind = InvalidControlState, operation = operation,
                  detail = "invalid current stack segment",
                  error_code = 0x0000000000000002, bus_error = false })
  else None()
}

