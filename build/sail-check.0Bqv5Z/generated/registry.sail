// Generated from instruction.yaml owners. Do not edit.

default Order dec

$include <prelude.sail>
$include <generic_equality.sail>

enum Form_id = Form_invalid | Form_short_abs_l_q_z_rn_r | Form_medium_abs_b_w_l_q_z_ea_e | Form_medium_adc_b_w_l_q_z_rn_s_rn_d | Form_long_adc_b_w_l_q_z_rn_s_ea_e | Form_long_adc_b_w_l_q_z_ea_e_rn_s | Form_extrashort_add_q_8_sp | Form_short_add_l_q_z_rn_s_rn_d | Form_short_add_q_imm8_i_sp | Form_medium_add_q_imm16s_sp | Form_medium_add_q_imm32s_sp | Form_medium_add_b_w_l_q_z_rn_s_ea_e | Form_medium_add_b_w_l_q_z_ea_e_rn_d | Form_medium_add_b_w_l_q_z_imm8s_ea_e | Form_medium_add_w_l_q_z_imm16s_ea_e | Form_medium_add_l_q_z_imm32s_ea_e | Form_medium_add_q_imm64_ea_e | Form_extrashort_afence_plain | Form_short_and_l_q_z_rn_s_rn_d | Form_medium_and_b_w_l_q_z_rn_s_ea_e | Form_medium_and_b_w_l_q_z_ea_e_rn_d | Form_medium_and_b_w_l_q_z_imm8s_ea_e | Form_medium_and_w_l_q_z_imm16s_ea_e | Form_medium_and_l_q_z_imm32s_ea_e | Form_medium_and_q_imm64_ea_e | Form_long_bchg_rn_b_ea_e | Form_long_bchg_imm6_i_ea_e | Form_medium_bchg_rn_b_rn_e | Form_long_bchg_imm6_i_rn_e | Form_long_bclr_rn_b_ea_e | Form_long_bclr_imm6_i_ea_e | Form_medium_bclr_rn_b_rn_e | Form_long_bclr_imm6_i_rn_e | Form_extrashort_bkpt_plain | Form_extralong_bndsii_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bndsii_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bndsix_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bndsix_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bndsxi_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bndsxi_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bndsxx_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bndsxx_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bnduii_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bnduii_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bnduix_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bnduix_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bnduxi_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bnduxi_b_w_l_q_z_rn_l_rn_v_rn_h | Form_extralong_bnduxx_b_w_l_q_z_rn_l_ea_e_rn_h | Form_extralong_bnduxx_b_w_l_q_z_rn_l_rn_v_rn_h | Form_long_bset_rn_b_ea_e | Form_long_bset_imm6_i_ea_e | Form_medium_bset_rn_b_rn_e | Form_long_bset_imm6_i_rn_e | Form_long_btest_rn_b_ea_e | Form_long_btest_imm6_i_ea_e | Form_medium_btest_rn_b_rn_e | Form_long_btest_imm6_i_rn_e | Form_medium_call_imm16s | Form_medium_call_imm32s | Form_medium_call_ea_e | Form_medium_call_rn_r | Form_medium_callcc_imm16s | Form_medium_callcc_imm32s | Form_long_callcc_ea_e | Form_long_callcc_rn_r | Form_long_clmul_b_w_l_q_z_ea_e_rn_d | Form_medium_clmul_b_w_l_q_z_rn_s_rn_d | Form_long_clmulh_q_ea_e_rn_d | Form_medium_clmulh_q_rn_s_rn_d | Form_extrashort_clr_q_rn_r | Form_short_clr_l_rn_r | Form_medium_clr_b_w_l_q_z_ea_e | Form_long_cls_b_w_l_q_z_ea_e_rn_d | Form_medium_cls_b_w_l_q_z_rn_s_rn_d | Form_long_clz_b_w_l_q_z_ea_e_rn_d | Form_medium_clz_b_w_l_q_z_rn_s_rn_d | Form_short_cmp_l_q_z_rn_s_rn_d | Form_medium_cmp_b_w_l_q_z_rn_s_ea_e | Form_medium_cmp_b_w_l_q_z_ea_e_rn_d | Form_long_cmp_b_w_l_q_z_ea_s_ea_d | Form_long_cmpjcc_b_w_l_q_z_rn_s_rn_d_imm8s | Form_long_cmpjcc_b_w_l_q_z_rn_s_rn_d_imm16s | Form_extralong_cmpxchg_b_w_l_q_z_order_o_rn_x_rn_d_ea_e | Form_medium_cpuid_rn_r | Form_long_cts_b_w_l_q_z_ea_e_rn_d | Form_medium_cts_b_w_l_q_z_rn_s_rn_d | Form_long_ctz_b_w_l_q_z_ea_e_rn_d | Form_medium_ctz_b_w_l_q_z_rn_s_rn_d | Form_short_dec_l_q_z_rn_r | Form_medium_dec_b_w_l_q_z_ea_e | Form_medium_decf_b_w_l_q_z_rn_r | Form_extralong_divmods_b_w_l_q_z_ea_e_rn_q_rn_r | Form_extralong_divmods_b_w_l_q_z_rn_e_rn_q_rn_r | Form_extralong_divmodu_b_w_l_q_z_ea_e_rn_q_rn_r | Form_extralong_divmodu_b_w_l_q_z_rn_e_rn_q_rn_r | Form_long_divs_b_w_l_q_z_ea_e_rn_d | Form_medium_divs_b_w_l_q_z_rn_s_rn_d | Form_long_divu_b_w_l_q_z_ea_e_rn_d | Form_medium_divu_b_w_l_q_z_rn_s_rn_d | Form_long_djcc_rn_r_ea_e | Form_long_djcc_rn_r_rn_e | Form_extrashort_eret_plain | Form_extralong_extract_b_w_l_q_z_imm7_i_rn_h_rn_l | Form_long_extsl_b_rn_s_ea_e | Form_long_extsl_w_rn_s_ea_e | Form_long_extsl_b_w_z_ea_s_ea_d | Form_medium_extsq_b_rn_s_rn_d | Form_medium_extsq_w_rn_s_rn_d | Form_short_extsq_l_rn_s_rn_d | Form_long_extsq_b_rn_s_ea_e | Form_medium_extsq_b_ea_e_rn_d | Form_long_extsq_w_rn_s_ea_e | Form_medium_extsq_w_ea_e_rn_d | Form_long_extsq_l_rn_s_ea_e | Form_medium_extsq_l_ea_e_rn_d | Form_long_extsq_b_ea_s_ea_d | Form_long_extsq_w_ea_s_ea_d | Form_long_extsq_l_ea_s_ea_d | Form_long_extsw_b_rn_s_ea_e | Form_long_extsw_b_ea_s_ea_d | Form_long_extzl_b_rn_s_ea_e | Form_long_extzl_w_rn_s_ea_e | Form_long_extzl_b_w_z_ea_s_ea_d | Form_long_extzq_b_rn_s_ea_e | Form_long_extzq_w_rn_s_ea_e | Form_long_extzq_l_rn_s_ea_e | Form_long_extzq_b_ea_s_ea_d | Form_long_extzq_w_ea_s_ea_d | Form_long_extzq_l_ea_s_ea_d | Form_long_extzw_b_rn_s_ea_e | Form_long_extzw_b_ea_s_ea_d | Form_extralong_fetchadd_b_w_l_q_z_order_o_rn_s_ea_e | Form_extralong_fetchand_b_w_l_q_z_order_o_rn_s_ea_e | Form_extralong_fetchor_b_w_l_q_z_order_o_rn_s_ea_e | Form_extralong_fetchsub_b_w_l_q_z_order_o_rn_s_ea_e | Form_extralong_fetchxor_b_w_l_q_z_order_o_rn_s_ea_e | Form_medium_flshdcache_ea_e | Form_short_halt_plain | Form_extralong_ijcc_rn_i_rn_b_ea_e | Form_extralong_ijcc_rn_i_rn_b_rn_e | Form_extrashort_illegal_plain | Form_short_inc_l_q_z_rn_r | Form_medium_inc_b_w_l_q_z_ea_e | Form_medium_incf_b_w_l_q_z_rn_r | Form_medium_invasid_imm16 | Form_medium_invdcache_ea_e | Form_medium_invicache_ea_e | Form_medium_invpage_ea_e | Form_medium_invpage_rn_r | Form_medium_invtlb_plain | Form_short_jcc_imm8s_i | Form_medium_jcc_imm16s | Form_medium_jcc_imm32s | Form_long_jcc_l_q_z_ea_e | Form_long_jcc_l_q_z_rn_r | Form_short_jmp_imm8s_i | Form_medium_jmp_imm16s | Form_medium_jmp_imm32s | Form_medium_jmp_l_q_z_ea_e | Form_medium_jmp_l_q_z_rn_r | Form_long_lcall_rn_r_ea_e | Form_medium_lcall_rn_s_rn_d | Form_medium_lea_b_w_l_q_z_ea_e_rn_d | Form_medium_lea_b_w_l_q_z_rn_s_rn_d | Form_long_ljmp_rn_r_ea_e | Form_medium_ljmp_rn_s_rn_d | Form_extrashort_lret_plain | Form_long_maxs_b_w_l_q_z_ea_e_rn_d | Form_long_maxs_b_w_l_q_z_rn_s_ea_e | Form_medium_maxs_b_w_l_q_z_rn_s_rn_d | Form_long_maxu_b_w_l_q_z_ea_e_rn_d | Form_long_maxu_b_w_l_q_z_rn_s_ea_e | Form_medium_maxu_b_w_l_q_z_rn_s_rn_d | Form_long_mins_b_w_l_q_z_ea_e_rn_d | Form_long_mins_b_w_l_q_z_rn_s_ea_e | Form_medium_mins_b_w_l_q_z_rn_s_rn_d | Form_long_minu_b_w_l_q_z_ea_e_rn_d | Form_long_minu_b_w_l_q_z_rn_s_ea_e | Form_medium_minu_b_w_l_q_z_rn_s_rn_d | Form_long_mods_b_w_l_q_z_ea_e_rn_d | Form_medium_mods_b_w_l_q_z_rn_s_rn_d | Form_long_modu_b_w_l_q_z_ea_e_rn_d | Form_medium_modu_b_w_l_q_z_rn_s_rn_d | Form_extrashort_mov_q_rn_r_sp | Form_extrashort_mov_q_sp_rn_r | Form_short_mov_l_q_z_rn_s_rn_d | Form_short_mov_b_rn_s_rn_d | Form_short_mov_w_rn_s_rn_d | Form_medium_mov_b_w_l_q_z_rn_s_ea_e | Form_medium_mov_b_w_l_q_z_ea_e_rn_d | Form_long_mov_b_w_l_q_z_ea_s_ea_d | Form_extralong_movcc_b_w_l_q_z_rn_s_ea_e | Form_extralong_movcc_b_w_l_q_z_ea_e_rn_d | Form_long_movcc_b_w_l_q_z_rn_s_rn_d | Form_long_movcu_b_w_l_q_z_ea_s_ea_d | Form_medium_movcu_b_w_l_q_z_rn_s_rn_d | Form_long_movcu_b_w_l_q_z_rn_s_ea_d | Form_long_movcu_b_w_l_q_z_ea_s_rn_d | Form_long_movnt_b_w_l_q_z_rn_s_ea_e | Form_long_movuc_b_w_l_q_z_ea_s_ea_d | Form_medium_movuc_b_w_l_q_z_rn_s_rn_d | Form_long_movuc_b_w_l_q_z_rn_s_ea_d | Form_long_movuc_b_w_l_q_z_ea_s_rn_d | Form_long_movuu_b_w_l_q_z_ea_s_ea_d | Form_long_mul_b_w_l_q_z_ea_e_rn_d | Form_medium_mul_b_w_l_q_z_rn_s_rn_d | Form_medium_mulhs_q_rn_s_rn_d | Form_medium_mulhsu_q_rn_s_rn_d | Form_medium_mulhu_q_rn_s_rn_d | Form_short_neg_l_q_z_rn_r | Form_medium_neg_b_w_l_q_z_ea_e | Form_extrashort_nop_plain | Form_short_not_l_q_z_rn_r | Form_medium_not_b_w_l_q_z_ea_e | Form_short_or_l_q_z_rn_s_rn_d | Form_medium_or_b_w_l_q_z_rn_s_ea_e | Form_medium_or_b_w_l_q_z_ea_e_rn_d | Form_medium_or_b_w_l_q_z_imm8s_ea_e | Form_medium_or_w_l_q_z_imm16s_ea_e | Form_medium_or_l_q_z_imm32s_ea_e | Form_medium_or_q_imm64_ea_e | Form_long_parity_b_w_l_q_z_ea_e_rn_d | Form_medium_parity_b_w_l_q_z_rn_s_rn_d | Form_extrashort_pop_rn_r | Form_short_pop_sreg_s | Form_long_popcnt_b_w_l_q_z_ea_e_rn_d | Form_medium_popcnt_b_w_l_q_z_rn_s_rn_d | Form_extrashort_popp_pairn_i | Form_medium_prefetch_ea_e | Form_medium_prefetchnt_ea_e | Form_long_ptquery_pt_level_i_ea_e_rn_d | Form_long_ptquery_pt_level_i_rn_s_rn_d | Form_extrashort_push_cs | Form_extrashort_push_rn_r | Form_short_push_sreg_s | Form_extrashort_pushp_pairn_i | Form_medium_rdcr_imm16_rn_d | Form_medium_rdflags_rn_d | Form_medium_rdpmc_imm16_rn_d | Form_medium_rdseg_sreg_s_rn_d | Form_medium_rdseg_cs_rn_d | Form_medium_rdstatus_rn_d | Form_medium_repcc_rn_r_instruction | Form_short_reset_plain | Form_medium_restore_ea_e | Form_medium_restore_rn_r | Form_extrashort_ret_plain | Form_short_revbyte_w_rn_r | Form_short_revbyte_l_rn_r | Form_short_revbyte_q_rn_r | Form_medium_revbyte_w_ea_e | Form_medium_revbyte_l_ea_e | Form_medium_revbyte_q_ea_e | Form_extrashort_rfence_plain | Form_short_rol_l_q_z_rn_s_rn_d | Form_long_rol_b_w_l_q_z_rn_s_ea_e | Form_long_rol_b_w_l_q_z_imm6_i_ea_e | Form_short_ror_l_q_z_rn_s_rn_d | Form_long_ror_b_w_l_q_z_rn_s_ea_e | Form_long_ror_b_w_l_q_z_imm6_i_ea_e | Form_short_sar_l_q_z_rn_s_rn_d | Form_long_sar_b_w_l_q_z_rn_s_ea_e | Form_long_sar_b_w_l_q_z_imm6_i_ea_e | Form_medium_save_ea_e | Form_medium_save_rn_r | Form_medium_sbb_b_w_l_q_z_rn_s_rn_d | Form_long_sbb_b_w_l_q_z_rn_s_ea_e | Form_long_sbb_b_w_l_q_z_ea_e_rn_d | Form_long_seglea_b_w_l_q_z_ea_e_rn_d | Form_medium_seglea_b_w_l_q_z_rn_s_rn_d | Form_short_set_rn_r | Form_short_setcc_rn_r | Form_medium_setf_flags_bitmap_m | Form_short_shl_l_q_z_rn_s_rn_d | Form_long_shl_b_w_l_q_z_rn_s_ea_e | Form_long_shl_b_w_l_q_z_imm6_i_ea_e | Form_short_shr_l_q_z_rn_s_rn_d | Form_long_shr_b_w_l_q_z_rn_s_ea_e | Form_long_shr_b_w_l_q_z_imm6_i_ea_e | Form_extrashort_sub_q_8_sp | Form_short_sub_l_q_z_rn_s_rn_d | Form_short_sub_q_imm8_i_sp | Form_medium_sub_q_imm16s_sp | Form_medium_sub_q_imm32s_sp | Form_medium_sub_b_w_l_q_z_rn_s_ea_e | Form_medium_sub_b_w_l_q_z_ea_e_rn_d | Form_long_sub_b_w_l_q_z_imm8s_ea_e | Form_long_sub_w_l_q_z_imm16s_ea_e | Form_long_sub_l_q_z_imm32s_ea_e | Form_medium_sub_q_imm64_ea_e | Form_medium_swpt_rn_p | Form_medium_swpta_rn_p_rn_a | Form_medium_synccache_ea_e | Form_extrashort_syscall_plain | Form_short_test_l_q_z_rn_s_rn_d | Form_long_test_b_w_l_q_z_rn_s_ea_e | Form_medium_test_b_w_l_q_z_ea_e_rn_d | Form_long_testjcc_b_w_l_q_z_rn_s_rn_d_imm8s | Form_long_testjcc_b_w_l_q_z_rn_s_rn_d_imm16s | Form_medium_trace_imm16 | Form_medium_vtop_rn_v_rn_p | Form_extrashort_wait_plain | Form_extrashort_wfence_plain | Form_medium_wrbkdcache_ea_e | Form_medium_wrcr_rn_s_imm16 | Form_medium_wrflags_rn_s | Form_medium_wrseg_rn_d_sreg_s | Form_medium_wrstatus_rn_s | Form_short_xchg_l_q_z_rn_s_rn_d | Form_long_xchg_b_w_l_q_z_rn_s_ea_e | Form_long_xchg_b_w_l_q_z_ea_e_rn_d | Form_short_xor_l_q_z_rn_s_rn_d | Form_medium_xor_b_w_l_q_z_rn_s_ea_e | Form_medium_xor_b_w_l_q_z_ea_e_rn_d | Form_long_xor_b_w_l_q_z_imm8s_ea_e | Form_long_xor_w_l_q_z_imm16s_ea_e | Form_long_xor_l_q_z_imm32s_ea_e | Form_medium_xor_q_imm64_ea_e | Form_extrashort_yield_plain | Form_medium_fabs_s_d_z_fn_s_fn_d | Form_long_fabs_s_d_z_ea_e_fn_d | Form_long_fabs_s_d_z_fn_s_ea_e | Form_medium_fadd_s_d_z_fn_s_fn_d | Form_long_fadd_s_d_z_ea_e_fn_d | Form_extralong_fbndii_s_d_z_fn_l_fn_v_fn_h | Form_extralong_fbndii_s_d_z_fn_l_ea_v_fn_h | Form_extralong_fbndii_s_d_z_ea_l_fn_v_ea_h | Form_extralong_fbndix_s_d_z_fn_l_fn_v_fn_h | Form_extralong_fbndix_s_d_z_fn_l_ea_v_fn_h | Form_extralong_fbndix_s_d_z_ea_l_fn_v_ea_h | Form_extralong_fbndxi_s_d_z_fn_l_fn_v_fn_h | Form_extralong_fbndxi_s_d_z_fn_l_ea_v_fn_h | Form_extralong_fbndxi_s_d_z_ea_l_fn_v_ea_h | Form_extralong_fbndxx_s_d_z_fn_l_fn_v_fn_h | Form_extralong_fbndxx_s_d_z_fn_l_ea_v_fn_h | Form_extralong_fbndxx_s_d_z_ea_l_fn_v_ea_h | Form_medium_fceil_s_d_z_fn_s_fn_d | Form_long_fceil_s_d_z_ea_e_fn_d | Form_long_fceil_s_d_z_fn_s_ea_e | Form_long_fclass_s_d_z_fn_s_rn_d | Form_medium_fclr_fn_d | Form_medium_fcmp_s_d_z_fn_s_fn_d | Form_long_fcmp_s_d_z_ea_e_fn_d | Form_long_fcopysign_s_d_z_fn_s_fn_m_fn_d | Form_medium_fcvt_s_d_z_fn_s_fn_d | Form_long_fcvt_s_d_z_fn_s_rn_d | Form_long_fcvt_s_d_z_rn_s_fn_d | Form_medium_fcvtu_s_d_z_fn_s_fn_d | Form_long_fcvtu_s_d_z_fn_s_rn_d | Form_long_fcvtu_s_d_z_rn_s_fn_d | Form_medium_fdiv_s_d_z_fn_s_fn_d | Form_long_fdiv_s_d_z_ea_e_fn_d | Form_medium_ffloor_s_d_z_fn_s_fn_d | Form_long_ffloor_s_d_z_ea_e_fn_d | Form_long_ffloor_s_d_z_fn_s_ea_e | Form_long_fgetexp_s_d_z_ea_e_fn_d | Form_medium_fgetexp_s_d_z_fn_s_fn_d | Form_long_fgetman_s_d_z_ea_e_fn_d | Form_medium_fgetman_s_d_z_fn_s_fn_d | Form_long_fint_s_d_z_ea_e_fn_d | Form_medium_fint_s_d_z_fn_s_fn_d | Form_long_fint_s_d_z_fn_s_ea_e | Form_long_fintrz_s_d_z_ea_e_fn_d | Form_medium_fintrz_s_d_z_fn_s_fn_d | Form_long_fintrz_s_d_z_fn_s_ea_e | Form_long_fmadd_s_d_z_fn_l_fn_r_fn_d | Form_extralong_fmadd_s_d_z_ea_l_fn_r_fn_d | Form_extralong_fmadd_s_d_z_fn_l_ea_r_fn_d | Form_medium_fmax_s_d_z_fn_s_fn_d | Form_long_fmax_s_d_z_ea_e_fn_d | Form_medium_fmin_s_d_z_fn_s_fn_d | Form_long_fmin_s_d_z_ea_e_fn_d | Form_long_fmod_s_d_z_ea_e_fn_d | Form_medium_fmod_s_d_z_fn_s_fn_d | Form_medium_fmov_s_d_z_fn_s_fn_d | Form_long_fmov_s_d_z_ea_e_fn_d | Form_long_fmov_s_d_z_fn_s_ea_e | Form_long_fmovcc_fn_s_fn_d | Form_long_fmovcc_s_d_z_ea_e_fn_d | Form_long_fmovcc_s_d_z_fn_s_ea_e | Form_medium_fmovcr_s_d_z_fconst_id_fn_d | Form_long_fmsub_s_d_z_fn_l_fn_r_fn_d | Form_extralong_fmsub_s_d_z_ea_l_fn_r_fn_d | Form_extralong_fmsub_s_d_z_fn_l_ea_r_fn_d | Form_medium_fmul_s_d_z_fn_s_fn_d | Form_long_fmul_s_d_z_ea_e_fn_d | Form_medium_fneg_s_d_z_fn_s_fn_d | Form_long_fneg_s_d_z_ea_e_fn_d | Form_long_fneg_s_d_z_fn_s_ea_e | Form_long_fnmadd_s_d_z_fn_l_fn_r_fn_d | Form_extralong_fnmadd_s_d_z_ea_l_fn_r_fn_d | Form_extralong_fnmadd_s_d_z_fn_l_ea_r_fn_d | Form_long_fnmsub_s_d_z_fn_l_fn_r_fn_d | Form_extralong_fnmsub_s_d_z_ea_l_fn_r_fn_d | Form_extralong_fnmsub_s_d_z_fn_l_ea_r_fn_d | Form_extrashort_fpopp_fpairn_i | Form_extrashort_fpushp_fpairn_i | Form_long_frem_s_d_z_ea_e_fn_d | Form_medium_frem_s_d_z_fn_s_fn_d | Form_medium_fround_s_d_z_fn_s_fn_d | Form_long_fround_s_d_z_ea_e_fn_d | Form_long_fround_s_d_z_fn_s_ea_e | Form_long_fscale_s_d_z_ea_e_fn_d | Form_medium_fscale_s_d_z_fn_s_fn_d | Form_medium_fsqrt_s_d_z_fn_s_fn_d | Form_long_fsqrt_s_d_z_ea_e_fn_d | Form_long_fsqrt_s_d_z_fn_s_ea_e | Form_medium_fsub_s_d_z_fn_s_fn_d | Form_long_fsub_s_d_z_ea_e_fn_d | Form_long_ftest_s_d_z_ea_e | Form_medium_ftest_s_d_z_fn_s | Form_medium_ftrunc_s_d_z_fn_s_fn_d | Form_long_ftrunc_s_d_z_ea_e_fn_d | Form_long_ftrunc_s_d_z_fn_s_ea_e | Form_medium_fxchg_fn_l_fn_r | Form_medium_rdfflags_rn_d | Form_medium_rdfstatus_rn_d | Form_medium_wrfflags_rn_s | Form_medium_wrfstatus_rn_s | Form_long_facosa_s_d_z_fn_s_fn_d | Form_long_fasina_s_d_z_fn_s_fn_d | Form_long_fatana_s_d_z_fn_s_fn_d | Form_long_fatanha_s_d_z_fn_s_fn_d | Form_long_fcosa_s_d_z_fn_s_fn_d | Form_long_fcosha_s_d_z_fn_s_fn_d | Form_long_fetoxa_s_d_z_fn_s_fn_d | Form_long_fetoxm1a_s_d_z_fn_s_fn_d | Form_long_flog10a_s_d_z_fn_s_fn_d | Form_long_flog2a_s_d_z_fn_s_fn_d | Form_long_flogna_s_d_z_fn_s_fn_d | Form_long_flognp1a_s_d_z_fn_s_fn_d | Form_long_fsina_s_d_z_fn_s_fn_d | Form_long_fsincosa_s_d_z_fn_s_fn_d_fn_c | Form_long_fsinha_s_d_z_fn_s_fn_d | Form_long_ftana_s_d_z_fn_s_fn_d | Form_long_ftanha_s_d_z_fn_s_fn_d | Form_long_ftentoxa_s_d_z_fn_s_fn_d | Form_long_ftwotoxa_s_d_z_fn_s_fn_d | Form_long_vdup_b_w_l_q_z_rn_r_vn_v | Form_long_vdup_h_s_d_z_fn_r_vn_v | Form_long_vdup_b_imm8_vn_v | Form_long_vdup_w_imm16_vn_v | Form_long_vdup_l_imm32_vn_v | Form_long_vdup_q_imm64_vn_v | Form_long_vmov_vn_v_vn_w | Form_extralong_vmov_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmov_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmov_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_phead_b_w_l_q_z_rn_r_pn_p | Form_long_ptail_b_w_l_q_z_rn_r_pn_p | Form_long_pfirst_b_w_l_q_z_pn_p_rn_r | Form_long_plast_b_w_l_q_z_pn_p_rn_r | Form_long_pcount_b_w_l_q_z_pn_p_rn_r | Form_long_pand_pn_p_pn_q | Form_long_por_pn_p_pn_q | Form_long_pxor_pn_p_pn_q | Form_long_punpklo_b_w_l_z_pn_p_pn_q | Form_long_punpkhi_b_w_l_z_pn_p_pn_q | Form_long_ppacklo_w_l_q_z_pn_p_pn_q | Form_long_ppackhi_w_l_q_z_pn_p_pn_q | Form_long_vclr_vn_v | Form_long_vindex_b_w_l_q_z_vn_v | Form_long_vlcnt_b_w_l_q_z_rn_r | Form_long_vlcadd_b_w_l_q_z_imm8s_rn_r | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_rn_i_mul_rn_s_vn_v | Form_xxlong_vgather1_l_pn_p_vn_x_rn_i_vn_v | Form_xxlong_vgather1_q_pn_p_vn_x_rn_i_vn_v | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_vn_v | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_vn_v | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp8s_vn_v | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp16s_vn_v | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp32s_vn_v | Form_xxlong_vgather1_b_w_l_q_z_pn_p_rn_b_add_vn_x_rn_i_mul_scale_add_disp64_vn_v | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_rn_i_mul_rn_s | Form_xxlong_vscatter1_l_pn_p_vn_v_vn_x_rn_i | Form_xxlong_vscatter1_q_pn_p_vn_v_vn_x_rn_i | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp8s | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp16s | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp32s | Form_xxlong_vscatter1_b_w_l_q_z_pn_p_vn_v_rn_b_add_vn_x_rn_i_mul_scale_add_disp64 | Form_long_ptrue_b_w_l_q_z_pn_p | Form_long_pfalse_pn_p | Form_long_pnot_pn_p | Form_long_bpany_pn_p_imm32s | Form_xxlong_bpany_pn_p_ea_e | Form_long_bpnone_pn_p_imm32s | Form_xxlong_bpnone_pn_p_ea_e | Form_long_bpall_b_w_l_q_z_pn_p_imm32s | Form_xxlong_bpall_b_w_l_q_z_pn_p_ea_e | Form_long_vneg_b_w_l_q_h_s_d_x_pn_p_vn_v | Form_xxlong_vneg_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v | Form_xxlong_vneg_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e | Form_long_vabs_b_w_l_q_h_s_d_x_pn_p_vn_v | Form_xxlong_vabs_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v | Form_xxlong_vabs_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e | Form_long_vnot_b_w_l_q_z_pn_p_vn_v | Form_xxlong_vnot_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vnot_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vclz_b_w_l_q_z_pn_p_vn_v | Form_xxlong_vclz_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vclz_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vctz_b_w_l_q_z_pn_p_vn_v | Form_xxlong_vctz_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vctz_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vcls_b_w_l_q_z_pn_p_vn_v | Form_xxlong_vcls_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vcls_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vcts_b_w_l_q_z_pn_p_vn_v | Form_xxlong_vcts_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vcts_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vpopcnt_b_w_l_q_z_pn_p_vn_v | Form_xxlong_vpopcnt_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vpopcnt_b_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vrevbyte_w_l_q_z_pn_p_vn_v | Form_xxlong_vrevbyte_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vrevbyte_w_l_q_z_pn_p_vn_v_ea_e | Form_long_vsqrt_h_s_d_z_pn_p_vn_v | Form_xxlong_vsqrt_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vsqrt_h_s_d_z_pn_p_vn_v_ea_e | Form_long_vround_h_s_d_z_pn_p_vn_v | Form_xxlong_vround_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vround_h_s_d_z_pn_p_vn_v_ea_e | Form_long_vtrunc_h_s_d_z_pn_p_vn_v | Form_xxlong_vtrunc_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vtrunc_h_s_d_z_pn_p_vn_v_ea_e | Form_long_vfloor_h_s_d_z_pn_p_vn_v | Form_xxlong_vfloor_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vfloor_h_s_d_z_pn_p_vn_v_ea_e | Form_long_vceil_h_s_d_z_pn_p_vn_v | Form_xxlong_vceil_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vceil_h_s_d_z_pn_p_vn_v_ea_e | Form_long_vclass_h_s_d_z_pn_p_vn_v | Form_xxlong_vclass_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vclass_h_s_d_z_pn_p_vn_v_ea_e | Form_long_pperm_b_w_l_q_z_vn_v_pn_p | Form_long_pslideup_b_w_l_q_z_imm6_i_pn_p | Form_long_pslidedn_b_w_l_q_z_imm6_i_pn_p | Form_extralong_vcmpcc_b_w_l_q_x_pn_p_vn_v_vn_w_pn_q | Form_extralong_vcmpcc_h_s_d_x_pn_p_vn_v_vn_w_pn_q | Form_xxlong_vcmpcc_b_w_l_q_x_pn_p_vn_v_ea_e_pn_q | Form_xxlong_vcmpcc_h_s_d_x_pn_p_vn_v_ea_e_pn_q | Form_extralong_vtestz_b_w_l_q_z_pn_p_vn_v_vn_w_pn_q | Form_xxlong_vtestz_b_w_l_q_z_pn_p_vn_v_ea_e_pn_q | Form_extralong_vtestnz_b_w_l_q_z_pn_p_vn_v_vn_w_pn_q | Form_xxlong_vtestnz_b_w_l_q_z_pn_p_vn_v_ea_e_pn_q | Form_extralong_vadd_b_w_l_q_h_s_d_x_pn_p_vn_v_vn_w | Form_xxlong_vadd_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v | Form_xxlong_vadd_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e | Form_extralong_vsub_b_w_l_q_h_s_d_x_pn_p_vn_v_vn_w | Form_xxlong_vsub_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v | Form_xxlong_vsub_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e | Form_extralong_vmul_b_w_l_q_h_s_d_x_pn_p_vn_v_vn_w | Form_xxlong_vmul_b_w_l_q_h_s_d_x_pn_p_ea_e_vn_v | Form_xxlong_vmul_b_w_l_q_h_s_d_x_pn_p_vn_v_ea_e | Form_extralong_vand_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vand_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vand_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vor_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vor_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vor_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vxor_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vxor_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vxor_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vmins_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmins_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmins_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vminu_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vminu_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vminu_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vmaxs_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmaxs_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmaxs_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vmaxu_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmaxu_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmaxu_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vmulhs_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmulhs_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmulhs_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vmulhu_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmulhu_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmulhu_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vmulhsu_b_w_l_q_z_pn_p_vn_v_vn_w | Form_xxlong_vmulhsu_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vmulhsu_b_w_l_q_z_pn_p_vn_v_ea_e | Form_extralong_vshl_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vshl_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_xxlong_vshl_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vshl_b_w_l_q_z_pn_p_vn_v_ea_e | Form_xxlong_vshl_b_w_l_q_z_pn_p_imm6_i_ea_e | Form_extralong_vshr_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vshr_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_xxlong_vshr_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vshr_b_w_l_q_z_pn_p_vn_v_ea_e | Form_xxlong_vshr_b_w_l_q_z_pn_p_imm6_i_ea_e | Form_extralong_vsar_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vsar_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_xxlong_vsar_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vsar_b_w_l_q_z_pn_p_vn_v_ea_e | Form_xxlong_vsar_b_w_l_q_z_pn_p_imm6_i_ea_e | Form_extralong_vrol_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vrol_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_xxlong_vrol_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vrol_b_w_l_q_z_pn_p_vn_v_ea_e | Form_xxlong_vrol_b_w_l_q_z_pn_p_imm6_i_ea_e | Form_extralong_vror_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vror_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_xxlong_vror_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_vror_b_w_l_q_z_pn_p_vn_v_ea_e | Form_xxlong_vror_b_w_l_q_z_pn_p_imm6_i_ea_e | Form_extralong_vmin_h_s_d_z_pn_p_vn_v_vn_w | Form_xxlong_vmin_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vmin_h_s_d_z_pn_p_vn_v_ea_e | Form_extralong_vmax_h_s_d_z_pn_p_vn_v_vn_w | Form_xxlong_vmax_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vmax_h_s_d_z_pn_p_vn_v_ea_e | Form_extralong_vdiv_h_s_d_z_pn_p_vn_v_vn_w | Form_xxlong_vdiv_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vdiv_h_s_d_z_pn_p_vn_v_ea_e | Form_extralong_vcopysign_h_s_d_z_pn_p_vn_v_vn_w | Form_xxlong_vcopysign_h_s_d_z_pn_p_ea_e_vn_v | Form_xxlong_vcopysign_h_s_d_z_pn_p_vn_v_ea_e | Form_extralong_vextzw_b_z_pn_p_vn_v_vn_w | Form_extralong_vextsw_b_z_pn_p_vn_v_vn_w | Form_extralong_vextzl_b_w_z_pn_p_vn_v_vn_w | Form_extralong_vextsl_b_w_z_pn_p_vn_v_vn_w | Form_extralong_vextzq_b_w_l_z_pn_p_vn_v_vn_w | Form_extralong_vextsq_b_w_l_z_pn_p_vn_v_vn_w | Form_extralong_vtruncb_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vtruncw_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vtruncl_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvts_h_d_z_pn_p_vn_v_vn_w | Form_extralong_vcvts_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvtd_h_s_z_pn_p_vn_v_vn_w | Form_extralong_vcvtd_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvtus_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvtud_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvtl_h_s_d_z_pn_p_vn_v_vn_w | Form_extralong_vcvtul_h_s_d_z_pn_p_vn_v_vn_w | Form_extralong_vcvtq_h_s_d_z_pn_p_vn_v_vn_w | Form_extralong_vcvtuq_h_s_d_z_pn_p_vn_v_vn_w | Form_extralong_vperm_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vziplo_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vziphi_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vuziplo_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vuziphi_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vtrnlo_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vtrnhi_b_w_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvth_s_d_z_pn_p_vn_v_vn_w | Form_extralong_vcvth_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vcvtuh_l_q_z_pn_p_vn_v_vn_w | Form_extralong_vmadd_h_s_d_z_pn_p_vn_v_vn_w_vn_y | Form_extralong_vmsub_h_s_d_z_pn_p_vn_v_vn_w_vn_y | Form_extralong_vnmadd_h_s_d_z_pn_p_vn_v_vn_w_vn_y | Form_extralong_vnmsub_h_s_d_z_pn_p_vn_v_vn_w_vn_y | Form_extralong_vslice_b_w_l_q_z_pn_p_vn_v_imm6_i_vn_w | Form_extralong_vslideup_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_extralong_vslidedn_b_w_l_q_z_pn_p_imm6_i_vn_v | Form_extralong_vextract_b_w_l_q_z_vn_v_rn_r_rn_s | Form_extralong_vextract_h_s_d_z_vn_v_rn_r_fn_s | Form_extralong_vinsert_b_w_l_q_z_rn_r_rn_s_vn_v | Form_extralong_vinsert_h_s_d_z_fn_r_rn_s_vn_v | Form_extralong_vredadd_b_w_l_q_z_pn_p_vn_v_rn_r | Form_extralong_vredadd_h_s_d_z_pn_p_vn_v_fn_r | Form_xxlong_vredadd_b_w_l_q_z_pn_p_ea_e_rn_r | Form_xxlong_vredadd_h_s_d_z_pn_p_ea_e_fn_r | Form_extralong_vredmins_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredmins_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredminu_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredminu_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredmaxs_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredmaxs_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredmaxu_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredmaxu_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredand_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredand_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredor_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredor_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredxor_b_w_l_q_z_pn_p_vn_v_rn_r | Form_xxlong_vredxor_b_w_l_q_z_pn_p_ea_e_rn_r | Form_extralong_vredmin_h_s_d_z_pn_p_vn_v_fn_r | Form_xxlong_vredmin_h_s_d_z_pn_p_ea_e_fn_r | Form_extralong_vredmax_h_s_d_z_pn_p_vn_v_fn_r | Form_xxlong_vredmax_h_s_d_z_pn_p_ea_e_fn_r | Form_extralong_psel_pn_p_pn_q_pn_h | Form_extralong_pziplo_b_w_l_q_z_pn_p_pn_q_pn_h | Form_extralong_pziphi_b_w_l_q_z_pn_p_pn_q_pn_h | Form_extralong_puziplo_b_w_l_q_z_pn_p_pn_q_pn_h | Form_extralong_puziphi_b_w_l_q_z_pn_p_pn_q_pn_h | Form_extralong_ptrnlo_b_w_l_q_z_pn_p_pn_q_pn_h | Form_extralong_ptrnhi_b_w_l_q_z_pn_p_pn_q_pn_h | Form_extralong_pslice_b_w_l_q_z_pn_p_imm6_i_pn_q | Form_xxlong_vmovz_b_w_l_q_z_pn_p_ea_e_vn_v | Form_xxlong_ploop_b_w_l_q_z_rn_r_rn_s_pn_p_ea_e | Form_xxlong_pmov_ea_e_pn_p | Form_xxlong_pmov_pn_p_ea_e
enum Operand_type = OperandType_CS | OperandType_EA | OperandType_FEA | OperandType_FPAIRn | OperandType_Fn | OperandType_PAIRn | OperandType_Pn | OperandType_Rn | OperandType_SP | OperandType_SREG | OperandType_VEA | OperandType_Vn | OperandType_condition | OperandType_fconstid | OperandType_flags_bitmap | OperandType_imm | OperandType_imm16 | OperandType_imm16s | OperandType_imm32 | OperandType_imm32s | OperandType_imm6 | OperandType_imm64 | OperandType_imm7 | OperandType_imm8 | OperandType_imm8s | OperandType_memory_order | OperandType_pt_level | OperandType_size_BW | OperandType_size_BWL | OperandType_size_BWLQ | OperandType_size_B_ONLY | OperandType_size_HD | OperandType_size_HS | OperandType_size_HSD | OperandType_size_LQ | OperandType_size_Q_ONLY | OperandType_size_SD | OperandType_size_VTYPE | OperandType_size_V_BW | OperandType_size_V_LQ | OperandType_size_V_SD | OperandType_size_WLQ
enum Size_code = Size_B | Size_D | Size_H | Size_L | Size_Q | Size_S | Size_W
enum Field_id = Field_a | Field_b | Field_c | Field_d | Field_e | Field_h | Field_i | Field_l | Field_m | Field_o | Field_p | Field_q | Field_r | Field_s | Field_v | Field_w | Field_x | Field_y | Field_z
enum Operand_id = Operand_address | Operand_asid | Operand_base | Operand_bit_index | Operand_bound | Operand_cc | Operand_constant_id | Operand_cos_dst | Operand_count | Operand_counter | Operand_counter_id | Operand_cr | Operand_cursor | Operand_desired | Operand_disp16s | Operand_disp32s | Operand_disp64 | Operand_disp8s | Operand_dst | Operand_expected | Operand_govern | Operand_hi | Operand_high | Operand_imm | Operand_immediate | Operand_index | Operand_level | Operand_lhs | Operand_lo | Operand_low_dst | Operand_magnitude_src | Operand_marker | Operand_mask | Operand_memory | Operand_new_cs | Operand_new_ptcr | Operand_offset | Operand_order | Operand_page | Operand_pair_id | Operand_phys | Operand_predicate | Operand_quotient | Operand_reg | Operand_remainder | Operand_remaining | Operand_rhs | Operand_seg | Operand_select | Operand_sign_src | Operand_sin_dst | Operand_src | Operand_stride | Operand_target | Operand_value | Operand_virt
enum Operand_domain = OperandDomain_user
enum Ea_role = EaRole_address | EaRole_base | EaRole_control_target | EaRole_index | EaRole_segment | EaRole_value
enum Ea_width = EaWidth_B | EaWidth_L | EaWidth_Q | EaWidth_W | EaWidth_operation_size | EaWidth_predicate
enum Ea_profile = EaProfile_ea | EaProfile_fea | EaProfile_vea
enum Ea_form_id = EaForm_absolute_32s | EaForm_absolute_64 | EaForm_default_segment_base_postincrement | EaForm_default_segment_base_predecrement | EaForm_explicit_segment_base | EaForm_explicit_segment_base_postincrement | EaForm_explicit_segment_base_predecrement | EaForm_explicit_segment_index | EaForm_explicit_segment_index_postincrement | EaForm_explicit_segment_index_predecrement | EaForm_explicit_segment_zero_base | EaForm_explicit_segment_zero_base_index | EaForm_explicit_segment_zero_base_index_postincrement | EaForm_explicit_segment_zero_base_index_predecrement | EaForm_ext1 | EaForm_ext1_disp16s | EaForm_ext1_disp32s | EaForm_ext1_disp64 | EaForm_ext1_disp8s | EaForm_ext2 | EaForm_ext2_disp16s | EaForm_ext2_disp32s | EaForm_ext2_disp64 | EaForm_ext2_disp8s | EaForm_immediate_16s | EaForm_immediate_32s | EaForm_immediate_64 | EaForm_immediate_8s | EaForm_immediate_df | EaForm_immediate_sf | EaForm_program_counter_disp16s | EaForm_program_counter_disp32s | EaForm_program_counter_disp64 | EaForm_program_counter_disp8s | EaForm_program_counter_index | EaForm_program_counter_index_postincrement | EaForm_program_counter_index_predecrement | EaForm_register_disp16s | EaForm_register_disp32s | EaForm_register_disp64 | EaForm_register_disp8s | EaForm_register_indirect | EaForm_stack_pointer_disp16s | EaForm_stack_pointer_disp32s | EaForm_stack_pointer_disp64 | EaForm_stack_pointer_disp8s | EaForm_stack_pointer_index | EaForm_stack_pointer_index_postincrement | EaForm_stack_pointer_index_predecrement | EaForm_stack_pointer_indirect
enum Ea_descriptor_family = EaDescriptor_ext1 | EaDescriptor_ext2
enum Ea_kind = EaKind_escape | EaKind_float_immediate | EaKind_immediate | EaKind_memory
enum Ea_segment = EaSegment_CS | EaSegment_SS | EaSegment_default | EaSegment_explicit
enum Ea_base = EaBase_PC | EaBase_SP | EaBase_zero
enum Ea_update_target = EaUpdateTarget_b | EaUpdateTarget_i
enum Ea_update_mode = EaUpdateMode_postincrement | EaUpdateMode_predecrement

enum Cpuid_flag =
  CpuidFlag_FP
| CpuidFlag_FPTRANSA
| CpuidFlag_VECTOR

enum Semantic_route =
  RouteIntegerUnary
| RouteIntegerAlu
| RouteCoreControl
| RouteIntegerBitfield
| RouteBounds
| RouteControlFlow
| RouteIntegerMulDiv
| RouteAtomics
| RouteSystemRegisters
| RouteCache
| RouteTlbContext
| RouteEaUtility
| RouteDataMovement
| RouteFpu
| RouteFpuTranscendental
| RouteVector

enum Instruction_set =
  BaseSet
| FpuSet
| FpuTranscendentalSet
| VectorSet
| VectorFpuSet

enum Fault_kind =
  NoFault
| IllegalInstruction
| PrivilegeFault
| ExtensionUnavailable
| InvalidControlState
| DivideByZero
| DivideOverflow
| BoundsFault
| AlignmentFault
| TranslationFault
| AccessFault
| EventFault
| FloatingPointFault
| VectorRangeFault

enum Effect_kind =
  NoEffect
| ReadMemory
| WriteMemory
| AtomicMemory
| TranslateAddress
| CacheOperation
| TlbOperation
| ControlRegisterAccess
| EventDelivery
| TraceMarker
| HaltProcessor
| ResetProcessor
| RepeatBody
| FenceOperation
| IntegerCompute
| FloatingPointCompute
| TranscendentalCompute

enum Event_frame_type =
  EventFrameBasic
| EventFrameError
| EventFramePage
| EventFrameAuxiliary

enum Event_family =
  EventFamilyNone
| EventFamily_DEBUG
| EventFamily_PRIVILEGE
| EventFamily_CONTROL_TRANSFER
| EventFamily_INTEGER_DIVIDE
| EventFamily_INSTRUCTION_VALIDATION
| EventFamily_ADDRESS_TRANSLATION
| EventFamily_PHYSICAL_ACCESS
| EventFamily_CONTROL_STATE
| EventFamily_BUS_FAILURE
| EventFamily_EVENT_DELIVERY_FAILURE
| EventFamily_MACHINE_STATE
| EventFamily_FLOATING_POINT
| EventFamily_VECTOR_RANGE

enum Architectural_event =
  Event_DEBUG_TRACE
| Event_BREAKPOINT
| Event_PRIVILEGE_VIOLATION
| Event_SYSTEM_CALL
| Event_DIVIDE_BY_ZERO
| Event_SIGNED_DIVIDE_OVERFLOW
| Event_INVALID_OPCODE
| Event_INVALID_ADDRESSING_FORM
| Event_RESERVED_INSTRUCTION_ENCODING
| Event_UNAVAILABLE_INSTRUCTION_EXTENSION
| Event_EXPLICIT_ILLEGAL_INSTRUCTION
| Event_TRUNCATED_INSTRUCTION
| Event_INVALID_OPERAND_RELATION
| Event_PAGE_NOT_PRESENT
| Event_PAGE_PERMISSION_VIOLATION
| Event_MALFORMED_PAGE_TABLE_ENTRY
| Event_NONCANONICAL_ADDRESS
| Event_SEGMENT_BOUNDS_VIOLATION
| Event_ATOMIC_ALIGNMENT_FAULT
| Event_MEMORY_TYPE_FAULT
| Event_PHYSICAL_ADDRESS_FAULT
| Event_MMIO_ALIGNMENT_FAULT
| Event_UNSUPPORTED_MMIO_OPERATION
| Event_INVALID_CONTROL_SELECTOR
| Event_RESERVED_CONTROL_BITS
| Event_INVALID_CONTROL_IMAGE
| Event_INVALID_CONTROL_TRANSITION
| Event_BUS_NO_RESPONDER
| Event_BUS_ACCESS_DENIED
| Event_BUS_TIMEOUT
| Event_BUS_DATA_ERROR
| Event_BUS_OTHER_ERROR
| Event_EVENT_ENTRY_STATE_FAILURE
| Event_EVENT_STACK_STATE_FAILURE
| Event_EVENT_FRAME_ADDRESS_FAILURE
| Event_EVENT_FRAME_STORE_FAILURE
| Event_MACHINE_CHECK
| Event_INTERRUPT
| Event_NMI
| Event_FLOATING_POINT_EXCEPTION
| Event_VECTOR_LOOP_OFFSET_OUT_OF_RANGE
| Event_VECTOR_LANE_INDEX_OUT_OF_RANGE

enum Semantic_operation =
  Op_ABS
| Op_ADC
| Op_ADD
| Op_AFENCE
| Op_AND
| Op_BCHG
| Op_BCLR
| Op_BKPT
| Op_BNDSII
| Op_BNDSIX
| Op_BNDSXI
| Op_BNDSXX
| Op_BNDUII
| Op_BNDUIX
| Op_BNDUXI
| Op_BNDUXX
| Op_BSET
| Op_BTEST
| Op_CALL
| Op_CALLcc
| Op_CLMUL
| Op_CLMULH
| Op_CLR
| Op_CLS
| Op_CLZ
| Op_CMP
| Op_CMPJcc
| Op_CMPXCHG
| Op_CPUID
| Op_CTS
| Op_CTZ
| Op_DEC
| Op_DECF
| Op_DIVMODS
| Op_DIVMODU
| Op_DIVS
| Op_DIVU
| Op_DJcc
| Op_ERET
| Op_EXTRACT
| Op_EXTSL
| Op_EXTSQ
| Op_EXTSW
| Op_EXTZL
| Op_EXTZQ
| Op_EXTZW
| Op_FETCHADD
| Op_FETCHAND
| Op_FETCHOR
| Op_FETCHSUB
| Op_FETCHXOR
| Op_FLSHDCACHE
| Op_HALT
| Op_IJcc
| Op_ILLEGAL
| Op_INC
| Op_INCF
| Op_INVASID
| Op_INVDCACHE
| Op_INVICACHE
| Op_INVPAGE
| Op_INVTLB
| Op_Jcc
| Op_JMP
| Op_LCALL
| Op_LEA
| Op_LJMP
| Op_LRET
| Op_MAXS
| Op_MAXU
| Op_MINS
| Op_MINU
| Op_MODS
| Op_MODU
| Op_MOV
| Op_MOVcc
| Op_MOVCU
| Op_MOVNT
| Op_MOVUC
| Op_MOVUU
| Op_MUL
| Op_MULHS
| Op_MULHSU
| Op_MULHU
| Op_NEG
| Op_NOP
| Op_NOT
| Op_OR
| Op_PARITY
| Op_POP
| Op_POPCNT
| Op_POPP
| Op_PREFETCH
| Op_PREFETCHNT
| Op_PTQUERY
| Op_PUSH
| Op_PUSHP
| Op_RDCR
| Op_RDFLAGS
| Op_RDPMC
| Op_RDSEG
| Op_RDSTATUS
| Op_REPcc
| Op_RESET
| Op_RESTORE
| Op_RET
| Op_REVBYTE
| Op_RFENCE
| Op_ROL
| Op_ROR
| Op_SAR
| Op_SAVE
| Op_SBB
| Op_SEGLEA
| Op_SET
| Op_SETcc
| Op_SETF
| Op_SHL
| Op_SHR
| Op_SUB
| Op_SWPT
| Op_SWPTA
| Op_SYNCCACHE
| Op_SYSCALL
| Op_TEST
| Op_TESTJcc
| Op_TRACE
| Op_VTOP
| Op_WAIT
| Op_WFENCE
| Op_WRBKDCACHE
| Op_WRCR
| Op_WRFLAGS
| Op_WRSEG
| Op_WRSTATUS
| Op_XCHG
| Op_XOR
| Op_YIELD
| Op_FABS
| Op_FADD
| Op_FBNDII
| Op_FBNDIX
| Op_FBNDXI
| Op_FBNDXX
| Op_FCEIL
| Op_FCLASS
| Op_FCLR
| Op_FCMP
| Op_FCOPYSIGN
| Op_FCVT
| Op_FCVTU
| Op_FDIV
| Op_FFLOOR
| Op_FGETEXP
| Op_FGETMAN
| Op_FINT
| Op_FINTRZ
| Op_FMADD
| Op_FMAX
| Op_FMIN
| Op_FMOD
| Op_FMOV
| Op_FMOVcc
| Op_FMOVCR
| Op_FMSUB
| Op_FMUL
| Op_FNEG
| Op_FNMADD
| Op_FNMSUB
| Op_FPOPP
| Op_FPUSHP
| Op_FREM
| Op_FROUND
| Op_FSCALE
| Op_FSQRT
| Op_FSUB
| Op_FTEST
| Op_FTRUNC
| Op_FXCHG
| Op_RDFFLAGS
| Op_RDFSTATUS
| Op_WRFFLAGS
| Op_WRFSTATUS
| Op_FACOSA
| Op_FASINA
| Op_FATANA
| Op_FATANHA
| Op_FCOSA
| Op_FCOSHA
| Op_FETOXA
| Op_FETOXM1A
| Op_FLOG10A
| Op_FLOG2A
| Op_FLOGNA
| Op_FLOGNP1A
| Op_FSINA
| Op_FSINCOSA
| Op_FSINHA
| Op_FTANA
| Op_FTANHA
| Op_FTENTOXA
| Op_FTWOTOXA
| Op_VDUP
| Op_VMOV
| Op_PHEAD
| Op_PTAIL
| Op_PFIRST
| Op_PLAST
| Op_PCOUNT
| Op_PAND
| Op_POR
| Op_PXOR
| Op_PUNPKLO
| Op_PUNPKHI
| Op_PPACKLO
| Op_PPACKHI
| Op_VCLR
| Op_VINDEX
| Op_VLCNT
| Op_VLCADD
| Op_VGATHER1
| Op_VSCATTER1
| Op_PTRUE
| Op_PFALSE
| Op_PNOT
| Op_BPANY
| Op_BPNONE
| Op_BPALL
| Op_VNEG
| Op_VABS
| Op_VNOT
| Op_VCLZ
| Op_VCTZ
| Op_VCLS
| Op_VCTS
| Op_VPOPCNT
| Op_VREVBYTE
| Op_VSQRT
| Op_VROUND
| Op_VTRUNC
| Op_VFLOOR
| Op_VCEIL
| Op_VCLASS
| Op_PPERM
| Op_PSLIDEUP
| Op_PSLIDEDN
| Op_VCMPcc
| Op_VTESTZ
| Op_VTESTNZ
| Op_VADD
| Op_VSUB
| Op_VMUL
| Op_VAND
| Op_VOR
| Op_VXOR
| Op_VMINS
| Op_VMINU
| Op_VMAXS
| Op_VMAXU
| Op_VMULHS
| Op_VMULHU
| Op_VMULHSU
| Op_VSHL
| Op_VSHR
| Op_VSAR
| Op_VROL
| Op_VROR
| Op_VMIN
| Op_VMAX
| Op_VDIV
| Op_VCOPYSIGN
| Op_VEXTZW
| Op_VEXTSW
| Op_VEXTZL
| Op_VEXTSL
| Op_VEXTZQ
| Op_VEXTSQ
| Op_VTRUNCB
| Op_VTRUNCW
| Op_VTRUNCL
| Op_VCVTS
| Op_VCVTD
| Op_VCVTUS
| Op_VCVTUD
| Op_VCVTL
| Op_VCVTUL
| Op_VCVTQ
| Op_VCVTUQ
| Op_VPERM
| Op_VZIPLO
| Op_VZIPHI
| Op_VUZIPLO
| Op_VUZIPHI
| Op_VTRNLO
| Op_VTRNHI
| Op_VCVTH
| Op_VCVTUH
| Op_VMADD
| Op_VMSUB
| Op_VNMADD
| Op_VNMSUB
| Op_VSLICE
| Op_VSLIDEUP
| Op_VSLIDEDN
| Op_VEXTRACT
| Op_VINSERT
| Op_VREDADD
| Op_VREDMINS
| Op_VREDMINU
| Op_VREDMAXS
| Op_VREDMAXU
| Op_VREDAND
| Op_VREDOR
| Op_VREDXOR
| Op_VREDMIN
| Op_VREDMAX
| Op_PSEL
| Op_PZIPLO
| Op_PZIPHI
| Op_PUZIPLO
| Op_PUZIPHI
| Op_PTRNLO
| Op_PTRNHI
| Op_PSLICE
| Op_VMOVZ
| Op_PLOOP
| Op_PMOV

function semantic_route(operation : Semantic_operation) -> Semantic_route = match operation {
  Op_ABS => RouteIntegerUnary,
  Op_ADC => RouteIntegerAlu,
  Op_ADD => RouteIntegerAlu,
  Op_AFENCE => RouteCoreControl,
  Op_AND => RouteIntegerAlu,
  Op_BCHG => RouteIntegerBitfield,
  Op_BCLR => RouteIntegerBitfield,
  Op_BKPT => RouteCoreControl,
  Op_BNDSII => RouteBounds,
  Op_BNDSIX => RouteBounds,
  Op_BNDSXI => RouteBounds,
  Op_BNDSXX => RouteBounds,
  Op_BNDUII => RouteBounds,
  Op_BNDUIX => RouteBounds,
  Op_BNDUXI => RouteBounds,
  Op_BNDUXX => RouteBounds,
  Op_BSET => RouteIntegerBitfield,
  Op_BTEST => RouteIntegerBitfield,
  Op_CALL => RouteControlFlow,
  Op_CALLcc => RouteControlFlow,
  Op_CLMUL => RouteIntegerMulDiv,
  Op_CLMULH => RouteIntegerMulDiv,
  Op_CLR => RouteIntegerUnary,
  Op_CLS => RouteIntegerBitfield,
  Op_CLZ => RouteIntegerBitfield,
  Op_CMP => RouteIntegerAlu,
  Op_CMPJcc => RouteControlFlow,
  Op_CMPXCHG => RouteAtomics,
  Op_CPUID => RouteSystemRegisters,
  Op_CTS => RouteIntegerBitfield,
  Op_CTZ => RouteIntegerBitfield,
  Op_DEC => RouteIntegerUnary,
  Op_DECF => RouteIntegerUnary,
  Op_DIVMODS => RouteIntegerMulDiv,
  Op_DIVMODU => RouteIntegerMulDiv,
  Op_DIVS => RouteIntegerMulDiv,
  Op_DIVU => RouteIntegerMulDiv,
  Op_DJcc => RouteControlFlow,
  Op_ERET => RouteCoreControl,
  Op_EXTRACT => RouteIntegerBitfield,
  Op_EXTSL => RouteIntegerUnary,
  Op_EXTSQ => RouteIntegerUnary,
  Op_EXTSW => RouteIntegerUnary,
  Op_EXTZL => RouteIntegerUnary,
  Op_EXTZQ => RouteIntegerUnary,
  Op_EXTZW => RouteIntegerUnary,
  Op_FETCHADD => RouteAtomics,
  Op_FETCHAND => RouteAtomics,
  Op_FETCHOR => RouteAtomics,
  Op_FETCHSUB => RouteAtomics,
  Op_FETCHXOR => RouteAtomics,
  Op_FLSHDCACHE => RouteCache,
  Op_HALT => RouteCoreControl,
  Op_IJcc => RouteControlFlow,
  Op_ILLEGAL => RouteCoreControl,
  Op_INC => RouteIntegerUnary,
  Op_INCF => RouteIntegerUnary,
  Op_INVASID => RouteTlbContext,
  Op_INVDCACHE => RouteCache,
  Op_INVICACHE => RouteCache,
  Op_INVPAGE => RouteTlbContext,
  Op_INVTLB => RouteTlbContext,
  Op_Jcc => RouteControlFlow,
  Op_JMP => RouteControlFlow,
  Op_LCALL => RouteControlFlow,
  Op_LEA => RouteEaUtility,
  Op_LJMP => RouteControlFlow,
  Op_LRET => RouteControlFlow,
  Op_MAXS => RouteIntegerAlu,
  Op_MAXU => RouteIntegerAlu,
  Op_MINS => RouteIntegerAlu,
  Op_MINU => RouteIntegerAlu,
  Op_MODS => RouteIntegerMulDiv,
  Op_MODU => RouteIntegerMulDiv,
  Op_MOV => RouteDataMovement,
  Op_MOVcc => RouteControlFlow,
  Op_MOVCU => RouteDataMovement,
  Op_MOVNT => RouteCache,
  Op_MOVUC => RouteDataMovement,
  Op_MOVUU => RouteDataMovement,
  Op_MUL => RouteIntegerMulDiv,
  Op_MULHS => RouteIntegerMulDiv,
  Op_MULHSU => RouteIntegerMulDiv,
  Op_MULHU => RouteIntegerMulDiv,
  Op_NEG => RouteIntegerUnary,
  Op_NOP => RouteCoreControl,
  Op_NOT => RouteIntegerUnary,
  Op_OR => RouteIntegerAlu,
  Op_PARITY => RouteIntegerBitfield,
  Op_POP => RouteDataMovement,
  Op_POPCNT => RouteIntegerBitfield,
  Op_POPP => RouteDataMovement,
  Op_PREFETCH => RouteCache,
  Op_PREFETCHNT => RouteCache,
  Op_PTQUERY => RouteTlbContext,
  Op_PUSH => RouteDataMovement,
  Op_PUSHP => RouteDataMovement,
  Op_RDCR => RouteSystemRegisters,
  Op_RDFLAGS => RouteSystemRegisters,
  Op_RDPMC => RouteSystemRegisters,
  Op_RDSEG => RouteSystemRegisters,
  Op_RDSTATUS => RouteSystemRegisters,
  Op_REPcc => RouteControlFlow,
  Op_RESET => RouteCoreControl,
  Op_RESTORE => RouteTlbContext,
  Op_RET => RouteControlFlow,
  Op_REVBYTE => RouteIntegerAlu,
  Op_RFENCE => RouteCoreControl,
  Op_ROL => RouteIntegerBitfield,
  Op_ROR => RouteIntegerBitfield,
  Op_SAR => RouteIntegerBitfield,
  Op_SAVE => RouteTlbContext,
  Op_SBB => RouteIntegerAlu,
  Op_SEGLEA => RouteEaUtility,
  Op_SET => RouteControlFlow,
  Op_SETcc => RouteControlFlow,
  Op_SETF => RouteSystemRegisters,
  Op_SHL => RouteIntegerBitfield,
  Op_SHR => RouteIntegerBitfield,
  Op_SUB => RouteIntegerAlu,
  Op_SWPT => RouteTlbContext,
  Op_SWPTA => RouteTlbContext,
  Op_SYNCCACHE => RouteCache,
  Op_SYSCALL => RouteCoreControl,
  Op_TEST => RouteIntegerAlu,
  Op_TESTJcc => RouteControlFlow,
  Op_TRACE => RouteControlFlow,
  Op_VTOP => RouteTlbContext,
  Op_WAIT => RouteCoreControl,
  Op_WFENCE => RouteCoreControl,
  Op_WRBKDCACHE => RouteCache,
  Op_WRCR => RouteSystemRegisters,
  Op_WRFLAGS => RouteSystemRegisters,
  Op_WRSEG => RouteSystemRegisters,
  Op_WRSTATUS => RouteSystemRegisters,
  Op_XCHG => RouteDataMovement,
  Op_XOR => RouteIntegerAlu,
  Op_YIELD => RouteCoreControl,
  Op_FABS => RouteFpu,
  Op_FADD => RouteFpu,
  Op_FBNDII => RouteFpu,
  Op_FBNDIX => RouteFpu,
  Op_FBNDXI => RouteFpu,
  Op_FBNDXX => RouteFpu,
  Op_FCEIL => RouteFpu,
  Op_FCLASS => RouteFpu,
  Op_FCLR => RouteFpu,
  Op_FCMP => RouteFpu,
  Op_FCOPYSIGN => RouteFpu,
  Op_FCVT => RouteFpu,
  Op_FCVTU => RouteFpu,
  Op_FDIV => RouteFpu,
  Op_FFLOOR => RouteFpu,
  Op_FGETEXP => RouteFpu,
  Op_FGETMAN => RouteFpu,
  Op_FINT => RouteFpu,
  Op_FINTRZ => RouteFpu,
  Op_FMADD => RouteFpu,
  Op_FMAX => RouteFpu,
  Op_FMIN => RouteFpu,
  Op_FMOD => RouteFpu,
  Op_FMOV => RouteFpu,
  Op_FMOVcc => RouteFpu,
  Op_FMOVCR => RouteFpu,
  Op_FMSUB => RouteFpu,
  Op_FMUL => RouteFpu,
  Op_FNEG => RouteFpu,
  Op_FNMADD => RouteFpu,
  Op_FNMSUB => RouteFpu,
  Op_FPOPP => RouteFpu,
  Op_FPUSHP => RouteFpu,
  Op_FREM => RouteFpu,
  Op_FROUND => RouteFpu,
  Op_FSCALE => RouteFpu,
  Op_FSQRT => RouteFpu,
  Op_FSUB => RouteFpu,
  Op_FTEST => RouteFpu,
  Op_FTRUNC => RouteFpu,
  Op_FXCHG => RouteFpu,
  Op_RDFFLAGS => RouteSystemRegisters,
  Op_RDFSTATUS => RouteSystemRegisters,
  Op_WRFFLAGS => RouteSystemRegisters,
  Op_WRFSTATUS => RouteSystemRegisters,
  Op_FACOSA => RouteFpuTranscendental,
  Op_FASINA => RouteFpuTranscendental,
  Op_FATANA => RouteFpuTranscendental,
  Op_FATANHA => RouteFpuTranscendental,
  Op_FCOSA => RouteFpuTranscendental,
  Op_FCOSHA => RouteFpuTranscendental,
  Op_FETOXA => RouteFpuTranscendental,
  Op_FETOXM1A => RouteFpuTranscendental,
  Op_FLOG10A => RouteFpuTranscendental,
  Op_FLOG2A => RouteFpuTranscendental,
  Op_FLOGNA => RouteFpuTranscendental,
  Op_FLOGNP1A => RouteFpuTranscendental,
  Op_FSINA => RouteFpuTranscendental,
  Op_FSINCOSA => RouteFpuTranscendental,
  Op_FSINHA => RouteFpuTranscendental,
  Op_FTANA => RouteFpuTranscendental,
  Op_FTANHA => RouteFpuTranscendental,
  Op_FTENTOXA => RouteFpuTranscendental,
  Op_FTWOTOXA => RouteFpuTranscendental,
  Op_VDUP => RouteVector,
  Op_VMOV => RouteVector,
  Op_PHEAD => RouteVector,
  Op_PTAIL => RouteVector,
  Op_PFIRST => RouteVector,
  Op_PLAST => RouteVector,
  Op_PCOUNT => RouteVector,
  Op_PAND => RouteVector,
  Op_POR => RouteVector,
  Op_PXOR => RouteVector,
  Op_PUNPKLO => RouteVector,
  Op_PUNPKHI => RouteVector,
  Op_PPACKLO => RouteVector,
  Op_PPACKHI => RouteVector,
  Op_VCLR => RouteVector,
  Op_VINDEX => RouteVector,
  Op_VLCNT => RouteVector,
  Op_VLCADD => RouteVector,
  Op_VGATHER1 => RouteVector,
  Op_VSCATTER1 => RouteVector,
  Op_PTRUE => RouteVector,
  Op_PFALSE => RouteVector,
  Op_PNOT => RouteVector,
  Op_BPANY => RouteVector,
  Op_BPNONE => RouteVector,
  Op_BPALL => RouteVector,
  Op_VNEG => RouteVector,
  Op_VABS => RouteVector,
  Op_VNOT => RouteVector,
  Op_VCLZ => RouteVector,
  Op_VCTZ => RouteVector,
  Op_VCLS => RouteVector,
  Op_VCTS => RouteVector,
  Op_VPOPCNT => RouteVector,
  Op_VREVBYTE => RouteVector,
  Op_VSQRT => RouteVector,
  Op_VROUND => RouteVector,
  Op_VTRUNC => RouteVector,
  Op_VFLOOR => RouteVector,
  Op_VCEIL => RouteVector,
  Op_VCLASS => RouteVector,
  Op_PPERM => RouteVector,
  Op_PSLIDEUP => RouteVector,
  Op_PSLIDEDN => RouteVector,
  Op_VCMPcc => RouteVector,
  Op_VTESTZ => RouteVector,
  Op_VTESTNZ => RouteVector,
  Op_VADD => RouteVector,
  Op_VSUB => RouteVector,
  Op_VMUL => RouteVector,
  Op_VAND => RouteVector,
  Op_VOR => RouteVector,
  Op_VXOR => RouteVector,
  Op_VMINS => RouteVector,
  Op_VMINU => RouteVector,
  Op_VMAXS => RouteVector,
  Op_VMAXU => RouteVector,
  Op_VMULHS => RouteVector,
  Op_VMULHU => RouteVector,
  Op_VMULHSU => RouteVector,
  Op_VSHL => RouteVector,
  Op_VSHR => RouteVector,
  Op_VSAR => RouteVector,
  Op_VROL => RouteVector,
  Op_VROR => RouteVector,
  Op_VMIN => RouteVector,
  Op_VMAX => RouteVector,
  Op_VDIV => RouteVector,
  Op_VCOPYSIGN => RouteVector,
  Op_VEXTZW => RouteVector,
  Op_VEXTSW => RouteVector,
  Op_VEXTZL => RouteVector,
  Op_VEXTSL => RouteVector,
  Op_VEXTZQ => RouteVector,
  Op_VEXTSQ => RouteVector,
  Op_VTRUNCB => RouteVector,
  Op_VTRUNCW => RouteVector,
  Op_VTRUNCL => RouteVector,
  Op_VCVTS => RouteVector,
  Op_VCVTD => RouteVector,
  Op_VCVTUS => RouteVector,
  Op_VCVTUD => RouteVector,
  Op_VCVTL => RouteVector,
  Op_VCVTUL => RouteVector,
  Op_VCVTQ => RouteVector,
  Op_VCVTUQ => RouteVector,
  Op_VPERM => RouteVector,
  Op_VZIPLO => RouteVector,
  Op_VZIPHI => RouteVector,
  Op_VUZIPLO => RouteVector,
  Op_VUZIPHI => RouteVector,
  Op_VTRNLO => RouteVector,
  Op_VTRNHI => RouteVector,
  Op_VCVTH => RouteVector,
  Op_VCVTUH => RouteVector,
  Op_VMADD => RouteVector,
  Op_VMSUB => RouteVector,
  Op_VNMADD => RouteVector,
  Op_VNMSUB => RouteVector,
  Op_VSLICE => RouteVector,
  Op_VSLIDEUP => RouteVector,
  Op_VSLIDEDN => RouteVector,
  Op_VEXTRACT => RouteVector,
  Op_VINSERT => RouteVector,
  Op_VREDADD => RouteVector,
  Op_VREDMINS => RouteVector,
  Op_VREDMINU => RouteVector,
  Op_VREDMAXS => RouteVector,
  Op_VREDMAXU => RouteVector,
  Op_VREDAND => RouteVector,
  Op_VREDOR => RouteVector,
  Op_VREDXOR => RouteVector,
  Op_VREDMIN => RouteVector,
  Op_VREDMAX => RouteVector,
  Op_PSEL => RouteVector,
  Op_PZIPLO => RouteVector,
  Op_PZIPHI => RouteVector,
  Op_PUZIPLO => RouteVector,
  Op_PUZIPHI => RouteVector,
  Op_PTRNLO => RouteVector,
  Op_PTRNHI => RouteVector,
  Op_PSLICE => RouteVector,
  Op_VMOVZ => RouteVector,
  Op_PLOOP => RouteVector,
  Op_PMOV => RouteVector,
}

function semantic_mnemonic(operation : Semantic_operation) -> string = match operation {
  Op_ABS => "ABS",
  Op_ADC => "ADC",
  Op_ADD => "ADD",
  Op_AFENCE => "AFENCE",
  Op_AND => "AND",
  Op_BCHG => "BCHG",
  Op_BCLR => "BCLR",
  Op_BKPT => "BKPT",
  Op_BNDSII => "BNDSII",
  Op_BNDSIX => "BNDSIX",
  Op_BNDSXI => "BNDSXI",
  Op_BNDSXX => "BNDSXX",
  Op_BNDUII => "BNDUII",
  Op_BNDUIX => "BNDUIX",
  Op_BNDUXI => "BNDUXI",
  Op_BNDUXX => "BNDUXX",
  Op_BSET => "BSET",
  Op_BTEST => "BTEST",
  Op_CALL => "CALL",
  Op_CALLcc => "CALLcc",
  Op_CLMUL => "CLMUL",
  Op_CLMULH => "CLMULH",
  Op_CLR => "CLR",
  Op_CLS => "CLS",
  Op_CLZ => "CLZ",
  Op_CMP => "CMP",
  Op_CMPJcc => "CMPJcc",
  Op_CMPXCHG => "CMPXCHG",
  Op_CPUID => "CPUID",
  Op_CTS => "CTS",
  Op_CTZ => "CTZ",
  Op_DEC => "DEC",
  Op_DECF => "DECF",
  Op_DIVMODS => "DIVMODS",
  Op_DIVMODU => "DIVMODU",
  Op_DIVS => "DIVS",
  Op_DIVU => "DIVU",
  Op_DJcc => "DJcc",
  Op_ERET => "ERET",
  Op_EXTRACT => "EXTRACT",
  Op_EXTSL => "EXTSL",
  Op_EXTSQ => "EXTSQ",
  Op_EXTSW => "EXTSW",
  Op_EXTZL => "EXTZL",
  Op_EXTZQ => "EXTZQ",
  Op_EXTZW => "EXTZW",
  Op_FETCHADD => "FETCHADD",
  Op_FETCHAND => "FETCHAND",
  Op_FETCHOR => "FETCHOR",
  Op_FETCHSUB => "FETCHSUB",
  Op_FETCHXOR => "FETCHXOR",
  Op_FLSHDCACHE => "FLSHDCACHE",
  Op_HALT => "HALT",
  Op_IJcc => "IJcc",
  Op_ILLEGAL => "ILLEGAL",
  Op_INC => "INC",
  Op_INCF => "INCF",
  Op_INVASID => "INVASID",
  Op_INVDCACHE => "INVDCACHE",
  Op_INVICACHE => "INVICACHE",
  Op_INVPAGE => "INVPAGE",
  Op_INVTLB => "INVTLB",
  Op_Jcc => "Jcc",
  Op_JMP => "JMP",
  Op_LCALL => "LCALL",
  Op_LEA => "LEA",
  Op_LJMP => "LJMP",
  Op_LRET => "LRET",
  Op_MAXS => "MAXS",
  Op_MAXU => "MAXU",
  Op_MINS => "MINS",
  Op_MINU => "MINU",
  Op_MODS => "MODS",
  Op_MODU => "MODU",
  Op_MOV => "MOV",
  Op_MOVcc => "MOVcc",
  Op_MOVCU => "MOVCU",
  Op_MOVNT => "MOVNT",
  Op_MOVUC => "MOVUC",
  Op_MOVUU => "MOVUU",
  Op_MUL => "MUL",
  Op_MULHS => "MULHS",
  Op_MULHSU => "MULHSU",
  Op_MULHU => "MULHU",
  Op_NEG => "NEG",
  Op_NOP => "NOP",
  Op_NOT => "NOT",
  Op_OR => "OR",
  Op_PARITY => "PARITY",
  Op_POP => "POP",
  Op_POPCNT => "POPCNT",
  Op_POPP => "POPP",
  Op_PREFETCH => "PREFETCH",
  Op_PREFETCHNT => "PREFETCHNT",
  Op_PTQUERY => "PTQUERY",
  Op_PUSH => "PUSH",
  Op_PUSHP => "PUSHP",
  Op_RDCR => "RDCR",
  Op_RDFLAGS => "RDFLAGS",
  Op_RDPMC => "RDPMC",
  Op_RDSEG => "RDSEG",
  Op_RDSTATUS => "RDSTATUS",
  Op_REPcc => "REPcc",
  Op_RESET => "RESET",
  Op_RESTORE => "RESTORE",
  Op_RET => "RET",
  Op_REVBYTE => "REVBYTE",
  Op_RFENCE => "RFENCE",
  Op_ROL => "ROL",
  Op_ROR => "ROR",
  Op_SAR => "SAR",
  Op_SAVE => "SAVE",
  Op_SBB => "SBB",
  Op_SEGLEA => "SEGLEA",
  Op_SET => "SET",
  Op_SETcc => "SETcc",
  Op_SETF => "SETF",
  Op_SHL => "SHL",
  Op_SHR => "SHR",
  Op_SUB => "SUB",
  Op_SWPT => "SWPT",
  Op_SWPTA => "SWPTA",
  Op_SYNCCACHE => "SYNCCACHE",
  Op_SYSCALL => "SYSCALL",
  Op_TEST => "TEST",
  Op_TESTJcc => "TESTJcc",
  Op_TRACE => "TRACE",
  Op_VTOP => "VTOP",
  Op_WAIT => "WAIT",
  Op_WFENCE => "WFENCE",
  Op_WRBKDCACHE => "WRBKDCACHE",
  Op_WRCR => "WRCR",
  Op_WRFLAGS => "WRFLAGS",
  Op_WRSEG => "WRSEG",
  Op_WRSTATUS => "WRSTATUS",
  Op_XCHG => "XCHG",
  Op_XOR => "XOR",
  Op_YIELD => "YIELD",
  Op_FABS => "FABS",
  Op_FADD => "FADD",
  Op_FBNDII => "FBNDII",
  Op_FBNDIX => "FBNDIX",
  Op_FBNDXI => "FBNDXI",
  Op_FBNDXX => "FBNDXX",
  Op_FCEIL => "FCEIL",
  Op_FCLASS => "FCLASS",
  Op_FCLR => "FCLR",
  Op_FCMP => "FCMP",
  Op_FCOPYSIGN => "FCOPYSIGN",
  Op_FCVT => "FCVT",
  Op_FCVTU => "FCVTU",
  Op_FDIV => "FDIV",
  Op_FFLOOR => "FFLOOR",
  Op_FGETEXP => "FGETEXP",
  Op_FGETMAN => "FGETMAN",
  Op_FINT => "FINT",
  Op_FINTRZ => "FINTRZ",
  Op_FMADD => "FMADD",
  Op_FMAX => "FMAX",
  Op_FMIN => "FMIN",
  Op_FMOD => "FMOD",
  Op_FMOV => "FMOV",
  Op_FMOVcc => "FMOVcc",
  Op_FMOVCR => "FMOVCR",
  Op_FMSUB => "FMSUB",
  Op_FMUL => "FMUL",
  Op_FNEG => "FNEG",
  Op_FNMADD => "FNMADD",
  Op_FNMSUB => "FNMSUB",
  Op_FPOPP => "FPOPP",
  Op_FPUSHP => "FPUSHP",
  Op_FREM => "FREM",
  Op_FROUND => "FROUND",
  Op_FSCALE => "FSCALE",
  Op_FSQRT => "FSQRT",
  Op_FSUB => "FSUB",
  Op_FTEST => "FTEST",
  Op_FTRUNC => "FTRUNC",
  Op_FXCHG => "FXCHG",
  Op_RDFFLAGS => "RDFFLAGS",
  Op_RDFSTATUS => "RDFSTATUS",
  Op_WRFFLAGS => "WRFFLAGS",
  Op_WRFSTATUS => "WRFSTATUS",
  Op_FACOSA => "FACOSA",
  Op_FASINA => "FASINA",
  Op_FATANA => "FATANA",
  Op_FATANHA => "FATANHA",
  Op_FCOSA => "FCOSA",
  Op_FCOSHA => "FCOSHA",
  Op_FETOXA => "FETOXA",
  Op_FETOXM1A => "FETOXM1A",
  Op_FLOG10A => "FLOG10A",
  Op_FLOG2A => "FLOG2A",
  Op_FLOGNA => "FLOGNA",
  Op_FLOGNP1A => "FLOGNP1A",
  Op_FSINA => "FSINA",
  Op_FSINCOSA => "FSINCOSA",
  Op_FSINHA => "FSINHA",
  Op_FTANA => "FTANA",
  Op_FTANHA => "FTANHA",
  Op_FTENTOXA => "FTENTOXA",
  Op_FTWOTOXA => "FTWOTOXA",
  Op_VDUP => "VDUP",
  Op_VMOV => "VMOV",
  Op_PHEAD => "PHEAD",
  Op_PTAIL => "PTAIL",
  Op_PFIRST => "PFIRST",
  Op_PLAST => "PLAST",
  Op_PCOUNT => "PCOUNT",
  Op_PAND => "PAND",
  Op_POR => "POR",
  Op_PXOR => "PXOR",
  Op_PUNPKLO => "PUNPKLO",
  Op_PUNPKHI => "PUNPKHI",
  Op_PPACKLO => "PPACKLO",
  Op_PPACKHI => "PPACKHI",
  Op_VCLR => "VCLR",
  Op_VINDEX => "VINDEX",
  Op_VLCNT => "VLCNT",
  Op_VLCADD => "VLCADD",
  Op_VGATHER1 => "VGATHER1",
  Op_VSCATTER1 => "VSCATTER1",
  Op_PTRUE => "PTRUE",
  Op_PFALSE => "PFALSE",
  Op_PNOT => "PNOT",
  Op_BPANY => "BPANY",
  Op_BPNONE => "BPNONE",
  Op_BPALL => "BPALL",
  Op_VNEG => "VNEG",
  Op_VABS => "VABS",
  Op_VNOT => "VNOT",
  Op_VCLZ => "VCLZ",
  Op_VCTZ => "VCTZ",
  Op_VCLS => "VCLS",
  Op_VCTS => "VCTS",
  Op_VPOPCNT => "VPOPCNT",
  Op_VREVBYTE => "VREVBYTE",
  Op_VSQRT => "VSQRT",
  Op_VROUND => "VROUND",
  Op_VTRUNC => "VTRUNC",
  Op_VFLOOR => "VFLOOR",
  Op_VCEIL => "VCEIL",
  Op_VCLASS => "VCLASS",
  Op_PPERM => "PPERM",
  Op_PSLIDEUP => "PSLIDEUP",
  Op_PSLIDEDN => "PSLIDEDN",
  Op_VCMPcc => "VCMPcc",
  Op_VTESTZ => "VTESTZ",
  Op_VTESTNZ => "VTESTNZ",
  Op_VADD => "VADD",
  Op_VSUB => "VSUB",
  Op_VMUL => "VMUL",
  Op_VAND => "VAND",
  Op_VOR => "VOR",
  Op_VXOR => "VXOR",
  Op_VMINS => "VMINS",
  Op_VMINU => "VMINU",
  Op_VMAXS => "VMAXS",
  Op_VMAXU => "VMAXU",
  Op_VMULHS => "VMULHS",
  Op_VMULHU => "VMULHU",
  Op_VMULHSU => "VMULHSU",
  Op_VSHL => "VSHL",
  Op_VSHR => "VSHR",
  Op_VSAR => "VSAR",
  Op_VROL => "VROL",
  Op_VROR => "VROR",
  Op_VMIN => "VMIN",
  Op_VMAX => "VMAX",
  Op_VDIV => "VDIV",
  Op_VCOPYSIGN => "VCOPYSIGN",
  Op_VEXTZW => "VEXTZW",
  Op_VEXTSW => "VEXTSW",
  Op_VEXTZL => "VEXTZL",
  Op_VEXTSL => "VEXTSL",
  Op_VEXTZQ => "VEXTZQ",
  Op_VEXTSQ => "VEXTSQ",
  Op_VTRUNCB => "VTRUNCB",
  Op_VTRUNCW => "VTRUNCW",
  Op_VTRUNCL => "VTRUNCL",
  Op_VCVTS => "VCVTS",
  Op_VCVTD => "VCVTD",
  Op_VCVTUS => "VCVTUS",
  Op_VCVTUD => "VCVTUD",
  Op_VCVTL => "VCVTL",
  Op_VCVTUL => "VCVTUL",
  Op_VCVTQ => "VCVTQ",
  Op_VCVTUQ => "VCVTUQ",
  Op_VPERM => "VPERM",
  Op_VZIPLO => "VZIPLO",
  Op_VZIPHI => "VZIPHI",
  Op_VUZIPLO => "VUZIPLO",
  Op_VUZIPHI => "VUZIPHI",
  Op_VTRNLO => "VTRNLO",
  Op_VTRNHI => "VTRNHI",
  Op_VCVTH => "VCVTH",
  Op_VCVTUH => "VCVTUH",
  Op_VMADD => "VMADD",
  Op_VMSUB => "VMSUB",
  Op_VNMADD => "VNMADD",
  Op_VNMSUB => "VNMSUB",
  Op_VSLICE => "VSLICE",
  Op_VSLIDEUP => "VSLIDEUP",
  Op_VSLIDEDN => "VSLIDEDN",
  Op_VEXTRACT => "VEXTRACT",
  Op_VINSERT => "VINSERT",
  Op_VREDADD => "VREDADD",
  Op_VREDMINS => "VREDMINS",
  Op_VREDMINU => "VREDMINU",
  Op_VREDMAXS => "VREDMAXS",
  Op_VREDMAXU => "VREDMAXU",
  Op_VREDAND => "VREDAND",
  Op_VREDOR => "VREDOR",
  Op_VREDXOR => "VREDXOR",
  Op_VREDMIN => "VREDMIN",
  Op_VREDMAX => "VREDMAX",
  Op_PSEL => "PSEL",
  Op_PZIPLO => "PZIPLO",
  Op_PZIPHI => "PZIPHI",
  Op_PUZIPLO => "PUZIPLO",
  Op_PUZIPHI => "PUZIPHI",
  Op_PTRNLO => "PTRNLO",
  Op_PTRNHI => "PTRNHI",
  Op_PSLICE => "PSLICE",
  Op_VMOVZ => "VMOVZ",
  Op_PLOOP => "PLOOP",
  Op_PMOV => "PMOV",
}

function all_semantic_operations() -> list(Semantic_operation) = [|
  Op_ABS, Op_ADC, Op_ADD, Op_AFENCE, Op_AND, Op_BCHG, Op_BCLR, Op_BKPT, Op_BNDSII, Op_BNDSIX, Op_BNDSXI, Op_BNDSXX, Op_BNDUII, Op_BNDUIX, Op_BNDUXI, Op_BNDUXX, Op_BSET, Op_BTEST, Op_CALL, Op_CALLcc, Op_CLMUL, Op_CLMULH, Op_CLR, Op_CLS, Op_CLZ, Op_CMP, Op_CMPJcc, Op_CMPXCHG, Op_CPUID, Op_CTS, Op_CTZ, Op_DEC, Op_DECF, Op_DIVMODS, Op_DIVMODU, Op_DIVS, Op_DIVU, Op_DJcc, Op_ERET, Op_EXTRACT, Op_EXTSL, Op_EXTSQ, Op_EXTSW, Op_EXTZL, Op_EXTZQ, Op_EXTZW, Op_FETCHADD, Op_FETCHAND, Op_FETCHOR, Op_FETCHSUB, Op_FETCHXOR, Op_FLSHDCACHE, Op_HALT, Op_IJcc, Op_ILLEGAL, Op_INC, Op_INCF, Op_INVASID, Op_INVDCACHE, Op_INVICACHE, Op_INVPAGE, Op_INVTLB, Op_Jcc, Op_JMP, Op_LCALL, Op_LEA, Op_LJMP, Op_LRET, Op_MAXS, Op_MAXU, Op_MINS, Op_MINU, Op_MODS, Op_MODU, Op_MOV, Op_MOVcc, Op_MOVCU, Op_MOVNT, Op_MOVUC, Op_MOVUU, Op_MUL, Op_MULHS, Op_MULHSU, Op_MULHU, Op_NEG, Op_NOP, Op_NOT, Op_OR, Op_PARITY, Op_POP, Op_POPCNT, Op_POPP, Op_PREFETCH, Op_PREFETCHNT, Op_PTQUERY, Op_PUSH, Op_PUSHP, Op_RDCR, Op_RDFLAGS, Op_RDPMC, Op_RDSEG, Op_RDSTATUS, Op_REPcc, Op_RESET, Op_RESTORE, Op_RET, Op_REVBYTE, Op_RFENCE, Op_ROL, Op_ROR, Op_SAR, Op_SAVE, Op_SBB, Op_SEGLEA, Op_SET, Op_SETcc, Op_SETF, Op_SHL, Op_SHR, Op_SUB, Op_SWPT, Op_SWPTA, Op_SYNCCACHE, Op_SYSCALL, Op_TEST, Op_TESTJcc, Op_TRACE, Op_VTOP, Op_WAIT, Op_WFENCE, Op_WRBKDCACHE, Op_WRCR, Op_WRFLAGS, Op_WRSEG, Op_WRSTATUS, Op_XCHG, Op_XOR, Op_YIELD, Op_FABS, Op_FADD, Op_FBNDII, Op_FBNDIX, Op_FBNDXI, Op_FBNDXX, Op_FCEIL, Op_FCLASS, Op_FCLR, Op_FCMP, Op_FCOPYSIGN, Op_FCVT, Op_FCVTU, Op_FDIV, Op_FFLOOR, Op_FGETEXP, Op_FGETMAN, Op_FINT, Op_FINTRZ, Op_FMADD, Op_FMAX, Op_FMIN, Op_FMOD, Op_FMOV, Op_FMOVcc, Op_FMOVCR, Op_FMSUB, Op_FMUL, Op_FNEG, Op_FNMADD, Op_FNMSUB, Op_FPOPP, Op_FPUSHP, Op_FREM, Op_FROUND, Op_FSCALE, Op_FSQRT, Op_FSUB, Op_FTEST, Op_FTRUNC, Op_FXCHG, Op_RDFFLAGS, Op_RDFSTATUS, Op_WRFFLAGS, Op_WRFSTATUS, Op_FACOSA, Op_FASINA, Op_FATANA, Op_FATANHA, Op_FCOSA, Op_FCOSHA, Op_FETOXA, Op_FETOXM1A, Op_FLOG10A, Op_FLOG2A, Op_FLOGNA, Op_FLOGNP1A, Op_FSINA, Op_FSINCOSA, Op_FSINHA, Op_FTANA, Op_FTANHA, Op_FTENTOXA, Op_FTWOTOXA, Op_VDUP, Op_VMOV, Op_PHEAD, Op_PTAIL, Op_PFIRST, Op_PLAST, Op_PCOUNT, Op_PAND, Op_POR, Op_PXOR, Op_PUNPKLO, Op_PUNPKHI, Op_PPACKLO, Op_PPACKHI, Op_VCLR, Op_VINDEX, Op_VLCNT, Op_VLCADD, Op_VGATHER1, Op_VSCATTER1, Op_PTRUE, Op_PFALSE, Op_PNOT, Op_BPANY, Op_BPNONE, Op_BPALL, Op_VNEG, Op_VABS, Op_VNOT, Op_VCLZ, Op_VCTZ, Op_VCLS, Op_VCTS, Op_VPOPCNT, Op_VREVBYTE, Op_VSQRT, Op_VROUND, Op_VTRUNC, Op_VFLOOR, Op_VCEIL, Op_VCLASS, Op_PPERM, Op_PSLIDEUP, Op_PSLIDEDN, Op_VCMPcc, Op_VTESTZ, Op_VTESTNZ, Op_VADD, Op_VSUB, Op_VMUL, Op_VAND, Op_VOR, Op_VXOR, Op_VMINS, Op_VMINU, Op_VMAXS, Op_VMAXU, Op_VMULHS, Op_VMULHU, Op_VMULHSU, Op_VSHL, Op_VSHR, Op_VSAR, Op_VROL, Op_VROR, Op_VMIN, Op_VMAX, Op_VDIV, Op_VCOPYSIGN, Op_VEXTZW, Op_VEXTSW, Op_VEXTZL, Op_VEXTSL, Op_VEXTZQ, Op_VEXTSQ, Op_VTRUNCB, Op_VTRUNCW, Op_VTRUNCL, Op_VCVTS, Op_VCVTD, Op_VCVTUS, Op_VCVTUD, Op_VCVTL, Op_VCVTUL, Op_VCVTQ, Op_VCVTUQ, Op_VPERM, Op_VZIPLO, Op_VZIPHI, Op_VUZIPLO, Op_VUZIPHI, Op_VTRNLO, Op_VTRNHI, Op_VCVTH, Op_VCVTUH, Op_VMADD, Op_VMSUB, Op_VNMADD, Op_VNMSUB, Op_VSLICE, Op_VSLIDEUP, Op_VSLIDEDN, Op_VEXTRACT, Op_VINSERT, Op_VREDADD, Op_VREDMINS, Op_VREDMINU, Op_VREDMAXS, Op_VREDMAXU, Op_VREDAND, Op_VREDOR, Op_VREDXOR, Op_VREDMIN, Op_VREDMAX, Op_PSEL, Op_PZIPLO, Op_PZIPHI, Op_PUZIPLO, Op_PUZIPHI, Op_PTRNLO, Op_PTRNHI, Op_PSLICE, Op_VMOVZ, Op_PLOOP, Op_PMOV
|]

function architectural_event_class(event : Architectural_event) -> bits(8) = match event {
  Event_DEBUG_TRACE => 0x00,
  Event_BREAKPOINT => 0x00,
  Event_PRIVILEGE_VIOLATION => 0x00,
  Event_SYSTEM_CALL => 0x00,
  Event_DIVIDE_BY_ZERO => 0x00,
  Event_SIGNED_DIVIDE_OVERFLOW => 0x00,
  Event_INVALID_OPCODE => 0x00,
  Event_INVALID_ADDRESSING_FORM => 0x00,
  Event_RESERVED_INSTRUCTION_ENCODING => 0x00,
  Event_UNAVAILABLE_INSTRUCTION_EXTENSION => 0x00,
  Event_EXPLICIT_ILLEGAL_INSTRUCTION => 0x00,
  Event_TRUNCATED_INSTRUCTION => 0x00,
  Event_INVALID_OPERAND_RELATION => 0x00,
  Event_PAGE_NOT_PRESENT => 0x00,
  Event_PAGE_PERMISSION_VIOLATION => 0x00,
  Event_MALFORMED_PAGE_TABLE_ENTRY => 0x00,
  Event_NONCANONICAL_ADDRESS => 0x00,
  Event_SEGMENT_BOUNDS_VIOLATION => 0x00,
  Event_ATOMIC_ALIGNMENT_FAULT => 0x00,
  Event_MEMORY_TYPE_FAULT => 0x00,
  Event_PHYSICAL_ADDRESS_FAULT => 0x00,
  Event_MMIO_ALIGNMENT_FAULT => 0x00,
  Event_UNSUPPORTED_MMIO_OPERATION => 0x00,
  Event_INVALID_CONTROL_SELECTOR => 0x00,
  Event_RESERVED_CONTROL_BITS => 0x00,
  Event_INVALID_CONTROL_IMAGE => 0x00,
  Event_INVALID_CONTROL_TRANSITION => 0x00,
  Event_BUS_NO_RESPONDER => 0x00,
  Event_BUS_ACCESS_DENIED => 0x00,
  Event_BUS_TIMEOUT => 0x00,
  Event_BUS_DATA_ERROR => 0x00,
  Event_BUS_OTHER_ERROR => 0x00,
  Event_EVENT_ENTRY_STATE_FAILURE => 0x00,
  Event_EVENT_STACK_STATE_FAILURE => 0x00,
  Event_EVENT_FRAME_ADDRESS_FAILURE => 0x00,
  Event_EVENT_FRAME_STORE_FAILURE => 0x00,
  Event_MACHINE_CHECK => 0x00,
  Event_INTERRUPT => 0x01,
  Event_NMI => 0x02,
  Event_FLOATING_POINT_EXCEPTION => 0x00,
  Event_VECTOR_LOOP_OFFSET_OUT_OF_RANGE => 0x00,
  Event_VECTOR_LANE_INDEX_OUT_OF_RANGE => 0x00,
}

function architectural_event_selector(event : Architectural_event) -> option(bits(24)) = match event {
  Event_DEBUG_TRACE => Some(0x000000),
  Event_BREAKPOINT => Some(0x000001),
  Event_PRIVILEGE_VIOLATION => Some(0x000002),
  Event_SYSTEM_CALL => Some(0x000003),
  Event_DIVIDE_BY_ZERO => Some(0x000004),
  Event_SIGNED_DIVIDE_OVERFLOW => Some(0x000005),
  Event_INVALID_OPCODE => Some(0x000010),
  Event_INVALID_ADDRESSING_FORM => Some(0x000011),
  Event_RESERVED_INSTRUCTION_ENCODING => Some(0x000012),
  Event_UNAVAILABLE_INSTRUCTION_EXTENSION => Some(0x000013),
  Event_EXPLICIT_ILLEGAL_INSTRUCTION => Some(0x000014),
  Event_TRUNCATED_INSTRUCTION => Some(0x000015),
  Event_INVALID_OPERAND_RELATION => Some(0x000016),
  Event_PAGE_NOT_PRESENT => Some(0x000020),
  Event_PAGE_PERMISSION_VIOLATION => Some(0x000021),
  Event_MALFORMED_PAGE_TABLE_ENTRY => Some(0x000022),
  Event_NONCANONICAL_ADDRESS => Some(0x000023),
  Event_SEGMENT_BOUNDS_VIOLATION => Some(0x000024),
  Event_ATOMIC_ALIGNMENT_FAULT => Some(0x000025),
  Event_MEMORY_TYPE_FAULT => Some(0x000026),
  Event_PHYSICAL_ADDRESS_FAULT => Some(0x000030),
  Event_MMIO_ALIGNMENT_FAULT => Some(0x000031),
  Event_UNSUPPORTED_MMIO_OPERATION => Some(0x000032),
  Event_INVALID_CONTROL_SELECTOR => Some(0x000040),
  Event_RESERVED_CONTROL_BITS => Some(0x000041),
  Event_INVALID_CONTROL_IMAGE => Some(0x000042),
  Event_INVALID_CONTROL_TRANSITION => Some(0x000043),
  Event_BUS_NO_RESPONDER => Some(0x000070),
  Event_BUS_ACCESS_DENIED => Some(0x000071),
  Event_BUS_TIMEOUT => Some(0x000072),
  Event_BUS_DATA_ERROR => Some(0x000073),
  Event_BUS_OTHER_ERROR => Some(0x000074),
  Event_EVENT_ENTRY_STATE_FAILURE => Some(0x000078),
  Event_EVENT_STACK_STATE_FAILURE => Some(0x000079),
  Event_EVENT_FRAME_ADDRESS_FAILURE => Some(0x00007a),
  Event_EVENT_FRAME_STORE_FAILURE => Some(0x00007b),
  Event_MACHINE_CHECK => Some(0x00007c),
  Event_INTERRUPT => None(),
  Event_NMI => None(),
  Event_FLOATING_POINT_EXCEPTION => Some(0x000060),
  Event_VECTOR_LOOP_OFFSET_OUT_OF_RANGE => Some(0x000050),
  Event_VECTOR_LANE_INDEX_OUT_OF_RANGE => Some(0x000051),
}

function architectural_event_frame(event : Architectural_event) -> Event_frame_type = match event {
  Event_DEBUG_TRACE => EventFrameBasic,
  Event_BREAKPOINT => EventFrameBasic,
  Event_PRIVILEGE_VIOLATION => EventFrameBasic,
  Event_SYSTEM_CALL => EventFrameBasic,
  Event_DIVIDE_BY_ZERO => EventFrameBasic,
  Event_SIGNED_DIVIDE_OVERFLOW => EventFrameBasic,
  Event_INVALID_OPCODE => EventFrameBasic,
  Event_INVALID_ADDRESSING_FORM => EventFrameBasic,
  Event_RESERVED_INSTRUCTION_ENCODING => EventFrameBasic,
  Event_UNAVAILABLE_INSTRUCTION_EXTENSION => EventFrameBasic,
  Event_EXPLICIT_ILLEGAL_INSTRUCTION => EventFrameBasic,
  Event_TRUNCATED_INSTRUCTION => EventFrameBasic,
  Event_INVALID_OPERAND_RELATION => EventFrameBasic,
  Event_PAGE_NOT_PRESENT => EventFramePage,
  Event_PAGE_PERMISSION_VIOLATION => EventFramePage,
  Event_MALFORMED_PAGE_TABLE_ENTRY => EventFramePage,
  Event_NONCANONICAL_ADDRESS => EventFramePage,
  Event_SEGMENT_BOUNDS_VIOLATION => EventFramePage,
  Event_ATOMIC_ALIGNMENT_FAULT => EventFramePage,
  Event_MEMORY_TYPE_FAULT => EventFramePage,
  Event_PHYSICAL_ADDRESS_FAULT => EventFramePage,
  Event_MMIO_ALIGNMENT_FAULT => EventFramePage,
  Event_UNSUPPORTED_MMIO_OPERATION => EventFramePage,
  Event_INVALID_CONTROL_SELECTOR => EventFrameBasic,
  Event_RESERVED_CONTROL_BITS => EventFrameBasic,
  Event_INVALID_CONTROL_IMAGE => EventFrameBasic,
  Event_INVALID_CONTROL_TRANSITION => EventFrameBasic,
  Event_BUS_NO_RESPONDER => EventFrameAuxiliary,
  Event_BUS_ACCESS_DENIED => EventFrameAuxiliary,
  Event_BUS_TIMEOUT => EventFrameAuxiliary,
  Event_BUS_DATA_ERROR => EventFrameAuxiliary,
  Event_BUS_OTHER_ERROR => EventFrameAuxiliary,
  Event_EVENT_ENTRY_STATE_FAILURE => EventFrameAuxiliary,
  Event_EVENT_STACK_STATE_FAILURE => EventFrameAuxiliary,
  Event_EVENT_FRAME_ADDRESS_FAILURE => EventFrameAuxiliary,
  Event_EVENT_FRAME_STORE_FAILURE => EventFrameAuxiliary,
  Event_MACHINE_CHECK => EventFrameAuxiliary,
  Event_INTERRUPT => EventFrameBasic,
  Event_NMI => EventFrameBasic,
  Event_FLOATING_POINT_EXCEPTION => EventFrameError,
  Event_VECTOR_LOOP_OFFSET_OUT_OF_RANGE => EventFrameBasic,
  Event_VECTOR_LANE_INDEX_OUT_OF_RANGE => EventFrameBasic,
}

function architectural_event_family(event : Architectural_event) -> Event_family = match event {
  Event_DEBUG_TRACE => EventFamily_DEBUG,
  Event_BREAKPOINT => EventFamily_DEBUG,
  Event_PRIVILEGE_VIOLATION => EventFamily_PRIVILEGE,
  Event_SYSTEM_CALL => EventFamily_CONTROL_TRANSFER,
  Event_DIVIDE_BY_ZERO => EventFamily_INTEGER_DIVIDE,
  Event_SIGNED_DIVIDE_OVERFLOW => EventFamily_INTEGER_DIVIDE,
  Event_INVALID_OPCODE => EventFamily_INSTRUCTION_VALIDATION,
  Event_INVALID_ADDRESSING_FORM => EventFamily_INSTRUCTION_VALIDATION,
  Event_RESERVED_INSTRUCTION_ENCODING => EventFamily_INSTRUCTION_VALIDATION,
  Event_UNAVAILABLE_INSTRUCTION_EXTENSION => EventFamily_INSTRUCTION_VALIDATION,
  Event_EXPLICIT_ILLEGAL_INSTRUCTION => EventFamily_INSTRUCTION_VALIDATION,
  Event_TRUNCATED_INSTRUCTION => EventFamily_INSTRUCTION_VALIDATION,
  Event_INVALID_OPERAND_RELATION => EventFamily_INSTRUCTION_VALIDATION,
  Event_PAGE_NOT_PRESENT => EventFamily_ADDRESS_TRANSLATION,
  Event_PAGE_PERMISSION_VIOLATION => EventFamily_ADDRESS_TRANSLATION,
  Event_MALFORMED_PAGE_TABLE_ENTRY => EventFamily_ADDRESS_TRANSLATION,
  Event_NONCANONICAL_ADDRESS => EventFamily_ADDRESS_TRANSLATION,
  Event_SEGMENT_BOUNDS_VIOLATION => EventFamily_ADDRESS_TRANSLATION,
  Event_ATOMIC_ALIGNMENT_FAULT => EventFamily_ADDRESS_TRANSLATION,
  Event_MEMORY_TYPE_FAULT => EventFamily_ADDRESS_TRANSLATION,
  Event_PHYSICAL_ADDRESS_FAULT => EventFamily_PHYSICAL_ACCESS,
  Event_MMIO_ALIGNMENT_FAULT => EventFamily_PHYSICAL_ACCESS,
  Event_UNSUPPORTED_MMIO_OPERATION => EventFamily_PHYSICAL_ACCESS,
  Event_INVALID_CONTROL_SELECTOR => EventFamily_CONTROL_STATE,
  Event_RESERVED_CONTROL_BITS => EventFamily_CONTROL_STATE,
  Event_INVALID_CONTROL_IMAGE => EventFamily_CONTROL_STATE,
  Event_INVALID_CONTROL_TRANSITION => EventFamily_CONTROL_STATE,
  Event_BUS_NO_RESPONDER => EventFamily_BUS_FAILURE,
  Event_BUS_ACCESS_DENIED => EventFamily_BUS_FAILURE,
  Event_BUS_TIMEOUT => EventFamily_BUS_FAILURE,
  Event_BUS_DATA_ERROR => EventFamily_BUS_FAILURE,
  Event_BUS_OTHER_ERROR => EventFamily_BUS_FAILURE,
  Event_EVENT_ENTRY_STATE_FAILURE => EventFamily_EVENT_DELIVERY_FAILURE,
  Event_EVENT_STACK_STATE_FAILURE => EventFamily_EVENT_DELIVERY_FAILURE,
  Event_EVENT_FRAME_ADDRESS_FAILURE => EventFamily_EVENT_DELIVERY_FAILURE,
  Event_EVENT_FRAME_STORE_FAILURE => EventFamily_EVENT_DELIVERY_FAILURE,
  Event_MACHINE_CHECK => EventFamily_MACHINE_STATE,
  Event_INTERRUPT => EventFamilyNone,
  Event_NMI => EventFamilyNone,
  Event_FLOATING_POINT_EXCEPTION => EventFamily_FLOATING_POINT,
  Event_VECTOR_LOOP_OFFSET_OUT_OF_RANGE => EventFamily_VECTOR_RANGE,
  Event_VECTOR_LANE_INDEX_OUT_OF_RANGE => EventFamily_VECTOR_RANGE,
}

function all_architectural_events() -> list(Architectural_event) = [|
  Event_DEBUG_TRACE, Event_BREAKPOINT, Event_PRIVILEGE_VIOLATION, Event_SYSTEM_CALL, Event_DIVIDE_BY_ZERO, Event_SIGNED_DIVIDE_OVERFLOW, Event_INVALID_OPCODE, Event_INVALID_ADDRESSING_FORM, Event_RESERVED_INSTRUCTION_ENCODING, Event_UNAVAILABLE_INSTRUCTION_EXTENSION, Event_EXPLICIT_ILLEGAL_INSTRUCTION, Event_TRUNCATED_INSTRUCTION, Event_INVALID_OPERAND_RELATION, Event_PAGE_NOT_PRESENT, Event_PAGE_PERMISSION_VIOLATION, Event_MALFORMED_PAGE_TABLE_ENTRY, Event_NONCANONICAL_ADDRESS, Event_SEGMENT_BOUNDS_VIOLATION, Event_ATOMIC_ALIGNMENT_FAULT, Event_MEMORY_TYPE_FAULT, Event_PHYSICAL_ADDRESS_FAULT, Event_MMIO_ALIGNMENT_FAULT, Event_UNSUPPORTED_MMIO_OPERATION, Event_INVALID_CONTROL_SELECTOR, Event_RESERVED_CONTROL_BITS, Event_INVALID_CONTROL_IMAGE, Event_INVALID_CONTROL_TRANSITION, Event_BUS_NO_RESPONDER, Event_BUS_ACCESS_DENIED, Event_BUS_TIMEOUT, Event_BUS_DATA_ERROR, Event_BUS_OTHER_ERROR, Event_EVENT_ENTRY_STATE_FAILURE, Event_EVENT_STACK_STATE_FAILURE, Event_EVENT_FRAME_ADDRESS_FAILURE, Event_EVENT_FRAME_STORE_FAILURE, Event_MACHINE_CHECK, Event_INTERRUPT, Event_NMI, Event_FLOATING_POINT_EXCEPTION, Event_VECTOR_LOOP_OFFSET_OUT_OF_RANGE, Event_VECTOR_LANE_INDEX_OUT_OF_RANGE
|]
