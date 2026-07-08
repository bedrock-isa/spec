// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vagu_tb.h for the primary calling header

#ifndef VERILATED_VAGU_TB___024ROOT_H_
#define VERILATED_VAGU_TB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vagu_tb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vagu_tb___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*3:0*/ agu_tb__DOT__access_size_bytes;
    CData/*0:0*/ agu_tb__DOT__valid;
    CData/*0:0*/ agu_tb__DOT__address_valid;
    CData/*0:0*/ agu_tb__DOT__update_write;
    CData/*0:0*/ agu_tb__DOT__update_invalid;
    CData/*2:0*/ __Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__words;
    CData/*2:0*/ __Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__words;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VinactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    IData/*31:0*/ __VactIterCount;
    IData/*31:0*/ __VinactIterCount;
    IData/*31:0*/ __Vi;
    QData/*61:0*/ agu_tb__DOT__request;
    QData/*63:0*/ agu_tb__DOT__base_reg_value;
    QData/*63:0*/ agu_tb__DOT__index_reg_value;
    QData/*63:0*/ agu_tb__DOT__pc_value;
    QData/*63:0*/ agu_tb__DOT__sp_value;
    QData/*63:0*/ agu_tb__DOT__payload_value;
    QData/*63:0*/ agu_tb__DOT__effective_address;
    QData/*63:0*/ agu_tb__DOT__update_value;
    QData/*63:0*/ agu_tb__DOT__dut__DOT____VlemCond_3;
    QData/*63:0*/ agu_tb__DOT__dut__DOT____VlemCall_2__sign_extend_payload;
    QData/*63:0*/ agu_tb__DOT__dut__DOT____VlemCond_1;
    QData/*63:0*/ agu_tb__DOT__dut__DOT____VlemCall_0__sign_extend_payload;
    QData/*63:0*/ __Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__26__value;
    QData/*63:0*/ __Vfunc_agu_tb__DOT__dut__DOT__sign_extend_payload__27__value;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    std::string __Vtask_agu_tb__DOT__expect_logic__1__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__2__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__3__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__5__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__7__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__9__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__11__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__12__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__13__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__15__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__16__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__17__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__19__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__20__name;
    std::string __Vtask_agu_tb__DOT__expect_u64__21__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__23__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__24__name;
    std::string __Vtask_agu_tb__DOT__expect_logic__25__name;
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vagu_tb__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vagu_tb___024root(Vagu_tb__Syms* symsp, const char* namep);
    ~Vagu_tb___024root();
    VL_UNCOPYABLE(Vagu_tb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
