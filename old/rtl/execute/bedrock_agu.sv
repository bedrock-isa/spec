`timescale 1ns/1ps
`default_nettype none

module bedrock_agu
  import bedrock_prefix_decode_pkg::*;
  import bedrock_ea_decode_pkg::*;
  import bedrock_agu_pkg::*;
(
  input  bedrock_agu_request_t request_i,
  input  logic [63:0]          base_reg_value_i,
  input  logic [63:0]          index_reg_value_i,
  input  logic [63:0]          pc_value_i,
  input  logic [63:0]          sp_value_i,
  input  logic [63:0]          payload_value_i,
  input  logic [3:0]           access_size_bytes_i,

  output logic                 valid_o,
  output logic                 address_valid_o,
  output logic [63:0]          effective_address_o,
  output logic [63:0]          immediate_value_o,
  output logic                 update_write_o,
  output logic [63:0]          update_value_o,
  output logic                 update_invalid_o
);

  logic [63:0] base_value;
  logic [63:0] updated_base_value;
  logic [63:0] address_base_value;
  logic [63:0] displacement_value;
  logic [63:0] absolute_value;
  logic [63:0] index_value;
  logic [63:0] scaled_index_value;
  logic [63:0] update_amount;
  logic update_is_pre;
  logic update_is_dec;

  function automatic logic [63:0] sign_extend_payload(
    input logic [63:0] value,
    input logic [2:0] words
  );
    unique case (words)
      3'd0: sign_extend_payload = 64'd0;
      3'd1: sign_extend_payload = {{48{value[15]}}, value[15:0]};
      3'd2: sign_extend_payload = {{32{value[31]}}, value[31:0]};
      default: sign_extend_payload = value;
    endcase
  endfunction

  always_comb begin
    unique case (request_i.base)
      BR_EA_BASE_D,
      BR_EA_BASE_A: base_value = base_reg_value_i;
      BR_EA_BASE_SP: base_value = sp_value_i;
      BR_EA_BASE_PC: base_value = pc_value_i;
      default: base_value = 64'd0;
    endcase

    displacement_value = request_i.has_displacement
      ? sign_extend_payload(payload_value_i, request_i.displacement_words)
      : 64'd0;
    absolute_value = request_i.has_absolute
      ? sign_extend_payload(payload_value_i, request_i.displacement_words)
      : 64'd0;
    index_value = request_i.signed32_index_escape
      ? {{32{index_reg_value_i[31]}}, index_reg_value_i[31:0]}
      : index_reg_value_i;
    scaled_index_value = request_i.has_index_reg
      ? (index_value << request_i.scale_log2)
      : 64'd0;

    update_amount = {60'd0, access_size_bytes_i};
    update_is_pre =
      request_i.update_mode == BR_UPDATE_PREINC
      || request_i.update_mode == BR_UPDATE_PREDEC;
    update_is_dec =
      request_i.update_mode == BR_UPDATE_POSTDEC
      || request_i.update_mode == BR_UPDATE_PREDEC;
    updated_base_value = update_is_dec
      ? (base_value - update_amount)
      : (base_value + update_amount);
    address_base_value = update_is_pre ? updated_base_value : base_value;

    effective_address_o = request_i.has_absolute
      ? absolute_value
      : (address_base_value + scaled_index_value + displacement_value);
    immediate_value_o = payload_value_i;
    update_invalid_o = request_i.update_invalid || (request_i.update_requested && access_size_bytes_i == 4'd0);
    valid_o = request_i.valid && request_i.segment_valid && !update_invalid_o;
    address_valid_o = valid_o && request_i.is_memory;
    update_write_o = valid_o && request_i.update_requested;
    update_value_o = request_i.update_requested ? updated_base_value : base_value;
  end
endmodule

`default_nettype wire
