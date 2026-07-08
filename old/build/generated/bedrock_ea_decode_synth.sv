`timescale 1ns/1ps
`default_nettype none

module bedrock_ea_decode_synth(
  input  [5:0]  ea_i,
  input  [15:0] descriptor_i,
  output reg        valid_o,
  output reg        reserved_o,
  output reg        needs_descriptor_o,
  output reg [5:0]  form_o,
  output reg        is_register_o,
  output reg        is_memory_o,
  output reg        is_immediate_o,
  output reg        update_eligible_o,
  output reg        signed32_index_escape_o,
  output reg        segment_selectable_o,
  output reg        segment_valid_o,
  output reg        has_base_reg_o,
  output reg        has_index_reg_o,
  output reg        has_displacement_o,
  output reg        has_absolute_o,
  output reg [2:0]  segment_o,
  output reg [2:0]  base_o,
  output reg [2:0]  base_reg_o,
  output reg [2:0]  index_reg_o,
  output reg [1:0]  scale_log2_o,
  output reg [2:0]  displacement_words_o,
  output reg [2:0]  payload_words_o
);
  localparam [5:0] BR_EA_DREG = 6'd1; // DREG
  localparam [5:0] BR_EA_AREG = 6'd2; // AREG
  localparam [5:0] BR_EA_INDIRECT = 6'd3; // INDIRECT
  localparam [5:0] BR_EA_A_DISP16 = 6'd4; // A_DISP16
  localparam [5:0] BR_EA_A_DISP32 = 6'd5; // A_DISP32
  localparam [5:0] BR_EA_PC_DISP16 = 6'd6; // PC_DISP16
  localparam [5:0] BR_EA_PC_DISP32 = 6'd7; // PC_DISP32
  localparam [5:0] BR_EA_PC_DISP64 = 6'd8; // PC_DISP64
  localparam [5:0] BR_EA_SP_DISP16 = 6'd9; // SP_DISP16
  localparam [5:0] BR_EA_SP_DISP32 = 6'd10; // SP_DISP32
  localparam [5:0] BR_EA_SP_DISP64 = 6'd11; // SP_DISP64
  localparam [5:0] BR_EA_SPREG = 6'd12; // SPREG
  localparam [5:0] BR_EA_ABS32 = 6'd13; // ABS32
  localparam [5:0] BR_EA_ABS64 = 6'd14; // ABS64
  localparam [5:0] BR_EA_IMM16 = 6'd15; // IMM16
  localparam [5:0] BR_EA_IMM32 = 6'd16; // IMM32
  localparam [5:0] BR_EA_IMM64 = 6'd17; // IMM64
  localparam [5:0] BR_EA_S32_INDEXED_EXTENDED = 6'd18; // S32_INDEXED_EXTENDED
  localparam [5:0] BR_EA_EXTENDED = 6'd19; // EXTENDED
  localparam [5:0] BR_EA_SEG_A_INDEX = 6'd20; // SEG_A_INDEX
  localparam [5:0] BR_EA_SEG_A_INDEX_DISP16 = 6'd21; // SEG_A_INDEX_DISP16
  localparam [5:0] BR_EA_SEG_A_INDEX_DISP32 = 6'd22; // SEG_A_INDEX_DISP32
  localparam [5:0] BR_EA_SEG_A_INDEX_DISP64 = 6'd23; // SEG_A_INDEX_DISP64
  localparam [5:0] BR_EA_SEG_A = 6'd24; // SEG_A
  localparam [5:0] BR_EA_SEG_A_DISP16 = 6'd25; // SEG_A_DISP16
  localparam [5:0] BR_EA_SEG_A_DISP32 = 6'd26; // SEG_A_DISP32
  localparam [5:0] BR_EA_SEG_ABS32 = 6'd27; // SEG_ABS32
  localparam [5:0] BR_EA_SEG_ABS64 = 6'd28; // SEG_ABS64
  localparam [5:0] BR_EA_SP_INDEX_DISP16 = 6'd29; // SP_INDEX_DISP16
  localparam [5:0] BR_EA_SP_INDEX_DISP32 = 6'd30; // SP_INDEX_DISP32
  localparam [5:0] BR_EA_SP_INDEX_DISP64 = 6'd31; // SP_INDEX_DISP64
  localparam [5:0] BR_EA_PC_INDEX_DISP16 = 6'd32; // PC_INDEX_DISP16
  localparam [5:0] BR_EA_PC_INDEX_DISP32 = 6'd33; // PC_INDEX_DISP32
  localparam [5:0] BR_EA_PC_INDEX_DISP64 = 6'd34; // PC_INDEX_DISP64
  localparam [5:0] BR_EA_S32_SEG_A_INDEX = 6'd35; // S32_SEG_A_INDEX
  localparam [5:0] BR_EA_S32_SEG_A_INDEX_DISP16 = 6'd36; // S32_SEG_A_INDEX_DISP16
  localparam [5:0] BR_EA_S32_SEG_A_INDEX_DISP32 = 6'd37; // S32_SEG_A_INDEX_DISP32
  localparam [5:0] BR_EA_S32_SEG_A_INDEX_DISP64 = 6'd38; // S32_SEG_A_INDEX_DISP64
  localparam [5:0] BR_EA_S32_SP_INDEX_DISP16 = 6'd39; // S32_SP_INDEX_DISP16
  localparam [5:0] BR_EA_S32_SP_INDEX_DISP32 = 6'd40; // S32_SP_INDEX_DISP32
  localparam [5:0] BR_EA_S32_SP_INDEX_DISP64 = 6'd41; // S32_SP_INDEX_DISP64
  localparam [5:0] BR_EA_S32_PC_INDEX_DISP16 = 6'd42; // S32_PC_INDEX_DISP16
  localparam [5:0] BR_EA_S32_PC_INDEX_DISP32 = 6'd43; // S32_PC_INDEX_DISP32
  localparam [5:0] BR_EA_S32_PC_INDEX_DISP64 = 6'd44; // S32_PC_INDEX_DISP64
  wire [4:0] mode = descriptor_i[15:11];
  wire [2:0] seg = descriptor_i[10:8];
  wire [7:0] extra = descriptor_i[7:0];
  reg signed32_escape;
  always @* begin
    valid_o = 1'b0;
    reserved_o = 1'b0;
    needs_descriptor_o = 1'b0;
    form_o = 6'd0;
    is_register_o = 1'b0;
    is_memory_o = 1'b0;
    is_immediate_o = 1'b0;
    update_eligible_o = 1'b0;
    signed32_index_escape_o = 1'b0;
    segment_selectable_o = 1'b0;
    segment_valid_o = 1'b1;
    has_base_reg_o = 1'b0;
    has_index_reg_o = 1'b0;
    has_displacement_o = 1'b0;
    has_absolute_o = 1'b0;
    segment_o = 3'd0;
    base_o = 3'd0;
    base_reg_o = 3'd0;
    index_reg_o = 3'd0;
    scale_log2_o = 2'd0;
    displacement_words_o = 3'd0;
    payload_words_o = 3'd0;
    signed32_escape = 1'b0;
    casez (ea_i)
      6'b000?_??: begin // DREG
        valid_o = 1'b1;
        form_o = BR_EA_DREG;
        is_register_o = 1'b1;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd1;
        has_base_reg_o = 1'b1;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd0;
        payload_words_o = 3'd0;
        base_reg_o = ea_i[2:0];
      end
      6'b001?_??: begin // AREG
        valid_o = 1'b1;
        form_o = BR_EA_AREG;
        is_register_o = 1'b1;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd2;
        has_base_reg_o = 1'b1;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd0;
        payload_words_o = 3'd0;
        base_reg_o = ea_i[2:0];
      end
      6'b010?_??: begin // INDIRECT
        valid_o = 1'b1;
        form_o = BR_EA_INDIRECT;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b1;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd2;
        has_base_reg_o = 1'b1;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd0;
        payload_words_o = 3'd0;
        base_reg_o = ea_i[2:0];
      end
      6'b011?_??: begin // A_DISP16
        valid_o = 1'b1;
        form_o = BR_EA_A_DISP16;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd2;
        has_base_reg_o = 1'b1;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd1;
        payload_words_o = 3'd1;
        base_reg_o = ea_i[2:0];
      end
      6'b100?_??: begin // A_DISP32
        valid_o = 1'b1;
        form_o = BR_EA_A_DISP32;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd2;
        has_base_reg_o = 1'b1;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd2;
        payload_words_o = 3'd2;
        base_reg_o = ea_i[2:0];
      end
      6'b1010_00: begin // PC_DISP16
        valid_o = 1'b1;
        form_o = BR_EA_PC_DISP16;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd0;
        base_o = 3'd3;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd1;
        payload_words_o = 3'd1;
      end
      6'b1010_01: begin // PC_DISP32
        valid_o = 1'b1;
        form_o = BR_EA_PC_DISP32;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd0;
        base_o = 3'd3;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd2;
        payload_words_o = 3'd2;
      end
      6'b1010_10: begin // PC_DISP64
        valid_o = 1'b1;
        form_o = BR_EA_PC_DISP64;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd0;
        base_o = 3'd3;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd4;
        payload_words_o = 3'd4;
      end
      6'b1011_00: begin // SP_DISP16
        valid_o = 1'b1;
        form_o = BR_EA_SP_DISP16;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd2;
        base_o = 3'd4;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd1;
        payload_words_o = 3'd1;
      end
      6'b1011_01: begin // SP_DISP32
        valid_o = 1'b1;
        form_o = BR_EA_SP_DISP32;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd2;
        base_o = 3'd4;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd2;
        payload_words_o = 3'd2;
      end
      6'b1011_10: begin // SP_DISP64
        valid_o = 1'b1;
        form_o = BR_EA_SP_DISP64;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd2;
        base_o = 3'd4;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b1;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd4;
        payload_words_o = 3'd4;
      end
      6'b1011_11: begin // SPREG
        valid_o = 1'b1;
        form_o = BR_EA_SPREG;
        is_register_o = 1'b1;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd4;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd0;
        payload_words_o = 3'd0;
      end
      6'b1100_00: begin // ABS32
        valid_o = 1'b1;
        form_o = BR_EA_ABS32;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd5;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b1;
        displacement_words_o = 3'd2;
        payload_words_o = 3'd2;
      end
      6'b1100_01: begin // ABS64
        valid_o = 1'b1;
        form_o = BR_EA_ABS64;
        is_register_o = 1'b0;
        is_memory_o = 1'b1;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd5;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b1;
        displacement_words_o = 3'd4;
        payload_words_o = 3'd4;
      end
      6'b1100_10: begin // IMM16
        valid_o = 1'b1;
        form_o = BR_EA_IMM16;
        is_register_o = 1'b0;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b1;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd6;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd1;
        payload_words_o = 3'd1;
      end
      6'b1100_11: begin // IMM32
        valid_o = 1'b1;
        form_o = BR_EA_IMM32;
        is_register_o = 1'b0;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b1;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd6;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd2;
        payload_words_o = 3'd2;
      end
      6'b1101_00: begin // IMM64
        valid_o = 1'b1;
        form_o = BR_EA_IMM64;
        is_register_o = 1'b0;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b1;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd6;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd4;
        payload_words_o = 3'd4;
      end
      6'b1111_10: begin // S32_INDEXED_EXTENDED
        valid_o = 1'b1;
        form_o = BR_EA_S32_INDEXED_EXTENDED;
        is_register_o = 1'b0;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd0;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd0;
        payload_words_o = 3'd0;
        needs_descriptor_o = 1'b1;
        signed32_escape = 1'b1;
        signed32_index_escape_o = 1'b1;
        payload_words_o = 3'd1;
      end
      6'b1111_11: begin // EXTENDED
        valid_o = 1'b1;
        form_o = BR_EA_EXTENDED;
        is_register_o = 1'b0;
        is_memory_o = 1'b0;
        is_immediate_o = 1'b0;
        update_eligible_o = 1'b0;
        segment_selectable_o = 1'b0;
        segment_o = 3'd1;
        base_o = 3'd0;
        has_base_reg_o = 1'b0;
        has_index_reg_o = 1'b0;
        has_displacement_o = 1'b0;
        has_absolute_o = 1'b0;
        displacement_words_o = 3'd0;
        payload_words_o = 3'd0;
        needs_descriptor_o = 1'b1;
        payload_words_o = 3'd1;
      end

      default: begin reserved_o = 1'b1; end
    endcase
    if (needs_descriptor_o) begin
      valid_o = 1'b0;
      reserved_o = 1'b0;
      form_o = 6'd0;
      is_register_o = 1'b0;
      is_memory_o = 1'b0;
      is_immediate_o = 1'b0;
      update_eligible_o = 1'b0;
      signed32_index_escape_o = signed32_escape;
      segment_selectable_o = 1'b0;
      segment_valid_o = 1'b1;
      has_base_reg_o = 1'b0;
      has_index_reg_o = 1'b0;
      has_displacement_o = 1'b0;
      has_absolute_o = 1'b0;
      segment_o = seg;
      base_o = 3'd0;
      base_reg_o = 3'd0;
      index_reg_o = 3'd0;
      scale_log2_o = 2'd0;
      displacement_words_o = 3'd0;
      payload_words_o = 3'd0;
      case (mode)
        5'h00: begin
          if (signed32_escape == 1'b0) begin // SEG_A_INDEX
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A_INDEX;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b0;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd0;
            payload_words_o = 3'd1;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else if (signed32_escape == 1'b1) begin // S32_SEG_A_INDEX
            valid_o = 1'b1;
            form_o = BR_EA_S32_SEG_A_INDEX;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b0;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd0;
            payload_words_o = 3'd1;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h01: begin
          if (signed32_escape == 1'b0) begin // SEG_A_INDEX_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A_INDEX_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else if (signed32_escape == 1'b1) begin // S32_SEG_A_INDEX_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_S32_SEG_A_INDEX_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h02: begin
          if (signed32_escape == 1'b0) begin // SEG_A_INDEX_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A_INDEX_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else if (signed32_escape == 1'b1) begin // S32_SEG_A_INDEX_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_S32_SEG_A_INDEX_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h03: begin
          if (signed32_escape == 1'b0) begin // SEG_A_INDEX_DISP64
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A_INDEX_DISP64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else if (signed32_escape == 1'b1) begin // S32_SEG_A_INDEX_DISP64
            valid_o = 1'b1;
            form_o = BR_EA_S32_SEG_A_INDEX_DISP64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            base_reg_o = extra[7:5];
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h04: begin
          if (signed32_escape == 1'b0) begin // SEG_A
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b1;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b0;
            has_displacement_o = 1'b0;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd0;
            payload_words_o = 3'd1;
            base_reg_o = extra[7:5];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h05: begin
          if (signed32_escape == 1'b0) begin // SEG_A_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b0;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            base_reg_o = extra[7:5];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h06: begin
          if (signed32_escape == 1'b0) begin // SEG_A_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_SEG_A_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd2;
            has_base_reg_o = 1'b1;
            has_index_reg_o = 1'b0;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            base_reg_o = extra[7:5];
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h07: begin
          if (signed32_escape == 1'b0) begin // SEG_ABS32
            valid_o = 1'b1;
            form_o = BR_EA_SEG_ABS32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd5;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b0;
            has_displacement_o = 1'b0;
            has_absolute_o = 1'b1;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h08: begin
          if (signed32_escape == 1'b0) begin // SEG_ABS64
            valid_o = 1'b1;
            form_o = BR_EA_SEG_ABS64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b1;
            segment_o = 3'd1;
            base_o = 3'd5;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b0;
            has_displacement_o = 1'b0;
            has_absolute_o = 1'b1;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            segment_o = seg;
            segment_valid_o = 1'b1;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h09: begin
          if (signed32_escape == 1'b0) begin // SP_INDEX_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_SP_INDEX_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd2;
            base_o = 3'd4;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd2;
          end
          else if (signed32_escape == 1'b1) begin // S32_SP_INDEX_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_S32_SP_INDEX_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd2;
            base_o = 3'd4;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd2;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h0a: begin
          if (signed32_escape == 1'b0) begin // SP_INDEX_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_SP_INDEX_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd2;
            base_o = 3'd4;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd2;
          end
          else if (signed32_escape == 1'b1) begin // S32_SP_INDEX_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_S32_SP_INDEX_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd2;
            base_o = 3'd4;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd2;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h0b: begin
          if (signed32_escape == 1'b0) begin // SP_INDEX_DISP64
            valid_o = 1'b1;
            form_o = BR_EA_SP_INDEX_DISP64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd2;
            base_o = 3'd4;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd2;
          end
          else if (signed32_escape == 1'b1) begin // S32_SP_INDEX_DISP64
            valid_o = 1'b1;
            form_o = BR_EA_S32_SP_INDEX_DISP64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd2;
            base_o = 3'd4;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd2;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h0c: begin
          if (signed32_escape == 1'b0) begin // PC_INDEX_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_PC_INDEX_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd0;
            base_o = 3'd3;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd0;
          end
          else if (signed32_escape == 1'b1) begin // S32_PC_INDEX_DISP16
            valid_o = 1'b1;
            form_o = BR_EA_S32_PC_INDEX_DISP16;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd0;
            base_o = 3'd3;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd1;
            payload_words_o = 3'd2;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd0;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h0d: begin
          if (signed32_escape == 1'b0) begin // PC_INDEX_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_PC_INDEX_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd0;
            base_o = 3'd3;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd0;
          end
          else if (signed32_escape == 1'b1) begin // S32_PC_INDEX_DISP32
            valid_o = 1'b1;
            form_o = BR_EA_S32_PC_INDEX_DISP32;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd0;
            base_o = 3'd3;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd2;
            payload_words_o = 3'd3;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd0;
          end
          else begin reserved_o = 1'b1; end
        end
        5'h0e: begin
          if (signed32_escape == 1'b0) begin // PC_INDEX_DISP64
            valid_o = 1'b1;
            form_o = BR_EA_PC_INDEX_DISP64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd0;
            base_o = 3'd3;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd0;
          end
          else if (signed32_escape == 1'b1) begin // S32_PC_INDEX_DISP64
            valid_o = 1'b1;
            form_o = BR_EA_S32_PC_INDEX_DISP64;
            is_register_o = 1'b0;
            is_memory_o = 1'b1;
            is_immediate_o = 1'b0;
            update_eligible_o = 1'b0;
            segment_selectable_o = 1'b0;
            segment_o = 3'd0;
            base_o = 3'd3;
            has_base_reg_o = 1'b0;
            has_index_reg_o = 1'b1;
            has_displacement_o = 1'b1;
            has_absolute_o = 1'b0;
            displacement_words_o = 3'd4;
            payload_words_o = 3'd5;
            index_reg_o = extra[4:2];
            scale_log2_o = extra[1:0];
            signed32_escape = 1'b1;
            signed32_index_escape_o = 1'b1;
            valid_o = valid_o && (seg == 3'd0);
            segment_valid_o = (seg == 3'd0);
            segment_o = 3'd0;
          end
          else begin reserved_o = 1'b1; end
        end
        default: begin reserved_o = 1'b1; end
      endcase
    end
  end
endmodule

`default_nettype wire
