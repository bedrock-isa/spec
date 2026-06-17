`timescale 1ns/1ps
`default_nettype none

// Generated from build/generated/allocation_plan.json.
// Do not edit by hand.

package bedrock_decode_pkg;
  import bedrock_pkg::*;

  localparam int BEDROCK_DECODE_FORM_COUNT = @FORM_COUNT@;
  localparam int BEDROCK_DECODE_FORM_ID_BITS = @FORM_BITS@;
  localparam int BEDROCK_DECODE_EXT_ROOT_COUNT = @EXT_ROOT_COUNT@;
  localparam int BEDROCK_DECODE_EXT_ROOT_BITS = @EXT_ROOT_BITS@;
  localparam int BEDROCK_DECODE_FIELD_SLOTS = @FIELD_SLOTS@;
  localparam int BEDROCK_DECODE_FIELD_KIND_BITS = @FIELD_KIND_BITS@;
  localparam int BEDROCK_DECODE_FIELD_SOURCE_BITS = @FIELD_SOURCE_BITS@;

  typedef enum logic [BEDROCK_DECODE_FORM_ID_BITS-1:0] {
    BR_FORM_INVALID = @FORM_BITS@'d0,
@FORM_ENUM_ENTRIES@
  } bedrock_form_id_e;

  typedef enum logic [BEDROCK_DECODE_EXT_ROOT_BITS-1:0] {
    BR_EXT_ROOT_NONE = @EXT_ROOT_BITS@'d0,
@EXT_ROOT_ENUM_ENTRIES@
  } bedrock_ext_root_e;

  typedef enum logic [BEDROCK_DECODE_FIELD_KIND_BITS-1:0] {
@FIELD_KIND_ENUM_ENTRIES@
  } bedrock_decode_field_kind_e;

  typedef enum logic [BEDROCK_DECODE_FIELD_SOURCE_BITS-1:0] {
@FIELD_SOURCE_ENUM_ENTRIES@
  } bedrock_decode_field_source_e;

  typedef struct packed {
    logic valid;
    bedrock_decode_field_kind_e kind;
    bedrock_decode_field_source_e source;
    logic [1:0] token;
    logic [3:0] low_bit;
    logic [4:0] width;
  } bedrock_decode_field_meta_t;

  typedef struct packed {
    logic valid;
    logic needs_extension;
    logic is_alias;
    bedrock_form_id_e form_id;
    bedrock_ext_root_e ext_root;
  } bedrock_primary_decode_t;

  typedef struct packed {
    logic valid;
    logic is_alias;
    bedrock_form_id_e form_id;
  } bedrock_extended_decode_t;

  typedef struct packed {
    logic repcc_allowed;
    logic repg_allowed;
    logic repg_fast_candidate;
  } bedrock_form_attributes_t;

  function automatic bedrock_primary_decode_t bedrock_decode_primary_payload(input primary_payload_t payload);
    bedrock_primary_decode_t r;
    r = '0;
    r.form_id = BR_FORM_INVALID;
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
    r.form_id = BR_FORM_INVALID;

    unique case (ext_root)
@EXTENDED_DECODE_CASES@
      default: begin
      end
    endcase

    return r;
  endfunction

  function automatic logic [3:0] bedrock_decode_form_required_words(input bedrock_form_id_e form_id);
    logic [3:0] r;
    r = 4'd1;
    unique case (form_id)
@REQUIRED_WORD_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic logic [3:0] bedrock_decode_form_field_token_words(input bedrock_form_id_e form_id);
    logic [3:0] r;
    r = 4'd1;
    unique case (form_id)
@FIELD_TOKEN_WORD_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_decode_field_meta_t bedrock_decode_form_field(
    input bedrock_form_id_e form_id,
    input logic [2:0] field_index
  );
    bedrock_decode_field_meta_t r;
    r = '0;
    r.kind = BR_FIELD_NONE;
    r.source = BR_SOURCE_NONE;
    unique case (form_id)
@FORM_FIELD_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_form_attributes_t bedrock_decode_form_attributes(input bedrock_form_id_e form_id);
    bedrock_form_attributes_t r;
    r = '0;
    unique case (form_id)
@FORM_ATTRIBUTE_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

endpackage

`default_nettype wire
