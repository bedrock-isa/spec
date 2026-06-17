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
  output logic              alias_o,
  output bedrock_form_id_e  form_id_o,
  output bedrock_ext_root_e ext_root_o,
  output logic              repcc_allowed_o,
  output logic              repg_allowed_o,
  output logic              repg_fast_candidate_o
);

  bedrock_primary_decode_t primary_decode;
  bedrock_extended_decode_t extended_decode;
  bedrock_form_attributes_t attributes;

  always_comb begin
    primary_decode = bedrock_decode_primary_payload(primary_payload_i);
    extended_decode = '0;
    extended_decode.form_id = BR_FORM_INVALID;
    attributes = '0;

    valid_o = primary_decode.valid;
    needs_extension_o = primary_decode.needs_extension;
    alias_o = primary_decode.is_alias;
    form_id_o = primary_decode.form_id;
    ext_root_o = primary_decode.ext_root;

    if (primary_decode.needs_extension) begin
      extended_decode = bedrock_decode_extended_opcode(primary_decode.ext_root, extension_word_i);
      valid_o = extended_decode.valid;
      alias_o = extended_decode.is_alias;
      form_id_o = extended_decode.form_id;
    end

    attributes = bedrock_decode_form_attributes(form_id_o);
    repcc_allowed_o = valid_o && attributes.repcc_allowed;
    repg_allowed_o = valid_o && attributes.repg_allowed;
    repg_fast_candidate_o = valid_o && attributes.repg_fast_candidate;
  end
endmodule

`default_nettype wire
