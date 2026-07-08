`timescale 1ns/1ps
`default_nettype none

module bedrock_ea_decode
  import bedrock_ea_decode_pkg::*;
(
  input  logic [5:0]  ea_i,
  input  logic [15:0] descriptor_i,
  output logic        valid_o,
  output logic        reserved_o,
  output logic        needs_descriptor_o,
  output bedrock_ea_form_e form_o,
  output logic        is_register_o,
  output logic        is_memory_o,
  output logic        is_immediate_o,
  output logic        update_eligible_o,
  output logic        signed32_index_escape_o,
  output logic        segment_selectable_o,
  output logic        segment_valid_o,
  output logic        has_base_reg_o,
  output logic        has_index_reg_o,
  output logic        has_displacement_o,
  output logic        has_absolute_o,
  output bedrock_ea_segment_e segment_o,
  output bedrock_ea_base_e base_o,
  output logic [2:0]  base_reg_o,
  output logic [2:0]  index_reg_o,
  output logic [1:0]  scale_log2_o,
  output logic [2:0]  displacement_words_o,
  output logic [2:0]  payload_words_o
);
  bedrock_ea_decode_t decode;
  always_comb begin
    decode = bedrock_decode_ea(ea_i, descriptor_i);
    valid_o = decode.valid;
    reserved_o = decode.reserved;
    needs_descriptor_o = decode.needs_descriptor;
    form_o = decode.form;
    is_register_o = decode.is_register;
    is_memory_o = decode.is_memory;
    is_immediate_o = decode.is_immediate;
    update_eligible_o = decode.update_eligible;
    signed32_index_escape_o = decode.signed32_index_escape;
    segment_selectable_o = decode.segment_selectable;
    segment_valid_o = decode.segment_valid;
    has_base_reg_o = decode.has_base_reg;
    has_index_reg_o = decode.has_index_reg;
    has_displacement_o = decode.has_displacement;
    has_absolute_o = decode.has_absolute;
    segment_o = decode.segment;
    base_o = decode.base;
    base_reg_o = decode.base_reg;
    index_reg_o = decode.index_reg;
    scale_log2_o = decode.scale_log2;
    displacement_words_o = decode.displacement_words;
    payload_words_o = decode.payload_words;
  end
endmodule

`default_nettype wire
