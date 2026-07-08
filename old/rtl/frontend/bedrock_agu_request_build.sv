`timescale 1ns/1ps
`default_nettype none

module bedrock_agu_request_build
  import bedrock_prefix_decode_pkg::*;
  import bedrock_ea_decode_pkg::*;
  import bedrock_agu_pkg::*;
(
  input  logic                     ea_present_i,
  input  logic [5:0]               ea_value_i,
  input  logic [3:0]               descriptor_token_i,
  input  logic                     ea_valid_i,
  input  logic                     ea_reserved_i,
  input  logic                     ea_needs_descriptor_i,
  input  bedrock_ea_form_e         ea_form_i,
  input  logic                     ea_is_register_i,
  input  logic                     ea_is_memory_i,
  input  logic                     ea_is_immediate_i,
  input  logic                     ea_update_eligible_i,
  input  logic                     ea_signed32_index_escape_i,
  input  logic                     ea_segment_selectable_i,
  input  logic                     ea_segment_valid_i,
  input  logic                     ea_has_base_reg_i,
  input  logic                     ea_has_index_reg_i,
  input  logic                     ea_has_displacement_i,
  input  logic                     ea_has_absolute_i,
  input  bedrock_ea_segment_e      ea_segment_i,
  input  bedrock_ea_base_e         ea_base_i,
  input  logic [2:0]               ea_base_reg_i,
  input  logic [2:0]               ea_index_reg_i,
  input  logic [1:0]               ea_scale_log2_i,
  input  logic [2:0]               ea_displacement_words_i,
  input  logic [2:0]               ea_payload_words_i,
  input  bedrock_update_mode_e     update_mode_i,

  output bedrock_agu_request_t     request_o
);

  logic update_requested;

  always_comb begin
    update_requested = update_mode_i != BR_UPDATE_NONE;
    request_o = '0;

    request_o.present = ea_present_i;
    request_o.raw_valid = ea_valid_i;
    request_o.reserved = ea_reserved_i;
    request_o.valid = ea_present_i && ea_valid_i && !ea_reserved_i;
    request_o.is_register = ea_is_register_i;
    request_o.is_memory = ea_is_memory_i;
    request_o.is_immediate = ea_is_immediate_i;
    request_o.needs_descriptor = ea_needs_descriptor_i;
    request_o.signed32_index_escape = ea_signed32_index_escape_i;
    request_o.segment_selectable = ea_segment_selectable_i;
    request_o.segment_valid = ea_segment_valid_i;
    request_o.update_eligible = ea_update_eligible_i;
    request_o.update_requested = ea_present_i && update_requested;
    request_o.update_valid = !request_o.update_requested || ea_update_eligible_i;
    request_o.update_invalid = request_o.update_requested && !ea_update_eligible_i;
    request_o.has_base_reg = ea_has_base_reg_i;
    request_o.has_index_reg = ea_has_index_reg_i;
    request_o.has_displacement = ea_has_displacement_i;
    request_o.has_absolute = ea_has_absolute_i;
    request_o.raw_ea = ea_value_i;
    request_o.descriptor_token = descriptor_token_i;
    request_o.payload_base_token = descriptor_token_i + (ea_needs_descriptor_i ? 4'd1 : 4'd0);
    request_o.payload_words = ea_payload_words_i;
    request_o.displacement_words = ea_displacement_words_i;
    request_o.update_mode = update_mode_i;
    request_o.form = ea_form_i;
    request_o.segment = ea_segment_i;
    request_o.base = ea_base_i;
    request_o.base_reg = ea_base_reg_i;
    request_o.index_reg = ea_index_reg_i;
    request_o.scale_log2 = ea_scale_log2_i;
  end
endmodule

`default_nettype wire
