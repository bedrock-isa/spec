`timescale 1ns/1ps
`default_nettype none

// Package-free generated decoder for synthesis/statistics tools.
// The typed integration wrapper is build/generated/bedrock_decode.sv.

module bedrock_decode_synth(
  input  [11:0] primary_payload_i,
  input  [15:0] extension_word_i,
  output reg        valid_o,
  output reg        needs_extension_o,
  output reg [@OPCODE_ID_MSB@:0] opcode_id_o,
  output reg [@FIELD_FORMAT_ID_MSB@:0] field_format_id_o,
  output reg [3:0]  required_words_o,
  output reg [@EXT_ROOT_MSB@:0] ext_root_o,
  output reg        repcc_allowed_o,
  output reg        repg_allowed_o,
  output reg        repg_fast_candidate_o
);

  localparam [@OPCODE_ID_MSB@:0] BR_OPCODE_INVALID = @OPCODE_BITS@'d0;
@OPCODE_LOCALPARAMS@

  localparam [@FIELD_FORMAT_ID_MSB@:0] BR_FIELD_FORMAT_NONE = @FIELD_FORMAT_BITS@'d0;
@FIELD_FORMAT_LOCALPARAMS@

  localparam [@EXT_ROOT_MSB@:0] BR_EXT_ROOT_NONE = @EXT_ROOT_BITS@'d0;
@EXT_ROOT_LOCALPARAMS@

  reg [3:0] field_format_token_words;

  always @* begin
    valid_o = 1'b0;
    needs_extension_o = 1'b0;
    opcode_id_o = BR_OPCODE_INVALID;
    field_format_id_o = BR_FIELD_FORMAT_NONE;
    required_words_o = 4'd0;
    ext_root_o = BR_EXT_ROOT_NONE;
    field_format_token_words = 4'd1;
    repcc_allowed_o = 1'b0;
    repg_allowed_o = 1'b0;
    repg_fast_candidate_o = 1'b0;

    casez (primary_payload_i)
@PRIMARY_DECODE_CASES@
      default: begin
      end
    endcase

    if (valid_o && required_words_o == 4'd0) begin
      required_words_o = 4'd1;
    end

    if (needs_extension_o) begin
      valid_o = 1'b0;
      opcode_id_o = BR_OPCODE_INVALID;
      field_format_id_o = BR_FIELD_FORMAT_NONE;
      required_words_o = 4'd2;

      case (ext_root_o)
@EXTENDED_DECODE_CASES@
        default: begin
        end
      endcase
    end

    if (valid_o) begin
      case (field_format_id_o)
@FIELD_FORMAT_TOKEN_WORD_CASES@
        default: begin
        end
      endcase
      if (field_format_token_words > required_words_o) begin
        required_words_o = field_format_token_words;
      end
    end
  end
endmodule

`default_nettype wire
