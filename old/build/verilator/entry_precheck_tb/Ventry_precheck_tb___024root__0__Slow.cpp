// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Ventry_precheck_tb.h for the primary calling header

#include "Ventry_precheck_tb__pch.h"

VL_ATTR_COLD void Ventry_precheck_tb___024root___eval_static(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_static\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Ventry_precheck_tb___024root___eval_initial__TOP(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_initial__TOP\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*42:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__prefix_decode__DOT__decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__prefix_decode__DOT__decode = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__460__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__460__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__460____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__460____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__460____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__460____VlefCall_0__bedrock_decode_prefix_byte = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__460__r;
    __Vfunc_bedrock_decode_prefix_word__460__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__461__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__461__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__461__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__461__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__461__r;
    __Vfunc_bedrock_decode_prefix_byte__461__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__462__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__462__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__462__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__462__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__462__r;
    __Vfunc_bedrock_decode_prefix_byte__462__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__463__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__463__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__463__state;
    __Vfunc_bedrock_apply_prefix_byte__463__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__463__prefix;
    __Vfunc_bedrock_apply_prefix_byte__463__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__463__r;
    __Vfunc_bedrock_apply_prefix_byte__463__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__464__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__464__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__464__state;
    __Vfunc_bedrock_apply_prefix_byte__464__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__464__prefix;
    __Vfunc_bedrock_apply_prefix_byte__464__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__464__r;
    __Vfunc_bedrock_apply_prefix_byte__464__r = 0;
    // Body
    __Vfunc_bedrock_decode_prefix_word__460__r = 0ULL;
    __Vfunc_bedrock_decode_prefix_word__460__r = (0x0000040000000000ULL 
                                                  | __Vfunc_bedrock_decode_prefix_word__460__r);
    __Vfunc_bedrock_decode_prefix_byte__461__prefix_byte = 0U;
    __Vfunc_bedrock_decode_prefix_byte__461__r = 0U;
    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__461__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__461__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r)));
                    __Vfunc_bedrock_decode_prefix_byte__461__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__461__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__461__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__461__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__461__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__461__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__461__r;
    __Vfunc_bedrock_decode_prefix_word__460____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__461__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__460__r = ((0x000004003fffffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__460__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__460____VlefCall_0__bedrock_decode_prefix_byte)) 
                                                     << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__462__prefix_byte = 0U;
    __Vfunc_bedrock_decode_prefix_byte__462__r = 0U;
    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__462__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__462__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r)));
                    __Vfunc_bedrock_decode_prefix_byte__462__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__462__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__462__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__462__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__462__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__462__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__462__r;
    __Vfunc_bedrock_decode_prefix_word__460____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__462__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__460__r = ((0x000007ffc003ffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__460__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__460____VlefCall_1__bedrock_decode_prefix_byte)) 
                                                     << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__463__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__460__r 
                                  >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__463__state = __Vfunc_bedrock_decode_prefix_word__460__r;
    __Vfunc_bedrock_apply_prefix_byte__463__r = __Vfunc_bedrock_apply_prefix_byte__463__state;
    __Vfunc_bedrock_apply_prefix_byte__463__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__463__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__463__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__463__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__463__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__463__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__463__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__463__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__463__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__463__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__463__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__463__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__463__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__463__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__463__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__463__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__463__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__463__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__463__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__463__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__463__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__463__r;
    __Vfunc_bedrock_decode_prefix_word__460__r = __Vfunc_bedrock_apply_prefix_byte__463__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__464__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__460__r 
                                  >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__464__state = __Vfunc_bedrock_decode_prefix_word__460__r;
    __Vfunc_bedrock_apply_prefix_byte__464__r = __Vfunc_bedrock_apply_prefix_byte__464__state;
    __Vfunc_bedrock_apply_prefix_byte__464__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__464__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__464__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__464__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__464__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__464__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__464__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__464__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__464__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__464__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__464__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__464__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__464__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__464__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__464__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__464__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__464__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__464__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__464__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__464__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__464__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__464__r;
    __Vfunc_bedrock_decode_prefix_word__460__r = __Vfunc_bedrock_apply_prefix_byte__464__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__460__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_word__460__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__prefix_decode__DOT__decode 
        = __Vfunc_bedrock_decode_prefix_word__460__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repeat_kind 
        = (3U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__prefix_decode__DOT__decode 
                         >> 8U)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__31__KET____DOT__prefix_decode__end_group_o 
        = (1U & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__prefix_decode__DOT__decode));
}

VL_ATTR_COLD void Ventry_precheck_tb___024root___eval_final(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_final\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Ventry_precheck_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Ventry_precheck_tb___024root___eval_phase__stl(Ventry_precheck_tb___024root* vlSelf);

VL_ATTR_COLD void Ventry_precheck_tb___024root___eval_settle(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_settle\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Ventry_precheck_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("tb/entry_precheck_tb.sv", 4, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Ventry_precheck_tb___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD void Ventry_precheck_tb___024root___eval_triggers_vec__stl(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_triggers_vec__stl\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
}

VL_ATTR_COLD bool Ventry_precheck_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Ventry_precheck_tb___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Ventry_precheck_tb___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Ventry_precheck_tb___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___trigger_anySet__stl\n"); );
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

void Ventry_precheck_tb___024root___act_sequent__TOP__0(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__1(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__2(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__3(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__4(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__5(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__6(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__7(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__8(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__9(Ventry_precheck_tb___024root* vlSelf);

VL_ATTR_COLD void Ventry_precheck_tb___024root___eval_stl(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_stl\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Ventry_precheck_tb___024root___act_sequent__TOP__0(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__1(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__2(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__3(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__4(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__5(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__6(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__7(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__8(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__9(vlSelf);
    }
}

VL_ATTR_COLD bool Ventry_precheck_tb___024root___eval_phase__stl(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_phase__stl\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Ventry_precheck_tb___024root___eval_triggers_vec__stl(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Ventry_precheck_tb___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Ventry_precheck_tb___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Ventry_precheck_tb___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Ventry_precheck_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Ventry_precheck_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Ventry_precheck_tb___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Ventry_precheck_tb___024root___ctor_var_reset(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___ctor_var_reset\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    VL_SCOPED_RAND_RESET_W(512, vlSelf->entry_precheck_tb__DOT__line_words, __VscopeHash, 14420400605313856354ull);
    vlSelf->entry_precheck_tb__DOT__entry_valid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8564427737933560002ull);
    vlSelf->entry_precheck_tb__DOT__repcc_allowed = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14399832306563251896ull);
    vlSelf->entry_precheck_tb__DOT__repg_allowed = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18180864901115704275ull);
    vlSelf->entry_precheck_tb__DOT__repg_fast_candidate = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 711704718757963453ull);
    vlSelf->entry_precheck_tb__DOT__repcc_valid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16601399720082543365ull);
    vlSelf->entry_precheck_tb__DOT__repg_valid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14386036863648360856ull);
    vlSelf->entry_precheck_tb__DOT__repeat_invalid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9314184151203189705ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2453680767643556285ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12068000665455470050ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2012655802072124988ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3878343829928628624ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13542398710509859290ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8350277375184803508ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__0__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3801301111324056513ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15556128103624521701ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13942390523292011565ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7474088296939970627ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14850917969889040866ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17404123998449698824ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__1__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3190370303259051681ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5272600130995701358ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 58587053150739367ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9827444707860000527ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3144978236377916053ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 486750895611898300ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__2__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8841368186584699442ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5124849829381401585ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5117148192159256184ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8000580032290646519ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15676939584049588582ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8454387993263113746ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__3__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3053667870442920208ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2873430288461668032ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1559462866736189414ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16574294099924310301ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2096479369667869221ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1170875734747911331ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__4__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14319614534428844504ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4938640251222173288ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3100571504810910870ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9732428022304756512ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1597017513553599428ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3833349377307740200ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__5__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16967365885959578033ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7289988392516376429ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12016688285516151270ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15058547814754409868ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4855806074919633045ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18381023406835828408ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18379390099546178796ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__6__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7274382436951371137ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8316460620382567888ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5463570686590504128ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10056668763791000186ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16567535050950754655ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1215123293196830264ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__7__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8060453562525371730ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 857210282885311028ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17991766231754560373ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12660872744426879657ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4635299722866670352ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2609191473649864574ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__8__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2834506747219105682ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15618844717495920689ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12815739113085105920ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10284647249609076338ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4065893881586622931ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16870931236452416291ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__9__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5472846386361536104ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14772110580248977092ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4156426069391536995ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15416522459513586657ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9161426609926389944ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13396403689565503700ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2986167399097677541ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__10__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9349157519286616384ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7001177814039141794ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4824300298946798372ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9586868381459608521ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1165570339744111860ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18003891842464907419ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__11__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17298612106575210647ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7897053145134292718ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8074114235400478535ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3216586316206568098ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2559455883380927386ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3910107989719399128ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__12__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14960052017470789332ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10955541081028496784ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10118012022814677741ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15511012333593519029ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12682633967384462835ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15171745614790691160ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__13__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3845910932731298117ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5489138567748299344ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 93682828295964501ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1986104411710906510ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14121232205930916239ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 909789256533988438ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2956036024697582724ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__14__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15392891980272779403ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15778237670179304206ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11300420148887346228ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6069964009258567016ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16131437672953858329ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8894203215216824767ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__15__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12812123234826082987ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8116539644783001951ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15993361772360951650ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17097527946492872412ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3810685106116613232ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 44395203624824818ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__16__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15584458814380128245ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10443544902806233474ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3881881462696628412ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13293044351268805401ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 499633922162030864ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 308596433901524293ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__17__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9787768047236989757ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15785044761419068240ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4820076416591160463ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3735783510827500784ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17610055522565070909ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 267438644303202181ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2506896352894822078ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__18__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9688053383578680007ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13458711754565830527ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13935488779173534568ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10400540112241881986ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3019858038922025056ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7164759269028555313ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__19__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10869226033789392899ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17363764431907514048ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17910055069792208801ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13179424588829234174ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3961990526064299249ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4355849465628434871ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__20__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1136922457805968238ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14268726527756703665ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10292039584059107502ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15255461233323390516ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11415187276418018484ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3341224798537211555ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__21__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17632092517198760052ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8037801553877088271ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14114750067462349190ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3455254205885994607ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1862377434431745638ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2768104942321963655ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4784235039650043153ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__22__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 161448573814727345ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9824984006508043865ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9947922477507974712ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1743649125404345523ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11246534692643640973ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15396069871334234428ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__23__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8291735284011101097ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4573026968055941211ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3574042781263377440ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7435785419709194045ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4663937495576658801ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15319818648013239580ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__24__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4367539434666969614ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2174944212883159490ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 585430401212553039ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 891710771815043321ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 400141585814118561ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4898893172904362883ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__25__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1662248906533801326ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11506944788980743546ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3881612846995509369ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3314060259875535207ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5725209840256135804ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4095008412672360085ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7782528205094330057ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__26__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3247425536165364620ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1940559473899404287ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15081246414942168583ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2452091318276863742ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3701752974002442287ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 356205549623477696ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__27__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1305700290484643241ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8109782456639767586ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13296481497078128181ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8669141376242583174ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8210060988190328393ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6079616161675951735ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__28__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13859124628981578426ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11674473968686217444ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repcc_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8761071924384746326ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repg_allowed_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15183874030093692901ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repg_fast_candidate_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1221256499203147253ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17359045786542592113ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__29__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10799232507602682324ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__needs_extension = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11955235500087097956ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__opcode_id = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13722325930571961206ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_valid_raw = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 933980178728718109ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17940151412642890866ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__30__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repeat_kind = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5933699155160933135ull);
    vlSelf->entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__31__KET____DOT__prefix_decode__end_group_o = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__218__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__218__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__218__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__218__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__226__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__226__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__226__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__226__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__234__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__234__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__234__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__234__r = 0;
    vlSelf->__Vfunc_bedrock_decode_opcode_attributes__235__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__242__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__242__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__242__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__242__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__250__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__250__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__250__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__250__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__258__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__258__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__258__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__258__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__266__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__266__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__266__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__266__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__274__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__274__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__274__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__274__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__282__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__282__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__282__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__282__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__290__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__290__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__290__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__290__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__298__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__298__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__298__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__298__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__306__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__306__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__306__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__306__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__314__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__314__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__314__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__314__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__322__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__322__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__322__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__322__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__330__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__330__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__330__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__330__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__338__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__338__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__338__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__338__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__346__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__346__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__346__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__346__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__354__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__354__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__354__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__354__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__362__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__362__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__362__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__362__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__370__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__370__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__370__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__370__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__378__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__378__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__378__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__378__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__386__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__386__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__386__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__386__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__394__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__394__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__394__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__394__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__402__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__402__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__402__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__402__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__410__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__410__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__410__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__410__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__418__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__418__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__418__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__418__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__426__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__426__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__426__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__426__r = 0;
    vlSelf->__Vfunc_bedrock_decode_prefix_word__428__prefix_word = 0;
    vlSelf->__Vfunc_bedrock_decode_prefix_word__428__r = 0;
    vlSelf->__Vfunc_bedrock_decode_prefix_byte__429__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__434__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__434__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__434__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__434__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__442__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__442__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__442__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__442__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__450__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__450__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__450__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__450__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__458__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__458__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__458__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__458__r = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__466__Vfuncout = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__466__ext_root = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__466__extension_word = 0;
    vlSelf->__Vfunc_bedrock_decode_extended_opcode__466__r = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_3 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_4 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_5 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_6 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_7 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_8 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_9 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_10 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_11 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_12 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_13 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_14 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_15 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_16 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_17 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_18 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_19 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_20 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_21 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_22 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_23 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_24 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_25 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_26 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_27 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_28 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_29 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_30 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_31 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_32 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_33 = 0;
    vlSelf->__VdfgRegularize_hebeb780c_0_34 = 0;
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
