`timescale 1ns/1ps
`default_nettype none

// Generated from isa/spec/ea.yaml.
// Do not edit by hand.

package bedrock_ea_decode_pkg;

@EA_FORM_ENUM@

@EA_BASE_ENUM@

@EA_SEGMENT_ENUM@

  typedef struct packed {
    logic valid;
    logic reserved;
    logic needs_descriptor;
    logic signed32_index_escape;
    bedrock_ea_form_e form;
    logic is_register;
    logic is_memory;
    logic is_immediate;
    logic update_eligible;
    logic segment_selectable;
    logic segment_valid;
    bedrock_ea_segment_e segment;
    bedrock_ea_base_e base;
    logic has_base_reg;
    logic has_index_reg;
    logic [2:0] base_reg;
    logic [2:0] index_reg;
    logic [1:0] scale_log2;
    logic has_displacement;
    logic has_absolute;
    logic [2:0] displacement_words;
    logic [2:0] payload_words;
  } bedrock_ea_decode_t;

  function automatic bedrock_ea_segment_e bedrock_ea_segment_decode(input logic [2:0] segment);
    unique case (segment)
@EA_SEGMENT_DECODE_CASES@
    endcase
  endfunction

  function automatic bedrock_ea_decode_t bedrock_decode_compact_ea(input logic [5:0] ea);
    bedrock_ea_decode_t r;
    r = '0;
    r.segment_valid = 1'b1;
    unique casez (ea)
@COMPACT_EA_CASES@
@RESERVED_COMPACT_EA_CASES@
      default: begin
        r.reserved = 1'b1;
      end
    endcase
    return r;
  endfunction

  function automatic bedrock_ea_decode_t bedrock_decode_extended_ea(
    input logic signed32_index_escape,
    input logic [15:0] descriptor
  );
    bedrock_ea_decode_t r;
    logic [4:0] mode;
    logic [2:0] segment;
    logic [7:0] extra;
    r = '0;
    r.signed32_index_escape = signed32_index_escape;
    mode = descriptor[15:11];
    segment = descriptor[10:8];
    extra = descriptor[7:0];
    r.segment = bedrock_ea_segment_decode(segment);
    r.segment_valid = 1'b1;
    unique case (mode)
@EXTENDED_EA_CASES@
      default: begin
        r.reserved = 1'b1;
      end
    endcase
    r.valid = r.valid && r.segment_valid;
    return r;
  endfunction

  function automatic bedrock_ea_decode_t bedrock_decode_ea(input logic [5:0] ea, input logic [15:0] descriptor);
    bedrock_ea_decode_t compact;
    compact = bedrock_decode_compact_ea(ea);
    if (compact.needs_descriptor) begin
      return bedrock_decode_extended_ea(compact.signed32_index_escape, descriptor);
    end
    return compact;
  endfunction

endpackage

`default_nettype wire
