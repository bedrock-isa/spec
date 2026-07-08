// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vprefix_ea_tb__pch.h"

//============================================================
// Constructors

Vprefix_ea_tb::Vprefix_ea_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vprefix_ea_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vprefix_ea_tb::Vprefix_ea_tb(const char* _vcname__)
    : Vprefix_ea_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vprefix_ea_tb::~Vprefix_ea_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vprefix_ea_tb___024root___eval_debug_assertions(Vprefix_ea_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Vprefix_ea_tb___024root___eval_static(Vprefix_ea_tb___024root* vlSelf);
void Vprefix_ea_tb___024root___eval_initial(Vprefix_ea_tb___024root* vlSelf);
void Vprefix_ea_tb___024root___eval_settle(Vprefix_ea_tb___024root* vlSelf);
void Vprefix_ea_tb___024root___eval(Vprefix_ea_tb___024root* vlSelf);

void Vprefix_ea_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vprefix_ea_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vprefix_ea_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vprefix_ea_tb___024root___eval_static(&(vlSymsp->TOP));
        Vprefix_ea_tb___024root___eval_initial(&(vlSymsp->TOP));
        Vprefix_ea_tb___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vprefix_ea_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vprefix_ea_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vprefix_ea_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vprefix_ea_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vprefix_ea_tb___024root___eval_final(Vprefix_ea_tb___024root* vlSelf);

VL_ATTR_COLD void Vprefix_ea_tb::final() {
    contextp()->executingFinal(true);
    Vprefix_ea_tb___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vprefix_ea_tb::hierName() const { return vlSymsp->name(); }
const char* Vprefix_ea_tb::modelName() const { return "Vprefix_ea_tb"; }
unsigned Vprefix_ea_tb::threads() const { return 1; }
void Vprefix_ea_tb::prepareClone() const { contextp()->prepareClone(); }
void Vprefix_ea_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}
