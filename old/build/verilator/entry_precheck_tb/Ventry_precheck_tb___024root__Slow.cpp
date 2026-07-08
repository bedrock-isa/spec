// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Ventry_precheck_tb.h for the primary calling header

#include "Ventry_precheck_tb__pch.h"

void Ventry_precheck_tb___024root___ctor_var_reset(Ventry_precheck_tb___024root* vlSelf);

Ventry_precheck_tb___024root::Ventry_precheck_tb___024root(Ventry_precheck_tb__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Ventry_precheck_tb___024root___ctor_var_reset(this);
}

void Ventry_precheck_tb___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Ventry_precheck_tb___024root::~Ventry_precheck_tb___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
