function architectural_state_fault(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_fault) = {
  let operation = instruction.form.operation;
  if instruction.form.route == RouteControlFlow & not_bool(segment_image_valid(state.segments[0])) then
    Some(struct { kind = InvalidControlState, operation = operation,
                  detail = "invalid current code segment",
                  error_code = 0x0000000000000002, bus_error = false })
  else None()
}
