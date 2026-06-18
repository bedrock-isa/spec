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
  localparam int BEDROCK_DECODE_FIELD_SLOTS = @FIELD_SLOTS@;
  localparam int BEDROCK_DECODE_FIELD_KIND_BITS = @FIELD_KIND_BITS@;

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

  typedef enum logic [BEDROCK_DECODE_FIELD_KIND_BITS-1:0] {
@FIELD_KIND_ENUM_ENTRIES@
  } bedrock_decode_field_kind_e;

  typedef struct packed {
    logic valid;
    bedrock_decode_field_kind_e kind;
    logic [1:0] token;
    logic [3:0] low_bit;
    logic [4:0] width;
  } bedrock_decode_field_meta_t;

  typedef struct packed {
    logic valid;
    logic needs_extension;
    bedrock_opcode_id_e opcode_id;
    bedrock_field_format_id_e field_format_id;
    logic [3:0] required_words;
    bedrock_ext_root_e ext_root;
  } bedrock_primary_decode_t;

  typedef struct packed {
    logic valid;
    bedrock_opcode_id_e opcode_id;
    bedrock_field_format_id_e field_format_id;
    logic [3:0] required_words;
  } bedrock_extended_decode_t;

  typedef struct packed {
    logic repcc_allowed;
    logic repg_allowed;
    logic repg_fast_candidate;
  } bedrock_opcode_attributes_t;

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

  function automatic bedrock_decode_field_meta_t bedrock_decode_field_format_field(
    input bedrock_field_format_id_e field_format_id,
    input logic [2:0] field_index
  );
    bedrock_decode_field_meta_t r;
    r = '0;
    r.kind = BR_FIELD_NONE;
    unique case (field_format_id)
@FIELD_FORMAT_FIELD_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_opcode_attributes_t bedrock_decode_opcode_attributes(input bedrock_opcode_id_e opcode_id);
    bedrock_opcode_attributes_t r;
    r = '0;
    unique case (opcode_id)
@OPCODE_ATTRIBUTE_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

endpackage

`default_nettype wire
