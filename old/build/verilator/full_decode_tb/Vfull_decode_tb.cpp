// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vfull_decode_tb__pch.h"

//============================================================
// Constructors

Vfull_decode_tb::Vfull_decode_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vfull_decode_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vfull_decode_tb::Vfull_decode_tb(const char* _vcname__)
    : Vfull_decode_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vfull_decode_tb::~Vfull_decode_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vfull_decode_tb___024root___eval_debug_assertions(Vfull_decode_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Vfull_decode_tb___024root___eval_static(Vfull_decode_tb___024root* vlSelf);
void Vfull_decode_tb___024root___eval_initial(Vfull_decode_tb___024root* vlSelf);
void Vfull_decode_tb___024root___eval_settle(Vfull_decode_tb___024root* vlSelf);
void Vfull_decode_tb___024root___eval(Vfull_decode_tb___024root* vlSelf);

void Vfull_decode_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vfull_decode_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vfull_decode_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vfull_decode_tb___024root___eval_static(&(vlSymsp->TOP));
        Vfull_decode_tb___024root___eval_initial(&(vlSymsp->TOP));
        Vfull_decode_tb___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vfull_decode_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vfull_decode_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vfull_decode_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vfull_decode_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vfull_decode_tb___024root___eval_final(Vfull_decode_tb___024root* vlSelf);

VL_ATTR_COLD void Vfull_decode_tb::final() {
    contextp()->executingFinal(true);
    Vfull_decode_tb___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vfull_decode_tb::hierName() const { return vlSymsp->name(); }
const char* Vfull_decode_tb::modelName() const { return "Vfull_decode_tb"; }
unsigned Vfull_decode_tb::threads() const { return 1; }
void Vfull_decode_tb::prepareClone() const { contextp()->prepareClone(); }
void Vfull_decode_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}
