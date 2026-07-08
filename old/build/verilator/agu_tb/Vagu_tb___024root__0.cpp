// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vagu_tb.h for the primary calling header

#include "Vagu_tb__pch.h"

VlCoroutine Vagu_tb___024root___eval_initial__TOP__Vtiming__0(Vagu_tb___024root* vlSelf);

void Vagu_tb___024root___eval_initial(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_initial\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vagu_tb___024root___eval_initial__TOP__Vtiming__0(vlSelf);
}

VlCoroutine Vagu_tb___024root___eval_initial__TOP__Vtiming__0(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ agu_tb__DOT__failures;
    agu_tb__DOT__failures = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__1__got;
    __Vtask_agu_tb__DOT__expect_logic__1__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__1__expected;
    __Vtask_agu_tb__DOT__expect_logic__1__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__2__got;
    __Vtask_agu_tb__DOT__expect_logic__2__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__2__expected;
    __Vtask_agu_tb__DOT__expect_logic__2__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__3__got;
    __Vtask_agu_tb__DOT__expect_u64__3__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__3__expected;
    __Vtask_agu_tb__DOT__expect_u64__3__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__5__got;
    __Vtask_agu_tb__DOT__expect_u64__5__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__5__expected;
    __Vtask_agu_tb__DOT__expect_u64__5__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__7__got;
    __Vtask_agu_tb__DOT__expect_u64__7__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__7__expected;
    __Vtask_agu_tb__DOT__expect_u64__7__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__9__got;
    __Vtask_agu_tb__DOT__expect_u64__9__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__9__expected;
    __Vtask_agu_tb__DOT__expect_u64__9__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__11__got;
    __Vtask_agu_tb__DOT__expect_logic__11__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__11__expected;
    __Vtask_agu_tb__DOT__expect_logic__11__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__12__got;
    __Vtask_agu_tb__DOT__expect_logic__12__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__12__expected;
    __Vtask_agu_tb__DOT__expect_logic__12__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__13__got;
    __Vtask_agu_tb__DOT__expect_u64__13__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__13__expected;
    __Vtask_agu_tb__DOT__expect_u64__13__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__15__got;
    __Vtask_agu_tb__DOT__expect_logic__15__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__15__expected;
    __Vtask_agu_tb__DOT__expect_logic__15__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__16__got;
    __Vtask_agu_tb__DOT__expect_u64__16__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__16__expected;
    __Vtask_agu_tb__DOT__expect_u64__16__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__17__got;
    __Vtask_agu_tb__DOT__expect_u64__17__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__17__expected;
    __Vtask_agu_tb__DOT__expect_u64__17__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__19__got;
    __Vtask_agu_tb__DOT__expect_logic__19__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__19__expected;
    __Vtask_agu_tb__DOT__expect_logic__19__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__20__got;
    __Vtask_agu_tb__DOT__expect_u64__20__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__20__expected;
    __Vtask_agu_tb__DOT__expect_u64__20__expected = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__21__got;
    __Vtask_agu_tb__DOT__expect_u64__21__got = 0;
    QData/*63:0*/ __Vtask_agu_tb__DOT__expect_u64__21__expected;
    __Vtask_agu_tb__DOT__expect_u64__21__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__23__got;
    __Vtask_agu_tb__DOT__expect_logic__23__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__23__expected;
    __Vtask_agu_tb__DOT__expect_logic__23__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__24__got;
    __Vtask_agu_tb__DOT__expect_logic__24__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__24__expected;
    __Vtask_agu_tb__DOT__expect_logic__24__expected = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__25__got;
    __Vtask_agu_tb__DOT__expect_logic__25__got = 0;
    CData/*0:0*/ __Vtask_agu_tb__DOT__expect_logic__25__expected;
    __Vtask_agu_tb__DOT__expect_logic__25__expected = 0;
    // Body
    agu_tb__DOT__failures = 0U;
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000010000ULL 
                                      | (0x3ffffffffff03fffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000200ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000400000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000100000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000800000ULL 
                                      | (0x3ffffffffc7fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__base_reg_value = 0x0000000000001000ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0x000000000000fff0ULL;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         85);
    __Vtask_agu_tb__DOT__expect_logic__1__expected = 1U;
    __Vtask_agu_tb__DOT__expect_logic__1__got = vlSelfRef.agu_tb__DOT__valid;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__1__name = "disp16 valid"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__1__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__1__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__1__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__1__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__1__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_logic__2__expected = 1U;
    __Vtask_agu_tb__DOT__expect_logic__2__got = vlSelfRef.agu_tb__DOT__address_valid;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__2__name = "disp16 address valid"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__2__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__2__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__2__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__2__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__2__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_u64__3__expected = 0x0000000000000ff0ULL;
    __Vtask_agu_tb__DOT__expect_u64__3__got = vlSelfRef.agu_tb__DOT__effective_address;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__3__name = "disp16 address"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__3__got 
                      != __Vtask_agu_tb__DOT__expect_u64__3__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__3__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__3__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__3__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000300ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000100000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000001000000ULL 
                                      | (0x3ffffffffc7fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__pc_value = 0x0000000000002000ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0x00000000fffffffcULL;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         98);
    __Vtask_agu_tb__DOT__expect_u64__5__expected = 0x0000000000001ffcULL;
    __Vtask_agu_tb__DOT__expect_u64__5__got = vlSelfRef.agu_tb__DOT__effective_address;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__5__name = "pc disp32 address"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__5__got 
                      != __Vtask_agu_tb__DOT__expect_u64__5__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__5__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__5__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__5__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000200ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000600000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (2ULL | (0x3ffffffffffffffcULL 
                                              & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000100000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000800000ULL 
                                      | (0x3ffffffffc7fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__base_reg_value = 0x0000000000001000ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 3ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0x0000000000000020ULL;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         113);
    __Vtask_agu_tb__DOT__expect_u64__7__expected = 0x000000000000102cULL;
    __Vtask_agu_tb__DOT__expect_u64__7__got = vlSelfRef.agu_tb__DOT__effective_address;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__7__name = "indexed address"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__7__got 
                      != __Vtask_agu_tb__DOT__expect_u64__7__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__7__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__7__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__7__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000080000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000500ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000000001000000ULL 
                                      | (0x3ffffffffc7fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__payload_value = 0x00000000fffffff0ULL;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         123);
    __Vtask_agu_tb__DOT__expect_u64__9__expected = 0xfffffffffffffff0ULL;
    __Vtask_agu_tb__DOT__expect_u64__9__got = vlSelfRef.agu_tb__DOT__effective_address;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__9__name = "abs32 address"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__9__got 
                      != __Vtask_agu_tb__DOT__expect_u64__9__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__9__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__9__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__9__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0080000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000600ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__payload_value = 0x0000000000001234ULL;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         131);
    __Vtask_agu_tb__DOT__expect_logic__11__expected = 1U;
    __Vtask_agu_tb__DOT__expect_logic__11__got = vlSelfRef.agu_tb__DOT__valid;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__11__name = "immediate valid"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__11__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__11__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__11__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__11__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__11__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_logic__12__expected = 0U;
    __Vtask_agu_tb__DOT__expect_logic__12__got = vlSelfRef.agu_tb__DOT__address_valid;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__12__name = "immediate address invalid"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__12__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__12__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__12__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__12__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__12__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_u64__13__expected = 0x0000000000001234ULL;
    __Vtask_agu_tb__DOT__expect_u64__13__got = vlSelfRef.agu_tb__DOT__payload_value;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__13__name = "immediate value"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__13__got 
                      != __Vtask_agu_tb__DOT__expect_u64__13__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__13__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__13__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__13__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000200ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000400000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0007000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000200000ULL 
                                      | (0x3fffffffff8fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__base_reg_value = 0x0000000000001000ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         147);
    __Vtask_agu_tb__DOT__expect_logic__15__expected = 1U;
    __Vtask_agu_tb__DOT__expect_logic__15__got = vlSelfRef.agu_tb__DOT__update_write;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__15__name = "preinc update write"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__15__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__15__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__15__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__15__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__15__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_u64__16__expected = 0x0000000000001008ULL;
    __Vtask_agu_tb__DOT__expect_u64__16__got = vlSelfRef.agu_tb__DOT__effective_address;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__16__name = "preinc address"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__16__got 
                      != __Vtask_agu_tb__DOT__expect_u64__16__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__16__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__16__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__16__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_u64__17__expected = 0x0000000000001008ULL;
    __Vtask_agu_tb__DOT__expect_u64__17__got = vlSelfRef.agu_tb__DOT__update_value;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__17__name = "preinc update value"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__17__got 
                      != __Vtask_agu_tb__DOT__expect_u64__17__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__17__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__17__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__17__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000200ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000400000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0007000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000300000ULL 
                                      | (0x3fffffffff8fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__base_reg_value = 0x0000000000001000ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         163);
    __Vtask_agu_tb__DOT__expect_logic__19__expected = 1U;
    __Vtask_agu_tb__DOT__expect_logic__19__got = vlSelfRef.agu_tb__DOT__update_write;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__19__name = "postdec update write"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__19__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__19__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__19__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__19__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__19__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_u64__20__expected = 0x0000000000001000ULL;
    __Vtask_agu_tb__DOT__expect_u64__20__got = vlSelfRef.agu_tb__DOT__effective_address;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__20__name = "postdec address"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__20__got 
                      != __Vtask_agu_tb__DOT__expect_u64__20__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__20__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__20__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__20__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_u64__21__expected = 0x0000000000000ff8ULL;
    __Vtask_agu_tb__DOT__expect_u64__21__got = vlSelfRef.agu_tb__DOT__update_value;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__21__name = "postdec update value"s;
    if (VL_UNLIKELY(((__Vtask_agu_tb__DOT__expect_u64__21__got 
                      != __Vtask_agu_tb__DOT__expect_u64__21__expected)))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:67: Assertion failed in %m: %s got 0x%016x expected 0x%016x\n",6, 'M',vlSymsp->name(),"agu_tb.expect_u64", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_u64__21__name)
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__21__got
                     , '#',64,__Vtask_agu_tb__DOT__expect_u64__21__expected);
        VL_STOP_MT("tb/agu_tb.sv", 67, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    vlSelfRef.agu_tb__DOT__request = 0ULL;
    vlSelfRef.agu_tb__DOT__request = (0x3800000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0008000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__base_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__index_reg_value = 0ULL;
    vlSelfRef.agu_tb__DOT__pc_value = 0ULL;
    vlSelfRef.agu_tb__DOT__sp_value = 0ULL;
    vlSelfRef.agu_tb__DOT__payload_value = 0ULL;
    vlSelfRef.agu_tb__DOT__access_size_bytes = 8U;
    vlSelfRef.agu_tb__DOT__request = (0x0100000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000000200ULL 
                                      | (0x3ffffffffffff8ffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    vlSelfRef.agu_tb__DOT__request = (0x0000400000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0002000000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000800000000000ULL 
                                      | vlSelfRef.agu_tb__DOT__request);
    vlSelfRef.agu_tb__DOT__request = (0x0000000000100000ULL 
                                      | (0x3fffffffff8fffffULL 
                                         & vlSelfRef.agu_tb__DOT__request));
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/agu_tb.sv", 
                                         176);
    __Vtask_agu_tb__DOT__expect_logic__23__expected = 0U;
    __Vtask_agu_tb__DOT__expect_logic__23__got = vlSelfRef.agu_tb__DOT__valid;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__23__name = "invalid update valid"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__23__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__23__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__23__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__23__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__23__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_logic__24__expected = 0U;
    __Vtask_agu_tb__DOT__expect_logic__24__got = vlSelfRef.agu_tb__DOT__update_write;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__24__name = "invalid update write"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__24__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__24__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__24__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__24__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__24__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    __Vtask_agu_tb__DOT__expect_logic__25__expected = 1U;
    __Vtask_agu_tb__DOT__expect_logic__25__got = vlSelfRef.agu_tb__DOT__update_invalid;
    vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__25__name = "invalid update flag"s;
    if (VL_UNLIKELY((((IData)(__Vtask_agu_tb__DOT__expect_logic__25__got) 
                      != (IData)(__Vtask_agu_tb__DOT__expect_logic__25__expected))))) {
        VL_WRITEF_NX("[%0t] %%Error: agu_tb.sv:60: Assertion failed in %m: %s got %0b expected %0b\n",6, 'M',vlSymsp->name(),"agu_tb.expect_logic", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , 'S',&(vlSelfRef.__Vtask_agu_tb__DOT__expect_logic__25__name)
                     , '#',1,(IData)(__Vtask_agu_tb__DOT__expect_logic__25__got)
                     , '#',1,__Vtask_agu_tb__DOT__expect_logic__25__expected);
        VL_STOP_MT("tb/agu_tb.sv", 60, "");
        agu_tb__DOT__failures = ((IData)(1U) + agu_tb__DOT__failures);
    }
    if (VL_UNLIKELY(((0U != agu_tb__DOT__failures)))) {
        VL_WRITEF_NX("[%0t] %%Fatal: agu_tb.sv:182: Assertion failed in %m: agu_tb failed with %0d failure(s)\n",4, 'M',vlSymsp->name(),"agu_tb", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '~',32,agu_tb__DOT__failures);
        VL_STOP_MT("tb/agu_tb.sv", 182, "", false);
    }
    VL_WRITEF_NX("agu_tb PASS\n",0);
    VL_FINISH_MT("tb/agu_tb.sv", 185, "");
    co_return;
}

void Vagu_tb___024root___eval_triggers_vec__act(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_triggers_vec__act\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered[0U] = (QData)((IData)(vlSelfRef.__VdlySched.awaitingCurrentTime()));
}

bool Vagu_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___trigger_anySet__act\n"); );
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

void Vagu_tb___024root___act_sequent__TOP__0(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___act_sequent__TOP__0\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ agu_tb__DOT__dut__DOT__base_value;
    agu_tb__DOT__dut__DOT__base_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__updated_base_value;
    agu_tb__DOT__dut__DOT__updated_base_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__address_base_value;
    agu_tb__DOT__dut__DOT__address_base_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__displacement_value;
    agu_tb__DOT__dut__DOT__displacement_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__absolute_value;
    agu_tb__DOT__dut__DOT__absolute_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__index_value;
    agu_tb__DOT__dut__DOT__index_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__scaled_index_value;
    agu_tb__DOT__dut__DOT__scaled_index_value = 0;
    QData/*63:0*/ agu_tb__DOT__dut__DOT__update_amount;
    agu_tb__DOT__dut__DOT__update_amount = 0;
    CData/*0:0*/ agu_tb__DOT__dut__DOT__update_is_pre;
    agu_tb__DOT__dut__DOT__update_is_pre = 0;
    CData/*0:0*/ agu_tb__DOT__dut__DOT__update_is_dec;
    agu_tb__DOT__dut__DOT__update_is_dec = 0;
    // Body
    vlSelfRef.agu_tb__DOT__update_invalid = (1U & ((IData)(
                                                           (vlSelfRef.agu_tb__DOT__request 
                                                            >> 0x0000002fU)) 
                                                   | ((IData)(
                                                              (vlSelfRef.agu_tb__DOT__request 
                                                               >> 0x00000031U)) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.agu_tb__DOT__access_size_bytes)))));
    vlSelfRef.agu_tb__DOT__valid = (IData)(((0x2008000000000000ULL 
                                             == (0x2008000000000000ULL 
                                                 & vlSelfRef.agu_tb__DOT__request)) 
                                            & (~ ((IData)(
                                                          (vlSelfRef.agu_tb__DOT__request 
                                                           >> 0x0000002fU)) 
                                                  | ((IData)(
                                                             (vlSelfRef.agu_tb__DOT__request 
                                                              >> 0x00000031U)) 
                                                     & (0U 
                                                        == (IData)(vlSelfRef.agu_tb__DOT__access_size_bytes)))))));
    agu_tb__DOT__dut__DOT__base_value = ((1U & (IData)(
                                                       (vlSelfRef.agu_tb__DOT__request 
                                                        >> 0x0000000aU)))
                                          ? ((1U & (IData)(
                                                           (vlSelfRef.agu_tb__DOT__request 
                                                            >> 9U)))
                                              ? 0ULL
                                              : ((1U 
                                                  & (IData)(
                                                            (vlSelfRef.agu_tb__DOT__request 
                                                             >> 8U)))
                                                  ? 0ULL
                                                  : vlSelfRef.agu_tb__DOT__sp_value))
                                          : ((1U & (IData)(
                                                           (vlSelfRef.agu_tb__DOT__request 
                                                            >> 9U)))
                                              ? ((1U 
                                                  & (IData)(
                                                            (vlSelfRef.agu_tb__DOT__request 
                                                             >> 8U)))
                                                  ? vlSelfRef.agu_tb__DOT__pc_value
                                                  : vlSelfRef.agu_tb__DOT__base_reg_value)
                                              : ((1U 
                                                  & (IData)(
                                                            (vlSelfRef.agu_tb__DOT__request 
                                                             >> 8U)))
                                                  ? vlSelfRef.agu_tb__DOT__base_reg_value
                                                  : 0ULL)));
    if ((1U & (IData)((vlSelfRef.agu_tb__DOT__request 
                       >> 0x0000002cU)))) {
        vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words 
            = (7U & (IData)((vlSelfRef.agu_tb__DOT__request 
                             >> 0x00000017U)));
        vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value 
            = vlSelfRef.agu_tb__DOT__payload_value;
        vlSelfRef.agu_tb__DOT__dut__DOT____VlemCall_0__sign_extend_payload 
            = ((0U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words))
                ? 0ULL : ((1U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words))
                           ? (((- (QData)((IData)((1U 
                                                   & (IData)(
                                                             (vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value 
                                                              >> 0x0fU)))))) 
                               << 0x00000010U) | (QData)((IData)(
                                                                 (0x0000ffffU 
                                                                  & (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value)))))
                           : ((2U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words))
                               ? (((QData)((IData)(
                                                   (- (IData)(
                                                              (1U 
                                                               & (IData)(
                                                                         (vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value 
                                                                          >> 0x1fU))))))) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value)))
                               : vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value)));
        if ((1U & (~ VL_ONEHOT_I((((2U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words)) 
                                   << 2U) | (((1U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words)) 
                                              << 1U) 
                                             | (0U 
                                                == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words)))))))) {
            if ((0U != (((2U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words)) 
                         << 2U) | (((1U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words)) 
                                    << 1U) | (0U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: bedrock_agu.sv:41: Assertion failed in %m: unique case, but multiple matches found for '3'h%X'\n",4, 'M',vlSymsp->name(),"agu_tb.dut.sign_extend_payload", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',3,(IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words));
                    VL_STOP_MT("execute/bedrock_agu.sv", 41, "");
                }
            }
        }
        vlSelfRef.agu_tb__DOT__dut__DOT____VlemCond_1 
            = vlSelfRef.agu_tb__DOT__dut__DOT____VlemCall_0__sign_extend_payload;
    } else {
        vlSelfRef.agu_tb__DOT__dut__DOT____VlemCond_1 = 0ULL;
    }
    agu_tb__DOT__dut__DOT__displacement_value = vlSelfRef.agu_tb__DOT__dut__DOT____VlemCond_1;
    if ((1U & (IData)((vlSelfRef.agu_tb__DOT__request 
                       >> 0x0000002bU)))) {
        vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words 
            = (7U & (IData)((vlSelfRef.agu_tb__DOT__request 
                             >> 0x00000017U)));
        vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value 
            = vlSelfRef.agu_tb__DOT__payload_value;
        vlSelfRef.agu_tb__DOT__dut__DOT____VlemCall_2__sign_extend_payload 
            = ((0U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words))
                ? 0ULL : ((1U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words))
                           ? (((- (QData)((IData)((1U 
                                                   & (IData)(
                                                             (vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value 
                                                              >> 0x0fU)))))) 
                               << 0x00000010U) | (QData)((IData)(
                                                                 (0x0000ffffU 
                                                                  & (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value)))))
                           : ((2U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words))
                               ? (((QData)((IData)(
                                                   (- (IData)(
                                                              (1U 
                                                               & (IData)(
                                                                         (vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value 
                                                                          >> 0x1fU))))))) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value)))
                               : vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value)));
        if ((1U & (~ VL_ONEHOT_I((((2U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words)) 
                                   << 2U) | (((1U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words)) 
                                              << 1U) 
                                             | (0U 
                                                == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words)))))))) {
            if ((0U != (((2U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words)) 
                         << 2U) | (((1U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words)) 
                                    << 1U) | (0U == (IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: bedrock_agu.sv:41: Assertion failed in %m: unique case, but multiple matches found for '3'h%X'\n",4, 'M',vlSymsp->name(),"agu_tb.dut.sign_extend_payload", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',3,(IData)(vlSelfRef.__Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words));
                    VL_STOP_MT("execute/bedrock_agu.sv", 41, "");
                }
            }
        }
        vlSelfRef.agu_tb__DOT__dut__DOT____VlemCond_3 
            = vlSelfRef.agu_tb__DOT__dut__DOT____VlemCall_2__sign_extend_payload;
    } else {
        vlSelfRef.agu_tb__DOT__dut__DOT____VlemCond_3 = 0ULL;
    }
    agu_tb__DOT__dut__DOT__absolute_value = vlSelfRef.agu_tb__DOT__dut__DOT____VlemCond_3;
    agu_tb__DOT__dut__DOT__index_value = ((1U & (IData)(
                                                        (vlSelfRef.agu_tb__DOT__request 
                                                         >> 0x00000035U)))
                                           ? (((QData)((IData)(
                                                               (- (IData)(
                                                                          (1U 
                                                                           & (IData)(
                                                                                (vlSelfRef.agu_tb__DOT__index_reg_value 
                                                                                >> 0x1fU))))))) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.agu_tb__DOT__index_reg_value)))
                                           : vlSelfRef.agu_tb__DOT__index_reg_value);
    agu_tb__DOT__dut__DOT__scaled_index_value = ((1U 
                                                  & (IData)(
                                                            (vlSelfRef.agu_tb__DOT__request 
                                                             >> 0x0000002dU)))
                                                  ? 
                                                 (agu_tb__DOT__dut__DOT__index_value 
                                                  << 
                                                  (3U 
                                                   & (IData)(vlSelfRef.agu_tb__DOT__request)))
                                                  : 0ULL);
    agu_tb__DOT__dut__DOT__update_amount = (QData)((IData)(vlSelfRef.agu_tb__DOT__access_size_bytes));
    agu_tb__DOT__dut__DOT__update_is_pre = ((2U == 
                                             (7U & (IData)(
                                                           (vlSelfRef.agu_tb__DOT__request 
                                                            >> 0x00000014U)))) 
                                            | (4U == 
                                               (7U 
                                                & (IData)(
                                                          (vlSelfRef.agu_tb__DOT__request 
                                                           >> 0x00000014U)))));
    agu_tb__DOT__dut__DOT__update_is_dec = ((3U == 
                                             (7U & (IData)(
                                                           (vlSelfRef.agu_tb__DOT__request 
                                                            >> 0x00000014U)))) 
                                            | (4U == 
                                               (7U 
                                                & (IData)(
                                                          (vlSelfRef.agu_tb__DOT__request 
                                                           >> 0x00000014U)))));
    agu_tb__DOT__dut__DOT__updated_base_value = ((IData)(agu_tb__DOT__dut__DOT__update_is_dec)
                                                  ? 
                                                 (agu_tb__DOT__dut__DOT__base_value 
                                                  - agu_tb__DOT__dut__DOT__update_amount)
                                                  : 
                                                 (agu_tb__DOT__dut__DOT__base_value 
                                                  + agu_tb__DOT__dut__DOT__update_amount));
    agu_tb__DOT__dut__DOT__address_base_value = ((IData)(agu_tb__DOT__dut__DOT__update_is_pre)
                                                  ? agu_tb__DOT__dut__DOT__updated_base_value
                                                  : agu_tb__DOT__dut__DOT__base_value);
    vlSelfRef.agu_tb__DOT__effective_address = ((1U 
                                                 & (IData)(
                                                           (vlSelfRef.agu_tb__DOT__request 
                                                            >> 0x0000002bU)))
                                                 ? agu_tb__DOT__dut__DOT__absolute_value
                                                 : 
                                                ((agu_tb__DOT__dut__DOT__address_base_value 
                                                  + agu_tb__DOT__dut__DOT__scaled_index_value) 
                                                 + agu_tb__DOT__dut__DOT__displacement_value));
    vlSelfRef.agu_tb__DOT__update_value = ((1U & (IData)(
                                                         (vlSelfRef.agu_tb__DOT__request 
                                                          >> 0x00000031U)))
                                            ? agu_tb__DOT__dut__DOT__updated_base_value
                                            : agu_tb__DOT__dut__DOT__base_value);
    vlSelfRef.agu_tb__DOT__address_valid = ((IData)(
                                                    (vlSelfRef.agu_tb__DOT__request 
                                                     >> 0x00000038U)) 
                                            & (IData)(vlSelfRef.agu_tb__DOT__valid));
    vlSelfRef.agu_tb__DOT__update_write = ((IData)(
                                                   (vlSelfRef.agu_tb__DOT__request 
                                                    >> 0x00000031U)) 
                                           & (IData)(vlSelfRef.agu_tb__DOT__valid));
}

void Vagu_tb___024root___eval_act(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_act\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        Vagu_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

void Vagu_tb___024root___eval_nba(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_nba\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vagu_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

void Vagu_tb___024root___timing_resume(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___timing_resume\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Vagu_tb___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vagu_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vagu_tb___024root___eval_phase__act(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_phase__act\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    Vagu_tb___024root___eval_triggers_vec__act(vlSelf);
    Vagu_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vagu_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vagu_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vagu_tb___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Vagu_tb___024root___timing_resume(vlSelf);
        Vagu_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vagu_tb___024root___eval_phase__inact(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_phase__inact\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("tb/agu_tb.sv", 4, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vagu_tb___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vagu_tb___024root___eval_phase__nba(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_phase__nba\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vagu_tb___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vagu_tb___024root___eval_nba(vlSelf);
        Vagu_tb___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vagu_tb___024root___eval(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vagu_tb___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("tb/agu_tb.sv", 4, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("tb/agu_tb.sv", 4, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vagu_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("tb/agu_tb.sv", 4, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vagu_tb___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vagu_tb___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vagu_tb___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vagu_tb___024root___eval_debug_assertions(Vagu_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vagu_tb___024root___eval_debug_assertions\n"); );
    Vagu_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
