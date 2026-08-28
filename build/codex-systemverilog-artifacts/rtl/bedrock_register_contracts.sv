// Generated from canonical Bedrock ISA definitions. Do not edit.
module bedrock_register_contracts
  import bedrock_register_pkg::*;
(
  input  bedrock_register_group_e group_i,
  input  logic [15:0] encoding_i,
  input  logic [63:0] write_data_i,
  output logic valid_o,
  output logic [1:0] width_kind_o,
  output logic [15:0] fixed_width_o,
  output logic [63:0] writable_mask_o,
  output logic reserved_zero_o,
  output logic reset_known_o,
  output logic [63:0] reset_value_o
);
  always_comb begin
    valid_o = 1'b0;
    width_kind_o = '0;
    fixed_width_o = '0;
    writable_mask_o = '0;
    reset_known_o = 1'b0;
    reset_value_o = '0;
    unique case ({group_i, encoding_i})
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R0}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R1}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R2}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R3}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R4}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R5}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R6}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R7}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R8}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R9}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R10}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R11}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R12}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R13}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R14}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_GPR, REGISTER_BASE_GPR_R15}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_DS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_SS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_GS0}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_GS1}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_GS2}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_GS3}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_GS4}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_SEGMENT, REGISTER_BASE_SEGMENT_GS5}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_PTCR}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'h00fffffffffff081;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_ASCR}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'h00000000ffff0001;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_ECR}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'h0000000000000f81;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_UPC}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_USP}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_UCS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_UDS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_USS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_UCTL}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'h00000001ffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_UINFO}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'h00000000ffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_EPC}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_ECS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_EDS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_SSS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_SSP}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_ISS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_ISP}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_FSS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_FSP}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_DSS}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_DSP}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_BOOTPC}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b0; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_BOOTCFG}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b0; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_CONTROL, REGISTER_BASE_CONTROL_PMC}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'h0000000000000001;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_PERFORMANCE, REGISTER_BASE_PERFORMANCE_CYCLE}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_PERFORMANCE, REGISTER_BASE_PERFORMANCE_INSTRET}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_BASE_PERFORMANCE, REGISTER_BASE_PERFORMANCE_PTWALK}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F0}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F1}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F2}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F3}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F4}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F5}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F6}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F7}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F8}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F9}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F10}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F11}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F12}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F13}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F14}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_FP_FPR, REGISTER_FP_FPR_F15}: begin
        valid_o = 1'b1; width_kind_o = 2'd0;
        fixed_width_o = 16'd64; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V0}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V1}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V2}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V3}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V4}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V5}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V6}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V7}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V8}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V9}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V10}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V11}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V12}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V13}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V14}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V15}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V16}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V17}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V18}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V19}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V20}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V21}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V22}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V23}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V24}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V25}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V26}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V27}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V28}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V29}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V30}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_VECTOR, REGISTER_VECTOR_VECTOR_V31}: begin
        valid_o = 1'b1; width_kind_o = 2'd1;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P0}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P1}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P2}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P3}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P4}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P5}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P6}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P7}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P8}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P9}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P10}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P11}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P12}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P13}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P14}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      {REGISTER_GROUP_VECTOR_PREDICATE, REGISTER_VECTOR_PREDICATE_P15}: begin
        valid_o = 1'b1; width_kind_o = 2'd2;
        fixed_width_o = 16'd0; writable_mask_o = 64'hffffffffffffffff;
        reset_known_o = 1'b1; reset_value_o = 64'h0000000000000000;
      end
      default: begin end
    endcase
    reserved_zero_o = valid_o && ((write_data_i & ~writable_mask_o) == 64'b0);
  end
endmodule
