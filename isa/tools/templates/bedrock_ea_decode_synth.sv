`timescale 1ns/1ps
`default_nettype none

module bedrock_ea_decode_synth(
  input  [5:0]  ea_i,
  input  [15:0] descriptor_i,
  output reg        valid_o,
  output reg        reserved_o,
  output reg        needs_descriptor_o,
  output reg [5:0]  form_o,
  output reg        is_register_o,
  output reg        is_memory_o,
  output reg        is_immediate_o,
  output reg        update_eligible_o,
  output reg        signed32_index_escape_o,
  output reg        segment_selectable_o,
  output reg        segment_valid_o,
  output reg        has_base_reg_o,
  output reg        has_index_reg_o,
  output reg        has_displacement_o,
  output reg        has_absolute_o,
  output reg [2:0]  segment_o,
  output reg [2:0]  base_o,
  output reg [2:0]  base_reg_o,
  output reg [2:0]  index_reg_o,
  output reg [1:0]  scale_log2_o,
  output reg [2:0]  displacement_words_o,
  output reg [2:0]  payload_words_o
);
@EA_FORM_LOCALPARAMS@
  wire [4:0] mode = descriptor_i[15:11];
  wire [2:0] seg = descriptor_i[10:8];
  wire [7:0] extra = descriptor_i[7:0];
  reg signed32_escape;
  always @* begin
    valid_o = 1'b0;
    reserved_o = 1'b0;
    needs_descriptor_o = 1'b0;
    form_o = 6'd0;
    is_register_o = 1'b0;
    is_memory_o = 1'b0;
    is_immediate_o = 1'b0;
    update_eligible_o = 1'b0;
    signed32_index_escape_o = 1'b0;
    segment_selectable_o = 1'b0;
    segment_valid_o = 1'b1;
    has_base_reg_o = 1'b0;
    has_index_reg_o = 1'b0;
    has_displacement_o = 1'b0;
    has_absolute_o = 1'b0;
    segment_o = 3'd0;
    base_o = 3'd0;
    base_reg_o = 3'd0;
    index_reg_o = 3'd0;
    scale_log2_o = 2'd0;
    displacement_words_o = 3'd0;
    payload_words_o = 3'd0;
    signed32_escape = 1'b0;
    casez (ea_i)
@COMPACT_EA_CASES@
@RESERVED_COMPACT_EA_CASES@
      default: begin reserved_o = 1'b1; end
    endcase
    if (needs_descriptor_o) begin
      valid_o = 1'b0;
      reserved_o = 1'b0;
      form_o = 6'd0;
      is_register_o = 1'b0;
      is_memory_o = 1'b0;
      is_immediate_o = 1'b0;
      update_eligible_o = 1'b0;
      signed32_index_escape_o = signed32_escape;
      segment_selectable_o = 1'b0;
      segment_valid_o = 1'b1;
      has_base_reg_o = 1'b0;
      has_index_reg_o = 1'b0;
      has_displacement_o = 1'b0;
      has_absolute_o = 1'b0;
      segment_o = seg;
      base_o = 3'd0;
      base_reg_o = 3'd0;
      index_reg_o = 3'd0;
      scale_log2_o = 2'd0;
      displacement_words_o = 3'd0;
      payload_words_o = 3'd0;
      case (mode)
@EXTENDED_EA_CASES@
        default: begin reserved_o = 1'b1; end
      endcase
    end
  end
endmodule

`default_nettype wire
