// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vprefix_ea_tb.h for the primary calling header

#ifndef VERILATED_VPREFIX_EA_TB___024ROOT_H_
#define VERILATED_VPREFIX_EA_TB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vprefix_ea_tb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vprefix_ea_tb___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ prefix_ea_tb__DOT__prefix_valid;
        CData/*0:0*/ prefix_ea_tb__DOT__nospec;
        CData/*0:0*/ prefix_ea_tb__DOT__saturate;
        CData/*2:0*/ prefix_ea_tb__DOT__update_mode;
        CData/*1:0*/ prefix_ea_tb__DOT__access_mode;
        CData/*1:0*/ prefix_ea_tb__DOT__repeat_kind;
        CData/*3:0*/ prefix_ea_tb__DOT__repeat_condition;
        CData/*2:0*/ prefix_ea_tb__DOT__repeat_counter;
        CData/*0:0*/ prefix_ea_tb__DOT__end_group;
        CData/*5:0*/ prefix_ea_tb__DOT__ea;
        CData/*0:0*/ prefix_ea_tb__DOT__ea_valid;
        CData/*0:0*/ prefix_ea_tb__DOT__ea_reserved;
        CData/*5:0*/ prefix_ea_tb__DOT__ea_form;
        CData/*2:0*/ prefix_ea_tb__DOT__segment;
        CData/*2:0*/ prefix_ea_tb__DOT__base;
        CData/*2:0*/ prefix_ea_tb__DOT__base_reg;
        CData/*2:0*/ prefix_ea_tb__DOT__index_reg;
        CData/*1:0*/ prefix_ea_tb__DOT__scale_log2;
        CData/*2:0*/ prefix_ea_tb__DOT__payload_words;
        CData/*5:0*/ __Vfunc_bedrock_decode_compact_ea__21__ea;
        CData/*0:0*/ __Vfunc_bedrock_decode_extended_ea__22__signed32_index_escape;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_13__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_12__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_11__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_10__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_9__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_8__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_7__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_6__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_5__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_4__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_3__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_2__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_1__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22____VlefCall_0__bedrock_ea_segment_decode;
        CData/*4:0*/ __Vfunc_bedrock_decode_extended_ea__22__mode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__22__segment;
        CData/*7:0*/ __Vfunc_bedrock_decode_extended_ea__22__extra;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__23__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__23__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__24__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__24__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__25__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__25__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__26__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__26__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__27__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__27__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__28__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__28__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__29__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__29__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__30__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__30__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__31__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__31__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__32__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__32__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__33__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__33__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__34__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__34__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__35__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__35__segment;
    };
    struct {
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__36__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__36__segment;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VinactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        SData/*15:0*/ prefix_ea_tb__DOT__prefix_word;
        SData/*15:0*/ prefix_ea_tb__DOT__descriptor;
        SData/*15:0*/ __Vfunc_bedrock_decode_extended_ea__22__descriptor;
        IData/*31:0*/ __VactIterCount;
        IData/*31:0*/ __VinactIterCount;
        IData/*31:0*/ __Vi;
        QData/*39:0*/ __Vfunc_bedrock_decode_ea__20__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_ea__20__compact;
        QData/*39:0*/ __Vfunc_bedrock_decode_compact_ea__21__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_compact_ea__21__r;
        QData/*39:0*/ __Vfunc_bedrock_decode_extended_ea__22__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_extended_ea__22__r;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vprefix_ea_tb__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vprefix_ea_tb___024root(Vprefix_ea_tb__Syms* symsp, const char* namep);
    ~Vprefix_ea_tb___024root();
    VL_UNCOPYABLE(Vprefix_ea_tb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
