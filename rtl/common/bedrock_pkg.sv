`timescale 1ns/1ps
`default_nettype none

package bedrock_pkg;
  localparam int WORD_BITS = 16;
  localparam int PRIMARY_PAYLOAD_BITS = 12;
  localparam int MAX_INSTRUCTION_WORDS = 8;

  localparam int WORD0_PREFIX_BIT = 15;
  localparam int WORD0_LENGTH_MSB = 14;
  localparam int WORD0_LENGTH_LSB = 12;
  localparam int WORD0_PAYLOAD_MSB = 11;
  localparam int WORD0_PAYLOAD_LSB = 0;

  typedef logic [WORD_BITS-1:0] word_t;
  typedef logic [2:0] length_field_t;
  typedef logic [3:0] instruction_length_t;
  typedef logic [PRIMARY_PAYLOAD_BITS-1:0] primary_payload_t;

  function automatic logic word0_prefix_present(input word_t word0);
    word0_prefix_present = word0[WORD0_PREFIX_BIT];
  endfunction

  function automatic length_field_t word0_length_field(input word_t word0);
    word0_length_field = word0[WORD0_LENGTH_MSB:WORD0_LENGTH_LSB];
  endfunction

  function automatic instruction_length_t word0_length_words(input word_t word0);
    word0_length_words = instruction_length_t'(word0_length_field(word0)) + 4'd1;
  endfunction

  function automatic primary_payload_t word0_primary_payload(input word_t word0);
    word0_primary_payload = word0[WORD0_PAYLOAD_MSB:WORD0_PAYLOAD_LSB];
  endfunction
endpackage

`default_nettype wire
