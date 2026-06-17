`timescale 1ns/1ps
`default_nettype none

// Package-free generated decoder for synthesis/statistics tools.
// The typed integration wrapper is build/generated/bedrock_decode.sv.

module bedrock_decode_synth(
  input  [11:0] primary_payload_i,
  input  [15:0] extension_word_i,
  output reg        valid_o,
  output reg        needs_extension_o,
  output reg        alias_o,
  output reg [@FORM_ID_MSB@:0] form_id_o,
  output reg [@EXT_ROOT_MSB@:0] ext_root_o,
  output reg        repcc_allowed_o,
  output reg        repg_allowed_o,
  output reg        repg_fast_candidate_o
);

  localparam [@FORM_ID_MSB@:0] BR_FORM_INVALID = @FORM_BITS@'d0;
@FORM_LOCALPARAMS@

  localparam [@EXT_ROOT_MSB@:0] BR_EXT_ROOT_NONE = @EXT_ROOT_BITS@'d0;
@EXT_ROOT_LOCALPARAMS@

  always @* begin
    valid_o = 1'b0;
    needs_extension_o = 1'b0;
    alias_o = 1'b0;
    form_id_o = BR_FORM_INVALID;
    ext_root_o = BR_EXT_ROOT_NONE;
    repcc_allowed_o = 1'b0;
    repg_allowed_o = 1'b0;
    repg_fast_candidate_o = 1'b0;

    casez (primary_payload_i)
@PRIMARY_DECODE_CASES@
      default: begin
      end
    endcase

    if (needs_extension_o) begin
      valid_o = 1'b0;
      alias_o = 1'b0;
      form_id_o = BR_FORM_INVALID;

      case (ext_root_o)
@EXTENDED_DECODE_CASES@
        default: begin
        end
      endcase
    end

    if (valid_o) begin
      case (form_id_o)
@ATTRIBUTE_CASES@
        default: begin
        end
      endcase
    end
  end
endmodule

`default_nettype wire
