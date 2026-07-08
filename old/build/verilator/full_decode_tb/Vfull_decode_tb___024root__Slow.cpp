// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vfull_decode_tb.h for the primary calling header

#include "Vfull_decode_tb__pch.h"

void Vfull_decode_tb___024root___ctor_var_reset(Vfull_decode_tb___024root* vlSelf);

Vfull_decode_tb___024root::Vfull_decode_tb___024root(Vfull_decode_tb__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vfull_decode_tb___024root___ctor_var_reset(this);
}

void Vfull_decode_tb___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vfull_decode_tb___024root::~Vfull_decode_tb___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
