// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Ventry_precheck_tb__pch.h"

Ventry_precheck_tb__Syms::Ventry_precheck_tb__Syms(VerilatedContext* contextp, const char* namep, Ventry_precheck_tb* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(22028);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
}

Ventry_precheck_tb__Syms::~Ventry_precheck_tb__Syms() {
    // Tear down scopes
    // Tear down sub module instances
}
