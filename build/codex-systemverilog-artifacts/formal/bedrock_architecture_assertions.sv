// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_architecture_assertions
  import bedrock_event_pkg::*;
(
  input logic clk_i,
  input logic reset_i,
  input logic register_valid_i,
  input logic register_reserved_zero_i,
  input logic register_write_i,
  input logic event_known_i,
  input bedrock_event_frame_type_e event_frame_i,
  input logic [7:0] event_frame_slots_i
);
  default clocking cb @(posedge clk_i); endclocking
  default disable iff (reset_i);

  assert property (register_valid_i && register_write_i |-> register_reserved_zero_i);
  assert property (event_known_i && event_frame_i == EVENT_FRAME_BASIC
                   |-> event_frame_slots_i == 8);
  assert property (event_known_i && event_frame_i == EVENT_FRAME_ERROR
                   |-> event_frame_slots_i == 10);
  assert property (event_known_i &&
                   (event_frame_i == EVENT_FRAME_PAGE ||
                    event_frame_i == EVENT_FRAME_AUXILIARY)
                   |-> event_frame_slots_i == 12);
endmodule
