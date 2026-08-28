// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_decode_assertions
  import bedrock_decode_pkg::*;
(
  input logic clk_i,
  input logic reset_i,
  input d0_result_t d0_i,
  input d1_opcode_result_t d1_i,
  input ea_decode_result_t ea_i
);
  default clocking cb @(posedge clk_i); endclocking
  default disable iff (reset_i);

  assert property (d0_i.status == D0_SUCCESS |-> d0_i.form != FORM_INVALID);
  assert property (d0_i.status == D0_SUCCESS |-> $onehot(d0_i.form_high_decode));
  assert property (d0_i.status == D0_SUCCESS |-> $onehot(d0_i.form_low_decode));
  assert property (d1_i.valid |-> d1_i.stage == D1_STAGE_SUCCESS);
  assert property (ea_i.valid |-> ea_i.stage == D1_STAGE_SUCCESS);
  assert property (d1_i.valid |-> d1_i.form == d0_i.form);
  cover property (d1_i.valid && ea_i.valid);
endmodule
