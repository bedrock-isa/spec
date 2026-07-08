`timescale 1ns/1ps
`default_nettype none

// Generated decode wrapper. The input extension_word_i is the first
// opcode/descriptor word after word 0 and after any prefix word.

module bedrock_decode
  import bedrock_pkg::*;
  import bedrock_decode_pkg::*;
(
  input  primary_payload_t  primary_payload_i,
  input  logic [15:0]       extension_word_i,
  output logic              valid_o,
  output logic              needs_extension_o,
  output bedrock_opcode_id_e opcode_id_o,
  output bedrock_field_format_id_e field_format_id_o,
  output logic [3:0]        required_words_o,
  output bedrock_ext_root_e ext_root_o,
  output logic              repg_fast_candidate_o
);

  bedrock_primary_decode_t primary_decode;
  bedrock_extended_decode_t extended_decode;
  logic [3:0] field_format_token_words;
  logic repg_fast_candidate;

  always_comb begin
    primary_decode = bedrock_decode_primary_payload(primary_payload_i);
    extended_decode = '0;
    extended_decode.opcode_id = BR_OPCODE_INVALID;
    extended_decode.field_format_id = BR_FIELD_FORMAT_NONE;
    field_format_token_words = 4'd1;

    valid_o = primary_decode.valid;
    needs_extension_o = primary_decode.needs_extension;
    opcode_id_o = primary_decode.opcode_id;
    field_format_id_o = primary_decode.field_format_id;
    required_words_o = primary_decode.required_words;
    ext_root_o = primary_decode.ext_root;
    repg_fast_candidate = primary_decode.repg_fast_candidate;

    if (primary_decode.needs_extension) begin
      extended_decode = bedrock_decode_extended_opcode(primary_decode.ext_root, extension_word_i);
      valid_o = extended_decode.valid;
      opcode_id_o = extended_decode.opcode_id;
      field_format_id_o = extended_decode.field_format_id;
      required_words_o = extended_decode.required_words;
      repg_fast_candidate = extended_decode.repg_fast_candidate;
    end

    if (valid_o) begin
      field_format_token_words = bedrock_decode_field_format_token_words(field_format_id_o);
      if (field_format_token_words > required_words_o) begin
        required_words_o = field_format_token_words;
      end
    end
    repg_fast_candidate_o = valid_o && repg_fast_candidate;
  end
endmodule

`default_nettype wire
