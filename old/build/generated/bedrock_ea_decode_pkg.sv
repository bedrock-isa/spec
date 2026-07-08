`timescale 1ns/1ps
`default_nettype none

// Generated from isa/spec/ea.yaml.
// Do not edit by hand.

package bedrock_ea_decode_pkg;

  typedef enum logic [5:0] {
    BR_EA_INVALID = 6'd0,
    BR_EA_DREG = 6'd1, // DREG
    BR_EA_AREG = 6'd2, // AREG
    BR_EA_INDIRECT = 6'd3, // INDIRECT
    BR_EA_A_DISP16 = 6'd4, // A_DISP16
    BR_EA_A_DISP32 = 6'd5, // A_DISP32
    BR_EA_PC_DISP16 = 6'd6, // PC_DISP16
    BR_EA_PC_DISP32 = 6'd7, // PC_DISP32
    BR_EA_PC_DISP64 = 6'd8, // PC_DISP64
    BR_EA_SP_DISP16 = 6'd9, // SP_DISP16
    BR_EA_SP_DISP32 = 6'd10, // SP_DISP32
    BR_EA_SP_DISP64 = 6'd11, // SP_DISP64
    BR_EA_SPREG = 6'd12, // SPREG
    BR_EA_ABS32 = 6'd13, // ABS32
    BR_EA_ABS64 = 6'd14, // ABS64
    BR_EA_IMM16 = 6'd15, // IMM16
    BR_EA_IMM32 = 6'd16, // IMM32
    BR_EA_IMM64 = 6'd17, // IMM64
    BR_EA_S32_INDEXED_EXTENDED = 6'd18, // S32_INDEXED_EXTENDED
    BR_EA_EXTENDED = 6'd19, // EXTENDED
    BR_EA_SEG_A_INDEX = 6'd20, // SEG_A_INDEX
    BR_EA_SEG_A_INDEX_DISP16 = 6'd21, // SEG_A_INDEX_DISP16
    BR_EA_SEG_A_INDEX_DISP32 = 6'd22, // SEG_A_INDEX_DISP32
    BR_EA_SEG_A_INDEX_DISP64 = 6'd23, // SEG_A_INDEX_DISP64
    BR_EA_SEG_A = 6'd24, // SEG_A
    BR_EA_SEG_A_DISP16 = 6'd25, // SEG_A_DISP16
    BR_EA_SEG_A_DISP32 = 6'd26, // SEG_A_DISP32
    BR_EA_SEG_ABS32 = 6'd27, // SEG_ABS32
    BR_EA_SEG_ABS64 = 6'd28, // SEG_ABS64
    BR_EA_SP_INDEX_DISP16 = 6'd29, // SP_INDEX_DISP16
    BR_EA_SP_INDEX_DISP32 = 6'd30, // SP_INDEX_DISP32
    BR_EA_SP_INDEX_DISP64 = 6'd31, // SP_INDEX_DISP64
    BR_EA_PC_INDEX_DISP16 = 6'd32, // PC_INDEX_DISP16
    BR_EA_PC_INDEX_DISP32 = 6'd33, // PC_INDEX_DISP32
    BR_EA_PC_INDEX_DISP64 = 6'd34, // PC_INDEX_DISP64
    BR_EA_S32_SEG_A_INDEX = 6'd35, // S32_SEG_A_INDEX
    BR_EA_S32_SEG_A_INDEX_DISP16 = 6'd36, // S32_SEG_A_INDEX_DISP16
    BR_EA_S32_SEG_A_INDEX_DISP32 = 6'd37, // S32_SEG_A_INDEX_DISP32
    BR_EA_S32_SEG_A_INDEX_DISP64 = 6'd38, // S32_SEG_A_INDEX_DISP64
    BR_EA_S32_SP_INDEX_DISP16 = 6'd39, // S32_SP_INDEX_DISP16
    BR_EA_S32_SP_INDEX_DISP32 = 6'd40, // S32_SP_INDEX_DISP32
    BR_EA_S32_SP_INDEX_DISP64 = 6'd41, // S32_SP_INDEX_DISP64
    BR_EA_S32_PC_INDEX_DISP16 = 6'd42, // S32_PC_INDEX_DISP16
    BR_EA_S32_PC_INDEX_DISP32 = 6'd43, // S32_PC_INDEX_DISP32
    BR_EA_S32_PC_INDEX_DISP64 = 6'd44 // S32_PC_INDEX_DISP64
  } bedrock_ea_form_e;

  typedef enum logic [2:0] {
    BR_EA_BASE_NONE = 3'd0,
    BR_EA_BASE_D = 3'd1,
    BR_EA_BASE_A = 3'd2,
    BR_EA_BASE_PC = 3'd3,
    BR_EA_BASE_SP = 3'd4,
    BR_EA_BASE_ABS = 3'd5,
    BR_EA_BASE_IMM = 3'd6
  } bedrock_ea_base_e;

  typedef enum logic [2:0] {
    BR_EA_SEG_CS = 3'd0,
    BR_EA_SEG_DS = 3'd1,
    BR_EA_SEG_GS0 = 3'd2,
    BR_EA_SEG_GS1 = 3'd3,
    BR_EA_SEG_GS2 = 3'd4,
    BR_EA_SEG_GS3 = 3'd5,
    BR_EA_SEG_GS4 = 3'd6,
    BR_EA_SEG_SS = 3'd7
  } bedrock_ea_segment_e;

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
      3'd0: bedrock_ea_segment_decode = BR_EA_SEG_CS;
      3'd1: bedrock_ea_segment_decode = BR_EA_SEG_DS;
      3'd3: bedrock_ea_segment_decode = BR_EA_SEG_GS0;
      3'd4: bedrock_ea_segment_decode = BR_EA_SEG_GS1;
      3'd5: bedrock_ea_segment_decode = BR_EA_SEG_GS2;
      3'd6: bedrock_ea_segment_decode = BR_EA_SEG_GS3;
      3'd7: bedrock_ea_segment_decode = BR_EA_SEG_GS4;
      3'd2: bedrock_ea_segment_decode = BR_EA_SEG_SS;
      default: bedrock_ea_segment_decode = BR_EA_SEG_SS;
    endcase
  endfunction

  function automatic bedrock_ea_decode_t bedrock_decode_compact_ea(input logic [5:0] ea);
    bedrock_ea_decode_t r;
    r = '0;
    r.segment_valid = 1'b1;
    unique casez (ea)
      6'b000?_??: begin // DREG
        r.valid = 1'b1;
        r.form = BR_EA_DREG;
        r.is_register = 1'b1;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_D;
        r.has_base_reg = 1'b1;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd0;
        r.payload_words = 3'd0;
        r.base_reg = ea[2:0];
      end
      6'b001?_??: begin // AREG
        r.valid = 1'b1;
        r.form = BR_EA_AREG;
        r.is_register = 1'b1;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_A;
        r.has_base_reg = 1'b1;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd0;
        r.payload_words = 3'd0;
        r.base_reg = ea[2:0];
      end
      6'b010?_??: begin // INDIRECT
        r.valid = 1'b1;
        r.form = BR_EA_INDIRECT;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b1;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_A;
        r.has_base_reg = 1'b1;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd0;
        r.payload_words = 3'd0;
        r.base_reg = ea[2:0];
      end
      6'b011?_??: begin // A_DISP16
        r.valid = 1'b1;
        r.form = BR_EA_A_DISP16;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_A;
        r.has_base_reg = 1'b1;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd1;
        r.payload_words = 3'd1;
        r.base_reg = ea[2:0];
      end
      6'b100?_??: begin // A_DISP32
        r.valid = 1'b1;
        r.form = BR_EA_A_DISP32;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_A;
        r.has_base_reg = 1'b1;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd2;
        r.payload_words = 3'd2;
        r.base_reg = ea[2:0];
      end
      6'b1010_00: begin // PC_DISP16
        r.valid = 1'b1;
        r.form = BR_EA_PC_DISP16;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_CS;
        r.base = BR_EA_BASE_PC;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd1;
        r.payload_words = 3'd1;
      end
      6'b1010_01: begin // PC_DISP32
        r.valid = 1'b1;
        r.form = BR_EA_PC_DISP32;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_CS;
        r.base = BR_EA_BASE_PC;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd2;
        r.payload_words = 3'd2;
      end
      6'b1010_10: begin // PC_DISP64
        r.valid = 1'b1;
        r.form = BR_EA_PC_DISP64;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_CS;
        r.base = BR_EA_BASE_PC;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd4;
        r.payload_words = 3'd4;
      end
      6'b1011_00: begin // SP_DISP16
        r.valid = 1'b1;
        r.form = BR_EA_SP_DISP16;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_SS;
        r.base = BR_EA_BASE_SP;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd1;
        r.payload_words = 3'd1;
      end
      6'b1011_01: begin // SP_DISP32
        r.valid = 1'b1;
        r.form = BR_EA_SP_DISP32;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_SS;
        r.base = BR_EA_BASE_SP;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd2;
        r.payload_words = 3'd2;
      end
      6'b1011_10: begin // SP_DISP64
        r.valid = 1'b1;
        r.form = BR_EA_SP_DISP64;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_SS;
        r.base = BR_EA_BASE_SP;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b1;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd4;
        r.payload_words = 3'd4;
      end
      6'b1011_11: begin // SPREG
        r.valid = 1'b1;
        r.form = BR_EA_SPREG;
        r.is_register = 1'b1;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_SP;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd0;
        r.payload_words = 3'd0;
      end
      6'b1100_00: begin // ABS32
        r.valid = 1'b1;
        r.form = BR_EA_ABS32;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_ABS;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b1;
        r.displacement_words = 3'd2;
        r.payload_words = 3'd2;
      end
      6'b1100_01: begin // ABS64
        r.valid = 1'b1;
        r.form = BR_EA_ABS64;
        r.is_register = 1'b0;
        r.is_memory = 1'b1;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_ABS;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b1;
        r.displacement_words = 3'd4;
        r.payload_words = 3'd4;
      end
      6'b1100_10: begin // IMM16
        r.valid = 1'b1;
        r.form = BR_EA_IMM16;
        r.is_register = 1'b0;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b1;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_IMM;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd1;
        r.payload_words = 3'd1;
      end
      6'b1100_11: begin // IMM32
        r.valid = 1'b1;
        r.form = BR_EA_IMM32;
        r.is_register = 1'b0;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b1;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_IMM;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd2;
        r.payload_words = 3'd2;
      end
      6'b1101_00: begin // IMM64
        r.valid = 1'b1;
        r.form = BR_EA_IMM64;
        r.is_register = 1'b0;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b1;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_IMM;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd4;
        r.payload_words = 3'd4;
      end
      6'b1111_10: begin // S32_INDEXED_EXTENDED
        r.valid = 1'b1;
        r.form = BR_EA_S32_INDEXED_EXTENDED;
        r.is_register = 1'b0;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_NONE;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd0;
        r.payload_words = 3'd0;
        r.needs_descriptor = 1'b1;
        r.signed32_index_escape = 1'b1;
        r.payload_words = 3'd1;
      end
      6'b1111_11: begin // EXTENDED
        r.valid = 1'b1;
        r.form = BR_EA_EXTENDED;
        r.is_register = 1'b0;
        r.is_memory = 1'b0;
        r.is_immediate = 1'b0;
        r.update_eligible = 1'b0;
        r.segment_selectable = 1'b0;
        r.segment = BR_EA_SEG_DS;
        r.base = BR_EA_BASE_NONE;
        r.has_base_reg = 1'b0;
        r.has_index_reg = 1'b0;
        r.has_displacement = 1'b0;
        r.has_absolute = 1'b0;
        r.displacement_words = 3'd0;
        r.payload_words = 3'd0;
        r.needs_descriptor = 1'b1;
        r.payload_words = 3'd1;
      end

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
      5'h00: begin
        if (!signed32_index_escape) begin // SEG_A_INDEX
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A_INDEX;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b0;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd0;
          r.payload_words = 3'd1;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else if (signed32_index_escape) begin // S32_SEG_A_INDEX
          r.valid = 1'b1;
          r.form = BR_EA_S32_SEG_A_INDEX;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b0;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd0;
          r.payload_words = 3'd1;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h01: begin
        if (!signed32_index_escape) begin // SEG_A_INDEX_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A_INDEX_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else if (signed32_index_escape) begin // S32_SEG_A_INDEX_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_S32_SEG_A_INDEX_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h02: begin
        if (!signed32_index_escape) begin // SEG_A_INDEX_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A_INDEX_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else if (signed32_index_escape) begin // S32_SEG_A_INDEX_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_S32_SEG_A_INDEX_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h03: begin
        if (!signed32_index_escape) begin // SEG_A_INDEX_DISP64
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A_INDEX_DISP64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else if (signed32_index_escape) begin // S32_SEG_A_INDEX_DISP64
          r.valid = 1'b1;
          r.form = BR_EA_S32_SEG_A_INDEX_DISP64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.base_reg = extra[7:5];
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h04: begin
        if (!signed32_index_escape) begin // SEG_A
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b1;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b0;
          r.has_displacement = 1'b0;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd0;
          r.payload_words = 3'd1;
          r.base_reg = extra[7:5];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h05: begin
        if (!signed32_index_escape) begin // SEG_A_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b0;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.base_reg = extra[7:5];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h06: begin
        if (!signed32_index_escape) begin // SEG_A_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_SEG_A_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_A;
          r.has_base_reg = 1'b1;
          r.has_index_reg = 1'b0;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.base_reg = extra[7:5];
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h07: begin
        if (!signed32_index_escape) begin // SEG_ABS32
          r.valid = 1'b1;
          r.form = BR_EA_SEG_ABS32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_ABS;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b0;
          r.has_displacement = 1'b0;
          r.has_absolute = 1'b1;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h08: begin
        if (!signed32_index_escape) begin // SEG_ABS64
          r.valid = 1'b1;
          r.form = BR_EA_SEG_ABS64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b1;
          r.segment = BR_EA_SEG_DS;
          r.base = BR_EA_BASE_ABS;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b0;
          r.has_displacement = 1'b0;
          r.has_absolute = 1'b1;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.segment = bedrock_ea_segment_decode(segment);
          r.segment_valid = 1'b1;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h09: begin
        if (!signed32_index_escape) begin // SP_INDEX_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_SP_INDEX_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_SS;
          r.base = BR_EA_BASE_SP;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_SS;
        end
        else if (signed32_index_escape) begin // S32_SP_INDEX_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_S32_SP_INDEX_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_SS;
          r.base = BR_EA_BASE_SP;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_SS;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h0a: begin
        if (!signed32_index_escape) begin // SP_INDEX_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_SP_INDEX_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_SS;
          r.base = BR_EA_BASE_SP;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_SS;
        end
        else if (signed32_index_escape) begin // S32_SP_INDEX_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_S32_SP_INDEX_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_SS;
          r.base = BR_EA_BASE_SP;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_SS;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h0b: begin
        if (!signed32_index_escape) begin // SP_INDEX_DISP64
          r.valid = 1'b1;
          r.form = BR_EA_SP_INDEX_DISP64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_SS;
          r.base = BR_EA_BASE_SP;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_SS;
        end
        else if (signed32_index_escape) begin // S32_SP_INDEX_DISP64
          r.valid = 1'b1;
          r.form = BR_EA_S32_SP_INDEX_DISP64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_SS;
          r.base = BR_EA_BASE_SP;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_SS;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h0c: begin
        if (!signed32_index_escape) begin // PC_INDEX_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_PC_INDEX_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_CS;
          r.base = BR_EA_BASE_PC;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_CS;
        end
        else if (signed32_index_escape) begin // S32_PC_INDEX_DISP16
          r.valid = 1'b1;
          r.form = BR_EA_S32_PC_INDEX_DISP16;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_CS;
          r.base = BR_EA_BASE_PC;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd1;
          r.payload_words = 3'd2;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_CS;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h0d: begin
        if (!signed32_index_escape) begin // PC_INDEX_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_PC_INDEX_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_CS;
          r.base = BR_EA_BASE_PC;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_CS;
        end
        else if (signed32_index_escape) begin // S32_PC_INDEX_DISP32
          r.valid = 1'b1;
          r.form = BR_EA_S32_PC_INDEX_DISP32;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_CS;
          r.base = BR_EA_BASE_PC;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd2;
          r.payload_words = 3'd3;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_CS;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
      5'h0e: begin
        if (!signed32_index_escape) begin // PC_INDEX_DISP64
          r.valid = 1'b1;
          r.form = BR_EA_PC_INDEX_DISP64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_CS;
          r.base = BR_EA_BASE_PC;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_CS;
        end
        else if (signed32_index_escape) begin // S32_PC_INDEX_DISP64
          r.valid = 1'b1;
          r.form = BR_EA_S32_PC_INDEX_DISP64;
          r.is_register = 1'b0;
          r.is_memory = 1'b1;
          r.is_immediate = 1'b0;
          r.update_eligible = 1'b0;
          r.segment_selectable = 1'b0;
          r.segment = BR_EA_SEG_CS;
          r.base = BR_EA_BASE_PC;
          r.has_base_reg = 1'b0;
          r.has_index_reg = 1'b1;
          r.has_displacement = 1'b1;
          r.has_absolute = 1'b0;
          r.displacement_words = 3'd4;
          r.payload_words = 3'd5;
          r.index_reg = extra[4:2];
          r.scale_log2 = extra[1:0];
          r.signed32_index_escape = 1'b1;
          r.segment_valid = (segment == 3'd0);
          r.segment = BR_EA_SEG_CS;
        end
        else begin
          r.reserved = 1'b1;
        end
      end
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
