`timescale 1ns/1ps
`default_nettype none

// Generated from isa/spec/prefixes.yaml.
// Do not edit by hand.

package bedrock_prefix_decode_pkg;

@KIND_ENUM@

@UPDATE_ENUM@

@ACCESS_ENUM@

@REPEAT_ENUM@

  typedef struct packed {
    logic valid;
    bedrock_prefix_kind_e kind;
    logic [3:0] condition;
    logic [2:0] counter;
  } bedrock_prefix_byte_decode_t;

  typedef struct packed {
    logic valid;
    bedrock_prefix_byte_decode_t low;
    bedrock_prefix_byte_decode_t high;
    logic nospec;
    logic saturate;
    logic nontemporal;
    bedrock_update_mode_e update_mode;
    bedrock_access_mode_e access_mode;
    bedrock_repeat_kind_e repeat_kind;
    logic [3:0] repeat_condition;
    logic [2:0] repeat_counter;
  } bedrock_prefix_word_decode_t;

  function automatic bedrock_prefix_byte_decode_t bedrock_decode_prefix_byte(input logic [7:0] prefix_byte);
    bedrock_prefix_byte_decode_t r;
    r = '0;
    unique casez (prefix_byte)
@PREFIX_DECODE_CASES@
      default: begin r.kind = BR_PREFIX_INVALID; end
    endcase
    return r;
  endfunction

  function automatic bedrock_prefix_word_decode_t bedrock_apply_prefix_byte(
    input bedrock_prefix_word_decode_t state,
    input bedrock_prefix_byte_decode_t prefix
  );
    bedrock_prefix_word_decode_t r;
    r = state;
    r.valid = r.valid && prefix.valid;
    unique case (prefix.kind)
@PREFIX_APPLY_CASES@
      default: begin
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_prefix_word_decode_t bedrock_decode_prefix_word(input logic [15:0] prefix_word);
    bedrock_prefix_word_decode_t r;
    r = '0;
    r.valid = 1'b1;
    r.low = bedrock_decode_prefix_byte(prefix_word[7:0]);
    r.high = bedrock_decode_prefix_byte(prefix_word[15:8]);
    r = bedrock_apply_prefix_byte(r, r.low);
    r = bedrock_apply_prefix_byte(r, r.high);
    return r;
  endfunction

endpackage

`default_nettype wire
