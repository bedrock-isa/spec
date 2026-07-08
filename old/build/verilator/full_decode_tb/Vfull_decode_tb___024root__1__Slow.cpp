// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vfull_decode_tb.h for the primary calling header

#include "Vfull_decode_tb__pch.h"

VL_ATTR_COLD void Vfull_decode_tb___024root___stl_sequent__TOP__0(Vfull_decode_tb___024root* vlSelf);

VL_ATTR_COLD void Vfull_decode_tb___024root___eval_stl(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_stl\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vfull_decode_tb___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vfull_decode_tb___024root___eval_triggers_vec__stl(Vfull_decode_tb___024root* vlSelf);
#ifdef VL_DEBUG
VL_ATTR_COLD void Vfull_decode_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vfull_decode_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

VL_ATTR_COLD bool Vfull_decode_tb___024root___eval_phase__stl(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___eval_phase__stl\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vfull_decode_tb___024root___eval_triggers_vec__stl(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vfull_decode_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vfull_decode_tb___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vfull_decode_tb___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vfull_decode_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vfull_decode_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vfull_decode_tb___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vfull_decode_tb___024root___ctor_var_reset(Vfull_decode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfull_decode_tb___024root___ctor_var_reset\n"); );
    Vfull_decode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->full_decode_tb__DOT__words, __VscopeHash, 3401435525933534156ull);
    vlSelf->full_decode_tb__DOT__undersized = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16467424285262756458ull);
    vlSelf->full_decode_tb__DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12081421354846880622ull);
    vlSelf->full_decode_tb__DOT__field_format_id = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11996878751201639730ull);
    vlSelf->full_decode_tb__DOT__needs_extension = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17341388922297686718ull);
    vlSelf->full_decode_tb__DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8912489166937583518ull);
    vlSelf->full_decode_tb__DOT__repcc_allowed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15646539329875636572ull);
    vlSelf->full_decode_tb__DOT__repg_allowed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7242471194245235611ull);
    vlSelf->full_decode_tb__DOT__repeat_present = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5773033190364605424ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->full_decode_tb__DOT__ea_value[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 9850246287179221933ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->full_decode_tb__DOT__ea_form[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6775519586031723085ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->full_decode_tb__DOT__agu_request[__Vi0] = VL_SCOPED_RAND_RESET_Q(62, __VscopeHash, 2781122904187892142ull);
    }
    vlSelf->full_decode_tb__DOT__dut__DOT__total_required_words = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9823728846766729392ull);
    vlSelf->full_decode_tb__DOT__dut__DOT__base_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8264110344457172272ull);
    vlSelf->full_decode_tb__DOT__dut__DOT__field_extract = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 7940800491538959634ull);
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__84__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__84__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__84__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__84__r = 0;
    vlSelf->__Vfunc_bedrock_decode_field_format_token_words__85__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_field_format_token_words__85__field_format_id = 0;
    vlSelf->__Vfunc_bedrock_decode_field_format_token_words__85__r = 0;
    vlSelf->__Vfunc_bedrock_decode_ea__86__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_ea__86__compact = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__87__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__87__ea = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__87__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__descriptor = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_13__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_12__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_11__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_10__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_9__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_8__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_7__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_6__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_5__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_4__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_3__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_2__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_1__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88____VlefCall_0__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__mode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__segment = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__88__extra = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__89__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__89__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__90__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__90__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__91__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__91__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__92__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__92__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__93__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__93__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__94__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__94__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__95__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__95__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__96__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__96__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__97__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__97__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__98__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__98__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__99__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__99__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__100__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__100__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__101__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__101__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__102__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__102__segment = 0;
    vlSelf->__Vfunc_bedrock_decode_ea__103__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_ea__103__compact = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__104__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__104__ea = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__104__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__descriptor = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_13__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_12__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_11__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_10__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_9__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_8__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_7__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_6__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_5__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_4__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_3__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_2__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_1__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105____VlefCall_0__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__mode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__segment = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__105__extra = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__106__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__106__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__107__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__107__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__108__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__108__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__109__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__109__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__110__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__110__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__111__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__111__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__112__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__112__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__113__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__113__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__114__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__114__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__115__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__115__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__116__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__116__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__117__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__117__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__118__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__118__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__119__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__119__segment = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}
