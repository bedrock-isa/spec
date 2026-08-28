// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_event_frame
  import bedrock_event_pkg::*;
(
  input  bedrock_event_frame_type_e frame_type_i,
  input  logic saved_dfa_i,
  input  logic [3:0] flags_i,
  input  logic [15:0] status_i,
  input  logic [31:0] event_code_i,
  input  logic [63:0] saved_pc_i,
  input  logic [63:0] saved_sp_i,
  input  logic [63:0] saved_cs_i,
  input  logic [63:0] saved_ds_i,
  input  logic [63:0] saved_ss_i,
  input  logic [63:0] error_code_i,
  input  logic [63:0] fault_ea_i,
  input  logic [63:0] fault_linear_i,
  input  logic [63:0] event_aux_i,
  output logic [7:0] frame_slots_o,
  output logic [12*64-1:0] frame_o
);
  always_comb begin
    frame_o = '0;
    unique case (frame_type_i)
      EVENT_FRAME_BASIC:     frame_slots_o = 8;
      EVENT_FRAME_ERROR:     frame_slots_o = 10;
      EVENT_FRAME_PAGE,
      EVENT_FRAME_AUXILIARY: frame_slots_o = 12;
    endcase
    frame_o[0*64 +: 64] = {12'b0, status_i, flags_i, 19'b0,
                            saved_dfa_i, 2'b0, frame_type_i, frame_slots_o};
    frame_o[1*64 +: 64] = {32'b0, event_code_i};
    frame_o[2*64 +: 64] = saved_pc_i;
    frame_o[3*64 +: 64] = saved_sp_i;
    frame_o[4*64 +: 64] = saved_cs_i;
    frame_o[5*64 +: 64] = saved_ds_i;
    frame_o[6*64 +: 64] = saved_ss_i;
    frame_o[7*64 +: 64] = '0;
    if (frame_type_i != EVENT_FRAME_BASIC)
      frame_o[8*64 +: 64] = error_code_i;
    if (frame_type_i == EVENT_FRAME_PAGE ||
        frame_type_i == EVENT_FRAME_AUXILIARY) begin
      frame_o[9*64 +: 64] = fault_ea_i;
      frame_o[10*64 +: 64] = fault_linear_i;
      frame_o[11*64 +: 64] = event_aux_i;
    end
  end
endmodule
