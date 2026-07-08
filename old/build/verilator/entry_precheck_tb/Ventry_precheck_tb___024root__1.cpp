// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Ventry_precheck_tb.h for the primary calling header

#include "Ventry_precheck_tb__pch.h"

void Ventry_precheck_tb___024root___act_sequent__TOP__1(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___act_sequent__TOP__1\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__opcode_id;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__opcode_id = 0;
    CData/*7:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__opcode_id;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__opcode_id = 0;
    CData/*7:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__opcode_id;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__opcode_id = 0;
    IData/*25:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode = 0;
    IData/*19:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode = 0;
    CData/*2:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__attributes;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__attributes = 0;
    IData/*25:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode = 0;
    IData/*19:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode = 0;
    CData/*2:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__attributes;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__attributes = 0;
    IData/*25:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode = 0;
    IData/*19:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode = 0;
    QData/*42:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_decode__DOT__decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_decode__DOT__decode = 0;
    QData/*42:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_decode__DOT__decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_decode__DOT__decode = 0;
    QData/*42:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_decode__DOT__decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_decode__DOT__decode = 0;
    QData/*42:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_decode__DOT__decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_decode__DOT__decode = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__217__Vfuncout;
    __Vfunc_bedrock_decode_primary_payload__217__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_primary_payload__217__payload;
    __Vfunc_bedrock_decode_primary_payload__217__payload = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__217__r;
    __Vfunc_bedrock_decode_primary_payload__217__r = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__219__Vfuncout;
    __Vfunc_bedrock_decode_opcode_attributes__219__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_opcode_attributes__219__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__219__opcode_id = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__219__r;
    __Vfunc_bedrock_decode_opcode_attributes__219__r = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__225__Vfuncout;
    __Vfunc_bedrock_decode_primary_payload__225__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_primary_payload__225__payload;
    __Vfunc_bedrock_decode_primary_payload__225__payload = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__225__r;
    __Vfunc_bedrock_decode_primary_payload__225__r = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__227__Vfuncout;
    __Vfunc_bedrock_decode_opcode_attributes__227__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_opcode_attributes__227__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__227__opcode_id = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__227__r;
    __Vfunc_bedrock_decode_opcode_attributes__227__r = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__233__Vfuncout;
    __Vfunc_bedrock_decode_primary_payload__233__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_primary_payload__233__payload;
    __Vfunc_bedrock_decode_primary_payload__233__payload = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__233__r;
    __Vfunc_bedrock_decode_primary_payload__233__r = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_opcode_attributes__235__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__235__opcode_id = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__428__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__428__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__428____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__428____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__428____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__428____VlefCall_0__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__429__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__429__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__430__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__430__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__430__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__430__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__430__r;
    __Vfunc_bedrock_decode_prefix_byte__430__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__431__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__431__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__431__state;
    __Vfunc_bedrock_apply_prefix_byte__431__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__431__prefix;
    __Vfunc_bedrock_apply_prefix_byte__431__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__431__r;
    __Vfunc_bedrock_apply_prefix_byte__431__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__432__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__432__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__432__state;
    __Vfunc_bedrock_apply_prefix_byte__432__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__432__prefix;
    __Vfunc_bedrock_apply_prefix_byte__432__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__432__r;
    __Vfunc_bedrock_apply_prefix_byte__432__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__436__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__436__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_prefix_word__436__prefix_word;
    __Vfunc_bedrock_decode_prefix_word__436__prefix_word = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__436____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__436____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__436____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__436____VlefCall_0__bedrock_decode_prefix_byte = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__436__r;
    __Vfunc_bedrock_decode_prefix_word__436__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__437__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__437__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__437__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__437__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__437__r;
    __Vfunc_bedrock_decode_prefix_byte__437__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__438__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__438__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__438__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__438__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__438__r;
    __Vfunc_bedrock_decode_prefix_byte__438__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__439__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__439__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__439__state;
    __Vfunc_bedrock_apply_prefix_byte__439__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__439__prefix;
    __Vfunc_bedrock_apply_prefix_byte__439__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__439__r;
    __Vfunc_bedrock_apply_prefix_byte__439__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__440__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__440__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__440__state;
    __Vfunc_bedrock_apply_prefix_byte__440__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__440__prefix;
    __Vfunc_bedrock_apply_prefix_byte__440__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__440__r;
    __Vfunc_bedrock_apply_prefix_byte__440__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__444__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__444__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_prefix_word__444__prefix_word;
    __Vfunc_bedrock_decode_prefix_word__444__prefix_word = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__444____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__444____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__444____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__444____VlefCall_0__bedrock_decode_prefix_byte = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__444__r;
    __Vfunc_bedrock_decode_prefix_word__444__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__445__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__445__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__445__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__445__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__445__r;
    __Vfunc_bedrock_decode_prefix_byte__445__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__446__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__446__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__446__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__446__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__446__r;
    __Vfunc_bedrock_decode_prefix_byte__446__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__447__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__447__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__447__state;
    __Vfunc_bedrock_apply_prefix_byte__447__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__447__prefix;
    __Vfunc_bedrock_apply_prefix_byte__447__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__447__r;
    __Vfunc_bedrock_apply_prefix_byte__447__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__448__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__448__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__448__state;
    __Vfunc_bedrock_apply_prefix_byte__448__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__448__prefix;
    __Vfunc_bedrock_apply_prefix_byte__448__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__448__r;
    __Vfunc_bedrock_apply_prefix_byte__448__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__452__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__452__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_bedrock_decode_prefix_word__452__prefix_word;
    __Vfunc_bedrock_decode_prefix_word__452__prefix_word = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__452____VlefCall_1__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__452____VlefCall_1__bedrock_decode_prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_word__452____VlefCall_0__bedrock_decode_prefix_byte;
    __Vfunc_bedrock_decode_prefix_word__452____VlefCall_0__bedrock_decode_prefix_byte = 0;
    QData/*42:0*/ __Vfunc_bedrock_decode_prefix_word__452__r;
    __Vfunc_bedrock_decode_prefix_word__452__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__453__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__453__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__453__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__453__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__453__r;
    __Vfunc_bedrock_decode_prefix_byte__453__r = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__454__Vfuncout;
    __Vfunc_bedrock_decode_prefix_byte__454__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_prefix_byte__454__prefix_byte;
    __Vfunc_bedrock_decode_prefix_byte__454__prefix_byte = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_prefix_byte__454__r;
    __Vfunc_bedrock_decode_prefix_byte__454__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__455__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__455__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__455__state;
    __Vfunc_bedrock_apply_prefix_byte__455__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__455__prefix;
    __Vfunc_bedrock_apply_prefix_byte__455__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__455__r;
    __Vfunc_bedrock_apply_prefix_byte__455__r = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__456__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__456__Vfuncout = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__456__state;
    __Vfunc_bedrock_apply_prefix_byte__456__state = 0;
    SData/*11:0*/ __Vfunc_bedrock_apply_prefix_byte__456__prefix;
    __Vfunc_bedrock_apply_prefix_byte__456__prefix = 0;
    QData/*42:0*/ __Vfunc_bedrock_apply_prefix_byte__456__r;
    __Vfunc_bedrock_apply_prefix_byte__456__r = 0;
    // Body
    __Vfunc_bedrock_decode_prefix_byte__429__Vfuncout 
        = vlSelfRef.__Vfunc_bedrock_decode_prefix_byte__429__r;
    __Vfunc_bedrock_decode_prefix_word__428____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__429__Vfuncout;
    vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r 
        = ((0x000004003fffffffULL & vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r) 
           | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__428____VlefCall_0__bedrock_decode_prefix_byte)) 
              << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__430__prefix_byte 
        = (0x000000ffU & ((IData)(vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__prefix_word) 
                          >> 8U));
    __Vfunc_bedrock_decode_prefix_byte__430__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__430__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__430__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__430__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r)));
                    __Vfunc_bedrock_decode_prefix_byte__430__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__430__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__430__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__430__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__430__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__430__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__430__r;
    __Vfunc_bedrock_decode_prefix_word__428____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__430__Vfuncout;
    vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r 
        = ((0x000007ffc003ffffULL & vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r) 
           | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__428____VlefCall_1__bedrock_decode_prefix_byte)) 
              << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__431__prefix 
        = (0x00000fffU & (IData)((vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r 
                                  >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__431__state = vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r;
    __Vfunc_bedrock_apply_prefix_byte__431__r = __Vfunc_bedrock_apply_prefix_byte__431__state;
    __Vfunc_bedrock_apply_prefix_byte__431__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__431__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__431__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__431__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__431__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__431__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__431__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__431__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__431__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__431__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__431__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__431__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__431__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__431__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__431__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__431__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__431__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__431__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__431__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__431__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__431__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__431__r;
    vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r 
        = __Vfunc_bedrock_apply_prefix_byte__431__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__432__prefix 
        = (0x00000fffU & (IData)((vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r 
                                  >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__432__state = vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r;
    __Vfunc_bedrock_apply_prefix_byte__432__r = __Vfunc_bedrock_apply_prefix_byte__432__state;
    __Vfunc_bedrock_apply_prefix_byte__432__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__432__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__432__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__432__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__432__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__432__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__432__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__432__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__432__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__432__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__432__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__432__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__432__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__432__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__432__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__432__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__432__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__432__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__432__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__432__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__432__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__432__r;
    vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r 
        = __Vfunc_bedrock_apply_prefix_byte__432__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__428__Vfuncout 
        = vlSelfRef.__Vfunc_bedrock_decode_prefix_word__428__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_decode__DOT__decode 
        = __Vfunc_bedrock_decode_prefix_word__428__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_valid_raw 
        = (1U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_decode__DOT__decode 
                         >> 0x0000002aU)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repeat_kind 
        = (3U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_decode__DOT__decode 
                         >> 8U)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__27__KET____DOT__prefix_decode__end_group_o 
        = (1U & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_decode__DOT__decode));
    __Vfunc_bedrock_decode_prefix_word__436__prefix_word 
        = (0x0000ffffU & (((vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                            << 0x00000010U) | (vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                               >> 0x00000010U)) 
                          & (- (IData)((1U & (vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                              >> 0x0000000fU))))));
    __Vfunc_bedrock_decode_prefix_word__436__r = 0ULL;
    __Vfunc_bedrock_decode_prefix_word__436__r = (0x0000040000000000ULL 
                                                  | __Vfunc_bedrock_decode_prefix_word__436__r);
    __Vfunc_bedrock_decode_prefix_byte__437__prefix_byte 
        = (0x000000ffU & (IData)(__Vfunc_bedrock_decode_prefix_word__436__prefix_word));
    __Vfunc_bedrock_decode_prefix_byte__437__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__437__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__437__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__437__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r)));
                    __Vfunc_bedrock_decode_prefix_byte__437__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__437__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__437__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__437__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__437__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__437__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__437__r;
    __Vfunc_bedrock_decode_prefix_word__436____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__437__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__436__r = ((0x000004003fffffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__436__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__436____VlefCall_0__bedrock_decode_prefix_byte)) 
                                                     << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__438__prefix_byte 
        = (0x000000ffU & ((IData)(__Vfunc_bedrock_decode_prefix_word__436__prefix_word) 
                          >> 8U));
    __Vfunc_bedrock_decode_prefix_byte__438__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__438__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__438__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__438__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r)));
                    __Vfunc_bedrock_decode_prefix_byte__438__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__438__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__438__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__438__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__438__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__438__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__438__r;
    __Vfunc_bedrock_decode_prefix_word__436____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__438__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__436__r = ((0x000007ffc003ffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__436__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__436____VlefCall_1__bedrock_decode_prefix_byte)) 
                                                     << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__439__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__436__r 
                                  >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__439__state = __Vfunc_bedrock_decode_prefix_word__436__r;
    __Vfunc_bedrock_apply_prefix_byte__439__r = __Vfunc_bedrock_apply_prefix_byte__439__state;
    __Vfunc_bedrock_apply_prefix_byte__439__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__439__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__439__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__439__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__439__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__439__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__439__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__439__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__439__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__439__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__439__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__439__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__439__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__439__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__439__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__439__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__439__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__439__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__439__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__439__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__439__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__439__r;
    __Vfunc_bedrock_decode_prefix_word__436__r = __Vfunc_bedrock_apply_prefix_byte__439__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__440__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__436__r 
                                  >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__440__state = __Vfunc_bedrock_decode_prefix_word__436__r;
    __Vfunc_bedrock_apply_prefix_byte__440__r = __Vfunc_bedrock_apply_prefix_byte__440__state;
    __Vfunc_bedrock_apply_prefix_byte__440__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__440__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__440__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__440__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__440__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__440__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__440__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__440__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__440__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__440__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__440__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__440__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__440__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__440__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__440__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__440__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__440__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__440__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__440__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__440__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__440__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__440__r;
    __Vfunc_bedrock_decode_prefix_word__436__r = __Vfunc_bedrock_apply_prefix_byte__440__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__436__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_word__436__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_decode__DOT__decode 
        = __Vfunc_bedrock_decode_prefix_word__436__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_valid_raw 
        = (1U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_decode__DOT__decode 
                         >> 0x0000002aU)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repeat_kind 
        = (3U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_decode__DOT__decode 
                         >> 8U)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__28__KET____DOT__prefix_decode__end_group_o 
        = (1U & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_decode__DOT__decode));
    __Vfunc_bedrock_decode_prefix_word__444__prefix_word 
        = (0x0000ffffU & (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                          & (- (IData)((vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                        >> 0x0000001fU)))));
    __Vfunc_bedrock_decode_prefix_word__444__r = 0ULL;
    __Vfunc_bedrock_decode_prefix_word__444__r = (0x0000040000000000ULL 
                                                  | __Vfunc_bedrock_decode_prefix_word__444__r);
    __Vfunc_bedrock_decode_prefix_byte__445__prefix_byte 
        = (0x000000ffU & (IData)(__Vfunc_bedrock_decode_prefix_word__444__prefix_word));
    __Vfunc_bedrock_decode_prefix_byte__445__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__445__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__445__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__445__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r)));
                    __Vfunc_bedrock_decode_prefix_byte__445__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__445__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__445__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__445__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__445__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__445__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__445__r;
    __Vfunc_bedrock_decode_prefix_word__444____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__445__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__444__r = ((0x000004003fffffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__444__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__444____VlefCall_0__bedrock_decode_prefix_byte)) 
                                                     << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__446__prefix_byte 
        = (0x000000ffU & ((IData)(__Vfunc_bedrock_decode_prefix_word__444__prefix_word) 
                          >> 8U));
    __Vfunc_bedrock_decode_prefix_byte__446__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__446__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__446__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__446__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r)));
                    __Vfunc_bedrock_decode_prefix_byte__446__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__446__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__446__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__446__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__446__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__446__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__446__r;
    __Vfunc_bedrock_decode_prefix_word__444____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__446__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__444__r = ((0x000007ffc003ffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__444__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__444____VlefCall_1__bedrock_decode_prefix_byte)) 
                                                     << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__447__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__444__r 
                                  >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__447__state = __Vfunc_bedrock_decode_prefix_word__444__r;
    __Vfunc_bedrock_apply_prefix_byte__447__r = __Vfunc_bedrock_apply_prefix_byte__447__state;
    __Vfunc_bedrock_apply_prefix_byte__447__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__447__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__447__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__447__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__447__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__447__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__447__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__447__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__447__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__447__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__447__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__447__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__447__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__447__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__447__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__447__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__447__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__447__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__447__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__447__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__447__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__447__r;
    __Vfunc_bedrock_decode_prefix_word__444__r = __Vfunc_bedrock_apply_prefix_byte__447__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__448__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__444__r 
                                  >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__448__state = __Vfunc_bedrock_decode_prefix_word__444__r;
    __Vfunc_bedrock_apply_prefix_byte__448__r = __Vfunc_bedrock_apply_prefix_byte__448__state;
    __Vfunc_bedrock_apply_prefix_byte__448__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__448__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__448__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__448__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__448__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__448__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__448__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__448__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__448__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__448__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__448__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__448__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__448__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__448__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__448__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__448__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__448__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__448__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__448__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__448__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__448__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__448__r;
    __Vfunc_bedrock_decode_prefix_word__444__r = __Vfunc_bedrock_apply_prefix_byte__448__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__444__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_word__444__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_decode__DOT__decode 
        = __Vfunc_bedrock_decode_prefix_word__444__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_valid_raw 
        = (1U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_decode__DOT__decode 
                         >> 0x0000002aU)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repeat_kind 
        = (3U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_decode__DOT__decode 
                         >> 8U)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__29__KET____DOT__prefix_decode__end_group_o 
        = (1U & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_decode__DOT__decode));
    __Vfunc_bedrock_decode_prefix_word__452__prefix_word 
        = (0x0000ffffU & (((vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                            << 0x00000010U) | (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                                               >> 0x00000010U)) 
                          & (- (IData)((1U & (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                                              >> 0x0000000fU))))));
    __Vfunc_bedrock_decode_prefix_word__452__r = 0ULL;
    __Vfunc_bedrock_decode_prefix_word__452__r = (0x0000040000000000ULL 
                                                  | __Vfunc_bedrock_decode_prefix_word__452__r);
    __Vfunc_bedrock_decode_prefix_byte__453__prefix_byte 
        = (0x000000ffU & (IData)(__Vfunc_bedrock_decode_prefix_word__452__prefix_word));
    __Vfunc_bedrock_decode_prefix_byte__453__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__453__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__453__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__453__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r)));
                    __Vfunc_bedrock_decode_prefix_byte__453__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__453__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__453__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__453__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__453__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__453__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__453__r;
    __Vfunc_bedrock_decode_prefix_word__452____VlefCall_0__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__453__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__452__r = ((0x000004003fffffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__452__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__452____VlefCall_0__bedrock_decode_prefix_byte)) 
                                                     << 0x0000001eU));
    __Vfunc_bedrock_decode_prefix_byte__454__prefix_byte 
        = (0x000000ffU & ((IData)(__Vfunc_bedrock_decode_prefix_word__452__prefix_word) 
                          >> 8U));
    __Vfunc_bedrock_decode_prefix_byte__454__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))) {
        __Vfunc_bedrock_decode_prefix_byte__454__r 
            = (0x00000e80U | (0x0000007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte)));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))) {
                    __Vfunc_bedrock_decode_prefix_byte__454__r 
                        = ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                                : ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                                    : (0x00000e00U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))))));
                } else {
                    __Vfunc_bedrock_decode_prefix_byte__454__r 
                        = (0x00000f00U | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r)));
                    __Vfunc_bedrock_decode_prefix_byte__454__r 
                        = ((0x0ff8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r)) 
                           | (7U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte)));
                }
            } else {
                __Vfunc_bedrock_decode_prefix_byte__454__r 
                    = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r));
            }
        } else {
            __Vfunc_bedrock_decode_prefix_byte__454__r 
                = (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r));
        }
    } else {
        __Vfunc_bedrock_decode_prefix_byte__454__r 
            = ((0x00000020U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                : ((0x00000010U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                    : ((8U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                        ? ((4U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                            ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                            : ((2U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                ? ((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                    ? (0x087fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))
                                    : (0x00000d80U 
                                       | (0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r))))
                                : ((0x007fU & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r)) 
                                   | (((1U & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                        ? 0x1aU : 0x19U) 
                                      << 7U)))) : (
                                                   (0x007fU 
                                                    & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__r)) 
                                                   | (((4U 
                                                        & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                        ? 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                          ? 0x18U
                                                          : 0x17U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                          ? 0x16U
                                                          : 0x15U))
                                                        : 
                                                       ((2U 
                                                         & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                         ? 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                          ? 0x14U
                                                          : 0x13U)
                                                         : 
                                                        ((1U 
                                                          & (IData)(__Vfunc_bedrock_decode_prefix_byte__454__prefix_byte))
                                                          ? 0x12U
                                                          : 0x11U))) 
                                                      << 7U)))));
    }
    __Vfunc_bedrock_decode_prefix_byte__454__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_byte__454__r;
    __Vfunc_bedrock_decode_prefix_word__452____VlefCall_1__bedrock_decode_prefix_byte 
        = __Vfunc_bedrock_decode_prefix_byte__454__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__452__r = ((0x000007ffc003ffffULL 
                                                   & __Vfunc_bedrock_decode_prefix_word__452__r) 
                                                  | ((QData)((IData)(__Vfunc_bedrock_decode_prefix_word__452____VlefCall_1__bedrock_decode_prefix_byte)) 
                                                     << 0x00000012U));
    __Vfunc_bedrock_apply_prefix_byte__455__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__452__r 
                                  >> 0x0000001eU)));
    __Vfunc_bedrock_apply_prefix_byte__455__state = __Vfunc_bedrock_decode_prefix_word__452__r;
    __Vfunc_bedrock_apply_prefix_byte__455__r = __Vfunc_bedrock_apply_prefix_byte__455__state;
    __Vfunc_bedrock_apply_prefix_byte__455__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__455__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__455__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__455__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__455__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__455__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__455__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__455__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__455__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__455__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__455__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__455__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__455__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__455__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__455__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__455__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__455__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__455__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__455__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__455__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__455__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__455__r;
    __Vfunc_bedrock_decode_prefix_word__452__r = __Vfunc_bedrock_apply_prefix_byte__455__Vfuncout;
    __Vfunc_bedrock_apply_prefix_byte__456__prefix 
        = (0x00000fffU & (IData)((__Vfunc_bedrock_decode_prefix_word__452__r 
                                  >> 0x00000012U)));
    __Vfunc_bedrock_apply_prefix_byte__456__state = __Vfunc_bedrock_decode_prefix_word__452__r;
    __Vfunc_bedrock_apply_prefix_byte__456__r = __Vfunc_bedrock_apply_prefix_byte__456__state;
    __Vfunc_bedrock_apply_prefix_byte__456__r = ((0x000003ffffffffffULL 
                                                  & __Vfunc_bedrock_apply_prefix_byte__456__r) 
                                                 | ((QData)((IData)((IData)(
                                                                            ((__Vfunc_bedrock_apply_prefix_byte__456__r 
                                                                              >> 0x0000002aU) 
                                                                             & ((IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix) 
                                                                                >> 0x0000000bU))))) 
                                                    << 0x0000002aU));
    if ((0x00000400U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))) {
        if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))) {
            if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix) 
                              >> 7U)))) {
                    __Vfunc_bedrock_apply_prefix_byte__456__r 
                        = ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__456__r) 
                           | ((QData)((IData)((0x00000100U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))))) 
                              << 1U));
                }
            } else {
                __Vfunc_bedrock_apply_prefix_byte__456__r 
                    = ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
                        ? ((0x000007fffffffc01ULL & __Vfunc_bedrock_apply_prefix_byte__456__r) 
                           | ((QData)((IData)((0x00000080U 
                                               | (0x0000007fU 
                                                  & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))))) 
                              << 1U)) : (1ULL | __Vfunc_bedrock_apply_prefix_byte__456__r));
            }
        } else {
            __Vfunc_bedrock_apply_prefix_byte__456__r 
                = ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
                    ? ((0x000007fffffff3ffULL & __Vfunc_bedrock_apply_prefix_byte__456__r) 
                       | ((QData)((IData)(((0x00000080U 
                                            & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
                                            ? 3U : 2U))) 
                          << 0x0000000aU)) : ((0x00000080U 
                                               & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
                                               ? (0x0000000000000400ULL 
                                                  | (0x000007fffffff3ffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__456__r))
                                               : (0x0000000000004000ULL 
                                                  | (0x000007ffffff8fffULL 
                                                     & __Vfunc_bedrock_apply_prefix_byte__456__r))));
        }
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__456__r = 
            ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
              ? ((0x000007ffffff8fffULL & __Vfunc_bedrock_apply_prefix_byte__456__r) 
                 | ((QData)((IData)(((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
                                      ? 3U : 2U))) 
                    << 0x0000000cU)) : ((0x00000080U 
                                         & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
                                         ? (0x0000000000001000ULL 
                                            | (0x000007ffffff8fffULL 
                                               & __Vfunc_bedrock_apply_prefix_byte__456__r))
                                         : (0x0000000000008000ULL 
                                            | __Vfunc_bedrock_apply_prefix_byte__456__r)));
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))) {
        __Vfunc_bedrock_apply_prefix_byte__456__r = 
            ((0x00000080U & (IData)(__Vfunc_bedrock_apply_prefix_byte__456__prefix))
              ? (0x0000000000010000ULL | __Vfunc_bedrock_apply_prefix_byte__456__r)
              : (0x0000000000020000ULL | __Vfunc_bedrock_apply_prefix_byte__456__r));
    }
    __Vfunc_bedrock_apply_prefix_byte__456__Vfuncout 
        = __Vfunc_bedrock_apply_prefix_byte__456__r;
    __Vfunc_bedrock_decode_prefix_word__452__r = __Vfunc_bedrock_apply_prefix_byte__456__Vfuncout;
    __Vfunc_bedrock_decode_prefix_word__452__Vfuncout 
        = __Vfunc_bedrock_decode_prefix_word__452__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_decode__DOT__decode 
        = __Vfunc_bedrock_decode_prefix_word__452__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_valid_raw 
        = (1U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_decode__DOT__decode 
                         >> 0x0000002aU)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repeat_kind 
        = (3U & (IData)((entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_decode__DOT__decode 
                         >> 8U)));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT____Vcellout__gen_entry__BRA__30__KET____DOT__prefix_decode__end_group_o 
        = (1U & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_decode__DOT__decode));
    __Vfunc_bedrock_decode_primary_payload__217__payload 
        = (0x00000fffU & vlSelfRef.entry_precheck_tb__DOT__line_words[0U]);
    __Vfunc_bedrock_decode_primary_payload__217__r = 0U;
    __Vfunc_bedrock_decode_primary_payload__217__r 
        = (0x00000020U | (0x03000000U & __Vfunc_bedrock_decode_primary_payload__217__r));
    if ((0x00000800U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                        if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                            if ((2U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                                if (
                                                    (1U 
                                                     & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                                        = 
                                                        (0x02000000U 
                                                         | __Vfunc_bedrock_decode_primary_payload__217__r);
                                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                                        = 
                                                        (0x006f0200U 
                                                         | (0x030001ffU 
                                                            & __Vfunc_bedrock_decode_primary_payload__217__r));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__217__payload) 
                                      >> 5U)))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__217__payload) 
                                              >> 3U)))) {
                                    if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                            if ((1U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__217__r);
                                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                                    = 
                                                    (0x0000000aU 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__217__r));
                                            } else {
                                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__217__r);
                                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                                    = 
                                                    (8U 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__217__r));
                                            }
                                        } else if (
                                                   (1U 
                                                    & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__217__r);
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (9U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__217__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__217__r);
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x00000016U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__217__r));
                                        }
                                    } else if ((2U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__217__r);
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x00000014U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__217__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__217__r);
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x00000015U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__217__r));
                                        }
                                    } else if ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__217__r);
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (2U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__217__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__217__r);
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (1U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__217__r));
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (3U | (0x03ffffe0U 
                                             & __Vfunc_bedrock_decode_primary_payload__217__r));
                            }
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__217__payload) 
                                                  >> 1U)))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__217__r);
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (4U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__217__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__217__r);
                                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                                = (7U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__217__r));
                                        }
                                    }
                                } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__217__r);
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (6U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__217__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__217__r);
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (5U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__217__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__217__r);
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x0000000fU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__217__r);
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x0000000eU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                                }
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__217__r);
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x0000000dU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__217__r);
                                        __Vfunc_bedrock_decode_primary_payload__217__r 
                                            = (0x0000000cU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__217__r);
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x00000012U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__217__r);
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x00000013U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                                }
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__217__r);
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x00000011U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__217__r);
                                    __Vfunc_bedrock_decode_primary_payload__217__r 
                                        = (0x00000010U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                                }
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x0000000bU 
                                       | (0x03ffffe0U 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00bf0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x008504a0U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00160800U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        }
                    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00160400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00950400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        }
                    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x00950800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x009b0400U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                    }
                } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00cf1c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00931c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            }
                        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00cd0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__217__r);
                                __Vfunc_bedrock_decode_primary_payload__217__r 
                                    = (0x00791040U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00cc0240U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                            __Vfunc_bedrock_decode_primary_payload__217__r 
                                = (0x00791040U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__217__r));
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x00921800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                        __Vfunc_bedrock_decode_primary_payload__217__r 
                            = (0x00901800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__217__r));
                    }
                } else {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x00294200U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                }
            } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x00cf4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x00bd4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                }
            } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00b64600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00934600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
        }
    } else if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00194600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00054600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
            }
        } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x00711800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x001f1800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
        }
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x00011800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                    __Vfunc_bedrock_decode_primary_payload__217__r 
                        = (0x00701800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__217__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
        }
    } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x00034600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x00281a00U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x001e1800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x00051c40U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x009b0800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00880240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
                __Vfunc_bedrock_decode_primary_payload__217__r 
                    = (0x00870240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
            }
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x00970240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x009c0240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x00a80200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
            __Vfunc_bedrock_decode_primary_payload__217__r 
                = (0x001302a0U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
        }
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__217__payload))) {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x00130260U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__217__r));
    } else {
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__217__r);
        __Vfunc_bedrock_decode_primary_payload__217__r 
            = (0x006e0200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__217__r));
    }
    __Vfunc_bedrock_decode_primary_payload__217__Vfuncout 
        = __Vfunc_bedrock_decode_primary_payload__217__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode 
        = __Vfunc_bedrock_decode_primary_payload__217__Vfuncout;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode = 0U;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode 
        = (0x0008000fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode);
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw 
        = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode 
                 >> 0x00000019U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__opcode_id 
        = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode 
                          >> 0x00000010U));
    if ((0x01000000U & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode)) {
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word 
            = (0x0000ffffU & ((0x00008000U & vlSelfRef.entry_precheck_tb__DOT__line_words[0U])
                               ? vlSelfRef.entry_precheck_tb__DOT__line_words[1U]
                               : ((vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                                   << 0x00000010U) 
                                  | (vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                                     >> 0x00000010U))));
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root 
            = (0x0000001fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__primary_decode);
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
            = (2U | (0x00080000U & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root)))) {
                            if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = (0x00092860U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                            }
                            if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                                if ((0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                                    if (VL_UNLIKELY((
                                                     vlSymsp->_vm_contextp__->assertOn()))) {
                                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2660: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2660, "");
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                        if (((((((((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                   | (1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                  | (2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                 | (8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                                | (0x0010U == (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                               | (0x0040U == (0xffc0U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                              | (0x0080U == (0xffc0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                             | (0x00c0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = ((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? (0x000bb010U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                    : ((1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x000b90a3U
                                        : ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x8401U
                                                : (
                                                   (8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                    ? 0xdc05U
                                                    : 
                                                   ((0x0010U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                     ? 0xd185U
                                                     : 
                                                    ((0x0040U 
                                                      == 
                                                      (0xffc0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                      ? 0xba86U
                                                      : 
                                                     ((0x0080U 
                                                       == 
                                                       (0xffc0U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                       ? 0xdc8fU
                                                       : 0xb986U))))) 
                                              << 4U))));
                        } else if ((0x0100U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000e2860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x0140U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000a8060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x0180U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000ba060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x01c0U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000dd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x0200U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000cc860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x0240U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000cd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x0280U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000e1060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (((((0x0280U 
                                                        == 
                                                        (0xffc0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                       << 3U) 
                                                      | ((0x0240U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                         << 2U)) 
                                                     | (((0x0200U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                         << 1U) 
                                                        | (0x01c0U 
                                                           == 
                                                           (0xffc0U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                                    << 0x0000000bU) 
                                                   | (((((0x0180U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0140U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0100U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                           << 1U) 
                                                          | (0x00c0U 
                                                             == 
                                                             (0xffc0U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                                      << 7U)) 
                                                  | ((((((0x0080U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0040U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0010U 
                                                            == 
                                                            (0xfff8U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                           << 1U) 
                                                          | (8U 
                                                             == 
                                                             (0xfff8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                                      << 3U) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                                         << 2U) 
                                                        | (((1U 
                                                             == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                                            << 1U) 
                                                           | (0U 
                                                              == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))))) {
                            if ((0U != (((((((0x0280U 
                                              == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                             << 3U) 
                                            | ((0x0240U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 2U)) 
                                           | (((0x0200U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 1U) 
                                              | (0x01c0U 
                                                 == 
                                                 (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                          << 0x0000000bU) 
                                         | (((((0x0180U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 3U) 
                                              | ((0x0140U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0100U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 1U) 
                                                | (0x00c0U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                            << 7U)) 
                                        | ((((((0x0080U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 3U) 
                                              | ((0x0040U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 1U) 
                                                | (8U 
                                                   == 
                                                   (0xfff8U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                            << 3U) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                               << 2U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                                  << 1U) 
                                                 | (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2578: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2578, "");
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                         >> 0x0000000fU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                      >> 0x0000000eU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                          >> 0x0000000dU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                              >> 0x0000000cU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                  >> 0x0000000bU)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                    >> 0x0000000aU)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                     >> 9U)))) {
                                                if (
                                                    (0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                             >> 7U)))) {
                                                        if (
                                                            (0x00000040U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                                     >> 5U)))) {
                                                                if (
                                                                    (0x00000010U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                                                    if (
                                                                        (8U 
                                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                                            = 
                                                                            (0x000e4050U 
                                                                             | (0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                                                    } else if (
                                                                               (1U 
                                                                                & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                                                >> 2U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                                                >> 1U)))) {
                                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                                                = 
                                                                                ((0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                                                                | (((1U 
                                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                                 ? 0xe801U
                                                                                 : 0xe201U) 
                                                                                << 4U));
                                                                        }
                                                                    }
                                                                } else {
                                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                                        = 
                                                                        ((8U 
                                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                          ? 0x000d1133U
                                                                          : 
                                                                         (0x000d0850U 
                                                                          | (0x0000000fU 
                                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r)));
                                                                }
                                                            }
                                                        } else {
                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                                = 
                                                                (0x000d3860U 
                                                                 | (0x0000000fU 
                                                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                                        }
                                                    }
                                                } else {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                        = 
                                                        ((0x00000080U 
                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                          ? 
                                                         ((0x0000000fU 
                                                           & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                                          | (((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                               ? 0xd786U
                                                               : 0xe491U) 
                                                             << 4U))
                                                          : 
                                                         ((0x00000040U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                           ? 
                                                          (0x000d21c0U 
                                                           | (0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                                           : 
                                                          ((0x00000020U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                            ? 
                                                           ((0x0000000fU 
                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                                            | (((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                  ? 0x8d85U
                                                                  : 
                                                                 ((4U 
                                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                   ? 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                     ? 0xe181U
                                                                     : 0xde01U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                     ? 0xdd81U
                                                                     : 0xd581U))
                                                                   : 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                     ? 0xd301U
                                                                     : 0xc881U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                     ? 0xbb81U
                                                                     : 0x8201U))))
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                  ? 0xe505U
                                                                  : 0xd285U)) 
                                                               << 4U))
                                                            : 
                                                           ((0x00000010U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                             ? 
                                                            ((0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                                             | (((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                                  ? 0xe385U
                                                                  : 0xd005U) 
                                                                << 4U))
                                                             : 
                                                            ((8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                              ? 0x000e3123U
                                                              : 0x000cf923U)))));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                    if ((0x00001000U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                    >> 0x0000000bU)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                = (0x000c7ab0U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                            = ((0x0000000fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                               | (((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc7abU
                                                    : 0xc72bU) 
                                                  << 4U));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                        = ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                           | (((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc72bU
                                                    : 0xc6abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc6abU
                                                    : 0xc62bU)) 
                                              << 4U));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                       | (((0x00002000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc62bU
                                                    : 0xc5abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc5abU
                                                    : 0xc22bU))
                                            : ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc22bU
                                                    : 0xc1abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xc1abU
                                                    : 0x91abU))) 
                                          << 4U));
                            }
                        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x00090ba0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0x91abU
                                            : 0x912bU) 
                                          << 4U));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = (0x000912b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                 >> 0x0000000aU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                         >> 5U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                             >> 4U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                                 >> 3U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                                     >> 2U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000903b3U;
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
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x8aabU : 0x8a2bU) 
                                      << 4U));
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000bf3a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000c53a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x4000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))) {
                            if ((0U != (((0x4000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                         << 1U) | (0U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2306: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2306, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00086ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000873a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00087ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000883a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2280: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2280, "");
                            }
                        }
                    }
                } else {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00084ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000853a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00085ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000863a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2254: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2254, "");
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000da2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000daae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000d72e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x8000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 2U) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                            if ((0U != (((0x8000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                         << 2U) | (
                                                   ((0x4000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xc000U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2233: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2233, "");
                                }
                            }
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000ceae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000cf2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000d62e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0xc000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000d6ae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   ((0xc000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                    << 3U) 
                                                   | ((0x8000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                      << 2U)) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                            if ((0U != ((((0xc000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                          << 3U) | 
                                         ((0x8000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                          << 2U)) | 
                                        (((0x4000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                          << 1U) | 
                                         (0U == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2207: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2207, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000832e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00083ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00088ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000892e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2181: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2181, "");
                            }
                        }
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                      >> 0x0000000dU)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xdaabU
                                            : 0xda2bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xd72bU
                                            : 0xd6abU)) 
                                      << 4U));
                        }
                    }
                } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = (0x000d62b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                  >> 8U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                            = (0x000daa60U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                       | (((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0xda26U
                                                : 0xd726U)
                                            : ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0xd6a6U
                                                : 0xd626U)) 
                                          << 4U));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000d4ab0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0xcf2bU : 0xceabU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0xcb2bU : 0x8eabU)) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x8e2bU : 0x8c2bU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x8babU : 0x892bU))
                                : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x88abU : 0x83abU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x832bU : 
                                       ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                         ? ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                 ? 0xd4a6U
                                                 : 0xcf26U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                 ? 0xcea6U
                                                 : 0xca15U))
                                         : ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                 ? 0x8926U
                                                 : 0x88a6U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                 ? 0x83a6U
                                                 : 0x8326U)))))) 
                              << 4U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                   | (((0x00002000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xe7abU
                                            : 0xdeabU)
                                        : ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xdb2bU
                                            : 0xd82bU)) 
                                      << 4U));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = (0x000d52b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                            = (0x000db140U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                    } else if ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                         >> 5U)))) {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000dba43U;
                                                }
                                            }
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                            = (0x000d5260U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = (0x000c9ab0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xc9abU
                                            : 0xc12bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xc12bU
                                            : 0xc0abU)) 
                                      << 4U));
                        }
                    } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                               | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xc0abU
                                            : 0xc02bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xc02bU
                                            : 0xbfabU))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xbfabU
                                            : 0x952aU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0x952aU
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0xc915U
                                                     : 0xc815U)
                                                    : 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0xb895U
                                                     : 0xb815U))
                                                : 0x94a9U)))) 
                                  << 4U));
                    } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000400U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0x94a9U
                                            : 0x9416U)
                                        : 0x93aaU) : 
                                   ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                     ? 0x93aaU : 0x9329U)) 
                                  << 4U));
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x0008cab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00082ab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00000100U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0x8f95U : 0x8f15U)
                                    : 0x8c94U) << 4U));
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00081940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x00093250U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x0008b060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000db9f3U;
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                          >> 3U)))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000e7b53U;
                                        }
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x000deb53U
                                                : 0x000db353U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x000d8353U
                                                : 0x000c9b53U));
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x00095983U
                                                : 0x00095313U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x00094b03U
                                                : 0x00094183U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x00093b13U
                                                : 0x00093303U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x0008cb53U
                                                : 0x0008cb23U)))
                                    : ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x00082b53U
                                                : 0x00082af3U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x00081b53U
                                                : 0x00081af3U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? 0x00081af3U
                                                : 0x00081353U)
                                            : 0x000812f3U)));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x00080950U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                      >> 0x0000000dU)))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                              >> 0x0000000bU)))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                        = (0x000b5b40U 
                                           | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xb434U
                                            : 0xb3b4U) 
                                          << 4U));
                            }
                        }
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                           | (((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xb334U
                                            : 0xb1b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xb134U
                                            : 0xb0b4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xa7b4U
                                            : 0xa734U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xa6b4U
                                            : 0xa634U)))
                                : ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0xa334U
                                            : 0xa2b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0x9e34U
                                            : 0x9db4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0x98b4U
                                            : 0x9834U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? 0x97b4U
                                            : 0x96b4U)))) 
                              << 4U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                if (((((((((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                           | (0x0800U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                          | (0x0840U == (0xffe0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                         | (0x0900U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                        | (0x0a00U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                       | (0x0c00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                      | (0x0d00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                     | (0x0e00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                            ? (0x0009cb40U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                            : ((0x0800U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                ? (0x000b49a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                : ((0x0840U == (0xffe0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                    ? 0x000ab9b3U : 
                                   ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                                    | (((0x0900U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                         ? 0x9e90U : 
                                        ((0x0a00U == 
                                          (0xfe00U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                          ? 0x9ba7U
                                          : ((0x0c00U 
                                              == (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                              ? 0x9e90U
                                              : 0x9f10U))) 
                                       << 4U)))));
                } else if ((0x1000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x0009cad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x2000U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000b4970U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x2400U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x0009e990U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x2800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000aab40U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x3000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x4000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x5000U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x0009f190U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                }
                if ((1U & (~ VL_ONEHOT_I((((((((0x5000U 
                                                == 
                                                (0xfc00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 3U) 
                                              | ((0x4000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 2U)) 
                                             | (((0x3000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 1U) 
                                                | (0x2800U 
                                                   == 
                                                   (0xf800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                            << 0x0000000bU) 
                                           | (((((0x2400U 
                                                  == 
                                                  (0xfc00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 3U) 
                                                | ((0x2000U 
                                                    == 
                                                    (0xff80U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 2U)) 
                                               | (((0x1000U 
                                                    == 
                                                    (0xf000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 1U) 
                                                  | (0x0e00U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                              << 7U)) 
                                          | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))))) {
                    if ((0U != (((((((0x5000U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                     << 3U) | ((0x4000U 
                                                == 
                                                (0xf000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 2U)) 
                                   | (((0x3000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                       << 1U) | (0x2800U 
                                                 == 
                                                 (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                  << 0x0000000bU) | 
                                 (((((0x2400U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                     << 3U) | ((0x2000U 
                                                == 
                                                (0xff80U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 2U)) 
                                   | (((0x1000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                       << 1U) | (0x0e00U 
                                                 == 
                                                 (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                  << 7U)) | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1463: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1463, "");
                        }
                    }
                }
            } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                          >> 0x0000000bU)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                    = (0x000b5340U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                = (0x000b52d0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? 0xb52dU : 0xb2adU) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? 0xb2b4U : 0xb234U)
                                    : 0xb22dU) : ((0x00001000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                   ? 0xb22dU
                                                   : 
                                                  ((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0xb034U
                                                    : 0xafb4U))) 
                              << 4U));
                }
            } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                       | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                            ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? 0xaf34U : 0xad34U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? 0xacb4U : 0xaa34U))
                            : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? 0xa9b4U : 0xa934U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? 0xa5b4U : 0xa534U))) 
                          << 4U));
            } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                       | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                            ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? 0xa4b4U : 0xa434U)
                            : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? 0xa3b4U : 0x9fb4U)) 
                          << 4U));
            } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r) 
                       | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                            ? 0x9b34U : 0x9734U) << 4U));
            } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                    = (0x00096340U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
            } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                    = (0x000b6190U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                 >> 9U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                              >> 8U)))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                      >> 6U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                          >> 5U)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                              >> 4U)))) {
                                    if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                        if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word) 
                                                     >> 1U)))) {
                                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                    = 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                      ? 0x000b0333U
                                                      : 0x000afb33U);
                                            }
                                        } else {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                                = (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000afb33U
                                                     : 0x000af333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 
                                                    (0x000ae810U 
                                                     | (0x0000000fU 
                                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                                     : 0x000ae3d3U));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                                            = ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 0x000ae3c4U
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000adbd3U
                                                     : 0x000adbc4U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000adbc4U
                                                     : 0x000ad333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000ad333U
                                                     : 0x000acb33U)));
                                    }
                                }
                            }
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                ? (0x0009c060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                : ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                    ? (0x0009c070U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                    : ((0x00000010U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                        ? ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000ac3d3U
                                                     : 0x000ac3c4U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000ac3c4U
                                                     : 0x000aa333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a9b33U
                                                     : 0x000a9333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a8bd3U
                                                     : 0x000a8bc4U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a8bc4U
                                                     : 0x000a5b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a5b33U
                                                     : 0x000a5333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a5333U
                                                     : 0x000a4b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a4333U
                                                     : 0x000a3b33U))))
                                        : ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000a3b33U
                                                     : 0x0009fb33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x0009d3d3U
                                                     : 0x0009b333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x0009b333U
                                                     : 0x0009abd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x0009abc4U
                                                     : 0x0009a3d3U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x0009a3c4U
                                                     : 0x00099bd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x00099bc4U
                                                     : 0x000993d3U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))
                                                     ? 0x000993c4U
                                                     : 0x00097333U)
                                                    : 0x00096333U))))));
                    }
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000bd940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x0200U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000d8940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    } else if ((0x0400U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = (0x000df060U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I((((0x0400U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 2U) 
                                              | (((0x0200U 
                                                   == 
                                                   (0xfe00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                        if ((0U != (((0x0400U == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                     << 2U) | (((0x0200U 
                                                 == 
                                                 (0xfe00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                << 1U) 
                                               | (0U 
                                                  == 
                                                  (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1021: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1021, "");
                            }
                        }
                    }
                } else {
                    if (((((((((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                               | (8U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                              | (0x0010U == (0xfff0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                             | (0x0020U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                            | (0x0030U == (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                           | (0x0040U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                          | (0x0050U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) 
                         | (0x0100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                            = ((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                ? (0x000b6850U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                : ((8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                    ? (0x000d9050U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                    : ((0x0010U == 
                                        (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                        ? 0x000c38b3U
                                        : ((0x0020U 
                                            == (0xfff0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                            ? 0x000c40b3U
                                            : ((0x0030U 
                                                == 
                                                (0xfff0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                ? (0x000d9030U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r))
                                                : (
                                                   (0x0040U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                    ? 0x000e60b3U
                                                    : 
                                                   ((0x0050U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))
                                                     ? 0x000e68b3U
                                                     : 0x000c4a03U)))))));
                    } else if ((0x0200U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000e7203U;
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((((0x0200U 
                                                   == 
                                                   (0xff00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                  << 4U) 
                                                 | (((0x0100U 
                                                      == 
                                                      (0xff00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                     << 3U) 
                                                    | ((0x0050U 
                                                        == 
                                                        (0xfff0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                       << 2U))) 
                                                | (((0x0040U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                    << 1U) 
                                                   | (0x0030U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                               << 4U) 
                                              | ((((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0010U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                     << 2U)) 
                                                 | (((8U 
                                                      == 
                                                      (0xfff8U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                     << 1U) 
                                                    | (0U 
                                                       == 
                                                       (0xfff8U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))))) {
                        if ((0U != ((((((0x0200U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                        << 4U) | ((
                                                   (0x0100U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0050U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                     << 2U))) 
                                      | (((0x0040U 
                                           == (0xfff0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                          << 1U) | 
                                         (0x0030U == 
                                          (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))) 
                                     << 4U) | ((((0x0020U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 3U) 
                                                | ((0x0010U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 2U)) 
                                               | (((8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:964: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 964, "");
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                if ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x1000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x4000U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c2ac0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x4000U 
                                             == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                            << 4U) 
                                           | (((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 3U) 
                                              | ((0x1000U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                 << 2U))) 
                                          | (((0x0800U 
                                               == (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                    if ((0U != ((((0x4000U == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                  << 4U) | (((0x1800U 
                                              == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                             << 3U) 
                                            | ((0x1000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                               << 2U))) 
                                | (((0x0800U == (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                    << 1U) | (0U == 
                                              (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:933: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 933, "");
                        }
                    }
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x00089860U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000be810U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x0200U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000bd160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000be160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x0400U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                            << 3U) 
                                           | ((0x0200U 
                                               == (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                              << 2U)) 
                                          | (((0x0040U 
                                               == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))))) {
                    if ((0U != ((((0x0400U == (0xfe00U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                  << 3U) | ((0x0200U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                            << 2U)) 
                                | (((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                                    << 1U) | (0U == 
                                              (0xffc0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:907: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 907, "");
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
                if ((0x07ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000923f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x0800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x0bffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000ab380U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000bc9d0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000bc370U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000e0010U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000e0890U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x0d00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x0dffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000d9b60U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x1000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x17ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x1800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x1fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x2000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x27ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                } else if (((0x2800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)) 
                            & (0x2fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r 
                        = (0x000cc060U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r));
                }
                if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                    if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:839: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 839, "");
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__ext_root))) {
            if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x0008d403U;
            } else if ((0x4000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000a0393U;
            } else if ((0x4800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000a0b93U;
            } else if ((0x5000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000a1393U;
            } else if ((0x5800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000a1b93U;
            } else if ((0x6000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r = 0x000a2393U;
            }
            if ((1U & (~ VL_ONEHOT_I(((((0x6000U == 
                                         (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                        << 5U) | ((
                                                   (0x5800U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 4U) 
                                                  | ((0x5000U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                     << 3U))) 
                                      | (((0x4800U 
                                           == (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                          << 2U) | 
                                         (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))))) {
                if ((0U != ((((0x6000U == (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                              << 5U) | (((0x5800U == 
                                          (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                         << 4U) | (
                                                   (0x5000U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                                   << 3U))) 
                            | (((0x4800U == (0xf800U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                << 2U) | (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word)))))))) {
                    if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:797: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__extension_word));
                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 797, "");
                    }
                }
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__r;
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__218__Vfuncout;
        vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw 
            = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode 
                     >> 0x00000013U));
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__opcode_id 
            = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__extended_decode 
                              >> 0x0000000bU));
    }
    __Vfunc_bedrock_decode_opcode_attributes__219__opcode_id 
        = entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__219__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                              >> 4U)))) {
                    if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                                    __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                                         >> 2U)))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                                    = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                                      >> 1U)))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
                            }
                        }
                    }
                } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                                     >> 1U)))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    }
                }
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    }
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    }
                } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__219__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
            } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                          >> 1U)))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        }
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                        }
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                                     >> 2U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                                  >> 1U)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                        }
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__219__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))))
                        : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                    } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__219__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)))
                            : 7U);
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id) 
                              >> 1U)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__219__r 
                        = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            }
        }
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                    ? ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? 7U : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                                     ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))))
                        : ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)))))
                    : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                    ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                        ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r))
                            : 7U) : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)))
                    : 7U);
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        }
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__219__r 
                        = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__219__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            }
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__219__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        }
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        }
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__219__r = 7U;
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__219__r 
            = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))
                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r)));
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__219__r 
            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__219__r));
    }
    __Vfunc_bedrock_decode_opcode_attributes__219__Vfuncout 
        = __Vfunc_bedrock_decode_opcode_attributes__219__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__attributes 
        = __Vfunc_bedrock_decode_opcode_attributes__219__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repcc_allowed_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__attributes) 
              >> 2U));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repg_allowed_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__attributes) 
              >> 1U));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repg_fast_candidate_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw) 
           & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode__DOT__attributes));
    __Vfunc_bedrock_decode_primary_payload__225__payload 
        = (0x00000fffU & (vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                          >> 0x00000010U));
    __Vfunc_bedrock_decode_primary_payload__225__r = 0U;
    __Vfunc_bedrock_decode_primary_payload__225__r 
        = (0x00000020U | (0x03000000U & __Vfunc_bedrock_decode_primary_payload__225__r));
    if ((0x00000800U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                        if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                            if ((2U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                                if (
                                                    (1U 
                                                     & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                                        = 
                                                        (0x02000000U 
                                                         | __Vfunc_bedrock_decode_primary_payload__225__r);
                                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                                        = 
                                                        (0x006f0200U 
                                                         | (0x030001ffU 
                                                            & __Vfunc_bedrock_decode_primary_payload__225__r));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__225__payload) 
                                      >> 5U)))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__225__payload) 
                                              >> 3U)))) {
                                    if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                            if ((1U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__225__r);
                                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                                    = 
                                                    (0x0000000aU 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__225__r));
                                            } else {
                                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__225__r);
                                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                                    = 
                                                    (8U 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__225__r));
                                            }
                                        } else if (
                                                   (1U 
                                                    & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__225__r);
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (9U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__225__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__225__r);
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x00000016U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__225__r));
                                        }
                                    } else if ((2U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__225__r);
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x00000014U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__225__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__225__r);
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x00000015U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__225__r));
                                        }
                                    } else if ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__225__r);
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (2U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__225__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__225__r);
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (1U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__225__r));
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (3U | (0x03ffffe0U 
                                             & __Vfunc_bedrock_decode_primary_payload__225__r));
                            }
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__225__payload) 
                                                  >> 1U)))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__225__r);
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (4U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__225__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__225__r);
                                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                                = (7U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__225__r));
                                        }
                                    }
                                } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__225__r);
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (6U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__225__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__225__r);
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (5U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__225__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__225__r);
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x0000000fU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__225__r);
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x0000000eU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                                }
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__225__r);
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x0000000dU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__225__r);
                                        __Vfunc_bedrock_decode_primary_payload__225__r 
                                            = (0x0000000cU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__225__r);
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x00000012U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__225__r);
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x00000013U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                                }
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__225__r);
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x00000011U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__225__r);
                                    __Vfunc_bedrock_decode_primary_payload__225__r 
                                        = (0x00000010U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                                }
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x0000000bU 
                                       | (0x03ffffe0U 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00bf0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x008504a0U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00160800U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        }
                    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00160400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00950400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        }
                    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x00950800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x009b0400U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                    }
                } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00cf1c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00931c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            }
                        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00cd0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__225__r);
                                __Vfunc_bedrock_decode_primary_payload__225__r 
                                    = (0x00791040U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00cc0240U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                            __Vfunc_bedrock_decode_primary_payload__225__r 
                                = (0x00791040U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__225__r));
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x00921800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                        __Vfunc_bedrock_decode_primary_payload__225__r 
                            = (0x00901800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__225__r));
                    }
                } else {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x00294200U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                }
            } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x00cf4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x00bd4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                }
            } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00b64600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00934600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
        }
    } else if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00194600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00054600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
            }
        } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x00711800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x001f1800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
        }
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x00011800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                    __Vfunc_bedrock_decode_primary_payload__225__r 
                        = (0x00701800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__225__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
        }
    } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x00034600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x00281a00U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x001e1800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x00051c40U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x009b0800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00880240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
                __Vfunc_bedrock_decode_primary_payload__225__r 
                    = (0x00870240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
            }
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x00970240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x009c0240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x00a80200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
            __Vfunc_bedrock_decode_primary_payload__225__r 
                = (0x001302a0U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
        }
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__225__payload))) {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x00130260U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__225__r));
    } else {
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__225__r);
        __Vfunc_bedrock_decode_primary_payload__225__r 
            = (0x006e0200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__225__r));
    }
    __Vfunc_bedrock_decode_primary_payload__225__Vfuncout 
        = __Vfunc_bedrock_decode_primary_payload__225__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode 
        = __Vfunc_bedrock_decode_primary_payload__225__Vfuncout;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode = 0U;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode 
        = (0x0008000fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode);
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw 
        = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode 
                 >> 0x00000019U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__opcode_id 
        = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode 
                          >> 0x00000010U));
    if ((0x01000000U & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode)) {
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word 
            = (0x0000ffffU & ((vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                               >> 0x0000001fU) ? ((vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                                   << 0x00000010U) 
                                                  | (vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                                     >> 0x00000010U))
                               : vlSelfRef.entry_precheck_tb__DOT__line_words[1U]));
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root 
            = (0x0000001fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__primary_decode);
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
            = (2U | (0x00080000U & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root)))) {
                            if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = (0x00092860U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                            }
                            if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                                if ((0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                                    if (VL_UNLIKELY((
                                                     vlSymsp->_vm_contextp__->assertOn()))) {
                                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2660: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2660, "");
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                        if (((((((((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                   | (1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                  | (2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                 | (8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                                | (0x0010U == (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                               | (0x0040U == (0xffc0U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                              | (0x0080U == (0xffc0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                             | (0x00c0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = ((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? (0x000bb010U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                    : ((1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x000b90a3U
                                        : ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x8401U
                                                : (
                                                   (8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                    ? 0xdc05U
                                                    : 
                                                   ((0x0010U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                     ? 0xd185U
                                                     : 
                                                    ((0x0040U 
                                                      == 
                                                      (0xffc0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                      ? 0xba86U
                                                      : 
                                                     ((0x0080U 
                                                       == 
                                                       (0xffc0U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                       ? 0xdc8fU
                                                       : 0xb986U))))) 
                                              << 4U))));
                        } else if ((0x0100U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000e2860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x0140U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000a8060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x0180U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000ba060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x01c0U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000dd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x0200U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000cc860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x0240U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000cd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x0280U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000e1060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (((((0x0280U 
                                                        == 
                                                        (0xffc0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                       << 3U) 
                                                      | ((0x0240U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                         << 2U)) 
                                                     | (((0x0200U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                         << 1U) 
                                                        | (0x01c0U 
                                                           == 
                                                           (0xffc0U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                                    << 0x0000000bU) 
                                                   | (((((0x0180U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0140U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0100U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                           << 1U) 
                                                          | (0x00c0U 
                                                             == 
                                                             (0xffc0U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                                      << 7U)) 
                                                  | ((((((0x0080U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0040U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0010U 
                                                            == 
                                                            (0xfff8U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                           << 1U) 
                                                          | (8U 
                                                             == 
                                                             (0xfff8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                                      << 3U) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                                         << 2U) 
                                                        | (((1U 
                                                             == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                                            << 1U) 
                                                           | (0U 
                                                              == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))))) {
                            if ((0U != (((((((0x0280U 
                                              == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                             << 3U) 
                                            | ((0x0240U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 2U)) 
                                           | (((0x0200U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 1U) 
                                              | (0x01c0U 
                                                 == 
                                                 (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                          << 0x0000000bU) 
                                         | (((((0x0180U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 3U) 
                                              | ((0x0140U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0100U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 1U) 
                                                | (0x00c0U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                            << 7U)) 
                                        | ((((((0x0080U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 3U) 
                                              | ((0x0040U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 1U) 
                                                | (8U 
                                                   == 
                                                   (0xfff8U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                            << 3U) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                               << 2U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                                  << 1U) 
                                                 | (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2578: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2578, "");
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                         >> 0x0000000fU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                      >> 0x0000000eU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                          >> 0x0000000dU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                              >> 0x0000000cU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                  >> 0x0000000bU)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                    >> 0x0000000aU)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                     >> 9U)))) {
                                                if (
                                                    (0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                             >> 7U)))) {
                                                        if (
                                                            (0x00000040U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                                     >> 5U)))) {
                                                                if (
                                                                    (0x00000010U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                                                    if (
                                                                        (8U 
                                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                                            = 
                                                                            (0x000e4050U 
                                                                             | (0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                                                    } else if (
                                                                               (1U 
                                                                                & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                                                >> 2U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                                                >> 1U)))) {
                                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                                                = 
                                                                                ((0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                                                                | (((1U 
                                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                                 ? 0xe801U
                                                                                 : 0xe201U) 
                                                                                << 4U));
                                                                        }
                                                                    }
                                                                } else {
                                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                                        = 
                                                                        ((8U 
                                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                          ? 0x000d1133U
                                                                          : 
                                                                         (0x000d0850U 
                                                                          | (0x0000000fU 
                                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r)));
                                                                }
                                                            }
                                                        } else {
                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                                = 
                                                                (0x000d3860U 
                                                                 | (0x0000000fU 
                                                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                                        }
                                                    }
                                                } else {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                        = 
                                                        ((0x00000080U 
                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                          ? 
                                                         ((0x0000000fU 
                                                           & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                                          | (((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                               ? 0xd786U
                                                               : 0xe491U) 
                                                             << 4U))
                                                          : 
                                                         ((0x00000040U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                           ? 
                                                          (0x000d21c0U 
                                                           | (0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                                           : 
                                                          ((0x00000020U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                            ? 
                                                           ((0x0000000fU 
                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                                            | (((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                  ? 0x8d85U
                                                                  : 
                                                                 ((4U 
                                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                   ? 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                     ? 0xe181U
                                                                     : 0xde01U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                     ? 0xdd81U
                                                                     : 0xd581U))
                                                                   : 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                     ? 0xd301U
                                                                     : 0xc881U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                     ? 0xbb81U
                                                                     : 0x8201U))))
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                  ? 0xe505U
                                                                  : 0xd285U)) 
                                                               << 4U))
                                                            : 
                                                           ((0x00000010U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                             ? 
                                                            ((0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                                             | (((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                                  ? 0xe385U
                                                                  : 0xd005U) 
                                                                << 4U))
                                                             : 
                                                            ((8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                              ? 0x000e3123U
                                                              : 0x000cf923U)))));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                    if ((0x00001000U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                    >> 0x0000000bU)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                = (0x000c7ab0U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                            = ((0x0000000fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                               | (((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc7abU
                                                    : 0xc72bU) 
                                                  << 4U));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                        = ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                           | (((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc72bU
                                                    : 0xc6abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc6abU
                                                    : 0xc62bU)) 
                                              << 4U));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                       | (((0x00002000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc62bU
                                                    : 0xc5abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc5abU
                                                    : 0xc22bU))
                                            : ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc22bU
                                                    : 0xc1abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xc1abU
                                                    : 0x91abU))) 
                                          << 4U));
                            }
                        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x00090ba0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0x91abU
                                            : 0x912bU) 
                                          << 4U));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = (0x000912b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                 >> 0x0000000aU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                         >> 5U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                             >> 4U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                                 >> 3U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                                     >> 2U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000903b3U;
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
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x8aabU : 0x8a2bU) 
                                      << 4U));
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000bf3a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000c53a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x4000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))) {
                            if ((0U != (((0x4000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                         << 1U) | (0U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2306: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2306, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00086ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000873a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00087ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000883a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2280: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2280, "");
                            }
                        }
                    }
                } else {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00084ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000853a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00085ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000863a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2254: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2254, "");
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000da2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000daae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000d72e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x8000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 2U) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                            if ((0U != (((0x8000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                         << 2U) | (
                                                   ((0x4000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xc000U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2233: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2233, "");
                                }
                            }
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000ceae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000cf2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000d62e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0xc000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000d6ae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   ((0xc000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                    << 3U) 
                                                   | ((0x8000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                      << 2U)) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                            if ((0U != ((((0xc000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                          << 3U) | 
                                         ((0x8000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                          << 2U)) | 
                                        (((0x4000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                          << 1U) | 
                                         (0U == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2207: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2207, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000832e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00083ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00088ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000892e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2181: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2181, "");
                            }
                        }
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                      >> 0x0000000dU)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xdaabU
                                            : 0xda2bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xd72bU
                                            : 0xd6abU)) 
                                      << 4U));
                        }
                    }
                } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = (0x000d62b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                  >> 8U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                            = (0x000daa60U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                       | (((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0xda26U
                                                : 0xd726U)
                                            : ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0xd6a6U
                                                : 0xd626U)) 
                                          << 4U));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000d4ab0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0xcf2bU : 0xceabU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0xcb2bU : 0x8eabU)) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x8e2bU : 0x8c2bU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x8babU : 0x892bU))
                                : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x88abU : 0x83abU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x832bU : 
                                       ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                         ? ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                 ? 0xd4a6U
                                                 : 0xcf26U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                 ? 0xcea6U
                                                 : 0xca15U))
                                         : ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                 ? 0x8926U
                                                 : 0x88a6U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                 ? 0x83a6U
                                                 : 0x8326U)))))) 
                              << 4U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                   | (((0x00002000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xe7abU
                                            : 0xdeabU)
                                        : ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xdb2bU
                                            : 0xd82bU)) 
                                      << 4U));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = (0x000d52b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                            = (0x000db140U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                    } else if ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                         >> 5U)))) {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000dba43U;
                                                }
                                            }
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                            = (0x000d5260U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = (0x000c9ab0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xc9abU
                                            : 0xc12bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xc12bU
                                            : 0xc0abU)) 
                                      << 4U));
                        }
                    } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                               | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xc0abU
                                            : 0xc02bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xc02bU
                                            : 0xbfabU))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xbfabU
                                            : 0x952aU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0x952aU
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0xc915U
                                                     : 0xc815U)
                                                    : 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0xb895U
                                                     : 0xb815U))
                                                : 0x94a9U)))) 
                                  << 4U));
                    } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000400U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0x94a9U
                                            : 0x9416U)
                                        : 0x93aaU) : 
                                   ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                     ? 0x93aaU : 0x9329U)) 
                                  << 4U));
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x0008cab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00082ab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00000100U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0x8f95U : 0x8f15U)
                                    : 0x8c94U) << 4U));
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00081940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x00093250U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x0008b060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000db9f3U;
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                          >> 3U)))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000e7b53U;
                                        }
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x000deb53U
                                                : 0x000db353U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x000d8353U
                                                : 0x000c9b53U));
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x00095983U
                                                : 0x00095313U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x00094b03U
                                                : 0x00094183U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x00093b13U
                                                : 0x00093303U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x0008cb53U
                                                : 0x0008cb23U)))
                                    : ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x00082b53U
                                                : 0x00082af3U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x00081b53U
                                                : 0x00081af3U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? 0x00081af3U
                                                : 0x00081353U)
                                            : 0x000812f3U)));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x00080950U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                      >> 0x0000000dU)))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                              >> 0x0000000bU)))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                        = (0x000b5b40U 
                                           | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xb434U
                                            : 0xb3b4U) 
                                          << 4U));
                            }
                        }
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                           | (((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xb334U
                                            : 0xb1b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xb134U
                                            : 0xb0b4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xa7b4U
                                            : 0xa734U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xa6b4U
                                            : 0xa634U)))
                                : ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0xa334U
                                            : 0xa2b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0x9e34U
                                            : 0x9db4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0x98b4U
                                            : 0x9834U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? 0x97b4U
                                            : 0x96b4U)))) 
                              << 4U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                if (((((((((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                           | (0x0800U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                          | (0x0840U == (0xffe0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                         | (0x0900U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                        | (0x0a00U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                       | (0x0c00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                      | (0x0d00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                     | (0x0e00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                            ? (0x0009cb40U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                            : ((0x0800U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                ? (0x000b49a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                : ((0x0840U == (0xffe0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                    ? 0x000ab9b3U : 
                                   ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                                    | (((0x0900U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                         ? 0x9e90U : 
                                        ((0x0a00U == 
                                          (0xfe00U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                          ? 0x9ba7U
                                          : ((0x0c00U 
                                              == (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                              ? 0x9e90U
                                              : 0x9f10U))) 
                                       << 4U)))));
                } else if ((0x1000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x0009cad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x2000U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000b4970U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x2400U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x0009e990U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x2800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000aab40U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x3000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x4000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x5000U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x0009f190U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                }
                if ((1U & (~ VL_ONEHOT_I((((((((0x5000U 
                                                == 
                                                (0xfc00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 3U) 
                                              | ((0x4000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 2U)) 
                                             | (((0x3000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 1U) 
                                                | (0x2800U 
                                                   == 
                                                   (0xf800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                            << 0x0000000bU) 
                                           | (((((0x2400U 
                                                  == 
                                                  (0xfc00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 3U) 
                                                | ((0x2000U 
                                                    == 
                                                    (0xff80U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 2U)) 
                                               | (((0x1000U 
                                                    == 
                                                    (0xf000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 1U) 
                                                  | (0x0e00U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                              << 7U)) 
                                          | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))))) {
                    if ((0U != (((((((0x5000U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                     << 3U) | ((0x4000U 
                                                == 
                                                (0xf000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 2U)) 
                                   | (((0x3000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                       << 1U) | (0x2800U 
                                                 == 
                                                 (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                  << 0x0000000bU) | 
                                 (((((0x2400U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                     << 3U) | ((0x2000U 
                                                == 
                                                (0xff80U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 2U)) 
                                   | (((0x1000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                       << 1U) | (0x0e00U 
                                                 == 
                                                 (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                  << 7U)) | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1463: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1463, "");
                        }
                    }
                }
            } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                          >> 0x0000000bU)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                    = (0x000b5340U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                = (0x000b52d0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? 0xb52dU : 0xb2adU) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? 0xb2b4U : 0xb234U)
                                    : 0xb22dU) : ((0x00001000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                   ? 0xb22dU
                                                   : 
                                                  ((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0xb034U
                                                    : 0xafb4U))) 
                              << 4U));
                }
            } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                       | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                            ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? 0xaf34U : 0xad34U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? 0xacb4U : 0xaa34U))
                            : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? 0xa9b4U : 0xa934U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? 0xa5b4U : 0xa534U))) 
                          << 4U));
            } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                       | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                            ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? 0xa4b4U : 0xa434U)
                            : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? 0xa3b4U : 0x9fb4U)) 
                          << 4U));
            } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r) 
                       | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                            ? 0x9b34U : 0x9734U) << 4U));
            } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                    = (0x00096340U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
            } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                    = (0x000b6190U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                 >> 9U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                              >> 8U)))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                      >> 6U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                          >> 5U)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                              >> 4U)))) {
                                    if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                        if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word) 
                                                     >> 1U)))) {
                                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                    = 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                      ? 0x000b0333U
                                                      : 0x000afb33U);
                                            }
                                        } else {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                                = (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000afb33U
                                                     : 0x000af333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 
                                                    (0x000ae810U 
                                                     | (0x0000000fU 
                                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                                     : 0x000ae3d3U));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                                            = ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 0x000ae3c4U
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000adbd3U
                                                     : 0x000adbc4U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000adbc4U
                                                     : 0x000ad333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000ad333U
                                                     : 0x000acb33U)));
                                    }
                                }
                            }
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                ? (0x0009c060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                : ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                    ? (0x0009c070U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                    : ((0x00000010U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                        ? ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000ac3d3U
                                                     : 0x000ac3c4U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000ac3c4U
                                                     : 0x000aa333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a9b33U
                                                     : 0x000a9333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a8bd3U
                                                     : 0x000a8bc4U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a8bc4U
                                                     : 0x000a5b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a5b33U
                                                     : 0x000a5333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a5333U
                                                     : 0x000a4b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a4333U
                                                     : 0x000a3b33U))))
                                        : ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000a3b33U
                                                     : 0x0009fb33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x0009d3d3U
                                                     : 0x0009b333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x0009b333U
                                                     : 0x0009abd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x0009abc4U
                                                     : 0x0009a3d3U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x0009a3c4U
                                                     : 0x00099bd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x00099bc4U
                                                     : 0x000993d3U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))
                                                     ? 0x000993c4U
                                                     : 0x00097333U)
                                                    : 0x00096333U))))));
                    }
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000bd940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x0200U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000d8940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    } else if ((0x0400U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = (0x000df060U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I((((0x0400U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 2U) 
                                              | (((0x0200U 
                                                   == 
                                                   (0xfe00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                        if ((0U != (((0x0400U == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                     << 2U) | (((0x0200U 
                                                 == 
                                                 (0xfe00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                << 1U) 
                                               | (0U 
                                                  == 
                                                  (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1021: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1021, "");
                            }
                        }
                    }
                } else {
                    if (((((((((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                               | (8U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                              | (0x0010U == (0xfff0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                             | (0x0020U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                            | (0x0030U == (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                           | (0x0040U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                          | (0x0050U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) 
                         | (0x0100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                            = ((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                ? (0x000b6850U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                : ((8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                    ? (0x000d9050U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                    : ((0x0010U == 
                                        (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                        ? 0x000c38b3U
                                        : ((0x0020U 
                                            == (0xfff0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                            ? 0x000c40b3U
                                            : ((0x0030U 
                                                == 
                                                (0xfff0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                ? (0x000d9030U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r))
                                                : (
                                                   (0x0040U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                    ? 0x000e60b3U
                                                    : 
                                                   ((0x0050U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))
                                                     ? 0x000e68b3U
                                                     : 0x000c4a03U)))))));
                    } else if ((0x0200U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000e7203U;
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((((0x0200U 
                                                   == 
                                                   (0xff00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                  << 4U) 
                                                 | (((0x0100U 
                                                      == 
                                                      (0xff00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                     << 3U) 
                                                    | ((0x0050U 
                                                        == 
                                                        (0xfff0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                       << 2U))) 
                                                | (((0x0040U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                    << 1U) 
                                                   | (0x0030U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                               << 4U) 
                                              | ((((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0010U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                     << 2U)) 
                                                 | (((8U 
                                                      == 
                                                      (0xfff8U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                     << 1U) 
                                                    | (0U 
                                                       == 
                                                       (0xfff8U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))))) {
                        if ((0U != ((((((0x0200U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                        << 4U) | ((
                                                   (0x0100U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0050U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                     << 2U))) 
                                      | (((0x0040U 
                                           == (0xfff0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                          << 1U) | 
                                         (0x0030U == 
                                          (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))) 
                                     << 4U) | ((((0x0020U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 3U) 
                                                | ((0x0010U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 2U)) 
                                               | (((8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:964: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 964, "");
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                if ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x1000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x4000U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c2ac0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x4000U 
                                             == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                            << 4U) 
                                           | (((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 3U) 
                                              | ((0x1000U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                 << 2U))) 
                                          | (((0x0800U 
                                               == (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                    if ((0U != ((((0x4000U == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                  << 4U) | (((0x1800U 
                                              == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                             << 3U) 
                                            | ((0x1000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                               << 2U))) 
                                | (((0x0800U == (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                    << 1U) | (0U == 
                                              (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:933: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 933, "");
                        }
                    }
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x00089860U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000be810U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x0200U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000bd160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000be160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x0400U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                            << 3U) 
                                           | ((0x0200U 
                                               == (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                              << 2U)) 
                                          | (((0x0040U 
                                               == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))))) {
                    if ((0U != ((((0x0400U == (0xfe00U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                  << 3U) | ((0x0200U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                            << 2U)) 
                                | (((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                                    << 1U) | (0U == 
                                              (0xffc0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:907: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 907, "");
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
                if ((0x07ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000923f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x0800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x0bffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000ab380U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000bc9d0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000bc370U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000e0010U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000e0890U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x0d00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x0dffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000d9b60U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x1000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x17ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x1800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x1fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x2000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x27ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                } else if (((0x2800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)) 
                            & (0x2fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r 
                        = (0x000cc060U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r));
                }
                if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                    if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:839: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 839, "");
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__ext_root))) {
            if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x0008d403U;
            } else if ((0x4000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000a0393U;
            } else if ((0x4800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000a0b93U;
            } else if ((0x5000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000a1393U;
            } else if ((0x5800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000a1b93U;
            } else if ((0x6000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r = 0x000a2393U;
            }
            if ((1U & (~ VL_ONEHOT_I(((((0x6000U == 
                                         (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                        << 5U) | ((
                                                   (0x5800U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 4U) 
                                                  | ((0x5000U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                     << 3U))) 
                                      | (((0x4800U 
                                           == (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                          << 2U) | 
                                         (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))))) {
                if ((0U != ((((0x6000U == (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                              << 5U) | (((0x5800U == 
                                          (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                         << 4U) | (
                                                   (0x5000U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                                   << 3U))) 
                            | (((0x4800U == (0xf800U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                << 2U) | (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word)))))))) {
                    if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:797: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__extension_word));
                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 797, "");
                    }
                }
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__r;
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__226__Vfuncout;
        vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw 
            = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode 
                     >> 0x00000013U));
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__opcode_id 
            = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__extended_decode 
                              >> 0x0000000bU));
    }
    __Vfunc_bedrock_decode_opcode_attributes__227__opcode_id 
        = entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__227__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                              >> 4U)))) {
                    if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                                    __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                                         >> 2U)))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                                    = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                                      >> 1U)))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
                            }
                        }
                    }
                } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                                     >> 1U)))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    }
                }
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    }
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    }
                } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__227__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
            } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                          >> 1U)))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        }
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                        }
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                                     >> 2U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                                  >> 1U)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                        }
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__227__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))))
                        : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                    } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__227__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)))
                            : 7U);
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id) 
                              >> 1U)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__227__r 
                        = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            }
        }
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                    ? ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? 7U : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                                     ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))))
                        : ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)))))
                    : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                    ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                        ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r))
                            : 7U) : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)))
                    : 7U);
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        }
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__227__r 
                        = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__227__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            }
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__227__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        }
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        }
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__227__r = 7U;
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__227__r 
            = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))
                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r)));
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__227__r 
            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__227__r));
    }
    __Vfunc_bedrock_decode_opcode_attributes__227__Vfuncout 
        = __Vfunc_bedrock_decode_opcode_attributes__227__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__attributes 
        = __Vfunc_bedrock_decode_opcode_attributes__227__Vfuncout;
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repcc_allowed_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__attributes) 
              >> 2U));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repg_allowed_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__attributes) 
              >> 1U));
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repg_fast_candidate_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw) 
           & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode__DOT__attributes));
    __Vfunc_bedrock_decode_primary_payload__233__payload 
        = (0x00000fffU & vlSelfRef.entry_precheck_tb__DOT__line_words[1U]);
    __Vfunc_bedrock_decode_primary_payload__233__r = 0U;
    __Vfunc_bedrock_decode_primary_payload__233__r 
        = (0x00000020U | (0x03000000U & __Vfunc_bedrock_decode_primary_payload__233__r));
    if ((0x00000800U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                        if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                            if ((2U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                                if (
                                                    (1U 
                                                     & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                                        = 
                                                        (0x02000000U 
                                                         | __Vfunc_bedrock_decode_primary_payload__233__r);
                                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                                        = 
                                                        (0x006f0200U 
                                                         | (0x030001ffU 
                                                            & __Vfunc_bedrock_decode_primary_payload__233__r));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__233__payload) 
                                      >> 5U)))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__233__payload) 
                                              >> 3U)))) {
                                    if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                            if ((1U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__233__r);
                                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                                    = 
                                                    (0x0000000aU 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__233__r));
                                            } else {
                                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__233__r);
                                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                                    = 
                                                    (8U 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__233__r));
                                            }
                                        } else if (
                                                   (1U 
                                                    & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__233__r);
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (9U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__233__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__233__r);
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x00000016U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__233__r));
                                        }
                                    } else if ((2U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__233__r);
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x00000014U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__233__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__233__r);
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x00000015U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__233__r));
                                        }
                                    } else if ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__233__r);
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (2U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__233__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__233__r);
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (1U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__233__r));
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (3U | (0x03ffffe0U 
                                             & __Vfunc_bedrock_decode_primary_payload__233__r));
                            }
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__233__payload) 
                                                  >> 1U)))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__233__r);
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (4U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__233__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__233__r);
                                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                                = (7U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__233__r));
                                        }
                                    }
                                } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__233__r);
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (6U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__233__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__233__r);
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (5U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__233__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__233__r);
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x0000000fU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__233__r);
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x0000000eU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                                }
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__233__r);
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x0000000dU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__233__r);
                                        __Vfunc_bedrock_decode_primary_payload__233__r 
                                            = (0x0000000cU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__233__r);
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x00000012U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__233__r);
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x00000013U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                                }
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__233__r);
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x00000011U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__233__r);
                                    __Vfunc_bedrock_decode_primary_payload__233__r 
                                        = (0x00000010U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                                }
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x0000000bU 
                                       | (0x03ffffe0U 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00bf0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x008504a0U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00160800U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        }
                    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00160400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00950400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        }
                    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x00950800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x009b0400U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                    }
                } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00cf1c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00931c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            }
                        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00cd0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__233__r);
                                __Vfunc_bedrock_decode_primary_payload__233__r 
                                    = (0x00791040U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00cc0240U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                            __Vfunc_bedrock_decode_primary_payload__233__r 
                                = (0x00791040U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__233__r));
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x00921800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                        __Vfunc_bedrock_decode_primary_payload__233__r 
                            = (0x00901800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__233__r));
                    }
                } else {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x00294200U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                }
            } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x00cf4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x00bd4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                }
            } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00b64600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00934600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
        }
    } else if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00194600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00054600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
            }
        } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x00711800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x001f1800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
        }
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x00011800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                    __Vfunc_bedrock_decode_primary_payload__233__r 
                        = (0x00701800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__233__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
        }
    } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x00034600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x00281a00U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x001e1800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x00051c40U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x009b0800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00880240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
                __Vfunc_bedrock_decode_primary_payload__233__r 
                    = (0x00870240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
            }
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x00970240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x009c0240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x00a80200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
            __Vfunc_bedrock_decode_primary_payload__233__r 
                = (0x001302a0U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
        }
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__233__payload))) {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x00130260U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__233__r));
    } else {
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__233__r);
        __Vfunc_bedrock_decode_primary_payload__233__r 
            = (0x006e0200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__233__r));
    }
    __Vfunc_bedrock_decode_primary_payload__233__Vfuncout 
        = __Vfunc_bedrock_decode_primary_payload__233__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode 
        = __Vfunc_bedrock_decode_primary_payload__233__Vfuncout;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode = 0U;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode 
        = (0x0008000fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode);
    vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode_valid_raw 
        = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode 
                 >> 0x00000019U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__opcode_id 
        = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode 
                          >> 0x00000010U));
    if ((0x01000000U & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode)) {
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word 
            = (0x0000ffffU & ((0x00008000U & vlSelfRef.entry_precheck_tb__DOT__line_words[1U])
                               ? vlSelfRef.entry_precheck_tb__DOT__line_words[2U]
                               : ((vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                   << 0x00000010U) 
                                  | (vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                     >> 0x00000010U))));
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root 
            = (0x0000001fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__primary_decode);
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
            = (2U | (0x00080000U & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root)))) {
                            if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = (0x00092860U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                            }
                            if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                                if ((0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                                    if (VL_UNLIKELY((
                                                     vlSymsp->_vm_contextp__->assertOn()))) {
                                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2660: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2660, "");
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                        if (((((((((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                   | (1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                  | (2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                 | (8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                                | (0x0010U == (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                               | (0x0040U == (0xffc0U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                              | (0x0080U == (0xffc0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                             | (0x00c0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = ((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? (0x000bb010U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                    : ((1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x000b90a3U
                                        : ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x8401U
                                                : (
                                                   (8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                    ? 0xdc05U
                                                    : 
                                                   ((0x0010U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                     ? 0xd185U
                                                     : 
                                                    ((0x0040U 
                                                      == 
                                                      (0xffc0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                      ? 0xba86U
                                                      : 
                                                     ((0x0080U 
                                                       == 
                                                       (0xffc0U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                       ? 0xdc8fU
                                                       : 0xb986U))))) 
                                              << 4U))));
                        } else if ((0x0100U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000e2860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x0140U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000a8060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x0180U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000ba060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x01c0U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000dd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x0200U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000cc860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x0240U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000cd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x0280U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000e1060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (((((0x0280U 
                                                        == 
                                                        (0xffc0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                       << 3U) 
                                                      | ((0x0240U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                         << 2U)) 
                                                     | (((0x0200U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                         << 1U) 
                                                        | (0x01c0U 
                                                           == 
                                                           (0xffc0U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                                    << 0x0000000bU) 
                                                   | (((((0x0180U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0140U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0100U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                           << 1U) 
                                                          | (0x00c0U 
                                                             == 
                                                             (0xffc0U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                                      << 7U)) 
                                                  | ((((((0x0080U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0040U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0010U 
                                                            == 
                                                            (0xfff8U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                           << 1U) 
                                                          | (8U 
                                                             == 
                                                             (0xfff8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                                      << 3U) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                                         << 2U) 
                                                        | (((1U 
                                                             == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                                            << 1U) 
                                                           | (0U 
                                                              == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))))) {
                            if ((0U != (((((((0x0280U 
                                              == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                             << 3U) 
                                            | ((0x0240U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 2U)) 
                                           | (((0x0200U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 1U) 
                                              | (0x01c0U 
                                                 == 
                                                 (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                          << 0x0000000bU) 
                                         | (((((0x0180U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 3U) 
                                              | ((0x0140U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0100U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 1U) 
                                                | (0x00c0U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                            << 7U)) 
                                        | ((((((0x0080U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 3U) 
                                              | ((0x0040U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 1U) 
                                                | (8U 
                                                   == 
                                                   (0xfff8U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                            << 3U) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                               << 2U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                                  << 1U) 
                                                 | (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2578: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2578, "");
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                         >> 0x0000000fU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                      >> 0x0000000eU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                          >> 0x0000000dU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                              >> 0x0000000cU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                  >> 0x0000000bU)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                    >> 0x0000000aU)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                     >> 9U)))) {
                                                if (
                                                    (0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                             >> 7U)))) {
                                                        if (
                                                            (0x00000040U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                                     >> 5U)))) {
                                                                if (
                                                                    (0x00000010U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                                                    if (
                                                                        (8U 
                                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                                            = 
                                                                            (0x000e4050U 
                                                                             | (0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                                                    } else if (
                                                                               (1U 
                                                                                & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                                                >> 2U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                                                >> 1U)))) {
                                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                                                = 
                                                                                ((0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                                                                | (((1U 
                                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                                 ? 0xe801U
                                                                                 : 0xe201U) 
                                                                                << 4U));
                                                                        }
                                                                    }
                                                                } else {
                                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                                        = 
                                                                        ((8U 
                                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                          ? 0x000d1133U
                                                                          : 
                                                                         (0x000d0850U 
                                                                          | (0x0000000fU 
                                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r)));
                                                                }
                                                            }
                                                        } else {
                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                                = 
                                                                (0x000d3860U 
                                                                 | (0x0000000fU 
                                                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                                        }
                                                    }
                                                } else {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                        = 
                                                        ((0x00000080U 
                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                          ? 
                                                         ((0x0000000fU 
                                                           & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                                          | (((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                               ? 0xd786U
                                                               : 0xe491U) 
                                                             << 4U))
                                                          : 
                                                         ((0x00000040U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                           ? 
                                                          (0x000d21c0U 
                                                           | (0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                                           : 
                                                          ((0x00000020U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                            ? 
                                                           ((0x0000000fU 
                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                                            | (((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                  ? 0x8d85U
                                                                  : 
                                                                 ((4U 
                                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                   ? 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                     ? 0xe181U
                                                                     : 0xde01U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                     ? 0xdd81U
                                                                     : 0xd581U))
                                                                   : 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                     ? 0xd301U
                                                                     : 0xc881U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                     ? 0xbb81U
                                                                     : 0x8201U))))
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                  ? 0xe505U
                                                                  : 0xd285U)) 
                                                               << 4U))
                                                            : 
                                                           ((0x00000010U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                             ? 
                                                            ((0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                                             | (((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                                  ? 0xe385U
                                                                  : 0xd005U) 
                                                                << 4U))
                                                             : 
                                                            ((8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                              ? 0x000e3123U
                                                              : 0x000cf923U)))));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                    if ((0x00001000U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                    >> 0x0000000bU)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                = (0x000c7ab0U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                            = ((0x0000000fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                               | (((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc7abU
                                                    : 0xc72bU) 
                                                  << 4U));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                        = ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                           | (((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc72bU
                                                    : 0xc6abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc6abU
                                                    : 0xc62bU)) 
                                              << 4U));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                       | (((0x00002000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc62bU
                                                    : 0xc5abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc5abU
                                                    : 0xc22bU))
                                            : ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc22bU
                                                    : 0xc1abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xc1abU
                                                    : 0x91abU))) 
                                          << 4U));
                            }
                        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x00090ba0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0x91abU
                                            : 0x912bU) 
                                          << 4U));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = (0x000912b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                 >> 0x0000000aU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                         >> 5U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                             >> 4U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                                 >> 3U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                                     >> 2U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000903b3U;
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
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x8aabU : 0x8a2bU) 
                                      << 4U));
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000bf3a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000c53a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x4000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))) {
                            if ((0U != (((0x4000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                         << 1U) | (0U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2306: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2306, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00086ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000873a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00087ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000883a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2280: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2280, "");
                            }
                        }
                    }
                } else {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00084ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000853a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00085ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000863a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2254: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2254, "");
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000da2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000daae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000d72e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x8000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 2U) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                            if ((0U != (((0x8000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                         << 2U) | (
                                                   ((0x4000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xc000U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2233: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2233, "");
                                }
                            }
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000ceae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000cf2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000d62e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0xc000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000d6ae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   ((0xc000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                    << 3U) 
                                                   | ((0x8000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                      << 2U)) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                            if ((0U != ((((0xc000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                          << 3U) | 
                                         ((0x8000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                          << 2U)) | 
                                        (((0x4000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                          << 1U) | 
                                         (0U == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2207: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2207, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000832e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00083ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00088ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000892e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2181: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2181, "");
                            }
                        }
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                      >> 0x0000000dU)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xdaabU
                                            : 0xda2bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xd72bU
                                            : 0xd6abU)) 
                                      << 4U));
                        }
                    }
                } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = (0x000d62b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                  >> 8U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                            = (0x000daa60U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                       | (((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0xda26U
                                                : 0xd726U)
                                            : ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0xd6a6U
                                                : 0xd626U)) 
                                          << 4U));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000d4ab0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0xcf2bU : 0xceabU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0xcb2bU : 0x8eabU)) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x8e2bU : 0x8c2bU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x8babU : 0x892bU))
                                : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x88abU : 0x83abU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x832bU : 
                                       ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                         ? ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                 ? 0xd4a6U
                                                 : 0xcf26U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                 ? 0xcea6U
                                                 : 0xca15U))
                                         : ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                 ? 0x8926U
                                                 : 0x88a6U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                 ? 0x83a6U
                                                 : 0x8326U)))))) 
                              << 4U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                   | (((0x00002000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xe7abU
                                            : 0xdeabU)
                                        : ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xdb2bU
                                            : 0xd82bU)) 
                                      << 4U));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = (0x000d52b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                            = (0x000db140U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                    } else if ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                         >> 5U)))) {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000dba43U;
                                                }
                                            }
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                            = (0x000d5260U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = (0x000c9ab0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xc9abU
                                            : 0xc12bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xc12bU
                                            : 0xc0abU)) 
                                      << 4U));
                        }
                    } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                               | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xc0abU
                                            : 0xc02bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xc02bU
                                            : 0xbfabU))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xbfabU
                                            : 0x952aU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0x952aU
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0xc915U
                                                     : 0xc815U)
                                                    : 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0xb895U
                                                     : 0xb815U))
                                                : 0x94a9U)))) 
                                  << 4U));
                    } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000400U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0x94a9U
                                            : 0x9416U)
                                        : 0x93aaU) : 
                                   ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                     ? 0x93aaU : 0x9329U)) 
                                  << 4U));
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x0008cab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00082ab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00000100U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0x8f95U : 0x8f15U)
                                    : 0x8c94U) << 4U));
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00081940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x00093250U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x0008b060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000db9f3U;
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                          >> 3U)))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000e7b53U;
                                        }
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x000deb53U
                                                : 0x000db353U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x000d8353U
                                                : 0x000c9b53U));
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x00095983U
                                                : 0x00095313U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x00094b03U
                                                : 0x00094183U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x00093b13U
                                                : 0x00093303U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x0008cb53U
                                                : 0x0008cb23U)))
                                    : ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x00082b53U
                                                : 0x00082af3U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x00081b53U
                                                : 0x00081af3U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? 0x00081af3U
                                                : 0x00081353U)
                                            : 0x000812f3U)));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x00080950U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                      >> 0x0000000dU)))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                              >> 0x0000000bU)))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                        = (0x000b5b40U 
                                           | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xb434U
                                            : 0xb3b4U) 
                                          << 4U));
                            }
                        }
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                           | (((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xb334U
                                            : 0xb1b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xb134U
                                            : 0xb0b4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xa7b4U
                                            : 0xa734U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xa6b4U
                                            : 0xa634U)))
                                : ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0xa334U
                                            : 0xa2b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0x9e34U
                                            : 0x9db4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0x98b4U
                                            : 0x9834U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? 0x97b4U
                                            : 0x96b4U)))) 
                              << 4U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                if (((((((((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                           | (0x0800U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                          | (0x0840U == (0xffe0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                         | (0x0900U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                        | (0x0a00U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                       | (0x0c00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                      | (0x0d00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                     | (0x0e00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                            ? (0x0009cb40U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                            : ((0x0800U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                ? (0x000b49a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                : ((0x0840U == (0xffe0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                    ? 0x000ab9b3U : 
                                   ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                                    | (((0x0900U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                         ? 0x9e90U : 
                                        ((0x0a00U == 
                                          (0xfe00U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                          ? 0x9ba7U
                                          : ((0x0c00U 
                                              == (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                              ? 0x9e90U
                                              : 0x9f10U))) 
                                       << 4U)))));
                } else if ((0x1000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x0009cad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x2000U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000b4970U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x2400U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x0009e990U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x2800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000aab40U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x3000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x4000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x5000U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x0009f190U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                }
                if ((1U & (~ VL_ONEHOT_I((((((((0x5000U 
                                                == 
                                                (0xfc00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 3U) 
                                              | ((0x4000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 2U)) 
                                             | (((0x3000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 1U) 
                                                | (0x2800U 
                                                   == 
                                                   (0xf800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                            << 0x0000000bU) 
                                           | (((((0x2400U 
                                                  == 
                                                  (0xfc00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 3U) 
                                                | ((0x2000U 
                                                    == 
                                                    (0xff80U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 2U)) 
                                               | (((0x1000U 
                                                    == 
                                                    (0xf000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 1U) 
                                                  | (0x0e00U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                              << 7U)) 
                                          | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))))) {
                    if ((0U != (((((((0x5000U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                     << 3U) | ((0x4000U 
                                                == 
                                                (0xf000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 2U)) 
                                   | (((0x3000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                       << 1U) | (0x2800U 
                                                 == 
                                                 (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                  << 0x0000000bU) | 
                                 (((((0x2400U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                     << 3U) | ((0x2000U 
                                                == 
                                                (0xff80U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 2U)) 
                                   | (((0x1000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                       << 1U) | (0x0e00U 
                                                 == 
                                                 (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                  << 7U)) | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1463: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1463, "");
                        }
                    }
                }
            } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                          >> 0x0000000bU)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                    = (0x000b5340U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                = (0x000b52d0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? 0xb52dU : 0xb2adU) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? 0xb2b4U : 0xb234U)
                                    : 0xb22dU) : ((0x00001000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                   ? 0xb22dU
                                                   : 
                                                  ((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0xb034U
                                                    : 0xafb4U))) 
                              << 4U));
                }
            } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                       | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                            ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? 0xaf34U : 0xad34U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? 0xacb4U : 0xaa34U))
                            : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? 0xa9b4U : 0xa934U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? 0xa5b4U : 0xa534U))) 
                          << 4U));
            } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                       | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                            ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? 0xa4b4U : 0xa434U)
                            : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? 0xa3b4U : 0x9fb4U)) 
                          << 4U));
            } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r) 
                       | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                            ? 0x9b34U : 0x9734U) << 4U));
            } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                    = (0x00096340U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
            } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                    = (0x000b6190U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                 >> 9U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                              >> 8U)))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                      >> 6U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                          >> 5U)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                              >> 4U)))) {
                                    if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                        if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word) 
                                                     >> 1U)))) {
                                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                    = 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                      ? 0x000b0333U
                                                      : 0x000afb33U);
                                            }
                                        } else {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                                = (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000afb33U
                                                     : 0x000af333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 
                                                    (0x000ae810U 
                                                     | (0x0000000fU 
                                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                                     : 0x000ae3d3U));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                                            = ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 0x000ae3c4U
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000adbd3U
                                                     : 0x000adbc4U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000adbc4U
                                                     : 0x000ad333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000ad333U
                                                     : 0x000acb33U)));
                                    }
                                }
                            }
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                ? (0x0009c060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                : ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                    ? (0x0009c070U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                    : ((0x00000010U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                        ? ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000ac3d3U
                                                     : 0x000ac3c4U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000ac3c4U
                                                     : 0x000aa333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a9b33U
                                                     : 0x000a9333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a8bd3U
                                                     : 0x000a8bc4U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a8bc4U
                                                     : 0x000a5b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a5b33U
                                                     : 0x000a5333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a5333U
                                                     : 0x000a4b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a4333U
                                                     : 0x000a3b33U))))
                                        : ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000a3b33U
                                                     : 0x0009fb33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x0009d3d3U
                                                     : 0x0009b333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x0009b333U
                                                     : 0x0009abd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x0009abc4U
                                                     : 0x0009a3d3U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x0009a3c4U
                                                     : 0x00099bd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x00099bc4U
                                                     : 0x000993d3U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))
                                                     ? 0x000993c4U
                                                     : 0x00097333U)
                                                    : 0x00096333U))))));
                    }
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000bd940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x0200U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000d8940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    } else if ((0x0400U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = (0x000df060U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I((((0x0400U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 2U) 
                                              | (((0x0200U 
                                                   == 
                                                   (0xfe00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                        if ((0U != (((0x0400U == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                     << 2U) | (((0x0200U 
                                                 == 
                                                 (0xfe00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                << 1U) 
                                               | (0U 
                                                  == 
                                                  (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1021: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1021, "");
                            }
                        }
                    }
                } else {
                    if (((((((((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                               | (8U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                              | (0x0010U == (0xfff0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                             | (0x0020U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                            | (0x0030U == (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                           | (0x0040U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                          | (0x0050U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) 
                         | (0x0100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                            = ((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                ? (0x000b6850U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                : ((8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                    ? (0x000d9050U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                    : ((0x0010U == 
                                        (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                        ? 0x000c38b3U
                                        : ((0x0020U 
                                            == (0xfff0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                            ? 0x000c40b3U
                                            : ((0x0030U 
                                                == 
                                                (0xfff0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                ? (0x000d9030U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r))
                                                : (
                                                   (0x0040U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                    ? 0x000e60b3U
                                                    : 
                                                   ((0x0050U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))
                                                     ? 0x000e68b3U
                                                     : 0x000c4a03U)))))));
                    } else if ((0x0200U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000e7203U;
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((((0x0200U 
                                                   == 
                                                   (0xff00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                  << 4U) 
                                                 | (((0x0100U 
                                                      == 
                                                      (0xff00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                     << 3U) 
                                                    | ((0x0050U 
                                                        == 
                                                        (0xfff0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                       << 2U))) 
                                                | (((0x0040U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                    << 1U) 
                                                   | (0x0030U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                               << 4U) 
                                              | ((((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0010U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                     << 2U)) 
                                                 | (((8U 
                                                      == 
                                                      (0xfff8U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                     << 1U) 
                                                    | (0U 
                                                       == 
                                                       (0xfff8U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))))) {
                        if ((0U != ((((((0x0200U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                        << 4U) | ((
                                                   (0x0100U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0050U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                     << 2U))) 
                                      | (((0x0040U 
                                           == (0xfff0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                          << 1U) | 
                                         (0x0030U == 
                                          (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))) 
                                     << 4U) | ((((0x0020U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 3U) 
                                                | ((0x0010U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 2U)) 
                                               | (((8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:964: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 964, "");
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                if ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x1000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x4000U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c2ac0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x4000U 
                                             == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                            << 4U) 
                                           | (((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 3U) 
                                              | ((0x1000U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                 << 2U))) 
                                          | (((0x0800U 
                                               == (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                    if ((0U != ((((0x4000U == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                  << 4U) | (((0x1800U 
                                              == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                             << 3U) 
                                            | ((0x1000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                               << 2U))) 
                                | (((0x0800U == (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                    << 1U) | (0U == 
                                              (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:933: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 933, "");
                        }
                    }
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x00089860U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000be810U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x0200U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000bd160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000be160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x0400U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                            << 3U) 
                                           | ((0x0200U 
                                               == (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                              << 2U)) 
                                          | (((0x0040U 
                                               == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))))) {
                    if ((0U != ((((0x0400U == (0xfe00U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                  << 3U) | ((0x0200U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                            << 2U)) 
                                | (((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                                    << 1U) | (0U == 
                                              (0xffc0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:907: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 907, "");
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
                if ((0x07ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000923f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x0800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x0bffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000ab380U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000bc9d0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000bc370U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000e0010U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000e0890U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x0d00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x0dffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000d9b60U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x1000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x17ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x1800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x1fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x2000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x27ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                } else if (((0x2800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)) 
                            & (0x2fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r 
                        = (0x000cc060U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r));
                }
                if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                    if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:839: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 839, "");
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__ext_root))) {
            if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x0008d403U;
            } else if ((0x4000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000a0393U;
            } else if ((0x4800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000a0b93U;
            } else if ((0x5000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000a1393U;
            } else if ((0x5800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000a1b93U;
            } else if ((0x6000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r = 0x000a2393U;
            }
            if ((1U & (~ VL_ONEHOT_I(((((0x6000U == 
                                         (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                        << 5U) | ((
                                                   (0x5800U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 4U) 
                                                  | ((0x5000U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                     << 3U))) 
                                      | (((0x4800U 
                                           == (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                          << 2U) | 
                                         (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))))) {
                if ((0U != ((((0x6000U == (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                              << 5U) | (((0x5800U == 
                                          (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                         << 4U) | (
                                                   (0x5000U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                                   << 3U))) 
                            | (((0x4800U == (0xf800U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                << 2U) | (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word)))))))) {
                    if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:797: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__extension_word));
                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 797, "");
                    }
                }
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__r;
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__234__Vfuncout;
        vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode_valid_raw 
            = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode 
                     >> 0x00000013U));
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__opcode_id 
            = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode__DOT__extended_decode 
                              >> 0x0000000bU));
    }
    __Vfunc_bedrock_decode_opcode_attributes__235__opcode_id 
        = entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__opcode_id;
    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                              >> 4U)))) {
                    if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                                         >> 2U)))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                                    = (2U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                                      >> 1U)))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
                            }
                        }
                    }
                } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                                     >> 1U)))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    }
                }
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    }
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    }
                } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                        = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                        ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
            } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                          >> 1U)))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                        ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
            }
        } else {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        }
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                        }
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                                     >> 2U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                                  >> 1U)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                        }
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                                ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                                ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))))
                        : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                    } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                                ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)))
                            : 7U);
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id) 
                              >> 1U)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                        = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            }
        }
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                    ? ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? 7U : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                                     ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))))
                        : ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                                ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)))))
                    : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                    ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                        ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                            ? (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r))
                            : 7U) : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)))
                    : 7U);
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
            }
        } else {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        }
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                        = (2U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                        ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                        = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            }
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id)))) {
                vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                    = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
            }
        } else {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        }
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        }
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
                = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
            vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r = 7U;
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
            = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))
                ? 7U : (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r)));
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__235__opcode_id))) {
        vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r 
            = (6U | (IData)(vlSelfRef.__Vfunc_bedrock_decode_opcode_attributes__235__r));
    }
}
