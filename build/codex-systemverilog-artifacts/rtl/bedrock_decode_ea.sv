// Generated from canonical Decode IR. Do not edit.
module bedrock_decode_ea
  import bedrock_decode_pkg::*;
(
  input  d0_ea_result_t d0_i,
  input  logic [BEDROCK_RECORD_BYTES*8-1:0] record_i,
  input  logic [4:0] byte_count_i,
  output ea_decode_result_t result_o
);
  typedef enum logic [1:0] {
    EA_DESCRIPTOR_FAMILY_NONE = 2'd0,
    EA_DESCRIPTOR_FAMILY_EXT1 = 2'd1,
    EA_DESCRIPTOR_FAMILY_EXT2 = 2'd2
  } ea_descriptor_family_e;

  typedef struct packed {
    logic valid;
    ea_descriptor_family_e descriptor_family;
    decoded_ea_t ea;
  } compact_ea_decode_t;

  typedef struct packed {
    logic valid;
    decoded_ea_t ea;
  } descriptor_decode_t;

  function automatic compact_ea_decode_t decode_compact_ea(
    input ea_profile_e profile,
    input logic [6:0] compact_raw
  );
    begin
      decode_compact_ea = '0;
      unique case (profile)
      EA_PROFILE_EA, EA_PROFILE_FEA, EA_PROFILE_VEA: begin
        unique casez (compact_raw)
      7'b000?_???: begin // register_indirect
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_0;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_compact_ea.ea.base_register_valid = 1'b1;
        decode_compact_ea.ea.base_register = 4'({compact_raw[3], compact_raw[2], compact_raw[1], compact_raw[0]});
      end
      7'b001?_???: begin // register_disp8s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_8;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_compact_ea.ea.base_register_valid = 1'b1;
        decode_compact_ea.ea.base_register = 4'({compact_raw[3], compact_raw[2], compact_raw[1], compact_raw[0]});
      end
      7'b010?_???: begin // register_disp16s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_16;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_compact_ea.ea.base_register_valid = 1'b1;
        decode_compact_ea.ea.base_register = 4'({compact_raw[3], compact_raw[2], compact_raw[1], compact_raw[0]});
      end
      7'b011?_???: begin // register_disp32s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_compact_ea.ea.base_register_valid = 1'b1;
        decode_compact_ea.ea.base_register = 4'({compact_raw[3], compact_raw[2], compact_raw[1], compact_raw[0]});
      end
      7'b100?_???: begin // register_disp64
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_compact_ea.ea.base_register_valid = 1'b1;
        decode_compact_ea.ea.base_register = 4'({compact_raw[3], compact_raw[2], compact_raw[1], compact_raw[0]});
      end
      7'b1010_000: begin // stack_pointer_disp8s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_8;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_SS;
        decode_compact_ea.ea.base = EA_BASE_SP;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_001: begin // stack_pointer_disp16s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_16;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_SS;
        decode_compact_ea.ea.base = EA_BASE_SP;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_010: begin // stack_pointer_disp32s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_SS;
        decode_compact_ea.ea.base = EA_BASE_SP;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_011: begin // stack_pointer_disp64
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_SS;
        decode_compact_ea.ea.base = EA_BASE_SP;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_100: begin // program_counter_disp8s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_8;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_CS;
        decode_compact_ea.ea.base = EA_BASE_PC;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_101: begin // program_counter_disp16s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_16;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_CS;
        decode_compact_ea.ea.base = EA_BASE_PC;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_110: begin // program_counter_disp32s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_CS;
        decode_compact_ea.ea.base = EA_BASE_PC;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1010_111: begin // program_counter_disp64
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_CS;
        decode_compact_ea.ea.base = EA_BASE_PC;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1011_001: begin // absolute_32s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1011_010: begin // absolute_64
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_MEMORY;
        decode_compact_ea.ea.segment = EA_SEGMENT_DEFAULT;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1011_111: begin // ext1_disp8s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT1;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_8;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_000: begin // ext1_disp16s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT1;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_16;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_001: begin // ext1_disp32s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT1;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_010: begin // ext1_disp64
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT1;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_011: begin // ext1
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT1;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_0;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_100: begin // ext2_disp8s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT2;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_8;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_101: begin // ext2_disp16s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT2;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_16;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_110: begin // ext2_disp32s
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT2;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
        decode_compact_ea.ea.payload_signed = 1'b1;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1100_111: begin // ext2_disp64
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT2;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
      7'b1101_000: begin // ext2
        decode_compact_ea.valid = 1'b1;
        decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_EXT2;
        decode_compact_ea.ea.valid = 1'b1;
        decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_0;
        decode_compact_ea.ea.payload_signed = 1'b0;
        decode_compact_ea.ea.kind = EA_KIND_ESCAPE;
        decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
        decode_compact_ea.ea.base = EA_BASE_NONE;
        decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
        decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
      end
        default: begin
          unique case (profile)
        EA_PROFILE_EA: begin
          unique case (compact_raw)
          7'h58: begin // stack_pointer_indirect
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_0;
            decode_compact_ea.ea.payload_signed = 1'b0;
            decode_compact_ea.ea.kind = EA_KIND_MEMORY;
            decode_compact_ea.ea.segment = EA_SEGMENT_SS;
            decode_compact_ea.ea.base = EA_BASE_SP;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
          7'h5b: begin // immediate_8s
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_8;
            decode_compact_ea.ea.payload_signed = 1'b1;
            decode_compact_ea.ea.kind = EA_KIND_IMMEDIATE;
            decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
            decode_compact_ea.ea.base = EA_BASE_NONE;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
          7'h5c: begin // immediate_16s
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_16;
            decode_compact_ea.ea.payload_signed = 1'b1;
            decode_compact_ea.ea.kind = EA_KIND_IMMEDIATE;
            decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
            decode_compact_ea.ea.base = EA_BASE_NONE;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
          7'h5d: begin // immediate_32s
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
            decode_compact_ea.ea.payload_signed = 1'b1;
            decode_compact_ea.ea.kind = EA_KIND_IMMEDIATE;
            decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
            decode_compact_ea.ea.base = EA_BASE_NONE;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
          7'h5e: begin // immediate_64
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
            decode_compact_ea.ea.payload_signed = 1'b0;
            decode_compact_ea.ea.kind = EA_KIND_IMMEDIATE;
            decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
            decode_compact_ea.ea.base = EA_BASE_NONE;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
            default: begin end
          endcase
        end
        EA_PROFILE_FEA: begin
          unique case (compact_raw)
          7'h5d: begin // immediate_sf
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_32;
            decode_compact_ea.ea.payload_signed = 1'b0;
            decode_compact_ea.ea.kind = EA_KIND_FLOAT_IMMEDIATE;
            decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
            decode_compact_ea.ea.base = EA_BASE_NONE;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
          7'h5e: begin // immediate_df
            decode_compact_ea.valid = 1'b1;
            decode_compact_ea.descriptor_family = EA_DESCRIPTOR_FAMILY_NONE;
            decode_compact_ea.ea.valid = 1'b1;
            decode_compact_ea.ea.payload_width = EA_PAYLOAD_WIDTH_64;
            decode_compact_ea.ea.payload_signed = 1'b0;
            decode_compact_ea.ea.kind = EA_KIND_FLOAT_IMMEDIATE;
            decode_compact_ea.ea.segment = EA_SEGMENT_NONE;
            decode_compact_ea.ea.base = EA_BASE_NONE;
            decode_compact_ea.ea.register_name = EA_REGISTER_NONE;
            decode_compact_ea.ea.update_target = EA_UPDATE_TARGET_NONE;
            decode_compact_ea.ea.update_mode = EA_UPDATE_MODE_NONE;
          end
            default: begin end
          endcase
        end
            default: begin end
          endcase
        end
        endcase
      end
        default: begin end
      endcase
    end
  endfunction

  function automatic descriptor_decode_t decode_ext1_descriptor(
    input logic [7:0] descriptor
  );
    begin
      decode_ext1_descriptor = '0;
      unique casez (descriptor)
      8'b0???_????: begin // explicit_segment_base
        decode_ext1_descriptor.valid = 1'b1;
        decode_ext1_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext1_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext1_descriptor.ea.base = EA_BASE_NONE;
        decode_ext1_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext1_descriptor.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_ext1_descriptor.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_ext1_descriptor.ea.base_register_valid = 1'b1;
        decode_ext1_descriptor.ea.base_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext1_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext1_descriptor.ea.segment_register = 4'({descriptor[6], descriptor[5], descriptor[4]});
      end
      8'b1???_0011: begin // explicit_segment_zero_base
        decode_ext1_descriptor.valid = 1'b1;
        decode_ext1_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext1_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext1_descriptor.ea.base = EA_BASE_ZERO;
        decode_ext1_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext1_descriptor.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_ext1_descriptor.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_ext1_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext1_descriptor.ea.segment_register = 4'({descriptor[6], descriptor[5], descriptor[4]});
      end
      8'b1???_?100: begin // default_segment_base_postincrement
        decode_ext1_descriptor.valid = 1'b1;
        decode_ext1_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext1_descriptor.ea.segment = EA_SEGMENT_DEFAULT;
        decode_ext1_descriptor.ea.base = EA_BASE_NONE;
        decode_ext1_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext1_descriptor.ea.update_target = EA_UPDATE_TARGET_B;
        decode_ext1_descriptor.ea.update_mode = EA_UPDATE_MODE_POSTINCREMENT;
        decode_ext1_descriptor.ea.base_register_valid = 1'b1;
        decode_ext1_descriptor.ea.base_register = 4'({descriptor[6], descriptor[5], descriptor[4], descriptor[3]});
      end
      8'b1???_?101: begin // default_segment_base_predecrement
        decode_ext1_descriptor.valid = 1'b1;
        decode_ext1_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext1_descriptor.ea.segment = EA_SEGMENT_DEFAULT;
        decode_ext1_descriptor.ea.base = EA_BASE_NONE;
        decode_ext1_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext1_descriptor.ea.update_target = EA_UPDATE_TARGET_B;
        decode_ext1_descriptor.ea.update_mode = EA_UPDATE_MODE_PREDECREMENT;
        decode_ext1_descriptor.ea.base_register_valid = 1'b1;
        decode_ext1_descriptor.ea.base_register = 4'({descriptor[6], descriptor[5], descriptor[4], descriptor[3]});
      end
        default: begin end
      endcase
    end
  endfunction
  function automatic descriptor_decode_t decode_ext2_descriptor(
    input logic [15:0] descriptor
  );
    begin
      decode_ext2_descriptor = '0;
      unique casez (descriptor)
      16'b1???_0000_????_????: begin // explicit_segment_index_postincrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_NONE;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_POSTINCREMENT;
        decode_ext2_descriptor.ea.base_register_valid = 1'b1;
        decode_ext2_descriptor.ea.base_register = 4'({descriptor[7], descriptor[6], descriptor[5], descriptor[4]});
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_0001_????_????: begin // explicit_segment_index_predecrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_NONE;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_PREDECREMENT;
        decode_ext2_descriptor.ea.base_register_valid = 1'b1;
        decode_ext2_descriptor.ea.base_register = 4'({descriptor[7], descriptor[6], descriptor[5], descriptor[4]});
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_0010_????_????: begin // explicit_segment_index
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_NONE;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_ext2_descriptor.ea.base_register_valid = 1'b1;
        decode_ext2_descriptor.ea.base_register = 4'({descriptor[7], descriptor[6], descriptor[5], descriptor[4]});
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_1000_????_0000: begin // explicit_segment_base_postincrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_NONE;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_B;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_POSTINCREMENT;
        decode_ext2_descriptor.ea.base_register_valid = 1'b1;
        decode_ext2_descriptor.ea.base_register = 4'({descriptor[7], descriptor[6], descriptor[5], descriptor[4]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_1000_????_0001: begin // explicit_segment_base_predecrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_NONE;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_B;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_PREDECREMENT;
        decode_ext2_descriptor.ea.base_register_valid = 1'b1;
        decode_ext2_descriptor.ea.base_register = 4'({descriptor[7], descriptor[6], descriptor[5], descriptor[4]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_1001_0000_????: begin // explicit_segment_zero_base_index_postincrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_ZERO;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_POSTINCREMENT;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_1001_0001_????: begin // explicit_segment_zero_base_index_predecrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_ZERO;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_PREDECREMENT;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1???_1001_0010_????: begin // explicit_segment_zero_base_index
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_EXPLICIT;
        decode_ext2_descriptor.ea.base = EA_BASE_ZERO;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
        decode_ext2_descriptor.ea.segment_register_valid = 1'b1;
        decode_ext2_descriptor.ea.segment_register = 4'({descriptor[14], descriptor[13], descriptor[12]});
      end
      16'b1000_1010_0000_????: begin // stack_pointer_index_postincrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_SS;
        decode_ext2_descriptor.ea.base = EA_BASE_SP;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_POSTINCREMENT;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
      end
      16'b1000_1010_0001_????: begin // stack_pointer_index_predecrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_SS;
        decode_ext2_descriptor.ea.base = EA_BASE_SP;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_PREDECREMENT;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
      end
      16'b1000_1010_0010_????: begin // stack_pointer_index
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_SS;
        decode_ext2_descriptor.ea.base = EA_BASE_SP;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
      end
      16'b1000_1011_0000_????: begin // program_counter_index_postincrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_CS;
        decode_ext2_descriptor.ea.base = EA_BASE_PC;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_POSTINCREMENT;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
      end
      16'b1000_1011_0001_????: begin // program_counter_index_predecrement
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_CS;
        decode_ext2_descriptor.ea.base = EA_BASE_PC;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_I;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_PREDECREMENT;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
      end
      16'b1000_1011_0010_????: begin // program_counter_index
        decode_ext2_descriptor.valid = 1'b1;
        decode_ext2_descriptor.ea.kind = EA_KIND_MEMORY;
        decode_ext2_descriptor.ea.segment = EA_SEGMENT_CS;
        decode_ext2_descriptor.ea.base = EA_BASE_PC;
        decode_ext2_descriptor.ea.register_name = EA_REGISTER_NONE;
        decode_ext2_descriptor.ea.update_target = EA_UPDATE_TARGET_NONE;
        decode_ext2_descriptor.ea.update_mode = EA_UPDATE_MODE_NONE;
        decode_ext2_descriptor.ea.index_register_valid = 1'b1;
        decode_ext2_descriptor.ea.index_register = 4'({descriptor[3], descriptor[2], descriptor[1], descriptor[0]});
      end
        default: begin end
      endcase
    end
  endfunction

  function automatic decoded_ea_t merge_descriptor_ea(
    input decoded_ea_t compact_ea,
    input decoded_ea_t descriptor_ea
  );
    begin
      merge_descriptor_ea = compact_ea;
      merge_descriptor_ea.kind = descriptor_ea.kind;
      merge_descriptor_ea.segment = descriptor_ea.segment;
      merge_descriptor_ea.base = descriptor_ea.base;
      merge_descriptor_ea.register_name = descriptor_ea.register_name;
      merge_descriptor_ea.update_target = descriptor_ea.update_target;
      merge_descriptor_ea.update_mode = descriptor_ea.update_mode;
      merge_descriptor_ea.direct_register_valid = descriptor_ea.direct_register_valid;
      merge_descriptor_ea.direct_register = descriptor_ea.direct_register;
      merge_descriptor_ea.base_register_valid = descriptor_ea.base_register_valid;
      merge_descriptor_ea.base_register = descriptor_ea.base_register;
      merge_descriptor_ea.index_register_valid = descriptor_ea.index_register_valid;
      merge_descriptor_ea.index_register = descriptor_ea.index_register;
      merge_descriptor_ea.stride_register_valid = descriptor_ea.stride_register_valid;
      merge_descriptor_ea.stride_register = descriptor_ea.stride_register;
      merge_descriptor_ea.segment_register_valid = descriptor_ea.segment_register_valid;
      merge_descriptor_ea.segment_register = descriptor_ea.segment_register;
    end
  endfunction

  function automatic ea_parse_result_t parse_ea_payload(
    input decoded_ea_t ea_in,
    input logic [BEDROCK_RECORD_BYTES*8-1:0] record,
    input logic [4:0] byte_count,
    input logic [5:0] cursor
  );
    begin
      parse_ea_payload = '0;
      parse_ea_payload.stage = D1_STAGE_EA_PAYLOAD;
      parse_ea_payload.next_cursor = cursor;
      parse_ea_payload.ea = ea_in;
      unique case (ea_in.payload_width)
      EA_PAYLOAD_WIDTH_0: begin
        parse_ea_payload.ok = 1'b1;
        parse_ea_payload.stage = D1_STAGE_SUCCESS;
      end
      EA_PAYLOAD_WIDTH_8: begin
        if ((cursor + 1) > byte_count || (cursor + 1) > BEDROCK_RECORD_BYTES) begin
          parse_ea_payload.next_cursor = cursor + 1;
        end else begin
          parse_ea_payload.ea.payload[0 +: 8] = record[((cursor + 0) * 8) +: 8];
          parse_ea_payload.next_cursor = cursor + 1;
          parse_ea_payload.ok = 1'b1;
          parse_ea_payload.stage = D1_STAGE_SUCCESS;
        end
      end
      EA_PAYLOAD_WIDTH_16: begin
        if ((cursor + 2) > byte_count || (cursor + 2) > BEDROCK_RECORD_BYTES) begin
          parse_ea_payload.next_cursor = cursor + 2;
        end else begin
          parse_ea_payload.ea.payload[0 +: 8] = record[((cursor + 0) * 8) +: 8];
          parse_ea_payload.ea.payload[8 +: 8] = record[((cursor + 1) * 8) +: 8];
          parse_ea_payload.next_cursor = cursor + 2;
          parse_ea_payload.ok = 1'b1;
          parse_ea_payload.stage = D1_STAGE_SUCCESS;
        end
      end
      EA_PAYLOAD_WIDTH_32: begin
        if ((cursor + 4) > byte_count || (cursor + 4) > BEDROCK_RECORD_BYTES) begin
          parse_ea_payload.next_cursor = cursor + 4;
        end else begin
          parse_ea_payload.ea.payload[0 +: 8] = record[((cursor + 0) * 8) +: 8];
          parse_ea_payload.ea.payload[8 +: 8] = record[((cursor + 1) * 8) +: 8];
          parse_ea_payload.ea.payload[16 +: 8] = record[((cursor + 2) * 8) +: 8];
          parse_ea_payload.ea.payload[24 +: 8] = record[((cursor + 3) * 8) +: 8];
          parse_ea_payload.next_cursor = cursor + 4;
          parse_ea_payload.ok = 1'b1;
          parse_ea_payload.stage = D1_STAGE_SUCCESS;
        end
      end
      EA_PAYLOAD_WIDTH_64: begin
        if ((cursor + 8) > byte_count || (cursor + 8) > BEDROCK_RECORD_BYTES) begin
          parse_ea_payload.next_cursor = cursor + 8;
        end else begin
          parse_ea_payload.ea.payload[0 +: 8] = record[((cursor + 0) * 8) +: 8];
          parse_ea_payload.ea.payload[8 +: 8] = record[((cursor + 1) * 8) +: 8];
          parse_ea_payload.ea.payload[16 +: 8] = record[((cursor + 2) * 8) +: 8];
          parse_ea_payload.ea.payload[24 +: 8] = record[((cursor + 3) * 8) +: 8];
          parse_ea_payload.ea.payload[32 +: 8] = record[((cursor + 4) * 8) +: 8];
          parse_ea_payload.ea.payload[40 +: 8] = record[((cursor + 5) * 8) +: 8];
          parse_ea_payload.ea.payload[48 +: 8] = record[((cursor + 6) * 8) +: 8];
          parse_ea_payload.ea.payload[56 +: 8] = record[((cursor + 7) * 8) +: 8];
          parse_ea_payload.next_cursor = cursor + 8;
          parse_ea_payload.ok = 1'b1;
          parse_ea_payload.stage = D1_STAGE_SUCCESS;
        end
      end
        default: begin end
      endcase
    end
  endfunction

  function automatic logic [5:0] ea_payload_cursor(
    input compact_ea_decode_t compact_decode,
    input logic [5:0] cursor_in
  );
    begin
      ea_payload_cursor = cursor_in;
      unique case (compact_decode.descriptor_family)
      EA_DESCRIPTOR_FAMILY_EXT1: ea_payload_cursor = cursor_in + 1;
      EA_DESCRIPTOR_FAMILY_EXT2: ea_payload_cursor = cursor_in + 2;
        default: begin end
      endcase
    end
  endfunction

  function automatic ea_parse_result_t resolve_ea_descriptor(
    input ea_profile_e profile,
    input operand_ea_width_e operand_width,
    input compact_ea_decode_t compact_decode,
    input descriptor_decode_t ext1_decode,
    input descriptor_decode_t ext2_decode,
    input logic [4:0] byte_count,
    input logic [5:0] cursor_in
  );
    begin
      resolve_ea_descriptor = '0;
      resolve_ea_descriptor.stage = D1_STAGE_EA_DESCRIPTOR;
      resolve_ea_descriptor.next_cursor = cursor_in;
      resolve_ea_descriptor.ea = compact_decode.ea;
      if (compact_decode.valid) unique case (compact_decode.descriptor_family)
      EA_DESCRIPTOR_FAMILY_NONE: begin
        resolve_ea_descriptor.ok = 1'b1;
        resolve_ea_descriptor.stage = D1_STAGE_SUCCESS;
      end
      EA_DESCRIPTOR_FAMILY_EXT1: begin
        if ((cursor_in + 1) > byte_count ||
            (cursor_in + 1) > BEDROCK_RECORD_BYTES) begin
          resolve_ea_descriptor.next_cursor = cursor_in + 1;
        end else if (ext1_decode.valid) begin
          resolve_ea_descriptor.ok = 1'b1;
          resolve_ea_descriptor.stage = D1_STAGE_SUCCESS;
          resolve_ea_descriptor.next_cursor = cursor_in + 1;
          resolve_ea_descriptor.ea = merge_descriptor_ea(
            compact_decode.ea,
            ext1_decode.ea
          );
        end
      end
      EA_DESCRIPTOR_FAMILY_EXT2: begin
        if ((cursor_in + 2) > byte_count ||
            (cursor_in + 2) > BEDROCK_RECORD_BYTES) begin
          resolve_ea_descriptor.next_cursor = cursor_in + 2;
        end else if (ext2_decode.valid) begin
          resolve_ea_descriptor.ok = 1'b1;
          resolve_ea_descriptor.stage = D1_STAGE_SUCCESS;
          resolve_ea_descriptor.next_cursor = cursor_in + 2;
          resolve_ea_descriptor.ea = merge_descriptor_ea(
            compact_decode.ea,
            ext2_decode.ea
          );
        end
      end
        default: begin end
      endcase
      resolve_ea_descriptor.ea.profile = profile;
      resolve_ea_descriptor.ea.operand_width = operand_width;
    end
  endfunction

  function automatic ea_parse_result_t combine_ea_parse(
    input ea_parse_result_t descriptor_parse,
    input ea_parse_result_t payload_parse
  );
    begin
      combine_ea_parse = descriptor_parse;
      if (descriptor_parse.ok) begin
        combine_ea_parse.ok = payload_parse.ok;
        combine_ea_parse.stage = payload_parse.stage;
        combine_ea_parse.next_cursor = payload_parse.next_cursor;
        combine_ea_parse.ea.payload = payload_parse.ea.payload;
      end
    end
  endfunction

  compact_ea_decode_t low_compact;
  compact_ea_decode_t alt_compact;
  descriptor_decode_t low_base_ext1;
  descriptor_decode_t low_base_ext2;
  descriptor_decode_t alt_base_ext1;
  descriptor_decode_t alt_base_ext2;
  descriptor_decode_t low_post_alt_ext1;
  descriptor_decode_t low_post_alt_ext2;
  descriptor_decode_t low_selected_ext1;
  descriptor_decode_t low_selected_ext2;
  ea_parse_result_t low_descriptor_parse;
  ea_parse_result_t alt_descriptor_parse;
  ea_parse_result_t low_payload_parse;
  ea_parse_result_t alt_payload_parse;
  ea_parse_result_t low_parse;
  ea_parse_result_t alt_parse;
  logic [5:0] low_cursor;
  logic [5:0] low_payload_cursor;
  logic [5:0] alt_payload_cursor;

  always_comb begin
    result_o = '0;
    result_o.stage = D1_STAGE_D0_REJECTED;
    low_compact = decode_compact_ea(
      d0_i.ea_profiles[BEDROCK_EA_LOW_SLOT],
      d0_i.low_raw
    );
    alt_compact = decode_compact_ea(
      d0_i.ea_profiles[BEDROCK_EA_ALT_SLOT],
      d0_i.alt_raw
    );
    low_base_ext1 = decode_ext1_descriptor(
      record_i[(d0_i.base_cursor * 8) +: 8]
    );
    low_base_ext2 = decode_ext2_descriptor({
      record_i[(d0_i.base_cursor * 8) +: 8],
      record_i[((d0_i.base_cursor + 1) * 8) +: 8]
    });
    alt_base_ext1 = decode_ext1_descriptor(
      record_i[(d0_i.base_cursor * 8) +: 8]
    );
    alt_base_ext2 = decode_ext2_descriptor({
      record_i[(d0_i.base_cursor * 8) +: 8],
      record_i[((d0_i.base_cursor + 1) * 8) +: 8]
    });
    low_post_alt_ext1 = decode_ext1_descriptor(
      record_i[(d0_i.post_alt_cursor * 8) +: 8]
    );
    low_post_alt_ext2 = decode_ext2_descriptor({
      record_i[(d0_i.post_alt_cursor * 8) +: 8],
      record_i[((d0_i.post_alt_cursor + 1) * 8) +: 8]
    });
    low_selected_ext1 = low_base_ext1;
    low_selected_ext2 = low_base_ext2;
    low_cursor = d0_i.base_cursor;
    if (d0_i.ea_layout == EA_LAYOUT_ALT_THEN_LOW) begin
      low_selected_ext1 = low_post_alt_ext1;
      low_selected_ext2 = low_post_alt_ext2;
      low_cursor = d0_i.post_alt_cursor;
    end
    low_payload_cursor = ea_payload_cursor(low_compact, low_cursor);
    alt_payload_cursor = ea_payload_cursor(
      alt_compact,
      d0_i.base_cursor
    );
    alt_descriptor_parse = resolve_ea_descriptor(
      d0_i.ea_profiles[BEDROCK_EA_ALT_SLOT],
      d0_i.ea_widths[BEDROCK_EA_ALT_SLOT],
      alt_compact,
      alt_base_ext1,
      alt_base_ext2,
      byte_count_i,
      d0_i.base_cursor
    );
    low_descriptor_parse = resolve_ea_descriptor(
      d0_i.ea_profiles[BEDROCK_EA_LOW_SLOT],
      d0_i.ea_widths[BEDROCK_EA_LOW_SLOT],
      low_compact,
      low_selected_ext1,
      low_selected_ext2,
      byte_count_i,
      low_cursor
    );
    alt_payload_parse = parse_ea_payload(
      alt_compact.ea,
      record_i,
      byte_count_i,
      alt_payload_cursor
    );
    low_payload_parse = parse_ea_payload(
      low_compact.ea,
      record_i,
      byte_count_i,
      low_payload_cursor
    );
    alt_parse = combine_ea_parse(alt_descriptor_parse, alt_payload_parse);
    low_parse = combine_ea_parse(low_descriptor_parse, low_payload_parse);
    if (d0_i.status == D0_SUCCESS) begin
      if (byte_count_i > BEDROCK_RECORD_BYTES) begin
        result_o.stage = D1_STAGE_RECORD_BOUNDS;
      end else begin
        if (low_parse.ok &&
            (d0_i.ea_layout != EA_LAYOUT_ALT_THEN_LOW || alt_parse.ok))
          result_o.eas[BEDROCK_EA_LOW_SLOT] = low_parse.ea;
        if (alt_parse.ok)
          result_o.eas[BEDROCK_EA_ALT_SLOT] = alt_parse.ea;
        unique case (d0_i.ea_layout)
        EA_LAYOUT_NONE: begin
          result_o.valid = 1'b1;
          result_o.stage = D1_STAGE_SUCCESS;
        end
        EA_LAYOUT_LOW: begin
          result_o.ea_count = 2'd1;
          result_o.required_bytes = low_parse.next_cursor;
          if (low_parse.ok) begin
            result_o.valid = 1'b1;
            result_o.stage = D1_STAGE_SUCCESS;
          end else begin
            result_o.stage = low_parse.stage;
          end
        end
        EA_LAYOUT_ALT: begin
          result_o.ea_count = 2'd1;
          result_o.required_bytes = alt_parse.next_cursor;
          if (alt_parse.ok) begin
            result_o.valid = 1'b1;
            result_o.stage = D1_STAGE_SUCCESS;
          end else begin
            result_o.stage = alt_parse.stage;
          end
        end
        EA_LAYOUT_ALT_THEN_LOW: begin
          result_o.ea_count = 2'd2;
          if (!alt_parse.ok) begin
            result_o.required_bytes = alt_parse.next_cursor;
            result_o.stage = alt_parse.stage;
          end else begin
            result_o.required_bytes = low_parse.next_cursor;
            if (!low_parse.ok) begin
              result_o.stage = low_parse.stage;
            end else begin
              result_o.valid = 1'b1;
              result_o.stage = D1_STAGE_SUCCESS;
            end
          end
        end
        endcase
      end
    end
  end
endmodule
