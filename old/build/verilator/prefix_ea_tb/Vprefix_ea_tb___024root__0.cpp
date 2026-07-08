// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vprefix_ea_tb.h for the primary calling header

#include "Vprefix_ea_tb__pch.h"

VlCoroutine Vprefix_ea_tb___024root___eval_initial__TOP__Vtiming__0(Vprefix_ea_tb___024root* vlSelf);

void Vprefix_ea_tb___024root___eval_initial(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_initial\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vprefix_ea_tb___024root___eval_initial__TOP__Vtiming__0(vlSelf);
}

VlCoroutine Vprefix_ea_tb___024root___eval_initial__TOP__Vtiming__0(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ prefix_ea_tb__DOT__failures;
    prefix_ea_tb__DOT__failures = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_nospec;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_nospec = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_saturate;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_saturate = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_update;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_update = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_access;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_access = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_repeat;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_repeat = 0;
    CData/*3:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_condition;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_condition = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_counter;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_counter = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_end_group;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_end_group = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_payload_words = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_payload_words = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_payload_words = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_payload_words = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_payload_words = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_payload_words = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_valid;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_valid = 0;
    CData/*0:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_reserved;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_reserved = 0;
    CData/*5:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_form;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_form = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_segment;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_segment = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base_reg = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_index_reg;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_index_reg = 0;
    CData/*1:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_scale;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_scale = 0;
    CData/*2:0*/ __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_payload_words;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_payload_words = 0;
    // Body
    prefix_ea_tb__DOT__failures = 0U;
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_counter = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_repeat = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__0__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0x0201U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_counter = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_repeat = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_saturate = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_nospec = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__1__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0x0604U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_counter = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_repeat = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_update = 3U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__2__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0x008dU;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_counter = 5U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_condition = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_repeat = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__3__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0x0073U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_counter = 3U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_repeat = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__4__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0x0078U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_end_group = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_counter = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_repeat = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__5__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 0x6900U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_counter = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_repeat = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_access = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_valid = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__6__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__prefix_word = 8U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_end_group = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_counter = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_condition = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_repeat = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_access = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_update = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_saturate = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_nospec = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         100);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:103: Assertion failed in %m: prefix %04h valid got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__prefix_valid
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_valid));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 103, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__nospec) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_nospec))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:108: Assertion failed in %m: prefix %04h nospec got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__nospec
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_nospec));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 108, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__saturate) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_saturate))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:113: Assertion failed in %m: prefix %04h saturate got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__saturate
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_saturate));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 113, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__update_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_update))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:118: Assertion failed in %m: prefix %04h update got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__update_mode
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_update));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 118, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__access_mode) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_access))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:123: Assertion failed in %m: prefix %04h access got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__access_mode
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_access));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 123, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_kind) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_repeat))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:128: Assertion failed in %m: prefix %04h repeat got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',2,vlSelfRef.prefix_ea_tb__DOT__repeat_kind
                     , '#',2,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_repeat));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 128, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_condition) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_condition))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:133: Assertion failed in %m: prefix %04h condition got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',4,vlSelfRef.prefix_ea_tb__DOT__repeat_condition
                     , '#',4,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_condition));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 133, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__repeat_counter) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_counter))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:138: Assertion failed in %m: prefix %04h counter got %0d expected %0d\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',3,vlSelfRef.prefix_ea_tb__DOT__repeat_counter
                     , '#',3,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_counter));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 138, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__end_group) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_end_group))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:143: Assertion failed in %m: prefix %04h end_group got %0b expected %0b\n",6, 'M',vlSymsp->name(),"prefix_ea_tb.expect_prefix", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',16,(IData)(vlSelfRef.prefix_ea_tb__DOT__prefix_word)
                     , '#',1,vlSelfRef.prefix_ea_tb__DOT__end_group
                     , '#',1,(IData)(__Vtask_prefix_ea_tb__DOT__expect_prefix__7__expected_end_group));
        VL_STOP_MT("tb/prefix_ea_tb.sv", 143, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__descriptor = 0U;
    vlSelfRef.prefix_ea_tb__DOT__ea = 5U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_payload_words = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_scale = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_index_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base_reg = 5U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_segment = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_form = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_reserved = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__8__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__ea = 0x1aU;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_payload_words = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_scale = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_index_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base_reg = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_segment = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_form = 4U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_reserved = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__9__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__ea = 0x32U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_payload_words = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_scale = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_index_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_segment = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base = 6U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_form = 0x0fU;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_reserved = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__10__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__ea = 0x2bU;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_payload_words = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_scale = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_index_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_segment = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_form = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_reserved = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_valid = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__11__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__ea = 0x3fU;
    vlSelfRef.prefix_ea_tb__DOT__descriptor = 0x01d2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_payload_words = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_scale = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_index_reg = 4U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base_reg = 6U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_segment = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_form = 0x14U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_reserved = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__12__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__ea = 0x3eU;
    vlSelfRef.prefix_ea_tb__DOT__descriptor = 0x01d2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_payload_words = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_scale = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_index_reg = 4U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base_reg = 6U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_segment = 1U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_form = 0x23U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_reserved = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_valid = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__13__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    vlSelfRef.prefix_ea_tb__DOT__ea = 0x3fU;
    vlSelfRef.prefix_ea_tb__DOT__descriptor = 0x4a12U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_payload_words = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_scale = 2U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_index_reg = 4U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base_reg = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_segment = 7U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base = 4U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_form = 0x1dU;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_reserved = 0U;
    __Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_valid = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/prefix_ea_tb.sv", 
                                         161);
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:164: Assertion failed in %m: ea %02h desc %04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_valid)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_valid);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 164, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_reserved))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:169: Assertion failed in %m: ea %02h desc %04h reserved got %0b expected %0b\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',1,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_reserved)
                     , '#',1,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_reserved);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 169, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_form))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:174: Assertion failed in %m: ea %02h desc %04h form got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea_form)
                     , '#',6,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_form);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 174, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:179: Assertion failed in %m: ea %02h desc %04h base got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 179, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__segment) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_segment))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:184: Assertion failed in %m: ea %02h desc %04h segment got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__segment)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_segment);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 184, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:189: Assertion failed in %m: ea %02h desc %04h base_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__base_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_base_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 189, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_index_reg))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:194: Assertion failed in %m: ea %02h desc %04h index_reg got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__index_reg)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_index_reg);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 194, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_scale))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:199: Assertion failed in %m: ea %02h desc %04h scale got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',2,(IData)(vlSelfRef.prefix_ea_tb__DOT__scale_log2)
                     , '#',2,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_scale);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 199, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words) 
                      != (IData)(__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_payload_words))))) {
        VL_WRITEF_NX("[%0t] %%Error: prefix_ea_tb.sv:204: Assertion failed in %m: ea %02h desc %04h payload_words got %0d expected %0d\n",7, 'M',vlSymsp->name(),"prefix_ea_tb.expect_ea", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',6,(IData)(vlSelfRef.prefix_ea_tb__DOT__ea)
                     , '#',16,vlSelfRef.prefix_ea_tb__DOT__descriptor
                     , '#',3,(IData)(vlSelfRef.prefix_ea_tb__DOT__payload_words)
                     , '#',3,__Vtask_prefix_ea_tb__DOT__expect_ea__14__expected_payload_words);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 204, "");
        prefix_ea_tb__DOT__failures = ((IData)(1U) 
                                       + prefix_ea_tb__DOT__failures);
    }
    if (VL_UNLIKELY(((0U != prefix_ea_tb__DOT__failures)))) {
        VL_WRITEF_NX("[%0t] %%Fatal: prefix_ea_tb.sv:265: Assertion failed in %m: prefix_ea_tb failed with %0d failure(s)\n",4, 'M',vlSymsp->name(),"prefix_ea_tb", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '~',32,prefix_ea_tb__DOT__failures);
        VL_STOP_MT("tb/prefix_ea_tb.sv", 265, "", false);
    }
    VL_WRITEF_NX("prefix_ea_tb PASS\n",0);
    VL_FINISH_MT("tb/prefix_ea_tb.sv", 268, "");
    co_return;
}

void Vprefix_ea_tb___024root___eval_triggers_vec__act(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_triggers_vec__act\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered[0U] = (QData)((IData)(vlSelfRef.__VdlySched.awaitingCurrentTime()));
}

bool Vprefix_ea_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___trigger_anySet__act\n"); );
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

void Vprefix_ea_tb___024root___act_sequent__TOP__0(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___act_sequent__TOP__0\n"); );
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

void Vprefix_ea_tb___024root___eval_act(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_act\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        Vprefix_ea_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

void Vprefix_ea_tb___024root___nba_sequent__TOP__0(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___nba_sequent__TOP__0\n"); );
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

void Vprefix_ea_tb___024root___eval_nba(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_nba\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vprefix_ea_tb___024root___nba_sequent__TOP__0(vlSelf);
    }
}

void Vprefix_ea_tb___024root___timing_resume(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___timing_resume\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Vprefix_ea_tb___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vprefix_ea_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vprefix_ea_tb___024root___eval_phase__act(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_phase__act\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    Vprefix_ea_tb___024root___eval_triggers_vec__act(vlSelf);
    Vprefix_ea_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vprefix_ea_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vprefix_ea_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vprefix_ea_tb___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Vprefix_ea_tb___024root___timing_resume(vlSelf);
        Vprefix_ea_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vprefix_ea_tb___024root___eval_phase__inact(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_phase__inact\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("tb/prefix_ea_tb.sv", 4, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vprefix_ea_tb___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vprefix_ea_tb___024root___eval_phase__nba(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_phase__nba\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vprefix_ea_tb___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vprefix_ea_tb___024root___eval_nba(vlSelf);
        Vprefix_ea_tb___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vprefix_ea_tb___024root___eval(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vprefix_ea_tb___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("tb/prefix_ea_tb.sv", 4, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("tb/prefix_ea_tb.sv", 4, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vprefix_ea_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("tb/prefix_ea_tb.sv", 4, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vprefix_ea_tb___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vprefix_ea_tb___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vprefix_ea_tb___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vprefix_ea_tb___024root___eval_debug_assertions(Vprefix_ea_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vprefix_ea_tb___024root___eval_debug_assertions\n"); );
    Vprefix_ea_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
