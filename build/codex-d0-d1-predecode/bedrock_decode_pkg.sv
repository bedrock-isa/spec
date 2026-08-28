// Generated from canonical Decode IR. Do not edit.
package bedrock_decode_pkg;
  localparam logic [9:0] BEDROCK_OPCODE_BITS = 10'd42;
  localparam logic [9:0] BEDROCK_RECORD_BYTES = 10'd18;
  localparam logic [9:0] BEDROCK_FORM_COUNT = 10'd697;
  localparam logic [9:0] BEDROCK_OPERAND_SLOTS = 10'd6;
  localparam logic [9:0] BEDROCK_EA_SLOTS = 10'd2;
  localparam logic [9:0] BEDROCK_SIZE_MASK_BITS = 10'd7;
  localparam logic [9:0] BEDROCK_CPUID_FLAG_MASK_BITS = 10'd3;
  localparam logic [9:0] BEDROCK_TOUCHED_FLAG_MASK_BITS = 10'd9;
  localparam logic [9:0] BEDROCK_POSSIBLE_EVENT_MASK_BITS = 10'd6;
  localparam logic [0:0] BEDROCK_EA_LOW_SLOT = 1'd0;
  localparam logic [0:0] BEDROCK_EA_ALT_SLOT = 1'd1;

  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_B = 7'h01; // bit 0: B
  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_D = 7'h02; // bit 1: D
  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_H = 7'h04; // bit 2: H
  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_L = 7'h08; // bit 3: L
  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_Q = 7'h10; // bit 4: Q
  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_S = 7'h20; // bit 5: S
  localparam logic [BEDROCK_SIZE_MASK_BITS-1:0] BEDROCK_SIZE_MASK_W = 7'h40; // bit 6: W
  localparam logic [BEDROCK_CPUID_FLAG_MASK_BITS-1:0] BEDROCK_CPUID_FLAG_MASK_FP = 3'h1; // bit 0: FP
  localparam logic [BEDROCK_CPUID_FLAG_MASK_BITS-1:0] BEDROCK_CPUID_FLAG_MASK_FPTRANSA = 3'h2; // bit 1: FPTRANSA
  localparam logic [BEDROCK_CPUID_FLAG_MASK_BITS-1:0] BEDROCK_CPUID_FLAG_MASK_VECTOR = 3'h4; // bit 2: VECTOR
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FFLAGS_DZ = 9'h001; // bit 0: FFLAGS.DZ
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FFLAGS_NV = 9'h002; // bit 1: FFLAGS.NV
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FFLAGS_NX = 9'h004; // bit 2: FFLAGS.NX
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FFLAGS_OF = 9'h008; // bit 3: FFLAGS.OF
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FFLAGS_UF = 9'h010; // bit 4: FFLAGS.UF
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FLAGS_C = 9'h020; // bit 5: FLAGS.C
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FLAGS_N = 9'h040; // bit 6: FLAGS.N
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FLAGS_V = 9'h080; // bit 7: FLAGS.V
  localparam logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] BEDROCK_TOUCHED_FLAG_MASK_FLAGS_Z = 9'h100; // bit 8: FLAGS.Z
  localparam logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] BEDROCK_POSSIBLE_EVENT_MASK_BREAKPOINT = 6'h01; // bit 0: BREAKPOINT
  localparam logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] BEDROCK_POSSIBLE_EVENT_MASK_DIVIDE_ERROR = 6'h02; // bit 1: DIVIDE_ERROR
  localparam logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] BEDROCK_POSSIBLE_EVENT_MASK_FLOATING_POINT_FAULT = 6'h04; // bit 2: FLOATING_POINT_FAULT
  localparam logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] BEDROCK_POSSIBLE_EVENT_MASK_ILLEGAL_INSTRUCTION = 6'h08; // bit 3: ILLEGAL_INSTRUCTION
  localparam logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] BEDROCK_POSSIBLE_EVENT_MASK_INVALID_CONTROL_STATE = 6'h10; // bit 4: INVALID_CONTROL_STATE
  localparam logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] BEDROCK_POSSIBLE_EVENT_MASK_VECTOR_RANGE_ERROR = 6'h20; // bit 5: VECTOR_RANGE_ERROR

  typedef enum logic [1:0] {
    D0_INVALID_INPUT = 2'd0,
    D0_UNALLOCATED_OPCODE = 2'd1,
    D0_CONSTRAINT_REJECTED = 2'd2,
    D0_SUCCESS = 2'd3
  } d0_status_e;

  typedef enum logic [3:0] {
    D1_STAGE_D0_REJECTED = 4'd0,
    D1_STAGE_RECORD_BOUNDS = 4'd1,
    D1_STAGE_EA_DESCRIPTOR = 4'd2,
    D1_STAGE_EA_PAYLOAD = 4'd3,
    D1_STAGE_STANDALONE_PAYLOAD = 4'd4,
    D1_STAGE_STATIC_LEGALITY = 4'd5,
    D1_STAGE_RECORD_LENGTH = 4'd6,
    D1_STAGE_SUCCESS = 4'd7
  } decode_stage_e;

  typedef enum logic [1:0] {
    EA_LAYOUT_NONE = 2'd0,
    EA_LAYOUT_LOW = 2'd1,
    EA_LAYOUT_ALT = 2'd2,
    EA_LAYOUT_ALT_THEN_LOW = 2'd3
  } ea_layout_e;



  typedef enum logic [2:0] {
    OPCODE_CLASS_INVALID = 3'd0,
    // extrashort
    OPCODE_CLASS_EXTRASHORT = 3'd1,
    // short
    OPCODE_CLASS_SHORT = 3'd2,
    // medium
    OPCODE_CLASS_MEDIUM = 3'd3,
    // long
    OPCODE_CLASS_LONG = 3'd4,
    // extralong
    OPCODE_CLASS_EXTRALONG = 3'd5,
    // xxlong
    OPCODE_CLASS_XXLONG = 3'd6
  } opcode_class_e;

  typedef enum logic [1:0] {
    OPERATOR_SPACE_NONE = 2'd0,
    // base
    OPERATOR_SPACE_BASE = 2'd1,
    // fpu
    OPERATOR_SPACE_FPU = 2'd2,
    // vector
    OPERATOR_SPACE_VECTOR = 2'd3
  } operator_space_e;

  typedef enum logic [9:0] {
    FORM_INVALID = 10'd0,
    // extralong.bndsii_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDSII_X_RN_L_EA_E_RN_H = 10'd1,
    // extralong.bndsii_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDSII_X_RN_L_RN_V_RN_H = 10'd2,
    // extralong.bndsix_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDSIX_X_RN_L_EA_E_RN_H = 10'd3,
    // extralong.bndsix_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDSIX_X_RN_L_RN_V_RN_H = 10'd4,
    // extralong.bndsxi_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDSXI_X_RN_L_EA_E_RN_H = 10'd5,
    // extralong.bndsxi_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDSXI_X_RN_L_RN_V_RN_H = 10'd6,
    // extralong.bndsxx_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDSXX_X_RN_L_EA_E_RN_H = 10'd7,
    // extralong.bndsxx_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDSXX_X_RN_L_RN_V_RN_H = 10'd8,
    // extralong.bnduii_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDUII_X_RN_L_EA_E_RN_H = 10'd9,
    // extralong.bnduii_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDUII_X_RN_L_RN_V_RN_H = 10'd10,
    // extralong.bnduix_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDUIX_X_RN_L_EA_E_RN_H = 10'd11,
    // extralong.bnduix_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDUIX_X_RN_L_RN_V_RN_H = 10'd12,
    // extralong.bnduxi_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDUXI_X_RN_L_EA_E_RN_H = 10'd13,
    // extralong.bnduxi_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDUXI_X_RN_L_RN_V_RN_H = 10'd14,
    // extralong.bnduxx_x_rn_l_ea_e_rn_h
    FORM_EXTRALONG_BNDUXX_X_RN_L_EA_E_RN_H = 10'd15,
    // extralong.bnduxx_x_rn_l_rn_v_rn_h
    FORM_EXTRALONG_BNDUXX_X_RN_L_RN_V_RN_H = 10'd16,
    // extralong.cmpxchg_x_order_o_rn_x_rn_d_ea_e
    FORM_EXTRALONG_CMPXCHG_X_ORDER_O_RN_X_RN_D_EA_E = 10'd17,
    // extralong.divmods_x_ea_e_rn_q_rn_r
    FORM_EXTRALONG_DIVMODS_X_EA_E_RN_Q_RN_R = 10'd18,
    // extralong.divmods_x_rn_e_rn_q_rn_r
    FORM_EXTRALONG_DIVMODS_X_RN_E_RN_Q_RN_R = 10'd19,
    // extralong.divmodu_x_ea_e_rn_q_rn_r
    FORM_EXTRALONG_DIVMODU_X_EA_E_RN_Q_RN_R = 10'd20,
    // extralong.divmodu_x_rn_e_rn_q_rn_r
    FORM_EXTRALONG_DIVMODU_X_RN_E_RN_Q_RN_R = 10'd21,
    // extralong.extract_x_imm7_i_rn_h_rn_l
    FORM_EXTRALONG_EXTRACT_X_IMM7_I_RN_H_RN_L = 10'd22,
    // extralong.fbndii_x_ea_l_fn_v_ea_h
    FORM_EXTRALONG_FBNDII_X_EA_L_FN_V_EA_H = 10'd23,
    // extralong.fbndii_x_fn_l_ea_v_fn_h
    FORM_EXTRALONG_FBNDII_X_FN_L_EA_V_FN_H = 10'd24,
    // extralong.fbndii_x_fn_l_fn_v_fn_h
    FORM_EXTRALONG_FBNDII_X_FN_L_FN_V_FN_H = 10'd25,
    // extralong.fbndix_x_ea_l_fn_v_ea_h
    FORM_EXTRALONG_FBNDIX_X_EA_L_FN_V_EA_H = 10'd26,
    // extralong.fbndix_x_fn_l_ea_v_fn_h
    FORM_EXTRALONG_FBNDIX_X_FN_L_EA_V_FN_H = 10'd27,
    // extralong.fbndix_x_fn_l_fn_v_fn_h
    FORM_EXTRALONG_FBNDIX_X_FN_L_FN_V_FN_H = 10'd28,
    // extralong.fbndxi_x_ea_l_fn_v_ea_h
    FORM_EXTRALONG_FBNDXI_X_EA_L_FN_V_EA_H = 10'd29,
    // extralong.fbndxi_x_fn_l_ea_v_fn_h
    FORM_EXTRALONG_FBNDXI_X_FN_L_EA_V_FN_H = 10'd30,
    // extralong.fbndxi_x_fn_l_fn_v_fn_h
    FORM_EXTRALONG_FBNDXI_X_FN_L_FN_V_FN_H = 10'd31,
    // extralong.fbndxx_x_ea_l_fn_v_ea_h
    FORM_EXTRALONG_FBNDXX_X_EA_L_FN_V_EA_H = 10'd32,
    // extralong.fbndxx_x_fn_l_ea_v_fn_h
    FORM_EXTRALONG_FBNDXX_X_FN_L_EA_V_FN_H = 10'd33,
    // extralong.fbndxx_x_fn_l_fn_v_fn_h
    FORM_EXTRALONG_FBNDXX_X_FN_L_FN_V_FN_H = 10'd34,
    // extralong.fetchadd_x_order_o_rn_s_ea_e
    FORM_EXTRALONG_FETCHADD_X_ORDER_O_RN_S_EA_E = 10'd35,
    // extralong.fetchand_x_order_o_rn_s_ea_e
    FORM_EXTRALONG_FETCHAND_X_ORDER_O_RN_S_EA_E = 10'd36,
    // extralong.fetchor_x_order_o_rn_s_ea_e
    FORM_EXTRALONG_FETCHOR_X_ORDER_O_RN_S_EA_E = 10'd37,
    // extralong.fetchsub_x_order_o_rn_s_ea_e
    FORM_EXTRALONG_FETCHSUB_X_ORDER_O_RN_S_EA_E = 10'd38,
    // extralong.fetchxor_x_order_o_rn_s_ea_e
    FORM_EXTRALONG_FETCHXOR_X_ORDER_O_RN_S_EA_E = 10'd39,
    // extralong.fmadd_x_ea_l_fn_r_fn_d
    FORM_EXTRALONG_FMADD_X_EA_L_FN_R_FN_D = 10'd40,
    // extralong.fmadd_x_fn_l_ea_r_fn_d
    FORM_EXTRALONG_FMADD_X_FN_L_EA_R_FN_D = 10'd41,
    // extralong.fmsub_x_ea_l_fn_r_fn_d
    FORM_EXTRALONG_FMSUB_X_EA_L_FN_R_FN_D = 10'd42,
    // extralong.fmsub_x_fn_l_ea_r_fn_d
    FORM_EXTRALONG_FMSUB_X_FN_L_EA_R_FN_D = 10'd43,
    // extralong.fnmadd_x_ea_l_fn_r_fn_d
    FORM_EXTRALONG_FNMADD_X_EA_L_FN_R_FN_D = 10'd44,
    // extralong.fnmadd_x_fn_l_ea_r_fn_d
    FORM_EXTRALONG_FNMADD_X_FN_L_EA_R_FN_D = 10'd45,
    // extralong.fnmsub_x_ea_l_fn_r_fn_d
    FORM_EXTRALONG_FNMSUB_X_EA_L_FN_R_FN_D = 10'd46,
    // extralong.fnmsub_x_fn_l_ea_r_fn_d
    FORM_EXTRALONG_FNMSUB_X_FN_L_EA_R_FN_D = 10'd47,
    // extralong.ijcc_rn_i_rn_b_ea_e
    FORM_EXTRALONG_IJCC_RN_I_RN_B_EA_E = 10'd48,
    // extralong.ijcc_rn_i_rn_b_rn_e
    FORM_EXTRALONG_IJCC_RN_I_RN_B_RN_E = 10'd49,
    // extralong.movcc_x_ea_e_rn_d
    FORM_EXTRALONG_MOVCC_X_EA_E_RN_D = 10'd50,
    // extralong.movcc_x_rn_s_ea_e
    FORM_EXTRALONG_MOVCC_X_RN_S_EA_E = 10'd51,
    // extralong.psel.v129
    FORM_EXTRALONG_PSEL_V129 = 10'd52,
    // extralong.pslice.v136
    FORM_EXTRALONG_PSLICE_V136 = 10'd53,
    // extralong.ptrnhi.v135
    FORM_EXTRALONG_PTRNHI_V135 = 10'd54,
    // extralong.ptrnlo.v134
    FORM_EXTRALONG_PTRNLO_V134 = 10'd55,
    // extralong.puziphi.v133
    FORM_EXTRALONG_PUZIPHI_V133 = 10'd56,
    // extralong.puziplo.v132
    FORM_EXTRALONG_PUZIPLO_V132 = 10'd57,
    // extralong.pziphi.v131
    FORM_EXTRALONG_PZIPHI_V131 = 10'd58,
    // extralong.pziplo.v130
    FORM_EXTRALONG_PZIPLO_V130 = 10'd59,
    // extralong.vadd.v50
    FORM_EXTRALONG_VADD_V50 = 10'd60,
    // extralong.vand.v53
    FORM_EXTRALONG_VAND_V53 = 10'd61,
    // extralong.vcmpcc.v47.fp
    FORM_EXTRALONG_VCMPCC_V47_FP = 10'd62,
    // extralong.vcmpcc.v47.integer
    FORM_EXTRALONG_VCMPCC_V47_INTEGER = 10'd63,
    // extralong.vcopysign.v71
    FORM_EXTRALONG_VCOPYSIGN_V71 = 10'd64,
    // extralong.vcvtd.v82
    FORM_EXTRALONG_VCVTD_V82 = 10'd65,
    // extralong.vcvtd.v85
    FORM_EXTRALONG_VCVTD_V85 = 10'd66,
    // extralong.vcvth.v100
    FORM_EXTRALONG_VCVTH_V100 = 10'd67,
    // extralong.vcvth.v99
    FORM_EXTRALONG_VCVTH_V99 = 10'd68,
    // extralong.vcvtl.v87
    FORM_EXTRALONG_VCVTL_V87 = 10'd69,
    // extralong.vcvtq.v89
    FORM_EXTRALONG_VCVTQ_V89 = 10'd70,
    // extralong.vcvts.v81
    FORM_EXTRALONG_VCVTS_V81 = 10'd71,
    // extralong.vcvts.v83
    FORM_EXTRALONG_VCVTS_V83 = 10'd72,
    // extralong.vcvtud.v86
    FORM_EXTRALONG_VCVTUD_V86 = 10'd73,
    // extralong.vcvtuh.v101
    FORM_EXTRALONG_VCVTUH_V101 = 10'd74,
    // extralong.vcvtul.v88
    FORM_EXTRALONG_VCVTUL_V88 = 10'd75,
    // extralong.vcvtuq.v90
    FORM_EXTRALONG_VCVTUQ_V90 = 10'd76,
    // extralong.vcvtus.v84
    FORM_EXTRALONG_VCVTUS_V84 = 10'd77,
    // extralong.vdiv.v70
    FORM_EXTRALONG_VDIV_V70 = 10'd78,
    // extralong.vextract.v114
    FORM_EXTRALONG_VEXTRACT_V114 = 10'd79,
    // extralong.vextract.v116
    FORM_EXTRALONG_VEXTRACT_V116 = 10'd80,
    // extralong.vextsl.v75
    FORM_EXTRALONG_VEXTSL_V75 = 10'd81,
    // extralong.vextsq.v77
    FORM_EXTRALONG_VEXTSQ_V77 = 10'd82,
    // extralong.vextsw.v73
    FORM_EXTRALONG_VEXTSW_V73 = 10'd83,
    // extralong.vextzl.v74
    FORM_EXTRALONG_VEXTZL_V74 = 10'd84,
    // extralong.vextzq.v76
    FORM_EXTRALONG_VEXTZQ_V76 = 10'd85,
    // extralong.vextzw.v72
    FORM_EXTRALONG_VEXTZW_V72 = 10'd86,
    // extralong.vinsert.v115
    FORM_EXTRALONG_VINSERT_V115 = 10'd87,
    // extralong.vinsert.v117
    FORM_EXTRALONG_VINSERT_V117 = 10'd88,
    // extralong.vmadd.v102
    FORM_EXTRALONG_VMADD_V102 = 10'd89,
    // extralong.vmax.v69
    FORM_EXTRALONG_VMAX_V69 = 10'd90,
    // extralong.vmaxs.v58
    FORM_EXTRALONG_VMAXS_V58 = 10'd91,
    // extralong.vmaxu.v59
    FORM_EXTRALONG_VMAXU_V59 = 10'd92,
    // extralong.vmin.v68
    FORM_EXTRALONG_VMIN_V68 = 10'd93,
    // extralong.vmins.v56
    FORM_EXTRALONG_VMINS_V56 = 10'd94,
    // extralong.vminu.v57
    FORM_EXTRALONG_VMINU_V57 = 10'd95,
    // extralong.vmov.v91
    FORM_EXTRALONG_VMOV_V91 = 10'd96,
    // extralong.vmsub.v103
    FORM_EXTRALONG_VMSUB_V103 = 10'd97,
    // extralong.vmul.v52
    FORM_EXTRALONG_VMUL_V52 = 10'd98,
    // extralong.vmulhs.v60
    FORM_EXTRALONG_VMULHS_V60 = 10'd99,
    // extralong.vmulhsu.v62
    FORM_EXTRALONG_VMULHSU_V62 = 10'd100,
    // extralong.vmulhu.v61
    FORM_EXTRALONG_VMULHU_V61 = 10'd101,
    // extralong.vnmadd.v104
    FORM_EXTRALONG_VNMADD_V104 = 10'd102,
    // extralong.vnmsub.v105
    FORM_EXTRALONG_VNMSUB_V105 = 10'd103,
    // extralong.vor.v54
    FORM_EXTRALONG_VOR_V54 = 10'd104,
    // extralong.vperm.v92
    FORM_EXTRALONG_VPERM_V92 = 10'd105,
    // extralong.vredadd.v118
    FORM_EXTRALONG_VREDADD_V118 = 10'd106,
    // extralong.vredadd.v126
    FORM_EXTRALONG_VREDADD_V126 = 10'd107,
    // extralong.vredand.v123
    FORM_EXTRALONG_VREDAND_V123 = 10'd108,
    // extralong.vredmax.v128
    FORM_EXTRALONG_VREDMAX_V128 = 10'd109,
    // extralong.vredmaxs.v121
    FORM_EXTRALONG_VREDMAXS_V121 = 10'd110,
    // extralong.vredmaxu.v122
    FORM_EXTRALONG_VREDMAXU_V122 = 10'd111,
    // extralong.vredmin.v127
    FORM_EXTRALONG_VREDMIN_V127 = 10'd112,
    // extralong.vredmins.v119
    FORM_EXTRALONG_VREDMINS_V119 = 10'd113,
    // extralong.vredminu.v120
    FORM_EXTRALONG_VREDMINU_V120 = 10'd114,
    // extralong.vredor.v124
    FORM_EXTRALONG_VREDOR_V124 = 10'd115,
    // extralong.vredxor.v125
    FORM_EXTRALONG_VREDXOR_V125 = 10'd116,
    // extralong.vrol.v110
    FORM_EXTRALONG_VROL_V110 = 10'd117,
    // extralong.vrol.v66
    FORM_EXTRALONG_VROL_V66 = 10'd118,
    // extralong.vror.v111
    FORM_EXTRALONG_VROR_V111 = 10'd119,
    // extralong.vror.v67
    FORM_EXTRALONG_VROR_V67 = 10'd120,
    // extralong.vsar.v109
    FORM_EXTRALONG_VSAR_V109 = 10'd121,
    // extralong.vsar.v65
    FORM_EXTRALONG_VSAR_V65 = 10'd122,
    // extralong.vshl.v107
    FORM_EXTRALONG_VSHL_V107 = 10'd123,
    // extralong.vshl.v63
    FORM_EXTRALONG_VSHL_V63 = 10'd124,
    // extralong.vshr.v108
    FORM_EXTRALONG_VSHR_V108 = 10'd125,
    // extralong.vshr.v64
    FORM_EXTRALONG_VSHR_V64 = 10'd126,
    // extralong.vslice.v106
    FORM_EXTRALONG_VSLICE_V106 = 10'd127,
    // extralong.vslidedn.v113
    FORM_EXTRALONG_VSLIDEDN_V113 = 10'd128,
    // extralong.vslideup.v112
    FORM_EXTRALONG_VSLIDEUP_V112 = 10'd129,
    // extralong.vsub.v51
    FORM_EXTRALONG_VSUB_V51 = 10'd130,
    // extralong.vtestnz.v49
    FORM_EXTRALONG_VTESTNZ_V49 = 10'd131,
    // extralong.vtestz.v48
    FORM_EXTRALONG_VTESTZ_V48 = 10'd132,
    // extralong.vtrnhi.v98
    FORM_EXTRALONG_VTRNHI_V98 = 10'd133,
    // extralong.vtrnlo.v97
    FORM_EXTRALONG_VTRNLO_V97 = 10'd134,
    // extralong.vtruncb.v78
    FORM_EXTRALONG_VTRUNCB_V78 = 10'd135,
    // extralong.vtruncl.v80
    FORM_EXTRALONG_VTRUNCL_V80 = 10'd136,
    // extralong.vtruncw.v79
    FORM_EXTRALONG_VTRUNCW_V79 = 10'd137,
    // extralong.vuziphi.v96
    FORM_EXTRALONG_VUZIPHI_V96 = 10'd138,
    // extralong.vuziplo.v95
    FORM_EXTRALONG_VUZIPLO_V95 = 10'd139,
    // extralong.vxor.v55
    FORM_EXTRALONG_VXOR_V55 = 10'd140,
    // extralong.vziphi.v94
    FORM_EXTRALONG_VZIPHI_V94 = 10'd141,
    // extralong.vziplo.v93
    FORM_EXTRALONG_VZIPLO_V93 = 10'd142,
    // extrashort.add_q_8_sp
    FORM_EXTRASHORT_ADD_Q_8_SP = 10'd143,
    // extrashort.afence
    FORM_EXTRASHORT_AFENCE = 10'd144,
    // extrashort.bkpt
    FORM_EXTRASHORT_BKPT = 10'd145,
    // extrashort.clr_q_rn_r
    FORM_EXTRASHORT_CLR_Q_RN_R = 10'd146,
    // extrashort.eret
    FORM_EXTRASHORT_ERET = 10'd147,
    // extrashort.fpopp_pair_id_i
    FORM_EXTRASHORT_FPOPP_PAIR_ID_I = 10'd148,
    // extrashort.fpushp_pair_id_i
    FORM_EXTRASHORT_FPUSHP_PAIR_ID_I = 10'd149,
    // extrashort.illegal
    FORM_EXTRASHORT_ILLEGAL = 10'd150,
    // extrashort.lret
    FORM_EXTRASHORT_LRET = 10'd151,
    // extrashort.mov_q_rn_r_sp
    FORM_EXTRASHORT_MOV_Q_RN_R_SP = 10'd152,
    // extrashort.mov_q_sp_rn_r
    FORM_EXTRASHORT_MOV_Q_SP_RN_R = 10'd153,
    // extrashort.nop
    FORM_EXTRASHORT_NOP = 10'd154,
    // extrashort.pop_rn_r
    FORM_EXTRASHORT_POP_RN_R = 10'd155,
    // extrashort.popp_pair_id_i
    FORM_EXTRASHORT_POPP_PAIR_ID_I = 10'd156,
    // extrashort.push_cs
    FORM_EXTRASHORT_PUSH_CS = 10'd157,
    // extrashort.push_rn_r
    FORM_EXTRASHORT_PUSH_RN_R = 10'd158,
    // extrashort.pushp_pair_id_i
    FORM_EXTRASHORT_PUSHP_PAIR_ID_I = 10'd159,
    // extrashort.ret
    FORM_EXTRASHORT_RET = 10'd160,
    // extrashort.rfence
    FORM_EXTRASHORT_RFENCE = 10'd161,
    // extrashort.sub_q_8_sp
    FORM_EXTRASHORT_SUB_Q_8_SP = 10'd162,
    // extrashort.syscall
    FORM_EXTRASHORT_SYSCALL = 10'd163,
    // extrashort.wait
    FORM_EXTRASHORT_WAIT = 10'd164,
    // extrashort.wfence
    FORM_EXTRASHORT_WFENCE = 10'd165,
    // extrashort.yield
    FORM_EXTRASHORT_YIELD = 10'd166,
    // long.adc_x_ea_e_rn_s
    FORM_LONG_ADC_X_EA_E_RN_S = 10'd167,
    // long.adc_x_rn_s_ea_e
    FORM_LONG_ADC_X_RN_S_EA_E = 10'd168,
    // long.bchg_imm6_i_ea_e
    FORM_LONG_BCHG_IMM6_I_EA_E = 10'd169,
    // long.bchg_imm6_i_rn_e
    FORM_LONG_BCHG_IMM6_I_RN_E = 10'd170,
    // long.bchg_rn_b_ea_e
    FORM_LONG_BCHG_RN_B_EA_E = 10'd171,
    // long.bclr_imm6_i_ea_e
    FORM_LONG_BCLR_IMM6_I_EA_E = 10'd172,
    // long.bclr_imm6_i_rn_e
    FORM_LONG_BCLR_IMM6_I_RN_E = 10'd173,
    // long.bclr_rn_b_ea_e
    FORM_LONG_BCLR_RN_B_EA_E = 10'd174,
    // long.bpall.v28
    FORM_LONG_BPALL_V28 = 10'd175,
    // long.bpany.v26
    FORM_LONG_BPANY_V26 = 10'd176,
    // long.bpnone.v27
    FORM_LONG_BPNONE_V27 = 10'd177,
    // long.bset_imm6_i_ea_e
    FORM_LONG_BSET_IMM6_I_EA_E = 10'd178,
    // long.bset_imm6_i_rn_e
    FORM_LONG_BSET_IMM6_I_RN_E = 10'd179,
    // long.bset_rn_b_ea_e
    FORM_LONG_BSET_RN_B_EA_E = 10'd180,
    // long.btest_imm6_i_ea_e
    FORM_LONG_BTEST_IMM6_I_EA_E = 10'd181,
    // long.btest_imm6_i_rn_e
    FORM_LONG_BTEST_IMM6_I_RN_E = 10'd182,
    // long.btest_rn_b_ea_e
    FORM_LONG_BTEST_RN_B_EA_E = 10'd183,
    // long.callcc_ea_e
    FORM_LONG_CALLCC_EA_E = 10'd184,
    // long.callcc_rn
    FORM_LONG_CALLCC_RN = 10'd185,
    // long.clmul_x_ea_e_rn_d
    FORM_LONG_CLMUL_X_EA_E_RN_D = 10'd186,
    // long.clmulh_q_ea_e_rn_d
    FORM_LONG_CLMULH_Q_EA_E_RN_D = 10'd187,
    // long.cls_x_ea_e_rn_d
    FORM_LONG_CLS_X_EA_E_RN_D = 10'd188,
    // long.clz_x_ea_e_rn_d
    FORM_LONG_CLZ_X_EA_E_RN_D = 10'd189,
    // long.cmp_x_ea_s_ea_d
    FORM_LONG_CMP_X_EA_S_EA_D = 10'd190,
    // long.cmpjcc_x_rn_s_rn_d_imm16s
    FORM_LONG_CMPJCC_X_RN_S_RN_D_IMM16S = 10'd191,
    // long.cmpjcc_x_rn_s_rn_d_imm8s
    FORM_LONG_CMPJCC_X_RN_S_RN_D_IMM8S = 10'd192,
    // long.cts_x_ea_e_rn_d
    FORM_LONG_CTS_X_EA_E_RN_D = 10'd193,
    // long.ctz_x_ea_e_rn_d
    FORM_LONG_CTZ_X_EA_E_RN_D = 10'd194,
    // long.divs_x_ea_e_rn_d
    FORM_LONG_DIVS_X_EA_E_RN_D = 10'd195,
    // long.divu_x_ea_e_rn_d
    FORM_LONG_DIVU_X_EA_E_RN_D = 10'd196,
    // long.djcc_rn_r_ea_e
    FORM_LONG_DJCC_RN_R_EA_E = 10'd197,
    // long.djcc_rn_r_rn_e
    FORM_LONG_DJCC_RN_R_RN_E = 10'd198,
    // long.extsl_b_rn_s_ea_e
    FORM_LONG_EXTSL_B_RN_S_EA_E = 10'd199,
    // long.extsl_w_rn_s_ea_e
    FORM_LONG_EXTSL_W_RN_S_EA_E = 10'd200,
    // long.extsl_x_ea_s_ea_d
    FORM_LONG_EXTSL_X_EA_S_EA_D = 10'd201,
    // long.extsq_b_ea_s_ea_d
    FORM_LONG_EXTSQ_B_EA_S_EA_D = 10'd202,
    // long.extsq_b_rn_s_ea_e
    FORM_LONG_EXTSQ_B_RN_S_EA_E = 10'd203,
    // long.extsq_l_ea_s_ea_d
    FORM_LONG_EXTSQ_L_EA_S_EA_D = 10'd204,
    // long.extsq_l_rn_s_ea_e
    FORM_LONG_EXTSQ_L_RN_S_EA_E = 10'd205,
    // long.extsq_w_ea_s_ea_d
    FORM_LONG_EXTSQ_W_EA_S_EA_D = 10'd206,
    // long.extsq_w_rn_s_ea_e
    FORM_LONG_EXTSQ_W_RN_S_EA_E = 10'd207,
    // long.extsw_b_ea_s_ea_d
    FORM_LONG_EXTSW_B_EA_S_EA_D = 10'd208,
    // long.extsw_b_rn_s_ea_e
    FORM_LONG_EXTSW_B_RN_S_EA_E = 10'd209,
    // long.extzl_b_rn_s_ea_e
    FORM_LONG_EXTZL_B_RN_S_EA_E = 10'd210,
    // long.extzl_w_rn_s_ea_e
    FORM_LONG_EXTZL_W_RN_S_EA_E = 10'd211,
    // long.extzl_x_ea_s_ea_d
    FORM_LONG_EXTZL_X_EA_S_EA_D = 10'd212,
    // long.extzq_b_ea_s_ea_d
    FORM_LONG_EXTZQ_B_EA_S_EA_D = 10'd213,
    // long.extzq_b_rn_s_ea_e
    FORM_LONG_EXTZQ_B_RN_S_EA_E = 10'd214,
    // long.extzq_l_ea_s_ea_d
    FORM_LONG_EXTZQ_L_EA_S_EA_D = 10'd215,
    // long.extzq_l_rn_s_ea_e
    FORM_LONG_EXTZQ_L_RN_S_EA_E = 10'd216,
    // long.extzq_w_ea_s_ea_d
    FORM_LONG_EXTZQ_W_EA_S_EA_D = 10'd217,
    // long.extzq_w_rn_s_ea_e
    FORM_LONG_EXTZQ_W_RN_S_EA_E = 10'd218,
    // long.extzw_b_ea_s_ea_d
    FORM_LONG_EXTZW_B_EA_S_EA_D = 10'd219,
    // long.extzw_b_rn_s_ea_e
    FORM_LONG_EXTZW_B_RN_S_EA_E = 10'd220,
    // long.fabs_x_ea_s_fn_d
    FORM_LONG_FABS_X_EA_S_FN_D = 10'd221,
    // long.fabs_x_fn_s_ea_d
    FORM_LONG_FABS_X_FN_S_EA_D = 10'd222,
    // long.facosa_x_fn_s_fn_d
    FORM_LONG_FACOSA_X_FN_S_FN_D = 10'd223,
    // long.fadd_x_ea_s_fn_d
    FORM_LONG_FADD_X_EA_S_FN_D = 10'd224,
    // long.fasina_x_fn_s_fn_d
    FORM_LONG_FASINA_X_FN_S_FN_D = 10'd225,
    // long.fatana_x_fn_s_fn_d
    FORM_LONG_FATANA_X_FN_S_FN_D = 10'd226,
    // long.fatanha_x_fn_s_fn_d
    FORM_LONG_FATANHA_X_FN_S_FN_D = 10'd227,
    // long.fceil_x_ea_s_fn_d
    FORM_LONG_FCEIL_X_EA_S_FN_D = 10'd228,
    // long.fceil_x_fn_s_ea_d
    FORM_LONG_FCEIL_X_FN_S_EA_D = 10'd229,
    // long.fclass_x_fn_s_rn_d
    FORM_LONG_FCLASS_X_FN_S_RN_D = 10'd230,
    // long.fcmp_x_ea_s_fn_d
    FORM_LONG_FCMP_X_EA_S_FN_D = 10'd231,
    // long.fcopysign_x_fn_s_fn_m_fn_d
    FORM_LONG_FCOPYSIGN_X_FN_S_FN_M_FN_D = 10'd232,
    // long.fcosa_x_fn_s_fn_d
    FORM_LONG_FCOSA_X_FN_S_FN_D = 10'd233,
    // long.fcosha_x_fn_s_fn_d
    FORM_LONG_FCOSHA_X_FN_S_FN_D = 10'd234,
    // long.fcvt_x_fn_s_rn_d
    FORM_LONG_FCVT_X_FN_S_RN_D = 10'd235,
    // long.fcvt_x_rn_s_fn_d
    FORM_LONG_FCVT_X_RN_S_FN_D = 10'd236,
    // long.fcvtu_x_fn_s_rn_d
    FORM_LONG_FCVTU_X_FN_S_RN_D = 10'd237,
    // long.fcvtu_x_rn_s_fn_d
    FORM_LONG_FCVTU_X_RN_S_FN_D = 10'd238,
    // long.fdiv_x_ea_s_fn_d
    FORM_LONG_FDIV_X_EA_S_FN_D = 10'd239,
    // long.fetoxa_x_fn_s_fn_d
    FORM_LONG_FETOXA_X_FN_S_FN_D = 10'd240,
    // long.fetoxm1a_x_fn_s_fn_d
    FORM_LONG_FETOXM1A_X_FN_S_FN_D = 10'd241,
    // long.ffloor_x_ea_s_fn_d
    FORM_LONG_FFLOOR_X_EA_S_FN_D = 10'd242,
    // long.ffloor_x_fn_s_ea_d
    FORM_LONG_FFLOOR_X_FN_S_EA_D = 10'd243,
    // long.fgetexp_x_ea_s_fn_d
    FORM_LONG_FGETEXP_X_EA_S_FN_D = 10'd244,
    // long.fgetman_x_ea_s_fn_d
    FORM_LONG_FGETMAN_X_EA_S_FN_D = 10'd245,
    // long.fint_x_ea_s_fn_d
    FORM_LONG_FINT_X_EA_S_FN_D = 10'd246,
    // long.fint_x_fn_s_ea_d
    FORM_LONG_FINT_X_FN_S_EA_D = 10'd247,
    // long.fintrz_x_ea_s_fn_d
    FORM_LONG_FINTRZ_X_EA_S_FN_D = 10'd248,
    // long.fintrz_x_fn_s_ea_d
    FORM_LONG_FINTRZ_X_FN_S_EA_D = 10'd249,
    // long.flog10a_x_fn_s_fn_d
    FORM_LONG_FLOG10A_X_FN_S_FN_D = 10'd250,
    // long.flog2a_x_fn_s_fn_d
    FORM_LONG_FLOG2A_X_FN_S_FN_D = 10'd251,
    // long.flogna_x_fn_s_fn_d
    FORM_LONG_FLOGNA_X_FN_S_FN_D = 10'd252,
    // long.flognp1a_x_fn_s_fn_d
    FORM_LONG_FLOGNP1A_X_FN_S_FN_D = 10'd253,
    // long.fmadd_x_fn_l_fn_r_fn_d
    FORM_LONG_FMADD_X_FN_L_FN_R_FN_D = 10'd254,
    // long.fmax_x_ea_s_fn_d
    FORM_LONG_FMAX_X_EA_S_FN_D = 10'd255,
    // long.fmin_x_ea_s_fn_d
    FORM_LONG_FMIN_X_EA_S_FN_D = 10'd256,
    // long.fmod_x_ea_s_fn_d
    FORM_LONG_FMOD_X_EA_S_FN_D = 10'd257,
    // long.fmov_x_ea_s_fn_d
    FORM_LONG_FMOV_X_EA_S_FN_D = 10'd258,
    // long.fmov_x_fn_s_ea_d
    FORM_LONG_FMOV_X_FN_S_EA_D = 10'd259,
    // long.fmovcc_fn_s_fn_d
    FORM_LONG_FMOVCC_FN_S_FN_D = 10'd260,
    // long.fmovcc_x_ea_s_fn_d
    FORM_LONG_FMOVCC_X_EA_S_FN_D = 10'd261,
    // long.fmovcc_x_fn_s_ea_d
    FORM_LONG_FMOVCC_X_FN_S_EA_D = 10'd262,
    // long.fmsub_x_fn_l_fn_r_fn_d
    FORM_LONG_FMSUB_X_FN_L_FN_R_FN_D = 10'd263,
    // long.fmul_x_ea_s_fn_d
    FORM_LONG_FMUL_X_EA_S_FN_D = 10'd264,
    // long.fneg_x_ea_s_fn_d
    FORM_LONG_FNEG_X_EA_S_FN_D = 10'd265,
    // long.fneg_x_fn_s_ea_d
    FORM_LONG_FNEG_X_FN_S_EA_D = 10'd266,
    // long.fnmadd_x_fn_l_fn_r_fn_d
    FORM_LONG_FNMADD_X_FN_L_FN_R_FN_D = 10'd267,
    // long.fnmsub_x_fn_l_fn_r_fn_d
    FORM_LONG_FNMSUB_X_FN_L_FN_R_FN_D = 10'd268,
    // long.frem_x_ea_s_fn_d
    FORM_LONG_FREM_X_EA_S_FN_D = 10'd269,
    // long.fround_x_ea_s_fn_d
    FORM_LONG_FROUND_X_EA_S_FN_D = 10'd270,
    // long.fround_x_fn_s_ea_d
    FORM_LONG_FROUND_X_FN_S_EA_D = 10'd271,
    // long.fscale_x_ea_s_fn_d
    FORM_LONG_FSCALE_X_EA_S_FN_D = 10'd272,
    // long.fsina_x_fn_s_fn_d
    FORM_LONG_FSINA_X_FN_S_FN_D = 10'd273,
    // long.fsincosa_x_fn_s_fn_d_fn_c
    FORM_LONG_FSINCOSA_X_FN_S_FN_D_FN_C = 10'd274,
    // long.fsinha_x_fn_s_fn_d
    FORM_LONG_FSINHA_X_FN_S_FN_D = 10'd275,
    // long.fsqrt_x_ea_s_fn_d
    FORM_LONG_FSQRT_X_EA_S_FN_D = 10'd276,
    // long.fsqrt_x_fn_s_ea_d
    FORM_LONG_FSQRT_X_FN_S_EA_D = 10'd277,
    // long.fsub_x_ea_s_fn_d
    FORM_LONG_FSUB_X_EA_S_FN_D = 10'd278,
    // long.ftana_x_fn_s_fn_d
    FORM_LONG_FTANA_X_FN_S_FN_D = 10'd279,
    // long.ftanha_x_fn_s_fn_d
    FORM_LONG_FTANHA_X_FN_S_FN_D = 10'd280,
    // long.ftentoxa_x_fn_s_fn_d
    FORM_LONG_FTENTOXA_X_FN_S_FN_D = 10'd281,
    // long.ftest_x_ea_s
    FORM_LONG_FTEST_X_EA_S = 10'd282,
    // long.ftrunc_x_ea_s_fn_d
    FORM_LONG_FTRUNC_X_EA_S_FN_D = 10'd283,
    // long.ftrunc_x_fn_s_ea_d
    FORM_LONG_FTRUNC_X_FN_S_EA_D = 10'd284,
    // long.ftwotoxa_x_fn_s_fn_d
    FORM_LONG_FTWOTOXA_X_FN_S_FN_D = 10'd285,
    // long.jcc_x_ea_e
    FORM_LONG_JCC_X_EA_E = 10'd286,
    // long.jcc_x_rn
    FORM_LONG_JCC_X_RN = 10'd287,
    // long.lcall_rn_r_ea_e
    FORM_LONG_LCALL_RN_R_EA_E = 10'd288,
    // long.ljmp_rn_r_ea_e
    FORM_LONG_LJMP_RN_R_EA_E = 10'd289,
    // long.maxs_x_ea_e_rn_d
    FORM_LONG_MAXS_X_EA_E_RN_D = 10'd290,
    // long.maxs_x_rn_s_ea_e
    FORM_LONG_MAXS_X_RN_S_EA_E = 10'd291,
    // long.maxu_x_ea_e_rn_d
    FORM_LONG_MAXU_X_EA_E_RN_D = 10'd292,
    // long.maxu_x_rn_s_ea_e
    FORM_LONG_MAXU_X_RN_S_EA_E = 10'd293,
    // long.mins_x_ea_e_rn_d
    FORM_LONG_MINS_X_EA_E_RN_D = 10'd294,
    // long.mins_x_rn_s_ea_e
    FORM_LONG_MINS_X_RN_S_EA_E = 10'd295,
    // long.minu_x_ea_e_rn_d
    FORM_LONG_MINU_X_EA_E_RN_D = 10'd296,
    // long.minu_x_rn_s_ea_e
    FORM_LONG_MINU_X_RN_S_EA_E = 10'd297,
    // long.mods_x_ea_e_rn_d
    FORM_LONG_MODS_X_EA_E_RN_D = 10'd298,
    // long.modu_x_ea_e_rn_d
    FORM_LONG_MODU_X_EA_E_RN_D = 10'd299,
    // long.mov_x_ea_s_ea_d
    FORM_LONG_MOV_X_EA_S_EA_D = 10'd300,
    // long.movcc_x_rn_s_rn_d
    FORM_LONG_MOVCC_X_RN_S_RN_D = 10'd301,
    // long.movcu_x_ea_s_ea_d
    FORM_LONG_MOVCU_X_EA_S_EA_D = 10'd302,
    // long.movcu_x_ea_s_rn_d
    FORM_LONG_MOVCU_X_EA_S_RN_D = 10'd303,
    // long.movcu_x_rn_s_ea_d
    FORM_LONG_MOVCU_X_RN_S_EA_D = 10'd304,
    // long.movnt_x_rn_s_ea_e
    FORM_LONG_MOVNT_X_RN_S_EA_E = 10'd305,
    // long.movuc_x_ea_s_ea_d
    FORM_LONG_MOVUC_X_EA_S_EA_D = 10'd306,
    // long.movuc_x_ea_s_rn_d
    FORM_LONG_MOVUC_X_EA_S_RN_D = 10'd307,
    // long.movuc_x_rn_s_ea_d
    FORM_LONG_MOVUC_X_RN_S_EA_D = 10'd308,
    // long.movuu_x_ea_s_ea_d
    FORM_LONG_MOVUU_X_EA_S_EA_D = 10'd309,
    // long.mul_x_ea_e_rn_d
    FORM_LONG_MUL_X_EA_E_RN_D = 10'd310,
    // long.pand.v9
    FORM_LONG_PAND_V9 = 10'd311,
    // long.parity_x_ea_e_rn_d
    FORM_LONG_PARITY_X_EA_E_RN_D = 10'd312,
    // long.pcount.v8
    FORM_LONG_PCOUNT_V8 = 10'd313,
    // long.pfalse.v24
    FORM_LONG_PFALSE_V24 = 10'd314,
    // long.pfirst.v6
    FORM_LONG_PFIRST_V6 = 10'd315,
    // long.phead.v4
    FORM_LONG_PHEAD_V4 = 10'd316,
    // long.plast.v7
    FORM_LONG_PLAST_V7 = 10'd317,
    // long.pnot.v25
    FORM_LONG_PNOT_V25 = 10'd318,
    // long.popcnt_x_ea_e_rn_d
    FORM_LONG_POPCNT_X_EA_E_RN_D = 10'd319,
    // long.por.v10
    FORM_LONG_POR_V10 = 10'd320,
    // long.ppackhi.v15
    FORM_LONG_PPACKHI_V15 = 10'd321,
    // long.ppacklo.v14
    FORM_LONG_PPACKLO_V14 = 10'd322,
    // long.pperm.v44
    FORM_LONG_PPERM_V44 = 10'd323,
    // long.pslidedn.v46
    FORM_LONG_PSLIDEDN_V46 = 10'd324,
    // long.pslideup.v45
    FORM_LONG_PSLIDEUP_V45 = 10'd325,
    // long.ptail.v5
    FORM_LONG_PTAIL_V5 = 10'd326,
    // long.ptquery_pt_level_i_ea_e_rn_d
    FORM_LONG_PTQUERY_PT_LEVEL_I_EA_E_RN_D = 10'd327,
    // long.ptquery_pt_level_i_rn_s_rn_d
    FORM_LONG_PTQUERY_PT_LEVEL_I_RN_S_RN_D = 10'd328,
    // long.ptrue.v23
    FORM_LONG_PTRUE_V23 = 10'd329,
    // long.punpkhi.v13
    FORM_LONG_PUNPKHI_V13 = 10'd330,
    // long.punpklo.v12
    FORM_LONG_PUNPKLO_V12 = 10'd331,
    // long.pxor.v11
    FORM_LONG_PXOR_V11 = 10'd332,
    // long.rol_x_imm6_i_ea_e
    FORM_LONG_ROL_X_IMM6_I_EA_E = 10'd333,
    // long.rol_x_rn_s_ea_e
    FORM_LONG_ROL_X_RN_S_EA_E = 10'd334,
    // long.ror_x_imm6_i_ea_e
    FORM_LONG_ROR_X_IMM6_I_EA_E = 10'd335,
    // long.ror_x_rn_s_ea_e
    FORM_LONG_ROR_X_RN_S_EA_E = 10'd336,
    // long.sar_x_imm6_i_ea_e
    FORM_LONG_SAR_X_IMM6_I_EA_E = 10'd337,
    // long.sar_x_rn_s_ea_e
    FORM_LONG_SAR_X_RN_S_EA_E = 10'd338,
    // long.sbb_x_ea_e_rn_d
    FORM_LONG_SBB_X_EA_E_RN_D = 10'd339,
    // long.sbb_x_rn_s_ea_e
    FORM_LONG_SBB_X_RN_S_EA_E = 10'd340,
    // long.seglea_x_ea_e_rn_d
    FORM_LONG_SEGLEA_X_EA_E_RN_D = 10'd341,
    // long.shl_x_imm6_i_ea_e
    FORM_LONG_SHL_X_IMM6_I_EA_E = 10'd342,
    // long.shl_x_rn_s_ea_e
    FORM_LONG_SHL_X_RN_S_EA_E = 10'd343,
    // long.shr_x_imm6_i_ea_e
    FORM_LONG_SHR_X_IMM6_I_EA_E = 10'd344,
    // long.shr_x_rn_s_ea_e
    FORM_LONG_SHR_X_RN_S_EA_E = 10'd345,
    // long.sub_x_imm16s_ea_e
    FORM_LONG_SUB_X_IMM16S_EA_E = 10'd346,
    // long.sub_x_imm32s_ea_e
    FORM_LONG_SUB_X_IMM32S_EA_E = 10'd347,
    // long.sub_x_imm8s_ea_e
    FORM_LONG_SUB_X_IMM8S_EA_E = 10'd348,
    // long.test_x_rn_s_ea_e
    FORM_LONG_TEST_X_RN_S_EA_E = 10'd349,
    // long.testjcc_x_rn_s_rn_d_imm16s
    FORM_LONG_TESTJCC_X_RN_S_RN_D_IMM16S = 10'd350,
    // long.testjcc_x_rn_s_rn_d_imm8s
    FORM_LONG_TESTJCC_X_RN_S_RN_D_IMM8S = 10'd351,
    // long.vabs.v30
    FORM_LONG_VABS_V30 = 10'd352,
    // long.vceil.v42
    FORM_LONG_VCEIL_V42 = 10'd353,
    // long.vclass.v43
    FORM_LONG_VCLASS_V43 = 10'd354,
    // long.vclr.v16
    FORM_LONG_VCLR_V16 = 10'd355,
    // long.vcls.v34
    FORM_LONG_VCLS_V34 = 10'd356,
    // long.vclz.v32
    FORM_LONG_VCLZ_V32 = 10'd357,
    // long.vcts.v35
    FORM_LONG_VCTS_V35 = 10'd358,
    // long.vctz.v33
    FORM_LONG_VCTZ_V33 = 10'd359,
    // long.vdup.v1
    FORM_LONG_VDUP_V1 = 10'd360,
    // long.vdup.v18.b
    FORM_LONG_VDUP_V18_B = 10'd361,
    // long.vdup.v18.l
    FORM_LONG_VDUP_V18_L = 10'd362,
    // long.vdup.v18.q
    FORM_LONG_VDUP_V18_Q = 10'd363,
    // long.vdup.v18.w
    FORM_LONG_VDUP_V18_W = 10'd364,
    // long.vdup.v2
    FORM_LONG_VDUP_V2 = 10'd365,
    // long.vfloor.v41
    FORM_LONG_VFLOOR_V41 = 10'd366,
    // long.vindex.v17
    FORM_LONG_VINDEX_V17 = 10'd367,
    // long.vlcadd.v21
    FORM_LONG_VLCADD_V21 = 10'd368,
    // long.vlcnt.v20
    FORM_LONG_VLCNT_V20 = 10'd369,
    // long.vmov.v3
    FORM_LONG_VMOV_V3 = 10'd370,
    // long.vneg.v29
    FORM_LONG_VNEG_V29 = 10'd371,
    // long.vnot.v31
    FORM_LONG_VNOT_V31 = 10'd372,
    // long.vpopcnt.v36
    FORM_LONG_VPOPCNT_V36 = 10'd373,
    // long.vrevbyte.v37
    FORM_LONG_VREVBYTE_V37 = 10'd374,
    // long.vround.v39
    FORM_LONG_VROUND_V39 = 10'd375,
    // long.vsqrt.v38
    FORM_LONG_VSQRT_V38 = 10'd376,
    // long.vtrunc.v40
    FORM_LONG_VTRUNC_V40 = 10'd377,
    // long.xchg_x_ea_e_rn_d
    FORM_LONG_XCHG_X_EA_E_RN_D = 10'd378,
    // long.xchg_x_rn_s_ea_e
    FORM_LONG_XCHG_X_RN_S_EA_E = 10'd379,
    // long.xor_x_imm16s_ea_e
    FORM_LONG_XOR_X_IMM16S_EA_E = 10'd380,
    // long.xor_x_imm32s_ea_e
    FORM_LONG_XOR_X_IMM32S_EA_E = 10'd381,
    // long.xor_x_imm8s_ea_e
    FORM_LONG_XOR_X_IMM8S_EA_E = 10'd382,
    // medium.abs_x_ea
    FORM_MEDIUM_ABS_X_EA = 10'd383,
    // medium.adc_x_rn_s_rn_d
    FORM_MEDIUM_ADC_X_RN_S_RN_D = 10'd384,
    // medium.add_q_ea_sp
    FORM_MEDIUM_ADD_Q_EA_SP = 10'd385,
    // medium.add_q_ea_sp.2
    FORM_MEDIUM_ADD_Q_EA_SP_2 = 10'd386,
    // medium.add_q_imm64_ea_e
    FORM_MEDIUM_ADD_Q_IMM64_EA_E = 10'd387,
    // medium.add_x_ea_e_rn_d
    FORM_MEDIUM_ADD_X_EA_E_RN_D = 10'd388,
    // medium.add_x_imm16s_ea_e
    FORM_MEDIUM_ADD_X_IMM16S_EA_E = 10'd389,
    // medium.add_x_imm32s_ea_e
    FORM_MEDIUM_ADD_X_IMM32S_EA_E = 10'd390,
    // medium.add_x_imm8s_ea_e
    FORM_MEDIUM_ADD_X_IMM8S_EA_E = 10'd391,
    // medium.add_x_rn_s_ea_e
    FORM_MEDIUM_ADD_X_RN_S_EA_E = 10'd392,
    // medium.and_q_imm64_ea_e
    FORM_MEDIUM_AND_Q_IMM64_EA_E = 10'd393,
    // medium.and_x_ea_e_rn_d
    FORM_MEDIUM_AND_X_EA_E_RN_D = 10'd394,
    // medium.and_x_imm16s_ea_e
    FORM_MEDIUM_AND_X_IMM16S_EA_E = 10'd395,
    // medium.and_x_imm32s_ea_e
    FORM_MEDIUM_AND_X_IMM32S_EA_E = 10'd396,
    // medium.and_x_imm8s_ea_e
    FORM_MEDIUM_AND_X_IMM8S_EA_E = 10'd397,
    // medium.and_x_rn_s_ea_e
    FORM_MEDIUM_AND_X_RN_S_EA_E = 10'd398,
    // medium.bchg_rn_b_rn_e
    FORM_MEDIUM_BCHG_RN_B_RN_E = 10'd399,
    // medium.bclr_rn_b_rn_e
    FORM_MEDIUM_BCLR_RN_B_RN_E = 10'd400,
    // medium.bset_rn_b_rn_e
    FORM_MEDIUM_BSET_RN_B_RN_E = 10'd401,
    // medium.btest_rn_b_rn_e
    FORM_MEDIUM_BTEST_RN_B_RN_E = 10'd402,
    // medium.call_ea
    FORM_MEDIUM_CALL_EA = 10'd403,
    // medium.call_ea.2
    FORM_MEDIUM_CALL_EA_2 = 10'd404,
    // medium.call_ea_e
    FORM_MEDIUM_CALL_EA_E = 10'd405,
    // medium.call_rn
    FORM_MEDIUM_CALL_RN = 10'd406,
    // medium.callcc_ea
    FORM_MEDIUM_CALLCC_EA = 10'd407,
    // medium.callcc_ea.2
    FORM_MEDIUM_CALLCC_EA_2 = 10'd408,
    // medium.clmul_x_rn_s_rn_d
    FORM_MEDIUM_CLMUL_X_RN_S_RN_D = 10'd409,
    // medium.clmulh_q_rn_s_rn_d
    FORM_MEDIUM_CLMULH_Q_RN_S_RN_D = 10'd410,
    // medium.clr_x_ea
    FORM_MEDIUM_CLR_X_EA = 10'd411,
    // medium.cls_x_rn_s_rn_d
    FORM_MEDIUM_CLS_X_RN_S_RN_D = 10'd412,
    // medium.clz_x_rn_s_rn_d
    FORM_MEDIUM_CLZ_X_RN_S_RN_D = 10'd413,
    // medium.cmp_x_ea_e_rn_d
    FORM_MEDIUM_CMP_X_EA_E_RN_D = 10'd414,
    // medium.cmp_x_rn_s_ea_e
    FORM_MEDIUM_CMP_X_RN_S_EA_E = 10'd415,
    // medium.cpuid_rn_r
    FORM_MEDIUM_CPUID_RN_R = 10'd416,
    // medium.cts_x_rn_s_rn_d
    FORM_MEDIUM_CTS_X_RN_S_RN_D = 10'd417,
    // medium.ctz_x_rn_s_rn_d
    FORM_MEDIUM_CTZ_X_RN_S_RN_D = 10'd418,
    // medium.dec_x_ea
    FORM_MEDIUM_DEC_X_EA = 10'd419,
    // medium.decf_x_rn_r
    FORM_MEDIUM_DECF_X_RN_R = 10'd420,
    // medium.divs_x_rn_s_rn_d
    FORM_MEDIUM_DIVS_X_RN_S_RN_D = 10'd421,
    // medium.divu_x_rn_s_rn_d
    FORM_MEDIUM_DIVU_X_RN_S_RN_D = 10'd422,
    // medium.extsq_b_ea_e_rn_d
    FORM_MEDIUM_EXTSQ_B_EA_E_RN_D = 10'd423,
    // medium.extsq_b_rn_s_rn_d
    FORM_MEDIUM_EXTSQ_B_RN_S_RN_D = 10'd424,
    // medium.extsq_l_ea_e_rn_d
    FORM_MEDIUM_EXTSQ_L_EA_E_RN_D = 10'd425,
    // medium.extsq_w_ea_e_rn_d
    FORM_MEDIUM_EXTSQ_W_EA_E_RN_D = 10'd426,
    // medium.extsq_w_rn_s_rn_d
    FORM_MEDIUM_EXTSQ_W_RN_S_RN_D = 10'd427,
    // medium.fabs_x_fn_s_fn_d
    FORM_MEDIUM_FABS_X_FN_S_FN_D = 10'd428,
    // medium.fadd_x_fn_s_fn_d
    FORM_MEDIUM_FADD_X_FN_S_FN_D = 10'd429,
    // medium.fceil_x_fn_s_fn_d
    FORM_MEDIUM_FCEIL_X_FN_S_FN_D = 10'd430,
    // medium.fclr_fn_d
    FORM_MEDIUM_FCLR_FN_D = 10'd431,
    // medium.fcmp_x_fn_s_fn_d
    FORM_MEDIUM_FCMP_X_FN_S_FN_D = 10'd432,
    // medium.fcvt_x_fn_s_fn_d
    FORM_MEDIUM_FCVT_X_FN_S_FN_D = 10'd433,
    // medium.fcvtu_x_fn_s_fn_d
    FORM_MEDIUM_FCVTU_X_FN_S_FN_D = 10'd434,
    // medium.fdiv_x_fn_s_fn_d
    FORM_MEDIUM_FDIV_X_FN_S_FN_D = 10'd435,
    // medium.ffloor_x_fn_s_fn_d
    FORM_MEDIUM_FFLOOR_X_FN_S_FN_D = 10'd436,
    // medium.fgetexp_x_fn_s_fn_d
    FORM_MEDIUM_FGETEXP_X_FN_S_FN_D = 10'd437,
    // medium.fgetman_x_fn_s_fn_d
    FORM_MEDIUM_FGETMAN_X_FN_S_FN_D = 10'd438,
    // medium.fint_x_fn_s_fn_d
    FORM_MEDIUM_FINT_X_FN_S_FN_D = 10'd439,
    // medium.fintrz_x_fn_s_fn_d
    FORM_MEDIUM_FINTRZ_X_FN_S_FN_D = 10'd440,
    // medium.flshdcache_ea_e
    FORM_MEDIUM_FLSHDCACHE_EA_E = 10'd441,
    // medium.fmax_x_fn_s_fn_d
    FORM_MEDIUM_FMAX_X_FN_S_FN_D = 10'd442,
    // medium.fmin_x_fn_s_fn_d
    FORM_MEDIUM_FMIN_X_FN_S_FN_D = 10'd443,
    // medium.fmod_x_fn_s_fn_d
    FORM_MEDIUM_FMOD_X_FN_S_FN_D = 10'd444,
    // medium.fmov_x_fn_s_fn_d
    FORM_MEDIUM_FMOV_X_FN_S_FN_D = 10'd445,
    // medium.fmovcr_x_imm16_fn_d
    FORM_MEDIUM_FMOVCR_X_IMM16_FN_D = 10'd446,
    // medium.fmul_x_fn_s_fn_d
    FORM_MEDIUM_FMUL_X_FN_S_FN_D = 10'd447,
    // medium.fneg_x_fn_s_fn_d
    FORM_MEDIUM_FNEG_X_FN_S_FN_D = 10'd448,
    // medium.frem_x_fn_s_fn_d
    FORM_MEDIUM_FREM_X_FN_S_FN_D = 10'd449,
    // medium.fround_x_fn_s_fn_d
    FORM_MEDIUM_FROUND_X_FN_S_FN_D = 10'd450,
    // medium.fscale_x_fn_s_fn_d
    FORM_MEDIUM_FSCALE_X_FN_S_FN_D = 10'd451,
    // medium.fsqrt_x_fn_s_fn_d
    FORM_MEDIUM_FSQRT_X_FN_S_FN_D = 10'd452,
    // medium.fsub_x_fn_s_fn_d
    FORM_MEDIUM_FSUB_X_FN_S_FN_D = 10'd453,
    // medium.ftest_x_fn_s
    FORM_MEDIUM_FTEST_X_FN_S = 10'd454,
    // medium.ftrunc_x_fn_s_fn_d
    FORM_MEDIUM_FTRUNC_X_FN_S_FN_D = 10'd455,
    // medium.fxchg_fn_l_fn_r
    FORM_MEDIUM_FXCHG_FN_L_FN_R = 10'd456,
    // medium.inc_x_ea
    FORM_MEDIUM_INC_X_EA = 10'd457,
    // medium.incf_x_rn_r
    FORM_MEDIUM_INCF_X_RN_R = 10'd458,
    // medium.invasid_ea
    FORM_MEDIUM_INVASID_EA = 10'd459,
    // medium.invdcache_ea_e
    FORM_MEDIUM_INVDCACHE_EA_E = 10'd460,
    // medium.invicache_ea_e
    FORM_MEDIUM_INVICACHE_EA_E = 10'd461,
    // medium.invpage_ea_e
    FORM_MEDIUM_INVPAGE_EA_E = 10'd462,
    // medium.invpage_rn
    FORM_MEDIUM_INVPAGE_RN = 10'd463,
    // medium.invtlb
    FORM_MEDIUM_INVTLB = 10'd464,
    // medium.jcc_ea
    FORM_MEDIUM_JCC_EA = 10'd465,
    // medium.jcc_ea.2
    FORM_MEDIUM_JCC_EA_2 = 10'd466,
    // medium.jmp_ea
    FORM_MEDIUM_JMP_EA = 10'd467,
    // medium.jmp_ea.2
    FORM_MEDIUM_JMP_EA_2 = 10'd468,
    // medium.jmp_x_ea_e
    FORM_MEDIUM_JMP_X_EA_E = 10'd469,
    // medium.jmp_x_rn
    FORM_MEDIUM_JMP_X_RN = 10'd470,
    // medium.lcall_rn_s_rn_d
    FORM_MEDIUM_LCALL_RN_S_RN_D = 10'd471,
    // medium.lea_x_ea_rn
    FORM_MEDIUM_LEA_X_EA_RN = 10'd472,
    // medium.lea_x_rn_s_rn_d
    FORM_MEDIUM_LEA_X_RN_S_RN_D = 10'd473,
    // medium.ljmp_rn_s_rn_d
    FORM_MEDIUM_LJMP_RN_S_RN_D = 10'd474,
    // medium.maxs_x_rn_s_rn_d
    FORM_MEDIUM_MAXS_X_RN_S_RN_D = 10'd475,
    // medium.maxu_x_rn_s_rn_d
    FORM_MEDIUM_MAXU_X_RN_S_RN_D = 10'd476,
    // medium.mins_x_rn_s_rn_d
    FORM_MEDIUM_MINS_X_RN_S_RN_D = 10'd477,
    // medium.minu_x_rn_s_rn_d
    FORM_MEDIUM_MINU_X_RN_S_RN_D = 10'd478,
    // medium.mods_x_rn_s_rn_d
    FORM_MEDIUM_MODS_X_RN_S_RN_D = 10'd479,
    // medium.modu_x_rn_s_rn_d
    FORM_MEDIUM_MODU_X_RN_S_RN_D = 10'd480,
    // medium.mov_x_ea_e_rn_d
    FORM_MEDIUM_MOV_X_EA_E_RN_D = 10'd481,
    // medium.mov_x_rn_s_ea_e
    FORM_MEDIUM_MOV_X_RN_S_EA_E = 10'd482,
    // medium.movcu_x_rn_s_rn_d
    FORM_MEDIUM_MOVCU_X_RN_S_RN_D = 10'd483,
    // medium.movuc_x_rn_s_rn_d
    FORM_MEDIUM_MOVUC_X_RN_S_RN_D = 10'd484,
    // medium.mul_x_rn_s_rn_d
    FORM_MEDIUM_MUL_X_RN_S_RN_D = 10'd485,
    // medium.mulhs_q_rn_s_rn_d
    FORM_MEDIUM_MULHS_Q_RN_S_RN_D = 10'd486,
    // medium.mulhsu_q_rn_s_rn_d
    FORM_MEDIUM_MULHSU_Q_RN_S_RN_D = 10'd487,
    // medium.mulhu_q_rn_s_rn_d
    FORM_MEDIUM_MULHU_Q_RN_S_RN_D = 10'd488,
    // medium.neg_x_ea
    FORM_MEDIUM_NEG_X_EA = 10'd489,
    // medium.not_x_ea
    FORM_MEDIUM_NOT_X_EA = 10'd490,
    // medium.or_q_imm64_ea_e
    FORM_MEDIUM_OR_Q_IMM64_EA_E = 10'd491,
    // medium.or_x_ea_e_rn_d
    FORM_MEDIUM_OR_X_EA_E_RN_D = 10'd492,
    // medium.or_x_imm16s_ea_e
    FORM_MEDIUM_OR_X_IMM16S_EA_E = 10'd493,
    // medium.or_x_imm32s_ea_e
    FORM_MEDIUM_OR_X_IMM32S_EA_E = 10'd494,
    // medium.or_x_imm8s_ea_e
    FORM_MEDIUM_OR_X_IMM8S_EA_E = 10'd495,
    // medium.or_x_rn_s_ea_e
    FORM_MEDIUM_OR_X_RN_S_EA_E = 10'd496,
    // medium.parity_x_rn_s_rn_d
    FORM_MEDIUM_PARITY_X_RN_S_RN_D = 10'd497,
    // medium.popcnt_x_rn_s_rn_d
    FORM_MEDIUM_POPCNT_X_RN_S_RN_D = 10'd498,
    // medium.prefetch_ea_e
    FORM_MEDIUM_PREFETCH_EA_E = 10'd499,
    // medium.prefetchnt_ea_e
    FORM_MEDIUM_PREFETCHNT_EA_E = 10'd500,
    // medium.rdcr_ea_rn_d
    FORM_MEDIUM_RDCR_EA_RN_D = 10'd501,
    // medium.rdfflags_rn_d
    FORM_MEDIUM_RDFFLAGS_RN_D = 10'd502,
    // medium.rdflags_rn_d
    FORM_MEDIUM_RDFLAGS_RN_D = 10'd503,
    // medium.rdfstatus_rn_d
    FORM_MEDIUM_RDFSTATUS_RN_D = 10'd504,
    // medium.rdpmc_ea_rn_d
    FORM_MEDIUM_RDPMC_EA_RN_D = 10'd505,
    // medium.rdseg_cs_rn_d
    FORM_MEDIUM_RDSEG_CS_RN_D = 10'd506,
    // medium.rdseg_sreg_s_rn_d
    FORM_MEDIUM_RDSEG_SREG_S_RN_D = 10'd507,
    // medium.rdstatus_rn_d
    FORM_MEDIUM_RDSTATUS_RN_D = 10'd508,
    // medium.repcc_rn_r
    FORM_MEDIUM_REPCC_RN_R = 10'd509,
    // medium.restore_ea_e
    FORM_MEDIUM_RESTORE_EA_E = 10'd510,
    // medium.restore_rn
    FORM_MEDIUM_RESTORE_RN = 10'd511,
    // medium.revbyte_l_ea
    FORM_MEDIUM_REVBYTE_L_EA = 10'd512,
    // medium.revbyte_q_ea
    FORM_MEDIUM_REVBYTE_Q_EA = 10'd513,
    // medium.revbyte_w_ea
    FORM_MEDIUM_REVBYTE_W_EA = 10'd514,
    // medium.save_ea_e
    FORM_MEDIUM_SAVE_EA_E = 10'd515,
    // medium.save_rn
    FORM_MEDIUM_SAVE_RN = 10'd516,
    // medium.sbb_x_rn_s_rn_d
    FORM_MEDIUM_SBB_X_RN_S_RN_D = 10'd517,
    // medium.seglea_x_rn_s_rn_d
    FORM_MEDIUM_SEGLEA_X_RN_S_RN_D = 10'd518,
    // medium.setf_flags_bitmap_m
    FORM_MEDIUM_SETF_FLAGS_BITMAP_M = 10'd519,
    // medium.sub_q_ea_sp
    FORM_MEDIUM_SUB_Q_EA_SP = 10'd520,
    // medium.sub_q_ea_sp.2
    FORM_MEDIUM_SUB_Q_EA_SP_2 = 10'd521,
    // medium.sub_q_imm64_ea_e
    FORM_MEDIUM_SUB_Q_IMM64_EA_E = 10'd522,
    // medium.sub_x_ea_e_rn_d
    FORM_MEDIUM_SUB_X_EA_E_RN_D = 10'd523,
    // medium.sub_x_rn_s_ea_e
    FORM_MEDIUM_SUB_X_RN_S_EA_E = 10'd524,
    // medium.swpt_rn_p
    FORM_MEDIUM_SWPT_RN_P = 10'd525,
    // medium.swpta_rn_p_rn_a
    FORM_MEDIUM_SWPTA_RN_P_RN_A = 10'd526,
    // medium.synccache_ea_e
    FORM_MEDIUM_SYNCCACHE_EA_E = 10'd527,
    // medium.test_x_ea_e_rn_d
    FORM_MEDIUM_TEST_X_EA_E_RN_D = 10'd528,
    // medium.trace_ea
    FORM_MEDIUM_TRACE_EA = 10'd529,
    // medium.vtop_rn_v_rn_p
    FORM_MEDIUM_VTOP_RN_V_RN_P = 10'd530,
    // medium.wrbkdcache_ea_e
    FORM_MEDIUM_WRBKDCACHE_EA_E = 10'd531,
    // medium.wrcr_rn_s_ea
    FORM_MEDIUM_WRCR_RN_S_EA = 10'd532,
    // medium.wrfflags_rn_s
    FORM_MEDIUM_WRFFLAGS_RN_S = 10'd533,
    // medium.wrflags_rn_s
    FORM_MEDIUM_WRFLAGS_RN_S = 10'd534,
    // medium.wrfstatus_rn_s
    FORM_MEDIUM_WRFSTATUS_RN_S = 10'd535,
    // medium.wrseg_rn_d_sreg_s
    FORM_MEDIUM_WRSEG_RN_D_SREG_S = 10'd536,
    // medium.wrstatus_rn_s
    FORM_MEDIUM_WRSTATUS_RN_S = 10'd537,
    // medium.xor_q_imm64_ea_e
    FORM_MEDIUM_XOR_Q_IMM64_EA_E = 10'd538,
    // medium.xor_x_ea_e_rn_d
    FORM_MEDIUM_XOR_X_EA_E_RN_D = 10'd539,
    // medium.xor_x_rn_s_ea_e
    FORM_MEDIUM_XOR_X_RN_S_EA_E = 10'd540,
    // short.abs_x_rn_r
    FORM_SHORT_ABS_X_RN_R = 10'd541,
    // short.add_q_imm8_i_sp
    FORM_SHORT_ADD_Q_IMM8_I_SP = 10'd542,
    // short.add_x_rn_s_rn_d
    FORM_SHORT_ADD_X_RN_S_RN_D = 10'd543,
    // short.and_x_rn_s_rn_d
    FORM_SHORT_AND_X_RN_S_RN_D = 10'd544,
    // short.clr_l_rn_r
    FORM_SHORT_CLR_L_RN_R = 10'd545,
    // short.cmp_x_rn_s_rn_d
    FORM_SHORT_CMP_X_RN_S_RN_D = 10'd546,
    // short.dec_x_rn_r
    FORM_SHORT_DEC_X_RN_R = 10'd547,
    // short.extsq_l_rn_s_rn_d
    FORM_SHORT_EXTSQ_L_RN_S_RN_D = 10'd548,
    // short.halt
    FORM_SHORT_HALT = 10'd549,
    // short.inc_x_rn_r
    FORM_SHORT_INC_X_RN_R = 10'd550,
    // short.jcc_imm8s_i
    FORM_SHORT_JCC_IMM8S_I = 10'd551,
    // short.jmp_imm8s_i
    FORM_SHORT_JMP_IMM8S_I = 10'd552,
    // short.mov_b_rn_s_rn_d
    FORM_SHORT_MOV_B_RN_S_RN_D = 10'd553,
    // short.mov_w_rn_s_rn_d
    FORM_SHORT_MOV_W_RN_S_RN_D = 10'd554,
    // short.mov_x_rn_s_rn_d
    FORM_SHORT_MOV_X_RN_S_RN_D = 10'd555,
    // short.neg_x_rn_r
    FORM_SHORT_NEG_X_RN_R = 10'd556,
    // short.not_x_rn_r
    FORM_SHORT_NOT_X_RN_R = 10'd557,
    // short.or_x_rn_s_rn_d
    FORM_SHORT_OR_X_RN_S_RN_D = 10'd558,
    // short.pop_sreg_s
    FORM_SHORT_POP_SREG_S = 10'd559,
    // short.push_sreg_s
    FORM_SHORT_PUSH_SREG_S = 10'd560,
    // short.reset
    FORM_SHORT_RESET = 10'd561,
    // short.revbyte_l_rn_r
    FORM_SHORT_REVBYTE_L_RN_R = 10'd562,
    // short.revbyte_q_rn_r
    FORM_SHORT_REVBYTE_Q_RN_R = 10'd563,
    // short.revbyte_w_rn_r
    FORM_SHORT_REVBYTE_W_RN_R = 10'd564,
    // short.rol_x_rn_s_rn_d
    FORM_SHORT_ROL_X_RN_S_RN_D = 10'd565,
    // short.ror_x_rn_s_rn_d
    FORM_SHORT_ROR_X_RN_S_RN_D = 10'd566,
    // short.sar_x_rn_s_rn_d
    FORM_SHORT_SAR_X_RN_S_RN_D = 10'd567,
    // short.set_rn_r
    FORM_SHORT_SET_RN_R = 10'd568,
    // short.setcc_rn_r
    FORM_SHORT_SETCC_RN_R = 10'd569,
    // short.shl_x_rn_s_rn_d
    FORM_SHORT_SHL_X_RN_S_RN_D = 10'd570,
    // short.shr_x_rn_s_rn_d
    FORM_SHORT_SHR_X_RN_S_RN_D = 10'd571,
    // short.sub_q_imm8_i_sp
    FORM_SHORT_SUB_Q_IMM8_I_SP = 10'd572,
    // short.sub_x_rn_s_rn_d
    FORM_SHORT_SUB_X_RN_S_RN_D = 10'd573,
    // short.test_x_rn_s_rn_d
    FORM_SHORT_TEST_X_RN_S_RN_D = 10'd574,
    // short.xchg_x_rn_s_rn_d
    FORM_SHORT_XCHG_X_RN_S_RN_D = 10'd575,
    // short.xor_x_rn_s_rn_d
    FORM_SHORT_XOR_X_RN_S_RN_D = 10'd576,
    // xxlong.bpall.v238
    FORM_XXLONG_BPALL_V238 = 10'd577,
    // xxlong.bpany.v236
    FORM_XXLONG_BPANY_V236 = 10'd578,
    // xxlong.bpnone.v237
    FORM_XXLONG_BPNONE_V237 = 10'd579,
    // xxlong.ploop.v233
    FORM_XXLONG_PLOOP_V233 = 10'd580,
    // xxlong.pmov.v234
    FORM_XXLONG_PMOV_V234 = 10'd581,
    // xxlong.pmov.v235
    FORM_XXLONG_PMOV_V235 = 10'd582,
    // xxlong.vabs.v186
    FORM_XXLONG_VABS_V186 = 10'd583,
    // xxlong.vabs.v187
    FORM_XXLONG_VABS_V187 = 10'd584,
    // xxlong.vadd.v140
    FORM_XXLONG_VADD_V140 = 10'd585,
    // xxlong.vadd.v141
    FORM_XXLONG_VADD_V141 = 10'd586,
    // xxlong.vand.v146
    FORM_XXLONG_VAND_V146 = 10'd587,
    // xxlong.vand.v147
    FORM_XXLONG_VAND_V147 = 10'd588,
    // xxlong.vceil.v210
    FORM_XXLONG_VCEIL_V210 = 10'd589,
    // xxlong.vceil.v211
    FORM_XXLONG_VCEIL_V211 = 10'd590,
    // xxlong.vclass.v212
    FORM_XXLONG_VCLASS_V212 = 10'd591,
    // xxlong.vclass.v213
    FORM_XXLONG_VCLASS_V213 = 10'd592,
    // xxlong.vcls.v194
    FORM_XXLONG_VCLS_V194 = 10'd593,
    // xxlong.vcls.v195
    FORM_XXLONG_VCLS_V195 = 10'd594,
    // xxlong.vclz.v190
    FORM_XXLONG_VCLZ_V190 = 10'd595,
    // xxlong.vclz.v191
    FORM_XXLONG_VCLZ_V191 = 10'd596,
    // xxlong.vcmpcc.v230.fp
    FORM_XXLONG_VCMPCC_V230_FP = 10'd597,
    // xxlong.vcmpcc.v230.integer
    FORM_XXLONG_VCMPCC_V230_INTEGER = 10'd598,
    // xxlong.vcopysign.v182
    FORM_XXLONG_VCOPYSIGN_V182 = 10'd599,
    // xxlong.vcopysign.v183
    FORM_XXLONG_VCOPYSIGN_V183 = 10'd600,
    // xxlong.vcts.v196
    FORM_XXLONG_VCTS_V196 = 10'd601,
    // xxlong.vcts.v197
    FORM_XXLONG_VCTS_V197 = 10'd602,
    // xxlong.vctz.v192
    FORM_XXLONG_VCTZ_V192 = 10'd603,
    // xxlong.vctz.v193
    FORM_XXLONG_VCTZ_V193 = 10'd604,
    // xxlong.vdiv.v180
    FORM_XXLONG_VDIV_V180 = 10'd605,
    // xxlong.vdiv.v181
    FORM_XXLONG_VDIV_V181 = 10'd606,
    // xxlong.vfloor.v208
    FORM_XXLONG_VFLOOR_V208 = 10'd607,
    // xxlong.vfloor.v209
    FORM_XXLONG_VFLOOR_V209 = 10'd608,
    // xxlong.vgather1.v239
    FORM_XXLONG_VGATHER1_V239 = 10'd609,
    // xxlong.vgather1.v240
    FORM_XXLONG_VGATHER1_V240 = 10'd610,
    // xxlong.vgather1.v241
    FORM_XXLONG_VGATHER1_V241 = 10'd611,
    // xxlong.vgather1.v242
    FORM_XXLONG_VGATHER1_V242 = 10'd612,
    // xxlong.vgather1.v243
    FORM_XXLONG_VGATHER1_V243 = 10'd613,
    // xxlong.vgather1.v244
    FORM_XXLONG_VGATHER1_V244 = 10'd614,
    // xxlong.vgather1.v245
    FORM_XXLONG_VGATHER1_V245 = 10'd615,
    // xxlong.vgather1.v246
    FORM_XXLONG_VGATHER1_V246 = 10'd616,
    // xxlong.vgather1.v247
    FORM_XXLONG_VGATHER1_V247 = 10'd617,
    // xxlong.vmax.v178
    FORM_XXLONG_VMAX_V178 = 10'd618,
    // xxlong.vmax.v179
    FORM_XXLONG_VMAX_V179 = 10'd619,
    // xxlong.vmaxs.v156
    FORM_XXLONG_VMAXS_V156 = 10'd620,
    // xxlong.vmaxs.v157
    FORM_XXLONG_VMAXS_V157 = 10'd621,
    // xxlong.vmaxu.v158
    FORM_XXLONG_VMAXU_V158 = 10'd622,
    // xxlong.vmaxu.v159
    FORM_XXLONG_VMAXU_V159 = 10'd623,
    // xxlong.vmin.v176
    FORM_XXLONG_VMIN_V176 = 10'd624,
    // xxlong.vmin.v177
    FORM_XXLONG_VMIN_V177 = 10'd625,
    // xxlong.vmins.v152
    FORM_XXLONG_VMINS_V152 = 10'd626,
    // xxlong.vmins.v153
    FORM_XXLONG_VMINS_V153 = 10'd627,
    // xxlong.vminu.v154
    FORM_XXLONG_VMINU_V154 = 10'd628,
    // xxlong.vminu.v155
    FORM_XXLONG_VMINU_V155 = 10'd629,
    // xxlong.vmov.v137
    FORM_XXLONG_VMOV_V137 = 10'd630,
    // xxlong.vmov.v138
    FORM_XXLONG_VMOV_V138 = 10'd631,
    // xxlong.vmovz.v139
    FORM_XXLONG_VMOVZ_V139 = 10'd632,
    // xxlong.vmul.v144
    FORM_XXLONG_VMUL_V144 = 10'd633,
    // xxlong.vmul.v145
    FORM_XXLONG_VMUL_V145 = 10'd634,
    // xxlong.vmulhs.v160
    FORM_XXLONG_VMULHS_V160 = 10'd635,
    // xxlong.vmulhs.v161
    FORM_XXLONG_VMULHS_V161 = 10'd636,
    // xxlong.vmulhsu.v164
    FORM_XXLONG_VMULHSU_V164 = 10'd637,
    // xxlong.vmulhsu.v165
    FORM_XXLONG_VMULHSU_V165 = 10'd638,
    // xxlong.vmulhu.v162
    FORM_XXLONG_VMULHU_V162 = 10'd639,
    // xxlong.vmulhu.v163
    FORM_XXLONG_VMULHU_V163 = 10'd640,
    // xxlong.vneg.v184
    FORM_XXLONG_VNEG_V184 = 10'd641,
    // xxlong.vneg.v185
    FORM_XXLONG_VNEG_V185 = 10'd642,
    // xxlong.vnot.v188
    FORM_XXLONG_VNOT_V188 = 10'd643,
    // xxlong.vnot.v189
    FORM_XXLONG_VNOT_V189 = 10'd644,
    // xxlong.vor.v148
    FORM_XXLONG_VOR_V148 = 10'd645,
    // xxlong.vor.v149
    FORM_XXLONG_VOR_V149 = 10'd646,
    // xxlong.vpopcnt.v198
    FORM_XXLONG_VPOPCNT_V198 = 10'd647,
    // xxlong.vpopcnt.v199
    FORM_XXLONG_VPOPCNT_V199 = 10'd648,
    // xxlong.vredadd.v219
    FORM_XXLONG_VREDADD_V219 = 10'd649,
    // xxlong.vredadd.v227
    FORM_XXLONG_VREDADD_V227 = 10'd650,
    // xxlong.vredand.v224
    FORM_XXLONG_VREDAND_V224 = 10'd651,
    // xxlong.vredmax.v229
    FORM_XXLONG_VREDMAX_V229 = 10'd652,
    // xxlong.vredmaxs.v222
    FORM_XXLONG_VREDMAXS_V222 = 10'd653,
    // xxlong.vredmaxu.v223
    FORM_XXLONG_VREDMAXU_V223 = 10'd654,
    // xxlong.vredmin.v228
    FORM_XXLONG_VREDMIN_V228 = 10'd655,
    // xxlong.vredmins.v220
    FORM_XXLONG_VREDMINS_V220 = 10'd656,
    // xxlong.vredminu.v221
    FORM_XXLONG_VREDMINU_V221 = 10'd657,
    // xxlong.vredor.v225
    FORM_XXLONG_VREDOR_V225 = 10'd658,
    // xxlong.vredxor.v226
    FORM_XXLONG_VREDXOR_V226 = 10'd659,
    // xxlong.vrevbyte.v200
    FORM_XXLONG_VREVBYTE_V200 = 10'd660,
    // xxlong.vrevbyte.v201
    FORM_XXLONG_VREVBYTE_V201 = 10'd661,
    // xxlong.vrol.v172
    FORM_XXLONG_VROL_V172 = 10'd662,
    // xxlong.vrol.v173
    FORM_XXLONG_VROL_V173 = 10'd663,
    // xxlong.vrol.v217
    FORM_XXLONG_VROL_V217 = 10'd664,
    // xxlong.vror.v174
    FORM_XXLONG_VROR_V174 = 10'd665,
    // xxlong.vror.v175
    FORM_XXLONG_VROR_V175 = 10'd666,
    // xxlong.vror.v218
    FORM_XXLONG_VROR_V218 = 10'd667,
    // xxlong.vround.v204
    FORM_XXLONG_VROUND_V204 = 10'd668,
    // xxlong.vround.v205
    FORM_XXLONG_VROUND_V205 = 10'd669,
    // xxlong.vsar.v170
    FORM_XXLONG_VSAR_V170 = 10'd670,
    // xxlong.vsar.v171
    FORM_XXLONG_VSAR_V171 = 10'd671,
    // xxlong.vsar.v216
    FORM_XXLONG_VSAR_V216 = 10'd672,
    // xxlong.vscatter1.v248
    FORM_XXLONG_VSCATTER1_V248 = 10'd673,
    // xxlong.vscatter1.v249
    FORM_XXLONG_VSCATTER1_V249 = 10'd674,
    // xxlong.vscatter1.v250
    FORM_XXLONG_VSCATTER1_V250 = 10'd675,
    // xxlong.vscatter1.v251
    FORM_XXLONG_VSCATTER1_V251 = 10'd676,
    // xxlong.vscatter1.v252
    FORM_XXLONG_VSCATTER1_V252 = 10'd677,
    // xxlong.vscatter1.v253
    FORM_XXLONG_VSCATTER1_V253 = 10'd678,
    // xxlong.vscatter1.v254
    FORM_XXLONG_VSCATTER1_V254 = 10'd679,
    // xxlong.vscatter1.v255
    FORM_XXLONG_VSCATTER1_V255 = 10'd680,
    // xxlong.vscatter1.v256
    FORM_XXLONG_VSCATTER1_V256 = 10'd681,
    // xxlong.vshl.v166
    FORM_XXLONG_VSHL_V166 = 10'd682,
    // xxlong.vshl.v167
    FORM_XXLONG_VSHL_V167 = 10'd683,
    // xxlong.vshl.v214
    FORM_XXLONG_VSHL_V214 = 10'd684,
    // xxlong.vshr.v168
    FORM_XXLONG_VSHR_V168 = 10'd685,
    // xxlong.vshr.v169
    FORM_XXLONG_VSHR_V169 = 10'd686,
    // xxlong.vshr.v215
    FORM_XXLONG_VSHR_V215 = 10'd687,
    // xxlong.vsqrt.v202
    FORM_XXLONG_VSQRT_V202 = 10'd688,
    // xxlong.vsqrt.v203
    FORM_XXLONG_VSQRT_V203 = 10'd689,
    // xxlong.vsub.v142
    FORM_XXLONG_VSUB_V142 = 10'd690,
    // xxlong.vsub.v143
    FORM_XXLONG_VSUB_V143 = 10'd691,
    // xxlong.vtestnz.v232
    FORM_XXLONG_VTESTNZ_V232 = 10'd692,
    // xxlong.vtestz.v231
    FORM_XXLONG_VTESTZ_V231 = 10'd693,
    // xxlong.vtrunc.v206
    FORM_XXLONG_VTRUNC_V206 = 10'd694,
    // xxlong.vtrunc.v207
    FORM_XXLONG_VTRUNC_V207 = 10'd695,
    // xxlong.vxor.v150
    FORM_XXLONG_VXOR_V150 = 10'd696,
    // xxlong.vxor.v151
    FORM_XXLONG_VXOR_V151 = 10'd697
  } form_id_e;

  typedef enum logic [8:0] {
    OP_INVALID = 9'd0,
    // ABS
    OP_ABS = 9'd1,
    // ADC
    OP_ADC = 9'd2,
    // ADD
    OP_ADD = 9'd3,
    // AFENCE
    OP_AFENCE = 9'd4,
    // AND
    OP_AND = 9'd5,
    // BCHG
    OP_BCHG = 9'd6,
    // BCLR
    OP_BCLR = 9'd7,
    // BKPT
    OP_BKPT = 9'd8,
    // BNDSII
    OP_BNDSII = 9'd9,
    // BNDSIX
    OP_BNDSIX = 9'd10,
    // BNDSXI
    OP_BNDSXI = 9'd11,
    // BNDSXX
    OP_BNDSXX = 9'd12,
    // BNDUII
    OP_BNDUII = 9'd13,
    // BNDUIX
    OP_BNDUIX = 9'd14,
    // BNDUXI
    OP_BNDUXI = 9'd15,
    // BNDUXX
    OP_BNDUXX = 9'd16,
    // BPALL
    OP_BPALL = 9'd17,
    // BPANY
    OP_BPANY = 9'd18,
    // BPNONE
    OP_BPNONE = 9'd19,
    // BSET
    OP_BSET = 9'd20,
    // BTEST
    OP_BTEST = 9'd21,
    // CALL
    OP_CALL = 9'd22,
    // CALLcc
    OP_CALLCC = 9'd23,
    // CLMUL
    OP_CLMUL = 9'd24,
    // CLMULH
    OP_CLMULH = 9'd25,
    // CLR
    OP_CLR = 9'd26,
    // CLS
    OP_CLS = 9'd27,
    // CLZ
    OP_CLZ = 9'd28,
    // CMP
    OP_CMP = 9'd29,
    // CMPJcc
    OP_CMPJCC = 9'd30,
    // CMPXCHG
    OP_CMPXCHG = 9'd31,
    // CPUID
    OP_CPUID = 9'd32,
    // CTS
    OP_CTS = 9'd33,
    // CTZ
    OP_CTZ = 9'd34,
    // DEC
    OP_DEC = 9'd35,
    // DECF
    OP_DECF = 9'd36,
    // DIVMODS
    OP_DIVMODS = 9'd37,
    // DIVMODU
    OP_DIVMODU = 9'd38,
    // DIVS
    OP_DIVS = 9'd39,
    // DIVU
    OP_DIVU = 9'd40,
    // DJcc
    OP_DJCC = 9'd41,
    // ERET
    OP_ERET = 9'd42,
    // EXTRACT
    OP_EXTRACT = 9'd43,
    // EXTSL
    OP_EXTSL = 9'd44,
    // EXTSQ
    OP_EXTSQ = 9'd45,
    // EXTSW
    OP_EXTSW = 9'd46,
    // EXTZL
    OP_EXTZL = 9'd47,
    // EXTZQ
    OP_EXTZQ = 9'd48,
    // EXTZW
    OP_EXTZW = 9'd49,
    // FABS
    OP_FABS = 9'd50,
    // FACOSA
    OP_FACOSA = 9'd51,
    // FADD
    OP_FADD = 9'd52,
    // FASINA
    OP_FASINA = 9'd53,
    // FATANA
    OP_FATANA = 9'd54,
    // FATANHA
    OP_FATANHA = 9'd55,
    // FBNDII
    OP_FBNDII = 9'd56,
    // FBNDIX
    OP_FBNDIX = 9'd57,
    // FBNDXI
    OP_FBNDXI = 9'd58,
    // FBNDXX
    OP_FBNDXX = 9'd59,
    // FCEIL
    OP_FCEIL = 9'd60,
    // FCLASS
    OP_FCLASS = 9'd61,
    // FCLR
    OP_FCLR = 9'd62,
    // FCMP
    OP_FCMP = 9'd63,
    // FCOPYSIGN
    OP_FCOPYSIGN = 9'd64,
    // FCOSA
    OP_FCOSA = 9'd65,
    // FCOSHA
    OP_FCOSHA = 9'd66,
    // FCVT
    OP_FCVT = 9'd67,
    // FCVTU
    OP_FCVTU = 9'd68,
    // FDIV
    OP_FDIV = 9'd69,
    // FETCHADD
    OP_FETCHADD = 9'd70,
    // FETCHAND
    OP_FETCHAND = 9'd71,
    // FETCHOR
    OP_FETCHOR = 9'd72,
    // FETCHSUB
    OP_FETCHSUB = 9'd73,
    // FETCHXOR
    OP_FETCHXOR = 9'd74,
    // FETOXA
    OP_FETOXA = 9'd75,
    // FETOXM1A
    OP_FETOXM1A = 9'd76,
    // FFLOOR
    OP_FFLOOR = 9'd77,
    // FGETEXP
    OP_FGETEXP = 9'd78,
    // FGETMAN
    OP_FGETMAN = 9'd79,
    // FINT
    OP_FINT = 9'd80,
    // FINTRZ
    OP_FINTRZ = 9'd81,
    // FLOG10A
    OP_FLOG10A = 9'd82,
    // FLOG2A
    OP_FLOG2A = 9'd83,
    // FLOGNA
    OP_FLOGNA = 9'd84,
    // FLOGNP1A
    OP_FLOGNP1A = 9'd85,
    // FLSHDCACHE
    OP_FLSHDCACHE = 9'd86,
    // FMADD
    OP_FMADD = 9'd87,
    // FMAX
    OP_FMAX = 9'd88,
    // FMIN
    OP_FMIN = 9'd89,
    // FMOD
    OP_FMOD = 9'd90,
    // FMOV
    OP_FMOV = 9'd91,
    // FMOVCR
    OP_FMOVCR = 9'd92,
    // FMOVcc
    OP_FMOVCC = 9'd93,
    // FMSUB
    OP_FMSUB = 9'd94,
    // FMUL
    OP_FMUL = 9'd95,
    // FNEG
    OP_FNEG = 9'd96,
    // FNMADD
    OP_FNMADD = 9'd97,
    // FNMSUB
    OP_FNMSUB = 9'd98,
    // FPOPP
    OP_FPOPP = 9'd99,
    // FPUSHP
    OP_FPUSHP = 9'd100,
    // FREM
    OP_FREM = 9'd101,
    // FROUND
    OP_FROUND = 9'd102,
    // FSCALE
    OP_FSCALE = 9'd103,
    // FSINA
    OP_FSINA = 9'd104,
    // FSINCOSA
    OP_FSINCOSA = 9'd105,
    // FSINHA
    OP_FSINHA = 9'd106,
    // FSQRT
    OP_FSQRT = 9'd107,
    // FSUB
    OP_FSUB = 9'd108,
    // FTANA
    OP_FTANA = 9'd109,
    // FTANHA
    OP_FTANHA = 9'd110,
    // FTENTOXA
    OP_FTENTOXA = 9'd111,
    // FTEST
    OP_FTEST = 9'd112,
    // FTRUNC
    OP_FTRUNC = 9'd113,
    // FTWOTOXA
    OP_FTWOTOXA = 9'd114,
    // FXCHG
    OP_FXCHG = 9'd115,
    // HALT
    OP_HALT = 9'd116,
    // IJcc
    OP_IJCC = 9'd117,
    // ILLEGAL
    OP_ILLEGAL = 9'd118,
    // INC
    OP_INC = 9'd119,
    // INCF
    OP_INCF = 9'd120,
    // INVASID
    OP_INVASID = 9'd121,
    // INVDCACHE
    OP_INVDCACHE = 9'd122,
    // INVICACHE
    OP_INVICACHE = 9'd123,
    // INVPAGE
    OP_INVPAGE = 9'd124,
    // INVTLB
    OP_INVTLB = 9'd125,
    // JMP
    OP_JMP = 9'd126,
    // Jcc
    OP_JCC = 9'd127,
    // LCALL
    OP_LCALL = 9'd128,
    // LEA
    OP_LEA = 9'd129,
    // LJMP
    OP_LJMP = 9'd130,
    // LRET
    OP_LRET = 9'd131,
    // MAXS
    OP_MAXS = 9'd132,
    // MAXU
    OP_MAXU = 9'd133,
    // MINS
    OP_MINS = 9'd134,
    // MINU
    OP_MINU = 9'd135,
    // MODS
    OP_MODS = 9'd136,
    // MODU
    OP_MODU = 9'd137,
    // MOV
    OP_MOV = 9'd138,
    // MOVCU
    OP_MOVCU = 9'd139,
    // MOVNT
    OP_MOVNT = 9'd140,
    // MOVUC
    OP_MOVUC = 9'd141,
    // MOVUU
    OP_MOVUU = 9'd142,
    // MOVcc
    OP_MOVCC = 9'd143,
    // MUL
    OP_MUL = 9'd144,
    // MULHS
    OP_MULHS = 9'd145,
    // MULHSU
    OP_MULHSU = 9'd146,
    // MULHU
    OP_MULHU = 9'd147,
    // NEG
    OP_NEG = 9'd148,
    // NOP
    OP_NOP = 9'd149,
    // NOT
    OP_NOT = 9'd150,
    // OR
    OP_OR = 9'd151,
    // PAND
    OP_PAND = 9'd152,
    // PARITY
    OP_PARITY = 9'd153,
    // PCOUNT
    OP_PCOUNT = 9'd154,
    // PFALSE
    OP_PFALSE = 9'd155,
    // PFIRST
    OP_PFIRST = 9'd156,
    // PHEAD
    OP_PHEAD = 9'd157,
    // PLAST
    OP_PLAST = 9'd158,
    // PLOOP
    OP_PLOOP = 9'd159,
    // PMOV
    OP_PMOV = 9'd160,
    // PNOT
    OP_PNOT = 9'd161,
    // POP
    OP_POP = 9'd162,
    // POPCNT
    OP_POPCNT = 9'd163,
    // POPP
    OP_POPP = 9'd164,
    // POR
    OP_POR = 9'd165,
    // PPACKHI
    OP_PPACKHI = 9'd166,
    // PPACKLO
    OP_PPACKLO = 9'd167,
    // PPERM
    OP_PPERM = 9'd168,
    // PREFETCH
    OP_PREFETCH = 9'd169,
    // PREFETCHNT
    OP_PREFETCHNT = 9'd170,
    // PSEL
    OP_PSEL = 9'd171,
    // PSLICE
    OP_PSLICE = 9'd172,
    // PSLIDEDN
    OP_PSLIDEDN = 9'd173,
    // PSLIDEUP
    OP_PSLIDEUP = 9'd174,
    // PTAIL
    OP_PTAIL = 9'd175,
    // PTQUERY
    OP_PTQUERY = 9'd176,
    // PTRNHI
    OP_PTRNHI = 9'd177,
    // PTRNLO
    OP_PTRNLO = 9'd178,
    // PTRUE
    OP_PTRUE = 9'd179,
    // PUNPKHI
    OP_PUNPKHI = 9'd180,
    // PUNPKLO
    OP_PUNPKLO = 9'd181,
    // PUSH
    OP_PUSH = 9'd182,
    // PUSHP
    OP_PUSHP = 9'd183,
    // PUZIPHI
    OP_PUZIPHI = 9'd184,
    // PUZIPLO
    OP_PUZIPLO = 9'd185,
    // PXOR
    OP_PXOR = 9'd186,
    // PZIPHI
    OP_PZIPHI = 9'd187,
    // PZIPLO
    OP_PZIPLO = 9'd188,
    // RDCR
    OP_RDCR = 9'd189,
    // RDFFLAGS
    OP_RDFFLAGS = 9'd190,
    // RDFLAGS
    OP_RDFLAGS = 9'd191,
    // RDFSTATUS
    OP_RDFSTATUS = 9'd192,
    // RDPMC
    OP_RDPMC = 9'd193,
    // RDSEG
    OP_RDSEG = 9'd194,
    // RDSTATUS
    OP_RDSTATUS = 9'd195,
    // REPcc
    OP_REPCC = 9'd196,
    // RESET
    OP_RESET = 9'd197,
    // RESTORE
    OP_RESTORE = 9'd198,
    // RET
    OP_RET = 9'd199,
    // REVBYTE
    OP_REVBYTE = 9'd200,
    // RFENCE
    OP_RFENCE = 9'd201,
    // ROL
    OP_ROL = 9'd202,
    // ROR
    OP_ROR = 9'd203,
    // SAR
    OP_SAR = 9'd204,
    // SAVE
    OP_SAVE = 9'd205,
    // SBB
    OP_SBB = 9'd206,
    // SEGLEA
    OP_SEGLEA = 9'd207,
    // SET
    OP_SET = 9'd208,
    // SETF
    OP_SETF = 9'd209,
    // SETcc
    OP_SETCC = 9'd210,
    // SHL
    OP_SHL = 9'd211,
    // SHR
    OP_SHR = 9'd212,
    // SUB
    OP_SUB = 9'd213,
    // SWPT
    OP_SWPT = 9'd214,
    // SWPTA
    OP_SWPTA = 9'd215,
    // SYNCCACHE
    OP_SYNCCACHE = 9'd216,
    // SYSCALL
    OP_SYSCALL = 9'd217,
    // TEST
    OP_TEST = 9'd218,
    // TESTJcc
    OP_TESTJCC = 9'd219,
    // TRACE
    OP_TRACE = 9'd220,
    // VABS
    OP_VABS = 9'd221,
    // VADD
    OP_VADD = 9'd222,
    // VAND
    OP_VAND = 9'd223,
    // VCEIL
    OP_VCEIL = 9'd224,
    // VCLASS
    OP_VCLASS = 9'd225,
    // VCLR
    OP_VCLR = 9'd226,
    // VCLS
    OP_VCLS = 9'd227,
    // VCLZ
    OP_VCLZ = 9'd228,
    // VCMPcc
    OP_VCMPCC = 9'd229,
    // VCOPYSIGN
    OP_VCOPYSIGN = 9'd230,
    // VCTS
    OP_VCTS = 9'd231,
    // VCTZ
    OP_VCTZ = 9'd232,
    // VCVTD
    OP_VCVTD = 9'd233,
    // VCVTH
    OP_VCVTH = 9'd234,
    // VCVTL
    OP_VCVTL = 9'd235,
    // VCVTQ
    OP_VCVTQ = 9'd236,
    // VCVTS
    OP_VCVTS = 9'd237,
    // VCVTUD
    OP_VCVTUD = 9'd238,
    // VCVTUH
    OP_VCVTUH = 9'd239,
    // VCVTUL
    OP_VCVTUL = 9'd240,
    // VCVTUQ
    OP_VCVTUQ = 9'd241,
    // VCVTUS
    OP_VCVTUS = 9'd242,
    // VDIV
    OP_VDIV = 9'd243,
    // VDUP
    OP_VDUP = 9'd244,
    // VEXTRACT
    OP_VEXTRACT = 9'd245,
    // VEXTSL
    OP_VEXTSL = 9'd246,
    // VEXTSQ
    OP_VEXTSQ = 9'd247,
    // VEXTSW
    OP_VEXTSW = 9'd248,
    // VEXTZL
    OP_VEXTZL = 9'd249,
    // VEXTZQ
    OP_VEXTZQ = 9'd250,
    // VEXTZW
    OP_VEXTZW = 9'd251,
    // VFLOOR
    OP_VFLOOR = 9'd252,
    // VGATHER1
    OP_VGATHER1 = 9'd253,
    // VINDEX
    OP_VINDEX = 9'd254,
    // VINSERT
    OP_VINSERT = 9'd255,
    // VLCADD
    OP_VLCADD = 9'd256,
    // VLCNT
    OP_VLCNT = 9'd257,
    // VMADD
    OP_VMADD = 9'd258,
    // VMAX
    OP_VMAX = 9'd259,
    // VMAXS
    OP_VMAXS = 9'd260,
    // VMAXU
    OP_VMAXU = 9'd261,
    // VMIN
    OP_VMIN = 9'd262,
    // VMINS
    OP_VMINS = 9'd263,
    // VMINU
    OP_VMINU = 9'd264,
    // VMOV
    OP_VMOV = 9'd265,
    // VMOVZ
    OP_VMOVZ = 9'd266,
    // VMSUB
    OP_VMSUB = 9'd267,
    // VMUL
    OP_VMUL = 9'd268,
    // VMULHS
    OP_VMULHS = 9'd269,
    // VMULHSU
    OP_VMULHSU = 9'd270,
    // VMULHU
    OP_VMULHU = 9'd271,
    // VNEG
    OP_VNEG = 9'd272,
    // VNMADD
    OP_VNMADD = 9'd273,
    // VNMSUB
    OP_VNMSUB = 9'd274,
    // VNOT
    OP_VNOT = 9'd275,
    // VOR
    OP_VOR = 9'd276,
    // VPERM
    OP_VPERM = 9'd277,
    // VPOPCNT
    OP_VPOPCNT = 9'd278,
    // VREDADD
    OP_VREDADD = 9'd279,
    // VREDAND
    OP_VREDAND = 9'd280,
    // VREDMAX
    OP_VREDMAX = 9'd281,
    // VREDMAXS
    OP_VREDMAXS = 9'd282,
    // VREDMAXU
    OP_VREDMAXU = 9'd283,
    // VREDMIN
    OP_VREDMIN = 9'd284,
    // VREDMINS
    OP_VREDMINS = 9'd285,
    // VREDMINU
    OP_VREDMINU = 9'd286,
    // VREDOR
    OP_VREDOR = 9'd287,
    // VREDXOR
    OP_VREDXOR = 9'd288,
    // VREVBYTE
    OP_VREVBYTE = 9'd289,
    // VROL
    OP_VROL = 9'd290,
    // VROR
    OP_VROR = 9'd291,
    // VROUND
    OP_VROUND = 9'd292,
    // VSAR
    OP_VSAR = 9'd293,
    // VSCATTER1
    OP_VSCATTER1 = 9'd294,
    // VSHL
    OP_VSHL = 9'd295,
    // VSHR
    OP_VSHR = 9'd296,
    // VSLICE
    OP_VSLICE = 9'd297,
    // VSLIDEDN
    OP_VSLIDEDN = 9'd298,
    // VSLIDEUP
    OP_VSLIDEUP = 9'd299,
    // VSQRT
    OP_VSQRT = 9'd300,
    // VSUB
    OP_VSUB = 9'd301,
    // VTESTNZ
    OP_VTESTNZ = 9'd302,
    // VTESTZ
    OP_VTESTZ = 9'd303,
    // VTOP
    OP_VTOP = 9'd304,
    // VTRNHI
    OP_VTRNHI = 9'd305,
    // VTRNLO
    OP_VTRNLO = 9'd306,
    // VTRUNC
    OP_VTRUNC = 9'd307,
    // VTRUNCB
    OP_VTRUNCB = 9'd308,
    // VTRUNCL
    OP_VTRUNCL = 9'd309,
    // VTRUNCW
    OP_VTRUNCW = 9'd310,
    // VUZIPHI
    OP_VUZIPHI = 9'd311,
    // VUZIPLO
    OP_VUZIPLO = 9'd312,
    // VXOR
    OP_VXOR = 9'd313,
    // VZIPHI
    OP_VZIPHI = 9'd314,
    // VZIPLO
    OP_VZIPLO = 9'd315,
    // WAIT
    OP_WAIT = 9'd316,
    // WFENCE
    OP_WFENCE = 9'd317,
    // WRBKDCACHE
    OP_WRBKDCACHE = 9'd318,
    // WRCR
    OP_WRCR = 9'd319,
    // WRFFLAGS
    OP_WRFFLAGS = 9'd320,
    // WRFLAGS
    OP_WRFLAGS = 9'd321,
    // WRFSTATUS
    OP_WRFSTATUS = 9'd322,
    // WRSEG
    OP_WRSEG = 9'd323,
    // WRSTATUS
    OP_WRSTATUS = 9'd324,
    // XCHG
    OP_XCHG = 9'd325,
    // XOR
    OP_XOR = 9'd326,
    // YIELD
    OP_YIELD = 9'd327
  } operation_e;

  typedef enum logic [4:0] {
    ROUTE_INVALID = 5'd0,
    // atomics
    ROUTE_ATOMICS = 5'd1,
    // bounds
    ROUTE_BOUNDS = 5'd2,
    // cache
    ROUTE_CACHE = 5'd3,
    // control_flow
    ROUTE_CONTROL_FLOW = 5'd4,
    // core_control
    ROUTE_CORE_CONTROL = 5'd5,
    // data_movement
    ROUTE_DATA_MOVEMENT = 5'd6,
    // ea_utility
    ROUTE_EA_UTILITY = 5'd7,
    // fpu
    ROUTE_FPU = 5'd8,
    // fpu_transcendental_approx
    ROUTE_FPU_TRANSCENDENTAL_APPROX = 5'd9,
    // integer_alu
    ROUTE_INTEGER_ALU = 5'd10,
    // integer_bitfield
    ROUTE_INTEGER_BITFIELD = 5'd11,
    // integer_mul_div
    ROUTE_INTEGER_MUL_DIV = 5'd12,
    // integer_unary
    ROUTE_INTEGER_UNARY = 5'd13,
    // system_registers
    ROUTE_SYSTEM_REGISTERS = 5'd14,
    // tlb_and_context
    ROUTE_TLB_AND_CONTEXT = 5'd15,
    // vector
    ROUTE_VECTOR = 5'd16
  } route_e;

  typedef enum logic [2:0] {
    INSTRUCTION_SET_INVALID = 3'd0,
    // base
    INSTRUCTION_SET_BASE = 3'd1,
    // fpu
    INSTRUCTION_SET_FPU = 3'd2,
    // fpu.transcendental_approx
    INSTRUCTION_SET_FPU_TRANSCENDENTAL_APPROX = 3'd3,
    // vector
    INSTRUCTION_SET_VECTOR = 3'd4
  } instruction_set_e;

  typedef enum logic [0:0] {
    INSTRUCTION_CLASS_INVALID = 1'd0,
    // <empty>
    INSTRUCTION_CLASS_NONE = 1'd1
  } instruction_class_e;

  typedef enum logic [1:0] {
    PRIVILEGE_INVALID = 2'd0,
    // any
    PRIVILEGE_ANY = 2'd1,
    // supervisor
    PRIVILEGE_SUPERVISOR = 2'd2,
    // unprivileged
    PRIVILEGE_UNPRIVILEGED = 2'd3
  } privilege_e;

  typedef enum logic [2:0] {
    PREDICATE_INVALID = 3'd0,
    // annul_on_false
    PREDICATE_ANNUL_ON_FALSE = 3'd1,
    // counter_and_condition
    PREDICATE_COUNTER_AND_CONDITION = 3'd2,
    // none
    PREDICATE_NONE = 3'd3,
    // temporary
    PREDICATE_TEMPORARY = 3'd4,
    // write_boolean
    PREDICATE_WRITE_BOOLEAN = 3'd5
  } predicate_mode_e;

  typedef enum logic [4:0] {
    OPERAND_TYPE_INVALID = 5'd0,
    // CS
    OPERAND_TYPE_CS = 5'd1,
    // EA
    OPERAND_TYPE_EA = 5'd2,
    // FEA
    OPERAND_TYPE_FEA = 5'd3,
    // FPAIRn
    OPERAND_TYPE_FPAIRN = 5'd4,
    // Fn
    OPERAND_TYPE_FN = 5'd5,
    // PAIRn
    OPERAND_TYPE_PAIRN = 5'd6,
    // Pn
    OPERAND_TYPE_PN = 5'd7,
    // Rn
    OPERAND_TYPE_RN = 5'd8,
    // SP
    OPERAND_TYPE_SP = 5'd9,
    // SREG
    OPERAND_TYPE_SREG = 5'd10,
    // VEA
    OPERAND_TYPE_VEA = 5'd11,
    // Vn
    OPERAND_TYPE_VN = 5'd12,
    // condition
    OPERAND_TYPE_CONDITION = 5'd13,
    // fconst_id
    OPERAND_TYPE_FCONST_ID = 5'd14,
    // flags_bitmap
    OPERAND_TYPE_FLAGS_BITMAP = 5'd15,
    // imm
    OPERAND_TYPE_IMM = 5'd16,
    // imm16
    OPERAND_TYPE_IMM16 = 5'd17,
    // imm16s
    OPERAND_TYPE_IMM16S = 5'd18,
    // imm32
    OPERAND_TYPE_IMM32 = 5'd19,
    // imm32s
    OPERAND_TYPE_IMM32S = 5'd20,
    // imm6
    OPERAND_TYPE_IMM6 = 5'd21,
    // imm64
    OPERAND_TYPE_IMM64 = 5'd22,
    // imm7
    OPERAND_TYPE_IMM7 = 5'd23,
    // imm8
    OPERAND_TYPE_IMM8 = 5'd24,
    // imm8s
    OPERAND_TYPE_IMM8S = 5'd25,
    // memory_order
    OPERAND_TYPE_MEMORY_ORDER = 5'd26,
    // pt_level
    OPERAND_TYPE_PT_LEVEL = 5'd27
  } operand_type_e;

  typedef enum logic [2:0] {
    ACCESS_INVALID = 3'd0,
    // address
    ACCESS_ADDRESS = 3'd1,
    // read
    ACCESS_READ = 3'd2,
    // read_write
    ACCESS_READ_WRITE = 3'd3,
    // write
    ACCESS_WRITE = 3'd4
  } operand_access_e;

  typedef enum logic [2:0] {
    EA_WIDTH_INVALID = 3'd0,
    // <empty>
    EA_WIDTH_NONE = 3'd1,
    // Q
    EA_WIDTH_Q = 3'd2,
    // operation_size
    EA_WIDTH_OPERATION_SIZE = 3'd3,
    // predicate
    EA_WIDTH_PREDICATE = 3'd4
  } operand_ea_width_e;

  typedef enum logic [1:0] {
    EA_PROFILE_INVALID = 2'd0,
    // ea
    EA_PROFILE_EA = 2'd1,
    // fea
    EA_PROFILE_FEA = 2'd2,
    // vea
    EA_PROFILE_VEA = 2'd3
  } ea_profile_e;

  typedef enum logic [1:0] {
    OVERLAP_INVALID = 2'd0,
    // illegal_instruction
    OVERLAP_ILLEGAL_INSTRUCTION = 2'd1,
    // same_value
    OVERLAP_SAME_VALUE = 2'd2
  } overlap_rule_e;

  typedef enum logic [2:0] {
    REPEAT_OBSERVED_INVALID = 3'd0,
    // <empty>
    REPEAT_OBSERVED_NONE = 3'd1,
    // computed
    REPEAT_OBSERVED_COMPUTED = 3'd2,
    // result
    REPEAT_OBSERVED_RESULT = 3'd3,
    // source
    REPEAT_OBSERVED_SOURCE = 3'd4
  } repeat_observed_e;

  typedef enum logic [2:0] {
    EA_KIND_INVALID = 3'd0,
    // escape
    EA_KIND_ESCAPE = 3'd1,
    // float_immediate
    EA_KIND_FLOAT_IMMEDIATE = 3'd2,
    // immediate
    EA_KIND_IMMEDIATE = 3'd3,
    // memory
    EA_KIND_MEMORY = 3'd4
  } ea_kind_e;

  typedef enum logic [2:0] {
    EA_SEGMENT_INVALID = 3'd0,
    // <empty>
    EA_SEGMENT_NONE = 3'd1,
    // CS
    EA_SEGMENT_CS = 3'd2,
    // SS
    EA_SEGMENT_SS = 3'd3,
    // default
    EA_SEGMENT_DEFAULT = 3'd4,
    // explicit
    EA_SEGMENT_EXPLICIT = 3'd5
  } ea_segment_e;

  typedef enum logic [2:0] {
    EA_BASE_INVALID = 3'd0,
    // <empty>
    EA_BASE_NONE = 3'd1,
    // PC
    EA_BASE_PC = 3'd2,
    // SP
    EA_BASE_SP = 3'd3,
    // zero
    EA_BASE_ZERO = 3'd4
  } ea_base_e;

  typedef enum logic [0:0] {
    EA_REGISTER_INVALID = 1'd0,
    // <empty>
    EA_REGISTER_NONE = 1'd1
  } ea_register_e;

  typedef enum logic [1:0] {
    EA_UPDATE_TARGET_INVALID = 2'd0,
    // <empty>
    EA_UPDATE_TARGET_NONE = 2'd1,
    // b
    EA_UPDATE_TARGET_B = 2'd2,
    // i
    EA_UPDATE_TARGET_I = 2'd3
  } ea_update_target_e;

  typedef enum logic [1:0] {
    EA_UPDATE_MODE_INVALID = 2'd0,
    // <empty>
    EA_UPDATE_MODE_NONE = 2'd1,
    // postincrement
    EA_UPDATE_MODE_POSTINCREMENT = 2'd2,
    // predecrement
    EA_UPDATE_MODE_PREDECREMENT = 2'd3
  } ea_update_mode_e;

  typedef enum logic [2:0] {
    EA_PAYLOAD_WIDTH_INVALID = 3'd0,
    // 0
    EA_PAYLOAD_WIDTH_0 = 3'd1,
    // 8
    EA_PAYLOAD_WIDTH_8 = 3'd2,
    // 16
    EA_PAYLOAD_WIDTH_16 = 3'd3,
    // 32
    EA_PAYLOAD_WIDTH_32 = 3'd4,
    // 64
    EA_PAYLOAD_WIDTH_64 = 3'd5
  } ea_payload_width_e;

  typedef struct packed {
    d0_status_e status;
    opcode_class_e opcode_class;
    operator_space_e operator_space;
    form_id_e form;
    logic [31:0] form_high_decode;
    logic [31:0] form_low_decode;
    logic [BEDROCK_OPCODE_BITS-1:0] opcode;
    logic [6:0] alt_raw;
    logic [3:0] base_cursor;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
    ea_profile_e [BEDROCK_EA_SLOTS-1:0] ea_profiles;
  } d0_result_t;

  typedef struct packed {
    d0_status_e status;
    ea_layout_e ea_layout;
    operand_ea_width_e [BEDROCK_EA_SLOTS-1:0] ea_widths;
    ea_profile_e [BEDROCK_EA_SLOTS-1:0] ea_profiles;
    logic [6:0] low_raw;
    logic [6:0] alt_raw;
    logic [3:0] base_cursor;
    logic [3:0] post_alt_cursor;
  } d0_ea_result_t;

  typedef struct packed {
    logic valid;
    operand_type_e type_name;
    operand_access_e access;
    operand_ea_width_e ea_width;
    logic [63:0] value;
    logic payload_signed;
    logic ea_valid;
    logic [0:0] ea_slot;
  } decoded_operand_t;

  typedef struct packed {
    logic valid;
    ea_profile_e profile;
    ea_kind_e kind;
    ea_segment_e segment;
    ea_base_e base;
    ea_register_e register_name;
    operand_ea_width_e operand_width;
    ea_update_target_e update_target;
    ea_update_mode_e update_mode;
    ea_payload_width_e payload_width;
    logic payload_signed;
    logic direct_register_valid;
    logic [3:0] direct_register;
    logic base_register_valid;
    logic [3:0] base_register;
    logic index_register_valid;
    logic [3:0] index_register;
    logic stride_register_valid;
    logic [3:0] stride_register;
    logic segment_register_valid;
    logic [3:0] segment_register;
    logic [63:0] payload;
  } decoded_ea_t;

  typedef struct packed {
    logic valid;
    overlap_rule_e rule;
    logic [1:0] left_operand;
    logic [1:0] right_operand;
  } overlap_descriptor_t;

  typedef struct packed {
    route_e route;
    instruction_set_e instruction_set;
    instruction_class_e instruction_class;
    privilege_e privilege;
    predicate_mode_e predicate_mode;
    repeat_observed_e repeat_observed;
    logic repeat_rep;
    logic repeat_repcc;
    logic [1:0] repeat_observed_operand;
    logic has_ea_operand;
  } control_metadata_t;

  typedef struct packed {
    logic valid;
    logic [3:0] encoded_bytes;
  } ea_span_result_t;

  typedef struct packed {
    logic valid;
    decode_stage_e stage;
    form_id_e form;
    operation_e operation;
    control_metadata_t control;
    logic [BEDROCK_SIZE_MASK_BITS-1:0] size_mask;
    logic [BEDROCK_CPUID_FLAG_MASK_BITS-1:0] required_cpuid_flag_mask;
    logic [2:0] operand_count;
    decoded_operand_t [BEDROCK_OPERAND_SLOTS-1:0] operands;
    overlap_descriptor_t overlap;
    logic [BEDROCK_TOUCHED_FLAG_MASK_BITS-1:0] touched_flag_mask;
    logic [BEDROCK_POSSIBLE_EVENT_MASK_BITS-1:0] possible_event_mask;
    logic [5:0] required_bytes;
    logic [4:0] encoded_bytes;
  } d1_opcode_result_t;

  typedef struct packed {
    logic valid;
    decode_stage_e stage;
    logic [1:0] ea_count;
    decoded_ea_t [BEDROCK_EA_SLOTS-1:0] eas;
    logic [5:0] required_bytes;
  } ea_decode_result_t;

  typedef struct packed {
    logic ok;
    decode_stage_e stage;
    logic [5:0] next_cursor;
    decoded_ea_t ea;
  } ea_parse_result_t;
endpackage
