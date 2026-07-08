// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vdecode_tb.h for the primary calling header

#include "Vdecode_tb__pch.h"

void Vdecode_tb___024root___ctor_var_reset(Vdecode_tb___024root* vlSelf);

Vdecode_tb___024root::Vdecode_tb___024root(Vdecode_tb__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vdecode_tb___024root___ctor_var_reset(this);
}

void Vdecode_tb___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vdecode_tb___024root::~Vdecode_tb___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
