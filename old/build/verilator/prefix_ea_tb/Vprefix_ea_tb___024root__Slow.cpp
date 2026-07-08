// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vprefix_ea_tb.h for the primary calling header

#include "Vprefix_ea_tb__pch.h"

void Vprefix_ea_tb___024root___ctor_var_reset(Vprefix_ea_tb___024root* vlSelf);

Vprefix_ea_tb___024root::Vprefix_ea_tb___024root(Vprefix_ea_tb__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vprefix_ea_tb___024root___ctor_var_reset(this);
}

void Vprefix_ea_tb___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vprefix_ea_tb___024root::~Vprefix_ea_tb___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
