// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VPREFIX_EA_TB__SYMS_H_
#define VERILATED_VPREFIX_EA_TB__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vprefix_ea_tb.h"

// INCLUDE MODULE CLASSES
#include "Vprefix_ea_tb___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vprefix_ea_tb__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vprefix_ea_tb* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vprefix_ea_tb___024root        TOP;

    // CONSTRUCTORS
    Vprefix_ea_tb__Syms(VerilatedContext* contextp, const char* namep, Vprefix_ea_tb* modelp);
    ~Vprefix_ea_tb__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
