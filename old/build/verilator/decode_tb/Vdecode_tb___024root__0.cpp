// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vdecode_tb.h for the primary calling header

#include "Vdecode_tb__pch.h"

VlCoroutine Vdecode_tb___024root___eval_initial__TOP__Vtiming__0(Vdecode_tb___024root* vlSelf);

void Vdecode_tb___024root___eval_initial(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_initial\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vdecode_tb___024root___eval_initial__TOP__Vtiming__0(vlSelf);
}

VlCoroutine Vdecode_tb___024root___eval_initial__TOP__Vtiming__0(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ decode_tb__DOT__failures;
    decode_tb__DOT__failures = 0;
    SData/*11:0*/ __Vtask_decode_tb__DOT__check_decode__0__payload;
    __Vtask_decode_tb__DOT__check_decode__0__payload = 0;
    SData/*15:0*/ __Vtask_decode_tb__DOT__check_decode__0__ext_word;
    __Vtask_decode_tb__DOT__check_decode__0__ext_word = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__0__expected_valid;
    __Vtask_decode_tb__DOT__check_decode__0__expected_valid = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__0__expected_extended;
    __Vtask_decode_tb__DOT__check_decode__0__expected_extended = 0;
    SData/*11:0*/ __Vtask_decode_tb__DOT__check_decode__1__payload;
    __Vtask_decode_tb__DOT__check_decode__1__payload = 0;
    SData/*15:0*/ __Vtask_decode_tb__DOT__check_decode__1__ext_word;
    __Vtask_decode_tb__DOT__check_decode__1__ext_word = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__1__expected_valid;
    __Vtask_decode_tb__DOT__check_decode__1__expected_valid = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__1__expected_extended;
    __Vtask_decode_tb__DOT__check_decode__1__expected_extended = 0;
    SData/*11:0*/ __Vtask_decode_tb__DOT__check_decode__2__payload;
    __Vtask_decode_tb__DOT__check_decode__2__payload = 0;
    SData/*15:0*/ __Vtask_decode_tb__DOT__check_decode__2__ext_word;
    __Vtask_decode_tb__DOT__check_decode__2__ext_word = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__2__expected_valid;
    __Vtask_decode_tb__DOT__check_decode__2__expected_valid = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__2__expected_extended;
    __Vtask_decode_tb__DOT__check_decode__2__expected_extended = 0;
    SData/*11:0*/ __Vtask_decode_tb__DOT__check_decode__3__payload;
    __Vtask_decode_tb__DOT__check_decode__3__payload = 0;
    SData/*15:0*/ __Vtask_decode_tb__DOT__check_decode__3__ext_word;
    __Vtask_decode_tb__DOT__check_decode__3__ext_word = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__3__expected_valid;
    __Vtask_decode_tb__DOT__check_decode__3__expected_valid = 0;
    CData/*0:0*/ __Vtask_decode_tb__DOT__check_decode__3__expected_extended;
    __Vtask_decode_tb__DOT__check_decode__3__expected_extended = 0;
    // Body
    decode_tb__DOT__failures = 0U;
    __Vtask_decode_tb__DOT__check_decode__0__expected_extended = 0U;
    __Vtask_decode_tb__DOT__check_decode__0__expected_valid = 1U;
    __Vtask_decode_tb__DOT__check_decode__0__ext_word = 0U;
    __Vtask_decode_tb__DOT__check_decode__0__payload = 0U;
    vlSelfRef.decode_tb__DOT__primary_payload = 0U;
    vlSelfRef.decode_tb__DOT__extension_word = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/decode_tb.sv", 
                                         40);
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__valid) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__0__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:42: Assertion failed in %m: payload=%03h ext=%04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__0__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__0__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__valid)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__0__expected_valid);
        VL_STOP_MT("tb/decode_tb.sv", 42, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__needs_extension) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__0__expected_extended))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:46: Assertion failed in %m: payload=%03h ext=%04h extended got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__0__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__0__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__needs_extension)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__0__expected_extended);
        VL_STOP_MT("tb/decode_tb.sv", 46, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    __Vtask_decode_tb__DOT__check_decode__1__expected_extended = 0U;
    __Vtask_decode_tb__DOT__check_decode__1__expected_valid = 1U;
    __Vtask_decode_tb__DOT__check_decode__1__ext_word = 0U;
    __Vtask_decode_tb__DOT__check_decode__1__payload = 0x0fffU;
    vlSelfRef.decode_tb__DOT__primary_payload = __Vtask_decode_tb__DOT__check_decode__1__payload;
    vlSelfRef.decode_tb__DOT__extension_word = __Vtask_decode_tb__DOT__check_decode__1__ext_word;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/decode_tb.sv", 
                                         40);
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__valid) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__1__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:42: Assertion failed in %m: payload=%03h ext=%04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__1__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__1__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__valid)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__1__expected_valid);
        VL_STOP_MT("tb/decode_tb.sv", 42, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__needs_extension) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__1__expected_extended))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:46: Assertion failed in %m: payload=%03h ext=%04h extended got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__1__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__1__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__needs_extension)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__1__expected_extended);
        VL_STOP_MT("tb/decode_tb.sv", 46, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    __Vtask_decode_tb__DOT__check_decode__2__expected_extended = 1U;
    __Vtask_decode_tb__DOT__check_decode__2__expected_valid = 1U;
    __Vtask_decode_tb__DOT__check_decode__2__ext_word = 0x0104U;
    __Vtask_decode_tb__DOT__check_decode__2__payload = 0x0f31U;
    vlSelfRef.decode_tb__DOT__primary_payload = __Vtask_decode_tb__DOT__check_decode__2__payload;
    vlSelfRef.decode_tb__DOT__extension_word = __Vtask_decode_tb__DOT__check_decode__2__ext_word;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/decode_tb.sv", 
                                         40);
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__valid) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__2__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:42: Assertion failed in %m: payload=%03h ext=%04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__2__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__2__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__valid)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__2__expected_valid);
        VL_STOP_MT("tb/decode_tb.sv", 42, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__needs_extension) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__2__expected_extended))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:46: Assertion failed in %m: payload=%03h ext=%04h extended got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__2__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__2__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__needs_extension)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__2__expected_extended);
        VL_STOP_MT("tb/decode_tb.sv", 46, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    __Vtask_decode_tb__DOT__check_decode__3__expected_extended = 1U;
    __Vtask_decode_tb__DOT__check_decode__3__expected_valid = 0U;
    __Vtask_decode_tb__DOT__check_decode__3__ext_word = 0x0118U;
    __Vtask_decode_tb__DOT__check_decode__3__payload = 0x0f31U;
    vlSelfRef.decode_tb__DOT__primary_payload = __Vtask_decode_tb__DOT__check_decode__3__payload;
    vlSelfRef.decode_tb__DOT__extension_word = __Vtask_decode_tb__DOT__check_decode__3__ext_word;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "tb/decode_tb.sv", 
                                         40);
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__valid) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__3__expected_valid))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:42: Assertion failed in %m: payload=%03h ext=%04h valid got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__3__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__3__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__valid)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__3__expected_valid);
        VL_STOP_MT("tb/decode_tb.sv", 42, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    if (VL_UNLIKELY((((IData)(vlSelfRef.decode_tb__DOT__needs_extension) 
                      != (IData)(__Vtask_decode_tb__DOT__check_decode__3__expected_extended))))) {
        VL_WRITEF_NX("[%0t] %%Error: decode_tb.sv:46: Assertion failed in %m: payload=%03h ext=%04h extended got %0b expected %0b\n",7, 'M',vlSymsp->name(),"decode_tb.check_decode", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '#',12,(IData)(__Vtask_decode_tb__DOT__check_decode__3__payload)
                     , '#',16,__Vtask_decode_tb__DOT__check_decode__3__ext_word
                     , '#',1,(IData)(vlSelfRef.decode_tb__DOT__needs_extension)
                     , '#',1,__Vtask_decode_tb__DOT__check_decode__3__expected_extended);
        VL_STOP_MT("tb/decode_tb.sv", 46, "");
        decode_tb__DOT__failures = ((IData)(1U) + decode_tb__DOT__failures);
    }
    if (VL_UNLIKELY(((0U != decode_tb__DOT__failures)))) {
        VL_WRITEF_NX("[%0t] %%Fatal: decode_tb.sv:61: Assertion failed in %m: decode_tb failed with %0d failure(s)\n",4, 'M',vlSymsp->name(),"decode_tb", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000)
                     , '~',32,decode_tb__DOT__failures);
        VL_STOP_MT("tb/decode_tb.sv", 61, "", false);
    }
    VL_WRITEF_NX("decode_tb PASS\n",0);
    VL_FINISH_MT("tb/decode_tb.sv", 64, "");
    co_return;
}

void Vdecode_tb___024root___eval_triggers_vec__act(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_triggers_vec__act\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered[0U] = (QData)((IData)(vlSelfRef.__VdlySched.awaitingCurrentTime()));
}

bool Vdecode_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___trigger_anySet__act\n"); );
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

void Vdecode_tb___024root___act_sequent__TOP__0(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___act_sequent__TOP__0\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*6:0*/ decode_tb__DOT__field_format_id;
    decode_tb__DOT__field_format_id = 0;
    CData/*3:0*/ decode_tb__DOT__required_words;
    decode_tb__DOT__required_words = 0;
    IData/*26:0*/ decode_tb__DOT__dut__DOT__primary_decode;
    decode_tb__DOT__dut__DOT__primary_decode = 0;
    IData/*20:0*/ decode_tb__DOT__dut__DOT__extended_decode;
    decode_tb__DOT__dut__DOT__extended_decode = 0;
    CData/*3:0*/ decode_tb__DOT__dut__DOT__field_format_token_words;
    decode_tb__DOT__dut__DOT__field_format_token_words = 0;
    IData/*26:0*/ __Vfunc_bedrock_decode_primary_payload__4__Vfuncout;
    __Vfunc_bedrock_decode_primary_payload__4__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_primary_payload__4__payload;
    __Vfunc_bedrock_decode_primary_payload__4__payload = 0;
    IData/*26:0*/ __Vfunc_bedrock_decode_primary_payload__4__r;
    __Vfunc_bedrock_decode_primary_payload__4__r = 0;
    // Body
    __Vfunc_bedrock_decode_primary_payload__4__payload 
        = vlSelfRef.decode_tb__DOT__primary_payload;
    __Vfunc_bedrock_decode_primary_payload__4__r = 0U;
    __Vfunc_bedrock_decode_primary_payload__4__r = 
        (0x00000040U | (0x06000001U & __Vfunc_bedrock_decode_primary_payload__4__r));
    if ((0x00000800U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                        if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                            if ((2U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                                if (
                                                    (1U 
                                                     & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                                        = 
                                                        (0x04000000U 
                                                         | __Vfunc_bedrock_decode_primary_payload__4__r);
                                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                                        = 
                                                        (0x00e20000U 
                                                         | (0x060003ffU 
                                                            & __Vfunc_bedrock_decode_primary_payload__4__r));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__4__payload) 
                                      >> 5U)))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__4__payload) 
                                              >> 3U)))) {
                                    if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                            if ((1U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                                    = 
                                                    (0x06000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__4__r);
                                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                                    = 
                                                    (0x00000014U 
                                                     | (0x07ffffc1U 
                                                        & __Vfunc_bedrock_decode_primary_payload__4__r));
                                            } else {
                                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                                    = 
                                                    (0x06000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__4__r);
                                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                                    = 
                                                    (0x00000010U 
                                                     | (0x07ffffc1U 
                                                        & __Vfunc_bedrock_decode_primary_payload__4__r));
                                            }
                                        } else if (
                                                   (1U 
                                                    & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__4__r);
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x00000012U 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__4__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__4__r);
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x0000002cU 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__4__r));
                                        }
                                    } else if ((2U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__4__r);
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x00000028U 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__4__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__4__r);
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x0000002aU 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__4__r));
                                        }
                                    } else if ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__4__r);
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (4U | 
                                               (0x07ffffc1U 
                                                & __Vfunc_bedrock_decode_primary_payload__4__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__4__r);
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (2U | 
                                               (0x07ffffc1U 
                                                & __Vfunc_bedrock_decode_primary_payload__4__r));
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x06000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (6U | (0x07ffffc1U 
                                             & __Vfunc_bedrock_decode_primary_payload__4__r));
                            }
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__4__payload) 
                                                  >> 1U)))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__4__r);
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (8U 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__4__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x06000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__4__r);
                                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                                = (0x0000000eU 
                                                   | (0x07ffffc1U 
                                                      & __Vfunc_bedrock_decode_primary_payload__4__r));
                                        }
                                    }
                                } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__4__r);
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x0000000cU 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__4__r);
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x0000000aU 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__4__r);
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x0000001eU 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__4__r);
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x0000001cU 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                                }
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__4__r);
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x0000001aU 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x06000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__4__r);
                                        __Vfunc_bedrock_decode_primary_payload__4__r 
                                            = (0x00000018U 
                                               | (0x07ffffc1U 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__4__r);
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x00000024U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__4__r);
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x00000026U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                                }
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__4__r);
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x00000022U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x06000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__4__r);
                                    __Vfunc_bedrock_decode_primary_payload__4__r 
                                        = (0x00000020U 
                                           | (0x07ffffc1U 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                                }
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x06000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x00000016U 
                                       | (0x07ffffc1U 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x01820080U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x010e0540U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x002c0c00U | (0x060003ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        }
                    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x002c0400U | (0x060003ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x012e0400U | (0x060003ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        }
                    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x012e0c00U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x013a0400U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                    }
                } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x01a23880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x012a3880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            }
                        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x00f47880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x00f47880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x00f47880U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x019e0080U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x04000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__4__r);
                                __Vfunc_bedrock_decode_primary_payload__4__r 
                                    = (0x00f61c80U 
                                       | (0x0600003fU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x00f47880U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x00f47880U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x00f47880U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x019c0080U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                            __Vfunc_bedrock_decode_primary_payload__4__r 
                                = (0x00f61c80U | (0x0600003fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__4__r));
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x01283000U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                        __Vfunc_bedrock_decode_primary_payload__4__r 
                            = (0x01243000U | (0x060003ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__4__r));
                    }
                } else {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x00528400U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
                }
            } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x01a28c00U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
                } else {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x017e8c00U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
                }
            } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x01708c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
            } else {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x012a8c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x010ea000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
        }
    } else if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x010ea000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x00328c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
            } else {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x000a8c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
            }
        } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x00e63000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x003e3000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x00548800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x00548800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
        }
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x00023000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                    __Vfunc_bedrock_decode_primary_payload__4__r 
                        = (0x00e43000U | (0x060003ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__4__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x004e8800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x004e8800U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
        }
    } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x00068c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x00503400U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x003c3000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x000a3880U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (1U | __Vfunc_bedrock_decode_primary_payload__4__r);
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x013a0c00U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x01140080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
                __Vfunc_bedrock_decode_primary_payload__4__r 
                    = (0x01120080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
            }
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x01320080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x013c0080U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x01540000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
            __Vfunc_bedrock_decode_primary_payload__4__r 
                = (0x00260140U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
        }
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__4__payload))) {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x002600c0U | (0x0600003fU & __Vfunc_bedrock_decode_primary_payload__4__r));
    } else {
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x04000000U | __Vfunc_bedrock_decode_primary_payload__4__r);
        __Vfunc_bedrock_decode_primary_payload__4__r 
            = (0x00e00000U | (0x060003ffU & __Vfunc_bedrock_decode_primary_payload__4__r));
    }
    __Vfunc_bedrock_decode_primary_payload__4__Vfuncout 
        = __Vfunc_bedrock_decode_primary_payload__4__r;
    decode_tb__DOT__dut__DOT__primary_decode = __Vfunc_bedrock_decode_primary_payload__4__Vfuncout;
    decode_tb__DOT__dut__DOT__extended_decode = 0U;
    decode_tb__DOT__dut__DOT__extended_decode = (0x0010001fU 
                                                 & decode_tb__DOT__dut__DOT__extended_decode);
    decode_tb__DOT__dut__DOT__field_format_token_words = 1U;
    vlSelfRef.decode_tb__DOT__valid = (1U & (decode_tb__DOT__dut__DOT__primary_decode 
                                             >> 0x0000001aU));
    vlSelfRef.decode_tb__DOT__needs_extension = (1U 
                                                 & (decode_tb__DOT__dut__DOT__primary_decode 
                                                    >> 0x00000019U));
    decode_tb__DOT__field_format_id = (0x0000007fU 
                                       & (decode_tb__DOT__dut__DOT__primary_decode 
                                          >> 0x0000000aU));
    decode_tb__DOT__required_words = (0x0000000fU & 
                                      (decode_tb__DOT__dut__DOT__primary_decode 
                                       >> 6U));
    if ((0x02000000U & decode_tb__DOT__dut__DOT__primary_decode)) {
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word 
            = vlSelfRef.decode_tb__DOT__extension_word;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root 
            = (0x0000001fU & (decode_tb__DOT__dut__DOT__primary_decode 
                              >> 1U));
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
            = (4U | (0x00100001U & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root)))) {
                            if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001250a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            }
                            if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                                if ((0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                                    if (VL_UNLIKELY((
                                                     vlSymsp->_vm_contextp__->assertOn()))) {
                                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2657: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2657, "");
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                        if (((((((((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                   | (1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                  | (2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                 | (8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                                | (0x0010U == (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                               | (0x0040U == (0xffc0U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                              | (0x0080U == (0xffc0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                             | (0x00c0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0xbc00U : 
                                       ((1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                         ? 0xba0aU : 
                                        ((2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                          ? 0x8400U
                                          : ((8U == 
                                              (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                              ? 0xdd04U
                                              : ((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                  ? 0xd284U
                                                  : 
                                                 ((0x0040U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                   ? 0xbb85U
                                                   : 
                                                  ((0x0080U 
                                                    == 
                                                    (0xffc0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                    ? 0xdd8fU
                                                    : 0xba85U))))))) 
                                      << 5U));
                        } else if ((0x0100U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001c70a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x0140U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001500a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x0180U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001760a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x01c0U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001bc0a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x0200U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x0019b0a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x0240U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x0019c0a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x0280U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001c40a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (((((0x0280U 
                                                        == 
                                                        (0xffc0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                       << 3U) 
                                                      | ((0x0240U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                         << 2U)) 
                                                     | (((0x0200U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                         << 1U) 
                                                        | (0x01c0U 
                                                           == 
                                                           (0xffc0U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                                    << 0x0000000bU) 
                                                   | (((((0x0180U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0140U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0100U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                           << 1U) 
                                                          | (0x00c0U 
                                                             == 
                                                             (0xffc0U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                                      << 7U)) 
                                                  | ((((((0x0080U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0040U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0010U 
                                                            == 
                                                            (0xfff8U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                           << 1U) 
                                                          | (8U 
                                                             == 
                                                             (0xfff8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                                      << 3U) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                                         << 2U) 
                                                        | (((1U 
                                                             == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                                            << 1U) 
                                                           | (0U 
                                                              == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))))) {
                            if ((0U != (((((((0x0280U 
                                              == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                             << 3U) 
                                            | ((0x0240U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 2U)) 
                                           | (((0x0200U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 1U) 
                                              | (0x01c0U 
                                                 == 
                                                 (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                          << 0x0000000bU) 
                                         | (((((0x0180U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 3U) 
                                              | ((0x0140U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0100U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 1U) 
                                                | (0x00c0U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                            << 7U)) 
                                        | ((((((0x0080U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 3U) 
                                              | ((0x0040U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 1U) 
                                                | (8U 
                                                   == 
                                                   (0xfff8U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                            << 3U) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                               << 2U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                                  << 1U) 
                                                 | (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2576: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2576, "");
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                         >> 0x0000000fU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                      >> 0x0000000eU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                          >> 0x0000000dU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                              >> 0x0000000cU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                  >> 0x0000000bU)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                    >> 0x0000000aU)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                     >> 9U)))) {
                                                if (
                                                    (0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                             >> 7U)))) {
                                                        if (
                                                            (0x00000040U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                                     >> 5U)))) {
                                                                if (
                                                                    (0x00000010U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                                                    if (
                                                                        (8U 
                                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                                            = 
                                                                            (0x001ca080U 
                                                                             | (0x0000001fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                                                    } else if (
                                                                               (1U 
                                                                                & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                                                >> 2U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                                                >> 1U)))) {
                                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                                                = 
                                                                                ((0x0000001fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                                                                | (((1U 
                                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                                 ? 0xe900U
                                                                                 : 0xe300U) 
                                                                                << 5U));
                                                                        }
                                                                    }
                                                                } else {
                                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                                        = 
                                                                        ((0x0000001fU 
                                                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                                                         | (((8U 
                                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                              ? 0xd213U
                                                                              : 0xd184U) 
                                                                            << 5U));
                                                                }
                                                            }
                                                        } else {
                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                                = 
                                                                (0x001a90a0U 
                                                                 | (0x0000001fU 
                                                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                                        }
                                                    }
                                                } else {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                        = 
                                                        ((0x0000001fU 
                                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                                         | (((0x00000080U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                              ? 
                                                             ((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                               ? 0xd885U
                                                               : 0xe591U)
                                                              : 
                                                             ((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                               ? 0xd31cU
                                                               : 
                                                              ((0x00000020U 
                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                ? 
                                                               ((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                  ? 0x8d84U
                                                                  : 
                                                                 ((4U 
                                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                   ? 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                     ? 0xe280U
                                                                     : 0xdf00U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                     ? 0xde80U
                                                                     : 0xd680U))
                                                                   : 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                     ? 0xd400U
                                                                     : 0xc980U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                     ? 0xbc80U
                                                                     : 0x8200U))))
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                  ? 0xe604U
                                                                  : 0xd384U))
                                                                : 
                                                               ((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                                  ? 0xe484U
                                                                  : 0xd104U)
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
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
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    if ((0x00001000U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                    >> 0x0000000bU)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                = (0x00191560U 
                                                   | (0x0000001fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = ((0x0000001fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                               | (((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc8abU
                                                    : 0xc82bU) 
                                                  << 5U));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = ((0x0000001fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                           | (((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc82bU
                                                    : 0xc7abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc7abU
                                                    : 0xc72bU)) 
                                              << 5U));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = ((0x0000001fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                       | (((0x00002000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc72bU
                                                    : 0xc6abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc6abU
                                                    : 0xc32bU))
                                            : ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc32bU
                                                    : 0xc2abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xc2abU
                                                    : 0x91abU))) 
                                          << 5U));
                            }
                        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00121720U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = ((0x0000001fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0x91abU
                                            : 0x912bU) 
                                          << 5U));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00122560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                 >> 0x0000000aU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                         >> 5U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                             >> 4U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                                 >> 3U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                                     >> 2U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                                            = 
                                                                            (0x00120740U 
                                                                             | (0x0000001fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
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
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x8aabU : 0x8a2bU) 
                                      << 5U));
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00180720U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x0018c720U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x4000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))) {
                            if ((0U != (((0x4000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                         << 1U) | (0U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2308: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2308, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0010d720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0010e720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0010f720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00110720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2282: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2282, "");
                            }
                        }
                    }
                } else {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00109720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0010a720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0010b720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0010c720U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2256: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2256, "");
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001b65c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001b75c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001b05c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x8000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 2U) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                            if ((0U != (((0x8000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                         << 2U) | (
                                                   ((0x4000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xc000U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2235: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2235, "");
                                }
                            }
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x0019f5c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001a05c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001ae5c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0xc000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001af5c0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   ((0xc000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                    << 3U) 
                                                   | ((0x8000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                      << 2U)) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                            if ((0U != ((((0xc000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                          << 3U) | 
                                         ((0x8000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                          << 2U)) | 
                                        (((0x4000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                          << 1U) | 
                                         (0U == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2209: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2209, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001065c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001075c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001115c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001125c0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2183: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2183, "");
                            }
                        }
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                      >> 0x0000000dU)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0xdbabU
                                            : 0xdb2bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0xd82bU
                                            : 0xd7abU)) 
                                      << 5U));
                        }
                    }
                } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001ae560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                  >> 8U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001b74c0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = ((0x0000001fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                       | (((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? 0xdb26U
                                                : 0xd826U)
                                            : ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? 0xd7a6U
                                                : 0xd726U)) 
                                          << 5U));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001ab560U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0xd02bU : 0xcfabU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0xcc2bU : 0x8eabU)) 
                                  << 5U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x8e2bU : 0x8c2bU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x8babU : 0x892bU))
                                : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x88abU : 0x83abU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x832bU : 
                                       ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                         ? ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                 ? 0xd5a6U
                                                 : 0xd026U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                 ? 0xcfa6U
                                                 : 0xcb15U))
                                         : ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                 ? 0x8926U
                                                 : 0x88a6U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                 ? 0x83a6U
                                                 : 0x8326U)))))) 
                              << 5U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    if ((0x00000800U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001d1560U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001d1560U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    }
                                } else if ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001bf560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001bf560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else if ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001b8560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001b8560U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001b2560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            }
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001ac560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001b8280U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    } else if ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                         >> 5U)))) {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                        = 
                                                        (0x001b9480U 
                                                         | (0x0000001fU 
                                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                                }
                                            }
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001ac4c0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00195560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00195560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00184560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0xc22bU : 0xc1abU) 
                                      << 5U));
                        }
                    } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0xc1abU
                                            : 0xc12bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0xc12bU
                                            : 0xc0abU)) 
                                      << 5U));
                        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00181560U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x0012a540U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x0012a540U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00000200U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? ((0x00000100U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0xca15U
                                            : 0xc915U)
                                        : ((0x00000100U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? 0xb995U
                                            : 0xb915U)) 
                                      << 5U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00129520U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x00129520U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else if ((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001282c0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001282c0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00127540U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00127540U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00126520U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00126520U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00119560U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00119560U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00105560U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00000100U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x8f95U : 0x8f15U) 
                                      << 5U));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00119280U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00103280U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001264a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001160a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001b93e0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                          >> 3U)))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                = (0x001d16a0U 
                                                   | (0x0000001fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                = (1U 
                                                   | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                        }
                                    }
                                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001bf6a0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x001b86a0U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001b26a0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001956a0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x0012b300U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x0012a620U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x00129600U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x00128300U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x00127620U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x00126600U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001196a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00119640U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001056a0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x001055e0U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001036a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001035e0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001035e0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x001026a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001025e0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001012a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                     >> 0x0000000fU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                          >> 0x0000000cU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                              >> 0x0000000bU)))) {
                                    if ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                    >> 9U)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                                = (0x0016d680U 
                                                   | (0x0000001fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = ((0x0000001fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                               | (((0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xb534U
                                                    : 0xb4b4U) 
                                                  << 5U));
                                    }
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xb434U
                                                    : 0xb2b4U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xb234U
                                                    : 0xb1b4U))
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xa7b4U
                                                    : 0xa734U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xa6b4U
                                                    : 0xa634U)))
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                            ? ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0xa334U
                                                    : 0xa2b4U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0x9e34U
                                                    : 0x9db4U))
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0x98b4U
                                                    : 0x9834U)
                                                : (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                    ? 0x97b4U
                                                    : 0x96b4U)))) 
                                      << 5U));
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                if (((((((((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                           | (0x0200U == (0xffe0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                          | (0x0220U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                         | (0x0280U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                        | (0x0300U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                       | (0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                      | (0x0600U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                     | (0x0680U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00139680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else if ((0x0200U == (0xffe0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0016b340U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else if ((0x0220U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00157360U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x0280U == (0xff80U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0013d200U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else if ((0x0300U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001374e0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x0400U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00155680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else if ((0x0600U == (0xff80U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0013d200U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0013e200U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    }
                } else if ((0x0700U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0013d320U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001395a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x1000U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0016b2e0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x1080U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0013e200U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x1100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0013e320U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001555a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x2000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001555a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                }
                if ((1U & (~ VL_ONEHOT_I((((((((0x2000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 3U) 
                                              | ((0x1800U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 2U)) 
                                             | (((0x1100U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 1U) 
                                                | (0x1080U 
                                                   == 
                                                   (0xff80U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                            << 0x0000000bU) 
                                           | (((((0x1000U 
                                                  == 
                                                  (0xff80U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 3U) 
                                                | ((0x0800U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0700U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 1U) 
                                                  | (0x0680U 
                                                     == 
                                                     (0xff80U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                              << 7U)) 
                                          | ((((((0x0600U 
                                                  == 
                                                  (0xff80U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 3U) 
                                                | ((0x0400U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0300U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 1U) 
                                                  | (0x0280U 
                                                     == 
                                                     (0xff80U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                              << 3U) 
                                             | (((0x0220U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 2U) 
                                                | (((0x0200U 
                                                     == 
                                                     (0xffe0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xfe00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))))) {
                    if ((0U != (((((((0x2000U == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                     << 3U) | ((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 2U)) 
                                   | (((0x1100U == 
                                        (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                       << 1U) | (0x1080U 
                                                 == 
                                                 (0xff80U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                  << 0x0000000bU) | 
                                 (((((0x1000U == (0xff80U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                     << 3U) | ((0x0800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 2U)) 
                                   | (((0x0700U == 
                                        (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                       << 1U) | (0x0680U 
                                                 == 
                                                 (0xff80U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                  << 7U)) | ((((((0x0600U 
                                                  == 
                                                  (0xff80U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 3U) 
                                                | ((0x0400U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0300U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 1U) 
                                                  | (0x0280U 
                                                     == 
                                                     (0xff80U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                              << 3U) 
                                             | (((0x0220U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 2U) 
                                                | (((0x0200U 
                                                     == 
                                                     (0xffe0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xfe00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1434: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1434, "");
                        }
                    }
                }
            } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                                  >> 9U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x0016c680U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x0016c5a0U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            }
                        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x0016c5a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001675a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001665a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001625a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00167680U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00166680U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? 0xb134U : 0xb0b4U) 
                                  << 5U));
                    }
                } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                           | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                ? 0xb0adU : ((0x00000800U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                              ? 0xb02dU
                                              : 0xad2dU)) 
                              << 5U));
                } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0015a5a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001595a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    }
                } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? 0xb034U : 0xad34U) 
                                  << 5U));
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00159680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00154680U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001545a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                }
            } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001535a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x001525a0U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0014b5a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00153680U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00152680U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                   | (((0x00000200U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0xa5b4U : 0xa534U) 
                                      << 5U));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0014a5a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                           | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                ? 0xa52dU : 0xa4adU) 
                              << 5U));
                }
            } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                           | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                ? 0xa42dU : 0xa3adU) 
                              << 5U));
                } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001475a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                           | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                ? 0xa4b4U : 0xa434U) 
                              << 5U));
                } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x00147680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0013f680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                }
            } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0013f5a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001365a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                }
            } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x001365a0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x00136680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0012e680U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                }
            } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x0012c680U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x0016e320U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                 >> 7U)))) {
                if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001380a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                  >> 4U)))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word) 
                                          >> 2U)))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                            = (0x0015f120U 
                                               | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = ((0x0000001fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                                           | (((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                                ? 0xaf09U
                                                : 0xae80U) 
                                              << 5U));
                                }
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x0015c780U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (0x0015c760U 
                                           | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x0015c760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x0015b780U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x0015b760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x0015b760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00158780U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00158760U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001380c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00158760U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (0x00151780U 
                                       | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                    = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00151760U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (0x00151760U | (0x0000001fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                                = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                               | (((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x9d3cU : 0x9abcU)
                                    : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                        ? 0x9abbU : 0x9a3cU)) 
                                  << 5U));
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                           | (((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? 0x9a3bU : 0x99bcU)
                                : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))
                                    ? 0x99bbU : 0x993cU)) 
                              << 5U));
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x00132760U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0012e660U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0012c660U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x0017d280U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x0200U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001b3280U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    } else if ((0x0400U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001c00a0U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I((((0x0400U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 2U) 
                                              | (((0x0200U 
                                                   == 
                                                   (0xfe00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                        if ((0U != (((0x0400U == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                     << 2U) | (((0x0200U 
                                                 == 
                                                 (0xfe00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                << 1U) 
                                               | (0U 
                                                  == 
                                                  (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1003: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1003, "");
                            }
                        }
                    }
                } else {
                    if (((((((((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                               | (8U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                              | (0x0010U == (0xfff0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                             | (0x0020U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                            | (0x0030U == (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                           | (0x0040U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                          | (0x0050U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) 
                         | (0x0100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = ((0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r) 
                               | (((0U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                    ? 0xb784U : ((8U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                  ? 0xda04U
                                                  : 
                                                 ((0x0010U 
                                                   == 
                                                   (0xfff0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                   ? 0xc48bU
                                                   : 
                                                  ((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                    ? 0xc50bU
                                                    : 
                                                   ((0x0030U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                     ? 0xda02U
                                                     : 
                                                    ((0x0040U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                      ? 0xe70bU
                                                      : 
                                                     ((0x0050U 
                                                       == 
                                                       (0xfff0U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))
                                                       ? 0xe78bU
                                                       : 0xc5a0U))))))) 
                                  << 5U));
                    } else if ((0x0200U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                            = (0x001d0400U | (0x0000001fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((((0x0200U 
                                                   == 
                                                   (0xff00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                  << 4U) 
                                                 | (((0x0100U 
                                                      == 
                                                      (0xff00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                     << 3U) 
                                                    | ((0x0050U 
                                                        == 
                                                        (0xfff0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                       << 2U))) 
                                                | (((0x0040U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                    << 1U) 
                                                   | (0x0030U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                               << 4U) 
                                              | ((((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0010U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                     << 2U)) 
                                                 | (((8U 
                                                      == 
                                                      (0xfff8U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                     << 1U) 
                                                    | (0U 
                                                       == 
                                                       (0xfff8U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))))) {
                        if ((0U != ((((((0x0200U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                        << 4U) | ((
                                                   (0x0100U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0050U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                     << 2U))) 
                                      | (((0x0040U 
                                           == (0xfff0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                          << 1U) | 
                                         (0x0030U == 
                                          (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))) 
                                     << 4U) | ((((0x0020U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 3U) 
                                                | ((0x0010U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 2U)) 
                                               | (((8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:952: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 952, "");
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                if ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x00187560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x00187560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                } else if ((0x1000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001cd560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001cd560U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x4000U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x00187580U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (1U | vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r);
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x4000U 
                                             == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                            << 4U) 
                                           | (((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 3U) 
                                              | ((0x1000U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                                 << 2U))) 
                                          | (((0x0800U 
                                               == (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                    if ((0U != ((((0x4000U == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                  << 4U) | (((0x1800U 
                                              == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                             << 3U) 
                                            | ((0x1000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                               << 2U))) 
                                | (((0x0800U == (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                    << 1U) | (0U == 
                                              (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:918: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 918, "");
                        }
                    }
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001130a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0017f000U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x0200U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0017c2c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0017e2c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x0400U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                            << 3U) 
                                           | ((0x0200U 
                                               == (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                              << 2U)) 
                                          | (((0x0040U 
                                               == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))))) {
                    if ((0U != ((((0x0400U == (0xfe00U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                  << 3U) | ((0x0200U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) 
                                            << 2U)) 
                                | (((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                    << 1U) | (0U == 
                                              (0xffc0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:892: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 892, "");
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
                if ((0x07ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001247c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x0800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x08ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x00156700U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x0900U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x097fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0017b3a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x0900U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x097fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0017a6e0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x0980U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001c2000U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if ((0x0980U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001c3100U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x0a00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x0affU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001b56c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x1000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x17ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001887a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x1800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x1fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001887c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x2000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x27ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001887a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                } else if (((0x2800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                            & (0x2fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x001887c0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                        = (0x0019a0a0U | (0x0000001fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
                }
                if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                    if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:824: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 824, "");
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__ext_root))) {
            if ((0U == (0xfffcU & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x0011a800U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((4U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x001407e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((5U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x001417e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((6U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x001427e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((7U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x001437e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            } else if ((8U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r 
                    = (0x001447e0U | (0x0000001fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r));
            }
            if ((1U & (~ VL_ONEHOT_I(((((8U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                        << 5U) | ((
                                                   (7U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                                   << 4U) 
                                                  | ((6U 
                                                      == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                                     << 3U))) 
                                      | (((5U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                          << 2U) | 
                                         (((4U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                           << 1U) | 
                                          (0U == (0xfffcU 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))))) {
                if ((0U != ((((8U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                              << 5U) | (((7U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                         << 4U) | (
                                                   (6U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                                   << 3U))) 
                            | (((5U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                << 2U) | (((4U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)) 
                                           << 1U) | 
                                          (0U == (0xfffcU 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word)))))))) {
                    if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:788: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__extension_word));
                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 788, "");
                    }
                }
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__r;
        decode_tb__DOT__dut__DOT__extended_decode = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__5__Vfuncout;
        vlSelfRef.decode_tb__DOT__valid = (1U & (decode_tb__DOT__dut__DOT__extended_decode 
                                                 >> 0x00000014U));
        decode_tb__DOT__field_format_id = (0x0000007fU 
                                           & (decode_tb__DOT__dut__DOT__extended_decode 
                                              >> 5U));
        decode_tb__DOT__required_words = (0x0000000fU 
                                          & (decode_tb__DOT__dut__DOT__extended_decode 
                                             >> 1U));
    }
    if (vlSelfRef.decode_tb__DOT__valid) {
        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id 
            = decode_tb__DOT__field_format_id;
        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 1U;
        if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id) 
                              >> 4U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id) 
                                  >> 3U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id) 
                                      >> 2U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id) 
                                          >> 1U)))) {
                                if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id)))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 3U;
                                }
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r 
                    = ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                        ? ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                            ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                    ? 3U : 2U) : ((1U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                                   ? 2U
                                                   : 3U))
                            : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                ? 3U : 2U)) : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                                    ? 2U
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                                     ? 3U
                                                     : 2U))
                                                : 3U));
            } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r 
                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                ? 3U : 2U) : 2U);
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r 
                    = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                        ? 2U : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                 ? 2U : 3U));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id) 
                                 >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 3U;
                }
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                        if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                            vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 3U;
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r 
                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                            ? ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                ? 3U : 2U) : ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                               ? 2U
                                               : 3U));
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r 
                    = ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                        ? 2U : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))
                                 ? 3U : 2U));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 3U;
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 3U;
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
                if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
                }
            } else {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id))) {
            if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__field_format_id)))) {
                vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r = 2U;
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__r;
        decode_tb__DOT__dut__DOT__field_format_token_words 
            = vlSelfRef.__Vfunc_bedrock_decode_field_format_token_words__6__Vfuncout;
        if (((IData)(decode_tb__DOT__dut__DOT__field_format_token_words) 
             > (IData)(decode_tb__DOT__required_words))) {
            decode_tb__DOT__required_words = decode_tb__DOT__dut__DOT__field_format_token_words;
        }
    }
}

void Vdecode_tb___024root___eval_act(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_act\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        Vdecode_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

void Vdecode_tb___024root___eval_nba(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_nba\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vdecode_tb___024root___act_sequent__TOP__0(vlSelf);
    }
}

void Vdecode_tb___024root___timing_resume(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___timing_resume\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Vdecode_tb___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vdecode_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vdecode_tb___024root___eval_phase__act(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_phase__act\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    Vdecode_tb___024root___eval_triggers_vec__act(vlSelf);
    Vdecode_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vdecode_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vdecode_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vdecode_tb___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Vdecode_tb___024root___timing_resume(vlSelf);
        Vdecode_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vdecode_tb___024root___eval_phase__inact(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_phase__inact\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("tb/decode_tb.sv", 4, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vdecode_tb___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vdecode_tb___024root___eval_phase__nba(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_phase__nba\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vdecode_tb___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vdecode_tb___024root___eval_nba(vlSelf);
        Vdecode_tb___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vdecode_tb___024root___eval(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vdecode_tb___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("tb/decode_tb.sv", 4, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("tb/decode_tb.sv", 4, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vdecode_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("tb/decode_tb.sv", 4, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vdecode_tb___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vdecode_tb___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vdecode_tb___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vdecode_tb___024root___eval_debug_assertions(Vdecode_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vdecode_tb___024root___eval_debug_assertions\n"); );
    Vdecode_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
