struct Time_state = {
  value : bits(64),
  ticks_per_second : bits(64),
  armed : bool,
  deadline : bits(64),
  interrupt_identity : bits(24),
}

function initial_time_state() -> Time_state = struct {
  value = 0x0000000000000000,
  ticks_per_second = 0x000000003B9ACA00,
  armed = false,
  deadline = 0x0000000000000000,
  interrupt_identity = 0x000000,
}
