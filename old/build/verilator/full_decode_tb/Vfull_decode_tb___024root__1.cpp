// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vfull_decode_tb.h for the primary calling header

#include "Vfull_decode_tb__pch.h"

void Vfull_decode_tb___024root___act_sequent__TOP__0(Vfull_decode_tb___024root* vlSelf);

void Vfull_decode_tb___024root___eval_act(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_act\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        Vfull_decode_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

void Vfull_decode_tb___024root___nba_sequent__TOP__0(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___nba_sequent__TOP__0\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*2:0*/ full_decode_tb__DOT__update_mode;
    full_decode_tb__DOT__update_mode = 0;
    SData/*15:0*/ full_decode_tb__DOT__dut__DOT__extension_word;
    full_decode_tb__DOT__dut__DOT__extension_word = 0;
    SData/*15:0*/ full_decode_tb__DOT__dut__DOT__token2_word;
    full_decode_tb__DOT__dut__DOT__token2_word = 0;
    SData/*15:0*/ full_decode_tb__DOT__dut__DOT__token3_word;
    full_decode_tb__DOT__dut__DOT__token3_word = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT__prefix_decode_valid;
    full_decode_tb__DOT__dut__DOT__prefix_decode_valid = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT__instruction_decode_valid;
    full_decode_tb__DOT__dut__DOT__instruction_decode_valid = 0;
    CData/*3:0*/ full_decode_tb__DOT__dut__DOT__decode_required_words;
    full_decode_tb__DOT__dut__DOT__decode_required_words = 0;
    CData/*3:0*/ full_decode_tb__DOT__dut__DOT__ea1_descriptor_token;
    full_decode_tb__DOT__dut__DOT__ea1_descriptor_token = 0;
    SData/*15:0*/ full_decode_tb__DOT__dut__DOT__ea1_descriptor_word;
    full_decode_tb__DOT__dut__DOT__ea1_descriptor_word = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT__ea0_payload_words;
    full_decode_tb__DOT__dut__DOT__ea0_payload_words = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT__ea1_payload_words;
    full_decode_tb__DOT__dut__DOT__ea1_payload_words = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__displacement_words_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__displacement_words_o = 0;
    CData/*1:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__scale_log2_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__scale_log2_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__index_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__index_reg_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_reg_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_absolute_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_absolute_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_displacement_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_displacement_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_index_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_index_reg_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_base_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_base_reg_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_valid_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_valid_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_selectable_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_selectable_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__signed32_index_escape_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__signed32_index_escape_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__update_eligible_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__update_eligible_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_immediate_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_immediate_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_memory_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_memory_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_register_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_register_o = 0;
    CData/*5:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__form_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__form_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__needs_descriptor_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__needs_descriptor_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__reserved_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__reserved_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__valid_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__valid_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__displacement_words_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__displacement_words_o = 0;
    CData/*1:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__scale_log2_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__scale_log2_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__index_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__index_reg_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_reg_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_o = 0;
    CData/*2:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_absolute_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_absolute_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_displacement_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_displacement_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_index_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_index_reg_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_base_reg_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_base_reg_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_valid_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_valid_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_selectable_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_selectable_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__signed32_index_escape_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__signed32_index_escape_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__update_eligible_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__update_eligible_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_immediate_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_immediate_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_memory_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_memory_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_register_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_register_o = 0;
    CData/*5:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__form_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__form_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__needs_descriptor_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__needs_descriptor_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__reserved_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__reserved_o = 0;
    CData/*0:0*/ full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__valid_o;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__valid_o = 0;
    QData/*42:0*/ full_decode_tb__DOT__dut__DOT__prefix_decode__DOT__decode;
    full_decode_tb__DOT__dut__DOT__prefix_decode__DOT__decode = 0;
    IData/*26:0*/ full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode;
    full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode = 0;
    IData/*20:0*/ full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode;
    full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode = 0;
    CData/*3:0*/ full_decode_tb__DOT__dut__DOT__decode__DOT__field_format_token_words;
    full_decode_tb__DOT__dut__DOT__decode__DOT__field_format_token_words = 0;
    QData/*39:0*/ full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode;
    full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode = 0;
    QData/*39:0*/ full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode;
    full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode = 0;
    QData/*33:0*/ __Vfunc_bedrock_decode_extract_fields__76__Vfuncout;
    __Vfunc_bedrock_decode_extract_fields__76__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_bedrock_decode_extract_fields__76__field_format_id;
    __Vfunc_bedrock_decode_extract_fields__76__field_format_id = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_extract_fields__76__token0_word;
    __Vfunc_bedrock_decode_extract_fields__76__token0_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_extract_fields__76__token1_word;
    __Vfunc_bedrock_decode_extract_fields__76__token1_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_extract_fields__76__token2_word;
    __Vfunc_bedrock_decode_extract_fields__76__token2_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_extract_fields__76__token3_word;
    __Vfunc_bedrock_decode_extract_fields__76__token3_word = 0;
    QData/*33:0*/ __Vfunc_bedrock_decode_extract_fields__76__r;
    __Vfunc_bedrock_decode_extract_fields__76__r = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__Vfuncout;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__token2_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token2_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea1_descriptor_word__77__r;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__78__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__78__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_prefix_word__78__prefix_word;
    __Vfunc_bedrock_decode_prefix_word__78__prefix_word = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__78____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__78____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__78____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__78____VlefCall_0__bedrock_decode_prefix_byte = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__78__r;
    __Vfunc_bedrock_decode_prefix_word__78__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__79__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__79__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__79__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__79__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__79__r;
    __Vfunc_bedrock_decode_prefix_byte__79__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__80__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__80__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__80__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__80__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__80__r;
    __Vfunc_bedrock_decode_prefix_byte__80__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__81__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__81__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__81__state;
    __Vfunc_bedrock_apply_prefix_byte__81__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__81__prefix;
    __Vfunc_bedrock_apply_prefix_byte__81__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__81__r;
    __Vfunc_bedrock_apply_prefix_byte__81__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__82__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__82__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__82__state;
    __Vfunc_bedrock_apply_prefix_byte__82__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__82__prefix;
    __Vfunc_bedrock_apply_prefix_byte__82__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__82__r;
    __Vfunc_bedrock_apply_prefix_byte__82__r = 0;
    IData/*26:0*/ __Vfunc_bedrock_decode_primary_payload__83__Vfuncout;
    __Vfunc_bedrock_decode_primary_payload__83__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_primary_payload__83__payload;
    __Vfunc_bedrock_decode_primary_payload__83__payload = 0;
    IData/*26:0*/ __Vfunc_bedrock_decode_primary_payload__83__r;
    __Vfunc_bedrock_decode_primary_payload__83__r = 0;
    CData/*5:0*/ __Vfunc_bedrock_decode_ea__86__ea;
    __Vfunc_bedrock_decode_ea__86__ea = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea__86__descriptor;
    __Vfunc_bedrock_decode_ea__86__descriptor = 0;
    CData/*5:0*/ __Vfunc_bedrock_decode_ea__103__ea;
    __Vfunc_bedrock_decode_ea__103__ea = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea__103__descriptor;
    __Vfunc_bedrock_decode_ea__103__descriptor = 0;
    CData/*0:0*/ __VdfgRegularize_hebeb780c_0_0;
    __VdfgRegularize_hebeb780c_0_0 = 0;
    CData/*0:0*/ __VdfgRegularize_hebeb780c_0_1;
    __VdfgRegularize_hebeb780c_0_1 = 0;
    CData/*3:0*/ __VdfgRegularize_hebeb780c_0_3;
    __VdfgRegularize_hebeb780c_0_3 = 0;
    CData/*0:0*/ __VdfgRegularize_hebeb780c_0_4;
    __VdfgRegularize_hebeb780c_0_4 = 0;
    CData/*0:0*/ __VdfgRegularize_hebeb780c_0_5;
    __VdfgRegularize_hebeb780c_0_5 = 0;
    // Body
    __Vfunc_bedrock_decode_prefix_word__78__prefix_word 
        = (0x0000ffffU & (((vlSelfRef.full_decode_tb__DOT__words[0U] 
                            << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                               >> 0x00000010U)) 
                          & (- (IData)((1U & (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                              >> 0x0000000fU))))));
    __Vfunc_bedrock_decode_prefix_word__78__r = 0ULL;
    __Vfunc_bedrock_decode_prefix_word__78__r = (0x0000040000000000ULL 
                                                 | __Vfunc_bedrock_decode_prefix_word__78__r);
    __Vfunc_bedrock_decode_prefix_byte__79__prefix_byte 
        = (0x000000ffU & (IData)(__Vfunc_bedrock_decode_prefix_word__78__prefix_word));
    __Vfunc_bedrock_decode_prefix_byte__79__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__79__r = 
            (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__79__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__79__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r)));
                    __Vfunc_bedrock_decode_prefix_byte__79__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__79__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__79__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__79__r = 
            ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
              ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
              : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
                  : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                      ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                          ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
                          : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                              ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))
                                  : (0x00000d80U | 
                                     (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r))))
                              : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r)) 
                                 | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                      ? 0x1aU : 0x19U) 
                                    << 7U)))) : ((0x007fU 
                                                  & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__r)) 
                                                 | (((4U 
                                                      & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                      ? 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                        ? 0x18U
                                                        : 0x17U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                        ? 0x16U
                                                        : 0x15U))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                        ? 0x14U
                                                        : 0x13U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__79__prefix_byte))
                                                        ? 0x12U
                                                        : 0x11U))) 
                                                    << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__79__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__79__r;
    __Vfunc_bedrock_decode_prefix_word__78____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__79__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__78__r = ((0x000004003fffffffULL 
                                                  & __Vfunc_bedrock_decode_prefix_word__78__r) 
                                                 | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__78____VlefCall_0__bedrock_decode_prefix_byte)) 
                                                    << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__80__prefix_byte 
        = (0x000000ffU & ((IData)(__Vfunc_bedrock_decode_prefix_word__78__prefix_word) 
                          >> 8U));
    __Vfunc_bedrock_decode_prefix_byte__80__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__80__r = 
            (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__80__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__80__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r)));
                    __Vfunc_bedrock_decode_prefix_byte__80__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__80__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__80__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__80__r = 
            ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
              ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
              : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
                  : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                      ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                          ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
                          : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                              ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))
                                  : (0x00000d80U | 
                                     (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r))))
                              : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r)) 
                                 | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                      ? 0x1aU : 0x19U) 
                                    << 7U)))) : ((0x007fU 
                                                  & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__r)) 
                                                 | (((4U 
                                                      & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                      ? 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                        ? 0x18U
                                                        : 0x17U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                        ? 0x16U
                                                        : 0x15U))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                        ? 0x14U
                                                        : 0x13U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__80__prefix_byte))
                                                        ? 0x12U
                                                        : 0x11U))) 
                                                    << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__80__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__80__r;
    __Vfunc_bedrock_decode_prefix_word__78____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__80__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__78__r = ((0x000007ffc003ffffULL 
                                                  & __Vfunc_bedrock_decode_prefix_word__78__r) 
                                                 | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__78____VlefCall_1__bedrock_decode_prefix_byte)) 
                                                    << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__81__prefix = 
        (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__78__r 
                                >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__81__state = __Vfunc_bedrock_decode_prefix_word__78__r;
    __Vfunc_bedrock_apply_prefix_byte__81__r = __Vfunc_bedrock_apply_prefix_byte__81__state;
    __Vfunc_bedrock_apply_prefix_byte__81__r = ((0x000003ffffffffffULL 
                                                 & __Vfunc_bedrock_apply_prefix_byte__81__r) 
                                                | ((QData)((IData)((IData)(
                                                                           ((__Vfunc_bedrock_apply_prefix_byte__81__r 
                                                                             >> 0x0000002aU) 
                                                                            & ((IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix) 
                                                                               >> 0x0000000bU))))) 
                                                   << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__81__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__81__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__81__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__81__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__81__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__81__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__81__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__81__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__81__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__81__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__81__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__81__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__81__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__81__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__81__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__81__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__81__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__81__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__81__r;
    __Vfunc_bedrock_decode_prefix_word__78__r = __Vfunc_bedrock_apply_prefix_byte__81__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__82__prefix = 
        (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__78__r 
                                >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__82__state = __Vfunc_bedrock_decode_prefix_word__78__r;
    __Vfunc_bedrock_apply_prefix_byte__82__r = __Vfunc_bedrock_apply_prefix_byte__82__state;
    __Vfunc_bedrock_apply_prefix_byte__82__r = ((0x000003ffffffffffULL 
                                                 & __Vfunc_bedrock_apply_prefix_byte__82__r) 
                                                | ((QData)((IData)((IData)(
                                                                           ((__Vfunc_bedrock_apply_prefix_byte__82__r 
                                                                             >> 0x0000002aU) 
                                                                            & ((IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix) 
                                                                               >> 0x0000000bU))))) 
                                                   << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__82__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__82__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__82__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__82__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__82__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__82__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__82__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__82__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__82__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__82__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__82__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__82__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__82__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__82__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__82__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__82__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__82__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__82__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__82__r;
    __Vfunc_bedrock_decode_prefix_word__78__r = __Vfunc_bedrock_apply_prefix_byte__82__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__78__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_word__78__r;
    full_decode_tb__DOT__dut__DOT__prefix_decode__DOT__decode 
        = __Vfunc_bedrock_decode_prefix_word__78__Vfuncout;
    full_decode_tb__DOT__dut__DOT__prefix_decode_valid 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__prefix_decode__DOT__decode 
                         >> 0x0000002aU)));
    full_decode_tb__DOT__update_mode = (7U & (IData)(
                                                     (full_decode_tb__DOT__dut__DOT__prefix_decode__DOT__decode 
                                                      >> 0x0000000cU)));
    vlSelfRef.full_decode_tb__DOT__repeat_kind = (3U 
                                                  & (IData)(
                                                            (full_decode_tb__DOT__dut__DOT__prefix_decode__DOT__decode 
                                                             >> 8U)));
    vlSelfRef.full_decode_tb__DOT__repeat_present = 
        ((0U != (IData)(vlSelfRef.full_decode_tb__DOT__repeat_kind)) 
         & (vlSelfRef.full_decode_tb__DOT__words[0U] 
            >> 0x0000000fU));
    __Vfunc_bedrock_decode_primary_payload__83__payload 
        = (0x00000fffU & vlSelfRef.full_decode_tb__DOT__words[0U]);
    __Vfunc_bedrock_decode_primary_payload__83__r = 0U;
    __Vfunc_bedrock_decode_primary_payload__83__r = 
        (0x00000040U | (0x06000001U & __Vfunc_bedrock_decode_primary_payload__83__r));
    if ((0x00000800U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                        if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                            if ((2U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                                if (
                                                    (1U 
                                                     & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                                        = 
                                                        (0x04000000U 
                                                         | __Vfunc_bedrock_decode_primary_payload__83__r);
                                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                                        = 
                                                        (0x00e20000U 
                                                         | (0x060003ffU 
                                                            & __Vfunc_bedrock_decode_primary_payload__83__r));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__83__payload) 
                                      >> 5U)))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__83__payload) 
                                              >> 3U)))) {
                                    if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                            if ((1U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                                    = 
                                                    (0x06000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__83__r);
                                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                                    = 
                                                    (0x00000014U 
                                                     | (0x07ffffc1U 
                                                        & __Vfunc_bedrock_decode_primary_payload__83__r));
                                            } else {
                                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                                    = 
                                                    (0x06000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__83__r);
                                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                                    = 
                                                    (0x00000010U 
                                                     | (0x07ffffc1U 
                                                        & __Vfunc_bedrock_decode_primary_payload__83__r));
                                            }
                                        } else if (
                                                   (1U 
                                                    & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__83__r);
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x00000012U 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__83__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__83__r);
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x0000002cU 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__83__r));
                                        }
                                    } else if ((2U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__83__r);
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x00000028U 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__83__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__83__r);
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x0000002aU 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__83__r));
                                        }
                                    } else if ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__83__r);
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (4U | 
                                               (0x07ffffc1U 
                                                & __Vfunc_bedrock_decode_primary_payload__83__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__83__r);
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (2U | 
                                               (0x07ffffc1U 
                                                & __Vfunc_bedrock_decode_primary_payload__83__r));
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x06000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (6U | (0x07ffffc1U 
                                             & __Vfunc_bedrock_decode_primary_payload__83__r));
                            }
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__83__payload) 
                                                  >> 1U)))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__83__r);
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (8U 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__83__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__83__r);
                                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                                = (0x0000000eU 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__83__r));
                                        }
                                    }
                                } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__83__r);
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x0000000cU 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__83__r);
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x0000000aU 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__83__r);
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x0000001eU 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__83__r);
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x0000001cU 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                                }
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__83__r);
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x0000001aU 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__83__r);
                                        __Vfunc_bedrock_decode_primary_payload__83__r 
                                            = (0x00000018U 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__83__r);
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x00000024U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__83__r);
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x00000026U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                                }
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__83__r);
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x00000022U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__83__r);
                                    __Vfunc_bedrock_decode_primary_payload__83__r 
                                        = (0x00000020U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                                }
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x06000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x00000016U 
                                       | (0x07ffffc1U 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x01820080U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x010e0540U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x002c0c00U | (0x060003ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        }
                    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x002c0400U | (0x060003ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x012e0400U | (0x060003ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        }
                    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x012e0c00U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x013a0400U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                    }
                } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x01a23880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x012a3880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            }
                        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x00f47880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x00f47880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x00f47880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x019e0080U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__83__r);
                                __Vfunc_bedrock_decode_primary_payload__83__r 
                                    = (0x00f61c80U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x00f47880U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x00f47880U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x00f47880U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x019c0080U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                            __Vfunc_bedrock_decode_primary_payload__83__r 
                                = (0x00f61c80U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__83__r));
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x01283000U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                        __Vfunc_bedrock_decode_primary_payload__83__r 
                            = (0x01243000U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__83__r));
                    }
                } else {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x00528400U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
                }
            } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x01a28c00U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
                } else {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x017e8c00U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
                }
            } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x01708c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
            } else {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x012a8c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x010ea000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
        }
    } else if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x010ea000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x00328c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
            } else {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x000a8c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
            }
        } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x00e63000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x003e3000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x00548800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x00548800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
        }
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x00023000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                    __Vfunc_bedrock_decode_primary_payload__83__r 
                        = (0x00e43000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__83__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x004e8800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x004e8800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
        }
    } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x00068c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x00503400U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x003c3000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x000a3880U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__83__r);
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x013a0c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x01140080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
                __Vfunc_bedrock_decode_primary_payload__83__r 
                    = (0x01120080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
            }
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x01320080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x013c0080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x01540000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
            __Vfunc_bedrock_decode_primary_payload__83__r 
                = (0x00260140U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
        }
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__83__payload))) {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x002600c0U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__83__r));
    } else {
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__83__r);
        __Vfunc_bedrock_decode_primary_payload__83__r 
            = (0x00e00000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__83__r));
    }
    __Vfunc_bedrock_decode_primary_payload__83__Vfuncout 
        = __Vfunc_bedrock_decode_primary_payload__83__r;
    full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
        = __Vfunc_bedrock_decode_primary_payload__83__Vfuncout;
    full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode = 0U;
    full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode 
        = (0x0010001fU & full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode);
    full_decode_tb__DOT__dut__DOT__decode__DOT__field_format_token_words = 1U;
    full_decode_tb__DOT__dut__DOT__instruction_decode_valid 
        = (1U & (full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
                 >> 0x0000001aU));
    vlSelfRef.full_decode_tb__DOT__needs_extension 
        = (1U & (full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
                 >> 0x00000019U));
    vlSelfRef.full_decode_tb__DOT__opcode_id = (0x000000ffU 
                                                & (full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
                                                   >> 0x00000011U));
    vlSelfRef.full_decode_tb__DOT__field_format_id 
        = (0x0000007fU & (full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
                          >> 0x0000000aU));
    full_decode_tb__DOT__dut__DOT__decode_required_words 
        = (0x0000000fU & (full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
                          >> 6U));
    if ((0x00008000U & vlSelfRef.full_decode_tb__DOT__words[0U])) {
        full_decode_tb__DOT__dut__DOT__token2_word 
            = (0x0000ffffU & ((vlSelfRef.full_decode_tb__DOT__words[1U] 
                               << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[1U] 
                                                  >> 0x00000010U)));
        full_decode_tb__DOT__dut__DOT__token3_word 
            = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[2U]);
        full_decode_tb__DOT__dut__DOT__extension_word 
            = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[1U]);
    } else {
        full_decode_tb__DOT__dut__DOT__token2_word 
            = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[1U]);
        full_decode_tb__DOT__dut__DOT__token3_word 
            = (0x0000ffffU & ((vlSelfRef.full_decode_tb__DOT__words[1U] 
                               << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[1U] 
                                                  >> 0x00000010U)));
        full_decode_tb__DOT__dut__DOT__extension_word 
            = (0x0000ffffU & ((vlSelfRef.full_decode_tb__DOT__words[0U] 
                               << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                                  >> 0x00000010U)));
    }
    if ((0x02000000U & full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode)) {
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word 
            = full_decode_tb__DOT__dut__DOT__extension_word;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root 
            = (0x0000001fU & (full_decode_tb__DOT__dut__DOT__decode__DOT__primary_decode 
                              >> 1U));
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
            = (4U | (0x00100001U & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root)))) {
                            if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001250a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            }
                            if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                                if ((0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                                    if (VL_UNLIKELY((
                                                     vlSymsp->_vm_contextp__->assertOn()))) {
                                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2657: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2657, "");
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                        if (((((((((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                   | (1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                  | (2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                 | (8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                                | (0x0010U == (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                               | (0x0040U == (0xffc0U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                              | (0x0080U == (0xffc0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                             | (0x00c0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0xbc00U : 
                                       ((1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                         ? 0xba0aU : 
                                        ((2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                          ? 0x8400U
                                          : ((8U == 
                                              (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                              ? 0xdd04U
                                              : ((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                  ? 0xd284U
                                                  : 
                                                 ((0x0040U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                   ? 0xbb85U
                                                   : 
                                                  ((0x0080U 
                                                    == 
                                                    (0xffc0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                    ? 0xdd8fU
                                                    : 0xba85U))))))) 
                                      << 5U));
                        } else if ((0x0100U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001c70a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x0140U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001500a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x0180U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001760a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x01c0U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001bc0a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x0200U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x0019b0a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x0240U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x0019c0a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x0280U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001c40a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (((((0x0280U 
                                                        == 
                                                        (0xffc0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                       << 3U) 
                                                      | ((0x0240U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                         << 2U)) 
                                                     | (((0x0200U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                         << 1U) 
                                                        | (0x01c0U 
                                                           == 
                                                           (0xffc0U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                                    << 0x0000000bU) 
                                                   | (((((0x0180U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0140U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0100U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                           << 1U) 
                                                          | (0x00c0U 
                                                             == 
                                                             (0xffc0U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                                      << 7U)) 
                                                  | ((((((0x0080U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0040U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0010U 
                                                            == 
                                                            (0xfff8U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                           << 1U) 
                                                          | (8U 
                                                             == 
                                                             (0xfff8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                                      << 3U) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                                         << 2U) 
                                                        | (((1U 
                                                             == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                                            << 1U) 
                                                           | (0U 
                                                              == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))))) {
                            if ((0U != (((((((0x0280U 
                                              == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                             << 3U) 
                                            | ((0x0240U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 2U)) 
                                           | (((0x0200U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 1U) 
                                              | (0x01c0U 
                                                 == 
                                                 (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                          << 0x0000000bU) 
                                         | (((((0x0180U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 3U) 
                                              | ((0x0140U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0100U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 1U) 
                                                | (0x00c0U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                            << 7U)) 
                                        | ((((((0x0080U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 3U) 
                                              | ((0x0040U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 1U) 
                                                | (8U 
                                                   == 
                                                   (0xfff8U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                            << 3U) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                               << 2U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                                  << 1U) 
                                                 | (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2576: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2576, "");
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                         >> 0x0000000fU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                      >> 0x0000000eU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                          >> 0x0000000dU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                              >> 0x0000000cU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                  >> 0x0000000bU)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                    >> 0x0000000aU)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                     >> 9U)))) {
                                                if (
                                                    (0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                             >> 7U)))) {
                                                        if (
                                                            (0x00000040U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                                     >> 5U)))) {
                                                                if (
                                                                    (0x00000010U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                                                    if (
                                                                        (8U 
                                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                                            = 
                                                                            (0x001ca080U 
                                                                             | (0x0000001fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                                                    } else if (
                                                                               (1U 
                                                                                & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                                                >> 2U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                                                >> 1U)))) {
                                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                                                = 
                                                                                ((0x0000001fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                                                                | (((1U 
                                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                                 ? 0xe900U
                                                                                 : 0xe300U) 
                                                                                << 5U));
                                                                        }
                                                                    }
                                                                } else {
                                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                                        = 
                                                                        ((0x0000001fU 
                                                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                                                         | (((8U 
                                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                              ? 0xd213U
                                                                              : 0xd184U) 
                                                                            << 5U));
                                                                }
                                                            }
                                                        } else {
                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                                = 
                                                                (0x001a90a0U 
                                                                 | (0x0000001fU 
                                                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                                        }
                                                    }
                                                } else {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                        = 
                                                        ((0x0000001fU 
                                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                                         | (((0x00000080U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                              ? 
                                                             ((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                               ? 0xd885U
                                                               : 0xe591U)
                                                              : 
                                                             ((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                               ? 0xd31cU
                                                               : 
                                                              ((0x00000020U 
                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                ? 
                                                               ((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                  ? 0x8d84U
                                                                  : 
                                                                 ((4U 
                                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                   ? 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                     ? 0xe280U
                                                                     : 0xdf00U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                     ? 0xde80U
                                                                     : 0xd680U))
                                                                   : 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                     ? 0xd400U
                                                                     : 0xc980U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                     ? 0xbc80U
                                                                     : 0x8200U))))
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                  ? 0xe604U
                                                                  : 0xd384U))
                                                                : 
                                                               ((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                  ? 0xe484U
                                                                  : 0xd104U)
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                                  ? 0xe412U
                                                                  : 0xd092U))))) 
                                                            << 5U));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    if ((0x00001000U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                    >> 0x0000000bU)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                = (0x00191560U 
                                                   | (0x0000001fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = ((0x0000001fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                               | (((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc8abU
                                                    : 0xc82bU) 
                                                  << 5U));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = ((0x0000001fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                           | (((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc82bU
                                                    : 0xc7abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc7abU
                                                    : 0xc72bU)) 
                                              << 5U));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = ((0x0000001fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                       | (((0x00002000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc72bU
                                                    : 0xc6abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc6abU
                                                    : 0xc32bU))
                                            : ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc32bU
                                                    : 0xc2abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xc2abU
                                                    : 0x91abU))) 
                                          << 5U));
                            }
                        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00121720U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = ((0x0000001fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0x91abU
                                            : 0x912bU) 
                                          << 5U));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00122560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                 >> 0x0000000aU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                         >> 5U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                             >> 4U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                                 >> 3U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                                     >> 2U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                                            = 
                                                                            (0x00120740U 
                                                                             | (0x0000001fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x8aabU : 0x8a2bU) 
                                      << 5U));
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00180720U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x0018c720U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x4000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))) {
                            if ((0U != (((0x4000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                         << 1U) | (0U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2308: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2308, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0010d720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0010e720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0010f720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00110720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2282: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2282, "");
                            }
                        }
                    }
                } else {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00109720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0010a720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0010b720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0010c720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2256: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2256, "");
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001b65c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001b75c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001b05c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x8000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 2U) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                            if ((0U != (((0x8000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                         << 2U) | (
                                                   ((0x4000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xc000U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2235: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2235, "");
                                }
                            }
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x0019f5c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001a05c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001ae5c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0xc000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001af5c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   ((0xc000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                    << 3U) 
                                                   | ((0x8000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                      << 2U)) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                            if ((0U != ((((0xc000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                          << 3U) | 
                                         ((0x8000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                          << 2U)) | 
                                        (((0x4000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                          << 1U) | 
                                         (0U == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2209: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2209, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001065c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001075c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001115c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001125c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2183: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2183, "");
                            }
                        }
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                      >> 0x0000000dU)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0xdbabU
                                            : 0xdb2bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0xd82bU
                                            : 0xd7abU)) 
                                      << 5U));
                        }
                    }
                } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001ae560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                  >> 8U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001b74c0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = ((0x0000001fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                       | (((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? 0xdb26U
                                                : 0xd826U)
                                            : ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? 0xd7a6U
                                                : 0xd726U)) 
                                          << 5U));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001ab560U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0xd02bU : 0xcfabU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0xcc2bU : 0x8eabU)) 
                                  << 5U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x8e2bU : 0x8c2bU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x8babU : 0x892bU))
                                : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x88abU : 0x83abU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x832bU : 
                                       ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                         ? ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                 ? 0xd5a6U
                                                 : 0xd026U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                 ? 0xcfa6U
                                                 : 0xcb15U))
                                         : ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                 ? 0x8926U
                                                 : 0x88a6U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                 ? 0x83a6U
                                                 : 0x8326U)))))) 
                              << 5U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    if ((0x00000800U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001d1560U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001d1560U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    }
                                } else if ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001bf560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001bf560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else if ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001b8560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001b8560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001b2560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            }
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001ac560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001b8280U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    } else if ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                         >> 5U)))) {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                        = 
                                                        (0x001b9480U 
                                                         | (0x0000001fU 
                                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                                }
                                            }
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001ac4c0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00195560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00195560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00184560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0xc22bU : 0xc1abU) 
                                      << 5U));
                        }
                    } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0xc1abU
                                            : 0xc12bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0xc12bU
                                            : 0xc0abU)) 
                                      << 5U));
                        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00181560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x0012a540U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x0012a540U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00000200U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? ((0x00000100U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0xca15U
                                            : 0xc915U)
                                        : ((0x00000100U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? 0xb995U
                                            : 0xb915U)) 
                                      << 5U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00129520U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x00129520U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else if ((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001282c0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001282c0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00127540U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00127540U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00126520U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00126520U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00119560U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00119560U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00105560U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00000100U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x8f95U : 0x8f15U) 
                                      << 5U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00119280U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00103280U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001264a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001160a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001b93e0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                          >> 3U)))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                = (0x001d16a0U 
                                                   | (0x0000001fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                = (1U 
                                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                        }
                                    }
                                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001bf6a0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x001b86a0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001b26a0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001956a0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x0012b300U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x0012a620U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x00129600U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x00128300U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x00127620U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x00126600U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001196a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00119640U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001056a0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x001055e0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001036a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001035e0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001035e0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x001026a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001025e0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001012a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                     >> 0x0000000fU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                          >> 0x0000000cU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                              >> 0x0000000bU)))) {
                                    if ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                    >> 9U)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                                = (0x0016d680U 
                                                   | (0x0000001fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = ((0x0000001fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                               | (((0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xb534U
                                                    : 0xb4b4U) 
                                                  << 5U));
                                    }
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xb434U
                                                    : 0xb2b4U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xb234U
                                                    : 0xb1b4U))
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xa7b4U
                                                    : 0xa734U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xa6b4U
                                                    : 0xa634U)))
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                            ? ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0xa334U
                                                    : 0xa2b4U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0x9e34U
                                                    : 0x9db4U))
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0x98b4U
                                                    : 0x9834U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                    ? 0x97b4U
                                                    : 0x96b4U)))) 
                                      << 5U));
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                if (((((((((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                           | (0x0200U == (0xffe0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                          | (0x0220U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                         | (0x0280U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                        | (0x0300U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                       | (0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                      | (0x0600U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                     | (0x0680U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00139680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else if ((0x0200U == (0xffe0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0016b340U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else if ((0x0220U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00157360U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x0280U == (0xff80U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0013d200U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else if ((0x0300U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001374e0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x0400U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00155680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else if ((0x0600U == (0xff80U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0013d200U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0013e200U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    }
                } else if ((0x0700U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0013d320U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001395a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x1000U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0016b2e0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x1080U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0013e200U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x1100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0013e320U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001555a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x2000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001555a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                }
                if ((1U & (~ VL_ONEHOT_I((((((((0x2000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 3U) 
                                              | ((0x1800U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 2U)) 
                                             | (((0x1100U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 1U) 
                                                | (0x1080U 
                                                   == 
                                                   (0xff80U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                            << 0x0000000bU) 
                                           | (((((0x1000U 
                                                  == 
                                                  (0xff80U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 3U) 
                                                | ((0x0800U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0700U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 1U) 
                                                  | (0x0680U 
                                                     == 
                                                     (0xff80U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                              << 7U)) 
                                          | ((((((0x0600U 
                                                  == 
                                                  (0xff80U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 3U) 
                                                | ((0x0400U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0300U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 1U) 
                                                  | (0x0280U 
                                                     == 
                                                     (0xff80U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                              << 3U) 
                                             | (((0x0220U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 2U) 
                                                | (((0x0200U 
                                                     == 
                                                     (0xffe0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xfe00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))))) {
                    if ((0U != (((((((0x2000U == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                     << 3U) | ((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 2U)) 
                                   | (((0x1100U == 
                                        (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                       << 1U) | (0x1080U 
                                                 == 
                                                 (0xff80U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                  << 0x0000000bU) | 
                                 (((((0x1000U == (0xff80U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                     << 3U) | ((0x0800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 2U)) 
                                   | (((0x0700U == 
                                        (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                       << 1U) | (0x0680U 
                                                 == 
                                                 (0xff80U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                  << 7U)) | ((((((0x0600U 
                                                  == 
                                                  (0xff80U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 3U) 
                                                | ((0x0400U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0300U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 1U) 
                                                  | (0x0280U 
                                                     == 
                                                     (0xff80U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                              << 3U) 
                                             | (((0x0220U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 2U) 
                                                | (((0x0200U 
                                                     == 
                                                     (0xffe0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xfe00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1434: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1434, "");
                        }
                    }
                }
            } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                                  >> 9U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x0016c680U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x0016c5a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            }
                        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x0016c5a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001675a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001665a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001625a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00167680U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00166680U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? 0xb134U : 0xb0b4U) 
                                  << 5U));
                    }
                } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                           | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                ? 0xb0adU : ((0x00000800U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                              ? 0xb02dU
                                              : 0xad2dU)) 
                              << 5U));
                } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0015a5a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001595a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    }
                } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? 0xb034U : 0xad34U) 
                                  << 5U));
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00159680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00154680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001545a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                }
            } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001535a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x001525a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0014b5a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00153680U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00152680U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                   | (((0x00000200U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0xa5b4U : 0xa534U) 
                                      << 5U));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0014a5a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                           | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                ? 0xa52dU : 0xa4adU) 
                              << 5U));
                }
            } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                           | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                ? 0xa42dU : 0xa3adU) 
                              << 5U));
                } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001475a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                           | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                ? 0xa4b4U : 0xa434U) 
                              << 5U));
                } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x00147680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0013f680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                }
            } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0013f5a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001365a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                }
            } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x001365a0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x00136680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0012e680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                }
            } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x0012c680U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x0016e320U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                 >> 7U)))) {
                if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001380a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                  >> 4U)))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word) 
                                          >> 2U)))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                            = (0x0015f120U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = ((0x0000001fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                                           | (((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                                ? 0xaf09U
                                                : 0xae80U) 
                                              << 5U));
                                }
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x0015c780U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (0x0015c760U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x0015c760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x0015b780U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x0015b760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x0015b760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00158780U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00158760U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001380c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00158760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (0x00151780U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00151760U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (0x00151760U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                               | (((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x9d3cU : 0x9abcU)
                                    : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                        ? 0x9abbU : 0x9a3cU)) 
                                  << 5U));
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                           | (((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? 0x9a3bU : 0x99bcU)
                                : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))
                                    ? 0x99bbU : 0x993cU)) 
                              << 5U));
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x00132760U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0012e660U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0012c660U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x0017d280U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x0200U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001b3280U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    } else if ((0x0400U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001c00a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I((((0x0400U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 2U) 
                                              | (((0x0200U 
                                                   == 
                                                   (0xfe00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                        if ((0U != (((0x0400U == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                     << 2U) | (((0x0200U 
                                                 == 
                                                 (0xfe00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                << 1U) 
                                               | (0U 
                                                  == 
                                                  (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1003: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1003, "");
                            }
                        }
                    }
                } else {
                    if (((((((((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                               | (8U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                              | (0x0010U == (0xfff0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                             | (0x0020U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                            | (0x0030U == (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                           | (0x0040U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                          | (0x0050U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) 
                         | (0x0100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r) 
                               | (((0U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                    ? 0xb784U : ((8U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                  ? 0xda04U
                                                  : 
                                                 ((0x0010U 
                                                   == 
                                                   (0xfff0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                   ? 0xc48bU
                                                   : 
                                                  ((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                    ? 0xc50bU
                                                    : 
                                                   ((0x0030U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                     ? 0xda02U
                                                     : 
                                                    ((0x0040U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                      ? 0xe70bU
                                                      : 
                                                     ((0x0050U 
                                                       == 
                                                       (0xfff0U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))
                                                       ? 0xe78bU
                                                       : 0xc5a0U))))))) 
                                  << 5U));
                    } else if ((0x0200U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                            = (0x001d0400U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((((0x0200U 
                                                   == 
                                                   (0xff00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                  << 4U) 
                                                 | (((0x0100U 
                                                      == 
                                                      (0xff00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                     << 3U) 
                                                    | ((0x0050U 
                                                        == 
                                                        (0xfff0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                       << 2U))) 
                                                | (((0x0040U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                    << 1U) 
                                                   | (0x0030U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                               << 4U) 
                                              | ((((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0010U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                     << 2U)) 
                                                 | (((8U 
                                                      == 
                                                      (0xfff8U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                     << 1U) 
                                                    | (0U 
                                                       == 
                                                       (0xfff8U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))))) {
                        if ((0U != ((((((0x0200U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                        << 4U) | ((
                                                   (0x0100U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0050U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                     << 2U))) 
                                      | (((0x0040U 
                                           == (0xfff0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                          << 1U) | 
                                         (0x0030U == 
                                          (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))) 
                                     << 4U) | ((((0x0020U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 3U) 
                                                | ((0x0010U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 2U)) 
                                               | (((8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:952: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 952, "");
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                if ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x00187560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x00187560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                } else if ((0x1000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001cd560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001cd560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x4000U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x00187580U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r);
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x4000U 
                                             == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                            << 4U) 
                                           | (((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 3U) 
                                              | ((0x1000U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                                 << 2U))) 
                                          | (((0x0800U 
                                               == (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                    if ((0U != ((((0x4000U == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                  << 4U) | (((0x1800U 
                                              == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                             << 3U) 
                                            | ((0x1000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                               << 2U))) 
                                | (((0x0800U == (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                    << 1U) | (0U == 
                                              (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:918: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 918, "");
                        }
                    }
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001130a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0017f000U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x0200U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0017c2c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0017e2c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x0400U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                            << 3U) 
                                           | ((0x0200U 
                                               == (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                              << 2U)) 
                                          | (((0x0040U 
                                               == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))))) {
                    if ((0U != ((((0x0400U == (0xfe00U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                  << 3U) | ((0x0200U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) 
                                            << 2U)) 
                                | (((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                    << 1U) | (0U == 
                                              (0xffc0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:892: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 892, "");
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
                if ((0x07ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001247c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x0800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x08ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x00156700U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x0900U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x097fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0017b3a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x0900U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x097fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0017a6e0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x0980U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001c2000U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if ((0x0980U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001c3100U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x0a00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x0affU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001b56c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x1000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x17ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001887a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x1800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x1fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001887c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x2000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x27ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001887a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                } else if (((0x2800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                            & (0x2fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x001887c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                        = (0x0019a0a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
                }
                if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                    if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:824: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 824, "");
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__ext_root))) {
            if ((0U == (0xfffcU & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x0011a800U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((4U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x001407e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((5U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x001417e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((6U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x001427e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((7U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x001437e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            } else if ((8U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r 
                    = (0x001447e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r));
            }
            if ((1U & (~ VL_ONEHOT_I(((((8U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                        << 5U) | ((
                                                   (7U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                                   << 4U) 
                                                  | ((6U 
                                                      == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                                     << 3U))) 
                                      | (((5U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                          << 2U) | 
                                         (((4U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                           << 1U) | 
                                          (0U == (0xfffcU 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))))) {
                if ((0U != ((((8U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                              << 5U) | (((7U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                         << 4U) | (
                                                   (6U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                                   << 3U))) 
                            | (((5U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                << 2U) | (((4U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)) 
                                           << 1U) | 
                                          (0U == (0xfffcU 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word)))))))) {
                    if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:788: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__extension_word));
                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 788, "");
                    }
                }
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__r;
        full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__84__Vfuncout;
        full_decode_tb__DOT__dut__DOT__instruction_decode_valid 
            = (1U & (full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode 
                     >> 0x00000014U));
        vlSelfRef.full_decode_tb__DOT__opcode_id = 
            (0x000000ffU & (full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode 
                            >> 0x0000000cU));
        vlSelfRef.full_decode_tb__DOT__field_format_id 
            = (0x0000007fU & (full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode 
                              >> 5U));
        full_decode_tb__DOT__dut__DOT__decode_required_words 
            = (0x0000000fU & (full_decode_tb__DOT__dut__DOT__decode__DOT__extended_decode 
                              >> 1U));
    }
    if (full_decode_tb__DOT__dut__DOT__instruction_decode_valid) {
        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id 
            = vlSelfRef.full_decode_tb__DOT__field_format_id;
        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 1U;
        if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id) 
                              >> 4U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id) 
                                  >> 3U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id) 
                                      >> 2U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id) 
                                          >> 1U)))) {
                                if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id)))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 3U;
                                }
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r 
                    = ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                        ? ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                    ? 3U : 2U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                                   ? 2U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                ? 3U : 2U)) : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                                    ? 2U
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                                     ? 3U
                                                     : 2U))
                                                : 3U));
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r 
                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                ? 3U : 2U) : 2U);
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r 
                    = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                        ? 2U : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                 ? 2U : 3U));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id) 
                                 >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 3U;
                }
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                            vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 3U;
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r 
                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                ? 3U : 2U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                               ? 2U
                                               : 3U));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                        ? 2U : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))
                                 ? 3U : 2U));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 3U;
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 3U;
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
                if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id))) {
            if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id)))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r = 2U;
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__r;
        full_decode_tb__DOT__dut__DOT__decode__DOT__field_format_token_words 
            = vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__85__Vfuncout;
        if (((IData)(full_decode_tb__DOT__dut__DOT__decode__DOT__field_format_token_words) 
             > (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words))) {
            full_decode_tb__DOT__dut__DOT__decode_required_words 
                = full_decode_tb__DOT__dut__DOT__decode__DOT__field_format_token_words;
        }
    }
    __Vfunc_bedrock_decode_extract_fields__76__token3_word 
        = full_decode_tb__DOT__dut__DOT__token3_word;
    __Vfunc_bedrock_decode_extract_fields__76__token2_word 
        = full_decode_tb__DOT__dut__DOT__token2_word;
    __Vfunc_bedrock_decode_extract_fields__76__token1_word 
        = full_decode_tb__DOT__dut__DOT__extension_word;
    __Vfunc_bedrock_decode_extract_fields__76__token0_word 
        = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[0U]);
    __Vfunc_bedrock_decode_extract_fields__76__field_format_id 
        = vlSelfRef.full_decode_tb__DOT__field_format_id;
    __Vfunc_bedrock_decode_extract_fields__76__r = 0ULL;
    __Vfunc_bedrock_decode_extract_fields__76__r = 
        (0x0000000040000000ULL | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
    __Vfunc_bedrock_decode_extract_fields__76__r = 
        (0x00000003ffff0000ULL & __Vfunc_bedrock_decode_extract_fields__76__r);
    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id) 
                      >> 5U)))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id)))) {
                                __Vfunc_bedrock_decode_extract_fields__76__r 
                                    = (0x00000000c0000000ULL 
                                       | (0x000000003fffffffULL 
                                          & __Vfunc_bedrock_decode_extract_fields__76__r));
                                __Vfunc_bedrock_decode_extract_fields__76__r 
                                    = (0x0000000010000000ULL 
                                       | __Vfunc_bedrock_decode_extract_fields__76__r);
                                __Vfunc_bedrock_decode_extract_fields__76__r 
                                    = ((0x00000003ffc00000ULL 
                                        & __Vfunc_bedrock_decode_extract_fields__76__r) 
                                       | (IData)((IData)(
                                                         ((0x003f0000U 
                                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                              << 0x0000000dU)) 
                                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                            }
                        }
                    }
                }
            }
        }
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                        if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                            __Vfunc_bedrock_decode_extract_fields__76__r 
                                = (0x00000000c0000000ULL 
                                   | (0x000000003fffffffULL 
                                      & __Vfunc_bedrock_decode_extract_fields__76__r));
                            __Vfunc_bedrock_decode_extract_fields__76__r 
                                = (0x0000000010000000ULL 
                                   | __Vfunc_bedrock_decode_extract_fields__76__r);
                            __Vfunc_bedrock_decode_extract_fields__76__r 
                                = ((0x00000003ffc00000ULL 
                                    & __Vfunc_bedrock_decode_extract_fields__76__r) 
                                   | (IData)((IData)(
                                                     ((0x003f0000U 
                                                       & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                          << 0x0000000dU)) 
                                                      | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                        } else {
                            __Vfunc_bedrock_decode_extract_fields__76__r 
                                = (0x0000000080000000ULL 
                                   | (0x000000003fffffffULL 
                                      & __Vfunc_bedrock_decode_extract_fields__76__r));
                            __Vfunc_bedrock_decode_extract_fields__76__r 
                                = (0x0000000010000000ULL 
                                   | __Vfunc_bedrock_decode_extract_fields__76__r);
                            __Vfunc_bedrock_decode_extract_fields__76__r 
                                = ((0x00000003ffc00000ULL 
                                    & __Vfunc_bedrock_decode_extract_fields__76__r) 
                                   | (IData)((IData)(
                                                     ((0x003f0000U 
                                                       & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                          << 0x00000010U)) 
                                                      | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000080000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                    } else {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x00000000c0000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                    }
                } else if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x00000000c0000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                    } else {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x00000000c0000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                    }
                } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000080000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                    } else {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000080000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                    }
                } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x00000000c0000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000020000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003f03fffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | ((QData)((IData)((0x0000003fU 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                  >> 6U)))) 
                              << 0x00000016U));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x00000000c0000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x00000000c0000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000020000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003f03fffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | ((QData)((IData)((0x0000003fU 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                  >> 6U)))) 
                              << 0x00000016U));
                }
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x00000000c0000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000020000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003f03fffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | ((QData)((IData)((0x0000003fU 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                              >> 6U)))) 
                          << 0x00000016U));
            } else {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x00000000c0000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000020000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003f03fffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | ((QData)((IData)((0x0000003fU 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                              >> 6U)))) 
                          << 0x00000016U));
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x00000000c0000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                    } else {
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000080000000ULL 
                               | (0x000000003fffffffULL 
                                  & __Vfunc_bedrock_decode_extract_fields__76__r));
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = (0x0000000010000000ULL 
                               | __Vfunc_bedrock_decode_extract_fields__76__r);
                        __Vfunc_bedrock_decode_extract_fields__76__r 
                            = ((0x00000003ffc00000ULL 
                                & __Vfunc_bedrock_decode_extract_fields__76__r) 
                               | (IData)((IData)(((0x003f0000U 
                                                   & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                      << 0x00000010U)) 
                                                  | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                    }
                } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000020000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003f03fffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | ((QData)((IData)((0x0000003fU 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  >> 6U)))) 
                              << 0x00000016U));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                }
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000080000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
            } else {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000040000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token0_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word)))));
            }
        } else {
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                   | ((QData)((IData)(((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                        ? ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                            ? 2U : 
                                           ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                             ? 2U : 3U))
                                        : ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                            ? 1U : 
                                           ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                             ? 1U : 3U))))) 
                      << 0x0000001eU));
        }
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        if ((8U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | ((QData)((IData)(((1U 
                                                & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                                ? 3U
                                                : 1U))) 
                              << 0x0000001eU));
                } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x0000000fU)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | ((QData)((IData)(((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                            ? 3U : 2U))) 
                          << 0x0000001eU));
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000080000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
            } else {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x00000000c0000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token3_word)))));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000020000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003f03fffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | ((QData)((IData)((0x0000003fU 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word) 
                                              >> 6U)))) 
                          << 0x00000016U));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                } else {
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000080000000ULL | 
                           (0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r));
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                    __Vfunc_bedrock_decode_extract_fields__76__r 
                        = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                           | (IData)((IData)(((0x003f0000U 
                                               & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                                  << 0x00000010U)) 
                                              | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
                }
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000080000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
            } else {
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000080000000ULL | (0x000000003fffffffULL 
                                                & __Vfunc_bedrock_decode_extract_fields__76__r));
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
                __Vfunc_bedrock_decode_extract_fields__76__r 
                    = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                       | (IData)((IData)(((0x003f0000U 
                                           & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                              << 0x00000010U)) 
                                          | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
            }
        } else {
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                   | ((QData)((IData)(((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                        ? 3U : 2U))) 
                      << 0x0000001eU));
        }
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        __Vfunc_bedrock_decode_extract_fields__76__r 
            = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
               | ((QData)((IData)(((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                    ? ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                        ? ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                            ? 2U : 1U)
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                                  ? 3U
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                                   ? 3U
                                                   : 1U))))) 
                  << 0x0000001eU));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                   | ((QData)((IData)(((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                        ? 1U : 2U))) 
                      << 0x0000001eU));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = (0x0000000080000000ULL | (0x000000003fffffffULL 
                                            & __Vfunc_bedrock_decode_extract_fields__76__r));
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = (0x0000000010000000ULL | __Vfunc_bedrock_decode_extract_fields__76__r);
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = ((0x00000003ffc00000ULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
                   | (IData)((IData)(((0x003f0000U 
                                       & ((IData)(__Vfunc_bedrock_decode_extract_fields__76__token1_word) 
                                          << 0x00000010U)) 
                                      | (IData)(__Vfunc_bedrock_decode_extract_fields__76__token2_word)))));
        } else {
            __Vfunc_bedrock_decode_extract_fields__76__r 
                = (0x0000000080000000ULL | (0x000000003fffffffULL 
                                            & __Vfunc_bedrock_decode_extract_fields__76__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        __Vfunc_bedrock_decode_extract_fields__76__r 
            = ((0x000000003fffffffULL & __Vfunc_bedrock_decode_extract_fields__76__r) 
               | ((QData)((IData)(((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))
                                    ? 1U : 2U))) << 0x0000001eU));
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_extract_fields__76__field_format_id))) {
        __Vfunc_bedrock_decode_extract_fields__76__r 
            = (0x0000000040000000ULL | (0x000000003fffffffULL 
                                        & __Vfunc_bedrock_decode_extract_fields__76__r));
    }
    __Vfunc_bedrock_decode_extract_fields__76__Vfuncout 
        = __Vfunc_bedrock_decode_extract_fields__76__r;
    vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
        = __Vfunc_bedrock_decode_extract_fields__76__Vfuncout;
    vlSelfRef.full_decode_tb__DOT__ea_value[0U] = (0x0000003fU 
                                                   & (IData)(
                                                             (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                              >> 0x00000010U)));
    vlSelfRef.full_decode_tb__DOT__ea_value[1U] = (0x0000003fU 
                                                   & (IData)(
                                                             (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                              >> 0x00000016U)));
    __VdfgRegularize_hebeb780c_0_1 = ((0U != (IData)(full_decode_tb__DOT__update_mode)) 
                                      & (IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                 >> 0x0000001cU)));
    __VdfgRegularize_hebeb780c_0_0 = ((0U != (IData)(full_decode_tb__DOT__update_mode)) 
                                      & (IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                 >> 0x0000001dU)));
    __Vfunc_bedrock_decode_ea__86__descriptor = (0x0000ffffU 
                                                 & (IData)(vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract));
    __Vfunc_bedrock_decode_ea__86__ea = (0x0000003fU 
                                         & (IData)(
                                                   (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                    >> 0x00000010U)));
    {
        vlSelf->__Vfunc_bedrock_decode_ea__86__Vfuncout = 0;
        vlSelf->__Vfunc_bedrock_decode_ea__86__compact = 0;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea 
            = __Vfunc_bedrock_decode_ea__86__ea;
        vlSelf->__Vfunc_bedrock_decode_compact_ea__87__Vfuncout = 0;
        vlSelf->__Vfunc_bedrock_decode_compact_ea__87__r = 0;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r = 0ULL;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
            = (0x0000000001000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000008000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x00000004c0000000ULL 
                                       | (0x000000f001ffffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000000000200000ULL 
                                       | (0x000000ffff00ffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000002000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (1ULL | (0x000000fffffffff8ULL 
                                               & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000008000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000000480000000ULL 
                                       | (0x000000f001ffffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000000000200000ULL 
                                       | (0x000000ffff00ffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (0x0000003000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                    = (1ULL | (0x000000fffffffff8ULL 
                                               & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000448000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000000024ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000408000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000000012ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x00000003c8000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (9ULL | (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000390000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000000000064ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000350000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000000000052ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                }
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x0000000320000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x0000000000300000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x000000ffffffff00ULL 
                                   & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x00000002d0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x0000000000f00000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                                = (0x00000000000000a4ULL 
                                   | (0x000000ffffffff00ULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000290000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000f00000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000000092ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000250000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000f00000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000000000089ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x0000000210000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x00000000000c0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                            = (0x00000000000000a4ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x00000001d0000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x00000000000c0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000000000092ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000190000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x00000000000c0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                        = (0x0000000000000089ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000000150000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000000000000092ULL | (0x000000ffffffff00ULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea)))) 
                          << 0x0000000dU));
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000000110000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000000000000089ULL | (0x000000ffffffff00ULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea)))) 
                          << 0x0000000dU));
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x00000000d4000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea)))) 
                          << 0x0000000dU));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea))) {
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x00000000a0000000ULL | (0x000000f001ffffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r) 
                   | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea)))) 
                      << 0x0000000dU));
        } else {
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x0000000060000000ULL | (0x000000f001ffffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x0000000000260000ULL | (0x000000ffff00ffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r 
                = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r) 
                   | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__ea)))) 
                      << 0x0000000dU));
        }
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__r;
        vlSelfRef.__Vfunc_bedrock_decode_ea__86__compact 
            = vlSelfRef.__Vfunc_bedrock_decode_compact_ea__87__Vfuncout;
        if ((1U & (IData)((vlSelfRef.__Vfunc_bedrock_decode_ea__86__compact 
                           >> 0x00000025U)))) {
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__descriptor 
                = __Vfunc_bedrock_decode_ea__86__descriptor;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape 
                = (1U & (IData)((vlSelfRef.__Vfunc_bedrock_decode_ea__86__compact 
                                 >> 0x00000024U)));
            vlSelf->__Vfunc_bedrock_decode_extended_ea__88__Vfuncout = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__88__r = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__88__mode = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__88__segment = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__88__extra = 0;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r = 0ULL;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                = ((0x000000efffffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                   | ((QData)((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape)) 
                      << 0x00000024U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode 
                = (0x0000001fU & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__descriptor) 
                                  >> 0x0bU));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment 
                = (7U & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__descriptor) 
                         >> 8U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra 
                = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__descriptor));
            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
            vlSelf->__Vfunc_bedrock_ea_segment_decode__89__Vfuncout = 0;
            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__Vfuncout 
                = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                    ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                            ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                                           ? 4U : 3U))
                    : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                            ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__segment))
                                           ? 1U : 0U)));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_0__bedrock_ea_segment_decode 
                = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__89__Vfuncout;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                   | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_0__bedrock_ea_segment_decode)))) 
                      << 0x00000015U));
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000b10000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000890000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000ad0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | (IData)((IData)(
                                                     (0x93U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000850000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | (IData)((IData)(
                                                     (0x93U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000a90000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x00000000000d0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((
                                                   (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                   << 3U))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000810000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x00000000000d0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((
                                                   (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                   << 3U))) 
                                  << 0x00000015U));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000a50000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000000f10000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      (7U 
                                                       | ((0U 
                                                           == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                          << 3U)))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x00000007d0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000000f10000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      (7U 
                                                       | ((0U 
                                                           == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                          << 3U)))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000a10000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x93U 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000790000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x93U 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x00000009d0000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000750000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000712000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000000000065ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__90__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_13__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__90__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_13__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x00000006d2000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000000340000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = (0x0000000000000053ULL 
                                   | (0x000000ffffffff00ULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment 
                                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                            vlSelf->__Vfunc_bedrock_ea_segment_decode__91__Vfuncout = 0;
                            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__Vfuncout 
                                = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                    ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                            ? 6U : 5U)
                                        : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                            ? 4U : 3U))
                                    : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                            ? 2U : 7U)
                                        : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__segment))
                                            ? 1U : 0U)));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_12__bedrock_ea_segment_decode 
                                = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__91__Vfuncout;
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                                   | ((QData)((IData)(
                                                      (8U 
                                                       | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_12__bedrock_ea_segment_decode)))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000692000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x00000000002a0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000000000093ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffff1fffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((7U 
                                                   & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                      >> 5U)))) 
                                  << 0x0000000dU));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__92__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_11__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__92__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_11__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000652000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x00000000002a0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x000000000000008aULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffffff1fffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((7U 
                                                   & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                      >> 5U)))) 
                                  << 0x0000000dU));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__93__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_10__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__93__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_10__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000616000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x00000000002a0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (1ULL | (0x000000ffffffff00ULL 
                                   & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((7U & 
                                               ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                >> 5U)))) 
                              << 0x0000000dU));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__94__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_9__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__94__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_9__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000000992000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffff000000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x002b00a5U 
                                                  | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                     << 8U)))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__95__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_7__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__95__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_7__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = (0x00000005d2000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000ffff000000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | (IData)((IData)((0x002b00a5U 
                                                  | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                     << 8U)))));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__96__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_8__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__96__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_8__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000952000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | (IData)((IData)((0x002b0093U 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__97__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_5__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__97__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_5__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000592000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | (IData)((IData)((0x002b0093U 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__98__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_6__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__98__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_6__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__mode))) {
                if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000912000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | (IData)((IData)((0x002b008aU 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__99__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_3__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__99__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_3__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = (0x0000000552000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | (IData)((IData)((0x002b008aU 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__100__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_4__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__100__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_4__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = (0x00000008d2000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                       | (IData)((IData)((0x002b0001U 
                                          | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                             << 8U)))));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment 
                    = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                vlSelf->__Vfunc_bedrock_ea_segment_decode__101__Vfuncout = 0;
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__Vfuncout 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                                ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                                               ? 4U
                                               : 3U))
                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                                ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__segment))
                                               ? 1U
                                               : 0U)));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_1__bedrock_ea_segment_decode 
                    = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__101__Vfuncout;
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                       | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_1__bedrock_ea_segment_decode)))) 
                          << 0x00000015U));
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r);
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = (0x0000000512000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                       | (IData)((IData)((0x002b0001U 
                                          | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__extra) 
                                             << 8U)))));
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment 
                    = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__segment;
                vlSelf->__Vfunc_bedrock_ea_segment_decode__102__Vfuncout = 0;
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__Vfuncout 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                                ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                                               ? 4U
                                               : 3U))
                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                                ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__segment))
                                               ? 1U
                                               : 0U)));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_2__bedrock_ea_segment_decode 
                    = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__102__Vfuncout;
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                    = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                       | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88____VlefCall_2__bedrock_ea_segment_decode)))) 
                          << 0x00000015U));
            }
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r 
                = ((0x0000007fffffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r) 
                   | ((QData)((IData)((IData)((0x0000008001000000ULL 
                                               == (0x0000008001000000ULL 
                                                   & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r))))) 
                      << 0x00000027U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__Vfuncout 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__r;
            vlSelfRef.__Vfunc_bedrock_decode_ea__86__Vfuncout 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__88__Vfuncout;
            goto __Vlabel0;
        }
        vlSelfRef.__Vfunc_bedrock_decode_ea__86__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_ea__86__compact;
        __Vlabel0: ;
    }
    if ((0x00008000U & vlSelfRef.full_decode_tb__DOT__words[0U])) {
        __Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word 
            = (0x0000ffffU & ((vlSelfRef.full_decode_tb__DOT__words[3U] 
                               << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[3U] 
                                                  >> 0x00000010U)));
        __Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word 
            = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[3U]);
        __Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word 
            = (0x0000ffffU & ((vlSelfRef.full_decode_tb__DOT__words[2U] 
                               << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[2U] 
                                                  >> 0x00000010U)));
    } else {
        __Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word 
            = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[3U]);
        __Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word 
            = (0x0000ffffU & ((vlSelfRef.full_decode_tb__DOT__words[2U] 
                               << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[2U] 
                                                  >> 0x00000010U)));
        __Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word 
            = (0x0000ffffU & vlSelfRef.full_decode_tb__DOT__words[2U]);
    }
    full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
        = vlSelfRef.__Vfunc_bedrock_decode_ea__86__Vfuncout;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__valid_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000027U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__reserved_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000026U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__needs_descriptor_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000025U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__form_o 
        = (0x0000003fU & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                                  >> 0x0000001eU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_register_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x0000001dU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_memory_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x0000001cU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_immediate_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x0000001bU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__update_eligible_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x0000001aU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__signed32_index_escape_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000024U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_selectable_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000019U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_valid_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000018U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_base_reg_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000011U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_index_reg_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000010U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_displacement_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 7U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_absolute_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 6U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000015U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x00000012U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_reg_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x0000000dU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__index_reg_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 0x0000000aU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__scale_log2_o 
        = (3U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 8U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__displacement_words_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode 
                         >> 3U)));
    full_decode_tb__DOT__dut__DOT__ea0_payload_words 
        = (7U & (IData)(full_decode_tb__DOT__dut__DOT__ea0_decode__DOT__decode));
    vlSelfRef.full_decode_tb__DOT__ea_form[0U] = full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__form_o;
    __VdfgRegularize_hebeb780c_0_5 = ((~ (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__reserved_o)) 
                                      & (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__valid_o));
    full_decode_tb__DOT__dut__DOT__ea1_descriptor_token 
        = (0x0000000fU & ((IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                   >> 0x0000001eU)) 
                          + (IData)(full_decode_tb__DOT__dut__DOT__ea0_payload_words)));
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word 
        = (0x0000ffffU & (((vlSelfRef.full_decode_tb__DOT__words[3U] 
                            << 0x00000010U) | (vlSelfRef.full_decode_tb__DOT__words[3U] 
                                               >> 0x00000010U)) 
                          & (- (IData)((1U & (~ (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                                 >> 0x0000000fU)))))));
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word 
        = full_decode_tb__DOT__dut__DOT__token3_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__token2_word 
        = full_decode_tb__DOT__dut__DOT__token2_word;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words 
        = full_decode_tb__DOT__dut__DOT__ea0_payload_words;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id 
        = vlSelfRef.full_decode_tb__DOT__field_format_id;
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__r = 0U;
    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id) 
                  >> 6U)))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id) 
                              >> 3U)))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id) 
                                      >> 1U)))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words)))) {
                                            __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                                = __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word;
                                        }
                                    }
                                } else {
                                    __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                        = ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                                ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word)
                                                : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word))
                                            : ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                                ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word)
                                                : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word)));
                                }
                            }
                        }
                    } else if ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id)))) {
                            if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words) 
                                              >> 1U)))) {
                                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words)))) {
                                        __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                            = __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word;
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                    = ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                        ? ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word))
                                        : ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word)));
                            }
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                        if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))) {
                            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words) 
                                          >> 1U)))) {
                                if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words)))) {
                                    __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                        = __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word;
                                }
                            }
                        } else {
                            __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                = ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                    ? ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                        ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word)
                                        : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word))
                                    : ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                        ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word)
                                        : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word)));
                        }
                    } else if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words)))) {
                                __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                    = __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word;
                            }
                        }
                    } else {
                        __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                            = ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                    ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word)
                                    : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                    ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word)
                                    : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word)));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id)))) {
                            if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words) 
                                              >> 1U)))) {
                                    __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                        = ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word));
                                }
                            } else {
                                __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                    = ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                        ? ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word))
                                        : ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token2_word)));
                            }
                        }
                    }
                }
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id) 
                              >> 2U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__field_format_id)))) {
                            if ((4U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words) 
                                              >> 1U)))) {
                                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words)))) {
                                        __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                            = __Vfunc_bedrock_decode_ea1_descriptor_word__77__token7_word;
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_ea1_descriptor_word__77__r 
                                    = ((2U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                        ? ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token6_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token5_word))
                                        : ((1U & (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__ea0_payload_words))
                                            ? (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token4_word)
                                            : (IData)(__Vfunc_bedrock_decode_ea1_descriptor_word__77__token3_word)));
                            }
                        }
                    }
                }
            }
        }
    }
    __Vfunc_bedrock_decode_ea1_descriptor_word__77__Vfuncout 
        = __Vfunc_bedrock_decode_ea1_descriptor_word__77__r;
    full_decode_tb__DOT__dut__DOT__ea1_descriptor_word 
        = __Vfunc_bedrock_decode_ea1_descriptor_word__77__Vfuncout;
    vlSelfRef.full_decode_tb__DOT__agu_request[0U] 
        = (((QData)((IData)(((((((((((IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                              >> 0x0000001cU)) 
                                     & (IData)(__VdfgRegularize_hebeb780c_0_5)) 
                                    << 3U) | (4U & 
                                              ((IData)(
                                                       (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                        >> 0x0000001cU)) 
                                               << 2U))) 
                                  | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__valid_o) 
                                      << 1U) | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__reserved_o))) 
                                 << 0x0000000bU) | 
                                (((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_register_o) 
                                    << 3U) | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_memory_o) 
                                              << 2U)) 
                                  | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__is_immediate_o) 
                                      << 1U) | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__needs_descriptor_o))) 
                                 << 7U)) | ((((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__signed32_index_escape_o) 
                                                << 3U) 
                                               | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_selectable_o) 
                                                  << 2U)) 
                                              | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_valid_o) 
                                                  << 1U) 
                                                 | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__update_eligible_o))) 
                                             << 3U) 
                                            | (((IData)(__VdfgRegularize_hebeb780c_0_1) 
                                                << 2U) 
                                               | ((2U 
                                                   & (((~ (IData)(__VdfgRegularize_hebeb780c_0_1)) 
                                                       | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__update_eligible_o)) 
                                                      << 1U)) 
                                                  | ((~ (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__update_eligible_o)) 
                                                     & (IData)(__VdfgRegularize_hebeb780c_0_1)))))) 
                              << 0x0000000eU) | (((
                                                   (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_base_reg_o) 
                                                     << 3U) 
                                                    | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_index_reg_o) 
                                                       << 2U)) 
                                                   | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_displacement_o) 
                                                       << 1U) 
                                                      | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__has_absolute_o))) 
                                                  << 0x0000000aU) 
                                                 | ((0x000003f0U 
                                                     & ((IData)(
                                                                (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                                 >> 0x00000010U)) 
                                                        << 4U)) 
                                                    | (0x0000000fU 
                                                       & (IData)(
                                                                 (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                                  >> 0x0000001eU)))))))) 
            << 0x00000021U) | (((QData)((IData)((((
                                                   (0x00000078U 
                                                    & (((IData)(
                                                                (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                                 >> 0x0000001eU)) 
                                                        + 
                                                        (1U 
                                                         & (- (IData)((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__needs_descriptor_o))))) 
                                                       << 3U)) 
                                                   | (IData)(full_decode_tb__DOT__dut__DOT__ea0_payload_words)) 
                                                  << 6U) 
                                                 | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__displacement_words_o) 
                                                     << 3U) 
                                                    | (IData)(full_decode_tb__DOT__update_mode))))) 
                                << 0x00000014U) | (QData)((IData)(
                                                                  ((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__form_o) 
                                                                     << 0x0000000eU) 
                                                                    | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__segment_o) 
                                                                       << 0x0000000bU)) 
                                                                   | ((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_o) 
                                                                        << 8U) 
                                                                       | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__base_reg_o) 
                                                                          << 5U)) 
                                                                      | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__index_reg_o) 
                                                                          << 2U) 
                                                                         | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea0_decode__scale_log2_o))))))));
    __Vfunc_bedrock_decode_ea__103__descriptor = full_decode_tb__DOT__dut__DOT__ea1_descriptor_word;
    __Vfunc_bedrock_decode_ea__103__ea = (0x0000003fU 
                                          & (IData)(
                                                    (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                     >> 0x00000016U)));
    {
        vlSelf->__Vfunc_bedrock_decode_ea__103__Vfuncout = 0;
        vlSelf->__Vfunc_bedrock_decode_ea__103__compact = 0;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea 
            = __Vfunc_bedrock_decode_ea__103__ea;
        vlSelf->__Vfunc_bedrock_decode_compact_ea__104__Vfuncout = 0;
        vlSelf->__Vfunc_bedrock_decode_compact_ea__104__r = 0;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r = 0ULL;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
            = (0x0000000001000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000008000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x00000004c0000000ULL 
                                       | (0x000000f001ffffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000000000200000ULL 
                                       | (0x000000ffff00ffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000002000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (1ULL | (0x000000fffffffff8ULL 
                                               & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000008000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000000480000000ULL 
                                       | (0x000000f001ffffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000000000200000ULL 
                                       | (0x000000ffff00ffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (0x0000003000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                    = (1ULL | (0x000000fffffffff8ULL 
                                               & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000448000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000000024ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000408000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000000012ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x00000003c8000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (9ULL | (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000390000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000000000064ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000350000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000000000052ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                }
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x0000000320000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x0000000000300000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x000000ffffffff00ULL 
                                   & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x00000002d0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x0000000000f00000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                                = (0x00000000000000a4ULL 
                                   | (0x000000ffffffff00ULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000290000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000f00000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000000092ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000250000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000f00000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000000000089ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x0000000210000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x00000000000c0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                            = (0x00000000000000a4ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x00000001d0000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x00000000000c0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000000000092ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000190000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x00000000000c0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                        = (0x0000000000000089ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000000150000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000000000000092ULL | (0x000000ffffffff00ULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea)))) 
                          << 0x0000000dU));
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000000110000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000000000000089ULL | (0x000000ffffffff00ULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea)))) 
                          << 0x0000000dU));
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x00000000d4000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea)))) 
                          << 0x0000000dU));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea))) {
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x00000000a0000000ULL | (0x000000f001ffffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r) 
                   | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea)))) 
                      << 0x0000000dU));
        } else {
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x0000000060000000ULL | (0x000000f001ffffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x0000000000260000ULL | (0x000000ffff00ffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r 
                = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r) 
                   | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__ea)))) 
                      << 0x0000000dU));
        }
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__r;
        vlSelfRef.__Vfunc_bedrock_decode_ea__103__compact 
            = vlSelfRef.__Vfunc_bedrock_decode_compact_ea__104__Vfuncout;
        if ((1U & (IData)((vlSelfRef.__Vfunc_bedrock_decode_ea__103__compact 
                           >> 0x00000025U)))) {
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__descriptor 
                = __Vfunc_bedrock_decode_ea__103__descriptor;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape 
                = (1U & (IData)((vlSelfRef.__Vfunc_bedrock_decode_ea__103__compact 
                                 >> 0x00000024U)));
            vlSelf->__Vfunc_bedrock_decode_extended_ea__105__Vfuncout = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__105__r = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__105__mode = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__105__segment = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__105__extra = 0;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r = 0ULL;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                = ((0x000000efffffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                   | ((QData)((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape)) 
                      << 0x00000024U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode 
                = (0x0000001fU & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__descriptor) 
                                  >> 0x0bU));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment 
                = (7U & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__descriptor) 
                         >> 8U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra 
                = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__descriptor));
            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
            vlSelf->__Vfunc_bedrock_ea_segment_decode__106__Vfuncout = 0;
            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__Vfuncout 
                = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                    ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                            ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                                           ? 4U : 3U))
                    : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                            ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__segment))
                                           ? 1U : 0U)));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_0__bedrock_ea_segment_decode 
                = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__106__Vfuncout;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                   | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_0__bedrock_ea_segment_decode)))) 
                      << 0x00000015U));
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000b10000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000890000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000ad0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | (IData)((IData)(
                                                     (0x93U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000850000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | (IData)((IData)(
                                                     (0x93U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000a90000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x00000000000d0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((
                                                   (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                   << 3U))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000810000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x00000000000d0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((
                                                   (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                   << 3U))) 
                                  << 0x00000015U));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000a50000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000000f10000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      (7U 
                                                       | ((0U 
                                                           == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                          << 3U)))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x00000007d0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000000f10000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      (7U 
                                                       | ((0U 
                                                           == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                          << 3U)))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000a10000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x93U 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000790000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x93U 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x00000009d0000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000750000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000712000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000000000065ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__107__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_13__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__107__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_13__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x00000006d2000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000000340000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = (0x0000000000000053ULL 
                                   | (0x000000ffffffff00ULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment 
                                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                            vlSelf->__Vfunc_bedrock_ea_segment_decode__108__Vfuncout = 0;
                            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__Vfuncout 
                                = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                    ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                            ? 6U : 5U)
                                        : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                            ? 4U : 3U))
                                    : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                            ? 2U : 7U)
                                        : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__segment))
                                            ? 1U : 0U)));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_12__bedrock_ea_segment_decode 
                                = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__108__Vfuncout;
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                                   | ((QData)((IData)(
                                                      (8U 
                                                       | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_12__bedrock_ea_segment_decode)))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000692000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x00000000002a0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000000000093ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffff1fffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((7U 
                                                   & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                      >> 5U)))) 
                                  << 0x0000000dU));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__109__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_11__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__109__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_11__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000652000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x00000000002a0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x000000000000008aULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffffff1fffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((7U 
                                                   & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                      >> 5U)))) 
                                  << 0x0000000dU));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__110__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_10__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__110__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_10__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000616000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x00000000002a0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (1ULL | (0x000000ffffffff00ULL 
                                   & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((7U & 
                                               ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                >> 5U)))) 
                              << 0x0000000dU));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__111__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_9__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__111__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_9__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000000992000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffff000000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x002b00a5U 
                                                  | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                     << 8U)))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__112__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_7__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__112__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_7__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = (0x00000005d2000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000ffff000000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | (IData)((IData)((0x002b00a5U 
                                                  | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                     << 8U)))));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__113__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_8__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__113__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_8__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000952000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | (IData)((IData)((0x002b0093U 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__114__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_5__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__114__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_5__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000592000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | (IData)((IData)((0x002b0093U 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__115__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_6__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__115__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_6__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__mode))) {
                if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000912000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | (IData)((IData)((0x002b008aU 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__116__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_3__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__116__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_3__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = (0x0000000552000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | (IData)((IData)((0x002b008aU 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__117__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_4__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__117__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_4__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = (0x00000008d2000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                       | (IData)((IData)((0x002b0001U 
                                          | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                             << 8U)))));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment 
                    = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                vlSelf->__Vfunc_bedrock_ea_segment_decode__118__Vfuncout = 0;
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__Vfuncout 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                                ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                                               ? 4U
                                               : 3U))
                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                                ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__segment))
                                               ? 1U
                                               : 0U)));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_1__bedrock_ea_segment_decode 
                    = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__118__Vfuncout;
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                       | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_1__bedrock_ea_segment_decode)))) 
                          << 0x00000015U));
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r);
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = (0x0000000512000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                       | (IData)((IData)((0x002b0001U 
                                          | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__extra) 
                                             << 8U)))));
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment 
                    = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__segment;
                vlSelf->__Vfunc_bedrock_ea_segment_decode__119__Vfuncout = 0;
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__Vfuncout 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                                ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                                               ? 4U
                                               : 3U))
                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                                ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__segment))
                                               ? 1U
                                               : 0U)));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_2__bedrock_ea_segment_decode 
                    = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__119__Vfuncout;
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                    = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                       | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105____VlefCall_2__bedrock_ea_segment_decode)))) 
                          << 0x00000015U));
            }
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r 
                = ((0x0000007fffffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r) 
                   | ((QData)((IData)((IData)((0x0000008001000000ULL 
                                               == (0x0000008001000000ULL 
                                                   & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r))))) 
                      << 0x00000027U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__Vfuncout 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__r;
            vlSelfRef.__Vfunc_bedrock_decode_ea__103__Vfuncout 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__105__Vfuncout;
            goto __Vlabel1;
        }
        vlSelfRef.__Vfunc_bedrock_decode_ea__103__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_ea__103__compact;
        __Vlabel1: ;
    }
    full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
        = vlSelfRef.__Vfunc_bedrock_decode_ea__103__Vfuncout;
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__valid_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000027U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__reserved_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000026U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__needs_descriptor_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000025U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__form_o 
        = (0x0000003fU & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                                  >> 0x0000001eU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_register_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x0000001dU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_memory_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x0000001cU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_immediate_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x0000001bU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__update_eligible_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x0000001aU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__signed32_index_escape_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000024U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_selectable_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000019U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_valid_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000018U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_base_reg_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000011U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_index_reg_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000010U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_displacement_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 7U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_absolute_o 
        = (1U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 6U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000015U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x00000012U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_reg_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x0000000dU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__index_reg_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 0x0000000aU)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__scale_log2_o 
        = (3U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 8U)));
    full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__displacement_words_o 
        = (7U & (IData)((full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode 
                         >> 3U)));
    full_decode_tb__DOT__dut__DOT__ea1_payload_words 
        = (7U & (IData)(full_decode_tb__DOT__dut__DOT__ea1_decode__DOT__decode));
    vlSelfRef.full_decode_tb__DOT__ea_form[1U] = full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__form_o;
    __VdfgRegularize_hebeb780c_0_3 = (0x0000000fU & 
                                      ((IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                >> 0x0000001eU)) 
                                       + (((- (IData)(
                                                      (1U 
                                                       & (IData)(
                                                                 (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                                  >> 0x0000001dU))))) 
                                           & (IData)(full_decode_tb__DOT__dut__DOT__ea1_payload_words)) 
                                          + ((- (IData)(
                                                        (1U 
                                                         & (IData)(
                                                                   (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                                    >> 0x0000001cU))))) 
                                             & (IData)(full_decode_tb__DOT__dut__DOT__ea0_payload_words)))));
    __VdfgRegularize_hebeb780c_0_4 = ((~ (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__reserved_o)) 
                                      & (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__valid_o));
    vlSelfRef.full_decode_tb__DOT__undersized = ((0x0000000fU 
                                                  & ((IData)(1U) 
                                                     + 
                                                     (7U 
                                                      & (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                                         >> 0x0000000cU)))) 
                                                 < 
                                                 (0x0000000fU 
                                                  & ((((IData)(__VdfgRegularize_hebeb780c_0_3) 
                                                       > (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words))
                                                       ? (IData)(__VdfgRegularize_hebeb780c_0_3)
                                                       : (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words)) 
                                                     + 
                                                     (1U 
                                                      & (- (IData)(
                                                                   (1U 
                                                                    & (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                                                       >> 0x0000000fU))))))));
    vlSelfRef.full_decode_tb__DOT__dut__DOT__total_required_words 
        = (0x0000000fU & ((((IData)(__VdfgRegularize_hebeb780c_0_3) 
                            > (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words))
                            ? (IData)(__VdfgRegularize_hebeb780c_0_3)
                            : (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words)) 
                          + (1U & (- (IData)((1U & 
                                              (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                               >> 0x0000000fU)))))));
    vlSelfRef.full_decode_tb__DOT__dut__DOT__base_valid 
        = (((~ (vlSelfRef.full_decode_tb__DOT__words[0U] 
                >> 0x0000000fU)) | (IData)(full_decode_tb__DOT__dut__DOT__prefix_decode_valid)) 
           & ((IData)(full_decode_tb__DOT__dut__DOT__instruction_decode_valid) 
              & (((0x0000000fU & ((IData)(1U) + (7U 
                                                 & (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                                    >> 0x0000000cU)))) 
                  >= (0x0000000fU & ((((IData)(__VdfgRegularize_hebeb780c_0_3) 
                                       > (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words))
                                       ? (IData)(__VdfgRegularize_hebeb780c_0_3)
                                       : (IData)(full_decode_tb__DOT__dut__DOT__decode_required_words)) 
                                     + (1U & (- (IData)(
                                                        (1U 
                                                         & (vlSelfRef.full_decode_tb__DOT__words[0U] 
                                                            >> 0x0000000fU)))))))) 
                 & (((~ (IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                 >> 0x0000001cU))) 
                     | (IData)(__VdfgRegularize_hebeb780c_0_5)) 
                    & ((~ (IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                   >> 0x0000001dU))) 
                       | (IData)(__VdfgRegularize_hebeb780c_0_4))))));
    vlSelfRef.full_decode_tb__DOT__agu_request[1U] 
        = (((QData)((IData)(((((((((((IData)((vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                              >> 0x0000001dU)) 
                                     & (IData)(__VdfgRegularize_hebeb780c_0_4)) 
                                    << 3U) | (4U & 
                                              ((IData)(
                                                       (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                        >> 0x0000001dU)) 
                                               << 2U))) 
                                  | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__valid_o) 
                                      << 1U) | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__reserved_o))) 
                                 << 0x0000000bU) | 
                                (((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_register_o) 
                                    << 3U) | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_memory_o) 
                                              << 2U)) 
                                  | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__is_immediate_o) 
                                      << 1U) | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__needs_descriptor_o))) 
                                 << 7U)) | ((((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__signed32_index_escape_o) 
                                                << 3U) 
                                               | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_selectable_o) 
                                                  << 2U)) 
                                              | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_valid_o) 
                                                  << 1U) 
                                                 | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__update_eligible_o))) 
                                             << 3U) 
                                            | (((IData)(__VdfgRegularize_hebeb780c_0_0) 
                                                << 2U) 
                                               | ((2U 
                                                   & (((~ (IData)(__VdfgRegularize_hebeb780c_0_0)) 
                                                       | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__update_eligible_o)) 
                                                      << 1U)) 
                                                  | ((~ (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__update_eligible_o)) 
                                                     & (IData)(__VdfgRegularize_hebeb780c_0_0)))))) 
                              << 0x0000000eU) | (((
                                                   (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_base_reg_o) 
                                                     << 3U) 
                                                    | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_index_reg_o) 
                                                       << 2U)) 
                                                   | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_displacement_o) 
                                                       << 1U) 
                                                      | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__has_absolute_o))) 
                                                  << 0x0000000aU) 
                                                 | ((0x000003f0U 
                                                     & ((IData)(
                                                                (vlSelfRef.full_decode_tb__DOT__dut__DOT__field_extract 
                                                                 >> 0x00000016U)) 
                                                        << 4U)) 
                                                    | (IData)(full_decode_tb__DOT__dut__DOT__ea1_descriptor_token)))))) 
            << 0x00000021U) | (((QData)((IData)((((
                                                   (0x00000078U 
                                                    & (((1U 
                                                         & (- (IData)((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__needs_descriptor_o)))) 
                                                        + (IData)(full_decode_tb__DOT__dut__DOT__ea1_descriptor_token)) 
                                                       << 3U)) 
                                                   | (IData)(full_decode_tb__DOT__dut__DOT__ea1_payload_words)) 
                                                  << 6U) 
                                                 | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__displacement_words_o) 
                                                     << 3U) 
                                                    | (IData)(full_decode_tb__DOT__update_mode))))) 
                                << 0x00000014U) | (QData)((IData)(
                                                                  ((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__form_o) 
                                                                     << 0x0000000eU) 
                                                                    | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__segment_o) 
                                                                       << 0x0000000bU)) 
                                                                   | ((((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_o) 
                                                                        << 8U) 
                                                                       | ((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__base_reg_o) 
                                                                          << 5U)) 
                                                                      | (((IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__index_reg_o) 
                                                                          << 2U) 
                                                                         | (IData)(full_decode_tb__DOT__dut__DOT____Vcellout__ea1_decode__scale_log2_o))))))));
}

void Vfull_decode_tb___024root___eval_nba(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_nba\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vfull_decode_tb___024root___nba_sequent__TOP__0(vlSelf);
    }
}

void Vfull_decode_tb___024root___timing_resume(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___timing_resume\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Vfull_decode_tb___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

void Vfull_decode_tb___024root___eval_triggers_vec__act(Vfull_decode_tb___024root* vlSelf);
#ifdef VL_DEBUG
VL_ATTR_COLD void Vfull_decode_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
bool Vfull_decode_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

bool Vfull_decode_tb___024root___eval_phase__act(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_phase__act\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    Vfull_decode_tb___024root___eval_triggers_vec__act(vlSelf);
    Vfull_decode_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vfull_decode_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vfull_decode_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vfull_decode_tb___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Vfull_decode_tb___024root___timing_resume(vlSelf);
        Vfull_decode_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vfull_decode_tb___024root___eval_phase__inact(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_phase__inact\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("tb/full_decode_tb.sv", 4, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vfull_decode_tb___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vfull_decode_tb___024root___eval_phase__nba(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_phase__nba\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vfull_decode_tb___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vfull_decode_tb___024root___eval_nba(vlSelf);
        Vfull_decode_tb___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vfull_decode_tb___024root___eval(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vfull_decode_tb___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("tb/full_decode_tb.sv", 4, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("tb/full_decode_tb.sv", 4, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vfull_decode_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("tb/full_decode_tb.sv", 4, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vfull_decode_tb___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vfull_decode_tb___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vfull_decode_tb___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vfull_decode_tb___024root___eval_debug_assertions(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_debug_assertions\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
