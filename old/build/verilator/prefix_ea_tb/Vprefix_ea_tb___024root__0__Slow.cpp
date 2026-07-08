// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vprefix_ea_tb.h for the primary calling header

#include "Vprefix_ea_tb__pch.h"

VL_ATTR_COLD void Vprefix_ea_tb___024root___eval_static(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_static\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Vprefix_ea_tb___024root___eval_final(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_final\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vprefix_ea_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vprefix_ea_tb___024root___eval_phase__stl(Vprefix_ea_tb___024root* vlSelf);

VL_ATTR_COLD void Vprefix_ea_tb___024root___eval_settle(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_settle\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vprefix_ea_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("tb/prefix_ea_tb.sv", 4, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vprefix_ea_tb___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD void Vprefix_ea_tb___024root___eval_triggers_vec__stl(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_triggers_vec__stl\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
}

VL_ATTR_COLD bool Vprefix_ea_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vprefix_ea_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vprefix_ea_tb___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vprefix_ea_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void Vprefix_ea_tb___024root___stl_sequent__TOP__0(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___stl_sequent__TOP__0\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*42:0*/ prefix_ea_tb__DOT__prefix_dut__DOT__decode;
    prefix_ea_tb__DOT__prefix_dut__DOT__decode = 0;
    QData/*39:0*/ prefix_ea_tb__DOT__ea_dut__DOT__decode;
    prefix_ea_tb__DOT__ea_dut__DOT__decode = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__15__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__15__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_prefix_word__15__prefix_word;
    __Vfunc_bedrock_decode_prefix_word__15__prefix_word = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__15____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__15____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__15____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__15____VlefCall_0__bedrock_decode_prefix_byte = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__15__r;
    __Vfunc_bedrock_decode_prefix_word__15__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__16__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__16__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__16__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__16__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__16__r;
    __Vfunc_bedrock_decode_prefix_byte__16__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__17__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__17__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__17__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__17__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__17__r;
    __Vfunc_bedrock_decode_prefix_byte__17__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__18__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__18__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__18__state;
    __Vfunc_bedrock_apply_prefix_byte__18__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__18__prefix;
    __Vfunc_bedrock_apply_prefix_byte__18__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__18__r;
    __Vfunc_bedrock_apply_prefix_byte__18__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__19__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__19__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__19__state;
    __Vfunc_bedrock_apply_prefix_byte__19__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__19__prefix;
    __Vfunc_bedrock_apply_prefix_byte__19__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__19__r;
    __Vfunc_bedrock_apply_prefix_byte__19__r = 0;
    CData/*5:0*/ __Vfunc_bedrock_decode_ea__20__ea;
    __Vfunc_bedrock_decode_ea__20__ea = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_ea__20__descriptor;
    __Vfunc_bedrock_decode_ea__20__descriptor = 0;
    // Body
    __Vfunc_bedrock_decode_prefix_word__15__prefix_word 
        = vlSelfRef.prefix_ea_tb__DOT__prefix_word;
    __Vfunc_bedrock_decode_prefix_word__15__r = 0ULL;
    __Vfunc_bedrock_decode_prefix_word__15__r = (0x0000040000000000ULL 
                                                 | __Vfunc_bedrock_decode_prefix_word__15__r);
    __Vfunc_bedrock_decode_prefix_byte__16__prefix_byte 
        = (0x000000ffU & (IData)(__Vfunc_bedrock_decode_prefix_word__15__prefix_word));
    __Vfunc_bedrock_decode_prefix_byte__16__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__16__r = 
            (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__16__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__16__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r)));
                    __Vfunc_bedrock_decode_prefix_byte__16__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__16__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__16__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__16__r = 
            ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
              ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
              : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
                  : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                      ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                          ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
                          : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                              ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))
                                  : (0x00000d80U | 
                                     (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r))))
                              : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r)) 
                                 | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                      ? 0x1aU : 0x19U) 
                                    << 7U)))) : ((0x007fU 
                                                  & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__r)) 
                                                 | (((4U 
                                                      & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                      ? 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                        ? 0x18U
                                                        : 0x17U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                        ? 0x16U
                                                        : 0x15U))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                        ? 0x14U
                                                        : 0x13U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__16__prefix_byte))
                                                        ? 0x12U
                                                        : 0x11U))) 
                                                    << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__16__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__16__r;
    __Vfunc_bedrock_decode_prefix_word__15____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__16__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__15__r = ((0x000004003fffffffULL 
                                                  & __Vfunc_bedrock_decode_prefix_word__15__r) 
                                                 | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__15____VlefCall_0__bedrock_decode_prefix_byte)) 
                                                    << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__17__prefix_byte 
        = (0x000000ffU & ((IData)(__Vfunc_bedrock_decode_prefix_word__15__prefix_word) 
                          >> 8U));
    __Vfunc_bedrock_decode_prefix_byte__17__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__17__r = 
            (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__17__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__17__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r)));
                    __Vfunc_bedrock_decode_prefix_byte__17__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__17__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__17__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__17__r = 
            ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
              ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
              : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
                  : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                      ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                          ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
                          : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                              ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                  ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))
                                  : (0x00000d80U | 
                                     (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r))))
                              : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r)) 
                                 | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                      ? 0x1aU : 0x19U) 
                                    << 7U)))) : ((0x007fU 
                                                  & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__r)) 
                                                 | (((4U 
                                                      & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                      ? 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                        ? 0x18U
                                                        : 0x17U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                        ? 0x16U
                                                        : 0x15U))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                       ? 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                        ? 0x14U
                                                        : 0x13U)
                                                       : 
                                                      ((1U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__17__prefix_byte))
                                                        ? 0x12U
                                                        : 0x11U))) 
                                                    << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__17__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__17__r;
    __Vfunc_bedrock_decode_prefix_word__15____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__17__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__15__r = ((0x000007ffc003ffffULL 
                                                  & __Vfunc_bedrock_decode_prefix_word__15__r) 
                                                 | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__15____VlefCall_1__bedrock_decode_prefix_byte)) 
                                                    << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__18__prefix = 
        (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__15__r 
                                >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__18__state = __Vfunc_bedrock_decode_prefix_word__15__r;
    __Vfunc_bedrock_apply_prefix_byte__18__r = __Vfunc_bedrock_apply_prefix_byte__18__state;
    __Vfunc_bedrock_apply_prefix_byte__18__r = ((0x000003ffffffffffULL 
                                                 & __Vfunc_bedrock_apply_prefix_byte__18__r) 
                                                | ((QData)((IData)((IData)(
                                                                           ((__Vfunc_bedrock_apply_prefix_byte__18__r 
                                                                             >> 0x0000002aU) 
                                                                            & ((IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix) 
                                                                               >> 0x0000000bU))))) 
                                                   << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__18__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__18__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__18__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__18__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__18__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__18__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__18__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__18__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__18__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__18__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__18__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__18__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__18__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__18__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__18__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__18__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__18__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__18__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__18__r;
    __Vfunc_bedrock_decode_prefix_word__15__r = __Vfunc_bedrock_apply_prefix_byte__18__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__19__prefix = 
        (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__15__r 
                                >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__19__state = __Vfunc_bedrock_decode_prefix_word__15__r;
    __Vfunc_bedrock_apply_prefix_byte__19__r = __Vfunc_bedrock_apply_prefix_byte__19__state;
    __Vfunc_bedrock_apply_prefix_byte__19__r = ((0x000003ffffffffffULL 
                                                 & __Vfunc_bedrock_apply_prefix_byte__19__r) 
                                                | ((QData)((IData)((IData)(
                                                                           ((__Vfunc_bedrock_apply_prefix_byte__19__r 
                                                                             >> 0x0000002aU) 
                                                                            & ((IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix) 
                                                                               >> 0x0000000bU))))) 
                                                   << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__19__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__19__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__19__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__19__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__19__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__19__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__19__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__19__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__19__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__19__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__19__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__19__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__19__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__19__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__19__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__19__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__19__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__19__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__19__r;
    __Vfunc_bedrock_decode_prefix_word__15__r = __Vfunc_bedrock_apply_prefix_byte__19__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__15__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_word__15__r;
    prefix_ea_tb__DOT__prefix_dut__DOT__decode = __Vfunc_bedrock_decode_prefix_word__15__Vfuncout;
    vlSelfRef.prefix_ea_tb__DOT__prefix_valid = (1U 
                                                 & (IData)(
                                                           (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                            >> 0x0000002aU)));
    vlSelfRef.prefix_ea_tb__DOT__nospec = (1U & (IData)(
                                                        (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                         >> 0x00000011U)));
    vlSelfRef.prefix_ea_tb__DOT__saturate = (1U & (IData)(
                                                          (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                           >> 0x00000010U)));
    vlSelfRef.prefix_ea_tb__DOT__update_mode = (7U 
                                                & (IData)(
                                                          (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                           >> 0x0000000cU)));
    vlSelfRef.prefix_ea_tb__DOT__access_mode = (3U 
                                                & (IData)(
                                                          (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                           >> 0x0000000aU)));
    vlSelfRef.prefix_ea_tb__DOT__repeat_kind = (3U 
                                                & (IData)(
                                                          (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                           >> 8U)));
    vlSelfRef.prefix_ea_tb__DOT__repeat_condition = 
        (0x0000000fU & (IData)((prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                >> 4U)));
    vlSelfRef.prefix_ea_tb__DOT__repeat_counter = (7U 
                                                   & (IData)(
                                                             (prefix_ea_tb__DOT__prefix_dut__DOT__decode 
                                                              >> 1U)));
    vlSelfRef.prefix_ea_tb__DOT__end_group = (1U & (IData)(prefix_ea_tb__DOT__prefix_dut__DOT__decode));
    __Vfunc_bedrock_decode_ea__20__descriptor = vlSelfRef.prefix_ea_tb__DOT__descriptor;
    __Vfunc_bedrock_decode_ea__20__ea = vlSelfRef.prefix_ea_tb__DOT__ea;
    {
        vlSelf->__Vfunc_bedrock_decode_ea__20__Vfuncout = 0;
        vlSelf->__Vfunc_bedrock_decode_ea__20__compact = 0;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea 
            = __Vfunc_bedrock_decode_ea__20__ea;
        vlSelf->__Vfunc_bedrock_decode_compact_ea__21__Vfuncout = 0;
        vlSelf->__Vfunc_bedrock_decode_compact_ea__21__r = 0;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r = 0ULL;
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
            = (0x0000000001000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000008000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x00000004c0000000ULL 
                                       | (0x000000f001ffffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000000000200000ULL 
                                       | (0x000000ffff00ffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000002000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (1ULL | (0x000000fffffffff8ULL 
                                               & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000008000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000000480000000ULL 
                                       | (0x000000f001ffffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000000000200000ULL 
                                       | (0x000000ffff00ffffULL 
                                          & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (0x0000003000000000ULL 
                                       | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                    = (1ULL | (0x000000fffffffff8ULL 
                                               & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000448000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000000024ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000408000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000000012ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x00000003c8000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000380000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (9ULL | (0x000000ffffffff00ULL 
                                       & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000390000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000000000064ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000350000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000000000052ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                }
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x0000000320000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x0000000000300000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x000000ffffffff00ULL 
                                   & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x00000002d0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x0000000000f00000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                                = (0x00000000000000a4ULL 
                                   | (0x000000ffffffff00ULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000290000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000f00000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000000092ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000250000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000f00000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000000000089ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x0000000210000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x00000000000c0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                            = (0x00000000000000a4ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x00000001d0000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x00000000000c0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000000000092ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000190000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x00000000000c0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                    vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                        = (0x0000000000000089ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000000150000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000000000000092ULL | (0x000000ffffffff00ULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea)))) 
                          << 0x0000000dU));
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000000110000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000000000000089ULL | (0x000000ffffffff00ULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea)))) 
                          << 0x0000000dU));
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x00000000d4000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
                vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                    = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r) 
                       | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea)))) 
                          << 0x0000000dU));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea))) {
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x00000000a0000000ULL | (0x000000f001ffffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x00000000002a0000ULL | (0x000000ffff00ffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r) 
                   | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea)))) 
                      << 0x0000000dU));
        } else {
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x0000000060000000ULL | (0x000000f001ffffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x0000000000260000ULL | (0x000000ffff00ffffULL 
                                            & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r));
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r);
            vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r 
                = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r) 
                   | ((QData)((IData)((7U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__ea)))) 
                      << 0x0000000dU));
        }
        vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__r;
        vlSelfRef.__Vfunc_bedrock_decode_ea__20__compact 
            = vlSelfRef.__Vfunc_bedrock_decode_compact_ea__21__Vfuncout;
        if ((1U & (IData)((vlSelfRef.__Vfunc_bedrock_decode_ea__20__compact 
                           >> 0x00000025U)))) {
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__descriptor 
                = __Vfunc_bedrock_decode_ea__20__descriptor;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape 
                = (1U & (IData)((vlSelfRef.__Vfunc_bedrock_decode_ea__20__compact 
                                 >> 0x00000024U)));
            vlSelf->__Vfunc_bedrock_decode_extended_ea__22__Vfuncout = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__22__r = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__22__mode = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__22__segment = 0;
            vlSelf->__Vfunc_bedrock_decode_extended_ea__22__extra = 0;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r = 0ULL;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                = ((0x000000efffffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                   | ((QData)((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape)) 
                      << 0x00000024U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode 
                = (0x0000001fU & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__descriptor) 
                                  >> 0x0bU));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment 
                = (7U & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__descriptor) 
                         >> 8U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra 
                = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__descriptor));
            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
            vlSelf->__Vfunc_bedrock_ea_segment_decode__23__Vfuncout = 0;
            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__Vfuncout 
                = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                    ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                            ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                                           ? 4U : 3U))
                    : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                            ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__segment))
                                           ? 1U : 0U)));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_0__bedrock_ea_segment_decode 
                = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__23__Vfuncout;
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                   | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_0__bedrock_ea_segment_decode)))) 
                      << 0x00000015U));
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000b10000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000890000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000ad0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | (IData)((IData)(
                                                     (0x93U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000850000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x00000000000d0000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | (IData)((IData)(
                                                     (0x93U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      ((0U 
                                                        == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                       << 3U))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000a90000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x00000000000d0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((
                                                   (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                   << 3U))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000810000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x00000000000d0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((
                                                   (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                   << 3U))) 
                                  << 0x00000015U));
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000a50000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000000f10000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000001000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      (7U 
                                                       | ((0U 
                                                           == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                          << 3U)))) 
                                      << 0x00000015U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x00000007d0000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000000f10000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000ffffffe000ULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | (IData)((IData)(
                                                     (0xa5U 
                                                      | (0x00001f00U 
                                                         & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                            << 8U))))));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      (7U 
                                                       | ((0U 
                                                           == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                          << 3U)))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000a10000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x93U 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000790000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x93U 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x00000009d0000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000750000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000000f10000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffffe000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x8aU 
                                                  | (0x00001f00U 
                                                     & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                        << 8U))))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((7U 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment)) 
                                                      << 3U)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000712000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000000340000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000000000065ULL | 
                           (0x000000ffffffff00ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__24__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_13__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__24__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_13__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                        if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000004000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000008000000000ULL 
                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x00000006d2000000ULL 
                                   | (0x000000f001ffffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000000340000ULL 
                                   | (0x000000ffff00ffffULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = (0x0000000000000053ULL 
                                   | (0x000000ffffffff00ULL 
                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment 
                                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                            vlSelf->__Vfunc_bedrock_ea_segment_decode__25__Vfuncout = 0;
                            vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__Vfuncout 
                                = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                    ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                            ? 6U : 5U)
                                        : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                            ? 4U : 3U))
                                    : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                        ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                            ? 2U : 7U)
                                        : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__segment))
                                            ? 1U : 0U)));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_12__bedrock_ea_segment_decode 
                                = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__25__Vfuncout;
                            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                                = ((0x000000fffe1fffffULL 
                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                                   | ((QData)((IData)(
                                                      (8U 
                                                       | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_12__bedrock_ea_segment_decode)))) 
                                      << 0x00000015U));
                        }
                    } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000692000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x00000000002a0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000000000093ULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffff1fffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((7U 
                                                   & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                      >> 5U)))) 
                                  << 0x0000000dU));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__26__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_11__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__26__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_11__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000004000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000652000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x00000000002a0000ULL 
                               | (0x000000ffff00ffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x000000000000008aULL 
                               | (0x000000ffffffff00ULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffffff1fffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((7U 
                                                   & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                      >> 5U)))) 
                                  << 0x0000000dU));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__27__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_10__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__27__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_10__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000004000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000616000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x00000000002a0000ULL | 
                           (0x000000ffff00ffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (1ULL | (0x000000ffffffff00ULL 
                                   & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000ffffff1fffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((7U & 
                                               ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                >> 5U)))) 
                              << 0x0000000dU));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__28__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_9__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__28__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_9__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                    if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000000992000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffff000000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x002b00a5U 
                                                  | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                     << 8U)))));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000001000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__29__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_7__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__29__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_7__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x0000008000000000ULL 
                               | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = (0x00000005d2000000ULL 
                               | (0x000000f001ffffffULL 
                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000ffff000000ULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | (IData)((IData)((0x002b00a5U 
                                                  | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                     << 8U)))));
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment 
                            = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                        vlSelf->__Vfunc_bedrock_ea_segment_decode__30__Vfuncout = 0;
                        vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__Vfuncout 
                            = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                        ? 6U : 5U) : 
                                   ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                     ? 4U : 3U)) : 
                               ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                 ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                     ? 2U : 7U) : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__segment))
                                                    ? 1U
                                                    : 0U)));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_8__bedrock_ea_segment_decode 
                            = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__30__Vfuncout;
                        vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                            = ((0x000000fffe1fffffULL 
                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                               | ((QData)((IData)((8U 
                                                   | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_8__bedrock_ea_segment_decode)))) 
                                  << 0x00000015U));
                    }
                } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000952000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | (IData)((IData)((0x002b0093U 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__31__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_5__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__31__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_5__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000592000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | (IData)((IData)((0x002b0093U 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__32__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_6__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__32__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_6__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__mode))) {
                if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000912000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | (IData)((IData)((0x002b008aU 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__33__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_3__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__33__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_3__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = (0x0000000552000000ULL | 
                           (0x000000f001ffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | (IData)((IData)((0x002b008aU 
                                              | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                                 << 8U)))));
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment 
                        = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                    vlSelf->__Vfunc_bedrock_ea_segment_decode__34__Vfuncout = 0;
                    vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__Vfuncout 
                        = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                                    ? 6U : 5U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                                                   ? 4U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                                    ? 2U : 7U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__segment))
                                                   ? 1U
                                                   : 0U)));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_4__bedrock_ea_segment_decode 
                        = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__34__Vfuncout;
                    vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                        = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                           | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_4__bedrock_ea_segment_decode)))) 
                              << 0x00000015U));
                }
            } else if (vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = (0x00000008d2000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                       | (IData)((IData)((0x002b0001U 
                                          | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                             << 8U)))));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = (0x0000001000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment 
                    = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                vlSelf->__Vfunc_bedrock_ea_segment_decode__35__Vfuncout = 0;
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__Vfuncout 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                                ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                                               ? 4U
                                               : 3U))
                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                                ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__segment))
                                               ? 1U
                                               : 0U)));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_1__bedrock_ea_segment_decode 
                    = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__35__Vfuncout;
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                       | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_1__bedrock_ea_segment_decode)))) 
                          << 0x00000015U));
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = (0x0000008000000000ULL | vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r);
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = (0x0000000512000000ULL | (0x000000f001ffffffULL 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = ((0x000000ffff000000ULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                       | (IData)((IData)((0x002b0001U 
                                          | ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__extra) 
                                             << 8U)))));
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment 
                    = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__segment;
                vlSelf->__Vfunc_bedrock_ea_segment_decode__36__Vfuncout = 0;
                vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__Vfuncout 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                                ? 6U : 5U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                                               ? 4U
                                               : 3U))
                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                                ? 2U : 7U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__segment))
                                               ? 1U
                                               : 0U)));
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_2__bedrock_ea_segment_decode 
                    = vlSelfRef.__Vfunc_bedrock_ea_segment_decode__36__Vfuncout;
                vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                    = ((0x000000fffe1fffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                       | ((QData)((IData)((8U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22____VlefCall_2__bedrock_ea_segment_decode)))) 
                          << 0x00000015U));
            }
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r 
                = ((0x0000007fffffffffULL & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r) 
                   | ((QData)((IData)((IData)((0x0000008001000000ULL 
                                               == (0x0000008001000000ULL 
                                                   & vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r))))) 
                      << 0x00000027U));
            vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__Vfuncout 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__r;
            vlSelfRef.__Vfunc_bedrock_decode_ea__20__Vfuncout 
                = vlSelfRef.__Vfunc_bedrock_decode_extended_ea__22__Vfuncout;
            goto __Vlabel0;
        }
        vlSelfRef.__Vfunc_bedrock_decode_ea__20__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_ea__20__compact;
        __Vlabel0: ;
    }
    prefix_ea_tb__DOT__ea_dut__DOT__decode = vlSelfRef.__Vfunc_bedrock_decode_ea__20__Vfuncout;
    vlSelfRef.prefix_ea_tb__DOT__ea_valid = (1U & (IData)(
                                                          (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                           >> 0x00000027U)));
    vlSelfRef.prefix_ea_tb__DOT__ea_reserved = (1U 
                                                & (IData)(
                                                          (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                           >> 0x00000026U)));
    vlSelfRef.prefix_ea_tb__DOT__ea_form = (0x0000003fU 
                                            & (IData)(
                                                      (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                       >> 0x0000001eU)));
    vlSelfRef.prefix_ea_tb__DOT__segment = (7U & (IData)(
                                                         (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                          >> 0x00000015U)));
    vlSelfRef.prefix_ea_tb__DOT__base = (7U & (IData)(
                                                      (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                       >> 0x00000012U)));
    vlSelfRef.prefix_ea_tb__DOT__base_reg = (7U & (IData)(
                                                          (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                           >> 0x0000000dU)));
    vlSelfRef.prefix_ea_tb__DOT__index_reg = (7U & (IData)(
                                                           (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                            >> 0x0000000aU)));
    vlSelfRef.prefix_ea_tb__DOT__scale_log2 = (3U & (IData)(
                                                            (prefix_ea_tb__DOT__ea_dut__DOT__decode 
                                                             >> 8U)));
    vlSelfRef.prefix_ea_tb__DOT__payload_words = (7U 
                                                  & (IData)(prefix_ea_tb__DOT__ea_dut__DOT__decode));
}

VL_ATTR_COLD void Vprefix_ea_tb___024root___eval_stl(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_stl\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vprefix_ea_tb___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD bool Vprefix_ea_tb___024root___eval_phase__stl(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_phase__stl\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vprefix_ea_tb___024root___eval_triggers_vec__stl(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vprefix_ea_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vprefix_ea_tb___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vprefix_ea_tb___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vprefix_ea_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vprefix_ea_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vprefix_ea_tb___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vprefix_ea_tb___024root___ctor_var_reset(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___ctor_var_reset\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->prefix_ea_tb__DOT__prefix_word = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5546928798066001393ull);
    vlSelf->prefix_ea_tb__DOT__prefix_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3940943707180519752ull);
    vlSelf->prefix_ea_tb__DOT__nospec = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5007781115590795916ull);
    vlSelf->prefix_ea_tb__DOT__saturate = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1531971239633367586ull);
    vlSelf->prefix_ea_tb__DOT__update_mode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7414066911843032229ull);
    vlSelf->prefix_ea_tb__DOT__access_mode = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6706706167197552541ull);
    vlSelf->prefix_ea_tb__DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3720052031035997431ull);
    vlSelf->prefix_ea_tb__DOT__repeat_condition = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11715796693446637302ull);
    vlSelf->prefix_ea_tb__DOT__repeat_counter = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11346966235195961118ull);
    vlSelf->prefix_ea_tb__DOT__end_group = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3586447819571286567ull);
    vlSelf->prefix_ea_tb__DOT__ea = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3125253699126575698ull);
    vlSelf->prefix_ea_tb__DOT__descriptor = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5365165304962791699ull);
    vlSelf->prefix_ea_tb__DOT__ea_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6865622348281243033ull);
    vlSelf->prefix_ea_tb__DOT__ea_reserved = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4322887631874014181ull);
    vlSelf->prefix_ea_tb__DOT__ea_form = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 9233700684581168766ull);
    vlSelf->prefix_ea_tb__DOT__segment = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14051061463142575064ull);
    vlSelf->prefix_ea_tb__DOT__base = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1601765511237696068ull);
    vlSelf->prefix_ea_tb__DOT__base_reg = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9283374230300393277ull);
    vlSelf->prefix_ea_tb__DOT__index_reg = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2400101767325755920ull);
    vlSelf->prefix_ea_tb__DOT__scale_log2 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6807448186337648580ull);
    vlSelf->prefix_ea_tb__DOT__payload_words = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4521480767252133764ull);
    vlSelf->__Vfunc_bedrock_decode_ea__20__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_ea__20__compact = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__21__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__21__ea = 0;
    vlSelf->__Vfunc_bedrock_decode_compact_ea__21__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__descriptor = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_13__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_12__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_11__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_10__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_9__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_8__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_7__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_6__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_5__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_4__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_3__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_2__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_1__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22____VlefCall_0__bedrock_ea_segment_decode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__mode = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__segment = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_ea__22__extra = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__23__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__23__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__24__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__24__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__25__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__25__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__26__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__26__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__27__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__27__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__28__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__28__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__29__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__29__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__30__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__30__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__31__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__31__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__32__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__32__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__33__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__33__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__34__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__34__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__35__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__35__segment = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__36__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_ea_segment_decode__36__segment = 0;
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
