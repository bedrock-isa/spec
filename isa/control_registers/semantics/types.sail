default Order dec

$include <prelude.sail>
$include <generic_equality.sail>

struct Interrupt_file = {
  max_id : bits(24),
  pending : list(bits(24)),
  enabled : list(bits(24)),
  threshold : bits(24),
  selector : bits(20),
}

function initial_interrupt_file() -> Interrupt_file = struct {
  max_id = 0xFFFFFF,
  pending = [||],
  enabled = [||],
  threshold = 0x000000,
  selector = 0x00000,
}

struct Debug_trigger_slot = {
  settings : bits(64),
  low : bits(64),
  high : bits(64),
}

struct Debug_trigger_file = {
  slot_count : int,
  selector : bits(18),
  slots : list(Debug_trigger_slot),
}

function empty_debug_trigger_slot() -> Debug_trigger_slot = struct {
  settings = 0x0000000000000000,
  low = 0x0000000000000000,
  high = 0x0000000000000000,
}

function empty_debug_trigger_slots(count : int) -> list(Debug_trigger_slot) =
  if count <= 0 then [||]
  else empty_debug_trigger_slot() :: empty_debug_trigger_slots(count - 1)

function initial_debug_trigger_file() -> Debug_trigger_file = struct {
  slot_count = 4,
  selector = 0b000000000000000000,
  slots = empty_debug_trigger_slots(4),
}
