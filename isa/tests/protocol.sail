function test_protocol_audit() -> unit = {
  test_protocol_environment_group();
  test_protocol_state_group();
  test_protocol_stack_group();
  test_protocol_events_group()
}
