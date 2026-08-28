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
