// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Ventry_precheck_tb__pch.h"

//============================================================
// Constructors

Ventry_precheck_tb::Ventry_precheck_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Ventry_precheck_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Ventry_precheck_tb::Ventry_precheck_tb(const char* _vcname__)
    : Ventry_precheck_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Ventry_precheck_tb::~Ventry_precheck_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Ventry_precheck_tb___024root___eval_debug_assertions(Ventry_precheck_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Ventry_precheck_tb___024root___eval_static(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___eval_initial(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___eval_settle(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___eval(Ventry_precheck_tb___024root* vlSelf);

void Ventry_precheck_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Ventry_precheck_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Ventry_precheck_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Ventry_precheck_tb___024root___eval_static(&(vlSymsp->TOP));
        Ventry_precheck_tb___024root___eval_initial(&(vlSymsp->TOP));
        Ventry_precheck_tb___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Ventry_precheck_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Ventry_precheck_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Ventry_precheck_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Ventry_precheck_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Ventry_precheck_tb___024root___eval_final(Ventry_precheck_tb___024root* vlSelf);

VL_ATTR_COLD void Ventry_precheck_tb::final() {
    contextp()->executingFinal(true);
    Ventry_precheck_tb___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Ventry_precheck_tb::hierName() const { return vlSymsp->name(); }
const char* Ventry_precheck_tb::modelName() const { return "Ventry_precheck_tb"; }
unsigned Ventry_precheck_tb::threads() const { return 1; }
void Ventry_precheck_tb::prepareClone() const { contextp()->prepareClone(); }
void Ventry_precheck_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}
