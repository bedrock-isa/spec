// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vdecode_tb__pch.h"

//============================================================
// Constructors

Vdecode_tb::Vdecode_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vdecode_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vdecode_tb::Vdecode_tb(const char* _vcname__)
    : Vdecode_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vdecode_tb::~Vdecode_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vdecode_tb___024root___eval_debug_assertions(Vdecode_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Vdecode_tb___024root___eval_static(Vdecode_tb___024root* vlSelf);
void Vdecode_tb___024root___eval_initial(Vdecode_tb___024root* vlSelf);
void Vdecode_tb___024root___eval_settle(Vdecode_tb___024root* vlSelf);
void Vdecode_tb___024root___eval(Vdecode_tb___024root* vlSelf);

void Vdecode_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vdecode_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vdecode_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vdecode_tb___024root___eval_static(&(vlSymsp->TOP));
        Vdecode_tb___024root___eval_initial(&(vlSymsp->TOP));
        Vdecode_tb___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vdecode_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vdecode_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vdecode_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vdecode_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vdecode_tb___024root___eval_final(Vdecode_tb___024root* vlSelf);

VL_ATTR_COLD void Vdecode_tb::final() {
    contextp()->executingFinal(true);
    Vdecode_tb___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vdecode_tb::hierName() const { return vlSymsp->name(); }
const char* Vdecode_tb::modelName() const { return "Vdecode_tb"; }
unsigned Vdecode_tb::threads() const { return 1; }
void Vdecode_tb::prepareClone() const { contextp()->prepareClone(); }
void Vdecode_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}
