`timescale 1ns/1ps
`default_nettype none

// Generated from isa/spec/prefixes.yaml.
// Do not edit by hand.

package bedrock_prefix_decode_pkg;

  typedef enum logic [3:0] {
    BR_PREFIX_INVALID = 4'd0,
    BR_PREFIX_NPX = 4'd1, // NPX
    BR_PREFIX_NOSPEC = 4'd2, // NOSPEC
    BR_PREFIX_SATURATE = 4'd3, // SATURATE
    BR_PREFIX_NONTEMPORAL = 4'd4, // NONTEMPORAL
    BR_PREFIX_POSTINC = 4'd5, // POSTINC
    BR_PREFIX_PREINC = 4'd6, // PREINC
    BR_PREFIX_POSTDEC = 4'd7, // POSTDEC
    BR_PREFIX_PREDEC = 4'd8, // PREDEC
    BR_PREFIX_U2C = 4'd9, // U2C
    BR_PREFIX_C2U = 4'd10, // C2U
    BR_PREFIX_U2U = 4'd11, // U2U
    BR_PREFIX_REPCC = 4'd12 // REPcc
  } bedrock_prefix_kind_e;

  typedef enum logic [2:0] {
    BR_UPDATE_NONE = 3'd0,
    BR_UPDATE_POSTINC = 3'd1,
    BR_UPDATE_PREINC = 3'd2,
    BR_UPDATE_POSTDEC = 3'd3,
    BR_UPDATE_PREDEC = 3'd4
  } bedrock_update_mode_e;

  typedef enum logic [1:0] {
    BR_ACCESS_C = 2'd0,
    BR_ACCESS_U2C = 2'd1,
    BR_ACCESS_C2U = 2'd2,
    BR_ACCESS_U2U = 2'd3
  } bedrock_access_mode_e;

  typedef enum logic [0:0] {
    BR_REPEAT_NONE = 1'd0,
    BR_REPEAT_REPCC = 1'd1
  } bedrock_repeat_kind_e;

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
      8'h00: begin r.valid = 1'b1; r.kind = BR_PREFIX_NPX; end
      8'h01: begin r.valid = 1'b1; r.kind = BR_PREFIX_NOSPEC; end
      8'h02: begin r.valid = 1'b1; r.kind = BR_PREFIX_SATURATE; end
      8'h03: begin r.valid = 1'b1; r.kind = BR_PREFIX_NONTEMPORAL; end
      8'h04: begin r.valid = 1'b1; r.kind = BR_PREFIX_POSTINC; end
      8'h05: begin r.valid = 1'b1; r.kind = BR_PREFIX_PREINC; end
      8'h06: begin r.valid = 1'b1; r.kind = BR_PREFIX_POSTDEC; end
      8'h07: begin r.valid = 1'b1; r.kind = BR_PREFIX_PREDEC; end
      8'h08: begin r.valid = 1'b1; r.kind = BR_PREFIX_U2C; end
      8'h09: begin r.valid = 1'b1; r.kind = BR_PREFIX_C2U; end
      8'h0a: begin r.valid = 1'b1; r.kind = BR_PREFIX_U2U; end
      8'b1???_????: begin r.valid = 1'b1; r.kind = BR_PREFIX_REPCC; r.condition = prefix_byte[6:3]; r.counter = prefix_byte[2:0]; end
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
      BR_PREFIX_NPX: begin end
      BR_PREFIX_NOSPEC: r.nospec = 1'b1;
      BR_PREFIX_SATURATE: r.saturate = 1'b1;
      BR_PREFIX_NONTEMPORAL: r.nontemporal = 1'b1;
      BR_PREFIX_POSTINC: r.update_mode = BR_UPDATE_POSTINC;
      BR_PREFIX_PREINC: r.update_mode = BR_UPDATE_PREINC;
      BR_PREFIX_POSTDEC: r.update_mode = BR_UPDATE_POSTDEC;
      BR_PREFIX_PREDEC: r.update_mode = BR_UPDATE_PREDEC;
      BR_PREFIX_U2C: r.access_mode = BR_ACCESS_U2C;
      BR_PREFIX_C2U: r.access_mode = BR_ACCESS_C2U;
      BR_PREFIX_U2U: r.access_mode = BR_ACCESS_U2U;
      BR_PREFIX_REPCC: begin r.repeat_kind = BR_REPEAT_REPCC; r.repeat_condition = prefix.condition; r.repeat_counter = prefix.counter; end
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
