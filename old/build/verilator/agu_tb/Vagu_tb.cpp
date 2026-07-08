// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vagu_tb__pch.h"

//============================================================
// Constructors

Vagu_tb::Vagu_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vagu_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vagu_tb::Vagu_tb(const char* _vcname__)
    : Vagu_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vagu_tb::~Vagu_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vagu_tb___024root___eval_debug_assertions(Vagu_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Vagu_tb___024root___eval_static(Vagu_tb___024root* vlSelf);
void Vagu_tb___024root___eval_initial(Vagu_tb___024root* vlSelf);
void Vagu_tb___024root___eval_settle(Vagu_tb___024root* vlSelf);
void Vagu_tb___024root___eval(Vagu_tb___024root* vlSelf);

void Vagu_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vagu_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vagu_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vagu_tb___024root___eval_static(&(vlSymsp->TOP));
        Vagu_tb___024root___eval_initial(&(vlSymsp->TOP));
        Vagu_tb___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vagu_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vagu_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vagu_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vagu_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vagu_tb___024root___eval_final(Vagu_tb___024root* vlSelf);

VL_ATTR_COLD void Vagu_tb::final() {
    contextp()->executingFinal(true);
    Vagu_tb___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vagu_tb::hierName() const { return vlSymsp->name(); }
const char* Vagu_tb::modelName() const { return "Vagu_tb"; }
unsigned Vagu_tb::threads() const { return 1; }
void Vagu_tb::prepareClone() const { contextp()->prepareClone(); }
void Vagu_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}
