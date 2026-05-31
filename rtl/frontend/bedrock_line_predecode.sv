`timescale 1ns/1ps
`default_nettype none

module bedrock_line_predecode #(
  parameter int LINE_WORDS = 32
) (
  input  logic [LINE_WORDS*bedrock_pkg::WORD_BITS-1:0]            line_i,
  output logic [LINE_WORDS-1:0]                                   prefix_present_o,
  output logic [LINE_WORDS*3-1:0]                                 length_field_o,
  output logic [LINE_WORDS*4-1:0]                                 length_words_o,
  output logic [LINE_WORDS*bedrock_pkg::PRIMARY_PAYLOAD_BITS-1:0] primary_payload_o,
  output logic [LINE_WORDS-1:0]                                   sentinel_halt_o,
  output logic [LINE_WORDS-1:0]                                   sentinel_illegal_o
);

  for (genvar word_index = 0; word_index < LINE_WORDS; word_index++) begin : gen_word_predecode
    bedrock_pkg::word_t word0;
    bedrock_pkg::length_field_t length_field;
    bedrock_pkg::instruction_length_t length_words;
    bedrock_pkg::primary_payload_t primary_payload;

    assign word0 = line_i[word_index*bedrock_pkg::WORD_BITS +: bedrock_pkg::WORD_BITS];
    assign length_field_o[word_index*3 +: 3] = length_field;
    assign length_words_o[word_index*4 +: 4] = length_words;
    assign primary_payload_o[word_index*bedrock_pkg::PRIMARY_PAYLOAD_BITS +: bedrock_pkg::PRIMARY_PAYLOAD_BITS] = primary_payload;

    bedrock_predecode predecode (
      .word0_i(word0),
      .prefix_present_o(prefix_present_o[word_index]),
      .length_field_o(length_field),
      .length_words_o(length_words),
      .primary_payload_o(primary_payload),
      .sentinel_halt_o(sentinel_halt_o[word_index]),
      .sentinel_illegal_o(sentinel_illegal_o[word_index])
    );
  end
endmodule

`default_nettype wire
