`timescale 1ns/1ps
`default_nettype none

module bedrock_predecode(
  input  bedrock_pkg::word_t               word0_i,
  output logic                             prefix_present_o,
  output bedrock_pkg::length_field_t       length_field_o,
  output bedrock_pkg::instruction_length_t length_words_o,
  output bedrock_pkg::primary_payload_t    primary_payload_o,
  output logic                             sentinel_halt_o,
  output logic                             sentinel_illegal_o
);

  always_comb begin
    prefix_present_o = bedrock_pkg::word0_prefix_present(word0_i);
    length_field_o = bedrock_pkg::word0_length_field(word0_i);
    length_words_o = bedrock_pkg::word0_length_words(word0_i);
    primary_payload_o = bedrock_pkg::word0_primary_payload(word0_i);
    sentinel_halt_o = bedrock_pkg::word0_is_halt(word0_i);
    sentinel_illegal_o = bedrock_pkg::word0_is_illegal(word0_i);
  end
endmodule

`default_nettype wire
