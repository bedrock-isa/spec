`timescale 1ns/1ps
`default_nettype none

module bedrock_prefix_decode
  import bedrock_prefix_decode_pkg::*;
(
  input  logic [15:0] prefix_word_i,
  output logic        valid_o,
  output logic        nospec_o,
  output logic        saturate_o,
  output logic        nontemporal_o,
  output bedrock_update_mode_e update_mode_o,
  output bedrock_access_mode_e access_mode_o,
  output bedrock_repeat_kind_e repeat_kind_o,
  output logic [3:0] repeat_condition_o,
  output logic [2:0] repeat_counter_o
);
  bedrock_prefix_word_decode_t decode;
  always_comb begin
    decode = bedrock_decode_prefix_word(prefix_word_i);
    valid_o = decode.valid;
    nospec_o = decode.nospec;
    saturate_o = decode.saturate;
    nontemporal_o = decode.nontemporal;
    update_mode_o = decode.update_mode;
    access_mode_o = decode.access_mode;
    repeat_kind_o = decode.repeat_kind;
    repeat_condition_o = decode.repeat_condition;
    repeat_counter_o = decode.repeat_counter;
  end
endmodule

`default_nettype wire
