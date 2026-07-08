// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vagu_tb.h for the primary calling header

#include "Vagu_tb__pch.h"

VL_ATTR_COLD void Vagu_tb___024root___eval_static(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_static\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Vagu_tb___024root___eval_final(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_final\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vagu_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vagu_tb___024root___eval_phase__stl(Vagu_tb___024root* vlSelf);

VL_ATTR_COLD void Vagu_tb___024root___eval_settle(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_settle\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vagu_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("tb/agu_tb.sv", 4, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vagu_tb___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD void Vagu_tb___024root___eval_triggers_vec__stl(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_triggers_vec__stl\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
}

VL_ATTR_COLD bool Vagu_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vagu_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vagu_tb___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vagu_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___trigger_anySet__stl\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vagu_tb___024root___act_sequent__TOP__0(Vagu_tb___024root* vlSelf);

VL_ATTR_COLD void Vagu_tb___024root___eval_stl(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_stl\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vagu_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD bool Vagu_tb___024root___eval_phase__stl(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_phase__stl\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vagu_tb___024root___eval_triggers_vec__stl(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vagu_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vagu_tb___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vagu_tb___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vagu_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vagu_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vagu_tb___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vagu_tb___024root___ctor_var_reset(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___ctor_var_reset\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->agu_tb__DOT__request = VL_SCOPED_RAND_RESET_Q(62, __VscopeHash, 18103023875645952193ull);
    vlSelf->agu_tb__DOT__base_reg_value = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13847741526833908044ull);
    vlSelf->agu_tb__DOT__index_reg_value = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9543792838837417054ull);
    vlSelf->agu_tb__DOT__pc_value = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6695708947668486165ull);
    vlSelf->agu_tb__DOT__sp_value = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17379289395680543349ull);
    vlSelf->agu_tb__DOT__payload_value = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6004183010182048863ull);
    vlSelf->agu_tb__DOT__access_size_bytes = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7608149803133860019ull);
    vlSelf->agu_tb__DOT__valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14601883826222570646ull);
    vlSelf->agu_tb__DOT__address_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6000457362045992469ull);
    vlSelf->agu_tb__DOT__effective_address = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7504987455047149395ull);
    vlSelf->agu_tb__DOT__update_write = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12441591345119956732ull);
    vlSelf->agu_tb__DOT__update_value = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16468805198025010588ull);
    vlSelf->agu_tb__DOT__update_invalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14361065392278861259ull);
    vlSelf->__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value = 0;
    vlSelf->__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words = 0;
    vlSelf->__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value = 0;
    vlSelf->__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words = 0;
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
