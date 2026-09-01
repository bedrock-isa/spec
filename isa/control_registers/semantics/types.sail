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
