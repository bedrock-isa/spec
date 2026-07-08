// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vagu_tb.h for the primary calling header

#include "Vagu_tb__pch.h"

void Vagu_tb___024root___ctor_var_reset(Vagu_tb___024root* vlSelf);

Vagu_tb___024root::Vagu_tb___024root(Vagu_tb__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vagu_tb___024root___ctor_var_reset(this);
}

void Vagu_tb___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vagu_tb___024root::~Vagu_tb___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
