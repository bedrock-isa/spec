// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vfull_decode_tb.h for the primary calling header

#ifndef VERILATED_VFULL_DECODE_TB___024ROOT_H_
#define VERILATED_VFULL_DECODE_TB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vfull_decode_tb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vfull_decode_tb___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ full_decode_tb__DOT__undersized;
        CData/*7:0*/ full_decode_tb__DOT__opcode_id;
        CData/*6:0*/ full_decode_tb__DOT__field_format_id;
        CData/*0:0*/ full_decode_tb__DOT__needs_extension;
        CData/*1:0*/ full_decode_tb__DOT__repeat_kind;
        CData/*0:0*/ full_decode_tb__DOT__repeat_present;
        CData/*3:0*/ full_decode_tb__DOT__dut__DOT__total_required_words;
        CData/*0:0*/ full_decode_tb__DOT__dut__DOT__base_valid;
        CData/*4:0*/ __Vfunc_bedrock_decode_extended_opcode__84__ext_root;
        CData/*3:0*/ __Vfunc_bedrock_decode_field_format_token_words__85__Vfuncout;
        CData/*6:0*/ __Vfunc_bedrock_decode_field_format_token_words__85__field_format_id;
        CData/*3:0*/ __Vfunc_bedrock_decode_field_format_token_words__85__r;
        CData/*5:0*/ __Vfunc_bedrock_decode_compact_ea__87__ea;
        CData/*0:0*/ __Vfunc_bedrock_decode_extended_ea__88__signed32_index_escape;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_13__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_12__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_11__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_10__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_9__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_8__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_7__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_6__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_5__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_4__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_3__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_2__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_1__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88____VlefCall_0__bedrock_ea_segment_decode;
        CData/*4:0*/ __Vfunc_bedrock_decode_extended_ea__88__mode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__88__segment;
        CData/*7:0*/ __Vfunc_bedrock_decode_extended_ea__88__extra;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__89__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__89__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__90__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__90__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__91__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__91__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__92__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__92__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__93__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__93__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__94__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__94__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__95__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__95__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__96__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__96__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__97__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__97__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__98__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__98__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__99__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__99__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__100__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__100__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__101__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__101__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__102__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__102__segment;
        CData/*5:0*/ __Vfunc_bedrock_decode_compact_ea__104__ea;
        CData/*0:0*/ __Vfunc_bedrock_decode_extended_ea__105__signed32_index_escape;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_13__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_12__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_11__bedrock_ea_segment_decode;
    };
    struct {
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_10__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_9__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_8__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_7__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_6__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_5__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_4__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_3__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_2__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_1__bedrock_ea_segment_decode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105____VlefCall_0__bedrock_ea_segment_decode;
        CData/*4:0*/ __Vfunc_bedrock_decode_extended_ea__105__mode;
        CData/*2:0*/ __Vfunc_bedrock_decode_extended_ea__105__segment;
        CData/*7:0*/ __Vfunc_bedrock_decode_extended_ea__105__extra;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__106__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__106__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__107__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__107__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__108__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__108__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__109__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__109__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__110__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__110__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__111__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__111__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__112__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__112__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__113__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__113__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__114__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__114__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__115__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__115__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__116__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__116__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__117__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__117__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__118__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__118__segment;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__119__Vfuncout;
        CData/*2:0*/ __Vfunc_bedrock_ea_segment_decode__119__segment;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VinactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        SData/*15:0*/ __Vfunc_bedrock_decode_extended_opcode__84__extension_word;
        SData/*15:0*/ __Vfunc_bedrock_decode_extended_ea__88__descriptor;
        SData/*15:0*/ __Vfunc_bedrock_decode_extended_ea__105__descriptor;
        VlWide<4>/*127:0*/ full_decode_tb__DOT__words;
        IData/*20:0*/ __Vfunc_bedrock_decode_extended_opcode__84__Vfuncout;
        IData/*20:0*/ __Vfunc_bedrock_decode_extended_opcode__84__r;
        IData/*31:0*/ __VactIterCount;
        IData/*31:0*/ __VinactIterCount;
        IData/*31:0*/ __Vi;
        QData/*33:0*/ full_decode_tb__DOT__dut__DOT__field_extract;
        QData/*39:0*/ __Vfunc_bedrock_decode_ea__86__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_ea__86__compact;
        QData/*39:0*/ __Vfunc_bedrock_decode_compact_ea__87__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_compact_ea__87__r;
        QData/*39:0*/ __Vfunc_bedrock_decode_extended_ea__88__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_extended_ea__88__r;
        QData/*39:0*/ __Vfunc_bedrock_decode_ea__103__Vfuncout;
    };
    struct {
        QData/*39:0*/ __Vfunc_bedrock_decode_ea__103__compact;
        QData/*39:0*/ __Vfunc_bedrock_decode_compact_ea__104__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_compact_ea__104__r;
        QData/*39:0*/ __Vfunc_bedrock_decode_extended_ea__105__Vfuncout;
        QData/*39:0*/ __Vfunc_bedrock_decode_extended_ea__105__r;
        VlUnpacked<CData/*5:0*/, 2> full_decode_tb__DOT__ea_value;
        VlUnpacked<CData/*5:0*/, 2> full_decode_tb__DOT__ea_form;
        VlUnpacked<QData/*61:0*/, 2> full_decode_tb__DOT__agu_request;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };
    std::string __Vtask_full_decode_tb__DOT__expect_logic__2__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__3__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__7__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__8__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__9__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__10__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__11__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__12__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__13__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__16__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__17__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__21__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__22__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__23__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__24__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__29__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__30__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__31__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__32__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__37__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__38__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__39__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__40__name;
    std::string __Vtask_full_decode_tb__DOT__expect_u16__41__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__45__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__46__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__47__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__48__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__53__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__54__name;
    std::string __Vtask_full_decode_tb__DOT__expect_logic__55__name;
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vfull_decode_tb__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vfull_decode_tb___024root(Vfull_decode_tb__Syms* symsp, const char* namep);
    ~Vfull_decode_tb___024root();
    VL_UNCOPYABLE(Vfull_decode_tb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
