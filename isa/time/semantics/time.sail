function time_deadline_reached(value : bits(64), deadline : bits(64)) -> bool =
  signed(sub_bits(deadline, value)) <= 0

function time_with_arm(state : Cpu_state, deadline : bits(64), identity : bits(24))
  -> Cpu_state =
  if time_deadline_reached(state.time.value, deadline) then {
    var updated = post_interrupt(state, identity);
    updated.time.armed = false;
    updated
  }
  else {
    var updated = state;
    updated.time.armed = true;
    updated.time.deadline = deadline;
    updated.time.interrupt_identity = identity;
    updated
  }

function time_with_cancel(state : Cpu_state) -> Cpu_state = {
  var updated = state;
  updated.time.armed = false;
  updated
}

function advance_time(state : Cpu_state, ticks : bits(64)) -> Cpu_state = {
  let distance = sub_bits(state.time.deadline, state.time.value);
  let expires = state.time.armed
    & (signed(distance) <= 0 | unsigned(ticks) >= unsigned(distance));
  var updated = state;
  updated.time.value = add_bits(state.time.value, ticks);
  if expires then {
    updated = post_interrupt(updated, state.time.interrupt_identity);
    updated.time.armed = false
  } else ();
  updated
}
