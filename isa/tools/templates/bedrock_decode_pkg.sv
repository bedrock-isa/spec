`timescale 1ns/1ps
`default_nettype none

// Generated from build/generated/allocation_plan.json.
// Do not edit by hand.

package bedrock_decode_pkg;
  import bedrock_pkg::*;

  localparam int BEDROCK_DECODE_OPCODE_COUNT = @OPCODE_COUNT@;
  localparam int BEDROCK_DECODE_OPCODE_ID_BITS = @OPCODE_BITS@;
  localparam int BEDROCK_DECODE_FIELD_FORMAT_COUNT = @FIELD_FORMAT_COUNT@;
  localparam int BEDROCK_DECODE_FIELD_FORMAT_ID_BITS = @FIELD_FORMAT_BITS@;
  localparam int BEDROCK_DECODE_EXT_ROOT_COUNT = @EXT_ROOT_COUNT@;
  localparam int BEDROCK_DECODE_EXT_ROOT_BITS = @EXT_ROOT_BITS@;

  typedef enum logic [BEDROCK_DECODE_OPCODE_ID_BITS-1:0] {
    BR_OPCODE_INVALID = @OPCODE_BITS@'d0,
@OPCODE_ENUM_ENTRIES@
  } bedrock_opcode_id_e;

  typedef enum logic [BEDROCK_DECODE_FIELD_FORMAT_ID_BITS-1:0] {
    BR_FIELD_FORMAT_NONE = @FIELD_FORMAT_BITS@'d0,
@FIELD_FORMAT_ENUM_ENTRIES@
  } bedrock_field_format_id_e;

  typedef enum logic [BEDROCK_DECODE_EXT_ROOT_BITS-1:0] {
    BR_EXT_ROOT_NONE = @EXT_ROOT_BITS@'d0,
@EXT_ROOT_ENUM_ENTRIES@
  } bedrock_ext_root_e;

  typedef struct packed {
    logic [3:0] token_words;
    logic [1:0] ea_present;
    logic [11:0] ea_value;
    word_t ea0_descriptor_word;
  } bedrock_decode_field_extract_t;

  typedef struct packed {
    logic valid;
    logic needs_extension;
    bedrock_opcode_id_e opcode_id;
    bedrock_field_format_id_e field_format_id;
    logic [3:0] required_words;
    bedrock_ext_root_e ext_root;
    logic repcc_allowed;
    logic repg_allowed;
    logic repg_fast_candidate;
  } bedrock_primary_decode_t;

  typedef struct packed {
    logic valid;
    bedrock_opcode_id_e opcode_id;
    bedrock_field_format_id_e field_format_id;
    logic [3:0] required_words;
    logic repcc_allowed;
    logic repg_allowed;
    logic repg_fast_candidate;
  } bedrock_extended_decode_t;

  function automatic bedrock_primary_decode_t bedrock_decode_primary_payload(input primary_payload_t payload);
    bedrock_primary_decode_t r;
    r = '0;
    r.opcode_id = BR_OPCODE_INVALID;
    r.field_format_id = BR_FIELD_FORMAT_NONE;
    r.required_words = 4'd1;
    r.ext_root = BR_EXT_ROOT_NONE;

    priority casez (payload)
@PRIMARY_DECODE_CASES@
      default: begin
      end
    endcase

    return r;
  endfunction

  function automatic bedrock_extended_decode_t bedrock_decode_extended_opcode(
    input bedrock_ext_root_e ext_root,
    input logic [15:0] extension_word
  );
    bedrock_extended_decode_t r;
    r = '0;
    r.opcode_id = BR_OPCODE_INVALID;
    r.field_format_id = BR_FIELD_FORMAT_NONE;
    r.required_words = 4'd2;

    unique case (ext_root)
@EXTENDED_DECODE_CASES@
      default: begin
      end
    endcase

    return r;
  endfunction

  function automatic logic [3:0] bedrock_decode_field_format_token_words(
    input bedrock_field_format_id_e field_format_id
  );
    logic [3:0] r;
    r = 4'd1;
    unique case (field_format_id)
@FIELD_FORMAT_TOKEN_WORD_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_decode_field_extract_t bedrock_decode_extract_fields(
    input bedrock_field_format_id_e field_format_id,
    input word_t token0_word,
    input word_t token1_word,
    input word_t token2_word,
    input word_t token3_word,
    input word_t token4_word,
    input word_t token5_word,
    input word_t token6_word,
    input word_t token7_word
  );
    bedrock_decode_field_extract_t r;
    r = '0;
    r.token_words = 4'd1;
    r.ea0_descriptor_word = word_t'(16'h0000);
    unique case (field_format_id)
@FIELD_FORMAT_EXTRACT_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic word_t bedrock_decode_ea1_descriptor_word(
    input bedrock_field_format_id_e field_format_id,
    input logic [2:0] ea0_payload_words,
    input word_t token0_word,
    input word_t token1_word,
    input word_t token2_word,
    input word_t token3_word,
    input word_t token4_word,
    input word_t token5_word,
    input word_t token6_word,
    input word_t token7_word
  );
    word_t r;
    r = word_t'(16'h0000);
    unique case (field_format_id)
@FIELD_FORMAT_EA1_DESCRIPTOR_WORD_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

endpackage

`default_nettype wire
