`timescale 1ns/1ps
`default_nettype none

package bedrock_agu_pkg;
  import bedrock_prefix_decode_pkg::*;
  import bedrock_ea_decode_pkg::*;

  localparam int BEDROCK_AGU_REQUEST_SLOTS = 2;

  typedef struct packed {
    logic valid;
    logic present;
    logic raw_valid;
    logic reserved;
    logic is_register;
    logic is_memory;
    logic is_immediate;
    logic needs_descriptor;
    logic signed32_index_escape;
    logic segment_selectable;
    logic segment_valid;
    logic update_eligible;
    logic update_requested;
    logic update_valid;
    logic update_invalid;
    logic has_base_reg;
    logic has_index_reg;
    logic has_displacement;
    logic has_absolute;
    logic [5:0] raw_ea;
    logic [3:0] descriptor_token;
    logic [3:0] payload_base_token;
    logic [2:0] payload_words;
    logic [2:0] displacement_words;
    bedrock_update_mode_e update_mode;
    bedrock_ea_form_e form;
    bedrock_ea_segment_e segment;
    bedrock_ea_base_e base;
    logic [2:0] base_reg;
    logic [2:0] index_reg;
    logic [1:0] scale_log2;
  } bedrock_agu_request_t;
endpackage

`default_nettype wire
