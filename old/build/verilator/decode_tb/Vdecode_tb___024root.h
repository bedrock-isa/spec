// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vdecode_tb.h for the primary calling header

#ifndef VERILATED_VDECODE_TB___024ROOT_H_
#define VERILATED_VDECODE_TB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vdecode_tb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vdecode_tb___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ decode_tb__DOT__valid;
    CData/*0:0*/ decode_tb__DOT__needs_extension;
    CData/*4:0*/ __Vfunc_bedrock_decode_extended_opcode__5__ext_root;
    CData/*3:0*/ __Vfunc_bedrock_decode_field_format_token_words__6__Vfuncout;
    CData/*6:0*/ __Vfunc_bedrock_decode_field_format_token_words__6__field_format_id;
    CData/*3:0*/ __Vfunc_bedrock_decode_field_format_token_words__6__r;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VinactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    SData/*11:0*/ decode_tb__DOT__primary_payload;
    SData/*15:0*/ decode_tb__DOT__extension_word;
    SData/*15:0*/ __Vfunc_bedrock_decode_extended_opcode__5__extension_word;
    IData/*20:0*/ __Vfunc_bedrock_decode_extended_opcode__5__Vfuncout;
    IData/*20:0*/ __Vfunc_bedrock_decode_extended_opcode__5__r;
    IData/*31:0*/ __VactIterCount;
    IData/*31:0*/ __VinactIterCount;
    IData/*31:0*/ __Vi;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vdecode_tb__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vdecode_tb___024root(Vdecode_tb__Syms* symsp, const char* namep);
    ~Vdecode_tb___024root();
    VL_UNCOPYABLE(Vdecode_tb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
