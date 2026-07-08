// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Ventry_precheck_tb.h for the primary calling header

#include "Ventry_precheck_tb__pch.h"

void Ventry_precheck_tb___024root___act_sequent__TOP__9(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___act_sequent__TOP__9\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repcc_allowed_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repcc_allowed_raw = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_allowed_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_allowed_raw = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_fast_candidate_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_fast_candidate_raw = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__needs_extension;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__needs_extension = 0;
    CData/*7:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__opcode_id;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__opcode_id = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repcc_allowed_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repcc_allowed_raw = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_allowed_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_allowed_raw = 0;
    CData/*0:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_fast_candidate_raw;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_fast_candidate_raw = 0;
    CData/*2:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode__DOT__attributes;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode__DOT__attributes = 0;
    IData/*25:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode = 0;
    IData/*19:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode = 0;
    CData/*2:0*/ entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__attributes;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__attributes = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__459__Vfuncout;
    __Vfunc_bedrock_decode_opcode_attributes__459__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_opcode_attributes__459__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__459__opcode_id = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__459__r;
    __Vfunc_bedrock_decode_opcode_attributes__459__r = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__465__Vfuncout;
    __Vfunc_bedrock_decode_primary_payload__465__Vfuncout = 0;
    SData/*11:0*/ __Vfunc_bedrock_decode_primary_payload__465__payload;
    __Vfunc_bedrock_decode_primary_payload__465__payload = 0;
    IData/*25:0*/ __Vfunc_bedrock_decode_primary_payload__465__r;
    __Vfunc_bedrock_decode_primary_payload__465__r = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__467__Vfuncout;
    __Vfunc_bedrock_decode_opcode_attributes__467__Vfuncout = 0;
    CData/*7:0*/ __Vfunc_bedrock_decode_opcode_attributes__467__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__467__opcode_id = 0;
    CData/*2:0*/ __Vfunc_bedrock_decode_opcode_attributes__467__r;
    __Vfunc_bedrock_decode_opcode_attributes__467__r = 0;
    IData/*31:0*/ __VdfgRegularize_hebeb780c_0_0;
    __VdfgRegularize_hebeb780c_0_0 = 0;
    IData/*31:0*/ __VdfgRegularize_hebeb780c_0_1;
    __VdfgRegularize_hebeb780c_0_1 = 0;
    IData/*31:0*/ __VdfgRegularize_hebeb780c_0_2;
    __VdfgRegularize_hebeb780c_0_2 = 0;
    // Body
    __Vfunc_bedrock_decode_opcode_attributes__459__opcode_id 
        = vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__459__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                              >> 4U)))) {
                    if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                                    __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                                         >> 2U)))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                                    = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                                      >> 1U)))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
                            }
                        }
                    }
                } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                                     >> 1U)))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    }
                }
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    }
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    }
                } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__459__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
            } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                          >> 1U)))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        }
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                        }
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                                     >> 2U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                                  >> 1U)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                        }
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__459__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))))
                        : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                    } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__459__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)))
                            : 7U);
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id) 
                              >> 1U)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__459__r 
                        = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            }
        }
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                    ? ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? 7U : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                                     ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))))
                        : ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)))))
                    : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                    ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                        ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r))
                            : 7U) : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)))
                    : 7U);
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        }
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__459__r 
                        = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__459__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            }
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__459__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        }
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        }
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__459__r = 7U;
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__459__r 
            = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))
                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r)));
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__459__r 
            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__459__r));
    }
    __Vfunc_bedrock_decode_opcode_attributes__459__Vfuncout 
        = __Vfunc_bedrock_decode_opcode_attributes__459__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode__DOT__attributes 
        = __Vfunc_bedrock_decode_opcode_attributes__459__Vfuncout;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repcc_allowed_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode__DOT__attributes) 
              >> 2U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_allowed_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode__DOT__attributes) 
              >> 1U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_fast_candidate_raw 
        = ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode_valid_raw) 
           & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode__DOT__attributes));
    __Vfunc_bedrock_decode_primary_payload__465__payload 
        = (0x00000fffU & (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                          >> 0x00000010U));
    __Vfunc_bedrock_decode_primary_payload__465__r = 0U;
    __Vfunc_bedrock_decode_primary_payload__465__r 
        = (0x00000020U | (0x03000000U & __Vfunc_bedrock_decode_primary_payload__465__r));
    if ((0x00000800U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                        if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                            if ((2U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                                if (
                                                    (1U 
                                                     & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                                        = 
                                                        (0x02000000U 
                                                         | __Vfunc_bedrock_decode_primary_payload__465__r);
                                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                                        = 
                                                        (0x006f0200U 
                                                         | (0x030001ffU 
                                                            & __Vfunc_bedrock_decode_primary_payload__465__r));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__465__payload) 
                                      >> 5U)))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__465__payload) 
                                              >> 3U)))) {
                                    if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                            if ((1U 
                                                 & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__465__r);
                                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                                    = 
                                                    (0x0000000aU 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__465__r));
                                            } else {
                                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                                    = 
                                                    (0x03000000U 
                                                     | __Vfunc_bedrock_decode_primary_payload__465__r);
                                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                                    = 
                                                    (8U 
                                                     | (0x03ffffe0U 
                                                        & __Vfunc_bedrock_decode_primary_payload__465__r));
                                            }
                                        } else if (
                                                   (1U 
                                                    & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__465__r);
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (9U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__465__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__465__r);
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x00000016U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__465__r));
                                        }
                                    } else if ((2U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__465__r);
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x00000014U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__465__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__465__r);
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x00000015U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__465__r));
                                        }
                                    } else if ((1U 
                                                & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__465__r);
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (2U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__465__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__465__r);
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (1U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__465__r));
                                    }
                                }
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (3U | (0x03ffffe0U 
                                             & __Vfunc_bedrock_decode_primary_payload__465__r));
                            }
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_primary_payload__465__payload) 
                                                  >> 1U)))) {
                                        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__465__r);
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (4U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__465__r));
                                        } else {
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (0x03000000U 
                                                   | __Vfunc_bedrock_decode_primary_payload__465__r);
                                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                                = (7U 
                                                   | (0x03ffffe0U 
                                                      & __Vfunc_bedrock_decode_primary_payload__465__r));
                                        }
                                    }
                                } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__465__r);
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (6U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__465__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__465__r);
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (5U | 
                                               (0x03ffffe0U 
                                                & __Vfunc_bedrock_decode_primary_payload__465__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__465__r);
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x0000000fU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__465__r);
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x0000000eU 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                                }
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__465__r);
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x0000000dU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                                    } else {
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x03000000U 
                                               | __Vfunc_bedrock_decode_primary_payload__465__r);
                                        __Vfunc_bedrock_decode_primary_payload__465__r 
                                            = (0x0000000cU 
                                               | (0x03ffffe0U 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                                    }
                                } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__465__r);
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x00000012U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__465__r);
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x00000013U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                                }
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__465__r);
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x00000011U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                                } else {
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x03000000U 
                                           | __Vfunc_bedrock_decode_primary_payload__465__r);
                                    __Vfunc_bedrock_decode_primary_payload__465__r 
                                        = (0x00000010U 
                                           | (0x03ffffe0U 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                                }
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x03000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x0000000bU 
                                       | (0x03ffffe0U 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00bf0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x008504a0U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00160800U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        }
                    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00160400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00950400U | (0x030001ffU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        }
                    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x00950800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x009b0400U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                    }
                } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                    if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00cf1c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00931c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            }
                        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00783c40U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00cd0240U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            } else {
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x02000000U 
                                       | __Vfunc_bedrock_decode_primary_payload__465__r);
                                __Vfunc_bedrock_decode_primary_payload__465__r 
                                    = (0x00791040U 
                                       | (0x0300001fU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                            }
                        } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00783c40U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00cc0240U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        } else {
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                            __Vfunc_bedrock_decode_primary_payload__465__r 
                                = (0x00791040U | (0x0300001fU 
                                                  & __Vfunc_bedrock_decode_primary_payload__465__r));
                        }
                    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x00921800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                    } else {
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                        __Vfunc_bedrock_decode_primary_payload__465__r 
                            = (0x00901800U | (0x030001ffU 
                                              & __Vfunc_bedrock_decode_primary_payload__465__r));
                    }
                } else {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x00294200U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                }
            } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x00cf4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x00bd4600U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                }
            } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00b64600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00934600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
        }
    } else if ((0x00000400U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x00855000U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else if ((0x00000200U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00194600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00054600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
            }
        } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x00711800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x001f1800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x002a4400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
        }
    } else if ((0x00000100U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x00011800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                } else {
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                    __Vfunc_bedrock_decode_primary_payload__465__r 
                        = (0x00701800U | (0x030001ffU 
                                          & __Vfunc_bedrock_decode_primary_payload__465__r));
                }
            } else {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
            }
        } else {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x00274400U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
        }
    } else if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x00034600U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x00281a00U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x001e1800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x00051c40U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x009b0800U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00880240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
            } else {
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
                __Vfunc_bedrock_decode_primary_payload__465__r 
                    = (0x00870240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
            }
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x00970240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x009c0240U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x00a80200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
        } else {
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
            __Vfunc_bedrock_decode_primary_payload__465__r 
                = (0x001302a0U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
        }
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_primary_payload__465__payload))) {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x00130260U | (0x0300001fU & __Vfunc_bedrock_decode_primary_payload__465__r));
    } else {
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x02000000U | __Vfunc_bedrock_decode_primary_payload__465__r);
        __Vfunc_bedrock_decode_primary_payload__465__r 
            = (0x006e0200U | (0x030001ffU & __Vfunc_bedrock_decode_primary_payload__465__r));
    }
    __Vfunc_bedrock_decode_primary_payload__465__Vfuncout 
        = __Vfunc_bedrock_decode_primary_payload__465__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode 
        = __Vfunc_bedrock_decode_primary_payload__465__Vfuncout;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode = 0U;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode 
        = (0x0008000fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode);
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw 
        = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode 
                 >> 0x00000019U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__needs_extension 
        = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode 
                 >> 0x00000018U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__opcode_id 
        = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode 
                          >> 0x00000010U));
    if ((0x01000000U & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode)) {
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root 
            = (0x0000001fU & entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__primary_decode);
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0U;
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
            = (2U | (0x00080000U & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root) 
                          >> 3U)))) {
                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root)))) {
                            if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = (0x00092860U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                            }
                            if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                                if ((0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                                    if (VL_UNLIKELY((
                                                     vlSymsp->_vm_contextp__->assertOn()))) {
                                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2660: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2660, "");
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                        if (((((((((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                   | (1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                  | (2U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                 | (8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                                | (0x0010U == (0xfff8U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                               | (0x0040U == (0xffc0U 
                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                              | (0x0080U == (0xffc0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                             | (0x00c0U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = ((0U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? (0x000bb010U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                    : ((1U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x000b90a3U
                                        : ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x8401U
                                                : (
                                                   (8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                    ? 0xdc05U
                                                    : 
                                                   ((0x0010U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                     ? 0xd185U
                                                     : 
                                                    ((0x0040U 
                                                      == 
                                                      (0xffc0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                      ? 0xba86U
                                                      : 
                                                     ((0x0080U 
                                                       == 
                                                       (0xffc0U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                       ? 0xdc8fU
                                                       : 0xb986U))))) 
                                              << 4U))));
                        } else if ((0x0100U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000e2860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x0140U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000a8060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x0180U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000ba060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x01c0U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000dd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x0200U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000cc860U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x0240U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000cd060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x0280U == (0xffc0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000e1060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (((((0x0280U 
                                                        == 
                                                        (0xffc0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                       << 3U) 
                                                      | ((0x0240U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                         << 2U)) 
                                                     | (((0x0200U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                         << 1U) 
                                                        | (0x01c0U 
                                                           == 
                                                           (0xffc0U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                                    << 0x0000000bU) 
                                                   | (((((0x0180U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0140U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0100U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                           << 1U) 
                                                          | (0x00c0U 
                                                             == 
                                                             (0xffc0U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                                      << 7U)) 
                                                  | ((((((0x0080U 
                                                          == 
                                                          (0xffc0U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                         << 3U) 
                                                        | ((0x0040U 
                                                            == 
                                                            (0xffc0U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                           << 2U)) 
                                                       | (((0x0010U 
                                                            == 
                                                            (0xfff8U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                           << 1U) 
                                                          | (8U 
                                                             == 
                                                             (0xfff8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                                      << 3U) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                                         << 2U) 
                                                        | (((1U 
                                                             == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                                            << 1U) 
                                                           | (0U 
                                                              == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))))) {
                            if ((0U != (((((((0x0280U 
                                              == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                             << 3U) 
                                            | ((0x0240U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 2U)) 
                                           | (((0x0200U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 1U) 
                                              | (0x01c0U 
                                                 == 
                                                 (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                          << 0x0000000bU) 
                                         | (((((0x0180U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 3U) 
                                              | ((0x0140U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0100U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 1U) 
                                                | (0x00c0U 
                                                   == 
                                                   (0xffc0U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                            << 7U)) 
                                        | ((((((0x0080U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 3U) 
                                              | ((0x0040U 
                                                  == 
                                                  (0xffc0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 2U)) 
                                             | (((0x0010U 
                                                  == 
                                                  (0xfff8U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 1U) 
                                                | (8U 
                                                   == 
                                                   (0xfff8U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                            << 3U) 
                                           | (((2U 
                                                == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                               << 2U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                                  << 1U) 
                                                 | (0U 
                                                    == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2578: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2578, "");
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                         >> 0x0000000fU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                      >> 0x0000000eU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                          >> 0x0000000dU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                              >> 0x0000000cU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                  >> 0x0000000bU)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                    >> 0x0000000aU)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                     >> 9U)))) {
                                                if (
                                                    (0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                             >> 7U)))) {
                                                        if (
                                                            (0x00000040U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                                     >> 5U)))) {
                                                                if (
                                                                    (0x00000010U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                                                    if (
                                                                        (8U 
                                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                                            = 
                                                                            (0x000e4050U 
                                                                             | (0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                                                    } else if (
                                                                               (1U 
                                                                                & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                                                >> 2U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ 
                                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                                                >> 1U)))) {
                                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                                                = 
                                                                                ((0x0000000fU 
                                                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                                                                | (((1U 
                                                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                                 ? 0xe801U
                                                                                 : 0xe201U) 
                                                                                << 4U));
                                                                        }
                                                                    }
                                                                } else {
                                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                                        = 
                                                                        ((8U 
                                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                          ? 0x000d1133U
                                                                          : 
                                                                         (0x000d0850U 
                                                                          | (0x0000000fU 
                                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r)));
                                                                }
                                                            }
                                                        } else {
                                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                                = 
                                                                (0x000d3860U 
                                                                 | (0x0000000fU 
                                                                    & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                                        }
                                                    }
                                                } else {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                        = 
                                                        ((0x00000080U 
                                                          & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                          ? 
                                                         ((0x0000000fU 
                                                           & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                                          | (((0x00000040U 
                                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                               ? 0xd786U
                                                               : 0xe491U) 
                                                             << 4U))
                                                          : 
                                                         ((0x00000040U 
                                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                           ? 
                                                          (0x000d21c0U 
                                                           | (0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                                           : 
                                                          ((0x00000020U 
                                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                            ? 
                                                           ((0x0000000fU 
                                                             & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                                            | (((0x00000010U 
                                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                 ? 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                  ? 0x8d85U
                                                                  : 
                                                                 ((4U 
                                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                   ? 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                     ? 0xe181U
                                                                     : 0xde01U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                     ? 0xdd81U
                                                                     : 0xd581U))
                                                                   : 
                                                                  ((2U 
                                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                    ? 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                     ? 0xd301U
                                                                     : 0xc881U)
                                                                    : 
                                                                   ((1U 
                                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                     ? 0xbb81U
                                                                     : 0x8201U))))
                                                                 : 
                                                                ((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                  ? 0xe505U
                                                                  : 0xd285U)) 
                                                               << 4U))
                                                            : 
                                                           ((0x00000010U 
                                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                             ? 
                                                            ((0x0000000fU 
                                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                                             | (((8U 
                                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                                  ? 0xe385U
                                                                  : 0xd005U) 
                                                                << 4U))
                                                             : 
                                                            ((8U 
                                                              & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                              ? 0x000e3123U
                                                              : 0x000cf923U)))));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                    if ((0x00001000U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                    >> 0x0000000bU)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                = (0x000c7ab0U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                            = ((0x0000000fU 
                                                & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                               | (((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc7abU
                                                    : 0xc72bU) 
                                                  << 4U));
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                        = ((0x0000000fU 
                                            & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                           | (((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc72bU
                                                    : 0xc6abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc6abU
                                                    : 0xc62bU)) 
                                              << 4U));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                       | (((0x00002000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc62bU
                                                    : 0xc5abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc5abU
                                                    : 0xc22bU))
                                            : ((0x00001000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc22bU
                                                    : 0xc1abU)
                                                : (
                                                   (0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xc1abU
                                                    : 0x91abU))) 
                                          << 4U));
                            }
                        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x00090ba0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0x91abU
                                            : 0x912bU) 
                                          << 4U));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = (0x000912b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                 >> 0x0000000aU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                         >> 5U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                             >> 4U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                                 >> 3U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                                     >> 2U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                                                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000903b3U;
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x8aabU : 0x8a2bU) 
                                      << 4U));
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000bf3a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000c53a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x4000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))) {
                            if ((0U != (((0x4000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                         << 1U) | (0U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2306: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2306, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00086ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000873a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00087ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000883a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2280: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2280, "");
                            }
                        }
                    }
                } else {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00084ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000853a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00085ba0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000863a0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2254: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2254, "");
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000da2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000daae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000d72e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   (0x8000U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 2U) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                            if ((0U != (((0x8000U == 
                                          (0xc000U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                         << 2U) | (
                                                   ((0x4000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xc000U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2233: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2233, "");
                                }
                            }
                        }
                    } else {
                        if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000ceae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x4000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000cf2e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x8000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000d62e0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0xc000U == (0xc000U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000d6ae0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        }
                        if ((1U & (~ VL_ONEHOT_I(((
                                                   ((0xc000U 
                                                     == 
                                                     (0xc000U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                    << 3U) 
                                                   | ((0x8000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                      << 2U)) 
                                                  | (((0x4000U 
                                                       == 
                                                       (0xc000U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                      << 1U) 
                                                     | (0U 
                                                        == 
                                                        (0xc000U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                            if ((0U != ((((0xc000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                          << 3U) | 
                                         ((0x8000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                          << 2U)) | 
                                        (((0x4000U 
                                           == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                          << 1U) | 
                                         (0U == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                    VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2207: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                                 , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                    VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2207, "");
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000832e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x4000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00083ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x8000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00088ae0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0xc000U == (0xc000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000892e0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((0xc000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 3U) 
                                               | ((0x8000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 2U)) 
                                              | (((0x4000U 
                                                   == 
                                                   (0xc000U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xc000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                        if ((0U != ((((0xc000U == (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                      << 3U) | ((0x8000U 
                                                 == 
                                                 (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 2U)) 
                                    | (((0x4000U == 
                                         (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                        << 1U) | (0U 
                                                  == 
                                                  (0xc000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:2181: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 2181, "");
                            }
                        }
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                      >> 0x0000000dU)))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xdaabU
                                            : 0xda2bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xd72bU
                                            : 0xd6abU)) 
                                      << 4U));
                        }
                    }
                } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = (0x000d62b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                              >> 9U)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                  >> 8U)))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                            = (0x000daa60U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                       | (((0x00000200U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0xda26U
                                                : 0xd726U)
                                            : ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0xd6a6U
                                                : 0xd626U)) 
                                          << 4U));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000d4ab0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0xcf2bU : 0xceabU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0xcb2bU : 0x8eabU)) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x8e2bU : 0x8c2bU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x8babU : 0x892bU))
                                : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x88abU : 0x83abU)
                                    : ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x832bU : 
                                       ((0x00000400U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                         ? ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                 ? 0xd4a6U
                                                 : 0xcf26U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                 ? 0xcea6U
                                                 : 0xca15U))
                                         : ((0x00000200U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                             ? ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                 ? 0x8926U
                                                 : 0x88a6U)
                                             : ((0x00000100U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                 ? 0x83a6U
                                                 : 0x8326U)))))) 
                              << 4U));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                   | (((0x00002000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xe7abU
                                            : 0xdeabU)
                                        : ((0x00001000U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xdb2bU
                                            : 0xd82bU)) 
                                      << 4U));
                        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = (0x000d52b0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                            } else if ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                            = (0x000db140U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                    } else if ((0x00000100U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                    >> 7U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                     >> 6U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                         >> 5U)))) {
                                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000dba43U;
                                                }
                                            }
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                            = (0x000d5260U 
                                               | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                    }
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = (0x000c9ab0U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                   | (((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xc9abU
                                            : 0xc12bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xc12bU
                                            : 0xc0abU)) 
                                      << 4U));
                        }
                    } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                               | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xc0abU
                                            : 0xc02bU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xc02bU
                                            : 0xbfabU))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xbfabU
                                            : 0x952aU)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0x952aU
                                            : ((0x00000400U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (0x00000200U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0xc915U
                                                     : 0xc815U)
                                                    : 
                                                   ((0x00000100U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0xb895U
                                                     : 0xb815U))
                                                : 0x94a9U)))) 
                                  << 4U));
                    } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000400U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0x94a9U
                                            : 0x9416U)
                                        : 0x93aaU) : 
                                   ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                     ? 0x93aaU : 0x9329U)) 
                                  << 4U));
                    } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x0008cab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00082ab0U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                               | (((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00000100U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0x8f95U : 0x8f15U)
                                    : 0x8c94U) << 4U));
                    } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00081940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x00093250U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x0008b060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000db9f3U;
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                          >> 3U)))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                  >> 1U)))) {
                                        if ((1U & (~ (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000e7b53U;
                                        }
                                    }
                                } else {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                        = ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x000deb53U
                                                : 0x000db353U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x000d8353U
                                                : 0x000c9b53U));
                                }
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x00095983U
                                                : 0x00095313U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x00094b03U
                                                : 0x00094183U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x00093b13U
                                                : 0x00093303U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x0008cb53U
                                                : 0x0008cb23U)))
                                    : ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x00082b53U
                                                : 0x00082af3U)
                                            : ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x00081b53U
                                                : 0x00081af3U))
                                        : ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? 0x00081af3U
                                                : 0x00081353U)
                                            : 0x000812f3U)));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x00080950U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    }
                } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                  >> 0x0000000eU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                      >> 0x0000000dU)))) {
                            if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                              >> 0x0000000bU)))) {
                                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                        = (0x000b5b40U 
                                           | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                                }
                            } else {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = ((0x0000000fU 
                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                       | (((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xb434U
                                            : 0xb3b4U) 
                                          << 4U));
                            }
                        }
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                           | (((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xb334U
                                            : 0xb1b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xb134U
                                            : 0xb0b4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xa7b4U
                                            : 0xa734U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xa6b4U
                                            : 0xa634U)))
                                : ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0xa334U
                                            : 0xa2b4U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0x9e34U
                                            : 0x9db4U))
                                    : ((0x00001000U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0x98b4U
                                            : 0x9834U)
                                        : ((0x00000800U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? 0x97b4U
                                            : 0x96b4U)))) 
                              << 4U));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                if (((((((((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                           | (0x0800U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                          | (0x0840U == (0xffe0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                         | (0x0900U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                        | (0x0a00U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                       | (0x0c00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                      | (0x0d00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                     | (0x0e00U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                            ? (0x0009cb40U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                            : ((0x0800U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                ? (0x000b49a0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                : ((0x0840U == (0xffe0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                    ? 0x000ab9b3U : 
                                   ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                                    | (((0x0900U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                         ? 0x9e90U : 
                                        ((0x0a00U == 
                                          (0xfe00U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                          ? 0x9ba7U
                                          : ((0x0c00U 
                                              == (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                              ? 0x9e90U
                                              : 0x9f10U))) 
                                       << 4U)))));
                } else if ((0x1000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x0009cad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x2000U == (0xff80U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000b4970U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x2400U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x0009e990U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x2800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000aab40U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x3000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x4000U == (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000aaad0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x5000U == (0xfc00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x0009f190U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                }
                if ((1U & (~ VL_ONEHOT_I((((((((0x5000U 
                                                == 
                                                (0xfc00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 3U) 
                                              | ((0x4000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 2U)) 
                                             | (((0x3000U 
                                                  == 
                                                  (0xf000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 1U) 
                                                | (0x2800U 
                                                   == 
                                                   (0xf800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                            << 0x0000000bU) 
                                           | (((((0x2400U 
                                                  == 
                                                  (0xfc00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 3U) 
                                                | ((0x2000U 
                                                    == 
                                                    (0xff80U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 2U)) 
                                               | (((0x1000U 
                                                    == 
                                                    (0xf000U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 1U) 
                                                  | (0x0e00U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                              << 7U)) 
                                          | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))))) {
                    if ((0U != (((((((0x5000U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                     << 3U) | ((0x4000U 
                                                == 
                                                (0xf000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 2U)) 
                                   | (((0x3000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                       << 1U) | (0x2800U 
                                                 == 
                                                 (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                  << 0x0000000bU) | 
                                 (((((0x2400U == (0xfc00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                     << 3U) | ((0x2000U 
                                                == 
                                                (0xff80U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 2U)) 
                                   | (((0x1000U == 
                                        (0xf000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                       << 1U) | (0x0e00U 
                                                 == 
                                                 (0xff00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                  << 7U)) | ((((((0x0d00U 
                                                  == 
                                                  (0xff00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 3U) 
                                                | ((0x0c00U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 2U)) 
                                               | (((0x0a00U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 1U) 
                                                  | (0x0900U 
                                                     == 
                                                     (0xff00U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                              << 3U) 
                                             | (((0x0840U 
                                                  == 
                                                  (0xffe0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 2U) 
                                                | (((0x0800U 
                                                     == 
                                                     (0xffc0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                    << 1U) 
                                                   | (0U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1463: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1463, "");
                        }
                    }
                }
            } else if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                          >> 0x0000000bU)))) {
                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                    = (0x000b5340U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                            }
                        } else {
                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                = (0x000b52d0U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                               | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? 0xb52dU : 0xb2adU) 
                                  << 4U));
                    }
                } else {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                           | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? ((0x00000800U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? 0xb2b4U : 0xb234U)
                                    : 0xb22dU) : ((0x00001000U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                   ? 0xb22dU
                                                   : 
                                                  ((0x00000800U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0xb034U
                                                    : 0xafb4U))) 
                              << 4U));
                }
            } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                       | (((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                            ? ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? 0xaf34U : 0xad34U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? 0xacb4U : 0xaa34U))
                            : ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? 0xa9b4U : 0xa934U)
                                : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? 0xa5b4U : 0xa534U))) 
                          << 4U));
            } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                       | (((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                            ? ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? 0xa4b4U : 0xa434U)
                            : ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? 0xa3b4U : 0x9fb4U)) 
                          << 4U));
            } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                    = ((0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r) 
                       | (((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                            ? 0x9b34U : 0x9734U) << 4U));
            } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                    = (0x00096340U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
            } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                    = (0x000b6190U | (0x0000000fU & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
            } else if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                 >> 9U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                              >> 8U)))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                      >> 6U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                          >> 5U)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                              >> 4U)))) {
                                    if ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                        if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word) 
                                                     >> 1U)))) {
                                                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                    = 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                      ? 0x000b0333U
                                                      : 0x000afb33U);
                                            }
                                        } else {
                                            vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                                = (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000afb33U
                                                     : 0x000af333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 
                                                    (0x000ae810U 
                                                     | (0x0000000fU 
                                                        & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                                     : 0x000ae3d3U));
                                        }
                                    } else {
                                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                                            = ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 0x000ae3c4U
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000adbd3U
                                                     : 0x000adbc4U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000adbc4U
                                                     : 0x000ad333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000ad333U
                                                     : 0x000acb33U)));
                                    }
                                }
                            }
                        }
                    } else {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0x00000040U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                ? (0x0009c060U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                : ((0x00000020U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                    ? (0x0009c070U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                    : ((0x00000010U 
                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                        ? ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000ac3d3U
                                                     : 0x000ac3c4U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000ac3c4U
                                                     : 0x000aa333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a9b33U
                                                     : 0x000a9333U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a8bd3U
                                                     : 0x000a8bc4U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a8bc4U
                                                     : 0x000a5b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a5b33U
                                                     : 0x000a5333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a5333U
                                                     : 0x000a4b33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a4333U
                                                     : 0x000a3b33U))))
                                        : ((8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                            ? ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000a3b33U
                                                     : 0x0009fb33U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x0009d3d3U
                                                     : 0x0009b333U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x0009b333U
                                                     : 0x0009abd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x0009abc4U
                                                     : 0x0009a3d3U)))
                                            : ((4U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                ? (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x0009a3c4U
                                                     : 0x00099bd3U)
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x00099bc4U
                                                     : 0x000993d3U))
                                                : (
                                                   (2U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))
                                                     ? 0x000993c4U
                                                     : 0x00097333U)
                                                    : 0x00096333U))))));
                    }
                }
            }
        } else if ((4U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
            if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                    if ((0U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000bd940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x0200U == (0xfe00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000d8940U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    } else if ((0x0400U == (0xffc0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = (0x000df060U | (0x0000000fU 
                                              & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                    }
                    if ((1U & (~ VL_ONEHOT_I((((0x0400U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 2U) 
                                              | (((0x0200U 
                                                   == 
                                                   (0xfe00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 1U) 
                                                 | (0U 
                                                    == 
                                                    (0xfe00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                        if ((0U != (((0x0400U == (0xffc0U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                     << 2U) | (((0x0200U 
                                                 == 
                                                 (0xfe00U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                << 1U) 
                                               | (0U 
                                                  == 
                                                  (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:1021: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 1021, "");
                            }
                        }
                    }
                } else {
                    if (((((((((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                               | (8U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                              | (0x0010U == (0xfff0U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                             | (0x0020U == (0xfff0U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                            | (0x0030U == (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                           | (0x0040U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                          | (0x0050U == (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) 
                         | (0x0100U == (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                            = ((0U == (0xfff8U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                ? (0x000b6850U | (0x0000000fU 
                                                  & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                : ((8U == (0xfff8U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                    ? (0x000d9050U 
                                       | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                    : ((0x0010U == 
                                        (0xfff0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                        ? 0x000c38b3U
                                        : ((0x0020U 
                                            == (0xfff0U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                            ? 0x000c40b3U
                                            : ((0x0030U 
                                                == 
                                                (0xfff0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                ? (0x000d9030U 
                                                   | (0x0000000fU 
                                                      & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r))
                                                : (
                                                   (0x0040U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                    ? 0x000e60b3U
                                                    : 
                                                   ((0x0050U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))
                                                     ? 0x000e68b3U
                                                     : 0x000c4a03U)))))));
                    } else if ((0x0200U == (0xff00U 
                                            & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000e7203U;
                    }
                    if ((1U & (~ VL_ONEHOT_I(((((((0x0200U 
                                                   == 
                                                   (0xff00U 
                                                    & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                  << 4U) 
                                                 | (((0x0100U 
                                                      == 
                                                      (0xff00U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                     << 3U) 
                                                    | ((0x0050U 
                                                        == 
                                                        (0xfff0U 
                                                         & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                       << 2U))) 
                                                | (((0x0040U 
                                                     == 
                                                     (0xfff0U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                    << 1U) 
                                                   | (0x0030U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                               << 4U) 
                                              | ((((0x0020U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0010U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                     << 2U)) 
                                                 | (((8U 
                                                      == 
                                                      (0xfff8U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                     << 1U) 
                                                    | (0U 
                                                       == 
                                                       (0xfff8U 
                                                        & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))))) {
                        if ((0U != ((((((0x0200U == 
                                         (0xff00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                        << 4U) | ((
                                                   (0x0100U 
                                                    == 
                                                    (0xff00U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 3U) 
                                                  | ((0x0050U 
                                                      == 
                                                      (0xfff0U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                     << 2U))) 
                                      | (((0x0040U 
                                           == (0xfff0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                          << 1U) | 
                                         (0x0030U == 
                                          (0xfff0U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))) 
                                     << 4U) | ((((0x0020U 
                                                  == 
                                                  (0xfff0U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 3U) 
                                                | ((0x0010U 
                                                    == 
                                                    (0xfff0U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 2U)) 
                                               | (((8U 
                                                    == 
                                                    (0xfff8U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 1U) 
                                                  | (0U 
                                                     == 
                                                     (0xfff8U 
                                                      & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))) {
                            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                                VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:964: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                             , '#',64,VL_TIME_UNITED_Q(1000)
                                             , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                                VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 964, "");
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                if ((0U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x0800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c2ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x1000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x1800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000e5ab0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x4000U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c2ac0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x4000U 
                                             == (0xc000U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                            << 4U) 
                                           | (((0x1800U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 3U) 
                                              | ((0x1000U 
                                                  == 
                                                  (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                 << 2U))) 
                                          | (((0x0800U 
                                               == (0xf800U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                    if ((0U != ((((0x4000U == (0xc000U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                  << 4U) | (((0x1800U 
                                              == (0xf800U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                             << 3U) 
                                            | ((0x1000U 
                                                == 
                                                (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                               << 2U))) 
                                | (((0x0800U == (0xf800U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                    << 1U) | (0U == 
                                              (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:933: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 933, "");
                        }
                    }
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x00089860U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000be810U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x0200U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000bd160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x0400U == (0xfe00U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000be160U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                }
                if ((1U & (~ VL_ONEHOT_I(((((0x0400U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                            << 3U) 
                                           | ((0x0200U 
                                               == (0xfe00U 
                                                   & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                              << 2U)) 
                                          | (((0x0040U 
                                               == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                              << 1U) 
                                             | (0U 
                                                == 
                                                (0xffc0U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))))) {
                    if ((0U != ((((0x0400U == (0xfe00U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                  << 3U) | ((0x0200U 
                                             == (0xfe00U 
                                                 & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                            << 2U)) 
                                | (((0x0040U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                                    << 1U) | (0U == 
                                              (0xffc0U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))))))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:907: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 907, "");
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
            if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
                if ((0x07ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000923f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x0800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x0bffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000ab380U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000bc9d0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x0c00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x0c7fU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000bc370U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000e0010U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if ((0x0c80U == (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000e0890U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x0d00U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x0dffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000d9b60U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x1000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x17ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x1800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x1fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x2000U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x27ffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c33e0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                } else if (((0x2800U <= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)) 
                            & (0x2fffU >= (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000c33f0U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                }
            } else {
                if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r 
                        = (0x000cc060U | (0x0000000fU 
                                          & vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r));
                }
                if ((0U != (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                    if ((0U == (0xffc0U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                        if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                            VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:839: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                         , '#',64,VL_TIME_UNITED_Q(1000)
                                         , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                            VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 839, "");
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__ext_root))) {
            if ((0U == (0xc000U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x0008d403U;
            } else if ((0x4000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000a0393U;
            } else if ((0x4800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000a0b93U;
            } else if ((0x5000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000a1393U;
            } else if ((0x5800U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000a1b93U;
            } else if ((0x6000U == (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))) {
                vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r = 0x000a2393U;
            }
            if ((1U & (~ VL_ONEHOT_I(((((0x6000U == 
                                         (0xf800U & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                        << 5U) | ((
                                                   (0x5800U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 4U) 
                                                  | ((0x5000U 
                                                      == 
                                                      (0xf800U 
                                                       & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                     << 3U))) 
                                      | (((0x4800U 
                                           == (0xf800U 
                                               & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                          << 2U) | 
                                         (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))))) {
                if ((0U != ((((0x6000U == (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                              << 5U) | (((0x5800U == 
                                          (0xf800U 
                                           & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                         << 4U) | (
                                                   (0x5000U 
                                                    == 
                                                    (0xf800U 
                                                     & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                                   << 3U))) 
                            | (((0x4800U == (0xf800U 
                                             & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                << 2U) | (((0x4000U 
                                            == (0xf800U 
                                                & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word))) 
                                           << 1U) | 
                                          (0U == (0xc000U 
                                                  & (IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word)))))))) {
                    if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                        VL_WRITEF_NX("[%0t] %%Error: bedrock_decode_pkg.sv:797: Assertion failed in %m: unique case, but multiple matches found for '16'h%X'\n",4, 'M',vlSymsp->name(),"bedrock_decode_pkg.bedrock_decode_extended_opcode", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',16,(IData)(vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__extension_word));
                        VL_STOP_MT("../build/generated/bedrock_decode_pkg.sv", 797, "");
                    }
                }
            }
        }
        vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__Vfuncout 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__r;
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode 
            = vlSelfRef.__Vfunc_bedrock_decode_extended_opcode__466__Vfuncout;
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw 
            = (1U & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode 
                     >> 0x00000013U));
        entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__opcode_id 
            = (0x000000ffU & (entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__extended_decode 
                              >> 0x0000000bU));
    }
    __Vfunc_bedrock_decode_opcode_attributes__467__opcode_id 
        = entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__opcode_id;
    __Vfunc_bedrock_decode_opcode_attributes__467__r = 0U;
    if ((0x00000080U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                          >> 5U)))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                              >> 4U)))) {
                    if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                                    __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
                                }
                            }
                        }
                    } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                                         >> 2U)))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                                    = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                                      >> 1U)))) {
                            if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                                __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
                            }
                        }
                    }
                } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                                     >> 1U)))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                        }
                    } else {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    }
                }
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                        }
                    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    }
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    }
                } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__467__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
            } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                          >> 1U)))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        }
    } else if ((0x00000040U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                        }
                    }
                } else if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                                     >> 2U)))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                                  >> 1U)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    }
                }
            } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                        }
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__467__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))))
                        : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
            }
        } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r 
                            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                    } else if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                        __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
                    }
                } else {
                    __Vfunc_bedrock_decode_opcode_attributes__467__r 
                        = ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)))
                            : 7U);
                }
            } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((1U & (~ ((IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id) 
                              >> 1U)))) {
                    __Vfunc_bedrock_decode_opcode_attributes__467__r 
                        = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
                }
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
            }
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            }
        }
    } else if ((0x00000020U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                    ? ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                        ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? 7U : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                                     ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))))
                        : ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))
                            : ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)))))
                    : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
        } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                    ? ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                        ? ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                            ? (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r))
                            : 7U) : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)))
                    : 7U);
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        }
    } else if ((0x00000010U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__467__r 
                        = (2U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                        ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
            }
        } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
                    __Vfunc_bedrock_decode_opcode_attributes__467__r 
                        = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
                }
            } else {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            }
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            if ((1U & (~ (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id)))) {
                __Vfunc_bedrock_decode_opcode_attributes__467__r 
                    = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
            }
        } else {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        }
    } else if ((8U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        }
    } else if ((4U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r 
                = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
        } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
            __Vfunc_bedrock_decode_opcode_attributes__467__r = 7U;
        }
    } else if ((2U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__467__r 
            = ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))
                ? 7U : (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r)));
    } else if ((1U & (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__opcode_id))) {
        __Vfunc_bedrock_decode_opcode_attributes__467__r 
            = (6U | (IData)(__Vfunc_bedrock_decode_opcode_attributes__467__r));
    }
    __Vfunc_bedrock_decode_opcode_attributes__467__Vfuncout 
        = __Vfunc_bedrock_decode_opcode_attributes__467__r;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__attributes 
        = __Vfunc_bedrock_decode_opcode_attributes__467__Vfuncout;
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repcc_allowed_raw 
        = ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__attributes) 
              >> 2U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_allowed_raw 
        = ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw) 
           & ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__attributes) 
              >> 1U));
    entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_fast_candidate_raw 
        = ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw) 
           & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode__DOT__attributes));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_34 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_33 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_32 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_31 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_30 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[2U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_29 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[2U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_28 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[3U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_27 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[3U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_26 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[4U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_25 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[4U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_24 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[5U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_23 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[5U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_22 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[6U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_21 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[6U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_20 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[7U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_19 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[7U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_18 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[8U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_17 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[8U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_16 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[9U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_15 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[9U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_14 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[10U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_13 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[10U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_12 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[11U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_11 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[11U] 
                                                    >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_10 = ((0U 
                                                  != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repeat_kind)) 
                                                 & (vlSelfRef.entry_precheck_tb__DOT__line_words[12U] 
                                                    >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_9 = ((0U 
                                                 != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repeat_kind)) 
                                                & (vlSelfRef.entry_precheck_tb__DOT__line_words[12U] 
                                                   >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_8 = ((0U 
                                                 != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repeat_kind)) 
                                                & (vlSelfRef.entry_precheck_tb__DOT__line_words[13U] 
                                                   >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_7 = ((0U 
                                                 != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repeat_kind)) 
                                                & (vlSelfRef.entry_precheck_tb__DOT__line_words[13U] 
                                                   >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_6 = ((0U 
                                                 != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repeat_kind)) 
                                                & (vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                                   >> 0x0000000fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_5 = ((0U 
                                                 != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repeat_kind)) 
                                                & (vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                                   >> 0x0000001fU));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_4 = ((0U 
                                                 != (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repeat_kind)) 
                                                & (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                                                   >> 0x0000000fU));
    vlSelfRef.entry_precheck_tb__DOT__entry_valid = 
        (((((((((2U & ((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                           >> 0x0000001fU)) << 1U)) 
                | (1U & ((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                             >> 0x0000000fU)) | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__prefix_valid_raw)))) 
               << 6U) | (((2U & (((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                      >> 0x0000001fU)) 
                                  | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__prefix_valid_raw)) 
                                 << 1U)) | (1U & ((~ 
                                                   (vlSelfRef.entry_precheck_tb__DOT__line_words[14U] 
                                                    >> 0x0000000fU)) 
                                                  | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__prefix_valid_raw)))) 
                         << 4U)) | ((((2U & (((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[13U] 
                                                  >> 0x0000001fU)) 
                                              | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__prefix_valid_raw)) 
                                             << 1U)) 
                                      | (1U & ((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[13U] 
                                                   >> 0x0000000fU)) 
                                               | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__prefix_valid_raw)))) 
                                     << 2U) | ((2U 
                                                & (((~ 
                                                     (vlSelfRef.entry_precheck_tb__DOT__line_words[12U] 
                                                      >> 0x0000001fU)) 
                                                    | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__prefix_valid_raw)) 
                                                   << 1U)) 
                                               | (1U 
                                                  & ((~ 
                                                      (vlSelfRef.entry_precheck_tb__DOT__line_words[12U] 
                                                       >> 0x0000000fU)) 
                                                     | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__prefix_valid_raw)))))) 
            << 0x00000018U) | ((((((2U & (((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[11U] 
                                               >> 0x0000001fU)) 
                                           | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__prefix_valid_raw)) 
                                          << 1U)) | 
                                   (1U & ((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[11U] 
                                              >> 0x0000000fU)) 
                                          | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__prefix_valid_raw)))) 
                                  << 6U) | (((2U & 
                                              (((~ 
                                                 (vlSelfRef.entry_precheck_tb__DOT__line_words[10U] 
                                                  >> 0x0000001fU)) 
                                                | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__prefix_valid_raw)) 
                                               << 1U)) 
                                             | (1U 
                                                & ((~ 
                                                    (vlSelfRef.entry_precheck_tb__DOT__line_words[10U] 
                                                     >> 0x0000000fU)) 
                                                   | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__prefix_valid_raw)))) 
                                            << 4U)) 
                                | ((((2U & (((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[9U] 
                                                 >> 0x0000001fU)) 
                                             | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__prefix_valid_raw)) 
                                            << 1U)) 
                                     | (1U & ((~ (vlSelfRef.entry_precheck_tb__DOT__line_words[9U] 
                                                  >> 0x0000000fU)) 
                                              | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__prefix_valid_raw)))) 
                                    << 2U) | ((2U & 
                                               (((~ 
                                                  (vlSelfRef.entry_precheck_tb__DOT__line_words[8U] 
                                                   >> 0x0000001fU)) 
                                                 | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__prefix_valid_raw)) 
                                                << 1U)) 
                                              | (1U 
                                                 & ((~ 
                                                     (vlSelfRef.entry_precheck_tb__DOT__line_words[8U] 
                                                      >> 0x0000000fU)) 
                                                    | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__prefix_valid_raw)))))) 
                               << 0x00000010U)) | (
                                                   ((((((2U 
                                                         & (((~ 
                                                              (vlSelfRef.entry_precheck_tb__DOT__line_words[7U] 
                                                               >> 0x0000001fU)) 
                                                             | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__prefix_valid_raw)) 
                                                            << 1U)) 
                                                        | (1U 
                                                           & ((~ 
                                                               (vlSelfRef.entry_precheck_tb__DOT__line_words[7U] 
                                                                >> 0x0000000fU)) 
                                                              | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__prefix_valid_raw)))) 
                                                       << 6U) 
                                                      | (((2U 
                                                           & (((~ 
                                                                (vlSelfRef.entry_precheck_tb__DOT__line_words[6U] 
                                                                 >> 0x0000001fU)) 
                                                               | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__prefix_valid_raw)) 
                                                              << 1U)) 
                                                          | (1U 
                                                             & ((~ 
                                                                 (vlSelfRef.entry_precheck_tb__DOT__line_words[6U] 
                                                                  >> 0x0000000fU)) 
                                                                | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__prefix_valid_raw)))) 
                                                         << 4U)) 
                                                     | ((((2U 
                                                           & (((~ 
                                                                (vlSelfRef.entry_precheck_tb__DOT__line_words[5U] 
                                                                 >> 0x0000001fU)) 
                                                               | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__prefix_valid_raw)) 
                                                              << 1U)) 
                                                          | (1U 
                                                             & ((~ 
                                                                 (vlSelfRef.entry_precheck_tb__DOT__line_words[5U] 
                                                                  >> 0x0000000fU)) 
                                                                | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__prefix_valid_raw)))) 
                                                         << 2U) 
                                                        | ((2U 
                                                            & (((~ 
                                                                 (vlSelfRef.entry_precheck_tb__DOT__line_words[4U] 
                                                                  >> 0x0000001fU)) 
                                                                | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__prefix_valid_raw)) 
                                                               << 1U)) 
                                                           | (1U 
                                                              & ((~ 
                                                                  (vlSelfRef.entry_precheck_tb__DOT__line_words[4U] 
                                                                   >> 0x0000000fU)) 
                                                                 | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__prefix_valid_raw)))))) 
                                                    << 8U) 
                                                   | (((((2U 
                                                          & (((~ 
                                                               (vlSelfRef.entry_precheck_tb__DOT__line_words[3U] 
                                                                >> 0x0000001fU)) 
                                                              | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__prefix_valid_raw)) 
                                                             << 1U)) 
                                                         | (1U 
                                                            & ((~ 
                                                                (vlSelfRef.entry_precheck_tb__DOT__line_words[3U] 
                                                                 >> 0x0000000fU)) 
                                                               | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__prefix_valid_raw)))) 
                                                        << 6U) 
                                                       | (((2U 
                                                            & (((~ 
                                                                 (vlSelfRef.entry_precheck_tb__DOT__line_words[2U] 
                                                                  >> 0x0000001fU)) 
                                                                | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__prefix_valid_raw)) 
                                                               << 1U)) 
                                                           | (1U 
                                                              & ((~ 
                                                                  (vlSelfRef.entry_precheck_tb__DOT__line_words[2U] 
                                                                   >> 0x0000000fU)) 
                                                                 | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__prefix_valid_raw)))) 
                                                          << 4U)) 
                                                      | ((((2U 
                                                            & (((~ 
                                                                 (vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                                                  >> 0x0000001fU)) 
                                                                | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__prefix_valid_raw)) 
                                                               << 1U)) 
                                                           | (1U 
                                                              & ((~ 
                                                                  (vlSelfRef.entry_precheck_tb__DOT__line_words[1U] 
                                                                   >> 0x0000000fU)) 
                                                                 | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__prefix_valid_raw)))) 
                                                          << 2U) 
                                                         | ((2U 
                                                             & (((~ 
                                                                  (vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                                                                   >> 0x0000001fU)) 
                                                                 | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__prefix_valid_raw)) 
                                                                << 1U)) 
                                                            | (1U 
                                                               & ((~ 
                                                                   (vlSelfRef.entry_precheck_tb__DOT__line_words[0U] 
                                                                    >> 0x0000000fU)) 
                                                                  | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__prefix_valid_raw)))))))) 
         & ((((((((((~ (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__needs_extension)) 
                    & (IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__decode_valid_raw)) 
                   << 3U) | (((~ ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__needs_extension) 
                                  & (vlSelfRef.entry_precheck_tb__DOT__line_words[15U] 
                                     >> 0x0000000fU))) 
                              & (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__decode_valid_raw)) 
                             << 2U)) | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__decode_valid_raw) 
                                         << 1U) | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__decode_valid_raw))) 
                << 0x0000000cU) | (((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__decode_valid_raw) 
                                      << 3U) | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__decode_valid_raw) 
                                                << 2U)) 
                                    | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__decode_valid_raw) 
                                        << 1U) | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__decode_valid_raw))) 
                                   << 8U)) | ((((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__decode_valid_raw) 
                                                  << 3U) 
                                                 | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__decode_valid_raw) 
                                                    << 2U)) 
                                                | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__decode_valid_raw) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__decode_valid_raw))) 
                                               << 4U) 
                                              | ((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__decode_valid_raw) 
                                                   << 3U) 
                                                  | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__decode_valid_raw) 
                                                     << 2U)) 
                                                 | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__decode_valid_raw) 
                                                     << 1U) 
                                                    | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__decode_valid_raw))))) 
             << 0x00000010U) | (((((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__decode_valid_raw) 
                                     << 3U) | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__decode_valid_raw) 
                                               << 2U)) 
                                   | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__decode_valid_raw) 
                                       << 1U) | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__decode_valid_raw))) 
                                  << 0x0000000cU) | 
                                 (((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__decode_valid_raw) 
                                     << 3U) | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__decode_valid_raw) 
                                               << 2U)) 
                                   | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__decode_valid_raw) 
                                       << 1U) | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__decode_valid_raw))) 
                                  << 8U)) | ((((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__decode_valid_raw) 
                                                 << 3U) 
                                                | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__decode_valid_raw) 
                                                   << 2U)) 
                                               | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__decode_valid_raw) 
                                                   << 1U) 
                                                  | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__decode_valid_raw))) 
                                              << 4U) 
                                             | ((((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__decode_valid_raw) 
                                                  << 3U) 
                                                 | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__decode_valid_raw) 
                                                    << 2U)) 
                                                | (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__decode_valid_raw) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__decode_valid_raw)))))));
    vlSelfRef.entry_precheck_tb__DOT__repg_fast_candidate 
        = ((((((((2U & (((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_fast_candidate_raw) 
                         << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                   >> 0x0000001eU))) 
                 | ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_fast_candidate_raw) 
                    & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                       >> 0x0000001eU))) << 6U) | (
                                                   ((0x0000000eU 
                                                     & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repg_fast_candidate_raw) 
                                                         << 1U) 
                                                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                           >> 0x0000001cU))) 
                                                    | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repg_fast_candidate_raw) 
                                                       & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                          >> 0x0000001cU))) 
                                                   << 4U)) 
              | ((((0x0000003eU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repg_fast_candidate_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000001aU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repg_fast_candidate_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000001aU))) << 2U) | 
                 ((0x000000feU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repg_fast_candidate_raw) 
                                   << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                             >> 0x00000018U))) 
                  | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repg_fast_candidate_raw) 
                     & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                        >> 0x00000018U))))) << 0x00000018U) 
            | ((((((0x000003feU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repg_fast_candidate_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x00000016U))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repg_fast_candidate_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x00000016U))) << 6U) | 
                 (((0x00000ffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repg_fast_candidate_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x00000014U))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repg_fast_candidate_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x00000014U))) << 4U)) 
                | ((((0x00003ffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repg_fast_candidate_raw) 
                                      << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                >> 0x00000012U))) 
                     | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repg_fast_candidate_raw) 
                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                           >> 0x00000012U))) << 2U) 
                   | ((0x0000fffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repg_fast_candidate_raw) 
                                       << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                 >> 0x00000010U))) 
                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repg_fast_candidate_raw) 
                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                            >> 0x00000010U))))) << 0x00000010U)) 
           | (((((((0x0003fffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repg_fast_candidate_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000000eU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repg_fast_candidate_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000000eU))) << 6U) | 
                 (((0x000ffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repg_fast_candidate_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000000cU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repg_fast_candidate_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000000cU))) << 4U)) 
                | ((((0x003ffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repg_fast_candidate_raw) 
                                      << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                >> 0x0000000aU))) 
                     | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repg_fast_candidate_raw) 
                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                           >> 0x0000000aU))) << 2U) 
                   | ((0x00fffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repg_fast_candidate_raw) 
                                       << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                 >> 8U))) 
                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repg_fast_candidate_raw) 
                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                            >> 8U))))) << 8U) | (((
                                                   ((0x03fffffeU 
                                                     & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repg_fast_candidate_raw) 
                                                         << 1U) 
                                                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                           >> 6U))) 
                                                    | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repg_fast_candidate_raw) 
                                                       & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                          >> 6U))) 
                                                   << 6U) 
                                                  | (((0x0ffffffeU 
                                                       & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repg_fast_candidate_raw) 
                                                           << 1U) 
                                                          & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                             >> 4U))) 
                                                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repg_fast_candidate_raw) 
                                                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                            >> 4U))) 
                                                     << 4U)) 
                                                 | ((((0x3ffffffeU 
                                                       & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repg_fast_candidate_raw) 
                                                           << 1U) 
                                                          & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                             >> 2U))) 
                                                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repg_fast_candidate_raw) 
                                                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                            >> 2U))) 
                                                     << 2U) 
                                                    | ((0xfffffffeU 
                                                        & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repg_fast_candidate_raw) 
                                                            << 1U) 
                                                           & vlSelfRef.entry_precheck_tb__DOT__entry_valid)) 
                                                       | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repg_fast_candidate_raw) 
                                                          & vlSelfRef.entry_precheck_tb__DOT__entry_valid))))));
    vlSelfRef.entry_precheck_tb__DOT__repcc_allowed 
        = ((((((((2U & (((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repcc_allowed_raw) 
                         << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                   >> 0x0000001eU))) 
                 | ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repcc_allowed_raw) 
                    & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                       >> 0x0000001eU))) << 6U) | (
                                                   ((0x0000000eU 
                                                     & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repcc_allowed_raw) 
                                                         << 1U) 
                                                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                           >> 0x0000001cU))) 
                                                    | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repcc_allowed_raw) 
                                                       & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                          >> 0x0000001cU))) 
                                                   << 4U)) 
              | ((((0x0000003eU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repcc_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000001aU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repcc_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000001aU))) << 2U) | 
                 ((0x000000feU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repcc_allowed_raw) 
                                   << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                             >> 0x00000018U))) 
                  | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repcc_allowed_raw) 
                     & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                        >> 0x00000018U))))) << 0x00000018U) 
            | ((((((0x000003feU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repcc_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x00000016U))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repcc_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x00000016U))) << 6U) | 
                 (((0x00000ffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repcc_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x00000014U))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repcc_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x00000014U))) << 4U)) 
                | ((((0x00003ffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repcc_allowed_raw) 
                                      << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                >> 0x00000012U))) 
                     | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repcc_allowed_raw) 
                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                           >> 0x00000012U))) << 2U) 
                   | ((0x0000fffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repcc_allowed_raw) 
                                       << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                 >> 0x00000010U))) 
                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repcc_allowed_raw) 
                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                            >> 0x00000010U))))) << 0x00000010U)) 
           | (((((((0x0003fffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repcc_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000000eU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repcc_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000000eU))) << 6U) | 
                 (((0x000ffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repcc_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000000cU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repcc_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000000cU))) << 4U)) 
                | ((((0x003ffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repcc_allowed_raw) 
                                      << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                >> 0x0000000aU))) 
                     | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repcc_allowed_raw) 
                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                           >> 0x0000000aU))) << 2U) 
                   | ((0x00fffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repcc_allowed_raw) 
                                       << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                 >> 8U))) 
                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repcc_allowed_raw) 
                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                            >> 8U))))) << 8U) | (((
                                                   ((0x03fffffeU 
                                                     & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repcc_allowed_raw) 
                                                         << 1U) 
                                                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                           >> 6U))) 
                                                    | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repcc_allowed_raw) 
                                                       & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                          >> 6U))) 
                                                   << 6U) 
                                                  | (((0x0ffffffeU 
                                                       & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repcc_allowed_raw) 
                                                           << 1U) 
                                                          & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                             >> 4U))) 
                                                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repcc_allowed_raw) 
                                                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                            >> 4U))) 
                                                     << 4U)) 
                                                 | ((((0x3ffffffeU 
                                                       & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repcc_allowed_raw) 
                                                           << 1U) 
                                                          & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                             >> 2U))) 
                                                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repcc_allowed_raw) 
                                                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                            >> 2U))) 
                                                     << 2U) 
                                                    | ((0xfffffffeU 
                                                        & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repcc_allowed_raw) 
                                                            << 1U) 
                                                           & vlSelfRef.entry_precheck_tb__DOT__entry_valid)) 
                                                       | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repcc_allowed_raw) 
                                                          & vlSelfRef.entry_precheck_tb__DOT__entry_valid))))));
    vlSelfRef.entry_precheck_tb__DOT__repg_allowed 
        = ((((((((2U & (((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repg_allowed_raw) 
                         << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                   >> 0x0000001eU))) 
                 | ((IData)(entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repg_allowed_raw) 
                    & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                       >> 0x0000001eU))) << 6U) | (
                                                   ((0x0000000eU 
                                                     & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repg_allowed_raw) 
                                                         << 1U) 
                                                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                           >> 0x0000001cU))) 
                                                    | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repg_allowed_raw) 
                                                       & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                          >> 0x0000001cU))) 
                                                   << 4U)) 
              | ((((0x0000003eU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repg_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000001aU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repg_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000001aU))) << 2U) | 
                 ((0x000000feU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repg_allowed_raw) 
                                   << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                             >> 0x00000018U))) 
                  | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repg_allowed_raw) 
                     & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                        >> 0x00000018U))))) << 0x00000018U) 
            | ((((((0x000003feU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repg_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x00000016U))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repg_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x00000016U))) << 6U) | 
                 (((0x00000ffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repg_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x00000014U))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repg_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x00000014U))) << 4U)) 
                | ((((0x00003ffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repg_allowed_raw) 
                                      << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                >> 0x00000012U))) 
                     | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repg_allowed_raw) 
                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                           >> 0x00000012U))) << 2U) 
                   | ((0x0000fffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repg_allowed_raw) 
                                       << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                 >> 0x00000010U))) 
                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repg_allowed_raw) 
                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                            >> 0x00000010U))))) << 0x00000010U)) 
           | (((((((0x0003fffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repg_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000000eU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repg_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000000eU))) << 6U) | 
                 (((0x000ffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repg_allowed_raw) 
                                    << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                              >> 0x0000000cU))) 
                   | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repg_allowed_raw) 
                      & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                         >> 0x0000000cU))) << 4U)) 
                | ((((0x003ffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repg_allowed_raw) 
                                      << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                >> 0x0000000aU))) 
                     | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repg_allowed_raw) 
                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                           >> 0x0000000aU))) << 2U) 
                   | ((0x00fffffeU & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repg_allowed_raw) 
                                       << 1U) & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                 >> 8U))) 
                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repg_allowed_raw) 
                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                            >> 8U))))) << 8U) | (((
                                                   ((0x03fffffeU 
                                                     & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repg_allowed_raw) 
                                                         << 1U) 
                                                        & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                           >> 6U))) 
                                                    | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repg_allowed_raw) 
                                                       & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                          >> 6U))) 
                                                   << 6U) 
                                                  | (((0x0ffffffeU 
                                                       & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repg_allowed_raw) 
                                                           << 1U) 
                                                          & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                             >> 4U))) 
                                                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repg_allowed_raw) 
                                                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                            >> 4U))) 
                                                     << 4U)) 
                                                 | ((((0x3ffffffeU 
                                                       & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repg_allowed_raw) 
                                                           << 1U) 
                                                          & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                             >> 2U))) 
                                                      | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repg_allowed_raw) 
                                                         & (vlSelfRef.entry_precheck_tb__DOT__entry_valid 
                                                            >> 2U))) 
                                                     << 2U) 
                                                    | ((0xfffffffeU 
                                                        & (((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repg_allowed_raw) 
                                                            << 1U) 
                                                           & vlSelfRef.entry_precheck_tb__DOT__entry_valid)) 
                                                       | ((IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repg_allowed_raw) 
                                                          & vlSelfRef.entry_precheck_tb__DOT__entry_valid))))));
    __VdfgRegularize_hebeb780c_0_1 = (vlSelfRef.entry_precheck_tb__DOT__repcc_allowed 
                                      & vlSelfRef.entry_precheck_tb__DOT__entry_valid);
    __VdfgRegularize_hebeb780c_0_2 = (vlSelfRef.entry_precheck_tb__DOT__repg_allowed 
                                      & vlSelfRef.entry_precheck_tb__DOT__entry_valid);
    vlSelfRef.entry_precheck_tb__DOT__repcc_valid = 
        ((((((((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repeat_kind)) 
                 & (__VdfgRegularize_hebeb780c_0_1 
                    >> 0x0000001fU)) << 3U) | (((1U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_1 
                                                   >> 0x0000001eU)) 
                                               << 2U)) 
              | ((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repeat_kind)) 
                   & (__VdfgRegularize_hebeb780c_0_1 
                      >> 0x0000001dU)) << 1U) | ((1U 
                                                  == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repeat_kind)) 
                                                 & (__VdfgRegularize_hebeb780c_0_1 
                                                    >> 0x0000001cU)))) 
             << 0x0000000cU) | ((((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repeat_kind)) 
                                    & (__VdfgRegularize_hebeb780c_0_1 
                                       >> 0x0000001bU)) 
                                   << 3U) | (((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repeat_kind)) 
                                              & (__VdfgRegularize_hebeb780c_0_1 
                                                 >> 0x0000001aU)) 
                                             << 2U)) 
                                 | ((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repeat_kind)) 
                                      & (__VdfgRegularize_hebeb780c_0_1 
                                         >> 0x00000019U)) 
                                     << 1U) | ((1U 
                                                == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repeat_kind)) 
                                               & (__VdfgRegularize_hebeb780c_0_1 
                                                  >> 0x00000018U)))) 
                                << 8U)) | (((((((1U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_1 
                                                   >> 0x00000017U)) 
                                               << 3U) 
                                              | (((1U 
                                                   == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repeat_kind)) 
                                                  & (__VdfgRegularize_hebeb780c_0_1 
                                                     >> 0x00000016U)) 
                                                 << 2U)) 
                                             | ((((1U 
                                                   == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repeat_kind)) 
                                                  & (__VdfgRegularize_hebeb780c_0_1 
                                                     >> 0x00000015U)) 
                                                 << 1U) 
                                                | ((1U 
                                                    == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repeat_kind)) 
                                                   & (__VdfgRegularize_hebeb780c_0_1 
                                                      >> 0x00000014U)))) 
                                            << 4U) 
                                           | (((((1U 
                                                  == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repeat_kind)) 
                                                 & (__VdfgRegularize_hebeb780c_0_1 
                                                    >> 0x00000013U)) 
                                                << 3U) 
                                               | (((1U 
                                                    == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repeat_kind)) 
                                                   & (__VdfgRegularize_hebeb780c_0_1 
                                                      >> 0x00000012U)) 
                                                  << 2U)) 
                                              | ((((1U 
                                                    == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repeat_kind)) 
                                                   & (__VdfgRegularize_hebeb780c_0_1 
                                                      >> 0x00000011U)) 
                                                  << 1U) 
                                                 | ((1U 
                                                     == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repeat_kind)) 
                                                    & (__VdfgRegularize_hebeb780c_0_1 
                                                       >> 0x00000010U)))))) 
          << 0x00000010U) | ((((((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repeat_kind)) 
                                   & (__VdfgRegularize_hebeb780c_0_1 
                                      >> 0x0000000fU)) 
                                  << 3U) | (((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repeat_kind)) 
                                             & (__VdfgRegularize_hebeb780c_0_1 
                                                >> 0x0000000eU)) 
                                            << 2U)) 
                                | ((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repeat_kind)) 
                                     & (__VdfgRegularize_hebeb780c_0_1 
                                        >> 0x0000000dU)) 
                                    << 1U) | ((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repeat_kind)) 
                                              & (__VdfgRegularize_hebeb780c_0_1 
                                                 >> 0x0000000cU)))) 
                               << 0x0000000cU) | ((
                                                   ((((1U 
                                                       == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repeat_kind)) 
                                                      & (__VdfgRegularize_hebeb780c_0_1 
                                                         >> 0x0000000bU)) 
                                                     << 3U) 
                                                    | (((1U 
                                                         == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repeat_kind)) 
                                                        & (__VdfgRegularize_hebeb780c_0_1 
                                                           >> 0x0000000aU)) 
                                                       << 2U)) 
                                                   | ((((1U 
                                                         == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repeat_kind)) 
                                                        & (__VdfgRegularize_hebeb780c_0_1 
                                                           >> 9U)) 
                                                       << 1U) 
                                                      | ((1U 
                                                          == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repeat_kind)) 
                                                         & (__VdfgRegularize_hebeb780c_0_1 
                                                            >> 8U)))) 
                                                  << 8U)) 
                             | (((((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repeat_kind)) 
                                     & (__VdfgRegularize_hebeb780c_0_1 
                                        >> 7U)) << 3U) 
                                   | (((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repeat_kind)) 
                                       & (__VdfgRegularize_hebeb780c_0_1 
                                          >> 6U)) << 2U)) 
                                  | ((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repeat_kind)) 
                                       & (__VdfgRegularize_hebeb780c_0_1 
                                          >> 5U)) << 1U) 
                                     | ((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repeat_kind)) 
                                        & (__VdfgRegularize_hebeb780c_0_1 
                                           >> 4U)))) 
                                 << 4U) | (((((1U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repeat_kind)) 
                                              & (__VdfgRegularize_hebeb780c_0_1 
                                                 >> 3U)) 
                                             << 3U) 
                                            | (((1U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_1 
                                                   >> 2U)) 
                                               << 2U)) 
                                           | ((((1U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_1 
                                                   >> 1U)) 
                                               << 1U) 
                                              | ((1U 
                                                  == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repeat_kind)) 
                                                 & __VdfgRegularize_hebeb780c_0_1))))));
    vlSelfRef.entry_precheck_tb__DOT__repg_valid = 
        ((((((((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__31__KET____DOT__repeat_kind)) 
                 & (__VdfgRegularize_hebeb780c_0_2 
                    >> 0x0000001fU)) << 3U) | (((2U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__30__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_2 
                                                   >> 0x0000001eU)) 
                                               << 2U)) 
              | ((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__29__KET____DOT__repeat_kind)) 
                   & (__VdfgRegularize_hebeb780c_0_2 
                      >> 0x0000001dU)) << 1U) | ((2U 
                                                  == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__28__KET____DOT__repeat_kind)) 
                                                 & (__VdfgRegularize_hebeb780c_0_2 
                                                    >> 0x0000001cU)))) 
             << 0x0000000cU) | ((((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__27__KET____DOT__repeat_kind)) 
                                    & (__VdfgRegularize_hebeb780c_0_2 
                                       >> 0x0000001bU)) 
                                   << 3U) | (((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__26__KET____DOT__repeat_kind)) 
                                              & (__VdfgRegularize_hebeb780c_0_2 
                                                 >> 0x0000001aU)) 
                                             << 2U)) 
                                 | ((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__25__KET____DOT__repeat_kind)) 
                                      & (__VdfgRegularize_hebeb780c_0_2 
                                         >> 0x00000019U)) 
                                     << 1U) | ((2U 
                                                == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__24__KET____DOT__repeat_kind)) 
                                               & (__VdfgRegularize_hebeb780c_0_2 
                                                  >> 0x00000018U)))) 
                                << 8U)) | (((((((2U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__23__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_2 
                                                   >> 0x00000017U)) 
                                               << 3U) 
                                              | (((2U 
                                                   == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__22__KET____DOT__repeat_kind)) 
                                                  & (__VdfgRegularize_hebeb780c_0_2 
                                                     >> 0x00000016U)) 
                                                 << 2U)) 
                                             | ((((2U 
                                                   == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__21__KET____DOT__repeat_kind)) 
                                                  & (__VdfgRegularize_hebeb780c_0_2 
                                                     >> 0x00000015U)) 
                                                 << 1U) 
                                                | ((2U 
                                                    == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__20__KET____DOT__repeat_kind)) 
                                                   & (__VdfgRegularize_hebeb780c_0_2 
                                                      >> 0x00000014U)))) 
                                            << 4U) 
                                           | (((((2U 
                                                  == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__19__KET____DOT__repeat_kind)) 
                                                 & (__VdfgRegularize_hebeb780c_0_2 
                                                    >> 0x00000013U)) 
                                                << 3U) 
                                               | (((2U 
                                                    == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__18__KET____DOT__repeat_kind)) 
                                                   & (__VdfgRegularize_hebeb780c_0_2 
                                                      >> 0x00000012U)) 
                                                  << 2U)) 
                                              | ((((2U 
                                                    == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__17__KET____DOT__repeat_kind)) 
                                                   & (__VdfgRegularize_hebeb780c_0_2 
                                                      >> 0x00000011U)) 
                                                  << 1U) 
                                                 | ((2U 
                                                     == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__16__KET____DOT__repeat_kind)) 
                                                    & (__VdfgRegularize_hebeb780c_0_2 
                                                       >> 0x00000010U)))))) 
          << 0x00000010U) | ((((((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__15__KET____DOT__repeat_kind)) 
                                   & (__VdfgRegularize_hebeb780c_0_2 
                                      >> 0x0000000fU)) 
                                  << 3U) | (((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__14__KET____DOT__repeat_kind)) 
                                             & (__VdfgRegularize_hebeb780c_0_2 
                                                >> 0x0000000eU)) 
                                            << 2U)) 
                                | ((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__13__KET____DOT__repeat_kind)) 
                                     & (__VdfgRegularize_hebeb780c_0_2 
                                        >> 0x0000000dU)) 
                                    << 1U) | ((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__12__KET____DOT__repeat_kind)) 
                                              & (__VdfgRegularize_hebeb780c_0_2 
                                                 >> 0x0000000cU)))) 
                               << 0x0000000cU) | ((
                                                   ((((2U 
                                                       == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__11__KET____DOT__repeat_kind)) 
                                                      & (__VdfgRegularize_hebeb780c_0_2 
                                                         >> 0x0000000bU)) 
                                                     << 3U) 
                                                    | (((2U 
                                                         == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__10__KET____DOT__repeat_kind)) 
                                                        & (__VdfgRegularize_hebeb780c_0_2 
                                                           >> 0x0000000aU)) 
                                                       << 2U)) 
                                                   | ((((2U 
                                                         == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__9__KET____DOT__repeat_kind)) 
                                                        & (__VdfgRegularize_hebeb780c_0_2 
                                                           >> 9U)) 
                                                       << 1U) 
                                                      | ((2U 
                                                          == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__8__KET____DOT__repeat_kind)) 
                                                         & (__VdfgRegularize_hebeb780c_0_2 
                                                            >> 8U)))) 
                                                  << 8U)) 
                             | (((((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__7__KET____DOT__repeat_kind)) 
                                     & (__VdfgRegularize_hebeb780c_0_2 
                                        >> 7U)) << 3U) 
                                   | (((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__6__KET____DOT__repeat_kind)) 
                                       & (__VdfgRegularize_hebeb780c_0_2 
                                          >> 6U)) << 2U)) 
                                  | ((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__5__KET____DOT__repeat_kind)) 
                                       & (__VdfgRegularize_hebeb780c_0_2 
                                          >> 5U)) << 1U) 
                                     | ((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__4__KET____DOT__repeat_kind)) 
                                        & (__VdfgRegularize_hebeb780c_0_2 
                                           >> 4U)))) 
                                 << 4U) | (((((2U == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__3__KET____DOT__repeat_kind)) 
                                              & (__VdfgRegularize_hebeb780c_0_2 
                                                 >> 3U)) 
                                             << 3U) 
                                            | (((2U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__2__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_2 
                                                   >> 2U)) 
                                               << 2U)) 
                                           | ((((2U 
                                                 == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__1__KET____DOT__repeat_kind)) 
                                                & (__VdfgRegularize_hebeb780c_0_2 
                                                   >> 1U)) 
                                               << 1U) 
                                              | ((2U 
                                                  == (IData)(vlSelfRef.entry_precheck_tb__DOT__dut__DOT__gen_entry__BRA__0__KET____DOT__repeat_kind)) 
                                                 & __VdfgRegularize_hebeb780c_0_2))))));
    __VdfgRegularize_hebeb780c_0_0 = (vlSelfRef.entry_precheck_tb__DOT__repcc_valid 
                                      | vlSelfRef.entry_precheck_tb__DOT__repg_valid);
    vlSelfRef.entry_precheck_tb__DOT__repeat_invalid 
        = ((((((((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_3)) 
                       | (__VdfgRegularize_hebeb780c_0_0 
                          >> 0x0000001fU))) & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_3)) 
                  << 3U) | (((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_4)) 
                                 | (__VdfgRegularize_hebeb780c_0_0 
                                    >> 0x0000001eU))) 
                             & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_4)) 
                            << 2U)) | ((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_5)) 
                                             | (__VdfgRegularize_hebeb780c_0_0 
                                                >> 0x0000001dU))) 
                                         & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_5)) 
                                        << 1U) | ((~ 
                                                   ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_6)) 
                                                    | (__VdfgRegularize_hebeb780c_0_0 
                                                       >> 0x0000001cU))) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_6)))) 
               << 0x0000000cU) | ((((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_7)) 
                                          | (__VdfgRegularize_hebeb780c_0_0 
                                             >> 0x0000001bU))) 
                                      & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_7)) 
                                     << 3U) | (((~ 
                                                 ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_8)) 
                                                  | (__VdfgRegularize_hebeb780c_0_0 
                                                     >> 0x0000001aU))) 
                                                & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_8)) 
                                               << 2U)) 
                                   | ((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_9)) 
                                            | (__VdfgRegularize_hebeb780c_0_0 
                                               >> 0x00000019U))) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_9)) 
                                       << 1U) | ((~ 
                                                  ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_10)) 
                                                   | (__VdfgRegularize_hebeb780c_0_0 
                                                      >> 0x00000018U))) 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_10)))) 
                                  << 8U)) | (((((((~ 
                                                   ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_11)) 
                                                    | (__VdfgRegularize_hebeb780c_0_0 
                                                       >> 0x00000017U))) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_11)) 
                                                 << 3U) 
                                                | (((~ 
                                                     ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_12)) 
                                                      | (__VdfgRegularize_hebeb780c_0_0 
                                                         >> 0x00000016U))) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_12)) 
                                                   << 2U)) 
                                               | ((((~ 
                                                     ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_13)) 
                                                      | (__VdfgRegularize_hebeb780c_0_0 
                                                         >> 0x00000015U))) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_13)) 
                                                   << 1U) 
                                                  | ((~ 
                                                      ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_14)) 
                                                       | (__VdfgRegularize_hebeb780c_0_0 
                                                          >> 0x00000014U))) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_14)))) 
                                              << 4U) 
                                             | (((((~ 
                                                    ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_15)) 
                                                     | (__VdfgRegularize_hebeb780c_0_0 
                                                        >> 0x00000013U))) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_15)) 
                                                  << 3U) 
                                                 | (((~ 
                                                      ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_16)) 
                                                       | (__VdfgRegularize_hebeb780c_0_0 
                                                          >> 0x00000012U))) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_16)) 
                                                    << 2U)) 
                                                | ((((~ 
                                                      ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_17)) 
                                                       | (__VdfgRegularize_hebeb780c_0_0 
                                                          >> 0x00000011U))) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_17)) 
                                                    << 1U) 
                                                   | ((~ 
                                                       ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_18)) 
                                                        | (__VdfgRegularize_hebeb780c_0_0 
                                                           >> 0x00000010U))) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_18)))))) 
            << 0x00000010U) | ((((((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_19)) 
                                         | (__VdfgRegularize_hebeb780c_0_0 
                                            >> 0x0000000fU))) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_19)) 
                                    << 3U) | (((~ (
                                                   (~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_20)) 
                                                   | (__VdfgRegularize_hebeb780c_0_0 
                                                      >> 0x0000000eU))) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_20)) 
                                              << 2U)) 
                                  | ((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_21)) 
                                           | (__VdfgRegularize_hebeb780c_0_0 
                                              >> 0x0000000dU))) 
                                       & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_21)) 
                                      << 1U) | ((~ 
                                                 ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_22)) 
                                                  | (__VdfgRegularize_hebeb780c_0_0 
                                                     >> 0x0000000cU))) 
                                                & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_22)))) 
                                 << 0x0000000cU) | 
                                ((((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_23)) 
                                         | (__VdfgRegularize_hebeb780c_0_0 
                                            >> 0x0000000bU))) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_23)) 
                                    << 3U) | (((~ (
                                                   (~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_24)) 
                                                   | (__VdfgRegularize_hebeb780c_0_0 
                                                      >> 0x0000000aU))) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_24)) 
                                              << 2U)) 
                                  | ((((~ ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_25)) 
                                           | (__VdfgRegularize_hebeb780c_0_0 
                                              >> 9U))) 
                                       & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_25)) 
                                      << 1U) | ((~ 
                                                 ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_26)) 
                                                  | (__VdfgRegularize_hebeb780c_0_0 
                                                     >> 8U))) 
                                                & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_26)))) 
                                 << 8U)) | (((((((~ 
                                                  ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_27)) 
                                                   | (__VdfgRegularize_hebeb780c_0_0 
                                                      >> 7U))) 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_27)) 
                                                << 3U) 
                                               | (((~ 
                                                    ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_28)) 
                                                     | (__VdfgRegularize_hebeb780c_0_0 
                                                        >> 6U))) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_28)) 
                                                  << 2U)) 
                                              | ((((~ 
                                                    ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_29)) 
                                                     | (__VdfgRegularize_hebeb780c_0_0 
                                                        >> 5U))) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_29)) 
                                                  << 1U) 
                                                 | ((~ 
                                                     ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_30)) 
                                                      | (__VdfgRegularize_hebeb780c_0_0 
                                                         >> 4U))) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_30)))) 
                                             << 4U) 
                                            | (((((~ 
                                                   ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_31)) 
                                                    | (__VdfgRegularize_hebeb780c_0_0 
                                                       >> 3U))) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_31)) 
                                                 << 3U) 
                                                | (((~ 
                                                     ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_32)) 
                                                      | (__VdfgRegularize_hebeb780c_0_0 
                                                         >> 2U))) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_32)) 
                                                   << 2U)) 
                                               | ((((~ 
                                                     ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_33)) 
                                                      | (__VdfgRegularize_hebeb780c_0_0 
                                                         >> 1U))) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_33)) 
                                                   << 1U) 
                                                  | ((~ 
                                                      ((~ (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_34)) 
                                                       | __VdfgRegularize_hebeb780c_0_0)) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_hebeb780c_0_34)))))));
}

void Ventry_precheck_tb___024root___act_sequent__TOP__0(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__1(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__2(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__3(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__4(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__5(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__6(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__7(Ventry_precheck_tb___024root* vlSelf);
void Ventry_precheck_tb___024root___act_sequent__TOP__8(Ventry_precheck_tb___024root* vlSelf);

void Ventry_precheck_tb___024root___eval_act(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_act\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        Ventry_precheck_tb___024root___act_sequent__TOP__0(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__1(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__2(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__3(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__4(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__5(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__6(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__7(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__8(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__9(vlSelf);
    }
}

void Ventry_precheck_tb___024root___eval_nba(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_nba\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Ventry_precheck_tb___024root___act_sequent__TOP__0(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__1(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__2(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__3(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__4(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__5(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__6(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__7(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__8(vlSelf);
        Ventry_precheck_tb___024root___act_sequent__TOP__9(vlSelf);
    }
}

void Ventry_precheck_tb___024root___timing_resume(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___timing_resume\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Ventry_precheck_tb___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

void Ventry_precheck_tb___024root___eval_triggers_vec__act(Ventry_precheck_tb___024root* vlSelf);
#ifdef VL_DEBUG
VL_ATTR_COLD void Ventry_precheck_tb___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
bool Ventry_precheck_tb___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

bool Ventry_precheck_tb___024root___eval_phase__act(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_phase__act\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    Ventry_precheck_tb___024root___eval_triggers_vec__act(vlSelf);
    Ventry_precheck_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Ventry_precheck_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Ventry_precheck_tb___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Ventry_precheck_tb___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Ventry_precheck_tb___024root___timing_resume(vlSelf);
        Ventry_precheck_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Ventry_precheck_tb___024root___eval_phase__inact(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_phase__inact\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("tb/entry_precheck_tb.sv", 4, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Ventry_precheck_tb___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Ventry_precheck_tb___024root___eval_phase__nba(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_phase__nba\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Ventry_precheck_tb___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Ventry_precheck_tb___024root___eval_nba(vlSelf);
        Ventry_precheck_tb___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Ventry_precheck_tb___024root___eval(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Ventry_precheck_tb___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("tb/entry_precheck_tb.sv", 4, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("tb/entry_precheck_tb.sv", 4, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Ventry_precheck_tb___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("tb/entry_precheck_tb.sv", 4, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Ventry_precheck_tb___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Ventry_precheck_tb___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Ventry_precheck_tb___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Ventry_precheck_tb___024root___eval_debug_assertions(Ventry_precheck_tb___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Ventry_precheck_tb___024root___eval_debug_assertions\n"); );
    Ventry_precheck_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
